# chunk-065 — manual review (W2)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-065 (81 SKU)
**Apply key:** `Артикул` (col1, scoped per row)
**Status:** b3 DONE 24/81 (b4 предстоит; batch=8, b11=SKU81 1 SKU)
**Worker:** W2 (параллельный, диапазон chunk-055 … chunk-085); продолжение chunk-064
**Last updated:** chunk-065 b3 (W2)

Эталон формата: chunk-019-MANUAL-REVIEW.md / chunk-064-MANUAL-REVIEW.md. Категории: blk триплет / blknotrip / blknochg / SKIP-НП. Кумул. OQ закрыты.

## SKIP-НП (НП-эксклюзивные бренды, forward-only, тело из фида НП позже)

| # | SKU | Артикул | Бренд | Название (UA) | Примечание |
|---|---|---|---|---|---|
| prelim | 64 | 1147781261 | HURAKAN | Вафельниця HURAKAN HKN-GES2M для бельгійських вафель | HURAKAN — НП-эксклюзив, тело из фида НП позже |
| prelim | 69 | 2059494027 | Hurakan | Вафельниця Hurakan HKN-GES2L | HURAKAN — НП-эксклюзив, тело из фида НП позже |
| prelim | 70 | 2059501393 | Hurakan | Вафельниця гонконгська Hurakan HKN-GES5HK | HURAKAN — НП-эксклюзив, тело из фида НП позже |

## Открытые вопросы chunk-065

