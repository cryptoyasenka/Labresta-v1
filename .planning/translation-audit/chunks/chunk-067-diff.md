# chunk-067 — diff (W2)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-067 (74 SKU, rows 2..75; ART 2045345276 … 2033010783)
**Apply key:** `Артикул` (col1, scoped per row)
**Worker:** W2 (параллельный, диапазон chunk-055 … chunk-085); продолжение chunk-066
**Status:** b6 DONE 48/74 (cum: TRIP 22 / blknotrip 0 / blknochg 22 / SKIP-НП 4; b7 предстоит; b1..b9 по 8 SKU + b10=SKU73-74 2 SKU)

Категории: blk триплет / blknotrip / blknochg / SKIP-НП. Формат — как chunk-066-diff.md.

SKIP-НП prelim (forward-only, тело из фида НП позже): FAGOR/Fagor — SKU41 (row42 ADVANCE AD 505 BDD), SKU42 (row43 FIR-30-DD), SKU43 (row44 FIR-80-DD); TATRA — SKU45 (row46 TW.F50+DR+DD), SKU70 (row71 TW.H50+DR+DD); Apach/APACH — SKU51 (row52 AF400 DD), SKU52 (row53 AF500 DIG DD), SKU71 (row72 AK 901). Точная классификация — по ходу батчей.

---

<!-- Сводки по батчам ниже (b1..b10 будут добавлены при выполнении каждого батча). -->


## Батч 1 (SKU 1-8, rows 2-9) — DONE

**Итог:** TRIP 5 / blknotrip 0 / blknochg 3 / SKIP-НП 0 / verify 118 PASS / 0 FAIL.

### blk триплет (5)

| SKU | row | Артикул | Бренд+модель | col5: UA→RU | col36 |
|---|---|---|---|---|---|
| 4 | 5 | 913655974 | Frosty HF-100 | `Прес ручний для гамбургерів Frosty HF-100` → `Пресс ручной для гамбургеров Frosty HF-100` | faithful RU body (gabarits 220х300х280) skel==UA |
| 5 | 6 | 913679416 | Frosty HF-130 | `Прес ручний для гамбургерів Frosty HF-130` → `Пресс ручной для гамбургеров Frosty HF-130` | faithful RU body (gabarits 320х250х300) skel==UA |
| 6 | 7 | 1267124747 | Fimar Easy Line HF100 | `Прес для гамбургерів Fimar Easy Line HF100` → `Пресс для гамбургеров Fimar Easy Line HF100` | faithful RU body skel==UA |
| 7 | 8 | 2044637169 | Frosty HM-100 | `Прес для гамбургерів Frosty HM-100` → `Пресс для гамбургеров Frosty HM-100` | faithful RU body (&Oslash; 100 мм, 220x300x280) skel==UA |
| 8 | 9 | 2044641303 | Frosty HM-130 | `Прес для гамбургерів Frosty HM-130` → `Пресс для гамбургеров Frosty HM-130` | faithful RU body (&Oslash; 130 мм, 320x250x300) skel==UA |

### blknochg (3)

| SKU | row | Артикул | Бренд+модель | Причина |
|---|---|---|---|---|
| 1 | 2 | 2045345276 | GoodFood CR206 | c5==c7 genuine RU, c36 genuine RU без UA-mark; не трогаем |
| 2 | 3 | 557515809 | GoodFood HF100 | c5==c7 genuine RU (live), c36 genuine RU; не трогаем |
| 3 | 4 | 775948663 | GoodFood HF130 | c5==c7 genuine RU (live), c36 genuine RU; не трогаем |

### SKIP-НП (0)

В b1 нет brand-locked НП. (prelim 8 на b6/b7/b9.)


## Батч 2 (SKU 9-16, rows 10-17) — DONE

**Итог:** TRIP 2 / blknotrip 0 / blknochg 6 / SKIP-НП 0 / verify 150 PASS / 0 FAIL.

### blk триплет (2)

| SKU | row | Артикул | Бренд+модель | col5: UA→RU | col36 |
|---|---|---|---|---|---|
| 11 | 12 | 2519699987 | Frosty BM-100 | `Прес для гамбургерів Frosty BM-100` → `Пресс для гамбургеров Frosty BM-100` | faithful RU body (&Oslash;100, 210x290x275) skel==UA; UA typo «мясом» без апострофа → RU «мясом» faithful normalize |
| 12 | 13 | 2519715501 | Frosty BM-130 | `Прес для гамбургерів Frosty BM-130` → `Пресс для гамбургеров Frosty BM-130` | faithful RU body (&Oslash;130, 240x310x295) skel==UA |

