# chunk-072 diff (W2, продолжение chunk-071)

**Status:** chunk-072 b5 DONE 40/89 (cum TRIP 33 / blknotrip 0 / blknochg 7 / blkfix 0 / SKIP-НП 0; 359 PASS / 0 FAIL) — next b6 (SKU 41-48, rows 42-49)
**Last updated:** chunk-072 b5 DONE 40/89

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


## b4 (SKU 25-32, rows 26-33) — 32/89

| # | SKU | row | ART | Brand+Model | Category | Изменения |
|---|-----|-----|-----|-------------|----------|-----------|
| 1 | 25 | 26 | 1158559861 | Hendi 551400 насадки для кондитерских мешков комплект 12 шт | **TRIP** | c5←c7 (78 chars, no-op — c5 уже RU); c36 RU 247 chars. **Source-quirk: «компл. 12 шт» в названии, но body «7 предметов» (number mismatch) preserve faithful**. h2 в c36 уже RU — translate body only (UA `<p>` блоки). |
| 2 | 26 | 27 | 1158566905 | Hendi 551592 насадки для кондитерских мешков комплект 5 шт | **TRIP** | c5←c7 (64 chars, no-op); c36 RU 362 chars. h2 + первый `<p>` уже RU preserve, остальные `<p>` translated. **Source-quirk: «гострим краях» UA gen/loc/dat hybrid → RU «острым краям»** preserve grammatical pattern. |
| 3 | 27 | 28 | 1158638980 | Hendi Profi Line 515143 ролик для теста перфорирующий | **blknochg** | c5 уже RU == c7 (no-op); c36 уже pure RU (len 204 vs c35 UA 201). UA только в c35 — forward-only. **Source-quirk: c35/c36 упоминают SKU 515051 хотя c4/c5/c7 указывают 515143** preserve. |
| 4 | 28 | 29 | 1158684841 | Hendi 676905 форма силиконовая Mini-Muffins 11 ячеек | **blknochg** | c5 уже RU == c7; c36 уже pure RU (1785 chars, full table + iframe `U-MpL0Ztt1k`). UA только в c35 — forward-only. HTML entities `&deg;` `&Oslash;` preserve. |
| 5 | 29 | 30 | 1160171502 | Hendi 515020 скалка для раскатки теста деревянная 39,5 см | **TRIP** | c5←c7 (58 chars); c36 RU 194 chars. Literal `'` в «дерев'яна» dropped → «деревянная». Малый блок: h2 + 3 `<p>`. |
| 6 | 30 | 31 | 1160207848 | Hendi 659403 скребок для теста 70x116x(L)410 мм | **TRIP** | c5←c7 (48 chars); c36 RU 649 chars. **Source-quirk: «110'C» literal `'` used as degree → translated to proper «110°C»** (drop `'`, use ° sign for semantics). Iframe `Gnw_h-FEhHY` preserve (тот же что силиконовые шпатели/скребки). |
| 7 | 31 | 32 | 1161547097 | Hendi 682401 форма для выпечки прямоугольная 300x110x75 мм | **TRIP** | c5←c7 (61 chars); c36 RU 120 chars (малый). **Source-quirk: c7 title «Форма для выпечки - прямоугольная» с тире, body без тире «Форма для выпечки прямоугольная»** preserve faithful. |
| 8 | 32 | 33 | 1161550239 | Hendi 673416 высечка кондитерская 14 шт гладкий край ø19-112 мм | **TRIP** | c5←c7 (66 chars); c36 RU 430 chars. Iframe `Lu-VBvLVe2c` preserve verbatim. «Висічка кондитерська» → «Высечка кондитерская». |

**Итого b4:** TRIP 6 + blknotrip 0 + blknochg 2 + blkfix 0 + SKIP-НП 0. Verify **385 PASS / 0 FAIL**.
**Cum после b4:** TRIP 28 + blknotrip 0 + blknochg 4 + blkfix 0 + SKIP-НП 0 = **32/89**. UNPROC = 57 (rows 34-90).


## b5 (SKU 33-40, rows 34-41) — 40/89

| # | SKU | row | ART | Brand+Model | Category | Изменения |
|---|-----|-----|-----|-------------|----------|-----------|
| 1 | 33 | 34 | 1161553274 | Hendi 674413 высечка кондитерская 14 шт зубчатый край ø18-108 мм | **TRIP** | c5←c7 (67 chars); c36 RU 447 chars. Iframe `Lu-VBvLVe2c` preserve. «Зубчастий (гофрований)» → «Зубчатый (гофрированный)». |
| 2 | 34 | 35 | 1161570960 | Hendi 673782 высечка кондитерская 8 шт бабочка | **blknochg** | c5 уже RU == c7; c36 уже pure RU 437 chars. UA только в c35 — forward-only. |
| 3 | 35 | 36 | 1162111467 | Hendi 673768 высечка кондитерская 9 шт звезда | **blknochg** | c5 уже RU == c7; c36 уже pure RU. UA только в c35. **Source-quirk: c35 UA typo «форма - метелик» (butterfly) но продукт «зірка» (star); c36 already correctly «звезда»** — leave alone. |
| 4 | 36 | 37 | 1162152815 | Hendi 673751 высечка кондитерская 9 шт квадратная | **blknochg** | c5 уже RU == c7; c36 уже pure RU. Forward-only. |
| 5 | 37 | 38 | 1166434765 | Hendi 880906 контейнер для теста 14 л 600x400х(H)70 мм | **TRIP** | c5←c7 (55 chars); c36 RU 168 chars. **Source-quirks: title (H)70 vs body external (H)75 mismatch; «внутрішні Габарити» mid-sentence cap asymmetric vs «Габарити зовнішні» → RU «внутренние Габариты»; c7 mixed Latin x + Cyrillic х** preserve. |
| 6 | 38 | 39 | 1166441242 | Hendi 880913 контейнер для теста 18 л 600x400х(H)90 мм | **TRIP** | c5←c7 (55 chars); c36 RU 169 chars. Те же quirks что r38: (H)90 vs (H)95, asymmetric cap. «Місткість» → «Емкость». |
| 7 | 39 | 40 | 1166442240 | Hendi 880920 контейнер для теста 24 л 600x400х(H)130 мм | **TRIP** | c5←c7 (56 chars); c36 RU 173 chars. **Source-quirks: title «24 л» vs body «Ємність - 28 л» volume mismatch; «Габарити внутрішні» (слово первым — другой order vs r38/r39 «внутрішні Габарити»)** preserve. |
| 8 | 40 | 41 | 1166446086 | Hendi 880968 крышка для контейнеров для теста 600x400 мм | **TRIP** | c5←c7 (56 chars); c36 RU 173 chars. **Source-quirk: продукт — LID но body описывает CONTAINER 28 л (структурное несоответствие)** preserve. |

