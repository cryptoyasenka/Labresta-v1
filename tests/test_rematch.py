"""Integration test for /matches/rematch endpoint.

Guarantees invariant #2: confirmed/manual matches survive rematch untouched,
while candidate/rejected matches are wiped and regenerated from the matcher.
"""

from datetime import datetime, timezone

from app.models.catalog import PromProduct
from app.models.product_match import ProductMatch
from app.models.supplier import Supplier
from app.models.supplier_product import SupplierProduct


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


def test_rematch_preserves_confirmed_and_manual(client, session, monkeypatch, tmp_path):
    # Stub out backup_db to avoid writing to the real backups/ directory.
    import scripts.backup_db as backup_mod
    monkeypatch.setattr(backup_mod, "backup", lambda: tmp_path / "stub.db")

    supplier, sps, pps, ids = _seed(session)

    resp = client.post(
        "/matches/rematch",
        json={"supplier_id": supplier.id},
    )
    assert resp.status_code == 200, resp.get_data(as_text=True)
    body = resp.get_json()
    assert body["status"] == "ok"
    assert len(body["suppliers"]) == 1
    result = body["suppliers"][0]
    assert result["supplier_id"] == supplier.id
    assert result["protected"] == 2  # confirmed + manual
    assert result["deleted"] == 2    # candidate + rejected

    session.expire_all()
    # Protected matches must still exist with same IDs and statuses.
    assert session.get(ProductMatch, ids["confirmed"]).status == "confirmed"
    assert session.get(ProductMatch, ids["manual"]).status == "manual"
    # The original candidate/rejected (sp, pp) pairs must no longer have those statuses.
    cand_row = ProductMatch.query.filter_by(
        supplier_product_id=sps[2].id, prom_product_id=pps[2].id, status="candidate",
    ).first()
    rej_row = ProductMatch.query.filter_by(
        supplier_product_id=sps[3].id, prom_product_id=pps[3].id, status="rejected",
    ).first()
    # If matcher happens to re-propose the same pair, it'd come back as 'candidate'
    # for the rejected sp — but never as 'rejected' (wiped).
    assert rej_row is None, "rejected match was not wiped"
    if cand_row is not None:
        # Matcher re-proposed the same pair — that's allowed; old row was wiped,
        # this is a freshly created one (different id).
        assert cand_row.id != ids["candidate"]


def test_rematch_all_scope(client, session, monkeypatch, tmp_path):
    import scripts.backup_db as backup_mod
    monkeypatch.setattr(backup_mod, "backup", lambda: tmp_path / "stub.db")

    sup_a, _, _, _ = _seed(session, supplier_name="Alpha")
    sup_b, _, _, _ = _seed(session, supplier_name="Bravo")

    resp = client.post("/matches/rematch", json={"supplier_id": "all"})
    assert resp.status_code == 200
    body = resp.get_json()
    ids = [r["supplier_id"] for r in body["suppliers"]]
    assert sup_a.id in ids and sup_b.id in ids
    assert body["total_deleted"] >= 4  # both suppliers contributed candidate+rejected


def test_rematch_rejects_bad_scope(client, session):
    resp = client.post("/matches/rematch", json={"supplier_id": "bogus"})
    assert resp.status_code == 400

    resp = client.post("/matches/rematch", json={"supplier_id": 999999})
    assert resp.status_code == 404

    resp = client.post("/matches/rematch", json={})
    assert resp.status_code == 400
