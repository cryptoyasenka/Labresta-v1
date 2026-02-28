# Architecture Research

**Domain:** Excel/Google Sheets supplier feed integration into existing YML price-sync pipeline
**Researched:** 2026-03-01
**Confidence:** HIGH (all findings from direct codebase inspection + verified openpyxl/Google Sheets docs)

---

## Current System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                          Web UI (Flask Blueprints)                   │
│  suppliers_bp   matches_bp   products_bp   dashboard_bp   feed_bp   │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────────┐
│                       sync_pipeline.py                               │
│   Stage 1: fetch_feed_with_retry(url) → raw_bytes                   │
│   Stage 2: parse_supplier_feed(raw_bytes, supplier_id) → [dicts]    │
│   Stage 3: save_supplier_products([dicts]) → stats                  │
│   Stage 4: _detect_disappeared()                                    │
│   Stage 5: run_matching_for_supplier(supplier_id)                   │
│   Stage 6: regenerate_yml_feed()                                    │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────────┐
│              Services Layer                                          │
│  feed_fetcher.py   feed_parser.py   matcher.py   yml_generator.py   │
│  pricing.py        export_service.py catalog_import.py              │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────────┐
│                        SQLite (WAL mode)                             │
│  suppliers  supplier_products  product_matches  match_rules          │
│  prom_products  sync_runs  users  notification_rules  notifications  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Component Responsibilities

| Component | Responsibility | Notes |
|-----------|----------------|-------|
| `feed_fetcher.py` | HTTP download, retry logic, returns `bytes` | Knows nothing about format |
| `feed_parser.py` | YML/XML parse + `save_supplier_products()` upsert | YML-specific, tightly coupled |
| `sync_pipeline.py` | Orchestrates stages 1-6 for each supplier | Currently hardcoded to `parse_supplier_feed()` |
| `matcher.py` | Fuzzy match + brand blocking + price gate | Reads `MatchRule` table — never queries it |
| `catalog_import.py` | Parses prom.ua CSV/XLSX uploads | Has working openpyxl pattern to reference |
| `Supplier` model | `feed_url`, `discount_percent`, `is_enabled` | Missing `feed_type` discriminator column |
| `MatchRule` model | Stored patterns linking supplier name to prom product | Written on manual match, never read by matcher |
| `ProductMatch` model | Match pairs with `status`, `score`, `discount_percent` | `discount_percent` has no UI to set it |

---

## What Needs to Change for Excel Support

### Decision: Separate `excel_parser.py`, not extension of `feed_parser.py`

`feed_parser.py` is YML-specific at every level — it calls `etree.fromstring()`, iterates `<offer>` elements, extracts `<vendor>`, `<model>`, `<vendorCode>`, `<currencyId>`. Excel has no such structure. Adding Excel logic would turn `feed_parser.py` into a branching module that does two unrelated things.

`catalog_import.py` proves a separate file works. It contains a working openpyxl pattern (`parse_xlsx` with `read_only=True`, `iter_rows`, header mapping) that is the direct template for Excel supplier parsing. Copy the pattern, adapt for supplier field names.

**Output contract is identical:** both parsers must return `list[dict]` with keys `{external_id, name, brand, model, article, price_cents, currency, available, supplier_id}`. `save_supplier_products()` already accepts this contract and does not need to change.

---

## Data Flow: Excel Path vs YML Path

### YML Path (current, unchanged)

```
Supplier.feed_url (XML URL)
    |
    v
fetch_feed_with_retry(url) --> raw_bytes (bytes)
    |
    v
parse_supplier_feed(raw_bytes, supplier_id) --> [product dicts]
    |
    v
save_supplier_products([dicts]) --> stats
    |
    v
[stages 4-6 unchanged]
```

### Excel/Google Sheets Path (new)

```
Supplier.feed_url (XLSX URL or Google Sheets export URL)
    |
    v
fetch_feed_with_retry(url) --> raw_bytes (bytes)        [NO CHANGE]
    |
    v
parse_excel_feed(raw_bytes, supplier_id) --> [product dicts]  [NEW]
    |
    v
save_supplier_products([dicts]) --> stats               [NO CHANGE]
    |
    v
[stages 4-6 unchanged]                                  [NO CHANGE]
```

