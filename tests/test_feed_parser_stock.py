"""parse_supplier_feed captures the MARESTO <stock> element (not just `available`)."""

from app.services.feed_parser import parse_supplier_feed

FEED = b"""<?xml version="1.0" encoding="UTF-8"?>
<yml_catalog><shop><offers>
  <offer id="1" available="true"><name>A</name><price>10</price><vendor>Brema</vendor><stock>Reserved</stock></offer>
  <offer id="2" available="false"><name>B</name><price>20</price><vendor>Forcar</vendor><stock>Out of stock</stock></offer>
  <offer id="3" available="true"><name>C</name><price>30</price><vendor>Rational</vendor></offer>
</offers></shop></yml_catalog>"""


def test_parse_captures_stock_status():
    products = parse_supplier_feed(FEED, supplier_id=1)
    by_id = {p["external_id"]: p for p in products}
    assert by_id["1"]["stock_status"] == "Reserved"
    assert by_id["2"]["stock_status"] == "Out of stock"
    # Offers without <stock> (non-MARESTO feeds) carry None, not a crash.
    assert by_id["3"]["stock_status"] is None
