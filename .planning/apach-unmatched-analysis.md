# Apach Unmatched-Catalog Analysis

**Date:** 2026-04-23
**Session:** 2506aa0b
**Trigger:** Yana showed `/products/unmatched-catalog?brand=Apach` with 48 items (47 after counting) and asked why Horoshop products aren't matched to supplier feed (Новий Проект, supplier_id=2).

## Data shape

- **125** Apach PP rows total in catalog
  - 77 confirmed, 2 candidate, 3 rejected, **47 with zero match rows** (subject of this analysis)
- **158** Apach SP rows in supplier feed (supplier_id=2)
- `run_matching_for_supplier(2)` re-ran during investigation → created 3 new candidates elsewhere, **zero** for the 47 orphan PPs.

## Root-cause categorisation of the 47 orphan PPs

### A. /PL-suffix gate rejection — 7 pairs (WAI but reviewable)

SPs carry a `/PL` logistical / packaging suffix that PP-side names do not. `normalize_model` glues `/` out, producing e.g. `appe47ppl` which fails the **Name-model gate** at `matcher.py:1072` against plain `appe47p`.

| PP (orphan) | SP (blocked) | SP.article |
|---|---|---|
| pp#73 Плита індукційна APACH APRI-47P | sp#4598 | `APRI-47P/PL` |
| pp#314 Поверхня APACH APTE-47PL | sp#4581 | `APTE-47PL/PL` |
| pp#315 Поверхня APACH APTE-47PR | sp#4767 | `APTE-47PR/PL` |
| pp#316 Поверхня APACH APTE-77PLR | sp#4736 | `APTE-77PLR/PL` |
| pp#477 Поверхня APACH APTE-77PL | sp#4580 | `APTE-77PL/PL` |
| pp#811 Макароноварка APACH APPE-77P | sp#4597 | `APPE-77P/PL` |
| pp#837 Макароноварка APACH APPE-47P | sp#4601 | `APPE-47P/PL` |

**Decision needed from Yana:** is `/PL` actually a different SKU (packaging variant) or the same product? If same, matcher needs a `/PL`-as-same-SKU rule.

### B. 1 PP ↔ 1 SP invariant — 1 pair (WAI)

pp#312 `Розстоєчну шафу Apach APE12ABQ` → the only SP with matching article (sp#4989 APE12ABQ) is already **confirmed** to pp#5009 (`Шафа розстійна Apach APE12ABQ D` — D-variant). Per invariant #2 (`feedback_labresta_one_to_one.md`) an SP can't produce a second confirmed match. `run_matching_for_supplier` skips confirmed SPs entirely (`matcher.py:1326`), so no candidate row is created for pp#312.

**WAI.** If Yana wants pp#312 linked, the D-variant confirmation on sp#4989 would need to be re-targeted manually.

### C. Model-variant mismatch — 7 pairs (WAI)

SPs exist with related but **distinct** model codes. `extract_model_from_name` produces different tokens → name-model gate rejects.

| PP | PP model | Closest SP | SP.article | Note |
|---|---|---|---|---|
| pp#1008 | AD46D | sp#5107 | AD46DI ECO | `D` vs `DI ECO` — different variant |
| pp#1341 | ASH05K | sp#4634 / sp#4635 | ASH05K R290 / ASH05K DF R290 | refrigerant-variant |
| pp#3034 | AFM350 VVC 300 | sp#5116 | AFM350VVC300 | numeric trailing may match if normalized |
| pp#3039 | AHM250V250 | sp#5106 | AHM250V250C | `C` suffix differs |
| pp#3042 | AFM250 VV 200 | sp#5115 | AFM250VV200 | may match if normalized |
| pp#3043 | AFM250 VVC 250 | sp#5115 | AFM250VV200 | different SKU |
| pp#4494 | AF500 DIG DD | sp#4958 | AF500DIG DD | space normalisation — potentially should match |

A few pairs in this category (especially 3034 / 3042 with spacing-only differences) are worth re-probing; spacing normalisation may already produce equality.

### D. Truly absent from supplier feed — 24 PPs

No SP row has an article code resembling the PP's model token. These PPs simply aren't offered by supplier_id=2 right now:

```
pp#9    APRG-77P (Плита газова)
pp#871  APKE-77 (Котел)
pp#1007 AD46MV (Піч)
pp#1009 AP5QD  (Пароконвектомат)
pp#1010 AP10QD (Пароконвектомат)
pp#1015 AD46DV (Піч)
pp#1570 AFM 02 (Стіл холодильний)
pp#1571 AFM 03
pp#1572 AFM 04
pp#1775 AFM 02 BT (Стіл морозильний)
pp#1776 AFM 03 BT
pp#1777 AFM 04 BT
pp#1870 AMT 50 (Піч піци)
pp#2663 ASM16F (Тістоміс)
pp#2666 L33 (Тістоміс)
pp#2833 ASF500-700 (Тісторозкатка)
pp#3113-3120 APL 5B/10B/20B/20P/30/40/60/80 (Планетарні міксери — 8 штук)
pp#3695 ACS1 ECO (Соковижималка)
pp#3749 ACG1 (Кавомолка)
pp#3772 AMX1 ECO (Міксер)
pp#3773 AMX2 ECO (Міксер)
pp#4911 M30 (Ферментатор)
```

