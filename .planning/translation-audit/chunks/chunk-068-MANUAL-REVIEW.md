# chunk-068 MANUAL REVIEW (W2)

**Status:** chunk-068 b2 DONE 16/50 (cum TRIP 10 + blknotrip 0 + blknochg 5 + SKIP-НП 1; OQ 0; 109 PASS) — следующий b3 (SKU 17-24, rows 18-25)
**Last updated:** chunk-068 b2 DONE 16/50

## Структура

- Источник: `chunk-068.xlsx` (RO)
- Operating target: `chunk-068-fixed.xlsx` (gitignored, скопирован из source при scaffold)
- Diff: `chunk-068-diff.md`
- Glossary: см. сводный `chunk-glossary-w2.md`
- Questions: `chunk-068-questions.md` (создаётся только при возникновении вопросов)

## Категории SKU (как в chunk-019/067)

- **TRIP (blk триплет):** c5==c4 UA-leak ИЛИ c35==c36 UA both → перевод c5←c7 + c36 faithful RU body skel==c35 / dims match
- **blknotrip:** c35!=c36 whitespace/skel-eq True (минор whitespace-only) → c5/c36 переписать с faithful skel c35
- **blknochg:** c5==c7 genuine RU + c36 genuine RU без UA-mark → НЕ трогаем
- **SKIP-НП:** brand ∈ {HURAKAN, APACH, FAGOR, TATRA, COLD, PROJECT SYSTEMS, ASTORIA, ARRIS, MAXIMA} → НЕ трогаем, тело из НП-фида позже

## Constraints (из chunk-067 carry-over)

- Без Ё в RU c36; UA `&#39;` → RU без апостр
- «тэн» через «э» (не «е», не «ё») — established in chunk-067 b7/b8
- Source typos faithful live (см. chunk-067: «конвеерный», «попа зливу», 1-мм dim variance)
- HTML entities preserved (`&mdash;`, `&ndash;`, `&Oslash;`, `&deg;`, `&#39;`)

## b1 (SKU 1-8, rows 2-9) — DONE 8/50

**Категории:** TRIP 4 + blknotrip 0 + blknochg 4 + SKIP-НП 0 = 8/8. Verify 90 PASS / 0 FAIL.

