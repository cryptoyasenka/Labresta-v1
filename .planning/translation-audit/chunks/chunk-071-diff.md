# chunk-071 diff (W2, продолжение chunk-070)

**Status:** chunk-071 b3 DONE 24/83 (cum TRIP 21 / blknotrip 0 / blknochg 3 / blkfix 0 / SKIP-НП 0; 312 PASS / 0 FAIL) — next b4 (SKU 25-32, rows 26-33)
**Last updated:** chunk-071 b3 DONE 24/83

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

## b2 (SKU 9-16, rows 10-17) — 16/83

| # | SKU | row | ART | Brand+Model | Category | Изменения |
|---|-----|-----|-----|-------------|----------|-----------|
| 1 | 9 | 10 | 873565142 | Hendi 271162 термометр цифр с зондом 120 мм | **TRIP** | c5←c7 «ТЕРМОМЕТР ЦИФРОВОЙ С ЗОНДОМ Hendi 271162»; c36 ← RU 604 chars (1 para + 9 li). **Source-typo preserved** «Терометр» (missing «м»). Source gender-mismatch «цифрової з зондом» → standard RU «цифровой с зондом» (semantic faithful). Зонд 120 мм нерж, -50..+300°C, lock mode, автовыкл 10 мин. |
| 2 | 10 | 11 | 873572737 | Hendi 224403 точило электрическое | **TRIP** | c5←c7 «ТОЧИЛО ЭЛЕКТРИЧЕСКОЕ ДЛЯ ЗАТОЧКИ НОЖЕЙ Hendi 224403»; c36 ← RU 231 chars (1 para + 3 li): быстрая заточка / удобная замена дисков / рыба-мясо-овощи-фрукты / 310х110х110. Literal `'` в «м'яса» drop. |
| 3 | 11 | 12 | 873573291 | Hendi 820612 точило для ножей (3 функции) | **TRIP** | c5←c7 «ТОЧИЛО ДЛЯ НОЖЕЙ Hendi 820612»; c36 ← RU 530 chars (ul+ol+ul mixed structure). 3 функции (COARSE/FINE/CERAMIC) для всех типов ножей включая керамические. UA tail «Не використовувати для заточування зубчастих лез» → RU. |
| 4 | 12 | 13 | 886827914 | Hendi 825617 доска HACCP красная | **TRIP** | c5←c7 «Доска разделочная Hendi 825617 HACCP 600x400 мм - красная»; c36 ← RU 979 chars (1 para + 4 li + 7-row HACCP table). Trailing 2 empty `<p> </p>` preserved (no iframe в этом SKU). |
| 5 | 13 | 14 | 886828528 | Hendi 825631 доска HACCP зелёная | **TRIP** | c5←c7 «Доска разделочная Hendi 825631 HACCP 600x400 мм - зелёная» (Ё в c7 preserved — Ё запрещён только в c36). c36 ← RU 1117 chars. **Structural diff:** table в этом SKU БЕЗ header row (preserved faithful). Leading space `<p> Дошка` preserved. + iframe youtube. |
| 6 | 14 | 15 | 886828693 | Hendi 825648 доска HACCP коричневая | **TRIP** | c5←c7 «Доска разделочная Hendi 825648 (600х400 мм) коричневая»; c36 ← RU 1178 chars. **Source-typo preserved:** missing «виготовлена/изготовлена» word — «Дошка обробна HACCP 600x400 мм - коричнева Hendi 825648 з поліетилену HDPE 500» → «Доска разделочная HACCP 600x400 мм - коричневая Hendi 825648 из полиэтилена HDPE 500» (без слова «изготовлена»). + iframe. |
| 7 | 15 | 16 | 886828999 | Hendi 825655 доска HACCP жёлтая | **TRIP** | c5←c7 «Доска разделочная Hendi 825655 HACCP 600x400 мм - жёлтая» (Ё preserved); c36 ← RU 1176 chars. **Source-typo preserved:** «825655изготовлена» (no space, RU word в UA-тексте) — faithful. + iframe. |
| 8 | 16 | 17 | 886829518 | Hendi 825624 доска HACCP синяя | **TRIP** | c5←c7 «Доска разделочная Hendi 825624 (600х400 мм) синяя»; c36 ← RU 1187 chars. **Structural quirk:** first sentence в `<h2>` а не `<p>` (preserved faithful). + iframe. |

