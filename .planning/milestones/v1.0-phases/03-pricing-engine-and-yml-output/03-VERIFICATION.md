---
phase: 03-pricing-engine-and-yml-output
verified: 2026-02-28T23:00:00Z
status: passed
score: 13/13 must-haves verified
re_verification:
  previous_status: passed
  previous_score: 11/11
  note: "Previous verification predated gap-closure plans 03-03 and 03-04. Re-verification adds 2 new truths and 4 new artifacts from those plans, covering the full post-UAT codebase."
  gaps_closed:
    - "Each offer in the YML feed contains a <url> element (UAT test 3 failure — now fixed in 03-03)"
    - "Match candidates with implausible price ratios are rejected (UAT test 4 failure — now fixed in 03-04)"
  gaps_remaining: []
  regressions: []
human_verification:
  - test: "Open instance/feeds/labresta-feed.yml in a browser or text editor and check Cyrillic product names"
    expected: "Names render correctly in UTF-8 — not garbled. Check that <url> elements are present on products imported after the 03-03 re-import."
    why_human: "Terminal output on Windows can garble Cyrillic due to console encoding; the file bytes may be correct. A human must confirm actual file content."
  - test: "Configure prom.ua to poll the /feed/yml URL and trigger an import"
    expected: "prom.ua accepts the feed, updates prices and availability for confirmed matched products."
    why_human: "Cannot simulate prom.ua's parser in automated tests; requires live external service interaction."
  - test: "While a sync is running, issue GET /feed/yml repeatedly"
    expected: "Every response is a complete, valid XML file — never a partial write."
    why_human: "The tempfile + os.replace pattern is correct, but concurrent behavior under real load requires human observation."
---

# Phase 3: Pricing Engine and YML Output Verification Report

**Phase Goal:** Confirmed matches produce a correctly priced, publicly accessible YML feed that prom.ua can poll automatically — and only matched products are included in the output.
**Verified:** 2026-02-28
**Status:** PASSED
**Re-verification:** Yes — supersedes initial verification; now covers all four plans including gap-closure plans 03-03 (YML URL) and 03-04 (matcher price gate).

---

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|---------|
| 1 | Supplier-level discount is applied to retail price correctly | VERIFIED | `calculate_price_eur(19999, 15.0) == 170` passes (test_basic_discount) |
| 2 | Per-product discount overrides supplier-level discount | VERIFIED | `get_effective_discount(20.0, 15.0) == 20.0`; `get_effective_discount(None, 15.0) == 15.0` — both pass |
| 3 | Prices use integer-cent math with mathematical rounding (0.5 rounds up) | VERIFIED | `(discounted_cents + 50) // 100` pattern in source; test_half_rounds_up and test_below_half_rounds_down pass |
| 4 | Zero/missing price products are detected as invalid | VERIFIED | `is_valid_price(0) is False`, `is_valid_price(None) is False`, `is_valid_price(-100) is False` — all pass |
| 5 | Generated YML contains only confirmed matches with correct discounted prices | VERIFIED | `.where(ProductMatch.status == "confirmed")` confirmed in yml_generator.py line 40; pricing chain: get_effective_discount -> calculate_price_eur applied per offer |
| 6 | YML file is written atomically (tmp + rename) and never half-written | VERIFIED | `tempfile.mkstemp(suffix=".tmp", prefix="yml_", dir=yml_dir)` + `os.replace(tmp_path, output_path)` + `os.unlink` on failure in yml_generator.py lines 116-134 |
| 7 | Public URL /feed/yml serves the YML without authentication | VERIFIED | feed_bp route at `/feed/yml` in feed.py; no login_required decorator; `app.register_blueprint(feed_bp)` in `__init__.py` line 33; returns `mimetype="application/xml"` |
| 8 | YML regenerates automatically after each successful sync | VERIFIED | Stage 6/6 `regenerate_yml_feed()` in `_sync_single_supplier` at sync_pipeline.py line 119; lazy import inside try block |
| 9 | Products with zero/missing price appear as out-of-stock in YML | VERIFIED | `is_valid_price(sp.price_cents)` check sets `avail_str = "false"` and `price_eur = 0` when invalid (yml_generator.py lines 73-83) |
| 10 | Disappeared products appear as out-of-stock in YML | VERIFIED | `sp.available and not sp.needs_review` guards availability; disappeared products set `available=False, needs_review=True` in pipeline Stage 4 |
| 11 | Failed sync does NOT regenerate YML — previous version preserved | VERIFIED | Stage 6 is inside the `try` block; any exception in Stages 1-5 propagates to `except Exception` which sets status="error" and returns before Stage 6 |
| 12 | Each offer in the YML feed contains a `<url>` element pointing to the prom.ua product page | VERIFIED | `if pp.page_url: etree.SubElement(offer, "url").text = pp.page_url` at yml_generator.py line 93-94; same pattern in yml_test_generator.py line 46-47; `page_url` column on PromProduct model; COLUMN_ALIASES maps Ukrainian/Russian URL headers |
| 13 | Match candidates with a price ratio >3x between supplier and prom product are rejected | VERIFIED | `MAX_PRICE_RATIO = 3.0` constant at matcher.py line 31; Step 5 price gate post-filter at lines 129-148; `test_rejects_high_ratio` (107300 vs 13500 = 7.9x, 0 results), `test_rejects_just_over_3x` (10000 vs 31000 = 3.1x, 0 results) — both pass; `test_keeps_plausible_rejects_implausible` passes |

