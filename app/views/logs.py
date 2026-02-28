"""Logs blueprint: detailed sync history viewer with filtering."""

from flask import Blueprint, render_template, request
from flask_login import login_required
from sqlalchemy import select

from app.extensions import db
from app.models.supplier import Supplier
from app.models.sync_run import SyncRun

logs_bp = Blueprint("logs", __name__)


@logs_bp.route("/")
@login_required
def index():
    """Detailed sync log viewer with filtering and pagination."""
    # Filter params
    supplier_id = request.args.get("supplier_id", type=int)
    status = request.args.get("status", "all")
    date_from = request.args.get("date_from", "")
    date_to = request.args.get("date_to", "")
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 25, type=int)
    per_page = min(per_page, 100)  # Cap at 100

    # Build query
    query = select(SyncRun).order_by(SyncRun.started_at.desc())

    if supplier_id:
        query = query.where(SyncRun.supplier_id == supplier_id)
    if status and status != "all":
        query = query.where(SyncRun.status == status)
    if date_from:
        query = query.where(SyncRun.started_at >= date_from)
    if date_to:
        query = query.where(SyncRun.started_at <= date_to + " 23:59:59")

    # Count total for pagination
    from sqlalchemy import func

    count_query = select(func.count()).select_from(query.subquery())
    total = db.session.execute(count_query).scalar() or 0

    # Summary stats (using same filters)
    stats_base = select(SyncRun)
    if supplier_id:
        stats_base = stats_base.where(SyncRun.supplier_id == supplier_id)
    if date_from:
        stats_base = stats_base.where(SyncRun.started_at >= date_from)
    if date_to:
        stats_base = stats_base.where(SyncRun.started_at <= date_to + " 23:59:59")

    success_count = db.session.execute(
        select(func.count()).select_from(
            stats_base.where(SyncRun.status == "success").subquery()
        )
    ).scalar() or 0
    error_count = db.session.execute(
        select(func.count()).select_from(
            stats_base.where(SyncRun.status == "error").subquery()
        )
    ).scalar() or 0

    # Paginate
    offset = (page - 1) * per_page
    runs = (
        db.session.execute(query.offset(offset).limit(per_page)).scalars().all()
    )

    # Suppliers for filter dropdown
    suppliers = db.session.execute(
        select(Supplier).order_by(Supplier.name)
    ).scalars().all()

    total_pages = max(1, (total + per_page - 1) // per_page)

    return render_template(
        "logs/index.html",
        runs=runs,
        suppliers=suppliers,
        total=total,
        success_count=success_count,
        error_count=error_count,
        page=page,
        per_page=per_page,
        total_pages=total_pages,
        supplier_id=supplier_id,
        status=status,
        date_from=date_from,
        date_to=date_to,
    )


@logs_bp.route("/<int:sync_run_id>")
@login_required
def detail(sync_run_id):
    """Single sync run detail page."""
    run = db.session.get(SyncRun, sync_run_id)
    if not run:
        from flask import abort

        abort(404)
    return render_template("logs/detail.html", run=run)
