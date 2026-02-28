# Milestones

## v1.0 MVP (Shipped: 2026-02-28)

**Phases completed:** 4 phases, 18 plans executed (1 superseded)
**Stats:** 87 commits | 9,016 LOC (Python 4,660 + HTML 2,734 + JS 1,527 + CSS 95)
**Timeline:** 3 days (2026-02-26 → 2026-02-28)
**Git range:** `feat(01-01)` → `feat(04-07)`

**Key accomplishments:**
1. Foundation: SQLAlchemy models, prom.ua catalog CSV import, supplier CRUD, chardet encoding detection
2. Sync pipeline: 4h scheduled fetch with 3x retry (tenacity), disappearance detection with 9h threshold, Telegram alerts
3. Fuzzy matching: rapidfuzz WRatio scorer with brand blocking, price plausibility gate (3x ratio), 60% score cutoff
4. Pricing engine: TDD with 21 tests, integer-cent math, per-product discount override, atomic YML write
5. Public YML feed: prom.ua/Horoshop compatible, `/feed/yml` endpoint, `<url>` element per offer
6. Management UI: Flask-Login auth (admin/operator roles), match review with bulk ops/export/diff, dashboard with Chart.js trends, notification rules with Telegram dispatch

**Delivered:** Ціни і наявність на prom.ua завжди актуальні — без ручної роботи щодня.

### Known Gaps

Proceeding with 3 formally unsatisfied requirements (all functionally complete):
- AUTH-03: Public YML URL without auth — works via `/feed/yml`, traceability checkbox not ticked
- SUPP-03: Download/parse supplier YML feeds — works via feed_fetcher + feed_parser, checkbox not ticked
- SUPP-04: Auto-detect feed encoding — works via chardet in feed_parser, checkbox not ticked

Root cause: Phase 1 has no VERIFICATION.md (risk validation phase, not formally verified).

### Tech Debt

- `price_forced` flag not respected by `save_supplier_products` — forced prices overwritten on next sync
- `MatchRule` records stored but never consumed by matcher during automated sync
- Sync progress bar shows only 1 stage (cosmetic)
- `notifications.js` not globally loaded — badge polling only on notifications page
- Operator-role users see notification bell that leads to 403
- `ftp_upload.py` and `yml_test_generator.py` are dead code
- `ProductMatch.discount_percent` column exists but no UI writes to it

**Archives:** `milestones/v1.0-ROADMAP.md`, `milestones/v1.0-REQUIREMENTS.md`, `milestones/v1.0-MILESTONE-AUDIT.md`

---

