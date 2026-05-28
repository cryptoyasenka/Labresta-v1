"""Tests for app.services.np_parser.parse_np_feed.

Self-contained: each test builds a tiny NP-layout xlsx in tmp_path with
openpyxl (header row + data rows at the real 0-based column indices), so there
is no dependency on the live feed, the network, or the DB / Flask fixtures.
"""

import openpyxl

from app.services.np_parser import parse_np_feed

# Mirror the parser's column contract (0-based).
_C_ARTICLE = 1
_C_PHOTOS = 3
_C_DESC_UA = 7
_C_BRAND = 9
_C_DESC_RU = 16
_NCOLS = 24


def _make_feed(tmp_path, data_rows, *, header_article="Артикул", sheet="Worksheet"):
    """Write an NP-style workbook; data_rows = list of {col_index: value}."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = sheet
    header = [None] * _NCOLS
    header[_C_ARTICLE] = header_article
    header[2] = "[КАТАЛОГ] Цена"
    ws.append(header)
    for spec in data_rows:
        row = [None] * _NCOLS
        for idx, val in spec.items():
            row[idx] = val
        ws.append(row)
    path = tmp_path / "np-feed.xlsx"
    wb.save(path)
    wb.close()
    return str(path)


def test_parses_single_row(tmp_path):
    path = _make_feed(tmp_path, [{
        _C_ARTICLE: "ART-1", _C_BRAND: "HURAKAN",
        _C_DESC_UA: "<p>опис</p>", _C_DESC_RU: "<p>описание</p>",
        _C_PHOTOS: "https://np.com.ua/a.jpg",
    }])
    content, errors = parse_np_feed(path)
    assert errors == []
    assert content == {
        "ART-1": {
            "brand": "HURAKAN",
            "description": "<p>опис</p>",
            "description_ru": "<p>описание</p>",
            "photos": ["https://np.com.ua/a.jpg"],
        }
    }


def test_gallery_split_dedup_and_order(tmp_path):
    path = _make_feed(tmp_path, [{
        _C_ARTICLE: "ART-2",
        _C_PHOTOS: "https://x/1.jpg; https://x/2.jpg ;https://x/1.jpg;;",
    }])
    content, _ = parse_np_feed(path)
    assert content["ART-2"]["photos"] == ["https://x/1.jpg", "https://x/2.jpg"]


def test_numeric_article_coerced_to_string(tmp_path):
    path = _make_feed(tmp_path, [{_C_ARTICLE: 1546341257, _C_BRAND: "APACH"}])
    content, _ = parse_np_feed(path)
    assert "1546341257" in content
    assert content["1546341257"]["brand"] == "APACH"


def test_duplicate_article_first_wins_with_warning(tmp_path):
    path = _make_feed(tmp_path, [
        {_C_ARTICLE: "DUP", _C_DESC_UA: "first"},
        {_C_ARTICLE: "DUP", _C_DESC_UA: "second"},
    ])
    content, errors = parse_np_feed(path)
    assert content["DUP"]["description"] == "first"
    assert any("duplicate" in e.lower() for e in errors)


def test_keyless_content_row_flagged_blank_row_silent(tmp_path):
    path = _make_feed(tmp_path, [
        {_C_DESC_UA: "<p>orphan</p>"},  # content but no Артикул → warn
        {_C_BRAND: None},               # nothing useful → silent skip
    ])
    content, errors = parse_np_feed(path)
    assert content == {}
    assert sum("empty Артикул" in e for e in errors) == 1


def test_empty_photos_cell_yields_empty_list(tmp_path):
    path = _make_feed(tmp_path, [{_C_ARTICLE: "ART-3", _C_PHOTOS: None}])
    content, _ = parse_np_feed(path)
    assert content["ART-3"]["photos"] == []


def test_missing_text_fields_are_none(tmp_path):
    path = _make_feed(tmp_path, [{_C_ARTICLE: "ART-5"}])
    content, _ = parse_np_feed(path)
    assert content["ART-5"]["brand"] is None
    assert content["ART-5"]["description"] is None
    assert content["ART-5"]["description_ru"] is None


def test_header_mismatch_aborts(tmp_path):
    path = _make_feed(tmp_path, [{_C_ARTICLE: "ART-4"}], header_article="НЕ ТО")
    content, errors = parse_np_feed(path)
    assert content == {}
    assert len(errors) == 1
    assert "header mismatch" in errors[0].lower()


def test_falls_back_to_first_sheet_when_no_worksheet_named(tmp_path):
    path = _make_feed(tmp_path, [{_C_ARTICLE: "ART-6"}], sheet="Аркуш1")
    content, errors = parse_np_feed(path)
    assert "ART-6" in content
    assert errors == []
