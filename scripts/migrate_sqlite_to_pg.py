"""One-shot migration: local SQLite -> Railway PostgreSQL."""

import sqlite3
import os
import sys

import psycopg2
import psycopg2.extras

PG_URL = os.environ["DATABASE_URL"]
SQLITE_PATH = os.path.join(os.path.dirname(__file__), "..", "instance", "labresta.db")

# Insert order respects FK deps; reverse for truncate
TABLE_ORDER = [
    "users",
    "suppliers",
    "prom_products",
    "supplier_brand_discounts",
    "supplier_products",
    "sync_runs",
    "product_matches",
    "match_rules",
    "notification_rules",
    "notifications",
    "audit_log",
    "custom_feeds",
]


def pg_connect(url: str):
    # railway gives postgresql://, psycopg2 needs it too
    return psycopg2.connect(url)


def get_sqlite_rows(conn: sqlite3.Connection, table: str):
    cur = conn.execute(f'SELECT * FROM "{table}"')
    cols = [d[0] for d in cur.description]
    rows = cur.fetchall()
    return cols, rows


def get_bool_columns(cur, table: str) -> set:
    """Return set of column names that are boolean in PostgreSQL."""
    cur.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = %s
          AND data_type = 'boolean'
    """, (table,))
    return {row[0] for row in cur.fetchall()}


def cast_row(row, cols, bool_cols):
    result = []
    for val, col in zip(row, cols):
        if col in bool_cols and isinstance(val, int):
            result.append(bool(val))
        else:
            result.append(val)
    return result


def main():
    print(f"Connecting to SQLite: {SQLITE_PATH}")
    sq = sqlite3.connect(SQLITE_PATH)

    print("Connecting to PostgreSQL...")
    pg = pg_connect(PG_URL)
    pg.autocommit = False
    cur = pg.cursor()

    # Widen columns that have longer data in SQLite than VARCHAR(500) allows
    print("Widening oversized columns...")
    widen = [
        ("prom_products", "image_url"),
        ("prom_products", "description_ua"),
        ("prom_products", "description_ru"),
        ("supplier_products", "description"),
        ("supplier_products", "images"),
        ("supplier_products", "params"),
        ("audit_log", "details"),
    ]
    for tbl, col in widen:
        cur.execute(f'ALTER TABLE "{tbl}" ALTER COLUMN "{col}" TYPE TEXT')
        print(f"  {tbl}.{col} -> TEXT")

    # Disable FK checks during bulk load
    cur.execute("SET session_replication_role = replica;")

    # Truncate all at once (avoids deadlock with concurrent app connections)
    print("Truncating PostgreSQL tables...")
    tables_sql = ", ".join([f'"{t}"' for t in reversed(TABLE_ORDER)])
    cur.execute(f"TRUNCATE {tables_sql} CASCADE;")
    print("  all tables truncated")

    # Copy data
    for table in TABLE_ORDER:
        cols, rows = get_sqlite_rows(sq, table)
        if not rows:
            print(f"  {table}: 0 rows - skip")
            continue

        bool_cols = get_bool_columns(cur, table)
        casted = [cast_row(r, cols, bool_cols) for r in rows]

        placeholders = ",".join(["%s"] * len(cols))
        col_names = ",".join([f'"{c}"' for c in cols])
        sql = f'INSERT INTO "{table}" ({col_names}) VALUES ({placeholders})'

        psycopg2.extras.execute_batch(cur, sql, casted, page_size=500)
        print(f"  {table}: {len(rows)} rows inserted")

    # Re-enable FK checks
    cur.execute("SET session_replication_role = DEFAULT;")

    # Reset sequences so next INSERT gets correct auto-id
    print("Resetting sequences...")
    cur.execute("""
        SELECT table_name, column_name
        FROM information_schema.columns
        WHERE table_schema = 'public'
          AND column_default LIKE 'nextval%'
    """)
    seq_cols = cur.fetchall()
    for tbl, col in seq_cols:
        cur.execute(f"""
            SELECT setval(
                pg_get_serial_sequence('{tbl}', '{col}'),
                COALESCE((SELECT MAX("{col}") FROM "{tbl}"), 1)
            )
        """)
        print(f"  reset sequence for {tbl}.{col}")

    pg.commit()
    print("\nMigration complete.")
    sq.close()
    pg.close()


if __name__ == "__main__":
    main()
