"""«Новый проект» (NP) native [КАТАЛОГ] feed parser — Channel-2 content.

The NP dealer export (np.com.ua ``dealer-export?...&platform=horoshop``) is a
24-column workbook in Horoshop's own [КАТАЛОГ] schema. Unlike the matcher YML
feeds (Channel 1: price + availability only — see FINAL-MODEL.md §1), this feed
carries the *content* for NP-exclusive brands: localized names (UA/RU),
localized bodies (UA/RU), brand, and a photo gallery.

This module is the single, tested reader of that feed. Two entry points:

  * ``parse_np_feed(path, supplier_id)`` — pure read; returns content dicts +
    warnings. Consumed by the mass Excel builder (Channel-2 delivery) and by
    ``enrich_sp_bodies``.
  * ``enrich_sp_bodies(rows)`` — narrow persistence: enriches *existing*
    SupplierProduct rows (matched by ``(supplier_id, article)``) with the four
    body/photo fields, preserve-on-empty. It deliberately does NOT use
    ``feed_parser.save_supplier_products`` (which requires name/price on INSERT
    and keys on external_id) so it can never create duplicates or regress other
    suppliers — it only touches NP rows the normal sync already created.

Verified sheet shape (np-feed.xlsx, 690 data rows, 2026-05-18):

  col B  ``Артикул``         → article  (anchor == SupplierProduct.article, sup 2)
  col D  ``[КАТАЛОГ] Фото``  → image_url (1st) + images (JSON of ';'-split URLs)
  col G  ``title_uk``        → name      (UA)
  col H  ``description_uk``  → description    (UA body, <br> kept verbatim)
  col J  ``attr_brend_uk``   → brand     (country suffix stripped)
  col P  ``title_ru``        → name_ru   (RU)
  col Q  ``description_ru``  → description_ru (RU body, <br> kept verbatim)

Columns are located by header NAME (not fixed index) so a future column
reshuffle in the export doesn't silently shift fields.

Invariants:
  - article is the only stable key; a row without one is skipped → warning.
  - price / availability are NOT read here — they flow through the existing
    excel_parser path (Channel 1). Channel 2 never quotes a price.
  - empty content from the feed never overwrites stored content (a partial or
    broken export must not wipe data) — same semantics as
    feed_parser.save_supplier_products.
"""

from __future__ import annotations

import json
import logging
import re

import openpyxl

from app.extensions import db
from app.models.supplier_product import SupplierProduct
from sqlalchemy import select

logger = logging.getLogger(__name__)

# Header → internal key. Located by exact native header string.
_HEADER_MAP = {
    "Артикул": "article",
    "title_uk": "name",
    "description_uk": "description",
    "attr_brend_uk": "brand",
    "title_ru": "name_ru",
    "description_ru": "description_ru",
}
# The photo column header carries the "[КАТАЛОГ] " prefix; match by suffix so we
# don't hardcode the (cyrillic, space-sensitive) prefix.
_PHOTO_HEADER_SUFFIX = "Фото"

_COUNTRY_SUFFIX_RE = re.compile(r"\s*\([^)]+\)\s*$")


def _strip_country_suffix(text: str) -> str:
    """"HURAKAN (Китай)" → "HURAKAN". Idempotent on already-clean labels."""
    return _COUNTRY_SUFFIX_RE.sub("", text).strip()


def _clean(value) -> str:
    """Coerce a cell to a trimmed string; None / non-str → ''."""
    if value is None:
        return ""
    return str(value).strip()


def _split_gallery(value) -> list[str]:
    """Split a ';'-separated photo cell into a trimmed, de-duplicated URL list.

    Preserves order (main photo first). Drops empties; keeps first occurrence
    of each URL.
    """
    raw = _clean(value)
    if not raw:
        return []
    urls: list[str] = []
    seen: set[str] = set()
    for part in raw.split(";"):
        u = part.strip()
        if u and u not in seen:
            seen.add(u)
            urls.append(u)
    return urls


def _resolve_columns(headers: list) -> tuple[dict[str, int], int | None]:
    """Map internal keys → column index from the header row.

    Returns ``(col_index_by_key, photo_idx)``. Missing keys simply absent from
    the dict (caller decides what's required).
    """
    col: dict[str, int] = {}
    photo_idx: int | None = None
    for idx, h in enumerate(headers):
        name = _clean(h)
        if name in _HEADER_MAP:
            col[_HEADER_MAP[name]] = idx
        elif name.endswith(_PHOTO_HEADER_SUFFIX) and name.startswith("["):
            # "[КАТАЛОГ] Фото"
            photo_idx = idx
    return col, photo_idx


