from datetime import datetime, timezone

from app.extensions import db


class MatchRule(db.Model):
    """Remembered match rule: maps supplier product name/brand to a prom catalog product."""

    __tablename__ = "match_rules"

    id = db.Column(db.Integer, primary_key=True)
    supplier_product_name_pattern = db.Column(
        db.String(500), nullable=False
    )  # exact name or pattern
    supplier_brand = db.Column(db.String(200), nullable=True)
    prom_product_id = db.Column(
        db.Integer, db.ForeignKey("prom_products.id"), nullable=False
    )
    created_by = db.Column(db.String(100), nullable=False)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )
    is_active = db.Column(db.Boolean, default=True)
    note = db.Column(db.Text, nullable=True)

    prom_product = db.relationship("PromProduct")
