"""Add suppliers.auto_sync_enabled to PostgreSQL on Railway.

Runs at startup via railway.toml startCommand (idempotent).
Uses only stdlib + psycopg2.
"""
import os
import sys

db_url = os.environ.get("DATABASE_URL", "")
if not db_url or db_url.startswith("sqlite"):
    print("Not a PostgreSQL environment - skipping.", flush=True)
    sys.exit(0)

import psycopg2

conn = psycopg2.connect(db_url)
conn.autocommit = True
cur = conn.cursor()
cur.execute(
    "ALTER TABLE suppliers "
    "ADD COLUMN IF NOT EXISTS auto_sync_enabled BOOLEAN NOT NULL DEFAULT TRUE"
)
cur.close()
conn.close()
print("auto_sync_enabled migration: done.", flush=True)
