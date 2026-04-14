from datetime import datetime, timezone

from app.extensions import db


class AuditLog(db.Model):
    """Operator action audit trail.

    Records every match-related action: confirm, reject, unconfirm,
    manual match, update-prom, mark-new, bulk confirm/reject, etc.
    """

    __tablename__ = "audit_log"

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), index=True
    )
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    user_name = db.Column(db.String(255), nullable=True)
    action = db.Column(db.String(50), nullable=False, index=True)
    # confirm | reject | unconfirm | manual_match | update_prom |
    # mark_new | unmark_new | bulk_confirm | bulk_reject | set_discount

    match_id = db.Column(db.Integer, nullable=True)
    supplier_product_id = db.Column(db.Integer, nullable=True)
    prom_product_id = db.Column(db.Integer, nullable=True)
    details = db.Column(db.Text, nullable=True)  # JSON string with action-specific data

    user = db.relationship("User", backref=db.backref("audit_logs", lazy="dynamic"))
