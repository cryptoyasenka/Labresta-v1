# chunk-063 — diff (W2)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-063 (88 SKU, rows 2..89; ART 2059513121 … 2567549749)
**Apply key:** `Артикул` (col1, scoped per row)
**Worker:** W2 (параллельный, диапазон chunk-055 … chunk-085); продолжение chunk-062
**Status:** b6 DONE 48/88 (b7..b11 remain; b1-b11 по 8 SKU)

Категории: blk триплет / blknotrip / blknochg / SKIP-НП. Формат — как chunk-062-diff.md.

SKIP-НП предварительно (HURAKAN, forward-only, тело из фида НП позже): SKU 1 (ART 2059513121), SKU 3 (ART 2176575775), SKU 54 (ART 1148895671). Точная классификация — по ходу батчей.

---

## b1 (SKU 1-8, rows 2-9)

Изменения только в `chunk-063-fixed.xlsx` (gitignored). Apply key `Артикул` (col1) НЕ менялся ни в одной строке.

**blk триплет (4): col5 ← col7 (genuine RU); col36 ← faithful RU (skeleton == UA col35)**

- **SKU 4 r5 ART 2191892433 — Sirman CUBE P2 HOT**
  - col5: `Вітрина теплова Sirman CUBE P2 HOT` → `Витрина тепловая Sirman CUBE P2 HOT`
  - col36: UA-leak (==col35) → RU `<p>Тепловая витрина SIRMAN CUBE P2 HOT…</p> <ul>…13×<li>…</ul>` (размеры `512x295`/`560X347X395`/`660Х500Х610`/`0.45` verbatim, AISI 304)
- **SKU 5 r6 ART 2301763319 — Frosty SWS-3P**
  - col5: `Вітрина теплова Frosty SWS-3P` → `Витрина тепловая Frosty SWS-3P`
  - col36: UA-leak → RU (3×`<p>` + `<ul>` 10×`<li>` + `<p>Материал:</p>` + `<ul>` 1×`<li>`; `880х280`/`950мм x 480мм x 600мм`/`1,2 кВт`/`28.00` verbatim)
- **SKU 6 r7 ART 2553918281 — Gooder XCR-50L Cube**
  - col5: `Теплова вітрина Gooder XCR-50L Cube` → `Тепловая витрина Gooder XCR-50L Cube`
  - col36: UA-leak → RU `<h2>…</h2> <ul>` 14×`<li>` `</ul> <p> </p>` (`520х260`/`555х361х368`/`706х478х496`/`0,8 кВт`/`220-240V/50Hz` verbatim)
- **SKU 7 r8 ART 2553925755 — Gooder XCR-45L**
  - col5: `Теплова вітрина Gooder XCR-45L` → `Тепловая витрина Gooder XCR-45L`
  - col36: UA-leak → RU `<h2>…</h2> <ul>` 14×`<li>` `</ul> <p> </p>` (`520х270`/`555х380х368`/`706х497х496` verbatim)

**blknochg (2): RU уже корректен — fixed НЕ тронут**

- SKU 2 r3 ART 2110267107 GoodFood WS3SS — c5==c7 genuine RU, c36 properly translated (c35!=c36).
- SKU 8 r9 ART 424917689 GGM Gastro WHVJ3 — c5==c7 genuine RU, c36 properly translated.

**SKIP-НП (2): HURAKAN forward-only — fixed НЕ тронут (тело из фида НП позже)**

- SKU 1 r2 ART 2059513121 Hurakan HKN WD-165L.
- SKU 3 r4 ART 2176575775 HURAKAN HKN WD-160L.

**Verify:** 136 PASS / 0 FAIL.

## b2 (SKU 9-16, rows 10-17)

Изменения только в `chunk-063-fixed.xlsx` (gitignored). Apply key `Артикул` (col1) НЕ менялся.

**blk триплет (1): col5 ← col7 (genuine RU); col36 ← faithful RU (skeleton == UA col35)**

