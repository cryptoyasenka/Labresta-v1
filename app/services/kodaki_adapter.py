"""Kodaki + Gooder feed adapters.

Both suppliers export non-YML XML. Each adapter rewrites the feed
in-memory into YML so that the standard feed_parser pipeline works
without modification.

--- Kodaki (kodaki.ua, OpenCart dwebexporter) ---
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

--- Gooder (gooder.kiev.ua) ---
Map:
    offer id attr       → id (numeric, already present)
    <in_stock>yes/no    → available="true" | "false"
    <manufacturer>      → <vendor>
    <model>             → <model> + <vendorCode>
    <price_eur>         → <price>  (<price> is UAH — ignored)
    -                   → <currencyId>EUR</currencyId>
    <image>             → <picture>
    <param>             → <param> (passed through)
    <param name="Напруга"> → voltage suffix in <name> if not already present
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
    """Apply per-supplier feed-format adapter if URL matches a known non-YML source."""
    if is_kodaki_url(feed_url):
        return kodaki_to_yml(raw_bytes)
    if is_gooder_url(feed_url):
        return gooder_to_yml(raw_bytes)
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


# ---------------------------------------------------------------------------
# Gooder adapter
# ---------------------------------------------------------------------------

def is_gooder_url(url: str | None) -> bool:
    """True if URL host is gooder.kiev.ua (or a subdomain)."""
    if not url:
        return False
    try:
        host = (urlparse(url).hostname or "").lower()
    except (ValueError, TypeError):
        return False
    return host == "gooder.kiev.ua" or host.endswith(".gooder.kiev.ua")


def _voltage_from_params(offer: etree._Element) -> str | None:
    """Pull voltage from <param> elements.

    Gooder encodes electrical specs as <param name="Напруга">220 В</param>.
    We scan all param values with the standard voltage regex so name variants
    (Напруга / Напряжение / voltage) are handled without hardcoding.
    """
    for param in offer.findall("param"):
        text = param.text or ""
        m = _VOLTAGE_RE.search(text)
        if m:
            return m.group(1)
    return None


def gooder_to_yml(raw_bytes: bytes) -> bytes:
    """Transform Гудер (gooder.kiev.ua) XML into YML-spec bytes for feed_parser."""
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

        # Voltage from <param> → name suffix (same invariant as Kodaki)
        if not _VOLTAGE_RE.search(name):
            voltage = _voltage_from_params(offer)
            if voltage:
                name = f"{name} ({voltage} В)"

        # Gooder has numeric id on every <offer> element
        external_id = offer.get("id")
        if not external_id:
            model_text = _text(offer, "model") or ""
            external_id = model_text or hashlib.sha256(name.encode("utf-8")).hexdigest()[:12]

        in_stock_raw = (_text(offer, "in_stock") or "").strip().lower()
        available = "true" if in_stock_raw == "yes" else "false"

        new_offer = etree.SubElement(offers_el, "offer")
        new_offer.set("id", external_id)
        new_offer.set("available", available)

        etree.SubElement(new_offer, "name").text = name

        manufacturer = _text(offer, "manufacturer")
        if manufacturer:
            etree.SubElement(new_offer, "vendor").text = manufacturer

        model = _text(offer, "model")
        if model:
            etree.SubElement(new_offer, "model").text = model
            etree.SubElement(new_offer, "vendorCode").text = model

        # <price> in Gooder is UAH — use <price_eur> as the working currency
        price_eur_raw = _text(offer, "price_eur")
        if price_eur_raw:
            try:
                price_val = float(price_eur_raw)
                if price_val > 0:
                    etree.SubElement(new_offer, "price").text = f"{price_val:.2f}"
            except (ValueError, TypeError):
                pass

        etree.SubElement(new_offer, "currencyId").text = "EUR"

        image = _text(offer, "image")
        if image:
            etree.SubElement(new_offer, "picture").text = image

        # Pass through <param> characteristics (picker uses them for display)
        for param in offer.findall("param"):
            param_name = param.get("name")
            param_text = param.text.strip() if param.text else ""
            if param_name and param_text:
                new_param = etree.SubElement(new_offer, "param")
                new_param.set("name", param_name)
                new_param.text = param_text

    return etree.tostring(yml_root, encoding="utf-8", xml_declaration=True)
