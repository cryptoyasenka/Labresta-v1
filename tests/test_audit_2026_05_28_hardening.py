"""Regression tests for the 2026-05-28 audit hardening fixes.

Covers two findings from .planning/CODE-AUDIT-2026-05-28.md:
  * M-4 — feed_parser._parse_xml must not expand custom/external XML entities
          (XXE / billion-laughs), matching the hardened parsers in kodaki_adapter.
  * M-7 — the post-login redirect must reject off-site ``next`` targets
          (open-redirect guard via auth._is_safe_next).
"""

from app.services.feed_parser import parse_supplier_feed
from app.views.auth import _is_safe_next


# ---------------------------------------------------------------------------
# M-4 — XML entity hardening in the generic feed parser
# ---------------------------------------------------------------------------

def test_feed_parser_does_not_expand_custom_entity():
    """A custom internal entity must NOT be expanded into the product name.

    With the old bare ``etree.fromstring`` (resolve_entities=True) the name
    would read "A EXPANDED B". The hardened parser leaves the entity
    unresolved, so the secret marker never lands in parsed output.
    """
    payload = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<!DOCTYPE yml_catalog [ <!ENTITY secret "EXPANDED"> ]>'
        "<yml_catalog><shop><offers>"
        '<offer id="1" available="true">'
        "<name>A&secret;B</name><price>10.00</price>"
        "<vendor>TestBrand</vendor>"
        "</offer>"
        "</offers></shop></yml_catalog>"
    ).encode("utf-8")

    products = parse_supplier_feed(payload, supplier_id=1)

    # Parsing still succeeds and the entity payload is not present.
    joined_names = " ".join(p["name"] for p in products)
    assert "EXPANDED" not in joined_names


def test_feed_parser_does_not_resolve_external_entity():
    """An external SYSTEM entity must not be fetched/inlined (no_network=True)."""
    payload = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<!DOCTYPE yml_catalog [ <!ENTITY xxe SYSTEM "file:///etc/hostname"> ]>'
        "<yml_catalog><shop><offers>"
        '<offer id="1" available="true">'
        "<name>safe&xxe;</name><price>10.00</price>"
        "<vendor>TestBrand</vendor>"
        "</offer>"
        "</offers></shop></yml_catalog>"
    ).encode("utf-8")

    # Must not raise (no network fetch) and must not leak file content.
    products = parse_supplier_feed(payload, supplier_id=1)
    for p in products:
        assert "root:" not in (p.get("name") or "")


def test_feed_parser_still_parses_predefined_entities():
    """Predefined entities (&amp; etc.) and plain feeds parse byte-identically."""
    payload = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        "<yml_catalog><shop><offers>"
        '<offer id="42" available="true">'
        "<name>Mixer &amp; Co</name><price>199.99</price>"
        "<vendor>Acme</vendor>"
        "</offer>"
        "</offers></shop></yml_catalog>"
    ).encode("utf-8")

    products = parse_supplier_feed(payload, supplier_id=1)
    assert len(products) == 1
    assert products[0]["name"] == "Mixer & Co"
    assert products[0]["price_cents"] == 19999


# ---------------------------------------------------------------------------
# M-7 — open-redirect guard on the post-login ``next`` parameter
# ---------------------------------------------------------------------------

def test_is_safe_next_accepts_local_paths():
    assert _is_safe_next("/matches/")
    assert _is_safe_next("/matches/?supplier_id=4&page=2")
    assert _is_safe_next("/")


def test_is_safe_next_rejects_offsite_and_empty():
    assert not _is_safe_next(None)
    assert not _is_safe_next("")
    assert not _is_safe_next("https://evil.com")
    assert not _is_safe_next("http://evil.com/path")
    assert not _is_safe_next("//evil.com")           # protocol-relative
    assert not _is_safe_next("relative/no/slash")    # not path-absolute
    assert not _is_safe_next("javascript:alert(1)")


def test_login_ignores_offsite_next(client, db):
    """POST /auth/login?next=https://evil.com must land on the local index."""
    from app.models.user import User

    u = User(email="redir@test.com", name="Redir", role="operator")
    u.set_password("pw12345")
    db.session.add(u)
    db.session.commit()

    # Fresh (unauthenticated) client — the shared `client` fixture is logged in.
    with client.application.test_client() as anon:
        resp = anon.post(
            "/auth/login?next=https://evil.com",
            data={"email": "redir@test.com", "password": "pw12345"},
            follow_redirects=False,
        )
        assert resp.status_code in (301, 302)
        location = resp.headers.get("Location", "")
        assert "evil.com" not in location
