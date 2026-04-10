"""Tests for YML feed generator — verify Horoshop compatibility."""

import os
import tempfile

import pytest
from lxml import etree

from app.models.catalog import PromProduct
from app.models.product_match import ProductMatch
from app.models.supplier import Supplier
from app.models.supplier_product import SupplierProduct
from app.services.yml_generator import regenerate_yml_feed


@pytest.fixture()
def yml_output_dir(app):
    """Point YML_OUTPUT_DIR at a temp dir for each test."""
    with tempfile.TemporaryDirectory() as tmp:
        old_dir = app.config.get("YML_OUTPUT_DIR")
        old_name = app.config.get("YML_FILENAME")
        app.config["YML_OUTPUT_DIR"] = tmp
        app.config["YML_FILENAME"] = "test-feed.yml"
        yield tmp
        app.config["YML_OUTPUT_DIR"] = old_dir
        app.config["YML_FILENAME"] = old_name


def _seed_confirmed_match(session, *, external_id, name, price_cents):
    """Create a Supplier + PromProduct + SupplierProduct + confirmed match."""
    supplier = Supplier(
        name="TestSupplier",
        feed_url="https://example.com/feed.xml",
        discount_percent=0,
        is_enabled=True,
    )
    session.add(supplier)
    session.flush()

    pp = PromProduct(
        external_id=external_id,
        name=name,
        brand="TestBrand",
        price=price_cents,
        page_url=f"https://labresta.com.ua/{external_id}/",
    )
    session.add(pp)
    session.flush()

    sp = SupplierProduct(
        supplier_id=supplier.id,
        external_id=f"ext-{external_id}",
        name=name,
        brand="TestBrand",
        price_cents=price_cents,
        available=True,
        needs_review=False,
    )
    session.add(sp)
    session.flush()

    match = ProductMatch(
        supplier_product_id=sp.id,
        prom_product_id=pp.id,
        score=100.0,
        status="confirmed",
        confirmed_by="test",
    )
    session.add(match)
    session.commit()
    return match


class TestYmlGenerator:
    def test_generates_file_with_confirmed_offers(self, session, yml_output_dir):
        _seed_confirmed_match(
            session, external_id="2565704494",
            name="Фритюрниця Bartscher A162410E", price_cents=17200,
        )
        result = regenerate_yml_feed()
        assert result["total"] == 1
        assert result["available"] == 1
        assert os.path.exists(result["path"])

    def test_vendorcode_equals_external_id(self, session, yml_output_dir):
        """Horoshop matches by artikul; vendorCode must hold external_id."""
        _seed_confirmed_match(
            session, external_id="877050535",
            name="Міксер Robot Coupe", price_cents=38100,
        )
        result = regenerate_yml_feed()
        tree = etree.parse(result["path"])
        offers = tree.findall(".//offer")
        assert len(offers) == 1
        offer = offers[0]
        assert offer.get("id") == "877050535"
        assert offer.findtext("vendorCode") == "877050535"

    def test_vendorcode_populated_for_all_offers(self, session, yml_output_dir):
        """Every confirmed match must get a vendorCode, even without sp.article."""
        for ext_id, name, price in [
            ("111", "Product A", 10000),
            ("222", "Product B", 20000),
            ("333", "Product C", 30000),
        ]:
            _seed_confirmed_match(
                session, external_id=ext_id, name=name, price_cents=price,
            )
        result = regenerate_yml_feed()
        tree = etree.parse(result["path"])
        offers = tree.findall(".//offer")
        assert len(offers) == 3
        for offer in offers:
            vc = offer.findtext("vendorCode")
            assert vc is not None and vc == offer.get("id"), (
                f"vendorCode must equal offer id for Horoshop matching"
            )

    def test_xml_structure_is_valid_yml(self, session, yml_output_dir):
        """Generated file must be a well-formed YML catalog."""
        _seed_confirmed_match(
            session, external_id="490032937",
            name="М'ясорубка Everest TC12E", price_cents=74300,
        )
        result = regenerate_yml_feed()
        tree = etree.parse(result["path"])
        root = tree.getroot()
        assert root.tag == "yml_catalog"
        assert root.find("shop") is not None
        assert root.find("shop/offers") is not None
        offer = root.find("shop/offers/offer")
        assert offer.findtext("name") is not None
        assert offer.findtext("price") is not None
        assert offer.findtext("currencyId") == "EUR"
