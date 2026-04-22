# Phase L — Supplier conflict resolution UX

**Status:** planned, not started  
**Trigger:** 2026-04-22. Yana bulk-confirmed 20 НП candidates, 5 silently skipped because their PP was already confirmed by MARESTO. No dialog, just a toast that flashed for 2.5s. She asked for proper UX.

## Goal
When `/matches/bulk-action` (action=confirm) skips rows because the PP is already claimed by another supplier (`skipped_claimed`), show operator a modal that lets them resolve each conflict: keep the existing supplier, switch to the new one, or postpone.

## Current behaviour (pain)
- `_pp_already_claimed` in `app/views/matches.py` detects claimed PPs
- Bulk-confirm loop appends `{match_id, prom_product_id, existing_match_id}` to `skipped_claimed`
- JS handler in `app/static/js/matches.js` (~line 770): shows a warning toast "Пропущено: N" for 2.5s then reloads
- No context about WHICH supplier holds the PP or HOW to resolve it
- Operator doesn't notice → thinks confirm is broken

## Design

### Backend
1. **Enrich `skipped_claimed` payload** in `bulk_action()`:
   ```json
   {
     "match_id": 1570,
     "prom_product_id": 42,
     "pp_name": "ТЕРМОПАКУВАЛЬНИЙ АПАРАТ SIRMAN 45К СЕ",
     "existing": {
       "match_id": 996,
       "supplier_name": "MARESTO",
       "sp_name": "Термопакувальний апарат...",
       "sp_article": "40602300",
       "score": 95
     },
     "candidate": {
       "supplier_name": "Новый Проект",
       "sp_name": "Термопакувальний апарат Sirman 45к се",
       "sp_article": "40602300",
       "score": 100
     }
   }
   ```

2. **New endpoint `POST /matches/resolve-conflict`**:
   - Body: `{candidate_match_id: int, action: "keep" | "switch"}`
   - `keep` → reject candidate (status=rejected, confirmed_by="conflict-keep:{user}")
   - `switch` → unconfirm existing + confirm candidate. Fresh defaults — don't copy MARESTO's `discount_percent` to НП match (confirmed with Yana 2026-04-22: each supplier has own margins).
   - Returns `{status: "ok", existing_match_id, new_status}`
   - Log_action with type "conflict_keep" / "conflict_switch"

### Frontend
3. **Modal `#conflictResolveModal` in `review.html`**:
   - Rendered when `skipped_claimed.length > 0`
   - Replaces the auto-reload toast for conflict case
   - One row per conflict, layout:
     ```
     PP: {pp_name}
       Сейчас у: {existing.supplier_name} — "{existing.sp_name}" ({existing.sp_article}, match #{existing.match_id})   [Оставить]
       Кандидат:  {candidate.supplier_name} — "{candidate.sp_name}" ({candidate.sp_article}, {candidate.score}%)       [Переключить]
     ```
   - Buttons call `/matches/resolve-conflict`, on ok hide the row (fade)
   - Footer: "Закрыть" (оставшиеся конфликты останутся candidate для будущего разбора) + "Применить и перезагрузить"

4. **JS flow in `matches.js`**:
   - `doBulkAction('confirm')` → on response with `skipped_claimed.length > 0`:
     - Still show "Применено: N" toast for the processed ones
     - Populate modal with conflict rows
     - Show modal (don't auto-reload)
     - After modal closes, reload
   - Per-row handler: `resolveConflict(candidate_match_id, action)` — POST, on ok remove row from DOM

### Tests
5. `tests/test_bulk_action_conflict_resolve.py`:
   - `test_resolve_keep_rejects_candidate` — verify old match untouched, new match status=rejected
   - `test_resolve_switch_unconfirms_existing_and_confirms_candidate` — verify atomicity
   - `test_resolve_invalid_action_returns_400`
   - `test_resolve_candidate_already_confirmed_returns_409` (idempotency guard)
   - `test_bulk_confirm_returns_enriched_skipped_info` — skipped_claimed includes supplier_name etc

## Out of scope
- Mass auto-resolve ("always prefer НП over MARESTO") — always one at a time. Too dangerous otherwise.
- Changing manual /matches/{id}/rebind — stays as-is for other use cases.
- Carrying over discount/settings — fresh defaults for new supplier (user confirmed).

## Files touched
- `app/views/matches.py` — enrich `skipped_claimed`, add `/resolve-conflict` endpoint
- `app/templates/matches/review.html` — `#conflictResolveModal`
- `app/static/js/matches.js` — modal populate + per-row handlers
- `tests/test_bulk_action_conflict_resolve.py` — new file

## Estimate
~60-90 min coding + ~20 min smoke testing via the live /matches UI against the existing NP↔MARESTO overlaps (currently 22 candidates in conflict).

## Done criteria
- Operator can bulk-confirm НП with conflicts and gets an actionable modal instead of a flash toast
- Modal resolves each conflict with one click, persists correctly, audit log captures decisions
- Existing bulk-confirm behaviour unchanged when there are no conflicts (modal not shown)
- Tests green (including existing 383 + 5 new conflict-resolution tests)
