"""Канарейка v4 — ФИНАЛЬНАЯ УЗКАЯ НП-СХЕМА (БЕЗ name/name_ru/url/vendor),
цена/наличие ИЗ МАТЧЕРА.

v2 выкинула цену (промах) → v3 вернул цену из матчера → v4 убрал
name/name_ru/url/vendor: на превью Horoshop профиль крест-маппит
<name>(укр) → русское «Название модификации(RU)» (доказано 2026-05-19);
колонку на стороне Horoshop отключить нельзя — только через содержимое
фида. Это и есть зафиксированный финальный состав узкого НП-фида.

Скрипт ЧИТАЕТ репо-БД mode=ro (без записи/Flask/касания репо) и считает
price/oldprice/currencyId/available ТОЧНО как live-фид после матча —
копия pricing.py + _build_offer_xml/_compute_price_eur/
_is_available_for_offer (verbatim).

Состав offer: id+available+price+oldprice?+currencyId+vendorCode+
description(UA НП)+description_ru(НП)+picture×N. Связка с карточкой —
по id/<vendorCode>=external_id (имя не нужно). Цена/наличие идемпотентны
(= то, что осн. фид уже отдаёт). Тело+фото = единств. предмет теста.

Пишет ТОЛЬКО в план-каталог (репо read-only, W1 на main не задет)."""
import math
import sqlite3
import openpyxl
from lxml import etree

DB = r"C:/Projects/labresta-sync/instance/labresta.db"  # читаем mode=ro, без записи
NP_FEED = r"C:/Users/Yana/labresta-np-feed-plan/np-feed.xlsx"  # фид поставщика НП (read-only)
EXTERNAL_ID = "1546341257"          # pp.external_id (= vendorCode на живой карточке)
_EUR_RATE_FALLBACK = 51.15

# --- ТЕЛО ПОСТАВЩИКА НП (предмет канарейки — НЕ из матчера, из фида НП) ---
DESC_UA = ("Тип: настільна хліборізка.<br>Продуктивність: до 240 батонів/год.<br>"
           "Кількість ножів: 32 шт.<br>Товщина нарізання: 12 мм.<br>"
           "Максимальний розмір хлібини: 165х375 мм.<br>"
           "Матеріал робочої частини та ножів: нержавіюча сталь.<br>"
           "Габарити (ШхГхВ): 745х510х710 мм.<br>Потужність: 0,37 кВт.<br>"
           "Напруга: 220 В.<br>Вага: 62 кг.")
DESC_RU = ("Тип: настольная хлеборезка.<br>Производительность: до 240 батонов/ч.<br>"
           "Количество ножей: 32 шт.<br>Толщина нарезки: 12 мм.<br>"
           "Максимальный размер буханки: 165х375 мм.<br>"
           "Материал рабочей части и ножей: нержавеющая сталь.<br>"
           "Габариты (ШхГхВ): 745х510х710 мм.<br>Мощность: 0,37 кВт.<br>"
           "Напряжение: 220 В.<br>Вес: 62 кг.")
PICS = ["https://np.com.ua/wp-content/uploads/2023/02/2-15-1.jpg",
        "https://np.com.ua/wp-content/uploads/2023/02/3-13-1.jpg"]


# ---- pricing.py (copied verbatim, read-only mirror) ----
def calculate_price_eur(retail_price_cents, discount_percent):
    discounted_cents = retail_price_cents * (100 - discount_percent) / 100
    tenths = math.floor(discounted_cents / 10 + 0.5)
    return tenths / 10.0


def resolve_discount_percent(match_discount, sup, brand, brand_rows):
    if match_discount is not None:
        return match_discount
    mode = (sup["pricing_mode"] or "flat")
    default = float(sup["discount_percent"] or 0.0)
    if mode == "per_brand" and brand:
        key = brand.strip().lower()
        if key:
            for row in brand_rows:
                if ((row["brand"] or "").strip().lower()) == key:
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


def resolve_eur_rate(sup):
    raw = sup["eur_rate_uah"]
    rate = float(raw or 0)
    if rate > 0:
        return rate
    print(f"  [WARN] supplier no eur_rate_uah ({raw!r}) -> fallback {_EUR_RATE_FALLBACK}")
    return _EUR_RATE_FALLBACK


# ---- pull matcher row (READ-ONLY) ----
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row
pp = con.execute(
    "SELECT id, external_id, name, name_ru, brand, page_url "
    "FROM prom_products WHERE external_id=?", (EXTERNAL_ID,)).fetchone()
m = con.execute(
    "SELECT * FROM product_matches WHERE prom_product_id=? "
    "AND status IN ('confirmed','manual') AND published=1", (pp["id"],)).fetchone()
if m is None:
    raise SystemExit("No published confirmed/manual match — feed would not emit this offer")
sp = con.execute("SELECT * FROM supplier_products WHERE id=?",
                  (m["supplier_product_id"],)).fetchone()
sup = con.execute("SELECT * FROM suppliers WHERE id=?",
                   (sp["supplier_id"],)).fetchone()
brand_rows = con.execute(
    "SELECT brand, discount_percent FROM supplier_brand_discounts "
    "WHERE supplier_id=?", (sup["id"],)).fetchall()
con.close()

# ---- _is_available_for_offer ----
is_available = (is_valid_price(sp["price_cents"]) and bool(sp["available"])
                and not bool(sp["needs_review"]))

