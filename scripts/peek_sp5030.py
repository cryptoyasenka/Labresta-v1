"""List all matches for SP#5030 and SP#5031 — what are the actual ambiguous pairs?"""
from app import create_app
from app.extensions import db
from app.models.product_match import ProductMatch
from sqlalchemy import select
from sqlalchemy.orm import joinedload


def main():
    app = create_app()
    with app.app_context():
        for sp_id in (5030, 5031):
            rows = db.session.execute(
                select(ProductMatch)
                .options(joinedload(ProductMatch.prom_product))
                .where(ProductMatch.supplier_product_id == sp_id)
            ).scalars().all()
            print(f"\n=== SP#{sp_id}: {len(rows)} matches ===")
            for m in rows:
                pp = m.prom_product
                print(f"  #{m.id} status={m.status} score={m.score}  PP#{pp.id}: {pp.name!r}")


if __name__ == "__main__":
    main()