**Итого b5:** TRIP 5 + blknotrip 0 + blknochg 3 + blkfix 0 + SKIP-НП 0. Verify **359 PASS / 0 FAIL**.
**Cum после b5:** TRIP 33 + blknotrip 0 + blknochg 7 + blkfix 0 + SKIP-НП 0 = **40/89**. UNPROC = 49 (rows 42-90).


## b6 (SKU 41-48, rows 42-49) — 48/89

| # | SKU | row | ART | Brand+Model | Category | Изменения |
|---|-----|-----|-----|-------------|----------|-----------|
| 1 | 41 | 42 | 1173082506 | Hendi 825556 доска разделочная HACCP 450x300x12,7 мм коричневая | **TRIP** | c5←c7 (62 chars); c36 RU 1112 chars. SMALL_BOARD_TABLE (825xxx серия 7 цветов 450x300x12,7) + iframe `sQhMvuX1twE` preserve. **Source-quirk: UA `<li>` «Коричневій колір» (typo locative) → RU «Коричневый цвет» standard form**; UA «сира птах» typo (должно «птиця») → RU «сырая птица» (нормализуем); «варене м'ясо» literal `'` dropped → «вареное мясо». No Ё в c36. |
| 2 | 42 | 43 | 1930950687 | Hendi 880906 — title/body MISMATCH (c5/c7 «Контейнер для еды двойной GN 1/1», c35 UA describes 880906 14 л) | **blknochg** | c5 уже RU == c7; c36 уже pure RU 120 chars («Контейнер для еды двойной GN 1/1... Габариты: 530х325х65... 7,5 л»). UA только в c35. **Источниковый конфликт: c4/c35 описывают Hendi 880906 14 л 600x400x70, но c5/c7/c36 — GN 1/1 530x325x65 7,5 л (совершенно другой продукт)**. Forward-only; **Открытый вопрос #2**. См. также r38 b5 (1166434765 — другая Horoshop-строка для того же 880906). |
| 3 | 43 | 44 | 873570684 | Hendi 271186 термометр для морозильников и холодильников | **TRIP** | c5←c7 (56 chars); c36 RU 354 chars. Малый блок: `<p>` + `<ul>` × 6 `<li>`. «Дозвіл: 2,5°C» (UA «разрешающая способность/шаг») → RU «Разрешение: 2,5°C» preserve term. Габариты «60х70 мм» — Cyrillic «х» preserve. |
| 4 | 44 | 45 | 1165829624 | HENDI 588574 сифон содовый 1 л | **TRIP** | c5←c7 (45 chars); c36 RU 612 chars + iframe `ESB30T0xPiA`. «Сифон содовий ємністю» → «Сифон содовый емкостью» (без Ё). «Пляшка з нержавіючої сталі» → «Бутылка из нержавеющей стали». «струсіть» → «встряхните». CO₂ + ø100 preserve. Размер ø100x(H)320 мм. |
| 5 | 45 | 46 | 876951846 | Сетка для варки риса 95х95 см (без бренда / no-brand) | **blknochg** | c5 уже RU == c7 (29 chars); c36 уже pure RU 360 chars. UA только в c35. Forward-only. |
| 6 | 46 | 47 | 921204080 | Хангири 60 см Япония (без бренда — кадка для риса, японская) | **blknochg** | c5 уже RU == c7 (21 chars); c36 уже pure RU 590 chars. UA только в c35. **Source-quirk: «кадка будет прослужит» — будущее время + инфинитив (структурный) — preserve as is** (нет правки c36). |
| 7 | 47 | 48 | 1060747430 | Хангири 39 см (Япония) (кадка для риса 39 см загрузка 1,5 кг) | **blknochg** | c5 уже RU == c7 (22 chars); c36 уже pure RU 583 chars. UA только в c35. Trailing `<p> </p>` preserve. |
| 8 | 48 | 49 | 1060762720 | Хангири 720х176 мм (Япония) | **blknochg** | c5 уже RU == c7 (29 chars); c36 уже pure RU 575 chars. UA только в c35 (с typos «Када», «харгірі», «каска» — UA quirks остаются в c35). Forward-only. |

**Итого b6:** TRIP 3 + blknotrip 0 + blknochg 5 + blkfix 0 + SKIP-НП 0. Verify **72 PASS / 0 FAIL**.
**Cum после b6:** TRIP 36 + blknotrip 0 + blknochg 12 + blkfix 0 + SKIP-НП 0 = **48/89**. UNPROC = 41 (rows 50-90).
