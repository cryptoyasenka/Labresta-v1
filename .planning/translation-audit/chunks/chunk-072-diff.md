# chunk-072 diff (W2, продолжение chunk-071)

**Status:** chunk-072 b3 DONE 24/89 (cum TRIP 22 / blknotrip 0 / blknochg 2 / blkfix 0 / SKIP-НП 0; 413 PASS / 0 FAIL) — next b4 (SKU 25-32, rows 26-33)
**Last updated:** chunk-072 b3 DONE 24/89

**Источник:** `.planning/translation-audit/chunks/chunk-072.xlsx` (89 SKU, rows 2..90, ART 1173123408..2197264833).
**Фикс-таргет:** `.planning/translation-audit/chunks/chunk-072-fixed.xlsx` (gitignored).
**Бренды:** Hendi 88 (NORMAL) + **FAGOR 1 SKIP-НП** (r83 сушильная машина FAGOR SCP-10).
**Категории товаров:** доски разделочные HACCP GN 1/2 + малая серия, точильные камни/станки, термометры с зондом, контейнеры, сифоны, янагиба-ножи, сушильные машины (НП).

## Workflow
- Batch=8 SKU; 2 commits/batch (C1 content + C2 marker); push после C2.
- TRIP=c5←c7 + c36 RU faithful; blknotrip=c5←c7 only; blknochg=без изменений; blkfix=c36 minor (Ё→Е и т.п.).
- SKIP-НП forward-only: пометить в MR, не трогать xlsx.
- Без Ё в c36; UA `&#39;` AND literal `'` → drop; «тэн»→«э».
- Source typos faithful в c5/title; structural typos preserved.
- chunk-NN.xlsx RO; modify chunk-NN-fixed.xlsx.

## Coverage plan
- b1..b11 = 88 SKU; b12 финал = 1 SKU. Возможна корректировка под классификации.
- SKIP-НП candidate: r83 (FAGOR SCP-10 M E 1P COMPACT CONCEPT сушильная машина).

## b1 (SKU 1-8, rows 2-9) — 8/89

| # | SKU | row | ART | Brand+Model | Category | Изменения |
|---|-----|-----|-----|-------------|----------|-----------|
| 1 | 1 | 2 | 1173123408 | Hendi 826102 доска HACCP GN 1/2 белая | **TRIP** | c5←c7; c36 RU 1348 chars. Новая GN 1/2 серия 8261xx (dims 265x325x(H)12). **Source-quirk: `<h3>` «- біла Hendi 826102 - біла» double color** preserve → «- белая Hendi 826102 - белая». Reused GN12_TABLE + iframe C8b5szTz-0g (тот же что chunk-071 b10). |
| 2 | 2 | 3 | 1173129125 | Hendi 826126 доска HACCP GN 1/2 голубая (синяя) | **TRIP** | c5←c7; c36 RU 1340 chars. Normal `<h3>` (single color). Usage table «синий → рыба». |
| 3 | 3 | 4 | 1173132435 | Hendi 826157 доска HACCP GN 1/2 желтая | **TRIP** | c5←c7; c36 RU 1341 chars. Usage table «желтый → сырая птица». |
| 4 | 4 | 5 | 1173141822 | Hendi 826133 доска HACCP GN 1/2 зеленая | **TRIP** | c5←c7 «зелёная» **(Ё в c5 от source c7 — allowed)**; c36 RU 1342 chars «зеленая» без Ё. Usage table «зеленый → овощи». |
| 5 | 5 | 6 | 1173143617 | Hendi 826140 доска HACCP GN 1/2 коричневая | **TRIP** | c5←c7; c36 RU 1344 chars. **Source-quirk: `<h3>` «- коричневаяизготовлена» glued (RU+RU without space, plus UA «з поліетилену»)** preserve glue → «- коричневаяизготовлена из полиэтилена HDPE 500.» |
| 6 | 6 | 7 | 1173145385 | Hendi 826119 доска HACCP GN 1/2 красная | **TRIP** | c5←c7; c36 RU 1342 chars. Normal `<h3>` (no glue typo). |
| 7 | 7 | 8 | 2045395280 | GoodFood DH1 воронка-дозатор для соусов и кремов | **blknochg** | c5 уже RU == c7. c36 уже pure RU. UA только в c35 — forward-only, не трогаем. |
| 8 | 8 | 9 | 2046058563 | GoodFood CDM10 аппарат для декорирования тортов | **blknochg** | c5 уже RU == c7. c36 уже pure RU. UA только в c35 — forward-only, не трогаем. |