- **SKU 10 r11 ART 1131731712 — Hendi 233962**
  - col5: `Теплова вітрина Hendi 233962` → `Тепловая витрина Hendi 233962`
  - col36: UA-leak (==col35) → RU `<h2>…</h2>\n<p>Технические характеристики: </p>\n<ul>\n` 10×`<li>` `\n</ul>\n<p> </p>` (литералы `°C`, `4хGN 1/2`, `650х467х630`, `0,56 кВт`, `220 В` verbatim)

**blknochg (7): c5==c7 genuine RU, c35!=c36 (RU уже переведён) — fixed НЕ тронут**

- SKU 9 r10 ART 424917690 GGM Gastro ATSM695 _(в genuine c36 опечатка источника «поддрежания» — не наша правка)_
- SKU 11 r12 ART 424917691 GGM ATSM615
- SKU 12 r13 ART 2538738615 SARO SHIRA
- SKU 13 r14 ART 2538743093 SARO YAEL
- SKU 14 r15 ART 2210058270 GoodFood WS85 ELIT
- SKU 15 r16 ART 2301733929 Frosty SWS-2P
- SKU 16 r17 ART 961887244 GoodFood WS920 Black Line

**SKIP-НП (0).**

**Verify:** 112 PASS / 0 FAIL.

## b3 (SKU 17-24, rows 18-25)

Изменения только в `chunk-063-fixed.xlsx` (gitignored). Apply key `Артикул` (col1) НЕ менялся.

**blk триплет (4): col5 ← col7 (genuine RU); col36 ← faithful RU (skeleton == UA col35)**

- **SKU 17 r18 ART 1043369426 — EWT INOX SDC5**
  - col5: `Вітрина теплова EWT INOX SDC5` → `Витрина тепловая EWT INOX SDC5`
  - col36: UA-leak (==col35) → RU `<p>…пять полок…</p>\n<ul>\n` 3×`<li>` `\n</ul>` (`220`/`1,1`/`400`/`380`/`750` verbatim)
- **SKU 20 r21 ART 475085014 — Bartscher 100061**
  - col5: `Електросупниця 9 л Bartscher 100061` → `Электросупница 9 л Bartscher 100061`
  - col36: UA-leak → RU (single-line `<p></p> <ul> 10×<li> </ul> <p> </p>`; `48 °C`/`94°С`/`9`/`8`/`330`/`360`/`0,4` verbatim)
- **SKU 21 r22 ART 475113512 — FROSTY SB-6000S (супник)**
  - col5: `Електросупниця 10 л FROSTY SB-6000S (супник)` → `Электросупница 10 л FROSTY SB-6000S (супник)`
  - col36: UA-leak → RU `<p></p> <p></p> <ul>\n` 8×`<li>` `\n</ul> <p> </p>` (`10`/`385`/`0,4` verbatim)
- **SKU 23 r24 ART 489952968 — AIRHOT BM-11**
  - col5: `Марміт AIRHOT BM-11` → `Мармит AIRHOT BM-11`
  - col36: UA-leak → RU (single-line `<p></p> <ul> 8×<li> </ul>`; `GN 1/3 — 3 шт., GN 1/2 - 2 шт.` пунктуация + `150`/`220`/`1.2`/`510х335х540`/`7` verbatim)

**blknochg (4): c5==c7 genuine RU, c35!=c36 (RU уже переведён) — fixed НЕ тронут**

- SKU 18 r19 ART 2210044738 GoodFood WS65 ELIT
- SKU 19 r20 ART 883765440 FROSTY DSK-10 (електросупниця)
- SKU 22 r23 ART 476419919 GoodFood SK10
- SKU 24 r25 ART 593853560 GoodFood BM3G вітрина _(в genuine c36 опечатка источника «укоплектоварн стекляной» — не наша правка)_

**SKIP-НП (0).**

**Verify:** 136 PASS / 0 FAIL.

## b4 (SKU 25-32, rows 26-33)

Изменения только в `chunk-063-fixed.xlsx` (gitignored). Apply key `Артикул` (col1) НЕ менялся.

**blk триплет (6): col5 ← col7 (genuine RU); col36 ← faithful RU (skeleton == UA col35)**

