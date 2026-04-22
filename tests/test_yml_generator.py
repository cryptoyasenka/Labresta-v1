"""Tests for YML feed generator — verify Horoshop compatibility."""

import os
import tempfile

import pytest
from lxml import etree

from app.models.catalog import PromProduct
from app.models.product_match import ProductMatch
from app.models.supplier import Supplier
from app.models.supplier_product import SupplierProduct
from app.services.yml_generator import (
    regenerate_yml_feed,
    sync_availability,
    sync_prices,
)


@pytest.fixture()
def yml_output_dir(app):
    """Point YML_OUTPUT_DIR at a temp dir for each test."""
    with tempfile.TemporaryDirectory() as tmp:
        old_dir = app.config.get("YML_OUTPUT_DIR")
        old_name = app.config.get("YML_FILENAME")
        old_prices = app.config.get("YML_PRICES_FILENAME")
        old_avail = app.config.get("YML_AVAILABILITY_FILENAME")
        app.config["YML_OUTPUT_DIR"] = tmp
        app.config["YML_FILENAME"] = "test-feed.yml"
        app.config["YML_PRICES_FILENAME"] = "test-prices.yml"
        app.config["YML_AVAILABILITY_FILENAME"] = "test-availability.yml"
        yield tmp
        app.config["YML_OUTPUT_DIR"] = old_dir
        app.config["YML_FILENAME"] = old_name
        app.config["YML_PRICES_FILENAME"] = old_prices
        app.config["YML_AVAILABILITY_FILENAME"] = old_avail


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


class TestSyncPrices:
    """Phase D — narrow price-only YML feed."""

    def test_bulk_generates_narrow_price_feed(self, session, yml_output_dir):
        """Narrow feed has id + vendorCode + price + currencyId; no name/desc."""
        _seed_confirmed_match(
            session, external_id="sp1", name="Плита", price_cents=30000,
            description_ua="<p>desc</p>",
        )
        result = sync_prices()

        assert result["total"] == 1
        assert result["skipped"] == 0
        assert os.path.exists(result["path"])

        tree = etree.parse(result["path"])
        offer = tree.find(".//offer")
        assert offer is not None
        assert offer.get("id") == "sp1"
        assert offer.findtext("vendorCode") == "sp1"
        assert offer.findtext("price") == "300.0"
        assert offer.findtext("currencyId") == "EUR"
        # Narrow feed must omit name and description
        assert offer.find("name") is None
        assert offer.find("description") is None

    def test_bumps_price_synced_at(self, session, yml_output_dir):
        m = _seed_confirmed_match(
            session, external_id="sp2", name="X", price_cents=10000,
        )
        assert m.price_synced_at is None
        sync_prices()
        session.refresh(m)
        assert m.price_synced_at is not None
        # availability timestamp must NOT be touched by price sync
        assert m.availability_synced_at is None

    def test_skips_matches_with_invalid_price(self, session, yml_output_dir):
        """Invalid-price matches are counted as skipped, not added to feed."""
        _seed_confirmed_match(
            session, external_id="ok", name="Ок", price_cents=20000,
        )
        # is_valid_price treats <=0 and implausible values as invalid
        bad = _seed_confirmed_match(
            session, external_id="bad", name="Бад", price_cents=10000,
        )
        bad.supplier_product.price_cents = 0
        session.commit()

        result = sync_prices()
        assert result["total"] == 1
        assert result["skipped"] == 1

        tree = etree.parse(result["path"])
        ids = [o.get("id") for o in tree.findall(".//offer")]
        assert ids == ["ok"]

    def test_subset_match_ids_only_syncs_those(self, session, yml_output_dir):
        m1 = _seed_confirmed_match(
            session, external_id="s1", name="A", price_cents=10000,
        )
        m2 = _seed_confirmed_match(
            session, external_id="s2", name="B", price_cents=20000,
        )
        result = sync_prices(match_ids=[m1.id])
        assert result["total"] == 1

        tree = etree.parse(result["path"])
        ids = [o.get("id") for o in tree.findall(".//offer")]
        assert ids == ["s1"]

        # Timestamp only on the synced one
        session.refresh(m1)
        session.refresh(m2)
        assert m1.price_synced_at is not None
        assert m2.price_synced_at is None

    def test_unpublished_excluded(self, session, yml_output_dir):
        m1 = _seed_confirmed_match(
            session, external_id="u1", name="Yes", price_cents=10000,
        )
        m2 = _seed_confirmed_match(
            session, external_id="u2", name="No", price_cents=10000,
        )
        m2.published = False
        session.commit()

        result = sync_prices()
        assert result["total"] == 1

        tree = etree.parse(result["path"])
        ids = [o.get("id") for o in tree.findall(".//offer")]
        assert ids == ["u1"]

        # Unpublished match must not get price_synced_at bumped
        session.refresh(m2)
        assert m2.price_synced_at is None

    def test_available_attribute_still_set(self, session, yml_output_dir):
        """Offer tag requires available attribute even in narrow price feed."""
        m = _seed_confirmed_match(
            session, external_id="a1", name="Есть", price_cents=10000,
        )
        m.supplier_product.available = False
        session.commit()
        sync_prices()

        tree = etree.parse(os.path.join(
            yml_output_dir, "test-prices.yml"
        ))
        offer = tree.find(".//offer")
        assert offer.get("available") == "false"


