# chunk-070 DIFF (W2)

**Status:** chunk-070 ЗАКРЫТ 59/59 (cum TRIP 22 / blknotrip 0 / blknochg 31 / blkfix 4 / SKIP-НП 2; 243 PASS / 0 FAIL)
**Last updated:** chunk-070 ЗАКРЫТ 59/59 — финиш

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


## b4 (SKU 25-32, rows 26-33) — 32/59

| # | SKU | row | ART | Brand+Model | Category | Изменения |
|---|-----|-----|-----|-------------|----------|-----------|
| 1 | 25 | 26 | 646844869 | Orved Petros С46 Н | blknochg | — (c36 586 chars RU) |
| 2 | 26 | 27 | 647442353 | Lavezzini DG30 камерный | **TRIP** | c5←c7; c36 ← RU 776 chars (Полуавтоматический камерный / автоподъём крышки / самоочистка масла / шов 300 мм / камера 310x350x190 / 10 м3/час / 0,4 кВт / 38 кг) |
| 3 | 27 | 28 | 878104998 | Lavezzini TOP BABY LCD автомат | **TRIP** | c5←c7; c36 ← RU 971 chars (Автоматический камерный 10 программ / микропечатный принтер / шов 300 мм / камера 310х350x190 / 10 м3/час / 0,4 кВт / 38 кг) |
| 4 | 28 | 29 | 1048994117 | Sammic SE-204 4 м3/час | blknochg | — (c36 2467 chars RU) |
| 5 | 29 | 30 | 1049057636 | Sammic SE-310 10 м3/час | blknochg | — (близнец r29) |
| 6 | 30 | 31 | 1049059995 | Sammic SE-416 16 м3/час | blknochg | — (близнец r29) |
| 7 | 31 | 32 | 2070683537 | Lavezzini Mini BIG бескамерный | **TRIP** | c5←c7; c36 ← RU 430 chars (Полуавтоматический бескамерный / насос 20 л/мин / шов 450 мм / 0,27 кВт / 470x260x130) |
| 8 | 32 | 33 | 2396519654 | SIRMAN S 400/2T с обрезкой | blknochg | — (c36 946 chars RU) |

**Итого b4:** TRIP 3 + blknotrip 0 + blknochg 5 + SKIP-НП 0. Verify **214 PASS / 0 FAIL**.
**Cum после b4:** TRIP 7 + blknotrip 0 + blknochg 23 + SKIP-НП 2 = **32/59**.

## b5 (SKU 33-40, rows 34-41) — 40/59

| # | SKU | row | ART | Brand+Model | Category | Изменения |
|---|-----|-----|-----|-------------|----------|-----------|
| 1 | 33 | 34 | 2396523353 | METROOPACK TYPE-10 | blknochg | — (c5/c7 RU «Термоупаковочная машина», c36 2321 chars RU) |
| 2 | 34 | 35 | 2396921807 | Metro-Plast MCS B 192 STRONG | blknochg | — (c5/c7 RU, c36 1385 chars RU) |
| 3 | 35 | 36 | 2396928077 | Sirman Sigix M20 | **TRIP** | c5←c7 «Термоупаковочная машина Sirman Sigix M20»; c36 ← RU 948 chars (припаивание крышек / AISI 304 / 4 секунды / 260x190 / 257x525x306 / 18 кг / 220 В / 0.9 квт + 4 размера лотков) |
| 4 | 36 | 37 | 2396931248 | Orved Profi 3 | blknochg | — (c5/c7 RU, c36 856 chars RU) |
| 5 | 37 | 38 | 2396940020 | JPACK TSS102-R | **blkfix** | c36 Ё→Е fix x2 (плёнки→пленки); c5/c7 unchanged |
| 6 | 38 | 39 | 2396946439 | Orved VGP60 с обрезкой | blknochg | — (c5/c7 RU, c36 655 chars RU; UA marker в c4 «з обрізкою» faithful) |
| 7 | 39 | 40 | 2396949577 | Orved VGP60N O2 | blknochg | — (близнец r39, c36 655 chars RU) |
| 8 | 40 | 41 | 2396954882 | Orved VGP 60 Skin | blknochg | — (c5/c7 RU, c36 1736 chars RU) |

