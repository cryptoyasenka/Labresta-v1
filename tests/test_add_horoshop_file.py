"""Tests for app.services.add_horoshop_file pure builders.

Mirrors tests/test_np_horoshop_file.py: pure-dict tests, no DB or Flask
fixtures. `_shape_rows` takes a list of already-priced/resolved row inputs
(plain dicts) so the shape/manifest logic and the native-schema output are
verified without the DB. `price_unmatched` is tested against a duck-typed
supplier (pricing.py accepts a duck-typed supplier by design). The DB shell
build_add_file()/_query_unmatched() is covered by the endpoint test.

The create-file = the NP builder PLUS the columns the update-files omit
(Название UA/RU, Бренд, Раздел, Отображать) so a "New products: Import" run
CREATES cards instead of only updating existing ones.
"""

import io

import openpyxl

from app.services.add_horoshop_file import (
    HEADERS,
    H_ARTICLE, H_NAME_UA, H_NAME_RU, H_BRAND, H_CATEGORY,
    H_PRICE, H_OLDPRICE, H_CURRENCY, H_AVAIL, H_VISIBLE,
    H_GALLERY, H_DESC_UA, H_DESC_RU,
    _shape_rows, _workbook_bytes, price_unmatched,
)


# --------------------------------------------------------------------------- #
# Row-input fixtures for _shape_rows (already priced + category resolved).
# --------------------------------------------------------------------------- #
def _ri(article="ART-1", name="НП товар", name_ru=None, brand="HURAKAN",
        category="Холодильне обладнання", price_eur=100.0, retail_eur=120.0,
        currency="EUR", available=True, photos=None,
        description="<p>ua</p>", description_ru="<p>ru</p>"):
    return {
        "article": article,
        "name": name,
        "name_ru": name_ru,
        "brand": brand,
        "category": category,
        "price_eur": price_eur,
        "retail_eur": retail_eur,
        "currency": currency,
        "available": available,
        "photos": ["https://x/1.jpg"] if photos is None else photos,
        "description": description,
        "description_ru": description_ru,
    }


# --------------------------------------------------------------------------- #
# Duck-typed supplier / SP for price_unmatched (pricing.py accepts duck types).
# --------------------------------------------------------------------------- #
class _BrandDiscount:
    def __init__(self, brand, discount_percent):
        self.brand = brand
        self.discount_percent = discount_percent


class _Supplier:
    def __init__(self, pricing_mode="flat", discount_percent=0.0,
                 min_margin_uah=0.0, cost_rate=0.75, eur_rate_uah=51.15,
                 brand_discounts=None):
        self.pricing_mode = pricing_mode
        self.discount_percent = discount_percent
        self.min_margin_uah = min_margin_uah
        self.cost_rate = cost_rate
        self.eur_rate_uah = eur_rate_uah
        self.brand_discounts = brand_discounts or []


class _SP:
    def __init__(self, supplier, price_cents=84500, currency="EUR",
                 brand="HURAKAN"):
        self.supplier = supplier
        self.price_cents = price_cents
        self.currency = currency
        self.brand = brand


# =========================================================================== #
# HEADERS / shape tests
# =========================================================================== #
def test_headers_include_create_columns():
    assert H_ARTICLE == "Артикул"  # bare top-level key, no prefix
    # Create-only columns the update-files (np/maresto) deliberately omit:
    assert H_NAME_UA == "[КАТАЛОГ] Название (UA)"
    assert H_BRAND == "[КАТАЛОГ] Бренд"
    assert H_CATEGORY == "[КАТАЛОГ] Раздел"
    assert H_VISIBLE == "[КАТАЛОГ] Отображать"
    # The 6 NP content columns must also be present.
    for h in (H_PRICE, H_OLDPRICE, H_CURRENCY, H_AVAIL, H_GALLERY,
              H_DESC_UA, H_DESC_RU):
        assert h in HEADERS
    for h in (H_ARTICLE, H_NAME_UA, H_NAME_RU, H_BRAND, H_CATEGORY, H_VISIBLE):
        assert h in HEADERS
    # Article first (the create key).
    assert HEADERS[0] == H_ARTICLE


def test_category_header_is_razdel_not_categories_uk():
    # RESEARCH Q1: a "categories_uk" column auto-maps to "do not import".
    assert H_CATEGORY == "[КАТАЛОГ] Раздел"
    joined = " ".join(HEADERS)
    assert "categories_uk" not in joined


