"""Integration tests for `POST /matches/rematch` and its status endpoints.

Guarantees invariant #2: confirmed/manual/rejected matches survive a rematch
untouched, while candidate matches are wiped and regenerated from the matcher.
Also exercises the background-job wrapper: audit-log start/finish entries,
progress reporting, 409 Conflict on concurrent start.
"""

from datetime import datetime, timezone

import pytest

from app.models.audit_log import AuditLog
from app.models.catalog import PromProduct
from app.models.product_match import ProductMatch
from app.models.supplier import Supplier
from app.models.supplier_product import SupplierProduct


@pytest.fixture(autouse=True)
def _clear_rematch_jobs():
    """Reset the in-memory job dict between tests.

    `_JOBS` is module-level and survives across tests in the same process.
    If we don't clear it, a second test sees a stale 'done' job from the
    first one (which is harmless), or — worse — a half-finished one from a
    flaky test would appear 'active' and poison the next `create_job` call.
    """
    from app.services import rematch_job
    with rematch_job._LOCK:
        rematch_job._JOBS.clear()
    yield
    with rematch_job._LOCK:
        rematch_job._JOBS.clear()


def _seed(session, supplier_name="TestSupplier"):
    supplier = Supplier(
        name=supplier_name,
        feed_url="http://test.xml",
        discount_percent=0,
        is_enabled=True,
    )
    session.add(supplier)
    session.flush()

    # Use supplier_name as prefix so _seed can be called for multiple suppliers
    # in one test without hitting UNIQUE external_id on supplier_products / prom_products.
    prefix = supplier_name

    sps = []
    for i, name in enumerate([
        "Плита Apach APRI-47 (confirmed)",
        "Плита Apach APRI-77 (manual)",
        "Плита Apach APRI-55 (candidate)",
        "Плита Apach APRI-33 (rejected)",
    ], start=1):
        sp = SupplierProduct(
            supplier_id=supplier.id,
            external_id=f"{prefix}-SP{i}",
            name=name,
            brand="Apach",
            price_cents=50000 + i * 100,
            available=True,
            needs_review=False,
        )
        session.add(sp)
        sps.append(sp)

    pps = []
    for i, name in enumerate([
        "Плита індукційна APACH APRI-47P",
        "Плита індукційна APACH APRI-77P",
        "Плита APACH APRI-55X something else",
        "Плита APACH APRI-33 other variant",
    ], start=1):
        pp = PromProduct(
            external_id=f"{prefix}-PP{i}",
            name=name,
            brand="Apach",
            price=50000 + i * 100,
        )
        session.add(pp)
        pps.append(pp)
    session.flush()

    confirmed = ProductMatch(
        supplier_product_id=sps[0].id, prom_product_id=pps[0].id,
        score=95.0, status="confirmed",
        confirmed_at=datetime.now(timezone.utc), confirmed_by="seed",
    )
    manual = ProductMatch(
        supplier_product_id=sps[1].id, prom_product_id=pps[1].id,
        score=100.0, status="manual",
        confirmed_at=datetime.now(timezone.utc), confirmed_by="seed",
    )
    candidate = ProductMatch(
        supplier_product_id=sps[2].id, prom_product_id=pps[2].id,
        score=70.0, status="candidate",
    )
    rejected = ProductMatch(
        supplier_product_id=sps[3].id, prom_product_id=pps[3].id,
        score=60.0, status="rejected",
    )
    session.add_all([confirmed, manual, candidate, rejected])
    session.commit()
    return supplier, sps, pps, {"confirmed": confirmed.id, "manual": manual.id,
                                  "candidate": candidate.id, "rejected": rejected.id}


def _stub_backup(monkeypatch, tmp_path):
    import scripts.backup_db as backup_mod
    monkeypatch.setattr(backup_mod, "backup", lambda: tmp_path / "stub.db")


def _poll_done(client, job_id):
    """In SYNC mode the job is already done when POST returns, but fetching
    it through the same endpoint the UI uses keeps the assertion honest."""
    resp = client.get(f"/matches/rematch/status/{job_id}")
    assert resp.status_code == 200, resp.get_data(as_text=True)
    body = resp.get_json()
    assert body["status"] == "ok"
    assert body["job"]["status"] == "done", body["job"]
    return body["job"]


