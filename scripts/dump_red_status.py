"""Dump current status of all RED_TODO matches with full names (UTF-8 JSON)."""
import json
import re
from app import create_app
from app.extensions import db
from app.models.product_match import ProductMatch


def main():
    with open("RED_TODO.md", "r", encoding="utf-8") as f:
        txt = f.read()

    ids = [int(m) for m in re.findall(r"match \*\*#(\d+)", txt)]

    app = create_app()
    with app.app_context():
        out = []
        for mid in ids:
            m = db.session.get(ProductMatch, mid)
            if not m:
                out.append({"id": mid, "status": "deleted"})
                continue
            out.append({
                "id": mid,
                "status": m.status,
                "score": m.score,
                "sp_id": m.supplier_product_id,
                "pp_id": m.prom_product_id,
                "sp_name": m.supplier_product.name if m.supplier_product else None,
                "sp_article": m.supplier_product.article if m.supplier_product else None,
                "pp_name": m.prom_product.name if m.prom_product else None,
            })

        with open("red_status_current.json", "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
        print(f"Wrote {len(out)} entries to red_status_current.json")


if __name__ == "__main__":
    main()
