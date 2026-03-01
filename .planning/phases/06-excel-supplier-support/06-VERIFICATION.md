---
phase: 06-excel-supplier-support
verified: 2026-03-01T03:15:00Z
status: gaps_found
score: 14/17 must-haves verified
re_verification: false
gaps:
  - truth: "Rows without brand or model are silently skipped (category headers)"
    status: failed
    reason: "Plan 01 truth was deliberately overridden in Plan 02 UAT: brand and model are now optional. The parser only skips rows missing 'name'. Two tests that assert the old skip-no-brand/skip-no-model behavior still fail (2 of 25 tests FAIL)."
    artifacts:
      - path: "app/services/excel_parser.py"
        issue: "parse_excel_products() skips only rows with empty 'name'. Rows with empty brand or empty model are NOT skipped — they get a name-only external_id. This contradicts Plan 01 must_have truth but is consistent with Plan 02 UAT decision."
      - path: "tests/test_excel_parser.py"
        issue: "test_skip_no_brand and test_skip_no_model assert old behavior and FAIL. Tests were never updated after Plan 02 changed the contract."
    missing:
      - "Either update tests to assert new behavior (brand/model optional, row gets name-only external_id) OR reinstate the skip logic and add explicit external_id fallback. The test contract must match the implementation contract."

  - truth: "Supplier list shows 'Настроить колонки' link only for Excel suppliers that have no saved column_mapping"
    status: failed
    reason: "The conditional guard from the plan spec was not implemented. The 'Настроить колонки' button renders unconditionally for every supplier regardless of type or mapping status."
    artifacts:
      - path: "app/templates/suppliers/list.html"
        issue: "Line 92-93: <a href='...supplier_mapping_preview...' class='btn btn-sm btn-warning'>Настроить колонки</a> has no conditional — shown to all suppliers including YML suppliers and already-mapped Excel suppliers. The plan specified: {% if supplier.column_mapping is none and supplier.feed_url and 'docs.google.com/spreadsheets' in supplier.feed_url %}"
    missing:
      - "Wrap the 'Настроить колонки' link in a Jinja2 conditional: only show for suppliers where feed_url contains 'docs.google.com/spreadsheets' AND column_mapping is None (or no feed_url, for file-upload-only suppliers without a mapping)."

  - truth: "REQUIRED_FIELDS_STRICT constant exists in excel_parser.py for relaxed validation"
    status: failed
    reason: "The Plan 02 SUMMARY claims 'Added REQUIRED_FIELDS_STRICT (name+price only) for relaxed validation' but this constant does not exist in excel_parser.py. The strict validation (name+price only) is implemented inline in the view (mapping_required = {name, price}), not as an exported constant."
    artifacts:
      - path: "app/services/excel_parser.py"
        issue: "Only REQUIRED_FIELDS = {'name', 'brand', 'model', 'price'} exists. REQUIRED_FIELDS_STRICT is absent. This is a minor SUMMARY inaccuracy — the strict behavior IS implemented in the view — but the constant is missing from the module interface."
    missing:
      - "Add REQUIRED_FIELDS_STRICT = {'name', 'price'} to excel_parser.py so it is importable and discoverable (low-priority cosmetic fix — functional behavior is correct)."
human_verification:
  - test: "Create Google Sheets supplier end-to-end"
    expected: "Navigate to Add Supplier, enter a public Google Sheets URL, submit — system should redirect to mapping_preview page with auto-detected columns, preview rows visible, dropdowns pre-selected. Confirm mapping, verify flash success with product count, verify products appear in matching queue."
    why_human: "Real network download of Google Sheets .xlsx cannot be verified statically."
  - test: "File upload flow"
    expected: "On supplier list page, click 'Загрузить файл' on any supplier, select an .xlsx file — system should redirect to mapping preview page. Confirm mapping, verify products imported."
    why_human: "Browser file upload interaction cannot be verified statically."
  - test: "Scheduled sync processes Excel supplier"
    expected: "Enable an Excel supplier with saved column_mapping, trigger sync (or wait for schedule) — sync completes with 'success' status, SyncRun log shows products_fetched > 0."
    why_human: "Scheduler execution with real external URL cannot be verified statically."
