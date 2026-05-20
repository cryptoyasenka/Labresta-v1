# chunk-068 DIFF (W2)

**Status:** chunk-068 **ЗАКРЫТ 50/50** — батчи b1..b7 (8+8+8+8+8+8+2); next chunk-069 scaffold
**Last updated:** chunk-068 ЗАКРЫТ 50/50

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

## b3 (SKU 17-24, rows 18-25) — 24/50

| # | SKU | row | ART | Brand+Model | Category | Изменения |
|---|-----|-----|-----|-------------|----------|-----------|
| 1 | 17 | 18 | 2460066584 | Oztiryakiler OBM1080TPD купольная | **TRIP** | c5←c7; c36 ← RU 29-строчный body (`<p>` lead + 22 li main + 4 li упаковка) |
| 2 | 18 | 19 | 2460074406 | Oztiryakiler OBY50TPDT фронтальная | **TRIP** | c5←c7; c36 ← RU 33-строчный body (`<p>` lead + 26 li main + 4 li упаковка) |
| 3 | 19 | 20 | 2556977107 | Gooder BY.500 | blknochg | — |
| 4 | 20 | 21 | 2556993881 | Gooder BY.500D | blknochg | — |
| 5 | 21 | 22 | 2557006167 | Gooder BYM.01 | blknochg | — |
| 6 | 22 | 23 | 2557011733 | Gooder BYM.02 | blknochg | — |
| 7 | 23 | 24 | 2558087500 | Gooder BY.1000 купольная | blknochg | — |
| 8 | 24 | 25 | 2558089725 | Gooder BY.1000D купольная | blknochg | — |

**Итого b3:** TRIP 2 + blknotrip 0 + blknochg 6 + SKIP-НП 0. Verify 103 PASS / 0 FAIL.
**Cum после b3:** TRIP 12 + blknotrip 0 + blknochg 11 + SKIP-НП 1 = 24/50.

## b4 (SKU 25-32, rows 26-33) — 32/50

| # | SKU | row | ART | Brand+Model | Category | Изменения |
|---|-----|-----|-----|-------------|----------|-----------|
| 1 | 25 | 26 | 2565641321 | Krupps C537TDGT Advance DP45K | blknochg | — (skel-eq False source variance, c5==c7 RU OK, не трогаем) |
| 2 | 26 | 27 | 2603547529 | APACH AF400 DDP | **SKIP-НП** | — (НП forward-only; fixed строка не тронута) |
| 3 | 27 | 28 | 2687383117 | ASBER GTX-H500 DD купольная | **TRIP** | c5←c7; c36 ← RU 18-строчный body (`<p>` + 15 li) |
| 4 | 28 | 29 | 2687394138 | ASBER GT-500 DD фронтальная | **TRIP** | c5←c7; c36 ← RU 16-строчный body (`<p>` + 13 li) |
| 5 | 29 | 30 | 2795786523 | ASBER GE-500 RD B DD (помпа слива) | **TRIP** | c5←c7; c36 ← RU 17-строчный body (`<h2>` + 14 li, перистальтический + электромеханическая + дренажная помпа) |
| 6 | 30 | 31 | 2796153409 | ASBER GEX-H500 RD DD купольная | **TRIP** | c5←c7; c36 ← RU 19-строчный body (`<p>` + 16 li) |
| 7 | 31 | 32 | 2796156408 | ASBER GT-500 RD DD фронтальная | **TRIP** | c5←c7; c36 ← RU 16-строчный body (`<h2>` + 13 li, перистальтический + электронная) |
| 8 | 32 | 33 | 2796159643 | ASBER GE-500 RD DD фронтальная (typo «B DD» preserved) | **TRIP** | c5←c7; c36 ← RU 16-строчный body (`<h2>` + 13 li, c35 body refers «GE-500 RD B DD» — source typo preserved verbatim) |

**Итого b4:** TRIP 6 + blknotrip 0 + blknochg 1 + SKIP-НП 1. Verify 130 PASS / 0 FAIL.
**Cum после b4:** TRIP 18 + blknotrip 0 + blknochg 12 + SKIP-НП 2 = 32/50.

## b5 (SKU 33-40, rows 34-41) — 40/50

