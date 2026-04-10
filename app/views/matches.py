"""Match review blueprint: list, filter, sort, paginate, confirm/reject, manual match, rules CRUD, export."""

from datetime import datetime, timezone

from flask import Blueprint, Response, jsonify, render_template, request, send_file
from flask_login import current_user, login_required
from sqlalchemy import asc, desc
from sqlalchemy.orm import joinedload

from app.extensions import db
from app.models.catalog import PromProduct
from app.models.match_rule import MatchRule
from app.models.product_match import ProductMatch
from app.models.supplier_product import SupplierProduct
from app.services.matcher import CONFIDENCE_HIGH, CONFIDENCE_MEDIUM, find_match_for_product

matches_bp = Blueprint("matches", __name__)


def _build_match_query():
    """Build filtered/sorted match query from request args. Returns (query, filters_dict)."""
    status = request.args.get("status", "all")
    confidence = request.args.get("confidence", "all")
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

    return render_template(
        "matches/review.html",
        matches=pagination.items,
        pagination=pagination,
        filters=filters,
        confidence_high=CONFIDENCE_HIGH,
        confidence_medium=CONFIDENCE_MEDIUM,
    )


@matches_bp.route("/<int:match_id>/confirm", methods=["POST"])
@login_required
def confirm_match(match_id):
    """AJAX endpoint to confirm a match."""
    match = db.get_or_404(ProductMatch, match_id)

    match.status = "confirmed"
    match.confirmed_at = datetime.now(timezone.utc)
    match.confirmed_by = current_user.name
    current_user.matches_processed += 1
    db.session.commit()

    return jsonify({"status": "ok", "new_status": "confirmed"})


@matches_bp.route("/<int:match_id>/reject", methods=["POST"])
@login_required
def reject_match(match_id):
    """AJAX endpoint to reject a match and attempt re-matching."""
    match = db.get_or_404(ProductMatch, match_id)

    supplier_product = match.supplier_product
    rejected_prom_id = match.prom_product_id

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

    db.session.commit()

    return jsonify({
        "status": "ok",
        "new_status": "rejected",
        "new_candidate_id": new_candidate_id,
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

    match.discount_percent = discount  # None clears the override
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

    if action not in ("confirm", "reject"):
        return jsonify({"status": "error", "message": "Invalid action"}), 400

    if not ids:
        return jsonify({"status": "error", "message": "No matches selected"}), 400

    matches = ProductMatch.query.filter(ProductMatch.id.in_(ids)).all()
    processed = 0

    for match in matches:
        if action == "confirm":
            match.status = "confirmed"
            match.confirmed_at = datetime.now(timezone.utc)
            match.confirmed_by = current_user.name
            current_user.matches_processed += 1
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

    db.session.commit()

    return jsonify({"status": "ok", "processed": processed})


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

    # Delete any existing match for this supplier product
    existing = ProductMatch.query.filter_by(
        supplier_product_id=supplier_product_id
    ).first()
    if existing:
        db.session.delete(existing)
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
