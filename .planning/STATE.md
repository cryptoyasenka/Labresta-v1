# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-02-26)

**Core value:** Ціни і наявність на prom.ua завжди актуальні — без ручної роботи щодня.
**Current focus:** Phase 2 — Feed Ingestion and Matching Engine

## Current Position

Phase: 2 of 4 (Feed Ingestion and Matching Engine)
Plan: 3 of 4 in current phase
Status: Executing
Last activity: 2026-02-27 — Completed 02-02-PLAN.md (Sync pipeline and CLI)

Progress: [███████░░░] 38%

## Performance Metrics

**Velocity:**
- Total plans completed: 4
- Average duration: 4 min
- Total execution time: 0.25 hours

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 1 | 2 | 8 min | 4 min |
| 2 | 2 | 7 min | 3.5 min |

**Recent Trend:**
- Last 5 plans: 01-01 (5 min), 01-03 (3 min), 02-01 (4 min), 02-02 (3 min)
- Trend: Stable

*Updated after each plan completion*

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.
Recent decisions affecting current work:

- [Roadmap]: Python + Flask + SQLite + rapidfuzz stack selected (PHP shared hosting disqualified — no production fuzzy match library)
- [Roadmap]: Phase 1 must verify prom.ua import mode with a test YML before any YML generation code is written — HIGH risk of wiping 5,950 unmanaged products
- [Roadmap]: UI is built last (Phase 4) — pipeline must be proven headless before adding UI layer
- [Roadmap]: No auto-approve for fuzzy matches in MVP — all matches require human confirmation
- [01-01]: Used hatchling build backend with explicit packages=['app'] for uv compatibility
- [01-01]: Model imports placed before db.create_all() using from-import to avoid name shadowing
- [01-01]: Catalog blueprint placeholder created early to prevent import errors in create_app
- [01-03]: Chardet for encoding detection with cp1251 fallback covers prom.ua CSV edge cases
- [01-03]: Price stored as integer cents (float*100) to avoid floating point issues
- [01-03]: Upsert matches on external_id unique column, updates all fields on re-import
- [02-01]: WAL mode via configure_sqlite_wal() called after db.init_app() for engine availability
- [02-01]: Telegram notifier reads env vars directly for APScheduler thread compatibility
- [02-01]: Telegram notifications only on permanent failure (all retries exhausted)
- [02-02]: tenacity @retry wraps existing fetch_feed, keeping original function unchanged
- [02-02]: Reappeared products stay needs_review=True — log-only visibility, no auto-restore
- [02-02]: 50% sanity guard prevents mass false-positive flagging from broken feeds
- [02-02]: 9-hour threshold for disappearance (2 sync intervals of 4h + 1h buffer)

### Pending Todos

None yet.

### Blockers/Concerns

- [Phase 1] prom.ua import mode behavior with partial feed is unverified — must test with 3-product subset YML before Phase 3 builds YML generator
- [Phase 1] MARESTO feed encoding (UTF-8 vs cp1251) unknown — fetch live URL before writing parser
- [Phase 2] Fuzzy match false-positive rate on real Ukrainian Cyrillic product names is unknown — benchmark against actual MARESTO + prom.ua name pairs before integrating into live pipeline

## Session Continuity

Last session: 2026-02-27
Stopped at: Completed 02-02-PLAN.md (Sync pipeline and CLI)
Resume file: .planning/phases/02-feed-ingestion-and-matching-engine/02-02-SUMMARY.md
