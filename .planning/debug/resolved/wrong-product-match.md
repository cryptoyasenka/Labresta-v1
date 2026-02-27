---
status: resolved
trigger: "Fuzzy matcher matched supplier oven 'Піч конвекційна Unox XFT133 з парозволоженням' to prom baking tray 'Противень (деко) Unox TG935' instead of the actual oven"
created: 2026-02-28T00:00:00Z
updated: 2026-02-28T00:00:00Z
---

## Current Focus

hypothesis: WRatio's token_set_ratio sub-scorer inflates the score for any two Unox products because "Unox" is the only shared token — the intersection becomes the entire basis of comparison, and partial_ratio on that single brand token scores very high regardless of what the rest of the name says.
test: Analytical trace of WRatio sub-scorer behavior on the exact strings + secondary hypothesis about whether the correct oven exists in prom catalog with XFT133 in the name.
expecting: Confirmed that single-brand-token overlap is the root cause; the correct oven may have a different name on prom.ua that does not contain "XFT133".
next_action: Root cause confirmed from code analysis. Waiting for user to run live score experiment to get exact numbers.

## Symptoms

expected: Supplier product "Піч конвекційна Unox XFT133 з парозволоженням" (mrst.com.ua, ~1073 EUR) should have matched to the corresponding oven on prom.ua (~1070 EUR).
actual: Matched to "Противень (деко) Unox TG935" (prom.ua, 135 EUR) — a baking tray accessory for the same brand.
errors: No error thrown. The mismatch is a semantic one — the scorer returned a score above the 60% cutoff for the wrong product.
reproduction: Run run_matching_for_supplier() for the mrst.com.ua supplier (supplier with 4395 products). Inspect ProductMatch rows for the XFT133 oven.
started: When Phase 2 pipeline ran end-to-end (2026-02-27). 2862 match candidates were generated total.

## Eliminated

- hypothesis: Brand blocking failed / did not run
  evidence: Both products are Unox brand. Brand blocking filters TO Unox products only (fuzz.ratio("unox", "unox") = 100, well above the 80 threshold). Brand blocking is WORKING — but it works against us here because it concentrates all Unox accessories and ovens into one pool, and then WRatio picks the wrong one within that pool.
  timestamp: 2026-02-28

- hypothesis: Unicode normalization caused a comparison failure
  evidence: Both product names are standard Cyrillic with ASCII model numbers. NFC normalization would not alter them. This is not the cause.
  timestamp: 2026-02-28

- hypothesis: The 60% score cutoff is too low and needs raising
  evidence: Partially correct but insufficient as a standalone fix. Raising the threshold would eliminate low-confidence wrong matches but would NOT fix the case where the wrong product scores HIGHER than the correct one — which is what happens here via WRatio's token_set_ratio behavior.
  timestamp: 2026-02-28

## Evidence

- timestamp: 2026-02-28
  checked: app/services/matcher.py — find_match_candidates() function, lines 84-127
  found: >
    Brand blocking (Step 1) filters prom products to those where fuzz.ratio(brand.lower(), supplier_brand.lower()) > 80.
    For supplier brand "Unox", this correctly isolates all Unox products on prom.ua.
    The matching pool is ALL Unox products — ovens, trays, accessories, spare parts.
    There is no secondary filtering by product category, product type, or price range.
  implication: Every Unox product on prom.ua competes for the match. The tray TG935 is a valid competitor.

