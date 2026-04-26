"""Tests for kodaki_adapter — XML→YML transform + host detector."""

import hashlib
import os

import pytest
from lxml import etree

from app.services.feed_parser import parse_supplier_feed
from app.services.kodaki_adapter import is_kodaki_url, kodaki_to_yml


SYNTHETIC = """<?xml version="1.0" encoding="UTF-8"?>
<offers>
    <offer>
        <name>FROSTY ICE-MAKER F-100</name>
        <description>Льодогенератор 100kg/24h</description>
        <image>https://kodaki.ua/img/f100.jpg</image>
        <price>45000.00</price>
        <manufacturer>FROSTY</manufacturer>
        <model>F-100</model>
        <in_stock>5</in_stock>
        <attributes>
            <attribute><name>Довжина</name><value>720.00</value></attribute>
            <attribute><name>Ширина</name><value>540.00</value></attribute>
            <attribute><name>Висота</name><value>880.00</value></attribute>
        </attributes>
    </offer>
    <offer>
        <name>FIMAR PIZZA OVEN P-200</name>
        <price>32000</price>
        <manufacturer>FIMAR</manufacturer>
        <model>P-200</model>
        <in_stock>0</in_stock>
    </offer>
    <offer>
        <name>NoModel Random Item</name>
        <price>1500.50</price>
        <manufacturer>SALVADOR</manufacturer>
        <in_stock>3</in_stock>
    </offer>
    <offer>
        <name>BadPrice Item</name>
        <price>not-a-number</price>
        <manufacturer>STAFF</manufacturer>
        <model>BP-1</model>
        <in_stock>1</in_stock>
    </offer>
    <offer>
        <description>missing name</description>
        <price>100</price>
        <model>SHOULD-BE-SKIPPED</model>
    </offer>
</offers>
""".encode("utf-8")


class TestIsKodakiUrl:
    def test_main_host(self):
        assert is_kodaki_url("https://kodaki.ua/index.php?route=x")

    def test_subdomain(self):
        assert is_kodaki_url("https://api.kodaki.ua/feed")

    def test_other_host(self):
        assert not is_kodaki_url("https://maresto.com.ua/feed.xml")

    def test_empty(self):
        assert not is_kodaki_url("")
        assert not is_kodaki_url(None)


class TestKodakiToYml:
    def test_returns_well_formed_yml(self):
        out = kodaki_to_yml(SYNTHETIC)
        root = etree.fromstring(out)
        assert root.tag == "yml_catalog"
        offers = root.findall("./shop/offers/offer")
        # 5 input offers, 1 skipped (no name) → 4 output
        assert len(offers) == 4

    def test_offer_with_model_uses_model_as_id(self):
        out = kodaki_to_yml(SYNTHETIC)
        root = etree.fromstring(out)
        ids = [o.get("id") for o in root.findall("./shop/offers/offer")]
        assert "F-100" in ids
        assert "P-200" in ids
        assert "BP-1" in ids

    def test_offer_without_model_synthesizes_id_from_name(self):
        out = kodaki_to_yml(SYNTHETIC)
        root = etree.fromstring(out)
        # NoModel Random Item has no <model> → expect sha256(name)[:12]
        expected = hashlib.sha256(
            "NoModel Random Item".encode("utf-8")
        ).hexdigest()[:12]
        ids = [o.get("id") for o in root.findall("./shop/offers/offer")]
        assert expected in ids

    def test_in_stock_maps_to_available(self):
        out = kodaki_to_yml(SYNTHETIC)
        root = etree.fromstring(out)
        by_id = {o.get("id"): o for o in root.findall("./shop/offers/offer")}
        assert by_id["F-100"].get("available") == "true"
        assert by_id["P-200"].get("available") == "false"  # in_stock=0

    def test_manufacturer_maps_to_vendor(self):
        out = kodaki_to_yml(SYNTHETIC)
        root = etree.fromstring(out)
        by_id = {o.get("id"): o for o in root.findall("./shop/offers/offer")}
        assert by_id["F-100"].find("vendor").text == "FROSTY"
        assert by_id["P-200"].find("vendor").text == "FIMAR"

    def test_currency_id_added(self):
        out = kodaki_to_yml(SYNTHETIC)
        root = etree.fromstring(out)
        offers = root.findall("./shop/offers/offer")
        assert all(o.find("currencyId").text == "EUR" for o in offers)

    def test_currency_override(self):
        out = kodaki_to_yml(SYNTHETIC, currency="UAH")
        root = etree.fromstring(out)
        offers = root.findall("./shop/offers/offer")
        assert all(o.find("currencyId").text == "UAH" for o in offers)

    def test_image_maps_to_picture(self):
        out = kodaki_to_yml(SYNTHETIC)
        root = etree.fromstring(out)
        by_id = {o.get("id"): o for o in root.findall("./shop/offers/offer")}
        assert by_id["F-100"].find("picture").text == "https://kodaki.ua/img/f100.jpg"

    def test_invalid_price_dropped_silently(self):
        out = kodaki_to_yml(SYNTHETIC)
        root = etree.fromstring(out)
        by_id = {o.get("id"): o for o in root.findall("./shop/offers/offer")}
        # BP-1 has bad price — should still appear but without <price>
        assert by_id["BP-1"].find("price") is None

    def test_offer_without_name_skipped(self):
        out = kodaki_to_yml(SYNTHETIC)
        root = etree.fromstring(out)
        ids = [o.get("id") for o in root.findall("./shop/offers/offer")]
        assert "SHOULD-BE-SKIPPED" not in ids

    def test_dimensions_attributes_ignored(self):
        """Adapter must NOT confuse <attributes>/Довжина/Ширина/Висота with prices."""
        out = kodaki_to_yml(SYNTHETIC)
        # Output contains no "Довжина" anywhere
        assert b"\xd0\x94\xd0\xbe\xd0\xb2\xd0\xb6\xd0\xb8\xd0\xbd\xd0\xb0" not in out


