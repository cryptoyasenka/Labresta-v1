# chunk-070 DIFF (W2)

**Status:** chunk-070 b1 DONE 8/59 (cum TRIP 3 / blknotrip 0 / blknochg 4 / SKIP-НП 1)
**Last updated:** chunk-070 b1 DONE 8/59

Source: `chunk-070.xlsx` (RO, 59 SKU rows 2..60, ART 2176091387..500051832) → operating: `chunk-070-fixed.xlsx` (gitignored, скопирован из source 1:1).

Batches заполняются после каждого закрытого батча.

## План батчей

- **b1**: SKU 1-8, rows 2-9 (включает SKIP-НП r3 HURAKAN HKN-VAC400E)
- **b2**: SKU 9-16, rows 10-17 (включает SKIP-НП r10 APACH AVM420)
- **b3**: SKU 17-24, rows 18-25
- **b4**: SKU 25-32, rows 26-33
- **b5**: SKU 33-40, rows 34-41
- **b6**: SKU 41-48, rows 42-49
- **b7**: SKU 49-56, rows 50-57
- **b8**: SKU 57-59, rows 58-60 (финал 3 SKU)

## SKIP-НП кандидаты (forward-only override)

- r3  ART 2373858169 — Вакууматор HURAKAN HKN-VAC400E
- r10 ART 639913426  — Вакуумний пакувальник Apach AVM420, 20 м3/год


## b1 (SKU 1-8, rows 2-9) — 8/59

| # | SKU | row | ART | Brand+Model | Category | Изменения |
|---|-----|-----|-----|-------------|----------|-----------|
| 1 | 1 | 2 | 2176091387 | GoodFood VMP400DSB вакуум-упак.машина | blknochg | — (c36 already RU 971 chars, no UA marks) |
| 2 | 2 | 3 | 2373858169 | HURAKAN HKN-VAC400E | **SKIP-НП** | — (brand=HURAKAN, тело из фида НП позже) |
| 3 | 3 | 4 | 2395310366 | SIRMAN 45К СЕ→СЭ термоупак. | **TRIP** | c5←c7; c36 ← RU body «Упаковщик горячих столов» 8 li (385х125/485х600х140/0.12 Вт/220 В/5 кг) |
| 4 | 4 | 5 | 2396480697 | Forpack TE-45 термоупак. | blknochg | — (c5/c7 already RU «Термоупаковочная», c36 already RU 527 chars) |
| 5 | 5 | 6 | 2396496014 | GASTRO HIT TE-39 187x137 | blknochg | — (c5/c7 «Термоупаковочная … 1-но секционная», c36 already RU 589 chars) |
| 6 | 6 | 7 | 2396503425 | GASTRO HIT TE-39 227x178 | blknochg | — (близнец r6, c36 already RU) |
| 7 | 7 | 8 | 647414869 | Hendi Kitchen Line 975374 (планка 420 мм) | **TRIP** | c5←c7 «Вакуумный упаковщик Hendi Kitchen Line»; c36 ← RU 13 li (бескамерный/л/мин/2-3 с/насос 16/406 мм/6,9 кг) |
| 8 | 8 | 9 | 1145567303 | Hendi 970362 | **TRIP** | c5←c7 «Вакуумный упаковщик Hendi 970362»; c36 ← RU 12 li (Profi Line 350/AISI 304 SB/л / мин/перфорированными/350 мм/0,25 кВт/220 В/370x280x(H)170) |

**Итого b1:** TRIP 3 + blknotrip 0 + blknochg 4 + SKIP-НП 1. Verify **201 PASS / 0 FAIL**.
**Cum после b1:** TRIP 3 + blknotrip 0 + blknochg 4 + SKIP-НП 1 = **8/59**.