**Score:** 13/13 truths verified

**Test run (confirmed):** `21 passed in 0.33s` — 14 pricing tests + 7 price gate tests, no failures.

---

## Required Artifacts

### Plan 03-01 Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `app/services/pricing.py` | Pure pricing calculation functions | VERIFIED | 50 lines, substantive; exports `calculate_price_eur`, `get_effective_discount`, `is_valid_price`; no DB access, no side effects; all three functions called by yml_generator.py |
| `app/models/product_match.py` | Per-product discount column | VERIFIED | `discount_percent = db.Column(db.Float, nullable=True)` at line 33; comment: "Per-product override; NULL = use supplier default" |
| `tests/test_pricing.py` | Pricing edge case coverage | VERIFIED | 79 lines, 14 test cases (7 calculate_price_eur, 3 get_effective_discount, 4 is_valid_price); all 14 pass |
| `app/config.py` | YML config settings | VERIFIED | `YML_OUTPUT_DIR = os.path.join(basedir, "instance", "feeds")` and `YML_FILENAME = "labresta-feed.yml"` in DefaultConfig |

### Plan 03-02 Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `app/services/yml_generator.py` | YML generation from confirmed matches | VERIFIED | 150 lines, substantive; exports `regenerate_yml_feed`; queries DB with joinedload, builds lxml XML with offers, writes atomically; imports all three pricing functions |
| `app/views/feed.py` | Public feed endpoint | VERIFIED | 17 lines; exports `feed_bp`; route `/feed/yml`; `mimetype="application/xml"`; no auth decorator; `send_from_directory` + 404 fallback |
| `app/services/sync_pipeline.py` | YML regeneration wired after matching stage | VERIFIED | Stage 6/6 present at lines 115-125; lazy import of `regenerate_yml_feed` inside function; runs after Stage 5 matching, before `sync_run.status = "success"` |
| `app/__init__.py` | Blueprint registration | VERIFIED | `from app.views.feed import feed_bp` at line 28; `app.register_blueprint(feed_bp)` at line 33 |

### Plan 03-03 Artifacts (Gap Closure — YML URL)

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `app/models/catalog.py` | page_url column on PromProduct | VERIFIED | `page_url = db.Column(db.String(500), nullable=True)` at line 17; placed between `currency` and `imported_at` |
| `app/services/catalog_import.py` | URL column alias mapping | VERIFIED | `"посилання_на_сторінку_товару": "page_url"` and `"ссылка_на_страницу_товара": "page_url"` in COLUMN_ALIASES lines 40-41; `page_url` persisted on both create and update paths in `save_catalog_products` |
| `app/services/yml_generator.py` | `<url>` element in each offer | VERIFIED | `if pp.page_url: etree.SubElement(offer, "url").text = pp.page_url` at lines 93-94; positioned between `<name>` and `<price>` |
| `app/services/yml_test_generator.py` | `<url>` element in test offers | VERIFIED | `if p.page_url: etree.SubElement(offer, "url").text = p.page_url` at lines 46-47 |

### Plan 03-04 Artifacts (Gap Closure — Matcher Price Gate)

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `app/services/matcher.py` | Price plausibility gate | VERIFIED | `MAX_PRICE_RATIO = 3.0` constant at line 31; `supplier_price_cents: int | None = None` parameter added to `find_match_candidates` (backward compatible); Step 5 post-filter at lines 129-148; `"price": p.price` in prom_list construction line 186; `supplier_price_cents=sp.price_cents` passed at call site line 201 |
| `tests/test_matcher_price_gate.py` | Price plausibility test coverage | VERIFIED | 92 lines, 7 test cases in `TestPricePlausibility` class; covers rejection, acceptance, 3x boundary, no-supplier-price skip, no-prom-price skip, and original UAT bug scenario; all 7 pass |