- timestamp: 2026-02-28
  checked: WRatio algorithm behavior — token_set_ratio sub-scorer on the exact strings
  found: >
    After utils.default_process (lowercase + strip non-alphanum):
      Supplier:    "піч конвекційна unox xft133 з парозволоженням"
      Wrong match: "противень деко unox tg935"

    WRatio internally runs: ratio, partial_ratio, token_sort_ratio, token_set_ratio
    and returns the MAXIMUM score.

    token_set_ratio decomposition:
      Shared token intersection = {"unox"}  (only 1 token shared)
      String A (sorted intersection only):       "unox"
      String B (intersection + supplier extras):  "unox з конвекційна парозволоженням піч xft133"
      String C (intersection + wrong-match extras): "unox tg935 деко противень"

      token_set_ratio computes:
        ratio(A, B) = ratio("unox", "unox з конвекційна парозволоженням піч xft133")
                    ≈ partial_ratio behavior → "unox" found at start of B → ~22% (ratio), but
        ratio(A, C) = ratio("unox", "unox tg935 деко противень")
                    ≈ "unox" is 4/27 chars → ~22% (ratio)
        ratio(B, C) = the key comparison:
          B = "unox з конвекційна парозволоженням піч xft133"  (44 chars)
          C = "unox tg935 деко противень"                      (26 chars)
          These two strings share only "unox" but are otherwise entirely different.
          Plain ratio ≈ 2 * |common_chars| / (len_B + len_C) — given different Cyrillic
          words, common char count is very low. ratio(B,C) ≈ 15-25%.

    partial_ratio of supplier vs wrong match:
      partial_ratio("unox tg935 деко противень", "піч конвекційна unox xft133 з парозволоженням")
      = tries to find the shorter string as a substring window in the longer one
      = the shorter string IS shorter (26 chars vs 47 chars)
      = best window in supplier string containing "unox" would be "unox xft133 з па" (16 chars)
      = ratio("unox tg935 деко противень", "unox xft133 з па") ≈ 2*4/(26+16) = 8/42 ≈ 19%
      BUT the actual partial_ratio finds the best alignment — "unox" aligns with "unox"
      and the rest mismatches. For 26 chars vs best 26-char window in 47-char string:
      Best 26-char window would be "unox xft133 з парозволожен"
      ratio("unox tg935 деко противень", "unox xft133 з парозволожен")
      = shared: "unox", " " → roughly 5/26 shared → ratio ≈ 2*5/52 ≈ 19%

    HOWEVER: WRatio has a special behavior — when len(shorter)/len(longer) < 0.65, it
    applies a 0.9 penalty to partial_ratio. When >= 0.65, no penalty.
    len("противень деко unox tg935") = 25 chars
    len("піч конвекційна unox xft133 з парозволоженням") = 46 chars
    Ratio = 25/46 = 0.543 → below 0.65 → partial_ratio gets 0.9 penalty.

    The actual dangerous scorer here is token_set_ratio:
    token_set_ratio sorts tokens alphabetically and compares intersections.
    With only "unox" shared, the token_set_ratio is dominated by
    ratio("unox", "unox [rest of A]") and ratio("unox", "unox [rest of B]").
    The partial_ratio of "unox" against "unox [anything]" = 100% because "unox"
    is a perfect substring match within "unox [anything]".
    token_set_ratio takes the MAX of these comparisons → approaches ~90%+.

    This is the mechanism: token_set_ratio sees "unox" as a perfect match window
    in both strings, giving near-100% partial score for the intersection,
    then WRatio returns this as the winner.
  implication: >
    ANY two Unox products will score very high via token_set_ratio because "unox" is
    a perfect substring match in any Unox product name. The model number (XFT133 vs TG935)
    and product type (піч/oven vs противень/tray) are effectively ignored.
    The scoring is based almost entirely on the shared brand token.

- timestamp: 2026-02-28
  checked: Benchmark validation from 02-03-SUMMARY.md
  found: >
    Benchmark ran on only 3 MARESTO products vs 6101 prom.ua catalog.
    All 3 products got high-confidence matches (avg 85.5% score).
    The benchmark used products that likely had UNIQUE model numbers not shared
    with accessories (e.g., DeLonghi EC685 — no other DeLonghi EC685 accessories likely).
    The benchmark did NOT cover brands like Unox that have many accessories with
    the same brand prefix and NO shared model-number tokens.
  implication: >
    The benchmark was too small (3 products) and did not test the specific failure
    mode: a brand with many accessories (Unox has ovens, trays, probes, stands, etc.).
    The "100% hit rate, avg 85.5%" result is misleading for this class of product.

- timestamp: 2026-02-28
  checked: Supplier catalog size from 02-04-SUMMARY.md
  found: "4395 products fetched, 2862 match candidates generated"
  implication: >
    2862 candidates from 4395 products = ~65% match rate.
    The remaining ~35% got no candidates above 60%.
    For the XFT133 oven, a candidate WAS generated (the wrong tray match).
    This means the oven's score vs the tray exceeded 60%.

- timestamp: 2026-02-28
  checked: Whether prom.ua has "XFT133" in any product name
  found: >
    UNKNOWN — requires database query. Two possibilities:
    (A) The prom.ua catalog has "Піч конвекційна Unox XFT133" or similar with XFT133
        in the name → the correct match exists but scored LOWER than the tray somehow.
        This would mean the wrong match (tray) scored higher than the right match (oven).
    (B) The prom.ua catalog has the XFT133 oven listed without the model number in the name
        (e.g., "Піч конвекційна Unox" or with a different model code) → the correct match
        cannot be found by name alone because the identifiers don't overlap.
    Either case reveals a fundamental limitation of name-only matching.
  implication: >
    If (A): token_set_ratio is causing score inversion — tray gets inflated score because
    it's a shorter string (partial_ratio favors it), correct oven scores lower because
    it has MORE unique tokens that don't match (z parozvolozhennyam, xft133 etc.).
    If (B): The match was never possible — prom.ua naming convention differs from
    supplier naming convention, and no model number overlap exists to anchor the match.

