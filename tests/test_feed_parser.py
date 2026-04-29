"""Tests for feed_parser upsert behaviour."""

import pytest

from app.models.supplier import Supplier
from app.models.supplier_product import SupplierProduct
from app.services.feed_parser import parse_supplier_feed, save_supplier_products


@pytest.fixture()
def supplier(session):
    s = Supplier(name="TestSup", feed_url="http://x")
    session.add(s)
    session.commit()
    return s


def _row(supplier_id, **overrides):
    base = {
        "supplier_id": supplier_id,
        "external_id": "sku-1",
        "name": "Piec TestModel",
        "brand": "TestBrand",
        "model": "TestModel",
        "article": "TM-1",
        "price_cents": 100000,
        "currency": "EUR",
        "available": True,
        "description": "Full description",
        "image_url": "http://img/1.jpg",
        "images": '["http://img/1.jpg"]',
        "params": '{"color":"red"}',
    }
    base.update(overrides)
    return base


class TestUpsertPreservesOptionalFields:
    """Partial/broken feeds must not wipe stored description/image/images/params."""

    def test_existing_description_preserved_when_feed_omits(self, session, supplier):
        save_supplier_products([_row(supplier.id)])
        existing = SupplierProduct.query.filter_by(external_id="sku-1").one()
        assert existing.description == "Full description"

        save_supplier_products([_row(supplier.id, description=None)])
        refreshed = SupplierProduct.query.filter_by(external_id="sku-1").one()
        assert refreshed.description == "Full description"

    def test_existing_image_preserved_when_feed_omits(self, session, supplier):
        save_supplier_products([_row(supplier.id)])
        save_supplier_products([_row(supplier.id, image_url=None, images=None)])
        refreshed = SupplierProduct.query.filter_by(external_id="sku-1").one()
        assert refreshed.image_url == "http://img/1.jpg"
        assert refreshed.images == '["http://img/1.jpg"]'

    def test_description_updated_when_feed_provides_new(self, session, supplier):
        save_supplier_products([_row(supplier.id)])
        save_supplier_products([_row(supplier.id, description="New description")])
        refreshed = SupplierProduct.query.filter_by(external_id="sku-1").one()
        assert refreshed.description == "New description"

    def test_required_fields_still_overwritten(self, session, supplier):
        """name/brand/available/price always reflect feed (no preservation)."""
        save_supplier_products([_row(supplier.id)])
        save_supplier_products([_row(supplier.id, name="New Name", available=False)])
        refreshed = SupplierProduct.query.filter_by(external_id="sku-1").one()
        assert refreshed.name == "New Name"
        assert refreshed.available is False


class TestParsePriceCentsRounding:
    """Regression: int(float('19.99')*100) returns 1998 due to IEEE-754 —
    parse_supplier_feed must round() so price_cents matches the YML value."""

    def _yml_with_price(self, price_text):
        return (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<yml_catalog><shop><offers>'
            f'<offer id="x"><name>P</name><price>{price_text}</price>'
            '<vendor>V</vendor><currencyId>EUR</currencyId></offer>'
            '</offers></shop></yml_catalog>'
        ).encode("utf-8")

    def test_19_99_roundtrips_to_1999(self):
        products = parse_supplier_feed(self._yml_with_price("19.99"), supplier_id=1)
        assert products[0]["price_cents"] == 1999

    def test_0_29_roundtrips_to_29(self):
        products = parse_supplier_feed(self._yml_with_price("0.29"), supplier_id=1)
        assert products[0]["price_cents"] == 29

    def test_integer_price_unchanged(self):
        products = parse_supplier_feed(self._yml_with_price("100"), supplier_id=1)
        assert products[0]["price_cents"] == 10000
