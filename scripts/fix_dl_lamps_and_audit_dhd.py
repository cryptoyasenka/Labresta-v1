"""Confirm DL775/DL800 bronze matches and audit ALL Hurakan dehydrators.

Yana says HKN-DHD**M and HKN-DHD**GM are DIFFERENT products.
Horoshop has DHD12G/DHD16G (or similar non-GM); supplier has DHD12GM/DHD16GM.
She insists supplier feed ALSO has non-GM variants — verify by dumping every
HKN-DHD SP in supplier_id=2 (НП).

Also creates MANUAL matches for:
  SP#5066 HKN-DL775 bronze → PP with lab_url ...hkn-dl775-bronzova...
  SP#5068 HKN-DL800 bronze → PP with lab_url ...hkn-dl800-bronza...

Dry-run by default. --apply to commit.
"""
import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import or_

from app import create_app
from app.extensions import db
from app.models.catalog import PromProduct
from app.models.product_match import ProductMatch
from app.models.supplier_product import SupplierProduct


LAMP_PAIRS = [
    # (sp_id, url fragments to match PP.page_url)
    (5066, ["hkn-dl775", "bronz"]),  # bronzova
    (5068, ["hkn-dl800", "bronz"]),  # bronza
]


def _find_pp_by_url_fragments(fragments: list[str]) -> list[PromProduct]:
    q = db.session.query(PromProduct)
    for frag in fragments:
        q = q.filter(PromProduct.page_url.ilike(f"%{frag}%"))
    return q.all()


def confirm_lamp(sp_id: int, fragments: list[str], apply: bool) -> bool:
    sp = db.session.get(SupplierProduct, sp_id)
    if not sp:
        print(f"  SP#{sp_id}: NOT FOUND")
        return False

    pps = _find_pp_by_url_fragments(fragments)
    if len(pps) != 1:
        print(f"  SP#{sp_id} ({sp.article}): PP search fragments={fragments} "
              f"→ {len(pps)} hits (need exactly 1)")
        for pp in pps[:5]:
            print(f"     pp#{pp.id} {pp.name} | {pp.page_url}")
        return False
    pp = pps[0]

    existing = db.session.query(ProductMatch).filter_by(
        supplier_product_id=sp.id, prom_product_id=pp.id
    ).first()
    if existing:
        print(f"  SP#{sp_id} ↔ pp#{pp.id}: match#{existing.id} already exists "
              f"(status={existing.status})")
        if existing.status in ("confirmed", "manual"):
            return False
        if apply:
            existing.status = "manual"
            existing.confirmed_at = datetime.now(timezone.utc)
            existing.confirmed_by = "script:fix_dl_lamps"
            print(f"    → upgraded to manual")
        return True

    # Check pp not already claimed
    claimed = db.session.query(ProductMatch).filter(
        ProductMatch.prom_product_id == pp.id,
        ProductMatch.status.in_(("confirmed", "manual")),
    ).first()
    if claimed:
        print(f"  SP#{sp_id} ↔ pp#{pp.id}: pp already claimed by "
              f"match#{claimed.id} (sp#{claimed.supplier_product_id}) — SKIP")
        return False

    print(f"  SP#{sp_id} {sp.article!r}  ↔  pp#{pp.id} {pp.name!r}")
    print(f"       lab_url: {pp.page_url}")
    if apply:
        m = ProductMatch(
            supplier_product_id=sp.id,
            prom_product_id=pp.id,
            score=100.0,
            status="manual",
            confirmed_at=datetime.now(timezone.utc),
            confirmed_by="script:fix_dl_lamps",
        )
        db.session.add(m)
        print(f"       → CREATED manual match")
    return True


def audit_hurakan_dehydrators():
    """Dump every SP in НП (supplier_id=2) whose article or name contains DHD."""
    print("\n=== ALL HKN-DHD in supplier_id=2 (НП) ===")
    sps = db.session.query(SupplierProduct).filter(
        SupplierProduct.supplier_id == 2,
        or_(
            SupplierProduct.article.ilike("%DHD%"),
            SupplierProduct.name.ilike("%DHD%"),
            SupplierProduct.article.ilike("%дегідрат%"),
            SupplierProduct.name.ilike("%дегідрат%"),
            SupplierProduct.article.ilike("%дегидрат%"),
            SupplierProduct.name.ilike("%дегидрат%"),
        ),
    ).order_by(SupplierProduct.article).all()
    if not sps:
        print("  (none found)")
        return
    for sp in sps:
        status = "DEL" if getattr(sp, "is_deleted", False) else "active"
        ext = getattr(sp, "external_id", None)
        print(f"  sp#{sp.id} [{status}] article={sp.article!r} ext={ext!r}")
        print(f"    name={sp.name!r}")

    print("\n=== Matches for those SPs ===")
    sp_ids = [sp.id for sp in sps]
    matches = db.session.query(ProductMatch).filter(
        ProductMatch.supplier_product_id.in_(sp_ids)
    ).all()
    if not matches:
        print("  (no matches at all)")
    for m in matches:
        pp = db.session.get(PromProduct, m.prom_product_id)
        pp_name = pp.name if pp else "?"
        pp_url = pp.page_url if pp else "?"
        print(f"  match#{m.id} sp#{m.supplier_product_id} → pp#{m.prom_product_id} "
              f"status={m.status}")
        print(f"    pp.name={pp_name!r}")
        print(f"    pp.url={pp_url!r}")


def audit_horoshop_dehydrators():
    """Every PP in Horoshop catalog with DHD in url/name."""
    print("\n=== ALL Horoshop PP with DHD in url/name ===")
    pps = db.session.query(PromProduct).filter(
        or_(
            PromProduct.page_url.ilike("%dhd%"),
            PromProduct.name.ilike("%dhd%"),
            PromProduct.name.ilike("%дегідрат%"),
        ),
    ).order_by(PromProduct.name).all()
    for pp in pps:
        print(f"  pp#{pp.id} {pp.name!r}")
        print(f"    url={pp.page_url!r}")
        print(f"    article={pp.article!r} display_article={pp.display_article!r}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--apply", action="store_true")
    args = p.parse_args()

    app = create_app()
    with app.app_context():
        print("=== Creating manual matches for DL775/DL800 bronze ===")
        changed = False
        for sp_id, frags in LAMP_PAIRS:
            if confirm_lamp(sp_id, frags, args.apply):
                changed = True

        audit_horoshop_dehydrators()
        audit_hurakan_dehydrators()

        if args.apply and changed:
            db.session.commit()
            print("\nCOMMITTED.")
        elif args.apply:
            print("\nNothing to apply.")
        else:
            print("\nDRY-RUN — pass --apply to commit lamp matches.")


if __name__ == "__main__":
    main()
