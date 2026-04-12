"""Integration tests for /matches endpoints:
- /matches/<id>/unconfirm — revert confirmed/manual back to candidate
- /matches/<id>/update-prom — inline edit of catalog name/description fields
- /matches/mark-new/<sp_id> — mark supplier product for catalog addition
- /matches/unmark-new/<sp_id> — remove the mark
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

    def test_unconfirm_preserves_name_synced(self, client, db):
        """Unconfirm must NOT clear name_synced — the PromProduct.name change
        survives unconfirm, so the flag should too, otherwise the DB ends up
        inconsistent (catalog has new name, match says it wasn't synced).
        """
        match, _, _ = _seed_confirmed_match(db.session, status="confirmed")
        match.name_synced = True
        db.session.commit()
        mid = match.id

        resp = client.post(f"/matches/{mid}/unconfirm")
        assert resp.status_code == 200

        refreshed = db.session.get(ProductMatch, mid)
        assert refreshed.status == "candidate"
        assert refreshed.name_synced is True

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


class TestMarkForCatalogEndpoint:
    def test_marks_available_product(self, client, db):
        match, sp, _ = _seed_confirmed_match(db.session, status="candidate")
        sp_id = sp.id
        assert sp.available is True

        resp = client.post(f"/matches/mark-new/{sp_id}")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["status"] == "ok"

        refreshed_sp = db.session.get(SupplierProduct, sp_id)
        assert refreshed_sp.needs_catalog_add is True

        refreshed_match = db.session.get(ProductMatch, match.id)
        assert refreshed_match.status == "rejected"

    def test_rejects_unavailable_product(self, client, db):
        match, sp, _ = _seed_confirmed_match(db.session, status="candidate")
        sp.available = False
        db.session.commit()
        sp_id = sp.id

        resp = client.post(f"/matches/mark-new/{sp_id}")
        assert resp.status_code == 400

        refreshed_sp = db.session.get(SupplierProduct, sp_id)
        assert refreshed_sp.needs_catalog_add is False

    def test_missing_product_returns_404(self, client, db):
        resp = client.post("/matches/mark-new/99999")
        assert resp.status_code == 404

    def test_unmark_clears_flag(self, client, db):
        _, sp, _ = _seed_confirmed_match(db.session, status="candidate")
        sp.needs_catalog_add = True
        db.session.commit()
        sp_id = sp.id

        resp = client.post(f"/matches/unmark-new/{sp_id}")
        assert resp.status_code == 200

        refreshed = db.session.get(SupplierProduct, sp_id)
        assert refreshed.needs_catalog_add is False


class TestApplyNameDiff:
    """Unit tests for _apply_name_diff — safe RU name update from UA diff."""

    def test_model_code_updated_in_ru(self):
        from app.views.matches import _apply_name_diff

        old_ua = "М'ясорубка Fama FTS137"
        new_ua = "М'ясорубка Fama FTS137UTE"
        old_ru = "Мясорубка Fama FTS137"
        result = _apply_name_diff(old_ua, new_ua, old_ru)
        assert result == "Мясорубка Fama FTS137UTE"

    def test_cyrillic_words_not_replaced(self):
        """Cyrillic tokens must never be transplanted into RU — UA and RU
        use different words (пакунок vs упаковка, пакети vs пакеты)."""
        from app.views.matches import _apply_name_diff

        old_ua = "Пакети гофровані Lavezzini 200x400 (паковання 100 шт.)"
        new_ua = "Пакет Lavezzini Gofer 200x400 ( пакунок 100 шт.)"
        old_ru = "Пакеты гофрированные Lavezzini 200x400 (упаковка 100 шт.)"
        result = _apply_name_diff(old_ua, new_ua, old_ru)
        # Cyrillic words must stay untouched in RU
        assert "Lavezzini" in result
        assert "упаковка" in result
        assert "пакунок" not in result
        assert "Пакет " not in result  # UA word form must not replace RU

    def test_size_token_updated(self):
        from app.views.matches import _apply_name_diff

        old_ua = "Слайсер RGV Lusso 200x300"
        new_ua = "Слайсер RGV Lusso 250x350"
        old_ru = "Слайсер RGV Lusso 200x300"
        result = _apply_name_diff(old_ua, new_ua, old_ru)
        assert "250x350" in result
        assert "200x300" not in result

    def test_no_changes_returns_original(self):
        from app.views.matches import _apply_name_diff

        name = "Фритюрниця Kogast EFT7"
        ru = "Фритюрница Kogast EFT7"
        result = _apply_name_diff(name, name, ru)
        assert result == ru

    def test_voltage_number_updated(self):
        from app.views.matches import _apply_name_diff

        old_ua = "Прес Fimar PF25E (220)"
        new_ua = "Прес Fimar PF25E (380)"
        old_ru = "Пресс Fimar PF25E (220)"
        result = _apply_name_diff(old_ua, new_ua, old_ru)
        assert "(380)" in result
