"""Add display_article column to prom_products and backfill from Horoshop xlsx.

One-shot migration — safe to re-run (checks column existence first).
Usage:
    python scripts/migrate_add_display_article.py [path-to-horoshop-export.xlsx]

If the xlsx path is omitted, the column is added but nothing is backfilled.
"""

import sys
from pathlib import Path

import sqlite3

import openpyxl

DB_PATH = Path(__file__).resolve().parent.parent / "instance" / "labresta.db"


def column_exists(conn, table: str, column: str) -> bool:
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return any(r[1] == column for r in rows)


def ensure_column(conn):
    if column_exists(conn, "prom_products", "display_article"):
        print("display_article column already exists — skipping ALTER")
    else:
        conn.execute(
            "ALTER TABLE prom_products ADD COLUMN display_article VARCHAR(255)"
        )
        print("Added display_article column")
    conn.execute(
        "CREATE INDEX IF NOT EXISTS ix_prom_products_display_article "
        "ON prom_products (display_article)"
    )
    print("Ensured ix_prom_products_display_article index")


def backfill(conn, xlsx_path: str):
    wb = openpyxl.load_workbook(xlsx_path, read_only=True)
    ws = wb.active
    rows = ws.iter_rows(values_only=True)
    headers = [str(h or "").strip().lower() for h in next(rows)]
    idx_artikul = headers.index("артикул")
    idx_display = headers.index("артикул для отображения на сайте")

    updated = 0
    missing = 0
    skipped_empty = 0
    for row in rows:
        if not row or row[idx_artikul] is None:
            continue
        ext_id = str(row[idx_artikul]).strip()
        display = row[idx_display]
        if display is None or str(display).strip() == "":
            skipped_empty += 1
            continue
        display = str(display).strip()

        cur = conn.execute(
            "UPDATE prom_products SET display_article = ? "
            "WHERE external_id = ? AND (display_article IS NULL OR display_article != ?)",
            (display, ext_id, display),
        )
        if cur.rowcount > 0:
            updated += cur.rowcount
        else:
            check = conn.execute(
                "SELECT 1 FROM prom_products WHERE external_id = ?", (ext_id,)
            ).fetchone()
            if not check:
                missing += 1

    wb.close()
    print(
        f"Backfill: updated={updated}, not-in-db={missing}, "
        f"xlsx-rows-without-display={skipped_empty}"
    )


if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)
    try:
        ensure_column(conn)
        if len(sys.argv) > 1:
            backfill(conn, sys.argv[1])
        else:
            print("No xlsx path given — ALTER only, no backfill")
        conn.commit()
    finally:
        conn.close()
