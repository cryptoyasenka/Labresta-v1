---
phase: 09-add-unmatched-to-horoshop
verified: 2026-05-31T04:30:00Z
status: passed
score: 9/9 goal deliverables verified
re_verification: # none — initial verification
  previous_status: none
human_verification:
  - test: "T7 — category strategy decision (ship-no-ai / enable-ai / mapping-table) + canary approval"
    expected: "Yana reviews CATEGORY-PROPOSAL.md + a real-data analogy audit, then picks the strategy and approves the 718.3/845.0 canary before any live import"
    why_human: "Business/product decision and live-store risk gate — the plan 09-02 is explicitly non-autonomous and ends at checkpoint:decision. Code ships AI DISABLED by default; enabling is Yana's call only."
---

# Phase 09: Add Unmatched Products to Horoshop — Verification Report

**Phase Goal:** A picker page selecting supplier products with no Horoshop card (no confirmed/manual ProductMatch) via supplier+brand filters + checkboxes (mirroring /feeds/np), generating a native-Horoshop create-card XLSX carrying name UA/RU, price+discount, availability, description UA/RU, photo, Артикул, brand, visibility="1", and a guaranteed non-empty category (smart chain feed→analogy→fallback holding «Новые товары / на разбор»).
**Verified:** 2026-05-31T04:30:00Z
**Status:** passed (PASS-WITH-NOTES — one legitimate human gate T7 remains)
**Re-verification:** No — initial verification

## Goal Achievement

### Full Test Suite (empirical)

```
835 passed, 2 skipped, 1 warning in 24.39s
```

Executor claimed "835 passed, 2 skipped" — **CONFIRMED, exact match.** (The 1 warning is a pre-existing urllib3/chardet version-mismatch warning, unrelated to this phase.)
Targeted isolation run of canary + FLAG-1 + resolver tests: **36 passed, 11 deselected in 0.30s.**

### Observable Truths (the 9 goal deliverables)

| # | Deliverable | Status | Evidence |
| --- | ----------- | ------ | -------- |
| 1 | Название UA + name RU where feed has it | ✓ VERIFIED | H_NAME_UA + H_NAME_RU columns; `_enrich_from_feed` backfills name/name_ru from feed (feed-first, DB fallback; NP DB never holds RU → always prefer feed RU). add_horoshop_file.py:67,216,320 |
| 2 | Цена + скидка (oldprice) — canary HURAKAN 15%, 84500 → 718.3 / "845.0" / EUR | ✓ VERIFIED | `price_unmatched` → `resolve_discount_percent(None,...)` + `calculate_price_eur` (NO compute_match_pricing). Test asserts `sell == 718.3`, `oldprice == "845.0"` at price_cents=84500/EUR/HURAKAN. test_add_horoshop_file.py:236,243 |
| 3 | Наличие | ✓ VERIFIED | H_AVAIL = "В наличии"/"Нет в наличии" from `ri["available"]`. add_horoshop_file.py:73,89-90,222 |
| 4 | Описание UA + RU where feed has it | ✓ VERIFIED | H_DESC_UA + H_DESC_RU; `_enrich_from_feed` fills description/description_ru from feed. add_horoshop_file.py:76-77,225-226,320 |
| 5 | Фото | ✓ VERIFIED | H_GALLERY = `;`.join(photos); photos from images JSON or image_url. add_horoshop_file.py:75,224,296-298 |
| 6 | Артикул = Horoshop create match-key (sp.article) | ✓ VERIFIED | H_ARTICLE = bare "Артикул" (top-level field, CREATE KEY); article = sp.article stripped; empty-article rows skipped + counted. add_horoshop_file.py:65,190-193,214 |
| 7 | brand | ✓ VERIFIED | H_BRAND from sp.brand. add_horoshop_file.py:68,217 |
| 8 | visibility [КАТАЛОГ] Отображать = "1" | ✓ VERIFIED | `_VISIBLE_YES = "1"`; H_VISIBLE always set to it. add_horoshop_file.py:74,91,223 |
| 9 | category [КАТАЛОГ] Раздел — guaranteed non-empty (smart chain + fallback «Новые товары / на разбор») | ✓ VERIFIED | H_CATEGORY = "[КАТАЛОГ] Раздел"; `build_resolver` puts FallbackResolver last → non-empty guaranteed; DEFAULT_FALLBACK_CATEGORY = "Новые товары / на разбор". category_resolver.py:48,90-105,311-312 |

**Score:** 9/9 deliverables verified.

### Goal-backward checklist (task-specific)