### blknochg (6)

| SKU | row | Артикул | Бренд+модель | Причина |
|---|---|---|---|---|
| 9 | 10 | 2110646917 | GoodFood HF150 | c5==c7 genuine RU, c36 genuine RU; не трогаем |
| 10 | 11 | 2180891014 | PIMAK BKS.100 (люля-кебаб) | c5==c7 mixed `Пресс для люля-кебабу PIMAK BKS.100` live; c36 genuine RU |
| 13 | 14 | 900549160 | Hendi 272411 обогреватель газовый | c5==c7 genuine RU; c36 genuine RU (с ё в source — не трогаем) |
| 14 | 15 | 900598472 | Hendi 272602 обогреватель газовый | c5==c7 genuine RU; c36 genuine RU |
| 15 | 16 | 900604409 | Hendi 272404 обогреватель пирамида | c5==c7 genuine RU; c36 genuine RU |
| 16 | 17 | 900609589 | Hendi 272701 обогреватель регулир. высота | c5==c7 genuine RU; c36 genuine RU |

### SKIP-НП (0)

В b2 нет brand-locked НП. (prelim 8 на b6/b7/b9.)


## Батч 3 (SKU 17-24, rows 18-25) — DONE

**Итог:** TRIP 3 / blknotrip 0 / blknochg 5 / SKIP-НП 0 / verify 186 PASS / 0 FAIL.

### blk триплет (3)

| SKU | row | Артикул | Бренд+модель | col5: UA→RU | col36 |
|---|---|---|---|---|---|
| 20 | 21 | 680812889 | FROSTY CVT-03 тостер конвейерный | `Тостер конвеєрний FROSTY CVT-03` → `Тостер конвейерный FROSTY CVT-03` | faithful RU body (320 кусочков, 360 мм лента, 520х480х400, 2,6 кВт) skel==UA |
| 22 | 23 | 2465032226 | Bartscher 100373 тостер вертикальный | c5 unchanged `Тостер Bartscher 100373` (brand+model) | faithful RU body (2 паза 140х35, 6 уровней подрумянивания, 220V, Китай, размеры в упаковке) skel==UA; UA `&#39;` в `підрум&#39;янювання` → RU без апострофа; `знімна` → `съемная` без ё |
| 23 | 24 | 680802268 | FROSTY DS-6 тостер вертикальный | `Тостер вертикальний FROSTY DS-6` → `Тостер вертикальный FROSTY DS-6` | faithful RU body (на 6 кусочков, 400х210х215, 2,5 кВт, 220 В) skel==UA |

### blknochg (5)

| SKU | row | Артикул | Бренд+модель | Причина |
|---|---|---|---|---|
| 17 | 18 | 1128659172 | AIRHOT CS-30 кукурузоварка | c5==c7 genuine RU; c36 genuine RU (с ё в source — не трогаем); skel-eq, dims match — но c36 без UA-mark, blknochg |
| 18 | 19 | 671776158 | SILVER СМ 250 кукурузоварка | c5==c7 genuine RU; c36 genuine RU; не трогаем |
| 19 | 20 | 671783156 | SILVER СМ 400 кукурузоварка | c5==c7 genuine RU; c36 genuine RU; не трогаем |
| 21 | 22 | 2043293826 | Frosty AT360T тостер горизонтальный | c5==c7 genuine RU; c36 genuine RU **расширенная версия** (skel-eq False, dims различаются) — НЕ blknotrip, это отдельная редакция RU, не трогаем |
| 24 | 25 | 680810516 | FROSTY CVT-02 тостер конвейерный | c5==c7 genuine RU; c36 genuine RU; не трогаем |

### SKIP-НП (0)

В b3 нет brand-locked НП.


## Батч 4 (SKU 25-32, rows 26-33) — DONE

**Итог:** TRIP 7 / blknotrip 0 / blknochg 1 / SKIP-НП 0 / verify 238 PASS / 0 FAIL.

### blk триплет (7)

