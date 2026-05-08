"""Phase L — conflict resolution UX for bulk-confirm.

Covers:
- Enriched `skipped_claimed` payload from /matches/bulk-action when a
  candidate's PP is already claimed (supplier names, sp_name, sp_article,
  scores, pp_name).
- POST /matches/resolve-conflict with action='keep' (rejects candidate,
  keeps existing) and 'switch' (unconfirms existing, confirms candidate,
  no discount carry-over).
- Idempotency / 409 / 400 / 404 edge cases.
"""

from datetime import datetime, timezone

from app.models.catalog import PromProduct
from app.models.product_match import ProductMatch
from app.models.supplier import Supplier
from app.models.supplier_product import SupplierProduct


def _two_suppliers_with_conflict(session):
    """Seed: 1 PP, 2 suppliers, each with 1 SP. SP1 confirmed on the PP,
    SP2 has a candidate match on the same PP — exactly the Phase L bulk
    conflict scenario.

    Returns (existing_match, candidate_match, sup1, sup2, sp1, sp2, pp).
    """
    sup1 = Supplier(
        name="MARESTO",
        feed_url="http://maresto.test/p.xml",
        discount_percent=0,
        is_enabled=True,
    )
    sup2 = Supplier(
        name="Новый Проект",
        feed_url="http://np.test/p.xml",
        discount_percent=0,
        is_enabled=True,
    )
    session.add_all([sup1, sup2])
    session.flush()

    sp1 = SupplierProduct(
        supplier_id=sup1.id,
        external_id="MR-1",
        name="Термопакувальний апарат SIRMAN 45К СЕ",
        article="40602300",
        brand="SIRMAN",
        price_cents=120000,
        available=True,
        needs_review=False,
    )
    sp2 = SupplierProduct(
        supplier_id=sup2.id,
        external_id="NP-1",
        name="Термопакувальний апарат Sirman 45к се",
        article="40602300",
        brand="SIRMAN",
        price_cents=118000,
        available=True,
        needs_review=False,
    )
    pp = PromProduct(
        external_id="PP-SIR",
        name="ТЕРМОПАКУВАЛЬНИЙ АПАРАТ SIRMAN 45К СЕ",
        name_ru="Термоупаковочный аппарат SIRMAN 45К СЕ",
        brand="SIRMAN",
        price=150000,
    )
    session.add_all([sp1, sp2, pp])
    session.flush()

    existing = ProductMatch(
        supplier_product_id=sp1.id,
        prom_product_id=pp.id,
        score=95.0,
        status="confirmed",
        confirmed_at=datetime.now(timezone.utc),
        confirmed_by="seed",
    )
    candidate = ProductMatch(
        supplier_product_id=sp2.id,
        prom_product_id=pp.id,
        score=100.0,
        status="candidate",
    )
    session.add_all([existing, candidate])
    session.commit()
    return existing, candidate, sup1, sup2, sp1, sp2, pp


# ----- Enriched payload from /bulk-action -----


class TestBulkConfirmEnrichedSkippedPayload:
    def test_skipped_claimed_includes_supplier_and_sp_details(self, client, db):
        existing, candidate, sup1, sup2, sp1, sp2, pp = _two_suppliers_with_conflict(
            db.session
        )
        resp = client.post(
            "/matches/bulk-action",
            json={"action": "confirm", "ids": [candidate.id]},
        )
        assert resp.status_code == 200
        body = resp.get_json()
        assert body["processed"] == 0
        assert len(body["skipped_claimed"]) == 1
        entry = body["skipped_claimed"][0]
        # Top-level identifiers (back-compat with pre-Phase-L consumers)
        assert entry["match_id"] == candidate.id
        assert entry["prom_product_id"] == pp.id
        assert entry["existing_match_id"] == existing.id
        # Phase L additions
        assert entry["pp_name"] == pp.name
        assert entry["existing"]["match_id"] == existing.id
        assert entry["existing"]["supplier_name"] == sup1.name
        assert entry["existing"]["sp_name"] == sp1.name
        assert entry["existing"]["sp_article"] == sp1.article
        assert entry["existing"]["score"] == 95.0
        assert entry["candidate"]["supplier_name"] == sup2.name
        assert entry["candidate"]["sp_name"] == sp2.name
        assert entry["candidate"]["sp_article"] == sp2.article
        assert entry["candidate"]["score"] == 100.0


# ----- /resolve-conflict — keep -----


class TestResolveConflictKeep:
    def test_keep_rejects_candidate_and_preserves_existing(self, client, db):
        existing, candidate, *_ = _two_suppliers_with_conflict(db.session)
        existing_id = existing.id
        cand_id = candidate.id

        resp = client.post(
            "/matches/resolve-conflict",
            json={"candidate_match_id": cand_id, "action": "keep"},
        )
        assert resp.status_code == 200
        body = resp.get_json()
        assert body["status"] == "ok"
        assert body["new_status"] == "rejected"
        assert body["candidate_match_id"] == cand_id
        assert body["existing_match_id"] == existing_id

        db.session.expire_all()
        cand = db.session.get(ProductMatch, cand_id)
        ex = db.session.get(ProductMatch, existing_id)
        assert cand.status == "rejected"
        assert (cand.confirmed_by or "").startswith("conflict-keep:")
        assert ex.status == "confirmed"  # untouched
        assert ex.confirmed_by == "seed"  # untouched


# ----- /resolve-conflict — switch -----


