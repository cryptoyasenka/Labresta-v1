"""Tests for rule_matcher: apply_match_rules auto-confirms products via MatchRule entries."""

import pytest
from datetime import datetime, timezone

from app import create_app
from app.extensions import db
from app.models.supplier import Supplier
from app.models.supplier_product import SupplierProduct
from app.models.catalog import PromProduct
from app.models.match_rule import MatchRule
from app.models.product_match import ProductMatch


@pytest.fixture()
def app():
    """Create a test Flask app with in-memory SQLite."""
    app = create_app("DefaultConfig")
    app.config.update({
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
    })
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def session(app):
    """Provide a DB session within app context."""
    with app.app_context():
        yield db.session


def _make_supplier(session, name="TestSupplier"):
    s = Supplier(name=name, feed_url="http://example.com/feed.xml")
    session.add(s)
    session.flush()
    return s


def _make_supplier_product(session, supplier, name, brand=None, available=True):
    sp = SupplierProduct(
        supplier_id=supplier.id,
        external_id=f"ext-{name[:20]}",
        name=name,
        brand=brand,
        available=available,
    )
    session.add(sp)
    session.flush()
    return sp


def _make_prom_product(session, name="Prom Product", brand=None):
    pp = PromProduct(
        external_id=f"prom-{name[:20]}",
        name=name,
        brand=brand,
    )
    session.add(pp)
    session.flush()
    return pp


def _make_rule(session, name_pattern, prom_product_id, brand=None, is_active=True):
    rule = MatchRule(
        supplier_product_name_pattern=name_pattern,
        supplier_brand=brand,
        prom_product_id=prom_product_id,
        created_by="test",
        is_active=is_active,
    )
    session.add(rule)
    session.flush()
    return rule


