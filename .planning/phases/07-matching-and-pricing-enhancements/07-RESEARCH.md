# Phase 7: Matching and Pricing Enhancements - Research

**Researched:** 2026-03-01
**Domain:** Sync pipeline rule-matching + per-product discount UI
**Confidence:** HIGH

## Summary

This phase adds two features to the existing system: (1) automatic match confirmation via MatchRule during sync, and (2) a per-product discount override UI. Both features build on infrastructure that already exists -- `MatchRule` model is fully defined but never consumed, `ProductMatch.discount_percent` column exists but has no write path, and `pricing.py`'s `get_effective_discount()` already implements the fallback logic consumed by `yml_generator.py`.

The rule-apply step is a new stage inserted into `sync_pipeline.py` before the fuzzy matching call (Stage 5). It queries active `MatchRule` rows, matches them against the current supplier product set (exact name + optional brand), and creates `ProductMatch` records with `status="confirmed"` and `confirmed_by="rule:{rule_id}"`. Since `run_matching_for_supplier()` already skips products with confirmed/manual status, auto-confirmed products will naturally be excluded from fuzzy matching.

The discount UI adds an AJAX endpoint for setting `discount_percent` on a `ProductMatch`, plus front-end changes: a discount column in the review table and a discount input field in the detail panel with live price preview. The `yml_generator.py` already calls `get_effective_discount(match.discount_percent, supplier.discount_percent)`, so no changes are needed in YML output logic.

**Primary recommendation:** Implement as two independent work streams -- (1) rule-apply in sync pipeline with backend tests, (2) discount UI with AJAX endpoint and front-end changes. No new libraries needed; all changes use existing stack.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **Exact name match only** -- MatchRule.supplier_product_name_pattern compared exactly against SupplierProduct.name (no fuzzy/pattern matching)
- **Brand check included** -- if rule has supplier_brand set, both name AND brand must match; if brand is NULL on the rule, name-only match
- **Pipeline position: before fuzzy matching** -- new step in sync pipeline runs rule matching first, then fuzzy matching runs only for products WITHOUT a rule match
- **Stale rules (deleted prom products)** -- skip the rule silently, log a warning, product falls through to fuzzy matching; rule stays active for if product returns
- **Status: 'confirmed'** -- rule-applied matches get the same status as manually confirmed matches (per success criteria)
- **Visual indicator** -- small icon or label next to the 'confirmed' badge to distinguish auto-confirmed from human-confirmed
- **confirmed_by stores 'rule:{rule_id}'** -- enables traceability back to which exact rule auto-confirmed the match
- **Undo: same as any confirmed match** -- operator can reject auto-confirmed matches using existing reject flow; the rule stays active for next sync
- **Location: detail panel** -- discount field added to the right-side detail panel that appears when a match row is selected
- **Visibility: confirmed/manual matches only** -- discount field only appears for matches with status confirmed or manual
- **Range: 0-100%** with visual warning for unusual values (>50% or 0%)
- **Live price preview** -- when operator types a discount, show calculated price instantly: supplier price x (1 - discount%) = X EUR
- **Clear button** -- 'Сбросить' button next to discount input, sets discount_percent back to NULL; supplier default discount shown as placeholder in the input field
- **Separate discount column** -- new column in the review table showing the effective discount % for each match
- **Default shown in gray** -- matches without custom discount show the supplier's default discount % in muted/gray text
- **Custom overrides highlighted** -- custom discount values displayed in normal/bold text to stand out
- **Расч. цена uses effective discount** -- calculated price column always uses get_effective_discount() logic (custom if set, supplier default otherwise) -- matches YML output
- **No filter/sort needed** -- discount column is display-only
- confirmed_by format: `rule:{rule_id}` (e.g., `rule:42`) for traceability
- Discount input should show supplier default as placeholder text so operator knows what they're overriding
- Live price calculation should use the same `calculate_price_eur` + `get_effective_discount` functions as YML generator for consistency

### Claude's Discretion
- Exact icon/styling for auto-confirmed indicator
- Warning threshold for unusual discounts
- Detail panel layout and field positioning
- Input debounce timing for live price preview

