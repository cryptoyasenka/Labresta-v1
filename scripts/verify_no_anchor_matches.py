"""Narrow verification of confirmed matches that lack a strict article-anchor.

Companion to verify_article_anchor_rule.py. That script flagged 1641 confirmed
matches as 'no article-anchor at all' — they passed via name-fuzzy / Кодаки
internal codes / manual confirms. Most are likely correct (different supplier
internal SKU vs Horoshop article, but model name shared) — but the bucket is
big enough that a focused check is worth running.

Per-match red flags this script raises (any one = 'suspicious'):
  R1. Brand mismatch (after lower/strip) on a non-empty pp.brand and sp.brand
  R2. Voltage disjoint sets between sp.name and pp.name (same gate as Cat C)
  R3. No model-token in common (>=3 chars, alphanumeric, present in both names)

Output: the 'suspicious' bucket sorted by score desc — high-confidence
mismatches deserve first look.
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
from app.services.matcher import extract_voltages, normalize_model


_TOKEN_RE = re.compile(r"[A-Za-z0-9А-Яа-яЇїІіЄєҐґ]+", flags=re.UNICODE)
_MODEL_RUN_RE = re.compile(r"[a-z0-9]+", flags=re.IGNORECASE)


def _norm_brand(s: str | None) -> str:
    """Normalize brand for comparison: lowercase, strip all non-alnum.
    'IceTech' == 'Ice Tech' == 'ICE-TECH'.
    """
    if not s:
        return ""
    return re.sub(r"[^a-z0-9]", "", s.lower())


def _model_tokens(s: str | None, *, min_len: int = 4) -> set[str]:
    """Extract model-like tokens (alphanumeric, >=min_len, contains digit)
    from text after collapsing whitespace inside potential model codes.

    Strategy: find all alpha-digit transitions and treat the joined run as
    a candidate token. Then split by whitespace into runs of [a-z0-9],
    and also consider 'letter+digit-with-space' patterns like 'TG 310' as
    'tg310' by also doing a whitespace-collapse pass.

    This catches both 'XL413' and 'XL 413' as the same token.
    """
    if not s:
        return set()
    out = set()
    lower = s.lower()
    # Pass 1: standard alpha-num runs (catches 'tg310' style)
    for m in _MODEL_RUN_RE.finditer(lower):
        t = m.group(0)
        if len(t) >= min_len and any(c.isdigit() for c in t):
            out.add(t)
    # Pass 2: collapse whitespace between letters and digits (catches 'TG 310')
    collapsed = re.sub(r"([a-z])\s+(\d)", r"\1\2", lower)
    collapsed = re.sub(r"(\d)\s+([a-z])", r"\1\2", collapsed)
    for m in _MODEL_RUN_RE.finditer(collapsed):
        t = m.group(0)
        if len(t) >= min_len and any(c.isdigit() for c in t):
            out.add(t)
    return out


def _alphanum_tokens(s: str | None, *, min_len: int = 3, must_have_digit: bool = False) -> set[str]:
    if not s:
        return set()
    out = set()
    for m in _TOKEN_RE.finditer(s.lower()):
        t = m.group(0)
        if len(t) < min_len:
            continue
        if must_have_digit and not any(c.isdigit() for c in t):
            continue
        out.add(t)
    return out


def _has_anchor(pp: PromProduct, sp: SupplierProduct) -> bool:
    """Same logic as verify_article_anchor_rule.py: skip matches that DO have
    an article anchor (already checked there)."""
    sp_a = normalize_model(sp.article) if sp.article else ""
    pp_d = normalize_model(pp.display_article) if pp.display_article else ""
    pp_a = normalize_model(pp.article) if pp.article else ""
    if not sp_a:
        return False
    name_blob = re.sub(r"[^a-z0-9]", "", f"{pp.name or ''} {pp.name_ru or ''}".lower())
    # Three-way
    if pp_d and pp_d == sp_a and len(sp_a) >= 4:
        if sp_a in name_blob or pp_a == sp_a:
            return True
    # Two-way (no display_article, anchor in name + sp)
    if not pp_d and (sp_a in name_blob or (pp_a and pp_a == sp_a)):
        return True
    return False


def main() -> int:
    app = create_app()
    with app.app_context():
        suppliers = {s.id: s for s in db.session.execute(select(Supplier)).scalars().all()}
        sps = {sp.id: sp for sp in db.session.execute(select(SupplierProduct)).scalars().all()}
        pps = {pp.id: pp for pp in db.session.execute(select(PromProduct)).scalars().all()}

        confirmed = [m for m in db.session.execute(select(ProductMatch)).scalars().all()
                     if m.status in ("confirmed", "manual")]

        no_anchor = []
        for m in confirmed:
            sp = sps.get(m.supplier_product_id)
            pp = pps.get(m.prom_product_id)
            if not sp or not pp:
                continue
            if not _has_anchor(pp, sp):
                no_anchor.append((m, sp, pp))

        # Categorize
        brand_mismatch = []
        voltage_mismatch = []
        no_common_model_token = []
        ok = 0

        for m, sp, pp in no_anchor:
            flags = []

            # R1: brand mismatch (normalize: strip non-alnum, lowercase)
            # 'IceTech' == 'Ice Tech', 'RESTO ITALIA' == 'Restoitalia'
            pp_b = _norm_brand(pp.brand)
            sp_b = _norm_brand(sp.brand)
            if pp_b and sp_b and pp_b != sp_b:
                flags.append("brand")

            # R2: voltage disjoint
            v_pp = extract_voltages(pp.name or "")
            v_sp = extract_voltages(sp.name or "")
            if v_pp and v_sp and v_pp.isdisjoint(v_sp):
                flags.append("voltage")

            # R3: no model token in common — use _model_tokens which collapses
            # whitespace between letters and digits ('TG 310' == 'TG310', 'XL 413' == 'XL413')
            pp_toks = _model_tokens(f"{pp.name or ''} {pp.name_ru or ''}", min_len=4)
            sp_toks = _model_tokens(sp.name or "", min_len=4)
            # also normalize to absorb cyrillic homoglyphs
            pp_norm = {normalize_model(t) for t in pp_toks}
            sp_norm = {normalize_model(t) for t in sp_toks}
            if pp_norm and sp_norm and pp_norm.isdisjoint(sp_norm):
                # allow if any pp token is substring of any sp token (and 4+ chars), or vice versa
                any_overlap = False
                for a in pp_norm:
                    for b in sp_norm:
                        if len(a) >= 4 and (a in b or b in a):
                            any_overlap = True
                            break
                    if any_overlap:
                        break
                if not any_overlap:
                    flags.append("no_model_token")

            if "brand" in flags:
                brand_mismatch.append((m, sp, pp, flags))
            elif "voltage" in flags:
                voltage_mismatch.append((m, sp, pp, flags))
            elif "no_model_token" in flags:
                no_common_model_token.append((m, sp, pp, flags))
            else:
                ok += 1

        # ---- Output ----
        print("# No-Anchor Matches Verification\n")
        print(f"**Total confirmed matches:** {len(confirmed)}")
        print(f"**Without article-anchor:** {len(no_anchor)}\n")
        print("## Summary\n")
        print(f"- ✅ OK (brand match + voltage compatible + shared model token): **{ok}**")
        print(f"- ⚠ Brand mismatch: **{len(brand_mismatch)}**")
        print(f"- ⚠ Voltage disjoint: **{len(voltage_mismatch)}**")
        print(f"- ⚠ No common model token (>=4 chars, has digit): **{len(no_common_model_token)}**")
        print()

        def dump_bucket(title, rows, *, limit=80):
            print(f"## {title} — {len(rows)} шт.\n")
            if not rows:
                print("  (none)\n")
                return
            rows_sorted = sorted(rows, key=lambda r: -float(r[0].score or 0))
            by_sup = defaultdict(list)
            for row in rows_sorted[:limit]:
                m, sp, pp, _flags = row
                sup_name = suppliers[sp.supplier_id].name if sp.supplier_id in suppliers else f"sup#{sp.supplier_id}"
                by_sup[sup_name].append(row)
            for sup_name in sorted(by_sup):
                bucket = by_sup[sup_name]
                print(f"### {sup_name} — {len(bucket)} шт. (top by score)")
                for m, sp, pp, flags in bucket:
                    print(f"  match#{m.id} score={m.score} status={m.status} flags={','.join(flags)}")
                    print(f"    PP#{pp.id} brand={pp.brand!r} disp={pp.display_article!r}")
                    print(f"      name={(pp.name or '')[:100]!r}")
                    print(f"    SP#{sp.id} brand={sp.brand!r} art={sp.article!r}")
                    print(f"      name={(sp.name or '')[:100]!r}")
                print()
            if len(rows) > limit:
                print(f"  ... +{len(rows)-limit} more (truncated)\n")

        dump_bucket("⚠ Brand mismatch (highest priority — almost certainly wrong)", brand_mismatch)
        dump_bucket("⚠ Voltage disjoint (likely wrong — Yana rule)", voltage_mismatch)
        dump_bucket("⚠ No common model token (might be wrong, might be name-only style)", no_common_model_token, limit=50)

    return 0


if __name__ == "__main__":
    sys.exit(main())