**TRIP (4) — Frosty посудомоечные/стакано-мойки:**
- r6 SKU5 ART 2080385348 **Frosty ECO35** Машина для мойки стаканов (бокалов): c5←c7 (`Машина для мойки стаканов (бокалов) Frosty ECO35`); c36 ← faithful RU body 25 строк (16-li main + 4-li комплект + 1-li материал; dims `30/350х350/276/2/1,5/9/3/55/2/4/2,70/220/430/485/660/30.00/1/1`; «миття» → «мойка», «келихів» → «бокалов», «корзин/год» → «корзин/час», «Об&#39;єм мийного бака» → «Объем моечного бака», «Опція: зливний насос» → «Опция: сливной насос», `&ordm;С` preserved).
- r7 SKU6 ART 2080393304 **Frosty ECO1000 3ph** Посудомоечная машина купольного типа: c5←c7; c36 24 строки (14-li main + 5-li комплект + 1-li материал; dims `60/20/15`, `1080/360/270` корзин/тарелок/час, `9,80` кВт/`380`В; «3 мийні цикли: 1/3 і 4 хв.» → «3 моечных цикла: 1/3 и 4 мин.», «Максимальний діаметр тарілок» → «Максимальный диаметр тарелок»).
- r8 SKU7 ART 2080397413 **Frosty ECO50 1ph** Посудомоечная машина фронтального типа: c5←c7; c36 27 строк (17-li main + 5-li комплект + 1-li материал; `<p><strong>Технические характеристики:</strong></p>`; dims `60/20`, `1080/360`, `3,40` кВт/`220`В; «2 мийні цикли: 1 хв і 3 хв» → «2 моечных цикла: 1 мин и 3 мин», «Вага: 60 кг» preserved «Вес: 60 кг»).
- r9 SKU8 ART 2080400876 **Frosty ECO50 3ph** Посудомоечная машина фронтального типа: c5←c7; c36 27 строк (same template как r8 но `6,65` кВт/`380`В + «Вага: 60.00» → «Вес: 60.00»; small variations «Допустимий тиск подачі води 2-4 бар» без двоеточия).

**blknochg (4) — fixed rows НЕ изменены:**
- r2 SKU1 ART 2045399173 **Empero EMP.500-380-SDF** Посудомоечная машина: c5==c7 RU OK, c36 без UA-mark, skel-eq True (len35=1388 / len36=1406).
- r3 SKU2 ART 2053905002 **Crystal CRW 500 TPD** Посудомоечная машина с помпой слива: c5==c7 RU OK, c36 без UA-mark, skel-eq True.
- r4 SKU3 ART 2053911972 **Crystal CRW 1000 TPD** Посудомоечная машина с помпой слива (купольная): c5==c7 RU OK, c36 без UA-mark, skel-eq True.
- r5 SKU4 ART 2054635608 **Adler EVO 1000 PD** Посудомоечная машина: c5==c7 RU OK, c36 без UA-mark, skel-eq True.

**SKIP-НП:** 0 в b1.

**OQ:** 0 новых открытых вопросов.

**Verify breakdown:** 50 ART regression + 4 TRIP × 7 checks (c4 untouched / c5==c7 / skel-eq / dims-eq / no UA / no Ё / nl-eq) = 28 + 4 blknochg × 3 checks (c4/c5/c36 unchanged vs RO) = 12. Total **90 PASS / 0 FAIL**.

## b2 (SKU 9-16, rows 10-17) — DONE 16/50

**Категории:** TRIP 6 + blknotrip 0 + blknochg 1 + SKIP-НП 1 = 8/8. Verify 109 PASS / 0 FAIL.

**TRIP (6):**
- r11 SKU10 ART 2191921582 **Frosty ECO40 1ph** стаканомойка: c5←c7 (`Машина для мытья стаканов (бокалов) Frosty ECO40 1ph` — c7 использует «мытья», не «мойки» как в r6 ECO35; preserve c7 verbatim); c36 25 строк (16-li main + 4-li комплект + 1-li материал; dims `60/30/400х400/276/2/1/2/1,5/11/3/55/2/4/2,50/220/480/517/696/30.00/1/1`; «Подуктивність» source typo → «Производительность» (correct RU)).
- r12 SKU11 ART 2213453082 **Krupps C327DGT Advance** со встроенным сл. насосом DP45K: c5←c7; c36 31 строка с `<h2>` header («Размер корзин: 350х350 мм»); 24-li main + 4-li упаковка; dims включают `<h2>2/2`, `327`, `45`, `350х350×2`, `30`, `240`, `36/420/485/660`, `2.79/220`, `90/120/150/180`, packaging `48/670/570/840`.
- r13 SKU12 ART 2213463204 **Krupps C537DGT Advance** со встроенным сл. насосом DP45K: c5←c7; c36 31 строка с `<h2>` («Подходит для тарелок высотой до 350 мм и бокалов высотой до 310 мм»); 24-li main + 4-li упаковка; ключевые dims: `350`, `310`, `500х500`, `30`, `395`, `60/585/600/815`, `3.12/220`, `32-40` посуды, packaging `69.2/800/680/1000`.
- r14 SKU13 ART 2221209761 **Winterhalter UC-M 012V0031** фронтальная: c5←c7; c36 20 строк (3 `<p>` блока + 18-li); preserved source typos «Посудомийна машина Посудомийна машина» dup (→ «Посудомоечная машина Посудомоечная машина»), «1цикл» no-space (→ «1цикл»); termostop / atmospheric bойlер / Touch Screen / Energy / Integrated softener; dims `012/0031./4/66/40/28/24/77/48/32/22/77/500х500×2/404/15,3/62/30/4/60,/120,/180/240/180/2,4/1/637х600х760/7,9/380`.
- r15 SKU14 ART 2278734126 **Oztiryakiler OBY35TPDT**: c5←c7; c36 22 строки с `<h2>` («Панель управления Touch. Корпус, моечный и нагревательные баки из нержавеющей стали...»); 15-li main + 4-li упаковка; dims `<h2>2×2`, `30/425/465/630/3.3/220/2,5/30`, `20-32` посуды, packaging `35/570/530/750`.
- r16 SKU15 ART 2278736666 **Oztiryakiler OBY40TPDT**: c5←c7; c36 22 строки (same template как r15 но более крупная машина: `35/475/545/765`, посуды `32-40`, packaging `40/650/560/890`).

**blknochg (1):**
- r17 SKU16 ART 2289323710 **Silanos S021 PS PD/РВ DIGIT** (стаканомойка): c5==c7 RU OK, c36 без UA-mark, skel-eq **False** (len35=1349 vs len36=1353, source variance — fixed строка НЕ изменена).

**SKIP-НП (1):**
- r10 SKU9 ART 2176569021 **APACH AC800DIG DD** Посудомоечная машина — brand=APACH ⇒ НП forward-only override; fixed строка (c4/c5/c6/c7/c35/c36) НЕ тронута, тело из НП-фида позже. cum SKIP-НП 1/?.

**OQ:** 0 новых открытых вопросов.

**Verify breakdown:** 50 ART + 6 TRIP × 7 = 42 + 1 SKIP-НП × 6 (all cols unchanged) = 6 + 1 blknochg × 3 = 3 + b1 regression 4 TRIP c5==c7 + 4 blknochg c5 unchanged = 8. Total **109 PASS / 0 FAIL**.

