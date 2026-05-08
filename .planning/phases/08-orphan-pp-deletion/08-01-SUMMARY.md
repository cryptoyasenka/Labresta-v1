---
phase: 8
plan: 1
type: summary
status: applied-to-prod
date: 2026-05-08
---

# Phase 8 SUMMARY — Orphan PP Detection (Stage 4.5)

## Outcome

Stage 4.5 implemented end-to-end: service + CLI + UI tab with brand filter. **Applied to prod 2026-05-08**: 26 PromProducts auto-flagged across 5 single-supplier brands. Operator now reviews via `/matches/deletion-candidates?tab=orphan`.

## Tasks delivered

| Task | Commit | Tests | Files |
|---|---|---|---|
| 1 — service + 11 unit tests | `51d274c` | 11/11 | `app/services/orphan_detector.py`, `tests/test_orphan_detector.py` |
| 2 — wire-in fetch-all + CLI | `11aa107` | n/a | `app/views/suppliers.py`, `app/cli.py`, `app/__init__.py` |
| 3 — UI tab + brand filter + clear endpoint | `cd1e91b` | smoke | `app/views/matches.py`, `app/templates/matches/deletion_candidates.html` |
| Fix — prod-driven hardening | `3f9f07a` | 13/13 (+2) | `app/services/orphan_detector.py`, `app/cli.py`, `tests/test_orphan_detector.py` |

**Final test count:** 658/658 passed.

## Prod-driven fixes (from `3f9f07a`)

Two issues surfaced during the first prod dry-run:

1. **`display_article=None` PPs were being flagged.** First dry-run showed 425 candidates, of which the inspected 15-row sample had `display_article=None` (200+ FROSTY, 31 Hurakan etc.). This is a data-quality issue, not orphanhood. Logic now **skips** PPs without display_article — operator must fill the field first; we re-evaluate next run. (False negative > false positive.)

2. **MARESTO permanent 403 froze Stage 4.5 forever.** `_feed_drop_check` blocked the run because MARESTO has 0/4509 fresh SPs (Cloudflare IP-block against Railway egress, documented as known issue). Added `--exclude-dead-suppliers` flag (off by default): excludes suppliers with `recent==0, total>0` from BOTH the drop-check AND the brand-anchor count. Partial-drop protection (recent>0 but <50%) preserved.

## Apply result (2026-05-08)

Command:
```bash
flask flag-orphans --exclude-dead-suppliers
```

Output:
```
[APPLY] Stage 4.5 orphan detection:
  flagged: 26
  cleared: 0
  L1_total: 26
  brand_single_supplier_count: 44
  dead_supplier_ids excluded: [1]   # MARESTO
```

Idempotency verified: re-run yields `flagged=0 cleared=0`.

### 26 orphans by brand × supplier

| Count | Brand | Supplier |
|---:|---|---|
| 9 | Rational | Кодаки |
| 6 | Robot Coupe | Новый Проект |
| 6 | FROSTY | Кодаки |
| 4 | GI.Metal | Кодаки |
| 1 | Bartscher | Новый Проект |

(Detailed list in commit `3f9f07a` description / pre-compact snapshot.)

## Operational notes

- **`suppliers_fetch_all` view does NOT pass `exclude_dead_suppliers=True`.** This is intentional: by default the sanity guard remains strict — partial drops AND dead-supplier presence both block the run. Phase 8 auto-stage only fires once MARESTO recovers (or is disabled). Manual CLI invocation with the flag is the authoritative re-run path until then.
- **Adding/disabling a supplier rebalances anchors.** Enabling a second supplier of an orphan brand will auto-clear our flag on next run (logic already covers this).
- **Manual operator decisions are immune.** Logic checks `note != AUTO_NOTE` before overwriting, and the `clear_orphan_pp_flag` endpoint refuses to act on non-auto rows.

## Next actions for Yana (UI side)

1. Open `/matches/deletion-candidates?tab=orphan` (badge will show 26).
2. Use brand dropdown to triage one brand at a time (Rational, Robot Coupe, FROSTY, GI.Metal, Bartscher).
3. For each row choose:
   - **Видалено** → already removed from Horoshop (decision = `reviewed`).
   - **Залишити** → keep visible, hunt other suppliers (decision = `keep_searching`).
   - **Запит** → ask current supplier to add SKU (decision = `needs_request`).

## Follow-ups (not blocking)

- [ ] Contact MARESTO support for Railway IP whitelist (or build local-fetch import script) to unfreeze automatic Stage 4.5.
- [ ] Yana manual review of 10 outstanding Astim candidates (m=6620, 6618, 6611 reject + 7 fuzzy confirm).
- [ ] Decide whether `suppliers_fetch_all` should pass `exclude_dead_suppliers=True` (more aggressive auto-mode) — leaving OFF for now per safety default.

## Memory implications

No new memory entries needed. Existing pointers cover it:
- `project_labresta.md` — main project pointer
- `feedback_labresta_one_to_one`, `feedback_labresta_live_import`, `feedback_dump_data_before_regex` — applied throughout
- `feedback_check_yourself` — sample inspection caught the display_article bug before destructive commit
