"""Add ProductMatch.deletion_candidate to PostgreSQL on Railway.

Runs at startup via railway.toml startCommand (idempotent).
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
cur.execute(
    "ALTER TABLE product_matches ADD COLUMN IF NOT EXISTS "
    "deletion_candidate BOOLEAN NOT NULL DEFAULT FALSE"
)
cur.close()
conn.close()
print("deletion_candidate migration: done.", flush=True)
