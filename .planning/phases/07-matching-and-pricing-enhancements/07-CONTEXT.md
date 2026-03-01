# Phase 7: Matching and Pricing Enhancements - Context

**Gathered:** 2026-03-01
**Status:** Ready for planning

<domain>
## Phase Boundary

Two enhancements to the existing matching and pricing system:
1. **MatchRule auto-apply** (MTCH-01): During sync, products with existing MatchRule entries are automatically confirmed without going through fuzzy matching
2. **Per-product discount UI** (PRC-01): Operator can set/clear an individual discount override on confirmed matches through the matches UI

Out of scope: new matching algorithms, bulk discount operations, discount templates, CSV import of discounts.

</domain>

<decisions>
## Implementation Decisions

### Rule auto-apply logic
- **Exact name match only** — MatchRule.supplier_product_name_pattern compared exactly against SupplierProduct.name (no fuzzy/pattern matching)
- **Brand check included** — if rule has supplier_brand set, both name AND brand must match; if brand is NULL on the rule, name-only match
- **Pipeline position: before fuzzy matching** — new step in sync pipeline runs rule matching first, then fuzzy matching runs only for products WITHOUT a rule match
- **Stale rules (deleted prom products)** — skip the rule silently, log a warning, product falls through to fuzzy matching; rule stays active for if product returns

### Auto-match visibility
- **Status: 'confirmed'** — rule-applied matches get the same status as manually confirmed matches (per success criteria)
- **Visual indicator** — small icon or label next to the 'confirmed' badge to distinguish auto-confirmed from human-confirmed
- **confirmed_by stores 'rule:{rule_id}'** — enables traceability back to which exact rule auto-confirmed the match
- **Undo: same as any confirmed match** — operator can reject auto-confirmed matches using existing reject flow; the rule stays active for next sync

### Discount input UI
- **Location: detail panel** — discount field added to the right-side detail panel that appears when a match row is selected
- **Visibility: confirmed/manual matches only** — discount field only appears for matches with status confirmed or manual
- **Range: 0-100%** with visual warning for unusual values (>50% or 0%)
- **Live price preview** — when operator types a discount, show calculated price instantly: supplier price x (1 - discount%) = X EUR
- **Clear button** — 'Сбросить' button next to discount input, sets discount_percent back to NULL; supplier default discount shown as placeholder in the input field

### Discount display
- **Separate discount column** — new column in the review table showing the effective discount % for each match
- **Default shown in gray** — matches without custom discount show the supplier's default discount % in muted/gray text
- **Custom overrides highlighted** — custom discount values displayed in normal/bold text to stand out
- **Расч. цена uses effective discount** — calculated price column always uses get_effective_discount() logic (custom if set, supplier default otherwise) — matches YML output
- **No filter/sort needed** — discount column is display-only

### Claude's Discretion
- Exact icon/styling for auto-confirmed indicator
- Warning threshold for unusual discounts
- Detail panel layout and field positioning
- Input debounce timing for live price preview

</decisions>

<specifics>
## Specific Ideas

- confirmed_by format: `rule:{rule_id}` (e.g., `rule:42`) for traceability
- Discount input should show supplier default as placeholder text so operator knows what they're overriding
- Live price calculation should use the same `calculate_price_eur` + `get_effective_discount` functions as YML generator for consistency

</specifics>

<code_context>
## Existing Code Insights

### Reusable Assets
- `MatchRule` model (`app/models/match_rule.py`): Already has supplier_product_name_pattern, supplier_brand, prom_product_id, is_active, created_by — fully ready for consumption
- `ProductMatch.discount_percent` column: Already exists (Float, nullable), NULL = use supplier default
- `pricing.py`: `get_effective_discount()` and `calculate_price_eur()` already implement the fallback logic correctly
- `yml_generator.py`: Already calls `get_effective_discount(match.discount_percent, supplier.discount_percent)` — no changes needed for YML output
- Detail panel (`#matchDetailPanel` in review.html): Existing right-side panel, currently shows "select row for details"

### Established Patterns
- AJAX with `fetchWithCSRF` for match actions (confirm/reject/manual) in `matches.js`
- Status badges with Bootstrap classes (bg-success, bg-danger, etc.)
- Manual match creates MatchRule when "remember" checkbox is checked (`app/views/matches.py:270-278`)
- Confirmed matches set `confirmed_at` and `confirmed_by` fields

### Integration Points
- `sync_pipeline.py` Stage 5: Insert rule-apply step before `run_matching_for_supplier()` call
- `run_matching_for_supplier()` already skips products with confirmed/manual status — auto-confirmed matches will naturally be skipped
- `matches.py` needs new AJAX endpoint for setting/clearing discount
- `review.html` needs discount column in table + discount input in detail panel

</code_context>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 07-matching-and-pricing-enhancements*
*Context gathered: 2026-03-01*
