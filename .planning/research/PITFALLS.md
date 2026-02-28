# Pitfalls Research

**Domain:** Adding Excel/Google Sheets supplier support + tech debt fixes to existing YML-based sync pipeline (v1.1)
**Researched:** 2026-03-01
**Confidence:** HIGH — based on direct codebase analysis + verified external sources

---

## Critical Pitfalls

### Pitfall 1: openpyxl Returns None for Formula Cells Unless Excel Cached the Value

**What goes wrong:**
A supplier delivers an Excel file where price cells contain formulas (e.g., `=B2*1.2` or `=ROUND(C5,2)`). `openpyxl` with `data_only=True` returns `None` for those cells unless the file was last saved by Excel with cached computed values. The parser stores `price_cents=None` for all such products, silently marking them as unavailable in the YML feed without any error.

**Why it happens:**
`openpyxl` never evaluates formulas — it only reads the cached value Excel stored at last save time. Files exported fresh from Google Sheets or opened/resaved by LibreOffice often have no cached values in the XLSX binary. The parser receives `None` and proceeds silently.

**How to avoid:**
- Open with `data_only=True` AND validate that the parsed price is not `None` before storing
- Log a warning per-row when price is `None` and count how many rows were skipped
- Reject the entire parse batch if more than 50% of rows have `None` price (same sanity-check pattern already used in `_detect_disappeared`)
- Document in the supplier config UI that "formula-based prices require the file to be saved by Excel, not LibreOffice or exported directly from Sheets"
- Prefer CSV export from Google Sheets (`format=csv`) which always contains final computed values, not formulas

**Warning signs:**
- Parser reports 0 products with valid `price_cents` after adding first Excel supplier
- `available` count in dashboard drops to 0 after Excel sync
- Sync log shows "created: 50, updated: 0" but feed shows no products

**Phase to address:** Excel Parser phase — before integration into `save_supplier_products`

---

### Pitfall 2: Google Sheets Export URL Returns HTML Login Page Despite HTTP 200

**What goes wrong:**
The export URL `https://docs.google.com/spreadsheets/d/{id}/export?format=xlsx` works for sheets shared as "Anyone with the link can view", but there are two failure modes:

1. The sheet is not truly public — returns a 302 redirect to the Google login page. `requests` follows it automatically and returns an HTML body with HTTP 200. `openpyxl` then raises `zipfile.BadZipFile` on what appears to be valid HTTP 200 bytes.
2. The sheet is public but Google returns a 429 or 403 after repeated automated fetches from the same IP. The existing `fetch_feed_with_retry` retries on `HTTPError` but 429 does not always surface as a non-2xx code in this path.

**Why it happens:**
Google's export endpoint is designed for human browser download, not programmatic access. Anonymous requests without a browser `Cookie` can get redirected to a consent page that returns HTTP 200 with an HTML body. `response.raise_for_status()` in `fetch_feed` only checks status code, not content type. The `fetch_feed_with_retry` retry logic handles `HTTPError`, `ConnectionError`, and `Timeout` — it does not handle the silent HTML-body case.

**How to avoid:**
- After fetching, validate that the response is actually XLSX before passing to openpyxl: check `response.headers['Content-Type']` contains `spreadsheet` or `zip`, OR check the first 4 bytes for the XLSX ZIP magic bytes (`PK\x03\x04`)
- Treat content-type mismatch as a fetch error (not a parse error) so it surfaces correctly in sync logs and `SyncRun.error_message`
- Catch 429 explicitly alongside existing retry logic in `fetch_feed_with_retry` or parse `Retry-After` header if present
- Prefer the CSV export variant (`format=csv`) for Google Sheets — it is more stable, lighter, and sidesteps the XLSX MIME ambiguity

**Warning signs:**
- `openpyxl.utils.exceptions.InvalidFileException: File is not a zip file` on a URL that returns HTTP 200
- Sync log shows "error" immediately on first attempt for a new Google Sheets supplier
- `Content-Type` in response is `text/html` instead of `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`

**Phase to address:** Excel Parser phase — validate response content before handing to openpyxl

---

### Pitfall 3: Merged Cells in Excel Cause Silent Row Skipping

