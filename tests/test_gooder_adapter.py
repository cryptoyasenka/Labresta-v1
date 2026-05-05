"""Tests for gooder_adapter — Gooder XML → YML transform + host detector."""

import pytest
from lxml import etree

from app.services.feed_parser import parse_supplier_feed
from app.services.kodaki_adapter import is_gooder_url, gooder_to_yml


SYNTHETIC = """<?xml version="1.0" encoding="UTF-8"?>
<offers>
    <offer id="101">
        <name>ВІТРИНА ХОЛОДИЛЬНА КУПЕЦ ВХСп-1</name>
        <manufacturer>Gooder</manufacturer>
        <model>МХМКУПЕЦ1</model>
        <in_stock>yes</in_stock>
        <price>115830.00</price>
        <price_usd>0.00</price_usd>
        <price_eur>2574.00</price_eur>
        <image>https://gooder.kiev.ua/img/vitrina.png</image>
        <param name="Вага">280 кг</param>
        <param name="Напруга">220 В</param>
        <param name="Розмір (ДХШХВ)">1330х820х2120 мм</param>
    </offer>
    <offer id="102">
        <name>GN Гастроємність 1/1-10</name>
        <manufacturer>Gooder</manufacturer>
        <model>GN1110</model>
        <in_stock>no</in_stock>
        <price>540.00</price>
        <price_usd>0.00</price_usd>
        <price_eur>12.00</price_eur>
        <image>https://gooder.kiev.ua/img/gn.jpg</image>
        <param name="Матеріал">Нержавіюча сталь</param>
    </offer>
    <offer id="103">
        <name>Душируючий пристрій BILGE (380 В)</name>
        <manufacturer>Gooder</manufacturer>
        <model>BILGESHOWER1</model>
        <in_stock>no</in_stock>
        <price>6930.00</price>
        <price_usd>0.00</price_usd>
        <price_eur>157.50</price_eur>
        <image>https://gooder.kiev.ua/img/shower.jpg</image>
        <param name="Напруга">380 В</param>
    </offer>
    <offer id="104">
        <name>Стіл виробничий без бренду</name>
        <in_stock>yes</in_stock>
        <price>3600.00</price>
        <price_usd>0.00</price_usd>
        <price_eur>80.00</price_eur>
    </offer>
    <offer id="105">
        <name>Нульова ціна в євро</name>
        <manufacturer>Gooder</manufacturer>
        <model>ZERO-PRICE</model>
        <in_stock>yes</in_stock>
        <price>1000.00</price>
        <price_usd>0.00</price_usd>
        <price_eur>0.00</price_eur>
    </offer>
    <offer>
        <price>500.00</price>
        <price_eur>11.00</price_eur>
        <in_stock>yes</in_stock>
    </offer>
</offers>
""".encode("utf-8")


class TestIsGooderUrl:
    def test_main_host(self):
        assert is_gooder_url("https://gooder.kiev.ua/xml.xml")

    def test_subdomain(self):
        assert is_gooder_url("https://api.gooder.kiev.ua/feed")

    def test_other_host(self):
        assert not is_gooder_url("https://kodaki.ua/feed")
        assert not is_gooder_url("https://maresto.com.ua/feed.xml")

    def test_empty(self):
        assert not is_gooder_url("")
        assert not is_gooder_url(None)