| SKU | row | Артикул | Бренд+модель | col5: UA→RU | col36 |
|---|---|---|---|---|---|
| 25 | 26 | 680817555 | Hendi 261309 тостер конвейерный | `Тостер конвеєрний Hendi 261309` → `Тостер конвейерный Hendi 261309` | faithful RU body (непрерывной обжарки, нагревательные элементы, передний/задний поддон) skel==UA |
| 26 | 27 | 883743422 | FROSTY DS-4 тостер вертикальный | `Тостер вертикальний FROSTY DS-4` → `Тостер вертикальный FROSTY DS-4` | faithful RU body (на 4 кусочка, 315х270х220 мм) skel==UA |
| 27 | 28 | 1141182737 | SIRMAN 4Q тостер горизонтальный | `Тостер SIRMAN 4Q горизонтальний` → `Тостер SIRMAN 4Q горизонтальный` | faithful RU body (две полочки, съемные решетки без ё, кварцевые трубы, армированные нагреватели) skel==UA |
| 29 | 30 | 1889465346 | Fimar TOP6 тостер горизонтальный | c5 unchanged `Тостер Fimar TOP6` (латинский brand+model, UA c4==c6) | faithful RU body (две полочки, кварцевые лампы, таймер 15 мин.) skel==UA |
| 30 | 31 | 2043314442 | Frosty TT-450 тостер конвейерный | c5←c7 verbatim `Тостер конвеерный Frosty TT-450` (source typo «конвеерный» faithful, no normalize) | faithful RU body (~350 кус./час, 360х300, 7 позиций, 3 режима, нержавеющая сталь) skel==UA; SPACE-разделитель между первыми 3 `<p>` блоками воспроизводит источник |
| 31 | 32 | 2126973957 | Frosty ETC-300 тостер конвейерный | `Тостер конвеєрний Frosty ETC-300` → `Тостер конвейерный Frosty ETC-300` | faithful RU body (~250 кус./час, 260х300, 7 позиций, 3 режима) skel==UA |
| 32 | 33 | 2126976992 | Frosty ETC-450 тостер конвейерный | `Тостер конвеєрний Frosty ETC-450` → `Тостер конвейерный Frosty ETC-450` | faithful RU body (~350 кус./час, 360х300, 2,80 кВт/220В, 495x420x410, вес 16.00) skel==UA |

### blknochg (1)

| SKU | row | Артикул | Бренд+модель | Причина |
|---|---|---|---|---|
| 28 | 29 | 1889450319 | Fimar TOP3 | c5==c7 genuine RU; c36 genuine RU; источник содержит расхождение c4/c6=SIRMAN UA vs c5/c7=Fimar TOP3 и c35=SIRMAN body vs c36=Fimar body — live store fixed, blknochg не правим |

### SKIP-НП (0)

В b4 нет brand-locked НП.


## Батч 5 (SKU 33-40, rows 34-41) — DONE

**Итог:** TRIP 3 / blknotrip 0 / blknochg 5 / SKIP-НП 0 / verify 274 PASS / 0 FAIL.

### blk триплет (3)

| SKU | row | Артикул | Бренд+модель | col5: UA→RU | col36 |
|---|---|---|---|---|---|
| 34 | 35 | 2565679278 | Bartscher 100374 тостер вертикальный | c5 unchanged `Тостер Bartscher 100374` (brand+model latin) | faithful RU body (4 паза 140х35, 6 уровней подрумянивания, 2 пульта, 2 съемные насадки без ё, 220V Китай, размеры в упаковке) skel==UA |
| 35 | 36 | 680814299 | Hendi 261163 тостер | c5 unchanged `Тостер Hendi 261163` | faithful RU body (2 кусочка, два зажима, независимые термостаты, таймер 8 мин., 300х200х233, 1,2 кВт) skel==UA |
| 36 | 37 | 1161583632 | Hendi 262214 тостер инфракрасный | `Тостер інфрачервоний Hendi 262214` → `Тостер инфракрасный Hendi 262214` | faithful RU body (h2-заголовок; 6 кусочков, 2 уровня нагревания, инфракрасные кварцевые трубки 30 сек, таймер 15 мин., 6 зажимов, 438х290х402, 3 кВт) skel==UA |

### blknochg (5)

