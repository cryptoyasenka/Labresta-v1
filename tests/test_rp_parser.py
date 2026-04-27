"""Tests for rp_parser — РП Україна section-grouped xlsx feed."""

import tempfile
from datetime import datetime
from pathlib import Path

import openpyxl
import pytest

from app.services.rp_parser import (
    _canonical_url,
    _is_brand_header,
    _parse_price_cents,
    _parse_stock_available,
    _strip_country_suffix,
    parse_rp_sheet,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_rp_xlsx(path: str, rows: list) -> None:
    """Write a raw list-of-lists into column A-D of sheet 1."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "ЗАЛИШКИ"
    for row in rows:
        padded = list(row) + [None] * (4 - len(row))
        ws.append(padded[:4])
    wb.save(path)
    wb.close()


SUPPLIER_ID = 42


# ===========================================================================
# Unit: helper functions
# ===========================================================================


class TestStripCountrySuffix:
    def test_strips_country(self):
        assert _strip_country_suffix("SIRMAN (Італія)") == "SIRMAN"

    def test_strips_with_spaces(self):
        assert _strip_country_suffix("HELIA SMOKER  (Німеччина) ") == "HELIA SMOKER"

    def test_no_suffix_unchanged(self):
        assert _strip_country_suffix("HURAKAN") == "HURAKAN"

    def test_empty_string(self):
        assert _strip_country_suffix("") == ""


class TestCanonicalUrl:
    def test_normalises_scheme(self):
        assert _canonical_url("http://rp.ua/product/123").startswith("https://")

    def test_strips_query_and_fragment(self):
        url = _canonical_url("https://rp.ua/product/123?ref=deal#top")
        assert "?" not in url
        assert "#" not in url

    def test_strips_whitespace(self):
        result = _canonical_url("  https://rp.ua/product/abc  ")
        assert result == "https://rp.ua/product/abc"

    def test_path_preserved(self):
        result = _canonical_url("https://rp.ua/catalog/knives/chef")
        assert result.endswith("/catalog/knives/chef")


class TestParsePriceCents:
    def test_float_value(self):
        assert _parse_price_cents(12.5) == 1250

    def test_int_value(self):
        assert _parse_price_cents(100) == 10000

    def test_string_with_euro(self):
        assert _parse_price_cents("25.00 €") == 2500

    def test_string_comma_decimal(self):
        assert _parse_price_cents("99,90") == 9990

    def test_zero_returns_none(self):
        assert _parse_price_cents(0) is None

    def test_negative_returns_none(self):
        assert _parse_price_cents(-5.0) is None

    def test_none_input(self):
        assert _parse_price_cents(None) is None

    def test_empty_string(self):
        assert _parse_price_cents("") is None

    def test_non_numeric_string(self):
        assert _parse_price_cents("н/а") is None


class TestParseStockAvailable:
    def test_bagato_available(self):
        assert _parse_stock_available("БАГАТО") is True

    def test_bagato_lowercase(self):
        assert _parse_stock_available("багато") is True

    def test_positive_int(self):
        assert _parse_stock_available(5) is True

    def test_positive_float(self):
        assert _parse_stock_available(1.0) is True

    def test_zero_int(self):
        assert _parse_stock_available(0) is False

    def test_zero_float(self):
        assert _parse_stock_available(0.0) is False

    def test_empty_string(self):
        assert _parse_stock_available("") is False

    def test_none(self):
        assert _parse_stock_available(None) is False

    def test_string_zero(self):
        assert _parse_stock_available("0") is False

    def test_numeric_string_positive(self):
        assert _parse_stock_available("3") is True

    def test_freeform_text(self):
        assert _parse_stock_available("є") is True


class TestIsBrandHeader:
    def test_valid_header(self):
        assert _is_brand_header(None, "SIRMAN (Італія)", None, None) is True

    def test_has_url_in_a(self):
        assert _is_brand_header("https://rp.ua/x", "SIRMAN", None, None) is False

    def test_has_price_in_c(self):
        assert _is_brand_header(None, "SIRMAN", 99.0, None) is False

    def test_datetime_in_d_not_header(self):
        assert _is_brand_header(None, "something", None, datetime(2025, 1, 1)) is False

    def test_too_long_label(self):
        assert _is_brand_header(None, "X" * 100, None, None) is False

    def test_multiline_not_header(self):
        assert _is_brand_header(None, "line1\nline2", None, None) is False

    def test_none_b_not_header(self):
        assert _is_brand_header(None, None, None, None) is False


# ===========================================================================
# Integration: parse_rp_sheet
# ===========================================================================


class TestParseRpSheet:
    def test_basic_two_brands(self, tmp_path):
        xlsx = str(tmp_path / "feed.xlsx")
        _make_rp_xlsx(xlsx, [
            [None, "SIRMAN (Італія)", None, None],
            ["https://rp.ua/a", "Слайсер SIRMAN S300", 150.0, 5],
            [None, None, None, None],
            [None, "HURAKAN (Китай)", None, None],
            ["https://rp.ua/b", "Блендер HURAKAN B500", 80.0, "БАГАТО"],
        ])
        products, errors = parse_rp_sheet(xlsx, SUPPLIER_ID)
        assert len(errors) == 0
        assert len(products) == 2
        names = [p["name"] for p in products]
        assert "Слайсер SIRMAN S300" in names
        assert "Блендер HURAKAN B500" in names

    def test_brand_inherited_across_rows(self, tmp_path):
        xlsx = str(tmp_path / "feed.xlsx")
        _make_rp_xlsx(xlsx, [
            [None, "ROBOT COUPE", None, None],
            ["https://rp.ua/r1", "R301 Ultra", 200.0, 2],
            ["https://rp.ua/r2", "Cutter CL50", 350.0, 1],
        ])
        products, errors = parse_rp_sheet(xlsx, SUPPLIER_ID)
        assert all(p["brand"] == "ROBOT COUPE" for p in products)

    def test_country_suffix_stripped_from_brand(self, tmp_path):
        xlsx = str(tmp_path / "feed.xlsx")
        _make_rp_xlsx(xlsx, [
            [None, "CEADO (Италія)", None, None],
            ["https://rp.ua/c1", "Espresso Machine", 500.0, 1],
        ])
        products, _ = parse_rp_sheet(xlsx, SUPPLIER_ID)
        assert products[0]["brand"] == "CEADO"

    def test_url_canonicalised(self, tmp_path):
        xlsx = str(tmp_path / "feed.xlsx")
        _make_rp_xlsx(xlsx, [
            [None, "BRAND", None, None],
            ["http://rp.ua/product/x?ref=1#anchor  ", "Товар", 10.0, 1],
        ])
        products, _ = parse_rp_sheet(xlsx, SUPPLIER_ID)
        assert products[0]["external_id"] == "https://rp.ua/product/x"

    def test_price_converted_to_cents(self, tmp_path):
        xlsx = str(tmp_path / "feed.xlsx")
        _make_rp_xlsx(xlsx, [
            [None, "BRAND", None, None],
            ["https://rp.ua/p", "Прилад", 99.5, 3],
        ])
        products, _ = parse_rp_sheet(xlsx, SUPPLIER_ID)
        assert products[0]["price_cents"] == 9950

    def test_currency_is_eur(self, tmp_path):
        xlsx = str(tmp_path / "feed.xlsx")
        _make_rp_xlsx(xlsx, [
            [None, "BRAND", None, None],
            ["https://rp.ua/p", "Item", 50.0, 1],
        ])
        products, _ = parse_rp_sheet(xlsx, SUPPLIER_ID)
        assert products[0]["currency"] == "EUR"

    def test_zero_stock_unavailable(self, tmp_path):
        xlsx = str(tmp_path / "feed.xlsx")
        _make_rp_xlsx(xlsx, [
            [None, "BRAND", None, None],
            ["https://rp.ua/p", "Item", 50.0, 0],
        ])
        products, _ = parse_rp_sheet(xlsx, SUPPLIER_ID)
        assert products[0]["available"] is False

    def test_bagato_available(self, tmp_path):
        xlsx = str(tmp_path / "feed.xlsx")
        _make_rp_xlsx(xlsx, [
            [None, "BRAND", None, None],
            ["https://rp.ua/p", "Item", 50.0, "БАГАТО"],
        ])
        products, _ = parse_rp_sheet(xlsx, SUPPLIER_ID)
        assert products[0]["available"] is True

    def test_zero_price_unavailable(self, tmp_path):
        xlsx = str(tmp_path / "feed.xlsx")
        _make_rp_xlsx(xlsx, [
            [None, "BRAND", None, None],
            ["https://rp.ua/p", "Item", 0, "БАГАТО"],
        ])
        products, errors = parse_rp_sheet(xlsx, SUPPLIER_ID)
        # Product is still emitted but marked unavailable; price warning issued.
        assert products[0]["available"] is False
        assert any("price" in e.lower() or "0" in e for e in errors)

    def test_product_before_brand_skipped(self, tmp_path):
        xlsx = str(tmp_path / "feed.xlsx")
        _make_rp_xlsx(xlsx, [
            ["https://rp.ua/orphan", "Orphan product", 10.0, 1],
            [None, "BRAND", None, None],
            ["https://rp.ua/ok", "Normal product", 20.0, 1],
        ])
        products, errors = parse_rp_sheet(xlsx, SUPPLIER_ID)
        assert len(products) == 1
        assert products[0]["name"] == "Normal product"
        assert any("brand" in e.lower() for e in errors)

    def test_duplicate_url_warns(self, tmp_path):
        xlsx = str(tmp_path / "feed.xlsx")
        _make_rp_xlsx(xlsx, [
            [None, "BRAND", None, None],
            ["https://rp.ua/dup", "Item A", 10.0, 1],
            ["https://rp.ua/dup", "Item B", 20.0, 1],
        ])
        products, errors = parse_rp_sheet(xlsx, SUPPLIER_ID)
        assert len(products) == 1
        assert any("duplicate" in e.lower() for e in errors)

    def test_blank_rows_skipped(self, tmp_path):
        xlsx = str(tmp_path / "feed.xlsx")
        _make_rp_xlsx(xlsx, [
            [None, None, None, None],
            [None, "BRAND", None, None],
            [None, None, None, None],
            ["https://rp.ua/p", "Item", 10.0, 1],
            [None, None, None, None],
        ])
        products, errors = parse_rp_sheet(xlsx, SUPPLIER_ID)
        assert len(products) == 1
        assert len(errors) == 0

    def test_supplier_id_attached(self, tmp_path):
        xlsx = str(tmp_path / "feed.xlsx")
        _make_rp_xlsx(xlsx, [
            [None, "BRAND", None, None],
            ["https://rp.ua/p", "Item", 10.0, 1],
        ])
        products, _ = parse_rp_sheet(xlsx, SUPPLIER_ID)
        assert products[0]["supplier_id"] == SUPPLIER_ID

    def test_empty_sheet_returns_no_products(self, tmp_path):
        xlsx = str(tmp_path / "feed.xlsx")
        _make_rp_xlsx(xlsx, [])
        products, errors = parse_rp_sheet(xlsx, SUPPLIER_ID)
        assert products == []
        assert errors == []
