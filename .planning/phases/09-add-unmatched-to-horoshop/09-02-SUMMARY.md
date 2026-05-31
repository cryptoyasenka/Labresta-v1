---
phase: 09-add-unmatched-to-horoshop
plan: 02
subsystem: api
tags: [horoshop, category-resolver, rapidfuzz, openpyxl, np-feed, flask]

# Dependency graph
requires:
  - phase: 09-add-unmatched-to-horoshop (plan 01)
    provides: "fallback-only category_resolver behind build_resolver(); add_horoshop_file builder + _query_unmatched returning (sp, row_input) pairs; /feeds/add picker"
provides:
  - "SMART category chain feed→analogy→fallback behind the SAME category_resolver interface (AI tier shipped DISABLED)"
  - "np_parser surfaces title_uk/title_ru/categories_uk (label-based, drift-resistant)"
  - "category_export.read_category_corpus recovers the «Раздел» corpus from a Horoshop export"
  - "NP create-card name/name_ru/description(_ru) enrichment from the NP feed (FLAG-1/D2)"
  - "optional second np_feed upload on /feeds/add (FLAG-2)"
  - "read-only, prod-guarded category-analogy evidence audit script"
  - "CATEGORY-PROPOSAL.md grounded in a real 320-product audit for Yana's strategy decision"
affects: [horoshop-import, np-bulk-import, category-mapping, ai-category-tier]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Three-tier ChainResolver (feed→analogy→fallback) — first non-empty category wins, fallback last; AI tier insertable by config, no refactor"
    - "Feed-category reconciliation to the store tree (never emit a category Horoshop can't create)"
    - "Brand-blocked analogy ranking via rapidfuzz.token_sort_ratio over matcher PRIMITIVES (not find_match_candidates)"
    - "Header-label column lookup (not fixed index) for both NP feed and export corpus"
    - "Prod-DB hard guard on audit scripts (abort unless local sqlite)"

key-files:
  created:
    - app/services/category_export.py
    - scripts/audit_category_analogy.py
    - .planning/phases/09-add-unmatched-to-horoshop/CATEGORY-PROPOSAL.md
  modified:
    - app/services/np_parser.py
    - app/services/category_resolver.py
    - app/services/add_horoshop_file.py
    - app/views/feed.py
    - app/templates/feeds/add_unmatched.html
    - tests/test_np_parser.py
    - tests/test_category_resolver.py
    - tests/test_views_add_horoshop.py

key-decisions:
  - "AI tier ships DISABLED (D3/REQ-06) — AICategoryResolver returns None when disabled (zero network), raises NotImplementedError if enabled; not wired live"
  - "Feed tier reconciles to the store tree at cutoff 80; analogy cutoff 60; both reuse matcher primitives only"
  - "NP create-card RU name + description come from the feed (matcher DB has no name_ru column and NP description is empty) — FLAG-1/D2"

patterns-established:
  - "Category chain behind one interface so AI is a config flip (strategies + ai_enabled), not a rewrite"
  - "Evidence-before-decision: a prod-guarded read-only audit produces real numbers feeding a proposal doc"

requirements-completed: [REQ-03, REQ-06]

# Metrics
duration: ~95min
completed: 2026-05-31
---

# Phase 09 Plan 02: Smart Category Resolution Summary

**Three-tier feed→analogy→fallback «Раздел» resolution layered onto the Phase 9 core behind the same `category_resolver` interface (AI shipped disabled), plus NP feed name/RU/description enrichment, an optional NP-feed upload, and a prod-guarded evidence audit that placed 95.3% of 320 real unmatched NP products automatically.**

## Performance

- **Duration:** ~95 min
- **Started:** 2026-05-31T02:55:00Z (approx)
- **Completed:** 2026-05-31T04:30:00Z (approx)
- **Tasks:** 6 of 7 (T7 is a blocking `checkpoint:decision` — awaits Yana; plan is `autonomous:false`)
- **Files modified:** 11 (3 created, 8 modified)

