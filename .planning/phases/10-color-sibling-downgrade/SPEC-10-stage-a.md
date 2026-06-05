# SPEC-10 Stage A — Colorless-SP → Color-Sibling Downgrade

**Status:** SPEC ONLY (read-only design). Not implemented. Decision needed from Yana before coding.
**Author run:** night maintenance, 2026-06-05. No code or DB was modified.
**Scope:** `app/services/matcher.py` (and one new test file). Sibling of Step 4.88 (Stage B).

---

## 1. Problem

The catalog (`prom_products`) frequently stores the same base model as several
rows that differ **only by a paint color** — e.g. GoodFood BL160 ships as 6 rows
(BLACK / WHITE / RED / BLUE / YELLOW / CARAMEL). When a supplier row
(`supplier_products`) has **no color token at all**, matching it confidently to
**one specific colored sibling** is arbitrary — the colorless SP could equally be
any sibling in the cluster.

Stage B (Step 4.88, DONE) only fires when **both** sides expose colors that
*discord*. It deliberately passes the colorless-SP case — its own code comment
(matcher.py:1696-1698) says:

> "If one side has no color, pass — that side may be a base/uncolored row, and
> Stage A handles the sibling-aware downgrade for that case."

Stage A is that missing sibling: detect *colorless SP → catalog has multiple
color siblings of the same base model*, and **downgrade** the match (force it to
`candidate` / needs-eyeball, or apply a score penalty) instead of letting it slip
through to auto-confirmation against one arbitrary sibling.

---

## 2. Current behavior (cited from matcher.py)

### 2.1 Color extraction
- `_extract_colors(*parts) -> set[str]` — matcher.py:**165-185**.
  Collapses uk/ru/en color words into canonical family tags via
  `_COLOR_FAMILIES` (matcher.py:**82-156**) and `_COLOR_FAMILY_RES`
  (matcher.py:**158-162**). Full-word, Unicode-boundary, no 3-letter stems.
  Families: black, white, silver, **inox**, red, blue, green, yellow, gold,
  bronze, chrome. **Note: `inox` (stainless) is a *material/finish*, not a paint
  color** — this matters for the trigger definition (§4.2).

### 2.2 Where colors are used today
- **Step 4.88 — Color-variant gate**, matcher.py:**1690-1731**.
  `sup_colors = _extract_colors(name, article, model)` (1699-1701). Only runs
  `if sup_colors:` (1702). For each candidate, computes
  `pp_colors = _extract_colors(pp.name, pp.article, pp.display_article)` (1721)
  and rejects when `pp_colors and not (sup_colors & pp_colors)` (1722).
  Bypasses (1704, 1715-1720): `_skip_post_gates` (display_article fast-match) and
  supplier_article appearing verbatim in PP blob.
  **Consequence:** when `sup_colors` is empty, the whole gate is skipped — the
  colorless-SP case is invisible to it. This is the exact hole Stage A fills.

### 2.3 Other gates relevant to "same base model"
- `normalize_model(value)` — matcher.py:**267-283** (strict literal SKU key).
- `extract_model_from_name(name, brand)` — matcher.py:**309-385** (first
  plausible model token after the brand). **This is the matcher's own notion of
  "base model"** — already used to build `_pool_model_counts` in the Step 4.91
  uniqueness bypass (matcher.py:**1758-1764**). Stage A should reuse it so its
  grouping key matches the matcher's existing concept of "same model".
- `meaningful_tokens(text)` — matcher.py:**802-857**. Color words are NOT
  stripped here (they are not in `VOLTAGE_TAGS`), so a colorless SP's after-brand
  tokens are a **strict subset** of a colored PP's tokens (PP has the extra color
  token). This is the lever that the auto-confirm rules use (§5.1).
- Step 4.9 after-brand containment — matcher.py:**1733-1877**.
  `_short_alpha_discriminator` (matcher.py:**731-760**) already separates SKU
  suffixes/material markers like `ABS`/`INOX`/`RD`/`LD` when they are the *only*
  extra on one side. This is why material variants (ABS vs INOX) are already
  handled and must be **excluded** from Stage A (§4.2, §6.3).
- Step 4.8 voltage gate — matcher.py:**1559-1581** handles (220)/(380) variants.

