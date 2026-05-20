# chunk-077 manual review (W2)

**Status:** chunk-077 scaffold (W2, продолжение chunk-076). Не стартован, ожидает b1.

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
