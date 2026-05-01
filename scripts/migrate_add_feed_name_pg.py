"""Add ProductMatch.feed_name to PostgreSQL on Railway.

Runs at startup via railway.toml startCommand (idempotent).
Uses only stdlib + psycopg2 (available in Railway venv).
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
cur.execute("ALTER TABLE product_matches ADD COLUMN IF NOT EXISTS feed_name VARCHAR(500)")
cur.close()
conn.close()
print("feed_name migration: done.", flush=True)
