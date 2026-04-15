"""YML feed generators — full feed plus narrow price/availability feeds.

Queries confirmed ProductMatch records, applies pricing via the pricing engine,
and writes atomic YML files for Horoshop import. Three flavors:
  - regenerate_yml_feed: full catalog (price + availability + description + name)
  - sync_prices: narrow feed, only price (Horoshop config ignores other fields)
  - sync_availability: narrow feed, only availability attribute

Narrow feeds let operator push just prices or just stock without re-importing
description/name, which matters when Horoshop catalog edits should survive.
"""

import logging
import os
import tempfile
from datetime import datetime, timezone

from flask import current_app
from lxml import etree
from sqlalchemy import select, true
from sqlalchemy.orm import joinedload

from app.extensions import db
from app.models.catalog import PromProduct  # noqa: F401 — needed for joinedload
from app.models.product_match import ProductMatch
from app.models.supplier import Supplier  # noqa: F401 — needed for joinedload
from app.models.supplier_product import SupplierProduct  # noqa: F401 — needed for joinedload
from app.services.pricing import (
    calculate_price_eur,
    get_effective_discount,
    is_valid_price,
)

logger = logging.getLogger(__name__)


def _query_published_matches(match_ids: list[int] | None = None):
    """Fetch confirmed/manual matches with related sp/pp/supplier, published=True.

    If match_ids provided, restrict to those ids (for per-row sync).
    """
    stmt = (
        select(ProductMatch)
        .where(
            ProductMatch.status.in_(["confirmed", "manual"]),
            ProductMatch.published.is_(True),
        )
        .options(
            joinedload(ProductMatch.supplier_product).joinedload(
                SupplierProduct.supplier
            ),
            joinedload(ProductMatch.prom_product),
        )
    )
    if match_ids:
        stmt = stmt.where(ProductMatch.id.in_(match_ids))
    return db.session.execute(stmt).scalars().unique().all()