### Deferred Ideas (OUT OF SCOPE)
None -- discussion stayed within phase scope
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| MTCH-01 | MatchRule is automatically applied during sync -- products with rules get confirmed match without fuzzy step | Rule-apply function in sync pipeline before Stage 5; MatchRule model already exists with all needed fields; run_matching_for_supplier() already skips confirmed products |
| PRC-01 | Operator can set individual discount (discount_percent) for a specific product through matches UI | ProductMatch.discount_percent column already exists; pricing.py already has get_effective_discount(); yml_generator.py already consumes it; needs AJAX endpoint + detail panel UI |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Flask | existing | Web framework | Already in project |
| SQLAlchemy | existing | ORM / database | Already in project |
| Jinja2 | existing | Templates | Already in project |
| Bootstrap 5 | existing | UI framework | Already in project |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| Split.js | existing | Resizable panel layout | Already loaded in review page |

### Alternatives Considered
None -- no new libraries required. All changes use existing stack.

**Installation:**
No new packages needed.

## Architecture Patterns

### Recommended Project Structure
No new files needed. Changes go into existing files:
```
app/
├── services/
│   ├── sync_pipeline.py      # Add rule-apply step before Stage 5
│   └── rule_matcher.py       # NEW: rule-apply logic (pure function, testable)
├── views/
│   └── matches.py            # Add discount AJAX endpoint
├── templates/matches/
│   └── review.html           # Add discount column + detail panel discount input
└── static/js/
    └── matches.js            # Add discount input handling + live preview
```

### Pattern 1: Rule-Apply as Separate Service Module
**What:** Extract rule matching into `app/services/rule_matcher.py` as a pure function
**When to use:** Keeps sync_pipeline.py clean and makes rule logic independently testable
**Example:**
```python
# app/services/rule_matcher.py
def apply_match_rules(supplier_id: int) -> int:
    """Apply active MatchRules to unmatched supplier products.

    Returns count of auto-confirmed matches created.
    """
    # 1. Get active rules with valid prom products
    rules = MatchRule.query.filter_by(is_active=True).all()

    # 2. Get supplier products that don't have confirmed/manual matches
    # (reuse same exclusion logic as run_matching_for_supplier)

    # 3. For each unmatched product, check against rules:
    #    - Exact name match: sp.name == rule.supplier_product_name_pattern
    #    - Brand match (if rule has brand): sp.brand == rule.supplier_brand

    # 4. Create ProductMatch with status='confirmed',
    #    confirmed_by=f'rule:{rule.id}', confirmed_at=utcnow, score=100.0

    # 5. Handle stale rules: if rule.prom_product is deleted, skip + log warning
```

### Pattern 2: AJAX Discount Endpoint Following Existing Conventions
**What:** New POST endpoint at `/matches/<id>/discount` using `fetchWithCSRF` pattern
**When to use:** Matches existing confirm/reject endpoint pattern in matches.py
**Example:**
```python
@matches_bp.route("/<int:match_id>/discount", methods=["POST"])
@login_required
def set_discount(match_id):
    match = db.get_or_404(ProductMatch, match_id)
    data = request.get_json()
    discount = data.get("discount_percent")

    if discount is not None:
        discount = float(discount)
        if not (0 <= discount <= 100):
            return jsonify({"status": "error", "message": "..."}), 400

    match.discount_percent = discount  # None clears override
    db.session.commit()
    return jsonify({"status": "ok", "discount_percent": match.discount_percent})
```

### Pattern 3: Detail Panel Conditional Sections
**What:** Show discount input only for confirmed/manual matches, using data attributes
**When to use:** Extends existing `showMatchDetail()` function in matches.js
**Example:**
```javascript
// In showMatchDetail(), add discount section after status display:
if (status === 'confirmed' || status === 'manual') {
    html += '<div class="mb-3">' +
        '<h6 class="text-muted mb-1">Скидка</h6>' +
        '<div class="input-group input-group-sm">' +
        '  <input type="number" id="discountInput" class="form-control" ' +
        '    min="0" max="100" step="0.1" placeholder="' + supplierDefault + '%">' +
        '  <span class="input-group-text">%</span>' +
        '  <button class="btn btn-outline-secondary" id="clearDiscountBtn">Сбросить</button>' +
        '</div>' +
        '<div id="pricePreview" class="mt-1 small text-muted"></div>' +
        '</div>';
}
```