### Google Sheets Export URL Format

Google Sheets can serve XLSX directly via:

```
https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=xlsx
```

This URL returns binary XLSX content over HTTPS. `fetch_feed_with_retry` downloads it as `response.content` (bytes). No special handling needed — the function already returns raw bytes, not decoded text.

`openpyxl.load_workbook(filename=BytesIO(raw_bytes), read_only=True)` accepts bytes wrapped in `BytesIO`. This is a documented, confirmed pattern from openpyxl official docs.

---

## New and Modified Files

### NEW: `app/services/excel_parser.py`

Parses an XLSX byte stream into the same `list[dict]` format that `save_supplier_products()` expects.

```python
"""Excel/XLSX supplier feed parser.

Parses XLSX byte content (from HTTP or Google Sheets export) into
SupplierProduct dicts compatible with save_supplier_products().
"""

import io
from openpyxl import load_workbook

# Column name aliases: supplier Excel headers -> internal field names
# Covers Ukrainian, Russian, and English variants
COLUMN_ALIASES = {
    "назва": "name", "название": "name", "name": "name",
    "ціна": "price", "цена": "price", "price": "price",
    "бренд": "brand", "brand": "brand", "виробник": "brand",
    "модель": "model", "model": "model",
    "артикул": "article", "article": "article",
    "наявність": "available", "наличие": "available", "available": "available",
    "id": "external_id", "код": "external_id", "sku": "external_id",
}

def parse_excel_feed(raw_bytes: bytes, supplier_id: int) -> list[dict]:
    """Parse XLSX bytes into supplier product dicts.

    Args:
        raw_bytes: Raw XLSX file content (from fetch_feed_with_retry).
        supplier_id: ID of the supplier.

    Returns:
        List of dicts compatible with save_supplier_products():
        {external_id, name, brand, model, article,
         price_cents, currency, available, supplier_id}
    """
    wb = load_workbook(filename=io.BytesIO(raw_bytes), read_only=True, data_only=True)
    ws = wb[wb.sheetnames[0]]
    rows = ws.iter_rows(values_only=True)

    try:
        raw_headers = [
            str(h).strip().lower() if h is not None else ""
            for h in next(rows)
        ]
    except StopIteration:
        wb.close()
        return []

    col_map = {}  # col_index -> field_name
    for idx, header in enumerate(raw_headers):
        field = COLUMN_ALIASES.get(header)
        if field and field not in col_map.values():
            col_map[idx] = field

    products = []
    for row_num, row in enumerate(rows, start=2):
        if not row or all(v is None or str(v).strip() == "" for v in row):
            continue

        row_data = {}
        for idx, field in col_map.items():
            val = row[idx] if idx < len(row) else None
            row_data[field] = str(val).strip() if val is not None else ""

        name = row_data.get("name", "")
        if not name:
            continue  # name is required

        # external_id: use provided value or synthesize from row number
        external_id = row_data.get("external_id") or f"row_{row_num}"

        # price: parse to cents; handle comma decimal separator
        price_cents = None
        price_str = row_data.get("price", "")
        if price_str:
            try:
                price_cents = int(float(price_str.replace(",", ".")) * 100)
            except (ValueError, TypeError):
                pass

        # available: empty = True (product listed = available by default)
        avail_str = row_data.get("available", "").lower()
        available = avail_str not in ("false", "0", "нет", "немає", "no")

        products.append({
            "external_id": external_id,
            "name": name,
            "brand": row_data.get("brand") or None,
            "model": row_data.get("model") or None,
            "article": row_data.get("article") or None,
            "price_cents": price_cents,
            "currency": "EUR",
            "available": available,
            "supplier_id": supplier_id,
        })

    wb.close()
    return products
```

Key design choices:
- `data_only=True` ensures cell values are returned, not Excel formulas.
- `row_num`-based fallback `external_id` gives stable keys across re-syncs for ordered supplier sheets without ID columns.
- Comma decimal separator normalized via `.replace(",", ".")` — common in Ukrainian/European Excel exports.
- Available column: empty string resolves to True (product listed = available), consistent with YML parser's `available` attribute default of `"true"`.

