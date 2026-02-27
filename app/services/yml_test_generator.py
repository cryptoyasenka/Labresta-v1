from datetime import datetime, timezone

from lxml import etree

from app.extensions import db
from app.models.catalog import PromProduct


def generate_test_yml(product_ids: list[str], output_path: str) -> str:
    """Generate a minimal YML (Yandex Market Language) file with selected products.

    Args:
        product_ids: list of PromProduct.external_id values to include.
        output_path: where to write the resulting XML file.

    Returns:
        The output_path on success.
    """
    products = (
        db.session.query(PromProduct)
        .filter(PromProduct.external_id.in_(product_ids))
        .all()
    )
    if not products:
        raise ValueError("No products found for the given IDs")

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")

    root = etree.Element("yml_catalog", date=now)
    shop = etree.SubElement(root, "shop")

    etree.SubElement(shop, "name").text = "LabResta"
    etree.SubElement(shop, "company").text = "LabResta"
    etree.SubElement(shop, "url").text = "https://labresta.com"

    currencies = etree.SubElement(shop, "currencies")
    etree.SubElement(currencies, "currency", id="EUR", rate="1")

    offers = etree.SubElement(shop, "offers")

    for p in products:
        offer = etree.SubElement(
            offers, "offer", id=str(p.external_id), available="true"
        )
        etree.SubElement(offer, "name").text = p.name
        if p.page_url:
            etree.SubElement(offer, "url").text = p.page_url
        # Price stored as integer cents -> convert to float string
        price_val = p.price / 100.0 if p.price else 0.0
        etree.SubElement(offer, "price").text = f"{price_val:.2f}"
        etree.SubElement(offer, "currencyId").text = p.currency or "EUR"

    tree = etree.ElementTree(root)
    with open(output_path, "wb") as f:
        tree.write(
            f,
            xml_declaration=True,
            encoding="UTF-8",
            pretty_print=True,
            doctype='<!DOCTYPE yml_catalog SYSTEM "shops.dtd">',
        )

    return output_path