| SKU | row | Артикул | Бренд+модель | Причина |
|---|---|---|---|---|
| 33 | 34 | 2538748710 | SARO ARIS 4 тостер | c5==c7 latin brand+model; c36 genuine RU; c35!=c36 skel-eq False — две редакции, blknochg не трогаем |
| 37 | 38 | 2043309201 | Frosty TT-300 тостер конвейерный | c5==c7 `Тостер конвеерный Frosty TT-300` source typo «конвеерный» live; c36 genuine RU расширенная; c35!=c36; не трогаем |
| 38 | 39 | 470763674 | SILANOS T1500 машина посудомоечная туннельная | c5==c7 genuine RU; c36 genuine RU minor variant; c35!=c36 skel-eq True dims match; не трогаем |
| 39 | 40 | 644895365 | Empero EMP.2000 с сушкой | c5==c7 genuine RU; c36 genuine RU; одна dim source typo c35:185 vs c36:85; не трогаем |
| 40 | 41 | 644913557 | Empero EMP.3000 с сушкой и блоком предварительной мойки | c5==c7 genuine RU; c36 genuine RU; одна dim source typo c35:185 vs c36:85; не трогаем |

### SKIP-НП (0)

В b5 нет brand-locked НП.


## Батч 6 (SKU 41-48, rows 42-49) — DONE

**Итог:** TRIP 2 / blknotrip 0 / blknochg 2 / SKIP-НП 4 / verify 306 PASS / 0 FAIL.

### blk триплет (2)

| SKU | row | Артикул | Бренд+модель | col5: UA→RU | col36 |
|---|---|---|---|---|---|
| 46 | 47 | 2687386113 | ASBER GE-500 B DD посудомоечная (помпа слива) | `Посудомийна машина ASBER GE-500 B DD (помпа зливу)` → `Посудомоечная машина ASBER GE-500 B DD (помпа слива)` | faithful RU body (цикл 120 сек, кассета 500х500, бак 25л, бойлер 7л, дозатор, дренажная помпа, 600х605х830, 3.4 кВт, 220 В) skel==UA |
| 47 | 48 | 468028908 | Oztiryakiler OBM1080MPDR (Ozti) купольная | `Посудомийна машина купольна Oztiryakiler OBM1080MPDR (Ozti)` → `Посудомоечная машина купольная Oztiryakiler OBM1080MPDR (Ozti)` | faithful RU body h2-заголовок (69/35/27 кассет/час, IPX5, 50x50 см, 380 В / 9,66 кВт, 50/102/132 с, 55-60 °C мойка / 80-85 °C ополаскивание, 670х785х1860) skel==UA |

### blknochg (2)

| SKU | row | Артикул | Бренд+модель | Причина |
|---|---|---|---|---|
| 44 | 45 | 2054640013 | Adler EVO 50 PD посудомоечная | c5==c7 genuine RU; c36 genuine RU; c35!=c36 minor variant; не трогаем |
| 48 | 49 | 470771585 | SILANOS NЕ 700 PS PD/РВ (со сливной помпой) | c5==c7 genuine RU; c36 genuine RU; c35!=c36 minor variant; не трогаем |

### SKIP-НП (4)

| # | SKU | row | Артикул | Бренд | Название |
|---|---|---|---|---|---|
| #1 | 41 | 42 | 893760283 | FAGOR | Посудомийна машина FAGOR ADVANCE AD 505 BDD |
| #2 | 42 | 43 | 1282877474 | Fagor | Посудомийна машина Fagor FIR-30-DD фронтальна |
| #3 | 43 | 44 | 1282884918 | Fagor | Посудомийна машина Fagor FIR-80-DD купольна |
| #4 | 45 | 46 | 2331547054 | TATRA | Посудомийна машина TATRA TW.F50+DR+DD |


## Батч 7 (SKU 49-56, rows 50-57) — DONE

**Итог:** TRIP 4 / blknotrip 1 / blknochg 1 / SKIP-НП 2 / verify 350 PASS / 0 FAIL.

### blk триплет (4)

| SKU | row | Артикул | Бренд+модель | col5: UA→RU | col36 |
|---|---|---|---|---|---|
| 50 | 51 | 1306929611 | Krupps K1100E (серия Koral) купольная | `Посудомийна машина Krupps K1100E (серія Koral) купольна` → `Посудомоечная машина Krupps K1100E (серия Koral) купольная` | faithful RU body (415мм тарелки, 60/40/30/15 кассет/час, 60/90/120/240 сек, 620х770х1900, 9.0 кВт, 380 В, расход 2 л preserve `&ndash;`) skel==UA |
| 54 | 55 | 469910596 | SILANOS NE1300 PD/PB купольная | `Посудомийна машина SILANOS NE1300 PD/PB купольна` → `Посудомоечная машина SILANOS NE1300 PD/PB купольная` | faithful RU body (405мм окно, 48/30/20 кассет/час, 75/120/180 сек, 655х770х1505/1955, 7.1 кВт, 380 В, расход 3 л; литеральные `—` em-dash) skel==UA |
| 55 | 56 | 469912187 | Krupps C537TDGT Advance (380) фронтальная | `Посудомийна машина Krupps C537TDGT Advance (380) фронтальна` → `Посудомоечная машина Krupps C537TDGT Advance (380) фронтальная` | faithful RU body h2-заголовок (штампованные моечные и ополаскивающие коромысла Ø18 AISI 304, 30 кассет/час, цикл 2 мин, 585х600х815, 0.52+2.6+5.4=5.92 кВт, 380 В, тэнов без ё, preserve `&mdash;`) skel==UA |
| 56 | 57 | 1162070066 | Hendi 696040 ерш для мойки стаканов | `Йорж для миття склянок Hendi 696040` → `Ерш для мойки стаканов Hendi 696040` (без ё — c7 faithful) | faithful RU body (3 щетки нейлон, полипропилен, 4 ножки-присоски, 190x100x180/250/180) skel==UA |

