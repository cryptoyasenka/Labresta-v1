# Phase 1: Foundation and Risk Validation - Context

**Gathered:** 2026-02-26
**Status:** Ready for planning

<domain>
## Phase Boundary

Scaffold the system skeleton, resolve two blocking risks, and deliver first end-to-end data flow — all without a full web UI. Blocking risks: (1) prom.ua import mode behavior with a partial YML (will unlisted products survive?), (2) MARESTO live feed encoding and schema (does Cyrillic parse correctly?). Deliverables: local Flask app running on Windows, SQLite DB, prom.ua catalog imported, supplier added, test YML fetched from shared hosting by prom.ua.

</domain>

<decisions>
## Implementation Decisions

### Deployment architecture
- App runs **locally on Windows PC** — no VPS, no cloud
- Flask + SQLite run on the user's machine
- Generated YML file is **uploaded to shared hosting via FTP** (`labresta.com/feed.yml`)
- prom.ua fetches that static file automatically every 4h
- Web UI accessible at `localhost:5000` (admin only, no public exposure needed)
- Shared hosting: adm.tools account "labresta", domains `labresta.com` / `labresta.com.ua`

### Minimal web UI in Phase 1
- Phase 1 includes a **minimal web UI** — not CLI-only
- Required forms: add/edit supplier (URL, name, discount %), import catalog file, trigger manual sync
- This is a deliberate choice: user is not comfortable with CLI commands
- Full dashboard, match review, logs come in Phase 4 — Phase 1 UI is bootstrap-only

### prom.ua catalog import
- Supports **both CSV and XML** formats exported from prom.ua admin panel
- Import is **manual** in Phase 1: user downloads file from prom.ua, uploads through web UI
- User adds products frequently (several times per week) — note for Phase 2: investigate if prom.ua provides a public catalog export URL that could be auto-fetched (same mechanism as supplier feeds)
- Required fields to extract: product ID (prom.ua), name, brand, model, article number

### prom.ua import mode spike (blocking risk)
- Must verify in Phase 1: upload a 3-product test YML to prom.ua and confirm unlisted products are left untouched
- This is a manual test against the live prom.ua store — not a code test
- Result must be confirmed before building the YML output generator in Phase 3
- Risk: if prom.ua overwrites unlisted products, the entire architecture must change

### MARESTO live feed (blocking risk)
- Must fetch the live URL `mrst.com.ua/include/price.xml` in Phase 1 — not a local fixture
- Confirm: Cyrillic product names readable in SQLite without encoding errors
- Confirm: field schema matches expectations (name, price, availability, article)
- Encoding detection must handle both UTF-8 and Windows-1251

### FTP upload
- YML generation must include FTP upload step to push `feed.yml` to `labresta.com`
- FTP credentials stored in local config file (not committed to git)
- Upload path and credentials configurable (not hardcoded)

### Claude's Discretion
- Python project structure (directory layout, module names)
- SQLite schema details (exact column names, indexes)
- FTP library choice
- Flask app factory vs simple app pattern
- Windows Task Scheduler setup instructions (deferred to Phase 2)

</decisions>

<specifics>
## Specific Ideas

- The web UI in Phase 1 is intentionally minimal — a scaffold for Phase 4, not a polished product
- FTP credentials must never be committed to git (`.gitignore` the config file)
- The prom.ua import mode spike is a manual test, not automated — document the result in the project notes

</specifics>

<deferred>
## Deferred Ideas

- Auto-fetch prom.ua catalog via URL (if prom.ua provides one) — investigate in Phase 2
- Windows Task Scheduler setup for auto-sync every 4h — Phase 2
- Authentication / login for web UI — Phase 4

</deferred>

---

*Phase: 01-foundation-and-risk-validation*
*Context gathered: 2026-02-26*
