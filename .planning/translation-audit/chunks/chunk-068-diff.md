# chunk-068 DIFF (W2)

**Status:** b2 DONE 16/50 — батчи b1..b7 (8+8+8+8+8+8+2); next b3 (SKU 17-24, rows 18-25)
**Last updated:** chunk-068 b2 DONE 16/50

Source: `chunk-068.xlsx` (RO) → operating: `chunk-068-fixed.xlsx` (gitignored).
Batches заполняются после каждого закрытого батча.

## b1 (SKU 1-8, rows 2-9) — 8/50

| # | SKU | row | ART | Brand+Model | Category | Изменения |
|---|-----|-----|-----|-------------|----------|-----------|
| 1 | 1 | 2 | 2045399173 | Empero EMP.500-380-SDF | blknochg | — (fixed row не изменён) |
| 2 | 2 | 3 | 2053905002 | Crystal CRW 500 TPD помпа слива | blknochg | — |
| 3 | 3 | 4 | 2053911972 | Crystal CRW 1000 TPD помпа слива (купольная) | blknochg | — |
| 4 | 4 | 5 | 2054635608 | Adler EVO 1000 PD | blknochg | — |
| 5 | 5 | 6 | 2080385348 | Frosty ECO35 (стаканомойка) | **TRIP** | c5←c7; c36 ← RU 25-строчный body (16+4+1 li) |
| 6 | 6 | 7 | 2080393304 | Frosty ECO1000 3ph купольная | **TRIP** | c5←c7; c36 ← RU 24-строчный body (14+5+1 li) |
| 7 | 7 | 8 | 2080397413 | Frosty ECO50 1ph фронтальная | **TRIP** | c5←c7; c36 ← RU 27-строчный body (17+5+1 li) |
| 8 | 8 | 9 | 2080400876 | Frosty ECO50 3ph фронтальная | **TRIP** | c5←c7; c36 ← RU 27-строчный body (same template как r8, 6,65/380В) |

**Итого b1:** TRIP 4 + blknotrip 0 + blknochg 4 + SKIP-НП 0. Verify 90 PASS / 0 FAIL.

## b2 (SKU 9-16, rows 10-17) — 16/50

| # | SKU | row | ART | Brand+Model | Category | Изменения |
|---|-----|-----|-----|-------------|----------|-----------|
| 1 | 9 | 10 | 2176569021 | APACH AC800DIG DD | **SKIP-НП** | — (НП forward-only; fixed строка не тронута) |
| 2 | 10 | 11 | 2191921582 | Frosty ECO40 1ph (стаканомойка «мытья») | **TRIP** | c5←c7; c36 ← RU 25-строчный body (16+4+1 li) |
| 3 | 11 | 12 | 2213453082 | Krupps C327DGT Advance DP45K | **TRIP** | c5←c7; c36 ← RU 31-строчный body с `<h2>` (24+4 li) |
| 4 | 12 | 13 | 2213463204 | Krupps C537DGT Advance DP45K | **TRIP** | c5←c7; c36 ← RU 31-строчный body с `<h2>` (24+4 li) |
| 5 | 13 | 14 | 2221209761 | Winterhalter UC-M 012V0031 фронтальная | **TRIP** | c5←c7; c36 ← RU 20-строчный body (3 `<p>` + 18 li); dup-typo + «1цикл» preserved |
| 6 | 14 | 15 | 2278734126 | Oztiryakiler OBY35TPDT | **TRIP** | c5←c7; c36 ← RU 22-строчный body с `<h2>` (15+4 li) |
| 7 | 15 | 16 | 2278736666 | Oztiryakiler OBY40TPDT | **TRIP** | c5←c7; c36 ← RU 22-строчный body (same template как r15) |
| 8 | 16 | 17 | 2289323710 | Silanos S021 PS PD/РВ DIGIT (стаканомойка) | blknochg | — (skel-eq False source variance, c5==c7 RU OK, не трогаем) |

**Итого b2:** TRIP 6 + blknotrip 0 + blknochg 1 + SKIP-НП 1. Verify 109 PASS / 0 FAIL.
**Cum после b2:** TRIP 10 + blknotrip 0 + blknochg 5 + SKIP-НП 1 = 16/50.

