# chunk-080 manual review (W2)

**Status:** chunk-080 b3 DONE 24/53 (cum TRIP 8 / blknotrip 0 / blknochg 14 / blkfix 0 / SKIP-НП 2; 208 PASS / 0 FAIL) — next b4 (SKU 25-32, rows 26-33). SKIP-НП: #1 r15 TATRA + #2 r19 Hurakan. 2 SKIP-НП preliminary остались (r36 Fagor / r39 HURAKAN, оба b5).

## Параметры

- Source: `.planning/translation-audit/chunks/chunk-080.xlsx` (RO).
- Working copy: `.planning/translation-audit/chunks/chunk-080-fixed.xlsx` (gitignored).
- Range: 53 SKU rows 2..54. ART 2106854043..2127214194.
- Header row: c1 Артикул, c4 NM_UA, c5 NM_RU, c7 NAZV_RU, c35 DSC_UA, c36 DSC_RU.
- Распределение батчей: b1 rows 2-9 (SKU 1-8), b2 rows 10-17 (SKU 9-16), b3 rows 18-25 (SKU 17-24), b4 rows 26-33 (SKU 25-32), b5 rows 34-41 (SKU 33-40), b6 rows 42-49 (SKU 41-48), b7 rows 50-54 (SKU 49-53, 5 финальный).

## SKIP-НП preliminary

- **r15** SKU=14 ART=1505341914 **TATRA** TRC700BT (попадёт в b2).
- **r19** SKU=18 ART=2104599345 **Hurakan** HKN-GX1410BT INOX 1400 л (попадёт в b3).
- **r36** SKU=35 ART=2460100897 **Fagor** AFN-801 EXP NEO CONCEPT 700 л (попадёт в b5).
- **r39** SKU=38 ART=2854784095 **HURAKAN** HKN-GX1410BTS 1400 л (попадёт в b5).

## Категории (определяются per-батч probe)

TRIP / blknotrip / blknochg / blkfix / SKIP-НП.

## OQ (chunk-080)

(пусто на момент scaffold)

## b1 (SKU 1-8, rows 2-9) — DONE 8/53

**Категории:** blk триплет 3 / blknotrip 0 / blknochg 5 / blkfix 0 / SKIP-НП 0.

### TRIP (c5 ← c7; c36 ← faithful RU translation)

