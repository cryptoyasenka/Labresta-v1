"""Kodaki feed adapter.

Кодаки (kodaki.ua) экспортирует каталог через OpenCart `dwebexporter`,
формат не совпадает с YML/Yandex.Market, который понимает feed_parser.
Адаптер in-memory переписывает фид в YML так, чтобы дальше работала
обычная пайплайна без правки парсера.

Map:
    <offer>             → <offer id="..." available="...">
    <model>             → id (fallback: sha256(name)[:12])
    <in_stock> > 0      → available="true" | "false"
    <manufacturer>      → <vendor>
    <model>             → <model> + <vendorCode>
    <price>             → <price>
    -                   → <currencyId>EUR</currencyId>
    <description>       → <description>
    <image>             → <picture>
    <attributes>        → IGNORED (Довжина/Ширина/Висота — размеры, не цены),
                          КРОМЕ "Технічні дані" — оттуда вытаскиваем voltage
                          (220В/380В) и приписываем к <name> как `(380 В)`,
                          иначе matcher не различает 220V/380V варианты одной
                          модели (см. invariant feedback_labresta_voltage_variants).
"""

import hashlib
import re
from urllib.parse import urlparse

from lxml import etree

_VOLTAGE_RE = re.compile(r"\b(220|230|380|400)\s*[ВB]", re.IGNORECASE)


def is_kodaki_url(url: str | None) -> bool:
    """True if URL host is kodaki.ua (or a subdomain)."""
    if not url:
        return False
    try:
        host = (urlparse(url).hostname or "").lower()
    except (ValueError, TypeError):
        return False
    return host == "kodaki.ua" or host.endswith(".kodaki.ua")


def kodaki_to_yml(raw_bytes: bytes, currency: str = "EUR") -> bytes:
    """Transform Кодаки `dwebexporter` XML into YML-spec bytes."""
    parser = etree.XMLParser(
        recover=True,
        resolve_entities=False,
        no_network=True,
        huge_tree=False,
    )
    src = etree.fromstring(raw_bytes, parser=parser)

    yml_root = etree.Element("yml_catalog")
    shop = etree.SubElement(yml_root, "shop")
    offers_el = etree.SubElement(shop, "offers")

    for offer in src.iter("offer"):
        name = _text(offer, "name")
        if not name:
            continue

        if not _VOLTAGE_RE.search(name):
            voltage = _voltage_from_attributes(offer)
            if voltage:
                name = f"{name} ({voltage} В)"

        model = _text(offer, "model") or ""
        external_id = model or hashlib.sha256(name.encode("utf-8")).hexdigest()[:12]

        in_stock_raw = _text(offer, "in_stock")
        in_stock = 0
        if in_stock_raw:
            try:
                in_stock = int(float(in_stock_raw))
            except (ValueError, TypeError):
                in_stock = 0
        available = "true" if in_stock > 0 else "false"

        new_offer = etree.SubElement(offers_el, "offer")
        new_offer.set("id", external_id)
        new_offer.set("available", available)

        etree.SubElement(new_offer, "name").text = name

        manufacturer = _text(offer, "manufacturer")
        if manufacturer:
            etree.SubElement(new_offer, "vendor").text = manufacturer

        if model:
            etree.SubElement(new_offer, "model").text = model
            etree.SubElement(new_offer, "vendorCode").text = model

        price_raw = _text(offer, "price")
        if price_raw:
            try:
                price_val = float(price_raw)
                etree.SubElement(new_offer, "price").text = f"{price_val:.2f}"
            except (ValueError, TypeError):
                pass

        etree.SubElement(new_offer, "currencyId").text = currency

        description = _text(offer, "description")
        if description:
            etree.SubElement(new_offer, "description").text = description

        image = _text(offer, "image")
        if image:
            etree.SubElement(new_offer, "picture").text = image

    return etree.tostring(yml_root, encoding="utf-8", xml_declaration=True)


def apply_supplier_adapter(raw_bytes: bytes, feed_url: str | None) -> bytes:
    """Apply per-supplier feed-format adapter if URL matches a known non-YML source.

    Currently handles Кодаки (kodaki.ua, OpenCart dwebexporter). Extend here
    when other suppliers ship feeds in non-YML formats.
    """
    if is_kodaki_url(feed_url):
        return kodaki_to_yml(raw_bytes)
    return raw_bytes


def _text(element: etree._Element, tag: str) -> str | None:
    child = element.find(tag)
    if child is not None and child.text:
        return child.text.strip()
    return None


def _voltage_from_attributes(offer: etree._Element) -> str | None:
    """Pull voltage tag (220/230/380/400) out of the 'Технічні дані' attribute.

    Кодаки encodes electrical specs only inside <attributes>; those don't
    survive the YML transform, so we read them here and let kodaki_to_yml
    splice the voltage back into <name>.
    """
    for attr in offer.iterfind("attributes/attribute"):
        name_el = attr.find("name")
        if name_el is None or not name_el.text:
            continue
        if "Технічні дані" not in name_el.text:
            continue
        value_el = attr.find("value")
        if value_el is None or not value_el.text:
            continue
        m = _VOLTAGE_RE.search(value_el.text)
        if m:
            return m.group(1)
    return None
