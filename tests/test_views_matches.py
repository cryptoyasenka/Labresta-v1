"""Integration tests for /matches endpoints added in session 3:
- /matches/<id>/unconfirm — revert confirmed/manual back to candidate
- /matches/<id>/update-prom — inline edit of catalog name/description fields
"""

from datetime import datetime, timezone

from app.models.catalog import PromProduct
from app.models.product_match import ProductMatch
from app.models.supplier import Supplier
from app.models.supplier_product import SupplierProduct


def _seed_confirmed_match(session, *, status="confirmed"):
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
        name="Кавомашина Test 220",
        brand="TestBrand",
        price_cents=50000,
        available=True,
        needs_review=False,
    )
    session.add(sp)

    pp = PromProduct(
        external_id="PROM1",
        name="Кавомашина Test 220 В",
        name_ru="Кофемашина Test 220 В",
        brand="TestBrand",
        price=50000,
        description_ua="<p>Старое описание</p>",
        description_ru="<p>Старое описание RU</p>",
    )
    session.add(pp)
    session.flush()

    match = ProductMatch(
        supplier_product_id=sp.id,
        prom_product_id=pp.id,
        score=95.0,
        status=status,
        confirmed_at=datetime.now(timezone.utc),
        confirmed_by="seed",
        name_synced=False,
    )
    session.add(match)
    session.commit()
    return match, sp, pp


class TestUnconfirmEndpoint:
    def test_confirmed_match_reverts_to_candidate(self, client, db):
        match, _, _ = _seed_confirmed_match(db.session, status="confirmed")
        mid = match.id

        resp = client.post(f"/matches/{mid}/unconfirm")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["status"] == "ok"
        assert data["new_status"] == "candidate"

        refreshed = db.session.get(ProductMatch, mid)
        assert refreshed.status == "candidate"
        assert refreshed.confirmed_at is None
        assert refreshed.confirmed_by is None
        assert refreshed.name_synced is False

    def test_manual_match_reverts_to_candidate(self, client, db):
        match, _, _ = _seed_confirmed_match(db.session, status="manual")
        mid = match.id

        resp = client.post(f"/matches/{mid}/unconfirm")
        assert resp.status_code == 200

        refreshed = db.session.get(ProductMatch, mid)
        assert refreshed.status == "candidate"

    def test_candidate_cannot_be_unconfirmed(self, client, db):
        """Unconfirm should only work on confirmed/manual, not already-candidate."""
        match, _, _ = _seed_confirmed_match(db.session, status="candidate")
        mid = match.id

        resp = client.post(f"/matches/{mid}/unconfirm")
        assert resp.status_code == 400

        refreshed = db.session.get(ProductMatch, mid)
        assert refreshed.status == "candidate"  # unchanged

    def test_unconfirm_missing_match_returns_404(self, client, db):
        resp = client.post("/matches/99999/unconfirm")
        assert resp.status_code == 404


class TestUpdatePromFieldsEndpoint:
    def test_updates_name_persists_to_db(self, client, db):
        match, _, pp = _seed_confirmed_match(db.session)
        pp_id = pp.id

        resp = client.post(
            f"/matches/{match.id}/update-prom",
            json={"name": "Кавомашина TestFix"},
        )
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["status"] == "ok"
        assert data["updated"]["name"] == "Кавомашина TestFix"

        refreshed = db.session.get(PromProduct, pp_id)
        assert refreshed.name == "Кавомашина TestFix"

    def test_empty_name_rejected(self, client, db):
        match, _, pp = _seed_confirmed_match(db.session)
        original = pp.name

        resp = client.post(
            f"/matches/{match.id}/update-prom",
            json={"name": "   "},
        )
        assert resp.status_code == 400
        data = resp.get_json()
        assert "пуст" in data["message"].lower()

        refreshed = db.session.get(PromProduct, pp.id)
        assert refreshed.name == original

    def test_name_over_500_chars_rejected(self, client, db):
        match, _, _ = _seed_confirmed_match(db.session)
        resp = client.post(
            f"/matches/{match.id}/update-prom",
            json={"name": "x" * 501},
        )
        assert resp.status_code == 400

    def test_update_description_ua(self, client, db):
        match, _, pp = _seed_confirmed_match(db.session)
        pp_id = pp.id
        new_desc = "<p>Новое <b>описание</b></p>"

        resp = client.post(
            f"/matches/{match.id}/update-prom",
            json={"name": pp.name, "description_ua": new_desc},
        )
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["updated"]["description_ua"] == new_desc

        refreshed = db.session.get(PromProduct, pp_id)
        assert refreshed.description_ua == new_desc

    def test_empty_description_clears_field(self, client, db):
        match, _, pp = _seed_confirmed_match(db.session)
        pp_id = pp.id

        resp = client.post(
            f"/matches/{match.id}/update-prom",
            json={"name": pp.name, "description_ua": ""},
        )
        assert resp.status_code == 200

        refreshed = db.session.get(PromProduct, pp_id)
        assert refreshed.description_ua is None

    def test_update_marks_name_synced(self, client, db):
        match, _, _ = _seed_confirmed_match(db.session)
        mid = match.id
        assert match.name_synced is False

        resp = client.post(
            f"/matches/{mid}/update-prom",
            json={"name": "Кавомашина Updated"},
        )
        assert resp.status_code == 200

        refreshed = db.session.get(ProductMatch, mid)
        assert refreshed.name_synced is True

    def test_no_changes_does_not_mark_synced(self, client, db):
        """If caller sends the same values, no changes — synced flag untouched."""
        match, _, pp = _seed_confirmed_match(db.session)
        mid = match.id

        resp = client.post(
            f"/matches/{mid}/update-prom",
            json={
                "name": pp.name,
                "name_ru": pp.name_ru,
                "description_ua": pp.description_ua,
                "description_ru": pp.description_ru,
            },
        )
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["updated"] == {}

        refreshed = db.session.get(ProductMatch, mid)
        assert refreshed.name_synced is False
