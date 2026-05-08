"""Full matching audit — find missed matches (false negatives) and suspect
matches (false positives) across ALL brand×supplier pairs.

Read-only. Produces a categorized report. NEVER applies changes.

Categories:
  Cat A — exact-anchor gap     (false neg, HIGH confidence: should be matched)
    PP without confirmed match has display_article (>=4 chars) that exactly
    equals an SP.article at an active supplier. Worth bulk-confirming after
    visual sanity check.

  Cat B — sibling SKU gap      (false neg, MED — needs visual check)
    SP article = PP anchor + suffix (e.g. HKN-DL800 → HKN-DL800-silver).
    Could be a real variant — Yana said AD46DV ↔ AD46M are different ovens.
    DO NOT auto-confirm.

  Cat B-reverse                (false neg, MED — rare)
    PP anchor extends SP article. Unusual; flag for review.

  Cat C — voltage mismatch     (false POS, HIGH risk: confirmed but wrong)
    Confirmed match where PP and SP voltage tags differ (220 ↔ 380, 1ф ↔ 3ф).

  Cat D — name divergence      (false POS, MED risk)
    Confirmed where pp.name and sp.name share <30% token overlap. Possible
    duplicate Horoshop card or wrong bind.

  Cat E — M:1 violation        (false POS, must fix)
    A single PP claimed by 2+ confirmed matches. Forbidden invariant.

  Cat F — short-anchor risk    (false POS, LOW)
    Confirmed where display_article is <4 chars or pure-letters that could
    collide with generic tokens (M30, AK, etc.).

  Cat G — rejected, but anchor matches (audit operator decisions)
    Match in status='rejected' where sp.article == pp.display_article exactly.
    Operator may have rejected in error.

  Cat H — duplicate display_article (catalog hygiene)
    Two or more PPs share the same display_article — matcher's exact anchor
    can land on the wrong one.

Run on prod (read-only):
  $env:DATABASE_URL="<DATABASE_PUBLIC_URL>"
  & .venv/Scripts/python.exe scripts/audit_matching_gaps.py

Output: prints to stdout; redirect to .planning/matching-audit-report.md
"""
import os
import re
import sys
from collections import defaultdict, Counter

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy import func, select

from app import create_app
from app.extensions import db
from app.models.catalog import PromProduct
from app.models.product_match import ProductMatch
from app.models.supplier import Supplier
from app.models.supplier_product import SupplierProduct
from app.services.matcher import (
    extract_model_from_name,
    extract_voltages,
    normalize_model,
)
from app.services.orphan_detector import _dead_supplier_ids


def _is_separator(ch: str) -> bool:
    return not ch.isalnum()


def _is_extension(longer: str, shorter: str) -> tuple[bool, str]:
    """True if `longer` extends `shorter` with a separator or short alpha tail."""
    if not longer or not shorter or longer == shorter:
        return False, ""
    if len(longer) <= len(shorter) or not longer.startswith(shorter):
        return False, ""
    tail = longer[len(shorter):]
    if not tail:
        return False, ""
    if _is_separator(tail[0]):
        return True, tail
    if tail[0].isalpha() and len(tail) <= 4:
        return True, tail
    return False, ""