class TestResolveConflictSwitch:
    def test_switch_unconfirms_existing_and_confirms_candidate(self, client, db):
        existing, candidate, *_ = _two_suppliers_with_conflict(db.session)
        existing_id = existing.id
        cand_id = candidate.id

        resp = client.post(
            "/matches/resolve-conflict",
            json={"candidate_match_id": cand_id, "action": "switch"},
        )
        assert resp.status_code == 200
        body = resp.get_json()
        assert body["status"] == "ok"
        assert body["new_status"] == "confirmed"

        db.session.expire_all()
        cand = db.session.get(ProductMatch, cand_id)
        ex = db.session.get(ProductMatch, existing_id)
        assert cand.status == "confirmed"
        assert cand.confirmed_at is not None
        assert cand.confirmed_by == "Test User"  # from conftest fixture
        assert ex.status == "candidate"
        assert ex.confirmed_at is None
        assert ex.confirmed_by is None

    def test_switch_does_not_carry_over_discount_percent(self, client, db):
        """Per Yana 2026-04-22: each supplier has its own margins, so the
        new confirmed match starts from supplier defaults (NULL), not the
        previously-confirmed match's override."""
        existing, candidate, *_ = _two_suppliers_with_conflict(db.session)
        existing.discount_percent = 12.5  # MARESTO had a per-product override
        db.session.commit()
        cand_id = candidate.id

        resp = client.post(
            "/matches/resolve-conflict",
            json={"candidate_match_id": cand_id, "action": "switch"},
        )
        assert resp.status_code == 200
        db.session.expire_all()
        cand = db.session.get(ProductMatch, cand_id)
        assert cand.discount_percent is None  # fresh defaults

    def test_switch_cleans_orphan_candidates_on_same_sp(self, client, db):
        """If the now-confirmed SP had other candidate matches against
        unrelated PPs, those become orphan rows (1 SP ↔ 1 confirmed PP).
        Cleanup matches the bulk-confirm path so the UI doesn't keep
        showing dead candidates."""
        existing, candidate, sup1, sup2, sp1, sp2, pp = (
            _two_suppliers_with_conflict(db.session)
        )
        # A second PP with a candidate match against sp2 — should be
        # deleted on switch.
        pp_other = PromProduct(
            external_id="PP-OTHER",
            name="Other product",
            brand="SIRMAN",
            price=99000,
        )
        db.session.add(pp_other)
        db.session.flush()
        orphan = ProductMatch(
            supplier_product_id=sp2.id,
            prom_product_id=pp_other.id,
            score=70.0,
            status="candidate",
        )
        db.session.add(orphan)
        db.session.commit()
        orphan_id = orphan.id

        resp = client.post(
            "/matches/resolve-conflict",
            json={"candidate_match_id": candidate.id, "action": "switch"},
        )
        assert resp.status_code == 200
        assert db.session.get(ProductMatch, orphan_id) is None


# ----- Edge cases -----


class TestResolveConflictEdges:
    def test_invalid_action_returns_400(self, client, db):
        _, candidate, *_ = _two_suppliers_with_conflict(db.session)
        resp = client.post(
            "/matches/resolve-conflict",
            json={"candidate_match_id": candidate.id, "action": "bogus"},
        )
        assert resp.status_code == 400

    def test_missing_candidate_match_id_returns_400(self, client, db):
        resp = client.post(
            "/matches/resolve-conflict",
            json={"action": "keep"},
        )
        assert resp.status_code == 400

    def test_unknown_candidate_returns_404(self, client, db):
        resp = client.post(
            "/matches/resolve-conflict",
            json={"candidate_match_id": 999999, "action": "keep"},
        )
        assert resp.status_code == 404

    def test_candidate_already_confirmed_returns_409(self, client, db):
        """Idempotency: if the candidate has already been resolved by
        another bulk run / operator click, refuse with 409 instead of
        silently re-applying."""
        _, candidate, *_ = _two_suppliers_with_conflict(db.session)
        candidate.status = "confirmed"
        db.session.commit()
        resp = client.post(
            "/matches/resolve-conflict",
            json={"candidate_match_id": candidate.id, "action": "switch"},
        )
        assert resp.status_code == 409
        body = resp.get_json()
        assert body.get("code") == "candidate_not_in_candidate_state"
        assert body.get("current_status") == "confirmed"

    def test_candidate_already_rejected_returns_409(self, client, db):
        _, candidate, *_ = _two_suppliers_with_conflict(db.session)
        candidate.status = "rejected"
        db.session.commit()
        resp = client.post(
            "/matches/resolve-conflict",
            json={"candidate_match_id": candidate.id, "action": "keep"},
        )
        assert resp.status_code == 409

    def test_switch_with_no_existing_claim_just_confirms(self, client, db):
        """Race scenario: existing match was unconfirmed between bulk-action
        and resolve-conflict. Switch should still confirm the candidate."""
        _, candidate, sup1, sup2, sp1, sp2, pp = _two_suppliers_with_conflict(
            db.session
        )
        # Simulate: existing match was unconfirmed (e.g. another operator
        # rebound it).
        existing = db.session.execute(
            ProductMatch.query.filter_by(supplier_product_id=sp1.id).statement
        ).scalar_one()
        existing.status = "candidate"
        existing.confirmed_at = None
        existing.confirmed_by = None
        db.session.commit()

        resp = client.post(
            "/matches/resolve-conflict",
            json={"candidate_match_id": candidate.id, "action": "switch"},
        )
        assert resp.status_code == 200
        db.session.expire_all()
        cand = db.session.get(ProductMatch, candidate.id)
        assert cand.status == "confirmed"
