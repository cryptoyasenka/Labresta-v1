"""Debug: why did audit miss #1761 (SP#5030 HKN-GXSD2GN -> PP HKN-GXSD2GN-GC)?"""
from app import create_app
from app.extensions import db
from app.models.product_match import ProductMatch
from sqlalchemy import select
from sqlalchemy.orm import joinedload


def main():
    app = create_app()
    with app.app_context():
        for mid in (1761, 1762, 1765, 1766):
            m = db.session.execute(
                select(ProductMatch)
                .options(
                    joinedload(ProductMatch.supplier_product),
                    joinedload(ProductMatch.prom_product),
                )
                .where(ProductMatch.id == mid)
            ).scalar_one_or_none()
            if not m:
                print(f"#{mid}: not found")
                continue
            sp = m.supplier_product
            pp = m.prom_product
            print(f"\n#{mid} {m.status} score={m.score}")
            print(f"  SP#{sp.id}: name={sp.name!r}")
            print(f"     article={sp.article!r}")
            print(f"     external_id={sp.external_id!r}")
            print(f"  PP#{pp.id}: name={pp.name!r}")
            print(f"     article={pp.article!r}")


if __name__ == "__main__":
    main()