- **r7** SKU=6 ART=932586613 COOLEQ GN650BT — c5 был UA «Шафа морозильна COOLEQ GN650BT», c7 уже RU. Переписан c5→«Шкаф морозильный COOLEQ GN650BT»; c36 переведён полностью с UA (был дубль c35): «Морозильный шкаф используется для охлаждения и хранения замороженных продуктов на предприятиях общественного питания, а также на профессиональных кухнях» + ТТХ: -22..-18 °C, 685 л, 740х830х2010 мм, нержавеющая сталь, авто-оттайка ТЭН с испарением конденсата, эл.блок терморегулятор, 3 полки 530x650, 0,75 кВт.
- **r8** SKU=7 ART=1048875476 REEDNEE GN650BT — c5 был UA, c7 уже RU. Переписан c5→«Шкаф морозильный REEDNEE GN650BT»; c36 переведён полностью с UA: однодверный, -18...-22 °C, динамическое охлаждение, электронное управление, авторазмораживание, 3 решетчатые полки GN 2/1 (40 кг макс), регулируемые ножки, подсветка, 740х830х2010, 640 Вт/220 В.
- **r9** SKU=8 ART=1087707881 FROSTY SNACK400BT — c5 был UA, c7 уже RU. Переписан c5→«Шкаф морозильный FROSTY SNACK400BT»; c36 переведён полностью с UA: корпус из нержавеющей стали, 1 глухая дверь, -15..-20 °C при +38 °C среды, 429 л, 3 регулируемые полки, замок, подсветка, колеса, статическое охлаждение с вентилятором, авторазмораживание, 0,42 кВт, 680x710x2010 мм. (источник c35 имел `&#39;` в «об&#39;єм» — в RU без апострофа «объем»).

### blknochg (c5==c7 genuine RU, c36 unchanged)

- **r2** SKU=1 ART=2106854043 Frosty FBD400 — c5==c7 RU clean.
- **r3** SKU=2 ART=2106856190 Frosty FBD600 — c5==c7 RU clean.
- **r4** SKU=3 ART=2212813069 GoodFood GF-GN650BT-HC — c5==c7 RU clean.
- **r5** SKU=4 ART=2212814857 GoodFood GF-GN1410BT-HC — c5==c7 RU clean.
- **r6** SKU=5 ART=2493884395 Tecnodom AF07PKMBT LEFT — c5==c7 RU clean.

**Verify:** 75 PASS / 0 FAIL. Без новых OQ.

## b2 (SKU 9-16, rows 10-17) — DONE 16/53

**Категории:** blk триплет 3 / blknotrip 0 / blknochg 4 / blkfix 0 / SKIP-НП 1.

### SKIP-НП

- **r15** SKU=14 ART=1505341914 **TATRA** TRC700BT — SKIP-НП (brand=TATRA, тело из фида НП позже). Ячейки в fixed не меняли. ⇒ SKIP-НП #1 по chunk-080.

### TRIP (c5 ← c7; c36 ← faithful RU translation)

- **r11** SKU=10 ART=1090611117 Tecnodom AF14PKMBT — c5 был UA, c7 уже RU. Переписан c5→«Шкаф морозильный Tecnodom AF14PKMBT»; c36 переведён полностью с UA (дубль c35): 1400 л, глухие двери, цифр.дисплей, 0,69 кВт (UA «потужніть» — typo источника), динам.охлаждение, авторазмораживание, R452A, автоиспарение конденсата, 6 полок GN 2/1, направляющие-крюки, регул.ножки, -18..-22 °C, 1420х800х2030 мм.
- **r12** SKU=11 ART=1167134361 FROSTY GN650BT — c5 UA→RU «Шкаф морозильный FROSTY GN650BT»; c36 полный RU-перевод (дубль c35): 1 глухая дверь, -18..-22 °C при +38 °C среды, 650 л, 3 полки GN2/1, замок, внутр.подсветка, вентилируемое охлаждение, авторазмораживание, нерж.сталь satin-finish SCOTCH-BRITE, колеса, 0,42 кВт, 740х830х2010.
- **r13** SKU=12 ART=1167138649 FROSTY GN1410BT — c5 UA→RU «Шкаф морозильный FROSTY GN1410BT»; c36 полный RU-перевод (дубль c35): двухдверный, 2 глухие двери, -18..-22 °C, 1340 л, 6 полок GN2/1, замок, внутр.подсветка, вентилируемое охлаждение, авторазмораживание, нерж.сталь satin-finish SCOTCH-BRITE, 0,42 кВт, 1480х830х2010.

### blknochg (c5==c7 genuine RU, c36 unchanged)

- **r10** SKU=9 ART=1090605534 Tecnodom AF07PKMBT — c5==c7 RU clean.
- **r14** SKU=13 ART=1395554157 COOLEQ GN1410BT (-18°С...-22°С, нерж.) — c5==c7 RU clean.
- **r16** SKU=15 ART=2046671059 Brillis BL7-M-R290-EF — c5==c7 RU clean.
- **r17** SKU=16 ART=2046787606 Brillis BL14-M-R290-EF — c5==c7 RU clean (c5 «Энергоэффективный шкаф морозильный...» — расхождение с c4 «Шафа морозильна...», но c5==c7 — наследие источника).

**Verify:** 68 PASS / 0 FAIL. Без новых OQ.

## b3 (SKU 17-24, rows 18-25) — DONE 24/53

**Категории:** blk триплет 2 / blknotrip 0 / blknochg 5 / blkfix 0 / SKIP-НП 1.

### SKIP-НП

- **r19** SKU=18 ART=2104599345 **Hurakan** HKN-GX1410BT INOX 1400 л — SKIP-НП (brand=Hurakan, тело из фида НП позже). Ячейки в fixed не меняли. ⇒ SKIP-НП #2 по chunk-080.

### TRIP (c5 ← c7; c36 ← faithful RU translation)

- **r20** SKU=19 ART=2106854841 Frosty FBD400SS — c5 UA→RU «Шкаф морозильный Frosty FBD400SS»; c36 полный RU-перевод (был дубль c35): 326 л общий / 249 л полезный, глухие двери, замок, 6 полок ПВХ 480х405, -18..-23 °C, цифр.контроллер, статическое охлаждение, ручное размораживание, внутри белый пластик, корпус нерж.сталь, 0,432 кВт/220В, 600x639x1875, 80 кг.
- **r21** SKU=20 ART=2106857097 Frosty FBD600SS — c5 UA→RU «Шкаф морозильный Frosty FBD600SS»; c36 полный RU-перевод (был дубль c35): 534 л общий / 411 л полезный, глухие двери, замок, 6 полок ПВХ 640х490 (UA «розмыром» — typo источника), автотермостат -18..-23 °C, статическое охлаждение, ручное размораживание, внутри белый пластик, корпус нерж.сталь, 0,48 кВт/220В, 775x744x1900, 96 кг.

### blknochg (c5==c7 genuine RU, c36 unchanged)

- **r18** SKU=17 ART=2094488928 Juka ND75G — c5==c7 RU clean.
- **r22** SKU=21 ART=2134159499 Tefcold UFFS371SD — c5==c7 RU clean.
- **r23** SKU=22 ART=2141755896 Tefcold UF400S — c5==c7 RU clean.
- **r24** SKU=23 ART=2143847088 Tefcold UF600 — c5==c7 RU clean.
- **r25** SKU=24 ART=2144730312 Tefcold GUF140 — c5==c7 RU clean.

**Verify:** 65 PASS / 0 FAIL. Без новых OQ.