## Accomplishments
- **Smart chain shipped** behind the unchanged `category_resolver` interface: `FeedCategoryResolver` (reconciles the NP feed category to the store tree, exact→100 else token similarity ≥80), `AnalogyResolver` (same-brand nearest card by rapidfuzz, cutoff 60), `FallbackResolver` (holding category). `build_resolver(strategies=("feed","analogy","fallback"), ai_enabled=False)`.
- **AI tier shipped DISABLED** (D3/REQ-06): `AICategoryResolver` returns `None` with zero network when disabled, raises `NotImplementedError` if enabled. No live AI call wired anywhere. Flipping it on is a one-argument change (documented in the proposal §5).
- **NP enrichment (FLAG-1/D2):** `_enrich_from_feed` backfills create-card `name/name_ru/description/description_ru` from the NP feed (the matcher DB has no `name_ru` column and NP `description` is empty), so NP cards no longer import with blank RU.
- **Optional NP-feed upload (FLAG-2):** `/feeds/add` accepts a second `np_feed` .xlsx (temp-filed like the export, unlinked in `finally`); `by_source` + `np_feed` added to the action log.
- **Evidence audit:** `scripts/audit_category_analogy.py` (read-only, hard prod-guarded) ran over **320 real unmatched NP products** → feed 130 (40.6%) / analogy 175 (54.7%) / fallback 15 (4.7%); wrote a per-row CSV and printed the feed↔store reconciliation delta (50 of 76 feed categories unmapped).
- **Proposal:** `CATEGORY-PROPOSAL.md` grounds every claim in that audit and lays out three options for Yana.

## Task Commits

Each task was committed atomically on `feat/horoshop-add-unmatched`:

1. **Task 1: np_parser surfaces title_uk/title_ru/categories_uk** - `1b4def4` (feat)
2. **Task 2: category_export reader recovers the «Раздел» corpus** - `514506d` (feat)
3. **Task 3: smart category tiers — feed/analogy/AI-stub chain** - `ae92685` (feat)
4. **Task 4: wire smart chain + NP feed enrichment into the create-file (+FLAG-1/FLAG-2)** - `df626e0` (feat)
5. **Task 5: read-only, prod-guarded category-analogy evidence audit script** - `7c95c07` (feat)
6. **Task 6: CATEGORY-PROPOSAL.md grounded in real audit evidence** - `2b07378` (docs)

**Task 7:** blocking `checkpoint:decision` — NOT executed (awaits Yana).

## Files Created/Modified
- `app/services/category_export.py` (created) - `read_category_corpus(export_path)` recovers `{external_id, display_article, name, brand, category}` rows + distinct categories from a Horoshop export (label-based column lookup, Sheet1/first sheet, aborts cleanly if article/category columns missing).
- `app/services/np_parser.py` - added label-based `_find_col` + surfaces `name` (title_uk), `name_ru` (title_ru), `category` (categories_uk); missing optional columns are non-fatal warnings.
- `app/services/category_resolver.py` - added `FeedCategoryResolver`, `AnalogyResolver`, `AICategoryResolver` (disabled stub), `_norm_brand`/`_leaf` helpers; extended `build_resolver` with feed/analogy/ai tiers + cutoffs. CORE fallback behaviour preserved.
- `app/services/add_horoshop_file.py` - `_enrich_from_feed`; `build_add_file` builds the smart resolver from the export corpus + per-article NP feed getter, enriches NP rows, and reports `manifest["by_source"]`.
- `app/views/feed.py` - optional `np_feed` upload (temp-filed, cleaned up), `by_source`/`np_feed` in the action log (FLAG-2).
- `app/templates/feeds/add_unmatched.html` - optional «НП-фід (.xlsx)» file input + UA help text.
- `scripts/audit_category_analogy.py` (created) - read-only, prod-guarded evidence run; CSV + console by-source/distribution/reconciliation-delta.
- `tests/test_np_parser.py`, `tests/test_category_resolver.py`, `tests/test_views_add_horoshop.py` - unit + endpoint coverage incl. the FLAG-1 NP-feed→non-empty H_NAME_RU/H_DESC_RU test and the analogy-overrides-fallback test.
- `.planning/phases/09-add-unmatched-to-horoshop/CATEGORY-PROPOSAL.md` (created) - evidence + options + canary for Yana.

