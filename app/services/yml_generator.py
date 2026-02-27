"""YML feed generator — builds Yandex Market Language XML from confirmed matches.

Queries confirmed ProductMatch records, applies pricing via the pricing engine,
and writes an atomic YML file for prom.ua import.
"""

import logging
import os
import tempfile
from datetime import datetime, timezone

from flask import current_app
from lxml import etree
from sqlalchemy import select
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


def regenerate_yml_feed() -> dict:
    """Generate YML feed from all confirmed matches and write atomically.

    Returns:
        Dict with stats: total, available, unavailable, path.
    """
    # Query confirmed matches with all related data
    stmt = (
        select(ProductMatch)
        .where(ProductMatch.status == "confirmed")
        .options(
            joinedload(ProductMatch.supplier_product).joinedload(
                SupplierProduct.supplier
            ),
            joinedload(ProductMatch.prom_product),
        )
    )
    matches = db.session.execute(stmt).scalars().unique().all()

    # Build YML XML
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
    root = etree.Element("yml_catalog", date=now)
    shop = etree.SubElement(root, "shop")

    etree.SubElement(shop, "name").text = "LabResta"
    etree.SubElement(shop, "company").text = "LabResta"
    etree.SubElement(shop, "url").text = "https://labresta.com"

    currencies = etree.SubElement(shop, "currencies")
    etree.SubElement(currencies, "currency", id="EUR", rate="1")

    offers_el = etree.SubElement(shop, "offers")

    available_count = 0
    unavailable_count = 0

    for match in matches:
        sp = match.supplier_product
        pp = match.prom_product
        supplier = sp.supplier

        # Determine availability
        price_valid = is_valid_price(sp.price_cents)
        is_available = price_valid and sp.available and not sp.needs_review

        # Calculate price
        effective_discount = get_effective_discount(
            match.discount_percent, supplier.discount_percent
        )
        if price_valid:
            price_eur = calculate_price_eur(sp.price_cents, effective_discount)
        else:
            price_eur = 0

        avail_str = "true" if is_available else "false"
        offer = etree.SubElement(
            offers_el,
            "offer",
            id=str(pp.external_id),
            available=avail_str,
        )
        etree.SubElement(offer, "name").text = pp.name
        etree.SubElement(offer, "price").text = str(price_eur)
        etree.SubElement(offer, "currencyId").text = "EUR"

        # Only include vendorCode if article is present
        if sp.article:
            etree.SubElement(offer, "vendorCode").text = sp.article

        if is_available:
            available_count += 1
        else:
            unavailable_count += 1

    total = available_count + unavailable_count

    # Atomic file write
    yml_dir = current_app.config["YML_OUTPUT_DIR"]
    yml_filename = current_app.config["YML_FILENAME"]
    output_path = os.path.join(yml_dir, yml_filename)

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
        # Clean up temp file on failure
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise

    logger.info(
        "YML feed generated: %d offers (%d available, %d unavailable) -> %s",
        total,
        available_count,
        unavailable_count,
        output_path,
    )

    return {
        "total": total,
        "available": available_count,
        "unavailable": unavailable_count,
        "path": output_path,
    }
