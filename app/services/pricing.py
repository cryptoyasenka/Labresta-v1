"""Pricing engine — pure functions for discount and rounding calculations.

All arithmetic uses integer cents to avoid floating-point errors.
Mathematical rounding: 0.5 always rounds up (not banker's rounding).
"""


def calculate_price_eur(retail_price_cents: int, discount_percent: float) -> int:
    """Calculate final price in whole EUR with mathematical rounding.

    Discount applied as: cents * (100 - discount) / 100.
    Rounding to whole EUR: (cents + 50) // 100 always rounds 0.5 up.

    Args:
        retail_price_cents: Supplier retail price in cents (e.g., 19999 for 199.99 EUR).
        discount_percent: Discount as percentage (e.g., 15.0 for 15%).

    Returns:
        Final price in whole EUR (e.g., 170 for 169.99 EUR at 15%).
    """
    discounted_cents = round(retail_price_cents * (100 - discount_percent) / 100)
    whole_eur = (discounted_cents + 50) // 100
    return whole_eur


def get_effective_discount(
    match_discount: float | None,
    supplier_discount: float,
) -> float:
    """Get effective discount -- per-product override takes priority.

    Args:
        match_discount: Per-product discount override (None = use supplier default).
        supplier_discount: Supplier-level default discount.

    Returns:
        The effective discount percentage to apply.
    """
    if match_discount is not None:
        return match_discount
    return supplier_discount


def is_valid_price(price_cents: int | None) -> bool:
    """Check if a price is valid for YML inclusion.

    Zero, None, and negative prices are invalid.
    """
    return price_cents is not None and price_cents > 0
