"""Post-upload verification after Horoshop XLSX catalog import.

Checks what catalog_import.py can affect (12 PP fields) AND what it should NOT affect
(matches, supplier links, sync timestamps, discounts).

Run immediately after a successful XLSX upload to confirm the import didn't corrupt
unrelated state. If something looks wrong → use restore_pp_from_backup.py.

Usage:
    .venv/Scripts/python.exe scripts/verify_after_catalog_import.py
"""
import sys

from app import create_app
from app.extensions import db
from app.models import PromProduct, ProductMatch, Supplier, SupplierProduct, SyncRun
from sqlalchemy import func

sys.stdout.reconfigure(encoding="utf-8")

# Baseline after first clean Horoshop XLSX upload + bench_pp cleanup (2026-05-14)
# Was 5683 in pre-import backup; -50 bench_pp* synthetic rows deleted.
BASELINE_PPS = 5633
BASELINE_MATCHES = 2689
BASELINE_SUPPLIERS = 6

# 7 Cat H PPs that MUST stay display_article=NULL after import
CAT_H_TARGETS = [
    (347, "Spidocook SP300"),
    (80, "Fimar PFD27"),
    (154, "Roller Grill PIS 30"),
    (958, "FROSTY RC-30"),
    (3933, "FROSTY IC80A"),
    (3932, "GoodFood ICE777"),
    (4179, "Saro SKZ-12"),
]

OK = "OK  "
WARN = "WARN"
FAIL = "FAIL"


def hr(t):
    print()
    print("=" * 80)
    print(t)
    print("=" * 80)


def main() -> int:
    app = create_app()
    with app.app_context():
        any_fail = False

        # 1) Cat H — 7 PPs must have display_article=NULL
        hr("1. Cat H — display_article must be NULL (Yana cleared in Horoshop CMS)")
        cat_h_fail = 0
        for pp_id, hint in CAT_H_TARGETS:
            pp = db.session.get(PromProduct, pp_id)
            if pp is None:
                print(f"  [{FAIL}] PP#{pp_id} ({hint}) — NOT FOUND in DB")
                cat_h_fail += 1
                continue
            da = pp.display_article
            if da is None or da == "":
                print(f"  [{OK}] PP#{pp_id:<5} ({hint:<22}) — display_article=NULL")
            else:
                print(f"  [{FAIL}] PP#{pp_id:<5} ({hint:<22}) — display_article={da!r} "
                      f"(Horoshop card still has it — clear there too)")
                cat_h_fail += 1
        if cat_h_fail:
            any_fail = True
            print(f"\n  >> {cat_h_fail}/7 Cat H PPs FAILED — display_article repopulated")
        else:
            print("\n  >> All 7 Cat H PPs clean")

        # 2) PP count — should be >= baseline (new SKUs in XLSX add, don't delete)
        hr("2. PromProduct count")
        pp_count = db.session.query(func.count(PromProduct.id)).scalar()
        delta = pp_count - BASELINE_PPS
        if pp_count < BASELINE_PPS:
            print(f"  [{FAIL}] {pp_count} PPs (was {BASELINE_PPS}, lost {-delta}) — "
                  f"catalog_import shouldn't delete, restore from backup")
            any_fail = True
        elif delta > 200:
            print(f"  [{WARN}] {pp_count} PPs (was {BASELINE_PPS}, +{delta}) — "
                  f"larger growth than expected, sanity-check")
        else:
            print(f"  [{OK}] {pp_count} PPs (was {BASELINE_PPS}, +{delta} new)")

        # 3) Match count — catalog_import doesn't touch matches
        hr("3. ProductMatch count (must equal baseline)")
        match_count = db.session.query(func.count(ProductMatch.id)).scalar()
        if match_count != BASELINE_MATCHES:
            print(f"  [{FAIL}] {match_count} matches (was {BASELINE_MATCHES}) — "
                  f"catalog_import shouldn't touch this table")
            any_fail = True
        else:
            print(f"  [{OK}] {match_count} matches (unchanged)")

        # 4) Confirmed match count — same
        hr("4. Confirmed matches (must equal baseline)")
        confirmed = db.session.query(func.count(ProductMatch.id)).filter(
            ProductMatch.status.in_(["confirmed", "manual"])
        ).scalar()
        print(f"  Confirmed/manual matches: {confirmed}")

        # 5) Suppliers unchanged
        hr("5. Suppliers (must equal baseline)")
        sup_count = db.session.query(func.count(Supplier.id)).scalar()
        if sup_count != BASELINE_SUPPLIERS:
            print(f"  [{FAIL}] {sup_count} suppliers (was {BASELINE_SUPPLIERS})")
            any_fail = True
        else:
            print(f"  [{OK}] {sup_count} suppliers (unchanged)")

        # 6) SupplierProduct count — catalog_import doesn't touch
        hr("6. SupplierProduct count (catalog_import doesn't touch)")
        sp_count = db.session.query(func.count(SupplierProduct.id)).scalar()
        print(f"  SP count: {sp_count}")

        # 7) Per-supplier confirmed counts (sanity check)
        hr("7. Confirmed matches per supplier")
        for sup in Supplier.query.order_by(Supplier.id).all():
            n = db.session.query(func.count(ProductMatch.id)).filter(
                ProductMatch.supplier_product_id.in_(
                    db.select(SupplierProduct.id).where(
                        SupplierProduct.supplier_id == sup.id
                    )
                ),
                ProductMatch.status.in_(["confirmed", "manual"]),
            ).scalar()
            print(f"  {sup.id} {sup.name:<20} {n:>4} confirmed")

        # 8) Spot-check: a few known PPs from different categories
        hr("8. Spot-check: well-known PPs have non-empty critical fields")
        sample_ids = [347, 80, 154, 958, 3933, 3932, 4179, 1, 2, 3]
        for pp_id in sample_ids:
            pp = db.session.get(PromProduct, pp_id)
            if pp is None:
                print(f"  [{WARN}] PP#{pp_id} not found")
                continue
            issues = []
            if not pp.name:
                issues.append("name empty")
            if not pp.brand:
                issues.append("brand empty")
            if not pp.page_url:
                issues.append("page_url empty")
            if pp.price is None:
                issues.append("price NULL")
            tag = f"[{FAIL}]" if issues else f"[{OK}]"
            issues_s = "  " + ", ".join(issues) if issues else ""
            name_short = (pp.name or "")[:40]
            print(f"  {tag} PP#{pp_id:<5} brand={pp.brand!s:<12} "
                  f"price={pp.price!s:<8} name={name_short!r}{issues_s}")

        # 9) Recent SyncRuns — ensure import didn't break sync state
        hr("9. Recent SyncRuns (top 5)")
        runs = SyncRun.query.order_by(SyncRun.id.desc()).limit(5).all()
        for r in runs:
            print(f"  SR#{r.id:<5} sup={r.supplier_id} status={r.status:<10} "
                  f"started={r.started_at}")

        # Final
        hr("FINAL VERDICT")
        if any_fail:
            print(f"  [{FAIL}] One or more checks failed. Inspect output above.")
            print("         Restore: .venv/Scripts/python.exe "
                  "scripts/restore_pp_from_backup.py "
                  "backups/pre-catalog-import_2026-05-13_1658.json")
            return 1
        print(f"  [{OK}] Import successful — Cat H clean, counts intact.")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
