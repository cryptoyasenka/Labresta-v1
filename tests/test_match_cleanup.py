"""Tests for candidate cleanup when matches are confirmed/manual."""

import json

from app.extensions import db
from app.models.catalog import PromProduct
from app.models.product_match import ProductMatch
from app.models.supplier import Supplier
from app.models.supplier_product import SupplierProduct


def _seed_products(db_session):
    """Create a supplier with one product and three catalog products."""
    supplier = Supplier(name="TestSupplier", feed_url="http://test.xml")
    db_session.add(supplier)
    db_session.flush()

    sp = SupplierProduct(
        supplier_id=supplier.id, external_id="SP1",
        name="Тестовый товар", brand="TestBrand", available=True,
    )
    db_session.add(sp)

    proms = []
    for i in range(1, 4):
        p = PromProduct(external_id=f"PROM{i}", name=f"Каталог товар {i}", brand="TestBrand")
        db_session.add(p)
        proms.append(p)

    db_session.flush()
    return supplier, sp, proms


def _create_candidates(db_session, sp, proms, scores=(95.0, 88.0, 72.0)):
    """Create candidate matches for a supplier product."""
    matches = []
    for prom, score in zip(proms, scores):
        m = ProductMatch(
            supplier_product_id=sp.id, prom_product_id=prom.id,
            score=score, status="candidate",
        )
        db_session.add(m)
        matches.append(m)
    db_session.flush()
    return matches


class TestConfirmCleansUpCandidates:
    """Confirming a match should remove other candidates for the same supplier product."""

    def test_confirm_removes_other_candidates(self, client, db):
        """POST /matches/<id>/confirm should delete sibling candidates."""
        supplier, sp, proms = _seed_products(db.session)
        matches = _create_candidates(db.session, sp, proms)
        db.session.commit()

        target_id = matches[0].id  # score 95.0
        resp = client.post(f"/matches/{target_id}/confirm")

        assert resp.status_code == 200
        data = resp.get_json()
        assert data["new_status"] == "confirmed"
        assert data["candidates_removed"] == 2

        # Verify DB state
        remaining = ProductMatch.query.filter_by(supplier_product_id=sp.id).all()
        assert len(remaining) == 1
        assert remaining[0].status == "confirmed"
        assert remaining[0].id == target_id

    def test_confirm_does_not_touch_other_supplier_products(self, client, db):
        """Cleanup only affects the same supplier_product_id."""
        supplier, sp1, proms = _seed_products(db.session)

        sp2 = SupplierProduct(
            supplier_id=supplier.id, external_id="SP2",
            name="Другой товар", brand="TestBrand", available=True,
        )
        db.session.add(sp2)
        db.session.flush()

        # Candidates for sp1
        m1 = ProductMatch(supplier_product_id=sp1.id, prom_product_id=proms[0].id, score=95.0, status="candidate")
        m2 = ProductMatch(supplier_product_id=sp1.id, prom_product_id=proms[1].id, score=80.0, status="candidate")
        # Candidate for sp2
        m3 = ProductMatch(supplier_product_id=sp2.id, prom_product_id=proms[2].id, score=90.0, status="candidate")
        db.session.add_all([m1, m2, m3])
        db.session.commit()

        # Confirm sp1's match
        client.post(f"/matches/{m1.id}/confirm")

        # sp2's candidate should still exist
        sp2_matches = ProductMatch.query.filter_by(supplier_product_id=sp2.id).all()
        assert len(sp2_matches) == 1
        assert sp2_matches[0].status == "candidate"


class TestBulkConfirmCleansUp:
    """Bulk confirm should clean up candidates for each confirmed match."""

    def test_bulk_confirm_cleans_candidates(self, client, db):
        supplier, sp, proms = _seed_products(db.session)
        matches = _create_candidates(db.session, sp, proms)
        db.session.commit()

        target_id = matches[0].id
        resp = client.post(
            "/matches/bulk-action",
            data=json.dumps({"action": "confirm", "ids": [target_id]}),
            content_type="application/json",
        )

        assert resp.status_code == 200
        remaining = ProductMatch.query.filter_by(supplier_product_id=sp.id).all()
        assert len(remaining) == 1
        assert remaining[0].status == "confirmed"


class TestConfirmAndUpdateName:
    """Confirm + update should update catalog product name from supplier."""

    def test_confirm_update_changes_name(self, client, db):
        """POST /matches/<id>/confirm-update should update catalog name."""
        supplier, sp, proms = _seed_products(db.session)
        # Supplier has different name than catalog
        sp.name = "Тестовый товар V2"
        proms[0].name = "Тестовый товар V1"
        proms[0].name_ru = "Тестовый товар V1"
        matches = _create_candidates(db.session, sp, proms)
        db.session.commit()

        target_id = matches[0].id
        resp = client.post(f"/matches/{target_id}/confirm-update")

        assert resp.status_code == 200
        data = resp.get_json()
        assert data["new_status"] == "confirmed"
        assert data["name_updated"] is True
        assert data["new_name"] == "Тестовый товар V2"

        # Verify catalog product name updated
        updated = PromProduct.query.get(proms[0].id)
        assert updated.name == "Тестовый товар V2"

    def test_confirm_update_applies_diff_to_ru_name(self, client, db):
        """RU name should get the same token replacement as UA."""
        supplier, sp, proms = _seed_products(db.session)
        sp.name = "Апарат GEMM BCB05E"
        proms[0].name = "Апарат GEMM BCB05"
        proms[0].name_ru = "Аппарат GEMM BCB05"
        matches = _create_candidates(db.session, sp, proms)
        db.session.commit()

        resp = client.post(f"/matches/{matches[0].id}/confirm-update")
        data = resp.get_json()

        assert data["name_ru"] == "Аппарат GEMM BCB05E"


class TestManualMatchCleansUp:
    """Manual match should remove all prior candidates for the supplier product."""

    def test_manual_match_replaces_candidates(self, client, db):
        supplier, sp, proms = _seed_products(db.session)
        _create_candidates(db.session, sp, proms)
        db.session.commit()

        resp = client.post(
            "/matches/manual",
            data=json.dumps({
                "supplier_product_id": sp.id,
                "prom_product_id": proms[0].id,
            }),
            content_type="application/json",
        )

        assert resp.status_code == 200
        remaining = ProductMatch.query.filter_by(supplier_product_id=sp.id).all()
        assert len(remaining) == 1
        assert remaining[0].status == "manual"
        assert remaining[0].prom_product_id == proms[0].id
