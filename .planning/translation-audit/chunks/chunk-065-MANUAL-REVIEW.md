# chunk-065 — manual review (W2)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-065 (81 SKU)
**Apply key:** `Артикул` (col1, scoped per row)
**Status:** b9 DONE 72/81 (b10 предстоит; batch=8, b11=SKU81 1 SKU)
**Worker:** W2 (параллельный, диапазон chunk-055 … chunk-085); продолжение chunk-064
**Last updated:** chunk-065 b9 (W2)

Эталон формата: chunk-019-MANUAL-REVIEW.md / chunk-064-MANUAL-REVIEW.md. Категории: blk триплет / blknotrip / blknochg / SKIP-НП. Кумул. OQ закрыты.

## SKIP-НП (НП-эксклюзивные бренды, forward-only, тело из фида НП позже)

| # | SKU | Артикул | Бренд | Название (UA) | Примечание |
|---|---|---|---|---|---|
| 1 | 64 | 1147781261 | HURAKAN | Вафельниця HURAKAN HKN-GES2M для бельгійських вафель | HURAKAN — НП-эксклюзив, fixed row65 НЕ тронут (тело из фида НП позже); b8 confirmed |
| 2 | 69 | 2059494027 | Hurakan | Вафельниця Hurakan HKN-GES2L | HURAKAN — НП-эксклюзив, fixed row70 НЕ тронут (тело из фида НП позже); b9 confirmed |
| 3 | 70 | 2059501393 | Hurakan | Вафельниця гонконгська Hurakan HKN-GES5HK | HURAKAN — НП-эксклюзив, fixed row71 НЕ тронут (тело из фида НП позже); b9 confirmed |

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

<!-- b4 marker -->

## b4 — SKU 25-32 (rows 26-33), 32/81

**Категории:** blk триплет 5 · blknotrip 0 · blknochg 3 · SKIP-НП 0 = 8.

| # | SKU | Артикул | Бренд / модель | Категория | Действие |
|---|---|---|---|---|---|
| 1 | 25 | 500052774 | HENDI 209882 кипятильник 10л | blk триплет | col5 ← c7 (`Кипятильник HENDI 209882, 10л`); col36 — faithful RU (skel==c35, dims==c35: 10/2,2/50/99/336х221х474, degL `°С` Cyr U+0421 literal U+00B0; XCH Cyr х ×2 в `336х221х474`; DASH `–` U+2013 в `заваривания – 50 мин`) |
| 2 | 26 | 500052775 | HENDI 209899 кипятильник 20л (глинтвейн) | blk триплет | col5 ← c7 (`Кипятильник HENDI 209899, 20л (подходит для глинтвейна)`); col36 — faithful RU (skel==c35, dims==c35: 20/2,2/50/99/384x268x602, degL `°С` Cyr U+0421; XCH Lat x ×2; DASH `–` U+2013) |
| 3 | 27 | 500052776 | HENDI 209905 кипятильник 30л (глинтвейн) | blk триплет | col5 ← c7 (`Кипятильник HENDI 209905, 30л (подходит для глинтвейна)`); col36 — faithful RU (skel==c35, dims==c35: 30/2,2/50/99/520x/500, degL `°С` Cyr U+0421; XCH Lat x в `Ø 520x(H)500`; DASH `–` U+2013; «Некапающий» в c35 уже RU — verbatim) |
| 4 | 28 | 500052779 | HENDI 211304 кипятильник-кофеварочная машина 15л подвійна стінка | blk триплет | col5 ← c7 (`Кипятильник – кофеварочная машина HENDI 211304, 15л , двойная стенка` с em-dash U+2013); col36 — faithful RU (skel==c35, dims==c35: 15/85/1,5/90/288x602, degL `°С` ×2 Cyr U+0421; XCH Lat x в `D288x602h`; DASH `-` U+002D в `Кипятильник - кофеварочная машина` ВЕРНО сохранён) |
| 5 | 29 | 1068056403 | HENDI 211366 кипятильник-кофеварочная машина 16л двойные стенки | blknochg | c5==c7 genuine RU, c35!=c36 — fixed НЕ тронут |
| 6 | 30 | 1091390651 | Hendi 240700 диспенсер для глинтвейна 28л | blk триплет | col5 ← c7 (`Диспенсер для глинтвейна Hendi 240700, 28 л, нерж.`); col36 — faithful RU (skel==c35 c `\n` + `<h2>`/`<ul>`/`<li>`, dims==c35: 240700/28/110/75/28/447x441x485/2,5, degL `°C` Lat U+0043 verbatim; XCH Lat x ×2 в `447x441x485`; DASH нет) |
| 7 | 31 | 422807338 | GGM WKH015 кипятильник-чаераздатчик 15л | blknochg | c5==c7 genuine RU, c35!=c36 — fixed НЕ тронут |
| 8 | 32 | 422807339 | GGM WKH20 кипятильник 18л | blknochg | c5==c7 genuine RU, c35!=c36 — fixed НЕ тронут |

