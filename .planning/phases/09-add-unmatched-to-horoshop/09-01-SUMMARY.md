---
phase: 09-add-unmatched-to-horoshop
plan: 01
subsystem: feeds
tags: [horoshop, xlsx, openpyxl, pricing, category-resolver, create-file, flask]

# Dependency graph
requires:
  - phase: pricing primitives (app/services/pricing.py)
    provides: resolve_discount_percent / resolve_eur_rate / clamp_discount_for_min_margin / calculate_price_eur / calculate_auto_discount
  - phase: NP builder (app/services/np_horoshop_file.py)
    provides: native-schema XLSX writer pattern + _shape_rows/_workbook_bytes shape
provides:
  - "app/services/add_horoshop_file.py — Horoshop CREATE-file builder for unmatched SupplierProducts (read-only)"
  - "price_unmatched(sp) — pure pricing for a product with no ProductMatch (reproduces canary 718.3/845.0/EUR)"
  - "app/services/category_resolver.py — CategoryResult/CategoryResolver/FallbackResolver/ChainResolver/build_resolver (fallback-only tier)"
  - "GET /feeds/add + POST /feeds/add/generate — supplier+brand picker with optional Horoshop-export upload"
affects: [09-02, smart-category-resolution, feed-enrichment]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Create-file = NP update-file builder + the columns updates omit (Название UA/RU, Бренд, Раздел, Отображать=1); article is the create key"
    - "Category resolution behind a Protocol + ChainResolver so smart tiers (09-02) drop in without touching the builder"
    - "_query_unmatched returns (sp, row_input) pairs so resolvers see the live SP object"
    - "Read-only builder: correlated NOT-EXISTS over confirmed/manual matches, zero DB writes; only the view's audit log_action commits"

key-files:
  created:
    - app/services/add_horoshop_file.py
    - app/services/category_resolver.py
    - app/templates/feeds/add_unmatched.html
    - tests/test_add_horoshop_file.py
    - tests/test_category_resolver.py
    - tests/test_views_add_horoshop.py
  modified:
    - app/views/feed.py

key-decisions:
  - "Builder mirrors np_horoshop_file.py shape; header strings copied verbatim from the canary (not retyped)"
  - "_query_unmatched returns (sp, row_input) pairs (PLAN-CHECK MINOR-A) so 09-02's resolvers can inspect the SP"
  - "ProductMatch.published deliberately excluded from the NOT-EXISTS predicate (RESEARCH Q7) — a published=False confirmed match must NOT read as unmatched"
  - "Horoshop export upload is OPTIONAL in the core: without it the fallback resolver gives every card the holding category (still a valid file)"
  - "auto_margin suppliers derive the discount via calculate_auto_discount, not resolve_discount_percent (CLAUDE.md #12, pricing.py:99)"

patterns-established:
  - "Pattern: CREATE-file builder = NP content columns + create-only columns + supplier-article key + visibility=1"
  - "Pattern: category resolver chain (fallback-only core, smart tiers layered in 09-02 behind the same interface)"

requirements-completed: [REQ-01, REQ-02, REQ-04, REQ-05]

# Metrics
duration: ~35min
completed: 2026-05-31
---

# Phase 9 Plan 01: Add Unmatched Products to Horoshop (CORE) Summary

**A logged-in operator picks a supplier + brands at /feeds/add and downloads a native-Horoshop CREATE XLSX (name UA/RU, brand, price/old-price, availability, gallery, description, Артикул, Отображать=1, and a guaranteed `[КАТАЛОГ] Раздел`) for every supplier product with no confirmed/manual match — read-only over the DB, fallback-only category so the file imports on its own.**

## Performance

- **Duration:** ~35 min
- **Started:** 2026-05-31 (TDD: RED → GREEN per task)
- **Completed:** 2026-05-31
- **Tasks:** 4 (T0 failing tests, T1 builder, T2 resolver, T3 view+template+endpoint tests)
- **Files created:** 6 | **Files modified:** 1

## Accomplishments
- `add_horoshop_file.py` — create-file builder: `HEADERS` with create columns + 6 NP content columns, `_shape_rows`, `_workbook_bytes` (verbatim from NP), `_query_unmatched` (read-only NOT-EXISTS returning (sp, row_input) pairs), `build_add_file` (DB shell, fallback resolver default).
- `price_unmatched(sp)` — pure pricing path with no ProductMatch; reproduces the canary 718.3 / 845.0 / EUR for a 15% HURAKAN SP; handles per-brand override, UAH→rate=1, min-margin clamp, and the auto_margin branch.
- `category_resolver.py` — `CategoryResult` dataclass, `CategoryResolver` Protocol, `FallbackResolver`, `ChainResolver`, `build_resolver` factory; fallback-only chain guarantees a non-empty Раздел; forward-compatible with 09-02's smart tiers (`export_rows` accepted, unknown strategy names ignored).
- `/feeds/add` picker (supplier select + DB-derived brand checkboxes with unmatched counts + optional export upload) and `/feeds/add/generate` (builds + downloads the XLSX); both `@login_required`, read-only (only the audit `log_action` commits).

## Task Commits

Each task committed atomically on `feat/horoshop-add-unmatched`:

1. **Task 0: failing builder tests (RED)** — `a90af42` (test)
2. **Task 1: create-file builder + price_unmatched (GREEN)** — `0a319f7` (feat)
3. **Task 2: fallback-only category_resolver (GREEN)** — `71849a1` (feat)
4. **Task 3: /feeds/add picker view + template + endpoint tests (GREEN)** — `e9b69e8` (feat)

_Note: T1's commit also corrected two of my own incorrect test expected values (see Deviations)._

