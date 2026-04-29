---
gsd_state_version: 1.0
milestone: v1.1
milestone_name: Tech Debt + Excel Suppliers + Multi-Supplier
status: maintenance
stopped_at: 2026-04-29 audit closed (eur_rate logging fix landed; #9-#15 await Yana)
last_updated: "2026-04-29T00:00:00.000Z"
last_activity: 2026-04-29
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
- Tests: 548 green @ commit `c7175d2`

## Recent landed work (2026-04-23 → 2026-04-29)

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

- **#9** Per-supplier YML route returns 404 — feed file generated only on manual regenerate. Decide: A) JIT generation, B) graceful page, or C) hide URLs until generated.
- **#10** SP color/voltage variant collisions auto-confirmed (real for #2650 FW-100 white sibling exists). Needs sibling-aware color gate (analogous to Step 4.85). Cannot fix one-line — symmetric voltage gate would regress 342 confirmed.
- **#12** 279 candidates remain — manual triage required (CLAUDE.md invariant #3 forbids 100%-bulk-confirm).
- **#14** Pure-letter SKU substring fast-path bypasses all text gates (deliberate compromise documented in code; voltage/paren/price gates still apply).
- **#15** RP candidates `#3546` (SIRMAN TC-12) + `#3569` (UNOX XFT193) score=100 + identical names BUT both PPs already have confirmed maresto matches → 1pp↔1supplier conflict.

## Blockers/Concerns

None code-level. All blockers above are decision-level for Yana.

## Session Continuity

Last session: 2026-04-29 audit (read-only + 1 fix landed)
Resume file: pre-compact-prep snapshot in `~/.claude/snapshots/`