| Check | Status | Evidence |
| ----- | ------ | -------- |
| Unmatched query: read-only correlated NOT-EXISTS over status∈{confirmed,manual}, NO `published` predicate (Q7) | ✓ | `_query_unmatched` uses `~exists(linked)` with `ProductMatch.status.in_(("confirmed","manual"))`; explicit comment "`published` is deliberately NOT part of the predicate". add_horoshop_file.py:254-280 |
| `_query_unmatched` returns `(sp, row_input)` pairs (MINOR-A) | ✓ | `pairs: list[tuple]`, each `(sp, row_input)`. add_horoshop_file.py:290-310 |
| FLAG-1: NP row with feed title_ru/description_ru → non-empty H_NAME_RU/H_DESC_RU | ✓ | Test `test_generate_np_feed_fills_ru_name_and_description` at test_views_add_horoshop.py:221; enrichment feed-first, DB fallback. PASSES. |
| FLAG-2: /feeds/add template has optional np_feed upload + POST threads `np_feed_path` into build_add_file | ✓ | Template `<input type=file name="np_feed">` (add_unmatched.html:86) + enctype multipart; feed.py:359-378 reads `np_feed` upload → `build_add_file(..., np_feed_path=np_feed_path)` |
| AI DISABLED: enabled=False → None/no network; enabled=True → NotImplementedError; no active AI call wired | ✓ | AICategoryResolver enabled=False returns None immediately; enabled=True raises NotImplementedError. Grep for active `requests`/`http`/nvidia call in resolver path = NONE FOUND (only docstring references). category_resolver.py:235-274; test_ai_disabled_returns_none_no_network + test_ai_enabled_is_stub |
| Read-only invariant: builder writes nothing except existing audit log_action | ✓ | NO db.session.add/commit/delete in add_horoshop_file.py. Only write = existing `log_action("add_file_generate")` + commit in the view (feed.py:386,397), mirroring np_file_generate |
| Audit script prod guard (abort if not sqlite, or rlwy/railway/postgres/psycopg) | ✓ | scripts/audit_category_analogy.py:74-77 — `if "sqlite" not in url or any(t in url for t in ("rlwy","railway","postgres","psycopg")): print("ABORT...") ` |
| No live import; nothing merged to main | ✓ | On branch feat/horoshop-add-unmatched, working tree clean; main untouched (diff shows only this branch's files) |

### Required Artifacts

| Artifact | Status | Details |
| -------- | ------ | ------- |
| app/services/add_horoshop_file.py | ✓ VERIFIED | 441 lines (min 180). HEADERS (13 cols), _shape_rows, _workbook_bytes, _query_unmatched, price_unmatched, _enrich_from_feed, build_add_file |
| app/services/category_resolver.py | ✓ VERIFIED | 359 lines (min 150). Protocol+CategoryResult, FallbackResolver, FeedCategoryResolver, AnalogyResolver, AICategoryResolver (disabled stub), build_resolver chain |
| app/services/category_export.py | ✓ VERIFIED | 131 lines (min 40). read_category_corpus → {external_id, display_article, name, brand, category} |
| app/services/np_parser.py | ✓ VERIFIED | Surfaces title_uk/title_ru/categories_uk via label scan |
| app/views/feed.py | ✓ VERIFIED | GET /feeds/add picker + POST generate, @login_required, supplier+brand+export+np_feed uploads |
| app/templates/feeds/add_unmatched.html | ✓ VERIFIED | 108 lines. Mirrors feeds/np.html: supplier select, brand checkboxes, export + np_feed file inputs |
| scripts/audit_category_analogy.py | ✓ VERIFIED | 194 lines, sqlite-only prod guard, runs analogy over real unmatched SPs |
| .planning/.../CATEGORY-PROPOSAL.md | ✓ VERIFIED | Present (analogy-vs-AI-vs-hybrid proposal for Yana) |
| tests/test_add_horoshop_file.py | ✓ VERIFIED | 319 lines, 23 tests |
| tests/test_views_add_horoshop.py | ✓ VERIFIED | 291 lines, 9 tests (incl FLAG-1) |
| tests/test_category_resolver.py | ✓ VERIFIED | 23 tests (feed/analogy/fallback chain, threshold/cutoff, AI-disabled-no-network, AI-enabled-stub) |
| tests/test_np_parser.py | ✓ VERIFIED | 11 tests |

gsd-tools `verify artifacts`: 09-01 = 6/6 passed, 09-02 = 6/6 passed.

### Key Link Verification (manual grep — gsd-tools mis-parsed `from:` fields containing parentheses/slashes and falsely reported "Source file not found"; all confirmed WIRED by grep)

| From | To | Via | Status |
| ---- | -- | --- | ------ |
| feed.py add_file_generate | add_horoshop_file build_add_file | call with supplier_id, selected, export_path, np_feed_path | ✓ WIRED (feed.py:41,377-378) |
| add_horoshop_file build_add_file | category_resolver build_resolver/resolve | resolver.resolve(sp) → category | ✓ WIRED (add_horoshop_file.py:50,422-423) |
| add_horoshop_file price_unmatched | pricing resolve_discount_percent + calculate_price_eur | pure primitives, NO compute_match_pricing | ✓ WIRED (add_horoshop_file.py:54-56,139,153; no compute_match_pricing call) |
| category_resolver build_resolver | category_export read_category_corpus | export_rows corpus → AnalogyResolver | ✓ WIRED (resolver.py:189,352; add_horoshop_file.py imports + calls read_category_corpus:384) |
| category_resolver AnalogyResolver | matcher meaningful_tokens / _transliterate_cyr | brand-block + token_sort_ratio (primitives, NOT find_match_candidates) | ✓ WIRED (resolver.py:40-41,208,224; explicit "NOT find_match_candidates") |
| category_resolver FeedCategoryResolver | np_parser categories_uk | feed category reconciled to store tree | ✓ WIRED (resolver.py:109-144; getter in add_horoshop_file.py:399-401) |
| audit script | AnalogyResolver/build_resolver | runs analogy over real LOCAL-sqlite SPs | ✓ WIRED (gsd-tools confirmed) |

### Data-Flow Trace (Level 4)

| Artifact | Data variable | Source | Produces real data | Status |
| -------- | ------------- | ------ | ------------------ | ------ |
| add_unmatched.html picker | suppliers / brands | feed.py GET reads SupplierProduct via existing query path (mirrors /feeds/np) | Yes (live DB query, same as np picker) | ✓ FLOWING |
| build_add_file rows | unmatched pairs | `_query_unmatched` correlated NOT-EXISTS on real ProductMatch/SupplierProduct | Yes (real ORM query, read-only) | ✓ FLOWING |
| category column | res.category | resolver chain over feed (parse_np_feed) + corpus (read_category_corpus) + fallback | Yes (feed/export parsed; fallback guaranteed) | ✓ FLOWING |

Note: end-to-end "real XLSX from real store data" is exercised by endpoint tests with synthetic fixtures (correct for unit/integration). The actual production import is the human gate (T7), by design — no live data was pushed.

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
| -------- | ------- | ------ | ------ |
| Full suite green | pytest -q | 835 passed, 2 skipped | ✓ PASS |
| Canary pricing 718.3/845.0/EUR | pytest -k price/discount/oldprice | asserted, passes | ✓ PASS |
| FLAG-1 RU enrichment | pytest test_generate_np_feed_fills_ru_name_and_description | passes | ✓ PASS |
| AI disabled, no network | pytest test_ai_disabled_returns_none_no_network | passes | ✓ PASS |
| Resolver chain feed→analogy→fallback | pytest test_category_resolver.py | 23 pass | ✓ PASS |

### Requirements Coverage

REQUIREMENTS.md carries no inline REQ-0X prose; ROADMAP.md:78 maps Phase 09 → REQ-01..REQ-06. Plan frontmatter assigns: 09-01 = REQ-01,02,04,05; 09-02 = REQ-03,06.

| Requirement | Source Plan | Maps to | Status | Evidence |
| ----------- | ----------- | ------- | ------ | -------- |
| REQ-01 | 09-01 | Picker + create-file builder | ✓ SATISFIED | /feeds/add view + add_horoshop_file.build_add_file |
| REQ-02 | 09-01 | Importable native-Horoshop XLSX (price/discount/avail/photo/article/brand/visibility) | ✓ SATISFIED | 13-col HEADERS, canary asserted |
| REQ-03 | 09-02 | Correct category not just fallback (smart chain) | ✓ SATISFIED | feed→analogy→fallback; tests pass. (Strategy choice = T7 human gate) |
| REQ-04 | 09-01 | Read-only / no DB writes | ✓ SATISFIED | builder no writes; only existing audit log_action |
| REQ-05 | 09-01 | Fallback guarantees non-empty Раздел | ✓ SATISFIED | FallbackResolver always last |
| REQ-06 | 09-02 | Real-data evidence + proposal; AI not default | ✓ SATISFIED | CATEGORY-PROPOSAL.md + audit script + AI disabled-by-default. (Approval = T7) |

### Anti-Patterns Found

None blocking. `skipped_no_category` manifest counter exists but with fallback-always-last it stays 0 in normal flow (defensive, not a stub). `name_ru: None` set in the DB query path is the intended DB-fallback value that feed enrichment overwrites — NOT a stub (verified `_enrich_from_feed` overwrites it from feed). No TODO/FIXME/placeholder in shipped source. No active network call in the AI path.

### Git Hygiene

- 9 commits on branch (task said 7 — the extra 2 are the docs(09-01)/docs(09-02) SUMMARY+state commits; all 7 code/feat commits present). Working tree clean.
- NO Claude / Co-Authored-By / "Generated with" / 🤖 traces in any commit message (grep clean).
- NO `instance/`, `.env`, `.db`, secrets, or tokens in the branch diff.
- main untouched; nothing merged.

### Human Verification Required (the one legitimate open gate)

**T7 — category strategy decision + canary approval.** Plan 09-02 is explicitly non-autonomous (`autonomous: false`, ends at checkpoint:decision). Yana must review CATEGORY-PROPOSAL.md + a real-data analogy audit and choose: ship-no-AI (feed+analogy+fallback as-is) vs enable-AI (NVIDIA, config flip) vs a mapping table — and approve the 718.3/"845.0" canary — before any live Horoshop import. This is the intended product/risk gate, **not a defect.**

### Gaps Summary

No gaps. All 9 goal deliverables, all 8 goal-backward checklist items, all 12 artifacts, and all 7 key links verified against the actual code and a green full suite (835/2/0). The single remaining item is the by-design human decision T7.

---

_Verified: 2026-05-31T04:30:00Z_
_Verifier: Claude (gsd-verifier)_
