"""Create custom_feeds table for ad-hoc YML feeds (Phase K.2).

Idempotent: skips if table exists.

Usage:
    .venv/Scripts/python.exe scripts/migrate_add_custom_feeds.py
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "instance" / "labresta.db"

DDL = """
CREATE TABLE custom_feeds (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    token           VARCHAR(16) NOT NULL UNIQUE,
    match_ids_json  TEXT NOT NULL,
    name            VARCHAR(200),
    filename        VARCHAR(200) NOT NULL,
    created_at      DATETIME,
    updated_at      DATETIME
)
"""


def table_exists(conn, name: str) -> bool:
    row = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (name,)
    ).fetchone()
    return row is not None


if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)
    try:
        if table_exists(conn, "custom_feeds"):
            print("custom_feeds: table already exists - skipping")
        else:
            conn.execute(DDL)
            print("custom_feeds: table created")
        conn.commit()
        print("Done.")
    finally:
        conn.close()
