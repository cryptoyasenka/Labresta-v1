# chunk-065 — diff (W2)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-065 (81 SKU, rows 2..82; ART 2121426618 … 2447469404)
**Apply key:** `Артикул` (col1, scoped per row)
**Worker:** W2 (параллельный, диапазон chunk-055 … chunk-085); продолжение chunk-064
**Status:** b8 DONE 64/81 (b9 предстоит; b1-b10 по 8 SKU + b11=SKU81 1 SKU)

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

## b3 — diff (SKU 17-24, rows 18-25), 24/81

**Категории:** blk триплет 2 · blknotrip 0 · blknochg 6 · SKIP-НП 0 = 8.

### blk триплет (2)
- **SKU 22** (r23, ART 2437750626, Frosty FWBD-20C): col5 `Кип'ятильник Frosty FWBD-20C` → `Кипятильник Frosty FWBD-20C`; col36 UA-leak → faithful RU (skel==c35, dims==c35: 20/20/8,5/30/100/1/2/2,00/220/220/220/500/4.20, deg `&deg;C` Lat U+0043 ×2; SOURCE TYPO `Cенсорная` Lat C verbatim).
- **SKU 24** (r25, ART 500052773, HENDI 208205 чаераздатчик-кофезаварник): col5 `Кавоварка одностінна HENDI 208205` → `Чаераздатчик-кофезаварник 15л. HENDI 208205`; col36 UA-leak → faithful RU (skel==c35 без `<p>` в начале, dims==c35: 15/85/1,5/90/280x580, degL `°С` ×2 literal U+00B0 + Cyr С, XCH Lat x в `D280x580h`).

### blknotrip (0)
— нет.

### blknochg (6)
- **SKU 17-19** (Silver 2040/2041/2042 электрокипятильники 12/16/23 л) / **SKU 20-21** (SARO ISOD 12 / SARO 317-2076 термосы) / **SKU 23** (GoodFood WB14S): c5==c7 genuine RU, c35!=c36.

### SKIP-НП (0)
— нет.

**Codepoint findings:** SKU22 `&deg;C` Lat ×2 + DASH U+002D в модели/inline + SOURCE-TYPO Lat C в `Cенсорна`; SKU24 literal `°` U+00B0 + Cyr С ×2 + XCH Lat x.

**Verify:** 105 PASS / 0 FAIL (REGR 16 + ART 81 + TRIP 2 + blknochg 6).

---

<!-- b4 marker -->

## b4 — diff (SKU 25-32, rows 26-33), 32/81

**Категории:** blk триплет 5 · blknotrip 0 · blknochg 3 · SKIP-НП 0 = 8.

### blk триплет (5)
- **SKU 25** (r26, ART 500052774, HENDI 209882 10л): col5 `Кип'ятильник HENDI 209882, 10л` → `Кипятильник HENDI 209882, 10л`; col36 UA-leak → faithful RU (skel==c35, dims==c35: 10/2,2/50/99/336х221х474, degL `°С` Cyr U+0421, XCH Cyr х ×2, DASH `–` U+2013).
- **SKU 26** (r27, ART 500052775, HENDI 209899 20л глинтвейн): col5 `Кип'ятильник HENDI 209899, 20л (підходить для глінтвейну)` → `Кипятильник HENDI 209899, 20л (подходит для глинтвейна)`; col36 UA-leak → faithful RU (skel==c35, dims==c35: 20/2,2/50/99/384x268x602, degL `°С`, XCH Lat x ×2, DASH `–` U+2013).
- **SKU 27** (r28, ART 500052776, HENDI 209905 30л глинтвейн): col5 `Кип'ятильник HENDI 209905, 30л (підходить для глінтвейну)` → `Кипятильник HENDI 209905, 30л (подходит для глинтвейна)`; col36 UA-leak → faithful RU (skel==c35, dims==c35: 30/2,2/50/99/520x/500, degL `°С`, XCH Lat x в `Ø 520x(H)500`, DASH `–` U+2013; «Некапающий» в c35 уже RU).
- **SKU 28** (r29, ART 500052779, HENDI 211304 15л подв.стенка): col5 `Кип'ятильник HENDI 211304, 15л , подвійна стінка` → `Кипятильник – кофеварочная машина HENDI 211304, 15л , двойная стенка` (col5←c7 verbatim с em-dash U+2013); col36 UA-leak → faithful RU (skel==c35, dims==c35: 15/85/1,5/90/288x602, degL `°С` ×2, XCH Lat x в `D288x602h`, DASH `-` U+002D в смешанной строке `Кип'ятильник - кофеварочная машина` сохранён в RU как `Кипятильник - кофеварочная машина`).
- **SKU 30** (r31, ART 1091390651, Hendi 240700 диспенсер 28л): col5 `Диспенсер для глінтвейну Hendi 240700, 28 л, нерж.` → `Диспенсер для глинтвейна Hendi 240700, 28 л, нерж.`; col36 UA-leak → faithful RU (skel==c35 c `\n` + `<h2>`/`<ul>`/`<li>`, dims==c35: 240700/28/110/75/28/447x441x485/2,5, degL `°C` **Lat U+0043** verbatim, XCH Lat x ×2 в `447x441x485`, DASH нет).

