# chunk-081 manual review (W2)

**Status:** chunk-081 b1 DONE 8/52 (TRIP 0 / blknotrip 0 / blknochg 8 / blkfix 0 / SKIP-НП 0; 32 PASS / 0 FAIL) — next b2 (SKU 9-16, rows 10-17). 1 SKIP-НП preliminary (r33 Fagor, b4).

## Параметры

- Source: `.planning/translation-audit/chunks/chunk-081.xlsx` (RO).
- Working copy: `.planning/translation-audit/chunks/chunk-081-fixed.xlsx` (gitignored).
- Range: 52 SKU rows 2..53. ART 2133530800..2217381714.
- Header row: c1 Артикул, c4 NM_UA, c5 NM_RU, c7 NAZV_RU, c35 DSC_UA, c36 DSC_RU.
- Распределение батчей: b1 rows 2-9 (SKU 1-8), b2 rows 10-17 (SKU 9-16), b3 rows 18-25 (SKU 17-24), b4 rows 26-33 (SKU 25-32), b5 rows 34-41 (SKU 33-40), b6 rows 42-49 (SKU 41-48), b7 rows 50-53 (SKU 49-52, 4 финальный).

## SKIP-НП preliminary

- **r33** SKU=32 ART=2197275420 **FAGOR** FMA-1650 — Шафа для дозрівання м'яса (попадёт в b4).

## Категории (определяются per-батч probe)

TRIP / blknotrip / blknochg / blkfix / SKIP-НП.

## OQ (chunk-081)

(пусто на момент scaffold)

## b1 (SKU 1-8, rows 2-9) — DONE 8/52

**Категории:** blk триплет 0 / blknotrip 0 / blknochg 8 / blkfix 0 / SKIP-НП 0.

### blknochg (c5==c7 genuine RU, c36 unchanged)

- **r2** SKU=1 ART=2133530800 Tefcold BF850 — c5==c7 RU clean (c4 UA «під протівні», но в c5/c7 не включено — наследие источника).
- **r3** SKU=2 ART=2134166130 Tefcold UF100G — c5==c7 RU clean.
- **r4** SKU=3 ART=2134354481 Tefcold UF50G-P — c5==c7 RU clean (c36 body head ссылается на «UF50G» без -P, минорный sibling cross-paste артефакт источника).
- **r5** SKU=4 ART=2141752605 Tefcold UF400 — c5==c7 RU clean.
- **r6** SKU=5 ART=2141761331 Tefcold UF400V — c5==c7 RU clean.
- **r7** SKU=6 ART=2143853708 Tefcold UF550 — c5==c7 RU clean.
- **r8** SKU=7 ART=2143858217 Tefcold UF400VS — c5==c7 RU clean.
- **r9** SKU=8 ART=2143877088 Tefcold UF400SG — c5==c7 RU clean.

**Verify:** 32 PASS / 0 FAIL. Без новых OQ.

