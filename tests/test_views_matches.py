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


class TestManualMatchEndpoint:
    """POST /matches/manual — must not hit UNIQUE constraint when the
    (supplier, prom) pair is already confirmed elsewhere."""

    def test_duplicate_pair_returns_409(self, client, db):
        # Seed one confirmed match for a (sp, pp) pair, then try to manual-match
        # the same pair again — must return 409, not 500.
        match, sp, pp = _seed_confirmed_match(db.session, status="confirmed")

        # Seed a lingering candidate for the same supplier_product pointing to
        # a DIFFERENT catalog entry, simulating stale queue state.
        other_pp = PromProduct(external_id="PP_OTHER", name="Other", brand="TestBrand")
        db.session.add(other_pp)
        db.session.flush()
        dangling = ProductMatch(
            supplier_product_id=sp.id, prom_product_id=other_pp.id,
            score=80.0, status="candidate",
        )
        db.session.add(dangling)
        db.session.commit()
        sp_id, pp_id, match_id, dangling_id = sp.id, pp.id, match.id, dangling.id

        resp = client.post(
            "/matches/manual",
            json={"supplier_product_id": sp_id, "prom_product_id": pp_id},
        )
        assert resp.status_code == 409
        data = resp.get_json()
        assert data["status"] == "already_matched"
        assert data["match_id"] == match_id

        db.session.expire_all()
        assert db.session.get(ProductMatch, dangling_id) is None
        refreshed = db.session.get(ProductMatch, match_id)
        assert refreshed.status == "confirmed"


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

    def test_digit_token_not_replaced_inside_larger_number(self):
        """Regression: `12` -> `13` must not corrupt `121` or `1200` elsewhere
        in the RU string. Old substring-replace would produce `131` / `1300`."""
        from app.views.matches import _apply_name_diff

        old_ua = "Модель 12 шт 121 упаковка 1200"
        new_ua = "Модель 13 шт 121 упаковка 1200"
        old_ru = "Модель 12 шт 121 упаковка 1200"
        result = _apply_name_diff(old_ua, new_ua, old_ru)
        assert "Модель 13" in result
        assert "121" in result
        assert "1200" in result
        assert "131" not in result
        assert "1300" not in result

    def test_digit_token_not_replaced_inside_alphanumeric(self):
        """`60` -> `80` must not touch `XFT60UTE` — model codes are not just digits."""
        from app.views.matches import _apply_name_diff

        old_ua = "Піч 60 см XFT60UTE"
        new_ua = "Піч 80 см XFT60UTE"
        old_ru = "Печь 60 см XFT60UTE"
        result = _apply_name_diff(old_ua, new_ua, old_ru)
        assert "Печь 80 см" in result
        assert "XFT60UTE" in result


# ===== 1 pp ↔ 1 confirmed/manual supplier match invariant =====


def _seed_second_sp_and_candidate(session, pp, *, brand="TestBrand", name="Кавомашина Test 220 Extra"):
    supplier = pp.__table__  # dummy — not used
    sp2 = SupplierProduct(
        supplier_id=1,  # reuse seeded supplier
        external_id="SP2",
        name=name,
        brand=brand,
        price_cents=55000,
        available=True,
        needs_review=False,
    )
    session.add(sp2)
    session.flush()
    cand = ProductMatch(
        supplier_product_id=sp2.id,
        prom_product_id=pp.id,
        score=90.0,
        status="candidate",
    )
    session.add(cand)
    session.commit()
    return sp2, cand


