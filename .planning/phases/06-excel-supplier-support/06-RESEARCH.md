# Phase 6: Excel Supplier Support - Research

**Researched:** 2026-03-01
**Domain:** Excel/Google Sheets parsing, supplier feed pipeline integration
**Confidence:** HIGH

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- Auto-detect columns by keyword matching in headers (3 languages: ukr/rus/eng)
- Keywords: назва/название/name, ціна/цена/price, наявність/наличие/available, бренд/brand, модель/model
- Auto-detect header row by scanning first 10 rows for keyword matches
- After auto-detection: show preview page with ~5-10 rows + dropdown per column (Название/Цена/Наявність/Бренд/Модель/Пропустить)
- Operator confirms or adjusts mapping before import proceeds
- If auto-detection fails completely (no columns recognized) — flash error, stop sync
- Confirmed mapping saved as JSON on Supplier model for subsequent syncs
- Mandatory fields: Название (name), Бренд (brand), Модель (model), Ціна (price)
- Optional: Наявність (availability) — if not found, default all to available=True
- Context-aware matching: brand+model must match, plus context words in name
- external_id = combination of brand+model (stable across row reordering)
- Rows with same brand+model (duplicates) — skip duplicates, log them, show in parse report
- Rows without brand or model — skip silently (category headers/brand dividers)
- Disappeared products logic: same as YML (2+ syncs without product -> available=False, needs_review=True)
- Auto-detect feed type by URL: docs.google.com -> Excel, everything else -> YML
- No feed_type selector on form — auto-detection handles it
- Google Sheets URL: extract spreadsheet ID and gid, convert to /export?format=xlsx&gid=XXX
- If no gid — download first sheet
- Only public links supported (no Google API auth needed)
- File upload: separate "Upload file" button on supplier page for one-time import
- File uploads parsed once, feed_url can remain empty (no auto-sync)
- Auto-sync on schedule: Excel suppliers with Google Sheets URL included in APScheduler cycle (same 4h interval)
- Flash message with summary + details in SyncRun log (same approach as YML)
- Invalid .xlsx file -> SyncRun status=error + Telegram notification
- Unparseable price in a row -> save product with available=False, log the issue
- HTTP errors -> retry 3 times with exponential backoff, then SyncRun error + Telegram
- Sanity check: if >50% of rows have parse errors -> stop sync, likely wrong column mapping
- Supplier retail prices -> stored in SupplierProduct.price_cents
- Supplier.discount_percent applied (existing mechanism)
- Individual per-product discount is Phase 7 (PRC-01), not this phase

### Claude's Discretion
- Excel parsing library choice (openpyxl vs xlrd vs other)
- Exact keyword matching algorithm for column auto-detection
- Preview page styling and layout details
- How to store uploaded .xlsx files temporarily during parsing

### Deferred Ideas (OUT OF SCOPE)
- Individual per-product discount UI (PRC-01) — Phase 7
- Multi-sheet workbook support (EXCEL-07) — v1.2+
- Saved column mapping editing UI (EXCEL-05) — v1.2+
- VAT toggle for suppliers (EXCEL-06) — v1.2+
- CSV support (DATA-01) — v1.2+
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| EXCEL-01 | Operator can add supplier with Excel type via Google Sheets URL or file upload | URL auto-detection pattern, Google Sheets URL conversion, file upload via tempfile + openpyxl, Supplier model `column_mapping` JSON field |
| EXCEL-02 | System downloads Excel file from public Google Sheets URL (auto-convert URL to /export?format=xlsx) | Regex-based URL parsing for spreadsheet ID + gid, existing `fetch_feed_with_retry()` reusable for download |
| EXCEL-03 | System parses Excel: extracts name, price, availability from worksheet columns | openpyxl 3.1.5 (already installed), keyword-based column auto-detection, header row scanning, preview confirmation flow |
| EXCEL-04 | Excel parser uses same SupplierProduct model and `save_supplier_products()` compatibility | Parser outputs `list[dict]` with same keys as YML parser; `save_supplier_products()` is format-agnostic, no changes needed |
</phase_requirements>

## Summary

