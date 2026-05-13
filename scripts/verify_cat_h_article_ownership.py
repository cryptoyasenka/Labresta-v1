"""Cat H: verify that each colliding display_article is genuinely owned by Hendi (or other claimed brand).

For each of the 11 colliding articles, list ALL supplier_products carrying that exact article,
showing supplier name + brand. This proves which brand the article *actually* belongs to in
the real feed data — and tells us which PP is the legitimate owner and which is a data-entry mistake.

Read-only. Safe.
"""
import sys
from app import create_app
from app.extensions import db
from app.models import Supplier, SupplierProduct

sys.stdout.reconfigure(encoding="utf-8")

# article -> (PPs claiming it, expected legit owner brand)
ARTICLES = [
    ("203149",       "Hendi+Spidocook"),
    ("239766",       "Hendi+Fimar"),
    ("239780",       "Hendi+Roller Grill"),
    ("240403",       "Hendi+FROSTY"),
    ("271599",       "Hendi+FROSTY+GoodFood"),
    ("860526",       "Hendi+Saro"),
    ("0830.00020.00","Ozti SPM 20 vs SPM 70"),
    ("212004",       "FROSTY VP-81 vs VP-2Y40"),
    ("40752102P",    "Sirman TM INOX base vs disc-set"),
    ("40802852F",    "Sirman IP 20 M vs IP 10 M"),
    ("66520502K1.2", "Sirman CICLONE A35 vs A25"),
]


def main() -> int:
    app = create_app()
    with app.app_context():
        sups = {s.id: s.name for s in Supplier.query.all()}
        print("=" * 90)
        print("Cat H — verification: who really owns each colliding display_article?")
        print("=" * 90)

        for art, hint in ARTICLES:
            print(f"\n## article = {art!r}   (PPs claim: {hint})")
            sps = (
                SupplierProduct.query
                .filter(SupplierProduct.article == art)
                .order_by(SupplierProduct.supplier_id, SupplierProduct.id)
                .all()
            )
            if not sps:
                print(f"   ❌ NO supplier carries this exact article — could be Yana-entered code")
                continue
            print(f"   ✅ Found {len(sps)} SP records carrying this article:")
            for sp in sps:
                sup = sups.get(sp.supplier_id, f"sup{sp.supplier_id}")
                brand = sp.brand or "—"
                name = (sp.name or "?")[:70]
                print(f"      SP#{sp.id} sup={sup!r:<10} brand={brand!r:<15} {name}")

        print("\n" + "=" * 90)
        print("Interpretation:")
        print("  - If only Astim (Hendi-supplier) carries it → Hendi article, clear non-Hendi PPs")
        print("  - If Sirman-supplier (Maresto/etc.) carries with brand=Sirman → Sirman article,")
        print("    Sirman PP is the legit owner, clear others")
        print("  - If no supplier carries → was manually entered by Yana, ask her")
        print("=" * 90)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
