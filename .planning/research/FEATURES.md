# Feature Research

**Domain:** Excel/Google Sheets supplier feed support + tech debt cleanup for existing price sync app
**Researched:** 2026-03-01
**Confidence:** HIGH (based on full codebase read + domain knowledge of openpyxl patterns and existing code contracts)

---

> **Scope note:** This file covers v1.1 ONLY. v1.0 features are fully shipped and not repeated here.
> The five v1.1 work items are: Excel parser, MatchRule auto-apply, per-product discount UI,
> notification bell fix (operators), dead code removal.

---

## Feature Landscape

### Table Stakes (Users Expect These)

Features expected in any production-quality Excel supplier integration. Missing these = the Excel
parser is not usable or produces silent incorrect results.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Read .xlsx files | Google Sheets exports .xlsx by default; openpyxl already in stack (`export_service.py`) | LOW | `openpyxl.load_workbook(file_bytes, read_only=True)` — read-only mode is critical for performance on large sheets |
| Header row auto-detection | Supplier sheets do not use row 1 consistently; many have logo/title rows above data | MEDIUM | Scan first 10 rows for a row where the majority of cells look like column labels (non-numeric strings). Fall back to row 1. |
| Column mapping by keyword | Ukrainian/Russian suppliers label columns inconsistently: "Назва", "Наименование", "Товар", "Ціна", "Вартість" | MEDIUM | Fuzzy-match column headers against known keyword sets for name, price, availability. Flag unmapped required columns as parse error. |
| Name column extraction (required) | Every supplier product must have a name — the primary key for fuzzy matching | LOW | Required column. Parse error if absent. Maps to `SupplierProduct.name`. |
| Price column extraction (required) | Price is the core sync data | LOW | Required column. Must handle: float strings ("1234.56"), comma decimals ("1 234,56"), currency symbols stripped. Convert to integer cents. |
| Availability column extraction (optional) | Some sheets have in-stock column; many do not | LOW | Optional. If absent, default all rows to `available=True`. Boolean detection: "+" / "є" / "yes" / "1" / "в наявності" → True. Empty / "0" / "немає" → False. |
| Skip empty rows | Excel sheets often have blank rows between sections | LOW | Skip rows where name cell is blank or whitespace only. |
| Synthetic external_id generation | Excel rows have no `offer id` equivalent (unlike YML `<offer id="...">`) | MEDIUM | Generate deterministic external_id from row content: `sha256(supplier_id + name + brand)[:16]`. This ensures upsert stability across re-imports without requiring article column. |
| Google Sheets export URL support | Next supplier provides Google Sheets link; must convert to download URL | MEDIUM | Detect `docs.google.com/spreadsheets` URL → transform to `/export?format=xlsx`. Existing `fetch_feed_with_retry` handles the actual HTTP fetch. |
| Parse error reporting | Silent parse failures leave supplier with stale/missing data | LOW | Return structured error list: which rows failed and why. Show in flash message and SyncRun log. |
| Feed type detection on Supplier model | System must know whether to call `parse_supplier_feed` (YML) or future `parse_excel_feed` (Excel) | LOW | Add `feed_type` column to `Supplier` model: `"yml"` (default) or `"excel"`. Supplier add/edit form gets a type selector. |

---

### Differentiators (Competitive Advantage)

Features that make Excel parsing robust beyond the minimum viable. Not required for v1.1 to ship,
but the ones most likely to be needed within the first real Excel supplier sync cycle.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Per-supplier column mapping config | Different suppliers use different column names — store the mapping after first setup so re-syncs don't re-detect | MEDIUM | Store as JSON on `Supplier` model: `column_map = {"name": "Назва", "price": "Ціна без ПДВ", "available": null}`. UI shows detected + confirmed mapping. |
| Brand column extraction | If sheet has a brand column, populate `SupplierProduct.brand` for better fuzzy match blocking | LOW | Optional. If present, maps to `SupplierProduct.brand`. If absent, brand stays NULL (matcher falls back to no-brand-filter mode — already supported). |
| Article/SKU column extraction | If sheet has article/SKU, store it for potential exact-match override later | LOW | Optional. Maps to `SupplierProduct.article`. No current consumer, but costs nothing to capture. |
| Multi-sheet workbook support | Some suppliers put products on Sheet 2 or use multiple sheets | MEDIUM | Default: first sheet. Config option to specify sheet name or index. |
| Price "without VAT" handling | Ukrainian B2B suppliers often provide ex-VAT prices; retail price = price * 1.2 | MEDIUM | Optional per-supplier VAT flag. If `include_vat=True`, multiply price by 1.2 before storing. Stored in cents before multiplication. |

