# Project Research Summary

**Project:** LabResta Sync — Supplier XML/YML Price Sync Tool
**Domain:** Supplier feed aggregation / marketplace price automation (prom.ua / Horoshop)
**Researched:** 2026-02-26
**Confidence:** MEDIUM

## Executive Summary

LabResta Sync is an internal ETL tool that fetches supplier YML/XML price feeds on a schedule, applies per-supplier discount rules, fuzzy-matches supplier products to a local prom.ua catalog, and emits a prom.ua-compatible YML feed for auto-import. The domain is well-understood — this is a classic Extract-Transform-Load pipeline — but the core technical challenge is non-trivial: fuzzy product matching without shared article codes across 6,100 catalog products and multiple supplier feeds. Python (Flask + APScheduler + SQLite + rapidfuzz) deployed on a low-cost VPS is the recommended stack. The fuzzy matching requirement alone disqualifies PHP shared hosting as a primary path, because no production-quality fuzzy match library exists for PHP.

The recommended architecture follows a strict linear pipeline: Fetch → Parse → Match → Price → Generate. Each stage is isolated and testable independently. The system has two planes: a sync pipeline (runs on schedule, headless) and a management UI (used by the operator to review/confirm product matches and monitor sync health). The output is a static YML file served at a public URL, which prom.ua polls every 4 hours. The store catalog is never pushed to prom.ua programmatically — the YML pull model is an explicit design decision that keeps the tool platform-agnostic for the planned Horoshop migration.

The dominant risk is fuzzy matching producing silent false positives — wrong products linked and priced incorrectly in the live store. This must be mitigated from the start by requiring human confirmation for all matches (no auto-approve in MVP), displaying match confidence prominently in the review UI, and writing unit tests for the matching algorithm before integrating it into the live pipeline. A secondary risk is misconfigured prom.ua import mode wiping 5,950 unmanaged products when the partial feed is uploaded. This must be verified manually with a test import before automation is enabled.

---

## Key Findings

### Recommended Stack

Python 3.12 + Flask + SQLAlchemy + SQLite is the right foundation. The key library that tips the decision away from PHP is `rapidfuzz` — the successor to fuzzywuzzy, with C-extension speed and token-set-ratio matching that handles Ukrainian/Cyrillic word-order differences that are endemic in product naming. `lxml` handles the XML/YML parsing, including malformed or mis-encoded feeds that are common from Ukrainian suppliers. `APScheduler` (pinned to 3.10.x, not 4.x) embedded in the Flask process eliminates the need for an external cron daemon. Deployment target is a low-cost VPS (Render/Railway free tier or ~$5/month), not shared hosting.

See [STACK.md](STACK.md) for full version matrix, alternatives considered, and the PHP shared hosting fallback spec.

**Core technologies:**
- Python 3.12+: runtime — 3.12 perf improvements, LTS until Oct 2028
- Flask 3.1.x: web framework — minimal footprint for single-developer internal tool
- SQLite (via SQLAlchemy 2.0.x): database — zero ops overhead; 6,100 products fit comfortably; upgradeable to PostgreSQL via config
- APScheduler 3.10.x: scheduler — embedded in Flask process, cron-style triggers, pin `<4.0`
- lxml 5.x: XML/YML parsing — handles malformed XML and encoding issues common in Ukrainian supplier feeds
- rapidfuzz 3.x: fuzzy matching — the entire value of this tool depends on this library; handles Cyrillic word-order variants
- gunicorn + nginx: production server — gunicorn serves Flask; nginx serves static feed.yml and handles SSL

### Expected Features

The MVP is intentionally small. One supplier (MARESTO, ~150 products), one operator, one store. The critical path from zero to working sync is: catalog import → fuzzy matching → confirmed mappings → YML output. Every other feature is secondary.