class TestVoltageInjection:
    """Voltage from 'Технічні дані' attribute → name suffix.

    Кодаки holds 220В/380В only in <attributes>, which we drop. The matcher's
    voltage gate reads voltage from the name only, so we splice it back.
    """

    VOLTAGE_FEED = """<?xml version="1.0" encoding="UTF-8"?>
<offers>
    <offer>
        <name>Тістоміс спіральний MSP50 JET/T</name>
        <price>8535</price>
        <manufacturer>MAC.PAN</manufacturer>
        <model>000010143</model>
        <in_stock>0</in_stock>
        <attributes>
            <attribute><name>Технічні дані</name><value>1,5 3,0 + 0,25 кВт 380В</value></attribute>
            <attribute><name>Довжина</name><value>570.00</value></attribute>
        </attributes>
    </offer>
    <offer>
        <name>Супник електричний SB-6000</name>
        <price>68</price>
        <manufacturer>FROSTY</manufacturer>
        <model>000004521</model>
        <in_stock>20</in_stock>
        <attributes>
            <attribute><name>Технічні дані</name><value>0,40 кВт/ 220В</value></attribute>
        </attributes>
    </offer>
    <offer>
        <name>Картоплечистка PPN10 (380 В)</name>
        <price>500</price>
        <manufacturer>FIMAR</manufacturer>
        <model>000099999</model>
        <in_stock>1</in_stock>
        <attributes>
            <attribute><name>Технічні дані</name><value>0,75 кВт/ 380В</value></attribute>
        </attributes>
    </offer>
    <offer>
        <name>Аксесуар без електрики</name>
        <price>10</price>
        <manufacturer>FROSTY</manufacturer>
        <model>000088888</model>
        <in_stock>5</in_stock>
        <attributes>
            <attribute><name>Довжина</name><value>100</value></attribute>
        </attributes>
    </offer>
</offers>
""".encode("utf-8")

    def test_voltage_appended_to_name_when_missing(self):
        out = kodaki_to_yml(self.VOLTAGE_FEED)
        root = etree.fromstring(out)
        by_id = {o.get("id"): o for o in root.findall("./shop/offers/offer")}
        # 380В injected from attribute
        assert by_id["000010143"].find("name").text == \
            "Тістоміс спіральний MSP50 JET/T (380 В)"
        # 220В injected from attribute
        assert by_id["000004521"].find("name").text == \
            "Супник електричний SB-6000 (220 В)"

    def test_voltage_not_double_appended_when_already_in_name(self):
        out = kodaki_to_yml(self.VOLTAGE_FEED)
        root = etree.fromstring(out)
        by_id = {o.get("id"): o for o in root.findall("./shop/offers/offer")}
        # Name already had '(380 В)' — must stay as-is, not become double
        assert by_id["000099999"].find("name").text == \
            "Картоплечистка PPN10 (380 В)"

    def test_no_voltage_attribute_leaves_name_intact(self):
        out = kodaki_to_yml(self.VOLTAGE_FEED)
        root = etree.fromstring(out)
        by_id = {o.get("id"): o for o in root.findall("./shop/offers/offer")}
        assert by_id["000088888"].find("name").text == "Аксесуар без електрики"

    def test_voltage_feeds_into_matcher_voltage_gate(self):
        """End-to-end: adapter → parser → matcher.extract_voltages picks it up."""
        from app.services.matcher import extract_voltages
        yml = kodaki_to_yml(self.VOLTAGE_FEED)
        products = parse_supplier_feed(yml, supplier_id=999)
        msp50 = next(p for p in products if p["external_id"] == "000010143")
        assert "380" in extract_voltages(msp50["name"])
        supnyk = next(p for p in products if p["external_id"] == "000004521")
        assert "220" in extract_voltages(supnyk["name"])


