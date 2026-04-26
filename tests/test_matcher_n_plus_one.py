"""Regression tests for N+1 SELECTs in batch matching paths.

These guard the preload optimisations in:
  - matcher.run_matching_for_supplier  (matcher.py: existing-pair preload)
  - rule_matcher.apply_match_rules     (rule_matcher.py: prom + pair preload)

Strategy: count SELECT statements via sqlalchemy.event.listen on
before_cursor_execute, run the function twice at different scales, assert
the SELECT count grew by at most a small constant. Anything that scales
linearly with the number of supplier products signals a regression.
"""

from __future__ import annotations

from contextlib import contextmanager

import pytest
from sqlalchemy import event

from app.extensions import db
from app.models.catalog import PromProduct
from app.models.match_rule import MatchRule
from app.models.product_match import ProductMatch
from app.models.supplier import Supplier
from app.models.supplier_product import SupplierProduct
from app.services.matcher import run_matching_for_supplier
from app.services.rule_matcher import apply_match_rules


@contextmanager
def count_selects():
    """Yield a list whose only entry is the SELECT count seen during the block.

    INSERT/UPDATE/DELETE/COMMIT/PRAGMA traffic is excluded — those are O(work
    done), not the N+1 leak we're guarding against.
    """
    holder = [0]
    bind = db.session.get_bind()

    def _on_exec(conn, cursor, statement, parameters, context, executemany):
        if statement.lstrip().upper().startswith("SELECT"):
            holder[0] += 1

    event.listen(bind, "before_cursor_execute", _on_exec)
    try:
        yield holder
    finally:
        event.remove(bind, "before_cursor_execute", _on_exec)


def _make_supplier(session, name):
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


class TestRunMatchingForSupplierNoNPlusOne:
    """matcher.run_matching_for_supplier must not scale SELECT count with SP."""

    def test_select_count_does_not_grow_linearly_with_sp_count(self, session):
        # Baseline: small supplier (5 SP) against the same PP catalog.
        small_supplier = _make_supplier(session, "small")
        for i in range(5):
            _make_sp(session, small_supplier, i)
        # Catalog of 30 PP (size-of-catalog is constant across both runs;
        # we vary only SP count to isolate per-SP query growth).
        for i in range(30):
            _make_pp(session, i)
        session.commit()

        with count_selects() as small_count:
            run_matching_for_supplier(small_supplier.id)
        baseline = small_count[0]

        # Larger supplier: 25 SP — 5x the baseline.
        big_supplier = _make_supplier(session, "big")
        for i in range(25):
            _make_sp(session, big_supplier, i)
        session.commit()

        with count_selects() as big_count:
            run_matching_for_supplier(big_supplier.id)
        scaled = big_count[0]

        # If we had an N+1, scaled would be roughly baseline + 20*K. A handful
        # of extra SELECTs are fine (e.g. SQLite housekeeping, deferred PP
        # autoload). Anything north of +5 is suspicious.
        assert scaled - baseline <= 5, (
            f"run_matching_for_supplier looks N+1: "
            f"5 SP -> {baseline} selects, 25 SP -> {scaled} selects "
            f"(delta {scaled - baseline}, expected <= 5)"
        )

    def test_existing_pairs_preloaded_in_one_query(self, session):
        # Pre-seed a candidate match for sp#0 -> pp#0 so the loop must
        # short-circuit on the existing-pair check. Without preload, that
        # would be another SELECT per candidate.
        supplier = _make_supplier(session, "preload")
        sps = [_make_sp(session, supplier, i) for i in range(10)]
        pps = [_make_pp(session, i) for i in range(10)]
        for sp, pp in zip(sps, pps):
            session.add(ProductMatch(
                supplier_product_id=sp.id,
                prom_product_id=pp.id,
                score=80.0,
                status="candidate",
            ))
        session.commit()

        with count_selects() as count:
            run_matching_for_supplier(supplier.id)

        # 10 SP, 10 PP, 10 pre-existing pairs. Reads we expect:
        # matched_ids, unmatched_sp, all_pp, existing_pairs = 4 SELECTs.
        # SQLite may add a few savepoint/PRAGMA SELECTs. Cap at 8.
        assert count[0] <= 8, (
            f"run_matching_for_supplier issued {count[0]} SELECTs for "
            f"a 10x10 setup with all pairs pre-seeded — preload regressed"
        )