**Must have (table stakes):**
- Supplier CRUD — add/edit/disable suppliers with URL and discount %
- YML feed ingestion from URL — HTTP GET + XML parse per supplier
- Scheduled feed refresh — 1-4h interval; prom.ua polls every 4h
- Store catalog import — one-time import of prom.ua product list to enable matching (hidden prerequisite)
- Fuzzy match candidate engine — brand + model token similarity; this is the entire value of the project
- Matching UI (review + confirm/reject + manual override) — operator's primary daily-use screen
- Confirmed mapping persistence — three-state DB table: confirmed / pending / rejected
- Price calculation engine — `final_price = supplier_price * (1 - discount%)`; use integer cents
- YML output at stable public URL — written atomically to avoid partial-file reads by prom.ua
- Discontinued product handler — absent from feed N syncs = mark unavailable, flag for review
- Sync status dashboard — last sync time, match counts, error state

**Should have (competitive, add after first supplier validated):**
- Change diff log — "what changed in last sync" view
- Bulk match confirmation — review and approve multiple candidates in one session
- Confidence score display — High/Medium/Low badges with matched strings side-by-side
- Staleness alerting — feed not updated in 2x interval → visible error banner
- Per-supplier field mapping config — for second supplier with different YML structure

**Defer (v2+):**
- Horoshop-specific output fields (YML is already compatible; defer Horoshop-specific divergences)
- Multi-supplier conflict resolution (which price wins when two suppliers match the same product)
- Price floor/ceiling rules
- Full audit trail / price history
- Email/webhook alerts (dashboard check sufficient initially)

### Architecture Approach

The system is a linear ETL pipeline (Ingestion → Matching → Pricing → Output) with a parallel management plane (Web UI + API). These two planes share the database but are otherwise independent — the sync pipeline can run headlessly without the UI, and the UI can be used without triggering a sync. The build order follows dependency order: DB schema first, then ingestion, then matching, then pricing, then output, then pipeline orchestration, then scheduler, then API, then UI. The UI is last because a working headless pipeline must be proven before UI is built.

See [ARCHITECTURE.md](ARCHITECTURE.md) for full component diagram, data flow diagrams, and anti-patterns.

**Major components:**
1. Feed Fetcher + Parser + Adapter — HTTP GET with retry/timeout; lxml parse; per-supplier adapter normalizes to internal SupplierProduct schema
2. Fuzzy Match Engine — brand pre-filter (reduces 6,100 to ~50-200 candidates), then token-set-ratio model matching; confidence threshold gates auto-confirm vs. review queue
3. Mapping Store (DB) — three-state persistence: confirmed / pending / rejected; confirmed mappings survive re-syncs and bypass the matcher
4. Pricing Engine — pure function; integer cents; per-supplier discount rule; rounds once at end
5. YML Feed Generator — overlays matched+priced updates onto catalog snapshot; atomic file write (write to .tmp, then rename)
6. Sync Pipeline Orchestrator — thin function calling stages 1-5 in order; triggered by APScheduler
7. Web UI — Dashboard, Supplier Manager, Match Reviewer; consumes REST API

### Critical Pitfalls

1. **Fuzzy matching silent false positives** — Wrong products get wrong prices published in the live store. Mitigate by requiring human confirmation for ALL matches in MVP (no auto-approve); displaying confidence with matched strings visible side-by-side; adding a "must differ" guard on numeric model suffixes (S500 vs S501 should flag as uncertain). Recovery cost is HIGH.

2. **YML output configured as full catalog replacement on prom.ua** — The partial feed (~150 matched products) triggers deletion of the 5,950 unmanaged store products. Mitigate by verifying prom.ua import mode manually before enabling automation; testing with a 3-product subset YML and confirming catalog is intact. Document this as a required deploy step. Recovery cost is HIGH.

3. **Silent feed failure serving stale data** — Supplier URL goes down; system fails quietly; prices go stale. Mitigate by: never overwriting DB on failed fetch (keep last known good), retry with backoff (min 3 retries), dashboard shows last-fetched timestamp prominently, error banner when feed hasn't updated in 2x interval.

