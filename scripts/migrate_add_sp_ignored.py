"""Add SupplierProduct.ignored flag.

Operator-driven exclusion for supplier products that should not appear in
/matches or the default /products/supplier view (e.g. brandless offers we
have no intention of cataloging).

Idempotent: safe to re-run. Usage:
    python scripts/migrate_add_sp_ignored.py
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "instance" / "labresta.db"

COLUMNS = [
    ("ignored", "BOOLEAN NOT NULL DEFAULT 0"),
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
