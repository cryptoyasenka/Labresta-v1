"""Add partial unique index: each prom_product may have at most one
confirmed/manual match.

Safe to run repeatedly. Aborts if existing data violates the constraint
(lists the offending prom_product_ids and does not touch the DB).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import text

from app import create_app
from app.extensions import db


INDEX_NAME = "uq_match_prom_confirmed"
INDEX_SQL = (
    f"CREATE UNIQUE INDEX {INDEX_NAME} "
    "ON product_matches (prom_product_id) "
    "WHERE status IN ('confirmed', 'manual')"
)


def main() -> None:
    app = create_app()
    with app.app_context():
        existing = db.session.execute(
            text(
                "SELECT name FROM sqlite_master WHERE type='index' AND name=:n"
            ),
            {"n": INDEX_NAME},
        ).scalar()
        if existing:
            print(f"Index {INDEX_NAME} already exists")
            return

        violations = db.session.execute(
            text(
                "SELECT prom_product_id, COUNT(*) c "
                "FROM product_matches WHERE status IN ('confirmed','manual') "
                "GROUP BY prom_product_id HAVING c > 1"
            )
        ).all()
        if violations:
            print(
                f"ABORT: {len(violations)} prom_product(s) already have multiple "
                "confirmed/manual matches. Resolve them first."
            )
            for pp_id, c in violations[:20]:
                print(f"  pp#{pp_id}: {c}")
            if len(violations) > 20:
                print(f"  ... and {len(violations) - 20} more")
            sys.exit(1)

        db.session.execute(text(INDEX_SQL))
        db.session.commit()
        print(f"Created partial unique index {INDEX_NAME}")


if __name__ == "__main__":
    main()
