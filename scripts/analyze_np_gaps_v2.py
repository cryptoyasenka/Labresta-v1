"""Analyze NP matching gaps v2 — distinguish:
  A1) Already candidate, waiting manual confirm in /matches UI
  A2) No match row at all (real matcher miss — orphan PP exists in catalog)
  B)  NP-exclusive brand PPs without any confirmed/manual match
"""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.extensions import db
from app.models.supplier_product import SupplierProduct
from app.models.catalog import PromProduct
from app.models.product_match import ProductMatch
from app.services.matcher import normalize_model

SUPPLIER_ID = 2
NP_EXCLUSIVE_HINT = ["Hurakan", "Cold", "Apach", "Fagor", "Tatra"]


def brand_key(b):
    if not b:
        return ""
    return re.sub(r"[^a-zа-я0-9]", "", b.lower())


def main():
    app = create_app()
    with app.app_context():
        sps = SupplierProduct.query.filter(
            SupplierProduct.supplier_id == SUPPLIER_ID,
            SupplierProduct.is_deleted == False,
            SupplierProduct.ignored == False,
        ).all()

        # SP ids with any confirmed/manual match (truly "done")
        final_sp = set(
            r[0] for r in db.session.query(ProductMatch.supplier_product_id).filter(
                ProductMatch.status.in_(["confirmed", "manual"])
            ).all()
        )
        # PP ids with confirmed/manual (locked)
        final_pp = set(
            r[0] for r in db.session.query(ProductMatch.prom_product_id).filter(
                ProductMatch.status.in_(["confirmed", "manual"])
            ).all()
        )

        orphans = [sp for sp in sps if sp.id not in final_sp]

        # Map sp_id -> set of candidate pp_ids
        sp_to_cand_pps = {}
        for m in ProductMatch.query.filter(ProductMatch.status == "candidate").all():
            sp_to_cand_pps.setdefault(m.supplier_product_id, set()).add(m.prom_product_id)

        # Build catalog brand index
        pps = PromProduct.query.all()
        brand_to_pps = {}
        for pp in pps:
            bk = brand_key(pp.brand)
            brand_to_pps.setdefault(bk, []).append(pp)

        # Find lost pairs
        already_cand = []  # (sp, pp, reason)
        no_row = []        # (sp, pp, reason)
        for sp in orphans:
            sp_bk = brand_key(sp.brand)
            if not sp_bk:
                continue
            cand_pps = brand_to_pps.get(sp_bk, [])
            if not cand_pps:
                continue
            sp_article_norm = normalize_model(sp.article or "") if sp.article else ""
            sp_name_norm = normalize_model(sp.name or "")
            existing_cand = sp_to_cand_pps.get(sp.id, set())
            for pp in cand_pps:
                if pp.id in final_pp:
                    continue
                pp_article_norm = normalize_model(pp.article or "") if pp.article else ""
                pp_display_norm = normalize_model(pp.display_article or "") if pp.display_article else ""
                pp_name_norm = normalize_model(pp.name or "")

                matched = False
                reason = ""
                if sp_article_norm and len(sp_article_norm) >= 4 and (
                    sp_article_norm == pp_article_norm
                    or sp_article_norm == pp_display_norm
                    or (pp_display_norm and sp_article_norm in pp_display_norm)
                    or (pp_article_norm and sp_article_norm in pp_article_norm)
                ):
                    matched, reason = True, "article_eq"
                elif sp_article_norm and len(sp_article_norm) >= 6 and sp_article_norm in pp_name_norm:
                    matched, reason = True, "art→ppname"
                elif pp_article_norm and len(pp_article_norm) >= 6 and pp_article_norm in sp_name_norm:
                    matched, reason = True, "ppart→spname"
                elif pp_display_norm and len(pp_display_norm) >= 6 and pp_display_norm in sp_name_norm:
                    matched, reason = True, "ppdisp→spname"

                if not matched:
                    continue
                if pp.id in existing_cand:
                    already_cand.append((sp, pp, reason))
                else:
                    no_row.append((sp, pp, reason))
                break  # one pp per sp

        print(f"NP orphans: {len(orphans)}")
        print(f"A1 already_candidate (just need manual confirm in UI): {len(already_cand)}")
        print(f"A2 NO ROW AT ALL (real matcher miss — should be candidate/confirmed): {len(no_row)}")

        def group_by_brand(rows):
            d = {}
            for sp, pp, r in rows:
                d.setdefault(brand_key(sp.brand), []).append((sp, pp, r))
            return d

        print("\n" + "=" * 72)
        print("A1 BY BRAND — already candidate, waiting manual confirm:")
        print("=" * 72)
        for bk, rows in sorted(group_by_brand(already_cand).items(), key=lambda x: -len(x[1])):
            print(f"  {bk:20s} {len(rows)}")

        print("\n" + "=" * 72)
        print("A2 BY BRAND — matcher MISSED these pairs entirely:")
        print("=" * 72)
        for bk, rows in sorted(group_by_brand(no_row).items(), key=lambda x: -len(x[1])):
            print(f"  {bk:20s} {len(rows)}")
            for sp, pp, r in rows[:15]:
                print(f"    [{r}]")
                print(f"      sp#{sp.id} art={sp.article or '-'!r:25s} {sp.name[:80]}")
                print(f"      pp#{pp.id} art={pp.article or '-'!r:15s} disp={pp.display_article or '-'!r:15s} {pp.name[:80]}")
            if len(rows) > 15:
                print(f"    ... +{len(rows)-15} more")

        # === B: unmatched PPs of hint brands ===
        print("\n" + "=" * 72)
        print("B) NP-EXCLUSIVE BRAND PPs without any confirmed/manual match")
        print("   (for you to review — either supplier doesn't have them, or matcher missed)")
        print("=" * 72)
        for hint in NP_EXCLUSIVE_HINT:
            bk = brand_key(hint)
            bpps = brand_to_pps.get(bk, [])
            unmatched = [pp for pp in bpps if pp.id not in final_pp]
            # annotate each unmatched pp: has candidate? covered-by-lost-match?
            no_sp_hint = []
            for pp in unmatched:
                cand_sps = [
                    m.supplier_product_id
                    for m in ProductMatch.query.filter_by(
                        prom_product_id=pp.id, status="candidate"
                    ).all()
                ]
                cand_np = []
                for sp_id in cand_sps:
                    sp = db.session.get(SupplierProduct, sp_id)
                    if sp and sp.supplier_id == SUPPLIER_ID:
                        cand_np.append(sp_id)
                no_sp_hint.append((pp, cand_np))
            only_no_cand = [(pp, c) for pp, c in no_sp_hint if not c]
            print(f"\n-- {hint} ({bk}): total={len(bpps)} matched={len(bpps)-len(unmatched)} "
                  f"unmatched={len(unmatched)} of which NO NP candidate={len(only_no_cand)} --")
            for pp, _ in only_no_cand[:30]:
                disp = pp.display_article or "-"
                art = pp.article or "-"
                print(f"  pp#{pp.id} art={art!r:15s} disp={disp!r:15s} {pp.name[:90]}")
            if len(only_no_cand) > 30:
                print(f"  ... +{len(only_no_cand)-30} more")


if __name__ == "__main__":
    main()
