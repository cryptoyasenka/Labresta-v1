"""Product management blueprint: supplier products, unmatched lists, and management actions."""

from datetime import datetime, timezone

from flask import Blueprint, jsonify, render_template, request
from flask_login import login_required
from sqlalchemy import func, or_, select, text
from sqlalchemy.orm import aliased

from app.extensions import db
from app.models.catalog import PromProduct
from app.models.product_match import ProductMatch
from app.models.supplier import Supplier
from app.models.supplier_product import SupplierProduct
from app.services.matcher import extract_model_from_name, normalize_model

products_bp = Blueprint("products", __name__)

VALID_SORT_SUPPLIER = {"name", "price", "brand", "last_seen_at", "model", "article"}
VALID_PER_PAGE = {25, 50, 100}

VALID_OPERATOR_DECISIONS = {
    "needs_delete",
    "needs_request",
    "keep_searching",
}


def _parse_pagination(default_sort="name"):
    """Parse common pagination/sort params from request args."""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 25, type=int)
    if per_page not in VALID_PER_PAGE:
        per_page = 25
    sort = request.args.get("sort", default_sort)
    order = request.args.get("order", "asc")
    if order not in ("asc", "desc"):
        order = "asc"
    search = request.args.get("search", "").strip()
    return page, per_page, sort, order, search


def _apply_sort(query, model, sort, order, sort_map):
    """Apply sorting to a query using a column map."""
    col = sort_map.get(sort)
    if col is None:
        col = sort_map.get("name", list(sort_map.values())[0])
    if order == "desc":
        query = query.order_by(col.desc())
    else:
        query = query.order_by(col.asc())
    return query