---

### MODIFIED: `app/models/supplier.py` — Add `feed_type` column

```python
feed_type = db.Column(
    db.String(20),
    nullable=False,
    default="yml",
    server_default="yml",
)
# Values: "yml" | "excel"
```

There is no Alembic migration system — the project uses `db.create_all()` on startup. `db.create_all()` does NOT alter existing tables, so the column must be added manually for existing databases:

```sql
ALTER TABLE suppliers ADD COLUMN feed_type VARCHAR(20) NOT NULL DEFAULT 'yml';
```

Add this as a one-time CLI migration command in `app/cli.py`, or run manually in production after deploy.

---

### MODIFIED: `app/services/sync_pipeline.py` — Route to correct parser

Single change in `_sync_single_supplier()`, Stage 2. All other stages are format-agnostic and require no changes:

```python
# Stage 2: Parse
logger.info("Stage 2/6: Parsing feed")
if supplier.feed_type == "excel":
    from app.services.excel_parser import parse_excel_feed
    products = parse_excel_feed(raw_bytes, supplier.id)
else:
    products = parse_supplier_feed(raw_bytes, supplier.id)
```

No other changes to `sync_pipeline.py`. Stages 3-6 (save, disappear detection, matching, YML) are all format-agnostic.

---

### MODIFIED: `app/views/suppliers.py` — Add `feed_type` to form handling

The supplier add/edit form needs a `feed_type` selector (dropdown: YML / Excel). Validation must accept `"yml"` and `"excel"`. The quick-fetch button (`supplier_fetch` route) needs identical parser routing to the pipeline:

```python
# In supplier_add and supplier_edit POST handlers:
supplier.feed_type = request.form.get("feed_type", "yml")

# In supplier_fetch route:
if supplier.feed_type == "excel":
    from app.services.excel_parser import parse_excel_feed
    products = parse_excel_feed(raw_bytes, supplier.id)
else:
    products = parse_supplier_feed(raw_bytes, supplier.id)
```

The supplier form template (`suppliers/form.html`) needs a `<select>` for `feed_type` with options `yml` and `excel`.

---

### MODIFIED: `app/services/matcher.py` — Integrate MatchRule into `run_matching_for_supplier`

`MatchRule` is written (in `matches.py` `manual_match()`) but never queried. The model has:
- `supplier_product_name_pattern` — exact name string (stored from `supplier_product.name`)
- `supplier_brand` — optional brand filter
- `prom_product_id` — the forced match target
- `is_active` — soft delete flag

Integration point: Before fuzzy matching each unmatched supplier product, check if an active `MatchRule` exists whose `supplier_product_name_pattern` matches the product name (case-insensitive exact match, since it was stored from an exact name).

```python
# In run_matching_for_supplier(), before the product loop:

from app.models.match_rule import MatchRule
from datetime import datetime, timezone

# Load all active rules once (avoids N+1 queries)
rules = db.session.execute(
    select(MatchRule).where(MatchRule.is_active == True)
).scalars().all()
rule_lookup = {r.supplier_product_name_pattern.lower(): r for r in rules}

# In the for sp in unmatched_products: loop, before find_match_candidates():

rule = rule_lookup.get(sp.name.lower())

# Brand gate: if rule specifies a brand, it must roughly match
if rule and rule.supplier_brand and sp.brand:
    if fuzz.ratio(rule.supplier_brand.lower(), sp.brand.lower()) < BRAND_MATCH_THRESHOLD:
        rule = None  # Brand mismatch, fall through to fuzzy

if rule:
    existing = db.session.execute(
        select(ProductMatch).where(
            ProductMatch.supplier_product_id == sp.id,
            ProductMatch.prom_product_id == rule.prom_product_id,
        )
    ).scalar_one_or_none()
    if existing is None:
        match = ProductMatch(
            supplier_product_id=sp.id,
            prom_product_id=rule.prom_product_id,
            score=100.0,
            status="confirmed",          # Human-verified fact, skip review queue
            confirmed_by="system:match_rule",
            confirmed_at=datetime.now(timezone.utc),
        )
        db.session.add(match)
        total_candidates += 1
    continue  # Skip fuzzy for this product

# ... existing fuzzy matching code follows unchanged ...
```

