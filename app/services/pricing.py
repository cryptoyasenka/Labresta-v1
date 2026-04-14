"""Pricing engine — pure functions for discount and price calculations.

Prices are computed in EUR to 1 decimal place (tenths).
Discount auto-calc keeps UAH margin >= configured minimum.
"""

import math


def calculate_price_eur(retail_price_cents: int, discount_percent: float) -> float:
    """Final sell price in EUR, rounded to 1 decimal place (half-up).

    Args:
        retail_price_cents: Supplier retail price in cents (19999 = 199.99 EUR).
        discount_percent: Discount to apply (19.0 = -19%).

    Returns:
        Price in EUR with one decimal (e.g. 161.9).
    """
    discounted_cents = retail_price_cents * (100 - discount_percent) / 100
    tenths = math.floor(discounted_cents / 10 + 0.5)
    return tenths / 10.0


def get_effective_discount(
    match_discount: float | None,
    supplier_discount: float,
) -> float:
    """Per-match override wins, else supplier default."""
    if match_discount is not None:
        return match_discount
    return supplier_discount


def is_valid_price(price_cents: int | None) -> bool:
    return price_cents is not None and price_cents > 0


def calculate_auto_discount(
    retail_price_cents: int,
    eur_rate_uah: float,
    target_discount: float = 19.0,
    cost_rate: float = 0.75,
    min_margin_uah: float = 500.0,
) -> int:
    """Largest integer discount % keeping UAH margin >= min_margin_uah.

    Margin formula:
        margin_eur = retail_eur * ((1 - d/100) - cost_rate)
        margin_uah = margin_eur * eur_rate_uah

    Returns:
        - target_discount (int) if full discount keeps margin >= min
        - smallest integer d in [1..target_discount-1] with margin >= min (ceil of d_max)
        - 0 if even zero discount can't reach min margin (cheap item, sell at retail)
    """
    if retail_price_cents <= 0 or eur_rate_uah <= 0:
        return 0

    retail_eur = retail_price_cents / 100.0
    max_margin_frac = 1 - cost_rate  # 0.25 when cost_rate=0.75

    # margin at 0% discount — if below min, cheap item, sell at retail
    margin_at_zero_uah = retail_eur * max_margin_frac * eur_rate_uah
    if margin_at_zero_uah < min_margin_uah:
        return 0

    # margin at target — if keeps min, apply full target discount
    target_frac = max_margin_frac - target_discount / 100.0
    if target_frac * retail_eur * eur_rate_uah >= min_margin_uah:
        return int(target_discount)

    # binary/search boundary: largest integer d in [0..target) with margin >= min.
    # d_max (real) satisfies (max_margin_frac - d/100) * retail_eur * rate = min
    # → d = 100 * (max_margin_frac - min/(retail_eur*rate))
    d_real = 100.0 * (max_margin_frac - min_margin_uah / (retail_eur * eur_rate_uah))
    # Round UP per spec ("до целого числа в большую сторону") — margin may dip slightly below min.
    d = math.ceil(d_real)
    if d < 0:
        return 0
    if d > int(target_discount):
        return int(target_discount)
    return d
