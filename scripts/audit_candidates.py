"""Audit candidate ProductMatch rows against current matcher gates.

Matcher logic tightened after many of the current `status='candidate'` rows
were created (cross-brand fix, type gate, containment gate, voltage gate,
display_article substring). Some candidates no longer survive today's gates —
they're stale. Others are still legitimate and need human review.

For each supplier-product with candidate matches:
  * re-run find_match_candidates against the full catalog
  * compare current DB candidates vs freshly produced pp_ids
  * label each as:
      - stale    : in DB, matcher no longer returns it
      - valid    : in DB, matcher still returns it
      - missing  : matcher returns pp_id not in DB (matcher improved, add)

--apply reject stale candidates + add missing candidates.
--dry-run (default) only reports.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from collections import defaultdict

from sqlalchemy import select

from app import create_app
from app.extensions import db
from app.models.catalog import PromProduct
from app.models.product_match import ProductMatch
from app.models.supplier_product import SupplierProduct
from app.services.matcher import find_match_candidates


def run(apply: bool) -> None:
    app = create_app()
    with app.app_context():
        candidate_rows = (
            ProductMatch.query.filter_by(status="candidate")
            .order_by(ProductMatch.supplier_product_id)
            .all()
        )
        by_sp: dict[int, list[ProductMatch]] = defaultdict(list)
        for m in candidate_rows:
            by_sp[m.supplier_product_id].append(m)

        prom_all = db.session.execute(select(PromProduct)).scalars().all()
        prom_list = [
            {
                "id": p.id, "name": p.name, "brand": p.brand, "price": p.price,
                "model": p.model, "article": p.article,
                "display_article": p.display_article,
            }
            for p in prom_all
        ]

        stats = {"stale": 0, "valid": 0, "missing": 0, "sp_scanned": 0}
        stale_rows: list[ProductMatch] = []
        missing_pairs: list[tuple[int, int, float]] = []

        for sp_id, matches in by_sp.items():
            sp = db.session.get(SupplierProduct, sp_id)
            if sp is None:
                continue
            stats["sp_scanned"] += 1
            current_pp = {m.prom_product_id: m for m in matches}

            fresh = find_match_candidates(
                sp.name, sp.brand, prom_list,
                supplier_price_cents=sp.price_cents,
                supplier_model=sp.model,
                supplier_article=sp.article,
            )
            fresh_pp = {c["prom_product_id"]: c["score"] for c in fresh}

            print(f"\nsp#{sp_id} [{sp.brand or '∅'}] {sp.name[:70]}")
            for pp_id, m in current_pp.items():
                if pp_id in fresh_pp:
                    stats["valid"] += 1
                    print(f"  valid   pp#{pp_id} db_score={m.score:.0f} now={fresh_pp[pp_id]:.0f}")
                else:
                    stats["stale"] += 1
                    stale_rows.append(m)
                    print(f"  STALE   pp#{pp_id} db_score={m.score:.0f} — matcher no longer returns")
            for pp_id, score in fresh_pp.items():
                if pp_id not in current_pp:
                    stats["missing"] += 1
                    missing_pairs.append((sp_id, pp_id, score))
                    pp = db.session.get(PromProduct, pp_id)
                    pp_name = pp.name[:60] if pp else "?"
                    print(f"  MISSING pp#{pp_id} score={score:.0f} :: {pp_name}")

        print("\n=== Summary ===")
        print(f"sp scanned:         {stats['sp_scanned']}")
        print(f"candidates valid:   {stats['valid']}")
        print(f"candidates stale:   {stats['stale']}")
        print(f"missing pairs:      {stats['missing']} (matcher produces them, DB doesn't have)")

        if not apply:
            print("\nDRY-RUN — pass --apply to reject stale + add missing.")
            return

        for m in stale_rows:
            m.status = "rejected"
        for sp_id, pp_id, score in missing_pairs:
            db.session.add(ProductMatch(
                supplier_product_id=sp_id,
                prom_product_id=pp_id,
                score=score,
                status="candidate",
            ))
        db.session.commit()
        print(f"\nAPPLIED: rejected {len(stale_rows)} stale, added {len(missing_pairs)} missing.")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--apply", action="store_true")
    args = p.parse_args()
    run(args.apply)


if __name__ == "__main__":
    main()
