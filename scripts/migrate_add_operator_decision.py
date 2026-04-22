"""Add operator_decision / note / at columns to prom_products.

One-shot migration, safe to re-run (checks column existence first).
Usage:
    python scripts/migrate_add_operator_decision.py
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "instance" / "labresta.db"


def column_exists(conn, table: str, column: str) -> bool:
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return any(r[1] == column for r in rows)


def add_column(conn, column: str, decl: str) -> None:
    if column_exists(conn, "prom_products", column):
        print(f"{column}: already present")
        return
    conn.execute(f"ALTER TABLE prom_products ADD COLUMN {column} {decl}")
    print(f"{column}: added")


def main() -> None:
    conn = sqlite3.connect(DB_PATH)
    try:
        add_column(conn, "operator_decision", "VARCHAR(32)")
        add_column(conn, "operator_decision_note", "TEXT")
        add_column(conn, "operator_decision_at", "DATETIME")
        conn.execute(
            "CREATE INDEX IF NOT EXISTS ix_prom_products_operator_decision "
            "ON prom_products (operator_decision)"
        )
        print("index: ensured ix_prom_products_operator_decision")
        conn.commit()
    finally:
        conn.close()


if __name__ == "__main__":
    main()