class TestPpClaimInvariant:
    def test_confirm_second_match_on_claimed_pp_returns_409(self, client, db):
        _, _, pp = _seed_confirmed_match(db.session, status="confirmed")
        _, cand = _seed_second_sp_and_candidate(db.session, pp)
        resp = client.post(f"/matches/{cand.id}/confirm")
        assert resp.status_code == 409
        body = resp.get_json()
        assert body["code"] == "prom_already_claimed"
        # Candidate must remain candidate
        db.session.refresh(cand)
        assert cand.status == "candidate"

    def test_confirm_update_on_claimed_pp_returns_409(self, client, db):
        _, _, pp = _seed_confirmed_match(db.session, status="confirmed")
        _, cand = _seed_second_sp_and_candidate(db.session, pp)
        resp = client.post(f"/matches/{cand.id}/confirm-update")
        assert resp.status_code == 409
        db.session.refresh(cand)
        assert cand.status == "candidate"

    def test_manual_match_on_claimed_pp_returns_409(self, client, db):
        m, _, pp = _seed_confirmed_match(db.session, status="confirmed")
        sp2 = SupplierProduct(
            supplier_id=1,
            external_id="SP3",
            name="Other sp",
            brand="Other",
            price_cents=40000,
            available=True,
            needs_review=False,
        )
        db.session.add(sp2)
        db.session.commit()
        resp = client.post(
            "/matches/manual",
            json={"supplier_product_id": sp2.id, "prom_product_id": pp.id},
        )
        assert resp.status_code == 409
        body = resp.get_json()
        assert body.get("code") == "prom_already_claimed"

    def test_bulk_confirm_skips_claimed_pp(self, client, db):
        _, _, pp = _seed_confirmed_match(db.session, status="confirmed")
        _, cand = _seed_second_sp_and_candidate(db.session, pp)
        resp = client.post(
            "/matches/bulk-action",
            json={"action": "confirm", "ids": [cand.id]},
        )
        assert resp.status_code == 200
        body = resp.get_json()
        assert body["processed"] == 0
        assert len(body["skipped_claimed"]) == 1
        db.session.refresh(cand)
        assert cand.status == "candidate"

    def test_confirming_self_still_works(self, client, db):
        """An already-confirmed match re-POSTed to /confirm doesn't flag itself."""
        m, _, _ = _seed_confirmed_match(db.session, status="confirmed")
        # Manually revert to candidate to simulate a re-confirm attempt
        m.status = "candidate"
        db.session.commit()
        resp = client.post(f"/matches/{m.id}/confirm")
        assert resp.status_code == 200


class TestUnpublishRepublishEndpoints:
    """Phase C — toggle ProductMatch.published without losing the match row."""

    def test_unpublish_sets_published_false(self, client, db):
        m, _, _ = _seed_confirmed_match(db.session, status="confirmed")
        m.published = True
        m.in_feed = True
        db.session.commit()
        mid = m.id

        resp = client.post(f"/matches/{mid}/unpublish")
        assert resp.status_code == 200
        body = resp.get_json()
        assert body["status"] == "ok"
        assert body["published"] is False

        refreshed = db.session.get(ProductMatch, mid)
        assert refreshed.published is False
        assert refreshed.in_feed is False
        assert refreshed.status == "confirmed"  # match row preserved

    def test_unpublish_idempotent(self, client, db):
        m, _, _ = _seed_confirmed_match(db.session, status="confirmed")
        m.published = False
        db.session.commit()

        resp = client.post(f"/matches/{m.id}/unpublish")
        assert resp.status_code == 200
        assert resp.get_json().get("already") is True

    def test_republish_sets_published_true(self, client, db):
        m, _, _ = _seed_confirmed_match(db.session, status="confirmed")
        m.published = False
        db.session.commit()

        resp = client.post(f"/matches/{m.id}/republish")
        assert resp.status_code == 200
        assert resp.get_json()["published"] is True

        refreshed = db.session.get(ProductMatch, m.id)
        assert refreshed.published is True

    def test_unpublish_rejected_match_returns_400(self, client, db):
        m, _, _ = _seed_confirmed_match(db.session, status="confirmed")
        m.status = "rejected"
        db.session.commit()
        resp = client.post(f"/matches/{m.id}/unpublish")
        assert resp.status_code == 400

    def test_unpublish_missing_returns_404(self, client, db):
        resp = client.post("/matches/99999/unpublish")
        assert resp.status_code == 404


class TestRegenerateFeedEndpoint:
    def test_regenerate_returns_stats(self, client, db, app, tmp_path):
        _seed_confirmed_match(db.session, status="confirmed")
        app.config["YML_OUTPUT_DIR"] = str(tmp_path)
        app.config["YML_FILENAME"] = "regen-test.yml"

        resp = client.post("/matches/regenerate-feed")
        assert resp.status_code == 200
        body = resp.get_json()
        assert body["status"] == "ok"
        assert body["total"] == 1
        assert "available" in body
        assert "path" in body


