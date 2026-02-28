# Stack Research

**Domain:** Price sync app — Excel/Google Sheets supplier feed support (v1.1 additions)
**Researched:** 2026-03-01
**Confidence:** HIGH

---

## Context: Existing v1.0 Stack (Validated — Do Not Re-research)

These are validated v1.0 dependencies declared in `pyproject.toml`. Do not change unless a specific v1.1 requirement demands it.

| Technology | Version (pyproject.toml) | Role |
|------------|--------------------------|------|
| Flask | >=3.1 | Web framework |
| Flask-SQLAlchemy | >=3.1 | ORM integration |
| SQLAlchemy | >=2.0 | DB layer |
| SQLite (WAL mode) | stdlib | Storage |
| flask-apscheduler | >=1.13.1 | Scheduled sync every 4h |
| lxml | >=5.0 | YML/XML parsing |
| requests | >=2.32 | HTTP feed fetching |
| chardet | >=5.0 | Encoding detection |
| tenacity | >=8.0 | Retry logic with exponential backoff |
| rapidfuzz | >=3.0 | Fuzzy matching (WRatio scorer) |
| openpyxl | >=3.1 | xlsx read/write (already declared) |
| python-dotenv | >=1.0 | Config via .env |
| Flask-Login | >=0.6 | Session auth |
| Flask-WTF | >=1.2 | CSRF + forms |
| alembic | >=1.13 | DB migrations |
| Chart.js | CDN | Dashboard charts |

---

## New Capability: Excel/Google Sheets Supplier Feeds

### No New Packages Required

All libraries needed for Excel + Google Sheets support are already in `pyproject.toml`. The work is integration code only.

### Core Technologies for New Feature

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| openpyxl | >=3.1.5 (tighten from >=3.1) | Parse .xlsx bytes from supplier feeds | Already declared. Current stable is 3.1.5 (released 2025-11-16). Use `load_workbook(BytesIO(raw_bytes), read_only=True, data_only=True)` — streams from in-memory bytes, no temp file needed. `data_only=True` returns computed values for formula cells; without it formula cells return `None`. |
| requests | >=2.32 (existing, no change) | Download Google Sheets as xlsx via public export URL | Already in stack. `fetch_feed_with_retry()` in `feed_fetcher.py` returns raw bytes. No changes needed — Google's export endpoint returns one redirect which requests follows automatically (`allow_redirects=True` is the default). |
| io.BytesIO | stdlib (no install) | Wrap raw bytes as file-like object for openpyxl | No temp file, no disk I/O, no cleanup logic needed. Standard pattern: `load_workbook(filename=BytesIO(raw_bytes))`. |

---

## Google Sheets Public Export URL

**Format (no API key, no OAuth, no google-api-python-client):**

```
https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=xlsx
```

**For a specific tab:**
```
https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=xlsx&gid={SHEET_ID}
```

**Supplier requirement:** Sheet must be shared as "Anyone with the link can view."

**How it flows through existing code:**
1. Operator enters the export URL when adding a supplier (or the UI detects `/edit` and rewrites to `/export?format=xlsx`)
2. `fetch_feed_with_retry(url)` fetches it — Google redirects once to a signed download URL, requests follows automatically
3. Returns raw xlsx bytes
4. New `parse_excel_feed(raw_bytes, supplier_id)` wraps in `BytesIO` and parses with openpyxl
5. Returns same `list[dict]` contract as `parse_supplier_feed()` — `save_supplier_products()` is unchanged

**If supplier provides a sharing link instead of export URL:**
Sharing links look like `https://docs.google.com/spreadsheets/d/{ID}/edit?usp=sharing`. Transform in the settings view before storing:

```python
def normalize_google_sheets_url(url: str) -> str:
    """Convert Google Sheets sharing/edit URL to export URL."""
    import re
    match = re.match(r'https://docs\.google\.com/spreadsheets/d/([^/]+)', url)
    if match:
        sheet_id = match.group(1)
        return f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"
    return url  # not a Google Sheets URL, return as-is
```

**Confidence:** MEDIUM — URL format documented across multiple sources including official Google documentation patterns, stable since at least 2016. If a supplier revokes sharing, the fetch returns 403 which tenacity reraises after 3 attempts and marks `last_fetch_status='error'` — existing error handling covers this correctly.

