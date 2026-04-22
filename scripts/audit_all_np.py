"""Full NP audit: every ProductMatch (supplier_id=2) in status
confirmed/manual/candidate. Flag article-anchor mismatches and prefix-crosses.
"""

import json
import re
from app import create_app
from app.extensions import db
from app.models.product_match import ProductMatch
from app.models.supplier_product import SupplierProduct
from sqlalchemy import select
from sqlalchemy.orm import joinedload


ARTICLE_RE = re.compile(r"[A-Za-z0-9]+(?:-[A-Za-z0-9]+)+")
VOLTAGE_RE = re.compile(r"\((220|380|110)\)|\b(220|380|110)\s*[вВvV]?\b")


def extract_articles(s: str) -> set:
    if not s:
        return set()
    out = set()
    for m in ARTICLE_RE.finditer(s):
        tok = m.group(0).upper()
        if any(c.isdigit() for c in tok) and len(tok) >= 5:
            out.add(tok)
    return out


def voltages(s: str) -> set:
    if not s:
        return set()
    out = set()
    for m in VOLTAGE_RE.finditer(s or ""):
        for g in m.groups():
            if g:
                out.add(g)
    return out


def analyze(m):
    sp_name = m.supplier_product.name or ""
    sp_article = m.supplier_product.article or ""
    pp_name = m.prom_product.name or ""
    pp_article = m.prom_product.article or ""

    sp_tokens = extract_articles(f"{sp_name} {sp_article}")
    pp_tokens = extract_articles(f"{pp_name} {pp_article}")
    sp_volt = voltages(f"{sp_name} {sp_article}")
    pp_volt = voltages(f"{pp_name} {pp_article}")

    flags = []
    severity = "ok"

    if sp_volt and pp_volt and sp_volt != pp_volt:
        flags.append(f"voltage mismatch SP={sp_volt} PP={pp_volt}")
        severity = "critical"

    if sp_tokens and pp_tokens:
        if sp_tokens & pp_tokens:
            pass
        else:
            cross_found = False
            for st in sp_tokens:
                for pt in pp_tokens:
                    if st == pt:
                        continue
                    if st.startswith(pt) or pt.startswith(st):
                        diff_a = st[len(pt):] if st.startswith(pt) else pt[len(st):]
                        flags.append(
                            f"article-cross SP={st} vs PP={pt} (diff={diff_a!r})"
                        )
                        severity = "critical"
                        cross_found = True
            if not cross_found:
                flags.append(f"no common article token SP={sorted(sp_tokens)} PP={sorted(pp_tokens)}")
                if severity == "ok":
                    severity = "warn"

    return {
        "match_id": m.id,
        "status": m.status,
        "score": m.score,
        "sp_id": m.supplier_product_id,
        "pp_id": m.prom_product_id,
        "sp_name": sp_name,
        "sp_article": sp_article,
        "pp_name": pp_name,
        "pp_article": pp_article,
        "sp_tokens": sorted(sp_tokens),
        "pp_tokens": sorted(pp_tokens),
        "flags": flags,
        "severity": severity,
    }


def main():
    app = create_app()
    with app.app_context():
        matches = db.session.execute(
            select(ProductMatch)
            .options(
                joinedload(ProductMatch.supplier_product),
                joinedload(ProductMatch.prom_product),
            )
            .join(SupplierProduct, ProductMatch.supplier_product_id == SupplierProduct.id)
            .where(
                SupplierProduct.supplier_id == 2,
                ProductMatch.status.in_(("confirmed", "manual", "candidate")),
            )
        ).scalars().all()

        by_status = {"confirmed": [], "manual": [], "candidate": []}
        for m in matches:
            by_status.setdefault(m.status, []).append(m)

        print(f"Total NP matches audited: {len(matches)}")
        for s, lst in by_status.items():
            print(f"  {s}: {len(lst)}")

        critical = []
        warn = []
        ok_count = 0
        for m in matches:
            r = analyze(m)
            if r["severity"] == "critical":
                critical.append(r)
            elif r["severity"] == "warn":
                warn.append(r)
            else:
                ok_count += 1

        print(f"\n  OK: {ok_count}")
        print(f"  WARN (no shared article token): {len(warn)}")
        print(f"  CRITICAL (voltage/article-cross): {len(critical)}")

        if critical:
            print("\n====== CRITICAL — likely wrong match ======")
            for r in sorted(critical, key=lambda x: (x["status"] != "candidate", -x["score"])):
                print(f"\n#{r['match_id']} {r['status']} score={r['score']}")
                print(f"  SP#{r['sp_id']}: {r['sp_name']}")
                print(f"  PP#{r['pp_id']}: {r['pp_name']}")
                for f_ in r["flags"]:
                    print(f"  ! {f_}")

        if warn:
            print(f"\n====== WARN ({len(warn)}) — no common article, needs eyeball ======")
            for r in sorted(warn, key=lambda x: (x["status"] != "candidate", -x["score"]))[:30]:
                print(f"\n#{r['match_id']} {r['status']} score={r['score']}")
                print(f"  SP#{r['sp_id']}: {r['sp_name']}")
                print(f"  PP#{r['pp_id']}: {r['pp_name']}")
                for f_ in r["flags"]:
                    print(f"  . {f_}")
            if len(warn) > 30:
                print(f"\n  ...and {len(warn) - 30} more in the JSON report")

        with open("np_audit_full.json", "w", encoding="utf-8") as f:
            json.dump(
                {"critical": critical, "warn": warn, "total": len(matches)},
                f, ensure_ascii=False, indent=2
            )
        print(f"\nFull report: np_audit_full.json")


if __name__ == "__main__":
    main()
