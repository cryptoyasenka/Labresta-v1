"""Cat H: for each of 7 Hendi-collision PPs, show current matches + potential SP candidates.

After we clear display_article on these PPs, matcher Step 0a will no longer flag a duplicate-anchor
collision. This script tells Yana what's already attached (so she knows whether anything needs
re-confirmation in UI) and what other SPs in the catalog might be the right supplier-side partner.

Read-only.
"""
import sys

from app import create_app
from app.extensions import db
from app.models import PromProduct, SupplierProduct, ProductMatch, Supplier

sys.stdout.reconfigure(encoding="utf-8")

# (pp_id, hint about which model token to look for in SP names)
TARGETS = [
    (347,  "Spidocook SP300"),
    (80,   "Fimar PFD27"),
    (154,  "Roller Grill PIS 30"),
    (958,  "FROSTY RC-30"),
    (3933, "FROSTY IC80A"),
    (3932, "GoodFood ICE777"),
    (4179, "Saro SKZ-12"),
]


def show_pp(pp_id: int, hint: str, sup_names: dict) -> None:
    pp = db.session.get(PromProduct, pp_id)
    if pp is None:
        print(f"\n## PP#{pp_id}  ({hint}) — ❌ NOT FOUND in DB")
        return

    print(f"\n## PP#{pp_id}  ({hint})")
    print(f"   name:            {pp.name}")
    print(f"   brand:           {pp.brand!r}")
    print(f"   display_article: {pp.display_article!r}  (will be CLEARED)")
    print(f"   page_url:        {pp.page_url}")

    # 1) existing matches (any status) ---------------------------------------
    matches = (
        ProductMatch.query
        .filter(ProductMatch.prom_product_id == pp_id)
        .order_by(ProductMatch.status, ProductMatch.id)
        .all()
    )
    if matches:
        print(f"   ── existing matches ({len(matches)}):")
        for m in matches:
            sp = db.session.get(SupplierProduct, m.supplier_product_id)
            sup_name = sup_names.get(sp.supplier_id, f"sup{sp.supplier_id}") if sp else "?"
            sp_name = (sp.name or "?")[:65] if sp else "—"
            sp_brand = (sp.brand or "—") if sp else "—"
            sp_art = (sp.article or "—") if sp else "—"
            print(
                f"      match#{m.id} status={m.status:<10} score={m.score:>5.1f}  "
                f"by={m.confirmed_by or '—'}"
            )
            print(
                f"         → SP#{sp.id if sp else '?'} sup={sup_name!r} brand={sp_brand!r} "
                f"art={sp_art!r}  {sp_name}"
            )
    else:
        print("   ── existing matches: NONE")

    # 2) other potential SP candidates (same brand, NOT already matched) -----
    matched_sp_ids = {m.supplier_product_id for m in matches}
    pp_brand = (pp.brand or "").strip()
    candidates_by_brand = []
    if pp_brand:
        candidates_by_brand = (
            SupplierProduct.query
            .filter(SupplierProduct.brand.ilike(pp_brand))
            .filter(~SupplierProduct.id.in_(matched_sp_ids) if matched_sp_ids else True)
            .order_by(SupplierProduct.supplier_id, SupplierProduct.id)
            .limit(20)
            .all()
        )

    if candidates_by_brand:
        print(f"   ── other SPs with brand={pp_brand!r} (top {len(candidates_by_brand)}):")
        for sp in candidates_by_brand:
            sup_name = sup_names.get(sp.supplier_id, f"sup{sp.supplier_id}")
            sp_name = (sp.name or "?")[:65]
            sp_art = (sp.article or "—")
            print(f"      SP#{sp.id:<6} sup={sup_name!r:<10} art={sp_art!r:<15} {sp_name}")
    else:
        print(f"   ── other SPs with brand={pp_brand!r}: NONE")

    # 3) name-token search across ALL suppliers -------------------------------
    # try to pull a model-token from hint (last word usually = SKU like SP300, PFD27)
    tokens = hint.split()
    likely_model = tokens[-1] if tokens else ""
    if len(likely_model) >= 3:
        token_hits = (
            SupplierProduct.query
            .filter(
                db.or_(
                    SupplierProduct.name.ilike(f"%{likely_model}%"),
                    SupplierProduct.article.ilike(f"%{likely_model}%"),
                )
            )
            .filter(~SupplierProduct.id.in_(matched_sp_ids) if matched_sp_ids else True)
            .order_by(SupplierProduct.supplier_id, SupplierProduct.id)
            .limit(20)
            .all()
        )
        if token_hits:
            print(f"   ── name/article contains {likely_model!r} (top {len(token_hits)}):")
            for sp in token_hits:
                sup_name = sup_names.get(sp.supplier_id, f"sup{sp.supplier_id}")
                sp_name = (sp.name or "?")[:65]
                sp_art = (sp.article or "—")
                sp_brand = (sp.brand or "—")
                print(
                    f"      SP#{sp.id:<6} sup={sup_name!r:<10} brand={sp_brand!r:<12} "
                    f"art={sp_art!r:<15} {sp_name}"
                )
        else:
            print(f"   ── name/article contains {likely_model!r}: NONE")


def main() -> int:
    app = create_app()
    with app.app_context():
        sup_names = {s.id: s.name for s in Supplier.query.all()}
        print("=" * 100)
        print("Cat H — match candidates report for 7 Hendi-collision PPs")
        print("=" * 100)
        for pp_id, hint in TARGETS:
            show_pp(pp_id, hint, sup_names)
        print("\n" + "=" * 100)
        print("Legend:")
        print("  - 'existing matches' = already in product_matches table (confirmed/candidate/rejected)")
        print("  - 'other SPs with brand=X' = potential supplier-side partner with matching brand")
        print("  - 'name/article contains X' = SPs whose name or article hints at the same model token")
        print("=" * 100)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
