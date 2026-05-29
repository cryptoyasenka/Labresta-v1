"""Tests for the MARESTO <stock> -> Horoshop «Наявність» mapping."""

from app.services.maresto_stock import (
    HOROSHOP_IN_STOCK,
    HOROSHOP_PREORDER,
    HOROSHOP_UNAVAILABLE,
    map_maresto_stock,
)


def test_in_stock_to_in_stock():
    assert map_maresto_stock("In stock", "Rational") == HOROSHOP_IN_STOCK


def test_running_low_folds_into_in_stock():
    # Yana's explicit rule: «заканчивается» still shown as «в наличии».
    assert map_maresto_stock("Running low", "Unox") == HOROSHOP_IN_STOCK


def test_reserved_to_preorder():
    assert map_maresto_stock("Reserved", "Brema") == HOROSHOP_PREORDER


def test_out_of_stock_chinese_brand_unavailable():
    for vendor in ("EWT INOX", "REEDNEE", "Forcar", "Forcold"):
        assert map_maresto_stock("Out of stock", vendor) == HOROSHOP_UNAVAILABLE


def test_out_of_stock_chinese_brand_is_case_insensitive():
    assert map_maresto_stock("Out of stock", "forcold") == HOROSHOP_UNAVAILABLE
    assert map_maresto_stock("out of stock", "ewt inox") == HOROSHOP_UNAVAILABLE


def test_out_of_stock_european_brand_to_preorder():
    assert map_maresto_stock("Out of stock", "Rational") == HOROSHOP_PREORDER


def test_out_of_stock_china_made_european_brand_not_buried():
    # Bartscher/Sirman/Fimar make goods in China but are re-ordered: they must
    # stay «под заказ», not «нет в наличии». Guards against a country-based rule.
    for vendor in ("Bartscher", "Sirman", "Fimar"):
        assert map_maresto_stock("Out of stock", vendor) == HOROSHOP_PREORDER


def test_in_stock_chinese_brand_stays_in_stock():
    # The brand split only affects out-of-stock items; in-stock Chinese goods
    # (e.g. 70 live REEDNEE products) must remain «в наличии».
    assert map_maresto_stock("In stock", "REEDNEE") == HOROSHOP_IN_STOCK


def test_unknown_or_missing_stock_returns_none():
    assert map_maresto_stock(None, "Rational") is None
    assert map_maresto_stock("", "Rational") is None
    assert map_maresto_stock("something else", "Rational") is None
