"""Integration tests for /products/unmatched-catalog filters + operator decisions."""

import json

from app.models.catalog import PromProduct
from app.models.product_match import ProductMatch
from app.models.supplier import Supplier
from app.models.supplier_product import SupplierProduct


def _seed(session):
    """Seed: 2 suppliers, 4 PP, 2 SP, 1 confirmed + 1 candidate match."""
    sup_a = Supplier(
        name="SupplierA", feed_url="http://a.xml", discount_percent=0, is_enabled=True
    )
    sup_b = Supplier(
        name="SupplierB", feed_url="http://b.xml", discount_percent=0, is_enabled=True
    )
    session.add_all([sup_a, sup_b])
    session.flush()

    pp1 = PromProduct(
        external_id="P1",
        name="Hurakan HKN-A",
        brand="Hurakan",
        article="HKN-A",
        display_article="HKN-A DISP",
        price=10000,
    )
    pp2 = PromProduct(
        external_id="P2",
        name="Hurakan HKN-B",
        brand="Hurakan",
        article="HKN-B",
        price=20000,
    )
    pp3 = PromProduct(
        external_id="P3",
        name="Apach AP-C",
        brand="Apach",
        article="AP-C",
        price=30000,
    )
    pp4 = PromProduct(
        external_id="P4",
        name="Fagor FG-D",
        brand="Fagor",
        article="FG-D",
        price=40000,
    )
    session.add_all([pp1, pp2, pp3, pp4])
    session.flush()

    sp_a1 = SupplierProduct(
        supplier_id=sup_a.id,
        external_id="SA1",
        name="Hurakan HKN-A offer",
        brand="Hurakan",
        article="HKN-A",
        available=True,
    )
    sp_a2 = SupplierProduct(
        supplier_id=sup_a.id,
        external_id="SA2",
        name="Hurakan HKN-B offer",
        brand="Hurakan",
        article="HKN-B",
        available=True,
    )
    session.add_all([sp_a1, sp_a2])
    session.flush()

    # pp1 ↔ sp_a1 confirmed (pp1 should NOT appear in unmatched list for sup_a)
    session.add(ProductMatch(
        supplier_product_id=sp_a1.id,
        prom_product_id=pp1.id,
        status="confirmed",
        score=95,
    ))
    # pp2 ↔ sp_a2 candidate (pp2 IS unmatched but has candidate)
    session.add(ProductMatch(
        supplier_product_id=sp_a2.id,
        prom_product_id=pp2.id,
        status="candidate",
        score=80,
    ))
    session.commit()
    return {
        "sup_a": sup_a, "sup_b": sup_b,
        "pp1": pp1, "pp2": pp2, "pp3": pp3, "pp4": pp4,
        "sp_a1": sp_a1, "sp_a2": sp_a2,
    }


class TestUnmatchedCatalogGlobal:
    def test_excludes_confirmed_pp(self, client, session):
        s = _seed(session)
        resp = client.get("/products/unmatched-catalog")
        body = resp.data.decode("utf-8")
        # pp1 has confirmed → hidden; pp2/pp3/pp4 shown
        assert "HKN-A" not in body or s["pp1"].name not in body
        assert "HKN-B" in body
        assert "AP-C" in body
        assert "FG-D" in body

    def test_brand_filter(self, client, session):
        _seed(session)
        resp = client.get("/products/unmatched-catalog?brand=Hurakan")
        body = resp.data.decode("utf-8")
        assert "HKN-B" in body
        assert "AP-C" not in body
        assert "FG-D" not in body

    def test_search_by_article(self, client, session):
        _seed(session)
        resp = client.get("/products/unmatched-catalog?search=AP-C")
        body = resp.data.decode("utf-8")
        assert "AP-C" in body
        assert "HKN-B" not in body
        assert "FG-D" not in body

    def test_match_state_none_excludes_candidates(self, client, session):
        _seed(session)
        resp = client.get("/products/unmatched-catalog?match_state=none")
        body = resp.data.decode("utf-8")
        # pp2 has candidate → excluded; pp3/pp4 have none
        assert "HKN-B" not in body
        assert "AP-C" in body
        assert "FG-D" in body

    def test_match_state_candidate_only_pp2(self, client, session):
        _seed(session)
        resp = client.get("/products/unmatched-catalog?match_state=candidate")
        body = resp.data.decode("utf-8")
        assert "HKN-B" in body
        assert "AP-C" not in body
        assert "FG-D" not in body