### 2.4 Scoring / "confirm" mechanics (why "downgrade" needs definition)
- The matcher **never auto-confirms**. `find_match_candidates` returns dicts with
  `score`; `run_matching_for_supplier` (matcher.py:**1989-2145**) writes them as
  `status="candidate"` (matcher.py:**2122-2127**).
- Auto-confirmation happens **downstream**, not in matcher.py:
  - `scripts/bulk_auto_confirm.py` rules R0-R4 (run in `sync_pipeline.py:244-251`
    Stage 6.5 and `rematch_job.py:229-233`). **R2** (`bulk_auto_confirm.py:
    classify_single`) auto-confirms a *single* candidate when SP tokens
    ⊂ PP tokens (or vice-versa) AND price within ±5%. **R1** confirms
    tokens-equal.
  - `app/services/rule_matcher.py:156,169` auto-confirms by `MatchRule` entries.
- **Therefore "downgrade" cannot mean "force status=candidate"** inside the
  matcher (the matcher already only emits `candidate`). It must mean: **make the
  candidate ineligible for the downstream R1/R2 auto-confirm** (and visibly flag
  it for human review). Two concrete mechanisms are proposed in §4.4.

---

## 3. Real DB evidence (`instance/labresta.db`, read-only)

Probed with the matcher's own `_extract_colors` / `extract_model_from_name` /
`normalize_model`. DB snapshot: 5683 PP, 12895 SP, matches = 2362 confirmed /
301 candidate / 71 rejected / 7 manual. Suppliers: maresto, novyy-proekt,
kodaki, rp-ukrayina, guder, astim.

### 3.1 Sibling clusters (grouping key = brand_norm + extract_model_from_name)
**57 paint-color sibling clusters** (≥2 members, same brand+base model, ≥1
painted member and either ≥2 distinct paint families OR a colorless base row).
**26** of them have **≥2 distinct paint families** (the cleanest ambiguous case).
(Including the `inox` material family, the raw count is 68 clusters; excluding
`inox`-only clusters leaves the 57 paint clusters above.)

Concrete real clusters (ids + names):

| Cluster (brand / base model) | Paint families | PP ids + names |
|---|---|---|
| **GoodFood BL160** | black, blue, red, white, yellow | pp#3074 BLACK · pp#3075 WHITE · pp#3076 CARAMEL · pp#3077 YELLOW · pp#3078 RED · pp#3079 BLUE ("Міксер погружний GoodFood BL160 …") |
| **GoodFood PM-B7** | black, red, silver | pp#3160 RED · pp#3161 BLACK · pp#3185 SILVER ("Машина збивальна GoodFood PM-B7 …") |
| **Everlasting 1500** | black, green | pp#5366 GREEN/INOX · pp#5367 GREEN VIP · pp#5368 BLACK · pp#5369 GREEN GLASS ("Шафа для визрівання Everlasting STG GREEN MEAT 1500 …") |
| **Hurakan HKN-LPD150S** | black, white | pp#2260 Black · pp#2262 White ("Вітрина кондитерська холодильна Hurakan HKN-LPD150S …") |
| **Hurakan HKN-LPD210S** | black, white | pp#2261 Black · pp#2263 White |
| **Hurakan HKN-LPD150** | black, white | pp#2264 Black · pp#2266 White |
| **Hurakan HKN-LPD210** | black, white | pp#2265 Black · pp#2267 White |
| **EWT INOX RT78B** | black, white | pp#1841 black · pp#1842 white |
| **EWT INOX RT98B** | black, white | pp#1843 white · pp#1859 black |
| **GoodFood RTW100L** | black, white | pp#2624 біла Premium · pp#2644 чорна Premium |
| **Frosty FL58/FL78/FL98/FL218/FL238/FL288** | black, white | pp#5516/5533, 5532/5553, 5517/5534, 5520/5530, 5518/5554, 5521/5559 |
| **Frosty RT235L/RT280L/RT78L-1D/RT98L-1D** | black, white | pp#5519/5523, 5515/5555, 5514/5524, 5549/5550 |
| **GoodFood RT68L/RT78L/RT98L** | black, white | pp#2625/5558, 5527/5551, 5556/5557 |
| **GoodFood WB08** | black, red | pp#4274 · pp#4275 |
| **Reednee RT78B / RT98B** | black, white | pp#5525/5529, 5526/5531 |

