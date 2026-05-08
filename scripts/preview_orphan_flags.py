"""Preview which PPs Phase M would flag as orphan, WITHOUT writing to DB.

Run with prod DATABASE_URL:
  $env:DATABASE_URL="postgresql://...switchyard.proxy.rlwy.net.../railway"
  & .venv/Scripts/python.exe scripts/preview_orphan_flags.py

Replicates the inner loop of `flag_orphan_pps` (orphan_detector.py:299-344)
but prints brand/id/name/anchor for each candidate instead of mutating DB rows.
Groups output by brand and reason (display-based vs name-scan fallback) so
you can spot-check Phase M's name-scan fallback hits separately from
display-article-based orphans (Phase 8 baseline behavior).
"""
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy import select

from app import create_app
from app.extensions import db
from app.models.catalog import PromProduct
from app.services.orphan_detector import (
    AUTO_NOTE,
    _any_sp_article_in_pp_name,
    _brand_supplier_counts,
    _dead_supplier_ids,
    _pp_articles_in_supplier,
    _pps_with_confirmed_match,
    _supplier_article_strings,
)


def main() -> int:
    app = create_app()
    with app.app_context():
        dead_ids = _dead_supplier_ids()
        brand_supps = _brand_supplier_counts()
        matched_pp_ids = _pps_with_confirmed_match()

        single_supp_brands = {
            b: sids[0]
            for b, sids in brand_supps.items()
            if len(sids) == 1 and sids[0] not in dead_ids
        }
        article_index = {}
        article_raw_index = {}
        for sup_id in set(single_supp_brands.values()):
            article_index[sup_id] = _pp_articles_in_supplier(sup_id)
            article_raw_index[sup_id] = _supplier_article_strings(sup_id)

        pps = db.session.execute(
            select(PromProduct).where(PromProduct.brand.isnot(None))
        ).scalars().all()

        # Bucket orphans by reason
        by_brand_disp = defaultdict(list)   # display-article path (Phase 8)
        by_brand_name = defaultdict(list)   # name-scan fallback (Phase M)
        already_flagged_count = 0

        for pp in pps:
            brand_l = (pp.brand or "").lower().strip()
            if not brand_l:
                continue
            sup_id = single_supp_brands.get(brand_l)
            if sup_id is None:
                continue
            if pp.id in matched_pp_ids:
                continue

            disp = (pp.display_article or "").lower().strip()
            articles = article_index.get(sup_id, set())
            if disp:
                is_orphan = disp not in articles
                bucket = by_brand_disp
            else:
                sp_arts = article_raw_index.get(sup_id, [])
                is_orphan = not _any_sp_article_in_pp_name(pp.name, sp_arts)
                bucket = by_brand_name

            if not is_orphan:
                continue

            already_was_flagged = (
                pp.operator_decision == "needs_delete"
                and pp.operator_decision_note == AUTO_NOTE
            )
            if already_was_flagged:
                already_flagged_count += 1

            bucket[pp.brand].append((pp.id, pp.display_article or "", pp.name, already_was_flagged))

        print(f"\n{'='*78}")
        print("Phase M dry-run preview (NO DB writes)")
        print(f"{'='*78}")
        print(f"dead suppliers excluded: {sorted(dead_ids)}")
        print(f"single-supplier brands: {len(single_supp_brands)}")
        print()

        total_disp = sum(len(v) for v in by_brand_disp.values())
        total_name = sum(len(v) for v in by_brand_name.values())

        print(f"--- Path A: display_article missing (Phase 8 baseline) — {total_disp} PPs ---")
        for brand in sorted(by_brand_disp):
            rows = by_brand_disp[brand]
            print(f"\n  [{brand}] {len(rows)} PPs")
            for pp_id, disp, name, was_flagged in rows[:30]:
                marker = "*" if was_flagged else " "
                print(f"    {marker} PP#{pp_id:<5} disp={disp!r:25} {name!r}")
            if len(rows) > 30:
                print(f"    ... and {len(rows)-30} more")

        print(f"\n--- Path B: name-scan fallback (Phase M new) — {total_name} PPs ---")
        for brand in sorted(by_brand_name):
            rows = by_brand_name[brand]
            print(f"\n  [{brand}] {len(rows)} PPs")
            for pp_id, disp, name, was_flagged in rows[:30]:
                marker = "*" if was_flagged else " "
                print(f"    {marker} PP#{pp_id:<5} {name!r}")
            if len(rows) > 30:
                print(f"    ... and {len(rows)-30} more")

        print(f"\n{'='*78}")
        print(f"SUMMARY")
        print(f"{'='*78}")
        print(f"  Path A (Phase 8 display-based):  {total_disp:>4} PPs across {len(by_brand_disp)} brands")
        print(f"  Path B (Phase M name-scan):      {total_name:>4} PPs across {len(by_brand_name)} brands  <- NEW")
        print(f"  Already auto-flagged before:     {already_flagged_count:>4} (marked with *)")
        print(f"  Total:                           {total_disp + total_name:>4}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
