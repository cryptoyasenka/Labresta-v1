# chunk-078 manual review (W2)

**Status:** chunk-078 b3 DONE 24/53 (cum TRIP 0 / blknotrip 0 / blknochg 23 / blkfix 0 / SKIP-НП 1; 210 PASS / 0 FAIL) — next b4 (SKU 25-32, rows 26-33). SKIP-НП #1: r19 TATRA TRC1400TN. Без новых OQ.

## Параметры

- Source: `.planning/translation-audit/chunks/chunk-078.xlsx` (RO).
- Working copy: `.planning/translation-audit/chunks/chunk-078-fixed.xlsx` (gitignored).
- Range: 53 SKU rows 2..54. ART 1836114228..2140758985.
- Header row: c1 Артикул, c4 NM_UA, c5 NM_RU, c7 NAZV_RU, c35 DSC_UA, c36 DSC_RU.
- Распределение батчей: b1 rows 2-9 (SKU 1-8), b2 rows 10-17 (SKU 9-16), b3 rows 18-25 (SKU 17-24), b4 rows 26-33 (SKU 25-32), b5 rows 34-41 (SKU 33-40), b6 rows 42-49 (SKU 41-48), b7 rows 50-54 (SKU 49-53, 5 финальный).

## SKIP-НП preliminary

- **r19** SKU=18 ART=2062033613 **TATRA** TRC1400TN (попадёт в b3).

## Категории (определяются per-батч probe)

TRIP / blknotrip / blknochg / blkfix / SKIP-НП.

## OQ (chunk-078)

(пусто на момент scaffold)


## b1 (SKU 1-8, rows 2-9) — DONE 8/53

**Категории:** blk триплет 0 / blknotrip 0 / blknochg 8 / blkfix 0 / SKIP-НП 0.

### blknochg (c5==c7 genuine RU, c36 unchanged)

- **r2** SKU=1 ART=1836114228 Tefcold RK1420 — c5==c7 RU clean.
- **r3** SKU=2 ART=1836123363 Tefcold RK1420G — c5==c7 RU clean.
- **r4** SKU=3 ART=2048300489 Gooder SR400G — c5==c7 RU clean.
- **r5** SKU=4 ART=2048301009 Gooder SR600G — c5==c7 RU clean.
- **r6** SKU=5 ART=2050431626 Snaige CC29SM-T100FFQ — c5==c7 RU clean (в c36 источник имеет «используетсяна» — наследие источника, не наш write).
- **r7** SKU=6 ART=2050432029 Snaige CC29SM-T1CBFFQ — c5==c7 RU clean (наследие «используетсяна»).
- **r8** SKU=7 ART=2050432666 Snaige CC31SM-T100FFQ — c5==c7 RU clean (наследие «используетсяна»).
- **r9** SKU=8 ART=2050433230 Snaige CC31SM-T1CBFFQ — c5==c7 RU clean (наследие «используетсяна»).

**Verify:** 72 PASS / 0 FAIL. Без новых OQ.


## b2 (SKU 9-16, rows 10-17) — DONE 16/53

**Категории:** blk триплет 0 / blknotrip 0 / blknochg 8 / blkfix 0 / SKIP-НП 0.

### blknochg (c5==c7 genuine RU, c36 unchanged)

- **r10** SKU=9 ART=2050433886 Snaige CC35DM-P6CBFD — c5==c7 RU clean (наследие «используетсяна»).
- **r11** SKU=10 ART=2050434203 Snaige CC48DM-P600FD — то же.
- **r12** SKU=11 ART=2050434473 Snaige CC48DM-P6CBFD — то же.
- **r13** SKU=12 ART=2050683823 Snaige CD350-100D — то же.
- **r14** SKU=13 ART=2050694836 Snaige CD35DM-S300SD — то же.
- **r15** SKU=14 ART=2050701525 Snaige CD40DM-S3002E — то же.
- **r16** SKU=15 ART=2050708198 Snaige CD48DM-S300AD — то же.
- **r17** SKU=16 ART=2052929591 Tefcold GUC70 — c5==c7 RU clean.

**Verify:** 72 PASS / 0 FAIL. Без новых OQ.


## b3 (SKU 17-24, rows 18-25) — DONE 24/53

**Категории:** blk триплет 0 / blknotrip 0 / blknochg 7 / blkfix 0 / SKIP-НП 1.

### SKIP-НП

- **r19** SKU=18 ART=2062033613 **TATRA** TRC1400TN — SKIP-НП (brand=TATRA, тело из фида НП позже). Ячейки в fixed не меняли. ⇒ SKIP-НП #1 по chunk-078.

### blknochg (c5==c7 genuine RU, c36 unchanged)

- **r18** SKU=17 ART=2052936584 Tefcold FSC175H узкий — c5==c7 RU clean.
- **r20** SKU=19 ART=2107580724 Tefcold FS890H BLACK — c5==c7 RU clean.
- **r21** SKU=20 ART=2133534707 Tefcold BK850 под противни кондитерский — c5==c7 RU clean.
- **r22** SKU=21 ART=2133551858 Tefcold UR400G — c5==c7 RU clean.
- **r23** SKU=22 ART=2134152498 Tefcold UR90G-SUB ZERO — c5==c7 RU clean.
- **r24** SKU=23 ART=2134186706 Tefcold UR600 — c5/c7 «UR600-I» (с суффиксом -I), c4 «UR600» — c5==c7 RU clean (расхождение c4 vs c5 — наследие).
- **r25** SKU=24 ART=2139042703 Tefcold CC45 — c5==c7 RU clean.

**Verify:** 66 PASS / 0 FAIL. Без новых OQ.