---

## Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `app/services/yml_generator.py` | `app/services/pricing.py` | `from app.services.pricing import calculate_price_eur, get_effective_discount, is_valid_price` | WIRED | Import at lines 22-26; all three functions called in `regenerate_yml_feed` body (lines 73, 77, 81) |
| `app/services/yml_generator.py` | `app/models/product_match.py` | `ProductMatch.status == "confirmed"` query | WIRED | `.where(ProductMatch.status == "confirmed")` at line 40; joinedload on `supplier_product` and `prom_product` at lines 42-45 |
| `app/services/sync_pipeline.py` | `app/services/yml_generator.py` | Lazy import + call after matching stage | WIRED | `from app.services.yml_generator import regenerate_yml_feed` at line 117; `yml_result = regenerate_yml_feed()` at line 119; confirmed inside try block (Stage 6/6) |
| `app/__init__.py` | `app/views/feed.py` | Blueprint registration | WIRED | `from app.views.feed import feed_bp` at line 28; `app.register_blueprint(feed_bp)` at line 33; no url_prefix — `/feed/yml` resolves to `feed.serve_yml` |
| `app/services/pricing.py` | `app/models/product_match.py` | `discount_percent` column used in YML generation | WIRED | `ProductMatch.discount_percent` nullable Float column exists; `yml_generator` passes `match.discount_percent` to `get_effective_discount` at line 77 |
| `app/services/catalog_import.py` | `app/models/catalog.py` | `page_url` field stored during upsert | WIRED | `page_url = product.get("page_url", "").strip() or None` at line 254; `existing.page_url = page_url` at line 267 (update path); `page_url=page_url` in PromProduct constructor at line 278 (create path) |
| `app/services/yml_generator.py` | `app/models/catalog.py` | `pp.page_url` read during offer generation | WIRED | `if pp.page_url:` at line 93; `etree.SubElement(offer, "url").text = pp.page_url` at line 94; `prom_product` loaded via joinedload at line 45 |
| `app/services/matcher.py` | `app/models/supplier_product.py` | `sp.price_cents` passed to price gate | WIRED | `supplier_price_cents=sp.price_cents` at line 201 in `run_matching_for_supplier`; `SupplierProduct.price_cents` column exists and is queried |
| `app/services/matcher.py` | `app/models/catalog.py` | `p.price` in prom_list for plausibility check | WIRED | `{"id": p.id, "name": p.name, "brand": p.brand, "price": p.price}` at line 186; `prom_price = p.get("price")` in Step 5 gate at line 137 |

---

## Requirements Coverage

| Requirement | Source Plan(s) | Description | Status | Evidence |
|-------------|---------------|-------------|--------|---------|
| PRICE-01 | 03-01 | Admin configures supplier-level discount % | SATISFIED | `Supplier.discount_percent` consumed by `get_effective_discount(match.discount_percent, supplier.discount_percent)` in yml_generator.py line 77 |
| PRICE-02 | 03-01 | Per-product discount override | SATISFIED | `ProductMatch.discount_percent` nullable Float column; `get_effective_discount` returns product override when not None (test_product_override passes) |
| PRICE-03 | 03-01, 03-04 | Final price = retail × (1 − discount%), priority per-product; implausible matches rejected | SATISFIED | `calculate_price_eur` + `get_effective_discount` compose correctly; 14 pricing tests verify all edge cases; price gate (03-04) additionally prevents grossly mismatched prices entering confirmed matches |
| PRICE-04 | 03-01 | Prices stored as integer cents | SATISFIED | `retail_price_cents: int` input; `round()` at discount boundary; `(cents + 50) // 100` for EUR conversion; return type confirmed `int` |
| FEED-01 | 03-02, 03-03, 03-04 | YML compatible with prom.ua and Horoshop (name, price, availability, article, url) | SATISFIED | `<name>` (prom product name), `<url>` (pp.page_url, conditional), `<price>` (whole EUR), `available=` attr, `<vendorCode>` (conditional on article); `yml_catalog` root with `shops.dtd` DOCTYPE; price gate ensures only plausible matches enter confirmed state |
| FEED-02 | 03-02 | YML accessible at public URL | SATISFIED | `/feed/yml` registered without auth; `send_from_directory` serving; `mimetype="application/xml"`; blueprint registered in `__init__.py` |
| FEED-03 | 03-02 | YML updates only matched products | SATISFIED | `.where(ProductMatch.status == "confirmed")` — only confirmed matches appear in output |
| FEED-04 | 03-02 | YML format not prom.ua-specific; Horoshop-compatible | SATISFIED | Uses standard Yandex Market Language (`yml_catalog` / `shops.dtd`); no prom.ua-specific elements; `<url>` element is standard YML |

