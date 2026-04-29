"""Phase K — per-supplier and custom YML feeds.

Covers:
  - Custom-feed token determinism (sorted set semantics)
  - Per-supplier regen does not bleed into other suppliers' offers
  - Only the main feed updates the in_feed column
  - /matches review page no longer renders narrow price/availability buttons
  - Public per-supplier and per-custom YML routes (404 / 200 paths)
  - Custom-feed delete removes both the file and the registry row
"""

import os
import tempfile

import pytest
from lxml import etree

from app.extensions import db as _db
from app.models.catalog import PromProduct
from app.models.custom_feed import CustomFeed
from app.models.product_match import ProductMatch
from app.models.supplier import Supplier
from app.models.supplier_product import SupplierProduct
from app.services.yml_generator import (
    custom_feed_token,
    regenerate_custom_feed,
    regenerate_supplier_feed,
    regenerate_yml_feed,
)


@pytest.fixture()
def yml_output_dir(app):
    """Point YML_OUTPUT_DIR at a temp dir so each test gets a clean filesystem."""
    with tempfile.TemporaryDirectory() as tmp:
        old_dir = app.config.get("YML_OUTPUT_DIR")
        old_name = app.config.get("YML_FILENAME")
        app.config["YML_OUTPUT_DIR"] = tmp
        app.config["YML_FILENAME"] = "test-feed.yml"
        yield tmp
        app.config["YML_OUTPUT_DIR"] = old_dir
        app.config["YML_FILENAME"] = old_name


def _make_supplier(session, name: str, slug: str | None = None) -> Supplier:
    sup = Supplier(
        name=name,
        feed_url=f"https://example.com/{name}.xml",
        discount_percent=0,
        is_enabled=True,
    )
    if slug is not None:
        sup.slug = slug
    session.add(sup)
    session.commit()
    return sup


def _make_match(session, supplier: Supplier, external_id: str, name: str,
                price_cents: int = 10000) -> ProductMatch:
    pp = PromProduct(
        external_id=external_id,
        name=name,
        brand="Brand",
        price=price_cents,
        page_url=f"https://labresta.com.ua/{external_id}/",
    )
    session.add(pp)
    session.flush()

    sp = SupplierProduct(
        supplier_id=supplier.id,
        external_id=f"ext-{external_id}",
        name=name,
        brand="Brand",
        price_cents=price_cents,
        available=True,
        needs_review=False,
    )
    session.add(sp)
    session.flush()

    match = ProductMatch(
        supplier_product_id=sp.id,
        prom_product_id=pp.id,
        score=100.0,
        status="confirmed",
        confirmed_by="test",
    )
    session.add(match)
    session.commit()
    return match


class TestCustomFeedToken:
    def test_token_is_order_independent(self):
        a = custom_feed_token([3, 1, 2])
        b = custom_feed_token([1, 2, 3])
        c = custom_feed_token([2, 3, 1])
        assert a == b == c

    def test_token_differs_for_different_sets(self):
        assert custom_feed_token([1, 2]) != custom_feed_token([1, 3])

    def test_token_format(self):
        token = custom_feed_token([1, 2, 3])
        assert len(token) == 12
        assert all(ch in "0123456789abcdef" for ch in token)


class TestPerSupplierIsolation:
    def test_supplier_regen_excludes_other_suppliers(self, session, yml_output_dir):
        s1 = _make_supplier(session, "Maresto", slug="maresto")
        s2 = _make_supplier(session, "Kodaki", slug="kodaki")
        _make_match(session, s1, "m1-a", "Maresto A")
        _make_match(session, s1, "m1-b", "Maresto B")
        _make_match(session, s2, "k2", "Kodaki One")

        result = regenerate_supplier_feed(s1.id)

        assert result["supplier_slug"] == "maresto"
        assert result["total"] == 2
        assert os.path.basename(result["path"]) == "labresta-feed-maresto.yml"

        tree = etree.parse(result["path"])
        ids = sorted(o.get("id") for o in tree.findall(".//offer"))
        assert ids == ["m1-a", "m1-b"]

    def test_supplier_regen_does_not_create_other_supplier_file(
        self, session, yml_output_dir
    ):
        s1 = _make_supplier(session, "Maresto", slug="maresto")
        s2 = _make_supplier(session, "Kodaki", slug="kodaki")
        _make_match(session, s1, "m1", "M")
        _make_match(session, s2, "k1", "K")

        regenerate_supplier_feed(s1.id)

        assert os.path.exists(os.path.join(yml_output_dir, "labresta-feed-maresto.yml"))
        assert not os.path.exists(
            os.path.join(yml_output_dir, "labresta-feed-kodaki.yml")
        )