- **SKU 26 r27 ART 648142042 — HENDI 860083 KITCHEN LINE**
  - col5: `Супниця 8 л HENDI 860083 KITCHEN LINE` → `Электросупница 8 л HENDI 860083 KITCHEN LINE`
  - col36: UA-leak (==col35) → RU `<p>…</p> <p>…</p> <ul> 8×<li> </ul> <p> </p>` (`8`/`340`/`360`/`0,435` verbatim)
- **SKU 27 r28 ART 659138198 — Hendi 707975**
  - col5: `Термоконтейнер для піци Hendi 707975` → `Термоконтейнер для пиццы Hendi 707975`
  - col36: UA-leak → RU `<p> …</p> <ul> 6×<li> </ul>` (`-20°C`/`+110°C` литералы, `21`/`350х350х175`/`410х410х240` verbatim)
- **SKU 29 r30 ART 659310459 — Hendi 709825**
  - col5: `Термосумка для піци Hendi (350x350 мм) 709825` → `Термосумка для пиццы Hendi (350x350 мм) 709825`
  - col36: UA-leak → RU `<p>…</p> <ul> 6×<li> </ul>` (`4`/`350х350` verbatim)
- **SKU 30 r31 ART 659315703 — Hendi 709818**
  - col5: `Термосумка для піци Hendi (450x450 мм) 709818` → `Термосумка для пиццы Hendi (450x450 мм) 709818`
  - col36: UA-leak → RU `<p>…</p> <ul> 6×<li> </ul>` (`4`/`450х450` verbatim)
- **SKU 31 r32 ART 660854999 — EWT INOX SK6000 (9 л)**
  - col5: `Електросупниця EWT INOX SK6000 (9 л)` → `Электросупница EWT INOX SK6000 (9 л)`
  - col36: UA-leak → RU `<p>…</p> <ul> 8×<li> </ul> <p> </p>` (`+70 °C`/`+90 °C` литералы, `9`/`340х340х305`/`0,4` verbatim)
- **SKU 32 r33 ART 682956337 — Hendi 238912 (Kitchen Line, зливний кран)**
  - col5: `Марміт зі зливним краном Kitchen Line Hendi (GN 1/1) 238912` → `Мармит со сливным краном Hendi Kitchen Line (GN 1/1) 238912`
  - col36: UA-leak → RU multi-line `<p> …</p>\n<ul>\n` 7×`<li>` `\n</ul>` (`85ºC` литерал º verbatim, `GN 1/1`/`150`/`340х540х250`/`1,2` verbatim)

**blknotrip (1): name lang-neutral (col5==col7, НЕ тронут); col36 ← faithful RU (col35==col36 UA-leak)**

- **SKU 28 r29 ART 659207301 — Hendi 707906 (GN1/1)**
  - col5: `Термоконтейнер Hendi 707906 (GN1/1)` — lang-neutral, c5==c7, НЕ тронут
  - col36: UA-leak (==col35) → RU `<p>…</p> <ul> 6×<li> </ul>` (`-20°C`/`+110°C` литералы, `40`/`538х338х234`/`600х410х320` verbatim)

**blknochg (1): c5==c7 genuine RU, c35!=c36 (RU уже переведён) — fixed НЕ тронут**

- SKU 25 r26 ART 593856839 GoodFood BM3 — c5==c7 «Мармит электрический GoodFood BM3», c36 properly translated (`&deg;С` в genuine RU — пред-существующий источник, не наша правка).

**SKIP-НП (0).**

**Verify:** 172 PASS / 0 FAIL.

## b5 (SKU 33-40, rows 34-41)

Изменения только в `chunk-063-fixed.xlsx` (gitignored). Apply key `Артикул` (col1) НЕ менялся.

**blk триплет (8): col5 ← col7 (genuine RU); col36 ← faithful RU (skeleton == UA col35)**

