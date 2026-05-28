"""Notification service tests.

M-9: Telegram messages are sent with parse_mode=HTML, so interpolated rule
names and product names must be HTML-escaped. A raw '&' or '<' (common in
product names) otherwise makes Telegram reject the whole message (400) and the
notification silently never arrives.

M-10: price_range criteria are entered in whole currency units (EUR/UAH), not
cents — _match_products converts to cents before comparing against price_cents.
"""

import app.services.notification_service as ns
from app.models.notification_rule import NotificationRule
from app.models.supplier_product import SupplierProduct
from app.services.notification_service import _match_products


def _pp(price_cents):
    return SupplierProduct(
        external_id=f"p{price_cents}", name="x", price_cents=price_cents
    )


def test_send_telegram_escapes_html_in_names(monkeypatch):
    captured = {}

    def fake_send(text):
        captured["text"] = text
        return True

    monkeypatch.setattr(ns, "send_telegram_message", fake_send)

    rule = NotificationRule(
        name="Mixers & Co",
        criteria_type="brand",
        criteria_value="A & B <test>",
    )
    product = SupplierProduct(
        external_id="X1",
        name="Блендер <Pro> & Co",
        price_cents=12345,
        currency="EUR",
    )

    ns._send_telegram_for_rule(rule, [product])

    text = captured["text"]
    # Dynamic values are escaped...
    assert "Mixers &amp; Co" in text
    assert "A &amp; B &lt;test&gt;" in text
    assert "Блендер &lt;Pro&gt; &amp; Co" in text
    # ...and no raw unescaped entity leaks from the interpolated values
    # (the only '&'/'<' in the message must be the escaped ones above).
    assert "& Co</b>" not in text
    assert "<Pro>" not in text
    # The structural <b> tag is still intact.
    assert text.startswith("<b>Правило: Mixers &amp; Co</b>")


# --- M-10: price_range in whole currency units (EUR/UAH), not cents ----------


def test_price_range_uses_whole_currency_units():
    rule = NotificationRule(
        name="r", criteria_type="price_range", criteria_value="1000-5000"
    )
    # "1000-5000" means 1000-5000 EUR/UAH = 100000-500000 cents.
    products = [_pp(99900), _pp(100000), _pp(500000), _pp(500100)]
    matched = {p.price_cents for p in _match_products(rule, products)}
    assert matched == {100000, 500000}


def test_price_range_open_ended_max():
    rule = NotificationRule(
        name="r", criteria_type="price_range", criteria_value="1000"
    )
    products = [_pp(99900), _pp(100000), _pp(9999999)]
    matched = {p.price_cents for p in _match_products(rule, products)}
    assert matched == {100000, 9999999}


def test_price_range_supports_decimals():
    rule = NotificationRule(
        name="r", criteria_type="price_range", criteria_value="10.5-50"
    )
    products = [_pp(1049), _pp(1050), _pp(5000), _pp(5001)]
    matched = {p.price_cents for p in _match_products(rule, products)}
    assert matched == {1050, 5000}


def test_price_range_invalid_value_returns_empty():
    rule = NotificationRule(
        name="r", criteria_type="price_range", criteria_value="abc", id=1
    )
    assert _match_products(rule, [_pp(100000)]) == []
