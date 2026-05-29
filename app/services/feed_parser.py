"""YML/XML feed parser with encoding detection for supplier product feeds."""

import json
import logging
from datetime import datetime, timezone

import chardet
from lxml import etree
from sqlalchemy import func, select

from app.extensions import db
from app.models.supplier import Supplier
from app.models.supplier_product import SupplierProduct

logger = logging.getLogger(__name__)


def _brand_canon_cache() -> dict[str, str]:
    """Return lowercase → canonical brand mapping (most-common form wins)."""
    rows = db.session.execute(
        select(SupplierProduct.brand, func.count(SupplierProduct.id).label("cnt"))
        .where(SupplierProduct.brand.isnot(None), SupplierProduct.brand != "")
        .group_by(SupplierProduct.brand)
        .order_by(func.count(SupplierProduct.id).desc())
    ).all()
    cache: dict[str, str] = {}
    for brand, _cnt in rows:
        key = brand.strip().lower()
        if key not in cache:
            cache[key] = brand.strip()
    return cache


def canonicalize_brand(brand: str | None, cache: dict[str, str]) -> str | None:
    """Normalize brand string to canonical form from cache, or strip-only if unknown."""
    if not brand:
        return brand
    brand = brand.strip()
    if not brand:
        return None
    return cache.get(brand.lower(), brand)


def parse_supplier_feed(raw_bytes: bytes, supplier_id: int) -> list[dict]:
    """Parse a YML/XML supplier feed from raw bytes into product dicts.

    Encoding strategy (from Research Pattern 2):
      1. First try: etree.fromstring(raw_bytes) — lxml reads XML declaration encoding.
      2. Fallback: chardet.detect() to find encoding, then parse with explicit encoding.

    Args:
        raw_bytes: Raw XML bytes (never pre-decoded).
        supplier_id: ID of the supplier this feed belongs to.

    Returns:
        List of product dicts with keys: external_id, name, brand, model,
        article, price_cents, currency, available, supplier_id.
    """
    root = _parse_xml(raw_bytes)
    if root is None:
        logger.error("parse_supplier_feed: XML parser returned None — invalid or empty document")
        return []

    products = []
    for offer in root.iter("offer"):
        external_id = offer.get("id")
        if not external_id:
            continue

        available_str = offer.get("available", "true")
        available = available_str.lower() in ("true", "1", "yes")

        # MARESTO carries a 4-value <stock> (In stock / Running low / Reserved /
        # Out of stock) richer than the binary `available`; keep it for the
        # Horoshop «Наявність» status mapping (see services/maresto_stock.py).
        stock_status = _text(offer, "stock")

        name = _text(offer, "name")
        if not name:
            continue  # skip offers without a name

        price_str = _text(offer, "price")
        price_cents = None
        if price_str:
            try:
                price_cents = int(round(float(price_str) * 100))
            except (ValueError, TypeError):
                pass

        # Extract pictures
        pictures = [pic.text.strip() for pic in offer.findall("picture")
                    if pic.text and pic.text.strip()]
        image_url = pictures[0] if pictures else None

        # Extract description
        description = _text(offer, "description")

        # Extract params (characteristics)
        params = {}
        for param in offer.findall("param"):
            param_name = param.get("name")
            param_value = param.text.strip() if param.text else ""
            if param_name and param_value:
                params[param_name] = param_value

        products.append({
            "external_id": external_id,
            "name": name,
            "brand": _text(offer, "vendor"),
            "model": _text(offer, "model"),
            "article": _text(offer, "vendorCode"),
            "price_cents": price_cents,
            "currency": _text(offer, "currencyId") or "EUR",
            "available": available,
            "stock_status": stock_status,
            "supplier_id": supplier_id,
            "description": description,
            "image_url": image_url,
            "images": json.dumps(pictures) if pictures else None,
            "params": json.dumps(params, ensure_ascii=False) if params else None,
        })

    return products


