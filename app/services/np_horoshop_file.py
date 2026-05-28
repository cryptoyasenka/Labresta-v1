"""НП Horoshop bulk file builder — Channel 2 (catalog content).

Produces the native-schema Horoshop XLSX the operator imports by hand for the
9 exclusive «Новый проект» brands. Carries the content the matcher YML feed
deliberately omits (Path B): description UA/RU + photo gallery, plus the
volatile price/availability so a single import refreshes everything.

Why a native XLSX *file* and not a YML feed: Horoshop's YML parser drops
<description_ru> and cross-maps <name> UA→RU (proven live 2026-05-19). The
native dealer-export schema auto-maps a column → catalog field ONLY when the
column header equals the field's qualified name ("[КАТАЛОГ] <leaf>", or a bare
top-level name like "Артикул"). build_canary_xlsx.py proved this end-to-end on
the live store (CANARY-IMPORT-GUIDE §7: 11/12 auto-mapped, ZERO UA→RU
corruption); this module generalises that single-row prototype to brand scope.

Column scope (Yana: «описание и фото + цена+наличие»). The file is NARROW — it
carries ONLY these eight proven-auto-mapping columns:
    Артикул (KEY, == PromProduct.external_id), [КАТАЛОГ] Цена, Старая цена,
    Валюта, Наличие, Галерея, Описание товара (UA), Описание товара (RU).
DELIBERATELY EXCLUDED — name «Название модификации UA/RU», «Бренд»,
«Отображать»: not requested + safer. Horoshop only updates columns present and
recognised, so an omitted column leaves that catalog field untouched. The
header strings below are copied verbatim from the live-proven canary — do NOT
retype them from memory.

Read-only w.r.t. the DB: queries matches/pricing, writes nothing. The live
import stays Yana's hand (invariant #13).
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
from app.services.np_parser import parse_np_feed
from app.services.pricing import compute_match_pricing
# Reuse the single source of truth for offer availability (don't duplicate the
# rule — divergence is exactly the P-3 class of bug the audit fixed).
from app.services.yml_generator import _is_available_for_offer

logger = logging.getLogger(__name__)

NP_SUPPLIER_SLUG = "novyy-proekt"

# Proven auto-mapping headers (canary live 2026-05-19, CANARY-IMPORT-GUIDE §7).
# Prefix "[КАТАЛОГ] " + leaf == Horoshop catalog field's qualified name.
_PREFIX = "[КАТАЛОГ] "
H_ARTICLE = "Артикул"                       # top-level field → bare name, KEY
H_PRICE = _PREFIX + "Цена"
H_OLDPRICE = _PREFIX + "Старая цена"
H_CURRENCY = _PREFIX + "Валюта"
H_AVAIL = _PREFIX + "Наличие"
H_GALLERY = _PREFIX + "Галерея"
H_DESC_UA = _PREFIX + "Описание товара (UA)"
H_DESC_RU = _PREFIX + "Описание товара (RU)"

# Column order of the output file. Article first (the key), then price bearers,
# then the catalog content. No name / brand / visibility columns by design.
HEADERS = [
    H_ARTICLE, H_PRICE, H_OLDPRICE, H_CURRENCY,
    H_AVAIL, H_GALLERY, H_DESC_UA, H_DESC_RU,
]

_AVAIL_YES = "В наличии"
_AVAIL_NO = "Нет в наличии"

_SHEET = "Worksheet"


def _norm(value) -> str:
    return (value or "").strip().lower()


def _shape_rows(
    content: dict[str, dict],
    priced: list[dict],
    selected_brands,
) -> tuple[list[dict], dict]:
    """Pure join: feed content × priced matches, filtered to selected brands.

    Args:
        content: parse_np_feed() output — {article: {brand, description,
            description_ru, photos}}.
        priced: list of {article, external_id, price_eur, retail_eur,
            available, currency} — one per NP published match (DB-derived).
        selected_brands: brand labels the operator ticked (case-insensitive).
            Empty/falsy = no brand filter (include every matched article).

    Returns:
        (rows, manifest). rows = list of {header: value}. manifest carries the
        counts the UI shows so the operator can sanity-check before importing.
    """
    sel = {_norm(b) for b in (selected_brands or []) if _norm(b)}
    rows: list[dict] = []
    manifest = {
        "total": 0,
        "with_photo": 0,
        "no_photo": 0,
        "missing_feed_row": 0,
        "skipped_no_price": 0,
        "unmatched": 0,
        "per_brand": {},
    }
    priced_articles: set[str] = set()

    for pm in priced:
        art = pm["article"]
        priced_articles.add(art)
        c = content.get(art)
        if c is None:
            # Published match whose article is absent from the current feed —
            # can't source description/photo for it.
            manifest["missing_feed_row"] += 1
            continue
        if sel and _norm(c.get("brand")) not in sel:
            continue
        price = pm.get("price_eur")
        if price is None or price <= 0:
            manifest["skipped_no_price"] += 1
            continue

        photos = c.get("photos") or []
        retail = pm.get("retail_eur")
        # oldprice only when a real discount applies (retail noticeably above
        # sell) — mirrors the YML feed; empty cell otherwise clears any stale
        # strikethrough price in Horoshop.
        oldprice = (
            f"{retail:.1f}"
            if (retail is not None and retail > price + 0.05)
            else ""
        )
        rows.append({
            H_ARTICLE: str(pm["external_id"]),          # KEY = our catalog card
            H_PRICE: f"{price:.1f}",
            H_OLDPRICE: oldprice,
            H_CURRENCY: pm.get("currency") or "EUR",
            H_AVAIL: _AVAIL_YES if pm.get("available") else _AVAIL_NO,
            H_GALLERY: ";".join(photos),
            H_DESC_UA: c.get("description") or "",
            H_DESC_RU: c.get("description_ru") or "",
        })

        manifest["total"] += 1
        if photos:
            manifest["with_photo"] += 1
        else:
            manifest["no_photo"] += 1
        brand_label = c.get("brand") or "(без бренда)"
        manifest["per_brand"][brand_label] = manifest["per_brand"].get(brand_label, 0) + 1

    # Informational: feed articles in the selected brands that have NO published
    # match (operator may want to match/publish them first).
    for art, c in content.items():
        if art in priced_articles:
            continue
        if sel and _norm(c.get("brand")) not in sel:
            continue
        manifest["unmatched"] += 1

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


def _query_np_priced(supplier_id: int) -> list[dict]:
    """DB → list of priced NP published matches (plain dicts for _shape_rows)."""
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

    priced: list[dict] = []
    for m in matches:
        sp = m.supplier_product
        pp = m.prom_product
        article = (sp.article or "").strip()
        if not article:
            # NP join key is the feed Артикул == sp.article; no article = no join.
            continue
        p = compute_match_pricing(m)
        priced.append({
            "article": article,
            "external_id": pp.external_id,
            "price_eur": p["price_eur"] if p else None,
            "retail_eur": (sp.price_cents or 0) / 100.0,
            "available": _is_available_for_offer(m),
            "currency": (sp.currency or "EUR") if sp.currency in ("EUR", "UAH") else "EUR",
        })
    return priced


def build_np_file(selected_brands, feed_path: str) -> tuple[bytes, dict]:
    """Build the NP Horoshop import file for the selected brands.

    Args:
        selected_brands: brand labels to include (case-insensitive). Empty =
            every matched NP article.
        feed_path: local path to a downloaded NP dealer-export xlsx. Fetching
            the live feed is the caller's job (keeps this testable, no network).

    Returns:
        (xlsx_bytes, manifest). manifest also carries parse_errors and
        matches_considered for the UI / operator.
    """
    content, parse_errors = parse_np_feed(feed_path)

    supplier = db.session.execute(
        select(Supplier).where(Supplier.slug == NP_SUPPLIER_SLUG)
    ).scalar_one_or_none()
    if supplier is None:
        return _workbook_bytes([]), {
            "error": f"NP supplier (slug={NP_SUPPLIER_SLUG!r}) not found",
            "parse_errors": parse_errors,
            "total": 0,
        }

    priced = _query_np_priced(supplier.id)
    rows, manifest = _shape_rows(content, priced, selected_brands)
    manifest["parse_errors"] = parse_errors
    manifest["matches_considered"] = len(priced)

    logger.info(
        "NP file: %d rows (%d with photo, %d no-photo), %d matched-no-feed, "
        "%d skipped-no-price, %d unmatched, %d parse warnings",
        manifest["total"], manifest["with_photo"], manifest["no_photo"],
        manifest["missing_feed_row"], manifest["skipped_no_price"],
        manifest["unmatched"], len(parse_errors),
    )
    return _workbook_bytes(rows), manifest
