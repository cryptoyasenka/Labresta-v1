"""READ-ONLY triage of status='candidate' ProductMatch rows into three buckets.

Buckets (LabResta domain rules):
  CONFIRM        - genuinely safe: names effectively identical, OR the SP article
                   appears in BOTH pp.name/name_ru AND pp.display_article, brand
                   matches, NO voltage conflict, NO suffix-variant conflict, high score.
  REJECT         - clear mismatch: brand mismatch, voltage conflict (220 vs 380 /
                   1ф vs 3ф), suffix-variant near-miss, or anchor article ABSENT
                   from pp.name/display_article (with low/empty token overlap).
  NEEDS-EYEBALL  - everything ambiguous in between.

NO MUTATION. Opens sqlite read-only (mode=ro) for raw reads; reuses the live
matcher's normalization helpers (import only, no DB writes). Never commits.
Writes a markdown dossier; prints before/after status snapshots to prove no row changed.
"""

import os
import sqlite3
import sys
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Reuse the production matcher's normalization so the triage mirrors real logic.
from app.services.matcher import (  # noqa: E402
    normalize_model,
    meaningful_tokens,
    after_brand_remainder,
    extract_voltages,
    extract_product_type,
    _extract_colors,
)


def _type_token(name, brand):
    """First meaningful Cyrillic/Latin word of the product type (before brand).

    Used to detect product-category divergence ('Рисоварка' vs 'Мультиварка')
    even when a manufacturer SKU anchor matches — same SKU with a clashing
    category word is suspicious enough to demote an article-anchor CONFIRM to
    EYEBALL. Returns '' when no usable type prefix exists.
    """
    t = extract_product_type(name or "", brand)
    if not t:
        return ""
    toks = meaningful_tokens(t)
    # Longest token = the head noun ('подрібнювач', 'рисоварка'); short
    # function words already dropped by meaningful_tokens.
    cyr = [x for x in toks if not x.isascii()]
    pool = cyr or list(toks)
    return max(pool, key=len) if pool else ""


def _product_type_conflict(pp_name, pp_brand, sp_name, sp_brand, brand):
    """True when both sides expose a product-type head word and they clash.

    Conservative: only fires when BOTH type tokens are present and neither is a
    prefix/substring of the other (covers 'рисоварка'/'мультиварка' clash but
    tolerates 'вітрина'/'вітрина кондитерська' style elaboration)."""
    a = _type_token(pp_name, brand or pp_brand)
    b = _type_token(sp_name, brand or sp_brand)
    if not a or not b:
        return False
    if a == b or a in b or b in a:
        return False
    return True

DB_URI = "file:instance/labresta.db?mode=ro"
MATCH_TABLE = "product_matches"
REPORT = ".planning/candidate-triage-2026-06-05.md"

SUPPLIER_NAMES = {
    1: "maresto", 2: "novyy-proekt (НП)", 3: "kodaki",
    6: "rp-ukrayina", 7: "guder", 8: "astim",
}


def snapshot(conn):
    rows = conn.execute(
        f"SELECT status, COUNT(*) FROM {MATCH_TABLE} GROUP BY status ORDER BY status"
    ).fetchall()
    return rows


def brand_match(pp_brand, sp_brand):
    """Return ('match'|'mismatch'|'unknown')."""
    pb = (pp_brand or "").strip().lower()
    sb = (sp_brand or "").strip().lower()
    if not pb or not sb:
        return "unknown"
    pbn = normalize_model(pp_brand)
    sbn = normalize_model(sp_brand)
    if pb == sb or (pbn and sbn and (pbn == sbn or pbn in sbn or sbn in pbn)):
        return "match"
    return "mismatch"


def md_escape(s):
    if s is None:
        return ""
    return str(s).replace("|", "\\|").replace("\n", " ").strip()


