---
phase: 01-foundation-and-risk-validation
plan: 02
subsystem: api
tags: [xml, yml, lxml, chardet, encoding, cyrillic, maresto, feed-parsing]

# Dependency graph
requires:
  - phase: 01-foundation-and-risk-validation/01
    provides: "Flask app skeleton, Supplier and SupplierProduct models, supplier CRUD views"
provides:
  - "Feed fetcher service returning raw bytes from supplier URLs"
  - "YML/XML parser with encoding detection (UTF-8/Windows-1251)"
  - "Supplier product upsert pipeline (fetch -> parse -> save)"
  - "Manual feed fetch trigger from supplier list UI"
  - "MARESTO feed schema documented (4,388 offers, no model/vendorCode)"
affects: [02-feed-ingestion-and-matching-engine, 03-pricing-engine-and-yml-output]

# Tech tracking
tech-stack:
  added: [lxml, chardet, requests]
  patterns: [raw-bytes-pipeline, encoding-fallback-chain, upsert-on-conflict]

key-files:
  created:
    - app/services/feed_fetcher.py
    - app/services/feed_parser.py
    - scripts/verify_maresto.py
  modified:
    - app/views/suppliers.py
    - app/templates/suppliers/list.html

key-decisions:
  - "Raw bytes pipeline: feed_fetcher returns response.content (bytes), never .text, to prevent encoding corruption"
  - "Encoding fallback: lxml native XML declaration first, then chardet detection as fallback"
  - "MARESTO schema finding: no model/vendorCode elements in feed -- matching must rely on name + vendor only"
  - "UTF-8 with BOM confirmed as MARESTO encoding -- BOM handled transparently by lxml"

patterns-established:
  - "Raw bytes pipeline: always pass raw bytes between fetch and parse stages, never intermediate string decode"
  - "Encoding detection chain: XML declaration -> chardet -> cp1251 fallback"
  - "Price as cents: float price * 100 cast to int for storage"

requirements-completed: [SUPP-03, SUPP-04]

# Metrics
duration: ~15min
completed: 2026-02-26
---

# Phase 1 Plan 2: MARESTO Feed Verification Summary

**YML feed fetcher and XML parser with encoding detection, verified against live MARESTO feed (4,388 offers, Cyrillic preserved through full pipeline)**

## Performance

- **Duration:** ~15 min (includes checkpoint wait)
- **Started:** 2026-02-26
- **Completed:** 2026-02-26
- **Tasks:** 3 (2 auto + 1 checkpoint)
- **Files modified:** 6

## Accomplishments
- Feed fetcher service fetches raw bytes from any supplier URL with timeout and error handling
- XML parser extracts all offer fields with dual encoding detection (lxml native + chardet fallback)
- Live MARESTO feed verified: 4,388 offers, UTF-8 with BOM, Cyrillic names preserved through SQLite round-trip
- MARESTO schema documented: no model or vendorCode elements exist (impacts future matching strategy)
- Manual "Fetch Feed" button on supplier list page triggers full fetch-parse-save pipeline

## Task Commits

Each task was committed atomically:

1. **Task 1: Implement feed fetcher and XML parser services** - `1a518f4` (feat)
2. **Task 2: Create MARESTO verification script and run against live feed** - `1378a3c` (feat)
3. **Task 3: Verify MARESTO feed results** - checkpoint (user approved)

## Files Created/Modified
- `app/services/__init__.py` - Services package init
- `app/services/feed_fetcher.py` - HTTP feed fetcher returning raw bytes
- `app/services/feed_parser.py` - YML/XML parser with encoding detection and product upsert
- `app/views/suppliers.py` - Added POST /suppliers/<id>/fetch route for manual feed trigger
- `app/templates/suppliers/list.html` - Added Fetch Feed button, last_fetched_at and status columns
- `scripts/verify_maresto.py` - Standalone MARESTO feed verification script

## Decisions Made
- Raw bytes pipeline: feed_fetcher returns response.content (bytes), never .text, to prevent encoding corruption
- Encoding fallback: lxml native XML declaration first, then chardet detection as fallback
- MARESTO schema finding: no model/vendorCode elements in feed -- matching must rely on name + vendor only
- UTF-8 with BOM confirmed as MARESTO encoding -- BOM handled transparently by lxml

## Deviations from Plan
None - plan executed exactly as written.

## Issues Encountered
- MARESTO feed has no `<model>` or `<vendorCode>` elements, contrary to the generic YML schema expectation. This is not a bug but a data reality that Phase 2 matching must account for (match on name + vendor only).

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Feed ingestion pipeline is complete and verified against live data
- Blocking risk "MARESTO feed encoding" is RESOLVED (UTF-8 with BOM, Cyrillic preserved)
- Phase 2 can build scheduled fetching on top of feed_fetcher + feed_parser services
- Matching engine must handle absence of model/vendorCode fields

---
*Phase: 01-foundation-and-risk-validation*
*Completed: 2026-02-26*