**Итого b1:** TRIP 6 + blknotrip 0 + blknochg 2 + blkfix 0 + SKIP-НП 0. Verify **285 PASS / 0 FAIL**.
**Cum после b1:** TRIP 6 + blknotrip 0 + blknochg 2 + blkfix 0 + SKIP-НП 0 = **8/89**. UNPROC = 81 (rows 10-90).


## b2 (SKU 9-16, rows 10-17) — 16/89

| # | SKU | row | ART | Brand+Model | Category | Изменения |
|---|-----|-----|-----|-------------|----------|-----------|
| 1 | 9 | 10 | 2102932030 | Gi Metal AC-TPF11 нож-лопатка для теста | **TRIP** | c5←c7 (31 chars); c36 RU 359 chars. Маленький короткий блок: <p> описание + <ul> Технические характеристики (Материал/Размеры/Вес) + <ul> Размер (ширина/длина). |
| 2 | 10 | 11 | 2102943418 | Gi Metal AC-TPM нож-лопатка для теста | **TRIP** | c5←c7 (29 chars); c36 RU 360 chars. Тот же шаблон что r10, dims 75×150, вес 0.18 кг. |
| 3 | 11 | 12 | 2121016179 | Hendi 198254 газовая горелка для крем брюле | **TRIP** | c5←c7 (43 chars); c36 RU 616 chars. **Source-quirk: c4 «Газова пальник» (UA gender mismatch — feminine adj + masc noun) → c7/c5 normal RU «Газовая горелка». Body h2 RU mirrors c7**. «Кухарський факел» → «Поварской факел». UA `&#39;` в «полум&#39;я»/«м&#39;яса» dropped. |
| 4 | 12 | 13 | 2852907601 | Frosty KS100E нож для шаурмы электрический | **TRIP** | c5←c7 (28 chars); c36 RU 587 chars. **Source-quirk: «корпус: нержавеющая сталь пластик (черный)» — отсутствует разделитель между «сталь» и «пластик» (RU+RU без знака — повторяет UA «нержавіюча сталь пластик»)** preserve glue. |
| 5 | 13 | 14 | 964757839 | Hendi 267240 электронож для шаурмы | **TRIP** | c5←c7 (34 chars); c36 RU 807 chars. UA `&#39;` в «м&#39;яса» dropped. Габариты «194x113x (H)173мм» (пробел перед `(H)` faithful). |
| 6 | 14 | 15 | 1156825442 | Hendi 588031 Kitchen Line сифон для сливок 0,25 л | **TRIP** | c5←c7 (49 chars); c36 RU 509 chars. UA `&#39;` в «Об&#39;єм» dropped → «Объем». «Фіолетовий колір» → «Фиолетовый цвет». «балончиками для збитих вершків (N₂O)» → «баллончиками для взбитых сливок (N₂O)». |
| 7 | 15 | 16 | 873362379 | Hendi 551813 воронка-дозатор для соусов и кремов | **TRIP** | c5←c7 (50 chars uppercase); c36 RU 338 chars. **Source-quirk: «Призначений» (masc) для «Воронка» (fem) — gender mismatch preserve → RU «Предназначен» (masc)**. Literal `'` в «Об'єм» dropped → «Объем». |
| 8 | 16 | 17 | 873550393 | Hendi 271407 термометр цифровой с зондом | **TRIP** | c5←c7 (65 chars uppercase); c36 RU 630 chars. «Протиударний» → «Противоударный». Режим "lock mode" preserved (latin literal). |