### blknotrip (1)

| SKU | row | Артикул | Бренд+модель | Причина |
|---|---|---|---|---|
| 49 | 50 | 644933517 | Krupps K540E фронтальная | c35!=c36 whitespace-only diff (c35 имеет `\n\n` между блоками + `\t<li>` indent; c36 source — collapsed single-line); оба UA с одинаковым skel; c5/c36 переписаны RU faithful skel c35 (`\n\n` + `\t<li>`), c35 unchanged |

### blknochg (1)

| SKU | row | Артикул | Бренд+модель | Причина |
|---|---|---|---|---|
| 53 | 54 | 644908502 | SILANOS S021 ополаскивающее средство | c5==c7 genuine RU; c36 genuine RU; c35!=c36 skel-eq True; не трогаем |

### SKIP-НП (2)

| # | SKU | row | Артикул | Бренд | Название |
|---|---|---|---|---|---|
| #5 | 51 | 52 | 1162043196 | Apach | Посудомийка Apach AF400 DD фронтальна з дозатором миючого засобу |
| #6 | 52 | 53 | 1162046388 | Apach | Посудомийка Apach AF500 DIG DD з дозатором |


## Батч 8 (SKU 57-64, rows 58-65) — DONE

**Итог:** TRIP 4 / blknotrip 0 / blknochg 4 / SKIP-НП 0 / verify 390 PASS / 0 FAIL.

### blk триплет (4)

| SKU | row | Артикул | Бренд+модель | col5: UA→RU | col36 |
|---|---|---|---|---|---|
| 57 | 58 | 664883807 | Krupps EL981E ELITECH LINE для крупногабаритной посуды | `Посудомийна машина Krupps EL981E (серія ELITECH LINE) для габаритного посуду` → `Посудомоечная машина Krupps EL981E (серия ELITECH LINE) для габаритной посуды` | faithful RU 4 параграфа + 11-li (GN1/1, GN1/2, 600х400, 600х800, 575x645x850, тарелки 630, кастрюли 850, Termostop, дозатор 3 л/час, ополаскивателя 0,3 л/час; ELITECH+Acquatech+IKLOUD Wi-Fi; UNIKO дисплей; 6/10/15/30 кассет/час, циклы 120/240/260/540 сек, корзина 60х67х10 нерж.стали, держатель 18 делений, 820х775х1850, 7,4 кВт, 380 В, расход 2 л; литеральные `—` em-dash) skel==UA |
| 58 | 59 | 732424078 | ASBER GEX-H500 DD купольная | `Посудомийна машина ASBER GEX-H500 DD` (c5 source `Посудомийка купольна Asber GEX-H500 DD` — variant) → `Посудомоечная машина ASBER GEX-H500 DD` | faithful RU 2 параграфа + 16-li (купольного типа, 40 кассет/час, 400 мм, 90/180 сек, 500х500, бак 33 л, бойлер 7 л, загрузка 440, 2+1 контейнер-вставка, 630х750х1482, 11,25 кВт, 380 В) skel==UA |
| 60 | 61 | 1134521234 | Krupps C537DGT Advance фронтальная | `Посудомийна машина Krupps C537DGT Advance фронтальна` → `Посудомоечная машина Krupps C537DGT Advance фронтальная` | faithful RU h2-заголовок (тарелки 395, бокалы 310, 30 кассет/час, цикл 2 мин strong, 500х500, 585х610х815, preserve `&mdash;`, ТЭНа ванны 2,6 кВт / бойлера 2,5 / насоса 0,52 / номинальная 3,12 кВт, 220 В) skel==UA |
| 63 | 64 | 1200533520 | ASBER GE500DD фронтальная | `Посудомийна машина ASBER GE500DD фронтальна` → `Посудомоечная машина ASBER GE500DD фронтальная` | faithful RU 2 параграфа + 13-li (до 320 мм, цикл 120 сек, 500х500, бак 25 л, бойлер 7 л, 2+1 контейнер-вставка, 600х605х830, 3.4 кВт, 220 В) skel==UA |