### blknotrip (0)
— нет.

### blknochg (3)
- **SKU 29** (HENDI 211366 кипятильник-кофеварочная машина 16л двойные стенки) / **SKU 31** (GGM WKH015 кипятильник-чаераздатчик 15л) / **SKU 32** (GGM WKH20 кипятильник 18л): c5==c7 genuine RU, c35!=c36.

### SKIP-НП (0)
— нет.

**Codepoint findings:** SKU25 `°С` Cyr U+0421 + XCH Cyr х ×2 + DASH `–` U+2013; SKU26 `°С` + XCH Lat x ×2 + DASH `–` U+2013; SKU27 `°С` + DASH `–` U+2013; SKU28 `°С` ×2 + XCH Lat x + DASH `-` U+002D в смешанной фразе (preserve); SKU30 `°C` Lat U+0043 + XCH Lat x ×2 + skel `\n`.

**Verify:** 113 PASS / 0 FAIL (REGR 24 + ART 81 + TRIP 5 + blknochg 3).

---

<!-- b5 marker -->

## b5 — diff (SKU 33-40, rows 34-41), 40/81

**Категории:** blk триплет 1 · blknotrip 0 · blknochg 7 · SKIP-НП 0 = 8.

### blk триплет (1)
- **SKU 33** (r34, ART 625811874, Hendi 240601 диспенсер глинтвейн 27л): col5 `Диспенсер для глінтвейну Hendi 240601, 27 л` → `Диспенсер для глинтвейна Hendi 240601, 27 л`; col36 UA-leak → faithful RU (skel==c35, dims==c35: 27/90/27/460x480x349/1,8/220, degL `°C` **Lat U+0043** verbatim, XCH Lat x ×2 в `460x480x349`, DASH нет).

### blknotrip (0)
— нет.

### blknochg (7)
- **SKU 34** (Эфес КНЭ-25) / **SKU 35** (Эфес КНЭ-50) / **SKU 36** (Эфес КНЭ-100) / **SKU 37** (GoodFood WB20HOT) / **SKU 38** (FROSTY WB-15 вафельница корн-дог) / **SKU 39** (FROSTY WS-15-2 бельгийские) / **SKU 40** (FROSTY XG-01 круглые): c5==c7 genuine RU, c35!=c36.

### SKIP-НП (0)
— нет.

**Codepoint findings:** SKU33 `°C` Lat U+0043 + XCH Lat x ×2 + DASH нет.

**Verify:** 121 PASS / 0 FAIL (REGR 32 + ART 81 + TRIP 1 + blknochg 7).

---

<!-- b6 marker -->

## b6 — diff (SKU 41-48, rows 42-49), 48/81