- **SKU 33 r34 ART 682961496 — Hendi 204825 Kitchen Line Tellano**
  - col5: `Марміт Hendi 204825 Kitchen Line Tellano (GN 1/1) настільний електричний` → `Мармит Hendi 204825 Kitchen Line Tellano (GN 1/1) электрический настольный`
  - col36: UA-leak (==col35) → RU multi-line `<p> …</p>\n<ul>\n` 9×`<li>` `\n</ul>` (`85°C` литерал, `573х348х284`/`0,9`/`GN 1/1`/`65` verbatim)
- **SKU 34 r35 ART 682983156 — Hendi 424155**
  - col5: `Піднос охолоджуваний з кришкою Hendi 424155` → `Поднос охлаждаемый с крышкой Hendi 424155`
  - col36: UA-leak → RU `<p>…</p>\n<ul>\n` 4×`<li>` `\n</ul>` (`430х290х150`/`2` verbatim; UA-typo «комлекті»→корректный RU «комплекте»)
- **SKU 35 r36 ART 682984915 — Hendi 871805**
  - col5: `Охолоджувана вітрина Hendi 871805` → `Витрина охлаждаемая Hendi 871805`
  - col36: UA-leak → RU `<p>…</p>\n<ul>\n` 5×`<li>` `\n</ul>` (`440х320х205`/`2` verbatim)
- **SKU 36 r37 ART 682986676 — Hendi 871812**
  - col5: `Охолоджувана вітрина подвійна Hendi 871812` → `Витрина охлаждаемая двойная Hendi 871812`
  - col36: UA-leak → RU `<p>…</p>\n<ul>\n` 5×`<li>` `\n</ul>` (`440х320х440`/`2`/`4` verbatim)
- **SKU 37 r38 ART 885050265 — Bartscher 100067 CLUB 8.5л**
  - col5: `Електросупниця Bartscher 100067 CLUB 8.5 л` → `Электросупница Bartscher 100067 CLUB 8.5л` (verbatim c7, без пробела перед л)
  - col36: UA-leak → RU `<p>…</p> <ul>\n` 12×`<li>` `\n</ul>` (`+30/+95 °C` литерал, `270x270x370` лат. x, `8,5`/`4.55`/`220`/`0,4` verbatim, em-dash —)
- **SKU 38 r39 ART 898117915 — HENDI 475904 Economic (чафингдиш)**
  - col5: `Марміт HENDI 475904 модель Economic GN 1/1 (чафингдиш)` → `Мармит HENDI 475904 модель Economic GN 1/1 (чафингдиш)`
  - col36: UA-leak → RU `<p>…</p>\n<p>…</p>\n<ul>\n` 3×`<li>` `\n</ul>` (`620x350x(H)310` лат. x, `9,0`/`65`/`GN 1/1` verbatim)
- **SKU 39 r40 ART 900354847 — HENDI 809600 нагревательный элемент**
  - col5: `Нагрівальний елемент HENDI 809600 для мармітів - 500 W, круглий Ø130 мм` → `Нагревательный элемент HENDI 809600 для мармитов - 500 W, круглый Ø130 мм`
  - col36: UA-leak → RU `<p>…</p>\n<p>…</p>\n<ul>\n` 3×`<li>` `\n</ul>` (`ø130x(H): 100` литерал ø, парт-номера 809600/470008/475201/470206/471005 verbatim)
- **SKU 40 r41 ART 900454506 — HENDI 470527 бачок (2 шт)**
  - col5: `Бачок для горючої пасти HENDI 470527 - 2 шт` → `Бачок для горючей пасты HENDI 470527 - 2 шт`
  - col36: UA-leak → RU `<p>…</p>\n<ul>\n` 2×`<li>` `\n</ul>` (`Ø90x(H)60` литерал Ø, `470527`/`2` verbatim)

**blknotrip (0). blknochg (0). SKIP-НП (0).**

**Verify:** 184 PASS / 0 FAIL.

## b6 (SKU 41-48, rows 42-49)

Изменения только в `chunk-063-fixed.xlsx` (gitignored). Apply key `Артикул` (col1) НЕ менялся.

**blk триплет (6): col5 ← col7 (genuine RU); col36 ← faithful RU (skeleton == UA col35)**