**Verify:** 113 PASS / 0 FAIL (REGR 24 + ART 81 + TRIP 5 + blknochg 3).

**Глоссарий b4:** ~14 net-new + ~14 reuse; см. `chunk-glossary-w2.md` (791 → 805).

**Codepoint findings (TRIP):** SKU25 — 1× literal `°` U+00B0 + Cyr С U+0421, XCH Cyr х U+0445 ×2, DASH `–` U+2013; SKU26 — 1× `°С`, XCH Lat x U+0078 ×2, DASH `–` U+2013; SKU27 — 1× `°С`, dim `Ø 520x(H)500` (regex даёт `520x` + `500`), DASH `–` U+2013; SKU28 — 2× `°С`, XCH Lat x в `D288x602h`, DASH `-` U+002D в смешанной фразе `Кип'ятильник - кофеварочная машина` (UA глагол + RU существительное в одной строке c35) сохранён; SKU30 — 1× `°C` Lat U+0043 (НЕ Cyr!), XCH Lat x ×2 в `447x441x485`, skel содержит `\n`.

**Soft-notes (pre-existing в c36, не наша правка):** SKU29 (HENDI 211366) / SKU31 (GGM WKH015) / SKU32 (GGM WKH20) — c36 уже RU, fixed.xlsx не трогаем. SKU28 c5/c4 содержит `15л ,` (пробел перед запятой) — сохранён в col5←c7 verbatim.

**Открытых вопросов b4:** нет.

---

<!-- b5 marker -->

## b5 — SKU 33-40 (rows 34-41), 40/81

**Категории:** blk триплет 1 · blknotrip 0 · blknochg 7 · SKIP-НП 0 = 8.

| # | SKU | Артикул | Бренд / модель | Категория | Действие |
|---|---|---|---|---|---|
| 1 | 33 | 625811874 | Hendi 240601 диспенсер для глинтвейна 27л | blk триплет | col5 ← c7 (`Диспенсер для глинтвейна Hendi 240601, 27 л`); col36 — faithful RU (skel==c35, dims==c35: 27/90/27/460x480x349/1,8/220, degL `°C` Lat U+0043 verbatim; XCH Lat x ×2 в `460x480x349`; DASH нет) |
| 2 | 34 | 2074393472 | Эфес КНЭ-25 кипятильник | blknochg | c5==c7 genuine RU, c35!=c36 — fixed НЕ тронут |
| 3 | 35 | 2074405173 | Эфес КНЭ-50 кипятильник | blknochg | c5==c7 genuine RU, c35!=c36 — fixed НЕ тронут |
| 4 | 36 | 2074414065 | Эфес КНЭ-100 кипятильник | blknochg | c5==c7 genuine RU, c35!=c36 — fixed НЕ тронут |
| 5 | 37 | 2110644149 | GoodFood WB20HOT кипятильник | blknochg | c5==c7 genuine RU, c35!=c36 — fixed НЕ тронут |
| 6 | 38 | 593820052 | FROSTY WB-15 вафельница корн-дог | blknochg | c5==c7 genuine RU, c35!=c36 — fixed НЕ тронут |
| 7 | 39 | 683160375 | FROSTY WS-15-2 вафельница бельгийские | blknochg | c5==c7 genuine RU, c35!=c36 — fixed НЕ тронут |
| 8 | 40 | 683160376 | FROSTY XG-01 вафельница круглые | blknochg | c5==c7 genuine RU, c35!=c36 — fixed НЕ тронут |