**Категории:** blk триплет 1 · blknotrip 0 · blknochg 7 · SKIP-НП 0 = 8.

### blk триплет (1)
- **SKU 48** (r49, ART 2301290442, Frosty WBS-1C вафельница): col5 `Вафельниця Frosty WBS-1C` → `Вафельница Frosty WBS-1C`; col36 UA-leak → faithful RU (skel==c35 c `\n`, dims==c35: 22/1/210/7х7/0/300/0/5/1,20/220/250/340/265/6.00, deg `&deg;C` ×2 **Lat U+0043** entity, XCH Cyr х в `7х7`, DASH `-` U+002D ×2 в `WBS-22B` + `1-постовая`, `&Oslash;` entity verbatim; SOURCE COPY-PASTE: тело упоминает WBS-22B при товаре WBS-1C — faithful preserve).

### blknotrip (0)
— нет.

### blknochg (7)
- **SKU 41** (Frosty XG-02 круглые) / **SKU 42** (SILVER 2147 бельгийская) / **SKU 43** (Frosty LD-117 1-постовая) / **SKU 44** (Frosty LD-2202 4-вафли) / **SKU 45** (Frosty LD-4 2-вафли) / **SKU 46** (Frosty WS-15-2 d 4-вафли) / **SKU 47** (GoodFood WB4S бельгийская): c5==c7 genuine RU, c35!=c36.

### SKIP-НП (0)
— нет.

**Codepoint findings:** SKU48 `&deg;C` Lat ×2 entity + XCH Cyr х в `7х7` + DASH `-` U+002D ×2 + `&Oslash;` entity.

**Verify:** 129 PASS / 0 FAIL (REGR 40 + ART 81 + TRIP 1 + blknochg 7).

---

<!-- Сводка по батчу b7 ниже. -->
<!-- b7 marker -->

## b7 — diff (SKU 49-56, rows 50-57), 56/81

**Категории:** blk триплет 3 · blknotrip 0 · blknochg 5 · SKIP-НП 0 = 8.

### blk триплет (3)
- **SKU 49** (r50, ART 2301293860, Frosty WBS-2C): col5 `Вафельниця Frosty WBS-2C` → `Вафельница Frosty WBS-2C`; col36 UA-leak → faithful RU (skel==c35 c `\n`, dims==c35: 1/210/7х7/0/300/0/5/2,4/220/500/340/265/11.50, deg `&deg;C` ×2 **Lat U+0043** entity verbatim, XCH Cyr х в `7х7`, DASH `-` U+002D в `1-постова`, `&Oslash;` entity verbatim; шаблон-сиблинг WBS-1C SKU48 b6).
- **SKU 53** (r54, ART 545492965, AIRHOT WS-1 корн-дог): col5 `Вафельниця для корн-догов AIRHOT WS-1` → `Вафельница для корн-догов AIRHOT WS-1`; col36 UA-leak → faithful RU (skel==c35 без `\n`, dims==c35: 5/2/3/295х185/140х40х15/220/1,5/410x385x315/8, no DEG, XCH Cyr х ×3 + Lat x ×2 source-mix verbatim, DASH `-` U+002D + `—` U+2014 em-dash в `корн-догів —` preserved).
- **SKU 54** (r55, ART 545492966, AIRHOT WE-1B бельгийская): col5 `Вафельниця для бельгійських вафель AIRHOT WE-1B` → `Вафельница для бельгийских вафель AIRHOT WE-1B`; col36 UA-leak → faithful RU (skel==c35 c `\n`, dims==c35: 1/1/4/185х185/12/2/3/220/1,6/382х305х233/7, no DEG, XCH Cyr х ×3 verbatim, DASH `-` U+002D ×2, Lat B в `WE-1B`).

### blknotrip (0)
— нет.

### blknochg (5)
- **SKU 50** (GoodFood WB-1HK Bubble гонконгская) / **SKU 51** (GoodFood WB1P Lolly Waffle ёлочка) / **SKU 52** (GoodFood DM6 аппарат для донатсов) / **SKU 55** (GoodFood WB1CF CREAM FISH) / **SKU 56** (GoodFood WB1SA бельгийская квадратная, source-typo `бельгийськая`): c5==c7 genuine RU, c35!=c36.

