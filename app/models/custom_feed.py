"""CustomFeed — registry of ad-hoc multi-product YML feeds with stable URLs.

Each row maps a deterministic token (sha256 of sorted match_ids) to:
  - the match_ids it covers (JSON list)
  - the generated filename (labresta-feed-custom-<token>.yml)
  - optional human-readable name

Lifecycle: tokens live forever until explicitly deleted via /feeds/custom UI.
Re-generating an existing token (same set of match_ids) updates the file in place.
"""

import json
from datetime import datetime, timezone

from app.extensions import db


class CustomFeed(db.Model):
    __tablename__ = "custom_feeds"

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(16), nullable=False, unique=True)
    match_ids_json = db.Column(db.Text, nullable=False)
    name = db.Column(db.String(200), nullable=True)
    filename = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    @property
    def match_ids(self) -> list[int]:
        try:
            return json.loads(self.match_ids_json or "[]")
        except (TypeError, ValueError):
            return []

    @match_ids.setter
    def match_ids(self, ids: list[int]) -> None:
        self.match_ids_json = json.dumps(sorted(int(i) for i in ids))