# ---------------------------------------------------------------------------
# Supplier Products List (DASH-05)
# ---------------------------------------------------------------------------
@products_bp.route("/supplier")
@login_required
def supplier_list():
    """List all supplier products with filters, search, sorting, pagination."""
    page, per_page, sort, order, search = _parse_pagination("name")
    supplier_id = request.args.get("supplier_id", type=int)
    available_filter = request.args.get("available", "all")
    needs_review_filter = request.args.get("needs_review", "all")
    match_filter = request.args.get("match_state", "all")
    brand_filter = request.args.get("brand", "").strip()
    show_deleted = request.args.get("show_deleted", "false") == "true"
    show_ignored = request.args.get("show_ignored", "false") == "true"

    query = select(SupplierProduct)

    # Exclude deleted by default
    if not show_deleted:
        query = query.where(SupplierProduct.is_deleted == False)  # noqa: E712

    # Exclude ignored by default — operator action, not feed state.
    if not show_ignored:
        query = query.where(SupplierProduct.ignored == False)  # noqa: E712

    if supplier_id:
        query = query.where(SupplierProduct.supplier_id == supplier_id)
    if brand_filter:
        query = query.where(SupplierProduct.brand == brand_filter)
    if available_filter == "yes":
        query = query.where(SupplierProduct.available == True)  # noqa: E712
    elif available_filter == "no":
        query = query.where(SupplierProduct.available == False)  # noqa: E712
    if needs_review_filter == "yes":
        query = query.where(SupplierProduct.needs_review == True)  # noqa: E712
    elif needs_review_filter == "no":
        query = query.where(SupplierProduct.needs_review == False)  # noqa: E712
    if search:
        query = query.where(SupplierProduct.name.ilike(f"%{search}%"))

    active_match_sp_ids = select(ProductMatch.supplier_product_id).where(
        ProductMatch.status.in_(["confirmed", "manual"])
    ).correlate(None)
    any_match_sp_ids = select(ProductMatch.supplier_product_id).where(
        ProductMatch.status.in_(["confirmed", "manual", "candidate"])
    ).correlate(None)

    if match_filter == "none":
        query = query.where(SupplierProduct.id.not_in(any_match_sp_ids))
    elif match_filter == "candidate":
        cand_ids = select(ProductMatch.supplier_product_id).where(
            ProductMatch.status == "candidate"
        ).correlate(None)
        query = query.where(SupplierProduct.id.in_(cand_ids))
    elif match_filter == "active":
        query = query.where(SupplierProduct.id.in_(active_match_sp_ids))
    elif match_filter == "confirmed":
        cf_ids = select(ProductMatch.supplier_product_id).where(
            ProductMatch.status == "confirmed"
        ).correlate(None)
        query = query.where(SupplierProduct.id.in_(cf_ids))
    elif match_filter == "manual":
        m_ids = select(ProductMatch.supplier_product_id).where(
            ProductMatch.status == "manual"
        ).correlate(None)
        query = query.where(SupplierProduct.id.in_(m_ids))

    # Sort
    sort_map = {
        "name": SupplierProduct.name,
        "price": SupplierProduct.price_cents,
        "brand": SupplierProduct.brand,
        "model": SupplierProduct.model,
        "article": SupplierProduct.article,
        "last_seen_at": SupplierProduct.last_seen_at,
    }
    query = _apply_sort(query, SupplierProduct, sort, order, sort_map)

    # Count
    count_q = select(func.count()).select_from(query.subquery())
    total = db.session.execute(count_q).scalar() or 0
    total_pages = max((total + per_page - 1) // per_page, 1)

    # Paginate
    offset = (page - 1) * per_page
    products = db.session.execute(query.offset(offset).limit(per_page)).scalars().all()

    # All suppliers for dropdown
    suppliers = db.session.execute(
        select(Supplier).order_by(Supplier.name)
    ).scalars().all()

    # Distinct brands for dropdown (scoped to selected supplier when provided,
    # and mirroring the is_deleted filter so the dropdown never offers a brand
    # that would yield zero visible rows).
    brands_q = (
        select(SupplierProduct.brand)
        .where(SupplierProduct.brand.isnot(None))
        .where(SupplierProduct.brand != "")
    )
    if not show_deleted:
        brands_q = brands_q.where(SupplierProduct.is_deleted == False)  # noqa: E712
    if supplier_id:
        brands_q = brands_q.where(SupplierProduct.supplier_id == supplier_id)
    brands = db.session.execute(
        brands_q.distinct().order_by(SupplierProduct.brand)
    ).scalars().all()
    # Keep the currently-selected brand visible even if it's not in the scoped
    # list — otherwise switching supplier silently drops the filter from the UI
    # while still applying it via the URL param, producing a confusing empty list.
    if brand_filter and brand_filter not in brands:
        brands = sorted(list(brands) + [brand_filter])

    # Load matches for displayed SPs (priority: manual > confirmed > candidate > rejected)
    sp_ids = [p.id for p in products]
    matches_by_sp: dict[int, ProductMatch] = {}
    if sp_ids:
        status_priority = {"manual": 0, "confirmed": 1, "candidate": 2, "rejected": 3}
        rows = db.session.execute(
            select(ProductMatch).where(ProductMatch.supplier_product_id.in_(sp_ids))
        ).scalars().all()
        for m in rows:
            prio = status_priority.get(m.status, 9)
            existing = matches_by_sp.get(m.supplier_product_id)
            if existing is None or status_priority.get(existing.status, 9) > prio:
                matches_by_sp[m.supplier_product_id] = m

    # Attach pp names for rendering in template
    pp_ids = {m.prom_product_id for m in matches_by_sp.values()}
    pp_by_id: dict[int, PromProduct] = {}
    if pp_ids:
        pp_by_id = {
            p.id: p for p in db.session.execute(
                select(PromProduct).where(PromProduct.id.in_(pp_ids))
            ).scalars().all()
        }

    # Claimed-PP detection: for each unmatched SP on this page, check if its
    # extracted model matches a catalog PP that's already confirmed/manual to a
    # DIFFERENT supplier. Operators see "Уже у [Supplier]" badge so they don't
    # waste time trying to manually match — the slot is taken.
    sp_brands = {p.brand.lower().strip() for p in products if p.brand}
    claimed_by_key: dict[tuple[str, str], dict] = {}
    if sp_brands:
        rows = db.session.execute(
            select(ProductMatch, PromProduct, SupplierProduct, Supplier)
            .join(PromProduct, PromProduct.id == ProductMatch.prom_product_id)
            .join(SupplierProduct, SupplierProduct.id == ProductMatch.supplier_product_id)
            .join(Supplier, Supplier.id == SupplierProduct.supplier_id)
            .where(
                ProductMatch.status.in_(["confirmed", "manual"]),
                func.lower(func.trim(PromProduct.brand)).in_(sp_brands),
            )
        ).all()
        for m, pp, claimer_sp, claimer_supp in rows:
            if not pp.brand:
                continue
            model = normalize_model(extract_model_from_name(pp.name, pp.brand))
            if not model:
                continue
            key = (pp.brand.lower().strip(), model)
            if key not in claimed_by_key:
                claimed_by_key[key] = {
                    "pp_id": pp.id, "pp_name": pp.name, "match_id": m.id,
                    "supplier_id": claimer_sp.supplier_id,
                    "supplier_name": claimer_supp.name,
                }

    claim_info_by_sp: dict[int, dict] = {}
    for sp in products:
        if not sp.brand:
            continue
        model = normalize_model(extract_model_from_name(sp.name, sp.brand))
        if not model:
            continue
        key = (sp.brand.lower().strip(), model)
        info = claimed_by_key.get(key)
        if info and info["supplier_id"] != sp.supplier_id:
            claim_info_by_sp[sp.id] = info

    return render_template(
        "products/supplier.html",
        products=products,
        suppliers=suppliers,
        brands=brands,
        brand=brand_filter,
        matches_by_sp=matches_by_sp,
        pp_by_id=pp_by_id,
        claim_info_by_sp=claim_info_by_sp,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages,
        sort=sort,
        order=order,
        search=search,
        supplier_id=supplier_id,
        available=available_filter,
        needs_review=needs_review_filter,
        match_state=match_filter,
        show_deleted=show_deleted,
        show_ignored=show_ignored,
    )


# ---------------------------------------------------------------------------
# Unmatched Prom.ua Products (MATCH-04)
# ---------------------------------------------------------------------------
@products_bp.route("/unmatched-catalog")
@login_required
def unmatched_catalog():
    """List Horoshop products without a confirmed/manual match.

    Filters:
      - brand: exact brand on PromProduct
      - supplier_id: narrow to "no confirmed/manual match from THIS supplier"
        and compute per-row candidate state scoped to this supplier
      - match_state: "all" | "none" (no candidate anywhere) | "candidate"
        (has candidate but not confirmed). When supplier is set, the scope
        is per-supplier; otherwise global.
      - decision: "" | "pending" | "needs_delete" | "needs_request" |
        "keep_searching" | "reviewed" (any non-null decision)
      - search: matches name, article, OR display_article (ilike)
      - sort: name | brand | price | article | display_article
    """
    page, per_page, sort, order, search = _parse_pagination("name")
    brand_filter = request.args.get("brand", "").strip()
    supplier_id = request.args.get("supplier_id", type=int)
    match_state = request.args.get("match_state", "all")
    decision_filter = request.args.get("decision", "").strip()

    # Base: PP with no confirmed/manual match from ANY supplier (global view).
    # When a supplier is chosen we re-scope the exclusion to that supplier only.
    if supplier_id:
        matched_ids = (
            select(ProductMatch.prom_product_id)
            .join(
                SupplierProduct,
                SupplierProduct.id == ProductMatch.supplier_product_id,
            )
            .where(
                ProductMatch.status.in_(["confirmed", "manual"]),
                SupplierProduct.supplier_id == supplier_id,
            )
            .correlate(None)
        )
    else:
        matched_ids = select(ProductMatch.prom_product_id).where(
            ProductMatch.status.in_(["confirmed", "manual"])
        ).correlate(None)

    query = select(PromProduct).where(PromProduct.id.not_in(matched_ids))

    # When a supplier is chosen, restrict PP to brands the supplier actually
    # carries — otherwise the result includes brands the supplier has never
    # stocked (Rational/Pavoni/GoodFood), which is meaningless for triage.
    # Case-insensitive because PP catalog and SP feed disagree on case
    # ("Hurakan" in PP vs "HURAKAN" in НП feed).
    if supplier_id:
        sup_brands_lower = (
            select(func.lower(SupplierProduct.brand))
            .where(
                SupplierProduct.supplier_id == supplier_id,
                SupplierProduct.brand.isnot(None),
                SupplierProduct.brand != "",
                SupplierProduct.is_deleted == False,  # noqa: E712
            )
            .correlate(None)
        )
        query = query.where(func.lower(PromProduct.brand).in_(sup_brands_lower))

    if search:
        like = f"%{search}%"
        query = query.where(
            or_(
                PromProduct.name.ilike(like),
                PromProduct.article.ilike(like),
                PromProduct.display_article.ilike(like),
            )
        )
    if brand_filter:
        query = query.where(PromProduct.brand == brand_filter)

    if decision_filter == "pending":
        query = query.where(PromProduct.operator_decision.is_(None))
    elif decision_filter == "reviewed":
        query = query.where(PromProduct.operator_decision.isnot(None))
    elif decision_filter in VALID_OPERATOR_DECISIONS:
        query = query.where(PromProduct.operator_decision == decision_filter)

    # match_state filter uses candidate presence. Scope to supplier when chosen.
    if match_state in ("none", "candidate"):
        candidate_pp_ids = select(ProductMatch.prom_product_id).where(
            ProductMatch.status == "candidate"
        )
        if supplier_id:
            candidate_pp_ids = candidate_pp_ids.join(
                SupplierProduct,
                SupplierProduct.id == ProductMatch.supplier_product_id,
            ).where(SupplierProduct.supplier_id == supplier_id)
        candidate_pp_ids = candidate_pp_ids.correlate(None)
        if match_state == "none":
            query = query.where(PromProduct.id.not_in(candidate_pp_ids))
        else:  # candidate
            query = query.where(PromProduct.id.in_(candidate_pp_ids))

    sort_map = {
        "name": PromProduct.name,
        "brand": PromProduct.brand,
        "price": PromProduct.price,
        "article": PromProduct.article,
        "display_article": PromProduct.display_article,
    }
    query = _apply_sort(query, PromProduct, sort, order, sort_map)

    count_q = select(func.count()).select_from(query.subquery())
    total = db.session.execute(count_q).scalar() or 0
    total_pages = max((total + per_page - 1) // per_page, 1)

    offset = (page - 1) * per_page
    products = db.session.execute(query.offset(offset).limit(per_page)).scalars().all()

    # Brands dropdown — scoped so the filter list never offers a dead option.
    brands_q = (
        select(PromProduct.brand)
        .where(PromProduct.brand.isnot(None))
        .where(PromProduct.brand != "")
    )
    if supplier_id:
        # Dropdown uses same case-insensitive intersect as the main query so
        # it never offers a dead option and covers PP 'Hurakan' vs SP 'HURAKAN'.
        sup_brands_lower_dd = (
            select(func.lower(SupplierProduct.brand))
            .where(
                SupplierProduct.supplier_id == supplier_id,
                SupplierProduct.brand.isnot(None),
                SupplierProduct.brand != "",
                SupplierProduct.is_deleted == False,  # noqa: E712
            )
            .correlate(None)
        )
        brands_q = brands_q.where(func.lower(PromProduct.brand).in_(sup_brands_lower_dd))
    brands = db.session.execute(
        brands_q.distinct().order_by(PromProduct.brand)
    ).scalars().all()
    if brand_filter and brand_filter not in brands:
        brands = sorted(list(brands) + [brand_filter])

    suppliers = db.session.execute(
        select(Supplier).order_by(Supplier.name)
    ).scalars().all()

    # Per-row candidate state for the displayed page (scoped to supplier if set).
    # Used to show a "has candidate → go to /matches" hint next to each row.
    pp_ids = [p.id for p in products]
    candidate_set: set[int] = set()
    if pp_ids:
        cand_q = select(ProductMatch.prom_product_id).where(
            ProductMatch.status == "candidate",
            ProductMatch.prom_product_id.in_(pp_ids),
        )
        if supplier_id:
            cand_q = cand_q.join(
                SupplierProduct,
                SupplierProduct.id == ProductMatch.supplier_product_id,
            ).where(SupplierProduct.supplier_id == supplier_id)
        candidate_set = set(db.session.execute(cand_q).scalars().all())

    return render_template(
        "products/unmatched_catalog.html",
        products=products,
        brands=brands,
        suppliers=suppliers,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages,
        sort=sort,
        order=order,
        search=search,
        brand=brand_filter,
        supplier_id=supplier_id,
        match_state=match_state,
        decision=decision_filter,
        candidate_set=candidate_set,
    )


# ---------------------------------------------------------------------------
# Unmatched Supplier Products (MATCH-05)
# ---------------------------------------------------------------------------
@products_bp.route("/unmatched-supplier")
@login_required
def unmatched_supplier():
    """List available supplier products with brand but no confirmed/manual match."""
    page, per_page, sort, order, search = _parse_pagination("name")
    supplier_id = request.args.get("supplier_id", type=int)
    brand_filter = request.args.get("brand", "").strip()

    matched_supplier_ids = select(ProductMatch.supplier_product_id).where(
        ProductMatch.status.in_(["confirmed", "manual"])
    ).correlate(None)

    query = select(SupplierProduct).where(
        SupplierProduct.id.not_in(matched_supplier_ids),
        SupplierProduct.available == True,  # noqa: E712
        SupplierProduct.brand.isnot(None),
        SupplierProduct.is_deleted == False,  # noqa: E712
    )

    if supplier_id:
        query = query.where(SupplierProduct.supplier_id == supplier_id)
    if search:
        query = query.where(SupplierProduct.name.ilike(f"%{search}%"))
    if brand_filter:
        query = query.where(SupplierProduct.brand == brand_filter)

    sort_map = {
        "name": SupplierProduct.name,
        "brand": SupplierProduct.brand,
        "price": SupplierProduct.price_cents,
        "model": SupplierProduct.model,
        "article": SupplierProduct.article,
    }
    query = _apply_sort(query, SupplierProduct, sort, order, sort_map)

    count_q = select(func.count()).select_from(query.subquery())
    total = db.session.execute(count_q).scalar() or 0
    total_pages = max((total + per_page - 1) // per_page, 1)

    offset = (page - 1) * per_page
    products = db.session.execute(query.offset(offset).limit(per_page)).scalars().all()

    suppliers = db.session.execute(
        select(Supplier).order_by(Supplier.name)
    ).scalars().all()

    # Distinct brands from supplier products for dropdown
    brands = db.session.execute(
        select(SupplierProduct.brand)
        .where(SupplierProduct.brand.isnot(None))
        .distinct()
        .order_by(SupplierProduct.brand)
    ).scalars().all()

    # Cross-supplier match indicator: two-pass detection.
    #
    # Pass 1 — article normalization (most reliable, no false positives):
    #   strip non-alphanumeric, lowercase → XB893-MP = XB893MP, XB693 ≠ XB693MP.
    # Pass 2 — high-confidence candidates (score ≥ 90) for products without articles
    #   or where article normalization found no match. Threshold filters wrong
    #   candidates like XB693→XB693MP (86%).
    cross_matched: dict[int, dict] = {}
    sp_ids = [p.id for p in products]
    if sp_ids:
        art_rows = db.session.execute(
            text("""
                SELECT DISTINCT ON (sp_u.id)
                    sp_u.id AS sp_id,
                    s_c.name AS other_supplier,
                    pp.name AS prom_name
                FROM supplier_products sp_u
                JOIN supplier_products sp_c
                    ON sp_c.supplier_id != sp_u.supplier_id
                    AND sp_c.article IS NOT NULL
                    AND REGEXP_REPLACE(LOWER(sp_c.article), '[^a-z0-9]', '', 'g')
                        = REGEXP_REPLACE(LOWER(sp_u.article), '[^a-z0-9]', '', 'g')
                    AND LENGTH(REGEXP_REPLACE(LOWER(sp_u.article), '[^a-z0-9]', '', 'g')) >= 4
                JOIN product_matches pm
                    ON pm.supplier_product_id = sp_c.id
                    AND pm.status IN ('confirmed', 'manual')
                JOIN prom_products pp ON pp.id = pm.prom_product_id
                JOIN suppliers s_c ON s_c.id = sp_c.supplier_id
                WHERE sp_u.id = ANY(:ids)
                  AND sp_u.article IS NOT NULL
            """),
            {"ids": sp_ids},
        ).all()
        for row in art_rows:
            cross_matched[row.sp_id] = {
                "supplier_name": row.other_supplier,
                "prom_name": row.prom_name,
            }

        remaining_ids = [i for i in sp_ids if i not in cross_matched]
        if remaining_ids:
            pm_cand = aliased(ProductMatch, name="pm_cand")
            pm_conf = aliased(ProductMatch, name="pm_conf")
            sp_conf = aliased(SupplierProduct, name="sp_conf")
            s_conf = aliased(Supplier, name="s_conf")
            cand_rows = db.session.execute(
                select(
                    pm_cand.supplier_product_id,
                    s_conf.name.label("other_supplier"),
                    PromProduct.name.label("prom_name"),
                )
                .select_from(pm_cand)
                .join(
                    pm_conf,
                    (pm_conf.prom_product_id == pm_cand.prom_product_id)
                    & pm_conf.status.in_(["confirmed", "manual"])
                    & (pm_conf.supplier_product_id != pm_cand.supplier_product_id),
                )
                .join(sp_conf, sp_conf.id == pm_conf.supplier_product_id)
                .join(s_conf, s_conf.id == sp_conf.supplier_id)
                .join(PromProduct, PromProduct.id == pm_cand.prom_product_id)
                .where(
                    pm_cand.supplier_product_id.in_(remaining_ids),
                    pm_cand.score >= 90,
                )
                .distinct(pm_cand.supplier_product_id)
            ).all()
            for row in cand_rows:
                cross_matched[row.supplier_product_id] = {
                    "supplier_name": row.other_supplier,
                    "prom_name": row.prom_name,
                }

    return render_template(
        "products/unmatched_supplier.html",
        products=products,
        suppliers=suppliers,
        brands=brands,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages,
        sort=sort,
        order=order,
        search=search,
        supplier_id=supplier_id,
        brand=brand_filter,
        cross_matched=cross_matched,
    )


# ---------------------------------------------------------------------------
# Product Management Write Endpoints
# ---------------------------------------------------------------------------
@products_bp.route("/supplier/<int:product_id>/mark-unavailable", methods=["POST"])
@login_required
def mark_unavailable(product_id):
    """Mark a supplier product as out of stock."""
    product = db.session.get(SupplierProduct, product_id)
    if not product:
        return jsonify({"status": "error", "message": "Товар не найден"}), 404
    product.available = False
    product.needs_review = False
    db.session.commit()
    return jsonify({"status": "ok", "message": "Товар отмечен как отсутствующий"})


@products_bp.route("/supplier/<int:product_id>/mark-available", methods=["POST"])
@login_required
def mark_available(product_id):
    """Mark a supplier product back in stock."""
    product = db.session.get(SupplierProduct, product_id)
    if not product:
        return jsonify({"status": "error", "message": "Товар не найден"}), 404
    product.available = True
    db.session.commit()
    return jsonify({"status": "ok", "message": "Товар отмечен как в наличии"})


@products_bp.route("/supplier/<int:product_id>/force-price", methods=["POST"])
@login_required
def force_price(product_id):
    """Force-set a product price (prevents sync overwrite)."""
    product = db.session.get(SupplierProduct, product_id)
    if not product:
        return jsonify({"status": "error", "message": "Товар не найден"}), 404
    data = request.get_json(silent=True) or {}
    price_cents = data.get("price_cents")
    currency = data.get("currency", product.currency)
    if price_cents is None:
        return jsonify({"status": "error", "message": "Укажите price_cents"}), 400
    product.price_cents = int(price_cents)
    product.currency = currency
    product.price_forced = True
    db.session.commit()
    return jsonify({"status": "ok", "message": "Цена принудительно установлена"})


@products_bp.route("/supplier/<int:product_id>/delete", methods=["POST"])
@login_required
def delete_product(product_id):
    """Soft-delete a supplier product."""
    product = db.session.get(SupplierProduct, product_id)
    if not product:
        return jsonify({"status": "error", "message": "Товар не найден"}), 404
    product.is_deleted = True
    product.available = False
    db.session.commit()
    return jsonify({"status": "ok", "message": "Товар удален"})


@products_bp.route("/supplier/<int:product_id>/ignore", methods=["POST"])
@login_required
def ignore_product(product_id):
    """Mark a supplier product as ignored (operator exclusion).

    Hides it from /matches and the default /products/supplier view. Use for
    offers that should not be cataloged at all — e.g. brandless feeds where
    cross-brand matching would be unsafe.
    """
    product = db.session.get(SupplierProduct, product_id)
    if not product:
        return jsonify({"status": "error", "message": "Товар не найден"}), 404
    product.ignored = True
    db.session.commit()
    return jsonify({"status": "ok", "message": "Товар исключён"})


@products_bp.route("/supplier/<int:product_id>/unignore", methods=["POST"])
@login_required
def unignore_product(product_id):
    """Remove the ignored flag from a supplier product."""
    product = db.session.get(SupplierProduct, product_id)
    if not product:
        return jsonify({"status": "error", "message": "Товар не найден"}), 404
    product.ignored = False
    db.session.commit()
    return jsonify({"status": "ok", "message": "Товар возвращён в работу"})


@products_bp.route("/supplier/<int:product_id>/set-status", methods=["POST"])
@login_required
def set_status(product_id):
    """Set arbitrary status fields on a supplier product."""
    product = db.session.get(SupplierProduct, product_id)
    if not product:
        return jsonify({"status": "error", "message": "Товар не найден"}), 404
    data = request.get_json(silent=True) or {}
    if "needs_review" in data:
        product.needs_review = bool(data["needs_review"])
    if "available" in data:
        product.available = bool(data["available"])
    db.session.commit()
    return jsonify({"status": "ok"})


# ---------------------------------------------------------------------------
# Operator triage for Horoshop PP without supplier match
# ---------------------------------------------------------------------------
@products_bp.route("/catalog/<int:pp_id>/set-decision", methods=["POST"])
@login_required
def set_catalog_decision(pp_id):
    """Record an operator decision on a Horoshop PP without supplier match."""
    pp = db.session.get(PromProduct, pp_id)
    if not pp:
        return jsonify({"status": "error", "message": "Товар не найден"}), 404
    data = request.get_json(silent=True) or {}
    decision = (data.get("decision") or "").strip()
    if decision not in VALID_OPERATOR_DECISIONS:
        return jsonify({
            "status": "error",
            "message": f"Недопустимое решение: {decision!r}",
        }), 400
    pp.operator_decision = decision
    note = data.get("note")
    if note is not None:
        pp.operator_decision_note = (str(note).strip() or None)
    pp.operator_decision_at = datetime.now(timezone.utc)
    db.session.commit()
    return jsonify({"status": "ok", "decision": decision})


@products_bp.route("/catalog/<int:pp_id>/clear-decision", methods=["POST"])
@login_required
def clear_catalog_decision(pp_id):
    """Clear an operator decision (put item back in the pending pile)."""
    pp = db.session.get(PromProduct, pp_id)
    if not pp:
        return jsonify({"status": "error", "message": "Товар не найден"}), 404
    pp.operator_decision = None
    pp.operator_decision_note = None
    pp.operator_decision_at = None
    db.session.commit()
    return jsonify({"status": "ok"})
