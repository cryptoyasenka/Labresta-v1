"""Horoshop create-file builder — add unmatched supplier products as new cards.

Produces the native-schema Horoshop XLSX an operator imports by hand under
"New products: Import" to CREATE catalog cards for supplier products that have
NO confirmed/manual match. This is the NP builder pattern (np_horoshop_file.py)
PLUS the columns the update-files deliberately OMIT, because a create needs
them: name UA/RU, brand, a category (`[КАТАЛОГ] Раздел`), and visibility
(`[КАТАЛОГ] Отображать`="1").

Why a native XLSX *file* and not a YML feed (same reasoning as the NP builder):
Horoshop's YML parser drops <description_ru> and cross-maps <name> UA→RU. The
native dealer-export schema auto-maps a column → catalog field ONLY when the
header equals the field's qualified name ("[КАТАЛОГ] <leaf>", or a bare
top-level name like "Артикул"). The header strings below are copied verbatim
from the live-proven canary — they are NOT retyped from memory.

Two create-file facts proven in research:
  - RESEARCH Q1: the category column MUST be "[КАТАЛОГ] Раздел". A
    "categories_uk" column auto-maps to "do not import" and silently drops the
    category — never use it.
  - RESEARCH Q2: an empty "[КАТАЛОГ] Отображать" hides the created card, so
    every emitted row sets it to "1". Horoshop also won't create a missing
    category, so a row with no Раздел errors the import — such rows are skipped
    and reported (the fallback resolver guarantees a category in normal flow).

Category resolution is delegated to app.services.category_resolver. The CORE
ships a fallback-only resolver (every card → one holding category) so the file
is importable on its own; plan 09-02 swaps in a smart chain behind the same
interface.

Read-only w.r.t. the DB: it queries products/pricing and writes NOTHING. The
live import stays Yana's hand (invariant #13).
"""

from __future__ import annotations

import io
import json
import logging

import openpyxl
from sqlalchemy import exists, select
from sqlalchemy.orm import selectinload

from app.extensions import db
from app.models.product_match import ProductMatch
from app.models.supplier import Supplier
from app.models.supplier_product import SupplierProduct
from app.services.category_export import read_category_corpus
from app.services.category_resolver import build_resolver
from app.services.np_parser import parse_np_feed
from app.services.pricing import (
    calculate_auto_discount,
    calculate_price_eur,
    clamp_discount_for_min_margin,
    resolve_discount_percent,
    resolve_eur_rate,
)

logger = logging.getLogger(__name__)

# Native auto-mapping headers. Prefix "[КАТАЛОГ] " + leaf == the catalog field's
# qualified name. Copied verbatim from the live-proven canary — do NOT retype.
_PREFIX = "[КАТАЛОГ] "
H_ARTICLE = "Артикул"                       # top-level field → bare name, CREATE KEY
H_NAME_UA = _PREFIX + "Название (UA)"
H_NAME_RU = _PREFIX + "Название (RU)"
H_BRAND = _PREFIX + "Бренд"
H_CATEGORY = _PREFIX + "Раздел"             # SINGLE switchable category constant (RESEARCH Q1)
H_PRICE = _PREFIX + "Цена"
H_OLDPRICE = _PREFIX + "Старая цена"
H_CURRENCY = _PREFIX + "Валюта"
H_AVAIL = _PREFIX + "Наличие"
H_VISIBLE = _PREFIX + "Отображать"          # "1" or the card is hidden (RESEARCH Q2)
H_GALLERY = _PREFIX + "Галерея"
H_DESC_UA = _PREFIX + "Описание товара (UA)"
H_DESC_RU = _PREFIX + "Описание товара (RU)"

# Column order: article (key) first, then name UA/RU, brand, category, the
# price bearers, availability, visibility, gallery, description UA/RU.
HEADERS = [
    H_ARTICLE,
    H_NAME_UA, H_NAME_RU, H_BRAND, H_CATEGORY,
    H_PRICE, H_OLDPRICE, H_CURRENCY,
    H_AVAIL, H_VISIBLE, H_GALLERY,
    H_DESC_UA, H_DESC_RU,
]

_AVAIL_YES = "В наличии"
_AVAIL_NO = "Нет в наличии"
_VISIBLE_YES = "1"

