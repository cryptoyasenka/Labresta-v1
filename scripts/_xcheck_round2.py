"""SCRATCH (not committed) — read-only supplier_products cross-check for round-2
value questions (classes D/H/E). Output -> .planning/translation-audit/_xcheck-round2.txt
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import create_app
from app.extensions import db
from app.models import SupplierProduct, PromProduct, ProductMatch

out_path = r".planning\translation-audit\_xcheck-round2.txt"

# (label, horoshop article on the catalog/PP side)
TARGETS = [
    ("D ch008 SKU39 FROSTY ZL1-8L (270 vs 275мм)", "2043363414"),
    ("D ch006 SKU1 Silver 2606 газова (750х510х240 vs 540х210)", "2237515493"),
    ("D ch006 SKU6 Frosty GES-762 (вес 48.50 дубль GES-760)", "2309272534"),
    ("D ch006 GES-760 (для сравнения веса)", "2309265766"),
    ("H ch006 SKU23 OZTI OGE 8070N (Об'єм 100 л)", "2183102436"),
    ("H ch006 SKU26 OZTI OGG 8070 (Об'єм 205 л)", "2183201142"),
    ("H ch006 SKU27 OZTI OGG 8070N (Об'єм 130 л)", "2183203028"),
    ("E ch005 SKU24 Apach APTE-47PR (гладка vs ребриста)", "524338454"),
    ("E ch007 SKU40 Apach APTE-77PL (гладка vs spec ребриста)", "524338456"),
]

lines = []
app = create_app()
with app.app_context():
    db_url = str(db.engine.url)
    lines.append(f"DB: {db_url}")
    lines.append("")
    for label, art in TARGETS:
        lines.append(f"===== {label} | art={art} =====")
        pp = PromProduct.query.filter(
            (PromProduct.article == art) | (PromProduct.display_article == art)
        ).first()
        if pp:
            lines.append(f"  PP#{pp.id} name={pp.name!r}")
            lines.append(f"     name_ru={pp.name_ru!r}")
            lines.append(f"     article={pp.article!r} display_article={pp.display_article!r}")
            ms = ProductMatch.query.filter_by(prom_product_id=pp.id).all()
            for m in ms:
                sp = SupplierProduct.query.get(m.supplier_product_id)
                if sp:
                    lines.append(
                        f"   MATCH m={m.id} status={m.status} -> SP#{sp.id} "
                        f"sup={sp.supplier_id} art={sp.article!r} name={sp.name!r}"
                    )
        else:
            lines.append("  (no PP by article/display_article)")
        # also scan SP by article directly (supplier feed side)
        sps = SupplierProduct.query.filter(SupplierProduct.article == art).all()
        for sp in sps:
            lines.append(
                f"   SP#{sp.id} sup={sp.supplier_id} art={sp.article!r} name={sp.name!r}"
            )
        lines.append("")

with open(out_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print(f"wrote {out_path} ({len(lines)} lines)")
