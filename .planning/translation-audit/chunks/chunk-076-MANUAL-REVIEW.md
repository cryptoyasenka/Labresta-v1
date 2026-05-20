# chunk-076 MANUAL REVIEW (W2, продолжение chunk-075)

**Status:** chunk-076 b3 DONE 24/57 (cum TRIP 9 / blknotrip 0 / blknochg 14 / blkfix 1 / SKIP-НП 0; 315 PASS / 0 FAIL) — next b4 (SKU 25-32, rows 26-33). OQ#6 NEW: r24 Forcar G-ER200SS vs G-ER400 model mismatch.
**Last updated:** chunk-076 b3 (24/57)

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


## b2 (SKU 9-16, rows 10-17) — DONE 8/8

**Категории:** blk триплет 3 / blknotrip 0 / blknochg 5 / blkfix 0 / SKIP-НП 0

**Резюме:**
- r10 SKU9 ART=2493932591 Tecnodom AF07PKMTN290 → **blknochg** (c5==c7, c36 876).
- r11 SKU10 ART=953090210 Whirlpool ADN 221/2 → **blknochg** (c5==c7, c36 806).
- r12 SKU11 ART=1771754120 Whirlpool ADN 480S → **blknochg** (c5==c7, c36 915).
- r13 SKU12 ART=983017191 Tefcold UR400W1 → **blknochg** (c5==c7, c36 808).
- r14 SKU13 ART=1048885139 REEDNEE GN1410TN → **TRIP**. c5 UA→«Шкаф холодильный REEDNEE GN1410TN»; c36 ← faithful RU (2 глухие двери, 1300 л, 1480х830х2010, 6 полок GN 2/1, вентилируемое, регулируемые ножки, подсветка, нерж.сталь, 220 В, 0,52 кВт).
- r15 SKU14 ART=1048889612 REEDNEE GN650TN (с суффиксом) → **TRIP**. c5 ← «Шкаф холодильный REEDNEE GN650TN (от -2°С до +8°С, нерж)»; c36 ← faithful RU (1 глухая дверь, 650 л, 740х830х2010, 3 полки GN 2/1, вентилируемое, авто разморозка, R290, ножки, подсветка, электронный блок, нерж.сталь, 220 В, 0,32 кВт; интервал t° окружающей среды +38 °C / влажность 65%).
- r16 SKU15 ART=1072407515 Forcold G-GN650TN-FC (с суффиксом) → **TRIP**. c5 ← «Шкаф холодильный Forcold G-GN650TN-FC (-2...+8°С, нерж.)»; c36 ← faithful RU (650 л, 3 решетчатые GN 2/1 пластиковое покрытие, глухая дверь, авто разморозка + испарение талой воды, R290, термоизоляция 60 мм, динамическое охлаждение, ножки, подсветка, электронный блок, 740х830х2010, отделка из нерж.стали).
- r17 SKU16 ART=1156089161 Tefcold CEV425 1 LED → **blknochg** (c5==c7, c36 1459).

**Verify:** 110 PASS / 0 FAIL.

**Открытых вопросов:** 0.


## b3 (SKU 17-24, rows 18-25) — DONE 8/8

**Категории:** blk триплет 4 / blknotrip 0 / blknochg 3 / blkfix 1 / SKIP-НП 0

**Резюме:**
- r18 SKU17 ART=1282195225 COOLEQ GN1410TN (с суффиксом, 1476 л) → **blknochg** (c5==c7 RU; c36 genuine RU с естественной Ё в «объёма» — допустимо для blknochg, не переписываем).
- r19 SKU18 ART=1355309476 Forcold M-GN1410TN-FC → **TRIP**. c5 UA→«Шкаф холодильный Forcold M-GN1410TN-FC»; c36 ← faithful RU (1300 л, 6 GN 2/1 пласт.покрытие, глухие двери, 0...+8°C, авто разморозка+испарение талой воды, R290, термоизоляция 60 мм, динамическое охлаждение, ножки, подсветка, электронный блок, 0,52 кВт/220В, 1480х830х2010).
- r20 SKU19 ART=1407653946 FROSTY SNACK400TN → **TRIP**. c5 UA→«Шкаф холодильный FROSTY SNACK400TN»; c36 ← faithful RU (429 л, 3 регулируемые полки, колеса, статическое охлаждение с вентилятором, авто разморозка, нерж.сталь, 0,18 кВт, 680x710x2010, -2..+8°C при t°окр +38°C).
- r21 SKU20 ART=1507862535 SNAIGE CC35DM-P600FD → **blknochg** (c5==c7, c36 725).
- r22 SKU21 ART=1771711024 Whirlpool ADN 221C → **blkfix**. c5/c7 уже OK; в c36 одно UA-слово «вібором» → «выбором» (одна замена; остальной текст RU без изменений).
- r23 SKU22 ART=1880359754 Tefcold CEV425 BLACK → **blknochg** (c5==c7, c36 1080).
- r24 SKU23 ART=1999339124 Forcar G-ER200SS → **TRIP + OQ#6**. c4 NM_UA «Forcar G-ER200SS» ≠ c7 NAZV_RU «Forcar G-ER400» (model mismatch upstream). c5 ← c7 «Шкаф холодильный Forcar G-ER400» per workflow (Yana ревью upstream). c36 ← faithful RU (Барный холодильный шкаф, 130 л, 600х585х855, 0,15 кВт, R600А, 3 решетчатые полки с пластиковым покрытием 2х500х415 + 1х500х211, статическое охлаждение, разморозка остановкой компрессора, без подсветки, наружная нерж.сталь, внутренняя пластик).
- r25 SKU24 ART=2008346168 COOLEQ GN650TN → **TRIP**. c5 UA→«Шкаф холодильный COOLEQ GN650TN»; c36 ← faithful RU (685 л, -2..+8˚С, цифровой контроллер, динамическое охлаждение, ножки регулируются по высоте, нерж.сталь, 740х830х2010).

**Verify:** 107 PASS / 0 FAIL.

**Открытых вопросов:** 1 новый (OQ#6 r24 Forcar модель upstream catalog).
