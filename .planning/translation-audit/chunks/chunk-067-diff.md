# chunk-067 — diff (W2)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-067 (74 SKU, rows 2..75; ART 2045345276 … 2033010783)
**Apply key:** `Артикул` (col1, scoped per row)
**Worker:** W2 (параллельный, диапазон chunk-055 … chunk-085); продолжение chunk-066
**Status:** b4 DONE 32/74 (cum: TRIP 17 / blknotrip 0 / blknochg 15 / SKIP-НП 0; b5 предстоит; b1..b9 по 8 SKU + b10=SKU73-74 2 SKU)

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