**Verify:** 121 PASS / 0 FAIL (REGR 32 + ART 81 + TRIP 1 + blknochg 7).

**Глоссарий b5:** ~6 net-new + ~10 reuse; см. `chunk-glossary-w2.md` (805 → 811).

**Codepoint findings (TRIP):** SKU33 — 1× literal `°` U+00B0 + Lat C U+0043 verbatim, XCH Lat x ×2 в `460x480x349`, DASH нет; skel содержит `<p>...</p> <ul> <li>...</li></ul>` (без `\n`).

**Soft-notes (pre-existing в c36, не наша правка):** SKU34-36 (Эфес КНЭ-25/50/100) c36 уже RU + ё (Эфес/электр.) verbatim; SKU37 (GoodFood WB20HOT) c36 открывается `<h4>` вместо `<p>`; SKU38-40 (FROSTY вафельницы) c36 уже RU.

**Открытых вопросов b5:** нет.

---

<!-- b6 marker -->

## b6 — SKU 41-48 (rows 42-49), 48/81

**Категории:** blk триплет 1 · blknotrip 0 · blknochg 7 · SKIP-НП 0 = 8.

| # | SKU | Артикул | Бренд / модель | Категория | Действие |
|---|---|---|---|---|---|
| 1 | 41 | 683160377 | Frosty XG-02 вафельница круглые | blknochg | c5==c7 genuine RU, c35!=c36 — fixed НЕ тронут |
| 2 | 42 | 1135994684 | SILVER 2147 вафельница бельгийская | blknochg | c5==c7 genuine RU, c35!=c36 — fixed НЕ тронут |
| 3 | 43 | 2041812422 | Frosty LD-117 вафельница 1-постовая | blknochg | c5==c7 genuine RU, c35!=c36 — fixed НЕ тронут |
| 4 | 44 | 2041848746 | Frosty LD-2202 вафельница 4-вафли | blknochg | c5==c7 genuine RU, c35!=c36 — fixed НЕ тронут |
| 5 | 45 | 2041869092 | Frosty LD-4 вафельница 2-вафли | blknochg | c5==c7 genuine RU, c35!=c36 — fixed НЕ тронут |
| 6 | 46 | 2041882194 | Frosty WS-15-2 d вафельница 4-вафли | blknochg | c5==c7 genuine RU, c35!=c36 — fixed НЕ тронут |
| 7 | 47 | 2213041449 | GoodFood WB4S вафельница бельгийская | blknochg | c5==c7 genuine RU, c35!=c36 — fixed НЕ тронут |
| 8 | 48 | 2301290442 | Frosty WBS-1C вафельница (тело WBS-22B copy-paste) | blk триплет | col5 ← c7 (`Вафельница Frosty WBS-1C`); col36 — faithful RU (skel==c35 c `\n`, dims==c35: 22/1/210/7х7/0/300/0/5/1,20/220/250/340/265/6.00, deg `&deg;C` ×2 Lat U+0043 verbatim; XCH Cyr х в `7х7`; DASH `-` U+002D в `WBS-22B` и `1-постовая`; `&Oslash;` entity verbatim; SOURCE COPY-PASTE: тело c35/c36 говорит `Frosty WBS-22B` при товаре WBS-1C — faithful preserve, не правим) |