All 8 requirements satisfied. No orphaned requirements detected.

REQUIREMENTS.md traceability table lists FEED-01, FEED-02, FEED-03, FEED-04, PRICE-01, PRICE-02, PRICE-03, PRICE-04 all as Phase 3 / Complete — consistent with plan declarations.

---

## Commits Verified

| Hash | Message | Files |
|------|---------|-------|
| `58ccecc` | feat(03-01): add per-product discount column and YML config | `app/config.py`, `app/models/product_match.py` |
| `36ec808` | test(03-01): add failing pricing tests | `tests/test_pricing.py`, `tests/__init__.py` |
| `28da4be` | feat(03-01): implement pricing service | `app/services/pricing.py` |
| `2d6b8bf` | feat(03-02): add YML feed generator and public serving endpoint | `app/services/yml_generator.py`, `app/views/feed.py`, `app/__init__.py` |
| `ae06031` | feat(03-02): wire YML regeneration into sync pipeline as Stage 6 | `app/services/sync_pipeline.py` |
| `8972604` | feat(03-03): add page_url column and import mapping for prom.ua product URLs | `app/models/catalog.py`, `app/services/catalog_import.py` |
| `8841ce9` | feat(03-03): emit url element in YML feed offers | `app/services/yml_generator.py`, `app/services/yml_test_generator.py` |
| `bc258ee` | feat(03-04): add price plausibility gate to fuzzy matcher | `app/services/matcher.py` |
| `de6e9ae` | test(03-04): add price plausibility gate test coverage | `tests/test_matcher_price_gate.py` |

All 9 commits confirmed present in git history.

---

## Anti-Patterns Found

None. Scanned all 10 phase-modified files for TODO/FIXME/PLACEHOLDER/empty returns — clean.

Notable patterns (non-issues):
- Three `# noqa: F401` in `yml_generator.py` for `PromProduct`, `Supplier`, `SupplierProduct` imports — these are legitimately needed for SQLAlchemy `joinedload` to resolve relationships, not dead imports.
- `# noqa: E712` in `sync_pipeline.py` and `matcher.py` for SQLAlchemy `== True` / `== False` comparisons — required for SQLAlchemy filter expressions, not a Python anti-pattern.

---

## Human Verification Required

### 1. YML encoding and url element for Cyrillic product names

**Test:** Run a catalog re-import (to populate page_url for existing products), then run a sync. Open `instance/feeds/labresta-feed.yml` in a browser or text editor.
**Expected:** Cyrillic product names render correctly (UTF-8, not garbled). Each offer that has a product page URL contains a `<url>` element. Products imported before the 03-03 re-import may lack `<url>` until re-imported.
**Why human:** The `<url>` element emission is conditional on `page_url` being populated — a re-import is needed to see the effect in a live environment. Terminal encoding on Windows can mask UTF-8 correctness.

### 2. prom.ua import acceptance

**Test:** Configure prom.ua to poll the `/feed/yml` URL and trigger an import.
**Expected:** prom.ua accepts the feed, updates prices and availability for confirmed matched products. The `<url>` elements are correctly recognized.
**Why human:** Cannot simulate prom.ua's parser in automated tests; requires live external service.

### 3. Atomic write under concurrent requests

**Test:** While a sync is running, issue `GET /feed/yml` repeatedly.
**Expected:** Every response is a complete, valid XML file — never a partial write.
**Why human:** The `tempfile + os.replace` pattern is correct, but concurrent behavior under real load requires human observation.

---

## Gaps Summary

No gaps. All 13 observable truths verified, all 8 requirements satisfied, all 12 artifacts substantive and wired, all 9 key links confirmed connected, all 9 commits present in git history, 21 tests pass (14 pricing + 7 price gate).

**Gap closure complete:** The two UAT failures (missing `<url>` element — test 3; wrong price from bad match — test 4) have been fully addressed:
- UAT test 3 (missing `<url>`): fixed in 03-03 — `page_url` column added to PromProduct, catalog import maps Ukrainian/Russian URL headers, both YML generators emit conditional `<url>` element.
- UAT test 4 (wrong match price): fixed in 03-04 — price plausibility gate rejects candidates where supplier-to-prom price ratio exceeds 3x; the 7.9x oven/tray mismatch from UAT is now explicitly caught by test_rejects_high_ratio.

---

_Verified: 2026-02-28_
_Verifier: Claude (gsd-verifier)_
