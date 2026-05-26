"""Read-only НП-фид × локальная БД снимок матчинга.

НИЧЕГО не пишет в БД и в репо. Открывает labresta.db в mode=ro.
Выход: snapshot stdout-файл (UTF-8) в план-каталоге.
"""
import json
import sqlite3
import sys

DB = r"C:\Projects\labresta-sync\instance\labresta.db"
OUT = r"C:\Users\Yana\labresta-np-feed-plan\scratch_np_snapshot.txt"

SCOPE = ["HURAKAN", "APACH", "FAGOR", "TATRA", "COLD",
         "PROJECT SYSTEMS", "ASTORIA", "ARRIS", "MAXIMA"]

con = sqlite3.connect(f"file:{DB}?mode=ro&immutable=1", uri=True)
con.row_factory = sqlite3.Row
c = con.cursor()

lines = []
def w(s=""):
    lines.append(str(s))

# --- supplier id for НП ---
sup = c.execute(
    "SELECT id, name, slug FROM suppliers WHERE slug='novyy-proekt' OR id=2"
).fetchall()
w("SUPPLIERS (НП):")
for r in sup:
    w(f"  id={r['id']} slug={r['slug']} name={r['name']}")
SUP_ID = 2

# --- total НП supplier_products ---
tot = c.execute(
    "SELECT COUNT(*) n, SUM(is_deleted) d FROM supplier_products WHERE supplier_id=?",
    (SUP_ID,)).fetchone()
w(f"\nНП supplier_products: total={tot['n']}  is_deleted={tot['d']}")

# --- matched (confirmed/manual + published) total ---
q_matched = """
SELECT COUNT(DISTINCT sp.id) n
FROM supplier_products sp
JOIN product_matches pm ON pm.supplier_product_id = sp.id
WHERE sp.supplier_id=? AND sp.is_deleted=0
  AND pm.status IN ('confirmed','manual') AND pm.published=1
"""
m = c.execute(q_matched, (SUP_ID,)).fetchone()
w(f"НП matched (confirmed/manual & published=1): {m['n']}")

q_matched_any = """
SELECT COUNT(DISTINCT sp.id) n
FROM supplier_products sp
JOIN product_matches pm ON pm.supplier_product_id = sp.id
WHERE sp.supplier_id=? AND sp.is_deleted=0
  AND pm.status IN ('confirmed','manual')
"""
ma = c.execute(q_matched_any, (SUP_ID,)).fetchone()
w(f"НП matched (confirmed/manual, любой published): {ma['n']}")

# --- per-brand breakdown (matched & published) ---
w("\nПо брендам (matched confirmed/manual & published=1):")
q_brand = """
SELECT UPPER(TRIM(sp.brand)) b, COUNT(DISTINCT sp.id) n
FROM supplier_products sp
JOIN product_matches pm ON pm.supplier_product_id = sp.id
WHERE sp.supplier_id=? AND sp.is_deleted=0
  AND pm.status IN ('confirmed','manual') AND pm.published=1
GROUP BY UPPER(TRIM(sp.brand)) ORDER BY n DESC
"""
rows = c.execute(q_brand, (SUP_ID,)).fetchall()
scope_total = 0
for r in rows:
    b = r["b"] or "(пусто)"
    inscope = "SCOPE" if (b in SCOPE) else "-"
    if b in SCOPE:
        scope_total += r["n"]
    w(f"  {b:<22} {r['n']:>4}   {inscope}")
w(f"\n  ИТОГО в scope (9 брендов, matched&published): {scope_total}")

# --- all НП supplier_products per brand (для контекста объёма) ---
w("\nВсе НП sp по брендам (для контекста, не только matched):")
q_all_brand = """
SELECT UPPER(TRIM(brand)) b, COUNT(*) n
FROM supplier_products WHERE supplier_id=? AND is_deleted=0
GROUP BY UPPER(TRIM(brand)) ORDER BY n DESC
"""
for r in c.execute(q_all_brand, (SUP_ID,)).fetchall():
    b = r["b"] or "(пусто)"
    if b in SCOPE:
        w(f"  {b:<22} {r['n']:>4}   SCOPE")

# --- канарейка HKN-PICO12M ---
w("\n--- КАНАРЕЙКА HKN-PICO12M ---")
q_canary = """
SELECT sp.id sp_id, sp.article, sp.brand, sp.name sp_name,
       sp.description IS NOT NULL AND sp.description<>'' has_desc,
       sp.image_url, sp.images,
       pm.id pm_id, pm.status, pm.published,
       pp.id pp_id, pp.external_id, pp.name pp_name,
       pp.description_ua IS NOT NULL AND pp.description_ua<>'' has_ua,
       pp.description_ru IS NOT NULL AND pp.description_ru<>'' has_ru,
       pp.image_url pp_img, pp.images pp_images
FROM supplier_products sp
LEFT JOIN product_matches pm ON pm.supplier_product_id = sp.id
     AND pm.status IN ('confirmed','manual')
LEFT JOIN prom_products pp ON pp.id = pm.prom_product_id
WHERE sp.supplier_id=? AND UPPER(sp.article) LIKE 'HKN-PICO12M%'
"""
can = c.execute(q_canary, (SUP_ID,)).fetchall()
if not can:
    w("  НЕ НАЙДЕНО по article LIKE 'HKN-PICO12M%' — пробую по name")
    can = c.execute(
        "SELECT id sp_id, article, brand, name sp_name FROM supplier_products "
        "WHERE supplier_id=? AND UPPER(name) LIKE '%PICO12M%'", (SUP_ID,)).fetchall()
for r in can:
    w(f"  sp_id={r['sp_id']} article={r['article']} brand={r['brand']}")
    w(f"  sp_name={r['sp_name']}")
    keys = r.keys()
    if "pm_id" in keys:
        w(f"  match: pm_id={r['pm_id']} status={r['status']} published={r['published']}")
        w(f"  pp_id={r['pp_id']} external_id={r['external_id']}")
        w(f"  pp_name={r['pp_name']}")
        w(f"  pp has_ua={r['has_ua']} has_ru={r['has_ru']} pp_img={r['pp_img']}")
        w(f"  pp_images={r['pp_images']}")

con.close()
with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("OK written", OUT)