class TestUnmatchedCatalogSupplierScope:
    def test_supplier_filter_includes_pp_not_matched_by_that_supplier(
        self, client, session
    ):
        s = _seed(session)
        # For supplier B: pp1 has confirmed only with supplier A, so relative
        # to B it IS unmatched and should appear.
        resp = client.get(f"/products/unmatched-catalog?supplier_id={s['sup_b'].id}")
        body = resp.data.decode("utf-8")
        assert "HKN-A" in body
        assert "HKN-B" in body
        assert "AP-C" in body
        assert "FG-D" in body

    def test_supplier_filter_hides_pp_confirmed_by_that_supplier(
        self, client, session
    ):
        s = _seed(session)
        resp = client.get(f"/products/unmatched-catalog?supplier_id={s['sup_a'].id}")
        body = resp.data.decode("utf-8")
        # pp1 has confirmed from sup_a → hidden
        # pp2 candidate only → still shown (candidate ≠ confirmed)
        assert "HKN-B" in body
        assert "AP-C" in body
        assert "FG-D" in body

    def test_supplier_brands_dropdown_restricted_to_supplier(self, client, session):
        s = _seed(session)
        resp = client.get(f"/products/unmatched-catalog?supplier_id={s['sup_a'].id}")
        body = resp.data.decode("utf-8")
        # sup_a has SP brand=Hurakan only
        assert 'value="Hurakan"' in body
        # Apach and Fagor are not in sup_a's offers
        assert 'value="Apach"' not in body
        assert 'value="Fagor"' not in body


class TestOperatorDecision:
    def test_set_decision_stores_value(self, client, session):
        s = _seed(session)
        resp = client.post(
            f"/products/catalog/{s['pp3'].id}/set-decision",
            data=json.dumps({"decision": "needs_delete", "note": "никто не везёт"}),
            content_type="application/json",
        )
        assert resp.status_code == 200
        session.expire_all()
        pp = session.get(PromProduct, s["pp3"].id)
        assert pp.operator_decision == "needs_delete"
        assert pp.operator_decision_note == "никто не везёт"
        assert pp.operator_decision_at is not None

    def test_set_decision_rejects_invalid_value(self, client, session):
        s = _seed(session)
        resp = client.post(
            f"/products/catalog/{s['pp3'].id}/set-decision",
            data=json.dumps({"decision": "hack_db"}),
            content_type="application/json",
        )
        assert resp.status_code == 400

    def test_clear_decision_resets(self, client, session):
        s = _seed(session)
        # Pre-set a decision
        s["pp3"].operator_decision = "needs_request"
        s["pp3"].operator_decision_note = "call them"
        session.commit()

        resp = client.post(f"/products/catalog/{s['pp3'].id}/clear-decision")
        assert resp.status_code == 200
        session.expire_all()
        pp = session.get(PromProduct, s["pp3"].id)
        assert pp.operator_decision is None
        assert pp.operator_decision_note is None

    def test_decision_filter_pending_vs_reviewed(self, client, session):
        s = _seed(session)
        s["pp3"].operator_decision = "needs_delete"
        session.commit()

        # pending → hides pp3 (which has a decision)
        resp = client.get("/products/unmatched-catalog?decision=pending")
        body = resp.data.decode("utf-8")
        assert "AP-C" not in body
        assert "FG-D" in body

        # reviewed → shows only pp3
        resp = client.get("/products/unmatched-catalog?decision=reviewed")
        body = resp.data.decode("utf-8")
        assert "AP-C" in body
        assert "FG-D" not in body

    def test_decision_filter_exact_value(self, client, session):
        s = _seed(session)
        s["pp3"].operator_decision = "needs_delete"
        s["pp4"].operator_decision = "needs_request"
        session.commit()

        resp = client.get("/products/unmatched-catalog?decision=needs_delete")
        body = resp.data.decode("utf-8")
        assert "AP-C" in body
        assert "FG-D" not in body
