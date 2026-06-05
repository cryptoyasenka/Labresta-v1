---
gsd_state_version: 1.0
milestone: v1.1
milestone_name: Tech Debt + Excel Suppliers + Multi-Supplier
status: maintenance
stopped_at: "2026-06-02 Phase 9 autonomous code COMPLETE; T7/#16 DECIDED by Yana = R2 (auto chain default + AI re-check as opt-in audit, built + provider-independent). Remaining = Yana hand only (her API key / fresh NP feed from her IP / canary then bulk import + backup). MARESTO awaits Horoshop support reply."
last_updated: "2026-06-05"
last_activity: 2026-06-05
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

Status: maintenance / audit-driven fixes. v1.0 + v1.1 plans complete; Phase 9 autonomous code complete (remaining = Yana's hand: import + optional AI re-check).
Last activity: 2026-06-05 (night maintenance: read-only candidate triage + doc hygiene)

## DB snapshot (2026-06-05, night maintenance — READ-ONLY)

- Suppliers: 6 (all enabled) — `maresto` (flat), `novyy-proekt` (per_brand), `kodaki` (flat), `rp-ukrayina` (flat), `guder` (flat), `astim` (flat)
- PromProducts: 5683
- SupplierProducts: 12895 (all live, 0 deleted) — astim 5597, maresto 4523, kodaki 1354, novyy-proekt 690, rp-ukrayina 374, guder 357
- Matches (table `product_matches`): 2362 confirmed + 7 manual + 301 candidate + 71 rejected
- Tests: 850 passed, 2 skipped @ branch `chore/night-maint-2026-06-05`
- Candidate triage → `.planning/candidate-triage-2026-06-05.md`: 301 candidates ⇒ recommend-CONFIRM 61 / NEEDS-EYEBALL 237 / recommend-REJECT 3. one-to-one cross-check (`scripts/triage_one_to_one_check.py`): 97/301 candidates sit on an already-matched PP; within CONFIRM, 15/61 are #15 conflicts ⇒ **46 safe-to-confirm**. No DB mutation (status snapshot identical before/after).

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

- **#16** (Phase 9 / 09-02 T7) ✅ **DECIDED by Yana 2026-06-02 = R2**: the auto chain (feed→analogy→fallback, ship-no-ai) is the DEFAULT, and AI re-check is a SEPARATE opt-in audit that only flags auto↔AI category discrepancies in a CSV and never rewrites the live category. R1 (AI as a live-chain tier) rejected. The AI re-check is BUILT and provider-independent (any OpenAI-compatible endpoint; NVIDIA NIM default) — commits `2276041`/`83c54a5`. Optional mapping-table is also built + wired opt-in (45 non-null mappings → feed 97.5% conf-100). Remaining is Yana's hand only, NOT a decision: (item2) run the AI re-check with her own API key, (item3) approve a 1-2 row `[КАТАЛОГ] Раздел` canary then bulk-import by hand + backup (invariant #13) using a fresh NP feed from her IP. Docs: `.planning/phases/09-add-unmatched-to-horoshop/CATEGORY-PROPOSAL.md`.
- **#9** ~~Per-supplier YML route returns 404~~ — closed 2026-04-29 by `eb22fbf` (option B: friendly HTML page with regen instructions, status stays 404 for bots).
- **#10** SP color/voltage variant collisions: stage B done 2026-04-29 (`960fea3`, Step 4.88 asymmetric color gate — defends against future cross-language color discord and parens/display_article cases that 4.85/4.9 miss). Stage A (sibling-aware downgrade for SP without color when catalog has color siblings) still pending.
- **#12** 301 candidates remain — manual triage required (CLAUDE.md invariant #3 forbids 100%-bulk-confirm). Read-only triage dossier built 2026-06-05: `.planning/candidate-triage-2026-06-05.md` classifies all 301 (CONFIRM 61 / EYEBALL 237 / REJECT 3) with PP-vs-SP evidence. After the one-to-one cross-check, only **46** of the 61 CONFIRM rows are safe to hand-confirm (15 are #15 supplier conflicts); the 237 EYEBALL rows still need a human read. Nothing auto-confirmed.
- **#14** Pure-letter SKU substring fast-path bypasses all text gates (deliberate compromise documented in code; voltage/paren/price gates still apply).
- **#15** Text-perfect candidates whose PP already holds a confirmed supplier → 1pp↔1supplier conflict (can't confirm without first rejecting the incumbent = a policy call for Yana). Original instances: RP `#3546` (SIRMAN TC-12) + `#3569` (UNOX XFT193). Now quantified by the 2026-06-05 triage: across ALL candidates, 97/301 sit on an already-matched PP; within the recommend-CONFIRM bucket specifically, 15/61 are conflicts (match_ids 3352,3357,3365,3369,3729,3730,3735,3743,3748,3754,3760,3779,3784,3785,4376) — e.g. `m3730` (PP2966→held 840) and `m3760` (PP1037→held 228). Re-list any time: `scripts/triage_one_to_one_check.py`.

## Blockers/Concerns

None code-level. #16 category strategy is DECIDED (2026-06-02 = R2). Remaining items are Yana's-hand (Phase 9 bulk import: her IP for a fresh NP feed + canary + backup; optional AI re-check with her key) or external (MARESTO blocked on a Horoshop support reply) — not autonomous, not code blockers.

## Session Continuity

Last session: 2026-06-05 (night maintenance, branch `chore/night-maint-2026-06-05`) — read-only candidate triage (#12) + doc hygiene (STATE/ROADMAP) + green test baseline (850 passed, 2 skipped). Prior: 2026-06-02 R2 confirmed + ai_recheck generalized to provider-independent on `feat/horoshop-add-unmatched`.
Resume file: pre-compact-prep snapshot in `~/.claude/snapshots/`; project memory `.planning/CURRENT.md`