---

### Anti-Features (Commonly Requested, Often Problematic)

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| Auto-detect sheet structure with LLM/AI | "Just figure out which columns are name and price" | Adds external API dependency, latency, cost; fails on edge cases silently; keyword matching works for 95% of real supplier sheets | Keyword-based column detection with per-supplier override config |
| Support .xls (old Excel format) | Some older suppliers use .xls | xlrd library needed (not in stack); security concerns (xlrd had CVEs); Google Sheets exports as .xlsx anyway | Tell supplier to export as .xlsx or use Google Sheets link. Document explicitly. |
| CSV support | "Supplier gives CSV" | Encoding hell (cp1251 vs utf-8, semicolon vs comma delimiters) on top of Excel parsing complexity | Defer to v1.2; focus on .xlsx which Google Sheets handles well |
| Real-time sheet polling | "Check for changes every 5 minutes" | Google Sheets rate limits; prom.ua re-imports every 4h anyway; existing scheduler is 4h | Same 4h schedule as YML suppliers. No change needed. |
| Automatic column mapping with no review | Map detected columns without showing operator what was found | Silent misconfiguration produces wrong prices in live store | Always show detected mapping to operator on first sync; require confirmation before storing |

---

### MatchRule Auto-Apply

This is a standalone tech debt item, not Excel-specific.

**Current state:** `MatchRule` rows are created when operator checks "remember" during manual match
(`matches.py:manual_match`). The rule stores `(supplier_product_name_pattern, supplier_brand,
prom_product_id)`. But `run_matching_for_supplier` in `matcher.py` never consults the rules table.
Rules are stored and displayed in the rules UI but produce no behavior.

**Expected behavior in any matching system with a rules engine:** Rules are checked before fuzzy
matching. A product whose name matches a rule is auto-confirmed (bypassing the candidate queue),
not just offered as a candidate.

| Behavior | Why Expected | Complexity | Notes |
|----------|--------------|------------|-------|
| Rule lookup before fuzzy matching | If an exact rule exists, the match is known — no need to queue for review | LOW | In `run_matching_for_supplier`: for each unmatched SupplierProduct, check `MatchRule` where `supplier_product_name_pattern == sp.name` and `supplier_brand == sp.brand` (or brand is NULL). If found and `is_active=True`, create `ProductMatch` with `status="manual"` (auto-confirmed), skip fuzzy step for that product. |
| Rule match creates confirmed ProductMatch | Auto-applied rules produce production-ready matches, not candidates | LOW | Same `status="manual"` as a human-confirmed manual match — goes directly into YML output on next regeneration. |
| Rule match does not overwrite existing confirmed match | If product already has a confirmed/manual match, rule is skipped | LOW | Matches already excluded by the `matched_ids` query at the top of `run_matching_for_supplier`. No extra logic needed. |
| Rule match logged | Operator should be able to see how many matches came from rules vs fuzzy | LOW | Log line: "Rule applied: supplier_product.name -> prom_product_id=%d". Count separately from fuzzy candidates in SyncRun or log output. |

**Implementation location:** `app/services/matcher.py` — `run_matching_for_supplier`. Add rule
lookup loop before the existing fuzzy matching loop. Requires `select(MatchRule).where(...)` query.

---

### Per-Product Discount UI

