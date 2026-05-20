# chunk-079 manual review (W2)

**Status:** chunk-079 b2 DONE 16/58 (cum TRIP 0 / blknotrip 0 / blknochg 16 / blkfix 0 / SKIP-НП 0; 144 PASS / 0 FAIL) — next b3 (SKU 17-24, rows 18-25). 2 новых OQ (c079 #1 r12 FSC1000H body=FSC1000S; c079 #2 r14 FSC1950S body=FS1202H).

## Параметры

- Source: `.planning/translation-audit/chunks/chunk-079.xlsx` (RO).
- Working copy: `.planning/translation-audit/chunks/chunk-079-fixed.xlsx` (gitignored).
- Range: 58 SKU rows 2..59. ART 2140760718..2046767826.
- Header row: c1 Артикул, c4 NM_UA, c5 NM_RU, c7 NAZV_RU, c35 DSC_UA, c36 DSC_RU.
- Распределение батчей: b1 rows 2-9 (SKU 1-8), b2 rows 10-17 (SKU 9-16), b3 rows 18-25 (SKU 17-24), b4 rows 26-33 (SKU 25-32), b5 rows 34-41 (SKU 33-40), b6 rows 42-49 (SKU 41-48), b7 rows 50-57 (SKU 49-56), b8 rows 58-59 (SKU 57-58, 2 финальный).

## SKIP-НП preliminary

- (пусто) — сканирование по brand-list дало 0 совпадений.

## Категории (определяются per-батч probe)

TRIP / blknotrip / blknochg / blkfix / SKIP-НП.

## OQ (chunk-079)

(пусто на момент scaffold)


## b1 (SKU 1-8, rows 2-9) — DONE 8/58

**Категории:** blk триплет 0 / blknotrip 0 / blknochg 8 / blkfix 0 / SKIP-НП 0.

### blknochg (c5==c7 genuine RU, c36 unchanged)

- **r2** SKU=1 ART=2140760718 Tefcold UR600SG — c5==c7 RU clean.
- **r3** SKU=2 ART=2140762562 Tefcold RK500SNACK — c5==c7 RU clean.
- **r4** SKU=3 ART=2140764901 Tefcold NC2500G — c5==c7 RU clean (c36 body упоминает «NC2500» без G — наследие источника, не наш write).
- **r5** SKU=4 ART=2140771607 Tefcold FS890H — c5==c7 RU clean.
- **r6** SKU=5 ART=2140773390 Tefcold FSC890S — c5==c7 RU clean.
- **r7** SKU=6 ART=2140774704 Tefcold FSC890H — c5==c7 RU clean.
- **r8** SKU=7 ART=2140777191 Tefcold RK710G — c5==c7 RU clean.
- **r9** SKU=8 ART=2140783030 Tefcold RKS600 — c5==c7 RU clean.

**Verify:** 72 PASS / 0 FAIL. Без новых OQ.


## b2 (SKU 9-16, rows 10-17) — DONE 16/58

**Категории:** blk триплет 0 / blknotrip 0 / blknochg 8 / blkfix 0 / SKIP-НП 0.

### blknochg (c5==c7 genuine RU, c36 unchanged)

- **r10** SKU=9 ART=2141128896 Tefcold FS1002S — c5==c7 RU clean.
- **r11** SKU=10 ART=2141131104 Tefcold FSC1000S — c5==c7 RU clean.
- **r12** SKU=11 ART=2141133910 Tefcold FSC1000H — c5==c7 RU clean (⚠ c35/c36 body упоминает «FSC1000S» вместо FSC1000H — наследие источника, источник переиспользовал описание sibling-SKU). ⇒ OQ c079 #1.
- **r13** SKU=12 ART=2141135512 Tefcold FS1202H — c5==c7 RU clean.
- **r14** SKU=13 ART=2141140987 Tefcold FSC1950S — c5==c7 RU clean (⚠ c35/c36 body упоминает «FS1202H» — описание sibling-SKU, не FSC1950S). ⇒ OQ c079 #2.
- **r15** SKU=14 ART=2141146470 Tefcold FSC1950H — c5==c7 RU clean.
- **r16** SKU=15 ART=2141154883 Tefcold FS1202S — c5==c7 RU clean.
- **r17** SKU=16 ART=2141159745 Tefcold ATOM MAXI C2DB — c5==c7 RU clean.

**Verify:** 72 PASS / 0 FAIL. 2 новых OQ.

### Открытые вопросы (новые)

- **OQ c079 #1**: r12 SKU=11 ART=2141133910 Tefcold **FSC1000H** — название (c4/c5/c7) указывает на FSC1000H, но тело описания (c35/c36) дословно идентично r11 FSC1000S и упоминает модель «FSC1000S» в первом предложении. Источник: ETL переиспользовал описание sibling-SKU. Не наш write. Решение Yana: либо переписать body под FSC1000H (нужен спец-лист модели), либо принять как есть.
- **OQ c079 #2**: r14 SKU=13 ART=2141140987 Tefcold **FSC1950S** — название указывает на FSC1950S, но тело описания (c35/c36) идентично r13 FS1202H и упоминает «FS1202H». Источник: cross-paste из соседнего SKU. Не наш write. Решение Yana: переписать body под FSC1950S или принять.