## Decisions Made
- **AI stays off by default** (D3/REQ-06). The disabled stub makes no network call; the proposal documents the one-line flip and the work still needed (implement the enabled path, verify endpoint/model, constrain to store labels, add tests).
- **Reconcile cutoff 80 / analogy cutoff 60** — defaults exposed via `build_resolver`; the audit shows feed reconciliation is high-confidence (all ≥80, 94/130 ≥90) while the analogy 60–69 band (45 cards) is the soft spot.
- **NP RU/description sourced from the feed**, confirmed empirically (no `name_ru` column on `SupplierProduct`; NP `description` empty in local sqlite) — FLAG-1/MINOR-B justified.

## Deviations from Plan

All three plan-check flags were folded into Task 4 exactly as instructed (these were pre-agreed inclusions, not unplanned auto-fixes):

- **FLAG-1 (D2):** NP feed now enriches `name/name_ru/description/description_ru`, not just `category`; covered by a dedicated endpoint test asserting non-empty `H_NAME_RU`/`H_DESC_RU`.
- **FLAG-2:** added the optional `np_feed` upload to `app/views/feed.py` + `app/templates/feeds/add_unmatched.html` (both added to T4 files).
- **MINOR-B:** verified the real NP row in local sqlite (empty description, no RU) → enrichment also fills `description`.

One small test-fixture correction during T4 (Rule 1, no scope change):

**1. [Rule 1 - Bug] Realistic export-card name in the analogy endpoint test**
- **Found during:** Task 4 (writing the analogy-overrides-fallback test)
- **Issue:** the first draft gave the export's HURAKAN card a placeholder name ("Існуюча картка") that shares no tokens with the unmatched SP ("Льодогенератор HKN"), so the analogy tier correctly scored below cutoff and fell to fallback — the test asserted analogy. The resolver was right; the fixture was unrealistic.
- **Fix:** named the export card "Льодогенератор HKN-450" so the analog legitimately matches (confidence 89.5, verified empirically before editing the test).
- **Files modified:** tests/test_views_add_horoshop.py
- **Verification:** test passes; full suite 835 passed, 2 skipped.
- **Committed in:** df626e0 (Task 4 commit)

---

**Total deviations:** flags folded as instructed + 1 test-fixture correction (Rule 1).
**Impact on plan:** none on scope. All flags were mandated. The AI tier remains disabled; the builder remains read-only; no live import performed.

## Issues Encountered
- **Plan's NP column positions were guessed** (interface block implied title_uk near description); real positions are title_uk@6, categories_uk@8, title_ru@15. No code change needed — the label-based `_find_col` lookup handles any position, as the plan itself directed ("locate by header label, not a guessed index").
- **`SupplierProduct` has no `name_ru` column** — a first test draft passed `name_ru=None` to the constructor and errored. This is exactly the FLAG-1 premise (NP RU lives only in the feed); fixed the test to drop the kwarg.

## User Setup Required
None - no external service configuration required. (Enabling the optional AI tier later would require a `NVIDIA_API_KEY` and the implementation described in CATEGORY-PROPOSAL.md §5.)

## Next Phase Readiness
- **T7 awaits Yana — BLOCKING `checkpoint:decision`.** She picks the category strategy: **ship-no-ai** (recommended first) / **enable-ai** / **mapping-table**, and confirms the 1–2 row `[КАТАЛОГ] Раздел` canary before any bulk import (invariant #13, her hand + backup). Evidence is in `CATEGORY-PROPOSAL.md`.
- The smart chain is shipped, tested (full suite green), and read-only. If Yana picks `enable-ai` or `mapping-table`, a follow-up plan wires it (one-argument change for AI; ~50-line dict for the mapping table — full unmapped list is in the proposal appendix).
- **No bulk Horoshop import performed** — that stays Yana's hand.

## Self-Check: PASSED

- All 3 created files + 5 modified-by-this-plan files present on disk.
- All 6 task commits (1b4def4, 514506d, ae92685, df626e0, 7c95c07, 2b07378) exist on the branch.
- Full test suite: 835 passed, 2 skipped.

---
*Phase: 09-add-unmatched-to-horoshop*
*Completed: 2026-05-31*
