# Roadmap: LabResta Sync

## Overview

Four phases move from zero to a fully operational price sync system. Phase 1 establishes the foundation and resolves two blocking risks before any production code is written: prom.ua import mode behavior with a partial feed, and the MARESTO feed's real-world encoding and schema. Phase 2 builds the headless sync pipeline — the actual product — including feed ingestion, fuzzy matching, and mapping persistence. Phase 3 overlays pricing logic and generates the public YML feed. Phase 4 adds the management UI and authentication, completing the tool for daily operator use.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [ ] **Phase 1: Foundation and Risk Validation** - Scaffold, live feed verification, prom.ua import mode spike, catalog import
- [ ] **Phase 2: Feed Ingestion and Matching Engine** - Scheduled fetching, retry logic, fuzzy match candidates, mapping persistence
- [ ] **Phase 3: Pricing Engine and YML Output** - Price calculation, YML generation, public feed URL, discontinued product handling
- [ ] **Phase 4: Management UI and Authentication** - Match review UI, supplier CRUD, dashboard, logs, login

## Phase Details

### Phase 1: Foundation and Risk Validation
**Goal**: Two blocking risks are resolved and the system skeleton is ready to build on — the team knows exactly how prom.ua handles partial YML imports, and the live MARESTO feed's encoding and schema are confirmed.
**Depends on**: Nothing (first phase)
**Requirements**: AUTH-03, CATLG-01, CATLG-02, SUPP-01, SUPP-02, SUPP-03, SUPP-04
**Success Criteria** (what must be TRUE):
  1. A 3-product test YML uploaded to prom.ua confirms that unlisted products are left untouched (import mode verified, catastrophic overwrite risk eliminated)
  2. The live MARESTO feed at mrst.com.ua/include/price.xml is fetched and parsed without encoding errors — product names in Cyrillic are readable in the database
  3. The prom.ua catalog CSV is imported and products are queryable by name, brand, and model in the local database
  4. Suppliers can be created, edited, enabled, and disabled via direct DB interaction or CLI
  5. The public YML URL path is accessible without authentication (no login required to fetch the feed file)
**Plans**: TBD

### Phase 2: Feed Ingestion and Matching Engine
**Goal**: The sync pipeline can fetch the MARESTO feed on a schedule, survive failures gracefully, and produce a set of fuzzy match candidates that a human can review and confirm — all without a UI.
**Depends on**: Phase 1
**Requirements**: MATCH-01, MATCH-03, MATCH-06, SUPP-05, SUPP-06, SUPP-07
**Success Criteria** (what must be TRUE):
  1. A scheduled job fetches the MARESTO feed every 4 hours; last-fetched timestamp is visible in the database and never overwrites good data on a failed fetch
  2. When the feed URL is unreachable, the system retries at least 3 times and keeps the last known good data intact
  3. Running the sync manually (via CLI or script) produces fuzzy match candidates ranked by confidence score in the database
  4. Confirmed matches (supplier_id to prom_product_id) persist across sync runs and are not re-matched on subsequent syncs
  5. A product absent from the MARESTO feed for 2 consecutive syncs is flagged as "needs review" in the database with availability set to unavailable
**Plans**: 4 plans
- [ ] 02-01-PLAN.md — Database schema (ProductMatch, SyncRun models), WAL mode, Telegram notifier
- [ ] 02-02-PLAN.md — Sync pipeline with retry, disappeared detection, Flask CLI
- [ ] 02-03-PLAN.md — Fuzzy matching engine with brand blocking, benchmark
- [ ] 02-04-PLAN.md — APScheduler setup, matcher integration, end-to-end verification

### Phase 3: Pricing Engine and YML Output
**Goal**: Confirmed matches produce a correctly priced, publicly accessible YML feed that prom.ua can poll automatically — and only matched products are included in the output.
**Depends on**: Phase 2
**Requirements**: FEED-01, FEED-02, FEED-03, FEED-04, PRICE-01, PRICE-02, PRICE-03, PRICE-04
**Success Criteria** (what must be TRUE):
  1. A confirmed match with a per-supplier discount of 15% and a supplier retail price of 199.99 EUR produces a final price of 169.99 EUR in the YML — no floating point errors
  2. The YML file is written atomically (write to .tmp then rename) and is available at a stable public URL without authentication
  3. The generated YML contains only products with confirmed matches — products without matches do not appear in the feed
  4. Per-product discount overrides take priority over the supplier-level discount when both are set
  5. The YML structure is compatible with both prom.ua and Horoshop import (fields: name, price, availability, article number)
**Plans**: 4 plans
- [ ] 03-01-PLAN.md — Pricing engine TDD (integer-cent math, per-product discount, mathematical rounding)
- [ ] 03-02-PLAN.md — YML generator, public feed endpoint, sync pipeline wiring
- [ ] 03-03-PLAN.md — [GAP CLOSURE] Add product page URL to catalog import and YML feed
- [ ] 03-04-PLAN.md — [GAP CLOSURE] Add price plausibility gate to fuzzy matcher

### Phase 4: Management UI and Authentication
**Goal**: An operator can log in, review and confirm fuzzy match candidates through a web UI, manage suppliers, monitor sync health from a dashboard, and browse logs — without touching the database directly.
**Depends on**: Phase 3
**Requirements**: AUTH-01, AUTH-02, DASH-01, DASH-02, DASH-03, DASH-04, DASH-05, MATCH-02, MATCH-04, MATCH-05
**Success Criteria** (what must be TRUE):
  1. An admin can log in with email and password; all management pages are inaccessible without a valid session; the public YML URL remains accessible without login
  2. The match review screen shows each candidate with confidence level (High/Medium/Low), the supplier product name, and the prom.ua product name side-by-side — the admin can confirm, reject, or manually specify a match
  3. The dashboard displays last sync time, count of matched products, count of unmatched products, count flagged for review, and any active errors — without navigating away
  4. The admin can trigger a manual sync from the dashboard with one click and see the updated status afterward
  5. The admin can see all supplier products with current prices, and separately see all prom.ua catalog products with no confirmed match
**Plans**: 6 plans
- [ ] 04-01-PLAN.md — Auth foundation: User model, Flask-Login, CSRF, login/logout, create-admin CLI, base template
- [ ] 04-02-PLAN.md — Match review table: filtering, sorting, pagination, confirm/reject, bulk actions
- [ ] 04-03-PLAN.md — Dashboard: widget cards, manual sync trigger, sync journal, auto-refresh polling
- [ ] 04-04-PLAN.md — Product lists: supplier products, unmatched prom.ua, unmatched supplier products
- [ ] 04-05-PLAN.md — Advanced match features: manual match modal, match rules, CSV/XLSX export, diff highlighting
- [ ] 04-06-PLAN.md — Logs section, user management CRUD, sync settings

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Foundation and Risk Validation | 0/TBD | Not started | - |
| 2. Feed Ingestion and Matching Engine | 0/4 | Not started | - |
| 3. Pricing Engine and YML Output | 2/4 | In progress | - |
| 4. Management UI and Authentication | 4/7 | In Progress|  |
