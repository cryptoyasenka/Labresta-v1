"""M-9: Telegram messages are sent with parse_mode=HTML, so interpolated
rule names and product names must be HTML-escaped. A raw '&' or '<' (common
in product names) otherwise makes Telegram reject the whole message (400)
and the notification silently never arrives."""

import app.services.notification_service as ns
from app.models.notification_rule import NotificationRule
from app.models.supplier_product import SupplierProduct


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
