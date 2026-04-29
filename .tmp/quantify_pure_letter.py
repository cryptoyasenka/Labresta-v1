"""Quantify how many confirmed/manual matches went through (or could have used)
the pure-letter SKU fast-path in matcher.py:941-950.

Conditions reproduced from matcher.py:
  - sup_article = normalize_model(supplier_article)  (post-normalize)
  - raw_article = re.sub(r"/pl$", "", supplier_article).strip()
  - has_dash = "-" in raw_article
  - has_digit = any(c.isdigit() for c in raw_article)
  - is_pure_letter_sku = has_dash and not has_digit
  - len(sup_article) >= 6
  - sup_article in normalize_model(pp.name)

If all true, the match WOULD fall through to the pure-letter branch IF earlier
fast-paths (article==prom_article, sup_article==prom_display, etc.) didn't fire.

Output: .tmp/pure-letter-quantify-2026-04-29.txt
"""
import io
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app import create_app
from app.extensions import db
from app.models import ProductMatch
from app.services.matcher import normalize_model


def main():
    app = create_app()
    eligible = []
    earlier_path_could_match = []
    only_pure_letter = []
    total = 0

    with app.app_context():
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
            total += 1
            raw_article = re.sub(
                r"/pl$", "", (sp.article or "").strip(), flags=re.IGNORECASE
            )
            if not raw_article:
                continue
            has_dash = "-" in raw_article
            has_digit = any(c.isdigit() for c in raw_article)
            if not (has_dash and not has_digit):
                continue
            sup_article = normalize_model(sp.article or "")
            if len(sup_article) < 6:
                continue
            pp_name_norm = normalize_model(pp.name or "")
            if not (pp_name_norm and sup_article in pp_name_norm):
                continue

            prom_article = normalize_model(pp.article or "")
            prom_display = normalize_model(pp.display_article or "")
            sup_name_norm = normalize_model(sp.name or "")
            earlier_match = False
            if sup_article == prom_article and sup_article:
                earlier_match = True
            elif prom_display and sup_article == prom_display:
                earlier_match = True
            elif (
                prom_display
                and len(prom_display) >= 6
                and any(c.isalpha() for c in prom_display)
                and any(c.isdigit() for c in prom_display)
                and sup_name_norm
                and prom_display in sup_name_norm
            ):
                earlier_match = True

            snapshot = {
                "match_id": m.id,
                "status": m.status,
                "sup_slug": sp.supplier.slug if sp.supplier else "?",
                "sp_article": sp.article,
                "sp_name": sp.name,
                "pp_article": pp.article,
                "pp_display_article": pp.display_article,
                "pp_name": pp.name,
            }
            eligible.append(snapshot)
            if earlier_match:
                earlier_path_could_match.append(snapshot)
            else:
                only_pure_letter.append(snapshot)

    out_path = ROOT / ".tmp" / "pure-letter-quantify-2026-04-29.txt"
    lines = []
    lines.append("Pure-letter SKU fast-path quantification (#14)")
    lines.append("=" * 60)
    lines.append(f"Total confirmed/manual matches: {total}")
    lines.append(f"Pass pure-letter eligibility (would match via line 941-950 IF reached): {len(eligible)}")
    lines.append(f"  - Also matchable via stronger earlier fast-path (lines 895-917): {len(earlier_path_could_match)}")
    lines.append(f"  - ONLY matchable via pure-letter (no earlier path): {len(only_pure_letter)}")
    lines.append("")

    if only_pure_letter:
        lines.append("These matches DEPEND on pure-letter fast-path:")
        lines.append("-" * 60)
        for s in only_pure_letter[:50]:
            lines.append(
                f"  match #{s['match_id']} sup={s['sup_slug']} status={s['status']}"
            )
            lines.append(f"    sp.article={s['sp_article']!r}  sp.name={s['sp_name']!r}")
            lines.append(
                f"    pp.article={s['pp_article']!r}  pp.display_article={s['pp_display_article']!r}"
            )
            lines.append(f"    pp.name={s['pp_name']!r}")
        if len(only_pure_letter) > 50:
            lines.append(f"  ... and {len(only_pure_letter) - 50} more")
    else:
        lines.append("VERDICT: 0 confirmed matches DEPEND on the pure-letter fast-path.")
        lines.append("All eligible matches would also have been caught by stronger earlier fast-paths.")
        lines.append("=> #14 is academic — close as deferred or wontfix.")

    if eligible and not only_pure_letter:
        lines.append("")
        lines.append("Sample of {} eligible (but redundant) matches:".format(min(10, len(eligible))))
        lines.append("-" * 60)
        for s in eligible[:10]:
            lines.append(
                f"  match #{s['match_id']} sup={s['sup_slug']} sp.article={s['sp_article']!r}"
            )

    text = "\n".join(lines) + "\n"
    out_path.write_text(text, encoding="utf-8")
    print(text)
    print(f"Wrote -> {out_path}")


if __name__ == "__main__":
    main()
