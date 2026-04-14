"""Audit logging helper — records operator actions to audit_log table."""

import json

from flask_login import current_user

from app.extensions import db
from app.models.audit_log import AuditLog


def log_action(
    action: str,
    match_id: int | None = None,
    supplier_product_id: int | None = None,
    prom_product_id: int | None = None,
    details: dict | None = None,
):
    """Record an operator action. Call before db.session.commit()."""
    entry = AuditLog(
        user_id=current_user.id if current_user and current_user.is_authenticated else None,
        user_name=current_user.name if current_user and current_user.is_authenticated else None,
        action=action,
        match_id=match_id,
        supplier_product_id=supplier_product_id,
        prom_product_id=prom_product_id,
        details=json.dumps(details, ensure_ascii=False) if details else None,
    )
    db.session.add(entry)
