from datetime import datetime, timezone

from app.extensions import db


class Supplier(db.Model):
    __tablename__ = "suppliers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    feed_url = db.Column(db.String(500), nullable=True)
    discount_percent = db.Column(db.Float, default=0.0)  # e.g. 15.0 for 15%
    column_mapping = db.Column(db.Text, nullable=True)  # JSON: {"header_row": int, "columns": {col_idx: field}}
    is_enabled = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    last_fetched_at = db.Column(db.DateTime, nullable=True)
    last_fetch_status = db.Column(db.String(50), nullable=True)  # 'success', 'error'
    last_fetch_error = db.Column(db.Text, nullable=True)
