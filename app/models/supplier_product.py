from datetime import datetime, timezone

from app.extensions import db


class SupplierProduct(db.Model):
    __tablename__ = "supplier_products"

    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.id"), nullable=False)
    external_id = db.Column(db.String(255), nullable=False)  # offer id from feed
    name = db.Column(db.String(500), nullable=False)
    brand = db.Column(db.String(200), nullable=True)  # <vendor> from YML
    model = db.Column(db.String(200), nullable=True)
    article = db.Column(db.String(255), nullable=True)  # <vendorCode>
    price_cents = db.Column(db.Integer, nullable=True)  # retail price in cents
    currency = db.Column(db.String(10), default="EUR")
    available = db.Column(db.Boolean, default=True)
    needs_review = db.Column(db.Boolean, default=False)
    last_seen_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    last_modified_at = db.Column(db.DateTime, nullable=True)
    price_forced = db.Column(db.Boolean, default=False, server_default="0")
    is_deleted = db.Column(db.Boolean, default=False, server_default="0")

    supplier = db.relationship("Supplier", backref="products")

    __table_args__ = (
        db.UniqueConstraint("supplier_id", "external_id", name="uq_supplier_product"),
    )
