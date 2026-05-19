# chunk-064 — diff (W2)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-064 (85 SKU, rows 2..86; ART 2567629973 … 2060623567)
**Apply key:** `Артикул` (col1, scoped per row)
**Worker:** W2 (параллельный, диапазон chunk-055 … chunk-085); продолжение chunk-063
**Status:** b6 DONE 48/85 (b7..b11 предстоят; b1-b11 по 8 SKU)

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

## b2 (SKU 9-16, rows 10-17)

Изменения только в `chunk-064-fixed.xlsx` (gitignored). Apply key `Артикул` (col1) НЕ менялся ни в одной строке.

**blk триплет (8): col5 ← col7 (genuine RU); col36 ← faithful RU (skeleton == UA col35)**

- **SKU 9 r10 ART 898016596 — Hendi 472507 мармит для супов Economic**
  - col5: `Марміт для супів Hendi 472507 підігрів горючої пастою - модель Economic` → `Мармит для супов Hendi 472507 подогрев горючей пастой - модель Economic`
  - col36: UA-leak (==col35) → RU (`<p>×2 <ul> 3×<li> </ul> <p> </p>`; `ø370x(H)325`/`Ø370x(H)325`/`10,0`/`10` verbatim; ø/Ø/лат.x)
- **SKU 10 r11 ART 898073892 — HENDI 470206 Rental-Top GN 1/1 9 л**
  - col5: `Марміт HENDI 470206 Rental-Top, кришка Rolltop, підігрів горючої пастою, - GN 1/1, 9 л` → `Мармит HENDI 470206 Rental-Top, крышка Rolltop, подогрев горючей пастой, - GN 1/1, 9 л`
  - col36: UA-leak → RU (`<p>×4 <ul> 3×<li> </ul>`; `590x340x(H)400`/`9,0`/`65`/`100`/`809709`/`1/1` verbatim; лат.x; источ. «Високоякісні професійний»→корректно «Высококачественный профессиональный»)
- **SKU 11 r12 ART 898155703 — HENDI 475201 Economic GN 1/2 чафингдиш**
  - col5: `Марміт HENDI 475201 модель Economic GN 1/2 (чафингдиш)` → `Мармит HENDI 475201 модель Economic GN 1/2 (чафингдиш)`
  - col36: UA-leak → RU (`<p>×2 <ul> 3×<li> </ul>`; `385x295x(H)310`/`4,5`/`65`/`1/2` verbatim; лат.x)
- **SKU 12 r13 ART 900262936 — HENDI 471005 Fiora GN 1/1 9 л чафингдиш**
  - col5: `Марміт HENDI 471005 модель Fiora GN 1/1, 9 л (чафингдиш)` → `Мармит HENDI 471005 модель Fiora GN 1/1, 9 л (чафингдиш)`
  - col36: UA-leak → RU (`<p>×2 <ul> 3×<li> </ul>`; `585x385x(H)315`/`9,0`/`65`/`100`/`1/1` verbatim; лат.x; источ. «Високоякісні професійний»→корректно «Высококачественный профессиональный»)
- **SKU 13 r14 ART 900277805 — HENDI 470619 Fiora GN 1/1 9 л чафингдиш**
  - col5: `Марміт HENDI 470619 модель Fiora GN 1/1, 9 л (чафингдиш)` → `Мармит HENDI 470619 модель Fiora GN 1/1, 9 л (чафингдиш)`
  - col36: UA-leak → RU (`<p>×2 <ul> 3×<li> </ul>`; `ø390x(H)270`/`3,5` verbatim; ø/лат.x; источ. опечатка «бачкок»→корректно «бачок»)
- **SKU 14 r15 ART 900374008 — HENDI 809709 нагревательный элемент GN 1/1**
  - col5: `Нагрівальний елемент HENDI 809709 електричний 200x320 мм для мармітів GN 1/1` → `Нагревательный элемент HENDI 809709 электрический 200x320 мм для мармитов GN 1/1`
  - col36: UA-leak → RU (`<p>×2 <ul> 3×<li> </ul>`; `200x320`/`220`/`400`/`809600`/`1/1` verbatim; лат.x/кир.В; _несоответствие источника: тело c35 артикул 809600 vs имя 809709 — faithful-рендер, soft-note для Yana_)