## Files Created/Modified
- `app/services/add_horoshop_file.py` — Horoshop CREATE-file builder + `price_unmatched` (read-only).
- `app/services/category_resolver.py` — category resolution interface + fallback tier.
- `app/views/feed.py` — added `_supplier_brands`, `_unmatched_brand_counts`, `_unmatched_exists_predicate`, GET `/feeds/add`, POST `/feeds/add/generate`; import of `build_add_file`, `distinct`, `exists`.
- `app/templates/feeds/add_unmatched.html` — supplier+brand picker mirroring `feeds/np.html`, with optional export upload (multipart).
- `tests/test_add_horoshop_file.py` — 23 pure-dict builder + `price_unmatched` tests.
- `tests/test_category_resolver.py` — 6 resolver tests (09-02 will append).
- `tests/test_views_add_horoshop.py` — 7 endpoint tests.

## Test Results
- New-file set: **36 passed** (`tests/test_add_horoshop_file.py` 23 + `tests/test_category_resolver.py` 6 + `tests/test_views_add_horoshop.py` 7).
- T0 confirmed RED before T1: `ModuleNotFoundError: No module named 'app.services.add_horoshop_file'`.
- Full suite stays green: **814 passed, 2 skipped** (the 2 skips and the urllib3 `RequestsDependencyWarning` are pre-existing, unrelated to this plan).

## Decisions Made
- Followed the plan as written, including the PLAN-CHECK MINOR-A pin: `_query_unmatched` returns `(sp, row_input)` pairs and `build_add_file` sets `row_input["category"] = resolver.resolve(sp, brand=...).category`.
- Kept the export upload optional in the core (fallback resolver covers the no-export case), matching the plan's explicit guidance.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Corrected my own test expected value: openpyxl empty-cell roundtrip**
- **Found during:** Task 1 (builder GREEN run)
- **Issue:** `test_workbook_bytes_roundtrip` asserted a reloaded blank `H_NAME_RU` cell equals `""`, but openpyxl normalizes an empty-string cell to `None` on read. The builder correctly writes `""`; the assertion was wrong.
- **Fix:** Relaxed the assertion to `in (None, "")` with a comment. The in-memory `_shape_rows` test (`test_name_ru_blank_when_absent`) still asserts the dict value is exactly `""`.
- **Files modified:** tests/test_add_horoshop_file.py
- **Verification:** All 23 builder tests pass.
- **Committed in:** `0a319f7` (Task 1 commit)

**2. [Rule 1 - Bug] Corrected my own test expected value: integer min-margin clamp**
- **Found during:** Task 1 (builder GREEN run)
- **Issue:** `test_uah_rate_is_1` expected sell == 3500.0 (margin exactly 500), but `clamp_discount_for_min_margin` floors the discount to an integer % (12, not 12.5), so the real sell is 3520.0. The test's *purpose* (prove UAH forces rate=1) is unchanged.
- **Fix:** Asserted `sell_uah == 3520.0` and added `assert sell_uah != 3200.0` to prove rate=1 was applied (the unclamped 20% would be 3200; the clamp only bites when rate=1).
- **Files modified:** tests/test_add_horoshop_file.py
- **Verification:** All 23 builder tests pass; manual arithmetic check matches.
- **Committed in:** `0a319f7` (Task 1 commit)

---

**Total deviations:** 2 auto-fixed (both Rule 1 — my own incorrect test expectations, not builder behavior changes).
**Impact on plan:** No scope change. The builder behaves exactly as the plan specified; only two test assertions were corrected to match real openpyxl/clamp arithmetic.

## Issues Encountered
- Module-import ordering: `add_horoshop_file.py` imports `build_resolver` from `category_resolver`, so `test_add_horoshop_file.py` could not even collect until `category_resolver.py` existed. Resolved by creating `category_resolver.py` (Task 2's deliverable) before Task 1's GREEN run, then committing in task order (T1 builder, T2 resolver). Tests for each module are committed with their task.

## Known Stubs
- The CORE ships a **fallback-only** category resolver by design: every unmatched card gets the holding category «Новые товары / на разбор». This is NOT an accidental stub — it is the planned core behavior (REQ-03 is explicitly deferred to plan 09-02, which layers feed/analogy/AI tiers behind the same `category_resolver` interface). The `build_resolver(export_rows, strategies=...)` signature is forward-compatible; `export_path`/`np_feed_path` are threaded through `build_add_file` for 09-02 to consume. The file is fully importable on its own with the fallback category.
- **Operator setup required (not code):** the fallback category «Новые товары / на разбор» MUST be pre-created in the Horoshop admin before any bulk import — Horoshop does not create missing categories on import (RESEARCH Q2/Pitfall 2).

## User Setup Required
None in code. Operator action: pre-create the «Новые товары / на разбор» category in Horoshop admin before importing a generated file. The live Horoshop import remains Yana's hand (invariant #13) — this plan only produces the file.

## Next Phase Readiness
- 09-02 can implement smart category tiers (feed_category / analogy / AI) as new resolvers inserted ahead of `FallbackResolver` in `build_resolver`, keyed off `strategies` and built from `export_rows`. No builder changes needed — `build_add_file` already passes the SP into `resolver.resolve(sp, brand=...)`.
- FLAG-1/FLAG-2 (feed RU enrichment + np_feed upload) are out of scope here and remain for 09-02.

## Self-Check: PASSED

All 6 created files + the SUMMARY exist on disk; all 4 task commits (`a90af42`, `0a319f7`, `71849a1`, `e9b69e8`) are present in the git log.

---
*Phase: 09-add-unmatched-to-horoshop*
*Completed: 2026-05-31*
