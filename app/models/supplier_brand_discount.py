"""Per-supplier, per-brand discount overrides.

Used when Supplier.pricing_mode == 'per_brand': the final customer-facing
discount for a ProductMatch depends on the supplier product's brand, not
a flat rate. See app/services/pricing.resolve_discount_percent.
"""

from app.extensions import db


class SupplierBrandDiscount(db.Model):
    __tablename__ = "supplier_brand_discounts"

    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(
        db.Integer,
        db.ForeignKey("suppliers.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    brand = db.Column(db.String(200), nullable=False)
    discount_percent = db.Column(db.Float, nullable=False, default=0.0)

    supplier = db.relationship(
        "Supplier",
        backref=db.backref("brand_discounts", cascade="all, delete-orphan"),
    )

    __table_args__ = (
        db.UniqueConstraint("supplier_id", "brand", name="uq_supplier_brand"),
    )
