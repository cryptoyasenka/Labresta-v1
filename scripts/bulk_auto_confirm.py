"""Auto-confirm safe candidates by proven bulk rules.

R1 (single-candidate): same brand + identical after-brand meaningful tokens.
R2 (single-candidate): SUP⊂PROM or PROM⊂SUP + price within ±5%.
R3 (multi-candidate): sp has multiple candidates BUT exactly one is
    tokens-equal; confirm that one and reject the subset sibling(s).
    Handles the "base model + bundle variant" catalog pattern where
    a supplier SKU matches both its exact twin and its sibling by subset.
R4 (reject-only): sp already has a confirmed match with tokens==sp_tokens
    AND a stray candidate to another pp with tokens ⊋ sp_tokens (strict
    superset, same brand). The candidate is a bundle-sibling of the
    already-confirmed base — reject. Confirmed rows are never modified.

Dry-run by default. --apply to commit.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from datetime import datetime, timezone

from sqlalchemy import func, select

from app import create_app
from app.extensions import db
from app.models.catalog import PromProduct
from app.models.product_match import ProductMatch
from app.models.supplier_product import SupplierProduct
from app.services.matcher import after_brand_remainder, meaningful_tokens


PRICE_BAND = 0.05  # ±5%


def _group_candidates_by_sp():
    sp_counts = db.session.execute(
        select(ProductMatch.supplier_product_id, func.count(ProductMatch.id))
        .where(ProductMatch.status == "candidate")
        .group_by(ProductMatch.supplier_product_id)
    ).all()
    single_ids = [sp for sp, c in sp_counts if c == 1]
    multi_ids = [sp for sp, c in sp_counts if c > 1]
    singles = (
        ProductMatch.query.filter(
            ProductMatch.status == "candidate",
            ProductMatch.supplier_product_id.in_(single_ids),
        ).all()
        if single_ids else []
    )
    multis_by_sp: dict[int, list[ProductMatch]] = {}
    if multi_ids:
        rows = ProductMatch.query.filter(
            ProductMatch.status == "candidate",
            ProductMatch.supplier_product_id.in_(multi_ids),
        ).all()
        for m in rows:
            multis_by_sp.setdefault(m.supplier_product_id, []).append(m)
    return singles, multis_by_sp


def _same_brand(sp, pp) -> bool:
    if not sp.brand or not pp.brand:
        return False
    return sp.brand.strip().lower() == pp.brand.strip().lower()


def _pair_tokens(sp, pp):
    return (
        meaningful_tokens(after_brand_remainder(sp.name, sp.brand)),
        meaningful_tokens(after_brand_remainder(pp.name, pp.brand)),
    )


def classify_single(match: ProductMatch) -> str | None:
    sp: SupplierProduct = match.supplier_product
    pp: PromProduct = match.prom_product
    if not sp or not pp or not _same_brand(sp, pp):
        return None
    sup, prom = _pair_tokens(sp, pp)
    if not sup or not prom:
        return None
    if sup == prom:
        return "R1:tokens-equal"
    if sup.issubset(prom) or prom.issubset(sup):
        if sp.price_cents and pp.price and pp.price > 0:
            sup_eur = sp.price_cents / 100.0
            prom_eur = float(pp.price)
            lo, hi = prom_eur * (1 - PRICE_BAND), prom_eur * (1 + PRICE_BAND)
            if lo <= sup_eur <= hi:
                return "R2:subset-tight-price"
    return None


def _find_r4_bundle_sibling_candidates() -> list[int]:
    """Return IDs of candidate matches to reject under R4.

    Finds supplier products where:
      - a CONFIRMED/MANUAL match exists with tokens exactly equal to sp tokens
      - a separate CANDIDATE match exists pointing to a different pp with
        tokens that are a strict superset of sp tokens (same brand).
    """
    to_reject: list[int] = []

    # Group all non-rejected matches by sp
    rows = (
        ProductMatch.query
        .filter(ProductMatch.status.in_(["candidate", "confirmed", "manual"]))
        .all()
    )
    by_sp: dict[int, list[ProductMatch]] = {}
    for m in rows:
        by_sp.setdefault(m.supplier_product_id, []).append(m)

    for sp_id, ms in by_sp.items():
        cands = [m for m in ms if m.status == "candidate"]
        confirmed_like = [m for m in ms if m.status in ("confirmed", "manual")]
        if not cands or not confirmed_like:
            continue
        sp = cands[0].supplier_product
        if not sp:
            continue
        sup_tokens = meaningful_tokens(after_brand_remainder(sp.name, sp.brand))
        if not sup_tokens:
            continue

        # Is there a confirmed match with tokens EXACTLY equal to sp?
        has_exact_confirmed = False
        for cm in confirmed_like:
            pp = cm.prom_product
            if not pp or not _same_brand(sp, pp):
                continue
            prom_tokens = meaningful_tokens(after_brand_remainder(pp.name, pp.brand))
            if prom_tokens == sup_tokens:
                has_exact_confirmed = True
                break
        if not has_exact_confirmed:
            continue

        # Reject candidates that are strict supersets of sp (bundle siblings)
        for c in cands:
            pp = c.prom_product
            if not pp or not _same_brand(sp, pp):
                continue
            prom_tokens = meaningful_tokens(after_brand_remainder(pp.name, pp.brand))
            if prom_tokens > sup_tokens:  # strict superset: pp has everything sp has + extras
                to_reject.append(c.id)
    return to_reject


def classify_multi(candidates: list[ProductMatch]) -> tuple[ProductMatch, list[ProductMatch]] | None:
    """Return (winner, losers) when exactly one candidate has tokens-equal
    AND the others are strict subsets (loser tokens ⊂ winner tokens or
    winner ⊂ loser). Otherwise return None (can't auto-resolve)."""
    sp = candidates[0].supplier_product
    if not sp:
        return None
    sup_tokens = meaningful_tokens(after_brand_remainder(sp.name, sp.brand))
    if not sup_tokens:
        return None

    equal_candidates: list[ProductMatch] = []
    other_candidates: list[ProductMatch] = []
    for m in candidates:
        pp = m.prom_product
        if not pp or not _same_brand(sp, pp):
            return None
        prom_tokens = meaningful_tokens(after_brand_remainder(pp.name, pp.brand))
        if not prom_tokens:
            return None
        if prom_tokens == sup_tokens:
            equal_candidates.append(m)
        else:
            other_candidates.append((m, prom_tokens))

    if len(equal_candidates) != 1:
        return None

    winner = equal_candidates[0]
    losers: list[ProductMatch] = []
    for m, prom_tokens in other_candidates:
        # Strict subset in either direction — "related variant", safe to reject
        if prom_tokens.issubset(sup_tokens) or sup_tokens.issubset(prom_tokens):
            losers.append(m)
        else:
            return None  # unrelated candidate, don't auto-decide
    return winner, losers


def run(apply: bool) -> None:
    app = create_app()
    with app.app_context():
        singles, multis_by_sp = _group_candidates_by_sp()
        print(f"Single-candidate matches: {len(singles)}")
        print(f"Multi-candidate supplier products: {len(multis_by_sp)}")

        confirm_buckets: dict[str, list[int]] = {}
        reject_ids: list[int] = []

        for m in singles:
            rule = classify_single(m)
            if rule:
                confirm_buckets.setdefault(rule, []).append(m.id)

        r3_confirms: list[int] = []
        for sp_id, cands in multis_by_sp.items():
            result = classify_multi(cands)
            if result:
                winner, losers = result
                r3_confirms.append(winner.id)
                reject_ids.extend(l.id for l in losers)
        if r3_confirms:
            confirm_buckets["R3:multi-winner-tokens-equal"] = r3_confirms

        # R4: reject candidates that duplicate a confirmed exact-tokens match
        r4_rejects = _find_r4_bundle_sibling_candidates()
        reject_ids.extend(r4_rejects)

        total_confirm = sum(len(v) for v in confirm_buckets.values())
        for rule, ids in confirm_buckets.items():
            print(f"  {rule}: confirm {len(ids)}")
        print(f"  R3 side effect: reject {len(reject_ids) - len(r4_rejects)} sibling subset candidates")
        print(f"  R4:reject-bundle-of-confirmed: reject {len(r4_rejects)}")
        print(f"Total confirmed: {total_confirm}, rejected: {len(reject_ids)}")

        if not apply:
            print("\nDRY-RUN — pass --apply to commit.")
            return

        now = datetime.now(timezone.utc)
        confirmed = 0
        for ids in confirm_buckets.values():
            for mid in ids:
                m = db.session.get(ProductMatch, mid)
                if not m or m.status != "candidate":
                    continue
                m.status = "confirmed"
                m.confirmed_at = now
                m.confirmed_by = "rule:bulk_auto_confirm"
                confirmed += 1
        rejected = 0
        for mid in reject_ids:
            m = db.session.get(ProductMatch, mid)
            if not m or m.status != "candidate":
                continue
            m.status = "rejected"
            rejected += 1
        db.session.commit()
        print(f"\nAPPLIED: {confirmed} confirmed, {rejected} rejected.")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--apply", action="store_true")
    args = p.parse_args()
    run(args.apply)


if __name__ == "__main__":
    main()
