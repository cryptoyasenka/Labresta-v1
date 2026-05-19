# chunk-065 — diff (W2)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-065 (81 SKU, rows 2..82; ART 2121426618 … 2447469404)
**Apply key:** `Артикул` (col1, scoped per row)
**Worker:** W2 (параллельный, диапазон chunk-055 … chunk-085); продолжение chunk-064
**Status:** b2 DONE 16/81 (b3 предстоит; b1-b10 по 8 SKU + b11=SKU81 1 SKU)

Категории: blk триплет / blknotrip / blknochg / SKIP-НП. Формат — как chunk-064-diff.md.

SKIP-НП prelim (HURAKAN, forward-only, тело из фида НП позже): SKU 64 (ART 1147781261), SKU 69 (ART 2059494027), SKU 70 (ART 2059501393). Точная классификация — по ходу батчей.

---

## b1 — diff (SKU 1-8, rows 2-9), 8/81

**Категории:** blk триплет 1 · blknotrip 0 · blknochg 7 · SKIP-НП 0 = 8.

### blk триплет (1)
- **SKU 1** (r2, ART 2121426618, Hendi 211427 Concept Line):
  - col5 (NMRU): `Кип'ятильник Concept Line Hendi 211427` (UA-leak) → `Кипятильник Concept Line Hendi 211427` (genuine RU из c7).
  - col36 (DSCRU): UA-leak копия c35 → faithful RU перевод (skel==c35, dims==c35: 230/502/1650/357/275/380/16/3.09, deg/degL: пустые, UA-clean, без ё, без `&#39;`/апострофов).

### blknotrip (0)
— нет.

### blknochg (7)
- **SKU 2-8** (r3-r9, GoodFood WB30A / WB08 RED / WB08 BLACK / WB30S / WB20S / WB06DW / WB08DW): c5==c7 genuine RU, c35!=c36 (c36 уже на русском, fixed.xlsx не трогаем).

### SKIP-НП (0)
— нет.

**Codepoint findings SKU1 c35:** DEG/XCH/Cyr-Lat ambiguity: нет; DASH 1× U+002D в «будь-якому» (UA only, в RU «любом» — без дефиса); С/В все Cyrillic; `&#39;` 1× в `об&#39;єм` (в RU `объем` без апострофа). Чисто.

**Verify:** 89 PASS / 0 FAIL (ART 81 + TRIP 1 + blknochg 7).

---

## b2 — diff (SKU 9-16, rows 10-17), 16/81

**Категории:** blk триплет 2 · blknotrip 0 · blknochg 6 · SKIP-НП 0 = 8.

### blk триплет (2)
- **SKU 14** (r15, ART 2193237181, AIRHOT WB-20):
  - col5: `Водонагрівач електричний AIRHOT WB-20` → `Водонагреватель электрический AIRHOT WB-20`.
  - col36: UA-leak копия c35 → faithful RU (skel==c35, dims==c35: 20/20/30../100,/20,/220,/2.5,/3.580,/5.250,/315x315x660,/330x330x680,, deg `&deg;С` Cyr U+0421 verbatim).
- **SKU 15** (r16, ART 2193245500, AIRHOT WB-30):
  - col5: `Водонагрівач електричний AIRHOT WB-30` → `Водонагреватель электрический AIRHOT WB-30`.
  - col36: UA-leak копия c35 → faithful RU (skel==c35, dims==c35: 30/30/30../100,/30,/220,/2.5,/4.570,/5.670,/440x440x490,/440x440x520,, deg `&deg;С` Cyr U+0421 verbatim).

### blknotrip (0)
— нет.

### blknochg (6)
- **SKU 9-13** (r10-r14, GoodFood WB10DW/WB14DW/WB16DW/WB25DW/WB30DW): c5==c7 genuine RU, c35!=c36 (c36 уже RU, `<h4>`).
- **SKU 16** (r17, Silver 2039): c5==c7 genuine RU, c35!=c36 (c36 уже RU).

### SKIP-НП (0)
— нет.

**Codepoint findings (TRIP SKU14/SKU15 c35):** DEG 1× `&deg;` tail С Cyr U+0421; XCH all Lat x U+0078; DASH только в WB-20/WB-30 U+002D; B Lat U+0042 в model; остальные С/В Cyrillic.

**Verify:** 97 PASS / 0 FAIL (REGR 8 + ART 81 + TRIP 2 + blknochg 6).

---

<!-- Сводка по батчу b3 ниже. -->
