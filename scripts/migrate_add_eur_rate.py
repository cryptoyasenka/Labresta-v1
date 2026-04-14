"""Add eur_rate_uah column to suppliers table (idempotent)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import text

from app import create_app
from app.extensions import db


DEFAULT_RATE = 51.15


def main() -> None:
    app = create_app()
    with app.app_context():
        existing = {
            row[1]
            for row in db.session.execute(text("PRAGMA table_info(suppliers)")).all()
        }
        if "eur_rate_uah" not in existing:
            db.session.execute(
                text(
                    f"ALTER TABLE suppliers ADD COLUMN eur_rate_uah FLOAT DEFAULT {DEFAULT_RATE}"
                )
            )
            print("Added column eur_rate_uah")
        else:
            print("Column eur_rate_uah already exists")

        updated = db.session.execute(
            text("UPDATE suppliers SET eur_rate_uah = :r WHERE eur_rate_uah IS NULL"),
            {"r": DEFAULT_RATE},
        ).rowcount
        db.session.commit()
        print(f"Backfilled {updated} rows with rate {DEFAULT_RATE}")


if __name__ == "__main__":
    main()
