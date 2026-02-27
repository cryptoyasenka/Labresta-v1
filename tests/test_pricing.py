"""Tests for pricing engine — integer-cent math with mathematical rounding."""

from app.services.pricing import calculate_price_eur, get_effective_discount, is_valid_price


# --- calculate_price_eur ---


def test_basic_discount():
    """199.99 EUR (19999 cents) at 15% discount."""
    assert calculate_price_eur(19999, 15.0) == 170


def test_zero_discount():
    """199.99 EUR at 0% = 199.99 -> 200 EUR (rounds up)."""
    assert calculate_price_eur(19999, 0.0) == 200


def test_half_rounds_up():
    """100.50 EUR (10050 cents) at 0% = 101 EUR (0.5 rounds up)."""
    assert calculate_price_eur(10050, 0.0) == 101


def test_below_half_rounds_down():
    """100.49 EUR (10049 cents) at 0% = 100 EUR (0.49 rounds down)."""
    assert calculate_price_eur(10049, 0.0) == 100


def test_small_price():
    """1.00 EUR (100 cents) at 10% = 90 cents -> 1 EUR."""
    assert calculate_price_eur(100, 10.0) == 1


def test_full_discount():
    """100% discount -> 0 EUR."""
    assert calculate_price_eur(19999, 100.0) == 0


def test_large_discount():
    """19999 cents at 50% = 9999.5 -> round -> 10000 cents -> 100 EUR."""
    assert calculate_price_eur(19999, 50.0) == 100


# --- get_effective_discount ---


def test_product_override():
    """Per-product discount takes priority over supplier default."""
    assert get_effective_discount(20.0, 15.0) == 20.0


def test_supplier_default():
    """None match discount falls back to supplier default."""
    assert get_effective_discount(None, 15.0) == 15.0


def test_both_zero():
    """None match + 0.0 supplier -> 0.0."""
    assert get_effective_discount(None, 0.0) == 0.0


# --- is_valid_price ---


def test_valid_price():
    assert is_valid_price(19999) is True


def test_zero_price():
    assert is_valid_price(0) is False


def test_none_price():
    assert is_valid_price(None) is False


def test_negative_price():
    assert is_valid_price(-100) is False
