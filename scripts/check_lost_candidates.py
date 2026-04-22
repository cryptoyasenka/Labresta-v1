"""For each lost-match SP in section A, check whether ProductMatch row exists."""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.extensions import db
from app.models.supplier_product import SupplierProduct
from app.models.catalog import PromProduct
from app.models.product_match import ProductMatch
from app.services.matcher import normalize_model


def brand_key(b):
    if not b:
        return ""
    return re.sub(r"[^a-zа-я0-9]", "", b.lower())


# Small sample of lost-match pairs found earlier
SAMPLE_PAIRS = [
    (5012, 2733, "HKN-10SN"),
    (5018, 2983, "HKN-12(CR) SCE"),
    (4995, 2986, "HKN-12SSE"),
    (4974, 4525, "AC800dig DD"),
    (4872, 1509, "ACB130.65B A R290"),
    (4780, 1746, "AFN-1602 EXP"),
    (4940, 1778, "TATRA TRC02BT"),
    (4777, 3108, "66520502"),
]


def main():
    app = create_app()
    with app.app_context():
        no_row = 0
        with_row = 0
        for sp_id, pp_id, label in SAMPLE_PAIRS:
            sp = db.session.get(SupplierProduct, sp_id)
            pp = db.session.get(PromProduct, pp_id)
            m = ProductMatch.query.filter_by(
                supplier_product_id=sp_id, prom_product_id=pp_id
            ).first()
            # Also: any ProductMatch for this sp at all?
            any_match = ProductMatch.query.filter_by(supplier_product_id=sp_id).all()
            print(f"\nsp#{sp_id} '{label}' → pp#{pp_id}")
            print(f"  sp.name  = {sp.name[:90]}")
            print(f"  pp.name  = {pp.name[:90]}")
            print(f"  sp.brand = {sp.brand!r}, pp.brand = {pp.brand!r}")
            if m:
                with_row += 1
                print(f"  *** ProductMatch EXISTS: score={m.score:.1f} status={m.status}")
            else:
                no_row += 1
                print(f"  *** NO ProductMatch row for this pair")
            if any_match:
                print(f"  Other candidates for sp#{sp_id}: {len(any_match)}")
                for am in any_match[:3]:
                    other = db.session.get(PromProduct, am.prom_product_id)
                    print(f"    → pp#{am.prom_product_id} score={am.score:.1f} status={am.status} name={other.name[:70] if other else '?'}")

        print(f"\n\nSummary: no_row={no_row}  with_row={with_row}")


if __name__ == "__main__":
    main()
