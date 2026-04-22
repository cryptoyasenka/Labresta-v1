"""Tests for pricing engine — tenths-EUR output + auto-discount with min-margin."""

import pytest

from types import SimpleNamespace

from app.services.pricing import (
    calculate_auto_discount,
    calculate_price_eur,
    get_effective_discount,
    is_valid_price,
    resolve_discount_percent,
)


def _supplier(mode="flat", default=15.0, brand_rows=None):
    return SimpleNamespace(
        pricing_mode=mode,
        discount_percent=default,
        brand_discounts=brand_rows or [],
    )


def _brand_row(brand, pct):
    return SimpleNamespace(brand=brand, discount_percent=pct)


# --- calculate_price_eur: tenths rounding ---


def test_basic_discount_tenths():
    """199.99 EUR at 19% -> 161.99 -> 162.0 (half-up to tenths)."""
    assert calculate_price_eur(19999, 19.0) == 162.0


def test_zero_discount_tenths():
    """199.99 EUR at 0% -> 200.0."""
    assert calculate_price_eur(19999, 0.0) == 200.0


def test_half_tenth_rounds_up():
    """100.05 EUR (10005 cents) at 0% -> 100.1."""
    assert calculate_price_eur(10005, 0.0) == 100.1


def test_below_half_tenth_rounds_down():
    """100.04 EUR at 0% -> 100.0."""
    assert calculate_price_eur(10004, 0.0) == 100.0


def test_small_price():
    """1.00 EUR at 10% -> 0.9 EUR."""
    assert calculate_price_eur(100, 10.0) == 0.9


def test_full_discount():
    assert calculate_price_eur(19999, 100.0) == 0.0


# --- get_effective_discount ---


def test_product_override():
    assert get_effective_discount(20.0, 15.0) == 20.0


def test_supplier_default():
    assert get_effective_discount(None, 15.0) == 15.0


def test_override_zero_wins_over_default():
    """Explicit 0 is NOT None and should override a non-zero supplier default."""
    assert get_effective_discount(0.0, 19.0) == 0.0


# --- is_valid_price ---


def test_valid_price():
    assert is_valid_price(19999) is True


def test_zero_price():
    assert is_valid_price(0) is False


def test_none_price():
    assert is_valid_price(None) is False


def test_negative_price():
    assert is_valid_price(-100) is False


# --- calculate_auto_discount ---
# Params: cost_rate=0.75, min_margin_uah=500, target=19, rate=51.15
# Breakpoints:
#   Full 19% keeps margin >= 500 when retail_eur * 0.06 * 51.15 >= 500
#       -> retail_eur >= 162.906...
#   Zero-discount margin hits 500 when retail_eur * 0.25 * 51.15 >= 500
#       -> retail_eur >= 39.1006...


def test_auto_expensive_full_discount():
    """Retail 200 EUR (20000 cents) — full 19% applies, margin ~614 UAH."""
    assert calculate_auto_discount(20000, 51.15) == 19


def test_auto_exactly_at_full_threshold():
    """Retail 162.91 EUR — margin at 19% is 500.02 UAH, full 19% ok."""
    assert calculate_auto_discount(16291, 51.15) == 19


def test_auto_just_below_full_threshold():
    """Retail 162.90 EUR — margin at 19% ~499.96 UAH, reduce discount.

    d_real = 100*(0.25 - 500/(162.90*51.15)) = 100*(0.25 - 0.060003) = 18.9994
    ceil -> 19. But at 19% margin < 500. Allowed per spec — round up.
    """
    d = calculate_auto_discount(16290, 51.15)
    assert d == 19


def test_auto_midrange_100eur():
    """Retail 100 EUR.
    d_real = 100*(0.25 - 500/(100*51.15)) = 100*(0.25 - 0.09775) = 15.22...
    ceil -> 16.
    """
    assert calculate_auto_discount(10000, 51.15) == 16


def test_auto_50eur():
    """Retail 50 EUR.
    d_real = 100*(0.25 - 500/(50*51.15)) = 100*(0.25 - 0.1955) = 5.45
    ceil -> 6.
    """
    assert calculate_auto_discount(5000, 51.15) == 6


def test_auto_at_zero_threshold():
    """Retail 39.11 EUR — margin-at-zero = 500.13 UAH, so d_max ~0.025 -> ceil 1."""
    assert calculate_auto_discount(3911, 51.15) == 1


def test_auto_just_below_zero_threshold():
    """Retail 39.00 EUR — margin-at-zero = 498.71 UAH < 500, zero discount."""
    assert calculate_auto_discount(3900, 51.15) == 0


