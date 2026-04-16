"""Add suppliers.slug column for per-supplier feed URLs (Phase K.1).

Adds:
  - slug VARCHAR(50) NOT NULL DEFAULT '' (then backfilled and unique-indexed)

Idempotent: safe to re-run. Backfills slugs from supplier names via
slugify_supplier_name() so existing rows get e.g. MARESTO → 'maresto'.

Conflict handling: if two suppliers transliterate to the same slug, the second
gets a numeric suffix ('-2', '-3', ...). Manual rename via UI later if needed.

Usage:
    .venv/Scripts/python.exe scripts/migrate_add_supplier_slug.py
"""

import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.models.supplier import slugify_supplier_name  # noqa: E402

DB_PATH = Path(__file__).resolve().parent.parent / "instance" / "labresta.db"


def column_exists(conn, table: str, column: str) -> bool:
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return any(r[1] == column for r in rows)


def index_exists(conn, name: str) -> bool:
    row = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='index' AND name=?", (name,)
    ).fetchone()
    return row is not None


def ensure_slug_column(conn) -> None:
    if column_exists(conn, "suppliers", "slug"):
        print("slug: column already exists — skipping ALTER")
    else:
        conn.execute(
            "ALTER TABLE suppliers ADD COLUMN slug VARCHAR(50) NOT NULL DEFAULT ''"
        )
        print("slug: column added")


def backfill_slugs(conn) -> None:
    rows = conn.execute("SELECT id, name, slug FROM suppliers ORDER BY id").fetchall()
    used: set[str] = {r[2] for r in rows if r[2]}
    for sid, name, slug in rows:
        if slug:
            continue
        base = slugify_supplier_name(name)
        candidate = base
        n = 2
        while candidate in used:
            candidate = f"{base}-{n}"
            n += 1
        used.add(candidate)
        conn.execute("UPDATE suppliers SET slug=? WHERE id=?", (candidate, sid))
        print(f"slug: supplier #{sid} '{name.encode('ascii', 'replace').decode()}' -> '{candidate}'")


def ensure_unique_index(conn) -> None:
    if index_exists(conn, "uq_supplier_slug"):
        print("uq_supplier_slug: index already exists — skipping")
        return
    conn.execute("CREATE UNIQUE INDEX uq_supplier_slug ON suppliers(slug)")
    print("uq_supplier_slug: index created")


if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)
    try:
        ensure_slug_column(conn)
        backfill_slugs(conn)
        ensure_unique_index(conn)
        conn.commit()
        print("Done.")
    finally:
        conn.close()