**Итого b5:** TRIP 1 + blknotrip 0 + blknochg 6 + blkfix 1 + SKIP-НП 0. Verify **213 PASS / 0 FAIL**.
**Cum после b5:** TRIP 8 + blknotrip 0 + blknochg 29 + blkfix 1 + SKIP-НП 2 = **40/59**.

## b6 (SKU 41-48, rows 42-49) — 48/59

| # | SKU | row | ART | Brand+Model | Category | Изменения |
|---|-----|-----|-----|-------------|----------|-----------|
| 1 | 41 | 42 | 2398018333 | Valko TS2 герметичный запайщик лотков | **TRIP** | c5←c7 «Термоупаковочная машина Valko TS2»; c36 ← RU 928 chars (14 li tech + 4 li pkg): настольный, алюм. пластина с тефлоновым покрытием, ручная подача рулона, электронный контроль T, 15 кг / 565x515x385 / 0.6 кВт / 220V / Италия |
| 2 | 42 | 43 | 2398030000 | Lavezzini TERMOPACK SV400 | **TRIP** | c5←c7; c36 ← RU 959 chars (11 li + 4 pkg): полуавтомат термоупаковщик в лоток / глубина max 100 мм / камера 265х325 / матрицы не входят / 60 кг / 400x500x300 / 1.2 кВт / 220V |
| 3 | 43 | 44 | 2398043789 | Lavezzini TERMOPACK SV300 | **TRIP** | c5←c7; c36 ← RU 999 chars: камера 265х196 / Тип подключения Электрический / 40 кг / 280x500x300 / 0.6 кВт / 220V (faithful pkg-height «33» preserved) |
| 4 | 44 | 45 | 2398077613 | Lavezzini BOXER DUO | **TRIP** | c5←c7; c36 ← RU 1123 chars: TOP SERIES / STEP VAC / самоочищающаяся насосная / 20 программ / камера 500x460x220 / 2 планки 450 мм / насос 20 м3/час / 63 кг / 600x560x450 / 0.95 кВт / 220V |
| 5 | 45 | 46 | 2398103996 | Lavezzini BOXER DUO gas | **TRIP** | c5←c7; c36 ← RU 1333 chars: близнец r45 + inert газ (+) + микропринтер для маркировки (4-й абзац) |
| 6 | 46 | 47 | 2398118216 | Lavezzini BOXER45 LCD | **TRIP** | c5←c7; c36 ← RU 1173 chars: близнец r45+r46 + inert газ (+) (без 4-го абзаца) |
| 7 | 47 | 48 | 2398121892 | Lavezzini LAPACK 500 | **TRIP** | c5←c7; c36 ← RU 1038 chars: с колпаком на колесах / ЖК-дисплей / камера 510х650х220 / 1 планка 500 мм / насос 60 м3/час / 140 кг / 630x760x1050 / 1.4 кВт / 380V |
| 8 | 48 | 49 | 2398143399 | Lavezzini LAPACK 550S | **TRIP** | c5←c7; c36 ← RU 1101 chars: камера 720x570x220 / 2 планки 550 мм / 60 м3/час / 150 кг / 840x680x1050 / 1.45 кВт / Тип подключения Электрический / 380V; structural typo «<strong>Технические характеристики</strong>:» (двоеточие вне strong) preserved faithful |

**Итого b6:** TRIP 8 + blknotrip 0 + blknochg 0 + blkfix 0 + SKIP-НП 0. Verify **225 PASS / 0 FAIL**.
**Cum после b6:** TRIP 16 + blknotrip 0 + blknochg 29 + blkfix 1 + SKIP-НП 2 = **48/59**.

## b7 (SKU 49-56, rows 50-57) — 56/59

