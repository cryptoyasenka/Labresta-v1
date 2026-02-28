"""Match review blueprint: list, filter, sort, paginate, confirm/reject matches."""

from datetime import datetime, timezone

from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user, login_required
from sqlalchemy import asc, desc
from sqlalchemy.orm import joinedload

from app.extensions import db
from app.models.catalog import PromProduct
from app.models.product_match import ProductMatch
from app.models.supplier_product import SupplierProduct
from app.services.matcher import CONFIDENCE_HIGH, CONFIDENCE_MEDIUM, find_match_for_product

matches_bp = Blueprint("matches", __name__)


@matches_bp.route("/")
@login_required
def review():
    """Main match review page with filtering, sorting, and pagination."""
    # Parse query params
    status = request.args.get("status", "all")
    confidence = request.args.get("confidence", "all")
    search = request.args.get("search", "").strip()
    sort_col = request.args.get("sort", "score")
    order = request.args.get("order", "asc")
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 25, type=int)

    # Validate per_page
    if per_page not in (25, 50, 100):
        per_page = 25

    # Build query
    query = ProductMatch.query.options(
        joinedload(ProductMatch.supplier_product),
        joinedload(ProductMatch.prom_product),
    )

    # Apply status filter
    if status and status != "all":
        query = query.filter(ProductMatch.status == status)

    # Apply confidence filter
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

    # Apply search filter (requires join)
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

    # Apply sorting
    sort_map = {
        "score": ProductMatch.score,
        "status": ProductMatch.status,
        "created_at": ProductMatch.created_at,
    }
    sort_column = sort_map.get(sort_col, ProductMatch.score)
    sort_func = asc if order == "asc" else desc
    query = query.order_by(sort_func(sort_column))

    # Paginate
    pagination = db.paginate(query, page=page, per_page=per_page)

    return render_template(
        "matches/review.html",
        matches=pagination.items,
        pagination=pagination,
        filters={
            "status": status,
            "confidence": confidence,
            "search": search,
            "sort": sort_col,
            "order": order,
            "per_page": per_page,
        },
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

    # Delete the rejected match
    db.session.delete(match)
    db.session.flush()

    # Attempt to find alternative candidate
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
