# Backlog — tasks parked for later

## Apply-discount UI for per-brand suppliers (REVISED 2026-04-29)

**Status:** parked — old endpoint removed 2026-04-27 (`37cdb64`), needs re-design.
**Created:** 2026-04-22 (during НП onboarding)
**Updated:** 2026-04-29

### Current state
- `eur_rate_uah` is **editable** in supplier form (`templates/suppliers/form.html:133`).
- Live rates 2026-04-29: maresto/НП/kodaki=51.15, rp-ukrayina=52.0.
- The old `/suppliers/<id>/apply-discount` endpoint was deleted 2026-04-27 along with the per-match apply button (live store, dead code).
- `clamp_discount_for_min_margin` is wired into `compute_match_pricing` so margin clamp happens at price-render time per match (no batch job needed).
- `resolve_eur_rate()` (2026-04-29 `c7175d2`) logs a WARNING when supplier rate falls back to 51.15.

### Open question
Does НП still need a batch "recalc all per-brand discounts" action, or is the live per-render clamp enough? If the second — close this backlog item entirely.

### If revived — what to build
1. New UI button on supplier page (per_brand + auto_margin only) → dry-run preview of % distribution → confirm.
2. Re-implement endpoint to call `clamp_discount_for_min_margin` per supplier-product (not per match) so all matches inherit the adjusted ceiling.
3. Tests: dry-run + apply on per_brand НП-style supplier with multi-brand mix + 3 price tiers.

### Constants (for НП)
- min_margin = 500 UAH
- cost_rate = 0.75
- per-brand defaults already set in `supplier_brand_discount` table

---

## Open audit items (await Yana — see STATE.md)

- #9 Per-supplier YML route 404
- #10 SP color/voltage variant siblings (sibling-aware color gate)
- #12 279 candidates manual triage
- #14 Pure-letter SKU bypass (deliberate compromise — review only if false positives observed)
- #15 RP/maresto duplicate confirms (decide policy: 1pp↔1supplier → which supplier wins)