class TestXmlSecurity:
    """Adapter must reject entity-bomb / XXE payloads safely."""

    def test_billion_laughs_does_not_expand(self):
        # Classic billion-laughs entity bomb. With resolve_entities=False the
        # &lol9; references must NOT expand — at worst we get an empty/partial
        # tree, never an OOM.
        bomb = b"""<?xml version="1.0"?>
<!DOCTYPE lolz [
  <!ENTITY lol "lol">
  <!ENTITY lol2 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
  <!ENTITY lol3 "&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;">
  <!ENTITY lol4 "&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;">
]>
<offers>
    <offer>
        <name>Bomb &lol4;</name>
        <price>100</price>
        <model>BOMB-1</model>
        <in_stock>1</in_stock>
    </offer>
</offers>
"""
        out = kodaki_to_yml(bomb)
        # Output must be small (KB, not MB) — entity didn't blow up
        assert len(out) < 5000
        root = etree.fromstring(out)
        offers = root.findall("./shop/offers/offer")
        # Either offer is dropped or its name is the literal/empty form,
        # but never a megabyte of expanded "lol".
        for o in offers:
            n = o.find("name")
            if n is not None and n.text:
                assert "lol" * 100 not in n.text

    def test_external_entity_not_fetched(self):
        # XXE attempt to read a local file. With no_network=True and
        # resolve_entities=False this must silently fail to expand.
        xxe = b"""<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<offers>
    <offer>
        <name>XXE &xxe;</name>
        <price>1</price>
        <model>XXE-1</model>
        <in_stock>1</in_stock>
    </offer>
</offers>
"""
        out = kodaki_to_yml(xxe)
        # No /etc/passwd content (or 'root:' shell user line) leaked into output
        assert b"root:" not in out
        assert b"/bin/" not in out

    def test_output_is_compatible_with_feed_parser(self):
        """The generated YML must parse cleanly through parse_supplier_feed."""
        yml_bytes = kodaki_to_yml(SYNTHETIC)
        products = parse_supplier_feed(yml_bytes, supplier_id=999)
        # 5 offers in, 1 dropped (no name) → 4 out
        assert len(products) == 4
        f100 = next(p for p in products if p["external_id"] == "F-100")
        assert f100["name"] == "FROSTY ICE-MAKER F-100"
        assert f100["brand"] == "FROSTY"
        assert f100["model"] == "F-100"
        assert f100["article"] == "F-100"
        assert f100["currency"] == "EUR"
        assert f100["available"] is True
        assert f100["price_cents"] == 4500000  # 45000.00 EUR

        p200 = next(p for p in products if p["external_id"] == "P-200")
        assert p200["available"] is False  # in_stock=0


# Integration smoke on real downloaded fixture if present
REAL_FEED_PATH = os.path.join(
    os.environ.get("TEMP", "/tmp"),
    "labresta_probe",
    "kodaki.xml",
)


@pytest.mark.skipif(
    not os.path.exists(REAL_FEED_PATH),
    reason=f"Real Kodaki probe not at {REAL_FEED_PATH}",
)
class TestRealKodakiFeed:
    def test_real_feed_normalizes_to_yml(self):
        with open(REAL_FEED_PATH, "rb") as f:
            raw = f.read()
        yml = kodaki_to_yml(raw)
        root = etree.fromstring(yml)
        offers = root.findall("./shop/offers/offer")
        # Real feed has 1356 offers; expect ≥1300 after name-guard
        assert len(offers) >= 1300, f"got {len(offers)}"

    def test_real_feed_passes_parse_supplier_feed(self):
        with open(REAL_FEED_PATH, "rb") as f:
            raw = f.read()
        yml = kodaki_to_yml(raw)
        products = parse_supplier_feed(yml, supplier_id=999)
        assert len(products) >= 1300
        # All EUR
        assert all(p["currency"] == "EUR" for p in products)
        # Mostly with brand
        with_brand = sum(1 for p in products if p["brand"])
        assert with_brand >= len(products) * 0.95  # ≥95% with manufacturer
        # Mix of available/unavailable (we know 514/1356 have in_stock=0)
        avail_count = sum(1 for p in products if p["available"])
        unavail_count = sum(1 for p in products if not p["available"])
        assert avail_count > 500
        assert unavail_count > 300