def _shop_skeleton():
    """Build <yml_catalog><shop>… skeleton, return (root, offers_el)."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
    root = etree.Element("yml_catalog", date=now)
    shop = etree.SubElement(root, "shop")
    etree.SubElement(shop, "name").text = "LabResta"
    etree.SubElement(shop, "company").text = "LabResta"
    etree.SubElement(shop, "url").text = "https://labresta.com"
    currencies = etree.SubElement(shop, "currencies")
    etree.SubElement(currencies, "currency", id="EUR", rate="1")
    offers_el = etree.SubElement(shop, "offers")
    return root, offers_el


def _is_available_for_offer(match) -> bool:
    """Match availability rule shared across full and narrow feeds."""
    sp = match.supplier_product
    return (
        is_valid_price(sp.price_cents)
        and sp.available
        and not sp.needs_review
    )


def _compute_price_eur(match) -> float:
    """Apply effective discount to supplier price, mirror full-feed logic."""
    sp = match.supplier_product
    supplier = sp.supplier
    if not is_valid_price(sp.price_cents):
        return 0.0
    effective_discount = get_effective_discount(
        match.discount_percent, supplier.discount_percent
    )
    return calculate_price_eur(sp.price_cents, effective_discount)


def _write_xml_atomic(root, yml_dir: str, filename: str) -> str:
    """Atomic write of the XML tree; return absolute output path."""
    output_path = os.path.join(yml_dir, filename)
    os.makedirs(yml_dir, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(suffix=".tmp", prefix="yml_", dir=yml_dir)
    try:
        tree = etree.ElementTree(root)
        with os.fdopen(fd, "wb") as f:
            tree.write(
                f,
                xml_declaration=True,
                encoding="UTF-8",
                pretty_print=True,
                doctype='<!DOCTYPE yml_catalog SYSTEM "shops.dtd">',
            )
        os.replace(tmp_path, output_path)
    except Exception:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise
    return output_path


def regenerate_yml_feed() -> dict:
    """Generate full YML feed from all confirmed matches and write atomically.

    Returns:
        Dict with stats: total, available, unavailable, path.
    """
    # published=False is a per-row unpublish toggle (phase C) — operator can
    # keep the match row in the DB but exclude it from the feed.
    matches = _query_published_matches()
    included_match_ids = {m.id for m in matches}

    root, offers_el = _shop_skeleton()
    available_count = 0
    unavailable_count = 0

    for match in matches:
        sp = match.supplier_product
        pp = match.prom_product
        is_available = _is_available_for_offer(match)
        price_eur = _compute_price_eur(match)

        avail_str = "true" if is_available else "false"
        offer = etree.SubElement(
            offers_el,
            "offer",
            id=str(pp.external_id),
            available=avail_str,
        )
        etree.SubElement(offer, "name").text = pp.name
        if pp.name_ru:
            etree.SubElement(offer, "name_ru").text = pp.name_ru
        if pp.page_url:
            etree.SubElement(offer, "url").text = pp.page_url
        etree.SubElement(offer, "price").text = f"{price_eur:.1f}"
        etree.SubElement(offer, "currencyId").text = "EUR"

        # Horoshop matches existing products by artikul; its YML import can be
        # configured to read either `offer id=` or `<vendorCode>`. We populate
        # both with external_id (= Horoshop artikul) so either setting works.
        etree.SubElement(offer, "vendorCode").text = str(pp.external_id)

        # Description — wrap in CDATA so HTML markup in the body survives.
        # Horoshop import reads <description> and updates the catalog entry's
        # description when "обновлять существующие" is enabled. Write UA and RU
        # as separate tags (<description> = UA, <description_ru> = RU) mirroring
        # the name / name_ru convention above.
        if pp.description_ua:
            desc_el = etree.SubElement(offer, "description")
            desc_el.text = etree.CDATA(pp.description_ua)
        if pp.description_ru:
            desc_ru_el = etree.SubElement(offer, "description_ru")
            desc_ru_el.text = etree.CDATA(pp.description_ru)

        if is_available:
            available_count += 1
        else:
            unavailable_count += 1

    total = available_count + unavailable_count

    yml_dir = current_app.config["YML_OUTPUT_DIR"]
    output_path = _write_xml_atomic(
        root, yml_dir, current_app.config["YML_FILENAME"]
    )

    # Mark in_feed flag: True for included matches, False for the rest.
    # One bulk UPDATE per side — avoid per-row session.add.
    if included_match_ids:
        db.session.query(ProductMatch).filter(
            ProductMatch.id.in_(included_match_ids)
        ).update({"in_feed": True}, synchronize_session=False)
    db.session.query(ProductMatch).filter(
        ~ProductMatch.id.in_(included_match_ids) if included_match_ids else true()
    ).update({"in_feed": False}, synchronize_session=False)
    db.session.commit()

    logger.info(
        "YML feed generated: %d offers (%d available, %d unavailable) -> %s",
        total, available_count, unavailable_count, output_path,
    )

    return {
        "total": total,
        "available": available_count,
        "unavailable": unavailable_count,
        "path": output_path,
    }


def sync_prices(match_ids: list[int] | None = None) -> dict:
    """Generate a narrow YML containing only price data; bump price_synced_at.

    Narrow feed structure per offer: id + vendorCode + price + currencyId.
    `available` attribute is still set (offer tag requires it) but Horoshop-side
    import settings should be configured to only update prices from this feed.

    Args:
        match_ids: Optional subset — if provided, only these matches are synced.
            None = sync all published confirmed/manual matches (bulk).

    Returns:
        Dict with stats: total, skipped (no valid price), path, synced_at.
    """
    matches = _query_published_matches(match_ids)
    root, offers_el = _shop_skeleton()

    synced_ids: list[int] = []
    skipped = 0

    for match in matches:
        pp = match.prom_product
        if not is_valid_price(match.supplier_product.price_cents):
            skipped += 1
            continue
        is_available = _is_available_for_offer(match)
        price_eur = _compute_price_eur(match)

        offer = etree.SubElement(
            offers_el,
            "offer",
            id=str(pp.external_id),
            available="true" if is_available else "false",
        )
        etree.SubElement(offer, "vendorCode").text = str(pp.external_id)
        etree.SubElement(offer, "price").text = f"{price_eur:.1f}"
        etree.SubElement(offer, "currencyId").text = "EUR"
        synced_ids.append(match.id)

    yml_dir = current_app.config["YML_OUTPUT_DIR"]
    output_path = _write_xml_atomic(
        root, yml_dir, current_app.config["YML_PRICES_FILENAME"]
    )

    now_utc = datetime.now(timezone.utc)
    if synced_ids:
        db.session.query(ProductMatch).filter(
            ProductMatch.id.in_(synced_ids)
        ).update({"price_synced_at": now_utc}, synchronize_session=False)
        db.session.commit()

    logger.info(
        "Prices sync: %d offers, %d skipped (invalid price) -> %s",
        len(synced_ids), skipped, output_path,
    )

    return {
        "total": len(synced_ids),
        "skipped": skipped,
        "path": output_path,
        "synced_at": now_utc.isoformat(),
    }


def sync_availability(match_ids: list[int] | None = None) -> dict:
    """Generate a narrow YML containing only availability; bump availability_synced_at.

    Narrow feed structure per offer: id + vendorCode + available attribute.
    Horoshop-side import settings should be configured to only update stock
    status from this feed.

    Args:
        match_ids: Optional subset — if provided, only these matches are synced.

    Returns:
        Dict with stats: total, available, unavailable, path, synced_at.
    """
    matches = _query_published_matches(match_ids)
    root, offers_el = _shop_skeleton()

    synced_ids: list[int] = []
    available_count = 0
    unavailable_count = 0

    for match in matches:
        pp = match.prom_product
        is_available = _is_available_for_offer(match)

        offer = etree.SubElement(
            offers_el,
            "offer",
            id=str(pp.external_id),
            available="true" if is_available else "false",
        )
        etree.SubElement(offer, "vendorCode").text = str(pp.external_id)
        synced_ids.append(match.id)
        if is_available:
            available_count += 1
        else:
            unavailable_count += 1

    yml_dir = current_app.config["YML_OUTPUT_DIR"]
    output_path = _write_xml_atomic(
        root, yml_dir, current_app.config["YML_AVAILABILITY_FILENAME"]
    )

    now_utc = datetime.now(timezone.utc)
    if synced_ids:
        db.session.query(ProductMatch).filter(
            ProductMatch.id.in_(synced_ids)
        ).update({"availability_synced_at": now_utc}, synchronize_session=False)
        db.session.commit()

    logger.info(
        "Availability sync: %d offers (%d available, %d unavailable) -> %s",
        len(synced_ids), available_count, unavailable_count, output_path,
    )

    return {
        "total": len(synced_ids),
        "available": available_count,
        "unavailable": unavailable_count,
        "path": output_path,
        "synced_at": now_utc.isoformat(),
    }
