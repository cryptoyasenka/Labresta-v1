"""Add SupplierProduct.stock_status to PostgreSQL on Railway.

Runs at startup via railway.toml startCommand (idempotent).
Uses only stdlib + psycopg2 (available in Railway venv).

Without this column, any SupplierProduct query on prod fails once the model
declares stock_status, so this must run before gunicorn boots.
"""
import os, sys

db_url = os.environ.get("DATABASE_URL", "")
if not db_url or db_url.startswith("sqlite"):
    print("Not a PostgreSQL environment — skipping.", flush=True)
    sys.exit(0)

import psycopg2
conn = psycopg2.connect(db_url)
conn.autocommit = True
cur = conn.cursor()
cur.execute("ALTER TABLE supplier_products ADD COLUMN IF NOT EXISTS stock_status VARCHAR(50)")
cur.close()
conn.close()
print("stock_status migration: done.", flush=True)
