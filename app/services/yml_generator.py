"""YML feed generators — main / per-supplier / custom selection / narrow feeds.

Queries confirmed ProductMatch records, applies pricing via the pricing engine,
and writes atomic YML files for Horoshop import. Five flavors:
  - regenerate_yml_feed: full catalog, all suppliers (= regenerate_all_feed)
  - regenerate_supplier_feed(supplier_id): same content but only one supplier
  - regenerate_custom_feed(match_ids): arbitrary selection, deterministic token URL
  - sync_prices: narrow feed, only price (kept for CLI; UI button removed in K.4)
  - sync_availability: narrow feed, only availability attribute (same)

Per-supplier and custom feeds use the SAME offer shape as the main feed
(name, vendorCode, price, available, description) — Horoshop import config
chooses what to update. Only the main feed touches the in_feed flag.
"""

import hashlib
import json
import logging
import os
import tempfile
from datetime import datetime, timezone

from flask import current_app
from lxml import etree
from sqlalchemy import select, true
from sqlalchemy.orm import joinedload, selectinload

from app.extensions import db
from app.models.catalog import PromProduct  # noqa: F401 — needed for joinedload
from app.models.custom_feed import CustomFeed
from app.models.product_match import ProductMatch
from app.models.supplier import Supplier
from app.models.supplier_product import SupplierProduct
from app.services.pricing import (
    calculate_price_eur,
    clamp_discount_for_min_margin,
    is_valid_price,
    resolve_discount_percent,
)

logger = logging.getLogger(__name__)


def _query_published_matches(
    match_ids: list[int] | None = None,
    supplier_ids: list[int] | None = None,
):
    """Fetch confirmed/manual published matches with sp/pp/supplier eager-loaded.

    Filters are AND-combined when both are provided.
    """
    stmt = (
        select(ProductMatch)
        .where(
            ProductMatch.status.in_(["confirmed", "manual"]),
            ProductMatch.published.is_(True),
        )
        .options(
            joinedload(ProductMatch.supplier_product)
            .joinedload(SupplierProduct.supplier)
            .selectinload(Supplier.brand_discounts),
            joinedload(ProductMatch.prom_product),
        )
    )
    if match_ids:
        stmt = stmt.where(ProductMatch.id.in_(match_ids))
    if supplier_ids:
        stmt = stmt.join(
            SupplierProduct, ProductMatch.supplier_product_id == SupplierProduct.id
        ).where(SupplierProduct.supplier_id.in_(supplier_ids))
    return db.session.execute(stmt).scalars().unique().all()


def custom_feed_token(match_ids: list[int]) -> str:
    """Deterministic 12-hex-char token from a sorted unique set of match ids."""
    canonical = ",".join(str(i) for i in sorted(set(int(x) for x in match_ids)))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:12]


