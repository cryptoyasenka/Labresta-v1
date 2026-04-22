"""Reproduce reject for candidates visible in Yana's current UI."""
import traceback
from app import create_app
from app.extensions import db
from app.models.product_match import ProductMatch
from app.models.supplier_product import SupplierProduct
from app.services.matcher import find_match_for_product


def try_reject(match_id):
    m = db.session.get(ProductMatch, match_id)
    if not m:
        print(f"#{match_id}: not found")
        return
    print(f"\n#{match_id} status={m.status} score={m.score}")
    print(f"  sp_id={m.supplier_product_id} pp_id={m.prom_product_id}")
    sp = m.supplier_product
    rejected_prom_id = m.prom_product_id
    try:
        db.session.delete(m)
        db.session.flush()
        new_match = find_match_for_product(sp, exclude_prom_ids=[rejected_prom_id])
        print(f"  new_match: {new_match}")
        if new_match:
            print(f"    pp_id={new_match.prom_product_id} score={new_match.score} status={new_match.status}")
    except Exception as e:
        print(f"CRASH: {type(e).__name__}: {e}")
        traceback.print_exc()
    finally:
        db.session.rollback()


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        # Find NP supplier candidates that are active
        np_sp = db.session.query(SupplierProduct).filter_by(supplier_id=2).filter(
            SupplierProduct.article.like('HKN-GXSD%')
        ).all()
        print(f"Found {len(np_sp)} HKN-GXSD* supplier products")
        for sp in np_sp[:5]:
            print(f"  SP#{sp.id} article={sp.article!r} name={sp.name[:60]!r}")
            matches = db.session.query(ProductMatch).filter_by(supplier_product_id=sp.id).all()
            for m in matches:
                print(f"    M#{m.id} status={m.status} score={m.score} pp={m.prom_product_id}")

        # Try recent candidate matches for NP
        print("\n\n=== Recent candidate matches for NP ===")
        recent = db.session.query(ProductMatch).join(SupplierProduct).filter(
            SupplierProduct.supplier_id == 2,
            ProductMatch.status == 'candidate'
        ).order_by(ProductMatch.id.desc()).limit(5).all()
        for m in recent:
            print(f"  M#{m.id} sp={m.supplier_product_id} pp={m.prom_product_id} score={m.score}")
            try_reject(m.id)