### Anti-Patterns to Avoid
- **Modifying run_matching_for_supplier() for rule logic:** Keep rule matching separate; fuzzy matching should not know about rules
- **Inline rule matching in sync_pipeline.py:** Extract to a service function for testability
- **Re-implementing price calculation in JavaScript:** Use same formula as pricing.py for consistency (supplier_price * (1 - discount/100)), but note JS does not need integer-cent math for preview -- float approximation is fine for display
- **Querying MatchRule inside the fuzzy matching loop:** Apply rules in a batch before fuzzy runs; fuzzy matcher already skips confirmed products naturally

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| CSRF protection | Manual token handling | Existing `fetchWithCSRF()` in common.js | Already standardized across project |
| Price calculation | JS re-implementation | Same formula as `pricing.py`: `price * (1 - discount/100)` | Must match YML output exactly |
| Input debounce | Custom timer code | Simple setTimeout pattern (already used in catalog search) | Proven pattern in matches.js |

**Key insight:** Almost everything needed already exists in the codebase. The risk is not building new things -- it's incorrectly wiring existing pieces.

## Common Pitfalls

### Pitfall 1: YML Generator Only Queries status='confirmed'
**What goes wrong:** The YML generator at `yml_generator.py:40` only includes `ProductMatch.status == "confirmed"`. If auto-confirmed matches used a different status, they would not appear in the YML feed.
**Why it happens:** Temptation to create a new status like "auto_confirmed" or "rule_confirmed".
**How to avoid:** Use `status='confirmed'` exactly as the user decided. Distinguish via `confirmed_by` field using `rule:{rule_id}` format.
**Warning signs:** Any discussion of a new status value.

### Pitfall 2: Stale PromProduct Reference in MatchRule
**What goes wrong:** A MatchRule references a `prom_product_id` that has been deleted from the catalog. Creating a ProductMatch with that FK would fail.
**Why it happens:** PromProduct catalog is re-imported periodically; products can disappear.
**How to avoid:** Before creating the auto-confirmed ProductMatch, verify the PromProduct still exists. If not, log a warning and skip. The rule stays active.
**Warning signs:** IntegrityError on ProductMatch insert during sync.

### Pitfall 3: Duplicate ProductMatch Records
**What goes wrong:** A rule matches a product that already has a candidate/rejected match for the same prom_product_id pair. The `uq_match_pair` unique constraint would fail.
**Why it happens:** Rule matching runs before fuzzy, but previous sync cycles may have created candidate matches.
**How to avoid:** Check for existing ProductMatch with the same supplier_product_id/prom_product_id pair. If a candidate exists, update it to confirmed. If a rejected match exists, skip (operator explicitly rejected this pairing).
**Warning signs:** UniqueConstraint violation during sync.

### Pitfall 4: Calculated Price Column Not Using Effective Discount
**What goes wrong:** The review.html "Расч. цена" column currently does a naive calculation that doesn't use `get_effective_discount()`. It shows `price * (1 - match.discount_percent/100)` only if `discount_percent` is set, otherwise shows raw price.
**Why it happens:** The template was written before discount functionality was planned.
**How to avoid:** Pass supplier default discount to the template (via relationship: `match.supplier_product.supplier.discount_percent`). Calculate effective discount in the template: `discount_percent if discount_percent is not none else supplier.discount_percent`.
**Warning signs:** Price shown in review table doesn't match YML output.

### Pitfall 5: Race Condition in Discount Save
**What goes wrong:** If operator rapidly clicks "Сбросить" and types a new value, multiple AJAX requests fire and the final state may not be what the user intended.
**Why it happens:** No debounce on the discount save action.
**How to avoid:** Debounce the save (300-500ms). Disable the input during save. Show a brief spinner/feedback.
**Warning signs:** Discount value flickering or reverting.

