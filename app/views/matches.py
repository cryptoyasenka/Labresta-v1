"""Match review blueprint: list, filter, sort, paginate, confirm/reject, manual match, rules CRUD, export."""

from datetime import datetime, timezone

from flask import Blueprint, Response, current_app, jsonify, redirect, render_template, request, send_file, url_for
from flask_login import current_user, login_required
from sqlalchemy import asc, desc, nulls_last
from sqlalchemy.orm import joinedload

import json
import re

from app.extensions import db
from app.models.catalog import PromProduct
from app.models.match_rule import MatchRule
from app.models.product_match import ProductMatch
from app.models.supplier import Supplier
from app.models.supplier_product import SupplierProduct
from app.services.audit_service import log_action
from app.services.matcher import (
    CONFIDENCE_HIGH,
    CONFIDENCE_MEDIUM,
    find_match_for_product,
    run_matching_for_supplier,
)

matches_bp = Blueprint("matches", __name__)


def _pp_already_claimed(prom_product_id: int, exclude_match_id: int | None = None) -> ProductMatch | None:
    """Return existing confirmed/manual match on this pp, or None.

    Enforces the 1:1 invariant (one pp ↔ one active supplier match).
    Pass exclude_match_id when the caller is the match being confirmed
    itself (so we don't flag the match against itself).
    """
    q = ProductMatch.query.filter(
        ProductMatch.prom_product_id == prom_product_id,
        ProductMatch.status.in_(("confirmed", "manual")),
    )
    if exclude_match_id is not None:
        q = q.filter(ProductMatch.id != exclude_match_id)
    return q.first()


def _pp_claim_error(existing: ProductMatch) -> tuple:
    sp = existing.supplier_product
    sp_name = sp.name if sp else f"sp#{existing.supplier_product_id}"
    return jsonify({
        "status": "error",
        "code": "prom_already_claimed",
        "message": (
            f"Этот каталожный товар уже подтверждён с поставщика «{sp_name}» "
            f"(match #{existing.id}). Сначала отмените тот матч."
        ),
        "existing_match_id": existing.id,
    }), 409


def _cleanup_other_candidates(supplier_product_id: int, keep_match_id: int) -> int:
    """Delete all candidate matches for a supplier product except the confirmed one.

    Called after confirming/manual-matching to remove orphaned candidates
    so they don't clutter the review UI or get re-processed.

    Returns count of deleted candidates.
    """
    orphans = ProductMatch.query.filter(
        ProductMatch.supplier_product_id == supplier_product_id,
        ProductMatch.id != keep_match_id,
        ProductMatch.status == "candidate",
    ).all()
    count = len(orphans)
    for m in orphans:
        db.session.delete(m)
    return count


def _build_match_query():
    """Build filtered/sorted match query from request args. Returns (query, filters_dict)."""
    status = request.args.get("status", "all")
    confidence = request.args.get("confidence", "all")
    availability = request.args.get("availability", "all")
    supplier_id = request.args.get("supplier_id", "all")
    search = request.args.get("search", "").strip()
    sort_col = request.args.get("sort", "score")
    # Default: highest score first — matches the review flow (confirm easy
    # 100% first, then drill into uncertain rows).
    order = request.args.get("order", "desc")
    per_page = request.args.get("per_page", 25, type=int)
    margin_below_raw = request.args.get("margin_below", "").strip()
    margin_below: float | None = None
    if margin_below_raw:
        try:
            margin_below = float(margin_below_raw)
            if margin_below < 0:
                margin_below = None
        except (TypeError, ValueError):
            margin_below = None

    if per_page not in (25, 50, 100):
        per_page = 25

    query = ProductMatch.query.options(
        joinedload(ProductMatch.supplier_product).joinedload(SupplierProduct.supplier),
        joinedload(ProductMatch.prom_product),
    )

    if status and status != "all":
        query = query.filter(ProductMatch.status == status)

    if confidence and confidence != "all":
        if confidence == "high":
            query = query.filter(ProductMatch.score >= CONFIDENCE_HIGH)
        elif confidence == "medium":
            query = query.filter(
                ProductMatch.score >= CONFIDENCE_MEDIUM,
                ProductMatch.score < CONFIDENCE_HIGH,
            )
        elif confidence == "low":
            query = query.filter(ProductMatch.score < CONFIDENCE_MEDIUM)

    if availability and availability != "all":
        if availability == "available":
            query = query.filter(ProductMatch.supplier_product.has(SupplierProduct.available == True))  # noqa: E712
        elif availability == "unavailable":
            query = query.filter(ProductMatch.supplier_product.has(SupplierProduct.available == False))  # noqa: E712

    if supplier_id and supplier_id != "all":
        try:
            sid = int(supplier_id)
        except (TypeError, ValueError):
            sid = None
        if sid is not None:
            query = query.filter(
                ProductMatch.supplier_product.has(SupplierProduct.supplier_id == sid)
            )

    # Always hide matches whose SP is ignored — operator explicitly opted them
    # out of the catalog. /products/supplier?show_ignored=1 stays the only
    # surface where they're visible.
    query = query.filter(
        ProductMatch.supplier_product.has(SupplierProduct.ignored == False)  # noqa: E712
    )

    if search:
        search_term = f"%{search}%"
        query = query.join(
            SupplierProduct, ProductMatch.supplier_product_id == SupplierProduct.id
        ).join(
            PromProduct, ProductMatch.prom_product_id == PromProduct.id
        ).filter(
            db.or_(
                SupplierProduct.name.ilike(search_term),
                SupplierProduct.article.ilike(search_term),
                PromProduct.name.ilike(search_term),
                PromProduct.article.ilike(search_term),
            )
        )

    # Hide "dead" candidates — ones whose prom_product is already claimed by
    # a confirmed/manual match. Backend will refuse to confirm them anyway
    # (1 pp ↔ 1 SP invariant), so surfacing them just wastes operator time.
    # Pass ?show_claimed=1 to inspect them (e.g. to bulk-reject).
    show_claimed = request.args.get("show_claimed", "0") == "1"
    if not show_claimed:
        claimed_pp_ids = db.session.query(ProductMatch.prom_product_id).filter(
            ProductMatch.status.in_(("confirmed", "manual"))
        )
        query = query.filter(
            db.or_(
                ProductMatch.status != "candidate",
                ~ProductMatch.prom_product_id.in_(claimed_pp_ids),
            )
        )

    sort_map = {
        "score": ProductMatch.score,
        "status": ProductMatch.status,
        "created_at": ProductMatch.created_at,
        # Per-match discount override column. NULLs (use supplier default)
        # should always sort last regardless of direction, otherwise a single
        # click sends the user to a page of "—" rows.
        "discount_percent": ProductMatch.discount_percent,
    }
    sort_column = sort_map.get(sort_col, ProductMatch.score)
    sort_func = asc if order == "asc" else desc
    if sort_col == "discount_percent":
        query = query.order_by(nulls_last(sort_func(sort_column)))
    else:
        query = query.order_by(sort_func(sort_column))

    filters = {
        "status": status,
        "confidence": confidence,
        "availability": availability,
        "supplier_id": supplier_id,
        "search": search,
        "sort": sort_col,
        "order": order,
        "per_page": per_page,
        "show_claimed": show_claimed,
        "margin_below": margin_below,
        "margin_below_raw": margin_below_raw,
    }
    return query, filters