| # | SKU | row | ART | Brand+Model | Category | Изменения |
|---|-----|-----|-----|-------------|----------|-----------|
| 1 | 33 | 34 | 506147414 | GGM GPE5 полировщик для бокалов | blknochg | — |
| 2 | 34 | 35 | 659353448 | Hendi 696002 ёрш для мойки стаканов | **TRIP** | c5←c7; c36 ← RU 7-строчный body (`<p>` + 4 li) |
| 3 | 35 | 36 | 1500252450 | Krupps C327DGT Advance фронтальная (без DP45K) | **TRIP** | c5←c7; c36 ← RU 12-строчный body с `<h2>` (10 li) |
| 4 | 36 | 37 | 753318879 | GGG GPE8 полировщик для бокалов | blknochg | — |
| 5 | 37 | 38 | 2389346752 | ATA ALP 43 котломоечная | blknochg | — |
| 6 | 38 | 39 | 2389351402 | ATA ALP 02S котломоечная | blknochg | — |
| 7 | 39 | 40 | 2389356892 | ATA ALP 40 котломоечная | blknochg | — |
| 8 | 40 | 41 | 2389361331 | ATA ALP 02GS котломоечная | blknochg | — |

**Итого b5:** TRIP 2 + blknotrip 0 + blknochg 6 + SKIP-НП 0. Verify 124 PASS / 0 FAIL.
**Cum после b5:** TRIP 20 + blknotrip 0 + blknochg 18 + SKIP-НП 2 = 40/50.

## b6 (SKU 41-48, rows 42-49) — 48/50

| # | SKU | row | ART | Brand+Model | Category | Изменения |
|---|-----|-----|-----|-------------|----------|-----------|
| 1 | 41 | 42 | 2389367033 | ATA ALP 30 котломоечная (560x500) | blknochg | — (c5==c7 RU OK, skel-eq True, dims-eq True) |
| 2 | 42 | 43 | 2389374106 | ATA ALP 01GS котломоечная (600x700) | blknochg | — (c5==c7 RU OK, skel-eq True, dims-eq True) |
| 3 | 43 | 44 | 2395348633 | OZTI OBY 50T PDRT | blknochg | — (c5==c7 RU OK, skel-eq True, dims-eq True) |
| 4 | 44 | 45 | 2227322220 | ADLER ECO 50 DP PD с помпой слива | blknochg | — (c5==c7 RU OK, skel-eq True, dims-eq True) |
| 5 | 45 | 46 | 1576147000 | Ozti OBY 50D PDT с помпой слива воды | blknochg | — (skel-eq False: c36 добавил `<strong>` вокруг «Дренажный насос», RU-enhance) |
| 6 | 46 | 47 | 2330374782 | OZTI OBM 1080 PDRT купольная | blknochg | — (c5==c7 RU OK, skel-eq True, dims-eq True) |
| 7 | 47 | 48 | 2389309688 | ATA ALP 01S котломоечная (600x700, Двобойлерна) | blknochg | — (skel-eq False: c35 имеет `<br />`, c36 без; c36 OK valid RU) |
| 8 | 48 | 49 | 2434107874 | ATA AT 1001 посудомоечная стаканомоечная | blknochg | — (c5==c7 RU OK, skel-eq True, dims-eq True) |

**Итого b6:** TRIP 0 + blknotrip 0 + blknochg 8 + SKIP-НП 0. Verify **280 PASS / 0 FAIL**.
**Cum после b6:** TRIP 20 + blknotrip 0 + blknochg 26 + SKIP-НП 2 = **48/50**.

## b7 (SKU 49-50, rows 50-51, ФИНАЛ) — 50/50

| # | SKU | row | ART | Brand+Model | Category | Изменения |
|---|-----|-----|-----|-------------|----------|-----------|
| 1 | 49 | 50 | 2434119030 | ATA AT 1201 купольная (1201 шт/час) | blknochg | — (c5==c7 RU OK, skel-eq True, dims-eq True 12 dims) |
| 2 | 50 | 51 | 2434126712 | ATA AT 1401 купольная (1401 шт/час) | blknochg | — (c5==c7 RU OK, skel-eq True, dims-eq True 12 dims) |

**Итого b7:** TRIP 0 + blknotrip 0 + blknochg 2 + SKIP-НП 0. Verify **256 PASS / 0 FAIL**.
**Cum после b7 (FINAL):** TRIP 20 + blknotrip 0 + blknochg 28 + SKIP-НП 2 = **50/50**. chunk-068 **ЗАКРЫТ**.

