"""Dashboard blueprint: sync status, stats, manual trigger, journal, charts."""

import json
import logging
import tempfile
import threading
from datetime import datetime, timedelta, timezone
from pathlib import Path

from flask import Blueprint, jsonify, render_template, request
from flask_login import login_required
from sqlalchemy import func, select

from app.extensions import db
from app.models.catalog import PromProduct
from app.models.product_match import ProductMatch
from app.models.supplier_product import SupplierProduct
from app.models.sync_run import SyncRun

logger = logging.getLogger(__name__)

dashboard_bp = Blueprint("dashboard", __name__)


# ---------------------------------------------------------------------------
# Sync progress helper — temp-file based progress tracking
# ---------------------------------------------------------------------------
class SyncProgress:
    """Write/read sync progress via a temp JSON file."""

    _progress_file = Path(tempfile.gettempdir()) / "labresta_sync_progress.json"

    @classmethod
    def update(cls, stage, count, total=None, **extra):
        data = {}
        if cls._progress_file.exists():
            try:
                data = json.loads(cls._progress_file.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                data = {}
        data["running"] = True
        data["stage"] = stage
        data.setdefault("stages", {})[stage] = {
            "done": False,
            "count": count,
            "total": total,
            **extra,
        }
        # Mark prior stages as done
        stage_order = [
            "fetching",
            "parsing",
            "saving",
            "matching",
            "yml_generation",
        ]
        current_idx = stage_order.index(stage) if stage in stage_order else -1
        for s in stage_order[:current_idx]:
            if s in data["stages"]:
                data["stages"][s]["done"] = True
        cls._progress_file.write_text(
            json.dumps(data, ensure_ascii=False), encoding="utf-8"
        )

    @classmethod
    def read(cls):
        if cls._progress_file.exists():
            try:
                return json.loads(cls._progress_file.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                pass
        return {"running": False}

    @classmethod
    def complete(cls):
        if cls._progress_file.exists():
            try:
                cls._progress_file.unlink()
            except OSError:
                pass


# ---------------------------------------------------------------------------
# Helper queries
# ---------------------------------------------------------------------------
def _get_aggregate_stats():
    """Return aggregate dashboard statistics."""
    # Latest sync run
    latest_run = db.session.execute(
        select(SyncRun).order_by(SyncRun.started_at.desc()).limit(1)
    ).scalar_one_or_none()

    # Match counts
    match_counts = db.session.execute(
        select(
            ProductMatch.status,
            func.count(ProductMatch.id),
        ).group_by(ProductMatch.status)
    ).all()
    match_map = {status: cnt for status, cnt in match_counts}
    confirmed = match_map.get("confirmed", 0)
    candidate = match_map.get("candidate", 0)
    rejected = match_map.get("rejected", 0)
    manual = match_map.get("manual", 0)
    total_matched = confirmed + candidate + rejected + manual

    # Unmatched prom products (no match record at all)
    matched_prom_ids = select(ProductMatch.prom_product_id).distinct()
    unmatched_count = db.session.execute(
        select(func.count(PromProduct.id)).where(
            PromProduct.id.notin_(matched_prom_ids)
        )
    ).scalar() or 0

    # Unavailable supplier products
    unavailable_count = db.session.execute(
        select(func.count(SupplierProduct.id)).where(
            SupplierProduct.available == False  # noqa: E712
        )
    ).scalar() or 0

    # Recent errors
    error_runs = db.session.execute(
        select(SyncRun)
        .where(SyncRun.status == "error")
        .order_by(SyncRun.started_at.desc())
        .limit(5)
    ).scalars().all()

    # Is sync currently running?
    sync_running = db.session.execute(
        select(func.count(SyncRun.id)).where(SyncRun.status == "running")
    ).scalar() > 0

    # Next sync time
    next_sync_seconds = None
    try:
        from app.scheduler import scheduler

        job = scheduler.get_job("sync_feeds")
        if job and job.next_run_time:
            delta = job.next_run_time - datetime.now(job.next_run_time.tzinfo)
            next_sync_seconds = max(0, int(delta.total_seconds()))
    except Exception:
        pass

    return {
        "last_sync_time": (
            latest_run.started_at.isoformat() + "Z" if latest_run else None
        ),
        "last_sync_status": latest_run.status if latest_run else None,
        "matched_count": confirmed,
        "unmatched_count": unmatched_count,
        "pending_review": candidate,
        "unavailable_count": unavailable_count,
        "total_matched": total_matched,
        "errors": [
            {
                "supplier": r.supplier.name if r.supplier else "Unknown",
                "message": (r.error_message or "")[:200],
                "time": r.started_at.isoformat() + "Z",
            }
            for r in error_runs
        ],
        "next_sync_seconds": next_sync_seconds,
        "sync_running": sync_running,
    }


def _get_journal(limit=20):
    """Return last N sync run records for the journal."""
    runs = db.session.execute(
        select(SyncRun).order_by(SyncRun.started_at.desc()).limit(limit)
    ).scalars().all()
    return [
        {
            "supplier": r.supplier.name if r.supplier else "Unknown",
            "started_at": r.started_at.isoformat() + "Z",
            "completed_at": (
                r.completed_at.isoformat() + "Z" if r.completed_at else None
            ),
            "status": r.status,
            "products_fetched": r.products_fetched or 0,
            "products_created": r.products_created or 0,
            "products_updated": r.products_updated or 0,
            "products_disappeared": r.products_disappeared or 0,
            "match_candidates": r.match_candidates_generated or 0,
            "error_message": (r.error_message or "")[:300],
        }
        for r in runs
    ]


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@dashboard_bp.route("/")
@login_required
def index():
    """Render dashboard page with initial data."""
    stats = _get_aggregate_stats()
    journal = _get_journal()
    return render_template(
        "dashboard/index.html", stats=stats, journal=journal
    )


@dashboard_bp.route("/stats")
@login_required
def stats_api():
    """JSON endpoint for AJAX polling — aggregate stats."""
    return jsonify(_get_aggregate_stats())


@dashboard_bp.route("/sync/trigger", methods=["POST"])
@login_required
def sync_trigger():
    """Trigger manual sync in background thread."""
    from flask import current_app

    # Check if sync already running
    running = db.session.execute(
        select(func.count(SyncRun.id)).where(SyncRun.status == "running")
    ).scalar()
    if running > 0:
        return jsonify({"status": "already_running"}), 409

    app = current_app._get_current_object()
    thread = threading.Thread(
        target=_run_sync_in_context, args=(app,), daemon=True
    )
    thread.start()
    return jsonify({"status": "started"})


@dashboard_bp.route("/journal")
@login_required
def journal_api():
    """JSON endpoint for sync journal polling."""
    return jsonify(_get_journal())


@dashboard_bp.route("/sync/progress")
@login_required
def sync_progress_api():
    """JSON endpoint for sync progress polling."""
    progress = SyncProgress.read()
    if not progress.get("running"):
        # Double-check DB
        running = db.session.execute(
            select(func.count(SyncRun.id)).where(SyncRun.status == "running")
        ).scalar()
        if running > 0:
            return jsonify({"running": True, "stage": "unknown", "stages": {}})
        return jsonify({"running": False})
    return jsonify(progress)


@dashboard_bp.route("/chart-data")
@login_required
def chart_data_api():
    """JSON endpoint for trend chart data."""
    days = min(int(request.args.get("days", 14)), 90)
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)

    date_col = func.date(SyncRun.started_at).label("date")
    rows = db.session.execute(
        select(
            date_col,
            func.sum(SyncRun.match_candidates_generated).label("matches"),
            func.sum(SyncRun.products_updated).label("updated"),
            func.count(SyncRun.id).label("syncs"),
        )
        .where(SyncRun.started_at >= cutoff)
        .group_by(func.date(SyncRun.started_at))
        .order_by(func.date(SyncRun.started_at))
    ).all()

    labels = [str(r.date) if r.date else "" for r in rows]
    matches = [int(r.matches or 0) for r in rows]
    syncs = [int(r.syncs or 0) for r in rows]
    updated = [int(r.updated or 0) for r in rows]

    return jsonify(
        {"labels": labels, "matches": matches, "syncs": syncs, "updated": updated}
    )


# ---------------------------------------------------------------------------
# Background sync helper
# ---------------------------------------------------------------------------
def _run_sync_in_context(app):
    """Run full sync inside Flask app context (for background thread)."""
    with app.app_context():
        from app.services.sync_pipeline import run_full_sync

        try:
            run_full_sync()
        except Exception:
            logger.exception("Background sync failed")
        finally:
            SyncProgress.complete()
