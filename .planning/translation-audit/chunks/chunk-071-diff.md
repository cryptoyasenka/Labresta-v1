# chunk-071 diff (W2, продолжение chunk-070)

**Status:** chunk-071 b10 DONE 80/83 (cum TRIP 76 / blknotrip 0 / blknochg 4 / blkfix 0 / SKIP-НП 0; 477 PASS / 0 FAIL) — next b11 финал (SKU 81-83, rows 82-84)
**Last updated:** chunk-071 b10 DONE 80/83

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

## b4 (SKU 25-32, rows 26-33) — 32/83

| # | SKU | row | ART | Brand+Model | Category | Изменения |
|---|-----|-----|-----|-------------|----------|-----------|
| 1 | 25 | 26 | 1157445613 | Hendi 199008 баллончики 0,2 л | **TRIP** | c5←c7; c36 RU 121 chars. «В наборе различные насадки». |
| 2 | 26 | 27 | 1157446283 | Hendi 199046 баллончики 4×0,2 л | **TRIP** | c5←c7; c36 RU 158 chars. Literal `'` в «Об'єм» drop. |
| 3 | 27 | 28 | 1157446826 | Hendi 198209 газовая горелка крем-брюле | **TRIP** | c5←c7; c36 RU 793 chars (`<h2>` preserved structural; 8 li + iframe fIJhmL59SPY). Literal `'` x3 drops («полум'я» x2 + «п'єзоелектричний»). Любой угол / пьезорозжиг / алюм ручка / регулируемое пламя / 145x190. |
| 4 | 28 | 29 | 1157555952 | Hendi 589106 набор игл-насадок Profi Line | **TRIP** | c5←c7; c36 RU 369 chars: 4 наконечника нерж (2 длинных ø3/ø5 + 2 коротких ø3/ø5). «травлення» (etching) preserved. Source-typo «збиті вершки» → RU «взбитых сливок». |
| 5 | 29 | 30 | 1157566957 | Hendi 589205 запчасти Profi Line | **TRIP** | c5←c7; c36 RU 462 chars (1 para + 8 li). **Source-typo preserved «588024 - емкость 0,1 л»** (модель 1,0!). Прокладка/адаптер сопла/плоская насадка/прямое сопло/держатель картриджа/клапан/щетка/«тюльпановой». |
| 6 | 30 | 31 | 1157577157 | Hendi 588208 баллончик (10 шт) | **TRIP** | c5←c7; c36 RU 344 chars (HTML spans+br). N₂O preserved. «Liss, Kidde, ISI i Kayser» (`i` Latin in UA) → «Liss, Kidde, ISI и Kayser». Empty `<span>` at start preserved. |
| 7 | 31 | 32 | 1157580753 | Hendi 589007 запчасти Kitchen Line | **TRIP** | c5←c7; c36 RU 482 chars. Близнец r30 структурно (8 li same). Для сифонов Kitchen Line 588369/588376. |
| 8 | 32 | 33 | 1157947758 | Hendi 271346 термометр для выпечки с зондом+таймером | **TRIP** | c5←c7; c36 RU 574 chars (1 para + 9 li). Таймер с обратным отсчетом + звук сигнал / 0..+300°C / 0,1°C / lock mode / MIN/MAX / зонд печной нерж / 65×70×17. |

**Итого b4:** TRIP 8 + blknotrip 0 + blknochg 0 + blkfix 0 + SKIP-НП 0. Verify **336 PASS / 0 FAIL**.
**Cum после b4:** TRIP 29 + blknotrip 0 + blknochg 3 + blkfix 0 + SKIP-НП 0 = **32/83**. UNPROC = 51 (rows 34-84).

## b5 (SKU 33-40, rows 34-41) — 40/83

