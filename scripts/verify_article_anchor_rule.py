"""Verify article-anchor rule on all confirmed matches.

Yana hardcoded rule (LabResta Article Anchor Rule, memory entry 2026-04):
  sp.article must equal pp.display_article AND the same article token must
  appear inside pp.name (or pp.name_ru, or pp.article). All three locations.

This script flags confirmed/manual matches where:
  - pp.display_article is non-empty AND equals sp.article (R0 territory),
    BUT the article token is NOT present in pp.name / pp.name_ru / pp.article.
  - These would be auto-confirms that violated the three-location rule and
    should have stayed candidates.

Also reports confirmed matches that were NOT made via R0 article anchor at all
(score-based fuzzy with no article alignment) — for spot-check awareness.

Read-only.
"""
import os
import re
import sys
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy import select

from app import create_app
from app.extensions import db
from app.models.catalog import PromProduct
from app.models.product_match import ProductMatch
from app.models.supplier import Supplier
from app.models.supplier_product import SupplierProduct
from app.services.matcher import normalize_model


def _norm_text_for_anchor_search(s: str | None) -> str:
    """Same normalization the matcher uses for anchor search inside name:
    lowercase, strip non-alphanumerics → single string of [a-z0-9]."""
    if not s:
        return ""
    return re.sub(r"[^a-z0-9]", "", s.lower())


def main() -> int:
    app = create_app()
    with app.app_context():
        suppliers = {s.id: s for s in db.session.execute(select(Supplier)).scalars().all()}
        sps = {sp.id: sp for sp in db.session.execute(select(SupplierProduct)).scalars().all()}
        pps = {pp.id: pp for pp in db.session.execute(select(PromProduct)).scalars().all()}

        confirmed = [m for m in db.session.execute(select(ProductMatch)).scalars().all()
                     if m.status in ("confirmed", "manual")]

        # Buckets
        rule_violations = []      # display_article matches sp.article but anchor not in pp.name/pp.article
        no_article_alignment = [] # match exists but no article-anchor at all (fuzzy/manual)
        ok_three_way = 0          # all three locations have the anchor — rule satisfied
        ok_two_way_no_disp = 0    # pp.display_article empty but article in name+sp.article (R0 path B only)

        for m in confirmed:
            sp = sps.get(m.supplier_product_id)
            pp = pps.get(m.prom_product_id)
            if not sp or not pp:
                continue

            sp_a = normalize_model(sp.article) if sp.article else ""
            pp_d = normalize_model(pp.display_article) if pp.display_article else ""
            pp_a = normalize_model(pp.article) if pp.article else ""

            # search the article token inside name/name_ru as a substring of normalized text
            name_blob = _norm_text_for_anchor_search(
                f"{pp.name or ''} {pp.name_ru or ''}"
            )

            # Case 1: pp.display_article matches sp.article exactly (R0 path A territory)
            if sp_a and pp_d and sp_a == pp_d and len(sp_a) >= 4:
                # Check rule: anchor must also appear in pp.name (or pp.article)
                in_name = sp_a in name_blob
                in_pp_article = (pp_a == sp_a) if pp_a else False
                if in_name or in_pp_article:
                    ok_three_way += 1
                else:
                    rule_violations.append((m, sp, pp, sp_a))
            elif sp_a and not pp_d:
                # No display_article — only name-based check could've fired
                if sp_a in name_blob or (pp_a and pp_a == sp_a):
                    ok_two_way_no_disp += 1
                else:
                    no_article_alignment.append((m, sp, pp, sp_a, "no display_article + no name hit"))
            elif not sp_a:
                no_article_alignment.append((m, sp, pp, "", "supplier has no article"))
            else:
                # display_article exists but doesn't equal sp.article
                no_article_alignment.append((m, sp, pp, sp_a, f"display_article={pp.display_article!r} != sp.article={sp.article!r}"))

        print("# Article-Anchor Rule Verification\n")
        print(f"**Total confirmed/manual matches:** {len(confirmed)}\n")
        print("## Summary\n")
        print(f"- ✅ Three-way anchor (display_article == sp.article AND in name/pp.article): **{ok_three_way}**")
        print(f"- ✅ Two-way (no display_article but article in name + sp.article): **{ok_two_way_no_disp}**")
        print(f"- ⚠ Rule violations (display_article == sp.article but NOT in name/pp.article): **{len(rule_violations)}**")
        print(f"- ℹ No article-anchor at all (fuzzy / mismatched / manual): **{len(no_article_alignment)}**")
        print()

        # ---- Rule violations: the dangerous bucket ----
        print("## ⚠ Rule violations (auto-confirmed but anchor missing from name)\n")
        if not rule_violations:
            print("  (none — rule fully respected on all auto-confirms)\n")
        else:
            print(f"These {len(rule_violations)} confirmed matches violate the three-location rule.")
            print(f"They should have stayed in 'candidate' status pending manual review.\n")
            by_sup = defaultdict(list)
            for m, sp, pp, anchor in rule_violations:
                sup_name = suppliers[sp.supplier_id].name if sp.supplier_id in suppliers else f"sup#{sp.supplier_id}"
                by_sup[sup_name].append((m, sp, pp, anchor))
            for sup_name in sorted(by_sup):
                rows = by_sup[sup_name]
                print(f"### {sup_name} — {len(rows)} шт.")
                for m, sp, pp, anchor in rows:
                    print(f"  match#{m.id} status={m.status} score={m.score} anchor={anchor!r}")
                    print(f"    PP#{pp.id} disp={pp.display_article!r} pp.article={pp.article!r}")
                    print(f"      name   = {(pp.name or '')[:120]!r}")
                    print(f"      name_ru= {(pp.name_ru or '')[:120]!r}")
                    print(f"    SP#{sp.id} art={sp.article!r}")
                    print(f"      name   = {(sp.name or '')[:120]!r}")
                print()

        # ---- No article-anchor: fuzzy / manual — informational ----
        print("## ℹ No article-anchor at all (fuzzy/manual confirmed)\n")
        if not no_article_alignment:
            print("  (none — every confirmed has some article alignment)\n")
        else:
            by_reason = defaultdict(list)
            for m, sp, pp, anchor, reason in no_article_alignment:
                by_reason[reason].append((m, sp, pp, anchor))
            for reason in sorted(by_reason):
                rows = by_reason[reason]
                print(f"### {reason} — {len(rows)} шт.")
                for m, sp, pp, anchor in rows[:10]:
                    sup_name = suppliers[sp.supplier_id].name if sp.supplier_id in suppliers else f"sup#{sp.supplier_id}"
                    print(f"  match#{m.id} sup={sup_name!r} score={m.score}")
                    print(f"    PP#{pp.id} disp={pp.display_article!r} {(pp.name or '')[:80]!r}")
                    print(f"    SP#{sp.id} art={sp.article!r} {(sp.name or '')[:80]!r}")
                if len(rows) > 10:
                    print(f"  ... +{len(rows)-10} more")
                print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
