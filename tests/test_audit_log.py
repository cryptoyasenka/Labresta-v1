"""Tests for audit log: verify that operator actions create audit entries."""

import json

from app.models.audit_log import AuditLog
from app.models.catalog import PromProduct
from app.models.product_match import ProductMatch
from app.models.supplier import Supplier
from app.models.supplier_product import SupplierProduct


def _seed(session, *, status="confirmed"):
    supplier = Supplier(
        name="TestSupplier",
        feed_url="http://test.xml",
        discount_percent=0,
        is_enabled=True,
    )
    session.add(supplier)
    session.flush()

    sp = SupplierProduct(
        supplier_id=supplier.id,
        external_id="SP1",
        name="Product A",
        brand="BrandX",
        price_cents=10000,
        available=True,
        needs_review=False,
    )
    session.add(sp)

    pp = PromProduct(
        external_id="PROM1",
        name="Product A catalog",
        price=12000,
    )
    session.add(pp)
    session.flush()

    match = ProductMatch(
        supplier_product_id=sp.id,
        prom_product_id=pp.id,
        score=85.0,
        status=status,
        confirmed_by="admin" if status in ("confirmed", "manual") else None,
    )
    session.add(match)
    session.commit()
    return sp, pp, match


def test_confirm_creates_audit_entry(client, db):
    sp, pp, match = _seed(db.session, status="candidate")

    resp = client.post(f"/matches/{match.id}/confirm")
    assert resp.status_code == 200

    entry = db.session.query(AuditLog).filter_by(action="confirm").first()
    assert entry is not None
    assert entry.match_id == match.id
    assert entry.user_name == "Test User"
    details = json.loads(entry.details)
    assert details["score"] == 85.0


def test_reject_creates_audit_entry(client, db):
    sp, pp, match = _seed(db.session, status="candidate")

    resp = client.post(f"/matches/{match.id}/reject")
    assert resp.status_code == 200

    entry = db.session.query(AuditLog).filter_by(action="reject").first()
    assert entry is not None
    assert entry.match_id == match.id
    assert entry.prom_product_id == pp.id


def test_unconfirm_creates_audit_entry(client, db):
    sp, pp, match = _seed(db.session, status="confirmed")

    resp = client.post(f"/matches/{match.id}/unconfirm")
    assert resp.status_code == 200

    entry = db.session.query(AuditLog).filter_by(action="unconfirm").first()
    assert entry is not None
    details = json.loads(entry.details)
    assert details["old_status"] == "confirmed"


def test_update_prom_creates_audit_entry(client, db):
    sp, pp, match = _seed(db.session, status="confirmed")

    resp = client.post(
        f"/matches/{match.id}/update-prom",
        json={"name": "Updated Name"},
        content_type="application/json",
    )
    assert resp.status_code == 200

    entry = db.session.query(AuditLog).filter_by(action="update_prom").first()
    assert entry is not None
    details = json.loads(entry.details)
    assert "name" in details["updated_fields"]


def test_manual_match_creates_audit_entry(client, db):
    sp, pp, match = _seed(db.session, status="candidate")

    pp2 = PromProduct(external_id="PROM2", name="Another product", price=15000)
    db.session.add(pp2)
    db.session.commit()

    resp = client.post(
        "/matches/manual",
        json={"supplier_product_id": sp.id, "prom_product_id": pp2.id},
        content_type="application/json",
    )
    assert resp.status_code == 200

    entry = db.session.query(AuditLog).filter_by(action="manual_match").first()
    assert entry is not None
    assert entry.prom_product_id == pp2.id
    details = json.loads(entry.details)
    assert details["prom_name"] == "Another product"


def test_mark_new_creates_audit_entry(client, db):
    sp, pp, match = _seed(db.session, status="candidate")

    resp = client.post(f"/matches/mark-new/{sp.id}")
    assert resp.status_code == 200

    entry = db.session.query(AuditLog).filter_by(action="mark_new").first()
    assert entry is not None
    assert entry.supplier_product_id == sp.id


def test_audit_page_loads(client, db):
    resp = client.get("/audit/")
    assert resp.status_code == 200
    assert "Журнал дій" in resp.data.decode()