_SHEET = "Worksheet"


def _norm(value) -> str:
    return (value or "").strip().lower()


def price_unmatched(sp) -> tuple[float | None, str]:
    """Sell price (EUR, tenths) + old-price string for an UNMATCHED product.

    There is no ProductMatch, so this uses the pure pricing primitives directly
    (no ``compute_match_pricing``). Mirrors ``resolve_effective_discount`` /
    ``compute_match_pricing`` semantics with ``match_discount=None``:

      - base discount from the supplier (per-brand override respected);
      - EUR rate forced to 1.0 for UAH-priced suppliers (so margin math stays in
        UAH end to end);
      - min-margin clamp applied when ``min_margin_uah > 0``;
      - auto_margin suppliers (MARESTO class, CLAUDE.md #12) derive the discount
        via ``calculate_auto_discount`` — ``resolve_discount_percent`` returns the
        supplier default for auto_margin by design (pricing.py:99).

    Returns ``(None, "")`` when the product has no usable retail price.
    """
    supplier = sp.supplier
    rate = resolve_eur_rate(supplier)
    if getattr(sp, "currency", "EUR") == "UAH":
        rate = 1.0  # keep the margin math in UAH

    mode = getattr(supplier, "pricing_mode", "flat") or "flat"
    cost_rate = float(getattr(supplier, "cost_rate", 0.75) or 0.75)
    min_margin = float(getattr(supplier, "min_margin_uah", 0.0) or 0.0)

    if mode == "auto_margin":
        # resolve_discount_percent would return the supplier default here, so
        # compute the margin-aware discount directly (CLAUDE.md #12).
        if not sp.price_cents:
            return None, ""
        eff_d = float(
            calculate_auto_discount(
                sp.price_cents, rate, cost_rate=cost_rate,
                min_margin_uah=min_margin if min_margin > 0 else 500.0,
            )
        )
    else:
        base_d = float(
            resolve_discount_percent(None, supplier, getattr(sp, "brand", None))
            or 0.0
        )
        eff_d = base_d
        if min_margin > 0 and sp.price_cents:
            eff_d = float(
                clamp_discount_for_min_margin(
                    base_d, sp.price_cents, rate, min_margin, cost_rate
                )
            )

    if not sp.price_cents:
        return None, ""

    sell = calculate_price_eur(sp.price_cents, eff_d)
    retail = (sp.price_cents or 0) / 100.0
    oldprice = f"{retail:.1f}" if retail > sell + 0.05 else ""
    return sell, oldprice