This phase adds Excel/Google Sheets as an alternative supplier feed format, running through the same sync pipeline as YML feeds. The core work is: (1) a new Excel parser service, (2) Google Sheets URL detection and conversion, (3) a column mapping preview/confirmation UI flow, and (4) branching in the sync pipeline to route Excel suppliers to the new parser.

The project is well-positioned for this work. **openpyxl 3.1.5 is already installed** (in `pyproject.toml` dependencies) and already used by `catalog_import.py` for prom.ua catalog imports. The `save_supplier_products()` function in `feed_parser.py` is completely format-agnostic — it accepts `list[dict]` with standardized keys and handles upsert, `last_seen_at` tracking, and supplier metadata updates. The sync pipeline's `_detect_disappeared()` works by `last_seen_at` timestamps, also format-agnostic. The matcher (`run_matching_for_supplier`) queries by `supplier_id` without caring about feed source. No changes needed to the downstream pipeline.

**Primary recommendation:** Create a new `app/services/excel_parser.py` service with keyword-based column detection and preview data generation. Add a `column_mapping` JSON field to the `Supplier` model. Branch in `_sync_single_supplier()` based on URL auto-detection. Add file upload endpoint and mapping confirmation page to `suppliers_bp`.

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| openpyxl | 3.1.5 (installed) | Parse .xlsx files from Google Sheets | Already in project dependencies, used by `catalog_import.py`. read_only mode for performance. |
| requests + tenacity | installed | Download .xlsx from Google Sheets | `fetch_feed_with_retry()` already handles HTTP with 3 retries + exponential backoff |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| re (stdlib) | - | Parse Google Sheets URLs | Extract spreadsheet ID and gid from sharing URLs |
| tempfile (stdlib) | - | Store uploaded .xlsx temporarily | Same pattern as `catalog_import_upload()` in `catalog.py` |
| json (stdlib) | - | Serialize column mapping | Store/load confirmed mapping on `Supplier.column_mapping` |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| openpyxl | xlrd | xlrd only supports .xls (old format), not .xlsx. openpyxl is already installed and handles .xlsx natively. No reason to switch. |
| openpyxl | pandas | Massive dependency for simple column reads. openpyxl is lighter and already in the project. |

**Installation:** No new dependencies needed. openpyxl 3.1.5 is already installed.

## Architecture Patterns

### Recommended Project Structure
```
app/
├── services/
│   ├── excel_parser.py      # NEW: Excel parsing + column detection + preview
│   ├── feed_parser.py        # EXISTING: YML parser + save_supplier_products (shared)
│   ├── feed_fetcher.py       # EXISTING: reuse fetch_feed_with_retry for .xlsx download
│   └── sync_pipeline.py      # MODIFY: branch on feed type in _sync_single_supplier
├── models/
│   └── supplier.py            # MODIFY: add column_mapping (JSON) field
├── views/
│   └── suppliers.py           # MODIFY: add file upload + mapping confirmation endpoints
├── templates/
│   └── suppliers/
│       ├── form.html          # MODIFY: add file upload button (or keep unchanged if auto-detect)
│       ├── list.html          # MODIFY: show feed type indicator (Excel/YML badge)
│       └── mapping_preview.html  # NEW: column mapping confirmation page
```

### Pattern 1: URL-Based Feed Type Detection
**What:** Auto-detect whether a supplier URL is Google Sheets or YML by checking the domain.
**When to use:** When creating/editing suppliers and when starting sync.
**Example:**
```python
import re

GOOGLE_SHEETS_PATTERN = re.compile(
    r'docs\.google\.com/spreadsheets/d/([a-zA-Z0-9_-]+)'
)

def detect_feed_type(url: str) -> str:
    """Return 'excel' if Google Sheets URL, else 'yml'."""
    if GOOGLE_SHEETS_PATTERN.search(url):
        return "excel"
    return "yml"

def convert_google_sheets_url(url: str) -> str:
    """Convert Google Sheets sharing URL to .xlsx download URL.

    Input:  https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit?gid=SHEET_GID#gid=SHEET_GID
    Output: https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/export?format=xlsx&gid=SHEET_GID
    """
    match = GOOGLE_SHEETS_PATTERN.search(url)
    if not match:
        raise ValueError(f"Not a Google Sheets URL: {url}")

    spreadsheet_id = match.group(1)

    # Extract gid from URL parameters or fragment
    gid_match = re.search(r'gid=(\d+)', url)
    gid_param = f"&gid={gid_match.group(1)}" if gid_match else ""

    return f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=xlsx{gid_param}"
```

