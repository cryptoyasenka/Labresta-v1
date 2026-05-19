# chunk-063 — diff (W2)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-063 (88 SKU, rows 2..89; ART 2059513121 … 2567549749)
**Apply key:** `Артикул` (col1, scoped per row)
**Worker:** W2 (параллельный, диапазон chunk-055 … chunk-085); продолжение chunk-062
**Status:** b4 DONE 32/88 (b5..b11 remain; b1-b11 по 8 SKU)

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

<!-- Сводки по батчам b5..b11 ниже. -->