def test_auto_cheap_item():
    """Retail 10 EUR — way below, 0% discount."""
    assert calculate_auto_discount(1000, 51.15) == 0


def test_auto_invalid_price():
    assert calculate_auto_discount(0, 51.15) == 0
    assert calculate_auto_discount(-100, 51.15) == 0


def test_auto_invalid_rate():
    assert calculate_auto_discount(10000, 0) == 0


@pytest.mark.parametrize(
    "retail_cents,expected",
    [
        (100000, 19),   # 1000 EUR
        (20000, 19),    # 200 EUR
        (16291, 19),    # 162.91 EUR — at threshold
        (10000, 16),    # 100 EUR
        (7500, 12),     # 75 EUR — d_real=100*(0.25 - 500/(75*51.15))=100*(0.25-0.1303)=11.97 -> ceil 12
        (5000, 6),      # 50 EUR
        (3911, 1),      # just above zero threshold
        (3900, 0),      # just below zero threshold
        (1000, 0),      # cheap
    ],
)
def test_auto_parametrized(retail_cents, expected):
    assert calculate_auto_discount(retail_cents, 51.15) == expected


# --- resolve_discount_percent ---


def test_resolve_match_override_wins_flat():
    s = _supplier(mode="flat", default=15.0)
    assert resolve_discount_percent(22.0, s, "HURAKAN") == 22.0


def test_resolve_match_override_wins_per_brand():
    s = _supplier(
        mode="per_brand", default=17.0, brand_rows=[_brand_row("HURAKAN", 15.0)]
    )
    assert resolve_discount_percent(5.0, s, "HURAKAN") == 5.0


def test_resolve_flat_returns_supplier_default():
    s = _supplier(mode="flat", default=15.0)
    assert resolve_discount_percent(None, s, "HURAKAN") == 15.0


def test_resolve_per_brand_hit():
    s = _supplier(
        mode="per_brand",
        default=17.0,
        brand_rows=[
            _brand_row("HURAKAN", 15.0),
            _brand_row("SIRMAN", 20.0),
        ],
    )
    assert resolve_discount_percent(None, s, "HURAKAN") == 15.0
    assert resolve_discount_percent(None, s, "SIRMAN") == 20.0


def test_resolve_per_brand_case_insensitive():
    s = _supplier(
        mode="per_brand", default=17.0, brand_rows=[_brand_row("Robot Coupe", 20.0)]
    )
    assert resolve_discount_percent(None, s, "ROBOT COUPE") == 20.0
    assert resolve_discount_percent(None, s, "robot coupe") == 20.0


def test_resolve_per_brand_trims_whitespace():
    s = _supplier(
        mode="per_brand", default=17.0, brand_rows=[_brand_row("BARTSCHER", 20.0)]
    )
    assert resolve_discount_percent(None, s, "  BARTSCHER  ") == 20.0


def test_resolve_per_brand_miss_falls_back_to_default():
    s = _supplier(
        mode="per_brand", default=17.0, brand_rows=[_brand_row("HURAKAN", 15.0)]
    )
    assert resolve_discount_percent(None, s, "APACH") == 17.0


def test_resolve_per_brand_empty_brand_uses_default():
    s = _supplier(
        mode="per_brand", default=17.0, brand_rows=[_brand_row("HURAKAN", 15.0)]
    )
    assert resolve_discount_percent(None, s, None) == 17.0
    assert resolve_discount_percent(None, s, "") == 17.0
    assert resolve_discount_percent(None, s, "   ") == 17.0


def test_resolve_auto_margin_returns_default():
    """auto_margin path isn't resolved here — caller uses calculate_auto_discount."""
    s = _supplier(mode="auto_margin", default=19.0)
    assert resolve_discount_percent(None, s, "HURAKAN") == 19.0


def test_resolve_unknown_mode_treated_as_flat():
    s = _supplier(mode="something_weird", default=10.0)
    assert resolve_discount_percent(None, s, "HURAKAN") == 10.0


def test_resolve_missing_attributes_defaults_zero():
    """Duck-typed object without pricing_mode/discount_percent should not explode."""
    s = SimpleNamespace()
    assert resolve_discount_percent(None, s, "HURAKAN") == 0.0


def test_resolve_match_override_zero_wins():
    """Explicit 0 discount from operator beats any supplier rule."""
    s = _supplier(
        mode="per_brand", default=17.0, brand_rows=[_brand_row("HURAKAN", 15.0)]
    )
    assert resolve_discount_percent(0.0, s, "HURAKAN") == 0.0