def _token_overlap(a: str, b: str) -> float:
    """Jaccard overlap on lowercased word tokens >=3 chars."""
    def toks(s: str) -> set[str]:
        return {t for t in re.findall(r"\w+", (s or "").lower(), flags=re.UNICODE) if len(t) >= 3}
    ta, tb = toks(a), toks(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def main() -> int:
    app = create_app()
    with app.app_context():
        # Suppliers — active only (skip dead)
        suppliers = db.session.execute(select(Supplier)).scalars().all()
        by_sup_id = {s.id: s for s in suppliers}
        dead_ids = _dead_supplier_ids()

        # All PPs and SPs
        pps = db.session.execute(select(PromProduct)).scalars().all()
        sps = db.session.execute(select(SupplierProduct)).scalars().all()

        # Index by brand
        pps_by_brand = defaultdict(list)
        for pp in pps:
            if pp.brand:
                pps_by_brand[pp.brand.lower().strip()].append(pp)

        sps_by_brand = defaultdict(list)  # (brand_lower) -> list[(sp, sup_id)]
        for sp in sps:
            if sp.brand and sp.supplier_id not in dead_ids:
                sps_by_brand[sp.brand.lower().strip()].append(sp)

        # Match index
        confirmed_matches = []
        rejected_matches = []
        confirmed_by_pp = defaultdict(list)  # pp_id -> list[ProductMatch]
        all_matches = db.session.execute(select(ProductMatch)).scalars().all()
        sp_by_id = {sp.id: sp for sp in sps}
        pp_by_id = {pp.id: pp for pp in pps}
        for m in all_matches:
            if m.status in ("confirmed", "manual"):
                confirmed_matches.append(m)
                confirmed_by_pp[m.prom_product_id].append(m)
            elif m.status == "rejected":
                rejected_matches.append(m)

        confirmed_pp_ids = set(confirmed_by_pp.keys())

        # Duplicate display_article index (Cat H)
        disp_count = Counter()
        for pp in pps:
            d = normalize_model(pp.display_article) if pp.display_article else ""
            if d and len(d) >= 4:
                disp_count[d] += 1
        dup_disp = {d for d, c in disp_count.items() if c > 1}

        # ============================================================
        # CAT A — exact-anchor gap
        # ============================================================
        cat_a_by_brand = defaultdict(list)
        for brand_l, brand_pps in pps_by_brand.items():
            sp_pool = sps_by_brand.get(brand_l, [])
            if not sp_pool:
                continue

            sp_by_article = defaultdict(list)
            for sp in sp_pool:
                a = normalize_model(sp.article) if sp.article else ""
                if a and len(a) >= 4:
                    sp_by_article[a].append(sp)

            for pp in brand_pps:
                if pp.id in confirmed_pp_ids:
                    continue
                disp = normalize_model(pp.display_article) if pp.display_article else ""
                if not disp or len(disp) < 4:
                    continue
                hits = sp_by_article.get(disp, [])
                if not hits:
                    continue
                # Skip if display_article is duplicated → high collision risk
                duped = disp in dup_disp
                cat_a_by_brand[pp.brand].append((pp, hits, duped))

        # ============================================================
        # CAT B / B-reverse — sibling extension
        # ============================================================
        cat_b_by_brand = defaultdict(list)
        cat_b_rev_by_brand = defaultdict(list)
        for brand_l, brand_pps in pps_by_brand.items():
            sp_pool = sps_by_brand.get(brand_l, [])
            if not sp_pool:
                continue
            sp_anchors = []
            for sp in sp_pool:
                art = normalize_model(sp.article) if sp.article else ""
                nm_model = normalize_model(extract_model_from_name(sp.name or "", sp.brand or ""))
                sp_anchors.append((sp, art, nm_model))

            for pp in brand_pps:
                if pp.id in confirmed_pp_ids:
                    continue
                disp = normalize_model(pp.display_article) if pp.display_article else ""
                pp_model = normalize_model(extract_model_from_name(pp.name or "", pp.brand or ""))
                anchor = disp or pp_model
                if not anchor or len(anchor) < 4:
                    continue

                ext_hits, rev_hits = [], []
                for sp, art, nm_model in sp_anchors:
                    for fld_val in (art, nm_model):
                        if not fld_val:
                            continue
                        if fld_val == anchor:
                            break  # exact (Cat A territory) — skip B
                        is_ext, tail = _is_extension(fld_val, anchor)
                        if is_ext:
                            ext_hits.append((sp, fld_val, tail))
                            break
                        is_rev, tail = _is_extension(anchor, fld_val)
                        if is_rev:
                            rev_hits.append((sp, fld_val, tail))
                            break
                if ext_hits:
                    cat_b_by_brand[pp.brand].append((pp, anchor, ext_hits))
                elif rev_hits:
                    cat_b_rev_by_brand[pp.brand].append((pp, anchor, rev_hits))

        # ============================================================
        # CAT C — voltage mismatch in confirmed
        # ============================================================
        cat_c = []
        for m in confirmed_matches:
            sp = sp_by_id.get(m.supplier_product_id)
            pp = pp_by_id.get(m.prom_product_id)
            if not sp or not pp:
                continue
            v_sp = extract_voltages(sp.name or "")
            v_pp = extract_voltages(pp.name or "")
            if v_sp and v_pp and v_sp.isdisjoint(v_pp):
                cat_c.append((m, sp, pp, v_sp, v_pp))

        # ============================================================
        # CAT D — name divergence
        # ============================================================
        cat_d = []
        for m in confirmed_matches:
            sp = sp_by_id.get(m.supplier_product_id)
            pp = pp_by_id.get(m.prom_product_id)
            if not sp or not pp:
                continue
            ov = _token_overlap(sp.name or "", pp.name or "")
            if ov < 0.30:
                cat_d.append((m, sp, pp, ov))

        # ============================================================
        # CAT E — M:1 violations
        # ============================================================
        cat_e = []
        for pp_id, ms in confirmed_by_pp.items():
            if len(ms) > 1:
                cat_e.append((pp_id, ms))

        # ============================================================
        # CAT F — short-anchor risk in confirmed
        # ============================================================
        cat_f = []
        for m in confirmed_matches:
            pp = pp_by_id.get(m.prom_product_id)
            if not pp:
                continue
            disp = (pp.display_article or "").strip()
            if disp and len(disp) < 4:
                cat_f.append((m, pp, disp))

        # ============================================================
        # CAT G — rejected matches with exact anchor
        # ============================================================
        cat_g = []
        for m in rejected_matches:
            sp = sp_by_id.get(m.supplier_product_id)
            pp = pp_by_id.get(m.prom_product_id)
            if not sp or not pp:
                continue
            sp_a = normalize_model(sp.article) if sp.article else ""
            pp_d = normalize_model(pp.display_article) if pp.display_article else ""
            if sp_a and pp_d and sp_a == pp_d and len(sp_a) >= 4:
                cat_g.append((m, sp, pp))

        # ============================================================
        # OUTPUT
        # ============================================================
        print("# Matching Audit Report")
        print()
        print(f"**Generated:** prod snapshot")
        print(f"**Total PP:** {len(pps)} | **Total SP:** {len(sps)} | "
              f"**Confirmed matches:** {len(confirmed_matches)} | "
              f"**Rejected:** {len(rejected_matches)}")
        print(f"**Dead suppliers excluded:** {sorted(dead_ids)}")
        print()
        print("## Summary table")
        print()
        print("| Cat | Description | Count | Risk | Action |")
        print("|-----|-------------|-------|------|--------|")
        total_a = sum(len(v) for v in cat_a_by_brand.values())
        total_b = sum(len(v) for v in cat_b_by_brand.values())
        total_brev = sum(len(v) for v in cat_b_rev_by_brand.values())
        print(f"| A | Exact-anchor gap (false neg) | {total_a} | HIGH conf | Visual check → bulk confirm |")
        print(f"| B | Sibling SKU gap (false neg) | {total_b} | MED | Per-row review |")
        print(f"| B-rev | PP-extends-SP (rare) | {total_brev} | MED | Per-row review |")
        print(f"| C | Voltage mismatch in confirmed | {len(cat_c)} | HIGH risk | Unconfirm |")
        print(f"| D | Name divergence (overlap <30%) | {len(cat_d)} | MED risk | Visual check |")
        print(f"| E | M:1 violations | {len(cat_e)} | MUST FIX | Pick one |")
        print(f"| F | Short-anchor confirmed (<4 chars) | {len(cat_f)} | LOW risk | Spot-check |")
        print(f"| G | Rejected with exact anchor | {len(cat_g)} | review | Re-evaluate |")
        print(f"| H | Duplicate display_article | {len(dup_disp)} | catalog | Merge/clean |")
        print()

        # ---------------- CAT A ----------------
        print("## Cat A — Exact-anchor gap (HIGH confidence false negatives)")
        print()
        print("PP без confirmed match де `pp.display_article == sp.article` точно. "
              "Це найбезпечніша категорія до bulk-confirm після візуальної перевірки. "
              "Колонка `dup` означає що display_article повторюється у каталозі (collision risk).")
        print()
        for brand in sorted(cat_a_by_brand):
            rows = cat_a_by_brand[brand]
            print(f"### {brand} — {len(rows)} шт.")
            for pp, hits, duped in rows:
                dup_marker = " ⚠ DUP-DISP" if duped else ""
                print(f"  PP#{pp.id} disp={pp.display_article!r}{dup_marker} name={(pp.name or '')[:70]!r}")
                for sp in hits[:3]:
                    sup_name = by_sup_id[sp.supplier_id].name if sp.supplier_id in by_sup_id else f"sup#{sp.supplier_id}"
                    print(f"      → SP#{sp.id} sup={sup_name!r} art={sp.article!r} name={(sp.name or '')[:60]!r}")
            print()

        # ---------------- CAT B ----------------
        print("## Cat B — Sibling SKU gap (SP=anchor+suffix)")
        print()
        print("⚠ ОБЕРЕЖНО: suffix може означати реальний variant. Yana 2026-05-09: "
              "AD46DV ↔ AD46M = різні печі. Не сматчити автоматично.")
        print()
        for brand in sorted(cat_b_by_brand):
            rows = cat_b_by_brand[brand]
            print(f"### {brand} — {len(rows)} шт.")
            for pp, anchor, hits in rows[:30]:
                print(f"  PP#{pp.id} anchor={anchor!r} name={(pp.name or '')[:70]!r}")
                for sp, fld_val, tail in hits[:3]:
                    sup_name = by_sup_id[sp.supplier_id].name if sp.supplier_id in by_sup_id else f"sup#{sp.supplier_id}"
                    print(f"      → SP#{sp.id} sup={sup_name!r} art={sp.article!r} fld={fld_val!r} suffix={tail!r}")
            if len(rows) > 30:
                print(f"  ... +{len(rows)-30} more")
            print()

        # ---------------- CAT B-rev ----------------
        if total_brev:
            print("## Cat B-reverse — PP-extends-SP (rare, suspicious)")
            print()
            for brand in sorted(cat_b_rev_by_brand):
                rows = cat_b_rev_by_brand[brand]
                print(f"### {brand} — {len(rows)} шт.")
                for pp, anchor, hits in rows[:20]:
                    print(f"  PP#{pp.id} anchor={anchor!r} name={(pp.name or '')[:70]!r}")
                    for sp, fld_val, tail in hits[:3]:
                        sup_name = by_sup_id[sp.supplier_id].name if sp.supplier_id in by_sup_id else f"sup#{sp.supplier_id}"
                        print(f"      → SP#{sp.id} sup={sup_name!r} art={sp.article!r} pp_extra={tail!r}")
                print()

        # ---------------- CAT C ----------------
        print("## Cat C — Voltage mismatch in confirmed (FALSE POSITIVE)")
        print()
        print("Confirmed matches where SP voltage tags ∩ PP voltage tags = ∅. Yana правило: 220 ↔ 380 = different SKU.")
        print()
        if not cat_c:
            print("  (none)")
        for m, sp, pp, v_sp, v_pp in cat_c:
            sup_name = by_sup_id[sp.supplier_id].name if sp.supplier_id in by_sup_id else f"sup#{sp.supplier_id}"
            print(f"  match#{m.id} status={m.status} sup={sup_name!r}")
            print(f"    PP#{pp.id} V={sorted(v_pp)} {(pp.name or '')[:80]!r}")
            print(f"    SP#{sp.id} V={sorted(v_sp)} {(sp.name or '')[:80]!r}")
        print()

        # ---------------- CAT D ----------------
        print("## Cat D — Name divergence in confirmed (overlap <30%)")
        print()
        print("Confirmed де SP/PP назви майже не перетинаються. Можливий duplicate Horoshop card "
              "або wrong bind. Перевірити вручну.")
        print()
        if not cat_d:
            print("  (none)")
        cat_d_sorted = sorted(cat_d, key=lambda x: x[3])
        for m, sp, pp, ov in cat_d_sorted[:60]:
            sup_name = by_sup_id[sp.supplier_id].name if sp.supplier_id in by_sup_id else f"sup#{sp.supplier_id}"
            print(f"  match#{m.id} ov={ov:.2f} sup={sup_name!r}  score={m.score}")
            print(f"    PP#{pp.id} {(pp.name or '')[:90]!r}")
            print(f"    SP#{sp.id} {(sp.name or '')[:90]!r}")
        if len(cat_d) > 60:
            print(f"  ... +{len(cat_d)-60} more")
        print()

        # ---------------- CAT E ----------------
        print("## Cat E — M:1 violations (one PP claimed by multiple confirmed)")
        print()
        if not cat_e:
            print("  (none — invariant holds)")
        for pp_id, ms in cat_e:
            pp = pp_by_id.get(pp_id)
            print(f"  PP#{pp_id} {(pp.name or '')[:80]!r}" if pp else f"  PP#{pp_id} (deleted?)")
            for m in ms:
                sp = sp_by_id.get(m.supplier_product_id)
                sup_name = by_sup_id[sp.supplier_id].name if sp and sp.supplier_id in by_sup_id else "?"
                print(f"    match#{m.id} status={m.status} score={m.score} sup={sup_name!r} "
                      f"sp#{m.supplier_product_id} art={(sp.article if sp else '')!r}")
        print()

        # ---------------- CAT F ----------------
        print("## Cat F — Short-anchor confirmed (display_article <4 chars)")
        print()
        print("Низький ризик але worth spot-check — короткі коди типу M30/AK можуть співпасти випадково.")
        print()
        if not cat_f:
            print("  (none)")
        for m, pp, disp in cat_f[:30]:
            sp = sp_by_id.get(m.supplier_product_id)
            sup_name = by_sup_id[sp.supplier_id].name if sp and sp.supplier_id in by_sup_id else "?"
            print(f"  match#{m.id} disp={disp!r} sup={sup_name!r}")
            print(f"    PP#{pp.id} {(pp.name or '')[:70]!r}")
            print(f"    SP#{m.supplier_product_id} {(sp.name if sp else '')[:70]!r}")
        if len(cat_f) > 30:
            print(f"  ... +{len(cat_f)-30} more")
        print()

        # ---------------- CAT G ----------------
        print("## Cat G — Rejected with exact anchor (review operator decisions)")
        print()
        print("Match у status=rejected, але `sp.article == pp.display_article`. "
              "Можливо помилкове відхилення — варто переглянути.")
        print()
        if not cat_g:
            print("  (none)")
        for m, sp, pp in cat_g[:30]:
            sup_name = by_sup_id[sp.supplier_id].name if sp.supplier_id in by_sup_id else "?"
            print(f"  match#{m.id} REJECTED sup={sup_name!r}")
            print(f"    PP#{pp.id} disp={pp.display_article!r} {(pp.name or '')[:70]!r}")
            print(f"    SP#{sp.id} art={sp.article!r} {(sp.name or '')[:70]!r}")
        if len(cat_g) > 30:
            print(f"  ... +{len(cat_g)-30} more")
        print()

        # ---------------- CAT H ----------------
        print("## Cat H — Duplicate display_article in catalog (merge candidates)")
        print()
        print("Той самий `display_article` присутній у кількох PP. Matcher Step 0a explicitly "
              "skips when there are 2+ collisions, тож матч не створюється — це блокує Cat A.")
        print()
        if not dup_disp:
            print("  (none)")
        for d in sorted(dup_disp)[:40]:
            owners = [pp for pp in pps
                      if normalize_model(pp.display_article) == d]
            print(f"  disp={d!r} ({len(owners)} PPs):")
            for pp in owners[:4]:
                print(f"    PP#{pp.id} brand={pp.brand!r} {(pp.name or '')[:70]!r}")
        if len(dup_disp) > 40:
            print(f"  ... +{len(dup_disp)-40} more")
        print()

        print("---")
        print("END OF REPORT")

    return 0


if __name__ == "__main__":
    sys.exit(main())
