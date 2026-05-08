"""Hardcoded (brand, supplier) exclusions.

When a supplier carries a small number of off-brand SPs that pollute
matching/orphan-detection (e.g. Кодаки has 2 Hendi baskets, but Hendi
should match only with Астим), list the exclusion here. Both the
matcher and orphan_detector consult this map.

Format:
    BRAND_SUPPLIER_EXCLUSIONS = {lower(brand): {supplier_id, ...}}
"""
from __future__ import annotations

# Yana confirmed 2026-05-08: Hendi belongs to Астим (id=8) only.
# Кодаки (id=3) has 2 Hendi-branded SPs (sp_id=6076, 6160 — corzine 877 012/043),
# but they shouldn't count for matching or anchor purposes.
BRAND_SUPPLIER_EXCLUSIONS: dict[str, set[int]] = {
    "hendi": {3},
}


def is_excluded(brand: str | None, supplier_id: int | None) -> bool:
    """True if (brand, supplier_id) is on the hardcoded blocklist."""
    if not brand or supplier_id is None:
        return False
    return supplier_id in BRAND_SUPPLIER_EXCLUSIONS.get(brand.lower().strip(), set())
