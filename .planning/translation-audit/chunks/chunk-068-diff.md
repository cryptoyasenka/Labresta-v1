# chunk-068 DIFF (W2)

**Status:** b1 DONE 8/50 — батчи b1..b7 (8+8+8+8+8+8+2); next b2 (SKU 9-16, rows 10-17)
**Last updated:** chunk-068 b1 DONE 8/50

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