class TestInFeedFlagScope:
    """in_feed reflects membership in the MAIN feed only.

    Per-supplier and custom regeneration must not flip it — otherwise a custom
    selection on a subset of supplier A's matches would silently mark the rest
    as out-of-feed even though the main feed still ships them.
    """

    def test_main_feed_sets_in_feed(self, session, yml_output_dir):
        s = _make_supplier(session, "Maresto", slug="maresto")
        m = _make_match(session, s, "if1", "X")
        assert m.in_feed is False

        regenerate_yml_feed()

        session.refresh(m)
        assert m.in_feed is True

    def test_supplier_feed_does_not_touch_in_feed(self, session, yml_output_dir):
        s = _make_supplier(session, "Maresto", slug="maresto")
        m = _make_match(session, s, "if2", "X")
        assert m.in_feed is False

        regenerate_supplier_feed(s.id)

        session.refresh(m)
        assert m.in_feed is False

    def test_custom_feed_does_not_touch_in_feed(self, session, yml_output_dir):
        s = _make_supplier(session, "Maresto", slug="maresto")
        m = _make_match(session, s, "if3", "X")
        assert m.in_feed is False

        regenerate_custom_feed(match_ids=[m.id])

        session.refresh(m)
        assert m.in_feed is False


class TestMatchesReviewPage:
    """Phase K.4 removed the narrow-feed buttons; custom-feed button replaces them."""

    def test_narrow_feed_buttons_absent(self, client, db, yml_output_dir):
        resp = client.get("/matches/")
        assert resp.status_code == 200
        body = resp.get_data(as_text=True)
        assert "syncPricesBtn" not in body
        assert "syncAvailabilityBtn" not in body

    def test_custom_feed_button_present(self, client, db, yml_output_dir):
        resp = client.get("/matches/")
        body = resp.get_data(as_text=True)
        assert "customFeedBtn" in body


class TestServeSupplierYml:
    def test_invalid_slug_format_returns_404(self, client, db, yml_output_dir):
        resp = client.get("/feed/yml/supplier/Bad_Slug!")
        assert resp.status_code == 404

    def test_unknown_slug_returns_404(self, client, db, yml_output_dir):
        resp = client.get("/feed/yml/supplier/no-such-supplier")
        assert resp.status_code == 404

    def test_serves_existing_supplier_file(self, client, db, yml_output_dir):
        s = _make_supplier(db.session, "Maresto", slug="maresto")
        _make_match(db.session, s, "served-1", "Served")
        regenerate_supplier_feed(s.id)

        resp = client.get("/feed/yml/supplier/maresto")
        assert resp.status_code == 200
        body = resp.get_data(as_text=True)
        assert "<offer" in body
        assert 'id="served-1"' in body

    def test_known_slug_but_missing_file_returns_friendly_404(
        self, client, db, yml_output_dir
    ):
        # Supplier exists but no regen ran → no file on disk.
        # Status is still 404 (correct for Horoshop bots), but the body is a
        # human-readable HTML page with regen instructions.
        _make_supplier(db.session, "Maresto", slug="maresto")
        resp = client.get("/feed/yml/supplier/maresto")
        assert resp.status_code == 404
        body = resp.get_data(as_text=True)
        assert "Фид ещё не собран" in body
        assert "Пересобрать YML" in body
        assert "labresta-feed-maresto.yml" in body
        assert "Maresto" in body  # supplier display name in label

    def test_main_feed_missing_file_returns_friendly_404(
        self, client, db, yml_output_dir
    ):
        resp = client.get("/feed/yml")
        assert resp.status_code == 404
        body = resp.get_data(as_text=True)
        assert "Фид ещё не собран" in body
        assert "главный фид" in body


class TestServeCustomYml:
    def test_invalid_token_format_returns_404(self, client, db, yml_output_dir):
        resp = client.get("/feed/yml/custom/NOT-A-TOKEN")
        assert resp.status_code == 404

    def test_unknown_token_returns_404(self, client, db, yml_output_dir):
        resp = client.get("/feed/yml/custom/" + "0" * 12)
        assert resp.status_code == 404

    def test_serves_existing_custom_file(self, client, db, yml_output_dir):
        s = _make_supplier(db.session, "Maresto", slug="maresto")
        m = _make_match(db.session, s, "cf-1", "Custom Match")
        result = regenerate_custom_feed(match_ids=[m.id])
        token = result["token"]

        resp = client.get(f"/feed/yml/custom/{token}")
        assert resp.status_code == 200
        body = resp.get_data(as_text=True)
        assert 'id="cf-1"' in body


class TestCustomFeedDelete:
    def test_delete_removes_file_and_row(self, client, db, yml_output_dir):
        s = _make_supplier(db.session, "Maresto", slug="maresto")
        m = _make_match(db.session, s, "del-1", "To Delete")
        result = regenerate_custom_feed(match_ids=[m.id])
        token = result["token"]
        file_path = os.path.join(yml_output_dir, f"labresta-feed-custom-{token}.yml")
        assert os.path.exists(file_path)
        assert _db.session.execute(
            _db.select(CustomFeed).where(CustomFeed.token == token)
        ).scalar_one_or_none() is not None

        resp = client.post(f"/feeds/custom/{token}/delete", follow_redirects=False)
        assert resp.status_code == 302

        assert not os.path.exists(file_path)
        assert _db.session.execute(
            _db.select(CustomFeed).where(CustomFeed.token == token)
        ).scalar_one_or_none() is None
