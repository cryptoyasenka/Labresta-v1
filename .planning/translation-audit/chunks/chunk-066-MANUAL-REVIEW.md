# chunk-066 — manual review (W2)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-066 (90 SKU, rows 2..91; ART 2496038149 … 2153078504)
**Apply key:** `Артикул` (col1, scoped per row)
**Status:** b1 DONE 8/90 (b2 предстоит; batch=8 b1..b11 по 8 + b12=SKU89-90 2 SKU = 90)
**Worker:** W2 (параллельный, диапазон chunk-055 … chunk-085); продолжение chunk-065
**Last updated:** chunk-066 b1 (W2)

Эталон формата: chunk-019-MANUAL-REVIEW.md / chunk-065-MANUAL-REVIEW.md. Категории: blk триплет / blknotrip / blknochg / SKIP-НП.

## SKIP-НП prelim (НП-эксклюзивные бренды, forward-only, тело из фида НП позже)

| # | SKU | Артикул | Бренд | Название (UA) | Примечание |
|---|---|---|---|---|---|
| 1 | 6 | 2784069485 | HURAKAN | ВАФЕЛЬНИЦЯ HURAKAN HKN-GES300 NUT | HURAKAN — НП-эксклюзив, fixed row7 НЕ тронут (тело из фида НП позже); b1 confirmed |
| prelim | 36 | (row 37) | Hurakan | Млинниця Hurakan HKN-CSE400P одинарна | HURAKAN — НП-эксклюзив, fixed row37 НЕ тронут; b5 confirm |
| prelim | 47 | (row 48) | Hurakan | Апарат для приготування солодкої вати Hurakan HKN-C1 | HURAKAN — НП-эксклюзив, fixed row48 НЕ тронут; b6 confirm |
| prelim | 57 | (row 58) | Hurakan | Апарат для приготування попкорну Hurakan HKN-PCORN | HURAKAN — НП-эксклюзив, fixed row58 НЕ тронут; b8 confirm |
| prelim | 67 | (row 68) | TATRA | Гриль для шаурми TATRA TDM E 4B | TATRA — НП-эксклюзив, fixed row68 НЕ тронут; b9 confirm |

Brand-list scan: HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA. По prelim-скану 4 HURAKAN + 1 TATRA. Остальные SKU (Roller Grill / Frosty / GoodFood / Hendi / Bartscher / SARO / EWT / AIRHOT / SILVER / FROSTY / PIMAK / CB и пр.) — обрабатываются обычно.

## Открытые вопросы chunk-066

_(нумерация отдельная, начинается с #1; пока нет)_

---

<!-- Сводка по батчу b1 ниже. -->

## b1 — SKU 1-8 (rows 2-9)

**Verify:** REGR 0 + ART 90 + TRIP 5 + BLKNOCHG 2 + SKIP-НП 1 = 98 PASS / 0 FAIL.

### blk триплет 5

| SKU | row | ART | Название | Действие |
|---|---|---|---|---|
| 2 | 3 | 2519380945 | Вафельниця Frosty WBS-6S (корн-доги / начинка) | c5←c7 genuine RU «Вафельница Frosty WBS-6S»; c36 ← faithful RU тело (skel==UA, dims 14×, &deg; ×2, x ×2 Lat / х ×6 Cyr); source artifact «WBS- 6S» (пробел после дефиса) preserved |
| 3 | 4 | 2519399322 | Вафельниця Frosty WBS-21W (кондитерські горішки) | c5←c7 genuine RU «Вафельница Frosty WBS-21W»; c36 ← faithful RU тело (skel==UA, dims 14×, &deg; ×2, x ×2 Lat / х ×8 Cyr) |
| 5 | 6 | 2519442607 | Вафельниця Frosty WBS-1UR (бургер UFO, закритий сендвіч) | c5←c7 genuine RU «Вафельница Frosty WBS-1UR»; c36 ← faithful RU тело (skel==UA, dims 15×, &deg; ×2, x ×2 Lat / х ×6 Cyr) |
| 7 | 8 | 630863408 | Вафельниця EWT INOX TRWB01 для тонких вафель | c5←c7 genuine RU «Вафельница EWT INOX TRWB01 для тонких вафель»; c36 ← faithful RU тело (skel==UA, dims 6×, ° U+00B0 ×1, х Cyr ×8); source typo «Термоература» → нормализовано в RU «Температура» (опечатка явная, не атрибут товара) |
| 8 | 9 | 823909747 | Вафельниця Hendi 212127 для бельгійських вафель (об'ємних) | c5←c7 genuine RU «Вафельница Hendi 212127 для бельгийских вафель»; c36 ← faithful RU тело (skel==UA, dims 7×, × U+00D7 mult ×2, х Cyr ×6); ASCII apos `'` ×2 в «об'ємних/п'ять» strip→ «объемных/пять» (ё avoided) |

### blknotrip 0
_(нет)_

### blknochg 2

| SKU | row | ART | Название | Замечание |
|---|---|---|---|---|
| 1 | 2 | 2496038149 | Вафельница Roller Grill GES 80 | c5==c7 genuine RU (Latin brand+model); c35!=c36 (fixed source: 928/949) — fixed строка НЕ тронута (соблюдаем blknochg); soft-note для merge-ревью: c36 source длиннее на 21 символ |
| 4 | 5 | 2519422914 | Вафельниця Frosty WBS-1UH | c5==c7 genuine RU «Вафельница Frosty WBS-1UH»; c35!=c36 (563/568) — fixed строка НЕ тронута; soft-note: source c35 lead «Вафельница Frosty WBS-21W використовується для виготовлення бургера UFO» при SKU=WBS-1UH — copy-paste артефакт из WBS-21W, WBS-1UH = UFO Burger вариант (body про UFO бургер, как SKU5 WBS-1UR), для merge-ревью |

### SKIP-НП 1
SKU6 r7 ART 2784069485 HURAKAN HKN-GES300 NUT (горішниця, для половинок горішків з згущеним молоком) — fixed row 7 НЕ тронут, тело из фида НП позже. Promoted prelim → confirmed #1 (см. SKIP-НП таблицу выше).

