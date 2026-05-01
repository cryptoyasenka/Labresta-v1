"""Add ProductMatch.feed_name to PostgreSQL on Railway.

Usage: railway run python scripts/migrate_add_feed_name_pg.py
"""
import sys
from app import create_app
from app.extensions import db

app = create_app()
with app.app_context():
    with db.engine.connect() as conn:
        conn.execute(db.text(
            "ALTER TABLE product_matches ADD COLUMN IF NOT EXISTS feed_name VARCHAR(500)"
        ))
        conn.commit()
    print("feed_name: added (or already existed). Done.", flush=True)

sys.exit(0)
