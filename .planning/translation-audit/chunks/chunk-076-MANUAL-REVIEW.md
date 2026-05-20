# chunk-076 MANUAL REVIEW (W2, продолжение chunk-075)

**Status:** chunk-076 b1 DONE 8/57 (TRIP 2 / blknotrip 0 / blknochg 6 / blkfix 0 / SKIP-НП 0; 98 PASS / 0 FAIL) — next b2 (SKU 9-16, rows 10-17)
**Last updated:** chunk-076 b1 (8/57)

**Объём:** 57 SKU rows 2..58. ART 2106845309..2239472491.

**Обзор (preliminary по NM_UA):**
- Шафи холодильні Frosty/GoodFood/SCAN/Bartscher/Tecnodom/Whirlpool/Tefcold/REEDNEE/Forcold/COOLEQ + другие (~33)
- Шкафи / морозильное / витрины (~14)
- SKIP-НП FAGOR: r36 SKU35 FAGOR AFP-1602; r50 SKU49 Fagor CUP-11G (preliminary, forward-only)
- Прочее (Tefcold НЕ SKIP — substring «COLD» в standalone бренде не считается)

**Контекст:** контёрный chunk полностью под холодильным/морозильным оборудованием. Tefcold-блок ~r13/r17 (НЕ SKIP, обрабатывается обычно).

**Категории:** TRIP / blknotrip / blknochg / blkfix / SKIP-НП.

**Кумулятив до chunk-076 (W2 chunk-055..075):** см. .planning/CURRENT-w2.md.


## b1 (SKU 1-8, rows 2-9) — DONE 8/8

**Категории:** blk триплет 2 / blknotrip 0 / blknochg 6 / blkfix 0 / SKIP-НП 0

**Резюме:**
- r2 SKU1 ART=2106845309 Frosty FTD400 → **blknochg** (c5==c7 genuine RU, c36 805).
- r3 SKU2 ART=2106846812 Frosty FTD600 → **blknochg** (c5==c7, c36 890).
- r4 SKU3 ART=2212807455 GoodFood GF-GN650TN-HC → **blknochg** (c5==c7, c36 821).
- r5 SKU4 ART=2212810082 GoodFood GF-GN1200TN-HC → **blknochg** (c5==c7, c36 826).
- r6 SKU5 ART=2212810687 GoodFood GF-GN1410TN-HC → **blknochg** (c5==c7, c36 826).
- r7 SKU6 ART=2239449208 GoodFood BC360NBB2LED (Шкаф холодильный для напитков) → **blknochg** (c5==c7, c36 845).
- r8 SKU7 ART=2326907236 SCAN SD 430 BE → **TRIP**. c5 «Шафа холодильна SCAN SD 430 BE» → «Шкаф холодильный SCAN SD 430 BE»; c36 ← faithful RU (360 л, стеклянные двери самозакрывающиеся с замком, 5 проволочных полок, 2 светодиода, вентилируемое охлаждение, 4 колесика, 0-10°C, 578х605х1980мм, 1,95 кВт, 220В, Дания, 68,5 кг).
- r9 SKU8 ART=2464196151 Bartscher 700183 → **TRIP**. c5 «Шафа холодильна Bartscher 700183» → «Шкаф холодильный Bartscher 700183»; c36 ← faithful RU (46 л, 1 стеклянная дверь, +4...+18°C, 1 решетчатая полка 365х165, компрессорное охлаждение, 5 уровней регулировки, пластик, 14.8 кг, 435х480х520, 0.09 кВт, 220V, Китай; pack 16.4 кг, 435х480х520).

**Verify:** 98 PASS / 0 FAIL.

**Открытых вопросов:** 0.
