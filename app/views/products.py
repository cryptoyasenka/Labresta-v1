"""Product management blueprint: supplier products, unmatched lists, and management actions."""

from flask import Blueprint, jsonify, render_template, request
from flask_login import login_required
from sqlalchemy import func, select

from app.extensions import db
from app.models.catalog import PromProduct
from app.models.product_match import ProductMatch
from app.models.supplier import Supplier
from app.models.supplier_product import SupplierProduct

products_bp = Blueprint("products", __name__)

VALID_SORT_SUPPLIER = {"name", "price", "brand", "last_seen_at", "model", "article"}
VALID_PER_PAGE = {25, 50, 100}


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
    show_deleted = request.args.get("show_deleted", "false") == "true"

    query = select(SupplierProduct)

    # Exclude deleted by default
    if not show_deleted:
        query = query.where(SupplierProduct.is_deleted == False)  # noqa: E712

    if supplier_id:
        query = query.where(SupplierProduct.supplier_id == supplier_id)
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

    return render_template(
        "products/supplier.html",
        products=products,
        suppliers=suppliers,
        matches_by_sp=matches_by_sp,
        pp_by_id=pp_by_id,
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
    )


# ---------------------------------------------------------------------------
# Unmatched Prom.ua Products (MATCH-04)
# ---------------------------------------------------------------------------
@products_bp.route("/unmatched-catalog")
@login_required
def unmatched_catalog():
    """List prom.ua products that have no confirmed/manual match."""
    page, per_page, sort, order, search = _parse_pagination("name")
    brand_filter = request.args.get("brand", "").strip()

    # Subquery: prom_product_ids with confirmed or manual match
    matched_ids = select(ProductMatch.prom_product_id).where(
        ProductMatch.status.in_(["confirmed", "manual"])
    ).correlate(None)

    query = select(PromProduct).where(PromProduct.id.not_in(matched_ids))

    if search:
        query = query.where(PromProduct.name.ilike(f"%{search}%"))
    if brand_filter:
        query = query.where(PromProduct.brand == brand_filter)

    sort_map = {
        "name": PromProduct.name,
        "brand": PromProduct.brand,
        "price": PromProduct.price,
        "article": PromProduct.article,
    }
    query = _apply_sort(query, PromProduct, sort, order, sort_map)

    count_q = select(func.count()).select_from(query.subquery())
    total = db.session.execute(count_q).scalar() or 0
    total_pages = max((total + per_page - 1) // per_page, 1)

    offset = (page - 1) * per_page
    products = db.session.execute(query.offset(offset).limit(per_page)).scalars().all()

    # Distinct brands for dropdown
    brands = db.session.execute(
        select(PromProduct.brand)
        .where(PromProduct.brand.isnot(None))
        .distinct()
        .order_by(PromProduct.brand)
    ).scalars().all()

    return render_template(
        "products/unmatched_catalog.html",
        products=products,
        brands=brands,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages,
        sort=sort,
        order=order,
        search=search,
        brand=brand_filter,
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