Key decisions for MatchRule integration:
- Load rules once before the loop — avoids N+1 queries.
- Status is `"confirmed"`, not `"candidate"` — a remembered rule is a human-verified fact; it must not go back to the review queue.
- Brand gate reuses existing `BRAND_MATCH_THRESHOLD` constant — consistent with the fuzzy blocking logic already in the module.
- If brand doesn't match, fall through to fuzzy rather than hard-skip — the rule is name-based; brand is an optional safety filter.

---

### MODIFIED: `app/views/products.py` + template — UI for `ProductMatch.discount_percent`

`ProductMatch.discount_percent` is a nullable Float that overrides supplier-level discount. The pricing engine (`pricing.py` `get_effective_discount()`) already consumes it correctly. Only the write path is missing.

Integration: In the supplier product list or match review page, add an inline edit field for `discount_percent` on confirmed/manual matches. No service logic changes needed — just a POST endpoint that sets `match.discount_percent = float(value)` and commits.

---

### TECH DEBT REMOVALS

**`app/services/ftp_upload.py`** — Delete. Not imported anywhere, not registered anywhere. Zero-risk `git rm`.

**`app/services/yml_test_generator.py`** — Delete. Dead code per v1.0 audit. `git rm`.

**`notifications.js` global loading** — Currently only loaded on `/settings/notifications` page via `{% block scripts %}`. The `updateNavbarBadge()` function polls `/settings/api/notifications/unread` every 30 seconds — needed on every page for the navbar bell. Move the `<script>` tag for `notifications.js` into `base.html` after `common.js`. The `DOMContentLoaded` listener guards against missing DOM elements (checks `if (typeSelect)`, `if (notifList)`) — safe to run on pages that don't have those elements.

**Operator notification bell 403** — The bell in `base.html` links unconditionally to `url_for('settings.notifications')`. The settings blueprint has an admin guard, giving operators a 403. Fix: add `{% if current_user.is_admin %}` guard around the bell's `href` to route operators to a dedicated read-only notifications page, or remove the admin guard from the notifications list view (read is safe for operators).

---

## Recommended Project Structure Changes

```
app/
|-- services/
|   |-- feed_fetcher.py         unchanged
|   |-- feed_parser.py          unchanged (YML only)
|   |-- excel_parser.py         NEW: XLSX bytes -> list[dict]
|   |-- sync_pipeline.py        MODIFIED: feed_type routing in Stage 2
|   |-- matcher.py              MODIFIED: MatchRule integration in run_matching_for_supplier
|   |-- catalog_import.py       unchanged
|   |-- export_service.py       unchanged
|   |-- pricing.py              unchanged
|   |-- yml_generator.py        unchanged
|   |-- notification_service.py unchanged
|   |-- telegram_notifier.py    unchanged
|   |-- ftp_upload.py           DELETE
|   `-- yml_test_generator.py   DELETE
|-- models/
|   `-- supplier.py             MODIFIED: add feed_type column
|-- views/
|   |-- suppliers.py            MODIFIED: feed_type form field + parser routing
|   `-- products.py             MODIFIED: discount_percent UI endpoint
|-- templates/
|   |-- base.html               MODIFIED: global notifications.js, bell operator guard
|   `-- suppliers/
|       `-- form.html           MODIFIED: feed_type selector dropdown
`-- static/js/
    `-- notifications.js        unchanged (content only, loading location changes)