### Pattern 2: Keyword-Based Column Auto-Detection
**What:** Scan first 10 rows for header keywords in 3 languages, return detected mapping.
**When to use:** When parsing Excel file for the first time (no saved mapping).
**Example:**
```python
COLUMN_KEYWORDS = {
    "name": ["назва", "название", "name"],
    "price": ["ціна", "цена", "price"],
    "available": ["наявність", "наличие", "available", "в наявності", "в наличии"],
    "brand": ["бренд", "brand", "виробник", "производитель"],
    "model": ["модель", "model"],
}

def detect_columns(ws, max_scan_rows=10):
    """Scan first N rows for keyword matches, return (header_row_idx, column_mapping).

    column_mapping: {col_idx: field_name}
    """
    for row_idx, row in enumerate(ws.iter_rows(max_row=max_scan_rows, values_only=True)):
        mapping = {}
        for col_idx, cell_value in enumerate(row):
            if cell_value is None:
                continue
            cell_lower = str(cell_value).strip().lower()
            for field, keywords in COLUMN_KEYWORDS.items():
                if any(kw in cell_lower for kw in keywords):
                    if field not in mapping.values():
                        mapping[col_idx] = field
                        break

        # Consider it a header row if we found at least name + one more field
        if "name" in mapping.values() and len(mapping) >= 2:
            return row_idx, mapping

    return None, {}
```

### Pattern 3: Two-Phase Parse (Preview + Confirm)
**What:** First pass generates preview data for operator confirmation. Second pass (after confirmation) does full parse.
**When to use:** First sync of an Excel supplier, or when column_mapping is not yet saved.
**Flow:**
1. Operator adds supplier with Google Sheets URL (or uploads file)
2. System downloads/reads Excel, runs column auto-detection
3. System shows preview page: first 5-10 data rows with detected column assignments
4. Operator confirms or adjusts via dropdown selectors
5. Confirmed mapping saved to `Supplier.column_mapping` (JSON)
6. Full parse runs with confirmed mapping, feeds into `save_supplier_products()`
7. Subsequent syncs use saved mapping directly (no preview step)

### Pattern 4: external_id from brand+model
**What:** Generate stable `external_id` from brand+model combination instead of row number.
**When to use:** For all Excel-sourced supplier products.
**Example:**
```python
def generate_external_id(brand: str, model: str) -> str:
    """Generate stable external_id from brand+model.

    Normalized: stripped, lowercased, joined with pipe separator.
    This is stable across row reordering in the spreadsheet.
    """
    b = (brand or "").strip().lower()
    m = (model or "").strip().lower()
    return f"{b}|{m}"
```

### Anti-Patterns to Avoid
- **Row-number-based external_id:** Supplier may reorder rows, insert rows, etc. Using row index as external_id would cause mass "disappeared" products on next sync. Always use brand+model.
- **Parsing without confirmation:** Never auto-import Excel data without operator confirming column mapping. Misdetected columns would silently corrupt data.
- **Pre-decoding .xlsx bytes:** openpyxl reads from file path or file-like object. Do not try to decode raw bytes as text first. Download to temp file, pass path to openpyxl.
- **Loading full workbook into memory:** Always use `read_only=True` for openpyxl when just reading data. This prevents loading the entire workbook DOM into memory.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Excel parsing | Custom XML/ZIP reader | openpyxl (already installed) | .xlsx is a complex ZIP/XML format with styles, shared strings, etc. |
| HTTP retry logic | Custom retry loops | `fetch_feed_with_retry()` (existing) | Already handles 3 retries with exponential backoff via tenacity |
| Product upsert | New save function | `save_supplier_products()` (existing) | Format-agnostic, handles create/update/last_seen_at/supplier metadata |
| Disappeared detection | New disappearance logic | `_detect_disappeared()` (existing) | Works by last_seen_at timestamp, completely format-agnostic |
| URL regex for Google Sheets | Manual string splitting | `re` module with compiled pattern | URL formats have edge cases (fragments, query params, encoding) |

