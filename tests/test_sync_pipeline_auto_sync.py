"""Verify auto_sync_enabled flag controls cron path but not manual/per-supplier paths."""

import pytest

from app.models.supplier import Supplier
from app.services import sync_pipeline


_OWN_NAMES = {"asTestAutoOn", "asTestAutoOff", "asTestDisabled"}


@pytest.fixture()
def suppliers(db):
    """Create one auto-on, one auto-off, one is_enabled=False supplier.

    Names prefixed `asTest` to filter from any supplier rows leaked by other
    tests (FK constraints can prevent the conftest cleanup from clearing
    `suppliers` when child tables hold references).
    """
    s_on = Supplier(name="asTestAutoOn", is_enabled=True, auto_sync_enabled=True)
    s_off = Supplier(name="asTestAutoOff", is_enabled=True, auto_sync_enabled=False)
    s_disabled = Supplier(name="asTestDisabled", is_enabled=False, auto_sync_enabled=True)
    db.session.add_all([s_on, s_off, s_disabled])
    db.session.commit()
    return s_on, s_off, s_disabled


@pytest.fixture()
def captured(monkeypatch):
    """Capture which of OUR suppliers `_sync_single_supplier` would have processed."""
    seen = []

    def _fake(supplier):
        if supplier.name in _OWN_NAMES:
            seen.append(supplier.name)
        return "success"

    monkeypatch.setattr(sync_pipeline, "_sync_single_supplier", _fake)
    return seen


def test_cron_skips_auto_sync_disabled(suppliers, captured):
    """Cron path (no args, manual=False default) excludes auto_sync_enabled=False."""
    sync_pipeline.run_full_sync()
    assert captured == ["asTestAutoOn"]


def test_manual_includes_auto_sync_disabled(suppliers, captured):
    """Manual UI trigger (manual=True) syncs ALL enabled suppliers, even auto-off."""
    sync_pipeline.run_full_sync(manual=True)
    assert sorted(captured) == ["asTestAutoOff", "asTestAutoOn"]


def test_per_supplier_ignores_flag(suppliers, captured):
    """Per-supplier trigger always works regardless of auto_sync_enabled."""
    _s_on, s_off, _disabled = suppliers
    sync_pipeline.run_full_sync(supplier_id=s_off.id)
    assert captured == ["asTestAutoOff"]


def test_disabled_supplier_never_synced(suppliers, captured):
    """is_enabled=False excludes from both cron and manual bulk paths."""
    sync_pipeline.run_full_sync()
    sync_pipeline.run_full_sync(manual=True)
    assert "asTestDisabled" not in captured


def test_sync_records_error_after_db_level_failure(db, monkeypatch):
    """Error path records status='error' + completed_at, even when the failing
    stage left the session needing a rollback (M-1 fix: rollback in except).

    NOTE: the test harness wraps each test in a SAVEPOINT, which auto-recovers
    the session, so this passes with or without the fix — it can't reproduce the
    production stuck-'running' condition (a real top-level transaction). It's a
    smoke test of the error path; the M-1 rollback is a defensive prod-only fix.
    """
    from sqlalchemy import text

    from app.models.sync_run import SyncRun

    sup = Supplier(name="asTestDbErr", is_enabled=True, feed_url="http://x/feed.xml")
    db.session.add(sup)
    db.session.commit()

    def _boom(*_a, **_k):
        try:
            db.session.execute(text("SELECT * FROM no_such_table_xyz"))
        except Exception:
            pass  # session now needs a rollback (mimics a flush failure)
        raise RuntimeError("boom")

    monkeypatch.setattr(sync_pipeline, "fetch_feed_with_retry", _boom)
    monkeypatch.setattr(sync_pipeline, "notify_sync_failure", lambda *a, **k: None)

    result = sync_pipeline._sync_single_supplier(sup)
    assert result == "error"

    run = (
        db.session.query(SyncRun)
        .filter_by(supplier_id=sup.id)
        .order_by(SyncRun.id.desc())
        .first()
    )
    assert run.status == "error"
    assert "boom" in (run.error_message or "")
    assert run.completed_at is not None


class TestToggleAutoSyncEndpoint:
    def test_toggle_flips_flag(self, client, db):
        sup = Supplier(name="Toggle-me", is_enabled=True, auto_sync_enabled=True)
        db.session.add(sup)
        db.session.commit()

        resp = client.post(
            f"/suppliers/{sup.id}/toggle-auto-sync", follow_redirects=False
        )
        assert resp.status_code == 302
        db.session.refresh(sup)
        assert sup.auto_sync_enabled is False

        resp = client.post(
            f"/suppliers/{sup.id}/toggle-auto-sync", follow_redirects=False
        )
        assert resp.status_code == 302
        db.session.refresh(sup)
        assert sup.auto_sync_enabled is True

    def test_toggle_unknown_supplier_redirects(self, client):
        resp = client.post("/suppliers/99999/toggle-auto-sync", follow_redirects=False)
        assert resp.status_code == 302