4. **XML encoding mismatch (Windows-1251 vs UTF-8)** — Ukrainian supplier feeds commonly serve cp1251 with mismatched HTTP headers. Garbled Cyrillic breaks fuzzy matching entirely. Mitigate by fetching the live MARESTO URL on Day 1 of ingestion phase, before writing parser code; using lxml's encoding detection; logging raw bytes of first 100 chars of every new feed.

5. **Float-point price calculation errors** — `price * (1 - 0.15)` produces `169.9915000000001`. Mitigate by storing prices as integer cents throughout, rounding once at output. Write a unit test: `assert calculate_price(199.99, 0.15) == 169.99` before shipping.

6. **Discontinued/renamed products creating orphaned matches** — Supplier removes a product; matched pair stays in DB; availability silently stays wrong. Mitigate by tracking `last_seen_in_feed` per matched pair; flagging as "needs review" after N consecutive missed syncs (default 2); never auto-deleting mappings.

---

## Implications for Roadmap

Based on component dependencies, pitfall prevention phase requirements, and the MVP definition from features research, the recommended phase structure is:

### Phase 1: Foundation and Risk Validation

**Rationale:** Before writing a line of application code, two HIGH-risk pitfalls must be validated manually: (a) prom.ua import mode behavior with a partial feed, and (b) MARESTO feed encoding and schema. These cannot be safely deferred — discovering either mid-build would require architecture changes. This phase also establishes the DB schema and project skeleton that everything else builds on.

**Delivers:** Proven understanding of prom.ua import behavior; confirmed MARESTO feed encoding and schema; DB schema + migrations; project scaffold (Flask app, SQLAlchemy, APScheduler wired up); store catalog imported (one-time: prom.ua CSV export loaded into DB).

**Addresses features:** Supplier CRUD (basic), store catalog import (prerequisite to matching), project setup.

**Avoids pitfalls:** YML import mode misconfiguration (verified before building output), XML encoding mismatch (confirmed before writing parser), float price errors (integer cents schema from day 1).

**Research flag:** Does not need `/gsd:research-phase` — the research here is hands-on validation with live URLs and prom.ua admin, not library research.

### Phase 2: Sync Pipeline (Headless)

**Rationale:** Build the full sync pipeline end-to-end without UI. This is the core product. A working headless pipeline (Feed → Parse → Match → Price → YML output) can be tested with scripts before any UI exists. Architecture research explicitly states: "After step 6 [YML Generator], you have a working headless sync tool." Building the pipeline first means the UI is built on a proven foundation.

**Delivers:** Working end-to-end sync pipeline: fetch MARESTO feed → parse → fuzzy match candidates → apply mappings (CLI-confirmed for now) → price calculation → YML output written to file. Scheduler running on interval. Basic sync log.

**Implements architecture components:** Feed Fetcher + MARESTO Adapter, Feed Parser, Fuzzy Match Engine (rapidfuzz, token-set-ratio, brand pre-filter), Mapping Store (three-state DB), Pricing Engine (integer cents), YML Generator (atomic write), Sync Pipeline Orchestrator, APScheduler.

**Addresses features:** Feed ingestion, scheduled refresh, fuzzy match engine, confirmed mapping store, price calculation, YML output, discontinued product handler.

**Avoids pitfalls:** Silent feed failure (retry logic, last-fetched-at tracking from day 1), sync job overlap (job lock in scheduler), non-atomic YML write (write-to-.tmp-then-rename pattern), monolithic parser (adapter pattern from the start even for single supplier).

**Research flag:** Fuzzy matching algorithm design for Ukrainian/Cyrillic product names warrants a `/gsd:research-phase` spike. The token-set-ratio approach is well-documented in rapidfuzz, but the normalization rules for Ukrainian product names (Cyrillic stopwords, brand alias handling, numeric suffix guards) are domain-specific and benefit from a focused research task before building.

