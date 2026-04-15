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


def _seed_confirmed_match(
    session,
    *,
    external_id,
    name,
    price_cents,
    name_ru=None,
    description_ua=None,
    description_ru=None,
    status="confirmed",
):
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
        name_ru=name_ru,
        brand="TestBrand",
        price=price_cents,
        page_url=f"https://labresta.com.ua/{external_id}/",
        description_ua=description_ua,
        description_ru=description_ru,
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
        status=status,
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

    def test_includes_manual_matches(self, session, yml_output_dir):
        """Manual matches must appear in the feed alongside confirmed ones."""
        _seed_confirmed_match(
            session, external_id="111", name="Продукт A", price_cents=10000,
        )
        _seed_confirmed_match(
            session, external_id="222", name="Продукт B", price_cents=20000,
            status="manual",
        )
        result = regenerate_yml_feed()
        assert result["total"] == 2

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


class TestYmlDescriptionPropagation:
    """Catalog edits (name_ru, description_ua, description_ru) must land in YML
    so Horoshop updates them on next import."""

    def test_name_ru_written_when_present(self, session, yml_output_dir):
        _seed_confirmed_match(
            session, external_id="n1",
            name="Кавомашина TestModel",
            name_ru="Кофемашина TestModel",
            price_cents=50000,
        )
        result = regenerate_yml_feed()
        tree = etree.parse(result["path"])
        offer = tree.find(".//offer")
        assert offer.findtext("name") == "Кавомашина TestModel"
        assert offer.findtext("name_ru") == "Кофемашина TestModel"

    def test_name_ru_absent_when_null(self, session, yml_output_dir):
        _seed_confirmed_match(
            session, external_id="n2",
            name="Плита UA only", name_ru=None, price_cents=50000,
        )
        result = regenerate_yml_feed()
        tree = etree.parse(result["path"])
        offer = tree.find(".//offer")
        assert offer.find("name_ru") is None

    def test_description_ua_written_with_cdata(self, session, yml_output_dir):
        """Description must round-trip through YML as raw HTML (CDATA wrapped)."""
        html_body = "<p>Потужна <b>кавомашина</b></p><ul><li>пункт</li></ul>"
        _seed_confirmed_match(
            session, external_id="d1",
            name="Кавомашина ProX", price_cents=100000,
            description_ua=html_body,
        )
        result = regenerate_yml_feed()
        # Parse XML then verify element text is preserved verbatim
        tree = etree.parse(result["path"])
        offer = tree.find(".//offer")
        desc = offer.find("description")
        assert desc is not None
        assert desc.text == html_body

        # Also verify CDATA wrapping is present in raw bytes so Horoshop
        # sees HTML, not escaped entities.
        with open(result["path"], "rb") as f:
            raw = f.read().decode("utf-8")
        assert "<![CDATA[" in raw
        assert html_body in raw  # unescaped

    def test_description_ru_written_with_cdata(self, session, yml_output_dir):
        _seed_confirmed_match(
            session, external_id="d2",
            name="Плита BigChef",
            price_cents=200000,
            description_ru="<p>Большая <em>плита</em></p>",
        )
        result = regenerate_yml_feed()
        tree = etree.parse(result["path"])
        offer = tree.find(".//offer")
        desc_ru = offer.find("description_ru")
        assert desc_ru is not None
        assert desc_ru.text == "<p>Большая <em>плита</em></p>"

    def test_descriptions_absent_when_null(self, session, yml_output_dir):
        """If nothing to write, description tags should not appear at all."""
        _seed_confirmed_match(
            session, external_id="d3",
            name="Пустышка", price_cents=1000,
        )
        result = regenerate_yml_feed()
        tree = etree.parse(result["path"])
        offer = tree.find(".//offer")
        assert offer.find("description") is None
        assert offer.find("description_ru") is None


class TestPublishFlag:
    """Phase C — published=False excludes match from feed but keeps the row."""

    def test_unpublished_match_excluded_from_feed(self, session, yml_output_dir):
        m1 = _seed_confirmed_match(
            session, external_id="p1", name="Включён", price_cents=10000,
        )
        m2 = _seed_confirmed_match(
            session, external_id="p2", name="Выключен", price_cents=10000,
        )
        m2.published = False
        session.commit()

        result = regenerate_yml_feed()
        assert result["total"] == 1

        tree = etree.parse(result["path"])
        offer_ids = [o.get("id") for o in tree.findall(".//offer")]
        assert "p1" in offer_ids
        assert "p2" not in offer_ids

        # in_feed flag mirrors inclusion
        session.refresh(m1)
        session.refresh(m2)
        assert m1.in_feed is True
        assert m2.in_feed is False
        assert m2.published is False  # not mutated
