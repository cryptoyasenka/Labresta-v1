# chunk-063 — manual review (W2)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-063 (88 SKU)
**Apply key:** `Артикул` (col1, scoped per row)
**Status:** b1 DONE 8/88 (b2..b11 remain; batch=8)
**Worker:** W2 (параллельный, диапазон chunk-055 … chunk-085); продолжение chunk-062
**Last updated:** chunk-063 b1 (W2)

Эталон формата: chunk-019-MANUAL-REVIEW.md / chunk-062-MANUAL-REVIEW.md. Категории: blk триплет / blknotrip / blknochg / SKIP-НП. Кумул. OQ закрыты (ОВ-1..ОВ-4 remediation c71341f).

## SKIP-НП (НП-эксклюзивные бренды, forward-only, тело из фида НП позже)

| # | SKU | Артикул | Бренд | Название (UA) | Примечание |
|---|---|---|---|---|---|
| ✓ b1 | 1 | 2059513121 | HURAKAN | Теплова вітрина Hurakan HKN WD-165L | подтверждён SKIP-НП; fixed row2 НЕ тронут (тело из фида НП позже) |
| ✓ b1 | 3 | 2176575775 | HURAKAN | Вітрина теплова HURAKAN HKN WD-160L | подтверждён SKIP-НП; fixed row4 НЕ тронут (тело из фида НП позже) |
| _(prelim)_ | 54 | 1148895671 | HURAKAN | Супниця HURAKAN HKN-FWP | подтвердить в b7 |

## Открытые вопросы chunk-063

_(нумерация отдельная, начинается с #1; пока нет)_

---

## b1 (SKU 1-8) — DONE 8/88

**Категории:** blk триплет 4 (SKU 4,5,6,7) · blknochg 2 (SKU 2,8) · SKIP-НП 2 (SKU 1,3 HURAKAN).

| SKU | row | ART | Бренд | Категория | Действие |
|---|---|---|---|---|---|
| 1 | 2 | 2059513121 | HURAKAN | SKIP-НП | fixed row2 НЕ тронут (тело из фида НП позже) |
| 2 | 3 | 2110267107 | GoodFood | blknochg | RU уже корректен: c5==c7 genuine RU «Витрина тепловая GoodFood WS3SS», c36 переведён; fixed НЕ тронут |
| 3 | 4 | 2176575775 | HURAKAN | SKIP-НП | fixed row4 НЕ тронут (тело из фида НП позже) |
| 4 | 5 | 2191892433 | Sirman | blk триплет | col5←c7 «Витрина тепловая Sirman CUBE P2 HOT»; col36← faithful RU (skel==UA c35) |
| 5 | 6 | 2301763319 | Frosty | blk триплет | col5←c7 «Витрина тепловая Frosty SWS-3P»; col36← faithful RU |
| 6 | 7 | 2553918281 | Gooder | blk триплет | col5←c7 «Тепловая витрина Gooder XCR-50L Cube»; col36← faithful RU |
| 7 | 8 | 2553925755 | Gooder | blk триплет | col5←c7 «Тепловая витрина Gooder XCR-45L»; col36← faithful RU |
| 8 | 9 | 424917689 | GGM Gastro | blknochg | RU уже корректен: c5==c7 genuine RU «Тепловая витрина GGM Gastro WHVJ3», c36 переведён; fixed НЕ тронут |

**Verify:** 136 PASS / 0 FAIL — 88 ART (apply key) unchanged + 4×{col5==src c7, col36 skeleton==c35, UA-clean, без ё, dims verbatim incl. кир. х, col4/6/7/35 untouched} + SKU 1/2/3/8 col5/col36==src.

**Глоссарий b1 (новые UA→RU):** круасанів→круассанов · оргскла→оргстекла · екструдованого алюмінію→экструдированного алюминия · дверцят→дверцы · висихання продуктів→высыхания продуктов · піддон для крихт→поддон для крошек · освітлення немає→освещение отсутствует · пофарбована сталь→окрашенная сталь. Reuse: вітрина теплова→витрина тепловая · наливне зволоження→наливное увлажнение · тени з термостатом→тэны с термостатом · напруга→напряжение · потужність→мощность.

**Открытых вопросов b1:** нет.

<!-- Сводки по батчам b2..b11 ниже. -->