- **SKU 15 r16 ART 900396268 — HENDI 470930 переходник для ёмкостей для супов**
  - col5: `Перехідник HENDI 470930 для ємностей для супів 530х325 мм` → `Переходник HENDI 470930 для ёмкостей для супов 530х325 мм` (genuine ё источника сохранён verbatim в col5)
  - col36: UA-leak → RU (`<p>×2 <ul> 2×<li> </ul>`; `530x325`/`470909`/`470930` verbatim; лат.x; наш col36 ё-free «емкостей»)
- **SKU 16 r17 ART 900410500 — HENDI 470909 вклад для переходника 470930**
  - col5: `Внесок HENDI 470909 для перехідника 470930, 4.2 л, Ø220х(Н)190 мм (для супів)` → `Вклад HENDI 470909 для переходника 470930, 4.2л, Ø220х(Н)190 мм (для супов)`
  - col36: UA-leak → RU (`<p>×2 <ul> 3×<li> </ul>`; `Ø220х(Н)190`/`4,2`/`470909`/`470930` verbatim; Ø/кир.х/кир.Н)

**blknotrip (0):** нет.

**blknochg (0):** нет.

**SKIP-НП (0):** нет (бренды Hendi/HENDI не НП-эксклюзивные).

**Verify:** 104 PASS / 0 FAIL.

## b3 (SKU 17-24, rows 18-25)

Изменения только в `chunk-064-fixed.xlsx` (gitignored). Apply key `Артикул` (col1) НЕ менялся ни в одной строке.

**blk триплет (7): col5 ← col7 (genuine RU); col36 ← faithful RU (skeleton == UA col35)**

- **SKU 17 r18 ART 900422383 — HENDI 463000 подогреватель настольный на 2 свечи**
  - col5: `Підігрівач настільний HENDI 463000 на 2 свічки` → `Подогреватель настольный HENDI 463000 на 2 свечи`
  - col36: UA-leak (==col35) → RU (`<p> <ul> <li> </ul>`; `330x180x(H)65`/`463000`/`2` verbatim; лат.x)
- **SKU 18 r19 ART 900488528 — HENDI 194357 горючая паста 6 шт 200 г этанол**
  - col5: `Горюча паста 6 шт HENDI 194357 для подогева мармітів - 200 г, етанол` → `Горючая паста 6 шт HENDI 194357 для подогева мармитов - 200 г, этанол` (источ. опечатка «подогева» сохранена verbatim)
  - col36: UA-leak → RU (`<p><br/> </p> <ul> <li> </ul>`; `200`/`3`/`6` verbatim; `<br/>`+\n сохранён)
- **SKU 19 r20 ART 900658610 — HENDI 195604 дозатор для канистры 195505**
  - col5: `Дозатор HENDI 195604 для каністри з пастою 195505` → `Дозатор HENDI 195604 для канистры с пастой 195505`
  - col36: UA-leak → RU (`<p> </p> <p> </p>`; `195604`/`280`/`5` verbatim)