| # | SKU | row | ART | Brand+Model | Category | Изменения |
|---|-----|-----|-----|-------------|----------|-----------|
| 1 | 33 | 34 | 1157950566 | Hendi 582015 кухонный таймер аналоговый Ø80 мм | **TRIP** | c5←c7; c36 RU 325 chars (5 li-dash + 1 li-Ø). UA-typo «расстояни» (truncated) → RU faithful «расстояния». «Червона лінія» → «Красная линия». |
| 2 | 34 | 35 | 1157954358 | Hendi 271339 термометр для стейков (4 шт в блистере) | **TRIP** | c5←c7; c36 RU 162 chars. «rare medium well» Latin preserved. «ТЕРМОМЕТР ДЛЯ СТЕЙКІВ» → «ТЕРМОМЕТР ДЛЯ СТЕЙКОВ». |
| 3 | 35 | 36 | 1157959901 | Hendi 271216 термометр с зондом (0/+100°C) | **TRIP** | c5←c7; c36 RU 261 chars. **Source-typo «100C» missing ° preserved**. «вістря зонда» → «острие зонда» / «з кліпсою» → «с клипсой». |
| 4 | 36 | 37 | 1157978504 | Hendi 271179 термометр универсальный для печей и духовок +50/+300°C | **TRIP** | c5←c7; c36 RU 281 chars. **Source-typo «Hendi 271179Температурный» (glued missing space) preserved**. «300C» missing ° preserve. «Дозвіл: 10°C» (BIG step) → «Разрешение: 10°C». «гачком і підставкою» → «крючком и подставкой». |
| 5 | 37 | 38 | 1158144305 | Hendi Kitchen Line 572313 порционная ложка для мороженого 1/20 Ø56 | **TRIP** | c5←c7; c36 RU 408 chars (1 para + 6 li). **Source-typo «Місткість в л::» (двойное двоеточие) preserved**. «Виготовлений з нержавіючої сталі» → «Изготовлена из нержавеющей стали». 47х70х17 dims. |
| 6 | 38 | 39 | 1158150087 | Hendi Kitchen Line 572511 порционная ложка для мороженого 1/30 Ø50 | **TRIP** | c5←c7; c36 RU 384 chars (1 para + 5 li). Близнец r38 с «Местимость в л:: 1/30» double colon. Без габ-li. |
| 7 | 39 | 40 | 1158162948 | Hendi Profi Line 759240 порционная ложка для мороженого 1/30 Ø50 | **TRIP** | c5←c7; c36 RU 376 chars. **Source-typo лишние пробелы «<br/> <br/> Особливості» preserved**. «ручка з поліаміду» → «ручка из полиамида». Без «<br/><br/>» рядом (другой источник). |
| 8 | 40 | 41 | 1158166263 | Hendi Profi Line 759257 порционная ложка для мороженого 1/36 Ø48 | **TRIP** | c5←c7; c36 RU 376 chars. Близнец r40 с 1/36 / Ø48. Лишние пробелы preserve. |

**Итого b5:** TRIP 8 + blknotrip 0 + blknochg 0 + blkfix 0 + SKIP-НП 0. Verify **360 PASS / 0 FAIL**.
**Cum после b5:** TRIP 37 + blknotrip 0 + blknochg 3 + blkfix 0 + SKIP-НП 0 = **40/83**. UNPROC = 43 (rows 42-84).

## b6 (SKU 41-48, rows 42-49) — 48/83

| # | SKU | row | ART | Brand+Model | Category | Изменения |
|---|-----|-----|-----|-------------|----------|-----------|
| 1 | 41 | 42 | 1158537698 | Hendi 677834 силиконовый коврик 400х300 | **TRIP** | c5←c7; c36 RU 290 chars. `<h2>` structural preserve. Dims swap «300 x 400» в теле vs «400х300» в названии — preserve. «-40 ° C до 250 ° C» с пробелами вокруг ° preserve. |
| 2 | 42 | 43 | 1158541722 | Hendi 512517 маркер для тортов ø320 12 порций | **TRIP** | c5←c7; c36 RU 170 chars. **Source-typo `<h2>` указан ART «Hendi 677834» (коврик) вместо 512517 (copy-paste от r42) preserved**. Размер 350х194х240. |
| 3 | 43 | 44 | 1158543784 | Hendi 557112 кондитерские мешки одноразовые рулон 100 шт | **TRIP** | c5←c7; c36 RU 239 chars. `<h2>` preserve. «557112-» glued (no space) preserve. HACCP / 80 микрон / рулон 100 / для теплой+холодной массы. |
| 4 | 44 | 45 | 1158548555 | Hendi Kitchen Line 550120 кондитерский мешок 300 мм 2 шт | **TRIP** | c5←c7; c36 RU 257 chars. `<h2>` + 5 отдельных `<p>` (не li). Супер-нейлон без швов / многоразовый / петля-вешалка / тонкий+эластичный / стирать в горячей воде. |
| 5 | 45 | 46 | 1158551353 | Hendi Kitchen Line 550229 350 мм 2 шт | **TRIP** | c5←c7; c36 RU 257 chars. Близнец r45 (550229/350). |
| 6 | 46 | 47 | 1158551694 | Hendi Kitchen Line 550526 500 мм 2 шт | **TRIP** | c5←c7; c36 RU 257 chars. Близнец r45/r46 (550526/500). |
| 7 | 47 | 48 | 1158557766 | Hendi Profi Line 550205 350 мм | **TRIP** | c5←c7; c36 RU 346 chars. `<h2>` + 2 `<p>`. **Source-typo internal contradiction: «з бавовни» (хлопок)+полиуретан, затем «супер нейлон» — preserve faithful**. С подвеской / гибкий+тонкий / кипящая вода. |
| 8 | 48 | 49 | 1158558532 | Hendi Profi Line 550304 400 мм | **TRIP** | c5←c7; c36 RU 346 chars. Близнец r48 с той же source-typo (хлопок+полиуретан+нейлон). 550304/400. |