class TestGooderToYml:
    def test_returns_well_formed_yml(self):
        out = gooder_to_yml(SYNTHETIC)
        root = etree.fromstring(out)
        assert root.tag == "yml_catalog"
        offers = root.findall("./shop/offers/offer")
        # 6 input offers, 1 skipped (no name) → 5 output
        assert len(offers) == 5

    def test_offer_id_from_attribute(self):
        out = gooder_to_yml(SYNTHETIC)
        root = etree.fromstring(out)
        ids = {o.get("id") for o in root.findall("./shop/offers/offer")}
        assert "101" in ids
        assert "102" in ids
        assert "103" in ids

    def test_yes_maps_to_available_true(self):
        out = gooder_to_yml(SYNTHETIC)
        root = etree.fromstring(out)
        by_id = {o.get("id"): o for o in root.findall("./shop/offers/offer")}
        assert by_id["101"].get("available") == "true"
        assert by_id["104"].get("available") == "true"

    def test_no_maps_to_available_false(self):
        out = gooder_to_yml(SYNTHETIC)
        root = etree.fromstring(out)
        by_id = {o.get("id"): o for o in root.findall("./shop/offers/offer")}
        assert by_id["102"].get("available") == "false"
        assert by_id["103"].get("available") == "false"

    def test_price_eur_used_not_uah(self):
        out = gooder_to_yml(SYNTHETIC)
        root = etree.fromstring(out)
        by_id = {o.get("id"): o for o in root.findall("./shop/offers/offer")}
        # EUR price 2574.00, not UAH 115830.00
        assert by_id["101"].find("price").text == "2574.00"
        assert by_id["102"].find("price").text == "12.00"

    def test_zero_eur_price_drops_price_element(self):
        """price_eur=0.00 must not produce a <price> element — zero-price offers are broken."""
        out = gooder_to_yml(SYNTHETIC)
        root = etree.fromstring(out)
        by_id = {o.get("id"): o for o in root.findall("./shop/offers/offer")}
        assert by_id["105"].find("price") is None

    def test_currency_id_is_eur(self):
        out = gooder_to_yml(SYNTHETIC)
        root = etree.fromstring(out)
        offers = root.findall("./shop/offers/offer")
        assert all(o.find("currencyId").text == "EUR" for o in offers)

    def test_manufacturer_maps_to_vendor(self):
        out = gooder_to_yml(SYNTHETIC)
        root = etree.fromstring(out)
        by_id = {o.get("id"): o for o in root.findall("./shop/offers/offer")}
        assert by_id["101"].find("vendor").text == "Gooder"

    def test_no_manufacturer_produces_no_vendor(self):
        out = gooder_to_yml(SYNTHETIC)
        root = etree.fromstring(out)
        by_id = {o.get("id"): o for o in root.findall("./shop/offers/offer")}
        assert by_id["104"].find("vendor") is None

    def test_model_maps_to_model_and_vendorcode(self):
        out = gooder_to_yml(SYNTHETIC)
        root = etree.fromstring(out)
        by_id = {o.get("id"): o for o in root.findall("./shop/offers/offer")}
        assert by_id["101"].find("model").text == "МХМКУПЕЦ1"
        assert by_id["101"].find("vendorCode").text == "МХМКУПЕЦ1"

    def test_image_maps_to_picture(self):
        out = gooder_to_yml(SYNTHETIC)
        root = etree.fromstring(out)
        by_id = {o.get("id"): o for o in root.findall("./shop/offers/offer")}
        assert by_id["101"].find("picture").text == "https://gooder.kiev.ua/img/vitrina.png"

    def test_offer_without_name_skipped(self):
        out = gooder_to_yml(SYNTHETIC)
        root = etree.fromstring(out)
        # The offer with no <name> must not appear
        ids = {o.get("id") for o in root.findall("./shop/offers/offer")}
        assert None not in ids or all(o.find("name") is not None
                                      for o in root.findall("./shop/offers/offer"))

    def test_params_passed_through(self):
        out = gooder_to_yml(SYNTHETIC)
        root = etree.fromstring(out)
        by_id = {o.get("id"): o for o in root.findall("./shop/offers/offer")}
        params = {p.get("name"): p.text for p in by_id["101"].findall("param")}
        assert "Вага" in params
        assert params["Вага"] == "280 кг"
        assert "Розмір (ДХШХВ)" in params

    def test_uah_price_not_in_output(self):
        """UAH value (115830) must never appear in the YML price element."""
        out = gooder_to_yml(SYNTHETIC)
        assert b"115830" not in out