**Verify:** 129 PASS / 0 FAIL (REGR 40 + ART 81 + TRIP 1 + blknochg 7).

**Глоссарий b6:** ~5 net-new + ~12 reuse; см. `chunk-glossary-w2.md` (811 → 816).

**Codepoint findings (TRIP):** SKU48 — 2× `&deg;C` Lat U+0043 entity-form, XCH Cyr х U+0445 в `7х7`, DASH `-` U+002D ×2 (модель `WBS-22B` + `1-постовая`), `&Oslash;` entity verbatim, skel содержит `\n` ×12.

**Soft-notes (pre-existing в c36, не наша правка):** SKU41 (Frosty XG-02), SKU42 (SILVER 2147), SKU43-46 (Frosty LD-117/LD-2202/LD-4/WS-15-2 d), SKU47 (GoodFood WB4S) — c36 уже RU. SKU48 body source-copy-paste WBS-22B при WBS-1C сохранён verbatim (faithful, не OQ).

**Открытых вопросов b6:** нет.

---

<!-- Сводка по батчу b7 ниже. -->
<!-- b7 marker -->

## b7 — SKU 49-56 (rows 50-57), 56/81

**Категории:** blk триплет 3 · blknotrip 0 · blknochg 5 · SKIP-НП 0 = 8.

| # | SKU | Артикул | Бренд / модель | Категория | Действие |
|---|---|---|---|---|---|
| 1 | 49 | 2301293860 | Frosty WBS-2C вафельница 1-постовая круглые | blk триплет | col5 ← c7 (`Вафельница Frosty WBS-2C`); col36 — faithful RU (skel==c35 c `\n`, dims==c35: 1/210/7х7/0/300/0/5/2,4/220/500/340/265/11.50, deg `&deg;C` ×2 Lat U+0043 entity verbatim; XCH Cyr х в `7х7`; DASH `-` U+002D в `1-постова`; `&Oslash;` entity verbatim; шаблон-сиблинг WBS-1C SKU48 b6) |
| 2 | 50 | 476343879 | GoodFood WB-1HK Bubble гонконгская | blknochg | c5==c7 genuine RU, c35!=c36 — fixed НЕ тронут |
| 3 | 51 | 476356084 | GoodFood WB1P Lolly Waffle (ёлочка) | blknochg | c5==c7 genuine RU (ё verbatim), c35!=c36 — fixed НЕ тронут |
| 4 | 52 | 476383537 | GoodFood DM6 аппарат для донатсов | blknochg | c5==c7 genuine RU, c35!=c36 — fixed НЕ тронут |
| 5 | 53 | 545492965 | AIRHOT WS-1 вафельница для корн-догов | blk триплет | col5 ← c7 (`Вафельница для корн-догов AIRHOT WS-1`); col36 — faithful RU (skel==c35 без `\n`, dims==c35: 5/2/3/295х185/140х40х15/220/1,5/410x385x315/8, no DEG; XCH Cyr х ×3 (`295х185`, `140х40х15`) + Lat x ×2 (`410x385x315`) verbatim; DASH `-` U+002D + `—` U+2014 em-dash в `корн-догів —` preserved) |
| 6 | 54 | 545492966 | AIRHOT WE-1B вафельница бельгийская | blk триплет | col5 ← c7 (`Вафельница для бельгийских вафель AIRHOT WE-1B`); col36 — faithful RU (skel==c35 c `\n`, dims==c35: 1/1/4/185х185/12/2/3/220/1,6/382х305х233/7, no DEG; XCH Cyr х ×3 (`185х185`, `382х305х233`) verbatim; DASH `-` U+002D ×2 (`WE-1B`, `2-3`); Lat B в модели `WE-1B`) |
| 7 | 55 | 593826052 | GoodFood WB1CF CREAM FISH рыбки | blknochg | c5==c7 genuine RU, c35!=c36 — fixed НЕ тронут |
| 8 | 56 | 593843443 | GoodFood WB1SA бельгийская квадратная (source-typo c5/c7 «бельгийськая») | blknochg | c5==c7 genuine RU verbatim (source-typo `бельгийськая` сохранён), c35!=c36 — fixed НЕ тронут |