### Phase 3: Management UI

**Rationale:** With a proven pipeline, build the UI that makes the tool usable by a non-technical operator. The matching review screen is the most critical — it is the operator's primary daily-use surface and the primary safeguard against false-positive matches reaching production. Build matching review first, then supplier management, then dashboard.

**Delivers:** Full web UI: Match Reviewer (review/confirm/reject/override matches, confidence display, unmapped queue), Supplier Manager (CRUD with URL + discount %), Dashboard (sync status, last-fetched timestamps, error state). REST API backing the UI. Basic auth protecting all routes.

**Addresses features:** Matching UI, manual override mapping, sync status dashboard, error visibility, confidence score display, unmapped product queue.

**Avoids pitfalls:** False positive matches propagating silently (human review gate), match confidence displayed as High/Medium/Low with matched strings side-by-side (not raw 0.87 number), sync status prominent on dashboard (not buried in logs).

**Research flag:** Standard Flask + Jinja2 server-rendered UI is well-documented — skip `/gsd:research-phase` for UI framework. If the decision is made to build a JavaScript-heavy UI, flag for research.

### Phase 4: Second Supplier and Hardening

**Rationale:** Adding the second supplier tests whether the architecture generalizes correctly. Per-supplier adapter pattern, per-supplier field mapping config, and multi-supplier pipeline execution all get exercised for the first time. This phase also adds the v1.x features deferred from MVP: change diff log, bulk match confirmation, staleness alerting.

**Delivers:** Second supplier fully onboarded and syncing. Per-supplier field mapping config UI. Change diff log ("what changed in last sync"). Bulk match confirmation. Staleness alerting (feed not updated in 2x interval → banner). Validated generalization of adapter pattern.

**Addresses features:** Second supplier, change diff log, bulk match confirmation, staleness alerting, per-supplier field mapping config.

**Avoids pitfalls:** Monolithic parser with per-supplier branches (adapter pattern already in place from Phase 2), sync log doesn't report per-supplier metrics (add per-supplier counters).

**Research flag:** Skip — standard patterns, no new technical unknowns after Phase 2-3.

### Phase Ordering Rationale

- **Foundation before pipeline:** The store catalog import is a hidden prerequisite to matching. It must be done before the fuzzy engine has anything to match against. Similarly, prom.ua import mode must be verified before the YML generator is built.
- **Pipeline before UI:** Architecture research explicitly establishes this order. The UI is worthless if the underlying sync is broken. Testing the pipeline with scripts first catches data issues before the UI adds a layer of indirection.
- **UI before second supplier:** The matching review UI is what makes adding a second supplier tractable. Without it, confirming 150+ matches from supplier 2 requires direct DB edits.
- **Second supplier validates architecture:** The adapter pattern and per-supplier config must be exercised before claiming the architecture is correct. One supplier can be handled with hardcoded workarounds; two suppliers exposes every assumption.

### Research Flags

**Needs deeper research during planning:**
- **Phase 2 — Fuzzy matching for Ukrainian Cyrillic product names:** The algorithm approach (rapidfuzz token-set-ratio) is clear, but domain-specific normalization rules (Cyrillic stopword lists, brand alias tables, numeric suffix guards for model numbers) need a focused spike. False-positive rate must be benchmarked against real MARESTO+prom.ua product name pairs before the engine is integrated into the live pipeline.

**Standard patterns, skip research-phase:**
- **Phase 1:** Hands-on validation with live URLs, not library research.
- **Phase 3:** Flask + Jinja2 server-rendered UI is standard. REST API design at this scale has no surprises.
- **Phase 4:** Adapter pattern is established in Phase 2. Adding a supplier is configuration, not new architecture.

