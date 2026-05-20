# chunk-067 — diff (W2)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-067 (74 SKU, rows 2..75; ART 2045345276 … 2033010783)
**Apply key:** `Артикул` (col1, scoped per row)
**Worker:** W2 (параллельный, диапазон chunk-055 … chunk-085); продолжение chunk-066
**Status:** b1 DONE 8/74 (TRIP 5 / blknotrip 0 / blknochg 3 / SKIP-НП 0; b2 предстоит; b1..b9 по 8 SKU + b10=SKU73-74 2 SKU)

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