def parse_np_feed(file_path: str, supplier_id: int) -> tuple[list[dict], list[str]]:
    """Parse an NP dealer-export xlsx into content dicts + warnings.

    Args:
        file_path: path to the downloaded native [КАТАЛОГ] xlsx.
        supplier_id: NP supplier row id (2) to stamp on each dict.

    Returns:
        ``(rows, errors)`` — each row dict:
            {supplier_id, article, brand, name, name_ru,
             description, description_ru, image_url, images}
        ``images`` is a JSON-encoded list (or None when no photos).
        ``errors`` collects human-readable warnings (missing article, dup).
    """
    wb = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
    ws = wb[wb.sheetnames[0]]

    rows: list[dict] = []
    errors: list[str] = []
    seen_articles: set[str] = set()

    iterator = ws.iter_rows(values_only=True)
    try:
        header_row = list(next(iterator))
    except StopIteration:
        wb.close()
        return [], ["empty workbook (no header row)"]

    col, photo_idx = _resolve_columns(header_row)
    if "article" not in col:
        wb.close()
        return [], [f"no 'Артикул' column found in header {header_row!r}"]

    def cell(row, key):
        i = col.get(key)
        if i is None or i >= len(row):
            return None
        return row[i]

    for row_idx, row in enumerate(iterator, start=2):  # 1-based, +header
        article = _clean(cell(row, "article"))
        if not article:
            # Skip blank trailing rows silently; warn only if the row has content.
            if any(_clean(c) for c in row):
                errors.append(f"Row {row_idx}: missing Артикул, skipped")
            continue
        if article in seen_articles:
            errors.append(f"Row {row_idx}: duplicate Артикул {article!r}, skipped")
            continue
        seen_articles.add(article)

        gallery = (
            _split_gallery(row[photo_idx])
            if photo_idx is not None and photo_idx < len(row)
            else []
        )
        brand = _strip_country_suffix(_clean(cell(row, "brand")))

        rows.append({
            "supplier_id": supplier_id,
            "article": article,
            "brand": brand or None,
            "name": _clean(cell(row, "name")) or None,
            "name_ru": _clean(cell(row, "name_ru")) or None,
            "description": _clean(cell(row, "description")) or None,
            "description_ru": _clean(cell(row, "description_ru")) or None,
            "image_url": gallery[0] if gallery else None,
            "images": json.dumps(gallery) if gallery else None,
        })

    wb.close()
    logger.info(
        "NP parser: %d content rows parsed, %d warnings", len(rows), len(errors)
    )
    return rows, errors


def enrich_sp_bodies(rows: list[dict]) -> dict:
    """Persist NP body/photo content onto existing SupplierProduct rows.

    Matches an existing sp by ``(supplier_id, article)`` — NP's stable anchor —
    and writes ONLY the four content fields, preserve-on-empty. Never inserts:
    a feed article with no existing sp (unmatched tail the normal sync hasn't
    created) is reported in ``missing`` for later triage, not created here.

    Idempotent: re-running on an unchanged feed produces zero writes.

    Returns ``{"updated": N, "unchanged": N, "missing": [articles...]}``.
    """
    updated = 0
    unchanged = 0
    missing: list[str] = []

    for r in rows:
        sp = db.session.execute(
            select(SupplierProduct).where(
                SupplierProduct.supplier_id == r["supplier_id"],
                SupplierProduct.article == r["article"],
            )
        ).scalars().first()

        if sp is None:
            missing.append(r["article"])
            continue

        changed = False
        # preserve-on-empty: a missing feed value never wipes stored content.
        if r.get("description") and sp.description != r["description"]:
            sp.description = r["description"]
            changed = True
        if r.get("description_ru") and sp.description_ru != r["description_ru"]:
            sp.description_ru = r["description_ru"]
            changed = True
        if r.get("image_url") and sp.image_url != r["image_url"]:
            sp.image_url = r["image_url"]
            changed = True
        if r.get("images") and sp.images != r["images"]:
            sp.images = r["images"]
            changed = True

        if changed:
            updated += 1
        else:
            unchanged += 1

    if updated:
        db.session.commit()
    else:
        # Nothing dirtied; keep the session clean for callers.
        db.session.rollback()

    logger.info(
        "NP enrich: %d updated, %d unchanged, %d missing sp",
        updated, unchanged, len(missing),
    )
    return {"updated": updated, "unchanged": unchanged, "missing": missing}
