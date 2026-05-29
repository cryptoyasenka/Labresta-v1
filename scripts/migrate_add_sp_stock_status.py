"""Add SupplierProduct.stock_status (local SQLite).

Raw MARESTO <stock> value (In stock / Running low / Reserved / Out of stock),
mapped to a Horoshop «Наявність» status by app/services/maresto_stock.py.

Idempotent: safe to re-run. Usage:
    python scripts/migrate_add_sp_stock_status.py
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "instance" / "labresta.db"

COLUMNS = [
    ("stock_status", "VARCHAR(50)"),
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