---

# Phase 6: Excel Supplier Support Verification Report

**Phase Goal:** Operators can add Excel/Google Sheets suppliers and sync their product data through the same pipeline as YML suppliers
**Verified:** 2026-03-01T03:15:00Z
**Status:** gaps_found
**Re-verification:** No — initial verification

## Goal Achievement

### Observable Truths

From ROADMAP.md success criteria and plan must_haves:

| # | Truth | Status | Evidence |
|---|-------|--------|---------|
| 1 | Google Sheets sharing URL is detected and converted to .xlsx download URL | VERIFIED | `is_google_sheets_url()` and `convert_google_sheets_url()` implemented, 4 tests pass |
| 2 | Excel column headers are auto-detected by keyword matching in 3 languages | VERIFIED | `detect_columns()` with COLUMN_KEYWORDS in ukr/rus/eng, 5 tests pass |
| 3 | Excel rows are parsed into list[dict] compatible with save_supplier_products() | VERIFIED | `parse_excel_products()` returns (products, errors) with all required keys; `save_supplier_products` called in supplier_fetch and mapping_confirm |
| 4 | Rows without brand or model are silently skipped (category headers) | FAILED | Parser only skips rows with empty 'name'. Brand/model were made optional in Plan 02 UAT. 2 tests fail. |
| 5 | Duplicate brand+model rows are skipped and logged | VERIFIED | seen_ids set check at line 213; test passes |
| 6 | Unparseable prices result in available=False for that product | VERIFIED | price_error flag sets available=False at line 253; test passes |
| 7 | Downloaded content is validated as .xlsx (PK magic bytes check) | VERIFIED | `validate_xlsx_response()` checks b"PK" header; 3 tests pass |
| 8 | Operator can create a supplier with a Google Sheets URL — auto-redirects to mapping preview | VERIFIED | `supplier_add()` POST detects Google Sheets URL, downloads, calls get_preview_data, stores in session, redirects |
| 9 | Operator can upload an .xlsx file for a supplier | VERIFIED | `supplier_upload` route accepts multipart/form-data .xlsx, calls get_preview_data, redirects to mapping_preview |
| 10 | Operator sees column mapping preview with dropdowns | VERIFIED | `mapping_preview.html` renders per-column `<select>` with FIELD_CHOICES, pre-selected from detected_mapping |
| 11 | Operator confirms mapping — saved to Supplier.column_mapping | VERIFIED | `supplier_mapping_confirm` saves JSON to supplier.column_mapping via db.commit() |
| 12 | Scheduled sync for Excel suppliers downloads .xlsx, parses with saved mapping | VERIFIED | `_sync_single_supplier()` branches on `is_google_sheets_url()`, calls `parse_excel_products` with saved mapping |
| 13 | Sync pipeline skips Excel suppliers without saved column_mapping — logs warning | VERIFIED | Lines 94-100: if not supplier.column_mapping: logs warning, raises ValueError which sets SyncRun status=error |
| 14 | Parse errors reported via flash messages and SyncRun log | VERIFIED | supplier_fetch flashes parse warnings; sync_pipeline logs each error; SyncRun.error_message populated on failure |
| 15 | Sanity check: >50% parse errors aborts sync | VERIFIED | `if len(errors) > len(products): raise ValueError(...)` in sync_pipeline line 137-141 and supplier_fetch line 185-191 |
| 16 | Supplier list shows feed type indicator (Excel/YML/File badge) | VERIFIED | list.html lines 30-36: badge bg-success for spreadsheets, bg-primary for YML, bg-secondary for file-only |
| 17 | Supplier list shows 'Настроить колонки' only for unmapped Excel suppliers | FAILED | Link shown unconditionally for all suppliers — conditional guard from plan spec not implemented |
| 18 | Excel-sourced products appear in matching queue identically to YML-sourced products | VERIFIED | `save_supplier_products()` is format-agnostic; same upsert function used for both paths |

**Score:** 14/17 truths verified (3 gaps)

### Required Artifacts

