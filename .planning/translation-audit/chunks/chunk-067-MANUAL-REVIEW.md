# chunk-067 — manual review (W2)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-067 (74 SKU, rows 2..75; ART 2045345276 … 2033010783)
**Apply key:** `Артикул` (col1, scoped per row)
**Status:** b1 DONE 8/74 (TRIP 5 / blknotrip 0 / blknochg 3 / SKIP-НП 0 / OQ 0; b2 предстоит; batch=8 b1..b9 по 8 + b10=SKU73-74 2 SKU = 74)
**Worker:** W2 (параллельный, диапазон chunk-055 … chunk-085); продолжение chunk-066
**Last updated:** chunk-067 b1 (W2)

Эталон формата: chunk-019-MANUAL-REVIEW.md / chunk-066-MANUAL-REVIEW.md. Категории: blk триплет / blknotrip / blknochg / SKIP-НП.

## SKIP-НП prelim (НП-эксклюзивные бренды, forward-only, тело из фида НП позже)

| # | SKU | Артикул | Бренд | Название (UA) | Примечание |
|---|---|---|---|---|---|
| prelim | 41 | 893760283 | FAGOR | Посудомийна машина FAGOR ADVANCE AD 505 BDD | FAGOR — НП-эксклюзив, fixed row42 НЕ тронут; b6 confirm |
| prelim | 42 | 1282877474 | Fagor | Посудомийна машина Fagor FIR-30-DD фронтальна | Fagor — НП-эксклюзив, fixed row43 НЕ тронут; b6 confirm |
| prelim | 43 | 1282884918 | Fagor | Посудомийна машина Fagor FIR-80-DD купольна | Fagor — НП-эксклюзив, fixed row44 НЕ тронут; b6 confirm |
| prelim | 45 | 2331547054 | TATRA | Посудомийна машина TATRA TW.F50+DR+DD | TATRA — НП-эксклюзив, fixed row46 НЕ тронут; b6 confirm |
| prelim | 51 | 525262231 | Apach | Посудомийна машина Apach AF400 DD | Apach — НП-эксклюзив, fixed row52 НЕ тронут; b7 confirm |
| prelim | 52 | 525269150 | Apach | Посудомийна машина Apach AF500 DIG DD | Apach — НП-эксклюзив, fixed row53 НЕ тронут; b7 confirm |
| prelim | 70 | 1519641570 | TATRA | Посудомийна купольна машина TATRA TW.H50+DR+DD. | TATRA — НП-эксклюзив, fixed row71 НЕ тронут; b9 confirm |
| prelim | 71 | 1519648525 | APACH | Посудомийна (котломийна) машина APACH AK 901 | APACH — НП-эксклюзив, fixed row72 НЕ тронут; b9 confirm |

Brand-list scan: HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA. По prelim-скану 3 Fagor/FAGOR + 2 Apach/APACH + 2 TATRA + 1 FAGOR = 8 prelim в b6/b7/b9. Остальные SKU (Adler / Airhot / Asber / ATA / Bartscher / Frosty / GoodFood и пр.) — обрабатываются обычно.

## Открытые вопросы chunk-067

_(нумерация отдельная, начинается с #1; пока нет)_

---

<!-- Сводки по батчам ниже (b1..b10 будут добавлены при выполнении каждого батча). -->


## Батч 1 (SKU 1-8, rows 2-9) — DONE

**Итог:** TRIP 5 / blknotrip 0 / blknochg 3 / SKIP-НП 0 / OQ 0 / verify 118 PASS / 0 FAIL / cum 8/74.

### blk триплет (TRIP) — 5 SKU

- **SKU 4 row 5 ART 913655974 — Прес ручний для гамбургерів Frosty HF-100**
  - col5 UA→genuine RU: `Прес ручний для гамбургерів Frosty HF-100` → `Пресс ручной для гамбургеров Frosty HF-100` (как c7)
  - col36 faithful RU: Пресс ручной для гамбургеров → формирование котлет; корпус из алюминия с анодированием; детали, соприкасающиеся с мясом — нержавеющая сталь; диаметр гамбургера 100мм; в комплекте 1 упаковка пергаментных прокладок (500 штук); габариты 220х300х280 мм. skel==UA, dims [100,1,500,220х300х280] match.
- **SKU 5 row 6 ART 913679416 — Прес ручний для гамбургерів Frosty HF-130**
  - col5 UA→genuine RU: → `Пресс ручной для гамбургеров Frosty HF-130`
  - col36 faithful RU: то же, диаметр 130 мм, габариты 320х250х300 мм. skel==UA, dims [130,500,320х250х300] match.
- **SKU 6 row 7 ART 1267124747 — Прес для гамбургерів Fimar Easy Line HF100**
  - col5 UA→genuine RU: → `Пресс для гамбургеров Fimar Easy Line HF100`
  - col36 faithful RU: Пресс ручной для гамбургеров Fimar Easy Line HF100; корпус из алюминия с анодированием; детали из нержавеющей стали; диаметр 100 мм; габариты 320х250х300 мм. skel==UA, dims [100,100,320х250х300] match.
- **SKU 7 row 8 ART 2044637169 — Прес для гамбургерів Frosty HM-100**
  - col5 UA→genuine RU: → `Пресс для гамбургеров Frosty HM-100`
  - col36 faithful RU: Пресс для гамбургеров — формирование котлет; размер гамбургеров &Oslash; 100 мм; части, контактирующие с мясом: нержавеющая сталь; размеры (Д*Ш*В): 220мм x 300мм x 280мм; в комплекте: набор пергаментных прокладок; материал корпуса: анодированный алюминий. skel==UA, dims [100,220,300,280] match. `&Oslash;` entity preserved verbatim.
- **SKU 8 row 9 ART 2044641303 — Прес для гамбургерів Frosty HM-130**
  - col5 UA→genuine RU: → `Пресс для гамбургеров Frosty HM-130`
  - col36 faithful RU: то же, &Oslash; 130 мм, размеры 320мм x 250мм x 300мм. skel==UA, dims [130,320,250,300] match.

### blknochg — 3 SKU (c5/c35/c36 НЕ тронуты; genuine RU в источнике)

- SKU 1 row 2 ART 2045345276 — GoodFood CR206 гриль для кур (c5==c7 `Гриль для кур GoodFood CR206`; c36 genuine RU; UA-mark False)
- SKU 2 row 3 ART 557515809 — GoodFood HF100 пресс ручной для гамбургеров (c5==c7 `Пресс ручний для гамбургеров GoodFood HF100` — источник live, не трогаем; c36 genuine RU)
- SKU 3 row 4 ART 775948663 — GoodFood HF130 пресс ручной для гамбургеров (c5==c7 `Пресс ручний для гамбургеров GoodFood HF130` — источник live, не трогаем; c36 genuine RU)

### SKIP-НП — 0 SKU

(prelim 8 на b6/b7/b9; в b1 НП брендов нет.)

### Открытые вопросы b1

Нет.
