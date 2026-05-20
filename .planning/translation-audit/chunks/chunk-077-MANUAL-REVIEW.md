# chunk-077 manual review (W2)

**Status:** chunk-077 b1 DONE 8/39 (cum TRIP 3 / blknotrip 0 / blknochg 5 / blkfix 0 / SKIP-НП 0; 65 PASS / 0 FAIL) — next b2 (SKU 9-16, rows 10-17). Preliminary SKIP-НП r13 HURAKAN (b2). Без новых OQ.

## Параметры

- Source: `.planning/translation-audit/chunks/chunk-077.xlsx` (RO).
- Working copy: `.planning/translation-audit/chunks/chunk-077-fixed.xlsx` (gitignored).
- Range: 39 SKU rows 2..40. ART 2239477693..1775843181.
- Header row: c1 Артикул, c4 NM_UA, c5 NM_RU, c7 NAZV_RU, c35 DSC_UA, c36 DSC_RU.
- Распределение батчей: b1 rows 2-9 (SKU 1-8), b2 rows 10-17 (SKU 9-16), b3 rows 18-25 (SKU 17-24), b4 rows 26-33 (SKU 25-32), b5 rows 34-40 (SKU 33-39, 7 SKU финальный).

## SKIP-НП preliminary

- **r13** SKU=12 **HURAKAN** HKN-GX650TNS (попадёт в b2).

## Категории (определяются per-батч probe)

TRIP / blknotrip / blknochg / blkfix / SKIP-НП.

## OQ (chunk-077)

(пусто на момент scaffold)


## b1 (SKU 1-8, rows 2-9) — DONE 8/39

**Категории:** blk триплет 3 / blknotrip 0 / blknochg 5 / blkfix 0 / SKIP-НП 0.

### TRIP (c5 ← c7; c36 ← faithful RU body)

- **r5** SKU=4 ART=2326908563 SCAN GUR 390W — c5→«Шкаф холодильный SCAN GUR 390W»; c36 RU: проф.холод.оборудование для производственных кухонь/складов/магазинов/общепита, 293 л, регулир.стеклянные полки, цифр.дисплей, перенавешиваемые двери, замок и ключ, 5 полок, 1-10°C, 595х625х1870, 523 КВт/год, 220В, Дания, 60 кг.
- **r6** SKU=5 ART=2367440138 Frosty FGN- 600TN — c5→«Шкаф холодильный Frosty FGN- 600TN»; c36 RU: 600 л / 514 л, 1 камера, глухие двери, замок, LED, 3 регулир. GN-2/1 ПВХ, цифр.контроллер, 0°С..+8°C (до +38°С), вентил.охлаждение, авто разморозка, регулир.ножки, 0,242 кВт/220В, 655х856х2083, 101 кг, нерж.сталь.
- **r8** SKU=7 ART=2402041388 Forcar G-ER600SS — c5→«Шкаф холодильный Forcar G-ER600SS»; c36 RU: для кухонь ресторана/кафе/магазинов/общепита, 1 дверь, статика (испаритель в полках), 3 несъемные 630х480+1 полка 630х290 пласт., 570 л, +2..+8°С (до +33°С), термоизол.60мм, разморозка остановкой компрессора+автоисп.талой воды, без подсветки, замок, мех.рег.t°, R600А, нерж.сталь корпус/пластик внутри; 90 кг, 777х695х1895, 0.19 кВт/220V, Италия; pack 120 / 760х840х2010.

### blknochg (c5==c7 genuine RU, c36 unchanged)

- **r2** SKU=1 ART=2239477693 GoodFood BC480BB2LED.
- **r3** SKU=2 ART=2284489499 BRILLIS BN9-LED-R290-EF-INV энергосберегающий.
- **r4** SKU=3 ART=2284520356 BRILLIS BN18-LED-R290-EF-INV с инверторной технологией.
- **r7** SKU=6 ART=2367445057 Frosty FGN-1400TN.
- **r9** SKU=8 ART=2402044817 Forcold G-SNACK400TN-FC.

**Verify:** 65 PASS / 0 FAIL. Без новых OQ.
