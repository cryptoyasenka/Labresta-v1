# Phase 3: Pricing Engine and YML Output - Context

**Gathered:** 2026-02-27
**Status:** Ready for planning

<domain>
## Phase Boundary

Confirmed matches produce a correctly priced, publicly accessible YML feed that prom.ua can poll automatically. Only matched products are included in the output. This phase covers pricing calculation, YML generation, and file serving. Adding new products to the catalog is out of scope.

</domain>

<decisions>
## Implementation Decisions

### Pricing rules
- Prices stay in EUR — no currency conversion needed (the platform has a built-in currency converter)
- Discount is applied to supplier's RRP (retail price): final_price = RRP × (1 − discount%)
- Per-product discount overrides supplier-level discount when both are set
- Rounding: mathematical rounding (round) to whole numbers (e.g., 169.49 → 169, 169.50 → 170)
- Internal storage as integer cents to avoid floating-point errors (per PRICE-04)

### YML feed content
- YML outputs only price and availability — product creation/addition is handled separately
- Product name taken from prom.ua catalog (not supplier feed)
- Offer ID = prom.ua product ID (so the platform updates the correct product)
- Currency in YML: EUR
- Minimal fields: name, price, availability status

### Feed serving & refresh
- Static file generated on disk (not on-the-fly endpoint)
- File lives on the same hosting as the application
- Atomic write: write to .tmp then rename to prevent partial reads
- YML regenerated immediately after each supplier feed sync (not on a separate schedule)
- File accessible at a stable public URL without authentication

### Availability & edge cases
- Matched product out of stock at supplier → include in YML as "out of stock"
- Product disappeared from supplier feed entirely → mark "out of stock" in YML + flag for operator review (for manual removal from prom.ua)
- Product with zero or missing price → mark "out of stock" + flag for operator review
- Supplier feed fails to load (network error) → do NOT update YML, keep the previous working version

### Claude's Discretion
- Exact YML XML structure and tag names (following prom.ua/Horoshop conventions)
- File path and URL structure for the generated YML
- How operator review flags are stored and surfaced (will be part of dashboard in Phase 4)
- Temporary file naming and cleanup strategy

</decisions>

<specifics>
## Specific Ideas

- Platform (Horoshop/prom.ua) handles EUR→UAH conversion automatically, so we pass EUR prices as-is
- Operator review list for disappeared/zero-price products — this feeds into Phase 4 dashboard

</specifics>

<deferred>
## Deferred Ideas

- Adding new products from supplier feed to prom.ua catalog — separate workflow
- Operator review UI for flagged products — Phase 4 dashboard
- Horoshop-specific field mapping — v2 requirement (HRSH-01)

</deferred>

---

*Phase: 03-pricing-engine-and-yml-output*
*Context gathered: 2026-02-27*
