# chunk-070 DIFF (W2)

**Status:** chunk-070 b3 DONE 24/59 (cum TRIP 4 / blknotrip 0 / blknochg 18 / SKIP-НП 2)
**Last updated:** chunk-070 b3 DONE 24/59

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


## b2 (SKU 9-16, rows 10-17) — 16/59

| # | SKU | row | ART | Brand+Model | Category | Изменения |
|---|-----|-----|-----|-------------|----------|-----------|
| 1 | 9 | 10 | 639913426 | Apach AVM420, 20 м3/час | **SKIP-НП** | — (brand=APACH, тело из фида НП позже) |
| 2 | 10 | 11 | 2333597378 | Dadaux Astorr 310 | blknochg | — (c5/c7 RU, c36 745 chars RU Becker насос 10 m³/h / 360х315х135 / 220-230V / 70 кг) |
| 3 | 11 | 12 | 2333599907 | Dadaux Astorr 416 | blknochg | — (близнец r11, c36 RU) |
| 4 | 12 | 13 | 2333601187 | Dadaux Astorr 421 | blknochg | — (близнец r11, c36 RU) |
| 5 | 13 | 14 | 2333602959 | Dadaux Astorr 570 | blknochg | — (c36 906 chars RU 70 m³/h / 666х550х500 / 380-400V / 240 кг) |
| 6 | 14 | 15 | 647442349 | Orved Profi 2 для лотков | blknochg | — (c5/c7 RU, c36 495 chars RU 190х260 vs 190х137+137х95 матрица / 0,7 кВт / 17,1 кг) |
| 7 | 15 | 16 | 1009188903 | Petros (Orved) С308, 8 м3/час | blknochg | — (c36 679 chars RU камерный купольная 8 м3/час / 332x335x170 / 0,6 кВт / 24 кг) |
| 8 | 16 | 17 | 646844871 | Orved Evox 25H (8mc) | blknochg | — (c36 709 chars RU ORVED EVOX 25 / 8 м3/час / 25 мм source-typo preserved / 303х293х110 / 0,45 кВт / 27 кг) |

**Итого b2:** TRIP 0 + blknotrip 0 + blknochg 7 + SKIP-НП 1. Verify **192 PASS / 0 FAIL**.
**Cum после b2:** TRIP 3 + blknotrip 0 + blknochg 11 + SKIP-НП 2 = **16/59**.


## b3 (SKU 17-24, rows 18-25) — 24/59

| # | SKU | row | ART | Brand+Model | Category | Изменения |
|---|-----|-----|-----|-------------|----------|-----------|
| 1 | 17 | 18 | 568706695 | Orved Evox 25, 4м3/час | blknochg | — (c36 1047 chars RU) |
| 2 | 18 | 19 | 646844866 | PERS.PETROS LEVAC 4 | blknochg | — (c36 454 chars RU) |
| 3 | 19 | 20 | 646844868 | Petros (Orved) Lerica С412 | blknochg | — (c36 584 chars RU) |
| 4 | 20 | 21 | 647442348 | Petros LT1 для лотков | blknochg | — (c5/c7 «Термоупаковочная … для лотков», c36 333 chars RU) |
| 5 | 21 | 22 | 1009196281 | Petros (Orved) Lerica С420 2 планки | blknochg | — (c36 631 chars RU) |
| 6 | 22 | 23 | 1869658739 | LAVEZZINI ECO45 L напольный | blknochg | — (c5/c7 «напольный», c36 489 chars RU h2 камерный купольная 460x500x220 / 560x640x1050 / 90 кг) |
| 7 | 23 | 24 | 2395332619 | SIRMAN W8 30 Vertigo | blknochg | — (c36 1340 chars RU EASY TOUCH Wi-Fi / 326x60x250 камера / 4 м3/час / 22 кг) |
| 8 | 24 | 25 | 489841522 | Lavezzini LX420 запайщик | **TRIP** | c5←c7 «Запайщик пакетов Lavezzini LX420»; c36 ← RU 5 li (пищевые пакеты до 5 мм / крашеный металл / 420 мм / 0,6 кВт / 80х550х260 / 4 кг) |

**Итого b3:** TRIP 1 + blknotrip 0 + blknochg 7 + SKIP-НП 0. Verify **198 PASS / 0 FAIL**.
**Cum после b3:** TRIP 4 + blknotrip 0 + blknochg 18 + SKIP-НП 2 = **24/59**.
