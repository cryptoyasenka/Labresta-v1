from datetime import datetime, timezone

from app.extensions import db


class PromProduct(db.Model):
    __tablename__ = "prom_products"

    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.String(255), unique=True, nullable=False)  # Identifier_tovaru
    name = db.Column(db.String(500), nullable=False)  # Название (UA)
    name_ru = db.Column(db.String(500), nullable=True)  # Название (RU)
    brand = db.Column(db.String(200), nullable=True)
    model = db.Column(db.String(200), nullable=True)
    article = db.Column(db.String(255), nullable=True)  # Kod_tovaru
    display_article = db.Column(db.String(255), nullable=True)  # "Артикул для відображення на сайті" (manufacturer SKU shown on the product page, e.g. Sirman 60SN002)
    price = db.Column(db.Integer, nullable=True)  # cents (integer)
    currency = db.Column(db.String(10), default="EUR")
    page_url = db.Column(db.String(500), nullable=True)
    image_url = db.Column(db.String(500), nullable=True)  # Main photo
    images = db.Column(db.Text, nullable=True)  # Gallery URLs, JSON array
    description_ua = db.Column(db.Text, nullable=True)
    description_ru = db.Column(db.Text, nullable=True)
    imported_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        db.Index("ix_prom_products_brand", "brand"),
        db.Index("ix_prom_products_name", "name"),
        db.Index("ix_prom_products_display_article", "display_article"),
    )
