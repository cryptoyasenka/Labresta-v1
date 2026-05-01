"""Add ProductMatch.feed_name — custom offer name for Horoshop YML.

When set, this name is used in <name> instead of pp.name. Allows operators
to fix names before upload without touching the Horoshop catalog.

Idempotent: safe to re-run. Usage:
    python scripts/migrate_add_feed_name.py
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "instance" / "labresta.db"


def column_exists(conn, table: str, column: str) -> bool:
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return any(r[1] == column for r in rows)


if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)
    try:
        if column_exists(conn, "product_matches", "feed_name"):
            print("feed_name: already exists — skipping")
        else:
            conn.execute("ALTER TABLE product_matches ADD COLUMN feed_name VARCHAR(500)")
            print("feed_name: added (VARCHAR(500) NULL)")
        conn.commit()
        print("Done.")
    finally:
        conn.close()