The pattern is **real and widespread** across GoodFood, Frosty, Hurakan, EWT
INOX, Reednee, Everlasting.

### 3.2 Ambiguous colorless-SP cases (the exact Stage A target)
**Catalog-wide colorless-SP rows that key-match a PAINT cluster: 0.**

Every supplier that carries one of these paint-sibling models **also labels its
SP rows with the color**, so they already confirm correctly via Stage B. Real
evidence (SP rows for cluster models, all carry paint):
- Hurakan HKN-LPD150S → SP#4648 `…Black…` (black), SP#4649 `…White…` (white)
  [novyy-proekt]
- Hurakan HKN-LPD210/210S → SP#4647 black, SP#4650 black, SP#4651 white,
  SP#4654 white [novyy-proekt]
- EWT INOX RT78B → SP#608 white, SP#609 black [maresto]
- Reednee RT78B → SP#967 white, SP#3669 black [maresto]
- GoodFood BL160 / PM-B7 / RTW100L → **0 SP rows** (catalog-only models).

The two "ambiguous" pairs the first (over-broad) probe surfaced are **NOT paint**
cases and must be excluded by Stage A:
- SP#824 `Льодогенератор Brema CB184AHC ABS` → cluster {pp#1493 INOX, pp#1498
  ABS}. This is a **material** (ABS plastic vs INOX steel) split, already handled
  by Step 4.9 `_short_alpha_discriminator`. SP#824 correctly confirmed to the ABS
  row pp#1498 (match#293).
- SP#6899 `Пила … SIRMAN SO-1650 F3 1 фаза` → cluster {pp#3486 (220), pp#3502
  (380), pp#3506 INOX}. This is a **voltage** (Step 4.8) + material split, not
  paint. Confirmed to pp#3486 (match#3239).

### 3.3 Population the rule would touch (existing matches)
Using the **paint-only** trigger (§4.2), matches where a colorless SP points into
a paint cluster:

| status | count |
|---|---|
| candidate | **0** |
| confirmed | **0** |
| manual | **0** |

