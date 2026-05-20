# chunk-079 manual review (W2)

**Status:** chunk-079 b1 DONE 8/58 (cum TRIP 0 / blknotrip 0 / blknochg 8 / blkfix 0 / SKIP-НП 0; 72 PASS / 0 FAIL) — next b2 (SKU 9-16, rows 10-17). Без новых OQ.

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
