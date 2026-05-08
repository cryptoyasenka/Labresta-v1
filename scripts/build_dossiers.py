"""Per-row dossier builder for Cat H / Cat B / Cat B-reverse / Astim fuzzy.

Read-only. Produces detailed side-by-side markdown files in
`.planning/dossiers/<category>/` so Yana can decide each per-row item in
~30 sec instead of digging up data manually.

Each dossier contains:
- PP detail (id, brand, name UA+RU, display_article, article, price+currency,
  page_url, image URLs, description excerpt, operator_decision)
- SP candidates (article, name, price+currency, supplier name, available,
  image URLs, brand, params)
- Diff hints (anchor + suffix for Cat B, model token comparison)
- Recommended action template (e.g., "merge / keep both / cleanup")

Run on prod (read-only):
    $env:DATABASE_URL = (railway variables --service Postgres --kv |
        Select-String DATABASE_PUBLIC_URL= | %{($_ -split "=",2)[1]})
    $env:PYTHONIOENCODING = "utf-8"
    & .venv/Scripts/python.exe scripts/build_dossiers.py --cat all

Output trees:
    .planning/dossiers/cat-h/<disp_article_safe>.md     (11 PPs)
    .planning/dossiers/cat-b/<pp_id>.md                 (13 PPs)
    .planning/dossiers/cat-b-rev/<pp_id>.md             (8 PPs)
    .planning/dossiers/astim-fuzzy/<match_id>.md        (7 candidates)
    .planning/dossiers/INDEX.md                         (overview + counts)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy import select

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


# ---------- helpers shared with audit_matching_gaps.py ----------

def _is_separator(ch: str) -> bool:
    return not ch.isalnum()


def _is_extension(longer: str, shorter: str) -> tuple[bool, str]:
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


# ---------- formatters ----------

_SAFE_NAME_RE = re.compile(r"[^a-zA-Z0-9_-]+")


def _safe_filename(s: str) -> str:
    return _SAFE_NAME_RE.sub("_", s).strip("_") or "unknown"


def _fmt_price(cents: int | None, currency: str | None) -> str:
    if cents is None:
        return "—"
    val = cents / 100
    cur = currency or ""
    return f"{val:,.2f} {cur}".strip()


def _parse_image_list(images_json: str | None) -> list[str]:
    if not images_json:
        return []
    try:
        data = json.loads(images_json)
        if isinstance(data, list):
            return [str(u) for u in data if u]
    except Exception:
        pass
    return []


def _truncate(s: str | None, n: int = 400) -> str:
    if not s:
        return "—"
    s = s.strip()
    return s[:n] + ("…" if len(s) > n else "")


def _fmt_pp_block(pp: PromProduct, sup_name: str | None = None,
                  matches: list[ProductMatch] | None = None) -> list[str]:
    lines = []
    lines.append(f"### PromProduct #{pp.id}")
    lines.append("")
    lines.append(f"- **Brand:** `{pp.brand or '—'}`")
    lines.append(f"- **Name (UA):** {pp.name or '—'}")
    if pp.name_ru:
        lines.append(f"- **Name (RU):** {pp.name_ru}")
    lines.append(f"- **display_article (на сайте):** `{pp.display_article or '—'}`")
    lines.append(f"- **article (Kod_tovaru):** `{pp.article or '—'}`")
    lines.append(f"- **Price:** {_fmt_price(pp.price, pp.currency)}")
    lines.append(f"- **Operator decision:** `{pp.operator_decision or '—'}`")
    if pp.operator_decision_note:
        lines.append(f"- **Note:** {pp.operator_decision_note}")
    if pp.page_url:
        lines.append(f"- **Page:** {pp.page_url}")
    if pp.image_url:
        lines.append(f"- **Main image:** {pp.image_url}")
    extra_imgs = _parse_image_list(pp.images)
    if extra_imgs:
        lines.append(f"- **Gallery ({len(extra_imgs)}):** {', '.join(extra_imgs[:3])}"
                     + (" …" if len(extra_imgs) > 3 else ""))
    if pp.description_ua:
        lines.append(f"- **Desc UA:** {_truncate(pp.description_ua, 250)}")
    if pp.description_ru:
        lines.append(f"- **Desc RU:** {_truncate(pp.description_ru, 250)}")
    if matches:
        lines.append(f"- **Existing matches ({len(matches)}):**")
        for m in matches:
            lines.append(f"   - match#{m.id} status=`{m.status}` score={m.score} "
                         f"sp_id={m.supplier_product_id} confirmed_by=`{m.confirmed_by or '—'}`")
    lines.append("")
    return lines


def _fmt_sp_block(sp: SupplierProduct, sup_name: str, *, label: str = "SupplierProduct") -> list[str]:
    lines = []
    lines.append(f"### {label} #{sp.id}  (supplier: **{sup_name}**)")
    lines.append("")
    lines.append(f"- **Brand:** `{sp.brand or '—'}`")
    lines.append(f"- **Name:** {sp.name or '—'}")
    lines.append(f"- **article (vendorCode):** `{sp.article or '—'}`")
    lines.append(f"- **Price:** {_fmt_price(sp.price_cents, sp.currency)}")
    lines.append(f"- **Available:** {sp.available} | **is_deleted:** {sp.is_deleted} | "
                 f"**ignored:** {sp.ignored} | **needs_review:** {sp.needs_review}")
    if sp.image_url:
        lines.append(f"- **Main image:** {sp.image_url}")
    extra_imgs = _parse_image_list(sp.images)
    if extra_imgs:
        lines.append(f"- **Gallery ({len(extra_imgs)}):** {', '.join(extra_imgs[:3])}"
                     + (" …" if len(extra_imgs) > 3 else ""))
    if sp.description:
        lines.append(f"- **Desc:** {_truncate(sp.description, 250)}")
    if sp.params:
        lines.append(f"- **Params:** {_truncate(sp.params, 250)}")
    lines.append("")
    return lines


# ---------- categorization (mirrors audit_matching_gaps.py) ----------

def _gather_state(app):
    with app.app_context():
        suppliers = db.session.execute(select(Supplier)).scalars().all()
        by_sup_id = {s.id: s for s in suppliers}
        dead_ids = _dead_supplier_ids()

        pps = db.session.execute(select(PromProduct)).scalars().all()
        sps = db.session.execute(select(SupplierProduct)).scalars().all()

        pp_by_id = {pp.id: pp for pp in pps}
        sp_by_id = {sp.id: sp for sp in sps}

        pps_by_brand = defaultdict(list)
        for pp in pps:
            if pp.brand:
                pps_by_brand[pp.brand.lower().strip()].append(pp)

        sps_by_brand = defaultdict(list)
        for sp in sps:
            if sp.brand and sp.supplier_id not in dead_ids:
                sps_by_brand[sp.brand.lower().strip()].append(sp)

        all_matches = db.session.execute(select(ProductMatch)).scalars().all()
        confirmed_by_pp = defaultdict(list)
        all_matches_by_pp = defaultdict(list)
        candidates = []
        for m in all_matches:
            all_matches_by_pp[m.prom_product_id].append(m)
            if m.status in ("confirmed", "manual"):
                confirmed_by_pp[m.prom_product_id].append(m)
            elif m.status == "candidate":
                candidates.append(m)

        return {
            "suppliers": suppliers,
            "by_sup_id": by_sup_id,
            "dead_ids": dead_ids,
            "pps": pps,
            "sps": sps,
            "pp_by_id": pp_by_id,
            "sp_by_id": sp_by_id,
            "pps_by_brand": pps_by_brand,
            "sps_by_brand": sps_by_brand,
            "all_matches": all_matches,
            "confirmed_by_pp": confirmed_by_pp,
            "all_matches_by_pp": all_matches_by_pp,
            "candidates": candidates,
        }


def _find_cat_h(state):
    """Duplicate display_article PPs grouped by normalized disp."""
    disp_owners = defaultdict(list)
    for pp in state["pps"]:
        d = normalize_model(pp.display_article) if pp.display_article else ""
        if d and len(d) >= 4:
            disp_owners[d].append(pp)
    return {d: owners for d, owners in disp_owners.items() if len(owners) > 1}


def _find_cat_b(state):
    """PP unmatched, SP article = anchor + suffix. Returns list of (pp, anchor, hits)."""
    cat_b = []
    cat_b_rev = []
    confirmed_pp_ids = set(state["confirmed_by_pp"].keys())
    for brand_l, brand_pps in state["pps_by_brand"].items():
        sp_pool = state["sps_by_brand"].get(brand_l, [])
        if not sp_pool:
            continue
        sp_anchors = []
        for sp in sp_pool:
            art = normalize_model(sp.article) if sp.article else ""
            nm = normalize_model(extract_model_from_name(sp.name or "", sp.brand or ""))
            sp_anchors.append((sp, art, nm))

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
                        break
                    is_ext, tail = _is_extension(fld_val, anchor)
                    if is_ext:
                        ext_hits.append((sp, fld_val, tail))
                        break
                    is_rev, tail = _is_extension(anchor, fld_val)
                    if is_rev:
                        rev_hits.append((sp, fld_val, tail))
                        break
            if ext_hits:
                cat_b.append((pp, anchor, ext_hits))
            elif rev_hits:
                cat_b_rev.append((pp, anchor, rev_hits))
    return cat_b, cat_b_rev


def _find_astim_fuzzy(state):
    """Astim (supplier_id=8) candidates that lack three-location anchor."""
    astim_id = None
    for s in state["suppliers"]:
        if (s.name or "").strip().lower() == "астим":
            astim_id = s.id
            break
    if astim_id is None:
        # try alternative spelling
        for s in state["suppliers"]:
            if "астим" in (s.name or "").lower() or "astim" in (s.name or "").lower():
                astim_id = s.id
                break
    if astim_id is None:
        return []

    out = []
    for m in state["candidates"]:
        sp = state["sp_by_id"].get(m.supplier_product_id)
        pp = state["pp_by_id"].get(m.prom_product_id)
        if not sp or not pp or sp.supplier_id != astim_id:
            continue
        out.append((m, sp, pp))
    return out


# ---------- writers ----------

def _ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def _write_cat_h(out_root: Path, state, dup_disp_owners: dict[str, list[PromProduct]]):
    cat_dir = out_root / "cat-h"
    _ensure_dir(cat_dir)
    by_sup_id = state["by_sup_id"]
    confirmed_by_pp = state["confirmed_by_pp"]
    sp_by_id = state["sp_by_id"]

    written = []
    for disp_norm, owners in sorted(dup_disp_owners.items()):
        # use original (un-normalized) display_article from first owner for filename
        raw = owners[0].display_article or disp_norm
        fname = f"{_safe_filename(raw)}.md"
        path = cat_dir / fname

        lines = []
        lines.append(f"# Cat H — display_article `{raw}` shared by {len(owners)} PPs")
        lines.append("")
        lines.append(f"**Normalized:** `{disp_norm}`  ")
        lines.append(f"**Owners:** {', '.join(f'PP#{pp.id} ({pp.brand})' for pp in owners)}  ")
        lines.append("")
        lines.append("**Why this matters:** matcher Step 0a explicitly skips when there are "
                     "2+ collisions on the same display_article — this blocks Cat A auto-match "
                     "for whichever PP is the legitimate owner.")
        lines.append("")
        lines.append("**Suggested action:** identify the WRONG owner(s) (likely brand mismatch — "
                     "Hendi article in non-Hendi PP), edit `display_article` in Horoshop to a "
                     "different value or delete the PP if not needed.")
        lines.append("")
        lines.append("---")
        lines.append("")
        for pp in owners:
            ms = confirmed_by_pp.get(pp.id, [])
            lines.extend(_fmt_pp_block(pp, matches=ms))
            # Show the SP behind any confirmed match for context
            for m in ms:
                sp = sp_by_id.get(m.supplier_product_id)
                if sp:
                    sup = by_sup_id.get(sp.supplier_id)
                    lines.append(f"  → confirmed via SP#{sp.id} (sup: {sup.name if sup else '?'})")
                    lines.append(f"     art=`{sp.article or '—'}` name={sp.name!r}")
            lines.append("")

        path.write_text("\n".join(lines), encoding="utf-8")
        written.append((raw, fname, len(owners)))
    return written


def _write_cat_b(out_root: Path, state, cat_b_rows, *, reverse: bool = False):
    sub = "cat-b-rev" if reverse else "cat-b"
    cat_dir = out_root / sub
    _ensure_dir(cat_dir)
    by_sup_id = state["by_sup_id"]
    all_matches_by_pp = state["all_matches_by_pp"]

    written = []
    for pp, anchor, hits in cat_b_rows:
        path = cat_dir / f"PP{pp.id}_{_safe_filename((pp.brand or 'unknown'))}.md"

        lines = []
        title_kind = "PP-extends-SP (rare)" if reverse else "SP=anchor+suffix"
        lines.append(f"# Cat {'B-rev' if reverse else 'B'} — PP#{pp.id} {pp.brand} — {title_kind}")
        lines.append("")
        lines.append(f"**Anchor:** `{anchor}`  ")
        lines.append(f"**Existing matches on this PP:** {len(all_matches_by_pp.get(pp.id, []))}")
        lines.append("")
        lines.append("**Decision needed:** is the suffix variant the SAME SKU as the PP "
                     "(should match) or a DIFFERENT product (leave unmatched)?  ")
        lines.append("Yana rule: AD46MV ≠ AD46M, AD46DV ≠ AD46D — Apach suffixes are SKU-defining.")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## PromProduct (catalog)")
        lines.append("")
        lines.extend(_fmt_pp_block(pp, matches=all_matches_by_pp.get(pp.id, [])))
        lines.append("---")
        lines.append("")
        lines.append(f"## Candidate SP rows ({len(hits)})")
        lines.append("")
        for sp, fld_val, tail in hits[:5]:
            sup = by_sup_id.get(sp.supplier_id)
            sup_name = sup.name if sup else f"sup#{sp.supplier_id}"
            lines.append(f"### Suffix `{tail}` (matched field: `{fld_val}`)")
            lines.append("")
            lines.extend(_fmt_sp_block(sp, sup_name))
            # quick voltage check
            v_pp = extract_voltages(pp.name or "")
            v_sp = extract_voltages(sp.name or "")
            if v_pp or v_sp:
                lines.append(f"**Voltage check:** PP={sorted(v_pp) or '∅'} | SP={sorted(v_sp) or '∅'}")
                if v_pp and v_sp and v_pp.isdisjoint(v_sp):
                    lines.append("  ⚠ DISJOINT voltage sets — Yana rule says different SKU.")
                lines.append("")

        path.write_text("\n".join(lines), encoding="utf-8")
        written.append((pp.id, pp.brand, len(hits)))
    return written


def _write_astim_fuzzy(out_root: Path, state, fuzzy_rows):
    cat_dir = out_root / "astim-fuzzy"
    _ensure_dir(cat_dir)
    by_sup_id = state["by_sup_id"]
    all_matches_by_pp = state["all_matches_by_pp"]

    written = []
    for m, sp, pp in fuzzy_rows:
        path = cat_dir / f"match{m.id}_PP{pp.id}.md"
        lines = []
        lines.append(f"# Astim fuzzy — match#{m.id} score={m.score}")
        lines.append("")
        lines.append(f"**Status:** `{m.status}`  ")
        lines.append(f"**Confirmed_by (rule fingerprint):** `{m.confirmed_by or '—'}`  ")
        lines.append("")
        lines.append("**Why fuzzy:** R0 article-anchor failed (article missing or no name "
                     "containment). Match suggested by lower-priority rule — needs visual confirm.")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## PromProduct (catalog)")
        lines.append("")
        lines.extend(_fmt_pp_block(pp, matches=all_matches_by_pp.get(pp.id, [])))
        lines.append("---")
        lines.append("")
        sup = by_sup_id.get(sp.supplier_id)
        lines.append("## Candidate SupplierProduct")
        lines.append("")
        lines.extend(_fmt_sp_block(sp, sup.name if sup else f"sup#{sp.supplier_id}"))
        v_pp = extract_voltages(pp.name or "")
        v_sp = extract_voltages(sp.name or "")
        if v_pp or v_sp:
            lines.append(f"**Voltage check:** PP={sorted(v_pp) or '∅'} | SP={sorted(v_sp) or '∅'}")
            if v_pp and v_sp and v_pp.isdisjoint(v_sp):
                lines.append("  ⚠ DISJOINT voltage sets — Yana rule says different SKU. REJECT.")
            lines.append("")

        path.write_text("\n".join(lines), encoding="utf-8")
        written.append((m.id, pp.id, sp.id))
    return written


# ---------- main ----------

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cat", choices=["cat-h", "cat-b", "cat-b-rev", "astim-fuzzy", "all"],
                        default="all")
    parser.add_argument("--out-root",
                        default=str(Path(__file__).parent.parent / ".planning" / "dossiers"))
    args = parser.parse_args()

    out_root = Path(args.out_root)
    _ensure_dir(out_root)

    app = create_app()
    state = _gather_state(app)

    print(f"Loaded: {len(state['pps'])} PPs, {len(state['sps'])} SPs, "
          f"{len(state['all_matches'])} total matches, "
          f"{len(state['candidates'])} candidates, "
          f"dead_suppliers={sorted(state['dead_ids'])}")

    summary_parts = []

    with app.app_context():
        if args.cat in ("cat-h", "all"):
            cat_h = _find_cat_h(state)
            print(f"Cat H: {len(cat_h)} duplicate display_articles")
            written = _write_cat_h(out_root, state, cat_h)
            summary_parts.append(("Cat H — duplicate display_article", "cat-h", written,
                                  ["disp", "file", "owners"]))

        if args.cat in ("cat-b", "cat-b-rev", "all"):
            cat_b, cat_b_rev = _find_cat_b(state)
            if args.cat in ("cat-b", "all"):
                print(f"Cat B: {len(cat_b)} sibling-suffix rows")
                written = _write_cat_b(out_root, state, cat_b, reverse=False)
                summary_parts.append(("Cat B — sibling SKU gap", "cat-b", written,
                                      ["pp_id", "brand", "hits"]))
            if args.cat in ("cat-b-rev", "all"):
                print(f"Cat B-rev: {len(cat_b_rev)} reverse rows")
                written = _write_cat_b(out_root, state, cat_b_rev, reverse=True)
                summary_parts.append(("Cat B-reverse — PP-extends-SP", "cat-b-rev", written,
                                      ["pp_id", "brand", "hits"]))

        if args.cat in ("astim-fuzzy", "all"):
            fuzzy = _find_astim_fuzzy(state)
            print(f"Astim fuzzy: {len(fuzzy)} candidates")
            written = _write_astim_fuzzy(out_root, state, fuzzy)
            summary_parts.append(("Astim fuzzy — candidates", "astim-fuzzy", written,
                                  ["match_id", "pp_id", "sp_id"]))

    # ---------- INDEX ----------
    idx = out_root / "INDEX.md"
    lines = []
    lines.append("# Per-row dossiers — INDEX")
    lines.append("")
    lines.append(f"Generated for the night audit follow-up. All dossiers are read-only "
                 "snapshots from prod — re-run `scripts/build_dossiers.py` to refresh.")
    lines.append("")
    for title, sub, written, headers in summary_parts:
        lines.append(f"## {title} — {len(written)} файлов")
        lines.append("")
        if not written:
            lines.append("  (none)")
            lines.append("")
            continue
        lines.append("| " + " | ".join(headers) + " |")
        lines.append("| " + " | ".join("---" for _ in headers) + " |")
        for row in written:
            cells = []
            for i, val in enumerate(row):
                if i == 1 and sub == "cat-h":
                    cells.append(f"[{val}]({sub}/{val})")
                elif i == 0 and sub in ("cat-b", "cat-b-rev"):
                    fname = next(
                        (Path(f).name for f in os.listdir(out_root / sub) if f.startswith(f"PP{val}_")),
                        None,
                    )
                    cells.append(f"[PP#{val}]({sub}/{fname})" if fname else f"PP#{val}")
                elif i == 0 and sub == "astim-fuzzy":
                    fname = next(
                        (Path(f).name for f in os.listdir(out_root / sub) if f.startswith(f"match{val}_")),
                        None,
                    )
                    cells.append(f"[match#{val}]({sub}/{fname})" if fname else f"match#{val}")
                else:
                    cells.append(str(val))
            lines.append("| " + " | ".join(cells) + " |")
        lines.append("")
    idx.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote INDEX: {idx}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