class TestGooderVoltageInjection:
    def test_voltage_injected_from_param(self):
        """Напруга=220В → (220 В) suffix appended to name."""
        out = gooder_to_yml(SYNTHETIC)
        root = etree.fromstring(out)
        by_id = {o.get("id"): o for o in root.findall("./shop/offers/offer")}
        assert by_id["101"].find("name").text == "ВІТРИНА ХОЛОДИЛЬНА КУПЕЦ ВХСп-1 (220 В)"

    def test_voltage_not_double_appended_when_already_in_name(self):
        """Name already contains (380 В) — must not append again."""
        out = gooder_to_yml(SYNTHETIC)
        root = etree.fromstring(out)
        by_id = {o.get("id"): o for o in root.findall("./shop/offers/offer")}
        assert by_id["103"].find("name").text == "Душируючий пристрій BILGE (380 В)"

    def test_no_voltage_param_leaves_name_intact(self):
        out = gooder_to_yml(SYNTHETIC)
        root = etree.fromstring(out)
        by_id = {o.get("id"): o for o in root.findall("./shop/offers/offer")}
        assert by_id["102"].find("name").text == "GN Гастроємність 1/1-10"


class TestGooderXmlSecurity:
    def test_entity_bomb_does_not_expand(self):
        bomb = b"""<?xml version="1.0"?>
<!DOCTYPE lolz [
  <!ENTITY lol "lol">
  <!ENTITY lol2 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
  <!ENTITY lol3 "&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;">
]>
<offers>
    <offer id="BOMB">
        <name>Bomb &lol3;</name>
        <price_eur>100.00</price_eur>
        <in_stock>yes</in_stock>
    </offer>
</offers>
"""
        out = gooder_to_yml(bomb)
        assert len(out) < 5000
        root = etree.fromstring(out)
        offers = root.findall("./shop/offers/offer")
        for o in offers:
            n = o.find("name")
            if n is not None and n.text:
                assert "lol" * 100 not in n.text

    def test_external_entity_not_fetched(self):
        xxe = b"""<?xml version="1.0"?>
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
<offers>
    <offer id="XXE">
        <name>XXE &xxe;</name>
        <price_eur>1.00</price_eur>
        <in_stock>yes</in_stock>
    </offer>
</offers>
"""
        out = gooder_to_yml(xxe)
        assert b"root:" not in out
        assert b"/bin/" not in out


class TestGooderFeedParserIntegration:
    def test_output_is_compatible_with_feed_parser(self):
        """gooder_to_yml output must parse cleanly through parse_supplier_feed."""
        yml = gooder_to_yml(SYNTHETIC)
        products = parse_supplier_feed(yml, supplier_id=999)
        # 6 input, 1 no-name → 5 products
        assert len(products) == 5

        vitrina = next(p for p in products if p["external_id"] == "101")
        assert vitrina["name"] == "ВІТРИНА ХОЛОДИЛЬНА КУПЕЦ ВХСп-1 (220 В)"
        assert vitrina["brand"] == "Gooder"
        assert vitrina["model"] == "МХМКУПЕЦ1"
        assert vitrina["article"] == "МХМКУПЕЦ1"
        assert vitrina["currency"] == "EUR"
        assert vitrina["available"] is True
        assert vitrina["price_cents"] == 257400  # 2574.00 EUR * 100

        gn = next(p for p in products if p["external_id"] == "102")
        assert gn["available"] is False
        assert gn["price_cents"] == 1200  # 12.00 EUR

    def test_zero_eur_price_yields_none_price_cents(self):
        yml = gooder_to_yml(SYNTHETIC)
        products = parse_supplier_feed(yml, supplier_id=999)
        zero_item = next(p for p in products if p["external_id"] == "105")
        assert zero_item["price_cents"] is None

    def test_all_currencies_are_eur(self):
        yml = gooder_to_yml(SYNTHETIC)
        products = parse_supplier_feed(yml, supplier_id=999)
        assert all(p["currency"] == "EUR" for p in products)