def test_visibility_value_is_1():
    # RESEARCH Q2: an empty «Отображать» hides the card.
    rows, _ = _shape_rows([_ri(article="A"), _ri(article="B")], [])
    assert rows  # sanity
    for r in rows:
        assert r[H_VISIBLE] == "1"


def test_row_key_is_supplier_article():
    rows, _ = _shape_rows([_ri(article="SUP-ART")], [])
    assert len(rows) == 1
    # The row key is the supplier article — there is no PromProduct external_id.
    assert rows[0][H_ARTICLE] == "SUP-ART"


def test_skip_empty_article():
    rows, manifest = _shape_rows(
        [_ri(article=""), _ri(article="  "), _ri(article="OK")], []
    )
    assert [r[H_ARTICLE] for r in rows] == ["OK"]
    assert manifest["skipped_no_artikul"] == 2


def test_category_always_present():
    rows, _ = _shape_rows([_ri(article="A", category="Печі/Конвекційні")], [])
    assert rows[0][H_CATEGORY] == "Печі/Конвекційні"


def test_row_without_category_is_skipped():
    # Horoshop errors on a row with no Раздел; the fallback resolver guarantees
    # a non-empty category in normal flow, so this skip is 0 then.
    rows, manifest = _shape_rows(
        [_ri(article="A", category=""), _ri(article="B", category=None),
         _ri(article="C", category="ok")], []
    )
    assert [r[H_ARTICLE] for r in rows] == ["C"]
    assert manifest["skipped_no_category"] == 2


def test_availability_strings():
    rows, _ = _shape_rows(
        [_ri(article="A", available=True), _ri(article="B", available=False)], []
    )
    by = {r[H_ARTICLE]: r for r in rows}
    assert by["A"][H_AVAIL] == "В наличии"
    assert by["B"][H_AVAIL] == "Нет в наличии"


def test_oldprice_only_when_discounted():
    rows, _ = _shape_rows([
        _ri(article="A", price_eur=100.0, retail_eur=120.0),  # discount → oldprice
        _ri(article="B", price_eur=100.0, retail_eur=100.0),  # no discount → empty
    ], [])
    by = {r[H_ARTICLE]: r for r in rows}
    assert by["A"][H_OLDPRICE] == "120.0"
    assert by["B"][H_OLDPRICE] == ""


def test_name_ru_blank_when_absent():
    rows, _ = _shape_rows([_ri(article="A", name_ru=None)], [])
    assert rows[0][H_NAME_RU] == ""
    assert rows[0][H_NAME_UA] == "НП товар"


def test_gallery_join():
    rows, _ = _shape_rows([_ri(article="A", photos=["u1", "u2"])], [])
    assert rows[0][H_GALLERY] == "u1;u2"


def test_brand_filter_case_insensitive():
    rows, manifest = _shape_rows([
        _ri(article="A", brand="HURAKAN"),
        _ri(article="B", brand="APACH"),
    ], ["hurakan"])
    assert [r[H_ARTICLE] for r in rows] == ["A"]
    assert manifest["per_brand"] == {"HURAKAN": 1}


def test_empty_selection_includes_all_brands():
    rows, _ = _shape_rows([
        _ri(article="A", brand="HURAKAN"),
        _ri(article="B", brand="APACH"),
    ], [])
    assert len(rows) == 2


def test_skipped_no_price():
    rows, manifest = _shape_rows([
        _ri(article="A", price_eur=None),
        _ri(article="B", price_eur=0.0),
    ], [])
    assert rows == []
    assert manifest["skipped_no_price"] == 2


def test_workbook_bytes_roundtrip():
    rows, _ = _shape_rows([
        _ri(article="777", name="Льодогенератор", name_ru=None,
            price_eur=50.0, retail_eur=60.0, photos=["u1", "u2"],
            category="Холодильне/Льодогенератори"),
    ], [])
    wb = openpyxl.load_workbook(
        io.BytesIO(_workbook_bytes(rows)), read_only=True, data_only=True
    )
    ws = wb["Worksheet"]
    all_rows = list(ws.iter_rows(values_only=True))
    wb.close()
    assert list(all_rows[0]) == HEADERS
    data_row = dict(zip(HEADERS, all_rows[1]))
    assert data_row[H_ARTICLE] == "777"
    assert data_row[H_NAME_UA] == "Льодогенератор"
    assert data_row[H_NAME_RU] == ""
    assert data_row[H_CATEGORY] == "Холодильне/Льодогенератори"
    assert data_row[H_VISIBLE] == "1"
    assert data_row[H_PRICE] == "50.0"
    assert data_row[H_OLDPRICE] == "60.0"
    assert data_row[H_GALLERY] == "u1;u2"