class TestSyncAvailability:
    """Phase D — narrow availability-only YML feed."""

    def test_bulk_generates_narrow_availability_feed(self, session, yml_output_dir):
        """Narrow feed has id + vendorCode + available attr; no price/name."""
        _seed_confirmed_match(
            session, external_id="av1", name="Плита", price_cents=30000,
            description_ua="<p>desc</p>",
        )
        result = sync_availability()

        assert result["total"] == 1
        assert result["available"] == 1
        assert os.path.exists(result["path"])

        tree = etree.parse(result["path"])
        offer = tree.find(".//offer")
        assert offer is not None
        assert offer.get("id") == "av1"
        assert offer.get("available") == "true"
        assert offer.findtext("vendorCode") == "av1"
        # Narrow feed must omit price, name, description
        assert offer.find("price") is None
        assert offer.find("name") is None
        assert offer.find("description") is None

    def test_bumps_availability_synced_at(self, session, yml_output_dir):
        m = _seed_confirmed_match(
            session, external_id="av2", name="X", price_cents=10000,
        )
        assert m.availability_synced_at is None
        sync_availability()
        session.refresh(m)
        assert m.availability_synced_at is not None
        # price timestamp must NOT be touched by availability sync
        assert m.price_synced_at is None

    def test_subset_match_ids_only_syncs_those(self, session, yml_output_dir):
        m1 = _seed_confirmed_match(
            session, external_id="av3", name="A", price_cents=10000,
        )
        m2 = _seed_confirmed_match(
            session, external_id="av4", name="B", price_cents=20000,
        )
        result = sync_availability(match_ids=[m2.id])
        assert result["total"] == 1

        tree = etree.parse(result["path"])
        ids = [o.get("id") for o in tree.findall(".//offer")]
        assert ids == ["av4"]

        session.refresh(m1)
        session.refresh(m2)
        assert m1.availability_synced_at is None
        assert m2.availability_synced_at is not None

    def test_unpublished_excluded(self, session, yml_output_dir):
        m1 = _seed_confirmed_match(
            session, external_id="av5", name="Yes", price_cents=10000,
        )
        m2 = _seed_confirmed_match(
            session, external_id="av6", name="No", price_cents=10000,
        )
        m2.published = False
        session.commit()

        result = sync_availability()
        assert result["total"] == 1

        tree = etree.parse(result["path"])
        ids = [o.get("id") for o in tree.findall(".//offer")]
        assert ids == ["av5"]

    def test_available_attribute_reflects_stock(self, session, yml_output_dir):
        """available='false' when sp.available is False or needs_review True."""
        m1 = _seed_confirmed_match(
            session, external_id="s_yes", name="In", price_cents=10000,
        )
        m2 = _seed_confirmed_match(
            session, external_id="s_no", name="Out", price_cents=10000,
        )
        m2.supplier_product.available = False
        session.commit()

        result = sync_availability()
        assert result["available"] == 1
        assert result["unavailable"] == 1

        tree = etree.parse(result["path"])
        by_id = {o.get("id"): o.get("available") for o in tree.findall(".//offer")}
        assert by_id["s_yes"] == "true"
        assert by_id["s_no"] == "false"

    def test_does_not_overwrite_full_feed(self, session, yml_output_dir):
        """Narrow feeds go to separate files; full feed is untouched."""
        _seed_confirmed_match(
            session, external_id="sep1", name="X", price_cents=10000,
        )
        full = regenerate_yml_feed()
        prices = sync_prices()
        avail = sync_availability()

        assert full["path"] != prices["path"] != avail["path"]
        # All three files coexist
        assert os.path.exists(full["path"])
        assert os.path.exists(prices["path"])
        assert os.path.exists(avail["path"])


