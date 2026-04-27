"""Add parser_type column to suppliers table.

Idempotent: safe to run multiple times.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app import create_app
from app.extensions import db


def run():
    app = create_app()
    with app.app_context():
        with db.engine.connect() as conn:
            cols = [
                row[1]
                for row in conn.execute(
                    db.text("PRAGMA table_info(suppliers)")
                ).fetchall()
            ]
            if "parser_type" not in cols:
                conn.execute(
                    db.text(
                        "ALTER TABLE suppliers ADD COLUMN parser_type VARCHAR(20) NOT NULL DEFAULT 'auto'"
                    )
                )
                conn.commit()
                print("Added parser_type column.")
            else:
                print("parser_type already present, skipping.")


if __name__ == "__main__":
    run()
