# Roadmap: LabResta Sync

## Milestones

- ✅ **v1.0 MVP** — Phases 1-4 (shipped 2026-02-28)
- 🚧 **v1.1 Tech Debt + Excel Suppliers** — Phases 5-7 (in progress)

## Phases

<details>
<summary>✅ v1.0 MVP (Phases 1-4) — SHIPPED 2026-02-28</summary>

- [x] Phase 1: Foundation and Risk Validation (3/3 plans + 1 superseded) — completed 2026-02-26
- [x] Phase 2: Feed Ingestion and Matching Engine (4/4 plans) — completed 2026-02-27
- [x] Phase 3: Pricing Engine and YML Output (4/4 plans) — completed 2026-02-28
- [x] Phase 4: Management UI and Authentication (7/7 plans) — completed 2026-02-28

</details>

### v1.1 Tech Debt + Excel Suppliers

- [x] **Phase 5: Cleanup and UX Fixes** - Remove dead code, fix notification bell for operators, load notifications.js globally
- [x] **Phase 6: Excel Supplier Support** - Add Excel/Google Sheets as supplier feed type with parsing and sync pipeline integration
- [ ] **Phase 7: Matching and Pricing Enhancements** - Activate MatchRule auto-apply during sync, add per-product discount UI

## Phase Details

### Phase 5: Cleanup and UX Fixes
**Goal**: Dead code removed and notification system works correctly for all user roles
**Depends on**: Phase 4 (v1.0 complete)
**Requirements**: CLEAN-01, CLEAN-02, UX-01, UX-02
**Success Criteria** (what must be TRUE):
  1. Files `yml_test_generator.py` and `generate_test_yml.py` no longer exist in the codebase (ftp_upload.py intentionally kept per user decision)
  2. Notification badge counter updates on every page (not just the notifications page)
  3. Operator-role user can click the notification bell and see their notifications without a 403 error
  4. Admin-role user still sees the full notification management page as before
**Plans**: 2 plans (Wave 1 — parallel)

Plans:
- [x] 05-01-PLAN.md — Dead code cleanup, global badge polling, notification dropdown
- [x] 05-02-PLAN.md — Operator notification page access with role-based rendering

### Phase 6: Excel Supplier Support
**Goal**: Operators can add Excel/Google Sheets suppliers and sync their product data through the same pipeline as YML suppliers
**Depends on**: Phase 5
**Requirements**: EXCEL-01, EXCEL-02, EXCEL-03, EXCEL-04
**Success Criteria** (what must be TRUE):
  1. Operator can create a new supplier with feed type "Excel" and provide a Google Sheets URL or upload an .xlsx file
  2. System automatically converts a Google Sheets sharing URL to a download URL and fetches the .xlsx file
  3. System parses Excel file and extracts product name, price, and availability into SupplierProduct records
  4. Excel-sourced supplier products appear in the matching queue and sync pipeline identically to YML-sourced products
  5. Parse errors (missing required columns, unparseable prices) are reported to the operator via flash messages and sync logs
**Plans**: 2 plans (Wave 1: 06-01, Wave 2: 06-02)

Plans:
- [x] 06-01-PLAN.md — Excel parser service with TDD (URL detection, column auto-detection, product parsing) + Supplier model column_mapping
- [x] 06-02-PLAN.md — Sync pipeline Excel branching + supplier UI (file upload, mapping preview/confirm, list badges)

### Phase 7: Matching and Pricing Enhancements
**Goal**: Matching rules produce automatic confirmed matches during sync, and operators can set per-product discount overrides through the UI
**Depends on**: Phase 6
**Requirements**: MTCH-01, PRC-01
**Success Criteria** (what must be TRUE):
  1. When a supplier syncs, products with existing MatchRule entries are automatically confirmed without going through the fuzzy matching queue
  2. Rule-applied matches appear as confirmed in the match list (same status as manually confirmed matches)
  3. Operator can set or clear an individual discount percentage on any confirmed match through the matches UI
  4. Per-product discount override takes priority over the supplier default discount in price calculation and YML output
**Plans**: 2 plans (Wave 1: 07-01, Wave 2: 07-02)

Plans:
- [x] 07-01-PLAN.md — MatchRule auto-apply in sync pipeline with TDD (rule_matcher.py + pipeline integration + review.html rule indicator)
- [x] 07-02-PLAN.md — Per-product discount UI (AJAX endpoint, discount column, detail panel input with live price preview)

## Progress

**Execution Order:**
Phases execute in numeric order: 5 → 6 → 7

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. Foundation and Risk Validation | v1.0 | 3/3 | Complete | 2026-02-26 |
| 2. Feed Ingestion and Matching Engine | v1.0 | 4/4 | Complete | 2026-02-27 |
| 3. Pricing Engine and YML Output | v1.0 | 4/4 | Complete | 2026-02-28 |
| 4. Management UI and Authentication | v1.0 | 7/7 | Complete | 2026-02-28 |
| 5. Cleanup and UX Fixes | v1.1 | 2/2 | Complete | 2026-03-01 |
| 6. Excel Supplier Support | v1.1 | 2/2 | Complete | 2026-03-01 |
| 7. Matching and Pricing Enhancements | v1.1 | 0/2 | Planned | - |

---
*Full v1.0 details: milestones/v1.0-ROADMAP.md*
