"""Tests for the MARESTO Horoshop availability file builder (pure parts)."""

import io

import openpyxl

from app.services.maresto_horoshop_file import (
    H_ARTICLE,
    H_AVAIL,
    HEADERS,
    _shape_rows,
    _workbook_bytes,
)


def test_shape_rows_maps_statuses_and_counts():
    matches = [
        {"external_id": "111", "stock_status": "In stock", "vendor": "Rational"},
        {"external_id": "222", "stock_status": "Running low", "vendor": "Unox"},
        {"external_id": "333", "stock_status": "Reserved", "vendor": "Brema"},
        {"external_id": "444", "stock_status": "Out of stock", "vendor": "Forcar"},    # chinese
        {"external_id": "555", "stock_status": "Out of stock", "vendor": "Rational"},  # european
        {"external_id": "666", "stock_status": None, "vendor": "X"},                   # skip: no status
        {"external_id": "", "stock_status": "In stock", "vendor": "Y"},               # skip: no artikul
    ]
    rows, manifest = _shape_rows(matches)

    assert manifest["total"] == 5
    assert manifest["skipped_no_status"] == 1
    assert manifest["skipped_no_artikul"] == 1

    by_art = {r[H_ARTICLE]: r[H_AVAIL] for r in rows}
    assert by_art["111"] == "В наявності"
    assert by_art["222"] == "В наявності"
    assert by_art["333"] == "Під замовлення"
    assert by_art["444"] == "Немає в наявності"     # chinese OOS
    assert by_art["555"] == "Під замовлення"        # european OOS
    assert "666" not in by_art

    assert manifest["per_status"]["В наявності"] == 2
    assert manifest["per_status"]["Під замовлення"] == 2
    assert manifest["per_status"]["Немає в наявності"] == 1


def test_workbook_bytes_roundtrips_header_and_rows():
    rows = [
        {H_ARTICLE: "111", H_AVAIL: "В наявності"},
        {H_ARTICLE: "444", H_AVAIL: "Немає в наявності"},
    ]
    data = _workbook_bytes(rows)

    wb = openpyxl.load_workbook(io.BytesIO(data))
    ws = wb.active
    assert [c.value for c in ws[1]] == HEADERS
    assert ws[2][0].value == "111"
    assert ws[2][1].value == "В наявності"
    assert ws[3][1].value == "Немає в наявності"


def test_empty_matches_produces_header_only_file():
    rows, manifest = _shape_rows([])
    assert rows == []
    assert manifest["total"] == 0
    data = _workbook_bytes(rows)
    wb = openpyxl.load_workbook(io.BytesIO(data))
    assert [c.value for c in wb.active[1]] == HEADERS