---

## Integration Points: Existing Code to Extend

| File | Change Required | Rationale |
|------|-----------------|-----------|
| `app/models/supplier.py` | Add `feed_type = db.Column(db.String(20), default='yml')` | Discriminator for parser routing in sync_pipeline. Values: `'yml'` (existing MARESTO) / `'excel'` (new). Requires one Alembic migration. |
| `app/services/feed_parser.py` | Add `parse_excel_feed(raw_bytes, supplier_id) -> list[dict]` | New function alongside existing `parse_supplier_feed()`. Same output contract — `save_supplier_products()` is unchanged. |
| `app/services/sync_pipeline.py` | Branch on `supplier.feed_type` in `_sync_single_supplier()` | Replace `parse_supplier_feed(raw_bytes, supplier.id)` call with a router: `parser = parse_excel_feed if supplier.feed_type == 'excel' else parse_supplier_feed`. |
| `app/views/settings.py` | Add `feed_type` field to supplier add/edit form | Dropdown: "YML feed" / "Excel (Google Sheets)". Also add URL normalization for Google Sheets links. |

### What Does NOT Need to Change

- `feed_fetcher.py` — `fetch_feed_with_retry()` works identically for xlsx URLs
- `save_supplier_products()` — output contract preserved
- `sync_pipeline.py` stages 3-6 — save, matching, YML generation all unchanged
- `matcher.py` — no change for Excel supplier support
- Alembic migration script — add one column to `suppliers` table

---

## Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| openpyxl read_only mode | — | Memory-efficient streaming for large xlsx | Always. Supplier xlsx files are typically small (<1MB) but read_only mode is best practice for ETL reading — workbook opens faster and memory stays near-constant. |
| openpyxl data_only mode | — | Read computed cell values, not formulas | Always. Suppliers share price sheets with formulas. Without `data_only=True`, formula cells return `None` instead of the calculated price. |

---

## Tech Debt Items: No New Stack Required

| Item | What's Needed | Stack Impact |
|------|---------------|--------------|
| Wire `MatchRule` into matcher | Logic change only in `matcher.py` — query `MatchRule` table before starting fuzzy search for a product; if an active rule exists for the name/brand, use its `prom_product_id` directly without fuzzy search | None. `MatchRule` model and table already exist. |
| UI for per-product `discount_percent` | Jinja2 form field in existing product/match view. Column `ProductMatch.discount_percent` (or `SupplierProduct`) already exists in DB — verify which model owns it | None. Pure template + view logic. |
| Fix notification bell for operators | Move `notifications.js` `<script>` tag to `base.html`. Remove role check that causes 403 for operators, or fix endpoint permissions | None. Pure template/JS/blueprint fix. |
| Delete dead code | Remove `ftp_upload.py`, `yml_test_generator.py`. Check imports with grep first. | None. |

---

## Installation

No new packages needed. Only tighten the openpyxl version pin:

```toml
# pyproject.toml — change:
"openpyxl>=3.1",
# to:
"openpyxl>=3.1.5",
```

```bash
# Reinstall to pick up the tightened pin (if venv is already on >=3.1.5, this is a no-op)
pip install "openpyxl>=3.1.5"
```

---

## Alternatives Considered

| Recommended | Alternative | Why Not |
|-------------|-------------|---------|
| openpyxl (already installed) | xlrd | xlrd dropped xlsx support in v2.0 (2020). Reads only legacy .xls (Excel 97-2003 format). Suppliers use modern xlsx. |
| openpyxl (already installed) | pandas | pandas adds ~30MB of dependencies (numpy, etc.) for a task openpyxl handles natively. We need 3-4 columns from 200 rows — no DataFrame operations required. |
| openpyxl (already installed) | calamine / python-calamine | Faster Rust-based reader, but not in stack yet. Not needed — supplier sheets are small. Worth considering if parsing >10MB files in the future. |
| requests export URL (no auth) | google-api-python-client | Requires OAuth2, service account credentials, or API key configuration. The downstream_consumer requirement explicitly states "no Google API client — public link only." |
| requests export URL (no auth) | gspread | Same auth requirement as google-api-python-client. Not needed. |
| BytesIO in-memory | Write xlsx to temp file | Temp files require cleanup logic, file locking on Windows, and disk space management. BytesIO is simpler, faster, and requires zero cleanup. |

