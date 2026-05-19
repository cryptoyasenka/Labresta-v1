# chunk-063 — diff (W2)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-063 (88 SKU, rows 2..89; ART 2059513121 … 2567549749)
**Apply key:** `Артикул` (col1, scoped per row)
**Worker:** W2 (параллельный, диапазон chunk-055 … chunk-085); продолжение chunk-062
**Status:** b1 DONE 8/88 (b2..b11 remain; b1-b11 по 8 SKU)

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

<!-- Сводки по батчам b2..b11 ниже. -->