**The rule would touch zero existing matches.** Confirmed matches *into* paint
clusters all have a colored SP on the other side (12 such confirmed pairs, e.g.
match#1647 sp#4648 black→pp#2260 black, match#642 sp#609 black→pp#1841 black) —
Stage A's trigger requires a **colorless** SP, so none of them qualify.

> If `inox` were (wrongly) treated as a paint color, the population would be
> candidate=1 / confirmed=2 (match#293 Brema, match#3239 Sirman) — all
> false positives. This is the single most important reason to exclude `inox`
> from the trigger (§4.2).

---

## 4. Proposed rule

### 4.1 Where it hooks
A new **Step 4.89** in `find_match_candidates`, placed **immediately after Step
4.88** (matcher.py:1731) and **before Step 4.9** (matcher.py:1733). It runs over
both `fast_matches` and `fuzzy_output`, like the neighboring gates.

### 4.2 Trigger condition (precise)
Fire Stage A for a candidate iff ALL hold:
1. **SP has no paint color.** `_extract_colors(sp_name, sp_article, sp_model) &
   PAINT == set()` where
   `PAINT = {black, white, red, blue, green, yellow, gold, bronze, chrome,
   silver}` — i.e. all color families **except `inox`**. (`inox`/material splits
   are handled by Step 4.9; including them produces only false positives — §3.3.)
2. **The matched PP carries a paint color OR is the base row of a paint
   cluster** — i.e. the matched PP belongs to a *paint cluster* (def. below).
3. **The matched PP has ≥1 paint *sibling* in the candidate pool** under the same
   grouping key, where a sibling is a different PP whose paint set differs from
   the matched PP's paint set (so the choice between them is genuinely
   ambiguous). Concretely: among pool PPs sharing the grouping key, there exist
   ≥2 *distinct paint sets* (counting the empty set of a base row as one), so a
   colorless SP cannot be uniquely assigned.

**Grouping key (operational):**
`(normalize_model(pp.brand), normalize_model(extract_model_from_name(pp.name,
pp.brand)))`, with the base-model component required to be ≥4 chars. This mirrors
`_pool_model_counts` (matcher.py:1758-1764), so Stage A's "same model" means the
same thing the existing Step 4.91 bypass already means. The cluster is built from
`candidates_pool` (the brand-blocked pool already in scope), not the full
catalog — consistent with every other gate.

**"Paint cluster"** = a grouping key whose pool members include ≥1 PP with a
non-empty PAINT set.

### 4.3 Exemptions (must NOT fire)
- **Already-decided matches.** Stage A lives in candidate *generation*; it
  cannot and must not touch rows already `confirmed`/`manual`/`rejected`.
  `run_matching_for_supplier` already skips SPs with confirmed/manual matches
  (matcher.py:2007-2018) and never recreates existing pairs
  (matcher.py:2113-2114, 2053-2075). So **confirmed/manual rows are structurally
  exempt** — Stage A only ever sees fresh candidates. The spec records this as an
  invariant; no extra code needed, but the test plan asserts it (§7).
- **`_skip_post_gates`** (display_article fast-match) → bypass, mirroring Step
  4.88 line 1704. Manufacturer-SKU equality is stronger than color ambiguity.
- **supplier_article verbatim in PP blob** → bypass, mirroring Step 4.88
  lines 1715-1720. If the SP's article string appears in the PP name/article/
  display_article, the row is pinned regardless of color.
- **SP carries its own paint color** → not triggered (condition 1). That is
  Stage B's job.
- **Material-only / voltage-only clusters** (inox vs abs, 220 vs 380) → excluded
  by the PAINT-only definition + existing Steps 4.8/4.9 (§3.2).
- **Single-paint cluster with no real ambiguity** (only one distinct paint set in
  pool, no base row) → condition 3 fails, no fire.

### 4.4 Action — two candidate mechanisms (decision for Yana, §8)

**Mechanism A — annotate + block downstream auto-confirm (recommended).**
Tag the surviving candidate with an internal flag (e.g.
`candidate["_color_ambiguous"] = True`) and persist a marker so the downstream
auto-confirm rules skip it. The matcher already emits only `candidate`; the real
risk is **R1/R2** in `bulk_auto_confirm.py` promoting it. Implementation outline:
- In matcher: keep the candidate (do NOT drop it — a human may still pick the
  right sibling), set the flag, and lower confidence to at most `"medium"` so the
  UI shows it as needs-eyeball.
- Downstream: `bulk_auto_confirm.classify_single` already keys on tokens+price.
  Add a guard there (R1/R2) that refuses to auto-confirm when the SP is colorless
  and the PP is in a paint cluster (same predicate). This is the surgical place
  to stop the only real auto-confirm path. *(This touches bulk_auto_confirm.py —
  flag for Yana; an alternative is a `ProductMatch` boolean column, heavier.)*

**Mechanism B — score penalty (lighter, self-contained in matcher).**
Apply a fixed penalty so the candidate drops below the auto-confirm-relevant
band but stays above `SCORE_CUTOFF` (60) so it remains visible for review.
Mirror the existing additive-score pattern (`MODEL_BOOST_POINTS`,
matcher.py:48,1465-1468) with a new `COLOR_SIBLING_PENALTY` (e.g. −25) and
re-label confidence via `get_confidence_label`. Caveat: R2 auto-confirm keys on
**tokens+price**, *not* score — a penalty alone does **not** stop R2. So
Mechanism B must be combined with the R1/R2 guard from Mechanism A to actually
close the auto-confirm hole. **Score penalty alone is insufficient.**

> Recommendation: **Mechanism A** (annotate + R1/R2 guard). It directly closes
> the only live auto-confirm path (R2 subset+price) and keeps the candidate
> available for manual selection. Score penalty can be layered on for UI
> ordering but is not load-bearing.

---

## 5. Regression guard

### 5.1 What could break
The downstream auto-confirm path is the regression surface, not the matcher:
a colorless SP whose after-brand tokens are a strict **subset** of a colored PP
(PP has the extra color token) + price within ±5% is exactly **R2:
subset-tight-price** (`bulk_auto_confirm.py:classify_single`, the `sup.issubset
(prom)` branch). Today this would silently confirm the colorless SP to whichever
single colored sibling happened to be the lone candidate. Stage A's job is to
make that pair ineligible.

### 5.2 Real confirmed ids at risk
**Zero.** Per §3.3, no currently-confirmed (or manual) match has a colorless SP
pointing into a paint cluster. The 12 confirmed matches that *do* point into
paint clusters (match#641, #642, #1065, #1066, #1442, #1443, #1647, #1648,
#1649, #1650, #1651, #1652) all have a **colored** SP, so Stage A's
colorless-SP trigger never selects them. They are safe by construction.

The only confirmed rows the *over-broad* (inox-as-paint) version would hit are
**match#293** (Brema CB184AHC ABS, sp#824) and **match#3239** (Sirman SO-1650,
sp#6899) — both **material/voltage**, not paint, and both correctly confirmed
today. Excluding `inox` from the trigger (§4.2) removes them from scope. These
are the canonical "must NOT downgrade" fixtures (§7).

### 5.3 Exemption logic for "true color vs coincidental color word"
- **True paint color** = a token from `PAINT` matched by `_extract_colors`'s
  full-word Unicode-boundary regexes (matcher.py:158-185). These already reject
  substrings (`син` in `синхронний`, `сер` in `серія`, `red` in `reduce`) —
  proven by `tests/test_matcher_color_gate.py::test_short_substrings_not_hijacked`.
- **Coincidental color in brand/model** — guard by requiring the paint difference
  to be in the cluster *siblings*, not in the shared base model. Because the
  grouping key is `extract_model_from_name` (the model token), a color word that
  is part of the model code would land in the key on *both* sides and cancel out;
  only colors in the descriptive tail create distinct paint sets. Additionally,
  keep the existing **article/`_skip_post_gates` bypasses** so any SKU-pinned
  pair is immune.
- **Material (`inox`) and voltage** are excluded by definition (§4.2) and remain
  the responsibility of Steps 4.8 / 4.9.

---

## 6. Edge cases worth encoding

1. **Everlasting 1500** (pp#5366-5369): mixes GREEN/INOX/BLACK/GLASS and the base
   model token is the bare digit `1500`. `extract_model_from_name` may return a
   weak key here — Stage A's ≥4-char base-model guard and "≥2 distinct paint
   sets" requirement keep it conservative. Verify behavior in a fixture.
2. **GoodFood BL160 CARAMEL** (pp#3076): "CARAMEL" is not in any color family →
   `_extract_colors` returns empty for it, so it reads as a *base/colorless*
   sibling. The cluster still trips condition 3 (BLACK/WHITE/RED/etc. are
   distinct paint sets), which is correct.
3. **Multi-tag PP** (EWT INOX `RT78B black` = {black, inox}): the PAINT subset is
   {black}; `inox` is ignored for the trigger but harmless.
4. **Single-supplier-claim guard** (matcher.py:2085-2095, Step 3.6) already
   prevents one SP fanning to multiple PPs of the same supplier; Stage A is
   orthogonal (it concerns colorless SP vs colored PP, not SP fan-out).

---

## 7. TDD test plan

New file: `tests/test_matcher_color_sibling_stage_a.py`. Reuse the `_make_prom`
helper style from `tests/test_matcher_color_gate.py`. All cases call
`find_match_candidates(...)` and assert on the returned candidate list / the
proposed `_color_ambiguous` flag (or score band, depending on §8 decision).

**Group 1 — rule FIRES (ambiguous, must downgrade / block auto-confirm):**
- `test_colorless_sp_two_paint_siblings_downgraded`:
  PP pool = Hurakan HKN-LPD150S Black (pp1) + White (pp2). SP =
  "Вітрина … Hurakan HKN-LPD150S 0,9 м" (no color), price within ±5% of pp1.
  Expect: candidate(s) returned but flagged `_color_ambiguous` (Mechanism A) /
  score reduced below auto-confirm band (Mechanism B); NOT a clean single
  high-confidence confirm.
- `test_colorless_sp_six_paint_siblings_downgraded`: GoodFood BL160 cluster
  (synthetic 6 rows) + colorless SP → flagged.
- `test_caramel_base_plus_painted_siblings_fires`: BL160 CARAMEL (reads as base)
  + BLACK + WHITE; colorless SP → fires (≥2 distinct paint sets incl. base).

**Group 2 — rule does NOT fire (safe; must keep passing):**
- `test_colored_sp_not_touched`: SP "… HKN-LPD150S **Black**" + same pool →
  Stage B handles it; Stage A inert (SP has paint). Asserts the existing
  Black→Black confirm path (mirrors current
  `test_matcher_color_gate.py::test_same_color_both_sides_passes`).
- `test_material_inox_vs_abs_not_downgraded` (**regression: match#293**):
  pool = Brema CB184AHC INOX (pp1) + ABS (pp2); SP "… Brema CB184AHC **ABS**"
  (no PAINT, has `abs` material). Stage A must NOT fire (inox excluded; this is a
  Step 4.9 short-alpha material case). Expect normal match to the ABS row.
- `test_voltage_variant_not_downgraded` (**regression: match#3239**):
  pool = Sirman SO 1650 F3 (220) + (380) + INOX; SP "… SIRMAN SO-1650 F3 1 фаза".
  Stage A must NOT fire (no PAINT). Voltage/phase handled by Step 4.8.
- `test_single_paint_no_sibling_not_downgraded`: pool has ONE colored row only,
  no other sibling → condition 3 fails → normal match.
- `test_article_pinned_bypasses`: SP has `supplier_article` appearing verbatim in
  one PP's name → bypass even if colorless and cluster exists (mirrors Step 4.88
  article bypass).
- `test_display_article_fast_match_bypasses`: candidate carrying
  `_skip_post_gates` → not downgraded.

**Group 3 — invariant (regression on real-world confirmed rows):**
- `test_confirmed_rows_never_regenerated`: integration-style — assert that
  `run_matching_for_supplier` skips SPs with an existing confirmed match (already
  guaranteed by matcher.py:2007-2018, 2113-2114) so Stage A can never re-touch
  the 12 confirmed paint pairs (match#641…#1652) or match#293 / #3239. Can be a
  focused unit test on the skip-set logic with fixtures mirroring those ids.

**Group 4 — extractor sanity (cheap, mirrors existing file):**
- `test_paint_excludes_inox`: assert the new `PAINT` set excludes `inox` and that
  the trigger predicate returns False for an inox-only PP cluster.

---

## 8. Open questions / decisions for Yana

1. **Action mechanism (§4.4).** Mechanism A (annotate + add an R1/R2 guard in
   `scripts/bulk_auto_confirm.py`) vs Mechanism B (score penalty in matcher
   only). Recommendation: A, because R2 auto-confirm keys on **tokens+price, not
   score**, so a penalty alone does not actually stop auto-confirm. A touches a
   second file (`bulk_auto_confirm.py`) — confirm that's acceptable, or approve a
   new `ProductMatch.color_ambiguous` boolean column instead (heavier, schema
   migration).
2. **Drop vs keep the ambiguous candidate.** Should Stage A *keep* the candidate
   (flagged, for manual sibling-selection) or *drop* it entirely (force the SP to
   the unmatched queue)? Recommendation: keep + flag — dropping loses the
   near-correct suggestion. Yana's call.
3. **Zero live cases — build now or defer?** §3.3 shows **0** matches touched and
   **0** colorless SPs hitting paint clusters today. Stage A is purely
   **defensive/future-proofing** (guards against a future supplier feed that adds
   a colorless row for a paint-sibling model). Worth building now for safety, or
   defer until a real case appears? (Stage B already blocks the
   *colored-discord* case, which is the common one.)
4. **`silver` classification.** `silver` is in `PAINT` here, but for appliances
   "silver/inox/stainless" are often the same finish. Should `silver` be treated
   like `inox` (material, excluded) instead of paint? Affects GoodFood PM-B7
   (pp#3185 SILVER). Yana's domain call.
5. **Base-model key strength.** `extract_model_from_name` returns weak keys for
   bare-digit models (Everlasting `1500`). Accept the ≥4-char guard, or require
   the key to contain a letter (stricter, fewer clusters)?

---

## 9. Confirmation

This document is the only artifact written. No `.py`, `.html`, `.cfg`, `.json`
files were modified. No `git add/commit/push`, no `pytest`. The DB was opened
read-only (verified resolved URI = `sqlite:///…/instance/labresta.db`, local
only); throwaway probe scripts were created under the gitignored `.tmp/` and
deleted after use. No data was mutated.
