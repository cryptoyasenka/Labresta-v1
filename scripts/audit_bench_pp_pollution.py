"""Audit: find synthetic 'bench_pp*' rows in PromProduct that pollute the catalog.

Yana spotted in /catalog rows like:
    external_id=bench_pp49, name=Sirman Mantegna 49, brand=Sirman, price=1000 EUR

These are benchmark/load-test artifacts, not real Horoshop products. They have:
    - external_id matching pattern '^bench_pp\\d+$' (or 'bench-pp', etc.)
    - identical price (1000.00 EUR)
    - synthetic name pattern 'Sirman Mantegna NN'

This script READS ONLY. It reports:
    1. Total bench_pp* count
    2. external_id pattern breakdown
    3. Any matches attached (would block deletion)
    4. imported_at range (when did they appear?)
    5. Suggested cleanup query

Usage:
    .venv/Scripts/python.exe scripts/audit_bench_pp_pollution.py
"""
import re
import sys

from app import create_app
from app.extensions import db
from app.models import PromProduct, ProductMatch
from sqlalchemy import func, or_

sys.stdout.reconfigure(encoding="utf-8")


def hr(t):
    print()
    print("=" * 80)
    print(t)
    print("=" * 80)


def main() -> int:
    app = create_app()
    with app.app_context():
        # 1. Count of bench_pp* by external_id
        hr("1. Count of likely-synthetic rows")
        patterns_q = PromProduct.query.filter(
            or_(
                PromProduct.external_id.ilike("bench_pp%"),
                PromProduct.external_id.ilike("bench-pp%"),
                PromProduct.external_id.ilike("test_pp%"),
                PromProduct.external_id.ilike("pp-%"),  # from test_matcher_n_plus_one
                PromProduct.name.ilike("Sirman Mantegna %"),
            )
        )
        rows = patterns_q.all()
        print(f"  Total rows matching pattern: {len(rows)}")

        # Bucket by external_id prefix
        buckets = {}
        for pp in rows:
            ext = pp.external_id or ""
            m = re.match(r"^([a-zA-Z_\-]+?)(\d+)$", ext)
            prefix = m.group(1) if m else "(other)"
            buckets.setdefault(prefix, []).append(pp)
        for prefix, items in sorted(buckets.items(), key=lambda x: -len(x[1])):
            print(f"    prefix={prefix!r:<15} count={len(items):>4}  "
                  f"sample_ext_id={items[0].external_id!r}")

        if not rows:
            print("  No synthetic rows found. Caller mistaken or already cleaned.")
            return 0

        # 2. Show first 20 to confirm pattern
        hr("2. Sample (first 20 rows)")
        print(f"  {'id':<6} {'external_id':<20} {'brand':<10} {'price':<8} "
              f"{'currency':<5} {'imported_at'}")
        for pp in sorted(rows, key=lambda p: p.id)[:20]:
            print(f"  {pp.id:<6} {(pp.external_id or '')[:20]:<20} "
                  f"{(pp.brand or '')[:10]:<10} {pp.price!s:<8} "
                  f"{(pp.currency or '')[:5]:<5} {pp.imported_at}")

        # 3. imported_at range
        hr("3. imported_at range (when did these appear?)")
        dates = [pp.imported_at for pp in rows if pp.imported_at]
        if dates:
            print(f"  min: {min(dates)}")
            print(f"  max: {max(dates)}")
            # Distribution by day
            from collections import Counter
            day_counter = Counter(d.date().isoformat() for d in dates)
            print("  by day:")
            for day, n in sorted(day_counter.items())[:10]:
                print(f"    {day}  {n:>4} rows")
        else:
            print("  No imported_at timestamps (NULL)")

        # 4. Any matches attached?
        hr("4. Matches attached (would block deletion)")
        pp_ids = [pp.id for pp in rows]
        matches = ProductMatch.query.filter(
            ProductMatch.prom_product_id.in_(pp_ids)
        ).all()
        print(f"  Total matches: {len(matches)}")
        if matches:
            from collections import Counter
            status_counter = Counter(m.status for m in matches)
            print("  by status:")
            for status, n in sorted(status_counter.items()):
                print(f"    {status:<15} {n:>4}")
            print()
            print("  First 10 matches:")
            for m in matches[:10]:
                print(f"    match#{m.id} pp#{m.prom_product_id} "
                      f"sp#{m.supplier_product_id} status={m.status} "
                      f"score={m.score}")

        # 5. Distinct brands (should be 'Sirman' only if test artifacts)
        hr("5. Brand distribution")
        from collections import Counter
        brand_counter = Counter(pp.brand for pp in rows)
        for brand, n in brand_counter.most_common():
            print(f"  {brand!r:<25} {n:>4}")

        # 6. Distinct prices
        hr("6. Price distribution (kopecks, divide by 100 for EUR)")
        price_counter = Counter(pp.price for pp in rows)
        for price, n in price_counter.most_common(10):
            eur = price / 100 if price else None
            print(f"  price_kop={price!s:<10} ({eur!s} EUR)  count={n}")

        # 7. Suggest cleanup
        hr("7. Cleanup suggestion")
        print(f"  If all {len(rows)} rows confirmed as test artifacts, delete with:")
        print(f"      DELETE FROM product_matches WHERE prom_product_id IN ({len(pp_ids)} ids);")
        print(f"      DELETE FROM prom_products WHERE id IN ({len(pp_ids)} ids);")
        print(f"  Or via Python: see scripts/delete_bench_pp_pollution.py (TBD)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
