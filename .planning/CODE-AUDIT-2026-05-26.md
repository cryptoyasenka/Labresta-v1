# Code Audit — labresta-sync (deployed matcher)

**Date:** 2026-05-26
**Scope:** deep audit of the deployed matcher — code errors, consistency/logic violations.
**Method:** layer-by-layer (models → matcher → services → views → feed) + pattern greps.
**Status:** COMPLETE (full read of matcher core + run_matching + sync_pipeline + pricing + yml + views).

Severity: 🔴 bug (wrong result / crash) · 🟠 logic/consistency risk · 🟡 minor/cosmetic.

---

## Findings so far

### 🟡 P-1 — `clamp_applied` false-positive on non-integer base discount
`app/services/pricing.py:191` `compute_match_pricing`:
```python
if float(clamped) != base_d:
    clamp_applied = True
```
`clamp_discount_for_min_margin` always returns `floor(base_d)` even when the
margin is fine. So a supplier with `discount_percent=19.5` and healthy margin
gets `clamped=19`, `19.0 != 19.5` → `clamp_applied=True`. The UI then shows
"скидка урезана под маржу" when nothing was actually clamped for margin — only
integer flooring happened. Cosmetic but misleads the operator.
**Fix idea:** compare against `floor(base_d)` not `base_d`, or have clamp return
a sentinel when it didn't reduce for margin.

### 🟡 P-2 — displayed margin uses unrounded discount, price uses rounded
`app/services/pricing.py:195-198`: `price_eur` is rounded to tenths via
`calculate_price_eur`, but `margin_eur = retail_eur * (1 - cost_rate - eff_d/100)`
uses the *unrounded* sell fraction. The margin shown next to the price can be off
by up to ~retail*0.05*rate UAH from the margin implied by the displayed price.
Minor, but two numbers on the same row won't reconcile exactly.

### ✅ RESOLVED-OK — 26× `except Exception`
All either log (`logger.exception/error`), surface to UI (jsonify 500 / flash), or
re-raise. Silent `pass` only at: matcher.py:2136 (progress cb advisory — fine),
dashboard.py:144 (scheduler next-run lookup, advisory — fine), yml_generator.py:245
(re-raises after unlinking temp file — correct). No silent error-swallowing bugs.

### ✅ RESOLVED-OK — `.first()` sites are not smells
matches.py 42/1466/1478/1659/1679 are existence checks for the 1:1 invariant or
lookups on the UNIQUE (supplier_product_id, prom_product_id) pair → deterministic.
Low-risk note only: `_pp_already_claimed` (matches.py:42) returns an arbitrary
conflicter IF the 1:1 invariant is already violated in data — acceptable since its
job is existence detection.

### 🟠 P-3 — effective-discount logic duplicated (drift risk)
The same "resolve base discount → clamp for min-margin (skip if per-match override,
rate=1 for UAH)" sequence is implemented TWICE:
- `app/services/pricing.py:184-194` (`compute_match_pricing`, used by the UI)
- `app/services/yml_generator.py:210-225` (`_compute_price_eur`, used by the feed)
They currently agree, so the price shown in the UI == the price emitted to Horoshop.
But there is no shared helper enforcing that — a future edit to one (e.g. changing
cost_rate handling or clamp rounding) silently desyncs the feed from the UI, which
on a live store means the customer sees a different price than the operator approved.
**Fix idea:** extract one `resolve_effective_discount(match) -> float` and call it
from both. Add a test asserting `compute_match_pricing(m)['price_eur'] ==
_compute_price_eur(m)` for a few fixtures.

### ✅ POSITIVE — Path B (matcher feed) correctly enforced
`yml_generator._build_offer_xml` emits ONLY `<price>/<oldprice>/<available>/
<vendorCode>` — no `<name>/<name_ru>/<description>/<vendor>`. The original
corruption bug (Horoshop mapping `<name>`→"Назва модифікації (RU)") cannot recur
through these feeds. Comment block documents the invariant clearly.

### ✅ POSITIVE — `find_match_candidates` core has no correctness bug
Full read of the ~1000-line core (matcher.py 929–1922). Gate pipeline is layered
and each gate that can reject a 100%-fuzzy false-positive is correctly guarded:
- Article/model/display fast-path matches carry `_skip_post_gates` and correctly
  bypass the paren/bracket/color/containment gates (manufacturer SKU equality is
  stronger evidence than name-token similarity).
- Variant gates (voltage 4.8, bracket-discriminator 4.85/4.87, color 4.88,
  after-brand containment 4.9) are symmetric/conservative — "one side missing the
  tag → pass" so base/uncolored rows aren't wrongly rejected.
- Score mutation is bounded (`min(100.0, score + MODEL_BOOST_POINTS)`); oversample
  (200) → sort → truncate to `limit` → re-filter by `score_cutoff` ordering is correct.