def _build_offer_xml(parent_el, match) -> bool:
    """Append a <offer> element to parent_el for match. Returns is_available."""
    sp = match.supplier_product
    pp = match.prom_product
    is_available = _is_available_for_offer(match)
    price_eur = _compute_price_eur(match)
    retail_eur = (sp.price_cents or 0) / 100.0

    avail_str = "true" if is_available else "false"
    offer = etree.SubElement(
        parent_el,
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
    # <oldprice> = supplier retail when we applied a real discount.
    # Horoshop then calculates the % from (oldprice - price) and ignores
    # its own "Знижка %" product-card field, preventing double-discount.
    if retail_eur > price_eur + 0.05:
        etree.SubElement(offer, "oldprice").text = f"{retail_eur:.1f}"
    etree.SubElement(offer, "currencyId").text = "EUR"
    etree.SubElement(offer, "vendorCode").text = str(pp.external_id)

    if pp.description_ua:
        desc_el = etree.SubElement(offer, "description")
        desc_el.text = etree.CDATA(pp.description_ua)
    if pp.description_ru:
        desc_ru_el = etree.SubElement(offer, "description_ru")
        desc_ru_el.text = etree.CDATA(pp.description_ru)
    return is_available


def _generate_feed(
    filename: str,
    supplier_ids: list[int] | None = None,
    match_ids: list[int] | None = None,
    update_in_feed: bool = False,
) -> dict:
    """Shared feed builder. Returns stats dict.

    update_in_feed=True is reserved for the main all-suppliers feed: it sets
    in_feed=True on included matches and False on the rest. Per-supplier and
    custom feeds never touch in_feed (multi-file ambiguity).
    """
    matches = _query_published_matches(
        match_ids=match_ids, supplier_ids=supplier_ids
    )
    included_ids = {m.id for m in matches}

    root, offers_el = _shop_skeleton()
    available_count = 0
    unavailable_count = 0
    for match in matches:
        is_avail = _build_offer_xml(offers_el, match)
        if is_avail:
            available_count += 1
        else:
            unavailable_count += 1

    yml_dir = current_app.config["YML_OUTPUT_DIR"]
    output_path = _write_xml_atomic(root, yml_dir, filename)

    if update_in_feed:
        if included_ids:
            db.session.query(ProductMatch).filter(
                ProductMatch.id.in_(included_ids)
            ).update({"in_feed": True}, synchronize_session=False)
        db.session.query(ProductMatch).filter(
            ~ProductMatch.id.in_(included_ids) if included_ids else true()
        ).update({"in_feed": False}, synchronize_session=False)
        db.session.commit()

    total = available_count + unavailable_count
    logger.info(
        "Feed %s: %d offers (%d available, %d unavailable)",
        filename, total, available_count, unavailable_count,
    )
    return {
        "total": total,
        "available": available_count,
        "unavailable": unavailable_count,
        "path": output_path,
        "filename": filename,
    }


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
    """Apply effective discount to supplier price, mirror full-feed logic.

    When supplier.min_margin_uah > 0 AND there is no per-match override, the
    base discount (per_brand / flat) is clamped DOWN so UAH margin stays at
    or above min_margin_uah. A per-match override bypasses the clamp —
    operator intent wins.
    """
    sp = match.supplier_product
    supplier = sp.supplier
    if not is_valid_price(sp.price_cents):
        return 0.0
    effective_discount = resolve_discount_percent(
        match.discount_percent, supplier, sp.brand
    )
    if match.discount_percent is None and supplier is not None:
        min_margin = float(getattr(supplier, "min_margin_uah", 0.0) or 0.0)
        if min_margin > 0:
            effective_discount = clamp_discount_for_min_margin(
                effective_discount,
                sp.price_cents,
                float(getattr(supplier, "eur_rate_uah", 51.15) or 51.15),
                min_margin,
                float(getattr(supplier, "cost_rate", 0.75) or 0.75),
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
    """Main feed: all suppliers, all confirmed published matches.

    This is the only feed that updates the in_feed column on ProductMatch.
    Per-supplier and custom feeds intentionally do not — multi-file ambiguity.
    """
    return _generate_feed(
        filename=current_app.config["YML_FILENAME"],
        update_in_feed=True,
    )


def regenerate_supplier_feed(supplier_id: int) -> dict:
    """Per-supplier feed at labresta-feed-<slug>.yml.

    Same offer shape as the main feed; only restricts query by supplier_id.
    """
    supplier = db.session.get(Supplier, supplier_id)
    if supplier is None:
        raise ValueError(f"Supplier id={supplier_id} not found")
    filename = f"labresta-feed-{supplier.slug}.yml"
    result = _generate_feed(
        filename=filename,
        supplier_ids=[supplier_id],
    )
    result["supplier_slug"] = supplier.slug
    return result


def regenerate_custom_feed(
    match_ids: list[int],
    name: str | None = None,
) -> dict:
    """Custom selection feed at labresta-feed-custom-<token>.yml.

    Token is sha256(sorted match_ids)[:12] — same selection always resolves
    to the same URL. Persists/updates a CustomFeed registry row so
    /feeds/custom can list and delete tokens.
    """
    if not match_ids:
        raise ValueError("regenerate_custom_feed requires non-empty match_ids")
    token = custom_feed_token(match_ids)
    filename = f"labresta-feed-custom-{token}.yml"
    result = _generate_feed(filename=filename, match_ids=match_ids)

    cf = db.session.execute(
        select(CustomFeed).where(CustomFeed.token == token)
    ).scalar_one_or_none()
    if cf is None:
        cf = CustomFeed(token=token, filename=filename, name=name)
        cf.match_ids = match_ids
        db.session.add(cf)
    else:
        cf.match_ids = match_ids
        cf.filename = filename
        if name is not None:
            cf.name = name
    db.session.commit()

    result["token"] = token
    return result


def delete_custom_feed(token: str) -> bool:
    """Remove a CustomFeed row and its YML file. Returns True if anything deleted."""
    cf = db.session.execute(
        select(CustomFeed).where(CustomFeed.token == token)
    ).scalar_one_or_none()
    if cf is None:
        return False
    yml_dir = current_app.config["YML_OUTPUT_DIR"]
    file_path = os.path.join(yml_dir, cf.filename)
    try:
        os.unlink(file_path)
    except FileNotFoundError:
        pass
    except OSError as e:
        logger.warning("Failed to remove %s: %s", file_path, e)
    db.session.delete(cf)
    db.session.commit()
    return True


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
