# Project Retrospective

*A living document updated after each milestone. Lessons feed forward into future planning.*

## Milestone: v1.0 — MVP

**Shipped:** 2026-02-28
**Phases:** 4 | **Plans:** 18 | **Sessions:** ~6

### What Was Built
- Full price sync pipeline: MARESTO XML feed → fuzzy matching → pricing → YML output
- Management UI: auth, match review, dashboard with charts, product lists, logs, notifications
- 21 automated tests (pricing + price gate), chardet encoding, Telegram alerts
- 9,016 LOC across Python/HTML/JS/CSS in 87 commits over 3 days

### What Worked
- **Phase ordering**: Building headless pipeline first (P1-P3), UI last (P4) prevented coupling
- **TDD for pricing**: 14 tests written before implementation caught edge cases early
- **Gap closure pattern**: UAT after Phase 3 found 2 issues, decimal plans 03-03/03-04 fixed them cleanly
- **Wave parallelization**: Phase 4's 7 plans across 4 waves maximized throughput
- **rapidfuzz WRatio**: Handled Cyrillic brand+model matching well (85.5% avg score)

### What Was Inefficient
- **Phase 1 no verification**: Skipped formal verification for "risk validation" phase, causing 7 orphaned requirements at audit
- **Plan 01-04 superseded**: FTP upload approach was replaced by Flask `/feed/yml` — wasted plan
- **REQUIREMENTS.md checkboxes stale**: 3 requirements checked as Pending but functionally complete — need discipline to tick checkboxes during execution
- **SyncProgress half-wired**: Dashboard progress bar infrastructure built but pipeline never calls it

### Patterns Established
- **Integer-cent pricing**: `(cents + 50) // 100` for mathematical rounding, no float accumulation
- **Atomic file writes**: `tempfile.mkstemp` + `os.replace` for YML generation
- **Lazy imports**: Inside functions to break circular import chains (sync_pipeline → yml_generator)
- **fetchWithCSRF pattern**: Client-side AJAX helper with CSRF token from meta tag
- **Context processor badges**: `pending_review_count` and `unread_notification_count` injected globally
- **admin_required decorator**: Reusable role check for admin-only routes

### Key Lessons
1. Always run formal verification on every phase, even "spike" phases — saves audit headaches
2. Update REQUIREMENTS.md checkboxes immediately when implementing, not retroactively
3. Price plausibility gate post-filter (not pre-filter) preserves scoring integrity
4. SQLite WAL mode is sufficient for single-server MVP — no need for PostgreSQL
5. chardet + cp1251 fallback handles all Ukrainian encoding scenarios

### Cost Observations
- Model mix: ~40% opus, ~50% sonnet, ~10% haiku (quality profile)
- Sessions: ~6 across 3 days
- Notable: Phase 3 was fastest (7 min total, 1.8 min/plan avg) — TDD plans are predictable

---

## Cross-Milestone Trends

### Process Evolution

| Milestone | Sessions | Phases | Key Change |
|-----------|----------|--------|------------|
| v1.0 | ~6 | 4 | Initial project, established all patterns |

### Cumulative Quality

| Milestone | Tests | Coverage | Zero-Dep Additions |
|-----------|-------|----------|-------------------|
| v1.0 | 21 | Pricing + price gate | 3 (tenacity, rapidfuzz, flask-apscheduler) |

### Top Lessons (Verified Across Milestones)

1. Verify every phase formally — audit catches orphaned requirements
2. Headless-first architecture (pipeline before UI) prevents coupling
