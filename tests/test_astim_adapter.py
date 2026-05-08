"""Tests for Astim adapter: dealer XML -> YML + Hendi display-article matching."""

from lxml import etree

from app.services.feed_parser import parse_supplier_feed
from app.services.kodaki_adapter import (
    apply_supplier_adapter,
    astim_to_yml,
    is_astim_url,
)
from app.services.matcher import find_match_candidates


SYNTHETIC = """<?xml version="1.0" encoding="UTF-8"?>
<catalog date="2026-05-07 13:00">
    <offers>
        <offer>
            <article>525630</article>
            <barcode>8711369525630</barcode>
            <name>Щітка для чищення печей Hendi 525630</name>
            <name_ru>Щетка для чистки печей Hendi 525630</name_ru>
            <price>47.95</price>
            <in_stock>так</in_stock>
            <category>Аксесуари для піцерії</category>
            <subcategory>Щітки</subcategory>
            <description>Щітка HENDI для печей.</description>
        </offer>
        <offer>
            <article>282588</article>
            <barcode>8711369282588</barcode>
            <name/>
            <name_ru>Шприц ковбасний Profi Line Hendi 282588</name_ru>
            <price>233.99</price>
            <in_stock>ні</in_stock>
            <category>Шприци ковбасні</category>
            <subcategory/>
            <description/>
        </offer>
        <offer>
            <article>NO-NAME</article>
            <price>100</price>
            <in_stock>так</in_stock>
        </offer>
    </offers>
</catalog>
""".encode("utf-8")


class TestIsAstimUrl:
    def test_main_host(self):
        assert is_astim_url("https://astim.in.ua/toDealers.xml")

    def test_subdomain(self):
        assert is_astim_url("https://feeds.astim.in.ua/toDealers.xml")

    def test_other_host(self):
        assert not is_astim_url("https://gooder.kiev.ua/xml.xml")

    def test_empty(self):
        assert not is_astim_url("")
        assert not is_astim_url(None)


class TestAstimToYml:
    def test_returns_well_formed_yml(self):
        out = astim_to_yml(SYNTHETIC)
        root = etree.fromstring(out)
        assert root.tag == "yml_catalog"
        offers = root.findall("./shop/offers/offer")
        assert len(offers) == 2

    def test_article_maps_to_id_and_vendor_code(self):
        out = astim_to_yml(SYNTHETIC)
        root = etree.fromstring(out)
        by_id = {o.get("id"): o for o in root.findall("./shop/offers/offer")}
        assert by_id["525630"].findtext("vendorCode") == "525630"
        assert by_id["282588"].findtext("vendorCode") == "282588"

    def test_stock_maps_to_available(self):
        out = astim_to_yml(SYNTHETIC)
        root = etree.fromstring(out)
        by_id = {o.get("id"): o for o in root.findall("./shop/offers/offer")}
        assert by_id["525630"].get("available") == "true"
        assert by_id["282588"].get("available") == "false"

    def test_hendi_brand_is_extracted_conservatively(self):
        out = astim_to_yml(SYNTHETIC)
        root = etree.fromstring(out)
        by_id = {o.get("id"): o for o in root.findall("./shop/offers/offer")}
        assert by_id["525630"].findtext("vendor") == "Hendi"
        assert by_id["282588"].findtext("vendor") == "Hendi"

    def test_currency_is_uah(self):
        out = astim_to_yml(SYNTHETIC)
        root = etree.fromstring(out)
        offers = root.findall("./shop/offers/offer")
        assert all(o.findtext("currencyId") == "UAH" for o in offers)

    def test_output_is_compatible_with_feed_parser(self):
        yml = astim_to_yml(SYNTHETIC)
        products = parse_supplier_feed(yml, supplier_id=999)
        assert len(products) == 2

        brush = next(p for p in products if p["external_id"] == "525630")
        assert brush["name"] == "Щітка для чищення печей Hendi 525630"
        assert brush["brand"] == "Hendi"
        assert brush["article"] == "525630"
        assert brush["currency"] == "UAH"
        assert brush["available"] is True
        assert brush["price_cents"] == 4795
        assert '"category":' in brush["params"]

        sausage = next(p for p in products if p["external_id"] == "282588")
        assert sausage["name"] == "Шприц ковбасний Profi Line Hendi 282588"
        assert sausage["available"] is False

    def test_apply_supplier_adapter_dispatches_astim(self):
        yml = apply_supplier_adapter(SYNTHETIC, "https://astim.in.ua/toDealers.xml")
        products = parse_supplier_feed(yml, supplier_id=999)
        assert [p["external_id"] for p in products] == ["525630", "282588"]


class TestAstimHendiDisplayArticleMatch:
    def test_astim_article_matches_horoshop_display_article(self):
        yml = astim_to_yml(SYNTHETIC)
        products = parse_supplier_feed(yml, supplier_id=999)
        brush = next(p for p in products if p["external_id"] == "525630")

        prom = [
            {
                "id": 1,
                "name": "Щітка для чищення печей Hendi 525630",
                "brand": "Hendi",
                "price": 4795,
                "model": None,
                "article": None,
                "display_article": "525630",
            }
        ]

        result = find_match_candidates(
            brush["name"],
            brush["brand"],
            prom,
            supplier_price_cents=brush["price_cents"],
            supplier_article=brush["article"],
        )

        assert len(result) == 1
        assert result[0]["prom_product_id"] == 1
        assert result[0]["score"] == 100.0
