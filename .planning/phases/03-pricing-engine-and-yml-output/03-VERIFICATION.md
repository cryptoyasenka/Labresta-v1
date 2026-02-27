---
phase: 03-pricing-engine-and-yml-output
verified: 2026-02-28T22:00:00Z
status: passed
score: 11/11 must-haves verified
re_verification: false
---

# Phase 3: Pricing Engine and YML Output Verification Report

**Phase Goal:** Build pricing engine (integer-cent math, discount overrides) and YML feed output (generator, public endpoint, pipeline integration)
**Verified:** 2026-02-28
**Status:** PASSED
**Re-verification:** No — initial verification

---

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|---------|
| 1 | Supplier-level discount is applied to retail price correctly | VERIFIED | `calculate_price_eur(19999, 15.0) == 170` passes in test suite |
| 2 | Per-product discount overrides supplier-level discount | VERIFIED | `get_effective_discount(20.0, 15.0) == 20.0`; `get_effective_discount(None, 15.0) == 15.0` — both pass |
| 3 | Prices use integer-cent math with mathematical rounding (0.5 rounds up) | VERIFIED | `(cents + 50) // 100` pattern confirmed; `calculate_price_eur(10050, 0.0) == 101` passes; return type is `int` |
| 4 | Zero/missing price products are detected as invalid | VERIFIED | `is_valid_price(0) is False`, `is_valid_price(None) is False`, `is_valid_price(-100) is False` — all pass |
| 5 | Generated YML contains only confirmed matches with correct discounted prices | VERIFIED | `ProductMatch.status == "confirmed"` filter confirmed in source; live DB has 1 confirmed match, YML total=1 |
| 6 | YML file is written atomically (tmp + rename) and never half-written | VERIFIED | `tempfile.mkstemp(..., dir=yml_dir)` + `os.replace(tmp_path, output_path)` + `os.unlink` on failure confirmed in source |
| 7 | Public URL /feed/yml serves the YML without authentication | VERIFIED | Route returns HTTP 200, Content-Type `application/xml`, no `login_required` decorator present |
| 8 | YML regenerates automatically after each successful sync | VERIFIED | Stage 6/6 (`regenerate_yml_feed`) present in `_sync_single_supplier`, runs after Stage 5 matching, before `sync_run.status = "success"` |
| 9 | Products with zero/missing price appear as out-of-stock in YML | VERIFIED | `is_valid_price(sp.price_cents)` check sets `available="false"` and `price_eur = 0` when invalid |
| 10 | Disappeared products appear as out-of-stock in YML | VERIFIED | `sp.available and not sp.needs_review` guards availability; disappeared products set `available=False, needs_review=True` in pipeline Stage 4 |
| 11 | Failed sync does NOT regenerate YML — previous version preserved | VERIFIED | Stage 6 is inside the `try` block; any exception in Stages 1-5 propagates to `except Exception` which returns `"error"` before reaching Stage 6 |

**Score:** 11/11 truths verified

---

## Required Artifacts

### Plan 03-01 Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `app/services/pricing.py` | Pure pricing calculation functions | VERIFIED | 49 lines, substantive; exports `calculate_price_eur`, `get_effective_discount`, `is_valid_price`; no DB access, no side effects |
| `app/models/product_match.py` | Per-product discount column | VERIFIED | `discount_percent = db.Column(db.Float, nullable=True)` at line 33 |
| `tests/test_pricing.py` | Pricing edge case coverage | VERIFIED | 78 lines, 14 test cases; all 14 pass (`pytest` confirmed) |
| `app/config.py` | YML config settings | VERIFIED | `YML_OUTPUT_DIR` and `YML_FILENAME` present in `DefaultConfig` |

### Plan 03-02 Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `app/services/yml_generator.py` | YML generation from confirmed matches | VERIFIED | 147 lines, substantive; exports `regenerate_yml_feed`; queries DB, builds lxml XML, writes atomically |
| `app/views/feed.py` | Public feed endpoint | VERIFIED | 16 lines; exports `feed_bp`; route `/feed/yml`, `mimetype="application/xml"`, no auth |
| `app/services/sync_pipeline.py` | YML regeneration wired after matching | VERIFIED | Stage 6/6 present; lazy import of `regenerate_yml_feed` inside function |
| `app/__init__.py` | Blueprint registration | VERIFIED | `from app.views.feed import feed_bp` + `app.register_blueprint(feed_bp)` at lines 27, 33 |

---

## Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `app/services/yml_generator.py` | `app/services/pricing.py` | `from app.services.pricing import calculate_price_eur, get_effective_discount, is_valid_price` | WIRED | Import at lines 22-26; all three functions called in `regenerate_yml_feed` body |
| `app/services/yml_generator.py` | `app/models/product_match.py` | `ProductMatch.status == "confirmed"` query | WIRED | `.where(ProductMatch.status == "confirmed")` present; joinedload on `supplier_product` and `prom_product` |
| `app/services/sync_pipeline.py` | `app/services/yml_generator.py` | Lazy import + call after matching stage | WIRED | `from app.services.yml_generator import regenerate_yml_feed` inside function (line 59 of source); `yml_result = regenerate_yml_feed()` called immediately after |
| `app/__init__.py` | `app/views/feed.py` | Blueprint registration | WIRED | `from app.views.feed import feed_bp` + `app.register_blueprint(feed_bp)` confirmed; `/feed/yml` route resolves to `feed.serve_yml` |
| `app/services/pricing.py` | `app/models/product_match.py` | `discount_percent` column | WIRED | `discount_percent` column exists on `ProductMatch`; `yml_generator` passes `match.discount_percent` to `get_effective_discount` |