def classify(c):
    """Return (bucket, reason). c is a dict with all PP/SP fields + score."""
    pp_name = c["pp_name"] or ""
    pp_name_ru = c["pp_name_ru"] or ""
    pp_brand = c["pp_brand"]
    pp_disp = c["pp_display_article"]
    sp_name = c["sp_name"] or ""
    sp_brand = c["sp_brand"]
    sp_art = c["sp_article"]
    score = c["score"]

    bm = brand_match(pp_brand, sp_brand)

    # --- Voltage conflict (hard REJECT) -------------------------------------
    sp_volts = extract_voltages(sp_name) | extract_voltages(sp_art or "")
    pp_volts = (
        extract_voltages(pp_name)
        | extract_voltages(pp_name_ru)
        | extract_voltages(pp_disp or "")
    )
    if sp_volts and pp_volts and not (sp_volts & pp_volts):
        return ("REJECT", f"voltage conflict SP{sorted(sp_volts)} vs PP{sorted(pp_volts)}")

    # --- Color conflict (hard REJECT) ---------------------------------------
    sp_colors = _extract_colors(sp_name, sp_art or "")
    pp_colors = _extract_colors(pp_name, pp_name_ru, pp_disp or "")
    if sp_colors and pp_colors and not (sp_colors & pp_colors):
        return ("REJECT", f"color conflict SP{sorted(sp_colors)} vs PP{sorted(pp_colors)}")

    # --- Brand mismatch (hard REJECT) ---------------------------------------
    if bm == "mismatch":
        return ("REJECT", f"brand mismatch PP='{pp_brand}' SP='{sp_brand}'")

    # --- Normalized name identity (strongest CONFIRM signal) ----------------
    sp_nn = normalize_model(sp_name)
    pp_nn = normalize_model(pp_name)
    pp_nn_ru = normalize_model(pp_name_ru)
    name_identical = bool(sp_nn) and (sp_nn == pp_nn or (pp_nn_ru and sp_nn == pp_nn_ru))

    # --- Article anchor analysis --------------------------------------------
    sp_art_n = normalize_model(sp_art)
    disp_n = normalize_model(pp_disp)
    pp_name_blob = " ".join(x for x in (pp_nn, pp_nn_ru) if x)

    # A real manufacturer SKU has BOTH letters and digits (matcher's own test,
    # extract_article_codes). Pure-digit / zero-padded supplier articles
    # ('000001491', '19047938') are supplier-internal IDs, NOT manufacturer
    # anchors — their absence from the PP says nothing, so they must not drive
    # an anchor-absent REJECT. The real SKU for those rows lives as a model
    # token in the name (TV2500, SI320) and is handled by token overlap.
    sp_art_is_sku = bool(sp_art_n) and any(ch.isalpha() for ch in sp_art_n) and any(
        ch.isdigit() for ch in sp_art_n
    )

    anchor_in_disp = bool(sp_art_n) and bool(disp_n) and (
        sp_art_n == disp_n or (len(sp_art_n) >= 4 and sp_art_n in disp_n)
        or (len(disp_n) >= 4 and disp_n in sp_art_n)
    )
    anchor_in_name = bool(sp_art_n) and len(sp_art_n) >= 4 and sp_art_n in pp_name_blob.replace(" ", "")

    # Token overlap (containment view, as matcher uses)
    sp_tok = meaningful_tokens(after_brand_remainder(sp_name, sp_brand or pp_brand))
    pp_tok = meaningful_tokens(after_brand_remainder(pp_name, pp_brand or sp_brand))
    if not pp_tok:
        pp_tok = meaningful_tokens(after_brand_remainder(pp_name_ru, pp_brand or sp_brand))
    inter = sp_tok & pp_tok
    union = sp_tok | pp_tok
    jacc = (len(inter) / len(union)) if union else 0.0
    sp_subset = bool(sp_tok) and sp_tok.issubset(pp_tok)
    pp_subset = bool(pp_tok) and pp_tok.issubset(sp_tok)

    # FULL-name token sets (brand included). After-brand remainders can diverge
    # purely because the brand sits in a different position (PP 'X Gooder FC-400RA'
    # vs SP 'X FC-400RA Gooder'), which makes the after-brand token sets look
    # asymmetric even when the products are identical. The full-name token sets
    # are word-order-independent, so an empty symmetric difference = same tokens.
    sp_tok_full = meaningful_tokens(sp_name)
    pp_tok_full = meaningful_tokens(pp_name) or meaningful_tokens(pp_name_ru)
    full_symdiff = sp_tok_full ^ pp_tok_full
    tokens_equal_full = bool(sp_tok_full) and not full_symdiff
    full_union = sp_tok_full | pp_tok_full
    jacc_full = (len(sp_tok_full & pp_tok_full) / len(full_union)) if full_union else 0.0
    full_subset_either = (
        (bool(sp_tok_full) and sp_tok_full.issubset(pp_tok_full))
        or (bool(pp_tok_full) and pp_tok_full.issubset(sp_tok_full))
    )

    # --- Suffix-variant near-miss detection (REJECT) ------------------------
    # When the article anchor is present in BOTH name and display but the
    # remaining short-alpha SKU tails differ on exactly one side, that's a
    # variant near-miss (AD46MV vs AD46M ECO). Treated under EYEBALL unless
    # clearly conflicting; pure article-vs-display equality is the safe lane.
    sp_extra = sp_tok - pp_tok
    pp_extra = pp_tok - sp_tok

    def short_alpha_only(s):
        return bool(s) and all(t.isalpha() and len(t) <= 4 for t in s)

    def digit_only(s):
        return bool(s) and all(t.isdigit() for t in s)

    one_sided_sku_discrim = (
        (short_alpha_only(sp_extra) and not pp_extra)
        or (short_alpha_only(pp_extra) and not sp_extra)
        or (digit_only(sp_extra) and not pp_extra)
        or (digit_only(pp_extra) and not sp_extra)
    )

    # ---- CONFIRM ------------------------------------------------------------
    # 1) Identical normalized names + brand not mismatched + high score.
    if name_identical and bm != "mismatch" and score >= 85:
        return ("CONFIRM", f"normalized name identical (score {score:.0f})")
    # 1b) Full-name token sets identical (word-order only diff) + brand match +
    #     high score. e.g. 'X Gooder FC-400RA' == 'X FC-400RA Gooder'.
    if tokens_equal_full and bm == "match" and score >= 90 and len(sp_tok_full) >= 3:
        return ("CONFIRM", f"identical token set (word-order diff), brand match, score {score:.0f}")
    # Product-type head-word clash (e.g. SKU matches but 'Рисоварка' vs
    # 'Мультиварка'): demote article-anchor CONFIRMs to EYEBALL when present.
    type_conflict = _product_type_conflict(pp_name, pp_brand, sp_name, sp_brand, sp_brand or pp_brand)

    # 2) Strong article anchor: SP article in BOTH pp.display_article AND
    #    pp.name/name_ru, brand matches, high score, no one-sided SKU tail diff,
    #    no product-type head-word clash.
    if (
        type_conflict is False
        and anchor_in_disp
        and anchor_in_name
        and bm == "match"
        and score >= 80
        and not one_sided_sku_discrim
    ):
        return (
            "CONFIRM",
            f"article '{sp_art}' in display+name, brand match, score {score:.0f}",
        )
    # 3) Article == display_article exactly AND brand match AND name tokens are a
    #    clean subset either way (no conflicting SKU tail), strong score.
    if (
        sp_art_n
        and disp_n
        and sp_art_n == disp_n
        and len(sp_art_n) >= 4
        and bm == "match"
        and score >= 90
        and (sp_subset or pp_subset)
        and not one_sided_sku_discrim
        and type_conflict is False
    ):
        return (
            "CONFIRM",
            f"article==display_article '{pp_disp}', brand match, clean tokens, score {score:.0f}",
        )

    # ---- REJECT -------------------------------------------------------------
    # Anchor article present but is a one-sided SKU-tail near-miss => variant.
    # Guard: require the FULL-name token sets to genuinely differ — otherwise
    # the asymmetric extras are just a brand-position artifact (word-order),
    # not a real variant, and the pair is actually identical.
    if (
        anchor_in_name
        and one_sided_sku_discrim
        and (sp_extra or pp_extra)
        and full_symdiff
    ):
        diff = sorted(sp_extra | pp_extra)
        return ("REJECT", f"suffix-variant near-miss, differing SKU tokens {diff}")
    # SP has a REAL manufacturer SKU anchor (alphanumeric) that is genuinely
    # ABSENT from name AND display, and FULL-name token overlap is weak => not
    # the same product. Excludes: supplier-internal pure-digit IDs (sp_art_is_sku),
    # word-order-only diffs / extra-descriptor pairs (full_subset_either), and
    # high full-name overlap (jacc_full). This avoids false-rejecting rows where
    # the article carries a glued brand token ('SGL017PGooder') but the model
    # itself ('SGL017P') is clearly present and the names otherwise align.
    if (
        sp_art_is_sku
        and len(sp_art_n) >= 4
        and not anchor_in_name
        and not anchor_in_disp
        and not full_subset_either
        and jacc_full < 0.5
    ):
        return (
            "REJECT",
            f"manufacturer SKU '{sp_art}' absent from PP name+display, weak token overlap (full jacc {jacc_full:.2f})",
        )

    # ---- NEEDS-EYEBALL (everything else) -----------------------------------
    bits = [f"score {score:.0f}", f"brand {bm}", f"jacc {jacc:.2f}"]
    if anchor_in_disp:
        bits.append("anchor∈display")
    if anchor_in_name:
        bits.append("anchor∈name")
    if name_identical:
        bits.append("name≈identical-but-lowscore")
    if not sp_art_n:
        bits.append("no SP article")
    elif not sp_art_is_sku:
        bits.append("SP article is internal-id (not SKU)")
    if one_sided_sku_discrim:
        bits.append(f"one-sided SKU diff {sorted(sp_extra | pp_extra)}")
    if type_conflict:
        bits.append("product-type word clash")
    return ("NEEDS-EYEBALL", "; ".join(bits))


