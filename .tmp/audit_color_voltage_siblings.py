"""Read-only audit of confirmed/manual matches for color/voltage sibling collisions.

For each confirmed match where SP has a color/voltage tag and PP does not,
look for a PP sibling under the same base model token that DOES have a
color/voltage tag. If a sibling with the SAME color/voltage as SP exists,
the current match is suspicious — SP probably belongs to the sibling.

Output: .tmp/confirmed-color-voltage-audit-2026-04-29.csv
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
from app.models import ProductMatch, PromProduct
from app.services.matcher import extract_voltages

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


def base_model_keys(name):
    if not name:
        return []
    return [
        tok.upper().replace("-", "")
        for tok in re.findall(r"[A-Za-z0-9\-]+", name)
        if len(tok) >= 5 and re.search(r"\d", tok)
    ]


def main():
    app = create_app()
    out_rows = []
    with app.app_context():
        # Index PP by base model keys
        pp_by_key = {}
        for pp in db.session.query(PromProduct).all():
            for key in base_model_keys(pp.name):
                pp_by_key.setdefault(key, []).append(pp)

        confirmed = (
            db.session.query(ProductMatch)
            .filter(ProductMatch.status.in_(("confirmed", "manual")))
            .all()
        )

        for m in confirmed:
            sp = m.supplier_product
            pp = m.prom_product
            if sp is None or pp is None:
                continue
            sc = extract_colors(sp.name or "")
            sv = extract_voltages(sp.name or "")
            pc = extract_colors(pp.name or "")
            pv = extract_voltages(pp.name or "")

            # We care about asymmetric cases: SP has tag, PP does not.
            sp_has_color_pp_doesnt = bool(sc) and not pc
            sp_has_voltage_pp_doesnt = bool(sv) and not pv
            if not (sp_has_color_pp_doesnt or sp_has_voltage_pp_doesnt):
                continue

            keys = base_model_keys(pp.name)
            sibling_color_match = []
            sibling_voltage_match = []
            sibling_explicit_no_color_no_match = []
            sibling_explicit_no_voltage_no_match = []
            seen_sib_ids = set()
            for key in keys:
                for sib in pp_by_key.get(key, []):
                    if sib.id == pp.id or sib.id in seen_sib_ids:
                        continue
                    seen_sib_ids.add(sib.id)
                    sib_c = extract_colors(sib.name or "")
                    sib_v = extract_voltages(sib.name or "")
                    if sp_has_color_pp_doesnt and sib_c:
                        if sib_c & sc:
                            sibling_color_match.append(sib)
                        else:
                            sibling_explicit_no_color_no_match.append(sib)
                    if sp_has_voltage_pp_doesnt and sib_v:
                        if sib_v & sv:
                            sibling_voltage_match.append(sib)
                        else:
                            sibling_explicit_no_voltage_no_match.append(sib)

            # Severity:
            # HIGH = SP color X, PP no color, sibling with color X exists → SP belongs to sibling
            # MEDIUM = SP color X, PP no color, sibling with color Y (≠X) exists → catalog has color variants but no X-PP; might mean SP-X is a new SKU we don't have catalog for
            # LOW = SP voltage 380, PP no voltage, sibling with voltage 380 exists → same as HIGH but voltage
            severity = ""
            reason_bits = []
            if sibling_color_match:
                severity = "HIGH"
                reason_bits.append("SP color={} matches sibling pp_id={}".format(
                    ",".join(sorted(sc)),
                    sibling_color_match[0].id,
                ))
            elif sibling_voltage_match:
                if "380" in sv or "230" in sv:
                    severity = "HIGH"
                else:
                    severity = "MEDIUM"
                reason_bits.append("SP voltage={} matches sibling pp_id={}".format(
                    ",".join(sorted(sv)),
                    sibling_voltage_match[0].id,
                ))
            elif sibling_explicit_no_color_no_match:
                severity = "MEDIUM"
                reason_bits.append("SP color={} but only different-color siblings ({}) exist".format(
                    ",".join(sorted(sc)),
                    ",".join("pp_id={}".format(s.id) for s in sibling_explicit_no_color_no_match[:3]),
                ))
            elif sibling_explicit_no_voltage_no_match:
                severity = "LOW"
                reason_bits.append("SP voltage={} but only different-voltage siblings exist".format(
                    ",".join(sorted(sv)),
                ))
            else:
                # No sibling with explicit tag — current match is likely fine
                continue

            out_rows.append({
                "match_id": m.id,
                "severity": severity,
                "supplier": sp.supplier.slug if sp.supplier else "?",
                "sp_id": sp.id,
                "pp_id": pp.id,
                "sp_color": ",".join(sorted(sc)),
                "sp_voltage": ",".join(sorted(sv)),
                "sp_name": sp.name,
                "pp_name": pp.name,
                "reason": "; ".join(reason_bits),
                "sibling_color_match_ids": ",".join(str(x.id) for x in sibling_color_match[:5]),
                "sibling_voltage_match_ids": ",".join(str(x.id) for x in sibling_voltage_match[:5]),
            })

    sev_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    out_rows.sort(key=lambda r: (sev_order.get(r["severity"], 99), r["match_id"]))

    out_path = ROOT / ".tmp" / "confirmed-color-voltage-audit-2026-04-29.csv"
    fields = list(out_rows[0].keys()) if out_rows else [
        "match_id", "severity", "supplier", "sp_id", "pp_id", "sp_color",
        "sp_voltage", "sp_name", "pp_name", "reason",
        "sibling_color_match_ids", "sibling_voltage_match_ids",
    ]
    with out_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in out_rows:
            w.writerow(r)

    print("Wrote {} suspicious confirmed matches -> {}".format(len(out_rows), out_path))
    by_sev = {}
    by_sup = {}
    for r in out_rows:
        by_sev[r["severity"]] = by_sev.get(r["severity"], 0) + 1
        by_sup[r["supplier"]] = by_sup.get(r["supplier"], 0) + 1
    print("\n  by severity:", by_sev)
    print("  by supplier:", by_sup)
    print("\nFirst 10 HIGH:")
    for r in out_rows[:10]:
        if r["severity"] != "HIGH":
            break
        print("  #{} sup={} sp_color={} sp_voltage={} sp={!r} pp={!r}".format(
            r["match_id"], r["supplier"], r["sp_color"], r["sp_voltage"],
            r["sp_name"][:60], r["pp_name"][:60],
        ))
        print("    reason: {}".format(r["reason"]))


if __name__ == "__main__":
    main()
