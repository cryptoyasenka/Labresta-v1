"""Check status of the 36 red candidates from RED_TODO.md."""
import re
from app import create_app
from app.extensions import db
from app.models.product_match import ProductMatch


def main():
    with open("RED_TODO.md", "r", encoding="utf-8") as f:
        txt = f.read()

    ids = [int(m) for m in re.findall(r"match \*\*#(\d+)", txt)]
    print(f"Total in RED_TODO: {len(ids)}")

    app = create_app()
    with app.app_context():
        still_candidate = []
        confirmed = []
        manual = []
        rejected_or_deleted = []

        for mid in ids:
            m = db.session.get(ProductMatch, mid)
            if not m:
                rejected_or_deleted.append(mid)
                continue
            if m.status == "candidate":
                still_candidate.append((mid, m.supplier_product_id, m.prom_product_id, m.score))
            elif m.status == "confirmed":
                confirmed.append(mid)
            elif m.status == "manual":
                manual.append(mid)
            else:
                rejected_or_deleted.append(mid)

        print(f"\nProcessed: {len(confirmed)} confirmed + {len(manual)} manual + {len(rejected_or_deleted)} rejected/deleted = {len(confirmed)+len(manual)+len(rejected_or_deleted)}")
        print(f"Still candidate (TO REVIEW): {len(still_candidate)}")

        if still_candidate:
            print("\n=== Still pending ===")
            for mid, sp_id, pp_id, score in still_candidate:
                m = db.session.get(ProductMatch, mid)
                sp = m.supplier_product
                pp = m.prom_product
                print(f"  M#{mid} score={score} SP#{sp_id} -> PP#{pp_id}")
                print(f"    SP: {sp.name[:80] if sp else '?'}")
                print(f"    PP: {pp.name[:80] if pp else '?'}")


if __name__ == "__main__":
    main()
