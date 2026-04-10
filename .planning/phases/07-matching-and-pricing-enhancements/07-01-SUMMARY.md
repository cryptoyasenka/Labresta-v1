---
phase: 07-matching-and-pricing-enhancements
plan: 01
subsystem: matching
tags: [tdd, rule-matching, auto-confirm, sync-pipeline]
dependency_graph:
  requires: []
  provides: [apply_match_rules]
  affects: [sync_pipeline, review_ui]
tech_stack:
  added: []
  patterns: [rule-based-auto-confirm, tdd-red-green]
key_files:
  created:
    - app/services/rule_matcher.py
    - tests/test_rule_matcher.py
  modified:
    - app/services/sync_pipeline.py
    - app/templates/matches/review.html
decisions:
  - "Module-scoped test fixture to avoid APScheduler singleton conflict on repeated create_app"
  - "Unicode lightning bolt for rule badge (no icon library dependency)"
  - "Break out of rule loop on first match per product (one rule wins)"
metrics:
  duration: "3 min"
  completed: "2026-04-10"
  tasks: 2
  tests: 10
---

# Phase 7 Plan 1: Rule Matcher Auto-Apply Summary

Rule-based auto-confirm for supplier products via MatchRule entries, integrated into sync pipeline as Stage 5/7 before fuzzy matching, with TDD tests covering all edge cases.

## What Was Done

### Task 1: Create rule_matcher.py with TDD tests (c563ada)

**RED phase:** Created `tests/test_rule_matcher.py` with 10 test cases:
- Name match creates confirmed ProductMatch (score=100.0, confirmed_by='rule:{id}')
- Brand+name both required when rule has supplier_brand
- NULL brand matches on name only
- Stale rule (deleted prom product) safely skipped
- Confirmed/manual matches skipped (not re-processed)
- Rejected matches never overwritten by rules
- Candidate matches upgraded to confirmed (not duplicated)
- Returns count of auto-confirmed matches
- Inactive rules (is_active=False) not applied
- Manual matches skipped

**GREEN phase:** Created `app/services/rule_matcher.py` with `apply_match_rules(supplier_id)`:
- Queries active MatchRules, filters out already-confirmed supplier products
- Exact name match with optional brand constraint
- Verifies prom product still exists before creating match
- Handles existing candidate/rejected/confirmed matches appropriately
- Commits and returns count

### Task 2: Integrate into sync pipeline + review badge (d85bdb0)

**sync_pipeline.py:** Inserted Stage 5/7 (rule apply) between disappeared detection and fuzzy matching. Updated all stage numbering from /6 to /7 (7 total stages).

**review.html:** Added `data-confirmed-by` attribute to table rows. Added visual lightning badge ("Правило") next to status for rule-auto-confirmed matches (confirmed_by starts with "rule:").

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] APScheduler singleton conflict in test fixtures**
- **Found during:** Task 1 GREEN phase
- **Issue:** Function-scoped app fixture called `create_app()` multiple times, causing `SchedulerAlreadyRunningError` from the singleton APScheduler
- **Fix:** Changed to module-scoped app fixture with per-test table cleanup
- **Files modified:** tests/test_rule_matcher.py

## Known Stubs

None -- all functionality is fully wired.

## Self-Check: PASSED

- [x] app/services/rule_matcher.py exists
- [x] tests/test_rule_matcher.py exists
- [x] Commit c563ada found (Task 1)
- [x] Commit d85bdb0 found (Task 2)
- [x] All 10 tests pass
- [x] Import check passes