**Итого b2:** TRIP 8 + blknotrip 0 + blknochg 0 + blkfix 0 + SKIP-НП 0. Verify **297 PASS / 0 FAIL**.
**Cum после b2:** TRIP 16 + blknotrip 0 + blknochg 0 + blkfix 0 + SKIP-НП 0 = **16/83**. UNPROC = 67 (rows 18-84).

## b3 (SKU 17-24, rows 18-25) — 24/83

| # | SKU | row | ART | Brand+Model | Category | Изменения |
|---|-----|-----|-----|-------------|----------|-----------|
| 1 | 17 | 18 | 908848545 | Hendi 199039 баллончики с газом (4 шт) | **TRIP** | c5←c7 «Баллончики с газом (4 шт) Hendi 199039 для газовой горелки»; c36 ← RU 142 chars (2 para): для горелок арт.198230/198216 + 4 шт в наборе. |
| 2 | 18 | 19 | 1144395391 | Hendi 222676 терка V-обр ручная | **TRIP** | c5←c7 «Терка для овощей Hendi 222676 РУЧНАЯ - V–образная»; c36 ← RU 507 chars (1 para + empty + 2 li ul). **Source-typo preserved «222676изготовлена»** (no space, RU word). V-обр главное + волнистое второе / 2 доп лезвия жюльен 6+9 мм для картофеля-фри / 530×165×203. |
| 3 | 19 | 20 | 1156818682 | Hendi 975862 сифон Kurt Scheller голубой | **blknochg** | Source c5/c36 already RU («Сифон для сливок ... голубой»), fixed cells unchanged. |
| 4 | 20 | 21 | 1156819719 | Hendi 975855 сифон Kurt Scheller желтый | **blknochg** | Source c5/c36 already RU («Сифон для сливок ... желтый»), fixed cells unchanged. |
| 5 | 21 | 22 | 1156821932 | Hendi 975879 сифон Kurt Scheller зеленый | **blknochg** | Source c5/c36 already RU («Сифон для сливок ... зеленый»), fixed cells unchanged. |
| 6 | 22 | 23 | 1156823550 | Hendi 975886 сифон Kurt Scheller фиолетовый | **TRIP** | c5←c7 «Сифон для сливок Hendi 975886 Kurt Scheller Edition фиолетовый»; c36 ← RU 469 chars (1 para + 6 li): 0,5 л / алюминий / 3 насадки полипропилен + щетка / N₂O preserved / для горячих соусов нельзя / не моется в ПММ. Literal `'` в «Об'єм» drop. |
| 7 | 23 | 24 | 1156829173 | Hendi 588369 Kitchen Line 0,5 л | **TRIP** | c5←c7 «Сифон для сливок Hendi 588369 (0,5 л)»; c36 ← RU 496 chars (1 para + 8 li): Ø 80 / H 260 / N₂O preserved / «не входят в комплект» (source mixed RU «не входят» + UA «до комплекту» normalized). `&#39;` в «Об&#39;єм» drop. |
| 8 | 24 | 25 | 1156830998 | Hendi 588376 Kitchen Line 1,0 л | **TRIP** | c5←c7 «Сифон для сливок Hendi 588376 Kitchen Line 1,0 л»; c36 ← RU 513 chars. **Source-typos preserved:** (1) «Kitchen Line 0,25 л» в первом предложении (модель 1,0 л!) — копипаст-typo, (2) «Фіолетовий колір» → «Фиолетовый цвет» в синем/жёлтом/etc SKU — копипаст, (3) lowercase «висота»→«высота» preserved. Ø 95 / H 320. |

**Итого b3:** TRIP 5 + blknotrip 0 + blknochg 3 + blkfix 0 + SKIP-НП 0. Verify **312 PASS / 0 FAIL**.
**Cum после b3:** TRIP 21 + blknotrip 0 + blknochg 3 + blkfix 0 + SKIP-НП 0 = **24/83**. UNPROC = 59 (rows 26-84).
