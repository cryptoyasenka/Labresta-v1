from datetime import datetime, timezone

from app.extensions import db


class SyncRun(db.Model):
    __tablename__ = "sync_runs"

    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(
        db.Integer,
        db.ForeignKey("suppliers.id"),
        nullable=False,
        index=True,
    )
    started_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    completed_at = db.Column(db.DateTime, nullable=True)
    status = db.Column(
        db.String(20), nullable=False, default="running"
    )  # running | success | error
    products_fetched = db.Column(db.Integer, default=0)
    products_created = db.Column(db.Integer, default=0)
    products_updated = db.Column(db.Integer, default=0)
    products_disappeared = db.Column(db.Integer, default=0)
    match_candidates_generated = db.Column(db.Integer, default=0)
    error_message = db.Column(db.Text, nullable=True)

    supplier = db.relationship("Supplier")