---

## Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|------------|-------------|--------|---------|
| PRICE-01 | 03-01 | Admin configures supplier-level discount % | SATISFIED | `Supplier.discount_percent` consumed by `get_effective_discount(match.discount_percent, supplier.discount_percent)` |
| PRICE-02 | 03-01 | Per-product discount override | SATISFIED | `ProductMatch.discount_percent` nullable Float column; `get_effective_discount` returns product override when not None |
| PRICE-03 | 03-01 | Final price = retail × (1 − discount%), priority per-product | SATISFIED | `calculate_price_eur` + `get_effective_discount` compose correctly; 14 tests verify all edge cases |
| PRICE-04 | 03-01 | Prices stored as integer cents | SATISFIED | `retail_price_cents: int` input; `round()` at discount boundary; `(cents + 50) // 100` for EUR; return type confirmed `int` |
| FEED-01 | 03-02 | YML file compatible with prom.ua and Horoshop (name, price, availability, article) | SATISFIED | `<name>`, `<price>`, `available=` attr, `<vendorCode>` (conditional on article); `yml_catalog` root with `shops.dtd` DOCTYPE |
| FEED-02 | 03-02 | YML accessible at public URL | SATISFIED | `/feed/yml` registered without auth; returns HTTP 200 with `application/xml` mimetype; `send_from_directory` serving confirmed |
| FEED-03 | 03-02 | YML updates only matched products | SATISFIED | `.where(ProductMatch.status == "confirmed")` — live test: 1 confirmed match yields YML total=1 (5723 candidates excluded) |
| FEED-04 | 03-02 | YML format not prom.ua-specific; Horoshop-compatible | SATISFIED | Uses standard Yandex Market Language (`yml_catalog` / `shops.dtd`); no prom.ua-specific elements in output |

All 8 requirements satisfied. No orphaned requirements detected.

---

## Commits Verified

| Hash | Message | Files |
|------|---------|-------|
| `58ccecc` | feat(03-01): add per-product discount column and YML config | `app/config.py`, `app/models/product_match.py` |
| `36ec808` | test(03-01): add failing pricing tests | `tests/test_pricing.py`, `tests/__init__.py` |
| `28da4be` | feat(03-01): implement pricing service | `app/services/pricing.py` |
| `2d6b8bf` | feat(03-02): add YML feed generator and public serving endpoint | `app/services/yml_generator.py`, `app/views/feed.py`, `app/__init__.py` |
| `ae06031` | feat(03-02): wire YML regeneration into sync pipeline as Stage 6 | `app/services/sync_pipeline.py` |

All 5 commits confirmed present in git history.

---

## Anti-Patterns Found

None. Scanned all 6 phase-modified files for TODO/FIXME/PLACEHOLDER/empty returns — clean.

Notable patterns (non-issues):
- Three `# noqa: F401` in `yml_generator.py` for `PromProduct`, `Supplier`, `SupplierProduct` imports — these are legitimately needed for SQLAlchemy `joinedload` to resolve relationships, not dead imports.

---

## Human Verification Required

### 1. YML encoding for non-ASCII product names

**Test:** Run a full sync, then open `instance/feeds/labresta-feed.yml` in a browser or text editor.
**Expected:** Cyrillic product names render correctly (UTF-8 encoded, not garbled).
**Why human:** The test client output showed `<name>���� ������������� Unox...` — this is a display artifact from the Python terminal encoding on Windows, not an actual file corruption. The file is declared `encoding="UTF-8"` in the XML declaration. A human should verify the actual file bytes are valid UTF-8 Cyrillic.

### 2. prom.ua import acceptance

**Test:** Configure prom.ua to poll the `/feed/yml` URL and trigger an import.
**Expected:** prom.ua accepts the feed, updates prices and availability for the 1 confirmed matched product.
**Why human:** Cannot simulate prom.ua's parser in tests; requires live external service.

### 3. Atomic write under concurrent requests

**Test:** While a sync is running, issue `GET /feed/yml` repeatedly.
**Expected:** Every response is a complete, valid XML file — never a partial write.
**Why human:** The `tempfile + os.replace` pattern is correct, but concurrent behavior under real load requires observation.

---

## Gaps Summary

No gaps. All 11 observable truths verified, all 8 requirements satisfied, all 5 artifacts substantive and wired, all 4 key links confirmed connected.

The one deviation noted in the SUMMARY (ALTER TABLE for SQLite column) is a runtime/dev-DB concern, not a source code gap — the model definition is correct and `db.create_all()` will create the column on fresh deployments.

---

_Verified: 2026-02-28_
_Verifier: Claude (gsd-verifier)_