### Pitfall 6: Rule Re-Application on Subsequent Syncs
**What goes wrong:** On each sync, the rule-apply step runs again. If a previously auto-confirmed match was rejected by the operator, the rule would re-create it as confirmed.
**Why it happens:** Rule matching doesn't check if the operator has already reviewed (and rejected) this pairing.
**How to avoid:** Before creating an auto-confirmed match, check if a ProductMatch with this supplier_product_id + prom_product_id pair was previously rejected (check `status='rejected'` or deleted). Since rejected matches are deleted (not status-updated), track this by checking: if a ProductMatch with `status='confirmed'` and `confirmed_by LIKE 'rule:%'` was already created and no longer exists, it was likely rejected. Simpler approach: only apply rules to products with NO existing ProductMatch record at all (no candidate, no confirmed, no manual).
**How the current code handles it:** `run_matching_for_supplier()` skips products with confirmed/manual matches. The rule-apply function should similarly skip products that already have ANY ProductMatch record (including candidates), since candidates mean fuzzy already found something.

## Code Examples

Verified patterns from the existing codebase:

### Existing AJAX Confirm Pattern (matches.py)
```python
# Source: app/views/matches.py:102-114
@matches_bp.route("/<int:match_id>/confirm", methods=["POST"])
@login_required
def confirm_match(match_id):
    match = db.get_or_404(ProductMatch, match_id)
    match.status = "confirmed"
    match.confirmed_at = datetime.now(timezone.utc)
    match.confirmed_by = current_user.name
    current_user.matches_processed += 1
    db.session.commit()
    return jsonify({"status": "ok", "new_status": "confirmed"})
```

### Existing Manual Match with Rule Creation (matches.py)
```python
# Source: app/views/matches.py:270-278
# Shows how MatchRule is created from a manual match
if remember:
    rule = MatchRule(
        supplier_product_name_pattern=supplier_product.name,
        supplier_brand=supplier_product.brand,
        prom_product_id=prom_product_id,
        created_by=current_user.name,
    )
    db.session.add(rule)
```

### Existing Fuzzy Matcher Skip Logic (matcher.py)
```python
# Source: app/services/matcher.py:391-399
# Shows how confirmed/manual products are skipped -- rule-apply uses same pattern
matched_ids_query = (
    select(ProductMatch.supplier_product_id)
    .where(ProductMatch.status.in_(["confirmed", "manual"]))
    .distinct()
)
matched_ids = set(db.session.execute(matched_ids_query).scalars().all())
```

### Existing Discount Logic in YML Generator (yml_generator.py)
```python
# Source: app/services/yml_generator.py:77-81
# Already consumes get_effective_discount -- no changes needed
effective_discount = get_effective_discount(
    match.discount_percent, supplier.discount_percent
)
if price_valid:
    price_eur = calculate_price_eur(sp.price_cents, effective_discount)
```

### Existing Detail Panel Rendering (matches.js)
```javascript
// Source: app/static/js/matches.js:238-280
// showMatchDetail() builds HTML from data attributes on the row
// Discount input will be appended here, conditionally on status
function showMatchDetail(row) {
    var status = row.getAttribute('data-status') || '-';
    // ... builds detailContent.innerHTML
}
```

### Review Table Data Attributes (review.html)
```html
<!-- Source: app/templates/matches/review.html:122-132 -->
<!-- Each row stores data for the detail panel; need to add discount data -->
<tr data-match-id="{{ match.id }}"
    data-supplier-id="{{ match.supplier_product.id }}"
    data-supplier-name="{{ match.supplier_product.name }}"
    data-supplier-price="..."
    data-prom-name="{{ match.prom_product.name }}"
    data-score="{{ '%.0f'|format(match.score) }}"
    data-status="{{ match.status }}">
```

## Key Implementation Details

### Data Attributes Needed on Review Table Rows
The detail panel and discount logic need additional data attributes on each `<tr>`:
- `data-discount-percent` -- current per-product discount (empty string if NULL)
- `data-supplier-default-discount` -- supplier's default discount_percent
- `data-confirmed-by` -- to show rule indicator icon