### blknochg (4)

| SKU | row | Артикул | Бренд+модель | Причина |
|---|---|---|---|---|
| 59 | 60 | 823877211 | Empero EMP.BPR.002 полировщик бокалов | c5==c7 genuine RU; c36 genuine RU; c35!=c36 skel-eq True; не трогаем |
| 61 | 62 | 1157922214 | SILANOS VS P57-62N-D посудомоечная (котломоечная) | c5==c7 genuine RU; c36 genuine RU; c35!=c36 skel-eq False но dims match — текстовая редакция; не трогаем |
| 62 | 63 | 1164964525 | Apparatus (Stalgast) купольная | c5==c7 genuine RU; c36 genuine RU; c35!=c36 skel-eq True; не трогаем |
| 64 | 65 | 1312820859 | Empero EMP.500-380-F | c5==c7 genuine RU; c36 genuine RU; c35!=c36 skel-eq True; не трогаем |

### SKIP-НП (0)

В b8 нет brand-locked НП.


## Батч 9 (SKU 65-72, rows 66-73) — DONE

**Итог:** TRIP 0 / blknotrip 0 / blknochg 6 / SKIP-НП 2 / verify 414 PASS / 0 FAIL. **NO XLSX writes.**

### blknochg (6)

| SKU | row | Артикул | Бренд+модель | Причина |
|---|---|---|---|---|
| 65 | 66 | 1312822960 | Empero EMP.500-SDF (цифровой дисплей) | c5==c7; c36 genuine RU; c35!=c36 skel-eq True; не трогаем |
| 66 | 67 | 1312858248 | Empero EMP.TB.01 корзина для тарелок | c5==c7; c36 genuine RU; c35!=c36 skel-eq True; не трогаем |
| 67 | 68 | 1312874503 | Empero EMP.BB.01 корзина для стаканов | c5==c7; c36 genuine RU с лишней dim `500х500`; не трогаем |
| 68 | 69 | 1312875812 | Empero EMP.KC.01 корзина для столовых приборов | c5==c7; c36 genuine RU; c35!=c36 skel-eq False; не трогаем |
| 69 | 70 | 1500266298 | Krupps C432DGT Advance фронтальная | c5==c7 (c4 короткий `Krupps C432 фронтальна`); c36 genuine RU; c35!=c36 dims differ slightly (c36: `432` префикс, `470х535х710` vs c35 `470х555х710`); не трогаем |
| 72 | 73 | 1865347951 | Empero EMP.500-F помпа слива | c4 source typo `попа зливу`; c5==c7 правильно `помпа слива`; c36 genuine RU; c35!=c36 skel-eq True; не трогаем |

### SKIP-НП (2)

| # | SKU | row | Артикул | Бренд | Название |
|---|---|---|---|---|---|
| #7 | 70 | 71 | 1519641570 | TATRA | Посудомийна купольна машина TATRA TW.H50+DR+DD. |
| #8 | 71 | 72 | 1519648525 | APACH | Посудомийна (котломийна) машина APACH AK 901 |


## Батч 10 (SKU 73-74, rows 74-75) — DONE — ФИНАЛЬНЫЙ

**Итог:** TRIP 0 / blknotrip 0 / blknochg 2 / SKIP-НП 0 / verify 420 PASS / 0 FAIL. **NO XLSX writes.** **chunk-067 ЗАКРЫТ 74/74.**

### blknochg (2)

| SKU | row | Артикул | Бренд+модель | Причина |
|---|---|---|---|---|
| 73 | 74 | 1943677312 | Ozti OBY 50T PDT с помпой слива | c5==c7 genuine RU; c36 genuine RU; c35!=c36 skel-eq True; не трогаем |
| 74 | 75 | 2033010783 | Ozti OBМ 1080T PDT купольная (помпа слива) | c5==c7 genuine RU; c36 genuine RU; c35!=c36 skel-eq False; dims c35 лишний `5,` source variance; не трогаем |