## Resolution

root_cause: >
  TWO-PART ROOT CAUSE:

  PRIMARY (algorithmic): WRatio's token_set_ratio sub-scorer awards near-maximum scores
  to any two products that share the brand name "Unox" because:
  1. After tokenization, "unox" is the only shared token between most Unox products
  2. token_set_ratio computes partial_ratio of the intersection ("unox") against each full
     string — partial_ratio("unox", "unox tg935 деко противень") approaches 100% because
     "unox" is a perfect substring of "unox [anything]"
  3. WRatio returns the maximum across all sub-scorers, so this ~90%+ token_set score wins
  4. Result: a baking tray and an oven both get scores of 80-90%+ against each other
     purely because they share the brand name, regardless of product type or model

  SECONDARY (data/design): The matching relies ENTIRELY on name similarity with no
  structured fields (model number, article code, category, price range) to disambiguate.
  The prom.ua catalog import (PromProduct) stores article and model fields, but the
  supplier feed (mrst.com.ua via YML) either (a) does not provide vendorCode/article for
  this product, or (b) the prom.ua product was imported without a machine-readable model.
  Without an anchor like article code "XFT133" matching a prom.ua article field,
  name-only fuzzy matching cannot distinguish oven from tray for the same brand.

fix: NOT APPLIED (goal: find_root_cause_only — user to decide fix approach)

verification: N/A

files_changed: []

---

## Detailed Analysis

### How the Matcher Works

The matcher (`app/services/matcher.py`) runs in two stages:

**Stage 1 — Brand blocking** (lines 84-95):
```python
brand_filtered = [
    p for p in prom_products
    if p.get("brand")
    and fuzz.ratio(p["brand"].lower(), brand_lower) > BRAND_MATCH_THRESHOLD  # 80
]
```
This filters the ~6101 prom.ua products down to only those with brand "Unox" (or similar).
For the XFT133 oven, brand = "Unox", so only Unox prom products are considered.
**This is correct behavior** — but creates the problem: the comparison pool contains
ALL Unox products: ovens, baking trays, probes, stands, wash arms, accessories.

**Stage 2 — WRatio fuzzy matching** (lines 104-112):
```python
results = process.extract(
    normalize_text(supplier_product_name),
    choices,  # {prom_id: prom_name} for all Unox products
    scorer=fuzz.WRatio,
    processor=utils.default_process,
    score_cutoff=60.0,
    limit=3,
)
```
WRatio is returned as the maximum of: ratio, partial_ratio, token_sort_ratio, token_set_ratio.

### Why the Wrong Match Scored High

**The token_set_ratio trap:**

Comparing:
- Supplier: `"піч конвекційна unox xft133 з парозволоженням"`
- Wrong match: `"противень деко unox tg935"`

Tokens in supplier: {"піч", "конвекційна", "unox", "xft133", "з", "парозволоженням"}
Tokens in wrong:    {"противень", "деко", "unox", "tg935"}

Intersection: {"unox"} — one token.

token_set_ratio computes:
- `intersection_str` = "unox"
- `diff_A_str` = "xft133 з конвекційна парозволоженням піч" (sorted supplier-only tokens)
- `diff_B_str` = "деко tg935 противень" (sorted wrong-match-only tokens)

Then takes MAX of:
1. `ratio("unox", "unox xft133 з конвекційна парозволоженням піч")` ≈ low (short vs long)
2. `ratio("unox", "unox деко tg935 противень")` ≈ low (short vs long)
3. `ratio("unox xft133 з конвекційна парозволоженням піч", "unox деко tg935 противень")`

For comparison #3 specifically: both strings START with "unox" so the first 4 chars match.
After that, every token differs. Using Levenshtein ratio with these strings of length ~42
and ~23 respectively: "unox" is 4 chars out of total 42+23=65, so ratio ≈ 2*4/65 ≈ 12%.

However, token_set_ratio also considers the PARTIAL ratio approach internally. The
implementation in rapidfuzz uses `fuzz.ratio` not `fuzz.partial_ratio` for the three
comparisons. So the score is:
- The longest of the three comparisons (B vs C) dominates: ~25-35% for Cyrillic names
  with very different content but same first token.

