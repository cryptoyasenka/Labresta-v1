# chunk-063 — manual review (W2)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-063 (88 SKU)
**Apply key:** `Артикул` (col1, scoped per row)
**Status:** b3 DONE 24/88 (b4..b11 remain; batch=8)
**Worker:** W2 (параллельный, диапазон chunk-055 … chunk-085); продолжение chunk-062
**Last updated:** chunk-063 b3 (W2)

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

## b2 (SKU 9-16) — DONE 16/88

**Категории:** blk триплет 1 (SKU 10) · blknochg 7 (SKU 9,11,12,13,14,15,16) · SKIP-НП 0.

| SKU | row | ART | Бренд | Категория | Действие |
|---|---|---|---|---|---|
| 9 | 10 | 424917690 | GGM Gastro | blknochg | c5==c7 genuine RU, c36 переведён; fixed НЕ тронут. _Замечание: в genuine c36 опечатка источника «поддрежания» (не наша правка, blknochg не трогаем) — для merge-ревью Yana._ |
| 10 | 11 | 1131731712 | Hendi | blk триплет | col5←c7 «Тепловая витрина Hendi 233962»; col36← faithful RU (skel==UA c35; `°C` литералы и `4хGN 1/2`/`650х467х630`/`0,56 кВт` verbatim) |
| 11 | 12 | 424917691 | GGM | blknochg | c5==c7 genuine RU, c36 переведён; fixed НЕ тронут |
| 12 | 13 | 2538738615 | SARO | blknochg | c5==c7 genuine RU, c36 переведён; fixed НЕ тронут |
| 13 | 14 | 2538743093 | SARO | blknochg | c5==c7 genuine RU, c36 переведён; fixed НЕ тронут |
| 14 | 15 | 2210058270 | GoodFood | blknochg | c5==c7 genuine RU, c36 переведён; fixed НЕ тронут |
| 15 | 16 | 2301733929 | Frosty | blknochg | c5==c7 genuine RU, c36 переведён; fixed НЕ тронут |
| 16 | 17 | 961887244 | GoodFood | blknochg | c5==c7 genuine RU, c36 переведён; fixed НЕ тронут |

**Verify:** 112 PASS / 0 FAIL — 88 ART (apply key) unchanged + SKU 10 {col5==src c7, col36 skeleton==c35, UA-clean, без ё, dims verbatim, col4/6/7/35 untouched} + 7 blknochg rows col5/col36==src.

**Глоссарий b2 (новые UA→RU):** бічні сторони→боковые стороны · загартоване скло→закаленное стекло · зігнута скляна двері→гнутая стеклянная дверь · дзеркальна панель→зеркальная панель · кварцовий нагрівач→кварцевый нагреватель. Reuse: вітрина теплова→витрина тепловая · нержавіюча сталь→нержавеющая сталь.

**Открытых вопросов b2:** нет (опечатка «поддрежания» в SKU 9 — пред-существующий дефект источника в genuine RU, blknochg не правим; зафиксировано как замечание для Yana, не OQ).

## b3 (SKU 17-24) — DONE 24/88

**Категории:** blk триплет 4 (SKU 17,20,21,23) · blknochg 4 (SKU 18,19,22,24) · SKIP-НП 0.

| SKU | row | ART | Бренд | Категория | Действие |
|---|---|---|---|---|---|
| 17 | 18 | 1043369426 | EWT INOX | blk триплет | col5←c7 «Витрина тепловая EWT INOX SDC5»; col36← faithful RU (skel==UA c35) |
| 18 | 19 | 2210044738 | GoodFood | blknochg | c5==c7 genuine RU, c36 переведён; fixed НЕ тронут |
| 19 | 20 | 883765440 | FROSTY | blknochg | c5==c7 genuine RU (Супник электрический…), c36 переведён; fixed НЕ тронут |
| 20 | 21 | 475085014 | Bartscher | blk триплет | col5←c7 «Электросупница 9 л Bartscher 100061»; col36← faithful RU (литералы `°C`/`°С` verbatim) |
| 21 | 22 | 475113512 | FROSTY | blk триплет | col5←c7 «Электросупница 10 л FROSTY SB-6000S (супник)»; col36← faithful RU |
| 22 | 23 | 476419919 | GoodFood | blknochg | c5==c7 genuine RU, c36 переведён; fixed НЕ тронут |
| 23 | 24 | 489952968 | AIRHOT | blk триплет | col5←c7 «Мармит AIRHOT BM-11»; col36← faithful RU (`GN 1/3 — 3 шт.` пунктуация verbatim) |
| 24 | 25 | 593853560 | GoodFood | blknochg | c5==c7 genuine RU, c36 переведён; fixed НЕ тронут. _Замечание: в genuine c36 опечатка источника «укоплектоварн стекляной» (не наша правка, blknochg) — для merge-ревью Yana._ |

**Verify:** 136 PASS / 0 FAIL — 88 ART (apply key) unchanged + 4×{col5==src c7, col36 skeleton==c35, UA-clean, без ё, dims verbatim incl. кир. х, col4/6/7/35 untouched} + 4 blknochg rows col5/col36==src.

**Глоссарий b3 (новые UA→RU):** настільна→настольная · LED-підсвітка→LED-подсветка · електросупниця→электросупница · вставка-каструля→вставка-кастрюля · відкидна кришка→откидная крышка · марміт→мармит. Reuse: вітрина теплова→витрина тепловая · нержавіюча сталь→нержавеющая сталь · потужність→мощность.

**Открытых вопросов b3:** нет (опечатка «укоплектоварн стекляной» в SKU 24 — пред-существующий дефект источника в genuine RU, blknochg не правим; замечание для Yana, не OQ).

<!-- Сводки по батчам b4..b11 ниже. -->
