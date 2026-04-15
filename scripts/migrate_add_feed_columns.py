"""Add feed-management columns to product_matches (Phase A).

Adds:
  - price_synced_at        DATETIME NULL
  - availability_synced_at DATETIME NULL
  - in_feed                BOOLEAN  DEFAULT 0
  - published              BOOLEAN  DEFAULT 1

Idempotent: safe to re-run. Usage:
    python scripts/migrate_add_feed_columns.py
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "instance" / "labresta.db"

COLUMNS = [
    ("price_synced_at", "DATETIME"),
    ("availability_synced_at", "DATETIME"),
    ("in_feed", "BOOLEAN NOT NULL DEFAULT 0"),
    ("published", "BOOLEAN NOT NULL DEFAULT 1"),
]


def column_exists(conn, table: str, column: str) -> bool:
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return any(r[1] == column for r in rows)


def ensure_columns(conn) -> None:
    for name, decl in COLUMNS:
        if column_exists(conn, "product_matches", name):
            print(f"{name}: already exists — skipping")
            continue
        conn.execute(f"ALTER TABLE product_matches ADD COLUMN {name} {decl}")
        print(f"{name}: added ({decl})")


if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)
    try:
        ensure_columns(conn)
        conn.commit()
        print("Done.")
    finally:
        conn.close()