### Review Table "Расч. цена" Column Fix
The current template (review.html lines 143-150) has a broken calculated price display. It only applies `match.discount_percent` and falls back to raw price. It should use effective discount:
```jinja2
{% set eff_discount = match.discount_percent if match.discount_percent is not none
   else match.supplier_product.supplier.discount_percent %}
{% if match.supplier_product.price_cents is not none %}
    {{ "%.2f"|format(match.supplier_product.price_cents / 100 * (1 - eff_discount / 100)) }} {{ match.supplier_product.currency }}
{% endif %}
```

### Sync Pipeline Integration Point
The rule-apply step goes between Stage 4 (detect disappeared) and Stage 5 (fuzzy matching) in `sync_pipeline.py:188-195`:
```python
# Stage 4.5: Apply match rules (before fuzzy)
logger.info("Stage 4.5/6: Applying match rules")
from app.services.rule_matcher import apply_match_rules
rules_applied = apply_match_rules(supplier.id)
sync_run.rules_applied = rules_applied  # Optional: track in SyncRun
logger.info("Match rules applied: %d auto-confirmed", rules_applied)

# Stage 5: Run fuzzy matching (unchanged -- skips auto-confirmed)
```

Note: The stage numbering changes from "X/6" to "X/7" if a new stage is added. Alternatively, keep it as 6 stages and call the rule step "Stage 4.5" or renumber.

### MatchRule Has No supplier_id Field
The `MatchRule` model does NOT have a `supplier_id` field. Rules are matched by product name/brand, not by supplier. This means:
- A rule created from Supplier A's product "Widget X" will also match Supplier B's product named "Widget X"
- This is the correct behavior for the user's use case (same product from different suppliers maps to same prom product)
- The rule-apply function should iterate all active rules and match against supplier products by name/brand, not filter rules by supplier

## Open Questions

1. **SyncRun tracking of auto-confirmed matches**
   - What we know: SyncRun has `match_candidates_generated` for fuzzy results
   - What's unclear: Should there be a separate field like `rules_applied` for tracking auto-confirmed count?
   - Recommendation: Add it if trivial (just an Integer column), skip if it requires migration complexity. Log the count either way.

2. **Manual matches not in YML feed**
   - What we know: `yml_generator.py` only queries `status == "confirmed"`, not `"manual"`. Manual matches are excluded from YML output.
   - What's unclear: Is this intentional? The discount UI targets confirmed AND manual matches.
   - Recommendation: This is a pre-existing behavior, not Phase 7 scope. Note it but don't fix unless user requests. The discount UI should still work for manual matches (discount_percent is saved even if the match isn't in YML yet).

## Sources

### Primary (HIGH confidence)
- Codebase analysis: `app/models/match_rule.py` -- MatchRule model fields verified
- Codebase analysis: `app/models/product_match.py` -- discount_percent column exists, confirmed_by field exists
- Codebase analysis: `app/services/pricing.py` -- get_effective_discount() and calculate_price_eur() verified
- Codebase analysis: `app/services/yml_generator.py` -- already calls get_effective_discount(), only queries status='confirmed'
- Codebase analysis: `app/services/matcher.py` -- run_matching_for_supplier() skip logic verified
- Codebase analysis: `app/services/sync_pipeline.py` -- Stage 5 integration point identified
- Codebase analysis: `app/views/matches.py` -- AJAX endpoint patterns verified
- Codebase analysis: `app/static/js/matches.js` -- showMatchDetail() and fetchWithCSRF patterns verified
- Codebase analysis: `app/templates/matches/review.html` -- detail panel, data attributes, calculated price column verified

### Secondary (MEDIUM confidence)
- None needed -- all research is codebase-internal

### Tertiary (LOW confidence)
- None

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- no new libraries, all existing
- Architecture: HIGH -- clear integration points identified in codebase, all models/services verified
- Pitfalls: HIGH -- identified from direct code analysis (FK constraints, status values, existing skip logic)

**Research date:** 2026-03-01
**Valid until:** 2026-03-31 (stable -- internal codebase, no external dependencies)