**Итого b6:** TRIP 8 + blknotrip 0 + blknochg 0 + blkfix 0 + SKIP-НП 0. Verify **384 PASS / 0 FAIL**.
**Cum после b6:** TRIP 45 + blknotrip 0 + blknochg 3 + blkfix 0 + SKIP-НП 0 = **48/83**. UNPROC = 35 (rows 50-84).

## b7 (SKU 49-56, rows 50-57) — 56/83

| # | SKU | row | ART | Brand+Model | Category | Изменения |
|---|-----|-----|-----|-------------|----------|-----------|
| 1 | 49 | 50 | 1158558969 | Hendi Profi Line 550502 кондитерский мешок 500 мм | **TRIP** | c5←c7; c36 RU 346 chars. Близнец r48/r49 с той же source-typo (хлопок+полиуретан vs супер нейлон). |
| 2 | 50 | 51 | 1158613536 | Hendi 551790 насадки для кондитерских мешков форма звезда (5 шт) | **TRIP** | c5←c7 (already RU); c36 RU 220 chars. Диаметры 6/8/10/12/14 мм. |
| 3 | 51 | 52 | 1158631508 | Hendi 551691 насадки 5 шт | **TRIP** | c5←c7 (already RU «форма простая»); c36 RU 221 chars. **Source-mismatch preserved: c4/c5/c7 «форма простая» vs c35<h2> «форма прямая»**. «діаметром:-» glued (двоеточие+тире) preserve. Диаметры 2/4/6/8/10. |
| 4 | 52 | 53 | 1158715104 | Hendi 676202 форма силиконовая Semi-sphere 6 ячеек | **TRIP** | c5←c7; c36 RU 1496 chars (1 para + 6 li + large table 11 rows). Все моды: Savarin/Semi-Sphere x2/Tartalette/Madeleines/Briochette/Mini-Muffins/Mini-Cake/Muffins/Mini-Madeleines/Cannele Bordelais. -60..+260°C / GN 1/3 / Ø70x(H)32. |
| 5 | 53 | 54 | 1158729232 | Hendi 676509 форма силиконовая Tartalette 15 ячеек | **TRIP** | c5←c7; c36 RU 1494 chars. **Source-typo preserved «Силиконовая форма для выпечки типа Semi-sphere x 15 шт» (на самом деле Tartalette)** copy-paste от r53. Same table. Ø50x17. |
| 6 | 54 | 55 | 1160131932 | Hendi 553404 нож для теста 150x110 | **TRIP** | c5←c7; c36 RU 102 chars. Минимал: «Нож для теста изготовлен из нержавеющей стали». |
| 7 | 55 | 56 | 1160148205 | Hendi 855751 нож для теста 150x110 + полипропилен ручка | **TRIP** | c5←c7; c36 RU 125 chars. + «Ручка из полипропилена». |
| 8 | 56 | 57 | 1160151245 | Hendi 856154 нож-ролик для теста - зубчатый | **TRIP** | c5←c7; c36 RU 486 chars. **Source-typo «Ручка для тіста» (должно быть Ролик?) preserved**. UA alt-spelling «з неіржавіючої сталі» → RU «из нержавеющей стали». ø60x180 / волнистое лезвие / декоративные ножи Hendi / самые модные блюда. |

**Итого b7:** TRIP 8 + blknotrip 0 + blknochg 0 + blkfix 0 + SKIP-НП 0. Verify **408 PASS / 0 FAIL**.
**Cum после b7:** TRIP 53 + blknotrip 0 + blknochg 3 + blkfix 0 + SKIP-НП 0 = **56/83**. UNPROC = 27 (rows 58-84).

## b8 (SKU 57-64, rows 58-65) — 64/83

