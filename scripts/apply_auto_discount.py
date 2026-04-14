"""Auto-set ProductMatch.discount_percent for confirmed+manual matches.

By default, only fills matches where discount_percent IS NULL
(so manually-set overrides are preserved).
Use --force to overwrite all confirmed+manual matches.
Use --dry-run to preview without writing.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import create_app
from app.extensions import db
from app.models.product_match import ProductMatch
from app.models.supplier import Supplier
from app.models.supplier_product import SupplierProduct
from app.services.pricing import calculate_auto_discount


def run(force: bool, dry_run: bool, supplier_id: int | None) -> None:
    app = create_app()
    with app.app_context():
        suppliers = Supplier.query.all()
        if supplier_id:
            suppliers = [s for s in suppliers if s.id == supplier_id]

        grand_total = 0
        grand_changed = 0

        for supplier in suppliers:
            eur_rate = supplier.eur_rate_uah or 51.15
            q = (
                db.session.query(ProductMatch, SupplierProduct)
                .join(SupplierProduct, ProductMatch.supplier_product_id == SupplierProduct.id)
                .filter(
                    ProductMatch.status.in_(["confirmed", "manual"]),
                    SupplierProduct.supplier_id == supplier.id,
                )
            )
            if not force:
                q = q.filter(ProductMatch.discount_percent.is_(None))

            rows = q.all()
            dist: dict[int, int] = {}
            changed = 0

            for match, sp in rows:
                if not sp.price_cents or sp.price_cents <= 0:
                    continue
                d = calculate_auto_discount(sp.price_cents, eur_rate)
                dist[d] = dist.get(d, 0) + 1
                if match.discount_percent != d:
                    if not dry_run:
                        match.discount_percent = float(d)
                    changed += 1

            if not dry_run:
                db.session.commit()

            print(f"[{supplier.name}] rate={eur_rate} scanned={len(rows)} changed={changed}")
            for d in sorted(dist):
                print(f"   {d:>2}%: {dist[d]}")
            grand_total += len(rows)
            grand_changed += changed

        prefix = "DRY-RUN " if dry_run else ""
        print(f"\n{prefix}Total scanned={grand_total} changed={grand_changed}")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--force", action="store_true", help="Overwrite existing discounts")
    p.add_argument("--dry-run", action="store_true", help="Preview without writing")
    p.add_argument("--supplier-id", type=int, default=None)
    args = p.parse_args()
    run(args.force, args.dry_run, args.supplier_id)


if __name__ == "__main__":
    main()
