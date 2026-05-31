# 09-PLAN-CHECK — goal-backward review of 09-01 + 09-02

**Reviewer:** orchestrator (in-context, both plans read in full; anchors grep-verified).
**Date:** 2026-05-31
**Verdict:** **09-01 = PASS** · **09-02 = PASS-WITH-FLAGS** → proceed to execution; fold FLAG-1/FLAG-2 into 09-02, pin MINOR-A into 09-01.

Why in-context and not a subagent: the first gsd-plan-checker subagent thrashed its own window
(over-scoped reading set: 888-line RESEARCH + CONTEXT + 6 sources at once → autocompact loop, 0 output,
agentId ae1727b59f57d6977 — do NOT resume). Plans are 463/493 lines; checking them in the main thread
is cheaper and thrash-free than re-spawning.

## Anchor verification (phantom-symbol axis) — PASS
Every symbol the plans call exists at the cited location:
- pricing.py: `resolve_eur_rate`:15 · `calculate_price_eur`:35 · `resolve_discount_percent`:83 · `clamp_discount_for_min_margin`:130 · `calculate_auto_discount`:275 ✓
- matcher.py: `normalize_text`:208 · `extract_model_from_name`:309 · `meaningful_tokens`:802 · `_transliterate_cyr`:894 ✓
- feed.py: `NP_BRANDS`:153 · `_np_brand_match_counts`:165 · `np_file_page`:188 · `np_file_generate`:202 ✓
- np_horoshop_file.py: `HEADERS`:67 · `_norm`:78 · `_shape_rows`:82 · `_workbook_bytes`:171 · `build_np_file`:223 ✓

## 09-01 (CORE) — PASS
Ships a self-contained importable file: UA name + price (canary 718.3/845.0/EUR) + availability +
photos + description-UA + Артикул + brand + visibility="1" + a guaranteed-non-empty `[КАТАЛОГ] Раздел`
(fallback holding category). TDD (T0 red → T1 green), read-only query (NOT-EXISTS, no `published`
in the predicate — correct per RESEARCH Q7), pricing via real primitives. No blocking issues.

## 09-02 (SMART CATEGORY) — PASS-WITH-FLAGS
The three-tier chain (feed→analogy→fallback, AI disabled stub), the export corpus reader, the
prod-guarded evidence script, and the proposal+checkpoint are all sound and satisfy REQ-03/REQ-06 in
shape. But two wiring gaps mean D2 ("RU from feed") and REQ-03-for-NP are **not reachable through the
live UI** as written — only via the audit script. Both are foldable into 09-02 execution.

### FLAG-1 (medium) — NP feed enriches ONLY category, not name_ru/description_ru
09-02 T4 builds `{article → category}` from the parsed feed and wires *only* `row_input["category"]`.
But the interface marks `SupplierProduct.description` as "(non-NP suppliers)" and NP carries no RU in
the DB → for NP unmatched rows, **name_ru / description_ru (and likely description-UA, name)** must be
pulled from the parsed feed by article and written into `row_input`, not just the category. As written,
NP cards import with **blank RU** — violating D2 ("RU from feed where it exists") and the objective
("name UA+RU where the feed has it", "description UA+RU").
→ **Fix in T4:** build one feed dict per article exposing `{name, name_ru, category, description,
description_ru}` (np_parser already surfaces all of these after T1) and enrich every NP `row_input`
field from it (DB value as fallback when the feed lacks one). Add a test: an NP SP whose feed row has
`title_ru`/`description_ru` emits non-empty `H_NAME_RU`/`H_DESC_RU`.

### FLAG-2 (medium) — /feeds/add endpoint never supplies np_feed_path
09-01 T3's POST calls `build_add_file(supplier.id, selected, export_path)` (no `np_feed_path`) and the
template has a single `export` upload. 09-02 T4 makes `build_add_file` *use* `np_feed_path` but lives
only in `add_horoshop_file.py` (its `files_modified` excludes the view/template) — so nothing ever
passes the NP feed in from the UI. Result: through the live page, the FeedCategoryResolver + FLAG-1
enrichment can never fire for NP; only the audit script (which takes `--np-feed`) exercises them.
→ **Fix:** expand 09-02 T4 (or add T4b) to also touch `app/views/feed.py` + `add_unmatched.html`:
add an OPTIONAL second upload `<input type="file" name="np_feed" accept=".xlsx">` (label «НП-фід
(.xlsx) — назви/опис/категорія RU для НП»), temp-file it exactly like the `export` field, and pass
`np_feed_path=` into `build_add_file`. Without a feed the chain degrades to analogy→fallback (still
valid). Add the file to T4's `files_modified`.

### MINOR-A (pin into 09-01 T1) — fix the `build_add_file` SP-access choice now
09-01 T1 step 3 offers a choice ("re-hydrate SP-like object OR have `_query_unmatched` return
(sp, row_input) pairs"). 09-02's FeedCategoryResolver/AnalogyResolver need live `sp.name/brand/article`.
→ **Pin:** `_query_unmatched` returns `list[(sp, row_input)]` pairs (resolver sees the real SP). Decide
this in 09-01 so 09-02 doesn't have to refactor the loop.

### MINOR-B (executor verifies empirically) — is NP description-UA in the DB or only the feed?
The interface comment implies NP UA description may also be feed-only. Executor: inspect one real NP
`SupplierProduct` row in the local sqlite; if `description` is empty for NP, FLAG-1's enrichment must
also fill `row_input["description"]` from the feed `description_uk`.

## Execution guidance
- Build 09-01 first; it stands alone (REQ-01/02/04/05) and unblocks nothing-blocks-it.
- In 09-02, treat FLAG-1 + FLAG-2 as part of T4's definition of done (RU + feed-category reachable via
  the UI, with a test proving non-empty H_NAME_RU/H_DESC_RU for an NP row). Pin MINOR-A in 09-01.
- 09-02 still ends at the blocking Yana checkpoint (T7) — AI stays disabled.
