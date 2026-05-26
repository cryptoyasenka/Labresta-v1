"""Tests for scripts/np_sync_bodies — sp→pp body/photo sync, scoped & idempotent."""

import pytest

from app.models.audit_log import AuditLog
from app.models.catalog import PromProduct
from app.models.product_match import ProductMatch
from app.models.supplier import Supplier
from app.models.supplier_product import SupplierProduct
from scripts.np_sync_bodies import collect_changes, sync_bodies


@pytest.fixture()
def np_supplier(session):
    s = Supplier(name="Новый проект", feed_url="http://np", slug="novyy-proekt")
    session.add(s)
    session.commit()
    return s


def _matched_pair(session, supplier_id, *, brand="HURAKAN", status="confirmed",
                  published=True, sp_kw=None, pp_kw=None):
    sp_kw = sp_kw or {}
    pp_kw = pp_kw or {}
    sp = SupplierProduct(
        supplier_id=supplier_id, external_id=sp_kw.get("article", "ART-1"),
        name="sp name", brand=brand, article=sp_kw.get("article", "ART-1"),
        price_cents=100000, currency="EUR", available=True,
        description=sp_kw.get("description", "UA body"),
        description_ru=sp_kw.get("description_ru", "RU body"),
        image_url=sp_kw.get("image_url", "https://np/a.jpg"),
        images=sp_kw.get("images", '["https://np/a.jpg"]'),
    )
    pp = PromProduct(
        external_id=pp_kw.get("external_id", "EXT-1"), name="pp name",
        brand=brand,
        description_ua=pp_kw.get("description_ua"),
        description_ru=pp_kw.get("description_ru"),
        image_url=pp_kw.get("image_url"),
        images=pp_kw.get("images"),
    )
    session.add_all([sp, pp])
    session.commit()
    m = ProductMatch(supplier_product_id=sp.id, prom_product_id=pp.id,
                     score=100.0, status=status, published=published)
    session.add(m)
    session.commit()
    return sp, pp, m


class TestCollectChanges:
    def test_detects_diff_for_inscope_confirmed_published(self, session, np_supplier):
        _matched_pair(session, np_supplier.id)
        changes = collect_changes(np_supplier.id)
        assert len(changes) == 1
        assert set(changes[0]["fields"]) == {
            "description_ua", "description_ru", "image_url", "images"
        }

    def test_excludes_non_scope_brand(self, session, np_supplier):
        _matched_pair(session, np_supplier.id, brand="ROBOT COUPE")
        assert collect_changes(np_supplier.id) == []

    def test_excludes_unpublished(self, session, np_supplier):
        _matched_pair(session, np_supplier.id, published=False)
        assert collect_changes(np_supplier.id) == []

    def test_excludes_candidate_status(self, session, np_supplier):
        _matched_pair(session, np_supplier.id, status="candidate")
        assert collect_changes(np_supplier.id) == []

    def test_excludes_other_supplier(self, session, np_supplier):
        other = Supplier(name="Other", feed_url="http://o")
        session.add(other)
        session.commit()
        _matched_pair(session, other.id)
        assert collect_changes(np_supplier.id) == []

    def test_preserve_on_empty_no_wipe(self, session, np_supplier):
        # sp has no RU body; pp already has one → must NOT appear as a change.
        _matched_pair(
            session, np_supplier.id,
            sp_kw={"description_ru": None},
            pp_kw={"description_ru": "existing RU"},
        )
        changes = collect_changes(np_supplier.id)
        assert all("description_ru" not in c["fields"] for c in changes)


class TestSyncBodies:
    def test_apply_writes_fields(self, session, np_supplier):
        _sp, pp, _m = _matched_pair(session, np_supplier.id)
        stats = sync_bodies(apply=True, supplier_id=np_supplier.id)
        assert stats["cards_changed"] == 1
        session.refresh(pp)
        assert pp.description_ua == "UA body"
        assert pp.description_ru == "RU body"
        assert pp.image_url == "https://np/a.jpg"
        assert pp.images == '["https://np/a.jpg"]'

    def test_idempotent_second_run_zero(self, session, np_supplier):
        _matched_pair(session, np_supplier.id)
        sync_bodies(apply=True, supplier_id=np_supplier.id)
        stats2 = sync_bodies(apply=True, supplier_id=np_supplier.id)
        assert stats2["cards_changed"] == 0

    def test_dry_run_writes_nothing(self, session, np_supplier):
        _sp, pp, _m = _matched_pair(session, np_supplier.id)
        sync_bodies(apply=False, supplier_id=np_supplier.id)
        session.refresh(pp)
        assert pp.description_ua is None
        assert pp.description_ru is None

    def test_apply_writes_audit_entry(self, session, np_supplier):
        _matched_pair(session, np_supplier.id)
        sync_bodies(apply=True, supplier_id=np_supplier.id)
        logs = AuditLog.query.filter_by(action="np_sync_bodies").all()
        assert len(logs) == 1
