"""MARESTO Horoshop availability file builder.

Produces a NARROW native-schema Horoshop XLSX the operator imports by hand to
push MARESTO's 4-value `<stock>` availability onto the store as named «Наявність»
statuses. Carries ONLY two columns — the article key and the availability status
— so a partial import refreshes availability and leaves price/photo/description
untouched.

Why a file (not the YML feed): the YML `available` attribute is binary, so the
3-way named status (В наявності / Під замовлення / Немає в наявності) can only be
delivered through the tabular «Наявність» column. The status MAPPING itself lives
in services/maresto_stock.py (single source of truth, locked with Yana 2026-05-29).

Header choice: "[КАТАЛОГ] Наличие" is the column header proven to auto-map to the
catalog availability field on the live store (NP canary 2026-05-19,
CANARY-IMPORT-GUIDE §7). The VALUES are Yana's actual Ukrainian store statuses
(see her «Наявність» dropdown). ⚠️ The acceptance of the 4 named Ukrainian
statuses through this column still needs a 1-row empirical import test before a
bulk push (see RESEARCH-horoshop-availability-and-new-offers.md and
feedback_labresta_live_import — the live import stays Yana's hand).

Read-only w.r.t. the DB: queries matches, writes nothing.
"""

from __future__ import annotations

import io
import logging

import openpyxl
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.extensions import db
from app.models.product_match import ProductMatch
from app.models.supplier import Supplier
from app.models.supplier_product import SupplierProduct
from app.services.maresto_stock import map_maresto_stock

logger = logging.getLogger(__name__)

MARESTO_SUPPLIER_SLUG = "maresto"

# Proven auto-mapping headers (live, NP canary 2026-05-19).
_PREFIX = "[КАТАЛОГ] "
H_ARTICLE = "Артикул"           # top-level field → bare name, KEY == PromProduct.external_id
H_AVAIL = _PREFIX + "Наличие"   # auto-maps to the catalog availability field

HEADERS = [H_ARTICLE, H_AVAIL]

_SHEET = "Worksheet"


def _shape_rows(matches: list[dict]) -> tuple[list[dict], dict]:
    """Pure: confirmed MARESTO matches → import rows + a sanity manifest.

    Args:
        matches: list of {external_id, stock_status, vendor} — one per confirmed
            MARESTO match (DB-derived; external_id == Horoshop artikul).

    Returns:
        (rows, manifest). rows = list of {header: value}. manifest carries the
        per-status counts the UI shows so the operator can sanity-check first.
    """
    rows: list[dict] = []
    manifest = {
        "total": 0,
        "per_status": {},
        "skipped_no_status": 0,
        "skipped_no_artikul": 0,
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
        rows.append({H_ARTICLE: artikul, H_AVAIL: status})
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
    """DB → list of confirmed MARESTO matches (plain dicts for _shape_rows)."""
    matches = db.session.execute(
        select(ProductMatch)
        .join(SupplierProduct, ProductMatch.supplier_product_id == SupplierProduct.id)
        .where(
            SupplierProduct.supplier_id == supplier_id,
            ProductMatch.status.in_(("confirmed", "manual")),
            ProductMatch.published.is_(True),
        )
        .options(
            joinedload(ProductMatch.supplier_product),
            joinedload(ProductMatch.prom_product),
        )
    ).scalars().unique().all()

    out: list[dict] = []
    for m in matches:
        sp = m.supplier_product
        pp = m.prom_product
        out.append({
            "external_id": pp.external_id,   # Horoshop artikul (KEY)
            "stock_status": sp.stock_status,
            "vendor": sp.brand,              # <vendor>, used only for the OOS brand split
        })
    return out


def build_maresto_file() -> tuple[bytes, dict]:
    """Build the MARESTO availability import file.

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
        "MARESTO availability file: %d rows from %d matches | per-status %s "
        "| skipped %d no-status, %d no-artikul",
        manifest["total"], len(matches), manifest["per_status"],
        manifest["skipped_no_status"], manifest["skipped_no_artikul"],
    )
    return _workbook_bytes(rows), manifest
