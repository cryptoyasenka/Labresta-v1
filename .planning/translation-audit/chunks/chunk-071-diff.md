# chunk-071 diff (W2, продолжение chunk-070)

**Status:** chunk-071 b1 DONE 8/83 (cum TRIP 8 / blknotrip 0 / blknochg 0 / blkfix 0 / SKIP-НП 0; 273 PASS / 0 FAIL) — next b2 (SKU 9-16, rows 10-17)
**Last updated:** chunk-071 b1 DONE 8/83

**Источник:** `.planning/translation-audit/chunks/chunk-071.xlsx` (83 SKU, rows 2..84, ART 500478925..1173086863).
**Фикс-таргет:** `.planning/translation-audit/chunks/chunk-071-fixed.xlsx` (gitignored).
**Бренды:** все 83 — **Hendi** (NORMAL, не SKIP-НП). 0 SKIP-НП.
**Категории товаров:** балончики для сифонов, газовые горелки крем-брюле, доски разделочные HACCP, тёрки, мандолины, воронки-дозаторы, термометры с зондом, точила.

## Workflow
- Batch=8 SKU; 2 commits/batch (C1 content + C2 marker); push после C2.
- TRIP=c5←c7 + c36 RU faithful; blknotrip=c5←c7 only; blknochg=без изменений; blkfix=c36 minor (Ё→Е и т.п.).
- Без Ё в c36; UA `&#39;` AND literal `'` → drop; «тэн»→«э».
- Source typos faithful в c5/title; structural typos preserved.
- chunk-NN.xlsx RO; modify chunk-NN-fixed.xlsx.

## b1 (SKU 1-8, rows 2-9) — 8/83

| # | SKU | row | ART | Brand+Model | Category | Изменения |
|---|-----|-----|-----|-------------|----------|-----------|
| 1 | 1 | 2 | 500478925 | Hendi 586907 балончик для эспумизатора | **TRIP** | c5←c7 «Баллончик для сифона HENDI 586907»; c36 ← RU 306 chars (HTML spans+br) 8 г N2O / 0,5 л / 50 шт. Literal `'` в «об'ємом» dropped. |
| 2 | 2 | 3 | 500484010 | Hendi 588215 балончик (24 шт.) | **TRIP** | c5←c7 «Баллончик для сифона HENDI 588215 (24 шт.)»; c36 ← RU 127 chars plain. Literal `'` в «об'ємом» dropped. |
| 3 | 3 | 4 | 623990170 | Hendi 198223 газовая горелка крем-брюле | **TRIP** | c5←c7 «Газовая горелка Hendi 198223 для крем брюле (фламбирования)»; c36 ← RU 236 chars (1 para + 4 li): многоразовая заправка / автоподжиг / без баллончика / с подставкой / Ø 115 мм × H 155 мм. |
| 4 | 4 | 5 | 659317970 | Hendi 825600 доска HACCP 600x400 белая | **TRIP** | c5←c7 «Доска разделочная Hendi 825600 HACCP 600x400 мм - белая»; c36 ← RU 1176 chars (1 para + 4 li + 7-row table HACCP цветокод + iframe youtube preserved verbatim). HDPE 500 / двусторонние / без желобков. Literal `'` в «м'ясо» drops. Source quirk «сира птах» → «сырая птица» (semantic faithful). |
| 5 | 5 | 6 | 873329344 | Hendi 222652 терка-мандолина ручная | **TRIP** | c5←c7 «ТЕРКА ДЛЯ ОВОЩЕЙ РУЧНАЯ - МАНДОЛИНА Hendi 222652»; c36 ← RU 345 chars (1 para + 5 li): 2 лезвия для ломтиков (1 гофрир.) + 3 для соломки (5/7/10 мм) / овощедержатель + ящик / нескольз. ножки / 395х195х200. |
| 6 | 6 | 7 | 873333560 | Hendi PROFI LINE 551806 воронка-дозатор | **TRIP** | c5←c7 «ВОРОНКА - ДОЗАТОР ДЛЯ СОУСОВ И КРЕМОВ Hendi PROFI LINE 551806»; c36 ← RU 478 chars (1 para + 7 li): нерж сталь / антискольз. полипропилен ручка / клапан / 1,5 л / 3 наконечника Ø 2/4/6 мм / штатив+лоток / 190х220. Literal `'` в «Об'єм» drops. |
| 7 | 7 | 8 | 873368628 | Hendi 222614 терка V-образная | **TRIP** | c5←c7 «ТЕРКА ДЛЯ ОВОЩЕЙ РУЧНАЯ - V–ОБРАЗНАЯ Hendi 222614»; c36 ← RU 582 chars — source mixed RU/UA (первые 6 li RU с Ё «чёрной», последние 3 li UA), переведено в чистый RU + de-Ё («чёрной»→«черной»). 5 лезвий-насадок / V-образн. главное / 6/9 мм брусочки / 1-9 мм ломтики / 130х335х75. |
| 8 | 8 | 9 | 873548120 | Hendi 271209 термометр цифровой с зондом | **TRIP** | c5←c7 «ТЕРМОМЕТР ЦИФРОВОЙ С ЗОНДОМ Hendi 271209»; c36 ← RU 520 chars (1 para + 10 li): зонд нерж 65 мм / -40..+200°C / °C/°F / 0,1 C / HOLD / автовыкл / защитный колпачок / батарейка в наборе / 20х150. |

**Итого b1:** TRIP 8 + blknotrip 0 + blknochg 0 + blkfix 0 + SKIP-НП 0. Verify **273 PASS / 0 FAIL**.
**Cum после b1:** TRIP 8 + blknotrip 0 + blknochg 0 + blkfix 0 + SKIP-НП 0 = **8/83**. UNPROC = 75 (rows 10-84).