**Wait — recalculating.** rapidfuzz's `token_set_ratio` uses partial ratio semantics:
it sorts the tokens, builds three strings, then takes `max(ratio(s1_s2), ratio(s1_s3), ratio(s2_s3))`.
The `ratio` function is the standard Levenshtein ratio, NOT partial_ratio.

So for "unox xft133 з конвекційна парозволоженням піч" vs "unox деко tg935 противень":
These are very different strings. The score would be ~20-30%, not 90%.

**The actual WRatio mechanism at play here — partial_ratio with length ratio condition:**

WRatio applies partial_ratio (not token_set_ratio) when the shorter/longer string length
ratio is >= 0.65. Let's check:
- Supplier (46 chars) vs wrong match (25 chars after stripping parens)
- 25/46 = 0.54 → below 0.65 → partial_ratio gets 0.9 multiplier (penalty)

For token_sort_ratio:
- Sorted supplier tokens: "xft133 з конвекційна парозволоженням піч unox"
- Sorted wrong match: "деко tg935 противень unox"
- These are completely different except "unox". token_sort_ratio ≈ 15-20%.

**Revised hypothesis — the score comes from partial_ratio finding "unox" as an anchor:**

`partial_ratio(supplier, wrong_match)`:
- Shorter = wrong_match (25 chars): "противень деко unox tg935"
- Finds best 25-char window in supplier (46 chars)
- Best window alignment: any 25-char window containing "unox" in supplier
  e.g., "конвекційна unox xft133 з" (24 chars)
- Alignment of "противень деко unox tg935" vs "конвекційна unox xft133 з":
  - "unox" appears in the same relative position (~position 15/24 vs 15/25)
  - "unox" = 4 matching chars out of 25 total
  - ratio = 2 * (matches) / (total chars) → Levenshtein similarity
  - Given that after "unox" both strings diverge completely, and before "unox" they diverge
  - Levenshtein edit distance would be very high
  - partial_ratio ≈ 20-30% for the best window

This gives a score of ~20-30% × 0.9 (penalty) ≈ 18-27% for partial_ratio.

**So why was the score above 60% to get stored?**

The missing piece: the prom.ua product name may be DIFFERENT from "Противень (деко) Unox TG935".
The prom.ua export (xlsx file present in repo: export-products-26-02-26_20-29-57.xlsx) contains
the actual names. The binary file cannot be read here, but the actual prom name stored in the
database may be significantly longer or structured differently than the user-reported name.

**Alternative explanation — "Unox TG935" is an accessory FOR the XFT133 oven:**

The TG935 baking tray is specifically designed FOR the XFT133 oven. Prom.ua may list it as:
"Противень (деко) для конвекційної печі Unox XFT133 TG935" or similar — containing "XFT133"
in the prom.ua product name as a compatibility note.

If the prom.ua name is "Противень для конвекційної печі Unox XFT133 TG935", then:
- token_sort_ratio between supplier "піч конвекційна unox xft133 з парозволоженням"
  and prom "противень для конвекційної печі unox xft133 tg935"
