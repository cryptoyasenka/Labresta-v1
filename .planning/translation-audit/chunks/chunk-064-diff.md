# chunk-064 — diff (W2)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-064 (85 SKU, rows 2..86; ART 2567629973 … 2060623567)
**Apply key:** `Артикул` (col1, scoped per row)
**Worker:** W2 (параллельный, диапазон chunk-055 … chunk-085); продолжение chunk-063
**Status:** b1 DONE 8/85 (b2..b11 предстоят; b1-b11 по 8 SKU)

Категории: blk триплет / blknotrip / blknochg / SKIP-НП. Формат — как chunk-063-diff.md.

SKIP-НП — по ходу батчей (forward-only, тело из фида НП позже). Точная классификация — по ходу батчей.

---

## b1 (SKU 1-8, rows 2-9)

Изменения только в `chunk-064-fixed.xlsx` (gitignored). Apply key `Артикул` (col1) НЕ менялся ни в одной строке.

**blk триплет (6): col5 ← col7 (genuine RU); col36 ← faithful RU (skeleton == UA col35)**

- **SKU 3 r4 ART 475091306 — HENDI 860502**
  - col5: `Супниця 8 л HENDI 860502` → `Электросупница 8 л HENDI 860502`
  - col36: UA-leak (==col35) → RU (`<p>×2 <ul> 12×<li>` (br/ во 2-м) `</ul> <p> </p>`; `65°С`/`95°С`/`1°С`/`0,45 кВт`/`370`/`300` verbatim)
- **SKU 4 r5 ART 682964239 — Hendi Kitchen Line 204832**
  - col5: `Марміт Kitchen Line Hendi 204832 електричний настільний круглий` → `Мармит Hendi Kitchen Line 204832 электрический настольный круглый`
  - col36: UA-leak → RU (`<p>\n<ul>\n` 8×`<li>` `\n</ul>`; `85°C`/`Ø360x65`/`Ø405х248`/`6,8`/`0,5 кВт` verbatim; Ø/лат.x/кир.х)
- **SKU 5 r6 ART 682970331 — Hendi Profi Line 204900**
  - col5: `Марміт Hendi Profi Line 204900 настільний електричний` → `Мармит Hendi Profi Line 204900 электрический настольный`
  - col36: UA-leak → RU (`<p>\n<ul>\n` 8×`<li>` `\n</ul>`; `85°C`/`615х355х280`; `Потужність-0,8`→`Мощность-0,8 кВт` без пробела verbatim)
- **SKU 6 r7 ART 682980201 — Hendi 424186**
  - col5: `Піднос охолоджуваний Hendi 424186 (GN 1/1)` → `Поднос охлаждаемый Hendi 424186 (GN 1/1)`
  - col36: UA-leak → RU (`<p>\n<ul>\n` 4×`<li>` `\n</ul>`; `555х357х175`/`1/1` verbatim; источ. опечатка «комлекті»→корректно «комплекте»)
- **SKU 7 r8 ART 897807414 — HENDI 470305 Profi Line**
  - col5: `Марміт HENDI 470305 Profi Line, кришка Rolltop, підігрів горючої пастою - GN 1/1, 9 л` → `Мармит HENDI 470305 Profi Line, крышка Rolltop, подогрев горючей пастой - GN 1/1, 9 л`
  - col36: UA-leak → RU (`<p>×4 (2×<br/> во 2-м) <ul> 3×<li> </ul>`; `9,0`/`180°`/`18/10`/`2,3`/`1,2`/`660x490x(H)460`/`ø345x(H)60` verbatim; ° / лат.x / ø)
- **SKU 8 r9 ART 897818040 — HENDI Profi Line 470312**
  - col5: `Марміт HENDI Profi Line 470312, кришка Rolltop - круглий 5,6 л` → `Мармит HENDI Profi Line 470312, крышка Rolltop - круглый 5,6 л`
  - col36: UA-leak → RU (`<p>×3 <ul> 3×<li> </ul> <p> </p>`; `5,6`/`180°`/`345х(H)60`/`18/10.`/`2,8`/`1,2`/`510x540x(H)480` verbatim; ° / кир.х / лат.x / ø)

**blknotrip (1): col36 ← faithful RU; имя col5==col7 lang-neutral — col5 НЕ тронут**

- **SKU 2 r3 ART 659126851 — Hendi 707999 термоконтейнер (8хGN1/1)**
  - col5 НЕ тронут (`Термоконтейнер кейтеринговый Hendi 707999 (8хGN1/1)`, c5==c7 lang-neutral)
  - col36: UA-leak (==col35) → RU (`<p> <ul> 10×<li> </ul>`; `100`/`61`/`1/1`/`+80°C`/`530х335х545`/`635х465х660` verbatim; кир.х)

**blknochg (1): RU уже корректен — fixed НЕ тронут**

- SKU 1 r2 ART 2567629973 SIRMAN BUFFET PLATE 1/1 — c5==c7 genuine RU, c36 properly translated (c35!=c36). _Лид-абзац c36 «Витрина нейтральная Bartscher 700355» — артефакт копипасты genuine RU (не наша правка), для merge-ревью._

**SKIP-НП (0):** нет (бренды SIRMAN/Hendi/HENDI не НП-эксклюзивные).

**Verify:** 96 PASS / 0 FAIL.

<!-- Сводки по батчам b2..b11 ниже. -->
