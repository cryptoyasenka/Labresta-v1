"""Audit v2: extract all article-like tokens (letters+digits+dashes, >=4 chars,
with at least 1 digit) from SP and PP names+articles. Compare anchors.

Catches crosses like 'HKN-GXSD2GN' vs 'HKN-GXSD2GN-SC' (different SKUs).
"""

import json
import re
from app import create_app
from app.extensions import db
from app.models.product_match import ProductMatch
from sqlalchemy import select
from sqlalchemy.orm import joinedload


ARTICLE_RE = re.compile(r"[A-Za-z0-9]+(?:-[A-Za-z0-9]+)+")


def extract_articles(s: str) -> set:
    if not s:
        return set()
    out = set()
    for m in ARTICLE_RE.finditer(s):
        tok = m.group(0).upper()
        if any(c.isdigit() for c in tok) and len(tok) >= 5:
            out.add(tok)
    return out


def main():
    with open("red_safe_100_ids.json", encoding="utf-8") as f:
        ids = json.load(f)

    app = create_app()
    with app.app_context():
        matches = db.session.execute(
            select(ProductMatch)
            .options(
                joinedload(ProductMatch.supplier_product),
                joinedload(ProductMatch.prom_product),
            )
            .where(ProductMatch.id.in_(ids))
        ).scalars().all()

        suspicious = []
        ok = []
        for m in matches:
            sp_name = m.supplier_product.name or ""
            sp_article = m.supplier_product.article or ""
            pp_name = m.prom_product.name or ""
            pp_article = m.prom_product.article or ""

            sp_tokens = extract_articles(f"{sp_name} {sp_article}")
            pp_tokens = extract_articles(f"{pp_name} {pp_article}")

            # Find common longest prefix token
            reasons = []
            if sp_tokens and pp_tokens and not (sp_tokens & pp_tokens):
                # No exact article match — check if one is prefix of another
                cross = False
                for st in sp_tokens:
                    for pt in pp_tokens:
                        if st != pt and (st.startswith(pt) or pt.startswith(st)):
                            reasons.append(
                                f"article-cross SP={st!r} vs PP={pt!r} "
                                f"(one is prefix of the other — likely different SKU)"
                            )
                            cross = True
                if not cross:
                    reasons.append(
                        f"no common article token SP={sp_tokens} PP={pp_tokens}"
                    )

            row = {
                "match_id": m.id,
                "score": m.score,
                "sp_id": m.supplier_product_id,
                "pp_id": m.prom_product_id,
                "sp_name": sp_name,
                "sp_article": sp_article,
                "pp_name": pp_name,
                "pp_article": pp_article,
                "sp_tokens": sorted(sp_tokens),
                "pp_tokens": sorted(pp_tokens),
                "reasons": reasons,
            }
            if reasons:
                suspicious.append(row)
            else:
                ok.append(row)

        print(f"Total audited: {len(matches)}")
        print(f"  OK: {len(ok)}")
        print(f"  SUSPICIOUS: {len(suspicious)}")

        if suspicious:
            print("\n=== SUSPICIOUS (article-anchor mismatch) ===")
            for r in suspicious:
                print(f"\nmatch #{r['match_id']} score={r['score']}")
                print(f"  SP#{r['sp_id']}: {r['sp_name']}")
                print(f"     article={r['sp_article']!r}  tokens={r['sp_tokens']}")
                print(f"  PP#{r['pp_id']}: {r['pp_name']}")
                print(f"     article={r['pp_article']!r}  tokens={r['pp_tokens']}")
                for reason in r["reasons"]:
                    print(f"  WARN {reason}")

        with open("red_audit_v2_result.json", "w", encoding="utf-8") as f:
            json.dump({"ok": ok, "suspicious": suspicious}, f, ensure_ascii=False, indent=2)
        print(f"\nFull report: red_audit_v2_result.json")


if __name__ == "__main__":
    main()