**What goes wrong:**
Suppliers format their Excel price lists with merged cells — brand name spanning multiple columns, category headers merged across rows. When iterating `ws.iter_rows()`, a merged cell in a data column returns `None` for all cells except the top-left of the merge. If the supplier merges price or name columns for visual grouping, the parser reads `None` and skips those rows entirely.

**Why it happens:**
In openpyxl, `MergedCell` objects have `value = None` (read-only). Only the top-left cell of a merged range holds the actual value. Row iteration does not automatically propagate the value to remaining cells in the merge — that is Excel's rendering behavior, not the file format's. Additionally, merged cell ranges are not accessible in `read_only=True` mode (openpyxl GitLab issue #540), so if `read_only=True` is used for memory efficiency, merge detection is impossible.

**How to avoid:**
- Load the workbook without `read_only=True` to allow `ws.merged_cells.ranges` access
- Before parsing data rows, iterate `ws.merged_cells.ranges` and propagate the top-left value to all cells in each range
- Add a pre-parse validation step that logs a warning if merged cells are detected in the columns identified as data columns (name, price, availability)
- Document which column layout the parser expects; reject files where column detection fails

**Warning signs:**
- Parser creates significantly fewer products than the Excel file has data rows
- Every N-th product is missing from the parsed list, where N matches the merge span size
- Name or price is `None` for alternating rows

**Phase to address:** Excel Parser phase — handle merge propagation before row iteration

---

### Pitfall 4: Excel Parser Bypasses `save_supplier_products`, Breaking `price_forced` Protection

**What goes wrong:**
`save_supplier_products` in `feed_parser.py` is the single shared save path for all suppliers. It correctly guards the price-lock mechanism:
```python
if not existing.price_forced:
    existing.price_cents = p["price_cents"]
```
If the Excel parser implements its own upsert loop (e.g., a `parse_and_save_excel()` function) instead of routing through `save_supplier_products`, it overwrites `price_cents` even when `price_forced=True`. This silently breaks the ability to lock individual product prices against sync overwrite — a feature already validated in v1.0.

**Why it happens:**
When adding a second parser type, the natural approach is a standalone function that handles parse and save in one place. The `price_forced` guard exists only in `save_supplier_products`, which is easy to overlook when writing a parallel implementation path.

**How to avoid:**
- The Excel parser must produce the same `list[dict]` format as `parse_supplier_feed` and call the SAME `save_supplier_products` function — no separate save path
- The `_sync_single_supplier` pipeline calls `save_supplier_products(products)` at Stage 3. The Excel parser plugs in at Stage 2 (parse), not Stage 3 (save)
- Define `external_id` generation for Excel rows that have no natural ID: use a hash of `(supplier_id, name, brand)` or a dedicated article/code column. Document this choice — it affects upsert deduplication across syncs
- Write a test: `price_forced=True` product is not overwritten after an Excel sync

**Warning signs:**
- After adding Excel supplier, `price_forced=True` products have prices updated by sync
- Supplier list shows updated prices for products an admin had manually locked

**Phase to address:** Excel Parser phase — design shared interface contract before implementing the parser

---

### Pitfall 5: MatchRule Auto-Apply Creates Confirmed Matches Without Human Review

**What goes wrong:**
`MatchRule` stores `supplier_product_name_pattern → prom_product_id` mappings created from manual matches (the "remember" checkbox in the manual match modal). If MatchRule auto-apply is implemented by creating `ProductMatch` with `status='confirmed'` directly, it bypasses the human review step entirely. A rule created for MARESTO will auto-confirm matches for an Excel supplier if product names match the pattern — even if the price plausibility gate would have rejected it, or the match is simply wrong for the new supplier's context.

**Why it happens:**
The intent of MatchRule is "we have seen this before, skip the fuzzy-matching ceremony." The obvious implementation is `status='confirmed'` directly. But the current pipeline invariant is that `run_matching_for_supplier` always produces `status='candidate'` for human review. Auto-applying rules as confirmed breaks this invariant silently.

**How to avoid:**
- MatchRule auto-apply must set `status='confirmed'` ONLY when the price plausibility gate passes (same `MAX_PRICE_RATIO=3.0` check as fuzzy matching in `find_match_candidates`)
- If the price gate fails for a rule match, fall back to `status='candidate'` — do not skip the product or auto-reject it
- Apply rules BEFORE fuzzy matching in `run_matching_for_supplier`; skip fuzzy matching for products that already matched a rule (avoid creating conflicting candidates)
- Log rule applications separately from fuzzy-generated candidates so operators can audit them in the matches UI
- Cross-supplier safety: a rule created for MARESTO must also apply to Excel supplier products with the same name — this is the intended behavior — but verify the rule's `prom_product_id` is still valid (prom product may have been removed from catalog)

**Warning signs:**
- Newly added Excel supplier products appear as `confirmed` without any operator action
- YML feed includes products that were never reviewed in the matches UI
- Dashboard shows 0 pending candidates for a new supplier with 50+ products

**Phase to address:** MatchRule integration phase — define exact auto-apply semantics before implementing

---

### Pitfall 6: Notification Bell Fix Incomplete — JS Global Load Does Not Fix the 403

**What goes wrong:**
There are two separate problems currently:

1. `notifications.js` is loaded ONLY in `settings/notifications.html` (line 245 of that template). The `base.html` bell badge relies on `updateNavbarBadge()` — a function defined in `notifications.js`. On every other page, this function is not defined. The `setInterval(updateNavbarBadge, 30000)` call in `notifications.js` only runs on the settings page. The badge never polls on dashboard, matches, or other pages.

2. The bell `href` in `base.html` links to `url_for('settings.notifications')`, which has `@admin_required`. Operators clicking the bell receive a 403 page.

A fix that only adds `notifications.js` to `base.html` solves problem 1 but not problem 2. Operators still get 403 on click.

**Why it happens:**
The notification bell and the notification settings page were built as a single feature. The bell link was hardcoded to the admin-only settings route. The operator role gap was identified post-v1.0 audit.

**How to avoid:**
- Solve both problems in one atomic change: move `notifications.js` to `base.html` AND change the bell `href` to a route accessible to all authenticated users
- Options for the operator-accessible destination: (a) create a read-only `/notifications/` view in a new or existing blueprint, or (b) make `settings/notifications.html` conditionally show rule management controls only for admins, and remove `@admin_required` from the route (keeping individual rule CRUD endpoints admin-only)
- The `api_notifications_unread` endpoint at `/settings/api/notifications/unread` is already only `@login_required` (not `@admin_required`) — the badge polling will work for operators once `notifications.js` is loaded globally
- The `DOMContentLoaded` handler in `notifications.js` references settings-page DOM elements (`notificationsList`, `markAllReadBtn`) with null guards already present — safe to load globally

**Warning signs:**
- Operator user gets a 403 error page when clicking the notification bell
- Browser console shows `ReferenceError: updateNavbarBadge is not defined` on dashboard or matches pages
- Badge never updates on non-settings pages even when `unread_notification_count > 0` in context processor

**Phase to address:** Tech Debt / UX Fix phase — fix JS global load AND destination URL in one commit

---

### Pitfall 7: Dead Code Removal Breaks `scripts/` CLI Tools That Import It

**What goes wrong:**
`ftp_upload.py` and `yml_test_generator.py` appear unused within the Flask application — no blueprint, scheduler, or service imports them. However, they are imported by maintenance scripts in `scripts/`:
- `scripts/upload_test_yml.py` imports `from app.services.ftp_upload import upload_to_ftp`
- `scripts/generate_test_yml.py` imports `from app.services.yml_test_generator import generate_test_yml`

Deleting the service files without deleting the dependent scripts causes `ImportError` on any invocation of those scripts. Static analysis tools (`vulture`, `autoflake`) scan `app/` only and report these files as dead without seeing the `scripts/` references.

**Why it happens:**
Dead code identification is typically done by scanning the main application package. The `scripts/` directory is outside the Flask app and is easily missed. The service files ARE genuinely dead in application runtime — no blueprint, scheduler, or CLI command references them — but they still live as test utilities accessed from outside the app package.

**How to avoid:**
- Before deleting any file, grep the entire repository (including `scripts/`): `grep -r "ftp_upload\|yml_test_generator" .`
- Delete both the service files AND their corresponding dependent scripts in the same commit
- Alternatively, move both files to `scripts/` if they are genuinely useful for manual operations — honest location, not pretending to be application services
- Run the full test suite after deletion and manually verify that no `ImportError` occurs from any `scripts/` entry point

**Warning signs:**
- `ImportError: cannot import name 'upload_to_ftp' from 'app.services.ftp_upload'` in any log or manual run
- CI/CD pipeline that invokes `scripts/upload_test_yml.py` starts failing after the deletion

**Phase to address:** Tech Debt cleanup phase — grep before delete, remove scripts and services together

---

### Pitfall 8: `discount_percent` UI Allows Values That Silently Remove Products From the Feed

**What goes wrong:**
`ProductMatch.discount_percent` is stored as `Float` and fed directly into `calculate_price_eur`:
```python
discounted_cents = round(retail_price_cents * (100 - discount_percent) / 100)
whole_eur = (discounted_cents + 50) // 100
```
If an operator sets `discount_percent=100.0`, the result is `price_eur=0`. `is_valid_price()` returns `False` for 0, so the product is excluded from the YML feed silently — no error, no warning, just disappears. A value above 100 produces a negative price that is also silently excluded. Neither case shows a validation error to the operator.

The supplier-level `discount_percent` already has validation in `_validate_supplier_form` (0-100 range check). The per-product UI will need its own validation — there is no shared discount validation function to inherit from.

**Why it happens:**
The per-product discount UI is a new field with a new form handler. The existing supplier-level validation is not reused. Without explicit server-side validation on the new endpoint, out-of-range values write to DB and the product silently vanishes from the feed on the next regeneration.

**How to avoid:**
- Define a shared validation rule: `0.0 <= discount_percent <= 99.9` — prevent 100% as it makes price 0 and removes the product from feed without a visible error
- The view handler for `discount_percent` must reject values outside this range with a user-visible HTTP 400 error before writing to DB
- Show a real-time price preview in the UI as the operator types: "Result: 170 EUR (was 200 EUR)" — prevents the "why did my product disappear" support request
- Add a test: setting `discount_percent=100` on a confirmed match causes the product to be absent from regenerated YML

**Warning signs:**
- Product disappears from YML after operator sets an individual discount
- `is_valid_price()` returns `False` for products with confirmed matches and valid supplier prices
- No validation error shown when entering discount >= 100 in the per-product UI

**Phase to address:** `discount_percent` UI phase — validate on write, preview on input

---

## Technical Debt Patterns

Shortcuts that seem reasonable but create long-term problems.

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Separate parse+save function per feed type | Faster to implement each parser independently | `price_forced` guard and other save-layer business rules duplicated; drift over time | Never — always funnel through `save_supplier_products` |
| Using row index as `external_id` for Excel rows | Simple, no ID column needed | Row index shifts if supplier reorders rows — causes phantom deletes + duplicate creates on next sync | Only if supplier guarantees row order is stable (rare) |
| Hardcoding column positions (A=name, B=price) in Excel parser | No config needed for first supplier | Breaks immediately when supplier changes column order or adds a column | Never for production — make column detection configurable per supplier |
| Auto-confirming MatchRule matches unconditionally | Reduces operator review load | Confirmed wrong matches appear in YML feed without human sign-off | Never — always apply price gate, produce candidate if gate fails |
| Loading `notifications.js` only on settings page | Simple, loads only where needed | `updateNavbarBadge()` unavailable on other pages; operator gets 403 on bell click | Only acceptable if bell is hidden for non-admin users (not current behavior) |

---

## Integration Gotchas

Common mistakes when connecting the Excel parser to the existing pipeline.

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| Google Sheets URL | Assume any HTTP 200 is valid Excel bytes; pass response directly to openpyxl | Validate `Content-Type` and magic bytes (`PK\x03\x04`) before passing to openpyxl; treat HTML response as a fetch error |
| `save_supplier_products` | Implement a separate `save_excel_products()` with its own upsert logic | Pass the same `list[dict]` format to the existing `save_supplier_products`; only the parse function differs |
| `external_id` for Excel rows | Skip the field (no offer ID in Excel) | Generate a stable synthetic ID: hash of `(supplier_id, name.strip().lower(), brand.strip().lower())` or use a dedicated Article/Code column if present |
| `_sync_single_supplier` pipeline | Add `if excel_supplier` branch inside the pipeline function | Keep the pipeline generic: detect format before Stage 2 and dispatch to the correct parser; Stage 3+ remain shared |
| MatchRule in `run_matching_for_supplier` | Apply rules after fuzzy matching as a post-filter | Apply rules first; skip fuzzy matching for products with a rule match to avoid creating conflicting candidates |
| Operator notification bell | Move `notifications.js` to `base.html` and call it done | Also change the bell `href` to a role-appropriate destination; create an operator-accessible notification view |

---

## Performance Traps

Patterns that work at small scale but fail as usage grows.

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| Loading full Excel workbook into memory for large files | Memory spike during sync on shared hosting | Use `read_only=True` for streaming row iteration when file > ~5 MB; note that merged cell detection requires non-read-only mode | Files with 1000+ rows or multi-sheet workbooks |
| Iterating all prom products (6100+) inside the MatchRule check loop | Sync slows noticeably as MatchRule table grows | Pre-load MatchRule patterns into a dict keyed by normalized name; O(1) lookup per supplier product | When MatchRule table has 100+ entries and supplier has 200+ products |
| Fetching Google Sheets CSV/XLSX on every scheduled sync without checking for changes | Hits Google rate limits; 429 errors accumulate silently | Check `ETag` or `Last-Modified` headers; skip re-parse if content unchanged | After 10-20 fetches per day from the same IP |
| `check_and_notify` inside sync pipeline blocking on Telegram API when many new products | Telegram rate limiting blocks sync completion; sync appears hung | Batch notifications; make `check_and_notify` async or move it out of the critical sync path | When a supplier batch creates 50+ products matching notification rules |

---

## Security Mistakes

Domain-specific security issues relevant to v1.1 changes.

| Mistake | Risk | Prevention |
|---------|------|------------|
| Storing a Google Sheets URL with an embedded OAuth token or API key in `Supplier.feed_url` | Token exposed in sync logs and UI for all admin users | If Sheets requires auth, store credentials separately in env vars; the `feed_url` field is displayed in the UI |
| Accepting Excel file by URL without validating the response is an actual XLSX | Malformed or malicious content crashes openpyxl or produces incorrect data silently | Validate magic bytes (`PK\x03\x04`) and `Content-Type` header before parsing |
| `discount_percent` form accepts unchecked float from operator input | Negative discount increases price above retail; 100% discount removes product from feed silently | Server-side validation: `0.0 <= value <= 99.9`, reject outside range before DB write |
| Bell link navigates operators to `@admin_required` page | Operators see confusing 403 error; may report as system outage | Separate read-only notification view for operators or conditional `href` based on `current_user.is_admin` |

---

## UX Pitfalls

| Pitfall | User Impact | Better Approach |
|---------|-------------|-----------------|
| No feedback when Excel sync finds 0 valid prices (formula cells) | Operator sees "sync success" but no products in feed; confused | Show warning in sync log: "X rows skipped: price unavailable (formula cell or missing value)" |
| `discount_percent` field has no price preview | Operator sets wrong discount, product disappears from feed; discovers it the next day | Show calculated price inline as operator types: "Result: 170 EUR (was 200 EUR)" |
| MatchRule auto-apply confirms matches without visible attribution | Operator never reviews matches for new Excel supplier; wrong matches enter the feed without audit trail | Show "auto-confirmed by rule: [rule name]" badge in match review UI |
| Bell navigates operator to 403 | Operator thinks the system is broken | Hide bell or link to an operator-accessible notifications view |
| Column mapping hardcoded, Excel supplier adds a column | Parser reads wrong column silently — prices become names or vice versa | Per-supplier column config in UI: "Column A = name, Column C = price, Column D = available" |

---

## "Looks Done But Isn't" Checklist

Things that appear complete but are missing critical pieces.

- [ ] **Excel parser:** Integrated with `save_supplier_products` — verify `price_forced` protection is preserved by running a test with a `price_forced=True` product through an Excel sync
- [ ] **Google Sheets fetch:** Content-type validation in place — verify that an HTML response (login redirect) produces a fetch error in `SyncRun.error_message`, not a silent parse failure
- [ ] **MatchRule auto-apply:** Price gate applied — verify that a rule match with >3x price ratio produces `status='candidate'`, not `status='confirmed'`
- [ ] **Notification bell:** Both JS load and destination URL fixed — verify operator can click bell and see notifications without 403
- [ ] **Dead code removed:** Both service files AND their dependent scripts deleted together — verify no `ImportError` from `scripts/` after deletion
- [ ] **`discount_percent` UI:** Server-side validation rejects values outside 0.0–99.9 — verify that entering 100 returns a validation error, not a silent product absence from feed
- [ ] **Excel `external_id`:** Synthetic ID strategy chosen and documented — verify that re-syncing the same Excel file with a reordered row does not create duplicate `SupplierProduct` records

---

## Recovery Strategies

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| Formula cells produce `price_cents=None` for all Excel products | LOW | Re-export the file as CSV from Google Sheets; re-run sync; no DB corruption |
| Google Sheets returns HTML, openpyxl throws parse error | LOW | Parser fails before reaching DB; check sync log for error; fix sharing settings or URL |
| MatchRule auto-confirmed wrong matches in YML feed | MEDIUM | Query `ProductMatch` where `status='confirmed'` and source was rule (add `confirmed_by='rule:[id]'`); reject each in UI; regenerate feed |
| `price_forced` overwritten by Excel sync | MEDIUM | Find affected rows (`price_forced=True`); restore correct `price_cents` from backup or manual re-entry; re-set `price_forced=True` |
| Dead code deletion broke `scripts/` | LOW | `git revert` the deletion commit; re-delete with scripts included |
| `discount_percent=100` set through UI, product disappeared from feed | LOW | Set `discount_percent=NULL` for the match row; regenerate feed |

---

## Pitfall-to-Phase Mapping

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| Formula cells produce None price | Excel Parser phase | Test: parse XLSX with formula cells; assert skipped rows logged, not silently stored as None |
| Google Sheets HTML redirect masquerades as HTTP 200 | Excel Parser phase | Test: mock `requests.get` returning HTML with status 200; assert FetchError raised, not ParseError |
| Merged cells cause row skipping | Excel Parser phase | Test: parse XLSX with merged brand column; assert correct product count matches data rows |
| `price_forced` bypassed by new parser | Excel Parser phase | Test: Excel sync with `price_forced=True` product; assert `price_cents` unchanged after sync |
| MatchRule auto-confirms without price gate | MatchRule integration phase | Test: rule match with >3x price ratio; assert `status='candidate'`, not `'confirmed'` |
| Notification bell 403 for operators | Tech Debt / UX Fix phase | Manual: log in as operator, click bell, verify page loads without 403 |
| Dead code removal breaks `scripts/` | Tech Debt cleanup phase | After deletion: `python scripts/upload_test_yml.py` must not raise `ImportError` (or script is gone too) |
| `discount_percent` >= 100 silently empties feed | `discount_percent` UI phase | Test: POST `discount_percent=100` to new endpoint; assert 400 validation error returned |

---

## Sources

- Codebase direct analysis: `app/services/feed_parser.py`, `app/services/sync_pipeline.py`, `app/services/matcher.py`, `app/services/pricing.py`, `app/views/settings.py`, `app/views/matches.py`, `app/models/match_rule.py`, `app/models/product_match.py`, `app/static/js/notifications.js`, `app/templates/base.html`, `app/__init__.py`, `scripts/upload_test_yml.py`, `scripts/generate_test_yml.py`
- [openpyxl formula/data_only behavior — official docs](https://openpyxl.readthedocs.io/en/stable/formula.html) (HIGH confidence)
- [openpyxl MergedCell value is read-only — GitLab issue #1333](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1333) (HIGH confidence)
- [openpyxl merged cell ranges inaccessible in read-only mode — GitLab issue #540](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/540) (HIGH confidence)
- [Google Sheets export URL pubhtml XLSX fix 2025](https://gist.github.com/e75ti/89d90dd723d17f4bdbac3327c33f21c7) (MEDIUM confidence — URL format stable, HTML-redirect failure mode observed in community)
- [Google Sheets export URL format and parameters](https://www.highviewapps.com/blog/how-to-create-a-csv-or-excel-direct-download-link-in-google-sheets/) (MEDIUM confidence)
- [Google Sheets API rate limits](https://developers.google.com/workspace/sheets/api/limits) (HIGH confidence — official docs)
- [autoflake side-effect import removal risk](https://github.com/PyCQA/autoflake) (HIGH confidence — documented behavior)
- Script dependency verification: direct `grep -r` of `scripts/` in this repository (HIGH confidence)

---

*Pitfalls research for: LabResta Sync v1.1 — Excel/Google Sheets supplier support + tech debt fixes*
*Researched: 2026-03-01*