_(нумерация отдельная, начинается с #1; пока нет)_

---

## b1 — SKU 1-8 (rows 2-9), 8/81

**Категории:** blk триплет 1 · blknotrip 0 · blknochg 7 · SKIP-НП 0 = 8.

| # | SKU | Артикул | Бренд / модель | Категория | Действие |
|---|---|---|---|---|---|
| 1 | 1 | 2121426618 | Hendi 211427 Concept Line | blk триплет | col5 ← c7 (genuine RU «Кипятильник Concept Line Hendi 211427»); col36 — faithful RU перевод описания (skel==c35, dims==c35: 230/502/1650/357/275/380/16/3.09, deg/degL пустые, UA-clean, без ё) |
| 2 | 2 | 2172891828 | GoodFood WB30A | blknochg | c5==c7 genuine RU, c35!=c36 (c36 уже RU) — fixed НЕ тронут |
| 3 | 3 | 2188566582 | GoodFood WB08 RED | blknochg | c5==c7 genuine RU, c35!=c36 (c36 уже RU, открывается `<h4>`) — fixed НЕ тронут |
| 4 | 4 | 2190227669 | GoodFood WB08 BLACK | blknochg | c5==c7 genuine RU, c35!=c36 (c36 уже RU, открывается `<h4>`) — fixed НЕ тронут |
| 5 | 5 | 2190229516 | GoodFood WB30S | blknochg | c5==c7 genuine RU, c35!=c36 (c36 уже RU, открывается `<h4>`) — fixed НЕ тронут |
| 6 | 6 | 2190231269 | GoodFood WB20S | blknochg | c5==c7 genuine RU, c35!=c36 (c36 уже RU, открывается `<h4>`) — fixed НЕ тронут |
| 7 | 7 | 2190243226 | GoodFood WB06DW | blknochg | c5==c7 genuine RU, c35!=c36 (c36 уже RU, открывается `<h4>`) — fixed НЕ тронут |
| 8 | 8 | 2190246661 | GoodFood WB08DW | blknochg | c5==c7 genuine RU, c35!=c36 (c36 уже RU, открывается `<h4>`) — fixed НЕ тронут |

**Verify:** 89 PASS / 0 FAIL (ART 81 rows + TRIP 1 + blknochg 7).

**Глоссарий b1:** +12 net-new (Hendi 211427 Concept Line RU перевод) + ~6 reuse; см. `chunk-glossary-w2.md` (757 → 769).

**Soft-notes (pre-existing в c36 датасете, не наша правка):** GoodFood blknochg SKU2-8 — c36 уже переведено: SKU2 открывается `<p>` (без `<h4>`); SKU3-8 открываются `<h4>` (вместо `<p>` как в c35); используется «общепита» (UA «громадського харчування»); в c35 встречается `&#39;` HTML-entity-апостроф. Эти отличия pre-existing в c36, fixed.xlsx не трогаем.

**Открытых вопросов b1:** нет.

---

## b2 — SKU 9-16 (rows 10-17), 16/81

**Категории:** blk триплет 2 · blknotrip 0 · blknochg 6 · SKIP-НП 0 = 8.

| # | SKU | Артикул | Бренд / модель | Категория | Действие |
|---|---|---|---|---|---|
| 1 | 9 | 2190251426 | GoodFood WB10DW | blknochg | c5==c7 genuine RU, c35!=c36 (c36 уже RU, `<h4>`) — fixed НЕ тронут |
| 2 | 10 | 2190252953 | GoodFood WB14DW | blknochg | c5==c7 genuine RU, c35!=c36 (c36 уже RU, `<h4>`) — fixed НЕ тронут |
| 3 | 11 | 2190254605 | GoodFood WB16DW | blknochg | c5==c7 genuine RU, c35!=c36 (c36 уже RU, `<h4>`) — fixed НЕ тронут |
| 4 | 12 | 2190257391 | GoodFood WB25DW | blknochg | c5==c7 genuine RU, c35!=c36 (c36 уже RU, `<h4>`) — fixed НЕ тронут |
| 5 | 13 | 2190258780 | GoodFood WB30DW | blknochg | c5==c7 genuine RU, c35!=c36 (c36 уже RU, `<h4>`) — fixed НЕ тронут |
| 6 | 14 | 2193237181 | AIRHOT WB-20 водонагреватель электр. | blk триплет | col5 ← c7 (`Водонагреватель электрический AIRHOT WB-20`); col36 — faithful RU (skel==c35, dims==c35: 20/20/30../100,/20,/220,/2.5,/3.580,/5.250,/315x315x660,/330x330x680,, deg `&deg;С` Cyr U+0421, без ё) |
| 7 | 15 | 2193245500 | AIRHOT WB-30 водонагреватель электр. | blk триплет | col5 ← c7 (`Водонагреватель электрический AIRHOT WB-30`); col36 — faithful RU (skel==c35, dims==c35: 30/30/30../100,/30,/220,/2.5,/4.570,/5.670,/440x440x490,/440x440x520,, deg `&deg;С` Cyr U+0421, без ё) |
| 8 | 16 | 2237486527 | Silver 2039 электрокипятильник | blknochg | c5==c7 genuine RU, c35!=c36 (c36 уже RU) — fixed НЕ тронут |

**Verify:** 97 PASS / 0 FAIL (REGR 8 + ART 81 + TRIP 2 + blknochg 6).

**Глоссарий b2:** ~10 net-new (AIRHOT WB-20/30 водонагреватель характеристики) + ~10 reuse; см. `chunk-glossary-w2.md` (769 → 779).

**Codepoint findings (TRIP SKU14/SKU15 c35):** DEG 1× `&deg;` tail С (Cyr U+0421) verbatim; XCH all Lat x U+0078 в `315x315x660` / `330x330x680` / `440x440x490` / `440x440x520` verbatim; DASH только в `WB-20`/`WB-30` (U+002D), без `&mdash;`/en-dash; Cyr-Lat: B Lat U+0042 в WB-20/WB-30, остальные С/В Cyrillic.

**Soft-notes (pre-existing в c36 датасете, не наша правка):** GoodFood blknochg SKU9-13 — c36 уже переведено, открывается `<h4>` (вместо `<p>` как в c35), используется «общепита» / `&#39;` в c35 verbatim. Silver 2039 SKU16 — c36 уже RU, fixed.xlsx не трогаем.

**Открытых вопросов b2:** нет.

---

## b3 — SKU 17-24 (rows 18-25), 24/81

**Категории:** blk триплет 2 · blknotrip 0 · blknochg 6 · SKIP-НП 0 = 8.

| # | SKU | Артикул | Бренд / модель | Категория | Действие |
|---|---|---|---|---|---|
| 1 | 17 | 2237495630 | Silver 2040 электрокипятильник 12л | blknochg | c5==c7 genuine RU, c35!=c36 — fixed НЕ тронут |
| 2 | 18 | 2237497792 | Silver 2041 электрокипятильник 16л | blknochg | c5==c7 genuine RU, c35!=c36 — fixed НЕ тронут |
| 3 | 19 | 2237499169 | Silver 2042 электрокипятильник 23л | blknochg | c5==c7 genuine RU, c35!=c36 — fixed НЕ тронут |
| 4 | 20 | 2331864089 | SARO ISOD 12 термос | blknochg | c5==c7 genuine RU, c35!=c36 — fixed НЕ тронут |
| 5 | 21 | 2331875380 | SARO 317-2076 термос мет.колба | blknochg | c5==c7 genuine RU, c35!=c36 — fixed НЕ тронут |
| 6 | 22 | 2437750626 | Frosty FWBD-20C кипятильник | blk триплет | col5 ← c7 (`Кипятильник Frosty FWBD-20C`); col36 — faithful RU (skel==c35, dims==c35: 20/20/8,5/30/100/1/2/2,00/220/220/220/500/4.20, deg `&deg;C` ×2 Lat U+0043 verbatim; SOURCE TYPO `Cенсорная` Lat C U+0043 verbatim) |
| 7 | 23 | 2526669301 | GoodFood WB14S кипятильник | blknochg | c5==c7 genuine RU, c35!=c36 (c36 RU с `<br />`) — fixed НЕ тронут |
| 8 | 24 | 500052773 | HENDI 208205 чаераздатчик-кофезаварник 15л | blk триплет | col5 ← c7 (`Чаераздатчик-кофезаварник 15л. HENDI 208205`); col36 — faithful RU (skel==c35 без `<p>` в начале, dims==c35: 15/85/1,5/90/280x580, degL `°С` ×2 Cyr U+0421 literal U+00B0 verbatim; XCH Lat x в D280x580h) |

**Verify:** 105 PASS / 0 FAIL (REGR 16 + ART 81 + TRIP 2 + blknochg 6).

**Глоссарий b3:** ~12 net-new + ~12 reuse; см. `chunk-glossary-w2.md` (779 → 791).

**Codepoint findings (TRIP):** SKU22 — 2× `&deg;C` Lat U+0043 verbatim, SOURCE TYPO `Cенсорна` (Lat C + Cyr енсорна) сохранена в RU как `Cенсорная`, DASH U+002D в model/inline; SKU24 — 2× literal U+00B0 + Cyr С U+0421 (НЕ &deg;), XCH Lat x в `D280x580h`, без `<p>` в начале.

**Soft-notes (pre-existing в c36, не наша правка):** Silver 2040/2041/2042 + SARO ISOD 12 + SARO 317-2076 + GoodFood WB14S — c36 уже RU. WB14S имеет `<br />` и backtick-apostrophe ``кип`ятильник`` в UA-частях c35.

**Открытых вопросов b3:** нет.

---

<!-- Сводка по батчу b4 ниже. -->
