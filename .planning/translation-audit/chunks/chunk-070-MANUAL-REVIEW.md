# chunk-070 MANUAL REVIEW (W2)

**Status:** chunk-070 b3 DONE 24/59 (cum TRIP 4 / blknotrip 0 / blknochg 18 / SKIP-НП 2; 198 PASS / 0 FAIL) — next b4 (SKU 25-32, rows 26-33)
**Last updated:** chunk-070 b3 DONE 24/59

## Структура

- Источник: `chunk-070.xlsx` (RO, 59 SKU rows 2..60)
- Operating target: `chunk-070-fixed.xlsx` (gitignored, скопирован из source при scaffold)
- Diff: `chunk-070-diff.md`
- Glossary: см. сводный `chunk-glossary-w2.md`
- Questions: `chunk-070-questions.md` (создаётся только при возникновении вопросов)

## Категории SKU (как в chunk-019/067/068/069)

- **TRIP**: c5←c7 + c36 ← faithful RU body (skel preserved + dims preserved + no UA-mark + no Ё)
- **blknotrip**: c5←c7 only, c36 без изменений (когда c36 уже RU OK)
- **blknochg**: c5/c7/c36 без изменений (когда уже всё RU OK / source genuine)
- **SKIP-НП**: forward-only override, brand ∈ {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA} → fixed строка НЕ тронута (тело из фида НП позже)

## Constraints (carry-over из chunk-069)

1. Source typos faithful: c5/c4/c6 — preserved verbatim; c36 body — preserved structural typos, fix только letter-misses в russian переводе.
2. Без Ё в RU c36: «Объем», «Ерш», «щеточки», «ножки», никогда Ё/ё.
3. UA `&#39;` → RU без апостр (drop). Literal `'` тоже drop.
4. «тэн» через «э» (не «тен»/«тэн» через «е»).
5. HTML entities preserved: `&Oslash;`, `&deg;`, `&mdash;`, `&ndash;`, `&times;` — нетронуты.
6. Skeleton preserved: `<p>`/`<ul>`/`<li>`/`<strong>`/`<br>` структура 1:1 с UA.
7. Размерности и числа preserved verbatim: длины, мощности, м3/час, кВт, Вт, мм, см, кг.

## SKIP-НП SKUs (планируется)

- b1: r3 HURAKAN HKN-VAC400E
- b2: r10 APACH AVM420

## Открытые вопросы

(будут добавлены по ходу батчей)


## b1 (SKU 1-8, rows 2-9) — 8/59

**Категории:** TRIP 3 (r4 SIRMAN 45К СЭ + r8 Hendi 975374 + r9 Hendi 970362) + blknochg 4 (r2 GoodFood VMP400DSB + r5 Forpack TE-45 + r6/r7 GASTRO HIT TE-39 187/227) + SKIP-НП 1 (r3 HURAKAN HKN-VAC400E).

**TRIP detail:**
- **r4 SIRMAN 45К СЭ** — c5 ← c7 «ТЕРМОУПАКОВОЧНЫЙ АППАРАТ SIRMAN 45К СЭ» (СЕ→СЭ как в c7); c36 ← RU body 564 chars (8 li): подогревается поверхность 385х125 мм, тефлоновое покрытие, нерж.сталь, 485х600х140 мм, 0.12 Вт, 220 В, 5 кг.
- **r8 Hendi Kitchen Line 975374** — c5 ← c7 (Hendi Kitchen Line порядок); c36 ← RU 839 chars (13 li): планка 420 мм бескамерный, два режима постоянный/пульсирующий, авто-выкл 10 мин, 5 мм шов 2-3 с, насос 16 л/мин, гофрированные пакеты 406 мм, 6,9 кг.
- **r9 Hendi 970362** — c5 ← c7; c36 ← RU 793 chars (`<h1>` Profi Line 350 — структурный typo поставщика preserved: title 970362 vs body 350; 12 li): нерж.сталь AISI 304 SB, насос 15 л / мин, шов 350 мм, 0,25 кВт, 220 В, 370x280x(H)170 мм. «твердыми» без Ё.