**No matcher change will help.** These require either a supplier feed update or manual confirmation from a different source.

### E. Fuzzy-prefilter saturation — 3+ pairs (BUG)

**This is the finding most worth acting on.**

For SP names with long descriptive tails (`Посудомийка Apach AF400 DDP фронтальна з дозатором миючого засобу + дренажна помпа`), `rapidfuzz.fuzz.WRatio` produces a score of 85.5 against **many** unrelated Apach PPs because `partial_ratio` latches onto the brand token `APACH` inside both strings. Pool of 125 Apach PPs produces ≥50 candidates tied at 85.5. `process.extract` truncates at `FUZZY_OVERSAMPLE_LIMIT = 50` — the **correct** short-named PP gets tied out and never reaches the gates.

Confirmed cases:

| SP | correct PP | WRatio | in top-50? |
|---|---|---|---|
| sp#4684 `Посудомийка Apach AF400 DDP + дренажна помпа…` | pp#4542 `Посудомийна машина APACH AF400 DDP` | 85.5 | **No** |
| sp#5053 `Посудомийка Apach AF400 DD + дозатор…` | pp#4493 `Посудомийна машина Apach AF400 DD` | (same pattern) | **No** |
| sp#4958 `Посудомийка Apach AF500DIG DD + …` | pp#4494 `Посудомийна машина Apach AF500 DIG DD` | (same pattern) | **No** |

Fix direction (for Yana's approval — matcher.py is restricted):

1. **Simplest:** raise `FUZZY_OVERSAMPLE_LIMIT` from 50 to ~200 (full-pool for a brand like Apach is 125). Cost: O(pool_size) not O(limit) — negligible.
2. **Better:** add a fast-path for pure article-code equality regardless of PP-side `article` field being NULL — extract article from PP name for the fast-path, not just from `pp.article`. sp#4684 article=`AF400DDP`, pp#4542.name contains `AF400 DDP` — normalize_model already handles the space.
3. **Also valid:** pre-trim descriptive tail ("+ дренажна помпа", "з дозатором…") before fuzzy scoring.

### F. Transliteration gap — 1 pair (BUG)

pp#4513 `Посудомийна (котломийна) машина APACH AK 901` (Latin `AK`) vs sp#4885 `Посудомийка Apach ак 901 котломийка` (Cyrillic `ак`). `find_match_candidates` returns 0. `_transliterate_cyr` runs inside the type gate but the fuzzy scorer sees raw `ак` vs `AK` → WRatio tanks. Same fix family as E (transliterate normalized names before WRatio, or add article-based fast-path).

## Summary table

| Category | Count | Status |
|---|---|---|
| A. /PL-gate rejected | 7 | **needs Yana decision** |
| B. 1pp↔1sp invariant | 1 | WAI |
| C. Model-variant mismatch | 7 | WAI (3 worth re-probing) |
| D. No SP in feed | 24 | n/a |
| E. Fuzzy-prefilter saturation | 3+ | **matcher bug** |
| F. Transliteration gap | 1 | **matcher bug** |
| **total** | **47** | |

## Recommendations

1. **Do not change `matcher.py`** without Yana's explicit go-ahead (269+ tests depend, matcher invariants #1–9, `feedback_labresta_proper_fix.md`).
2. Present this report to Yana; get direction on:
   - `/PL` suffix policy (Category A)
   - FUZZY_OVERSAMPLE_LIMIT bump + article-from-name fast-path (Category E/F)
   - Possibly the pp#312 re-assignment (Category B)
3. Categories D (24 PPs) are not actionable in code — they need either a supplier-feed expansion or manual confirmation against another supplier.

## Files touched during investigation

- Read: `app/services/matcher.py` (lines 1–1393, sampling), `scripts/diagnose_sp_match.py`
- DB queries: read-only (no writes, no migrations)
- `run_matching_for_supplier(2)` re-executed once; it committed 3 new candidates (elsewhere, not on the 47 orphans)

## Quick-return commands

```bash
# Re-query orphan Apach PPs
PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe -c "from app import create_app; app=create_app(); app.app_context().push(); from app.extensions import db; from sqlalchemy import text; [print(r) for r in db.session.execute(text(\"SELECT pp.id, pp.external_id, pp.name FROM prom_products pp LEFT JOIN product_matches m ON m.prom_product_id=pp.id WHERE lower(pp.brand) LIKE '%apach%' AND m.id IS NULL ORDER BY pp.id\")).all()]"

# Probe pp#4542 ↔ sp#4684 fuzzy saturation
.venv/Scripts/python.exe scripts/diagnose_sp_match.py --sp-id 4684 --pp-filter "AF400 DDP"
```