class TestSyncPricesEndpoint:
    """Phase D — POST /matches/sync-prices."""

    def _setup(self, app, tmp_path):
        app.config["YML_OUTPUT_DIR"] = str(tmp_path)
        app.config["YML_PRICES_FILENAME"] = "test-prices.yml"

    def test_bulk_sync_returns_stats(self, client, db, app, tmp_path):
        self._setup(app, tmp_path)
        m, _, _ = _seed_confirmed_match(db.session, status="confirmed")

        resp = client.post("/matches/sync-prices")
        assert resp.status_code == 200
        body = resp.get_json()
        assert body["status"] == "ok"
        assert body["total"] == 1
        assert body["skipped"] == 0
        assert "synced_at" in body

        refreshed = db.session.get(ProductMatch, m.id)
        assert refreshed.price_synced_at is not None

    def test_subset_sync_via_match_ids(self, client, db, app, tmp_path):
        self._setup(app, tmp_path)
        m1, _, _ = _seed_confirmed_match(db.session, status="confirmed")
        resp = client.post(
            "/matches/sync-prices",
            json={"match_ids": [m1.id]},
        )
        assert resp.status_code == 200
        body = resp.get_json()
        assert body["total"] == 1

    def test_empty_body_treated_as_bulk(self, client, db, app, tmp_path):
        self._setup(app, tmp_path)
        _seed_confirmed_match(db.session, status="confirmed")
        # Plain POST with no body must still succeed as bulk
        resp = client.post("/matches/sync-prices")
        assert resp.status_code == 200


class TestSyncAvailabilityEndpoint:
    """Phase D — POST /matches/sync-availability."""

    def _setup(self, app, tmp_path):
        app.config["YML_OUTPUT_DIR"] = str(tmp_path)
        app.config["YML_AVAILABILITY_FILENAME"] = "test-avail.yml"

    def test_bulk_sync_returns_stats(self, client, db, app, tmp_path):
        self._setup(app, tmp_path)
        m, _, _ = _seed_confirmed_match(db.session, status="confirmed")

        resp = client.post("/matches/sync-availability")
        assert resp.status_code == 200
        body = resp.get_json()
        assert body["status"] == "ok"
        assert body["total"] == 1
        assert body["available"] == 1
        assert body["unavailable"] == 0
        assert "synced_at" in body

        refreshed = db.session.get(ProductMatch, m.id)
        assert refreshed.availability_synced_at is not None
        # price timestamp must NOT be touched
        assert refreshed.price_synced_at is None

    def test_subset_sync_via_match_ids(self, client, db, app, tmp_path):
        self._setup(app, tmp_path)
        m1, _, _ = _seed_confirmed_match(db.session, status="confirmed")
        resp = client.post(
            "/matches/sync-availability",
            json={"match_ids": [m1.id]},
        )
        assert resp.status_code == 200
        assert resp.get_json()["total"] == 1


class TestNarrowFeedServing:
    """Phase D — /feed/prices.yml and /feed/availability.yml serve the files."""

    def test_prices_feed_404_before_generated(self, client, app, tmp_path):
        app.config["YML_OUTPUT_DIR"] = str(tmp_path)
        app.config["YML_PRICES_FILENAME"] = "nonexistent-prices.yml"
        resp = client.get("/feed/prices.yml")
        assert resp.status_code == 404

    def test_availability_feed_404_before_generated(self, client, app, tmp_path):
        app.config["YML_OUTPUT_DIR"] = str(tmp_path)
        app.config["YML_AVAILABILITY_FILENAME"] = "nonexistent-avail.yml"
        resp = client.get("/feed/availability.yml")
        assert resp.status_code == 404

    def test_prices_feed_served_after_sync(self, client, db, app, tmp_path):
        app.config["YML_OUTPUT_DIR"] = str(tmp_path)
        app.config["YML_PRICES_FILENAME"] = "served-prices.yml"
        _seed_confirmed_match(db.session, status="confirmed")
        client.post("/matches/sync-prices")

        resp = client.get("/feed/prices.yml")
        assert resp.status_code == 200
        assert resp.mimetype == "application/xml"
        assert b"<yml_catalog" in resp.data