**Current state:** `ProductMatch.discount_percent` column exists in DB and is respected by the
pricing engine (`pricing.py` presumably checks it). But no UI writes it — the field is always NULL,
so the supplier default always applies.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Discount field in match review UI | Per-product discount is already modeled; the UI just needs an input | LOW | Add inline editable discount field to the match review table row (or match detail). AJAX POST to a new endpoint. |
| Per-product discount endpoint | Write `ProductMatch.discount_percent` | LOW | `PATCH /matches/<id>/discount` — accepts `{"discount_percent": float or null}`. NULL clears the override, restoring supplier default. |
| Discount display in match list | Operator needs to see current effective discount at a glance | LOW | Show "15% (supplier default)" or "22% (override)" in the match row. |
| Discount validation | Prevent nonsense values | LOW | 0.0 to 99.9 range. Reject negative or > 100. |

**Dependency:** Check that `pricing.py` already reads `ProductMatch.discount_percent` and falls back
to `Supplier.discount_percent` when NULL. If not, that's a pricing bug that must be fixed alongside
the UI.

---

### Notification Bell Fix (Operators Get 403)

**Root cause (confirmed from code):**

1. `base.html` renders the bell icon for ALL authenticated users and links it to
   `url_for('settings.notifications')`.
2. `settings.notifications` has `@admin_required` decorator, which aborts with 403 for operators.
3. `notifications.js` is not in `base.html`'s global script block — it's only loaded on pages that
   explicitly include it in `{% block scripts %}`. The badge polling (`updateNavbarBadge()`) only
   runs on those pages.

| Fix | What Changes | Complexity | Notes |
|-----|--------------|------------|-------|
| Operator-accessible notification view | Create `/settings/my-notifications` route without `@admin_required`; operators see only their unread notifications, not rule management | LOW | New route in `settings.py`. Renders a simplified template (no rule CRUD). Bell links to this for operators, to full notifications page for admins. |
| notifications.js globally loaded | Move `notifications.js` include into `base.html` (below `common.js`) | LOW | Badge polling currently only works on pages that load notifications.js. Must be global for the bell to update on all pages. |
| Bell link adapts to role | `base.html` navbar: `href="{{ url_for('settings.my_notifications') if not current_user.is_admin else url_for('settings.notifications') }}"` | LOW | Single template change. |

---

### Dead Code Removal

| File | Why Dead | Risk to Remove | Notes |
|------|----------|----------------|-------|
| `app/services/ftp_upload.py` | FTP upload was an early approach for publishing YML. Replaced by serving directly from Flask (`/feed/yml`). No imports anywhere in codebase. | ZERO | Delete file. No tests reference it. Grep confirms no callers. |
| `app/services/yml_test_generator.py` | Test utility for generating a sample YML with selected products. Never called from production code or CLI. No tests reference it. | ZERO | Delete file. Uses `db.session.query` (legacy style) — another reason to remove rather than maintain. |

---

## Feature Dependencies

```
[Supplier.feed_type column (migration)]
    └──required by──> [Excel parser dispatch in sync_pipeline.py]
                          └──required by──> [parse_excel_feed() service]
                                                └──requires──> [column mapping config]
                                                └──requires──> [synthetic external_id generation]

[Google Sheets URL detection]
    └──feeds into──> [fetch_feed_with_retry() — existing, no change]
                          └──feeds into──> [parse_excel_feed()]

[MatchRule auto-apply in run_matching_for_supplier]
    └──depends on──> [MatchRule model — existing, no change]
    └──produces──> [ProductMatch with status="manual" — existing status, no change]

[ProductMatch.discount_percent UI]
    └──depends on──> [ProductMatch.discount_percent column — existing, no change]
    └──depends on──> [pricing.py reading discount_percent — must verify]

[notifications.js global load in base.html]
    └──required by──> [bell badge polling on all pages]

[operator notification route]
    └──depends on──> [notification_service.get_unread_notifications() — existing, no change]
```

### Dependency Notes

- **Excel parser requires `feed_type` migration first:** The `Supplier` model needs a `feed_type`
  column before the parser dispatch can work. This is a one-line Alembic migration (or `db.create_all` if using auto-create). Must be Phase 1 of the Excel work.

- **MatchRule auto-apply has no external dependencies:** The `MatchRule` model, the `run_matching_for_supplier` function, and the `ProductMatch` statuses are all already in place. This is purely adding a query + loop to `matcher.py`. Lowest-risk change in v1.1.