```

---

## Architectural Patterns

### Pattern 1: Parser Contract (explicit dispatch over class hierarchy)

All parsers return identical `list[dict]` with the same keys. `save_supplier_products()` is the single consumer. The pipeline dispatches to the right parser via `supplier.feed_type`.

A class hierarchy (`FeedParser` ABC with `YMLParser` and `ExcelParser` subclasses) would be over-engineering for two formats. A single `if supplier.feed_type == "excel":` branch in `_sync_single_supplier()` is readable and explicit. If a third format appears (e.g., CSV supplier feed), the pattern remains: add `excel_parser.py`-style file, extend the `if/elif` in the pipeline.

### Pattern 2: Rule-First, Fuzzy-Fallback Matching

In `run_matching_for_supplier`, check `MatchRule` lookup first. If a rule matches, create a `confirmed` match and skip fuzzy. If no rule matches, fall through to the existing fuzzy pipeline.

This order is mandatory: rules are human-verified certainties. Running fuzzy matching on a product that has a rule wastes CPU and may generate candidate entries that then need to be reviewed — defeating the purpose of the rule entirely.

Lookup strategy: normalize to lowercase before building the dict and before each lookup. Avoids case mismatches between stored rule names and incoming feed names.

### Pattern 3: Bytes-First Feed Download

`fetch_feed_with_retry()` always returns `bytes`, never `str`. Both the XML parser (lxml) and the XLSX parser (openpyxl via `BytesIO`) accept bytes natively. No format-specific download path needed.

This works for Google Sheets because `https://docs.google.com/spreadsheets/d/{ID}/export?format=xlsx` returns binary XLSX over HTTPS. `requests.get(...).content` captures it correctly. The existing fetch function handles this without modification.

---

## Integration Points

### Internal Boundaries

| Boundary | Communication | Change Required |
|----------|---------------|-----------------|
| `feed_fetcher` to `sync_pipeline` | `bytes` return value | None |
| `sync_pipeline` to `excel_parser` | `(bytes, supplier_id)` call | New dispatch branch |
| `excel_parser` to `save_supplier_products` | `list[dict]` contract | Must match exact keys |
| `sync_pipeline` to `matcher` | `run_matching_for_supplier(supplier_id)` | Unchanged call |
| `matcher` to `MatchRule` table | SQLAlchemy query | Currently missing — add before product loop |
| `matches.py` to `MatchRule` table | SQLAlchemy write on manual match | Already works correctly |
| `base.html` to `notifications.js` | `<script>` tag location | Move from block to base |

### External Services

| Service | Integration Pattern | Notes |
|---------|---------------------|-------|
| Google Sheets | HTTP GET to `export?format=xlsx` URL | Returns raw XLSX bytes; sheet must be publicly accessible |
| Supplier XLSX files | HTTP GET to direct file URL | Same pattern as above |

---

## Build Order (dependency-ordered)

1. **Delete dead code** (`ftp_upload.py`, `yml_test_generator.py`) — no dependencies, zero risk. Do first to reduce noise in subsequent diffs.

2. **Fix `notifications.js` global load + bell operator guard** — pure template change, no model or service dependencies. Do early so operators work normally while Excel work proceeds.

3. **Add `Supplier.feed_type` column** — model change required before view and pipeline changes. Add to model with `server_default="yml"` and run `ALTER TABLE` migration for existing databases. Must be done before supplier form UI.

4. **Create `excel_parser.py`** — standalone new file, depends only on openpyxl (already in requirements) and the `list[dict]` output contract. No dependencies on column or UI changes. Write tests against a fixture XLSX file.

5. **Modify `suppliers.py` + supplier form template** — depends on `feed_type` column (step 3) and `excel_parser.py` (step 4). Both the add/edit form and the quick-fetch button need the parser routing.

6. **Modify `sync_pipeline.py`** — depends on `excel_parser.py` (step 4) and `feed_type` column (step 3). This is the automated scheduled sync path.

7. **Integrate `MatchRule` into `matcher.py`** — depends only on existing `MatchRule` model, no new migrations. Independent of the Excel work. Can be done in parallel with steps 4-6.

8. **UI for `ProductMatch.discount_percent`** — UI-only, depends on no new services. Can be done at any point.

Suggested phase grouping:
- Phase A (tech debt): steps 1, 2
- Phase B (Excel pipeline): steps 3, 4, 5, 6
- Phase C (matching + pricing UX): steps 7, 8

---

## Anti-Patterns to Avoid