def save_supplier_products(products: list[dict]) -> dict:
    """Upsert parsed products into the SupplierProduct table.

    Inserts new products or updates existing ones based on the unique
    constraint (supplier_id, external_id). Updates last_seen_at on all
    matched records.

    After save, updates Supplier.last_fetched_at and last_fetch_status.

    Args:
        products: List of product dicts from parse_supplier_feed().

    Returns:
        Dict with counts: {"created": N, "updated": N, "total": N}.
    """
    if not products:
        return {"created": 0, "updated": 0, "total": 0}

    supplier_id = products[0]["supplier_id"]
    now = datetime.now(timezone.utc)
    created = 0
    updated = 0

    # Normalize brands to canonical case before upserting
    canon = _brand_canon_cache()
    for p in products:
        p["brand"] = canonicalize_brand(p.get("brand"), canon)

    # Preload all existing rows for this supplier in ONE query, keyed by
    # external_id (unique within a supplier), instead of a SELECT per product.
    # A feed carries hundreds-to-thousands of offers, so the per-item lookup
    # was thousands of round-trips per sync.
    existing_by_ext = {
        row.external_id: row
        for row in db.session.execute(
            select(SupplierProduct).where(
                SupplierProduct.supplier_id == supplier_id
            )
        ).scalars().all()
    }

    try:
        for p in products:
            existing = existing_by_ext.get(p["external_id"])

            if existing:
                existing.name = p["name"]
                existing.brand = p["brand"]
                existing.model = p["model"]
                existing.article = p["article"]
                if not existing.price_forced:
                    existing.price_cents = p["price_cents"]
                    existing.currency = p["currency"]
                existing.available = p["available"]
                existing.stock_status = p.get("stock_status")
                existing.last_seen_at = now
                # Preserve existing optional fields when the feed omits them —
                # a partial/broken feed dropping a field should not wipe data.
                new_description = p.get("description")
                if new_description:
                    existing.description = new_description
                new_image_url = p.get("image_url")
                if new_image_url:
                    existing.image_url = new_image_url
                new_images = p.get("images")
                if new_images:
                    existing.images = new_images
                new_params = p.get("params")
                if new_params:
                    existing.params = new_params
                updated += 1
            else:
                new_product = SupplierProduct(
                    supplier_id=p["supplier_id"],
                    external_id=p["external_id"],
                    name=p["name"],
                    brand=p["brand"],
                    model=p["model"],
                    article=p["article"],
                    price_cents=p["price_cents"],
                    currency=p["currency"],
                    available=p["available"],
                    stock_status=p.get("stock_status"),
                    last_seen_at=now,
                    description=p.get("description"),
                    image_url=p.get("image_url"),
                    images=p.get("images"),
                    params=p.get("params"),
                )
                db.session.add(new_product)
                # Track within the batch so a duplicate external_id later in the
                # same feed updates this row instead of inserting a collision
                # (previously handled implicitly by autoflush before each SELECT).
                existing_by_ext[p["external_id"]] = new_product
                created += 1

        # Update supplier fetch metadata
        supplier = db.session.get(Supplier, supplier_id)
        if supplier:
            supplier.last_fetched_at = now
            supplier.last_fetch_status = "success"
            supplier.last_fetch_error = None

        db.session.commit()

    except Exception as e:
        db.session.rollback()
        # Mark supplier as failed
        try:
            supplier = db.session.get(Supplier, supplier_id)
            if supplier:
                supplier.last_fetch_status = "error"
                supplier.last_fetch_error = str(e)
                db.session.commit()
        except Exception:
            db.session.rollback()
        raise

    return {"created": created, "updated": updated, "total": created + updated}


def _parse_xml(raw_bytes: bytes) -> etree._Element:
    """Parse XML bytes with encoding fallback.

    1. Try lxml native parsing (respects XML declaration encoding).
    2. Fallback: detect encoding with chardet, parse with explicit encoding.

    Both paths use a hardened parser (resolve_entities=False, no_network=True,
    huge_tree=False) to block XXE / external-entity fetches / billion-laughs
    expansion from a malformed or hostile supplier feed. This mirrors the
    parsers already used in kodaki_adapter; the predefined XML entities
    (&amp; &lt; &gt; &quot; &apos;) still resolve, so valid feeds parse
    byte-identically — only custom DTD/external entities are left untouched.
    """
    # First try: strict parse, lets lxml read encoding from the XML declaration.
    try:
        return etree.fromstring(
            raw_bytes,
            parser=etree.XMLParser(
                resolve_entities=False, no_network=True, huge_tree=False
            ),
        )
    except etree.XMLSyntaxError:
        pass

    # Fallback: detect encoding with chardet, recover from minor corruption.
    detected = chardet.detect(raw_bytes)
    encoding = detected.get("encoding", "utf-8") or "utf-8"
    parser = etree.XMLParser(
        encoding=encoding,
        recover=True,
        resolve_entities=False,
        no_network=True,
        huge_tree=False,
    )
    return etree.fromstring(raw_bytes, parser=parser)


def _text(element: etree._Element, tag: str) -> str | None:
    """Get text content of a child element, or None if missing."""
    child = element.find(tag)
    if child is not None and child.text:
        return child.text.strip()
    return None
