"""Delete synthetic 'bench_pp*' rows from PromProduct.

These 50 rows (IDs 5684-5733, created in a single transaction 2026-04-26 20:29:13)
are not real Horoshop products — likely artifacts from a perf-benchmark script
that ran against prod by mistake. Verified via audit_bench_pp_pollution.py:
    - All 50 rows: brand=Sirman, name='Sirman Mantegna N', price=1000 EUR, no matches
    - Not present in Horoshop XLSX export (only 1 real Sirman Mantegna exists)
    - 0 ProductMatch rows attached → safe to delete

Defensive: this script re-verifies before deleting — if any match shows up,
it ABORTS and reports the conflicting row.

Usage:
    .venv/Scripts/python.exe scripts/delete_bench_pp_pollution.py          # dry-run
    .venv/Scripts/python.exe scripts/delete_bench_pp_pollution.py --apply  # commit
"""
import sys

from app import create_app
from app.extensions import db
from app.models import PromProduct, ProductMatch

sys.stdout.reconfigure(encoding="utf-8")

EXPECTED_COUNT = 50
EXPECTED_BRAND = "Sirman"
EXPECTED_PRICE_KOP = 100000  # 1000 EUR


def main() -> int:
    apply = "--apply" in sys.argv
    mode = "APPLY" if apply else "DRY-RUN"

    app = create_app()
    with app.app_context():
        print("=" * 80)
        print(f"Delete bench_pp* synthetic PromProduct rows  [{mode}]")
        print("=" * 80)

        rows = PromProduct.query.filter(
            PromProduct.external_id.ilike("bench_pp%")
        ).order_by(PromProduct.id).all()
        print(f"Found {len(rows)} rows matching external_id ILIKE 'bench_pp%'")

        if not rows:
            print("Nothing to delete. Exiting.")
            return 0

        # Defensive checks — abort if anything looks unexpected
        problems = []
        if len(rows) > EXPECTED_COUNT + 10:
            problems.append(f"too many rows ({len(rows)} > expected {EXPECTED_COUNT}+10)")

        for pp in rows:
            if pp.brand != EXPECTED_BRAND:
                problems.append(f"PP#{pp.id} brand={pp.brand!r} != {EXPECTED_BRAND!r}")
                break  # one is enough
            if pp.price != EXPECTED_PRICE_KOP:
                problems.append(f"PP#{pp.id} price={pp.price} != {EXPECTED_PRICE_KOP}")
                break

        # Check for matches — if any exist, abort
        pp_ids = [pp.id for pp in rows]
        match_count = ProductMatch.query.filter(
            ProductMatch.prom_product_id.in_(pp_ids)
        ).count()
        if match_count > 0:
            problems.append(f"{match_count} ProductMatch rows attached — abort")

        if problems:
            print("\nABORT — defensive checks failed:")
            for p in problems:
                print(f"  - {p}")
            print("\nRun audit_bench_pp_pollution.py first and investigate before retry.")
            return 1

        print(f"\nAll defensive checks passed:")
        print(f"  - count={len(rows)}")
        print(f"  - all rows brand=Sirman, price=1000 EUR")
        print(f"  - 0 matches attached")
        print()
        print(f"IDs to delete: {pp_ids[0]}..{pp_ids[-1]} (sample: {pp_ids[:3]}...{pp_ids[-3:]})")

        if apply:
            for pp in rows:
                db.session.delete(pp)
            db.session.commit()
            print(f"\n✅ Deleted {len(rows)} bench_pp* rows.")
            # Verify
            remaining = PromProduct.query.filter(
                PromProduct.external_id.ilike("bench_pp%")
            ).count()
            print(f"   Post-delete count of bench_pp*: {remaining}")
            total = PromProduct.query.count()
            print(f"   Total PromProducts now: {total}")
        else:
            print(f"\nDRY-RUN: would delete {len(rows)} rows. Re-run with --apply.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