### SKIP-НП (0)
— нет.

**Codepoint findings:** SKU49 `&deg;C` Lat ×2 entity + XCH Cyr х в `7х7` + DASH `-` U+002D + `&Oslash;`; SKU53 no DEG + XCH Cyr х ×3 + Lat x ×2 source-mix + em-dash `—` U+2014; SKU54 no DEG + XCH Cyr х ×3 + DASH `-` U+002D ×2 + Lat B в `WE-1B`.

**Verify:** 137 PASS / 0 FAIL (REGR 48 + ART 81 + TRIP 3 + blknochg 5).

---

<!-- Сводка по батчу b8 ниже. -->
<!-- b8 marker -->

## b8 — diff (SKU 57-64, rows 58-65), 64/81

**Категории:** blk триплет 2 · blknotrip 0 · blknochg 5 · SKIP-НП 1 = 8.

### blk триплет (2)
- **SKU 59** (r60, ART 683160374, FROSTY WS-15 бельгийская): col5 `Вафельниця FROSTY WS-15 для бельгійських вафель` → `Вафельница FROSTY WS-15 для бельгийских вафель`; col36 UA-leak → faithful RU (skel==c35 без `\n` с leading-text перед `<p>`, dims==c35: 4х6/300/15/340x370x240/1,5, deg `°C` U+00B0+Lat U+0043 verbatim, XCH Cyr х в `4х6` + Lat x ×2 в `340x370x240` source-mix verbatim, em-dash `—` U+2014 в «корпус — нержавеющая сталь» preserved).
- **SKU 61** (r62, ART 823889894, Hendi 212103 бельгийская): col5 `Вафельниця Hendi 212103 для бельгійських вафель` → `Вафельница Hendi 212103 для бельгийских вафель`; col36 UA-leak → faithful RU (skel==c35 c `\n` ×11, dims==c35: 2/3х5/1,5/220/320x437x/251/28, no DEG, XCH Cyr х в `3х5` + Lat x в `320x437x(H)251` source-mix, `(H)` высота-маркер preserved; SOURCE-MIX UA/RU: UA «однопостовая» (RU-форма в UA) + «неприлипающая поверхню» (UA noun + RU adj) → RU нормализованы «однопостовая» + «антипригарная поверхность»; ASCII apostrophe `'` U+0027 в UA «об'ємних»/«п'ять» → RU без апострофа «объемных»/«пять»; UA «Тена» → RU «ТЭНа»).

### blknotrip (0)
— нет.

### blknochg (5)
- **SKU 57** (AIRHOT WВ-НК1 гонгконгская с начинкой, Cyr В в модели) / **SKU 58** (FROSTY VE-01 гонконгская bubble waffle) / **SKU 60** (GoodFood WB1RA поворотная круглые) / **SKU 62** (GoodFood EG25R оладьи, c5 «оладьев» нестандартная форма род.мн. verbatim) / **SKU 63** (SILVER 2137 сердечками): c5==c7 genuine RU, c35!=c36.

### SKIP-НП (1)
- **SKU 64** (r65, ART 1147781261, HURAKAN HKN-GES2M бельгийская) — НП-эксклюзив, fixed row65 НЕ тронут (тело из фида НП позже). SKIP-НП #1 для chunk-065.

**Codepoint findings:** SKU59 `°C` Lat ×1 + XCH Cyr х + Lat x ×2 source-mix + em-dash `—` U+2014; SKU61 no DEG + XCH Cyr х + Lat x source-mix + `(H)` + ASCII apostrophe `'` ×2 removed in RU.

**Verify:** 144 PASS / 0 FAIL (REGR 56 + ART 81 + TRIP 2 + blknochg 4 + SKIP-НП 1).

---

<!-- Сводка по батчу b9 ниже. -->