**Verify:** 137 PASS / 0 FAIL (REGR 48 + ART 81 + TRIP 3 + blknochg 5).

**Глоссарий b7:** см. `chunk-glossary-w2.md` (816 → +N).

**Codepoint findings (TRIP):**
- SKU49 r50: `&deg;C` Lat U+0043 entity ×2, XCH Cyr х U+0445 в `7х7`, DASH `-` U+002D в `1-постова`, `&Oslash;` entity, skel содержит `\n`. Шаблон-сиблинг WBS-1C (b6 SKU48).
- SKU53 r54: NO DEG, XCH Cyr х U+0445 ×3 (`295х185`, `140х40х15`) + Lat x U+0078 ×2 (`410x385x315`) verbatim (source-mix), DASH `-` U+002D в `корн-догів` + `—` U+2014 em-dash в `корн-догів —` preserved, no `\n`.
- SKU54 r55: NO DEG, XCH Cyr х U+0445 ×3 (`185х185`, `382х305х233`) verbatim, DASH `-` U+002D ×2 (`WE-1B` + `2-3`), Lat B U+0042 в модели `WE-1B`, skel содержит `\n`.

**Soft-notes (pre-existing в c36, не наша правка):** SKU50/52/55 — c36 уже RU (fixed НЕ тронут). SKU51 (Lolly Waffle ёлочка) — c5 и c7 содержат `ё` verbatim («ёлочка»). SKU56 — c5/c7 имеют source-typo «бельгийськая» (RU + UA hybrid), col5 NMRU сохранён verbatim (genuine RU + источниковая опечатка). SKU53 — source-mix Cyr х и Lat x в размерах preserved. SKU54 — модель `WE-1B` с Lat B preserved.

**Открытых вопросов b7:** нет.

---

<!-- Сводка по батчу b8 ниже. -->
<!-- b8 marker -->

## b8 — SKU 57-64 (rows 58-65), 64/81

**Категории:** blk триплет 2 · blknotrip 0 · blknochg 5 · SKIP-НП 1 = 8.

| # | SKU | Артикул | Бренд / модель | Категория | Действие |
|---|---|---|---|---|---|
| 1 | 57 | 675937435 | AIRHOT WВ-НК1 вафельница гонгконгская с начинкой | blknochg | c5==c7 genuine RU, c35!=c36 — fixed НЕ тронут |
| 2 | 58 | 683160373 | FROSTY VE-01 вафельница гонконгская (bubble waffle) | blknochg | c5==c7 genuine RU, c35!=c36 — fixed НЕ тронут |
| 3 | 59 | 683160374 | FROSTY WS-15 вафельница бельгийская | blk триплет | col5 ← c7 (`Вафельница FROSTY WS-15 для бельгийских вафель`); col36 — faithful RU (skel==c35 без `\n`, dims==c35: 4х6/300/15/340x370x240/1,5, deg `°C` U+00B0+Lat U+0043 verbatim; XCH Cyr х в `4х6` + Lat x ×2 в `340x370x240` source-mix verbatim; DASH `—` U+2014 em-dash в `корпус — нержавеющая сталь` preserved) |
| 4 | 60 | 758595319 | GoodFood WB1RA вафельница поворотная круглые | blknochg | c5==c7 genuine RU, c35!=c36 — fixed НЕ тронут |
| 5 | 61 | 823889894 | Hendi 212103 вафельница бельгийская | blk триплет | col5 ← c7 (`Вафельница Hendi 212103 для бельгийских вафель`); col36 — faithful RU (skel==c35 c `\n` ×11, dims==c35: 2/3х5/1,5/220/320x437x/251/28, no DEG; XCH Cyr х в `3х5` + Lat x в `320x437x(H)251` source-mix; `(H)` высота preserved; SOURCE-MIX UA «однопостовая» (RU-форма в UA) + «неприлипающая поверхню» (UA noun + RU adj) → RU нормализованы «однопостовая» + «антипригарная поверхность»; UA «п'ять» / «об'ємних» апострофы → RU «пять» / «объемных»; UA «Тена» → RU «ТЭНа») |
| 6 | 62 | 1009164465 | GoodFood EG25R аппарат для оладьев | blknochg | c5==c7 genuine RU («оладьев» verbatim), c35!=c36 — fixed НЕ тронут |
| 7 | 63 | 1135992959 | SILVER 2137 вафельница сердечками | blknochg | c5==c7 genuine RU, c35!=c36 — fixed НЕ тронут |
| 8 | 64 | 1147781261 | HURAKAN HKN-GES2M вафельница бельгийская | SKIP-НП #1 | HURAKAN — НП-эксклюзив, fixed row65 НЕ тронут (тело из фида НП позже) |