**Key insight:** The existing pipeline is already format-agnostic from `save_supplier_products()` onward. The only new code needed is: (a) Excel-specific parser producing the same `list[dict]` output format, (b) Google Sheets URL detection/conversion, (c) mapping confirmation UI, and (d) a branch in the sync pipeline.

## Common Pitfalls

### Pitfall 1: Google Sheets URL Variations
**What goes wrong:** Google Sheets sharing URLs come in many forms — /edit, /edit#gid=X, /edit?gid=X, /view, /htmlview, with or without fragment hash.
**Why it happens:** Google Sheets URLs have evolved over time and users copy different URL variants.
**How to avoid:** Extract only the spreadsheet ID (always `/d/SPREADSHEET_ID/`) and gid parameter. Construct the download URL from scratch rather than modifying the original URL.
**Warning signs:** Test with the real URL from CONTEXT.md: `https://docs.google.com/spreadsheets/d/1-4UJcVAUefqV1NuSAGljghvzu-ulXf-A/edit?gid=1075932276#gid=1075932276` — note both query param AND fragment have gid.

### Pitfall 2: Non-Public Google Sheets
**What goes wrong:** Download returns HTML error page (Google sign-in page) instead of .xlsx binary.
**Why it happens:** Sheet is not set to "Anyone with the link can view."
**How to avoid:** Check first bytes of response — if starts with `<` or `<!DOCTYPE`, it's HTML not .xlsx. Raise a clear error: "Google Sheet is not shared publicly."
**Warning signs:** Response content-type is text/html instead of application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.

### Pitfall 3: Supplier Files with Category Headers
**What goes wrong:** Rows like "BRAND NAME" or "Печи для пиццы" (category headers) get parsed as products.
**Why it happens:** Supplier Excel files often have brand names or category names as divider rows.
**How to avoid:** Per user decision — rows without brand OR model are skipped silently. This naturally filters category headers which only have text in one column.
**Warning signs:** Large number of products with empty brand/model.

### Pitfall 4: Duplicate brand+model Combinations
**What goes wrong:** Two products from same supplier have identical brand+model (e.g., same oven in different colors).
**Why it happens:** Model number alone may not be unique if supplier sells variants.
**How to avoid:** Per user decision — skip duplicates, log them, show in parse report. First occurrence wins (by row order).
**Warning signs:** Parse report shows high duplicate count. May indicate need for more granular external_id (future enhancement).

### Pitfall 5: openpyxl read_only Mode and Row Access
**What goes wrong:** In read_only mode, you cannot access `ws.max_row` or index rows by number — only forward iteration is possible.
**Why it happens:** read_only mode streams rows lazily from the XML, never builds full row map.
**How to avoid:** Iterate rows sequentially. For preview (first N rows after header), collect into a list during single pass. For header detection (first 10 rows), use `ws.iter_rows(max_row=10)`.
**Warning signs:** `TypeError` or `None` when accessing `ws[row_num]` in read_only mode.

### Pitfall 6: Column Mapping Persistence vs. First-Run Flow
**What goes wrong:** Sync pipeline runs on schedule and fails because no column_mapping is saved yet.
**Why it happens:** Operator added supplier URL but hasn't confirmed mapping via preview page.
**How to avoid:** If `column_mapping` is None/empty for an Excel-type supplier, skip auto-sync and log a warning. Only sync when mapping is confirmed. Alternatively, require mapping confirmation as part of supplier creation flow.
**Warning signs:** Scheduled sync errors for new Excel suppliers before operator visits preview page.

### Pitfall 7: Sanity Check Threshold
**What goes wrong:** >50% parse errors triggers sync abort, but on first sync there are no previous products to compare against.
**Why it happens:** The >50% rule is about parse errors within the current batch, not disappeared products.
**How to avoid:** Count rows with parse errors (missing required fields, unparseable price) vs. total data rows. If error_count / total_rows > 0.5, abort and report. This works even on first sync.
**Warning signs:** First sync always failing because all rows have issues (wrong column mapping).

## Code Examples