### Anti-Pattern 1: Extending `feed_parser.py` with Excel branching

**What people do:** Add `if raw_bytes[:4] == b"PK\x03\x04":` (XLSX magic bytes) to `parse_supplier_feed()` and branch internally.

**Why it's wrong:** The function is named `parse_supplier_feed`, its docstring says "YML/XML", its internals use lxml throughout. Adding openpyxl imports and a branching code path conflates two different parsing strategies in one function. It also makes both paths harder to test in isolation.

**Do this instead:** Separate `excel_parser.py` with its own function. Dispatch in `sync_pipeline.py` at the `supplier.feed_type` level — one line of routing code, two separate parsers.

### Anti-Pattern 2: Downloading XLSX to disk before parsing

**What people do:** Save `raw_bytes` to a temp file path, then call `load_workbook(temp_path)`.

**Why it's wrong:** Unnecessary disk I/O. `catalog_import.py` uses a file path because the user upload goes to disk first as a side effect of the upload. For feed sync, the bytes are already in memory from the HTTP response.

**Do this instead:** `load_workbook(filename=io.BytesIO(raw_bytes), read_only=True, data_only=True)` directly in `parse_excel_feed`. No temp file needed.

### Anti-Pattern 3: Creating rule-matched products as `"candidate"` status

**What people do:** Rule-matched products get `status="candidate"` and go to the human review queue.

**Why it's wrong:** The point of a `MatchRule` is that a human already verified this match once and said "remember this." Sending it back to the review queue forces the operator to confirm it again every sync cycle — the rule is useless.

**Do this instead:** `status="confirmed"`, `confirmed_by="system:match_rule"`, `confirmed_at=now`. This ensures the product goes directly to the YML feed on the next sync.

### Anti-Pattern 4: Querying `MatchRule` inside the product loop (N+1)

**What people do:** Inside `for sp in unmatched_products:`, query `MatchRule` once per product.

**Why it's wrong:** 50 unmatched products = 50 rule queries. For 150 products this is minor but still unnecessary. The pattern also makes the relationship between rules and products harder to follow.

**Do this instead:** Load all active rules once before the loop, build a normalized-name dict, do O(1) dict lookup per product.

---

## Scaling Considerations

This is a small-data system: approximately 150 supplier products, approximately 6100 prom.ua products. Scaling is not a current concern. For reference:

| Concern | Current Scale | If supplier grows to 1000+ products |
|---------|---------------|--------------------------------------|
| Excel parse time | Negligible (under 1s for 150 rows) | Still fast — openpyxl `read_only` handles 10k+ rows without issue |
| MatchRule lookup | O(rules) dict build once before loop | O(1) per product after dict build — scales fine |
| Fuzzy matching | ~150 x 6100 with brand blocking | Brand blocking reduces to ~50-200 per product — acceptable to ~5000 supplier products |
| SQLite WAL | Adequate for single-process Flask | Remains adequate — no concurrent write pressure from Excel path |

---

## Sources

- Direct codebase inspection: `app/services/feed_parser.py`, `sync_pipeline.py`, `matcher.py`, `catalog_import.py`, `feed_fetcher.py`
- Direct model inspection: `Supplier`, `MatchRule`, `ProductMatch`, `SupplierProduct`
- openpyxl `load_workbook` from `BytesIO`: confirmed pattern from [openpyxl official docs](https://openpyxl.readthedocs.io/en/stable/api/openpyxl.reader.excel.html) and [Snyk openpyxl advisor](https://snyk.io/advisor/python/openpyxl/functions/openpyxl.load_workbook)
- Google Sheets XLSX export URL format: `https://docs.google.com/spreadsheets/d/{ID}/export?format=xlsx` confirmed from [Highview Apps guide](https://www.highviewapps.com/blog/how-to-create-a-csv-or-excel-direct-download-link-in-google-sheets/) and [spreadsheet.dev](https://spreadsheet.dev/comprehensive-guide-export-google-sheets-to-pdf-excel-csv-apps-script)

---

*Architecture research for: LabResta Sync v1.1 — Excel supplier feed integration + tech debt*
*Researched: 2026-03-01*
