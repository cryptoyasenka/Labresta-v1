# chunk-068 MANUAL REVIEW (W2)

**Status:** chunk-068 b5 DONE 40/50 (cum TRIP 20 + blknotrip 0 + blknochg 18 + SKIP-НП 2; OQ 0; 124 PASS) — следующий b6 (SKU 41-48, rows 42-49)
**Last updated:** chunk-068 b5 DONE 40/50

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

## b3 (SKU 17-24, rows 18-25) — DONE 24/50

**Категории:** TRIP 2 + blknotrip 0 + blknochg 6 + SKIP-НП 0 = 8/8. Verify 103 PASS / 0 FAIL.

**TRIP (2) — Oztiryakiler посудомоечные машины:**
- r18 SKU17 ART 2460066584 **Oztiryakiler OBM1080TPD** Посудомоечная машина купольная: c5←c7 (`Посудомоечная машина Oztiryakiler OBM1080TPD`); c36 ← faithful RU body 29 строк (`<p>` lead + `<p><strong>Технические характеристики:</strong></p>` + 22-li main + `<p>Размеры в упаковке</p>` + 4-li упаковка; dims `1080/69/50x50/445/102/700/785/1960/9.66/380/52/102/132/152/192/2,8/69/40/112/820/750/1550`; «ідеально підходить … в ресторанах, кафе, барах, кав&#39;ярнях, пивних пабах» → «идеально подходит … в ресторанах, кафе, барах, кофейнях, пивных пабах», «Цикл миття, с» → «Цикл мойки, с», «понад 40» → «свыше 40», «Тип завантаження: купольна» → «Тип загрузки: купольная»).
- r19 SKU18 ART 2460074406 **Oztiryakiler OBY50TPDT** Посудомоечная машина фронтальная: c5←c7 (`Посудомоечная машина Oztiryakiler OBY50TPDT`); c36 ← faithful RU body 33 строки (`<p>` lead + `<p><strong>Технические характеристики:</strong></p>` + 26-li main + `<p>Размеры в упаковке</p>` + 4-li упаковка; dims `50/35/50x50/335/2,8/5/102/132/152/172/192/60/595/650/830/5.5/220/2,8/35/32/40/70/700/650/1000`; «5 програм мийки 102/132/152/172/192 с» → «5 программ мойки 102/132/152/172/192 с», «Розмір кошиків 50x50см» → «Размер корзин 50x50см», «Висота завантаження 335 мм» → «Высота загрузки 335 мм», «Три кошики в комплекті» → «Три корзины в комплекте», «Тип завантаження: фронтальне» → «Тип загрузки: фронтальная»).

**blknochg (6) — Gooder fixed rows НЕ изменены:**
- r20 SKU19 ART 2556977107 **Gooder BY.500**: c5==c7 RU OK, c36 без UA-mark, skel-eq True (len35=1412 / len36=1441).
- r21 SKU20 ART 2556993881 **Gooder BY.500D**: c5==c7 RU OK, c36 без UA-mark, skel-eq True.
- r22 SKU21 ART 2557006167 **Gooder BYM.01**: c5==c7 RU OK, c36 без UA-mark, skel-eq True.
- r23 SKU22 ART 2557011733 **Gooder BYM.02**: c5==c7 RU OK, c36 без UA-mark, skel-eq True.
- r24 SKU23 ART 2558087500 **Gooder BY.1000** купольная: c5==c7 RU OK, c36 без UA-mark, skel-eq True.
- r25 SKU24 ART 2558089725 **Gooder BY.1000D** купольная: c5==c7 RU OK, c36 без UA-mark, skel-eq True.

**SKIP-НП:** 0 в b3. Gooder НЕ в списке НП-эксклюзивных брендов.

**OQ:** 0 новых открытых вопросов.

**Verify breakdown:** 50 ART regression + 2 TRIP × 7 = 14 + 6 blknochg × 3 = 18 + b1/b2 regression (10 prior TRIP c5==c7 + 5 prior blknochg c5 unchanged + 6 SKIP-НП r10 cols unchanged) = 21. Total **103 PASS / 0 FAIL**.

## b4 (SKU 25-32, rows 26-33) — DONE 32/50

**Категории:** TRIP 6 + blknotrip 0 + blknochg 1 + SKIP-НП 1 = 8/8. Verify 130 PASS / 0 FAIL.

**TRIP (6) — ASBER посудомоечные машины DD:**
- r28 SKU27 ART 2687383117 **ASBER GTX-H500 DD** купольного типа: c5←c7 (`Посудомоечная машина ASBER GTX-H500 DD`); c36 ← faithful RU body 18 строк (`<p>` lead «подходит для кастрюль, тарелок, стаканов, бокалов» + `<p>Технические характеристики:</p>` + 15-li main; dims `500/40/90/120/180./500х500/33/7/440/2/1/630х750х1482/11,25/380`; «Зворотній клапан» → «Обратный клапан», «Вбудований дозатор для миючого і ополіскуючого засобу» → «Встроенный дозатор для моющего и ополаскивающего средства», «контейнер-вставка для столових приборів» → «контейнер-вставка для столовых приборов»).
- r29 SKU28 ART 2687394138 **ASBER GT-500 DD** фронтальная: c5←c7; c36 ← 16-строчный body (`<p>` lead «підходить для посуду заввишки до 320 мм» → «подходит для посуды высотой до 320 мм» + 13-li main; dims `500/320/120/500х500/25/7/2/1/600х605х830/3.4/220`).
- r30 SKU29 ART 2795786523 **ASBER GE-500 RD B DD (помпа зливу)** фронтального типа: c5←c7 (`Посудомоечная машина ASBER GE-500 RD B DD (помпа слива)`); c36 ← 17-строчный body с `<h2>` + 14-li main (dims `2/500/2/120/500х500/25/7/2/1/600х605х830/3,4/220`; ключевые «Дренажна помпа» → «Дренажная помпа», «перистальтичний» дозатор → «перистальтический», «електромеханічна» → «электромеханическая», «Об&#39;єм бака/бойлера» → «Объем бака/бойлера» (без Ё)).
- r31 SKU30 ART 2796153409 **ASBER GEX-H500 RD DD** купольная: c5←c7; c36 ← 19-строчный body (`<p>` lead + 16-li main; dims `500/40/90/180/500х500/33/7/440/2/1/630х750х1482/11,25/380`; ключевые «Продуктивність: 40 касет/годину» → «Производительность: 40 кассет/час», перистальтический + электромеханическая).
- r32 SKU31 ART 2796156408 **ASBER GT-500 RD DD** фронтального типа: c5←c7; c36 ← 16-строчный body с `<h2>` + 13-li main (dims `2/500/2/90/120/180/500х500/25/7/2/1/600х605х830/3,4/220`; перистальтический + электронная).
- r33 SKU32 ART 2796159643 **ASBER GE-500 RD DD** фронтального типа: c5←c7; c36 ← 16-строчный body с `<h2>` + 13-li main; **source typo preserved:** c4/c5/c6/c7 говорят «GE-500 RD DD» (без B), но c35 body начинается с «ASBER GE-500 RD B DD фронтального типу» — типа copy-paste from r30; preserved verbatim в RU («ASBER GE-500 RD B DD фронтального типа»); dims `2/500/2/120/500х500/25/7/2/1/600х605х830/3,4/220`.

**blknochg (1):**
- r26 SKU25 ART 2565641321 **Krupps C537TDGT Advance со встроенным сливным насосом DP45K**: c5==c7 RU OK, c36 без UA-mark, skel-eq **False** (len35=549 / len36=594, source variance — c36 содержит дополнительную li «1 держатель для тарелок» отсутствующую в c35). Fixed строка НЕ изменена (источник варианс не правим).

**SKIP-НП (1):**
- r27 SKU26 ART 2603547529 **APACH AF400 DDP** Посудомоечная машина — brand=APACH ⇒ НП forward-only override; fixed строка (c4/c5/c6/c7/c35/c36) НЕ тронута, тело из НП-фида позже. cum SKIP-НП 2/?.

**OQ:** 0 новых открытых вопросов.

**Verify breakdown:** 50 ART regression + 6 TRIP × 7 = 42 + 1 blknochg × 3 = 3 + 1 SKIP-НП × 6 = 6 + b1/b2/b3 regression (12 prior TRIP c5==c7 + 11 prior blknochg c5 unchanged + 6 SKIP-НП r10 cols unchanged) = 29. Total **130 PASS / 0 FAIL**.

## b5 (SKU 33-40, rows 34-41) — DONE 40/50

**Категории:** TRIP 2 + blknotrip 0 + blknochg 6 + SKIP-НП 0 = 8/8. Verify 124 PASS / 0 FAIL.

**TRIP (2):**
- r35 SKU34 ART 659353448 **Hendi 696002 ёрш для мойки стаканов**: c5←c7 (`Ерш для мойки стаканов Hendi 696002`); c36 ← 7-строчный body (`<p>` lead + `<ul>` + 4-li; dims `3/4/190x100x180`; «Йорж для миття склянок з трьома щіточками» → «Ерш для мойки стаканов с тремя щеточками» (без Ё); «Виготовлений з поліпропілену» → «Изготовлен из полипропилена», «3 щітки з нейлону» → «3 щетки из нейлона», «На дні 4 ніжки-присоски» → «На дне 4 ножки-присоски»).
- r36 SKU35 ART 1500252450 **Krupps C327DGT Advance фронтальная** (различный SKU от b2 r12 ART 2213453082 — без DP45K насоса): c5←c7; c36 ← 12-строчный body с `<h2>` (1 h2-lead «Размер корзин: 350х350 мм» + `<p>Технические характеристики:</p>` + 10-li; dims `2/327/350х350/2/240/2/2/1/1/2/2,79/220/420х548х660`; ключевые «висота склянки 240 мм» → «высота стакана 240 мм», «довжина циклу 2 хв» → «длина цикла 2 мин», «тримач для приладів/тарілок» → «держатель для приборов/тарелок»).

**blknochg (6):**
- r34 SKU33 ART 506147414 **GGM GPE5 полировщик для бокалов**: c5==c7 RU OK, c36 без UA-mark, skel-eq True; fixed строка НЕ изменена.
- r37 SKU36 ART 753318879 **GGG GPE8 полировщик для бокалов**: c5==c7 RU OK, c36 без UA-mark, skel-eq True; fixed строка НЕ изменена.
- r38 SKU37 ART 2389346752 **ATA ALP 43** Посудомоечная котломоечная машина: c5==c7 RU OK, c36 без UA-mark, skel-eq True (len35=1771/len36=1868 source variance); fixed строка НЕ изменена. ATA brand НЕ в списке НП-эксклюзивных, но c5/c7 уже RU genuine.
- r39 SKU38 ART 2389351402 **ATA ALP 02S** котломоечная: c5==c7 RU OK, c36 без UA-mark, skel-eq True; fixed строка НЕ изменена.
- r40 SKU39 ART 2389356892 **ATA ALP 40** котломоечная: c5==c7 RU OK, c36 без UA-mark, skel-eq True; fixed строка НЕ изменена.
- r41 SKU40 ART 2389361331 **ATA ALP 02GS** котломоечная: c5==c7 RU OK, c36 без UA-mark, skel-eq True; fixed строка НЕ изменена.

**SKIP-НП:** 0 в b5.

**OQ:** 0 новых открытых вопросов.

**Verify breakdown:** 50 ART regression + 2 TRIP × 7 = 14 + 6 blknochg × 3 = 18 + b1..b4 regression (18 prior TRIP c5==c7 + 12 prior blknochg c5 unchanged + 2 SKIP-НП × 6 = 12) = 42. Total **124 PASS / 0 FAIL**.