| Artifact | Provides | Exists | Lines | Status | Notes |
|----------|---------|--------|-------|--------|-------|
| `app/services/excel_parser.py` | Excel parsing service with URL detection, column mapping, product extraction | Yes | 325 | VERIFIED | All 6 required exports present |
| `app/models/supplier.py` | Supplier model with column_mapping JSON field, feed_url nullable | Yes | 24 | VERIFIED | column_mapping=Text nullable=True; feed_url nullable=True |
| `tests/test_excel_parser.py` | 25 tests for URL detection, column detection, product parsing | Yes | 371 | PARTIAL | 23/25 pass; 2 fail (test_skip_no_brand, test_skip_no_model) |
| `app/services/sync_pipeline.py` | Sync pipeline with Excel/YML branching in _sync_single_supplier | Yes | 320 | VERIFIED | Contains `is_google_sheets_url` import and branch |
| `app/views/suppliers.py` | File upload, mapping preview/confirm endpoints | Yes | 397 | VERIFIED | supplier_upload, supplier_mapping_preview, supplier_mapping_confirm all defined |
| `app/templates/suppliers/mapping_preview.html` | Column mapping confirmation page with preview rows and dropdowns | Yes | 150 | VERIFIED | Full form with CSRF, dropdowns, JS validation |
| `app/templates/suppliers/form.html` | Updated form with Google Sheets URL help text, optional feed_url | Yes | 57 | VERIFIED | Help text present, no `required` on feed_url |
| `app/templates/suppliers/list.html` | Feed type badges, upload button, configure columns link | Yes | 106 | PARTIAL | Badges correct; upload button present with CSRF; configure columns link unconditional (should be conditional) |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `app/services/sync_pipeline.py` | `app/services/excel_parser.py` | `from app.services.excel_parser import` | WIRED | Line 15-20: imports is_google_sheets_url, convert_google_sheets_url, parse_excel_products, validate_xlsx_response |
| `app/views/suppliers.py` | `app/services/excel_parser.py` | `from app.services.excel_parser import` | WIRED | Lines 20-27: imports convert_google_sheets_url, get_preview_data, is_google_sheets_url, parse_excel_products, validate_xlsx_response, REQUIRED_FIELDS |
| `app/views/suppliers.py` | `app/services/feed_parser.py` | `save_supplier_products` | WIRED | Line 29: imported; called in supplier_fetch (line 193) and supplier_mapping_confirm (line 361) |
| `app/templates/suppliers/mapping_preview.html` | `app/views/suppliers.py` | POST to `url_for('suppliers.supplier_mapping_confirm', ...)` | WIRED | Line 11: `action="{{ url_for('suppliers.supplier_mapping_confirm', supplier_id=supplier.id) }}"` |
| `app/services/excel_parser.py` | `openpyxl` | `load_workbook(read_only=True)` | WIRED | Lines 175, 288, 294: openpyxl.load_workbook with read_only=True |
| `app/services/excel_parser.py` | `app/services/feed_parser.py` | Same list[dict] output format | WIRED | parse_excel_products returns dicts with: external_id, name, brand, model, article, price_cents, currency, available, supplier_id |

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|------------|-------------|--------|----------|
| EXCEL-01 | 06-02 | Operator can add Excel supplier — Google Sheets URL or upload file | SATISFIED | supplier_add auto-redirects Google Sheets URLs to mapping preview; supplier_upload route accepts .xlsx |
| EXCEL-02 | 06-01, 06-02 | System downloads .xlsx via auto-converted Google Sheets URL | SATISFIED | convert_google_sheets_url() + fetch_feed_with_retry() in sync_pipeline and supplier_add |
| EXCEL-03 | 06-01, 06-02 | System parses Excel: extracts name, price, availability | SATISFIED | parse_excel_products() extracts name/price/available/brand/model; all saved via save_supplier_products |
| EXCEL-04 | 06-01 | Excel parser uses same SupplierProduct model / save_supplier_products | SATISFIED | parse_excel_products output is format-identical to parse_supplier_feed output; same save_supplier_products call |

