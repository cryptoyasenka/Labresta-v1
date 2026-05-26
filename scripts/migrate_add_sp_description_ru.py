"""Add SupplierProduct.description_ru column.

The «Новый проект» (NP) native [КАТАЛОГ] feed carries a separate Russian
body (column Q, ``description_ru``) alongside the Ukrainian one (column H).
The existing ``description`` column holds the UA body; this adds the RU twin
so Channel-2 content sync can populate ``PromProduct.description_ru`` from the
feed without the YML round-trip that drops it.

SQLite ``ADD COLUMN`` with no default is additive and nullable — existing rows
get NULL, every other supplier is unaffected.

Idempotent: safe to re-run. Usage:
    python scripts/migrate_add_sp_description_ru.py
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "instance" / "labresta.db"

COLUMNS = [
    ("description_ru", "TEXT"),
]


def column_exists(conn, table: str, column: str) -> bool:
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return any(r[1] == column for r in rows)


def ensure_columns(conn) -> None:
    for name, decl in COLUMNS:
        if column_exists(conn, "supplier_products", name):
            print(f"{name}: already exists — skipping")
            continue
        conn.execute(f"ALTER TABLE supplier_products ADD COLUMN {name} {decl}")
        print(f"{name}: added ({decl})")


if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)
    try:
        ensure_columns(conn)
        conn.commit()
        print("Done.")
    finally:
        conn.close()
