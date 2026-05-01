"""Run brand normalization SQL directly via psycopg2 (Railway production)."""
import os, sys

db_url = os.environ.get("DATABASE_URL", "")
if not db_url or db_url.startswith("sqlite"):
    print("Not a PostgreSQL environment — skipping.", flush=True)
    sys.exit(0)

import psycopg2
conn = psycopg2.connect(db_url)
conn.autocommit = False
cur = conn.cursor()

sql = """
WITH brand_counts AS (
    SELECT brand, COUNT(*) AS cnt, LOWER(brand) AS brand_lower
    FROM supplier_products
    WHERE brand IS NOT NULL AND brand <> ''
    GROUP BY brand
),
canonicals AS (
    SELECT DISTINCT ON (brand_lower) brand_lower, brand AS canonical
    FROM brand_counts
    ORDER BY brand_lower, cnt DESC
)
UPDATE supplier_products sp
SET brand = c.canonical
FROM canonicals c
WHERE LOWER(sp.brand) = c.brand_lower
  AND sp.brand <> c.canonical
"""

cur.execute(sql)
print(f"Brand normalization: updated {cur.rowcount} rows.", flush=True)
conn.commit()
cur.close()
conn.close()