**Итого b2:** TRIP 8 + blknotrip 0 + blknochg 0 + blkfix 0 + SKIP-НП 0. Verify **437 PASS / 0 FAIL**.
**Cum после b2:** TRIP 14 + blknotrip 0 + blknochg 2 + blkfix 0 + SKIP-НП 0 = **16/89**. UNPROC = 73 (rows 18-90).


## b3 (SKU 17-24, rows 18-25) — 24/89

| # | SKU | row | ART | Brand+Model | Category | Изменения |
|---|-----|-----|-----|-------------|----------|-----------|
| 1 | 17 | 18 | 1144489433 | Hendi 271148 термометр бесконтактный лазерный | **TRIP** | c5←c7 (47 chars); c36 RU 617 chars. **Source-quirk: <p> body начинается «термометр с зондом» хотя c7 title «бесконтактный» — structural mismatch preserve**. Iframe `MsXPbN-Jm2A` preserve verbatim. |
| 2 | 18 | 19 | 1156808407 | Hendi 975893 Kurt Scheller Edition сифон для сливок 0,5 л бирюзовый | **TRIP** | c5←c7 (61 chars); c36 RU 468 chars. Literal `'` в «Об'єм» dropped → «Объем». «Не може бути вимитий» → «Не может быть вымыт». |
| 3 | 19 | 20 | 1158022720 | Hendi 271230 термометр с зондом цифровой (-50/350°C) | **TRIP** | c5←c7 (52 chars); c36 RU 706 chars. <p> title uppercase «ТЕРМОМЕТР ЦИФРОВОЙ С ЗОНДОМ». Iframe `98xxO29PNQg` preserve. Режим "hold" (latin literal). |
| 4 | 20 | 21 | 1158035300 | Hendi 271308 термометр цифровой со складным зондом (-50/350°C) | **TRIP** | c5←c7 (62 chars); c36 RU 534 chars. **Source-quirk: title c7 «-50/350°C» vs body <p> «-50/+300°C» (range mismatch) preserve faithful**. «0 °с» (lowercase с) preserve в body. |
| 5 | 21 | 22 | 1158149014 | Hendi 572412 Kitchen Line порционная ложка 1/24 л, Ø53 мм | **TRIP** | c5←c7 (71 chars uppercase); c36 RU 406 chars. **Source-quirks preserve: «Місткість в л::» double colon → «Емкость в л::»; «Виготовлений» (masc) для «Ложка» (fem) gender mismatch → RU «Изготовлен»**. |
| 6 | 22 | 23 | 1158152359 | Hendi 572610 Kitchen Line порционная ложка 1/36 л, Ø48 мм | **TRIP** | c5←c7 (72 chars uppercase); c36 RU 376 chars. Same template r22. Layout «гастрономии. <br/>\n<br/> Особенности» (single space delta vs r22). |
| 7 | 23 | 24 | 1158156178 | Hendi 572719 Kitchen Line порционная ложка 1/40, Ø44 мм | **TRIP** | c5←c7 (70 chars uppercase); c36 RU 375 chars. Same r22 template. |
| 8 | 24 | 25 | 1158158850 | Hendi 759233 Profi Line порционная ложка 1/24, Ø53 мм | **TRIP** | c5←c7 (68 chars uppercase); c36 RU 366 chars. **Отличия от r22-24: «Profi Line» mixed case (не all caps), «Емкость в л:» single colon (без typo), «Ручка из полиамида» новый item**. |

**Итого b3:** TRIP 8 + blknotrip 0 + blknochg 0 + blkfix 0 + SKIP-НП 0. Verify **413 PASS / 0 FAIL**.
**Cum после b3:** TRIP 22 + blknotrip 0 + blknochg 2 + blkfix 0 + SKIP-НП 0 = **24/89**. UNPROC = 65 (rows 26-90).