**blknochg detail (никаких изменений в c5/c36):**
- r2 GoodFood VMP400DSB — c5/c7 «Вакууматор GoodFood VMP400DSB» (без UA-маркеров, Cyrillic «Вакууматор» нейтральный); c36 уже RU 971 chars.
- r5 Forpack TE-45 — c5/c7 «Термоупаковочная машина Forpack TE-45»; c36 уже RU 527 chars (с source-typo «темепературе» preserved faithful).
- r6 GASTRO HIT TE-39 187x137 — c5/c7/c36 уже RU.
- r7 GASTRO HIT TE-39 227x178 — близнец r6.

**SKIP-НП detail:**
- r3 HURAKAN HKN-VAC400E — brand=HURAKAN, fixed.xlsx строка r3 НЕ тронута, тело из фида НП позже.

**Открытые вопросы:** 0 новых в b1.

**Verify:** 201 PASS / 0 FAIL.


## b2 (SKU 9-16, rows 10-17) — 16/59

**Категории:** TRIP 0 + blknochg 7 (r11-r17) + SKIP-НП 1 (r10 APACH AVM420).

**blknochg detail (никаких изменений):**
- r11 Dadaux Astorr 310 — c36 уже RU (Becker насос 10 m³/h / шов 420 мм / 220-230V / 70 кг).
- r12 Dadaux Astorr 416 — близнец r11.
- r13 Dadaux Astorr 421 — близнец r11.
- r14 Dadaux Astorr 570 — c36 уже RU (Becker 70 m³/h / шов 550 мм / 380-400V / 240 кг / planки 2×500 D/G + 2×710 AV/AR / 870×852×1075).
- r15 Orved Profi 2 для лотков — c36 уже RU (290х480х355 / 17,1 кг / 0,7 кВт; матрица 190х260 или 2× 190х137+137х95).
- r16 Petros (Orved) С308, 8 м3/час — c36 уже RU камерный купольная (332x335x170 / 0,6 кВт / 24 кг).
- r17 Orved Evox 25H (8mc) — c36 уже RU (8 м3/час, шов 25 мм source-typo preserved faithful; 303х293х110 / 0,45 кВт / 27 кг).

**SKIP-НП detail:**
- r10 APACH AVM420 — brand=APACH, fixed строка НЕ тронута, тело из фида НП позже.

**Открытые вопросы:** 0 новых в b2.

**Verify:** 192 PASS / 0 FAIL.


## b3 (SKU 17-24, rows 18-25) — 24/59

**Категории:** TRIP 1 (r25 Lavezzini LX420 запайщик) + blknochg 7 (r18..r24) + SKIP-НП 0.

**TRIP detail:**
- **r25 Lavezzini LX420** — c5 ← c7 «Запайщик пакетов Lavezzini LX420»; c36 ← RU 268 chars (5 li: пищевые пакеты до 5 мм / крашеный металл / шов 420 мм / 0,6 кВт / 80х550х260 мм / 4 кг).

**blknochg detail (никаких изменений в c5/c36):**
- r18 Orved Evox 25 4м3/час (c36 1047 chars RU).
- r19 PERS.PETROS LEVAC 4.
- r20 Petros (Orved) Lerica С412.
- r21 Petros LT1 для лотков «Термоупаковочная».
- r22 Petros (Orved) Lerica С420 2 планки.
- r23 LAVEZZINI ECO45 L напольный камерный 20 м3/час шов 450 мм 460x500x220 90 кг.
- r24 SIRMAN W8 30 Vertigo вертикальная EASY TOUCH Wi-Fi 4 м3/час 22 кг.

**Открытые вопросы:** 0 новых в b3.

**Verify:** 198 PASS / 0 FAIL.
