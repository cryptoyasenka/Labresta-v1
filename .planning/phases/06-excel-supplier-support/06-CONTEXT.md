# Phase 6: Excel Supplier Support - Context

**Gathered:** 2026-03-01
**Status:** Ready for planning

<domain>
## Phase Boundary

Operators can add Excel/Google Sheets suppliers and sync their product data through the same pipeline as YML suppliers. The system parses Excel files, matches products by brand+model with context-aware filtering, and feeds price/availability into the existing sync pipeline. The final prom.ua feed uses prom.ua product IDs — supplier IDs/articles are internal only.

</domain>

<decisions>
## Implementation Decisions

### Column Mapping
- Auto-detect columns by keyword matching in headers (3 languages: укр/рус/англ)
- Keywords: назва/название/name, ціна/цена/price, наявність/наличие/available, бренд/brand, модель/model
- Auto-detect header row by scanning first 10 rows for keyword matches
- After auto-detection: show preview page with ~5-10 rows + dropdown per column (Название/Цена/Наявність/Бренд/Модель/Пропустить)
- Operator confirms or adjusts mapping before import proceeds
- If auto-detection fails completely (no columns recognized) — flash error, stop sync
- If operator doesn't find needed columns — they can manually assign via dropdowns
- Confirmed mapping saved as JSON on Supplier model for subsequent syncs

### Required Fields
- Mandatory for parsing: Название (name), Бренд (brand), Модель (model), Ціна (price)
- Optional: Наявність (availability) — if column not found, default all to available=True
- Context-aware matching: brand+model must match, plus context words in name (печь, стол, etc.) to avoid matching spare parts or similar nomenclatures

### Product Identification (external_id)
- external_id = combination of brand+model (stable across row reordering)
- Rows with same brand+model (duplicates) — skip duplicates, log them, show in parse report
- Rows without brand or model — skip silently (these are category headers/brand dividers in supplier files)
- Disappeared products logic: same as YML (2+ syncs without product → available=False, needs_review=True)

### Input Source
- Auto-detect feed type by URL: docs.google.com → Excel, everything else → YML
- No feed_type selector on form — auto-detection handles it
- Google Sheets URL handling:
  - Operator pastes sharing link (e.g., docs.google.com/spreadsheets/d/ID/edit?gid=XXX)
  - System extracts spreadsheet ID and gid parameter
  - Converts to download URL: /export?format=xlsx&gid=XXX
  - If no gid — download first sheet
  - Only public links supported (no Google API auth needed)
- File upload: separate "Upload file" button on supplier page for one-time import
  - File is parsed once, feed_url can remain empty (no auto-sync for file uploads)
- Auto-sync on schedule: Excel suppliers with Google Sheets URL included in APScheduler cycle (same 4h interval as YML)

### Error Handling
- Flash message with summary + details in SyncRun log (same approach as YML)
- Invalid .xlsx file (HTML error page, empty, corrupted) → SyncRun status=error + Telegram notification
- Unparseable price in a row → save product with available=False, log the issue. Operator can manually fix later
- HTTP errors (timeout, 403, 404) → retry 3 times with exponential backoff, then SyncRun error + Telegram
- Sanity check: if >50% of rows have parse errors → stop sync, likely wrong column mapping. SyncRun error + flash

### Pricing
- Supplier retail prices from Excel → stored in SupplierProduct.price_cents
- Supplier.discount_percent applied to all products (existing mechanism)
- Individual per-product discount (ProductMatch.discount_percent) — Phase 7 (PRC-01), not this phase

### Claude's Discretion
- Excel parsing library choice (openpyxl vs xlrd vs other)
- Exact keyword matching algorithm for column auto-detection
- Preview page styling and layout details
- How to store uploaded .xlsx files temporarily during parsing

</decisions>

<specifics>
## Specific Ideas

- Real supplier URL example: `https://docs.google.com/spreadsheets/d/1-4UJcVAUefqV1NuSAGljghvzu-ulXf-A/edit?gid=1075932276#gid=1075932276`
- Supplier files may have category headers / brand name rows mixed with product rows — filter by presence of brand+model
- Matching context: product type words (печь, стол, etc.) prevent false matches with spare parts/accessories with similar model numbers
- Pricing flow: supplier gives retail → system applies Supplier.discount_percent → final price in prom.ua feed

</specifics>

<code_context>
## Existing Code Insights

### Reusable Assets
- `save_supplier_products(products: list[dict])` — format-agnostic upsert, works with any parser that outputs the right dict format
- `fetch_feed_with_retry(url)` — HTTP fetcher with retry, can download .xlsx from Google Sheets
- `Supplier.discount_percent` — already exists on model for supplier-wide discount
- `SupplierProduct` model — external_id, name, brand, model, article, price_cents, currency, available, needs_review
- `_detect_disappeared()` in sync_pipeline.py — works by last_seen_at, format-agnostic

### Established Patterns
- Parser returns `list[dict]` with keys: external_id, name, brand, model, article, price_cents, currency, available, supplier_id
- Sync pipeline: fetch → parse → save → detect_disappeared → matching → YML regeneration
- Error reporting: SyncRun model tracks status, error_message, product counts
- Flash messages for operator feedback (Russian language)
- Telegram notifications for sync failures

### Integration Points
- `Supplier` model: needs `feed_type` field (or auto-detect) + `column_mapping` JSON field for saved mappings
- `sync_pipeline._sync_single_supplier()`: needs branching to call Excel parser instead of YML parser based on feed type
- `suppliers_bp` views: needs file upload endpoint + mapping confirmation page
- `app/templates/suppliers/form.html`: no changes needed if auto-detect by URL
- APScheduler: no changes needed — already syncs all enabled suppliers

</code_context>

<deferred>
## Deferred Ideas

- Individual per-product discount UI (PRC-01) — Phase 7
- Multi-sheet workbook support (EXCEL-07) — v1.2+
- Saved column mapping editing UI (EXCEL-05) — v1.2+
- VAT toggle for suppliers (EXCEL-06) — v1.2+
- CSV support (DATA-01) — v1.2+

</deferred>

---

*Phase: 06-excel-supplier-support*
*Context gathered: 2026-03-01*