def main():
    conn = sqlite3.connect(DB_URI, uri=True)
    conn.row_factory = sqlite3.Row

    before = snapshot(conn)
    print("BEFORE snapshot:")
    for r in before:
        print(f"  {r[0]}: {r[1]}")

    rows = conn.execute(
        f"""
        SELECT m.id AS match_id, m.score AS score, m.status AS status,
               pp.id AS pp_id, pp.article AS pp_article, pp.display_article AS pp_display_article,
               pp.brand AS pp_brand, pp.name AS pp_name, pp.name_ru AS pp_name_ru,
               sp.id AS sp_id, sp.supplier_id AS sp_supplier_id, sp.article AS sp_article,
               sp.brand AS sp_brand, sp.name AS sp_name
        FROM {MATCH_TABLE} m
        JOIN prom_products pp ON pp.id = m.prom_product_id
        JOIN supplier_products sp ON sp.id = m.supplier_product_id
        WHERE m.status = 'candidate'
        ORDER BY sp.supplier_id, m.score DESC, m.id
        """
    ).fetchall()

    candidates = [dict(r) for r in rows]
    total = len(candidates)

    buckets = {"CONFIRM": [], "NEEDS-EYEBALL": [], "REJECT": []}
    for c in candidates:
        bucket, reason = classify(c)
        c["_bucket"] = bucket
        c["_reason"] = reason
        buckets[bucket].append(c)

    after = snapshot(conn)

    # ---- Build report -------------------------------------------------------
    def fmt_pp(c):
        return f"{c['pp_id']} / `{md_escape(c['pp_article'])}` / `{md_escape(c['pp_display_article'])}` / {md_escape(c['pp_brand'])}"

    def fmt_sp(c):
        sup = SUPPLIER_NAMES.get(c["sp_supplier_id"], str(c["sp_supplier_id"]))
        return f"{c['sp_id']} / {sup} / `{md_escape(c['sp_article'])}` / {md_escape(c['sp_brand'])}"

    out = []
    out.append("# Candidate triage — LabResta supplier↔product matches")
    out.append("")
    out.append("**Generated:** 2026-06-05 by `scripts/triage_candidates_readonly.py` (READ-ONLY)")
    out.append("")
    out.append(f"- Match table (`__tablename__`): **`{MATCH_TABLE}`**")
    out.append(f"- Total candidates (status='candidate'): **{total}**")
    out.append("- Per-bucket counts:")
    out.append(f"  - recommend-CONFIRM: **{len(buckets['CONFIRM'])}**")
    out.append(f"  - NEEDS-EYEBALL: **{len(buckets['NEEDS-EYEBALL'])}**")
    out.append(f"  - recommend-REJECT: **{len(buckets['REJECT'])}**")
    out.append(f"  - sum check: {len(buckets['CONFIRM']) + len(buckets['NEEDS-EYEBALL']) + len(buckets['REJECT'])} == {total}")
    out.append("")
    out.append("## Mutation-proof status snapshot")
    out.append("")
    out.append("BEFORE:")
    out.append("")
    out.append("| status | count |")
    out.append("|---|---:|")
    for r in before:
        out.append(f"| {r[0]} | {r[1]} |")
    out.append("")
    out.append("AFTER (must be identical):")
    out.append("")
    out.append("| status | count |")
    out.append("|---|---:|")
    for r in after:
        out.append(f"| {r[0]} | {r[1]} |")
    out.append("")
    out.append(f"**Identical:** {list(map(tuple, before)) == list(map(tuple, after))}")
    out.append("")
    out.append("## Method")
    out.append("")
    out.append(
        "Each candidate joined to `prom_products` (PP) and `supplier_products` (SP). "
        "Normalization reuses the live matcher (`app.services.matcher`): `normalize_model` "
        "(lowercase, strip non-alnum, fix Cyrillic homoglyphs, drop `/PL`), `meaningful_tokens` "
        "(after-brand token set, voltage tags removed), `extract_voltages` (incl. 1ф/3ф→voltage), "
        "`_extract_colors`. Decision order: voltage conflict→REJECT; color conflict→REJECT; "
        "brand mismatch→REJECT; then CONFIRM if (normalized names identical & score≥85) OR "
        "(SP article ∈ BOTH display_article AND name/name_ru, brand match, score≥80, no one-sided "
        "SKU-tail diff) OR (article==display_article, brand match, clean subset tokens, score≥90); "
        "then REJECT for suffix-variant near-miss (one-sided short-alpha/digit SKU tail) or anchor "
        "article absent from name+display with Jaccard token overlap <0.5; everything else → "
        "NEEDS-EYEBALL. Brand 'match' = exact or normalized containment; 'unknown' if either side "
        "blank (never auto-CONFIRM on unknown brand unless names are identical)."
    )
    out.append("")

    col_header = (
        "| match_id | PP (id / article / display_article / brand) | PP name | "
        "SP (id / supplier / article / brand) | SP name | score | reason |"
    )
    col_sep = "|---:|---|---|---|---|---:|---|"

    for bucket in ("CONFIRM", "NEEDS-EYEBALL", "REJECT"):
        rows_b = buckets[bucket]
        title = {
            "CONFIRM": "recommend-CONFIRM",
            "NEEDS-EYEBALL": "NEEDS-EYEBALL",
            "REJECT": "recommend-REJECT",
        }[bucket]
        out.append(f"## {title} ({len(rows_b)})")
        out.append("")
        if not rows_b:
            out.append("_none_")
            out.append("")
            continue
        by_sup = defaultdict(list)
        for c in rows_b:
            by_sup[c["sp_supplier_id"]].append(c)
        for sup_id in sorted(by_sup):
            sup = SUPPLIER_NAMES.get(sup_id, str(sup_id))
            grp = by_sup[sup_id]
            out.append(f"### {sup} ({len(grp)})")
            out.append("")
            out.append(col_header)
            out.append(col_sep)
            for c in grp:
                out.append(
                    f"| {c['match_id']} | {fmt_pp(c)} | {md_escape(c['pp_name'])} | "
                    f"{fmt_sp(c)} | {md_escape(c['sp_name'])} | {c['score']:.0f} | "
                    f"{md_escape(c['_reason'])} |"
                )
            out.append("")

    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    with open(REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(out))

    conn.close()

    print("\nAFTER snapshot:")
    for r in after:
        print(f"  {r[0]}: {r[1]}")
    print(f"\nSnapshots identical: {list(map(tuple, before)) == list(map(tuple, after))}")
    print(f"\nTotal candidates: {total}")
    print(f"  CONFIRM:       {len(buckets['CONFIRM'])}")
    print(f"  NEEDS-EYEBALL: {len(buckets['NEEDS-EYEBALL'])}")
    print(f"  REJECT:        {len(buckets['REJECT'])}")
    print(f"  sum: {sum(len(v) for v in buckets.values())}")
    print(f"\nReport: {REPORT}")

    # Print a few examples per bucket for the orchestrator sanity-check.
    for bucket in ("CONFIRM", "NEEDS-EYEBALL", "REJECT"):
        print(f"\n--- examples {bucket} ---")
        for c in buckets[bucket][:3]:
            print(
                f"  m#{c['match_id']} PP#{c['pp_id']}[{c['pp_brand']}] '{(c['pp_name'] or '')[:42]}' "
                f"<> SP#{c['sp_id']}[{c['sp_brand']}] '{(c['sp_name'] or '')[:42]}' "
                f"score={c['score']:.0f} :: {c['_reason']}"
            )


if __name__ == "__main__":
    main()