| # | SKU | row | ART | Brand+Model | Category | Изменения |
|---|-----|-----|-----|-------------|----------|-----------|
| 1 | 49 | 50 | 2398156637 | Lavezzini LAPACK 550S_2x700 | **TRIP** | c5←c7; c36 ← RU 1058 chars (близнец r49 с другими размерами): камера 720x570x220 / 2 планки 550 мм / 60 м3/час / 160 кг / 840x700x1050 / 2 кВт / 380V; structural typo `<strong>...</strong>:` preserved |
| 2 | 50 | 51 | 2398169922 | Lavezzini MEGA | **TRIP** | c5←c7; c36 ← RU 839 chars: чрезвычайно требовательный клиент, камера 830х660х230 / 2 планки 600 мм / насос 100 м3/час / 220 кг / 900x800x1150 / 2.4 кВт / 380V (pkg dims 59/590/670/550 inconsistent source — preserved faithful) |
| 3 | 51 | 52 | 2398185496 | Valko Favola 415/25 Rapida (1410V154) | blknochg | — (c5/c7 RU «Вакуумный упаковщик», c36 762 chars RU без UA, без Ё) |
| 4 | 52 | 53 | 838995845 | Sirman Minicooker индукционный | **blkfix** | c36 Ё→Е x1 (лёгкого→легкого) |
| 5 | 53 | 54 | 1455941492 | HotmixPRO Gastro | **TRIP** | c5←c7 «Термомиксер HotmixPRO Gastro»; c36 ← RU 2125 chars (5 intro paras + 11 li applications + 13 li tech): 1500 Вт двигатель / 12500 об/мин / до 190°C / 250 рецептов / SD-карта / sous-vide; UA `&#39;` (пам'яті, 1'500, 2'300) dropped; «карамелізовату»→«карамелизовать» faithful intent; «Обсяг»→«Объем» (без Ё) |
| 6 | 54 | 55 | 838981620 | Sirman Mycook индукционный | **blkfix** | c36 Ё→Е x1 (лёгкого→легкого) |
| 7 | 55 | 56 | 524318041 | Pacojet II Sirman | **blkfix** | c36 Ё→Е x1 (Ёмкость→Емкость) |
| 8 | 56 | 57 | 881139623 | FROSTY JD-2 дозатор для соусов | blknochg | — (c5/c7 RU, c36 236 chars RU без UA, без Ё) |

**Итого b7:** TRIP 3 (r50/r51/r54) + blknotrip 0 + blknochg 2 (r52/r57) + blkfix 3 (r53/r55/r56) + SKIP-НП 0. Verify **234 PASS / 0 FAIL**.
**Cum после b7:** TRIP 19 + blknotrip 0 + blknochg 31 + blkfix 4 + SKIP-НП 2 = **56/59**.

## b8 ФИНАЛ (SKU 57-59, rows 58-60) — 59/59 ЗАКРЫТ

| # | SKU | row | ART | Brand+Model | Category | Изменения |
|---|-----|-----|-----|-------------|----------|-----------|
| 1 | 57 | 58 | 2044611060 | Frosty KS100T нож для шаурмы | **TRIP** | c5←c7 «Нож для шаурмы Frosty KS100T»; c36 ← RU 1717 chars (4 marketing paras + 3× ul): высококачественная нерж. сталь / лезвие 100 см (source-typo vs 100 мм во 2-м списке — preserved faithful) / толщина 0-8 мм / 2 лезвия (гладкое+зубчатое vs «круглое+зубчатое» — source list inconsistency preserved) / точило / отвертка / штифт / шнур 2,8 м / пластиковая ручка. UA `&#39;` («м'яса» x4) dropped. |
| 2 | 58 | 59 | 500049851 | Hendi 588017 Profi Line 0,5 л сифон | **TRIP** | c5←c7 «Сифон для сливок HENDI 588017 Profi Line 0,5 л»; c36 ← RU 580 chars (1 para + 9 li): для взбитых сливок/муссов/кремов/соусов / 0,5 л / 85x235 / нерж. сталь / 3 наконечника / для мелких и средних точек / горячие кремы и соусы / в присутствии клиента / N2O картриджи (не включены) / «Посудомоечная машина безопасна» source phrasing faithful. Literal `'` в «Об'єм»→«Объем». |
| 3 | 59 | 60 | 500051832 | Hendi 588024 Profi Line 1 л сифон | **TRIP** | c5←c7 «Сифон для сливок HENDI 588024 Profi Line 1 л»; c36 ← RU 392 chars: близнец r59 (1 л / 98x330) + «Данная модеь» (source-typo «модель»→«модеь») preserved + свежесть 14 дней / 2 насадки нерж + 1 полипропилен + щетка для чистки. Literal `'` в «Об'єм»→«Объем». |

**Итого b8:** TRIP 3 + blknotrip 0 + blknochg 0 + blkfix 0 + SKIP-НП 0. Verify **243 PASS / 0 FAIL**.
**Cum после b8 (ФИНАЛ chunk-070):** TRIP 22 + blknotrip 0 + blknochg 31 + blkfix 4 + SKIP-НП 2 = **59/59 ЗАКРЫТ**.
