#!/usr/bin/env python
"""READ-ONLY dossier for the remaining #15 keep-vs-switch conflicts.

After NEEDS-EYEBALL + the 5 ambiguous were resolved, every still-`candidate`
ProductMatch sits on a prom_product that is ALREADY held by a confirmed/manual
match from another (or the same) supplier. That is invariant #15: one PP holds at
most one confirmed/manual supplier. The remaining decision is NOT "is this a
match" — it is policy: KEEP the current confirmed supplier, or SWITCH to the
candidate's supplier (which would mean reject-incumbent + confirm-candidate).

This script mutates NOTHING. It builds a per-candidate-supplier dossier comparing,
for each conflict:
    CANDIDATE  : supplier · SP name · price · availability   (the alternative offer)
    INCUMBENT  : supplier · SP name · price · availability · match status (current)
    PP         : the catalog item both point at
and flags a price signal (candidate cheaper / same / dearer / diff-currency) so the
"keep current" no-brainers (candidate not cheaper) separate from real switch choices.

Output:
  - console summary (counts per candidate supplier + price-signal breakdown)
  - dossier markdown at .planning/keep-vs-switch-2026-06-07.md

Run:  .venv/Scripts/python.exe scripts/triage_15_keep_vs_switch.py
"""
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / ".planning" / "keep-vs-switch-2026-06-07.md"


def money(sp):
    if sp is None or sp.price_cents is None:
        return "—"
    return f"{sp.price_cents / 100:.2f} {sp.currency or '?'}"


def avail(sp):
    if sp is None:
        return "—"
    base = "в наявності" if sp.available else "НЕМАЄ"
    return f"{base} ({sp.stock_status})" if sp.stock_status else base


def price_signal(cand_sp, inc_sp):
    """Compare candidate supplier price vs incumbent supplier price."""
    if cand_sp is None or inc_sp is None:
        return "?"
    if cand_sp.price_cents is None or inc_sp.price_cents is None:
        return "no-price"
    cc, ic = cand_sp.currency or "?", inc_sp.currency or "?"
    if cc != ic:
        return f"diff-cur ({cc} vs {ic})"
    d = cand_sp.price_cents - inc_sp.price_cents
    if d < 0:
        return f"CHEAPER by {abs(d)/100:.2f} {cc}"
    if d > 0:
        return f"dearer by {d/100:.2f} {cc}"
    return f"same ({cc})"


def main():
    sys.path.insert(0, str(ROOT))
    from app import create_app
    from app.extensions import db
    from app.models import ProductMatch

    app = create_app()
    with app.app_context():
        cands = (
            db.session.query(ProductMatch)
            .filter(ProductMatch.status == "candidate")
            .all()
        )

        # incumbent (confirmed/manual) per prom_product_id
        held = defaultdict(list)
        for m in (
            db.session.query(ProductMatch)
            .filter(ProductMatch.status.in_(["confirmed", "manual"]))
            .all()
        ):
            held[m.prom_product_id].append(m)

        conflicts, free = [], []
        for m in cands:
            incs = held.get(m.prom_product_id, [])
            (conflicts if incs else free).append((m, incs[0] if incs else None))

        # group conflicts by CANDIDATE supplier
        by_sup = defaultdict(list)
        for m, inc in conflicts:
            sup = getattr(m.supplier_product.supplier, "name", "?") if m.supplier_product else "?"
            by_sup[sup].append((m, inc))

        # price-signal tally
        sig_tally = defaultdict(int)
        for m, inc in conflicts:
            sig = price_signal(m.supplier_product, inc.supplier_product if inc else None)
            sig_tally[sig.split(" ")[0]] += 1

        print(f"candidates total      : {len(cands)}")
        print(f"#15 conflicts         : {len(conflicts)}")
        print(f"free (no incumbent)   : {len(free)}  {'<-- NOT #15!' if free else ''}")
        print(f"\nby candidate supplier :")
        for sup in sorted(by_sup, key=lambda s: -len(by_sup[s])):
            print(f"  {sup:20s} {len(by_sup[sup])}")
        print(f"\nprice signal (cand vs incumbent):")
        for sig, n in sorted(sig_tally.items(), key=lambda kv: -kv[1]):
            print(f"  {sig:12s} {n}")
        if free:
            print("\nFREE (no incumbent) match_ids:", ", ".join(str(m.id) for m, _ in free))

        # ---- write dossier ----
        lines = []
        lines.append("# #15 keep-vs-switch dossier — LabResta")
        lines.append("")
        lines.append("**Generated:** 2026-06-07 · READ-ONLY (no DB row mutated).")
        lines.append("")
        lines.append(
            "Every row below is a `candidate` match whose catalog PP is ALREADY held by a "
            "confirmed/manual match from the **INCUMBENT** supplier. Decision = policy: "
            "**KEEP** the incumbent (reject the candidate) or **SWITCH** to the candidate's "
            "supplier (reject incumbent's match + confirm candidate). `price` = supplier offer "
            "(`price_cents/100`). Price signal compares candidate vs incumbent (same currency only)."
        )
        lines.append("")
        lines.append(f"**Totals:** {len(conflicts)} #15 conflicts across {len(by_sup)} candidate suppliers.")
        lines.append("")
        for sup in sorted(by_sup, key=lambda s: -len(by_sup[s])):
            rows = sorted(by_sup[sup], key=lambda t: (t[0].prom_product.name or "").lower())
            lines.append(f"## {sup} ({len(rows)})")
            lines.append("")
            lines.append("| cand m_id | score | PP (catalog) | CANDIDATE — SP / price / avail | INCUMBENT — supplier / SP / price / avail / m | price signal |")
            lines.append("|---:|---:|---|---|---|---|")
            for m, inc in rows:
                pp = m.prom_product
                csp = m.supplier_product
                isp = inc.supplier_product if inc else None
                isup = getattr(isp.supplier, "name", "?") if isp else "?"
                pp_name = (pp.name or "").replace("|", "/")
                csp_name = (csp.name or "").replace("|", "/") if csp else "?"
                isp_name = (isp.name or "").replace("|", "/") if isp else "?"
                lines.append(
                    f"| {m.id} | {m.score:.0f} | {pp_name} "
                    f"| {csp_name} · {money(csp)} · {avail(csp)} "
                    f"| {isup} · {isp_name} · {money(isp)} · {avail(isp)} · m{inc.id}:{inc.status} "
                    f"| {price_signal(csp, isp)} |"
                )
            lines.append("")
        OUT.write_text("\n".join(lines), encoding="utf-8")
        print(f"\ndossier written: {OUT}")


if __name__ == "__main__":
    main()