class TestApplyMatchRules:
    """Tests for apply_match_rules function."""

    def test_name_match_creates_confirmed_match(self, session):
        """Rule with matching name creates confirmed ProductMatch with score=100.0."""
        from app.services.rule_matcher import apply_match_rules

        supplier = _make_supplier(session)
        sp = _make_supplier_product(session, supplier, "Widget Alpha")
        pp = _make_prom_product(session, "Prom Widget Alpha")
        _make_rule(session, "Widget Alpha", pp.id)
        session.commit()

        count = apply_match_rules(supplier.id)

        assert count == 1
        match = ProductMatch.query.filter_by(supplier_product_id=sp.id).first()
        assert match is not None
        assert match.status == "confirmed"
        assert match.score == 100.0
        assert match.confirmed_by.startswith("rule:")
        assert match.confirmed_at is not None

    def test_brand_and_name_must_both_match(self, session):
        """Rule with supplier_brand set requires both name AND brand to match."""
        from app.services.rule_matcher import apply_match_rules

        supplier = _make_supplier(session)
        # Product has brand "BrandA", rule requires "BrandB"
        _make_supplier_product(session, supplier, "Widget Alpha", brand="BrandA")
        pp = _make_prom_product(session)
        _make_rule(session, "Widget Alpha", pp.id, brand="BrandB")
        session.commit()

        count = apply_match_rules(supplier.id)

        assert count == 0
        assert ProductMatch.query.count() == 0

    def test_null_brand_rule_matches_on_name_only(self, session):
        """Rule with supplier_brand=NULL matches on name only (brand ignored)."""
        from app.services.rule_matcher import apply_match_rules

        supplier = _make_supplier(session)
        sp = _make_supplier_product(session, supplier, "Widget Alpha", brand="AnyBrand")
        pp = _make_prom_product(session)
        _make_rule(session, "Widget Alpha", pp.id, brand=None)
        session.commit()

        count = apply_match_rules(supplier.id)

        assert count == 1
        match = ProductMatch.query.filter_by(supplier_product_id=sp.id).first()
        assert match is not None
        assert match.status == "confirmed"

    def test_stale_rule_skipped_no_error(self, session):
        """Stale rule (prom_product deleted) is skipped, no match created."""
        from app.services.rule_matcher import apply_match_rules

        supplier = _make_supplier(session)
        _make_supplier_product(session, supplier, "Widget Alpha")
        pp = _make_prom_product(session)
        _make_rule(session, "Widget Alpha", pp.id)
        # Delete the prom product to make the rule stale
        prom_id = pp.id
        session.delete(pp)
        session.commit()

        count = apply_match_rules(supplier.id)

        assert count == 0
        assert ProductMatch.query.count() == 0

    def test_confirmed_match_skipped(self, session):
        """Product that already has a confirmed ProductMatch is skipped."""
        from app.services.rule_matcher import apply_match_rules

        supplier = _make_supplier(session)
        sp = _make_supplier_product(session, supplier, "Widget Alpha")
        pp = _make_prom_product(session)
        pp2 = _make_prom_product(session, "Another Prom Product")
        # Existing confirmed match
        existing = ProductMatch(
            supplier_product_id=sp.id,
            prom_product_id=pp.id,
            score=85.0,
            status="confirmed",
            confirmed_by="human",
            confirmed_at=datetime.now(timezone.utc),
        )
        session.add(existing)
        # Rule pointing to a different prom product
        _make_rule(session, "Widget Alpha", pp2.id)
        session.commit()

        count = apply_match_rules(supplier.id)

        assert count == 0
        # Only the original match exists
        assert ProductMatch.query.count() == 1

    def test_rejected_match_not_overwritten(self, session):
        """Product with rejected ProductMatch for same pair is not re-created."""
        from app.services.rule_matcher import apply_match_rules

        supplier = _make_supplier(session)
        sp = _make_supplier_product(session, supplier, "Widget Alpha")
        pp = _make_prom_product(session)
        # Existing rejected match for the same pair
        rejected = ProductMatch(
            supplier_product_id=sp.id,
            prom_product_id=pp.id,
            score=50.0,
            status="rejected",
        )
        session.add(rejected)
        _make_rule(session, "Widget Alpha", pp.id)
        session.commit()

        count = apply_match_rules(supplier.id)

        assert count == 0
        match = ProductMatch.query.filter_by(supplier_product_id=sp.id).first()
        assert match.status == "rejected"  # unchanged

    def test_candidate_match_upgraded_to_confirmed(self, session):
        """Existing candidate match for same pair is updated to confirmed."""
        from app.services.rule_matcher import apply_match_rules

        supplier = _make_supplier(session)
        sp = _make_supplier_product(session, supplier, "Widget Alpha")
        pp = _make_prom_product(session)
        # Existing candidate match
        candidate = ProductMatch(
            supplier_product_id=sp.id,
            prom_product_id=pp.id,
            score=75.0,
            status="candidate",
        )
        session.add(candidate)
        _make_rule(session, "Widget Alpha", pp.id)
        session.commit()

        count = apply_match_rules(supplier.id)

        assert count == 1
        match = ProductMatch.query.filter_by(supplier_product_id=sp.id).first()
        assert match.status == "confirmed"
        assert match.score == 100.0
        assert match.confirmed_by.startswith("rule:")
        # Should not have created a duplicate
        assert ProductMatch.query.count() == 1

    def test_returns_count_of_auto_confirmed(self, session):
        """Returns count of auto-confirmed matches."""
        from app.services.rule_matcher import apply_match_rules

        supplier = _make_supplier(session)
        pp1 = _make_prom_product(session, "Prom 1")
        pp2 = _make_prom_product(session, "Prom 2")
        _make_supplier_product(session, supplier, "Product A")
        _make_supplier_product(session, supplier, "Product B")
        _make_rule(session, "Product A", pp1.id)
        _make_rule(session, "Product B", pp2.id)
        session.commit()

        count = apply_match_rules(supplier.id)

        assert count == 2

    def test_inactive_rules_not_applied(self, session):
        """Inactive rules (is_active=False) are not applied."""
        from app.services.rule_matcher import apply_match_rules

        supplier = _make_supplier(session)
        _make_supplier_product(session, supplier, "Widget Alpha")
        pp = _make_prom_product(session)
        _make_rule(session, "Widget Alpha", pp.id, is_active=False)
        session.commit()

        count = apply_match_rules(supplier.id)

        assert count == 0
        assert ProductMatch.query.count() == 0

    def test_manual_match_skipped(self, session):
        """Product that already has a manual ProductMatch is skipped."""
        from app.services.rule_matcher import apply_match_rules

        supplier = _make_supplier(session)
        sp = _make_supplier_product(session, supplier, "Widget Alpha")
        pp = _make_prom_product(session)
        pp2 = _make_prom_product(session, "Another Prom")
        existing = ProductMatch(
            supplier_product_id=sp.id,
            prom_product_id=pp.id,
            score=100.0,
            status="manual",
            confirmed_by="operator",
            confirmed_at=datetime.now(timezone.utc),
        )
        session.add(existing)
        _make_rule(session, "Widget Alpha", pp2.id)
        session.commit()

        count = apply_match_rules(supplier.id)

        assert count == 0
        assert ProductMatch.query.count() == 1
