"""Audit the 32 red matches confirmed via CLI — look for suffix/voltage mismatches.

Red flag: SP article without suffix matched to PP article WITH suffix (or vice versa).
Example: SP 'HKN-GXSD2GN' matched to PP 'HKN-GXSD2GN-SC' — wrong SKU.
"""

import json
import re
from app import create_app
from app.extensions import db
from app.models.product_match import ProductMatch
from sqlalchemy import select
from sqlalchemy.orm import joinedload


SUFFIX_RE = re.compile(r"-(?:GC|SC|GN|SN)\b", re.IGNORECASE)
VOLTAGE_RE = re.compile(r"\((220|380)\)|\b(220|380)\s*[вВvV]")


def tokens_of(s: str) -> set:
    if not s:
        return set()
    # keep alnum + dashes, uppercase, split on whitespace
    return {t for t in re.split(r"\s+", s.upper()) if len(t) >= 4}


def suffixes(s: str) -> set:
    if not s:
        return set()
    return {m.group(0).upper() for m in SUFFIX_RE.finditer(s)}


def voltages(s: str) -> set:
    if not s:
        return set()
    out = set()
    for m in VOLTAGE_RE.finditer(s):
        for g in m.groups():
            if g:
                out.add(g)
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

            sp_all = f"{sp_name} {sp_article}"
            pp_all = f"{pp_name} {pp_article}"

            sp_suf = suffixes(sp_all)
            pp_suf = suffixes(pp_all)
            sp_volt = voltages(sp_all)
            pp_volt = voltages(pp_all)

            reasons = []
            if sp_suf != pp_suf:
                reasons.append(f"suffix mismatch SP={sp_suf or '∅'} PP={pp_suf or '∅'}")
            if sp_volt != pp_volt:
                reasons.append(f"voltage mismatch SP={sp_volt or '∅'} PP={pp_volt or '∅'}")

            # also check: shared core token exists?
            core_tokens = tokens_of(sp_name) & tokens_of(pp_name)
            if not core_tokens:
                reasons.append(f"no shared long token (SP vs PP)")

            row = {
                "match_id": m.id,
                "status": m.status,
                "score": m.score,
                "sp_id": m.supplier_product_id,
                "pp_id": m.prom_product_id,
                "sp_name": sp_name,
                "sp_article": sp_article,
                "pp_name": pp_name,
                "pp_article": pp_article,
                "reasons": reasons,
            }
            if reasons:
                suspicious.append(row)
            else:
                ok.append(row)

        print(f"Total audited: {len(matches)}")
        print(f"  OK (no suffix/voltage mismatch): {len(ok)}")
        print(f"  SUSPICIOUS: {len(suspicious)}")

        if suspicious:
            print("\n=== SUSPICIOUS MATCHES ===")
            for r in suspicious:
                print(f"\nmatch #{r['match_id']} (status={r['status']}, score={r['score']})")
                print(f"  SP#{r['sp_id']}: {r['sp_name']!r}  art={r['sp_article']!r}")
                print(f"  PP#{r['pp_id']}: {r['pp_name']!r}  art={r['pp_article']!r}")
                for reason in r["reasons"]:
                    print(f"  ⚠ {reason}")

        with open("red_audit_result.json", "w", encoding="utf-8") as f:
            json.dump({"ok": ok, "suspicious": suspicious}, f, ensure_ascii=False, indent=2)
        print(f"\nFull report written to red_audit_result.json")


if __name__ == "__main__":
    main()
