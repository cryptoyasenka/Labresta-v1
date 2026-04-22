"""Reproduce the reject error: find_match_for_product on SP#5030 after rejecting #1762."""
import traceback
from app import create_app
from app.extensions import db
from app.models.supplier_product import SupplierProduct
from app.services.matcher import find_match_for_product


def main():
    app = create_app()
    with app.app_context():
        sp = db.session.get(SupplierProduct, 5030)
        print(f"SP#{sp.id}: {sp.name!r}")
        print(f"  brand={sp.brand!r} article={sp.article!r}")
        try:
            new_match = find_match_for_product(sp, exclude_prom_ids=[1419])
            print(f"Result: {new_match}")
            if new_match:
                print(f"  pp_id={new_match.prom_product_id} score={new_match.score}")
        except Exception as e:
            print(f"CRASH: {type(e).__name__}: {e}")
            traceback.print_exc()


if __name__ == "__main__":
    main()
