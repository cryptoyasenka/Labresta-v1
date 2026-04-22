"""Add Supplier.pricing_mode + create supplier_brand_discounts table.

Idempotent: safe to re-run. Usage:
    python scripts/migrate_add_brand_discounts.py
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "instance" / "labresta.db"


def column_exists(conn, table: str, column: str) -> bool:
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return any(r[1] == column for r in rows)


def table_exists(conn, table: str) -> bool:
    row = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,)
    ).fetchone()
    return row is not None


def ensure(conn) -> None:
    if column_exists(conn, "suppliers", "pricing_mode"):
        print("suppliers.pricing_mode: already exists — skipping")
    else:
        conn.execute(
            "ALTER TABLE suppliers ADD COLUMN pricing_mode VARCHAR(20) "
            "NOT NULL DEFAULT 'flat'"
        )
        print("suppliers.pricing_mode: added (VARCHAR(20) NOT NULL DEFAULT 'flat')")

    if table_exists(conn, "supplier_brand_discounts"):
        print("supplier_brand_discounts: already exists — skipping")
    else:
        conn.execute(
            """
            CREATE TABLE supplier_brand_discounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                supplier_id INTEGER NOT NULL REFERENCES suppliers(id) ON DELETE CASCADE,
                brand VARCHAR(200) NOT NULL,
                discount_percent REAL NOT NULL DEFAULT 0.0,
                CONSTRAINT uq_supplier_brand UNIQUE (supplier_id, brand)
            )
            """
        )
        conn.execute(
            "CREATE INDEX ix_supplier_brand_discounts_supplier_id "
            "ON supplier_brand_discounts(supplier_id)"
        )
        print("supplier_brand_discounts: created (+uq_supplier_brand, +supplier_id idx)")


if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)
    try:
        ensure(conn)
        conn.commit()
        print("Done.")
    finally:
        conn.close()
