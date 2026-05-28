"""Tests for app.services.np_horoshop_file pure builders (_shape_rows /
_workbook_bytes). No DB or network: _shape_rows takes plain dicts, so the
join/filter/manifest logic and the exact native-schema output are verified
without Flask fixtures. The DB shell build_np_file() is covered by the
endpoint/integration test added with the UI step.
"""

import io

import openpyxl

from app.services.np_horoshop_file import (
    HEADERS,
    H_ARTICLE, H_PRICE, H_OLDPRICE, H_CURRENCY,
    H_AVAIL, H_GALLERY, H_DESC_UA, H_DESC_RU,
    _shape_rows, _workbook_bytes,
)


def _c(brand="HURAKAN", desc="<p>ua</p>", desc_ru="<p>ru</p>", photos=None):
    return {
        "brand": brand,
        "description": desc,
        "description_ru": desc_ru,
        "photos": ["https://x/1.jpg"] if photos is None else photos,
    }


def _p(article, external_id, price_eur=100.0, retail_eur=120.0,
       available=True, currency="EUR"):
    return {
        "article": article, "external_id": external_id,
        "price_eur": price_eur, "retail_eur": retail_eur,
        "available": available, "currency": currency,
    }


def test_headers_exact_and_exclude_name_brand_visibility():
    assert HEADERS == [
        H_ARTICLE, H_PRICE, H_OLDPRICE, H_CURRENCY,
        H_AVAIL, H_GALLERY, H_DESC_UA, H_DESC_RU,
    ]
    assert H_ARTICLE == "Артикул"  # bare top-level key, no prefix
    joined = " ".join(HEADERS)
    assert "Бренд" not in joined
    assert "Название модификации" not in joined
    assert "Отображать" not in joined


def test_row_uses_external_id_as_key_not_supplier_article():
    content = {"SUP-ART": _c()}
    rows, manifest = _shape_rows(content, [_p("SUP-ART", "999111")], ["HURAKAN"])
    assert len(rows) == 1
    assert rows[0][H_ARTICLE] == "999111"          # pp.external_id, not "SUP-ART"
    assert rows[0][H_DESC_UA] == "<p>ua</p>"
    assert rows[0][H_DESC_RU] == "<p>ru</p>"
    assert rows[0][H_GALLERY] == "https://x/1.jpg"
    assert manifest["total"] == 1


def test_oldprice_only_when_discounted():
    content = {"A": _c(), "B": _c()}
    priced = [
        _p("A", "1", price_eur=100.0, retail_eur=120.0),  # discount → oldprice
        _p("B", "2", price_eur=100.0, retail_eur=100.0),  # no discount → empty
    ]
    rows, _ = _shape_rows(content, priced, [])
    by = {r[H_ARTICLE]: r for r in rows}
    assert by["1"][H_OLDPRICE] == "120.0"
    assert by["2"][H_OLDPRICE] == ""


def test_price_and_oldprice_one_decimal():
    content = {"A": _c()}
    rows, _ = _shape_rows(content, [_p("A", "1", price_eur=718.3, retail_eur=845.0)], [])
    assert rows[0][H_PRICE] == "718.3"
    assert rows[0][H_OLDPRICE] == "845.0"


def test_availability_strings():
    content = {"A": _c(), "B": _c()}
    rows, _ = _shape_rows(
        content, [_p("A", "1", available=True), _p("B", "2", available=False)], []
    )
    by = {r[H_ARTICLE]: r for r in rows}
    assert by["1"][H_AVAIL] == "В наличии"
    assert by["2"][H_AVAIL] == "Нет в наличии"


def test_gallery_join_and_no_photo_counts():
    content = {"A": _c(photos=["u1", "u2"]), "B": _c(photos=[])}
    rows, manifest = _shape_rows(content, [_p("A", "1"), _p("B", "2")], [])
    by = {r[H_ARTICLE]: r for r in rows}
    assert by["1"][H_GALLERY] == "u1;u2"
    assert by["2"][H_GALLERY] == ""
    assert manifest["with_photo"] == 1
    assert manifest["no_photo"] == 1


def test_brand_filter_case_insensitive():
    content = {"A": _c(brand="HURAKAN"), "B": _c(brand="APACH")}
    rows, manifest = _shape_rows(content, [_p("A", "1"), _p("B", "2")], ["hurakan"])
    assert [r[H_ARTICLE] for r in rows] == ["1"]
    assert manifest["per_brand"] == {"HURAKAN": 1}


def test_empty_selection_includes_all_brands():
    content = {"A": _c(brand="HURAKAN"), "B": _c(brand="APACH")}
    rows, _ = _shape_rows(content, [_p("A", "1"), _p("B", "2")], [])
    assert len(rows) == 2


def test_missing_feed_row_counted_not_emitted():
    content = {"A": _c()}
    rows, manifest = _shape_rows(content, [_p("A", "1"), _p("GHOST", "2")], [])
    assert [r[H_ARTICLE] for r in rows] == ["1"]
    assert manifest["missing_feed_row"] == 1


def test_skipped_no_price():
    content = {"A": _c(), "B": _c()}
    priced = [_p("A", "1", price_eur=None), _p("B", "2", price_eur=0.0)]
    rows, manifest = _shape_rows(content, priced, [])
    assert rows == []
    assert manifest["skipped_no_price"] == 2


def test_unmatched_feed_article_in_selected_brand():
    content = {"A": _c(brand="HURAKAN"), "B": _c(brand="HURAKAN")}
    rows, manifest = _shape_rows(content, [_p("A", "1")], ["HURAKAN"])
    assert manifest["total"] == 1
    assert manifest["unmatched"] == 1


def test_workbook_bytes_roundtrip_native_schema():
    content = {"A": _c(photos=["u1", "u2"])}
    rows, _ = _shape_rows(content, [_p("A", "777", price_eur=50.0, retail_eur=60.0)], [])
    wb = openpyxl.load_workbook(io.BytesIO(_workbook_bytes(rows)), read_only=True, data_only=True)
    ws = wb["Worksheet"]
    all_rows = list(ws.iter_rows(values_only=True))
    wb.close()
    assert list(all_rows[0]) == HEADERS
    data_row = dict(zip(HEADERS, all_rows[1]))
    assert data_row[H_ARTICLE] == "777"
    assert data_row[H_PRICE] == "50.0"
    assert data_row[H_OLDPRICE] == "60.0"
    assert data_row[H_GALLERY] == "u1;u2"
    hdr_join = " ".join(str(h) for h in all_rows[0])
    assert "Бренд" not in hdr_join
    assert "Название модификации" not in hdr_join