def _seed_second_sp(session, *, name="Другой товар", supplier_name="OtherSupplier",
                    external_id="SP2", brand="TestBrand", price_cents=40000,
                    article=None, available=True):
    """Add a second supplier+SP (for rebind tests) to an existing scenario."""
    sup = Supplier(
        name=supplier_name,
        feed_url="http://other.xml",
        discount_percent=0,
        is_enabled=True,
    )
    session.add(sup)
    session.flush()
    sp = SupplierProduct(
        supplier_id=sup.id,
        external_id=external_id,
        name=name,
        brand=brand,
        article=article,
        price_cents=price_cents,
        available=available,
        needs_review=False,
    )
    session.add(sp)
    session.commit()
    return sp


class TestSearchSuppliersEndpoint:
    """Phase E — GET /matches/search-suppliers."""

    def test_short_query_returns_empty(self, client, db):
        _seed_confirmed_match(db.session)
        resp = client.get("/matches/search-suppliers?q=x")
        assert resp.status_code == 200
        assert resp.get_json() == []

    def test_finds_by_name(self, client, db):
        _seed_confirmed_match(db.session)
        _seed_second_sp(db.session, name="Уникальный миксер Robot")
        resp = client.get("/matches/search-suppliers?q=Уникальный")
        data = resp.get_json()
        assert len(data) == 1
        assert data[0]["name"] == "Уникальный миксер Robot"
        assert data[0]["supplier_name"] == "OtherSupplier"

    def test_finds_by_external_id(self, client, db):
        _seed_confirmed_match(db.session)
        _seed_second_sp(db.session, external_id="ABC-12345")
        resp = client.get("/matches/search-suppliers?q=ABC-12345")
        assert len(resp.get_json()) == 1

    def test_finds_by_article(self, client, db):
        _seed_confirmed_match(db.session)
        _seed_second_sp(db.session, article="ART-999")
        resp = client.get("/matches/search-suppliers?q=ART-999")
        assert len(resp.get_json()) == 1

    def test_excludes_deleted(self, client, db):
        _seed_confirmed_match(db.session)
        sp = _seed_second_sp(db.session, name="Удалённый товар")
        sp.is_deleted = True
        db.session.commit()
        resp = client.get("/matches/search-suppliers?q=Удалённый")
        assert resp.get_json() == []

    def test_includes_active_match_metadata(self, client, db):
        """SP already in a confirmed match must surface its active_match_* fields."""
        _, sp, pp = _seed_confirmed_match(db.session)
        resp = client.get(f"/matches/search-suppliers?q={sp.name[:10]}")
        data = resp.get_json()
        hit = [r for r in data if r["id"] == sp.id][0]
        assert hit["active_match_id"] is not None
        assert hit["active_match_pp_id"] == pp.id
        assert hit["active_match_status"] == "confirmed"


