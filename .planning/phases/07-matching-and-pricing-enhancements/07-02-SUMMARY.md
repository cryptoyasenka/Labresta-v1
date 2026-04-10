---
phase: "07"
plan: "02"
subsystem: matching-ui
tags: [discount, pricing, ajax, detail-panel]
dependency_graph:
  requires: [07-01]
  provides: [discount-ui, discount-endpoint]
  affects: [review-table, detail-panel, pricing-display]
tech_stack:
  added: []
  patterns: [event-delegation, debounced-autosave, live-preview]
key_files:
  created: []
  modified:
    - app/views/matches.py
    - app/templates/matches/review.html
    - app/static/js/matches.js
decisions:
  - Eager-load supplier relationship via joinedload chain to avoid N+1 queries for discount display
  - Event delegation for dynamically created discount input and clear button
  - Initial price preview shown when detail panel opens (not just on input)
metrics:
  duration: "3 min"
  completed: "2026-04-10"
  tasks_completed: 2
  tasks_total: 2
  files_modified: 3
---

# Phase 7 Plan 2: Per-Product Discount Override UI Summary

Per-product discount input in detail panel with AJAX save, live price preview, and discount column in review table using effective discount logic.

## Task Completion

| Task | Name | Commit | Key Files |
|------|------|--------|-----------|
| 1 | Discount AJAX endpoint + review table column + data attributes | a6a051e | app/views/matches.py, app/templates/matches/review.html |
| 2 | Discount input in detail panel with live price preview | d56a8bc | app/static/js/matches.js |

## Changes Made

### Task 1: Discount AJAX endpoint + review table

**matches.py:**
- Added `POST /matches/<match_id>/discount` endpoint with validation (0-100 range, confirmed/manual status only)
- Accepts `discount_percent` in JSON body; null clears the override
- Added eager-load of `SupplierProduct.supplier` via joinedload chain to avoid N+1 queries

**review.html:**
- Added `data-discount-percent` and `data-supplier-default-discount` attributes to each table row
- Added "Скидка" column header and cells showing effective discount (custom bold, supplier default gray)
- Fixed "Расч. цена" column to use effective discount (custom if set, supplier default otherwise)
- Updated empty-row colspan from 9 to 10

### Task 2: Discount input in detail panel

**matches.js:**
- Discount input section added to `showMatchDetail()` for confirmed/manual matches
- Supplier default discount shown as placeholder in the input
- Live price preview updates on input, shows calculated price with currency
- Debounced auto-save (500ms) via `fetchWithCSRF` POST
- Warning display for unusual values (>50% or exactly 0%)
- Clear button resets discount to NULL, saves immediately, shows supplier default preview
- Input disabled during save to prevent race conditions
- Row data-discount-percent attribute updated after successful save
- Rule indicator badge added for auto-confirmed matches (confirmedBy starts with "rule:")

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Performance] Added eager-load for supplier relationship**
- **Found during:** Task 1
- **Issue:** Template accesses `match.supplier_product.supplier.discount_percent` for every row, causing N+1 queries
- **Fix:** Added `.joinedload(SupplierProduct.supplier)` to the query in `_build_match_query()`
- **Files modified:** app/views/matches.py
- **Commit:** a6a051e

**2. [Rule 2 - UX] Added initial price preview on panel open**
- **Found during:** Task 2
- **Issue:** Price preview only showed after typing; should show immediately when panel opens with existing discount
- **Fix:** Call `updatePricePreview(discountPercent)` at end of `showMatchDetail()` for confirmed/manual matches
- **Files modified:** app/static/js/matches.js
- **Commit:** d56a8bc

## Verification Results

- `python -c "from app.views.matches import matches_bp"` -- Import OK
- Discount endpoint registered in app URL map (verified via `app.url_map.iter_rules()`)
- `node --check app/static/js/matches.js` -- JS syntax OK
- All 74 existing tests pass (pytest)

## Known Stubs

None -- all functionality is fully wired.