- `_model_contained` correctly exempts a candidate from the price-plausibility gate
  (catalog price may be stale when the SKU is confirmed inside the PP name).
Temp flags (`_skip_post_gates`, `_model_contained`) are popped before return (1919-1921).

### 🟡 M-2 — per-gate linear rescans of `candidates_pool` (performance, not correctness)
Every post-fuzzy gate re-finds the PP dict with `for p in candidates_pool: if p["id"]==…`.
With ~10 gates × up to 200 candidates × full pool (thousands of PPs) this is millions
of iterations per supplier product, repeated for every SP in a sync. Pure perf smell —
a single `pool_by_id = {p["id"]: p for p in candidates_pool}` built once would remove it.
No wrong results. Out of scope to change on the live matcher without a benchmark.

### 🟠 M-3 — `claimed_pp_ids` is first-SP-wins within a supplier run
`run_matching_for_supplier` (matcher.py 2085-2131) reserves a PP for the first SP that
produces a candidate for it; a later SP that would score *higher* on the same PP is
silently skipped. Protects the 1pp↔1supplier invariant and prevents dup-explosion, but
the operator may be shown the weaker of two same-supplier candidates for a PP. Acceptable
by design (human reviews, can rematch), noted for awareness. Not changing.

### 🟠 M-1 — sync error path can lose the SyncRun "error" status on a DB-level exception
`sync_pipeline._sync_single_supplier`: stages 3 (save) and 6 (matching) commit
internally, so for the common network/parse/ValueError the session is clean and the
`finally: db.session.commit()` correctly persists `status="error"`. BUT if the raised
exception is itself a SQLAlchemy/DB error mid-flush, the session is left in a needs-
rollback state → the `finally` commit raises `PendingRollbackError`, the error status
and `error_message` are lost, and the SyncRun stays `"running"` forever.
**Fix:** `db.session.rollback()` at the top of the `except` block before setting the
error fields. Low-risk (only discards the already-failed stage's uncommitted dirt).

### 🟡 S-1 — per-supplier sync runs a GLOBAL safe-auto-confirm pass
`sync_pipeline` Stage 6.5 calls `bulk_auto_confirm.apply_rules(apply=True)` with no
supplier scope, so syncing supplier A also auto-confirms/rejects candidates belonging
to supplier B. Likely intended (the R1-R4 rules are globally safe), but a per-supplier
manual sync having cross-supplier write side effects is a surprising coupling. Note only.

### ✅ RESOLVED-OK — sync pipeline staging & cleanup
`tmp_path` unlinked in `finally` (OSError-guarded); `_detect_disappeared` has a >50%
feed-shrink guard before flagging disappearances; disappeared confirmed/manual matches
become `deletion_candidate` (not silently deleted), candidates auto-reject. Reappeared
products are NOT auto-restored (stay needs_review) — matches the documented decision.

---

## Fix plan (authorized 2026-05-26 — "пофиксить")
| ID | Fix | Risk | Touches feed price? |
|----|-----|------|---------------------|
| P-3 | Extract `resolve_effective_discount(match) -> (base, eff)`, call from both pricing.compute_match_pricing and yml._compute_price_eur | low (behavior-preserving, + parity test) | indirectly — must stay byte-identical |
| P-1 | `clamp_applied = eff_d < floor(base_d)` instead of `!= base_d` | none (UI flag only) | no |
| P-2 | `margin_eur = price_eur - retail_eur*cost_rate` so margin reconciles with displayed price | none (UI margin only) | no |
| M-1 | `db.session.rollback()` at top of sync except block | low (defensive) | no |

M-2, M-3, S-1: noted, NOT changing (perf / by-design / out of scope on live matcher).

---

## Next checks (resume order)
0. (this session covered: pricing, .first(), except, yml Path B + feed/UI price parity)
1. Read `find_match_candidates` (matcher.py 929–1925) — the 1000-line core: gate
   ordering, early-returns, score mutation, candidate truncation vs oversample.
2. Read the 5 `.first()` sites in matches.py + supplier.py:89 — uniqueness.
3. Grep+read the 26 `except Exception` — which swallow silently.
4. yml_generator.py — Path B two-channel (matcher feed = price/avail only). Confirm
   no name/desc leak into matcher feeds (the original corruption bug).
5. sync_pipeline.py — order of fetch/parse/match/price/export; partial-failure handling.
6. Model ↔ usage consistency: currency default 'EUR' vs UAH suppliers; price_cents
   int vs float; nullable fields read without None-guard.
7. catalog_import preview/save already audited this session (just shipped) — skim only.

## Notes / constraints
- This is the LIVE store. Fixes authorized for P-1/P-2/P-3/M-1 (none change the
  emitted feed price — P-3 is behavior-preserving with a parity test). Matcher GATE
  LOGIC is NOT being touched (no correctness bug found there).
- Deliver summary to Yana in Russian.
