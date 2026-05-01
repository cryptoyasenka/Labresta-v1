"""One-time migration: normalize brand case duplicates.

For each case-insensitive brand group, keeps the most-common form
and updates all minority variants to match it.

Run with:
    flask shell -c "exec(open('scripts/normalize_brands.py').read())"
  or:
    python -m flask --app app shell
    >>> exec(open('scripts/normalize_brands.py').read())
"""
from collections import defaultdict

from sqlalchemy import select, func, update

from app.extensions import db
from app.models.supplier_product import SupplierProduct

# Build groups: lowercase → [(brand, count), ...]
rows = db.session.execute(
    select(SupplierProduct.brand, func.count(SupplierProduct.id).label("cnt"))
    .where(SupplierProduct.brand.isnot(None), SupplierProduct.brand != "")
    .group_by(SupplierProduct.brand)
    .order_by(func.count(SupplierProduct.id).desc())
).all()

groups: dict[str, list] = defaultdict(list)
for brand, cnt in rows:
    groups[brand.strip().lower()].append((brand, cnt))

dupes = {k: v for k, v in groups.items() if len(v) > 1}

if not dupes:
    print("No brand duplicates found — nothing to do.")
else:
    total_updated = 0
    for key, variants in sorted(dupes.items()):
        canonical = max(variants, key=lambda x: x[1])[0]
        minority = [b for b, _ in variants if b != canonical]
        print(f"[{key}] canonical='{canonical}', updating: {minority}")
        for old_brand in minority:
            result = db.session.execute(
                update(SupplierProduct)
                .where(SupplierProduct.brand == old_brand)
                .values(brand=canonical)
            )
            total_updated += result.rowcount

    db.session.commit()
    print(f"\nDone. Updated {total_updated} rows across {len(dupes)} brand groups.")
