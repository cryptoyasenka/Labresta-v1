"""Match review blueprint: list, filter, sort, paginate, confirm/reject, manual match, rules CRUD, export."""

from datetime import datetime, timezone

from flask import Blueprint, Response, jsonify, render_template, request, send_file
from flask_login import current_user, login_required
from sqlalchemy import asc, desc
from sqlalchemy.orm import joinedload

import json
import re

from app.extensions import db
from app.models.catalog import PromProduct
from app.models.match_rule import MatchRule
from app.models.product_match import ProductMatch
from app.models.supplier_product import SupplierProduct
from app.services.audit_service import log_action
from app.services.matcher import CONFIDENCE_HIGH, CONFIDENCE_MEDIUM, find_match_for_product

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
    search = request.args.get("search", "").strip()
    sort_col = request.args.get("sort", "score")
    order = request.args.get("order", "asc")
    per_page = request.args.get("per_page", 25, type=int)

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

    if search:
        search_term = f"%{search}%"
        query = query.join(
            SupplierProduct, ProductMatch.supplier_product_id == SupplierProduct.id
        ).join(
            PromProduct, ProductMatch.prom_product_id == PromProduct.id
        ).filter(
            db.or_(
                SupplierProduct.name.ilike(search_term),
                PromProduct.name.ilike(search_term),
            )
        )

    sort_map = {
        "score": ProductMatch.score,
        "status": ProductMatch.status,
        "created_at": ProductMatch.created_at,
    }
    sort_column = sort_map.get(sort_col, ProductMatch.score)
    sort_func = asc if order == "asc" else desc
    query = query.order_by(sort_func(sort_column))

    filters = {
        "status": status,
        "confidence": confidence,
        "availability": availability,
        "search": search,
        "sort": sort_col,
        "order": order,
        "per_page": per_page,
    }
    return query, filters


@matches_bp.route("/")
@login_required
def review():
    """Main match review page with filtering, sorting, and pagination."""
    query, filters = _build_match_query()
    page = request.args.get("page", 1, type=int)
    pagination = db.paginate(query, page=page, per_page=filters["per_page"])

    # Count supplier products matching the search but without any match row.
    # Helps the operator realise that /matches hides unmatched SP — surfaces
    # a link to /products/supplier?match_state=none.
    unmatched_sp_count = 0
    if filters["search"]:
        from sqlalchemy import func as sa_func
        matched_sp_ids = db.session.query(ProductMatch.supplier_product_id).distinct()
        unmatched_sp_count = db.session.execute(
            db.select(sa_func.count(SupplierProduct.id)).where(
                SupplierProduct.name.ilike(f"%{filters['search']}%"),
                SupplierProduct.is_deleted == False,  # noqa: E712
                SupplierProduct.id.not_in(matched_sp_ids),
            )
        ).scalar() or 0

    return render_template(
        "matches/review.html",
        matches=pagination.items,
        pagination=pagination,
        filters=filters,
        confidence_high=CONFIDENCE_HIGH,
        confidence_medium=CONFIDENCE_MEDIUM,
        unmatched_sp_count=unmatched_sp_count,
    )


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
    import re
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
        result = result.replace(old_tok, new_tok)

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

    if action not in ("confirm", "reject", "recalc_discount"):
        return jsonify({"status": "error", "message": "Invalid action"}), 400

    if not ids:
        return jsonify({"status": "error", "message": "No matches selected"}), 400

    matches = ProductMatch.query.filter(ProductMatch.id.in_(ids)).all()
    processed = 0
    skipped_claimed: list[dict] = []

    for match in matches:
        if action == "confirm":
            existing = _pp_already_claimed(match.prom_product_id, exclude_match_id=match.id)
            if existing:
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
            _cleanup_other_candidates(match.supplier_product_id, match.id)
            processed += 1
        elif action == "reject":
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
            rate = (sp.supplier.eur_rate_uah or 51.15) if sp.supplier else 51.15
            from app.services.pricing import calculate_auto_discount
            new_d = float(calculate_auto_discount(sp.price_cents, rate))
            if match.discount_percent != new_d:
                match.discount_percent = new_d
            processed += 1

    log_action(f"bulk_{action}",
               details={"match_ids": ids, "processed": processed,
                        "skipped_claimed": [s["match_id"] for s in skipped_claimed]})
    db.session.commit()

    return jsonify({
        "status": "ok",
        "processed": processed,
        "skipped_claimed": skipped_claimed,
    })


# ========== Catalog search for manual match modal ==========


@matches_bp.route("/search-catalog")
@login_required
def search_catalog():
    """AJAX endpoint for catalog product search (used in manual match modal)."""
    q = request.args.get("q", "").strip()
    if len(q) < 2:
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