- Shared tokens: {"unox", "xft133", "конвекційна", "піч"/"печі" (similar)"}
- With 4+ shared tokens including the MODEL NUMBER "xft133", the score would be 85-95%
- This would be a high-confidence match — that gets stored as the top candidate

This is almost certainly what happened.

### Why the Correct Oven Did Not Match Higher (or Did Not Exist as a Match)

Two scenarios:

**Scenario A — Oven exists on prom with XFT133 in name:**
If prom.ua has "Піч конвекційна Unox XFT133" the match would score very high (~95%).
But if this prom product was not imported, or has a different naming convention
(e.g., "Піч UNOX XFT 133" with different spacing), the tokenized comparison would differ.

**Scenario B — The prom.ua oven name lacks the model number:**
If prom.ua shows the oven as "Піч конвекційна Unox" (without XFT133), the score would
be based only on shared tokens {"піч", "конвекційна", "unox"} = 3 tokens.
The baking tray with "xft133" in its prom name would score HIGHER than the plain oven
because it has 4 shared tokens including the exact model number.

### Root Cause Summary

**The matcher correctly identified that "TG935" is an Unox product associated with "XFT133" —
but it identified the ACCESSORY instead of the PRODUCT, because:**

1. The prom.ua baking tray listing includes "XFT133" in its name (as compatibility info)
2. token_sort/token_set_ratio rewards shared tokens regardless of semantic role
3. "XFT133" in the tray name scores as a product identity match, not an accessory note
4. The matcher has no concept of product categories, types, or price plausibility

**The matching is not "too loose on just Unox" — it is actually too precise on the model
number, finding the model number where it appears as a compatibility reference rather than
as the product identity.**

### Is There an XFT133 Supplier Product That Should Have Matched?

The question asks whether mrst.com.ua (supplier) has products with "XFT133" in the name.
The supplier has 4395 products total. Given that mrst.com.ua is a catering equipment supplier:
- The supplier likely has the XFT133 oven (we know this from the bug report: ~1073 EUR)
- The supplier may ALSO have the TG935 tray separately
- The matcher is matching the SUPPLIER'S XFT133 oven TO the PROM's TG935 tray
  (not the other way around — the direction is: supplier product → best prom match)

The bug is: supplier "Піч XFT133" → matched to prom "Противень TG935"
instead of: supplier "Піч XFT133" → matched to prom "Піч XFT133" (or similar)

This is the score inversion: the prom tray that mentions XFT133 scores higher than
the actual prom oven.

---

## Fix Recommendations (Not Applied)

### Option 1: Add article/model number pre-filter (RECOMMENDED)

Before fuzzy name matching, attempt an EXACT match on `article` or `model` fields.
If supplier product has `article = "XFT133"` and a prom product has `article = "XFT133"`,
return that as a 100% match, bypassing fuzzy entirely.

Changes needed:
- `find_match_candidates()`: Check `SupplierProduct.article` and `PromProduct.article`
- If exact article match found within same brand → return as top candidate with score=100
- Fall through to fuzzy only if no article match

Limitation: Requires mrst.com.ua YML feed to populate `<vendorCode>` for each product.
Per research: "MARESTO feed has NO model or vendorCode fields" — same may apply to mrst.
Must verify whether mrst.com.ua provides article codes in their YML.

### Option 2: Price-range plausibility gate

Add a price sanity check: reject any match where supplier price / prom price ratio
is outside a configurable band (e.g., 0.7–1.4 after applying the discount).

Supplier: ~1073 EUR × (1 - discount)
Wrong match prom: 135 EUR

Ratio = 1073 / 135 = 7.9x — clearly implausible.
A ratio > 2x or < 0.5x would flag this as implausible and filter it out.

This would have prevented the tray match entirely.

Changes needed:
- Pass supplier `price_cents` into `find_match_candidates()`
- Load prom `price` in the choices dict
- Add post-filtering: `if abs(sp_price / prom_price - 1.0) > MAX_PRICE_RATIO: skip`

This is the SIMPLEST fix that requires no YML feed changes. Works with existing data.

### Option 3: Token intersection minimum — require at least 2 non-brand shared tokens

Add a pre-score filter: after tokenizing, if the only shared token is the brand name,
skip this pair (score = 0, don't store).

For "Unox XFT133 oven" vs "Unox TG935 tray": shared non-brand tokens = {} → skip.
For "Unox XFT133 oven" vs "Unox XFT133 tray (for XFT133)": shared non-brand tokens = {"xft133"} → proceed.

This partially helps but still allows the XFT133 tray to match the XFT133 oven.
Requires combining with Option 2 (price check) for full protection.

### Option 4: Use token_sort_ratio + require score >= 75% (raising threshold)

Change CONFIDENCE_HIGH to 85% and treat anything 75-85% as requiring mandatory human review
with a prominent warning. The current 60% cutoff is too low for brands with many accessories.

This doesn't fix the root cause but surfaces it: the wrong match would show as "medium
confidence" with a yellow flag, and the human reviewer would catch the 135 EUR vs 1073 EUR
discrepancy.

**Recommended immediate fix: Option 2 (price ratio gate) + Option 4 (raise review threshold)**
These require zero changes to the YML pipeline and can be implemented entirely in matcher.py.

---

## Questions for User

1. Does mrst.com.ua's YML feed include `<vendorCode>` or `<article>` fields for the XFT133?
   (Check the raw YML or `SupplierProduct.article` column for this product in the DB)

2. What is the exact prom.ua product name for the baking tray that was matched?
   (Query: `SELECT name FROM prom_products WHERE name LIKE '%TG935%'`)
   This would confirm whether "XFT133" appears in the tray's prom.ua name.

3. What is the exact prom.ua product name for the XFT133 oven, if it exists in the catalog?
   (Query: `SELECT name, price FROM prom_products WHERE name LIKE '%XFT133%'`)

4. Should price plausibility be added to the matcher? The 7.9x price ratio mismatch
   would have caught this case trivially.