def test_rematch_preserves_confirmed_and_manual(client, session, monkeypatch, tmp_path):
    _stub_backup(monkeypatch, tmp_path)
    supplier, sps, pps, ids = _seed(session)

    resp = client.post("/matches/rematch", json={"supplier_id": supplier.id})
    assert resp.status_code == 202, resp.get_data(as_text=True)
    body = resp.get_json()
    assert body["status"] == "started"
    job = _poll_done(client, body["job_id"])

    result = job["result"]
    assert len(result["suppliers"]) == 1
    assert result["suppliers"][0]["supplier_id"] == supplier.id
    assert result["suppliers"][0]["protected"] == 2  # confirmed + manual
    assert result["suppliers"][0]["deleted"] == 1    # only candidate; rejected preserved

    session.expire_all()
    assert session.get(ProductMatch, ids["confirmed"]).status == "confirmed"
    assert session.get(ProductMatch, ids["manual"]).status == "manual"
    rej_row = ProductMatch.query.filter_by(
        supplier_product_id=sps[3].id, prom_product_id=pps[3].id, status="rejected",
    ).first()
    assert rej_row is not None, "rejected match should be preserved across rematch"


def test_rematch_writes_audit_start_and_finish(client, session, monkeypatch, tmp_path):
    _stub_backup(monkeypatch, tmp_path)
    supplier, *_ = _seed(session)

    resp = client.post("/matches/rematch", json={"supplier_id": supplier.id})
    assert resp.status_code == 202
    _poll_done(client, resp.get_json()["job_id"])

    session.expire_all()
    actions = [a.action for a in AuditLog.query.order_by(AuditLog.id).all()]
    assert "rematch_start" in actions
    assert "rematch_finish" in actions
    # start must come before finish
    assert actions.index("rematch_start") < actions.index("rematch_finish")


def test_rematch_all_scope(client, session, monkeypatch, tmp_path):
    _stub_backup(monkeypatch, tmp_path)
    sup_a, *_ = _seed(session, supplier_name="Alpha")
    sup_b, *_ = _seed(session, supplier_name="Bravo")

    resp = client.post("/matches/rematch", json={"supplier_id": "all"})
    assert resp.status_code == 202
    job = _poll_done(client, resp.get_json()["job_id"])

    ids = [r["supplier_id"] for r in job["result"]["suppliers"]]
    assert sup_a.id in ids and sup_b.id in ids
    assert job["result"]["total_deleted"] >= 2  # both contributed at least 1 candidate each


def test_rematch_rejects_bad_scope(client, session):
    assert client.post("/matches/rematch", json={"supplier_id": "bogus"}).status_code == 400
    assert client.post("/matches/rematch", json={"supplier_id": 999999}).status_code == 404
    assert client.post("/matches/rematch", json={}).status_code == 400


def test_rematch_status_not_found(client):
    resp = client.get("/matches/rematch/status/doesnotexist")
    assert resp.status_code == 404


def test_rematch_status_active_when_idle(client):
    resp = client.get("/matches/rematch/status/active")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "none"}


def test_rematch_conflict_when_already_running(app, client, session, monkeypatch, tmp_path):
    """Starting a second rematch while one is running must return 409."""
    _stub_backup(monkeypatch, tmp_path)
    supplier, *_ = _seed(session)

    from app.services import rematch_job

    # Inject a fake 'running' job directly so we don't need real threads.
    fake_id = "fakejob01"
    with rematch_job._LOCK:
        rematch_job._JOBS[fake_id] = {
            "id": fake_id, "scope": "all", "status": "running",
            "phase": "matching", "progress": {}, "started_at": "now",
            "finished_at": None, "finished_ts": 0, "result": None,
            "error": None, "backup": None, "user_id": None, "user_name": None,
        }

    resp = client.post("/matches/rematch", json={"supplier_id": supplier.id})
    assert resp.status_code == 409
    body = resp.get_json()
    assert body["status"] == "busy"
    assert body["active_job_id"] == fake_id


def test_rematch_progress_reports_per_supplier(client, session, monkeypatch, tmp_path):
    _stub_backup(monkeypatch, tmp_path)
    supplier, *_ = _seed(session)

    resp = client.post("/matches/rematch", json={"supplier_id": supplier.id})
    job = _poll_done(client, resp.get_json()["job_id"])

    prog = job["progress"]
    assert str(supplier.id) in prog or supplier.id in prog
    row = prog.get(supplier.id) or prog.get(str(supplier.id))
    assert row["done"] == row["total"], row
    assert row["total"] >= 1  # at least the seeded SPs
    assert row["supplier_name"] == supplier.name