### Example 1: Excel Parser Service (core function)
```python
# app/services/excel_parser.py
import logging
import re
import tempfile
import os

import openpyxl

logger = logging.getLogger(__name__)

COLUMN_KEYWORDS = {
    "name": ["назва", "название", "name"],
    "price": ["ціна", "цена", "price"],
    "available": ["наявність", "наличие", "available", "в наявності", "в наличии"],
    "brand": ["бренд", "brand", "виробник", "производитель"],
    "model": ["модель", "model"],
}

REQUIRED_FIELDS = {"name", "brand", "model", "price"}

GOOGLE_SHEETS_PATTERN = re.compile(
    r'docs\.google\.com/spreadsheets/d/([a-zA-Z0-9_-]+)'
)


def is_google_sheets_url(url: str) -> bool:
    return bool(GOOGLE_SHEETS_PATTERN.search(url))


def convert_google_sheets_url(url: str) -> str:
    match = GOOGLE_SHEETS_PATTERN.search(url)
    if not match:
        raise ValueError(f"Not a Google Sheets URL: {url}")
    spreadsheet_id = match.group(1)
    gid_match = re.search(r'gid=(\d+)', url)
    gid_param = f"&gid={gid_match.group(1)}" if gid_match else ""
    return f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=xlsx{gid_param}"


def detect_columns(ws, max_scan_rows=10):
    """Return (header_row_idx, {col_idx: field_name}) or (None, {})."""
    for row_idx, row in enumerate(ws.iter_rows(max_row=max_scan_rows, values_only=True)):
        mapping = {}
        for col_idx, cell in enumerate(row):
            if cell is None:
                continue
            cell_lower = str(cell).strip().lower()
            for field, keywords in COLUMN_KEYWORDS.items():
                if any(kw in cell_lower for kw in keywords):
                    if field not in mapping.values():
                        mapping[col_idx] = field
                        break
        if "name" in mapping.values() and len(mapping) >= 2:
            return row_idx, mapping
    return None, {}


def parse_excel_products(file_path: str, column_mapping: dict,
                         header_row: int, supplier_id: int) -> list[dict]:
    """Parse Excel file using confirmed column mapping.

    Returns list[dict] compatible with save_supplier_products().
    """
    wb = openpyxl.load_workbook(file_path, read_only=True)
    ws = wb[wb.sheetnames[0]]

    products = []
    errors = []
    seen_ids = set()

    for row_idx, row in enumerate(ws.iter_rows(values_only=True)):
        if row_idx <= header_row:
            continue  # Skip header and rows above it

        # Extract values by mapping
        values = {}
        for col_idx_str, field in column_mapping.items():
            col_idx = int(col_idx_str)
            if col_idx < len(row):
                val = row[col_idx]
                values[field] = str(val).strip() if val is not None else ""
            else:
                values[field] = ""

        brand = values.get("brand", "").strip()
        model = values.get("model", "").strip()

        # Skip rows without brand or model (category headers)
        if not brand or not model:
            continue

        # Generate stable external_id
        ext_id = f"{brand.lower()}|{model.lower()}"

        # Skip duplicates
        if ext_id in seen_ids:
            errors.append(f"Row {row_idx+1}: duplicate brand+model '{brand} {model}'")
            continue
        seen_ids.add(ext_id)

        # Parse price
        price_str = values.get("price", "")
        price_cents = None
        if price_str:
            try:
                price_cents = int(float(price_str.replace(",", ".").replace(" ", "")) * 100)
            except (ValueError, TypeError):
                errors.append(f"Row {row_idx+1}: unparseable price '{price_str}'")
                # Per user decision: save with available=False

        # Parse availability
        avail_str = values.get("available", "").strip().lower()
        if avail_str in ("", "да", "так", "yes", "true", "+", "1", "в наявності", "в наличии"):
            available = True
        else:
            available = False

        # If price unparseable, mark unavailable
        if price_cents is None and price_str:
            available = False

        name = values.get("name", "").strip()
        if not name:
            errors.append(f"Row {row_idx+1}: empty name")
            continue

        products.append({
            "external_id": ext_id,
            "name": name,
            "brand": brand,
            "model": model,
            "article": None,
            "price_cents": price_cents,
            "currency": "EUR",
            "available": available,
            "supplier_id": supplier_id,
        })

    wb.close()
    return products
```

