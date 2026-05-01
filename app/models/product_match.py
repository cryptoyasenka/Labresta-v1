from datetime import datetime, timezone

from app.extensions import db


class ProductMatch(db.Model):
    __tablename__ = "product_matches"

    id = db.Column(db.Integer, primary_key=True)
    supplier_product_id = db.Column(
        db.Integer,
        db.ForeignKey("supplier_products.id"),
        nullable=False,
        index=True,
    )
    prom_product_id = db.Column(
        db.Integer,
        db.ForeignKey("prom_products.id"),
        nullable=False,
    )
    score = db.Column(db.Float, nullable=False)  # fuzzy confidence 0-100
    status = db.Column(
        db.String(20),
        nullable=False,
        default="candidate",
        index=True,
    )  # candidate | confirmed | rejected | manual
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )
    confirmed_at = db.Column(db.DateTime, nullable=True)
    confirmed_by = db.Column(db.String(100), nullable=True)  # Phase 4 username
    discount_percent = db.Column(
        db.Float, nullable=True
    )  # Per-product override; NULL = use supplier default
    name_synced = db.Column(db.Boolean, default=False, server_default="0")  # Name updated from supplier
    feed_name = db.Column(db.String(500), nullable=True)  # Override name in Horoshop YML; NULL = use pp.name
    price_synced_at = db.Column(db.DateTime, nullable=True)
    availability_synced_at = db.Column(db.DateTime, nullable=True)
    in_feed = db.Column(db.Boolean, nullable=False, default=False, server_default="0")
    published = db.Column(db.Boolean, nullable=False, default=True, server_default="1")

    supplier_product = db.relationship("SupplierProduct")
    prom_product = db.relationship("PromProduct")

    __table_args__ = (
        db.UniqueConstraint(
            "supplier_product_id",
            "prom_product_id",
            name="uq_match_pair",
        ),
    )