def _shape_rows(row_inputs: list[dict], selected_brands) -> tuple[list[dict], dict]:
    """Pure: shape priced/resolved row inputs into native-schema rows.

    Args:
        row_inputs: list of dicts {article, name, name_ru, brand, category,
            price_eur, retail_eur, currency, available, photos, description,
            description_ru}.
        selected_brands: brand labels the operator ticked (case-insensitive).
            Empty/falsy = no brand filter.

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
        "skipped_no_artikul": 0,
        "skipped_no_price": 0,
        "skipped_no_category": 0,
        "per_brand": {},
    }

    for ri in row_inputs:
        brand = ri.get("brand")
        if sel and _norm(brand) not in sel:
            continue

        article = (ri.get("article") or "").strip()
        if not article:
            manifest["skipped_no_artikul"] += 1
            continue

        price = ri.get("price_eur")
        if price is None or price <= 0:
            manifest["skipped_no_price"] += 1
            continue

        category = (ri.get("category") or "").strip()
        if not category:
            # Horoshop errors on a row with no Раздел (RESEARCH Q2).
            manifest["skipped_no_category"] += 1
            continue

        retail = ri.get("retail_eur")
        oldprice = (
            f"{retail:.1f}"
            if (retail is not None and retail > price + 0.05)
            else ""
        )
        photos = ri.get("photos") or []
        rows.append({
            H_ARTICLE: article,                       # KEY = supplier article
            H_NAME_UA: ri.get("name") or "",
            H_NAME_RU: ri.get("name_ru") or "",
            H_BRAND: brand or "",
            H_CATEGORY: category,
            H_PRICE: f"{price:.1f}",
            H_OLDPRICE: oldprice,
            H_CURRENCY: ri.get("currency") or "EUR",
            H_AVAIL: _AVAIL_YES if ri.get("available") else _AVAIL_NO,
            H_VISIBLE: _VISIBLE_YES,
            H_GALLERY: ";".join(photos),
            H_DESC_UA: ri.get("description") or "",
            H_DESC_RU: ri.get("description_ru") or "",
        })

        manifest["total"] += 1
        if photos:
            manifest["with_photo"] += 1
        else:
            manifest["no_photo"] += 1
        brand_label = brand or "(без бренда)"
        manifest["per_brand"][brand_label] = manifest["per_brand"].get(brand_label, 0) + 1

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


def _query_unmatched(supplier_id: int, selected_brands=None) -> list[tuple]:
    """DB → list of (sp, row_input) pairs for products with NO active match.

    Read-only. Uses a correlated NOT-EXISTS against confirmed/manual matches
    (RESEARCH Q7). ``published`` is deliberately NOT part of the predicate — a
    published=False confirmed match would otherwise read as "unmatched" and get
    re-created.

    Returns (sp, row_input) pairs so the category resolver in ``build_add_file``
    can see the live SP object (and 09-02's smart resolvers can inspect it). The
    ``row_input["category"]`` is left None here; the builder fills it.
    """
    linked = (
        select(ProductMatch.id)
        .where(
            ProductMatch.supplier_product_id == SupplierProduct.id,
            ProductMatch.status.in_(("confirmed", "manual")),
        )
        .correlate(SupplierProduct)
    )
    stmt = (
        select(SupplierProduct)
        .where(
            SupplierProduct.supplier_id == supplier_id,
            SupplierProduct.is_deleted.is_(False),
            SupplierProduct.ignored.is_(False),
            ~exists(linked),
        )
        .options(
            selectinload(SupplierProduct.supplier).selectinload(
                Supplier.brand_discounts
            )
        )
        .order_by(SupplierProduct.brand, SupplierProduct.name)
    )

    sel = {_norm(b) for b in (selected_brands or []) if _norm(b)}
    pairs: list[tuple] = []
    for sp in db.session.execute(stmt).scalars().all():
        if sel and _norm(sp.brand) not in sel:
            continue
        price_eur, _ = price_unmatched(sp)
        # photos: prefer the JSON images array, else the single main image
        # (mirror matches.py json.loads pattern).
        photos = (json.loads(sp.images) if sp.images else []) or (
            [sp.image_url] if sp.image_url else []
        )
        currency = (sp.currency or "EUR") if sp.currency in ("EUR", "UAH") else "EUR"
        row_input = {
            "article": (sp.article or "").strip(),
            "name": sp.name,
            "name_ru": None,
            "brand": sp.brand,
            "category": None,            # filled by the resolver in build_add_file
            "price_eur": price_eur,
            "retail_eur": (sp.price_cents or 0) / 100.0,
            "currency": currency,
            "available": sp.available,
            "photos": photos,
            "description": sp.description,
            "description_ru": None,
        }
        pairs.append((sp, row_input))
    return pairs


def _enrich_from_feed(row_input: dict, feed_row: dict | None) -> None:
    """Fill name/name_ru/category/description(_ru) on row_input from an NP feed.

    The DB value is the fallback when the feed lacks a field — NP carries NO RU
    in the matcher DB (and often no description either), so without this enrich
    NP create-cards would import with blank RU name/description, violating
    decision D2 (FLAG-1/MINOR-B). Brand and photos are left to the DB/existing
    logic; this only backfills the create-card text the DB doesn't hold for NP.
    """
    if not feed_row:
        return
    for field in ("name", "name_ru", "description", "description_ru"):
        # Feed wins when present; DB value (already in row_input) is the fallback.
        feed_val = feed_row.get(field)
        if feed_val and not (row_input.get(field) or "").strip():
            row_input[field] = feed_val
        elif feed_val and field in ("name_ru", "description_ru"):
            # NP DB never holds RU → always prefer the feed RU when it exists.
            row_input[field] = feed_val
    # `category` is consumed by the resolver's feed getter, not written directly
    # here (the resolver reconciles it to the store tree).


def build_add_file(
    supplier_id: int,
    selected_brands,
    export_path: str | None = None,
    *,
    resolver=None,
    np_feed_path: str | None = None,
) -> tuple[bytes, dict]:
    """Build the Horoshop create-file for a supplier's unmatched products.

    When an export and/or NP feed is provided this constructs the SMART resolver
    (feed → analogy → fallback, AI OFF — decision D3) instead of the fallback-
    only chain, and enriches NP rows (name/RU/description) from the feed. The
    output schema is unchanged — only category resolution and the create-card
    text get smarter.

    Args:
        supplier_id: the supplier whose unmatched products to emit.
        selected_brands: brand labels to include (case-insensitive). Empty =
            every unmatched product for the supplier.
        export_path: local path to a downloaded Horoshop export. When given, its
            «Раздел» corpus drives the analogy tier + the store-category label set.
        resolver: optional CategoryResolver override (mainly for tests). When
            None, the smart chain is built from the export/feed (degrades to
            analogy→fallback without a feed, fallback-only without an export).
        np_feed_path: optional NP feed path. When given, its parsed content
            supplies a per-article feed category (for the feed tier) AND enriches
            each NP row's name/name_ru/description(_ru) (FLAG-1/MINOR-B).

    Returns:
        (xlsx_bytes, manifest). manifest carries by_source = {feed, analogy,
        fallback, ai, none} counts so the operator/audit sees how each card's
        category was assigned.
    """
    pairs = _query_unmatched(supplier_id, selected_brands)

    # Category corpus from the uploaded export (the Раздел catalog_import drops).
    corpus: list[dict] = []
    if export_path:
        corpus, corpus_errs = read_category_corpus(export_path)
        if corpus_errs:
            logger.warning("Category export issues: %s", corpus_errs)

    # NP feed content → per-article enrichment map (name/RU/desc) + a category
    # getter for the feed tier. Keyed by stripped article == sp.article.
    feed_by_article: dict[str, dict] = {}
    if np_feed_path:
        feed_content, feed_errs = parse_np_feed(np_feed_path)
        if feed_errs:
            logger.info("NP feed parse warnings: %d", len(feed_errs))
        feed_by_article = {
            (art or "").strip(): row for art, row in feed_content.items()
        }

    def _feed_category_getter(sp):
        fr = feed_by_article.get((getattr(sp, "article", None) or "").strip())
        return fr.get("category") if fr else None

    if resolver is None:
        if corpus or feed_by_article:
            # SMART chain. Feed tier only engages when a feed is present; AI off.
            resolver = build_resolver(
                corpus,
                strategies=("feed", "analogy", "fallback"),
                feed_category_getter=(
                    _feed_category_getter if feed_by_article else None
                ),
                ai_enabled=False,
            )
        else:
            # No export, no feed: fallback-only (still a valid importable file).
            resolver = build_resolver(export_rows=[], strategies=("fallback",))

    by_source = {"feed": 0, "analogy": 0, "fallback": 0, "ai": 0, "none": 0}
    row_inputs: list[dict] = []
    for sp, row_input in pairs:
        # FLAG-1/MINOR-B: backfill the create-card text NP's DB lacks (name UA/RU,
        # description UA/RU) from the feed BEFORE shaping the row.
        _enrich_from_feed(row_input, feed_by_article.get(row_input.get("article", "")))
        res = resolver.resolve(sp, brand=row_input["brand"])
        row_input["category"] = res.category
        by_source[res.source] = by_source.get(res.source, 0) + 1
        row_inputs.append(row_input)

    rows, manifest = _shape_rows(row_inputs, selected_brands)
    manifest["export_path"] = export_path
    manifest["np_feed_path"] = np_feed_path
    manifest["candidates"] = len(pairs)
    manifest["by_source"] = by_source

    logger.info(
        "Add-file: %d rows (%d with photo, %d no-photo), %d skipped-no-artikul, "
        "%d skipped-no-price, %d skipped-no-category, from %d unmatched candidates; "
        "by_source=%s",
        manifest["total"], manifest["with_photo"], manifest["no_photo"],
        manifest["skipped_no_artikul"], manifest["skipped_no_price"],
        manifest["skipped_no_category"], len(pairs), by_source,
    )
    return _workbook_bytes(rows), manifest