# =========================================================================== #
# price_unmatched tests — the pure pricing path (no DB, no ProductMatch).
# =========================================================================== #
def test_price_flat_supplier():
    sup = _Supplier(pricing_mode="flat", discount_percent=15.0, min_margin_uah=0.0)
    sp = _SP(sup, price_cents=84500, currency="EUR", brand="HURAKAN")
    sell, _ = price_unmatched(sp)
    assert sell == 718.3  # reproduces the canary: calculate_price_eur(84500, 15.0)


def test_oldprice_present_when_discount():
    sup = _Supplier(pricing_mode="flat", discount_percent=15.0, min_margin_uah=0.0)
    sp = _SP(sup, price_cents=84500, currency="EUR", brand="HURAKAN")
    _, oldprice = price_unmatched(sp)
    assert oldprice == "845.0"


def test_price_no_oldprice_when_zero_discount():
    sup = _Supplier(pricing_mode="flat", discount_percent=0.0, min_margin_uah=0.0)
    sp = _SP(sup, price_cents=84500, currency="EUR")
    sell, oldprice = price_unmatched(sp)
    assert sell == 845.0
    assert oldprice == ""


def test_price_none_when_no_price_cents():
    sup = _Supplier(discount_percent=15.0)
    sp = _SP(sup, price_cents=None)
    sell, oldprice = price_unmatched(sp)
    assert sell is None
    assert oldprice == ""


def test_price_per_brand_override():
    # per_brand mode + a brand_discount row for the SP's brand uses the brand %,
    # not the supplier default.
    sup = _Supplier(
        pricing_mode="per_brand", discount_percent=10.0, min_margin_uah=0.0,
        brand_discounts=[_BrandDiscount("HURAKAN", 20.0)],
    )
    sp = _SP(sup, price_cents=100000, currency="EUR", brand="HURAKAN")
    sell, _ = price_unmatched(sp)
    # 20% brand discount → 800.0 (not 900.0 from the 10% supplier default).
    assert sell == 800.0


def test_uah_rate_is_1():
    # For a UAH-priced supplier the EUR rate must be forced to 1.0 before the
    # min-margin clamp. With min_margin>0, using the real EUR rate vs rate=1
    # gives different clamps; assert the UAH path matches the rate=1 result.
    sup_uah = _Supplier(
        pricing_mode="flat", discount_percent=20.0,
        min_margin_uah=500.0, cost_rate=0.75, eur_rate_uah=51.15,
    )
    sp_uah = _SP(sup_uah, price_cents=400000, currency="UAH", brand="HURAKAN")
    sell_uah, _ = price_unmatched(sp_uah)
    # retail_uah = 4000; buy = 3000; at 20% sell = 3200, margin = 200 < 500 →
    # clamp reduces discount until margin >= 500 → sell = 3500 (margin exactly 500).
    assert sell_uah == 3500.0


def test_clamp_applies_when_min_margin_positive():
    # A cheap item + min_margin_uah=500 reduces the effective discount so the
    # sell price rises toward retail (vs the unclamped discount).
    sup = _Supplier(
        pricing_mode="flat", discount_percent=20.0,
        min_margin_uah=500.0, cost_rate=0.75, eur_rate_uah=51.15,
    )
    sp = _SP(sup, price_cents=8000, currency="EUR", brand="HURAKAN")  # 80 EUR
    sell, _ = price_unmatched(sp)
    # Unclamped 20% would be 64.0; margin = (64 - 60) * 51.15 = 204.6 < 500 →
    # clamp pushes discount to 0 (even 0% margin = 20*51.15 = 1023 >= 500... but
    # at 0% margin_eur=20 → 1023 >= 500, so d_max solves; assert sell rises above 64.
    assert sell > 64.0


def test_auto_margin_supplier_uses_auto_discount():
    # auto_margin suppliers (MARESTO class, CLAUDE.md #12): the discount comes
    # from calculate_auto_discount, not resolve_discount_percent (which returns
    # the supplier default for auto_margin by design — pricing.py:99).
    sup = _Supplier(
        pricing_mode="auto_margin", discount_percent=0.0,
        min_margin_uah=500.0, cost_rate=0.75, eur_rate_uah=51.15,
    )
    # retail 200 EUR ≥ 162.9 → auto discount 19% → sell 162.0.
    sp = _SP(sup, price_cents=20000, currency="EUR", brand="HURAKAN")
    sell, _ = price_unmatched(sp)
    assert sell == 162.0
