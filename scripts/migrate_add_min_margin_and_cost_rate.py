"""Add min_margin_uah and cost_rate columns to suppliers table (idempotent)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import text

from app import create_app
from app.extensions import db


DEFAULT_MIN_MARGIN = 500.0
DEFAULT_COST_RATE = 0.75


def main() -> None:
    app = create_app()
    with app.app_context():
        existing = {
            row[1]
            for row in db.session.execute(text("PRAGMA table_info(suppliers)")).all()
        }

        if "min_margin_uah" not in existing:
            db.session.execute(
                text(
                    f"ALTER TABLE suppliers ADD COLUMN min_margin_uah FLOAT DEFAULT {DEFAULT_MIN_MARGIN}"
                )
            )
            print("Added column min_margin_uah")
        else:
            print("Column min_margin_uah already exists")

        if "cost_rate" not in existing:
            db.session.execute(
                text(
                    f"ALTER TABLE suppliers ADD COLUMN cost_rate FLOAT DEFAULT {DEFAULT_COST_RATE}"
                )
            )
            print("Added column cost_rate")
        else:
            print("Column cost_rate already exists")

        updated_min = db.session.execute(
            text("UPDATE suppliers SET min_margin_uah = :v WHERE min_margin_uah IS NULL"),
            {"v": DEFAULT_MIN_MARGIN},
        ).rowcount
        updated_cost = db.session.execute(
            text("UPDATE suppliers SET cost_rate = :v WHERE cost_rate IS NULL"),
            {"v": DEFAULT_COST_RATE},
        ).rowcount
        db.session.commit()
        print(f"Backfilled {updated_min} rows with min_margin_uah={DEFAULT_MIN_MARGIN}")
        print(f"Backfilled {updated_cost} rows with cost_rate={DEFAULT_COST_RATE}")


if __name__ == "__main__":
    main()