All 4 requirements mapped to Phase 6 are formally satisfied. No orphaned requirements in REQUIREMENTS.md for Phase 6.

**Note on REQUIREMENTS.md traceability table:** EXCEL-01 is marked in the traceability table as `Phase 6 | Complete` and is declared in the 06-02-PLAN.md requirements field. EXCEL-02, EXCEL-03, EXCEL-04 are declared in 06-01-PLAN.md. Coverage is complete.

### Anti-Patterns Found

| File | Location | Pattern | Severity | Impact |
|------|----------|---------|----------|--------|
| `tests/test_excel_parser.py` | Lines 219-233, 235-249 | Tests assert behavior the implementation deliberately does not have (skip on missing brand/model) | Warning | 2/25 tests FAIL. Test suite reports failure; CI would block. |
| `app/templates/suppliers/list.html` | Line 92-94 | "Настроить колонки" button shown unconditionally for all suppliers | Warning | YML suppliers and already-mapped Excel suppliers see an unnecessary/confusing action button |
| `app/services/excel_parser.py` | Line 31 | REQUIRED_FIELDS = {"name", "brand", "model", "price"} — no REQUIRED_FIELDS_STRICT exported constant | Info | SUMMARY claim is inaccurate; strict check lives inline in view. No external callers affected. |

### Human Verification Required

#### 1. Google Sheets Supplier End-to-End Flow

**Test:** Add a supplier with URL `https://docs.google.com/spreadsheets/d/1-4UJcVAUefqV1NuSAGljghvzu-ulXf-A/edit?gid=1075932276#gid=1075932276`. System should redirect to mapping preview automatically.
**Expected:** Column mapping preview page loads with auto-detected column assignments in dropdowns and 5-10 preview rows visible. After confirming, flash message shows product count.
**Why human:** Real network download of Google Sheets file cannot be verified statically.

#### 2. File Upload Flow

**Test:** On supplier list page, click "Загрузить файл" button on any supplier. Select a real .xlsx file from local disk.
**Expected:** Browser submits form, system redirects to mapping preview page. No 500 errors.
**Why human:** Browser file upload interaction with multipart/form-data cannot be tested statically.

#### 3. Scheduled Sync for Excel Supplier

**Test:** Enable an Excel supplier with a saved column_mapping. Wait for or manually trigger scheduled sync.
**Expected:** SyncRun created with status="success", products_fetched > 0. Products visible in matching queue.
**Why human:** APScheduler execution with real external URL requires live environment.

### Gaps Summary

Three gaps were found, none are goal-blockers at the feature level but one is a CI blocker:

**Gap 1 (CI BLOCKER): 2 failing tests.** `test_skip_no_brand` and `test_skip_no_model` were written for Plan 01 behavior (skip rows without brand or model). Plan 02 UAT deliberately changed this: brand and model are now optional, and rows without them get a name-only external_id. The implementation is correct for real-world use, but the tests were never updated. Fix requires updating the 2 failing tests to assert the new behavior (product count = 2, second product has brand="" and ext_id="category header") — OR explicitly documenting that the Plan 01 truth was superseded.

**Gap 2 (UX): Unconditional "Настроить колонки" button.** The supplier list shows the configure-columns button for every supplier, including YML suppliers that have no column mapping concept. The plan specified a conditional guard (`supplier.column_mapping is none and 'docs.google.com/spreadsheets' in supplier.feed_url`). This is a UX issue — clicking the button for a YML supplier will show an empty/confusing mapping preview or error.

**Gap 3 (Minor/Cosmetic): Missing REQUIRED_FIELDS_STRICT constant.** The Plan 02 SUMMARY claims this was added but it was not. The strict validation logic (name+price only required) exists inline in the view. No functional impact, but the module interface does not match the SUMMARY documentation.

The **phase goal is substantially achieved**: operators CAN add Excel/Google Sheets suppliers and sync through the same pipeline. All 4 requirements are satisfied. The gaps are test maintenance (Gap 1) and UX polish (Gap 2).

---

_Verified: 2026-03-01T03:15:00Z_
_Verifier: Claude (gsd-verifier)_