- **SKU 20 r21 ART 900666462 — HENDI 193693 топливо 24 шт 145 г диэтиленгликоль**
  - col5: `Паливо HENDI 193693 уп. 24 шт для мармітів з гнотом, 145 г, діетиленгліколь` → `Топливо HENDI 193693 упаковка 24 шт для мармитов с фитилем – банка 145 г, диэтиленгликоль` (en-dash – U+2013 verbatim)
  - col36: UA-leak → RU (`<p><br/> </p> <ul> <li> <li> </ul>`; `145`/`24`/`4` verbatim; источ. полум'я → пламени UA-clean; `± ` сохранён)
- **SKU 22 r23 ART 1144483193 — Hendi Kitchen Line 707098 термоконтейнер 21 л для пиццы**
  - col5: `Термоконтейнер Kitchen Line Hendi 707098 (21 літр) для піци` → `Термоконтейнер Hendi Kitchen Line 707098 (21 литр) для пиццы`
  - col36: UA-leak → RU (`<p>×7 <ul> 6×<li> </ul>`; `420x420x(H)117`/`480x480x(H)165мм`/`-20°C`/`+110°C`/`+ 80 ° C`/`100%`/`21`/`3`/`40` verbatim; «див»→«см»; лат.x)
- **SKU 23 r24 ART 1146294285 — Hendi 871713 витрина двойная нейтральная**
  - col5: `Вітрина подвійна Hendi 871713 нейтральна` → `Витрина двойная Hendi 871713 нейтральная`
  - col36: UA-leak → RU (`<p> <ul> 4×<li> </ul>`; `465x310x(H)410`/`871713.`/`2` verbatim; лат.x)
- **SKU 24 r25 ART 1146294718 — Hendi 871706 витрина одиночная нейтральная**
  - col5: `Вітрина одиночна Hendi 871706 нейтральна` → `Витрина одиночная Hendi 871706 нейтральная`
  - col36: UA-leak → RU (`<p> <ul> 4×<li> </ul>`; `465x310x(H)190`/`871706.`/`1` verbatim; лат.x; _тело c35 «подвійна» при одиночном товаре 871706 — артефакт копипасты, faithful-рендер «двойная», soft-note для Yana_)

**blknotrip (0):** нет.

**blknochg (1): RU уже корректен — fixed НЕ тронут**

- SKU 21 r22 ART 901111364 — HENDI 193679 топливо 250 г диэтиленгликоль. c5==c7 genuine RU, c36 properly translated (c35!=c36). _Замечание: c36 «Cгорает» начинается с латинской C (U+0043) вместо кириллической С — артефакт источника в genuine RU (не наша правка), для merge-ревью Yana._

**SKIP-НП (0):** нет (бренды Hendi/HENDI не НП-эксклюзивные).

**Verify:** 107 PASS / 0 FAIL.

## b4 (SKU 25-32, rows 26-33)

Изменения только в `chunk-064-fixed.xlsx` (gitignored). Apply key `Артикул` (col1) НЕ менялся ни в одной строке.

**blk триплет (0):** нет.

**blknotrip (1): col36 ← faithful RU (col35==col36 UA-leak); col5 lang-neutral НЕ тронут**

- **SKU 28 r29 ART 2123253137 — GastroPlast TCB--00100 термоконтейнер (GN 1/1 100 мм)**
  - col5: `Термоконтейнер GastroPlast TCB--00100 (GN 1/1 100 мм)` — lang-neutral (c5==c7), НЕ тронут
  - col36: UA-leak (==col35) → RU (`<p><br/>×2 </p> <p><br/>×3 </p> <p><br/>×2 </p> <ul> 4×<li> </ul>`; `38-40`/`PA6.`/`-40 &deg;C`/`+100 &deg;C`/`1,5 &deg;C`/`1 &deg;C`/`550х350х(В)110`/`635х435х(В)200` verbatim; `&rsquo;` источ. снят (RU «здоровья» без апострофа); `&deg;` entity verbatim; кир. х/В verbatim; ` / ` verbatim)

**blknochg (7): RU уже корректен — fixed НЕ тронут**

- SKU 25 r26 ART 2123542091 — Hendi 707487 термос 15 л. c5==c7 genuine RU, c36 переведён (c35!=c36). _Замечание: c36 «изготовлены из Сталь AISI 304» (именит. п. вместо родит.) + `<br />` после «температуры» — артефакт источника genuine RU, не наша правка, soft-note Yana._
- SKU 26 r27 ART 2123546166 — Hendi 707517 термос 36 л. c5==c7 genuine RU, c36 переведён (c35!=c36). _Замечание: тело c35 (UA) «Термос на 15 літрів» при товаре 36 л — копипаста источника; c36 (RU) корректно «на 36 литров» (dims c35!=c36 — дефект UA-источника, не наша правка), soft-note Yana._
- SKU 27 r28 ART 1146262096 — Avatherm 601М термоконтейнер. c5==c7 (lang-neutral), c36 переведён (c35!=c36); fixed НЕ тронут.
- SKU 29 r30 ART 659130237 — Avatherm 601 термоконтейнер. c5==c7 (lang-neutral), c36 переведён (c35!=c36); fixed НЕ тронут.
- SKU 30 r31 ART 1146269989 — Avatherm 660 150 л термоконтейнер для выпечки. c5==c7 genuine RU, c36 переведён (c35!=c36); fixed НЕ тронут.
- SKU 31 r32 ART 1146273884 — Avatherm PizzaBox Red термоконтейнер для пиццы. c5==c7 (lang-neutral), c35==c36 уже корректный RU (UA-flag False, `<h2>`); fixed НЕ тронут.
- SKU 32 r33 ART 619276860 — GoodFood SK5 электросупница (мармит) 5,7 л. c5==c7 genuine RU, c36 переведён (c35!=c36; `&ndash;`/`&deg;С` кир.С verbatim); fixed НЕ тронут.

**SKIP-НП (0):** нет (бренды Hendi/Avatherm/GastroPlast/GoodFood не НП-эксклюзивные).

**Verify:** 117 PASS / 0 FAIL.

## b5 (SKU 33-40, rows 34-41)

Изменения только в `chunk-064-fixed.xlsx` (gitignored). Apply key `Артикул` (col1) НЕ менялся ни в одной строке.

**blk триплет (6): col5 ← c7 (genuine RU verbatim); col36 ← faithful RU (skel==c35, dims==c35, `&deg;`-хвост==c35)**

- **SKU 33 r34 ART 421840639 — Bartscher 200063 кипятильник 28 л**
  - col5: `Електрокип'ятильників 28 л Bartscher 200063` → `Электрокипятильник 28 л Bartscher 200063` (c7 verbatim)
  - col36: UA-leak (c35==c36) → RU (`<p> <ul> 3×<li> </ul>`; `&#39;` источ. снят; `&deg;C` ×2 лат. C (U+0043) verbatim; `28`/`220`/`2,8`/`395`/`640` verbatim)
- **SKU 36 r37 ART 2193248085 — AIRHOT WB-40 водонагреватель**
  - col5: `Водонагрівач електричний AIRHOT WB-40` → `Водонагреватель электрический AIRHOT WB-40` (c7 verbatim)
  - col36: UA-leak (c35==c36) → RU (`<p>×2 <p><strong> </p> <ul> 15×<li> </ul>`; `&#39;` снят; `&deg;С` кир. С (U+0421) verbatim; `400x400x640,`/`410x410x650,`/`5.030,`/`6.230,` лат.x + хвост-запятые verbatim)
- **SKU 37 r38 ART 2193280101 — AIRHOT CP06 электрокипятильник-кофеварка**
  - col5: `Електрокип'ятильник-кавоварка AIRHOT CP06` → `Электрокипятильник-кофеварка AIRHOT CP06` (c7 verbatim)
  - col36: UA-leak (c35==c36) → RU (`<p> <p><strong> </p> <ul> 16×<li> </ul>`; тело «CP-06» faithful (имя c7 «CP06» — артефакт источника, soft-note Yana); `&deg;С` кир. verbatim)
- **SKU 38 r39 ART 2193283954 — AIRHOT CP15 электрокипятильник-кофеварка**
  - col5: `Електрокип'ятильник-кавоварка AIRHOT CP15` → `Электрокипятильник-кофеварка AIRHOT CP15` (c7 verbatim)
  - col36: UA-leak (c35==c36) → RU (`<p> <p><strong> </p> <ul> 16×<li> </ul>`; `&deg;С` кир. verbatim)
- **SKU 39 r40 ART 2237103884 — Airhot CP10 электрокипятильник-кофеварка**
  - col5: `Електрокип'ятильник-кавоварка Airhot CP10` → `Электрокипятильник-кофеварка Airhot CP10` (c7 verbatim)
  - col36: UA-leak (c35==c36) → RU (2×`<ul>`: `<p> <p><strong> </p> <ul> 15×<li> </ul> <p>В комплекте:</p> <ul> 2×<li> </ul>`; тело «AIRHOT CP10» faithful (имя c7 «Airhot CP10» — регистр источника, soft-note Yana); `&deg;С` кир. verbatim)
- **SKU 40 r41 ART 2463611818 — Bartscher 200043 электрокипятильник**
  - col5: `Електрокип'ятильник Bartscher 200043` → `Электрокипятильник Bartscher 200043` (c7 verbatim)
  - col36: UA-leak (c35==c36) → RU (`<p>×2 <p><strong> </p> <ul> 15×<li> </ul> <p>Размеры в упаковке </p> <ul> 4×<li> </ul>`; `220V` лат. V verbatim; «Нержавеющая сталь/Пластик.» ` / ` skel verbatim; хвостовой пробел «упаковке » verbatim)

**blknotrip (0):** нет.

**blknochg (1): RU уже корректен — fixed НЕ тронут**

- SKU 34 r35 ART 422807332 — GGM WKH06 кипятильник-чаераздатчик. c5==c7 genuine RU, c36 properly translated (c35!=c36); fixed НЕ тронут.

**SKIP-НП (1): NP-эксклюзивный бренд — fixed НЕ тронут**

- SKU 35 r36 ART 2060619856 — Hurakan HKN-HVN10. SKIP-НП (brand=Hurakan, тело из фида НП позже); fixed row36 НЕ тронут (col5/col36 как в источнике).

**Verify:** 125 PASS / 0 FAIL.

## b6 (SKU 41-48, rows 42-49)

Изменения только в `chunk-064-fixed.xlsx` (gitignored). Apply key `Артикул` (col1) НЕ менялся ни в одной строке.

**blk триплет (6): col5 ← c7 (genuine RU verbatim); col36 ← faithful RU (skel==c35, dims==c35, `&deg;`/`°`-хвост==c35)**

- **SKU 41 r42 ART 2463614102 — Bartscher 200128 электрокипятильник 15 л**
  - col5: `Електрокип'ятильник Bartscher 200128` → `Электрокипятильник Bartscher 200128` (c7 verbatim)
  - col36: UA-leak (c35==c36) → RU (`<p>×2 <p><strong> </p> <ul> 17×<li> </ul> <p>Размеры в упаковке </p> <ul> 4×<li> </ul>`; `&#39;` снят; `220V` лат. V verbatim; `20...100`/`200128` verbatim; хвостовой пробел «упаковке » verbatim)
- **SKU 42 r43 ART 421840637 — Bartscher A200050 электрокипятильник-термос 20 л**
  - col5: `Електрокип'ятильник — термос багатофункціональний 20 л Bartscher A200050` → `Электрокипятильник - термос многофункциональный 20 л Bartscher A200050` (c7 verbatim; c7 дефис, c4/c5 em-dash)
  - col36: UA-leak (c35==c36) → RU (`<p> </p> <ul> <li>×3 </ul>` одной строкой; `&#39;`/`'` снят; «Вес — 6 кг» em-dash U+2014 + хвостовой пробел перед `</p>` verbatim)
- **SKU 43 r44 ART 421840638 — Bartscher 200054 электрокипятильник 10 л**
  - col5: `Електрокип'ятильник 10 л Bartscher 200054` → `Электрокипятильник 10 л Bartscher 200054` (c7 verbatim)
  - col36: UA-leak (c35==c36) → RU (`<p> </p> <ul> <li>×3 </ul>`; «Основание — пластик» em-dash; «30 °С – 100 °C» кир. С (U+0421) + лат. C (U+0043) + en-dash U+2013 + ° U+00B0 verbatim; хвостовой пробел перед `</p>`)
- **SKU 44 r45 ART 421840640 — Bartscher 200069 электрокипятильник 8,5 л**
  - col5: `Електрокип'ятильник 8,5 л Bartscher 200069` → `Электрокипятильник 8,5 л Bartscher 200069` (c7 verbatim)
  - col36: UA-leak (c35==c36) → RU (`<p> </p> <ul> <li>×3 </ul>`; 2×em-dash «Кипятильник — Диспенсер», «энергии — преимущества»; «100 °C» лат. C + ° U+00B0 verbatim)
- **SKU 45 r46 ART 421840641 — EWT INOX WB10E1 электрокипятильник 10 л**
  - col5: `Електрокип'ятильник EWT INOX WB10E1` → `Электрокипятильник EWT INOX WB10E1` (c7 verbatim)
  - col36: UA-leak (c35==c36) → RU (`<h2> </h2> <p> </p> <ul> 3×<li> </ul>`; `<h2>` verbatim; `&#39;` снят; `WB10E1` модель verbatim)
- **SKU 46 r47 ART 421840643 — EWT INOX WB30E1 электрокипятильник 30 л**
  - col5: `Електрокип'ятильник EWT INOX WB30E1` → `Электрокипятильник EWT INOX WB30E1` (c7 verbatim)
  - col36: UA-leak (c35==c36) → RU (`<p> </p> <ul> <li>×3 </ul>`; `&#39;` снят; хвостовой пробел перед `</p>`)

**blknotrip (0):** нет.

**blknochg (2): RU уже корректен — fixed НЕ тронут**

- SKU 47 r48 ART 422807335 — GGM WKH10 кипятильник 9 л. c5==c7 genuine RU, c36 properly translated (c35!=c36); fixed НЕ тронут.
- SKU 48 r49 ART 422807337 — GGM WKH010 кипятильник-чаераздатчик 10 л. c5==c7 genuine RU, c36 properly translated (c35!=c36); fixed НЕ тронут.

**SKIP-НП (0):** нет (бренды Bartscher/EWT INOX/GGM не НП-эксклюзивные).

**Verify:** 133 PASS / 0 FAIL.

<!-- Сводки по батчам b7..b11 ниже. -->
