# Code Audit — labresta-sync (deployed matcher)

**Date:** 2026-05-26
**Scope:** deep audit of the deployed matcher — code errors, consistency/logic violations.
**Method:** layer-by-layer (models → matcher → services → views → feed) + pattern greps.
**Status:** IN PROGRESS (interrupted by context compaction — resume from "Next checks").

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
- This is the LIVE store matcher. Report only — do NOT change matcher logic without
  Yana's go-ahead. Findings doc is the deliverable.
- Deliver summary to Yana in Russian.