**Verify:** 144 PASS / 0 FAIL (REGR 56 + ART 81 + TRIP 2 + blknochg 4 + SKIP-НП 1 verified untouched).

**Глоссарий b8:** см. `chunk-glossary-w2.md` (822 → 832).

**Codepoint findings (TRIP):**
- SKU59 r60: 1× literal `°C` U+00B0+Lat U+0043, XCH Cyr х U+0445 в `4х6` + Lat x U+0078 ×2 в `340x370x240` (source-mix), DASH `—` U+2014 em-dash в «корпус — неіржавка сталь» (RU: «корпус — нержавеющая сталь»), no `\n` (single-line skel с leading-text перед `<p>`).
- SKU61 r62: NO DEG, XCH Cyr х U+0445 в `3х5` + Lat x U+0078 в `320x437x(H)251` (source-mix), no DASH, ASCII apostrophe `'` U+0027 ×2 в «об'ємних»/«п'ять» (RU: без апострофа «объемных»/«пять»), `\n` ×11.

**Soft-notes (pre-existing в c36, не наша правка):** SKU57/58/60/62/63 — c36 уже RU (fixed НЕ тронут). SKU57/58 модель содержит Cyr В U+0412 verbatim (не Lat W+B). SKU61 c35 source-mix UA/RU (RU-форма «однопостовая» в UA-тексте; RU adj «неприлипающая» + UA noun «поверхню») — RU нормализованы. SKU62 c5 genuine RU «оладьев» (нестандартная форма род.мн., правильнее «оладий») — источник verbatim.

**Открытых вопросов b8:** нет.

---

<!-- Сводка по батчу b9 ниже. -->
<!-- b9 marker -->

## b9 — SKU 65-72 (rows 66-73), 72/81

**Категории:** blk триплет 2 · blknotrip 0 · blknochg 4 · SKIP-НП 2 = 8.

