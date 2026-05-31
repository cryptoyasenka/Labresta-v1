---
gsd_state_version: 1.0
milestone: v1.1
milestone_name: Tech Debt + Excel Suppliers + Multi-Supplier
status: maintenance
stopped_at: "2026-05-31 Phase 9 (add-unmatched-to-horoshop) plan 09-02 T1-T6 done; T7 checkpoint:decision awaits Yana (category strategy + canary)"
last_updated: "2026-05-31T04:30:00.000Z"
last_activity: 2026-05-31
progress:
  total_phases: 7
  completed_phases: 7
  total_plans: 18
  completed_plans: 18
  percent: 100
---

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-03-01)

**Core value:** Ціни і наявність на prom.ua/Horoshop завжди актуальні — без ручної роботи щодня.
**Current focus:** maintenance + audit; multi-supplier rollout (Maresto + НП + Kodaki + РП Україна).

## Current Position

Status: maintenance / audit-driven fixes. v1.0 + v1.1 plans complete.
Last activity: 2026-04-29 (read-only audit + eur_rate fallback fix)

## DB snapshot (2026-04-29)

- Suppliers: 4 — `maresto` (flat), `novyy-proekt` (per_brand), `kodaki` (flat), `rp-ukrayina` (flat)
- PromProducts: 5683
- SupplierProducts: 6918
- Matches: 1861 confirmed + 7 manual + 279 candidate, 0 rejected
- Tests: 569 green @ commit `960fea3`

## Recent landed work (2026-04-23 → 2026-05-31)

- 2026-05-31 Phase 9 plan 09-02 (smart category) `1b4def4`→`2b07378` on `feat/horoshop-add-unmatched` — three-tier feed→analogy→fallback «Раздел» resolver behind the same interface (AI tier DISABLED, D3/REQ-06); NP feed name/RU/description enrichment (FLAG-1/D2) + optional np_feed upload on /feeds/add (FLAG-2); read-only prod-guarded audit script. Real audit over 320 unmatched NP: feed 40.6% / analogy 54.7% / fallback 4.7%. Full suite 835 passed, 2 skipped. **T7 checkpoint awaits Yana** (see Open issues). NOT merged to main; NO Horoshop import performed.
- 2026-05-30 Phase 9 plan 09-01 (CORE create-file) `a90af42`→`b63a7fb` on `feat/horoshop-add-unmatched` — add_horoshop_file builder + price_unmatched + fallback resolver + /feeds/add picker.
- 2026-04-29 `960fea3` — Step 4.88 asymmetric color-variant gate (#10 stage B)
- 2026-04-29 `eb22fbf` — friendly "Фид ещё не собран" page replaces blank 404 on all 5 public feed routes (closes #9)
- 2026-04-29 `c7175d2` — `resolve_eur_rate()` helper logs WARNING when supplier rate falls back to 51.15
- 2026-04-27 `37cdb64` — removed per-match apply-discount endpoint (live store, dead code)
- 2026-04-27 `76ca146` — visible feed URL + copy button on dashboard
- 2026-04-27 `f1489a4`/`b1c4d91` — xlsx URL detection + RP parser branch in sync_pipeline
- 2026-04-27 `ca2e1eb` — РП Україна xlsx parser + pipeline integration
- 2026-04-26 `4faa73a` — Kodaki feed adapter (OpenCart dwebexporter → YML)
- 2026-04-26 `6908d11` + `753390d` — asymmetric bracket-token containment gate (Step 4.87) + invariant #15
- 2026-04-26 — N+1 batch performance fixes across rule_matcher / matcher / matches view
- 2026-04-23 `cdcf158` — bracket-discriminator gate (Step 4.85)

## Open issues (await Yana decision)

- **#16** (Phase 9 / 09-02 T7 — BLOCKING checkpoint) Category strategy for unmatched-product create-cards: **ship-no-ai** (feed→analogy→fallback, recommended first) / **enable-ai** (NVIDIA tier — not built; one-arg flip + implementation) / **mapping-table** (~50 unreconciled feed categories → store labels). Plus approve the 1–2 row `[КАТАЛОГ] Раздел` canary before any bulk import (invariant #13, Yana's hand + backup). Evidence + options: `.planning/phases/09-add-unmatched-to-horoshop/CATEGORY-PROPOSAL.md`. AI is OFF until Yana says otherwise (REQ-06).
- **#9** ~~Per-supplier YML route returns 404~~ — closed 2026-04-29 by `eb22fbf` (option B: friendly HTML page with regen instructions, status stays 404 for bots).
- **#10** SP color/voltage variant collisions: stage B done 2026-04-29 (`960fea3`, Step 4.88 asymmetric color gate — defends against future cross-language color discord and parens/display_article cases that 4.85/4.9 miss). Stage A (sibling-aware downgrade for SP without color when catalog has color siblings) still pending.
- **#12** 279 candidates remain — manual triage required (CLAUDE.md invariant #3 forbids 100%-bulk-confirm).
- **#14** Pure-letter SKU substring fast-path bypasses all text gates (deliberate compromise documented in code; voltage/paren/price gates still apply).
- **#15** RP candidates `#3546` (SIRMAN TC-12) + `#3569` (UNOX XFT193) score=100 + identical names BUT both PPs already have confirmed maresto matches → 1pp↔1supplier conflict.

## Blockers/Concerns

None code-level. All blockers above are decision-level for Yana.

## Session Continuity

Last session: 2026-05-31 (night run) — Phase 9 plan 09-02 T1–T6 executed + committed + pushed on `feat/horoshop-add-unmatched`; T7 checkpoint awaits Yana (#16)
Resume file: pre-compact-prep snapshot in `~/.claude/snapshots/`; project memory `.planning/CURRENT.md`