class TestPerBrandPricing:
    """End-to-end: Supplier.pricing_mode=per_brand resolves per-brand rates
    at feed-generation time (not from match.discount_percent).
    """

    def _seed_per_brand_supplier(self, session):
        from app.models.supplier_brand_discount import SupplierBrandDiscount

        supplier = Supplier(
            name="NP",
            discount_percent=17.0,  # fallback for brands not listed
            pricing_mode="per_brand",
            is_enabled=True,
        )
        session.add(supplier)
        session.flush()
        session.add_all([
            SupplierBrandDiscount(supplier_id=supplier.id, brand="HURAKAN", discount_percent=15.0),
            SupplierBrandDiscount(supplier_id=supplier.id, brand="SIRMAN", discount_percent=20.0),
        ])
        session.commit()
        return supplier

    def _add_match(self, session, supplier, brand, external_id, price_cents):
        pp = PromProduct(
            external_id=external_id,
            name=f"{brand} item",
            brand=brand,
            price=price_cents,
            page_url=f"https://labresta.com.ua/{external_id}/",
        )
        session.add(pp)
        session.flush()
        sp = SupplierProduct(
            supplier_id=supplier.id,
            external_id=f"np-{external_id}",
            name=f"{brand} item",
            brand=brand,
            price_cents=price_cents,
            available=True,
            needs_review=False,
        )
        session.add(sp)
        session.flush()
        m = ProductMatch(
            supplier_product_id=sp.id,
            prom_product_id=pp.id,
            score=100.0,
            status="confirmed",
            confirmed_by="test",
        )
        session.add(m)
        session.commit()
        return m

    def test_feed_applies_brand_specific_rates(self, session, yml_output_dir):
        """HURAKAN=15%, SIRMAN=20%, unknown brand falls back to supplier default 17%."""
        supplier = self._seed_per_brand_supplier(session)
        self._add_match(session, supplier, "HURAKAN", "h1", 10000)   # 100 EUR → -15% → 85.0
        self._add_match(session, supplier, "SIRMAN", "s1", 10000)    # 100 EUR → -20% → 80.0
        self._add_match(session, supplier, "APACH", "a1", 10000)     # 100 EUR → -17% (fallback) → 83.0

        result = regenerate_yml_feed()
        assert result["total"] == 3

        tree = etree.parse(result["path"])
        prices = {
            o.get("id"): float(o.find("price").text)
            for o in tree.findall(".//offer")
        }
        assert prices["h1"] == 85.0
        assert prices["s1"] == 80.0
        assert prices["a1"] == 83.0

    def test_match_override_still_wins_in_per_brand_mode(self, session, yml_output_dir):
        """Per-match discount_percent (operator intent) beats brand lookup."""
        supplier = self._seed_per_brand_supplier(session)
        m = self._add_match(session, supplier, "HURAKAN", "h1", 10000)
        m.discount_percent = 30.0  # operator override
        session.commit()

        result = regenerate_yml_feed()
        tree = etree.parse(result["path"])
        offer = tree.find(".//offer[@id='h1']")
        assert float(offer.find("price").text) == 70.0  # 100 * 0.70

    def test_brand_lookup_case_insensitive_in_feed(self, session, yml_output_dir):
        """Brand in feed can be lower-case while DB row is upper-case."""
        supplier = self._seed_per_brand_supplier(session)
        self._add_match(session, supplier, "hurakan", "h1", 10000)  # lowercase

        result = regenerate_yml_feed()
        tree = etree.parse(result["path"])
        offer = tree.find(".//offer[@id='h1']")
        assert float(offer.find("price").text) == 85.0