class TestRebindEndpoint:
    """Phase E — POST /matches/<id>/rebind."""

    def test_rebind_swaps_sp(self, client, db):
        match, sp_old, pp = _seed_confirmed_match(db.session, status="confirmed")
        sp_new = _seed_second_sp(db.session)
        mid = match.id

        resp = client.post(
            f"/matches/{mid}/rebind",
            json={"new_supplier_product_id": sp_new.id},
        )
        assert resp.status_code == 200
        body = resp.get_json()
        assert body["status"] == "ok"
        new_id = body["new_match_id"]

        # Old match rejected, unpublished; pp claim released.
        old = db.session.get(ProductMatch, mid)
        assert old.status == "rejected"
        assert old.published is False
        assert old.confirmed_by.startswith("rebind:")

        # New match confirmed on same pp.
        new = db.session.get(ProductMatch, new_id)
        assert new.status == "manual"
        assert new.supplier_product_id == sp_new.id
        assert new.prom_product_id == pp.id
        assert new.published is True
        assert new.price_synced_at is None
        assert new.availability_synced_at is None

    def test_rebind_upgrades_existing_candidate_pair(self, client, db):
        """If (new_sp, target_pp) exists as candidate, upgrade in place."""
        match, _, pp = _seed_confirmed_match(db.session, status="confirmed")
        sp_new = _seed_second_sp(db.session)
        # Pre-existing candidate row on the target pair
        existing = ProductMatch(
            supplier_product_id=sp_new.id,
            prom_product_id=pp.id,
            score=72.0,
            status="candidate",
        )
        db.session.add(existing)
        db.session.commit()
        existing_id = existing.id

        resp = client.post(
            f"/matches/{match.id}/rebind",
            json={"new_supplier_product_id": sp_new.id},
        )
        assert resp.status_code == 200
        body = resp.get_json()
        assert body["new_match_id"] == existing_id

        upgraded = db.session.get(ProductMatch, existing_id)
        assert upgraded.status == "manual"
        assert upgraded.score == 100.0

    def test_rebind_rejects_candidate_match_as_source(self, client, db):
        """Can only rebind from confirmed/manual matches."""
        match, _, _ = _seed_confirmed_match(db.session, status="confirmed")
        match.status = "candidate"
        db.session.commit()
        sp_new = _seed_second_sp(db.session)

        resp = client.post(
            f"/matches/{match.id}/rebind",
            json={"new_supplier_product_id": sp_new.id},
        )
        assert resp.status_code == 400

    def test_rebind_requires_new_supplier_product_id(self, client, db):
        match, _, _ = _seed_confirmed_match(db.session)
        resp = client.post(f"/matches/{match.id}/rebind", json={})
        assert resp.status_code == 400

    def test_rebind_rejects_same_sp(self, client, db):
        match, sp_old, _ = _seed_confirmed_match(db.session)
        resp = client.post(
            f"/matches/{match.id}/rebind",
            json={"new_supplier_product_id": sp_old.id},
        )
        assert resp.status_code == 400

    def test_rebind_404_on_missing_sp(self, client, db):
        match, _, _ = _seed_confirmed_match(db.session)
        resp = client.post(
            f"/matches/{match.id}/rebind",
            json={"new_supplier_product_id": 99999},
        )
        assert resp.status_code == 404

    def test_rebind_409_when_new_sp_claims_different_pp(self, client, db):
        """If the new SP is already confirmed on a DIFFERENT pp, refuse."""
        match, _, _ = _seed_confirmed_match(db.session)
        sp_new = _seed_second_sp(db.session)

        other_pp = PromProduct(
            external_id="OTHER_PP",
            name="Другой каталог",
            brand="TestBrand",
            price=30000,
        )
        db.session.add(other_pp)
        db.session.flush()

        other_match = ProductMatch(
            supplier_product_id=sp_new.id,
            prom_product_id=other_pp.id,
            score=100.0,
            status="confirmed",
            confirmed_at=datetime.now(timezone.utc),
            confirmed_by="seed",
        )
        db.session.add(other_match)
        db.session.commit()

        resp = client.post(
            f"/matches/{match.id}/rebind",
            json={"new_supplier_product_id": sp_new.id},
        )
        assert resp.status_code == 409

    def test_rebind_creates_audit_entry(self, client, db):
        from app.models.audit_log import AuditLog
        match, _, _ = _seed_confirmed_match(db.session)
        sp_new = _seed_second_sp(db.session)

        resp = client.post(
            f"/matches/{match.id}/rebind",
            json={"new_supplier_product_id": sp_new.id},
        )
        assert resp.status_code == 200

        entry = (
            AuditLog.query.filter_by(action="rebind")
            .order_by(AuditLog.id.desc())
            .first()
        )
        assert entry is not None
        assert entry.prom_product_id == match.prom_product_id


class TestRebindUIRender:
    """Phase E UI — review page renders rebind button + modal."""

    def test_rebind_button_on_confirmed_match(self, client, db):
        _seed_confirmed_match(db.session, status="confirmed")
        resp = client.get("/matches/?status=confirmed")
        assert resp.status_code == 200
        body = resp.data.decode("utf-8")
        assert "rebind-btn" in body
        assert "Переподвязать" in body
        assert 'id="rebindModal"' in body

    def test_rebind_button_on_manual_match(self, client, db):
        _seed_confirmed_match(db.session, status="manual")
        resp = client.get("/matches/?status=manual")
        assert resp.status_code == 200
        assert "rebind-btn" in resp.data.decode("utf-8")

    def test_no_rebind_button_on_candidate(self, client, db):
        _seed_confirmed_match(db.session, status="candidate")
        resp = client.get("/matches/?status=candidate")
        assert resp.status_code == 200
        body = resp.data.decode("utf-8")
        # Modal HTML is always present on the page; the per-row button isn't.
        assert "rebind-btn" not in body
