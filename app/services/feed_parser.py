"""YML/XML feed parser with encoding detection for supplier product feeds."""

from datetime import datetime, timezone

import chardet
from lxml import etree
from sqlalchemy import select

from app.extensions import db
from app.models.supplier import Supplier
from app.models.supplier_product import SupplierProduct


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

    products = []
    for offer in root.iter("offer"):
        external_id = offer.get("id")
        if not external_id:
            continue

        available_str = offer.get("available", "true")
        available = available_str.lower() in ("true", "1", "yes")

        name = _text(offer, "name")
        if not name:
            continue  # skip offers without a name

        price_str = _text(offer, "price")
        price_cents = None
        if price_str:
            try:
                price_cents = int(float(price_str) * 100)
            except (ValueError, TypeError):
                pass

        products.append({
            "external_id": external_id,
            "name": name,
            "brand": _text(offer, "vendor"),
            "model": _text(offer, "model"),
            "article": _text(offer, "vendorCode"),
            "price_cents": price_cents,
            "currency": _text(offer, "currencyId") or "EUR",
            "available": available,
            "supplier_id": supplier_id,
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

    try:
        for p in products:
            existing = db.session.execute(
                select(SupplierProduct).where(
                    SupplierProduct.supplier_id == p["supplier_id"],
                    SupplierProduct.external_id == p["external_id"],
                )
            ).scalar_one_or_none()

            if existing:
                existing.name = p["name"]
                existing.brand = p["brand"]
                existing.model = p["model"]
                existing.article = p["article"]
                existing.price_cents = p["price_cents"]
                existing.currency = p["currency"]
                existing.available = p["available"]
                existing.last_seen_at = now
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
                    last_seen_at=now,
                )
                db.session.add(new_product)
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
    """
    # First try: let lxml handle encoding from XML declaration
    try:
        return etree.fromstring(raw_bytes)
    except etree.XMLSyntaxError:
        pass

    # Fallback: detect encoding with chardet
    detected = chardet.detect(raw_bytes)
    encoding = detected.get("encoding", "utf-8") or "utf-8"
    parser = etree.XMLParser(encoding=encoding, recover=True)
    return etree.fromstring(raw_bytes, parser=parser)


def _text(element: etree._Element, tag: str) -> str | None:
    """Get text content of a child element, or None if missing."""
    child = element.find(tag)
    if child is not None and child.text:
        return child.text.strip()
    return None
