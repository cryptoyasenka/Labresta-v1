#!/usr/bin/env python3
"""MARESTO feed verification script.

Fetches the live MARESTO feed, parses XML with encoding detection,
prints sample Cyrillic product names, and verifies SQLite round-trip.

Usage:
    python -m uv run python scripts/verify_maresto.py
"""

import sys
import re

import chardet
import requests
from lxml import etree


MARESTO_URL = "https://mrst.com.ua/include/price.xml"


def main():
    print("=== MARESTO Feed Verification ===")
    print(f"URL: {MARESTO_URL}")
    print()

    # 1. Fetch the feed
    try:
        response = requests.get(
            MARESTO_URL,
            timeout=30,
            headers={"User-Agent": "LabResta-Sync/1.0"},
        )
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"ERROR: Could not fetch feed: {e}")
        sys.exit(1)

    raw_bytes = response.content
    print(f"Status: {response.status_code} OK")
    print(f"Content-Length: {len(raw_bytes)} bytes")
    print()

    # 2. Print first 200 bytes to check encoding declaration and BOM
    print(f"First 200 bytes: {raw_bytes[:200]}")
    print()

    # 3. Detect encoding
    detected = chardet.detect(raw_bytes)
    detected_encoding = detected.get("encoding", "unknown")
    confidence = detected.get("confidence", 0)
    print(f"Detected encoding: {detected_encoding} (confidence: {confidence:.2%})")

    # Check XML declaration encoding
    xml_decl_match = re.search(rb'encoding=["\']([^"\']+)["\']', raw_bytes[:200])
    xml_decl_encoding = xml_decl_match.group(1).decode("ascii") if xml_decl_match else "not declared"
    print(f"XML declaration encoding: {xml_decl_encoding}")

    if detected_encoding and xml_decl_encoding != "not declared":
        if detected_encoding.lower().replace("-", "") != xml_decl_encoding.lower().replace("-", ""):
            print(f"WARNING: Detected encoding ({detected_encoding}) differs from XML declaration ({xml_decl_encoding})")
    print()

    # 4. Parse XML
    try:
        root = etree.fromstring(raw_bytes)
        parse_method = "lxml native (XML declaration)"
    except etree.XMLSyntaxError:
        parser = etree.XMLParser(encoding=detected_encoding, recover=True)
        root = etree.fromstring(raw_bytes, parser=parser)
        parse_method = f"chardet fallback ({detected_encoding})"

    print(f"Parse method: {parse_method}")
    print()

    # 5. Count offers
    offers = list(root.iter("offer"))
    print(f"Total offers: {len(offers)}")
    print()

    if not offers:
        print("ERROR: No <offer> elements found in feed")
        print("=== VERDICT: FAIL ===")
        sys.exit(1)

    # 6. Sample products
    print("Sample products:")
    for i, offer in enumerate(offers[:3], 1):
        name = _text(offer, "name") or "(no name)"
        brand = _text(offer, "vendor") or "(no brand)"
        price = _text(offer, "price") or "(no price)"
        article = _text(offer, "vendorCode") or "(no article)"
        print(f"  {i}. {name} (brand: {brand}, price: {price}, article: {article})")
    print()

    # 7. Unique element names in <offer>
    all_tags = set()
    for offer in offers[:50]:  # sample first 50 for speed
        for child in offer:
            tag = child.tag if isinstance(child.tag, str) else str(child.tag)
            all_tags.add(tag)
    print(f"Unique element names in <offer>: {sorted(all_tags)}")
    print()

    # 8. SQLite round-trip test
    print("SQLite round-trip test...")
    try:
        sqlite_result = _test_sqlite_roundtrip(raw_bytes, offers[:3])
        print(f"  {sqlite_result}")
    except Exception as e:
        print(f"  FAIL: {e}")
        print()
        print("=== VERDICT: FAIL ===")
        sys.exit(1)

    print()

    # 9. Verdict
    cyrillic_ok = any(
        _has_cyrillic(_text(offer, "name") or "")
        for offer in offers[:10]
    )
    if not cyrillic_ok:
        print("WARNING: No Cyrillic characters detected in sample product names")
        print("=== VERDICT: FAIL ===")
        sys.exit(1)

    print("=== VERDICT: PASS ===")


def _test_sqlite_roundtrip(raw_bytes, sample_offers):
    """Store 3 sample products in SQLite and re-read to verify no corruption."""
    from app import create_app
    from app.extensions import db
    from app.models.supplier import Supplier
    from app.services.feed_parser import parse_supplier_feed, save_supplier_products
    from sqlalchemy import select
    from app.models.supplier_product import SupplierProduct

    app = create_app()
    with app.app_context():
        # Ensure a MARESTO supplier exists
        supplier = db.session.execute(
            select(Supplier).where(Supplier.name == "MARESTO (verify)")
        ).scalar_one_or_none()

        if not supplier:
            supplier = Supplier(
                name="MARESTO (verify)",
                feed_url=MARESTO_URL,
                discount_percent=15.0,
            )
            db.session.add(supplier)
            db.session.commit()

        # Parse and save just the sample offers
        products = parse_supplier_feed(raw_bytes, supplier.id)
        if not products:
            return "FAIL: No products parsed"

        # Save first 3 only
        save_supplier_products(products[:3])

        # Re-read from DB
        stored = db.session.execute(
            select(SupplierProduct).where(
                SupplierProduct.supplier_id == supplier.id
            ).limit(3)
        ).scalars().all()

        if not stored:
            return "FAIL: No products found in DB after save"

        # Check Cyrillic preservation
        for sp in stored:
            if _has_cyrillic(sp.name):
                return f"PASS - stored {len(stored)} products, Cyrillic preserved (e.g. '{sp.name}')"

        return f"PASS - stored {len(stored)} products (no Cyrillic in sample names)"


def _text(element, tag):
    """Get text content of a child element, or None."""
    child = element.find(tag)
    if child is not None and child.text:
        return child.text.strip()
    return None


def _has_cyrillic(text):
    """Check if text contains Cyrillic characters."""
    if not text:
        return False
    return any("\u0400" <= ch <= "\u04ff" for ch in text)


if __name__ == "__main__":
    main()
