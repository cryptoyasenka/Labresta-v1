"""Analyze NP (supplier_id=2) matching gaps.

Output:
  A) Lost-match candidates among NP orphan SPs — SP has brand+article that exists
     in catalog but matcher didn't pair them.
  B) PP of NP-exclusive brands (Hurakan, Cold, Apach, Fagor, Tatra, ...) without
     any confirmed/manual match from NP — to hand-check whether missing from
     supplier feed or matcher failed.
"""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.extensions import db
from app.models.supplier_product import SupplierProduct
from app.models.catalog import PromProduct
from app.models.product_match import ProductMatch
from app.services.matcher import normalize_model, normalize_text


def brand_key(b):
    """Cheap brand canonicalization."""
    if not b:
        return ""
    return re.sub(r"[^a-zа-я0-9]", "", b.lower())

SUPPLIER_ID = 2

# Brands Yana said are NP-exclusive (she'll expand later)
NP_EXCLUSIVE_HINT = ["Hurakan", "Cold", "Apach", "Fagor", "Tatra"]


def norm_brand(b):
    return brand_key(b or "") if b else ""


def main():
    app = create_app()
    with app.app_context():
        # All NP SPs not deleted/ignored
        sps = SupplierProduct.query.filter(
            SupplierProduct.supplier_id == SUPPLIER_ID,
            SupplierProduct.is_deleted == False,
            SupplierProduct.ignored == False,
        ).all()

        # SP ids with confirmed/manual match
        matched_sp = set(
            r[0] for r in db.session.query(ProductMatch.supplier_product_id).filter(
                ProductMatch.status.in_(["confirmed", "manual"])
            ).all()
        )

        orphans = [sp for sp in sps if sp.id not in matched_sp]
        print(f"NP: {len(sps)} total SP, {len(sps)-len(orphans)} matched, {len(orphans)} orphan")

        # Build catalog index: brand_key -> list of (pp, normalized_article, normalized_name, normalized_display_article)
        pps = PromProduct.query.all()
        brand_to_pps = {}
        for pp in pps:
            bk = norm_brand(pp.brand)
            brand_to_pps.setdefault(bk, []).append(pp)
        # also by-any (no brand) fallback
        print(f"Catalog: {len(pps)} PP, {len(brand_to_pps)} distinct brand keys")

        # Brand stats among NP sps
        brand_counts = {}
        for sp in sps:
            bk = norm_brand(sp.brand)
            brand_counts[bk] = brand_counts.get(bk, 0) + 1
        print("\nTop NP brands (supplier side):")
        for bk, n in sorted(brand_counts.items(), key=lambda x: -x[1])[:25]:
            print(f"  {bk:30s} {n}")

        # PP which are confirmed/manual-matched to SOMEONE (to exclude from "PP unmatched")
        matched_pp = set(
            r[0] for r in db.session.query(ProductMatch.prom_product_id).filter(
                ProductMatch.status.in_(["confirmed", "manual"])
            ).all()
        )

        # === A: lost-match orphans ===
        # For each orphan sp, look in brand_to_pps[brand_key(sp.brand)]:
        # if any pp has same normalized article OR sp.article is contained in pp normalized name
        # and the pp is not already matched to some other supplier's product
        print("\n" + "=" * 72)
        print("A) LOST-MATCH CANDIDATES — orphan SP where catalog PP with same brand+article exists")
        print("=" * 72)

        found = []
        for sp in orphans:
            sp_bk = norm_brand(sp.brand)
            if not sp_bk:
                continue
            cand_pps = brand_to_pps.get(sp_bk, [])
            if not cand_pps:
                continue
            sp_article_norm = normalize_model(sp.article or "") if sp.article else ""
            sp_name_norm = normalize_model(sp.name or "")
            for pp in cand_pps:
                if pp.id in matched_pp:
                    continue
                pp_article_norm = normalize_model(pp.article or "") if pp.article else ""
                pp_display_norm = normalize_model(pp.display_article or "") if pp.display_article else ""
                pp_name_norm = normalize_model(pp.name or "")
                # Signal 1: article equality
                if sp_article_norm and len(sp_article_norm) >= 4 and (
                    sp_article_norm == pp_article_norm
                    or sp_article_norm == pp_display_norm
                    or (pp_display_norm and sp_article_norm in pp_display_norm)
                    or (pp_article_norm and sp_article_norm in pp_article_norm)
                ):
                    found.append((sp, pp, "article_match"))
                    break
                # Signal 2: sp article appears inside pp name (pure-letter or otherwise)
                if sp_article_norm and len(sp_article_norm) >= 6 and sp_article_norm in pp_name_norm:
                    found.append((sp, pp, "article_in_name"))
                    break
                # Signal 3: pp article appears inside sp name (symmetric)
                if pp_article_norm and len(pp_article_norm) >= 6 and pp_article_norm in sp_name_norm:
                    found.append((sp, pp, "ppart_in_spname"))
                    break
                if pp_display_norm and len(pp_display_norm) >= 6 and pp_display_norm in sp_name_norm:
                    found.append((sp, pp, "ppdisp_in_spname"))
                    break

        print(f"\nFound {len(found)} potential lost matches")
        by_brand = {}
        for sp, pp, reason in found:
            bk = norm_brand(sp.brand)
            by_brand.setdefault(bk, []).append((sp, pp, reason))
        for bk in sorted(by_brand.keys(), key=lambda b: -len(by_brand[b])):
            rows = by_brand[bk]
            print(f"\n-- {bk} ({len(rows)}) --")
            for sp, pp, reason in rows[:20]:
                sp_art = sp.article or "-"
                pp_art = pp.article or "-"
                pp_disp = pp.display_article or "-"
                print(f"  [{reason}]")
                print(f"    sp#{sp.id} art={sp_art!r:25s} name={sp.name[:80]!r}")
                print(f"    pp#{pp.id} art={pp_art!r:15s} disp={pp_disp!r:20s} name={pp.name[:80]!r}")
            if len(rows) > 20:
                print(f"    ... +{len(rows)-20} more")

        # === B: NP-exclusive brands — PP unmatched ===
        print("\n" + "=" * 72)
        print("B) NP-EXCLUSIVE BRANDS — catalog PP without ANY confirmed/manual match")
        print("=" * 72)

        for hint in NP_EXCLUSIVE_HINT:
            bk = norm_brand(hint)
            hint_pps = brand_to_pps.get(bk, [])
            unmatched = [pp for pp in hint_pps if pp.id not in matched_pp]
            matched = [pp for pp in hint_pps if pp.id in matched_pp]
            print(f"\n-- {hint} (brand_key={bk}): {len(hint_pps)} PP total, "
                  f"{len(matched)} matched, {len(unmatched)} UNMATCHED --")
            for pp in unmatched[:40]:
                print(f"  pp#{pp.id} art={pp.article or '-'!r:15s} disp={pp.display_article or '-'!r:20s} {pp.name[:90]}")
            if len(unmatched) > 40:
                print(f"  ... +{len(unmatched)-40} more")

        # Also: NP SP brands → show any hint brands we don't have
        print("\n" + "=" * 72)
        print("C) Are the hint brands even in NP supplier feed?")
        print("=" * 72)
        for hint in NP_EXCLUSIVE_HINT:
            bk = norm_brand(hint)
            sp_in_brand = [sp for sp in sps if norm_brand(sp.brand) == bk]
            print(f"  {hint:12s} ({bk}): {len(sp_in_brand)} SP in NP feed")


if __name__ == "__main__":
    main()
