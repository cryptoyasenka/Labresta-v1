# chunk-078 diff (W2)

**Source:** `.planning/translation-audit/chunks/chunk-078.xlsx` (RO)
**Working copy:** `.planning/translation-audit/chunks/chunk-078-fixed.xlsx` (gitignored)
**Range:** 53 SKU rows 2..54. ART 1836114228..2140758985.

**Категории:** TRIP / blknotrip / blknochg / blkfix / SKIP-НП.

**SKIP-НП preliminary:** r19 TATRA TRC1400TN (b3).

**Распределение батчей:** b1 (2-9, 8 SKU) → b2 (10-17, 8) → b3 (18-25, 8) → b4 (26-33, 8) → b5 (34-41, 8) → b6 (42-49, 8) → b7 (50-54, 5 финальный).


## b1 (SKU 1-8, rows 2-9)

Категории: blk триплет 0 / blknotrip 0 / blknochg 8 / blkfix 0 / SKIP-НП 0.

### blknochg

| row | SKU | ART | модель | примечание |
|---|---|---|---|---|
| 2 | 1 | 1836114228 | Tefcold RK1420 | |
| 3 | 2 | 1836123363 | Tefcold RK1420G | |
| 4 | 3 | 2048300489 | Gooder SR400G | |
| 5 | 4 | 2048301009 | Gooder SR600G | |
| 6 | 5 | 2050431626 | Snaige CC29SM-T100FFQ | в источнике c36 «используетсяна» (без пробела) — не наш write |
| 7 | 6 | 2050432029 | Snaige CC29SM-T1CBFFQ | то же |
| 8 | 7 | 2050432666 | Snaige CC31SM-T100FFQ | то же |
| 9 | 8 | 2050433230 | Snaige CC31SM-T1CBFFQ | то же |

**Verify:** 72 PASS / 0 FAIL. Без новых OQ.


## b2 (SKU 9-16, rows 10-17)

Категории: blk триплет 0 / blknotrip 0 / blknochg 8 / blkfix 0 / SKIP-НП 0.

### blknochg

| row | SKU | ART | модель | примечание |
|---|---|---|---|---|
| 10 | 9 | 2050433886 | Snaige CC35DM-P6CBFD | source «используетсяна» |
| 11 | 10 | 2050434203 | Snaige CC48DM-P600FD | source «используетсяна» |
| 12 | 11 | 2050434473 | Snaige CC48DM-P6CBFD | source «используетсяна» |
| 13 | 12 | 2050683823 | Snaige CD350-100D | source «используетсяна» |
| 14 | 13 | 2050694836 | Snaige CD35DM-S300SD | source «используетсяна» |
| 15 | 14 | 2050701525 | Snaige CD40DM-S3002E | source «используетсяна» |
| 16 | 15 | 2050708198 | Snaige CD48DM-S300AD | source «используетсяна» |
| 17 | 16 | 2052929591 | Tefcold GUC70 | |

**Verify:** 72 PASS / 0 FAIL. Без новых OQ.


## b3 (SKU 17-24, rows 18-25)

Категории: blk триплет 0 / blknotrip 0 / blknochg 7 / blkfix 0 / SKIP-НП 1.

### SKIP-НП

| row | SKU | ART | бренд | модель |
|---|---|---|---|---|
| 19 | 18 | 2062033613 | TATRA | TRC1400TN |

⇒ SKIP-НП #1 по chunk-078. Ячейки в fixed не меняли. Тело из фида НП позже.

### blknochg

| row | SKU | ART | модель | примечание |
|---|---|---|---|---|
| 18 | 17 | 2052936584 | Tefcold FSC175H узкий | |
| 20 | 19 | 2107580724 | Tefcold FS890H BLACK | |
| 21 | 20 | 2133534707 | Tefcold BK850 под противни кондитерский | |
| 22 | 21 | 2133551858 | Tefcold UR400G | |
| 23 | 22 | 2134152498 | Tefcold UR90G-SUB ZERO | |
| 24 | 23 | 2134186706 | Tefcold UR600 | c5/c7 имеет суффикс «-I» (UR600-I), c4 — UR600; наследие источника |
| 25 | 24 | 2139042703 | Tefcold CC45 | |

**Verify:** 66 PASS / 0 FAIL. Без новых OQ.