---

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| `google-api-python-client` | OAuth/service account required; heavy dependency; not needed for public sheets | requests + public export URL |
| `gspread` | Auth-only library; same problem | requests + public export URL |
| `xlrd` | Dropped xlsx in v2.0; reads .xls only | openpyxl |
| `pandas` | 30MB dep for reading 200 rows; no DataFrame use case here | openpyxl directly |
| Writing xlsx to disk before parsing | Cleanup complexity, Windows file locking | `BytesIO(raw_bytes)` |
| openpyxl without `data_only=True` | Formula cells return `None` — prices will be missing | Always pass `data_only=True` |
| openpyxl without `read_only=True` | Loads entire workbook into memory; unnecessary for read-only ETL | Always pass `read_only=True` for feed parsing |

---

## Stack Patterns by Variant

**If supplier provides a Google Sheets sharing link (not the export URL):**
- Detect in settings view: URL contains `docs.google.com/spreadsheets/d/` + `/edit`
- Transform to export URL before storing in DB: replace `/edit?...` with `/export?format=xlsx`
- Normalize in `settings.py` form validation, not in `feed_fetcher.py` (keep fetcher generic)

**If supplier xlsx has multiple sheets:**
- v1.1 default: use `wb.worksheets[0]` (first sheet)
- If supplier needs a specific tab: store `feed_sheet_name` in `Supplier` model (optional field, `nullable=True`)
- Do not attempt auto-detection — too fragile for v1.1

**If supplier xlsx has variable column layout:**
- v1.1 scope: require a header row with known column names (e.g., "Name", "Price", "Available" or Ukrainian equivalents)
- Detect header row by scanning first 5 rows for price-like content
- Do not attempt schema-free detection — defer to v1.2

**If supplier provides a direct .xlsx URL (not Google Sheets):**
- Identical code path — `fetch_feed_with_retry(url)` + `parse_excel_feed(raw_bytes, supplier_id)`
- No special handling needed; `feed_type='excel'` covers this case too

---

## Version Compatibility

| Package | Compatible With | Notes |
|---------|-----------------|-------|
| openpyxl 3.1.5 | Python >=3.8, project requires >=3.11 | Fully compatible. No breaking changes from >=3.1. |
| openpyxl `read_only=True` | `BytesIO` input | Confirmed: `load_workbook(filename=BytesIO(...), read_only=True)` supported since openpyxl 2.x. |
| openpyxl `data_only=True` | `read_only=True` | These flags are compatible and commonly combined for ETL reading. |
| requests 2.32 | Google Sheets export URL redirects | Redirects followed by default. No configuration needed. |
| alembic 1.13 | SQLAlchemy 2.0 | Required for `Supplier.feed_type` migration. Already in stack. |

---

## Sources

- [openpyxl PyPI page](https://pypi.org/project/openpyxl/) — version 3.1.5, released 2025-11-16 (MEDIUM confidence — from search results)
- [openpyxl Optimised Modes docs](https://openpyxl.readthedocs.io/en/stable/optimized.html) — read_only + data_only flags (HIGH confidence — official docs)
- [openpyxl reader API](https://openpyxl.readthedocs.io/en/stable/api/openpyxl.reader.excel.html) — BytesIO input accepted by `load_workbook` (HIGH confidence — official docs)
- [Google Sheets export URL format](https://www.highviewapps.com/blog/how-to-create-a-csv-or-excel-direct-download-link-in-google-sheets/) — `/export?format=xlsx` without API key (MEDIUM confidence — verified across multiple community sources)
- [Google Sheets URL tricks](https://www.benlcollins.com/spreadsheets/url-tricks-for-google-sheets/) — gid parameter for specific sheet tab (MEDIUM confidence — widely referenced)
- Codebase direct read: `app/services/feed_fetcher.py`, `feed_parser.py`, `sync_pipeline.py`, `models/supplier.py`, `pyproject.toml` — integration points verified (HIGH confidence)

---

*Stack research for: LabResta Sync v1.1 — Excel/Google Sheets supplier feed support*
*Researched: 2026-03-01*