- **Discount UI depends on pricing engine behavior:** Before adding the UI, verify that
  `pricing.py` applies `ProductMatch.discount_percent` when non-NULL and falls back to
  `Supplier.discount_percent` when NULL. If this is already working (likely, given the column was
  added with intent), the UI is trivial. If not, the pricing logic must be fixed first.

- **Notification bell fix has two independent parts:** Loading `notifications.js` globally and
  creating the operator route are independent changes. Either can ship first.

- **Dead code removal has zero dependencies:** Delete and done. No ordering constraint.

---

## MVP Definition

### Launch With (v1.1)

All five items are the v1.1 MVP. None are optional — they are the explicit goal of the milestone.

- [x] **Excel parser** (`parse_excel_feed` service, `Supplier.feed_type` column, Google Sheets URL
      transform, column mapping, synthetic external_id). MEDIUM complexity overall.
- [x] **MatchRule auto-apply** (add rule lookup to `run_matching_for_supplier`). LOW complexity.
- [x] **Per-product discount UI** (AJAX endpoint + inline input in match review). LOW complexity.
- [x] **Notification bell operator fix** (operator route + global JS load). LOW complexity.
- [x] **Dead code removal** (`ftp_upload.py`, `yml_test_generator.py`). ZERO complexity.

### Add After Validation (v1.1+)

These arise naturally after the first real Excel supplier is connected:

- [ ] **Per-supplier column mapping config (stored JSON)** — Add after first Excel supplier is
      synced and the detected mapping is confirmed correct. Then store it so next sync doesn't
      re-detect.
- [ ] **VAT toggle per supplier** — Add when a supplier provides ex-VAT prices and the operator
      notices prices are wrong.
- [ ] **Multi-sheet config** — Add when a supplier's data is on Sheet 2.

### Future Consideration (v2+)

- [ ] **CSV support** — Encoding complexity. Defer until a supplier explicitly cannot provide XLSX.
- [ ] **Article-based exact matching** — If future suppliers reliably provide article codes, build
      a fast-path that bypasses fuzzy matching entirely.

---

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| Excel parser (core: name + price + avail) | HIGH | MEDIUM | P1 |
| `Supplier.feed_type` DB column | HIGH | LOW | P1 (prereq for parser) |
| Google Sheets URL transform | HIGH | LOW | P1 (needed for real supplier) |
| Synthetic external_id generation | HIGH | LOW | P1 (parser correctness) |
| MatchRule auto-apply | HIGH | LOW | P1 |
| Per-product discount UI | MEDIUM | LOW | P1 |
| Notification bell operator access | MEDIUM | LOW | P1 |
| `notifications.js` global load | LOW | LOW | P1 (2-line change) |
| Dead code removal | LOW | LOW | P1 (no-risk cleanup) |
| Per-supplier column map config (stored) | MEDIUM | MEDIUM | P2 |
| Brand column extraction | MEDIUM | LOW | P2 |
| VAT toggle per supplier | MEDIUM | LOW | P2 |
| Multi-sheet support | LOW | LOW | P2 |
| CSV support | LOW | HIGH | P3 |

**Priority key:**
- P1: Must have for v1.1 launch
- P2: Add when first Excel supplier reveals the need
- P3: Future milestone

---

## Implementation Contracts

These are the precise integration points between v1.1 features and existing v1.0 code. Critical for
roadmap phase planning.

### Excel Parser → Existing Code Interface

The parser must return the same `list[dict]` format as `parse_supplier_feed` so that
`save_supplier_products` (unchanged) can consume it:

```python
# Required output format (matches existing save_supplier_products contract)
{
    "external_id": str,       # synthetic: sha256(f"{supplier_id}:{name}:{brand}")[:16]
    "name": str,              # required, non-empty
    "brand": str | None,      # from brand column if present, else None
    "model": str | None,      # from model column if present, else None
    "article": str | None,    # from article column if present, else None
    "price_cents": int | None, # required; int((float(raw_price)) * 100)
    "currency": str,          # hardcoded "EUR" for now (Ukrainian B2B default)
    "available": bool,        # True if column absent, else parsed boolean
    "supplier_id": int,       # passed in, not from sheet
}
```

