"""READ-ONLY probe: replicate yml_generator._build_offer_xml pricing/availability
for the HKN-PICO12M canary (pp external_id=1546341257) EXACTLY as the live feed
does after the matcher. No writes anywhere. Opens repo DB with mode=ro.

Mirrors (verbatim logic, repo read-only, copied not imported to avoid Flask app
context / repo touch):
  pricing.resolve_discount_percent
  pricing.clamp_discount_for_min_margin
  pricing.calculate_price_eur
  pricing.resolve_eur_rate (only the fallback branch matters for logging)
  yml_generator._is_available_for_offer
  yml_generator._compute_price_eur
  yml_generator._build_offer_xml field selection (price/oldprice/currencyId/available)
"""
import math
import sqlite3

DB = r"C:/Projects/labresta-sync/instance/labresta.db"
EXTERNAL_ID = "1546341257"          # pp.external_id == sp article for HKN-PICO12M
_EUR_RATE_FALLBACK = 51.15


# ---- pricing.py logic (copied verbatim) ------------------------------------
def calculate_price_eur(retail_price_cents, discount_percent):
    discounted_cents = retail_price_cents * (100 - discount_percent) / 100
    tenths = math.floor(discounted_cents / 10 + 0.5)
    return tenths / 10.0


def resolve_discount_percent(match_discount, supplier, brand, brand_rows):
    if match_discount is not None:
        return match_discount
    mode = (supplier["pricing_mode"] or "flat")
    default = float(supplier["discount_percent"] or 0.0)
    if mode == "per_brand" and brand:
        key = brand.strip().lower()
        if key:
            for row in brand_rows:
                row_brand = ((row["brand"] or "").strip().lower())
                if row_brand == key:
                    return float(row["discount_percent"])
        return default
    return default


def clamp_discount_for_min_margin(base_discount, retail_price_cents,
                                  eur_rate_uah, min_margin_uah, cost_rate=0.75):
    if retail_price_cents <= 0 or eur_rate_uah <= 0 or min_margin_uah <= 0:
        return int(base_discount)
    base_d = float(base_discount)
    retail_eur = retail_price_cents / 100.0
    max_margin_frac = 1 - cost_rate
    if retail_eur * max_margin_frac * eur_rate_uah < min_margin_uah:
        return 0
    base_frac = max_margin_frac - base_d / 100.0
    if base_frac * retail_eur * eur_rate_uah >= min_margin_uah:
        return int(math.floor(base_d))
    d_max = 100.0 * (max_margin_frac - min_margin_uah / (retail_eur * eur_rate_uah))
    d = int(math.floor(d_max))
    if d < 0:
        return 0
    if d > int(math.floor(base_d)):
        return int(math.floor(base_d))
    return d


def is_valid_price(price_cents):
    return price_cents is not None and price_cents > 0


def resolve_eur_rate(supplier):
    raw = supplier["eur_rate_uah"]
    rate = float(raw or 0)
    if rate > 0:
        return rate
    print(f"  [WARN] supplier has no eur_rate_uah (got {raw!r}) -> fallback {_EUR_RATE_FALLBACK}")
    return _EUR_RATE_FALLBACK


# ---- main ------------------------------------------------------------------
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row

pp = con.execute(
    "SELECT id, external_id, name, name_ru, brand, page_url, description_ua, "
    "description_ru FROM prom_products WHERE external_id=?", (EXTERNAL_ID,)
).fetchone()
print("PP:", dict(pp) if pp else None)

m = con.execute(
    "SELECT * FROM product_matches WHERE prom_product_id=? "
    "AND status IN ('confirmed','manual') AND published=1", (pp["id"],)
).fetchone()
print("MATCH:", dict(m) if m else None)
if m is None:
    print("!! No published confirmed/manual match -> offer would NOT be emitted by the feed.")
    raise SystemExit(1)

sp = con.execute("SELECT * FROM supplier_products WHERE id=?",
                  (m["supplier_product_id"],)).fetchone()
print("SP:", {k: sp[k] for k in ("id", "supplier_id", "external_id", "name",
      "brand", "price_cents", "currency", "available", "needs_review",
      "is_deleted", "ignored")})

sup = con.execute("SELECT * FROM suppliers WHERE id=?",
                   (sp["supplier_id"],)).fetchone()
print("SUPPLIER:", {k: sup[k] for k in ("id", "name", "slug", "pricing_mode",
      "discount_percent", "eur_rate_uah", "min_margin_uah", "cost_rate")})

brand_rows = con.execute(
    "SELECT brand, discount_percent FROM supplier_brand_discounts "
    "WHERE supplier_id=?", (sup["id"],)).fetchall()
print("BRAND_DISCOUNTS:", [dict(r) for r in brand_rows])

# ---- _is_available_for_offer ----
is_available = (is_valid_price(sp["price_cents"])
                and bool(sp["available"])
                and not bool(sp["needs_review"]))

# ---- _compute_price_eur ----
eff = resolve_discount_percent(m["discount_percent"], sup, sp["brand"], brand_rows)
clamp_note = "no clamp (override set)" if m["discount_percent"] is not None else "no clamp"
if m["discount_percent"] is None and sup is not None:
    min_margin = float(sup["min_margin_uah"] or 0.0)
    if min_margin > 0:
        rate = resolve_eur_rate(sup)
        if (sp["currency"] or "EUR") == "UAH":
            rate = 1.0
        before = eff
        eff = clamp_discount_for_min_margin(
            eff, sp["price_cents"], rate, min_margin,
            float(sup["cost_rate"] or 0.75))
        clamp_note = f"clamp {before}% -> {eff}% (rate={rate}, min_margin={min_margin})"

price_eur = calculate_price_eur(sp["price_cents"], eff) if is_valid_price(sp["price_cents"]) else 0.0
retail_eur = (sp["price_cents"] or 0) / 100.0
currency_id = (sp["currency"] or "EUR") if sp["currency"] in ("EUR", "UAH") else "EUR"
emit_oldprice = retail_eur > price_eur + 0.05

print("\n=== OFFER VALUES the live feed would emit ===")
print(f"  available  = {'true' if is_available else 'false'}")
print(f"  base/eff discount = {eff}%  ({clamp_note})")
print(f"  retail_eur = {retail_eur:.2f}  (sp.price_cents={sp['price_cents']})")
print(f"  <price>    = {price_eur:.1f}")
print(f"  <oldprice> = {retail_eur:.1f}" if emit_oldprice else "  <oldprice> = (omitted: retail <= price+0.05)")
print(f"  <currencyId> = {currency_id}")
print(f"  pp.name      = {pp['name']!r}")
print(f"  pp.name_ru   = {pp['name_ru']!r}")
print(f"  pp.page_url  = {pp['page_url']!r}")
print(f"  pp.brand     = {pp['brand']!r}")
print(f"  feed_name    = {m['feed_name']!r}  (name = feed_name or pp.name)")
con.close()