# ---- _compute_price_eur ----
eff = resolve_discount_percent(m["discount_percent"], sup, sp["brand"], brand_rows)
if m["discount_percent"] is None and sup is not None:
    min_margin = float(sup["min_margin_uah"] or 0.0)
    if min_margin > 0:
        rate = resolve_eur_rate(sup)
        if (sp["currency"] or "EUR") == "UAH":
            rate = 1.0
        eff = clamp_discount_for_min_margin(
            eff, sp["price_cents"], rate, min_margin,
            float(sup["cost_rate"] or 0.75))
price_eur = calculate_price_eur(sp["price_cents"], eff) if is_valid_price(sp["price_cents"]) else 0.0
retail_eur = (sp["price_cents"] or 0) / 100.0
currency_id = (sp["currency"] or "EUR") if sp["currency"] in ("EUR", "UAH") else "EUR"

# ---- ИМЯ UA/RU ИЗ ФИДА ПОСТАВЩИКА НП (title_uk=G, title_ru=P) ----
# Решение Yana 2026-05-19: имя тянем из фида поставщика (поставщик уже
# перевёл UA+RU) — источник правды, как и описание. Связка строки фида с
# товаром — по Артикул(B) == sp.external_id (тот же ключ, что у матчера).
_art = (sp["external_id"] or "").strip().lower()
_wb = openpyxl.load_workbook(NP_FEED, read_only=True, data_only=True)
_ws = _wb["Worksheet"]
_rows = _ws.iter_rows(values_only=True)
next(_rows)  # header
NAME_UA = NAME_RU = None
for _r in _rows:
    if (str(_r[1]) if _r[1] is not None else "").strip().lower() == _art:
        NAME_UA = (_r[6] or "").strip()    # G title_uk
        NAME_RU = (_r[15] or "").strip()   # P title_ru
        break
_wb.close()
if not NAME_UA:
    raise SystemExit(f"НП-фид: нет строки Артикул={_art!r} или пустой title_uk")

# ---- skeleton (1:1 _shop_skeleton) ----
from datetime import datetime, timezone
now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
root = etree.Element("yml_catalog", date=now)
shop = etree.SubElement(root, "shop")
etree.SubElement(shop, "name").text = "LabResta"
etree.SubElement(shop, "company").text = "LabResta"
etree.SubElement(shop, "url").text = "https://labresta.com"
cur = etree.SubElement(shop, "currencies")
etree.SubElement(cur, "currency", id="EUR", rate="1")
etree.SubElement(cur, "currency", id="UAH", rate="1")
offers = etree.SubElement(shop, "offers")

# ---- offer: ФИНАЛЬНАЯ УЗКАЯ НП-СХЕМА (БЕЗ name/name_ru/url/vendor) ----
# v4: Horoshop-профиль крест-маппит <name>(укр) → русское «Название
# модификации(RU)» (доказано на превью 2026-05-19); колонку на стороне
# Horoshop отключить нельзя — регулируется только содержимым фида. Поэтому
# имя/имя_ru/vendor/url ИСКЛЮЧЕНЫ из файла = ровно зафиксированный финальный
# состав узкого НП-фида. Связка с карточкой — по offer id / <vendorCode>
# = external_id (1546341257), имя не нужно. price/oldprice/currencyId/
# available — из матчера (идемпотентно). Тело+фото = предмет теста.
offer = etree.SubElement(offers, "offer", id=str(pp["external_id"]),
                         available=("true" if is_available else "false"))
etree.SubElement(offer, "name").text = NAME_UA          # = title_uk из фида НП
if NAME_RU:
    etree.SubElement(offer, "name_ru").text = NAME_RU    # = title_ru из фида НП
etree.SubElement(offer, "price").text = f"{price_eur:.1f}"
if retail_eur > price_eur + 0.05:
    etree.SubElement(offer, "oldprice").text = f"{retail_eur:.1f}"
etree.SubElement(offer, "currencyId").text = currency_id
etree.SubElement(offer, "vendorCode").text = str(pp["external_id"])
# --- предмет канарейки: тело НП + фото (заменяет pp.description) ---
d = etree.SubElement(offer, "description"); d.text = etree.CDATA(DESC_UA)
dr = etree.SubElement(offer, "description_ru"); dr.text = etree.CDATA(DESC_RU)
for p in PICS:
    etree.SubElement(offer, "picture").text = p

tree = etree.ElementTree(root)
for path in (r"C:/Users/Yana/labresta-np-feed-plan/canary-HKN-PICO12M.yml",
             r"C:/Users/Yana/labresta-np-feed-plan/_serve/canary-HKN-PICO12M.yml"):
    with open(path, "wb") as f:
        tree.write(f, xml_declaration=True, encoding="UTF-8",
                   pretty_print=True,
                   doctype='<!DOCTYPE yml_catalog SYSTEM "shops.dtd">')

_old = f"{retail_eur:.1f}" if retail_eur > price_eur + 0.05 else "(omitted)"
print(f"OK date={now}")
print(f"  match_id={m['id']} sp_id={sp['id']} pp_id={pp['id']} "
      f"status={m['status']} available={'true' if is_available else 'false'}")
print(f"  discount eff={eff}%  retail={retail_eur:.2f}  "
      f"<price>={price_eur:.1f}  <oldprice>={_old}  <currencyId>={currency_id}")
print(f"  NO name/name_ru/url/vendor (узкая НП-схема); link by id/vendorCode={pp['external_id']}")
