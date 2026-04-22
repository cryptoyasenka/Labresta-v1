"""Re-check match #1643 + current HKN-HEP2 matches."""
from app import create_app
from app.extensions import db
from app.models.product_match import ProductMatch
from app.models.supplier_product import SupplierProduct


def main():
    app = create_app()
    with app.app_context():
        m = db.session.get(ProductMatch, 1643)
        if m:
            print(f"M#1643 status={m.status} score={m.score}")
            print(f"  SP#{m.supplier_product_id} article={m.supplier_product.article!r} name={m.supplier_product.name!r}")
            print(f"  PP#{m.prom_product_id} name={m.prom_product.name!r}")
        else:
            print("M#1643: NOT FOUND (deleted)")

        # All HEP2 matches
        print("\n=== All HKN-HEP2* matches ===")
        sps = db.session.query(SupplierProduct).filter(
            SupplierProduct.article.like('HKN-HEP2%')
        ).all()
        for sp in sps:
            print(f"\nSP#{sp.id} article={sp.article!r} supplier_id={sp.supplier_id}")
            print(f"  name={sp.name!r}")
            matches = db.session.query(ProductMatch).filter_by(supplier_product_id=sp.id).all()
            for m in matches:
                print(f"  M#{m.id} status={m.status} score={m.score} pp={m.prom_product_id} pp_name={m.prom_product.name[:80] if m.prom_product else '?'!r}")


if __name__ == "__main__":
    main()