### Sync Pipeline → Parser Dispatch

In `sync_pipeline.py`, `_sync_single_supplier` currently calls:
```python
products = parse_supplier_feed(raw_bytes, supplier.id)
```

V1.1 change:
```python
if supplier.feed_type == "excel":
    from app.services.excel_parser import parse_excel_feed
    products = parse_excel_feed(raw_bytes, supplier.id)
else:
    products = parse_supplier_feed(raw_bytes, supplier.id)  # unchanged
```

`raw_bytes` is already fetched by `fetch_feed_with_retry` — no change to the fetch layer. The Excel
parser receives bytes (not a file path) and calls `openpyxl.load_workbook(io.BytesIO(raw_bytes), read_only=True)`.

### MatchRule Auto-Apply → matcher.py Insertion Point

In `run_matching_for_supplier`, after Step 3 (load prom products), before Step 4 (match each):

```python
# NEW: Step 3.5 — Apply remembered match rules first
from app.models.match_rule import MatchRule
active_rules = db.session.execute(
    select(MatchRule).where(MatchRule.is_active == True)
).scalars().all()
rule_map = {
    (r.supplier_product_name_pattern, r.supplier_brand): r.prom_product_id
    for r in active_rules
}

rule_matched_ids = set()
for sp in unmatched_products:
    key = (sp.name, sp.brand)
    if key in rule_map:
        prom_id = rule_map[key]
        existing = db.session.execute(
            select(ProductMatch).where(
                ProductMatch.supplier_product_id == sp.id,
                ProductMatch.prom_product_id == prom_id,
            )
        ).scalar_one_or_none()
        if existing is None:
            match = ProductMatch(
                supplier_product_id=sp.id,
                prom_product_id=prom_id,
                score=100.0,
                status="manual",
                confirmed_at=datetime.now(timezone.utc),
                confirmed_by="rule_engine",
            )
            db.session.add(match)
            total_candidates += 1  # or separate counter
        rule_matched_ids.add(sp.id)

# Existing Step 4 — only for products not handled by rules
for sp in unmatched_products:
    if sp.id in rule_matched_ids:
        continue
    # ... existing fuzzy matching loop unchanged
```

---

## Sources

- Codebase analysis: `app/services/feed_parser.py`, `app/services/matcher.py`,
  `app/models/match_rule.py`, `app/models/product_match.py`, `app/models/supplier.py`,
  `app/services/sync_pipeline.py`, `app/services/export_service.py` (openpyxl usage confirmed),
  `app/views/matches.py`, `app/views/settings.py`, `app/static/js/notifications.js`,
  `app/templates/base.html` — Confidence: HIGH (read directly from codebase)
- openpyxl `load_workbook(read_only=True)` pattern: confirmed in existing `export_service.py`
  which uses `openpyxl.Workbook()` for write — Confidence: HIGH
- Google Sheets export URL pattern: `docs.google.com/spreadsheets/d/{id}/export?format=xlsx` —
  standard Google Sheets public export URL — Confidence: HIGH
- `Supplier.feed_type` gap: confirmed absent from `app/models/supplier.py` — Confidence: HIGH
- `MatchRule` not queried in `matcher.py`: confirmed by reading `run_matching_for_supplier` in
  full — Confidence: HIGH
- `ProductMatch.discount_percent` has no UI endpoint: confirmed by reading all routes in
  `app/views/matches.py` — no discount PATCH endpoint exists — Confidence: HIGH
- Notification 403 for operators: confirmed from `settings.py` `@admin_required` on
  `notifications()` + `base.html` bell linking to that route for all users — Confidence: HIGH
- Dead code confirmed unimported: `ftp_upload.py` and `yml_test_generator.py` have no import
  statements referencing them in any other file — Confidence: HIGH

---
*Feature research for: v1.1 Excel supplier support + tech debt cleanup (LabResta Sync)*
*Researched: 2026-03-01*