class TestApplyMatchRulesNoNPlusOne:
    """rule_matcher.apply_match_rules must not scale SELECT count with SP/rules."""

    def test_select_count_does_not_grow_linearly_with_sp_count(self, session):
        # Build a PP catalog (rules will reference these), then small +
        # large suppliers with identical SP names so the rule fires for
        # every SP — maximising the loop body.
        pps = [_make_pp(session, i, name=f"Catalog Item {i}") for i in range(10)]
        rules = []
        for pp in pps:
            r = MatchRule(
                supplier_product_name_pattern=f"SP Name {pp.id}",
                supplier_brand=None,
                prom_product_id=pp.id,
                created_by="test",
                is_active=True,
            )
            session.add(r)
            rules.append(r)
        session.flush()

        small = _make_supplier(session, "small_rule")
        for i, pp in enumerate(pps[:5]):
            sp = _make_sp(session, small, i, name=f"SP Name {pp.id}")
        session.commit()

        with count_selects() as small_count:
            apply_match_rules(small.id)
        baseline = small_count[0]

        big = _make_supplier(session, "big_rule")
        # 5x SP so the loop body runs 5x as often.
        for i in range(25):
            pp = pps[i % len(pps)]
            _make_sp(session, big, i, name=f"SP Name {pp.id}")
        session.commit()

        with count_selects() as big_count:
            apply_match_rules(big.id)
        scaled = big_count[0]

        assert scaled - baseline <= 5, (
            f"apply_match_rules looks N+1: "
            f"5 SP -> {baseline} selects, 25 SP -> {scaled} selects "
            f"(delta {scaled - baseline}, expected <= 5). "
            f"Each preload (prom_by_id, existing_by_pair) should be 1 SELECT "
            f"regardless of SP count."
        )

    def test_no_per_pair_lookup_when_pp_already_claimed(self, session):
        # Trigger the claimed-pp branch (line ~94 in rule_matcher.py): one PP
        # is already locked by a confirmed match. Every rule pointing at it
        # must NOT issue a SELECT to look up the existing pair (preloaded).
        pps = [_make_pp(session, i, name=f"Item {i}") for i in range(5)]
        rules = []
        for pp in pps:
            r = MatchRule(
                supplier_product_name_pattern=f"Match {pp.id}",
                supplier_brand=None,
                prom_product_id=pp.id,
                created_by="test",
                is_active=True,
            )
            session.add(r)
            rules.append(r)

        # Pre-claim every PP via a different supplier — forces the loop into
        # the "leave as candidate" branch on every iteration.
        claimer = _make_supplier(session, "claimer")
        for pp in pps:
            sp_claim = _make_sp(session, claimer, pp.id, name=f"claim-{pp.id}")
            session.add(ProductMatch(
                supplier_product_id=sp_claim.id,
                prom_product_id=pp.id,
                score=100.0,
                status="confirmed",
            ))
        session.commit()

        target = _make_supplier(session, "target")
        for pp in pps:
            _make_sp(session, target, pp.id, name=f"Match {pp.id}")
        session.commit()

        with count_selects() as count:
            apply_match_rules(target.id)

        # 5 SP, 5 rules, every pair routed through claimed branch. Without
        # preload that's at minimum 5 extra SELECTs (one per existing-pair
        # lookup). With preload it's the constant-overhead set: rules,
        # confirmed_ids, claimed_pp_ids, eligible, prom_by_id,
        # existing_by_pair = 6, plus a handful of SQLite/SAVEPOINT noise.
        assert count[0] <= 12, (
            f"apply_match_rules issued {count[0]} SELECTs for 5 SP x 5 rules "
            f"with all pp_ids claimed — claimed-branch preload regressed"
        )
