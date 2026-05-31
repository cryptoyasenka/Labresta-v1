"""Tests for app.services.np_parser.parse_np_feed.

Self-contained: each test builds a tiny NP-layout xlsx in tmp_path with
openpyxl (header row + data rows at the real 0-based column indices), so there
is no dependency on the live feed, the network, or the DB / Flask fixtures.
"""

import openpyxl

from app.services.np_parser import parse_np_feed

# Mirror the parser's column contract (0-based). title_uk/title_ru/categories_uk
# are located by header LABEL (not fixed index), so the fixture sets both the
# label in the header row and the value at the same index. Live positions are
# 6/15/8; the fixture mirrors them but the parser would find them anywhere.
_C_ARTICLE = 1
_C_PHOTOS = 3
_C_NAME_UA = 6
_C_DESC_UA = 7
_C_CATEGORY = 8
_C_BRAND = 9
_C_NAME_RU = 15
_C_DESC_RU = 16
_NCOLS = 24


def _make_feed(
    tmp_path,
    data_rows,
    *,
    header_article="Артикул",
    sheet="Worksheet",
    name_labels=True,
):
    """Write an NP-style workbook; data_rows = list of {col_index: value}.

    When ``name_labels`` is True the header row carries the title_uk/title_ru/
    categories_uk labels (located by the parser via header scan); set it False
    to simulate a feed missing those optional columns.
    """
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = sheet
    header = [None] * _NCOLS
    header[_C_ARTICLE] = header_article
    header[2] = "[КАТАЛОГ] Цена"
    if name_labels:
        header[_C_NAME_UA] = "title_uk"
        header[_C_CATEGORY] = "categories_uk"
        header[_C_NAME_RU] = "title_ru"
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
            "name": None,
            "name_ru": None,
            "category": None,
        }
    }


def test_parses_name_and_category(tmp_path):
    path = _make_feed(tmp_path, [{
        _C_ARTICLE: "ART-7", _C_BRAND: "HURAKAN",
        _C_NAME_UA: "Льодогенератор Hurakan HKN-IMC25",
        _C_NAME_RU: "Ледогенератор Hurakan HKN-IMC25",
        _C_CATEGORY: "Холодильне обладнання/Льодогенератори",
        _C_DESC_UA: "<p>опис</p>",
    }])
    content, errors = parse_np_feed(path)
    assert errors == []
    assert content["ART-7"]["name"] == "Льодогенератор Hurakan HKN-IMC25"
    assert content["ART-7"]["name_ru"] == "Ледогенератор Hurakan HKN-IMC25"
    assert content["ART-7"]["category"] == "Холодильне обладнання/Льодогенератори"
    # Existing fields stay intact (additive).
    assert content["ART-7"]["brand"] == "HURAKAN"
    assert content["ART-7"]["description"] == "<p>опис</p>"


def test_missing_name_columns_non_fatal(tmp_path):
    # A feed lacking the title_uk/title_ru/categories_uk labels still parses;
    # name/name_ru/category come back None with a warning, brand/desc/photos read.
    path = _make_feed(
        tmp_path,
        [{
            _C_ARTICLE: "ART-8", _C_BRAND: "APACH",
            _C_DESC_UA: "<p>опис</p>",
            _C_PHOTOS: "https://np.com.ua/x.jpg",
        }],
        name_labels=False,
    )
    content, errors = parse_np_feed(path)
    assert content["ART-8"]["name"] is None
    assert content["ART-8"]["name_ru"] is None
    assert content["ART-8"]["category"] is None
    # Brand / description / photos still read despite the missing labels.
    assert content["ART-8"]["brand"] == "APACH"
    assert content["ART-8"]["description"] == "<p>опис</p>"
    assert content["ART-8"]["photos"] == ["https://np.com.ua/x.jpg"]
    # Three non-fatal warnings (one per missing optional column).
    assert sum("missing optional column" in e for e in errors) == 3


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
    # Name/category labels present in the header but the row leaves them empty.
    assert content["ART-5"]["name"] is None
    assert content["ART-5"]["name_ru"] is None
    assert content["ART-5"]["category"] is None


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
