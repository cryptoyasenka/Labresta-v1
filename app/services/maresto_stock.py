"""Map MARESTO feed `<stock>` values to Horoshop «Наявність» statuses.

MARESTO's YML carries a 4-value `<stock>` element (In stock / Running low /
Reserved / Out of stock) that our generic parser otherwise flattens to the
binary `available` attribute. Horoshop's «Наявність» field, however, supports
named statuses. This module is the single source of truth for that mapping,
locked with Yana on 2026-05-29:

    In stock      -> В наявності
    Running low   -> В наявності        (заканчивается, но ещё есть)
    Reserved      -> Під замовлення     (под заказ, можно купить)
    Out of stock  -> Немає в наявності  ONLY for the cheap own-brands below
                  -> Під замовлення     for every other brand (везём под заказ)

«Очікується» is intentionally NOT produced: the feed has no delivery date or
expected-supply signal, so there is nothing to drive it.

The Chinese-brand split keys on `<vendor>`, NOT on the `Країна виробник`
country field: country == КИТАЙ also tags European brands (Bartscher, Sirman,
Fimar) that merely manufacture in China and are still re-ordered, so country
would wrongly bury them as "нет в наличии".
"""

# Exact Horoshop «Наявність» status strings (Ukrainian, from the store admin).
HOROSHOP_IN_STOCK = "В наявності"
HOROSHOP_PREORDER = "Під замовлення"
HOROSHOP_UNAVAILABLE = "Немає в наявності"

# Own cheap brands whose out-of-stock items are treated as gone (not re-ordered),
# matched case-insensitively against the MARESTO `<vendor>`.
CHINESE_BRANDS = frozenset({"ewt inox", "reednee", "forcar", "forcold"})


def map_maresto_stock(stock_status: str | None, vendor: str | None) -> str | None:
    """Return the Horoshop «Наявність» status for a MARESTO product.

    Args:
        stock_status: raw MARESTO `<stock>` value (e.g. "Out of stock").
        vendor: MARESTO `<vendor>` (brand), used only to split out-of-stock.

    Returns:
        A Horoshop status string, or None for an unknown/missing `<stock>`
        (caller should leave such a product's availability untouched).
    """
    status = (stock_status or "").strip().casefold()
    brand = (vendor or "").strip().casefold()

    if status in ("in stock", "running low"):
        return HOROSHOP_IN_STOCK
    if status == "reserved":
        return HOROSHOP_PREORDER
    if status == "out of stock":
        return HOROSHOP_UNAVAILABLE if brand in CHINESE_BRANDS else HOROSHOP_PREORDER
    return None