### Example 2: Sync Pipeline Branching
```python
# In sync_pipeline.py _sync_single_supplier():

# Stage 2: Parse — branch by feed type
if is_google_sheets_url(supplier.feed_url):
    # Download URL already converted, raw_bytes is .xlsx
    # Save to temp file for openpyxl
    import tempfile, os
    fd, tmp_path = tempfile.mkstemp(suffix=".xlsx")
    try:
        with os.fdopen(fd, 'wb') as f:
            f.write(raw_bytes)

        if supplier.column_mapping:
            mapping = json.loads(supplier.column_mapping)
            products = parse_excel_products(
                tmp_path, mapping["columns"], mapping["header_row"], supplier.id
            )
        else:
            # No mapping yet — cannot auto-sync
            raise ValueError("Column mapping not configured. Please configure via supplier page.")
    finally:
        os.unlink(tmp_path)
else:
    products = parse_supplier_feed(raw_bytes, supplier.id)
```

### Example 3: Google Sheets HTML Detection
```python
def validate_xlsx_response(raw_bytes: bytes) -> None:
    """Check that downloaded content is actually .xlsx, not an HTML error page."""
    # .xlsx files are ZIP archives, starting with PK magic bytes
    if raw_bytes[:2] != b'PK':
        if raw_bytes[:1] == b'<' or b'<!DOCTYPE' in raw_bytes[:100]:
            raise ValueError(
                "Google Sheet is not shared publicly. "
                "Got HTML instead of .xlsx. "
                "Please set sharing to 'Anyone with the link can view'."
            )
        raise ValueError("Downloaded file is not a valid .xlsx (expected ZIP/PK header)")
```