---

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | MEDIUM | Core libraries (Flask, SQLAlchemy, rapidfuzz, lxml, APScheduler) are stable and well-documented. Versions verified against training cutoff Aug 2025. APScheduler 4.x pre-release status is LOW confidence — pin to 3.10.x. prom.ua-specific YML field behavior is MEDIUM — verify against live prom.ua admin before implementation. |
| Features | MEDIUM | Table stakes and differentiators are clear from project context and domain analysis. Competitor analysis is LOW confidence (no network access during research). prom.ua import behavior (4h cycle, selective field update mode) is MEDIUM — confirm in prom.ua admin during Phase 1. |
| Architecture | MEDIUM | ETL pipeline pattern and adapter-per-supplier pattern are industry-standard and HIGH confidence. Fuzzy matching architecture is MEDIUM — the approach is sound but Ukrainian Cyrillic normalization rules are domain-specific and unverified against real data. Atomic file write pattern is HIGH confidence. |
| Pitfalls | MEDIUM | Six critical pitfalls identified with clear prevention strategies. Float price pitfall is HIGH confidence (multiple independent sources). prom.ua import mode pitfall is MEDIUM confidence (prom.ua docs returned 403; inferred from integration patterns). UX pitfalls are well-documented patterns. |

**Overall confidence:** MEDIUM

The research provides a solid foundation for roadmap and implementation. The main uncertainty area is prom.ua-specific behavior (import mode, field update semantics, 4h polling), which must be validated hands-on during Phase 1 before building the output layer. No gaps require blocking the roadmap.

### Gaps to Address

- **prom.ua YML import mode configuration:** Must be verified in prom.ua admin during Phase 1 before building the YML generator. Specifically: does "update fields only" mode leave unlisted products untouched, or mark them unavailable? Test with a 3-product subset YML.
- **MARESTO feed encoding and schema:** Fetch the live URL before writing parser code. Confirm encoding (UTF-8 vs cp1251), confirm field names (vendor/model/price/available), and confirm whether any fields are optional or absent.
- **Fuzzy match false-positive rate on real data:** The algorithm design is sound, but false-positive rate against actual MARESTO + prom.ua product name pairs is unknown. Must be benchmarked with real data before the engine is integrated into the live pipeline. A manual audit of 20 random matches (checking that brand+model are genuinely the same product) is the minimum bar for Phase 2 completion.
- **APScheduler 4.x release status:** As of training cutoff (Aug 2025), 4.x was in pre-release with a breaking API change. Pin to `apscheduler>=3.10,<4.0` and verify on PyPI before project setup.

---

## Sources

### Primary (HIGH confidence)
- `C:/Projects/labresta-sync/.planning/PROJECT.md` — authoritative project scope, constraints, requirements
- rapidfuzz documentation (github.com/maxbachmann/RapidFuzz) — confirmed replacement for fuzzywuzzy
- POSIX rename(2) specification — atomic file write pattern
- Adapter pattern (Gang of Four) — adapter-per-supplier architecture

### Secondary (MEDIUM confidence)
- Python ecosystem training knowledge (Flask, SQLAlchemy, APScheduler, lxml) — versions as of Aug 2025
- Yandex Market Language (YML) format — training knowledge; verify at yandex.ru/support/partnermarket/export/yml.html
- prom.ua YML import behavior — training knowledge + project context; verify at support.prom.ua
- Fuzzy matching algorithm patterns (Levenshtein, token-set-ratio, Cyrillic text) — training knowledge
- Atomic Object / Modern Treasury on float currency rounding — multiple corroborating sources
- WinPure, DataWeave, DataLadder on fuzzy matching pitfalls — MEDIUM confidence

### Tertiary (LOW confidence)
- prom.ua YML import docs (support.prom.ua) — returned 403 during research; behavior inferred from third-party integrations; verify directly in prom.ua admin
- Ukrainian marketplace competitor analysis — no direct competitor research possible (network access denied); based on WooCommerce/OpenCart ecosystem patterns
- APScheduler 4.x pre-release status — verify exact release date on PyPI before project setup

---
*Research completed: 2026-02-26*
*Ready for roadmap: yes*
