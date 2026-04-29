"""Read-only triage script for candidate matches.

Buckets each candidate by safety signals so Yana can prioritize manual review.

Output: .tmp/candidates-triage-2026-04-29.csv
"""
import csv
import io
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app import create_app
from app.extensions import db
from app.models import ProductMatch, PromProduct, SupplierProduct
from app.services.matcher import extract_voltages, normalize_text

_COLOR_TOKENS = {
    "black", "white", "silver", "inox", "gold", "red", "blue", "green",
    "matte", "abs",
    "чорний",
    "білий",
    "сірий",
    "червоний",
    "синій",
    "зелений",
}


def extract_colors(name):
    if not name:
        return set()
    n = name.lower()
    found = set()
    for tok in _COLOR_TOKENS:
        if re.search(r"(^|[\s,()\-])" + re.escape(tok) + r"([\s,()\-]|$)", n):
            found.add(tok)
    return found


def norm_brand(b):
    if not b:
        return ""
    return b.strip().lower()


def norm_artikul(a):
    if not a:
        return ""
    return re.sub(r"[\s\-_/.,]", "", a.strip().upper())


def main():
    app = create_app()
    out_rows = []
    summary = {
        "total": 0,
        "artikul_match": 0,
        "identical_name": 0,
        "voltage_mismatch": 0,
        "color_mismatch": 0,
        "brand_mismatch": 0,
        "pp_conflict": 0,
        "by_supplier": {},
        "by_score_bucket": {"100": 0, "95-99": 0, "85-94": 0, "75-84": 0, "60-74": 0, "<60": 0},
    }
    with app.app_context():
        cands = (
            db.session.query(ProductMatch)
            .filter(ProductMatch.status == "candidate")
            .all()
        )
        pp_index = {}
        for pp in db.session.query(PromProduct).all():
            for tok in re.findall(r"[A-Za-z0-9\-]+", pp.name or ""):
                if len(tok) >= 5 and re.search(r"\d", tok):
                    key = tok.upper().replace("-", "")
                    pp_index.setdefault(key, []).append(pp)

        conflict_pp_ids = set(
            mid for (mid,) in db.session.query(ProductMatch.prom_product_id)
            .filter(ProductMatch.status.in_(("confirmed", "manual")))
            .all()
        )

        for m in cands:
            sp = m.supplier_product
            pp = m.prom_product
            if sp is None or pp is None:
                continue
            summary["total"] += 1

            sup_slug = sp.supplier.slug if sp.supplier else "?"
            summary["by_supplier"][sup_slug] = summary["by_supplier"].get(sup_slug, 0) + 1

            score = float(m.score or 0)
            if score >= 100:
                bucket = "100"
            elif score >= 95:
                bucket = "95-99"
            elif score >= 85:
                bucket = "85-94"
            elif score >= 75:
                bucket = "75-84"
            elif score >= 60:
                bucket = "60-74"
            else:
                bucket = "<60"
            summary["by_score_bucket"][bucket] += 1

            artikul_match = bool(
                norm_artikul(sp.article)
                and (
                    norm_artikul(sp.article) == norm_artikul(pp.article)
                    or norm_artikul(sp.article) == norm_artikul(pp.display_article)
                )
            )
            identical_name = normalize_text(sp.name or "") == normalize_text(pp.name or "")

            sv = extract_voltages(sp.name or "")
            pv = extract_voltages(pp.name or "")
            voltage_mismatch = bool(sv and pv and not (sv & pv))

            sc = extract_colors(sp.name or "")
            pc = extract_colors(pp.name or "")
            color_direct_mismatch = bool(sc and pc and not (sc & pc))
            color_sibling_collision = False
            if sc and not pc:
                base_tokens = [
                    tok.upper().replace("-", "")
                    for tok in re.findall(r"[A-Za-z0-9\-]+", pp.name or "")
                    if len(tok) >= 5 and re.search(r"\d", tok)
                ]
                for key in base_tokens:
                    for sib in pp_index.get(key, []):
                        if sib.id == pp.id:
                            continue
                        sib_colors = extract_colors(sib.name or "")
                        if sib_colors and sib_colors & sc:
                            color_sibling_collision = True
                            break
                    if color_sibling_collision:
                        break
            color_mismatch = color_direct_mismatch or color_sibling_collision

            sb = norm_brand(sp.brand)
            pb = norm_brand(pp.brand)
            brand_mismatch = bool(sb and pb and sb != pb)

            pp_conflict = pp.id in conflict_pp_ids

            if artikul_match:
                summary["artikul_match"] += 1
            if identical_name:
                summary["identical_name"] += 1
            if voltage_mismatch:
                summary["voltage_mismatch"] += 1
            if color_mismatch:
                summary["color_mismatch"] += 1
            if brand_mismatch:
                summary["brand_mismatch"] += 1
            if pp_conflict:
                summary["pp_conflict"] += 1

            if pp_conflict:
                rec = "NEEDS_POLICY"
            elif voltage_mismatch or color_mismatch or brand_mismatch:
                rec = "REJECT"
            elif artikul_match or identical_name:
                rec = "SAFE_CONFIRM"
            elif score >= 95:
                rec = "REVIEW_HIGH"
            elif score >= 80:
                rec = "REVIEW_MID"
            else:
                rec = "REVIEW_LOW"

            out_rows.append({
                "match_id": m.id,
                "score": round(score, 1),
                "score_bucket": bucket,
                "supplier": sup_slug,
                "sp_id": sp.id,
                "pp_id": pp.id,
                "sp_name": sp.name,
                "pp_name": pp.name,
                "sp_brand": sp.brand or "",
                "pp_brand": pp.brand or "",
                "sp_article": sp.article or "",
                "pp_article": pp.article or "",
                "pp_display_article": pp.display_article or "",
                "artikul_match": "Y" if artikul_match else "",
                "identical_name": "Y" if identical_name else "",
                "voltage_mismatch": "Y" if voltage_mismatch else "",
                "color_mismatch": "Y" if color_mismatch else "",
                "brand_mismatch": "Y" if brand_mismatch else "",
                "pp_conflict": "Y" if pp_conflict else "",
                "recommendation": rec,
            })

    rec_order = {
        "SAFE_CONFIRM": 0,
        "REVIEW_HIGH": 1,
        "REVIEW_MID": 2,
        "REVIEW_LOW": 3,
        "REJECT": 4,
        "NEEDS_POLICY": 5,
    }
    out_rows.sort(key=lambda r: (rec_order.get(r["recommendation"], 99), -r["score"]))

    out_path = ROOT / ".tmp" / "candidates-triage-2026-04-29.csv"
    fields = list(out_rows[0].keys()) if out_rows else []
    with out_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in out_rows:
            w.writerow(r)

    print("Wrote {} rows -> {}".format(len(out_rows), out_path))
    print("\nSummary:")
    print("  total:", summary["total"])
    print("  by supplier:", summary["by_supplier"])
    print("  by score bucket:", summary["by_score_bucket"])
    print("  artikul match:", summary["artikul_match"])
    print("  identical name:", summary["identical_name"])
    print("  voltage mismatch:", summary["voltage_mismatch"])
    print("  color mismatch:", summary["color_mismatch"])
    print("  brand mismatch:", summary["brand_mismatch"])
    print("  pp conflict (1pp<->1supplier):", summary["pp_conflict"])
    by_rec = {}
    for r in out_rows:
        by_rec[r["recommendation"]] = by_rec.get(r["recommendation"], 0) + 1
    print("\n  by recommendation:")
    for k, v in sorted(by_rec.items(), key=lambda kv: rec_order.get(kv[0], 99)):
        print("    {}: {}".format(k, v))


if __name__ == "__main__":
    main()
