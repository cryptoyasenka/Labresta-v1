---
phase: 03-pricing-engine-and-yml-output
plan: 03
subsystem: api
tags: [yml, prom-ua, catalog-import, xml-feed]

# Dependency graph
requires:
  - phase: 03-pricing-engine-and-yml-output/plan-02
    provides: YML feed generator and pipeline wiring
provides:
  - page_url column on PromProduct model
  - URL header mapping in catalog import (Ukrainian/Russian)
  - url element emission in YML feed offers
affects: [04-management-ui]

# Tech tracking
tech-stack:
  added: []
  patterns: [conditional YML element emission based on nullable field]

key-files:
  created: []
  modified:
    - app/models/catalog.py
    - app/services/catalog_import.py
    - app/services/yml_generator.py
    - app/services/yml_test_generator.py

key-decisions:
  - "Conditional url emission -- only when page_url is populated, graceful for pre-migration products"
  - "Ukrainian and Russian header aliases for prom.ua product page URL column"

patterns-established:
  - "Nullable URL fields with conditional YML emission for backward compatibility"

requirements-completed: [FEED-01]

# Metrics
duration: 1min
completed: 2026-02-28
---

# Phase 3 Plan 3: YML URL Gap Closure Summary

**Product page URL storage via catalog import and conditional url element emission in YML feed offers**

## Performance

- **Duration:** 1 min
- **Started:** 2026-02-27T23:25:23Z
- **Completed:** 2026-02-27T23:26:25Z
- **Tasks:** 2
- **Files modified:** 4

## Accomplishments
- PromProduct model extended with page_url column for storing prom.ua product page URLs
- Catalog import maps Ukrainian and Russian URL header variants to page_url field
- Both YML generators (production and test) emit url element when page_url is available

## Task Commits

Each task was committed atomically:

1. **Task 1: Add page_url column and import mapping** - `8972604` (feat)
2. **Task 2: Emit url element in both YML generators** - `8841ce9` (feat)

## Files Created/Modified
- `app/models/catalog.py` - Added page_url nullable column to PromProduct
- `app/services/catalog_import.py` - Added URL header aliases and page_url persistence in upsert
- `app/services/yml_generator.py` - Conditional url element between name and price in offers
- `app/services/yml_test_generator.py` - Conditional url element in test YML offers

## Decisions Made
- Conditional url emission (only when page_url populated) ensures backward compatibility with products imported before this change
- Ukrainian/Russian header aliases match prom.ua standard export column names

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- YML feed now includes product page URLs after catalog re-import
- Ready for 03-04 gap closure (matcher price gate) or Phase 4 (Management UI)

## Self-Check: PASSED

All 4 modified files verified present. Both task commits (8972604, 8841ce9) verified in git log.

---
*Phase: 03-pricing-engine-and-yml-output*
*Completed: 2026-02-28*
