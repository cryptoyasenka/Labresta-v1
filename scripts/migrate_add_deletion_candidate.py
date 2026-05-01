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

# Backfill: confirmed/manual matches where supplier product already disappeared
# before this feature was introduced (available=False, needs_review=True).
cur.execute("""
    UPDATE product_matches pm
    SET deletion_candidate = TRUE
    FROM supplier_products sp
    WHERE pm.supplier_product_id = sp.id
      AND pm.status IN ('confirmed', 'manual')
      AND pm.deletion_candidate = FALSE
      AND sp.available = FALSE
      AND sp.needs_review = TRUE
""")
backfill_count = cur.rowcount
print(f"deletion_candidate backfill: {backfill_count} matches flagged.", flush=True)

cur.close()
conn.close()
print("deletion_candidate migration: done.", flush=True)