- **SKU 41 r42 ART 900469355 — HENDI 194546 паста для подогрева мармитов**
  - col5: `Паста HENDI 194546 для підігріву мармітів - 200 г, етанол` → `Горючая паста 48 шт HENDI 194546 для подогева мармитов - 200 г, этанол` (genuine c7 verbatim; опечатка источника «подогева» сохранена)
  - col36: UA-leak (==col35) → RU `<p>…<br/>\n…</p>\n<ul>\n` 1×`<li>` `\n</ul>` (`200`/`3`/`48` verbatim)
- **SKU 42 r43 ART 900509655 — HENDI 195109 бутылка 1 л**
  - col5: `Горюча паста 12 шт HENDI 195109 пляшка 1 л, етанол` → `Горючая паста 12 шт HENDI 195109 бутылка 1 л, этанол`
  - col36: UA-leak → RU `<p>…</p>\n<ul>\n` 2×`<li>` `\n</ul>` (part-номер HENDI 470527, `1`/`12` verbatim)
- **SKU 43 r44 ART 900604525 — HENDI 195505 канистра 5 л**
  - col5: `Горюча паста HENDI 195505 каністра 5 л, етанол` → `Горючая паста HENDI 195505 канистра 5 л, этанол`
  - col36: UA-leak → RU `<p>…</p> <ul>\n` 1×`<li>` `\n</ul>` (`</p> <ul>` одной строкой; UA `&#39;` в c35 «об&#39;ємом» → RU «объемом» без апострофа; `5`/`470527` verbatim)
- **SKU 46 r47 ART 1069314215 — Hendi 710104 термос 10 л**
  - col5: `Термос Hendi 710104 для транспортування їжі 10 л з нержавіючої сталі` → `Термос Hendi 710104 для транспортировки пищи 10 л из нержавеющей стали`
  - col36: UA-leak → RU `<p>…</p>\n<ul>\n` 8×`<li>` `\n</ul>` (`ø330x(H)200` литерал ø + лат. x, финальный `<li> </li>` пробел-only verbatim)
- **SKU 47 r48 ART 1069323202 — Hendi 710111 термос 15 л**
  - col5: `Термос Hendi 710111 для транспортування їжі 15 л з нержавіючої сталі` → `Термос Hendi 710111 для транспортировки пищи 15 л из нержавеющей стали`
  - col36: UA-leak → RU `<p>…</p>\n<ul>\n` 8×`<li>` `\n</ul>` (`ø330x(H)280` verbatim)
- **SKU 48 r49 ART 1069332170 — Hendi 710203 термос 20 л**
  - col5: `Термос Hendi 710203 для транспортування їжі 20 л з нержавіючої сталі` → `Термос Hendi 710203 для транспортировки пищи 20 л из нержавеющей стали`
  - col36: UA-leak → RU `<p>…</p>\n<ul>\n` 8×`<li>` `\n</ul>` (`ø330x(H)310` verbatim)

**blknotrip (0). blknochg (2): c5==c7 genuine RU, c36 уже переведён (c35!=c36), fixed НЕ тронут.**

- **SKU 44 r45 ART 1009198166 — GoodFood BM4G витрина** — genuine RU c5/c7 «Мармит электрический GoodFood BM4G витрина (GN 1/2 х h100 мм)»; c36 переведён. Замечание: genuine c36 содержит `&deg;С` и дефис вместо тире (пред-существующий источник, не правим).
- **SKU 45 r46 ART 1009203341 — GoodFood BM5G витрина** — genuine RU c5/c7 «Мармит электрический GoodFood BM5G витрина (GN 1/2 х h100 мм)»; c36 переведён. Замечание: тело c35 (UA) и c36 (RU) говорит «GoodFood BM4G» при товаре BM5G — пред-существующая нестыковка источника в обеих версиях (blknochg, не правим).

**SKIP-НП (0).**

**Verify:** 164 PASS / 0 FAIL.

<!-- Сводки по батчам b7..b11 ниже. -->
