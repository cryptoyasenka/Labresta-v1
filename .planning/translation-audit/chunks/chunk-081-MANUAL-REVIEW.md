# chunk-081 manual review (W2)

**Status:** chunk-081 b3 DONE 24/52 (cum TRIP 0 / blknotrip 0 / blknochg 24 / blkfix 0 / SKIP-НП 0; 96 PASS / 0 FAIL) — next b4 (SKU 25-32, rows 26-33, включая r33 Fagor SKIP-НП). 1 SKIP-НП preliminary (r33 Fagor, b4).

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

## b2 (SKU 9-16, rows 10-17) — DONE 16/52

**Категории:** blk триплет 0 / blknotrip 0 / blknochg 8 / blkfix 0 / SKIP-НП 0.

### blknochg (c5==c7 genuine RU, c36 unchanged)

- **r10** SKU=9 ART=2143881489 Tefcold UFFS371G — c5==c7 RU clean.
- **r11** SKU=10 ART=2143885138 Tefcold UFFS370G — c5==c7 RU clean.
- **r12** SKU=11 ART=2143887884 Tefcold UFFS371G LEFT — c5==c7 RU clean.
- **r13** SKU=12 ART=2143890960 Tefcold UFFS371GCP — c5==c7 RU clean.
- **r14** SKU=13 ART=2143894012 Tefcold UFFS370GCP — c5==c7 RU clean.
- **r15** SKU=14 ART=2143896940 Tefcold UF400VG — c5==c7 RU clean.
- **r16** SKU=15 ART=2143899546 Tefcold RF500SNACK — c5==c7 RU clean.
- **r17** SKU=16 ART=2144701837 Tefcold UF400VSG — c5==c7 RU clean.

**Verify:** 32 PASS / 0 FAIL. Без новых OQ.

## b3 (SKU 17-24, rows 18-25) — DONE 24/52

**Категории:** blk триплет 0 / blknotrip 0 / blknochg 8 / blkfix 0 / SKIP-НП 0.

### blknochg (c5==c7 genuine RU, c36 unchanged)

- **r18** SKU=17 ART=2144708272 Tefcold RF505 — c5==c7 RU clean.
- **r19** SKU=18 ART=2144714399 Tefcold UFSC370GCP BLACK — c5==c7 RU clean.
- **r20** SKU=19 ART=2144722408 Tefcold UFSC1450GCP NF — c5==c7 RU clean.
- **r21** SKU=20 ART=2144727092 Tefcold UFSC1450GCP NF SILVER — c5==c7 RU clean.
- **r22** SKU=21 ART=2144732211 Tefcold ATOM MAXI F1DB — c5==c7 RU clean.
- **r23** SKU=22 ART=2144735365 Tefcold RF1010 — c5==c7 RU clean.
- **r24** SKU=23 ART=2144745038 Tefcold ATOM MAXI F2DB — c5==c7 RU clean.
- **r25** SKU=24 ART=2144751676 Tefcold NF7500G — c5==c7 RU clean.

**Verify:** 32 PASS / 0 FAIL. Без новых OQ.



## b4 (SKU 25-32, rows 26-33) — DONE 32/52

**Категории:** blk триплет 2 / blknotrip 0 / blknochg 5 / blkfix 0 / SKIP-НП 1.

### TRIP (c5 UA→RU + c36 полный RU перевод)

- **r31** SKU=30 ART=2044227917 Frosty H730T — Шафа для дозрівання м'яса → Шкаф для созревания мяса. c5←c7. c36 UA→RU (1304 chars, 730 л, 3 полки нерж., 4 вентилятора, чёрное стекло/корпус).
- **r32** SKU=31 ART=2077841122 Frosty H730S — Шафа для дозрівання м'яса → Шкаф для созревания мяса. c5←c7. c36 UA→RU (1198 chars, 730 л, 6 полок нерж., 6 вентиляторов, серебристое стекло, чёрный корпус).

### blknochg (c5==c7 genuine RU, c36 unchanged)

- **r26** SKU=25 ART=2144755547 Tefcold ATOM MAXI F3DB — c5==c7 RU clean.
- **r27** SKU=26 ART=2144758114 Tefcold UFSC1600GCP — c5==c7 RU clean.
- **r28** SKU=27 ART=2245914296 Tefcold UF400-I — c5==c7 RU clean.
- **r29** SKU=28 ART=2331855260 SARO KYRA GN 700 BT — c5==c7 RU clean.
- **r30** SKU=29 ART=2047212257 Brillis BL4-R290 — c5==c7 RU clean.

### SKIP-НП (brand=FAGOR, тело из фида НП позже)

- **r33** SKU=32 ART=2197275420 FAGOR FMA-1650 — Шкаф для созревания мяса. SKIP-НП #1. Ячейки не меняем.

**Verify:** 39 PASS / 0 FAIL. Без новых OQ.

**Cumulative chunk-081:** 32/52 (TRIP 2 / blknotrip 0 / blknochg 29 / blkfix 0 / SKIP-НП 1; 135 PASS / 0 FAIL).
