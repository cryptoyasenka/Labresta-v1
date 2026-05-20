# chunk-080 manual review (W2)

**Status:** chunk-080 b1 DONE 8/53 (cum TRIP 3 / blknotrip 0 / blknochg 5 / blkfix 0 / SKIP-НП 0; 75 PASS / 0 FAIL) — next b2 (SKU 9-16, rows 10-17). 4 SKIP-НП preliminary (r15 TATRA / r19 Hurakan / r36 Fagor / r39 HURAKAN).

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