@matches_bp.route("/")
@login_required
def review():
    """Main match review page with filtering, sorting, and pagination."""
    from app.services.pricing import compute_match_pricing

    query, filters = _build_match_query()
    page = request.args.get("page", 1, type=int)

    if filters["margin_below"] is not None:
        # Margin depends on per_brand + clamp — can't express in SQL. Materialize
        # the filtered query, compute margin per row, then paginate in Python.
        # Filter by margin at BASE discount (pre-clamp) so the operator sees all
        # items where the min-margin rule triggered or would trigger, not just
        # the ones the clamp couldn't save.
        all_items = query.all()
        threshold = float(filters["margin_below"])
        kept: list = []
        pricing_map: dict[int, dict] = {}
        for m in all_items:
            p = compute_match_pricing(m)
            if p is None:
                continue
            sp = m.supplier_product
            supplier = sp.supplier
            rate = float(getattr(supplier, "eur_rate_uah", 51.15) or 51.15)
            cost_rate_v = float(getattr(supplier, "cost_rate", 0.75) or 0.75)
            retail_eur = sp.price_cents / 100.0
            margin_at_base = retail_eur * (1 - cost_rate_v - p["base_discount"] / 100.0) * rate
            if margin_at_base < threshold:
                kept.append(m)
                pricing_map[m.id] = p
        per_page = filters["per_page"]
        total = len(kept)
        pages = max(1, (total + per_page - 1) // per_page)
        if page < 1:
            page = 1
        if page > pages and total > 0:
            args = request.args.to_dict(flat=True)
            args["page"] = pages
            return redirect(url_for("matches.review", **args))
        start = (page - 1) * per_page
        items = kept[start : start + per_page]
        pagination = _InMemoryPagination(items=items, page=page, per_page=per_page, total=total, pages=pages)
    else:
        pagination = db.paginate(query, page=page, per_page=filters["per_page"], error_out=False)
        # After bulk-confirm the list shrinks — redirect to the last existing page
        # instead of showing 404 / empty state on page=N.
        if page > 1 and not pagination.items and pagination.pages >= 1:
            args = request.args.to_dict(flat=True)
            args["page"] = pagination.pages
            return redirect(url_for("matches.review", **args))
        pricing_map = {m.id: compute_match_pricing(m) for m in pagination.items}

    # Count supplier products matching the search but without any match row.
    # Helps the operator realise that /matches hides unmatched SP — surfaces
    # a link to /products/supplier?match_state=none.
    unmatched_sp_count = 0
    if filters["search"]:
        from sqlalchemy import func as sa_func
        matched_sp_ids = db.session.query(ProductMatch.supplier_product_id).distinct()
        search_term_uc = f"%{filters['search']}%"
        unmatched_sp_count = db.session.execute(
            db.select(sa_func.count(SupplierProduct.id)).where(
                db.or_(
                    SupplierProduct.name.ilike(search_term_uc),
                    SupplierProduct.article.ilike(search_term_uc),
                ),
                SupplierProduct.is_deleted == False,  # noqa: E712
                SupplierProduct.id.not_in(matched_sp_ids),
            )
        ).scalar() or 0

    # Support ?manual_for_sp=<id> — lets /products/supplier trigger the manual
    # match modal for a specific SP instead of fuzzy-matching by name (which
    # found the wrong SP when several SPs shared a common name prefix).
    auto_manual_sp = None
    manual_for_sp_id = request.args.get("manual_for_sp", type=int)
    if manual_for_sp_id:
        auto_manual_sp = db.session.get(SupplierProduct, manual_for_sp_id)

    suppliers_list = db.session.execute(
        db.select(Supplier).order_by(Supplier.name)
    ).scalars().all()

    return render_template(
        "matches/review.html",
        matches=pagination.items,
        pagination=pagination,
        filters=filters,
        confidence_high=CONFIDENCE_HIGH,
        confidence_medium=CONFIDENCE_MEDIUM,
        unmatched_sp_count=unmatched_sp_count,
        auto_manual_sp=auto_manual_sp,
        suppliers_list=suppliers_list,
        pricing_map=pricing_map,
    )


class _InMemoryPagination:
    """Drop-in replacement for flask_sqlalchemy.Pagination when we need to
    filter by a Python-computed column (margin_uah) and still render the
    standard pagination controls.
    """
    def __init__(self, items, page, per_page, total, pages):
        self.items = items
        self.page = page
        self.per_page = per_page
        self.total = total
        self.pages = pages

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    @property
    def prev_num(self):
        return self.page - 1

    @property
    def next_num(self):
        return self.page + 1

    def iter_pages(self, left_edge=1, left_current=2, right_current=3, right_edge=1):
        last = 0
        for num in range(1, self.pages + 1):
            if (
                num <= left_edge
                or (num > self.page - left_current - 1 and num < self.page + right_current)
                or num > self.pages - right_edge
            ):
                if last + 1 != num:
                    yield None
                yield num
                last = num


@matches_bp.route("/<int:match_id>/confirm", methods=["POST"])
@login_required
def confirm_match(match_id):
    """AJAX endpoint to confirm a match."""
    match = db.get_or_404(ProductMatch, match_id)

    existing = _pp_already_claimed(match.prom_product_id, exclude_match_id=match.id)
    if existing:
        return _pp_claim_error(existing)

    match.status = "confirmed"
    match.confirmed_at = datetime.now(timezone.utc)
    match.confirmed_by = current_user.name
    current_user.matches_processed += 1
    cleaned = _cleanup_other_candidates(match.supplier_product_id, match.id)
    log_action("confirm", match_id=match.id,
               supplier_product_id=match.supplier_product_id,
               prom_product_id=match.prom_product_id,
               details={"score": match.score, "candidates_removed": cleaned})
    db.session.commit()

    return jsonify({"status": "ok", "new_status": "confirmed", "candidates_removed": cleaned})


@matches_bp.route("/<int:match_id>/confirm-update", methods=["POST"])
@login_required
def confirm_and_update(match_id):
    """Confirm match and update catalog product name from supplier.

    Updates the UA name. For RU name, replaces the model number
    portion if the change is just a model/article number difference.
    """
    match = db.get_or_404(ProductMatch, match_id)
    existing = _pp_already_claimed(match.prom_product_id, exclude_match_id=match.id)
    if existing:
        return _pp_claim_error(existing)

    supplier_product = match.supplier_product
    prom_product = match.prom_product

    old_name_ua = prom_product.name
    new_name_ua = supplier_product.name

    # Update UA name
    prom_product.name = new_name_ua

    # Try to update RU name: replace the changed part
    if prom_product.name_ru and old_name_ua != new_name_ua:
        prom_product.name_ru = _apply_name_diff(old_name_ua, new_name_ua, prom_product.name_ru)

    # Confirm the match
    match.status = "confirmed"
    match.confirmed_at = datetime.now(timezone.utc)
    match.confirmed_by = current_user.name
    match.name_synced = True
    current_user.matches_processed += 1
    cleaned = _cleanup_other_candidates(match.supplier_product_id, match.id)
    log_action("confirm_update", match_id=match.id,
               supplier_product_id=match.supplier_product_id,
               prom_product_id=match.prom_product_id,
               details={"old_name": old_name_ua, "new_name": new_name_ua,
                         "name_ru": prom_product.name_ru})
    db.session.commit()

    return jsonify({
        "status": "ok",
        "new_status": "confirmed",
        "candidates_removed": cleaned,
        "name_updated": True,
        "old_name": old_name_ua,
        "new_name": new_name_ua,
        "name_ru": prom_product.name_ru,
    })


@matches_bp.route("/<int:match_id>/details")
@login_required
def match_details(match_id):
    """AJAX endpoint returning detailed comparison data for a match."""
    match = db.get_or_404(ProductMatch, match_id)
    sp = match.supplier_product
    pp = match.prom_product

    sp_images = json.loads(sp.images) if sp.images else []
    pp_images = json.loads(pp.images) if pp.images else []
    sp_params = json.loads(sp.params) if sp.params else {}

    return jsonify({
        "supplier": {
            "name": sp.name,
            "brand": sp.brand,
            "model": sp.model,
            "article": sp.article,
            "description": sp.description,
            "image_url": sp.image_url,
            "images": sp_images,
            "params": sp_params,
        },
        "catalog": {
            "name": pp.name,
            "name_ru": pp.name_ru,
            "brand": pp.brand,
            "model": pp.model,
            "article": pp.article,
            "display_article": pp.display_article,
            "description_ua": pp.description_ua,
            "description_ru": pp.description_ru,
            "image_url": pp.image_url,
            "images": pp_images,
            "page_url": pp.page_url,
        },
        "match": {
            "id": match.id,
            "score": match.score,
            "status": match.status,
            "name_synced": match.name_synced,
        },
    })


def _is_model_token(token: str) -> bool:
    """Return True if token looks like a model/article/size (safe to replace in RU).

    Safe tokens: latin letters, digits, sizes like 200x400, codes like FTS137UTE,
    parenthesized numbers like (220). Unsafe: Cyrillic words — they differ between
    UA and RU and must not be transplanted.
    """
    clean = token.strip("(),.:;")
    if not clean:
        return False
    # Pure digits or digit patterns (220, 100)
    if re.fullmatch(r"\d+", clean):
        return True
    # Size patterns: 200x400, 150x350
    if re.fullmatch(r"\d+x\d+", clean, re.IGNORECASE):
        return True
    # Latin model codes: FTS137UTE, BCB05, SHE50075 (at least one letter + one digit)
    if re.fullmatch(r"[A-Za-z0-9/+._-]+", clean):
        has_letter = any(c.isalpha() for c in clean)
        has_digit = any(c.isdigit() for c in clean)
        if has_letter and has_digit:
            return True
    return False


def _apply_name_diff(old_ua: str, new_ua: str, old_ru: str) -> str:
    """Apply the UA name change to the RU name, but only for model/article tokens.

    Only replaces tokens that look like model numbers, article codes, or sizes
    (latin+digits). Cyrillic words are never touched because UA and RU use
    different vocabulary for the same meaning (e.g. пакунок vs упаковка).
    """
    old_tokens = old_ua.split()
    new_tokens = new_ua.split()

    # Find tokens that changed AND both old and new are model-like.
    # Both sides must be model tokens to avoid positional misalignment
    # (e.g. when word count differs, "100" can align with "пакунок").
    replacements = {}
    for i in range(min(len(old_tokens), len(new_tokens))):
        if (old_tokens[i] != new_tokens[i]
                and _is_model_token(old_tokens[i])
                and _is_model_token(new_tokens[i])):
            replacements[old_tokens[i]] = new_tokens[i]

    if not replacements:
        return old_ru

    result = old_ru
    for old_tok, new_tok in replacements.items():
        pattern = re.compile(r"(?<![A-Za-z0-9])" + re.escape(old_tok) + r"(?![A-Za-z0-9])")
        result = pattern.sub(new_tok, result)

    return result


@matches_bp.route("/<int:match_id>/reject", methods=["POST"])
@login_required
def reject_match(match_id):
    """AJAX endpoint to reject a match and attempt re-matching."""
    match = db.get_or_404(ProductMatch, match_id)

    supplier_product = match.supplier_product
    rejected_prom_id = match.prom_product_id
    rejected_match_id = match.id
    rejected_sp_id = match.supplier_product_id

    db.session.delete(match)
    db.session.flush()

    new_match = find_match_for_product(
        supplier_product, exclude_prom_ids=[rejected_prom_id]
    )
    new_candidate_id = None
    if new_match:
        db.session.add(new_match)
        db.session.flush()
        new_candidate_id = new_match.id

    log_action("reject", match_id=rejected_match_id,
               supplier_product_id=rejected_sp_id,
               prom_product_id=rejected_prom_id,
               details={"new_candidate_id": new_candidate_id})
    db.session.commit()

    return jsonify({
        "status": "ok",
        "new_status": "rejected",
        "new_candidate_id": new_candidate_id,
    })


@matches_bp.route("/<int:match_id>/unconfirm", methods=["POST"])
@login_required
def unconfirm_match(match_id):
    """Revert a confirmed/manual match back to candidate status.

    Used when an operator confirmed a match by mistake. Note: sibling
    candidates were deleted by _cleanup_other_candidates on the original
    confirm, so after unconfirming, this match becomes the only candidate
    for its supplier product. If the operator wants a different match,
    they should use 'Сопоставить вручную' to pick another catalog entry.
    """
    match = db.get_or_404(ProductMatch, match_id)

    if match.status not in ("confirmed", "manual"):
        return jsonify({
            "status": "error",
            "message": "Отменить можно только подтвержденный или ручной матч",
        }), 400

    old_status = match.status
    match.status = "candidate"
    match.confirmed_at = None
    match.confirmed_by = None
    # NOTE: do NOT clear name_synced here. It tracks whether the catalog
    # product name was updated from the supplier, which is a mutation on
    # prom_product and is NOT rolled back by this endpoint. Clearing the
    # flag would leave the DB inconsistent (PromProduct has the new name
    # but the match says it wasn't synced).
    if current_user.matches_processed and current_user.matches_processed > 0:
        current_user.matches_processed -= 1
    log_action("unconfirm", match_id=match.id,
               supplier_product_id=match.supplier_product_id,
               prom_product_id=match.prom_product_id,
               details={"old_status": old_status})
    db.session.commit()

    return jsonify({"status": "ok", "new_status": "candidate"})


@matches_bp.route("/<int:match_id>/unpublish", methods=["POST"])
@login_required
def unpublish_match(match_id):
    """Remove match from YML feed (published=False) without losing the match."""
    match = db.get_or_404(ProductMatch, match_id)
    if match.status not in ("confirmed", "manual"):
        return jsonify({
            "status": "error",
            "message": "Снять с фида можно только подтверждённый или ручной матч",
        }), 400
    if not match.published:
        return jsonify({"status": "ok", "already": True, "published": False})
    match.published = False
    match.in_feed = False
    log_action("unpublish", match_id=match.id,
               supplier_product_id=match.supplier_product_id,
               prom_product_id=match.prom_product_id)
    db.session.commit()
    return jsonify({"status": "ok", "published": False, "in_feed": False})


@matches_bp.route("/<int:match_id>/republish", methods=["POST"])
@login_required
def republish_match(match_id):
    """Return match to YML feed (published=True). in_feed updates on next regen."""
    match = db.get_or_404(ProductMatch, match_id)
    if match.status not in ("confirmed", "manual"):
        return jsonify({
            "status": "error",
            "message": "Вернуть в фид можно только подтверждённый или ручной матч",
        }), 400
    if match.published:
        return jsonify({"status": "ok", "already": True, "published": True})
    match.published = True
    log_action("republish", match_id=match.id,
               supplier_product_id=match.supplier_product_id,
               prom_product_id=match.prom_product_id)
    db.session.commit()
    return jsonify({"status": "ok", "published": True})


@matches_bp.route("/regenerate-feed", methods=["POST"])
@login_required
def regenerate_feed():
    """Regenerate the YML feed on demand and return stats."""
    from app.services.yml_generator import regenerate_yml_feed
    try:
        result = regenerate_yml_feed()
    except Exception as exc:  # pragma: no cover — surfaced to UI
        return jsonify({"status": "error", "message": str(exc)}), 500
    log_action("regenerate_feed", details={
        "total": result["total"],
        "available": result["available"],
        "unavailable": result["unavailable"],
    })
    return jsonify({"status": "ok", **result})


@matches_bp.route("/rematch", methods=["POST"])
@login_required
def rematch():
    """Queue a background rematch job and return `job_id` immediately.

    Body: {"supplier_id": <int>}  — single supplier.
          {"supplier_id": "all"}  — all enabled suppliers.

    Response: 202 Accepted `{status: "started", job_id: str}`.
              409 Conflict `{status: "busy", active_job_id: str}` if another
              rematch is already running.

    The UI then polls `GET /matches/rematch/status/<job_id>` every ~2 s.

    Invariant: `confirmed` and `manual` matches are never touched. They are
    protected both by the job's DELETE WHERE (status IN ('candidate','rejected'))
    and by `run_matching_for_supplier` skipping supplier products that already
    have confirmed/manual. Also enforced by `uq_match_prom_confirmed` index.
    """
    data = request.get_json(silent=True) or {}
    scope_raw = data.get("supplier_id")
    if scope_raw is None:
        return jsonify({"status": "error", "message": "supplier_id required"}), 400

    # Validate scope before spawning the thread so errors are surfaced sync.
    if scope_raw == "all":
        any_enabled = db.session.execute(
            db.select(db.func.count(Supplier.id)).where(Supplier.is_enabled == True)  # noqa: E712
        ).scalar() or 0
        if not any_enabled:
            return jsonify({"status": "error", "message": "Нет активных поставщиков"}), 400
    else:
        try:
            sid = int(scope_raw)
        except (TypeError, ValueError):
            return jsonify({"status": "error", "message": "supplier_id must be int or 'all'"}), 400
        if not db.session.get(Supplier, sid):
            return jsonify({"status": "error", "message": f"Supplier #{sid} not found"}), 404
        scope_raw = sid

    from app.services import rematch_job

    user_id = current_user.id if current_user and current_user.is_authenticated else None
    user_name = current_user.name if current_user and current_user.is_authenticated else None
    job_id, active = rematch_job.create_job(scope_raw, user_id, user_name)
    if job_id is None:
        return jsonify({
            "status": "busy",
            "message": "Rematch уже запущен",
            "active_job_id": active["id"] if active else None,
        }), 409

    # In tests we may want to run synchronously — honour that toggle.
    if current_app.config.get("REMATCH_SYNC_MODE"):
        rematch_job.run_job(current_app._get_current_object(), job_id)
    else:
        rematch_job.start_thread(current_app._get_current_object(), job_id)
    return jsonify({"status": "started", "job_id": job_id}), 202


@matches_bp.route("/rematch/status/active", methods=["GET"])
@login_required
def rematch_status_active():
    """Return the currently running (or pending) rematch job, if any."""
    from app.services import rematch_job
    job = rematch_job.get_active_job()
    if not job:
        return jsonify({"status": "none"})
    return jsonify({"status": "ok", "job": job})


@matches_bp.route("/rematch/status/<job_id>", methods=["GET"])
@login_required
def rematch_status(job_id):
    """Return the current state of a rematch job (running / done / error)."""
    from app.services import rematch_job
    job = rematch_job.get_job(job_id)
    if not job:
        return jsonify({"status": "not_found"}), 404
    return jsonify({"status": "ok", "job": job})


def _parse_match_ids(data: dict) -> list[int] | None:
    """Read optional match_ids list from JSON body. Empty/missing → None (bulk)."""
    raw = data.get("match_ids") if isinstance(data, dict) else None
    if not raw:
        return None
    if not isinstance(raw, list):
        return None
    out: list[int] = []
    for item in raw:
        try:
            out.append(int(item))
        except (TypeError, ValueError):
            continue
    return out or None


@matches_bp.route("/sync-prices", methods=["POST"])
@login_required
def sync_prices_feed():
    """Generate narrow price-only YML and bump price_synced_at.

    Body (optional): {"match_ids": [123, 456]} — restrict to these matches.
    No body / empty list = bulk sync of all published confirmed/manual matches.
    """
    from app.services.yml_generator import sync_prices
    data = request.get_json(silent=True) or {}
    match_ids = _parse_match_ids(data)
    try:
        result = sync_prices(match_ids=match_ids)
    except Exception as exc:  # pragma: no cover — surfaced to UI
        return jsonify({"status": "error", "message": str(exc)}), 500
    log_action("sync_prices", details={
        "total": result["total"],
        "skipped": result["skipped"],
        "scope": "bulk" if match_ids is None else f"ids:{len(match_ids)}",
    })
    return jsonify({"status": "ok", **result})


@matches_bp.route("/sync-availability", methods=["POST"])
@login_required
def sync_availability_feed():
    """Generate narrow availability-only YML and bump availability_synced_at.

    Body (optional): {"match_ids": [123, 456]} — restrict to these matches.
    No body / empty list = bulk sync of all published confirmed/manual matches.
    """
    from app.services.yml_generator import sync_availability
    data = request.get_json(silent=True) or {}
    match_ids = _parse_match_ids(data)
    try:
        result = sync_availability(match_ids=match_ids)
    except Exception as exc:  # pragma: no cover — surfaced to UI
        return jsonify({"status": "error", "message": str(exc)}), 500
    log_action("sync_availability", details={
        "total": result["total"],
        "available": result["available"],
        "unavailable": result["unavailable"],
        "scope": "bulk" if match_ids is None else f"ids:{len(match_ids)}",
    })
    return jsonify({"status": "ok", **result})


@matches_bp.route("/regenerate-custom", methods=["POST"])
@login_required
def regenerate_custom():
    """Generate a custom-selection YML feed and return its public URL.

    Body: {"match_ids": [int, ...], "name": "optional human label"}.
    Token is deterministic over the sorted unique match_ids — same selection
    always resolves to the same URL.
    """
    from app.services.yml_generator import regenerate_custom_feed

    data = request.get_json(silent=True) or {}
    match_ids = _parse_match_ids(data)
    if not match_ids:
        return jsonify({
            "status": "error",
            "message": "Не выбрано ни одной позиции для фида.",
        }), 400
    name = (data.get("name") or "").strip() or None

    try:
        result = regenerate_custom_feed(match_ids=match_ids, name=name)
    except Exception as exc:  # pragma: no cover — surfaced to UI
        return jsonify({"status": "error", "message": str(exc)}), 500

    log_action("regenerate_custom_feed", details={
        "token": result["token"],
        "name": name,
        "match_count": len(match_ids),
        "available": result["available"],
        "unavailable": result["unavailable"],
    })

    feed_url = url_for(
        "feed.serve_custom_yml", token=result["token"], _external=True
    )
    return jsonify({"status": "ok", "url": feed_url, **result})


@matches_bp.route("/<int:match_id>/update-prom", methods=["POST"])
@login_required
def update_prom_fields(match_id):
    """Manually update catalog product fields (name UA/RU, description UA/RU).

    Used from the details modal when the operator spots a typo or wants to
    improve the Horoshop catalog entry. Only updates fields that are present
    in the request body AND non-null — empty strings clear the field.
    Changes go into prom_product and will be pushed to Horoshop on the next
    YML feed regeneration (name + description are written into the feed).
    """
    match = db.get_or_404(ProductMatch, match_id)
    pp = match.prom_product

    data = request.get_json(silent=True) or {}
    updated = {}

    if "name" in data:
        new_val = (data["name"] or "").strip()
        if not new_val:
            return jsonify({"status": "error", "message": "Название UA не может быть пустым"}), 400
        if len(new_val) > 500:
            return jsonify({"status": "error", "message": "Название UA превышает 500 символов"}), 400
        if new_val != pp.name:
            pp.name = new_val
            updated["name"] = new_val

    if "name_ru" in data:
        new_val = (data["name_ru"] or "").strip() or None
        if new_val and len(new_val) > 500:
            return jsonify({"status": "error", "message": "Название RU превышает 500 символов"}), 400
        if new_val != pp.name_ru:
            pp.name_ru = new_val
            updated["name_ru"] = new_val

    if "description_ua" in data:
        new_val = (data["description_ua"] or "").strip() or None
        if new_val != pp.description_ua:
            pp.description_ua = new_val
            updated["description_ua"] = new_val

    if "description_ru" in data:
        new_val = (data["description_ru"] or "").strip() or None
        if new_val != pp.description_ru:
            pp.description_ru = new_val
            updated["description_ru"] = new_val

    if updated:
        match.name_synced = True
        log_action("update_prom", match_id=match.id,
                   supplier_product_id=match.supplier_product_id,
                   prom_product_id=pp.id,
                   details={"updated_fields": updated})
        db.session.commit()

    return jsonify({
        "status": "ok",
        "updated": updated,
        "prom_id": pp.id,
    })


@matches_bp.route("/<int:match_id>/discount", methods=["POST"])
@login_required
def set_discount(match_id):
    """AJAX endpoint to set or clear per-product discount override."""
    match = db.get_or_404(ProductMatch, match_id)

    # Only allow discount on confirmed/manual matches
    if match.status not in ("confirmed", "manual"):
        return jsonify({"status": "error", "message": "Скидка доступна только для подтвержденных матчей"}), 400

    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No data provided"}), 400

    discount = data.get("discount_percent")

    if discount is not None:
        try:
            discount = float(discount)
        except (TypeError, ValueError):
            return jsonify({"status": "error", "message": "Некорректное значение скидки"}), 400
        if not (0 <= discount <= 100):
            return jsonify({"status": "error", "message": "Скидка должна быть от 0 до 100%"}), 400

    old_discount = match.discount_percent
    match.discount_percent = discount  # None clears the override
    log_action("set_discount", match_id=match.id,
               supplier_product_id=match.supplier_product_id,
               prom_product_id=match.prom_product_id,
               details={"old_discount": old_discount, "new_discount": discount})
    db.session.commit()

    return jsonify({
        "status": "ok",
        "discount_percent": match.discount_percent,
    })


@matches_bp.route("/bulk-action", methods=["POST"])
@login_required
def bulk_action():
    """AJAX endpoint for bulk confirm/reject."""
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No data provided"}), 400

    action = data.get("action")
    ids = data.get("ids", [])

    if action not in ("confirm", "reject", "recalc_discount", "clamp_margin"):
        return jsonify({"status": "error", "message": "Invalid action"}), 400

    if not ids:
        return jsonify({"status": "error", "message": "No matches selected"}), 400

    dry_run = bool(data.get("dry_run"))
    # Eager-load sp + supplier to avoid lazy SELECT per match in the loop
    # (recalc_discount / clamp_margin / supplier_product_name on skip).
    matches = ProductMatch.query.options(
        joinedload(ProductMatch.supplier_product).joinedload(SupplierProduct.supplier),
    ).filter(ProductMatch.id.in_(ids)).all()
    processed = 0
    skipped_claimed: list[dict] = []
    preview: list[dict] = []

    # Bulk preloads for action="confirm" — kill N+1 from _pp_already_claimed
    # and _cleanup_other_candidates running once per match in the loop.
    claimed_by_pp: dict[int, ProductMatch] = {}
    orphans_by_sp: dict[int, list[ProductMatch]] = {}
    if action == "confirm" and matches:
        match_ids = {m.id for m in matches}
        pp_ids = {m.prom_product_id for m in matches}
        sp_ids = {m.supplier_product_id for m in matches}

        # Single SELECT for all "is some other confirmed/manual match
        # already claiming any of these pp_ids?" lookups.
        claimed_rows = ProductMatch.query.filter(
            ProductMatch.prom_product_id.in_(pp_ids),
            ProductMatch.status.in_(("confirmed", "manual")),
            ProductMatch.id.notin_(match_ids),
        ).all()
        for row in claimed_rows:
            # Keep the first claim per pp_id — _pp_already_claimed used .first()
            # so callers only ever inspect one row.
            claimed_by_pp.setdefault(row.prom_product_id, row)

        # Single SELECT for all candidate orphans across the sp_ids being
        # confirmed. _cleanup_other_candidates filters by != keep_match_id
        # at use-time so we keep ALL candidates and let the per-match step
        # exclude its own id.
        orphan_rows = ProductMatch.query.filter(
            ProductMatch.supplier_product_id.in_(sp_ids),
            ProductMatch.status == "candidate",
        ).all()
        for row in orphan_rows:
            orphans_by_sp.setdefault(row.supplier_product_id, []).append(row)

    for match in matches:
        if action == "confirm":
            existing = claimed_by_pp.get(match.prom_product_id)
            if existing is not None and existing.id != match.id:
                skipped_claimed.append({
                    "match_id": match.id,
                    "prom_product_id": match.prom_product_id,
                    "existing_match_id": existing.id,
                })
                continue
            match.status = "confirmed"
            match.confirmed_at = datetime.now(timezone.utc)
            match.confirmed_by = current_user.name
            current_user.matches_processed += 1
            # Inline _cleanup_other_candidates using preloaded orphans.
            for orphan in orphans_by_sp.get(match.supplier_product_id, []):
                if orphan.id == match.id:
                    continue
                db.session.delete(orphan)
            # Reflect the new claim so a later match in the same batch
            # targeting the same pp_id sees it as claimed.
            claimed_by_pp[match.prom_product_id] = match
            processed += 1
        elif action == "reject":
            if match.status != "candidate":
                continue
            supplier_product = match.supplier_product
            rejected_prom_id = match.prom_product_id
            db.session.delete(match)
            db.session.flush()

            new_match = find_match_for_product(
                supplier_product, exclude_prom_ids=[rejected_prom_id]
            )
            if new_match:
                db.session.add(new_match)
            processed += 1
        elif action == "recalc_discount":
            if match.status not in ("confirmed", "manual"):
                continue
            sp = match.supplier_product
            if not sp or not sp.price_cents or sp.price_cents <= 0:
                continue
            supplier = sp.supplier
            rate = (supplier.eur_rate_uah or 51.15) if supplier else 51.15
            min_margin = float((supplier.min_margin_uah or 500.0) if supplier else 500.0)
            cost_rate_v = float((supplier.cost_rate or 0.75) if supplier else 0.75)
            from app.services.pricing import calculate_auto_discount
            new_d = float(calculate_auto_discount(
                sp.price_cents, rate,
                cost_rate=cost_rate_v, min_margin_uah=min_margin,
            ))
            if match.discount_percent != new_d:
                match.discount_percent = new_d
            processed += 1
        elif action == "clamp_margin":
            # Materializes the current effective discount (per_brand / flat +
            # min-margin clamp) into match.discount_percent so the UI column
            # "Скидка" shows the final rate. Matches with an existing override
            # are skipped — operator intent wins.
            if match.status not in ("confirmed", "manual"):
                continue
            if match.discount_percent is not None:
                continue  # manual override — do not touch
            from app.services.pricing import compute_match_pricing
            p = compute_match_pricing(match)
            if p is None:
                continue
            new_d = float(p["effective_discount"])
            old_d = match.discount_percent
            preview.append({
                "match_id": match.id,
                "supplier_product_name": match.supplier_product.name if match.supplier_product else "",
                "base_discount": p["base_discount"],
                "effective_discount": new_d,
                "margin_uah": round(p["margin_uah"], 2),
                "clamp_applied": p["clamp_applied"],
            })
            if not dry_run:
                match.discount_percent = new_d
                processed += 1

    if dry_run:
        return jsonify({
            "status": "ok",
            "dry_run": True,
            "preview": preview,
            "would_change": len(preview),
        })

    log_action(f"bulk_{action}",
               details={"match_ids": ids, "processed": processed,
                        "skipped_claimed": [s["match_id"] for s in skipped_claimed]})
    db.session.commit()

    return jsonify({
        "status": "ok",
        "processed": processed,
        "skipped_claimed": skipped_claimed,
        "preview": preview if action == "clamp_margin" else [],
    })


# ========== Catalog search for manual match modal ==========


@matches_bp.route("/search-catalog")
@login_required
def search_catalog():
    """AJAX endpoint for catalog product search (used in manual match modal)."""
    q = request.args.get("q", "").strip()
    if len(q) < 2 or len(q) > 200:
        return jsonify([])

    search_term = f"%{q}%"
    products = (
        PromProduct.query.filter(
            db.or_(
                PromProduct.name.ilike(search_term),
                PromProduct.article.ilike(search_term),
            )
        )
        .limit(20)
        .all()
    )

    results = []
    for p in products:
        results.append({
            "id": p.id,
            "name": p.name,
            "brand": p.brand or "",
            "model": p.model or "",
            "article": p.article or "",
            "price": f"{p.price / 100:.2f}" if p.price else "",
        })

    return jsonify(results)


# ========== Manual match ==========


@matches_bp.route("/mark-new/<int:sp_id>", methods=["POST"])
@login_required
def mark_for_catalog(sp_id):
    """Mark a supplier product as needing addition to the Horoshop catalog.

    Used when the manual-match search returns zero results — the product
    exists at the supplier but has no catalog counterpart. Rejects any
    existing candidate matches for this supplier product so they don't
    clutter the review queue.
    """
    sp = db.get_or_404(SupplierProduct, sp_id)

    if not sp.available:
        return jsonify({
            "status": "error",
            "message": "Товар не в наличии у поставщика",
        }), 400

    sp.needs_catalog_add = True

    # Reject remaining candidate matches — they're all wrong
    candidates = ProductMatch.query.filter(
        ProductMatch.supplier_product_id == sp_id,
        ProductMatch.status == "candidate",
    ).all()
    for m in candidates:
        m.status = "rejected"
        m.confirmed_by = "mark-new"

    log_action("mark_new", supplier_product_id=sp_id,
               details={"supplier_name": sp.name, "rejected_count": len(candidates)})
    db.session.commit()

    return jsonify({
        "status": "ok",
        "rejected_count": len(candidates),
    })


@matches_bp.route("/unmark-new/<int:sp_id>", methods=["POST"])
@login_required
def unmark_for_catalog(sp_id):
    """Remove the 'needs catalog add' flag from a supplier product."""
    sp = db.get_or_404(SupplierProduct, sp_id)
    sp.needs_catalog_add = False
    log_action("unmark_new", supplier_product_id=sp_id,
               details={"supplier_name": sp.name})
    db.session.commit()
    return jsonify({"status": "ok"})


@matches_bp.route("/manual", methods=["POST"])
@login_required
def manual_match():
    """Create a manual match between supplier product and catalog product."""
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No data provided"}), 400

    supplier_product_id = data.get("supplier_product_id")
    prom_product_id = data.get("prom_product_id")
    remember = data.get("remember", False)

    if not supplier_product_id or not prom_product_id:
        return jsonify({"status": "error", "message": "Missing product IDs"}), 400

    supplier_product = db.get_or_404(SupplierProduct, supplier_product_id)
    prom_product = db.get_or_404(PromProduct, prom_product_id)

    # Enforce 1 pp ↔ 1 active supplier match: if this pp is already claimed
    # by a DIFFERENT supplier product, refuse. The operator must first
    # unconfirm the existing match.
    existing_on_pp = ProductMatch.query.filter(
        ProductMatch.prom_product_id == prom_product_id,
        ProductMatch.supplier_product_id != supplier_product_id,
        ProductMatch.status.in_(("confirmed", "manual")),
    ).first()
    if existing_on_pp:
        return _pp_claim_error(existing_on_pp)

    # If this exact (supplier, prom) pair already has a non-candidate match,
    # treat it as "already matched" — clean up dangling candidates for the
    # same supplier product so the operator's queue refreshes cleanly, but
    # don't try to insert a duplicate (would hit UNIQUE constraint).
    existing_pair = ProductMatch.query.filter(
        ProductMatch.supplier_product_id == supplier_product_id,
        ProductMatch.prom_product_id == prom_product_id,
        ProductMatch.status.in_(["confirmed", "manual"]),
    ).first()
    if existing_pair:
        cleaned = ProductMatch.query.filter(
            ProductMatch.supplier_product_id == supplier_product_id,
            ProductMatch.status == "candidate",
        ).delete()
        db.session.commit()
        return jsonify({
            "status": "already_matched",
            "message": (
                f"Товар уже сопоставлен с этим каталожным товаром "
                f"(матч #{existing_pair.id}, статус={existing_pair.status}). "
                f"Очищено лишних кандидатов: {cleaned}."
            ),
            "match_id": existing_pair.id,
        }), 409

    # Delete all existing candidate matches for this supplier product
    ProductMatch.query.filter(
        ProductMatch.supplier_product_id == supplier_product_id,
        ProductMatch.status == "candidate",
    ).delete()
    db.session.flush()

    # Create manual match
    new_match = ProductMatch(
        supplier_product_id=supplier_product_id,
        prom_product_id=prom_product_id,
        score=100.0,
        status="manual",
        confirmed_at=datetime.now(timezone.utc),
        confirmed_by=current_user.name,
    )
    db.session.add(new_match)
    db.session.flush()

    # Optionally create a remembered rule
    if remember:
        rule = MatchRule(
            supplier_product_name_pattern=supplier_product.name,
            supplier_brand=supplier_product.brand,
            prom_product_id=prom_product_id,
            created_by=current_user.name,
        )
        db.session.add(rule)

    current_user.matches_processed += 1
    log_action("manual_match", match_id=new_match.id,
               supplier_product_id=supplier_product_id,
               prom_product_id=prom_product_id,
               details={"supplier_name": supplier_product.name,
                         "prom_name": prom_product.name,
                         "remember": remember})
    db.session.commit()

    return jsonify({"status": "ok", "match_id": new_match.id})


# ========== Rebind (Phase E) ==========


@matches_bp.route("/search-suppliers")
@login_required
def search_suppliers():
    """AJAX endpoint: search SupplierProduct by name/external_id/article/brand.

    Used by the rebind modal — excludes is_deleted rows. Returns current match
    state so the operator can see which SP is already in use.
    """
    q = request.args.get("q", "").strip()
    if len(q) < 2 or len(q) > 200:
        return jsonify([])

    term = f"%{q}%"
    rows = (
        db.session.query(SupplierProduct)
        .options(joinedload(SupplierProduct.supplier))
        .filter(
            SupplierProduct.is_deleted.is_(False),
            db.or_(
                SupplierProduct.name.ilike(term),
                SupplierProduct.external_id.ilike(term),
                SupplierProduct.article.ilike(term),
                SupplierProduct.brand.ilike(term),
            ),
        )
        .order_by(SupplierProduct.name.asc())
        .limit(30)
        .all()
    )

    # Look up which of these SP already have confirmed/manual matches.
    if rows:
        sp_ids = [r.id for r in rows]
        active = {
            m.supplier_product_id: (m.id, m.prom_product_id, m.status)
            for m in ProductMatch.query.filter(
                ProductMatch.supplier_product_id.in_(sp_ids),
                ProductMatch.status.in_(("confirmed", "manual")),
            ).all()
        }
    else:
        active = {}

    results = []
    for sp in rows:
        existing = active.get(sp.id)
        results.append({
            "id": sp.id,
            "name": sp.name,
            "brand": sp.brand or "",
            "model": sp.model or "",
            "external_id": sp.external_id,
            "article": sp.article or "",
            "supplier_name": sp.supplier.name if sp.supplier else "",
            "price_eur": f"{sp.price_cents / 100:.2f}" if sp.price_cents else "",
            "available": bool(sp.available),
            "active_match_id": existing[0] if existing else None,
            "active_match_pp_id": existing[1] if existing else None,
            "active_match_status": existing[2] if existing else None,
        })
    return jsonify(results)


@matches_bp.route("/<int:match_id>/rebind", methods=["POST"])
@login_required
def rebind_match(match_id):
    """Atomically swap the supplier product on a confirmed/manual match.

    Old match: status=rejected, confirmed_by="rebind:{user}". Row preserved
    for audit trail. New match on (new_sp, same_pp): upsert to confirmed.

    Blocks if the new_sp already has a confirmed/manual match on a DIFFERENT
    pp — the operator must unconfirm that first (1 sp ↔ 1 active match is
    not an invariant of the system, but rebinding into a claimed sp would
    create a three-way tangle the operator likely didn't intend).
    """
    old_match = db.get_or_404(ProductMatch, match_id)
    if old_match.status not in ("confirmed", "manual"):
        return jsonify({
            "status": "error",
            "message": "Переподвязать можно только подтверждённый или ручной матч",
        }), 400

    data = request.get_json(silent=True) or {}
    new_sp_id = data.get("new_supplier_product_id")
    if not new_sp_id:
        return jsonify({
            "status": "error",
            "message": "Не указан новый supplier_product_id",
        }), 400

    try:
        new_sp_id = int(new_sp_id)
    except (TypeError, ValueError):
        return jsonify({
            "status": "error",
            "message": "supplier_product_id должен быть целым числом",
        }), 400

    new_sp = db.session.get(SupplierProduct, new_sp_id)
    if new_sp is None or new_sp.is_deleted:
        return jsonify({
            "status": "error",
            "message": "Новый товар поставщика не найден",
        }), 404

    if new_sp_id == old_match.supplier_product_id:
        return jsonify({
            "status": "error",
            "message": "Новый товар совпадает с текущим — переподвязывать нечего",
        }), 400

    # Reject rebind if new_sp already claims a DIFFERENT pp.
    new_sp_existing = ProductMatch.query.filter(
        ProductMatch.supplier_product_id == new_sp_id,
        ProductMatch.prom_product_id != old_match.prom_product_id,
        ProductMatch.status.in_(("confirmed", "manual")),
    ).first()
    if new_sp_existing:
        return jsonify({
            "status": "error",
            "message": (
                f"Новый товар поставщика уже подтверждён на другой каталог "
                f"(матч #{new_sp_existing.id}, pp#{new_sp_existing.prom_product_id}). "
                f"Сначала отмените тот матч."
            ),
        }), 409

    target_pp_id = old_match.prom_product_id
    user_tag = f"rebind:{current_user.name}" if current_user and current_user.is_authenticated else "rebind"
    now = datetime.now(timezone.utc)

    # Does an existing row already link (new_sp, target_pp)?  If it's rejected
    # or candidate, upgrade it in place rather than insert (would hit UNIQUE).
    existing_pair = ProductMatch.query.filter_by(
        supplier_product_id=new_sp_id,
        prom_product_id=target_pp_id,
    ).first()

    old_sp_id = old_match.supplier_product_id

    # Mark old match rejected — releases the pp claim.
    old_match.status = "rejected"
    old_match.confirmed_by = user_tag
    old_match.confirmed_at = now
    old_match.in_feed = False
    old_match.published = False
    db.session.flush()

    if existing_pair is not None:
        existing_pair.status = "manual"
        existing_pair.score = 100.0
        existing_pair.confirmed_by = user_tag
        existing_pair.confirmed_at = now
        existing_pair.published = True
        # Reset sync timestamps — new link, never synced yet.
        existing_pair.price_synced_at = None
        existing_pair.availability_synced_at = None
        existing_pair.in_feed = False
        new_match = existing_pair
    else:
        new_match = ProductMatch(
            supplier_product_id=new_sp_id,
            prom_product_id=target_pp_id,
            score=100.0,
            status="manual",
            confirmed_at=now,
            confirmed_by=user_tag,
            published=True,
        )
        db.session.add(new_match)
        db.session.flush()

    log_action(
        "rebind",
        match_id=new_match.id,
        supplier_product_id=new_sp_id,
        prom_product_id=target_pp_id,
        details={
            "old_match_id": old_match.id,
            "old_supplier_product_id": old_sp_id,
            "new_supplier_product_id": new_sp_id,
            "prom_product_id": target_pp_id,
        },
    )
    db.session.commit()

    return jsonify({
        "status": "ok",
        "old_match_id": old_match.id,
        "new_match_id": new_match.id,
    })


# ========== Match rules CRUD ==========


@matches_bp.route("/rules")
@login_required
def rules():
    """Match rules management page."""
    page = request.args.get("page", 1, type=int)
    query = (
        MatchRule.query.filter_by(is_active=True)
        .options(joinedload(MatchRule.prom_product))
        .order_by(MatchRule.created_at.desc())
    )
    pagination = db.paginate(query, page=page, per_page=25)

    return render_template(
        "matches/rules.html",
        rules=pagination.items,
        pagination=pagination,
    )


@matches_bp.route("/rules/<int:rule_id>/delete", methods=["POST"])
@login_required
def delete_rule(rule_id):
    """Soft-delete a match rule."""
    rule = db.get_or_404(MatchRule, rule_id)
    rule.is_active = False
    db.session.commit()

    return jsonify({"status": "ok"})


@matches_bp.route("/rules/<int:rule_id>/edit", methods=["POST"])
@login_required
def edit_rule(rule_id):
    """Edit a match rule (note, prom_product_id)."""
    rule = db.get_or_404(MatchRule, rule_id)
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No data provided"}), 400

    if "note" in data:
        rule.note = data["note"]
    if "prom_product_id" in data:
        prom_product = db.get_or_404(PromProduct, data["prom_product_id"])
        rule.prom_product_id = prom_product.id
    if "is_active" in data:
        rule.is_active = bool(data["is_active"])

    db.session.commit()

    return jsonify({"status": "ok"})


# ========== Export endpoints ==========


@matches_bp.route("/export/csv")
@login_required
def export_csv():
    """Download matches as CSV with current filters applied."""
    from app.services.export_service import export_matches_csv

    query, _filters = _build_match_query()
    matches = query.all()
    output = export_matches_csv(matches)

    return Response(
        output.getvalue(),
        mimetype="text/csv; charset=utf-8-sig",
        headers={"Content-Disposition": "attachment; filename=matches.csv"},
    )


@matches_bp.route("/export/xlsx")
@login_required
def export_xlsx():
    """Download matches as XLSX with current filters applied."""
    from app.services.export_service import export_matches_xlsx

    query, _filters = _build_match_query()
    matches = query.all()
    buf = export_matches_xlsx(matches)

    return send_file(
        buf,
        as_attachment=True,
        download_name="matches.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