### Example 4: Mapping Preview Data Generation
```python
def get_preview_data(file_path: str, max_rows: int = 10):
    """Generate preview data for mapping confirmation page.

    Returns:
        {
            "header_row": int,
            "detected_mapping": {col_idx: field_name},
            "all_headers": [str, ...],
            "preview_rows": [[str, ...], ...],
            "total_data_rows": int (approximate),
        }
    """
    wb = openpyxl.load_workbook(file_path, read_only=True)
    ws = wb[wb.sheetnames[0]]

    header_row, detected = detect_columns(ws)

    # Re-open to get preview rows (read_only iterator consumed)
    wb.close()
    wb = openpyxl.load_workbook(file_path, read_only=True)
    ws = wb[wb.sheetnames[0]]

    all_rows = []
    for i, row in enumerate(ws.iter_rows(values_only=True)):
        all_rows.append([str(c) if c is not None else "" for c in row])
        if i >= (header_row or 0) + max_rows + 1:
            break

    wb.close()

    headers = all_rows[header_row] if header_row is not None else []
    data_rows = all_rows[header_row + 1:header_row + 1 + max_rows] if header_row is not None else []

    return {
        "header_row": header_row,
        "detected_mapping": detected,
        "all_headers": headers,
        "preview_rows": data_rows,
    }
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| xlrd for .xlsx | openpyxl for .xlsx | xlrd 2.0 (2020) dropped .xlsx support | xlrd only reads .xls now; openpyxl is the standard for .xlsx |
| openpyxl normal mode | openpyxl read_only=True | Available since openpyxl 2.4 | 10x memory reduction for large files; streams rows lazily |

**Deprecated/outdated:**
- xlrd: Version 2.0+ only supports .xls (old Excel format). For .xlsx, openpyxl is the standard.
- Old Google Sheets export URL format (`/pub?output=xlsx`) was deprecated in favor of `/export?format=xlsx`.

## Open Questions

1. **Column mapping on file-upload-only suppliers**
   - What we know: File upload is one-time (no feed_url for auto-sync). Operator uploads file, system needs mapping.
   - What's unclear: Should file upload go through the same preview flow, or should it be simpler since it's one-time?
   - Recommendation: Use the same preview flow. Even for one-time imports, the operator needs to confirm which columns are which. Save mapping anyway in case they upload again.

2. **Availability column value variations**
   - What we know: Ukrainian/Russian suppliers may use various formats: "Так/Ні", "Да/Нет", "+/-", "В наявності/Немає", numeric 1/0.
   - What's unclear: Exact set of positive/negative values to recognize.
   - Recommendation: Treat empty string and known positive values ("да", "так", "yes", "true", "+", "1", "в наявності", "в наличии") as available=True. Everything else (including "нет", "ні", "0", "-") as available=False. If availability column not mapped, default all to True (per user decision).

3. **Temporary file cleanup for scheduled syncs**
   - What we know: Scheduled sync downloads .xlsx to temp file, parses, then deletes.
   - What's unclear: If process crashes between download and cleanup.
   - Recommendation: Use `try/finally` for cleanup (same pattern as `catalog_import_upload`). Temp files in system temp dir are cleaned by OS eventually.

## Integration Points (Codebase-Specific)

### Model Changes
- **`Supplier` model** (`app/models/supplier.py`): Add `column_mapping = db.Column(db.Text, nullable=True)` — stores JSON with `{"header_row": int, "columns": {col_idx_str: field_name}}`. Using `db.Text` (not `db.JSON`) for SQLite compatibility.
- **`Supplier.feed_url`**: Currently `nullable=False`. Needs to become `nullable=True` for file-upload-only suppliers with no URL. Alternatively, store empty string.

### Files to Modify
1. `app/models/supplier.py` — add `column_mapping` field
2. `app/services/sync_pipeline.py` — branch in `_sync_single_supplier()` for Excel vs YML
3. `app/views/suppliers.py` — add file upload endpoint, mapping preview/confirm endpoints
4. `app/templates/suppliers/form.html` — may need help text about Google Sheets URLs
5. `app/templates/suppliers/list.html` — show feed type indicator

### Files to Create
1. `app/services/excel_parser.py` — all Excel parsing logic
2. `app/templates/suppliers/mapping_preview.html` — column mapping confirmation page

### Existing Code Reuse (No Changes Needed)
- `save_supplier_products()` in `feed_parser.py` — format-agnostic upsert
- `fetch_feed_with_retry()` in `feed_fetcher.py` — HTTP download with retry
- `_detect_disappeared()` in `sync_pipeline.py` — works by `last_seen_at`
- `run_matching_for_supplier()` in `matcher.py` — queries by supplier_id
- `regenerate_yml_feed()` in `yml_generator.py` — queries by confirmed ProductMatch
- `notify_sync_failure()` in `telegram_notifier.py` — existing Telegram alerts
- APScheduler config — already syncs all enabled suppliers

### Database Schema
Project uses `db.create_all()` (no Alembic migrations in production). Adding new columns to the `Supplier` model will automatically create them on new databases. For existing database, need an ALTER TABLE or a one-time migration script:
```sql
ALTER TABLE suppliers ADD COLUMN column_mapping TEXT;
```

## Sources

### Primary (HIGH confidence)
- Codebase analysis: `app/services/feed_parser.py` — verified `save_supplier_products()` accepts generic `list[dict]`, format-agnostic
- Codebase analysis: `app/services/catalog_import.py` — openpyxl usage pattern already established in project (read_only mode, row iteration)
- Codebase analysis: `app/services/sync_pipeline.py` — verified pipeline stages are format-agnostic after parse step
- Codebase analysis: `pyproject.toml` — openpyxl >= 3.1 already in dependencies
- Installed: openpyxl 3.1.5 verified via Python import
- Google Sheets export URL format: `/export?format=xlsx&gid=SHEET_GID` is the documented public export endpoint

### Secondary (MEDIUM confidence)
- Google Sheets URL patterns: spreadsheet ID regex `[a-zA-Z0-9_-]+` covers standard Google Docs ID format
- .xlsx PK magic bytes: ZIP format specification (PK = 0x504B) is well-established

### Tertiary (LOW confidence)
- None — all findings verified against codebase or standard specifications

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — openpyxl already installed and used in project, no new dependencies
- Architecture: HIGH — format-agnostic pipeline verified by codebase analysis, clear integration points
- Pitfalls: HIGH — Google Sheets URL handling and column detection are the main risk areas, mitigations documented

**Research date:** 2026-03-01
**Valid until:** 2026-03-31 (stable domain, no fast-moving dependencies)
