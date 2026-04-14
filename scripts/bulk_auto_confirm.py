"""Auto-confirm safe candidates by proven bulk rules.

Rules applied only to single-candidate supplier products (sp with exactly 1 candidate match):
  R1 after-brand-tokens-equal: same brand + identical after-brand meaningful tokens
  R2 subset-tight-price: SUP tokens ⊂ PROM or PROM ⊂ SUP + supplier/prom price ratio within 5%

Uses --dry-run by default to preview. Pass --apply to commit.
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


def single_candidate_matches():
    sp_counts = db.session.execute(
        select(ProductMatch.supplier_product_id, func.count(ProductMatch.id))
        .where(ProductMatch.status == "candidate")
        .group_by(ProductMatch.supplier_product_id)
    ).all()
    single_ids = [sp for sp, c in sp_counts if c == 1]
    if not single_ids:
        return []
    return (
        ProductMatch.query.filter(
            ProductMatch.status == "candidate",
            ProductMatch.supplier_product_id.in_(single_ids),
        )
        .all()
    )


def classify(match: ProductMatch) -> str | None:
    sp: SupplierProduct = match.supplier_product
    pp: PromProduct = match.prom_product
    if not sp or not pp:
        return None

    # brand match required
    if not sp.brand or not pp.brand:
        return None
    if sp.brand.strip().lower() != pp.brand.strip().lower():
        return None

    sup_tokens = meaningful_tokens(after_brand_remainder(sp.name, sp.brand))
    prom_tokens = meaningful_tokens(after_brand_remainder(pp.name, pp.brand))
    if not sup_tokens or not prom_tokens:
        return None

    # R1: identical tokens
    if sup_tokens == prom_tokens:
        return "R1:tokens-equal"

    # R2: subset + price within 5%
    if sup_tokens.issubset(prom_tokens) or prom_tokens.issubset(sup_tokens):
        if sp.price_cents and pp.price and pp.price > 0:
            sup_eur = sp.price_cents / 100.0
            prom_eur = float(pp.price)
            lo, hi = prom_eur * (1 - PRICE_BAND), prom_eur * (1 + PRICE_BAND)
            if lo <= sup_eur <= hi:
                return "R2:subset-tight-price"
    return None


def run(apply: bool) -> None:
    app = create_app()
    with app.app_context():
        matches = single_candidate_matches()
        print(f"Single-candidate matches to evaluate: {len(matches)}")

        buckets: dict[str, list[int]] = {}
        for m in matches:
            rule = classify(m)
            if rule:
                buckets.setdefault(rule, []).append(m.id)

        total_confirm = 0
        for rule, ids in buckets.items():
            print(f"  {rule}: {len(ids)}")
            total_confirm += len(ids)
        print(f"Total would be auto-confirmed: {total_confirm}")

        if not apply:
            print("\nDRY-RUN — pass --apply to commit.")
            return

        now = datetime.now(timezone.utc)
        confirmed = 0
        for ids in buckets.values():
            for mid in ids:
                m = db.session.get(ProductMatch, mid)
                if not m or m.status != "candidate":
                    continue
                m.status = "confirmed"
                m.confirmed_at = now
                m.confirmed_by = "rule:bulk_auto_confirm"
                confirmed += 1
        db.session.commit()
        print(f"\nAPPLIED: {confirmed} candidates confirmed.")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--apply", action="store_true")
    args = p.parse_args()
    run(args.apply)


if __name__ == "__main__":
    main()