| # | SKU | Артикул | Бренд / модель | Категория | Действие |
|---|---|---|---|---|---|
| 1 | 65 | 1149716562 | Roller Grill GED 10 вафельница | blknochg | c5==c7 genuine RU, c35!=c36 — fixed НЕ тронут |
| 2 | 66 | 1149732444 | Roller Grill GED 20 вафельница | blknochg | c5==c7 genuine RU, c35!=c36 — fixed НЕ тронут |
| 3 | 67 | 1233837289 | GoodFood WB4B вафельница-тарталетница | blknochg | c5==c7 genuine RU, c35!=c36 — fixed НЕ тронут |
| 4 | 68 | 1755774485 | AIRHOT WE-1 вафельница бельгийская | blk триплет | col5 ← c7 (`Вафельница для бельгийских вафель AIRHOT WE-1`); col36 — faithful RU (skel==c35 c `\n` ×13, dims==c35: `<h2>`2/WE-1/4/1./4/`</h2>`2/175/12/2/3/220/1,2/250x350x260/6, no DEG; XCH Cyr х ×5 + Lat x ×2 в `250x350x260` source-mix verbatim; Cyr В ×4 в «Вафельница»/«220 В»/«кВт»/«Вес» preserved) |
| 5 | 69 | 2059494027 | HURAKAN HKN-GES2L вафельница | SKIP-НП #2 | HURAKAN — НП-эксклюзив, fixed row70 НЕ тронут (тело из фида НП позже) |
| 6 | 70 | 2059501393 | HURAKAN HKN-GES5HK вафельница гонконгская | SKIP-НП #3 | HURAKAN — НП-эксклюзив, fixed row71 НЕ тронут (тело из фида НП позже) |
| 7 | 71 | 2085217160 | EWT INOX MT100 аппарат для пончиков | blk триплет | col5 ← c7 (`Аппарат для приготовления пончиков EWT INOX MT100`); col36 — faithful RU (skel==c35 c `\n` ×17, dims==c35: MT100/`&#39;`×2/12/`&#39;`×2/7/3/300-1200/42/1050/600/750/6/220/53/530/565/465, no DEG; XCH Cyr х ×3 + Lat X ×1 в `INOX` preserved; `&#39;` U+0027 entity ×2 в UA «Об&#39;єм» → RU «Объем» (entity снят, dims preserved via numeric-entity-strip; numeric-entity «39» отфильтрован symmetrically); `220V` без пробела verbatim) |
| 8 | 72 | 2110637577 | GoodFood WB1FL вафельница цветок | blknochg | c5==c7 genuine RU, c35!=c36 — fixed НЕ тронут |

**Verify:** 153 PASS / 0 FAIL (REGR 64 + ART 81 + TRIP 2 + blknochg 4 + SKIP-НП 2 verified untouched).

**Глоссарий b9:** см. `chunk-glossary-w2.md` (832 → 842).

**Codepoint findings (TRIP):**
- SKU68 r69 (AIRHOT WE-1, len 543): NO DEG, XCH Cyr х U+0445 ×5 (вафлі/вафлі/хв/без/etc?) + Lat x U+0078 ×2 в `250x350x260`, DASH `-` U+002D ×2 в `WE-1` и `2-3`, Cyr В U+0412 ×4 в «Вафельниця/220 В/кВт/Вага». `<h2>...<br />\nКількість...</h2> <ul>` skel с двумя цифрами «2» из самих тегов h2 (учтены в dims).
- SKU71 r72 (EWT INOX MT100, len 664): NO DEG, XCH Cyr х U+0445 ×3 + Lat X U+0058 ×1 в `INOX`, DASH `-` U+002D ×2 в `300-1200`/`фаст-фуді`, `&#39;` U+0027 numeric-entity ×2 в UA «Об&#39;єм» — в RU «Объем» без апострофа/энтити; dims-strip расширен на numeric entities (`&(?:[a-zA-Z]+|#\d+);`) чтобы оба теряли «39» symmetrically.

**Soft-notes (pre-existing в c36, не наша правка):** SKU65/66 Roller Grill GED 10/20 — c36 уже RU (fixed НЕ тронут). SKU67 GoodFood WB4B вафельница-тарталетница c36 уже RU. SKU72 GoodFood WB1FL цветок c36 уже RU. SKU68/71 source c35==c36 (оба UA) — настоящие TRIP, faithful RU написан с нуля. SKU68 AIRHOT WE-1 — sibling SKU54 AIRHOT WE-1B (b7), шаблон совпадает (количество секций/сегментов/диаметр/толщина/таймер/терморегулятор/индикатор/время/материал/напряжение/мощность/габариты/вес). SKU71 EWT INOX MT100 — новая категория: аппарат для пончиков в форме колец.

**Открытых вопросов b9:** нет.

---

<!-- Сводка по батчу b10 ниже. -->
