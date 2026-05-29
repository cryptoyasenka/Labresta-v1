"""MARESTO Horoshop matcher file builder — price + availability (Channel 2).

Produces the native-schema Horoshop XLSX the operator imports by hand to refresh
MARESTO matched products: PRICE (as the matcher computes it, with discount) AND
availability as a named «Наявність» status derived from the feed's 4-value
`<stock>` (In stock / Running low / Reserved / Out of stock).

Why Excel and not the YML-by-URL feed: the YML `<offer available>` attribute is
binary, so the named statuses (В наявності / Під замовлення / Немає в наявності)
can only be delivered through the tabular «Наличие» column — the same native
[КАТАЛОГ] channel NP uses (proven live: NP canary 2026-05-19, and the MARESTO
1-row import preview 2026-05-29 where «[КАТАЛОГ] Наличие» auto-mapped and
accepted «Під замовлення»). The status MAPPING lives in services/maresto_stock.py
(single source of truth, locked with Yana 2026-05-29).

Column scope = price + availability ONLY (Yana: «цены и наличия как обычно»):
    Артикул (KEY == PromProduct.external_id), [КАТАЛОГ] Цена, Старая цена,
    Валюта, Наличие. NO name/description/photo (those are owned by Horoshop /
    delivered via the NP content channel) — an omitted column leaves that catalog
    field untouched on import.

Header strings are copied verbatim from the live-proven NP canary — do NOT
retype them from memory. Read-only w.r.t. the DB: queries matches, writes nothing.

⚠️ Before the first bulk import, run a 1-row empirical test (done 2026-05-29 for
the availability column). The live import stays Yana's hand (feedback_labresta_live_import).
"""

from __future__ import annotations

import io
import logging

import openpyxl
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from app.extensions import db
from app.models.product_match import ProductMatch
from app.models.supplier import Supplier
from app.models.supplier_product import SupplierProduct
from app.services.maresto_stock import map_maresto_stock
from app.services.pricing import compute_match_pricing

logger = logging.getLogger(__name__)

MARESTO_SUPPLIER_SLUG = "maresto"

# Proven auto-mapping headers (live: NP canary 2026-05-19). Prefix "[КАТАЛОГ] "
# + leaf == the catalog field's qualified import name.
_PREFIX = "[КАТАЛОГ] "
H_ARTICLE = "Артикул"            # top-level field → bare name, KEY == PromProduct.external_id
H_PRICE = _PREFIX + "Цена"
H_OLDPRICE = _PREFIX + "Старая цена"
H_CURRENCY = _PREFIX + "Валюта"
H_AVAIL = _PREFIX + "Наличие"    # named «Наявність» status goes here

HEADERS = [H_ARTICLE, H_PRICE, H_OLDPRICE, H_CURRENCY, H_AVAIL]

_SHEET = "Worksheet"


def _shape_rows(matches: list[dict]) -> tuple[list[dict], dict]:
    """Pure: confirmed MARESTO matches → import rows + a sanity manifest.

    Args:
        matches: list of {external_id, stock_status, vendor, price_eur,
            retail_eur, currency} — one per confirmed MARESTO match
            (external_id == Horoshop artikul; price_eur == discounted sell price).

    Returns:
        (rows, manifest). rows = list of {header: value}. manifest carries the
        per-status counts the UI/operator sanity-checks before importing.
    """
    rows: list[dict] = []
    manifest = {
        "total": 0,
        "per_status": {},
        "skipped_no_status": 0,
        "skipped_no_artikul": 0,
        "skipped_no_price": 0,
    }

    for m in matches:
        artikul = str(m.get("external_id") or "").strip()
        if not artikul:
            manifest["skipped_no_artikul"] += 1
            continue
        status = map_maresto_stock(m.get("stock_status"), m.get("vendor"))
        if status is None:
            # Unknown/missing <stock> — leave this card's availability untouched.
            manifest["skipped_no_status"] += 1
            continue
        price = m.get("price_eur")
        if price is None or price <= 0:
            # No valid price → can't refresh "цена как обычно"; skip the whole row
            # rather than push availability without price.
            manifest["skipped_no_price"] += 1
            continue

        retail = m.get("retail_eur")
        # <oldprice> only on a real discount (retail noticeably above sell);
        # empty cell otherwise clears any stale strikethrough price in Horoshop.
        oldprice = f"{retail:.1f}" if (retail is not None and retail > price + 0.05) else ""

        rows.append({
            H_ARTICLE: artikul,
            H_PRICE: f"{price:.1f}",
            H_OLDPRICE: oldprice,
            H_CURRENCY: m.get("currency") or "EUR",
            H_AVAIL: status,
        })
        manifest["total"] += 1
        manifest["per_status"][status] = manifest["per_status"].get(status, 0) + 1

    return rows, manifest


def _workbook_bytes(rows: list[dict]) -> bytes:
    """Pure: serialise shaped rows into native-schema xlsx bytes."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = _SHEET
    ws.append(HEADERS)
    for r in rows:
        ws.append([r[h] for h in HEADERS])
    buf = io.BytesIO()
    wb.save(buf)
    wb.close()
    return buf.getvalue()


def _query_maresto_matches(supplier_id: int) -> list[dict]:
    """DB → list of priced confirmed MARESTO matches (plain dicts for _shape_rows)."""
    matches = db.session.execute(
        select(ProductMatch)
        .join(SupplierProduct, ProductMatch.supplier_product_id == SupplierProduct.id)
        .where(
            SupplierProduct.supplier_id == supplier_id,
            ProductMatch.status.in_(("confirmed", "manual")),
            ProductMatch.published.is_(True),
        )
        .options(
            joinedload(ProductMatch.supplier_product)
            .joinedload(SupplierProduct.supplier)
            .selectinload(Supplier.brand_discounts),
            joinedload(ProductMatch.prom_product),
        )
    ).scalars().unique().all()

    out: list[dict] = []
    for m in matches:
        sp = m.supplier_product
        pp = m.prom_product
        p = compute_match_pricing(m)
        out.append({
            "external_id": pp.external_id,            # Horoshop artikul (KEY)
            "stock_status": sp.stock_status,
            "vendor": sp.brand,                       # <vendor>, used only for the OOS brand split
            "price_eur": p["price_eur"] if p else None,
            "retail_eur": (sp.price_cents or 0) / 100.0,
            "currency": (sp.currency or "EUR") if sp.currency in ("EUR", "UAH") else "EUR",
        })
    return out


def build_maresto_file() -> tuple[bytes, dict]:
    """Build the MARESTO price+availability import file.

    Returns:
        (xlsx_bytes, manifest). manifest carries per-status counts +
        matches_considered for the UI / operator.
    """
    supplier = db.session.execute(
        select(Supplier).where(Supplier.slug == MARESTO_SUPPLIER_SLUG)
    ).scalar_one_or_none()
    if supplier is None:
        return _workbook_bytes([]), {
            "error": f"MARESTO supplier (slug={MARESTO_SUPPLIER_SLUG!r}) not found",
            "total": 0,
        }

    matches = _query_maresto_matches(supplier.id)
    rows, manifest = _shape_rows(matches)
    manifest["matches_considered"] = len(matches)

    logger.info(
        "MARESTO file: %d rows from %d matches | per-status %s | skipped "
        "%d no-status, %d no-price, %d no-artikul",
        manifest["total"], len(matches), manifest["per_status"],
        manifest["skipped_no_status"], manifest["skipped_no_price"],
        manifest["skipped_no_artikul"],
    )
    return _workbook_bytes(rows), manifest
