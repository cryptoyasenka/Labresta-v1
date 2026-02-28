"""Notification rule and notification models for configurable alerts."""

from datetime import datetime, timezone

from app.extensions import db


class NotificationRule(db.Model):
    """Configurable rule for triggering notifications on new supplier products."""

    __tablename__ = "notification_rules"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    criteria_type = db.Column(
        db.String(50), nullable=False
    )  # "category", "price_range", "keyword", "brand"
    criteria_value = db.Column(
        db.String(500), nullable=False
    )  # e.g., "coffee", "1000-5000", "espresso,latte"
    telegram_enabled = db.Column(db.Boolean, default=True)
    ui_enabled = db.Column(db.Boolean, default=True)
    is_active = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    notifications = db.relationship(
        "Notification", backref="rule", lazy="dynamic"
    )

    def __repr__(self):
        return f"<NotificationRule {self.id}: {self.name} ({self.criteria_type})>"


class Notification(db.Model):
    """Individual notification generated when a product matches a rule."""

    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    rule_id = db.Column(
        db.Integer, db.ForeignKey("notification_rules.id"), nullable=False
    )
    supplier_product_id = db.Column(
        db.Integer, db.ForeignKey("supplier_products.id"), nullable=True
    )
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    supplier_product = db.relationship("SupplierProduct", backref="notifications")

    def __repr__(self):
        return f"<Notification {self.id}: rule={self.rule_id} read={self.is_read}>"