| # | SKU | row | ART | Brand+Model | Category | Изменения |
|---|-----|-----|-----|-------------|----------|-----------|
| 1 | 57 | 58 | 1160159230 | Hendi Kitchen Line 515068 резак для теста | **blknochg** | c5/c7 уже RU «Резак для теста Hendi Kitchen Line 515068»; c36 уже pure RU (UA только в c35). Нет изменений. |
| 2 | 58 | 59 | 1160167764 | Hendi 515006 скалка для раскатки теста Ø65×250/470, 1,8 кг | **TRIP** | c5←c7; c36 RU 142 chars. UA «Качалка для розкочування тіста» → RU «Скалка для раскатки теста». UA alt «неіржавіючої» → RU «нержавеющей». «На втулках ковзання» → «На втулках скольжения». |
| 3 | 59 | 60 | 1160174458 | Hendi 554173 декоративный скребок для теста прямоугольный 110×72, 6 шт | **TRIP** | c5←c7; c36 RU 491 chars. «Декоративний кондитерський скребок для тортів, мусів, мас і кремів» → «Декоративный кондитерский скребок для тортов, муссов, масс и кремов». «прямокутна форма - гребінець» → «прямоугольная форма - гребень». Белый полипропилен. |
| 4 | 60 | 61 | 1160190700 | Hendi 659304 скребок для теста 70×116×L358 + iframe | **TRIP** | c5←c7; c36 RU 648 chars. **Literal `'` в «110'C» drop → «110C»** (источник использует `'` как °, faithful to source-typo style). АБС-пластик / синтетический каучук. iframe Gnw_h-FEhHY preserved. |
| 5 | 61 | 62 | 1160209022 | Hendi 659465 скребок для теста в форме ложки 75×112×L356 | **TRIP** | c5←c7; c36 RU 441 chars. ABS пластик / синтетический каучук / подходит для горячих блюд. |
| 6 | 62 | 63 | 1160220125 | Hendi 659472 скребок в форме ложки 75×117×L408 | **TRIP** | c5←c7; c36 RU 440 chars. Близнец r62. **Source-quirk: «(L)408мм» glued no space preserve в `<h2>` (отличие от r62: 356 мм с пробелом)**. |
| 7 | 63 | 64 | 1160224561 | Hendi 658604 скребок из нейлона 55×90×L250 | **TRIP** | c5←c7; c36 RU 473 chars. Нейлон, армированный стекловолокном / натуральный каучук / **НЕ подходит** для горячих блюд. |
| 8 | 64 | 65 | 1160229352 | Hendi 658703 скребок из нейлона 55×90×L320 | **TRIP** | c5←c7; c36 RU 473 chars. Близнец r64. |

**Итого b8:** TRIP 7 + blknotrip 0 + blknochg 1 + blkfix 0 + SKIP-НП 0. Verify **429 PASS / 0 FAIL**.
**Cum после b8:** TRIP 60 + blknotrip 0 + blknochg 4 + blkfix 0 + SKIP-НП 0 = **64/83**. UNPROC = 19 (rows 66-84).

## b9 (SKU 65-72, rows 66-73) — 72/83

| # | SKU | row | ART | Brand+Model | Category | Изменения |
|---|-----|-----|-----|-------------|----------|-----------|
| 1 | 65 | 66 | 1160231659 | Hendi 658802 скребок из нейлона 55×90×L420 | **TRIP** | c5←c7; c36 RU 495 chars. Близнец r64/r65, длиннее (L)420. Prefix «Hendi сборщик тортов» preserve. |
| 2 | 66 | 67 | 1160236004 | Hendi 554234 декоративный скребок прямоугольный 110×72 нерж | **TRIP** | c5←c7; c36 RU 534 chars. **Source-quirk: dims `<h2>` «102х69 мм» != c5/c7 «110х72 мм» — preserve faithful**; также c36 упоминает «з нержавіючої сталі» которое отсутствует в c5/c7. |
| 3 | 67 | 68 | 1160246515 | Hendi 554364 скребок прямоугольный 120×93 компл 6шт | **TRIP** | c5←c7; c36 RU 235 chars. Полипропилен. Простое описание. |
| 4 | 68 | 69 | 1160249312 | Hendi 659106 скребок с силиконовой лопаткой 70×105×L420 + iframe | **TRIP** | c5←c7; c36 RU 679 chars. iframe Gnw_h-FEhHY preserved. **Real °C present** «-60 ° C до + 260 ° C» — preserve as is. Source-quirk: «- рукоятка з пластику ABS<br/> термостійкість...» — glued without bullet on 2nd part — preserve. |
| 5 | 69 | 70 | 1162408700 | Hendi 637821 сито для просеивания сахарной пудры ø410 | **TRIP** | c5 уже RU (==c7) сохраняем; c36 mixed UA («Особенности продукта:» RU + UA body) → pure RU 223 chars. Header order «ø410 мм Hendi 637821» preserve. |
| 6 | 70 | 71 | 1165850116 | Hendi 588406 баллончики с углекислым газом 10 шт | **TRIP** | c5←c7; c36 RU 176 chars. «Картриджи-баллончики с CO2». «- золото» solo color line preserve. |
| 7 | 71 | 72 | 1166974852 | Hendi 515228 кисть кондитерская деревянная плоская 20×210 2шт | **TRIP** | c5 уже RU (==c7) сохраняем; c36 UA → RU 146 chars. «Кількість в упаковці» / «Розміри, мм» → RU. |
| 8 | 72 | 73 | 1166977971 | Hendi 515358 кисть кондитерская силиконовая плоская 35×235 | **TRIP** | c5←c7; c36 RU 316 chars. **Source-typo: `<h2>` content says «Hendi 515228» (wrong SKU, should be 515358) — preserve faithful**. «градусів C» → «градусов C» (написано словом, не °). |

**Итого b9:** TRIP 8 + blknotrip 0 + blknochg 0 + blkfix 0 + SKIP-НП 0. Verify **453 PASS / 0 FAIL**.
**Cum после b9:** TRIP 68 + blknotrip 0 + blknochg 4 + blkfix 0 + SKIP-НП 0 = **72/83**. UNPROC = 11 (rows 74-84).

## b10 (SKU 73-80, rows 74-81) — 80/83

| # | SKU | row | ART | Brand+Model | Category | Изменения |
|---|-----|-----|-----|-------------|----------|-----------|
| 1 | 73 | 74 | 1166980507 | Hendi 515365 кисть кондитерская силиконовая плоская 50×235 | **TRIP** | c5←c7; c36 RU 316 chars. Близнец r73 (b9), шире 50 мм. `<h2>` SKU 515365 (correct, no typo unlike r73). |
| 2 | 74 | 75 | 1167020747 | Hendi 826065 доска разделочная HACCP GN 1/1 фиолетовая | **TRIP** | c5←c7; c36 RU 1632 chars. HACCP board template + iframe C8b5szTz-0g preserved. **Reusable 7-row color table** (одинаковая для всех b10 досок). «(антиаллергическая маркування)» mix RU+UA → «(антиаллергическая маркировка)». |
| 3 | 75 | 76 | 1167027087 | Hendi 826003 доска разделочная HACCP GN 1/1 белая | **TRIP** | c5←c7; c36 RU 1617 chars. Тот же template; usage «молочные продукты, хлеб». |
| 4 | 76 | 77 | 1167033802 | Hendi 826027 доска разделочная HACCP GN 1/1 голубая (синяя) | **TRIP** | c5←c7; c36 RU 1608 chars. Color «голубая (синяя)» preserve dual naming; usage «рыба». |
| 5 | 77 | 78 | 1167060549 | Hendi 826058 доска разделочная HACCP GN 1/1 желтая | **TRIP** | c5←c7; c36 RU 1607 chars. **Source-typo: «сира птах» (broken UA, должно быть «сира птиця») → translate «сырая птица»** (faithful RU). |
| 6 | 78 | 79 | 1172959385 | Hendi 826034 доска разделочная HACCP GN 1/1 зеленая | **TRIP** | c5←c7; c36 RU 1612 chars. Usage «(овощи и зелень)». |
| 7 | 79 | 80 | 1172963060 | Hendi 826041 доска разделочная HACCP GN 1/1 коричневая | **TRIP** | c5←c7; c36 RU 1625 chars. Usage «(колбасы, вареное мясо)» — note `<li>` order differs from table column («ковбаси, варене м'ясо» в `<li>` vs «варене м'ясо, ковбаси» в таблице — preserve as in source). |
| 8 | 80 | 81 | 1172965322 | Hendi 826010 доска разделочная HACCP GN 1/1 красная | **TRIP** | c5←c7; c36 RU 1608 chars. Usage «(сырое мясо)». |

**Итого b10:** TRIP 8 + blknotrip 0 + blknochg 0 + blkfix 0 + SKIP-НП 0. Verify **477 PASS / 0 FAIL**.
**Cum после b10:** TRIP 76 + blknotrip 0 + blknochg 4 + blkfix 0 + SKIP-НП 0 = **80/83**. UNPROC = 3 (rows 82-84) → b11 финал.
