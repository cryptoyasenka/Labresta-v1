"""Regression tests for the 1pp ↔ 1 supplier invariant guard in matcher.

run_matching_for_supplier must NOT create a new candidate when the target
PP already has a non-rejected match (confirmed/manual/candidate) from any
SP of the same supplier. This blocks duplicate same-supplier candidates
that previously appeared when a supplier shipped two SP rows resolving to
the same catalog product (variants, in-feed dups, leftover external_ids).
"""

from __future__ import annotations

from app.models.catalog import PromProduct
from app.models.product_match import ProductMatch
from app.models.supplier import Supplier
from app.models.supplier_product import SupplierProduct
from app.services.matcher import run_matching_for_supplier


def _make_supplier(session, name="Maresto"):
    s = Supplier(name=name, feed_url=f"http://x/{name}.xml")
    session.add(s)
    session.flush()
    return s


def _make_sp(session, supplier, idx, name="Sirman Mantegna 300", brand="Sirman"):
    sp = SupplierProduct(
        supplier_id=supplier.id,
        external_id=f"sp-{supplier.id}-{idx}",
        name=name,
        brand=brand,
        price_cents=150000,
        available=True,
    )
    session.add(sp)
    session.flush()
    return sp


def _make_pp(session, idx, name="Sirman Mantegna 300", brand="Sirman"):
    pp = PromProduct(
        external_id=f"pp-{idx}",
        name=name,
        brand=brand,
        price=150000,
    )
    session.add(pp)
    session.flush()
    return pp


class TestSameSupplierInvariantGuard:
    def test_skips_pp_with_existing_confirmed_from_same_supplier(self, session):
        supplier = _make_supplier(session)
        pp = _make_pp(session, 0)
        sp_old = _make_sp(session, supplier, "old")
        sp_new = _make_sp(session, supplier, "new")
        session.add(ProductMatch(
            supplier_product_id=sp_old.id,
            prom_product_id=pp.id,
            score=100.0,
            status="confirmed",
        ))
        session.commit()

        run_matching_for_supplier(supplier.id)

        new_matches = session.query(ProductMatch).filter_by(
            supplier_product_id=sp_new.id,
        ).all()
        assert new_matches == [], (
            f"Expected no candidate created on a PP already claimed by same "
            f"supplier (confirmed). Got: "
            f"{[(m.prom_product_id, m.status) for m in new_matches]}"
        )

    def test_skips_pp_with_existing_candidate_from_same_supplier(self, session):
        supplier = _make_supplier(session)
        pp = _make_pp(session, 0)
        sp_first = _make_sp(session, supplier, "first")
        sp_second = _make_sp(session, supplier, "second")
        session.add(ProductMatch(
            supplier_product_id=sp_first.id,
            prom_product_id=pp.id,
            score=100.0,
            status="candidate",
        ))
        session.commit()

        run_matching_for_supplier(supplier.id)

        new_matches = session.query(ProductMatch).filter_by(
            supplier_product_id=sp_second.id,
        ).all()
        assert new_matches == [], (
            f"Expected no candidate when PP is already claimed by another "
            f"candidate from same supplier. Got: "
            f"{[(m.prom_product_id, m.status) for m in new_matches]}"
        )

    def test_allows_candidate_when_existing_match_is_rejected(self, session):
        supplier = _make_supplier(session)
        pp = _make_pp(session, 0)
        sp_old = _make_sp(session, supplier, "old")
        sp_new = _make_sp(session, supplier, "new")
        session.add(ProductMatch(
            supplier_product_id=sp_old.id,
            prom_product_id=pp.id,
            score=100.0,
            status="rejected",
        ))
        session.commit()

        run_matching_for_supplier(supplier.id)

        new_matches = session.query(ProductMatch).filter_by(
            supplier_product_id=sp_new.id,
        ).all()
        assert any(m.prom_product_id == pp.id for m in new_matches), (
            f"Rejected matches must not block re-matching. Got: "
            f"{[(m.prom_product_id, m.status) for m in new_matches]}"
        )

    def test_allows_candidate_from_different_supplier(self, session):
        sup_a = _make_supplier(session, "Maresto")
        sup_b = _make_supplier(session, "RP-Ukrayina")
        pp = _make_pp(session, 0)
        sp_a = _make_sp(session, sup_a, 0)
        sp_b = _make_sp(session, sup_b, 0)
        session.add(ProductMatch(
            supplier_product_id=sp_a.id,
            prom_product_id=pp.id,
            score=100.0,
            status="confirmed",
        ))
        session.commit()

        run_matching_for_supplier(sup_b.id)

        new_matches = session.query(ProductMatch).filter_by(
            supplier_product_id=sp_b.id,
        ).all()
        assert any(m.prom_product_id == pp.id for m in new_matches), (
            f"Cross-supplier alternatives must still be generated. Got: "
            f"{[(m.prom_product_id, m.status) for m in new_matches]}"
        )

    def test_first_seen_sp_within_run_wins_when_two_dups_arrive(self, session):
        supplier = _make_supplier(session)
        pp = _make_pp(session, 0)
        sp1 = _make_sp(session, supplier, "1")
        sp2 = _make_sp(session, supplier, "2")
        session.commit()

        run_matching_for_supplier(supplier.id)

        all_matches = (
            session.query(ProductMatch)
            .filter(ProductMatch.prom_product_id == pp.id)
            .filter(ProductMatch.supplier_product_id.in_([sp1.id, sp2.id]))
            .all()
        )
        assert len(all_matches) == 1, (
            f"Two same-supplier SPs against one PP must produce exactly one "
            f"candidate. Got: "
            f"{[(m.supplier_product_id, m.status) for m in all_matches]}"
        )
