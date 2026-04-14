"""Audit log blueprint: browse operator action history."""

import json

from flask import Blueprint, render_template, request
from flask_login import login_required
from sqlalchemy import func, select

from app.extensions import db
from app.models.audit_log import AuditLog

audit_bp = Blueprint("audit", __name__)

ACTION_LABELS = {
    "confirm": "Підтвердження",
    "confirm_update": "Підтвердження + оновлення",
    "reject": "Відхилення",
    "unconfirm": "Скасування підтвердження",
    "manual_match": "Ручний матч",
    "update_prom": "Редагування каталогу",
    "set_discount": "Зміна знижки",
    "mark_new": "Позначено для додавання",
    "unmark_new": "Знято позначку додавання",
    "bulk_confirm": "Масове підтвердження",
    "bulk_reject": "Масове відхилення",
}


@audit_bp.route("/")
@login_required
def index():
    """Audit log viewer with filtering and pagination."""
    action_filter = request.args.get("action", "all")
    user_filter = request.args.get("user", "all")
    date_from = request.args.get("date_from", "")
    date_to = request.args.get("date_to", "")
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 50, type=int)
    per_page = min(per_page, 100)

    query = select(AuditLog).order_by(AuditLog.timestamp.desc())

    if action_filter and action_filter != "all":
        query = query.where(AuditLog.action == action_filter)
    if user_filter and user_filter != "all":
        query = query.where(AuditLog.user_name == user_filter)
    if date_from:
        query = query.where(AuditLog.timestamp >= date_from)
    if date_to:
        query = query.where(AuditLog.timestamp <= date_to + " 23:59:59")

    count_query = select(func.count()).select_from(query.subquery())
    total = db.session.execute(count_query).scalar() or 0

    offset = (page - 1) * per_page
    entries = db.session.execute(query.offset(offset).limit(per_page)).scalars().all()

    total_pages = max(1, (total + per_page - 1) // per_page)

    # Distinct users for filter dropdown
    users = db.session.execute(
        select(AuditLog.user_name).where(AuditLog.user_name.isnot(None)).distinct()
    ).scalars().all()

    return render_template(
        "audit/index.html",
        entries=entries,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages,
        action_filter=action_filter,
        user_filter=user_filter,
        date_from=date_from,
        date_to=date_to,
        users=sorted(users),
        action_labels=ACTION_LABELS,
        json_module=json,
    )
