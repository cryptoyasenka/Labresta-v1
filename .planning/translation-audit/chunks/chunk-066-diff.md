# chunk-066 — diff (W2)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-066 (90 SKU, rows 2..91; ART 2496038149 … 2153078504)
**Apply key:** `Артикул` (col1, scoped per row)
**Worker:** W2 (параллельный, диапазон chunk-055 … chunk-085); продолжение chunk-065
**Status:** b2 DONE 16/90 (b3 предстоит; b1..b11 по 8 SKU + b12=SKU89-90 2 SKU)

Категории: blk триплет / blknotrip / blknochg / SKIP-НП. Формат — как chunk-065-diff.md.

SKIP-НП prelim (forward-only, тело из фида НП позже): HURAKAN — SKU6 (ART/row7 HKN-GES300 NUT), SKU36 (row37 HKN-CSE400P млинниця), SKU47 (row48 HKN-C1 сладкая вата), SKU57 (row58 HKN-PCORN попкорн); TATRA — SKU67 (row68 TDM E 4B шаурма). Точная классификация — по ходу батчей.

---

<!-- Сводка по батчу b1 ниже. -->

## b1 — SKU 1-8 (rows 2-9) — DONE 8/8

**Verify:** REGR 0 + ART 90 + TRIP 5 + BLKNOCHG 2 + SKIP-НП 1 = 98 PASS / 0 FAIL.

### blk триплет 5
- **SKU 2 r3 ART 2519380945** Вафельниця Frosty WBS-6S (корн-доги / начинка): c5 «Вафельниця» → «Вафельница», c36 ← faithful RU (skel==UA; dims c35==c36 14×; &deg; ×2; x Lat ×2 / х Cyr ×6; \n ×14; «WBS- 6S» space-after-dash preserved).
- **SKU 3 r4 ART 2519399322** Вафельниця Frosty WBS-21W (кондитерські горішки): c5 ← genuine RU, c36 ← faithful RU (dims 14×; &deg; ×2; x Lat ×2 / х Cyr ×8).
- **SKU 5 r6 ART 2519442607** Вафельниця Frosty WBS-1UR (бургер UFO, закритий сендвіч): c5 ← genuine RU, c36 ← faithful RU (dims 15×; &deg; ×2; x Lat ×2 / х Cyr ×6).
- **SKU 7 r8 ART 630863408** Вафельниця EWT INOX TRWB01 для тонких вафель: c5 ← genuine RU, c36 ← faithful RU (dims 6×; ° U+00B0 ×1; х Cyr ×8); source typo «Термоература» → RU «Температура» (UA-опечатка, не атрибут).
- **SKU 8 r9 ART 823909747** Вафельниця Hendi 212127 для бельгійських (об'ємних) вафель: c5 ← genuine RU, c36 ← faithful RU (dims 7×; × U+00D7 mult ×2; х Cyr ×6); ASCII apos `'` ×2 → strip в RU («объемных/пять», ё avoided).

### blknotrip 0
_(нет)_

### blknochg 2
- **SKU 1 r2 ART 2496038149** Вафельница Roller Grill GES 80: c5==c7 genuine RU (Latin brand+model); c35!=c36 (928/949) — fixed строка НЕ тронута; soft-note: c36 source длиннее на 21 символ.
- **SKU 4 r5 ART 2519422914** Вафельниця Frosty WBS-1UH: c5==c7 genuine RU; c35!=c36 (563/568) — fixed строка НЕ тронута; soft-note: source c35 lead «Вафельница Frosty WBS-21W ... бургера UFO» при SKU=WBS-1UH — copy-paste артефакт; body про UFO burger как у SKU5.

### SKIP-НП 1
- **SKU 6 r7 ART 2784069485** HURAKAN HKN-GES300 NUT (горішниця): fixed row 7 НЕ тронут, тело из фида НП позже. prelim→confirmed #1.



## b2 — SKU 9-16 (rows 10-17) — DONE 16/16 (cum)

**Verify:** REGR 8 (b1) + ART 90 + TRIP 3 + BLKNOCHG 5 = 106 PASS / 0 FAIL.

### blk триплет 3
- **SKU 9 r10 ART 823914812** Вафельниця Hendi 212134 "серця" (квітка з 5 сердець): c5←c7 genuine RU `Вафельница Hendi 212134 "сердца"` (ASCII " ×2 preserved); c36 ← faithful RU (skel==UA; dims c35==c36 5×; × U+00D7 mult ×2; х Cyr ×4; \n ×12; ASCII apos `'` ×2 «п'яти/з'єднаних» → strip RU «пяти/соединенных», ё avoided).
- **SKU 14 r15 ART 2447939241** Вафельниця EWT INOX WB30N (об'ємні кондитерські горішки, 30 шт.): c5 ← genuine RU, c36 ← faithful RU (dims 14× включая `30` из WB30N; &#39; ×1 в `об&#39;ємних` → RU «объемных» (entity исчезает); «Однопостовая,» и `220V` Lat verbatim preserved).
- **SKU 16 r17 ART 630863406** Вафельниця EWT INOX FY1 для бельгійських (об'ємних) вафель: c5 ← genuine RU, c36 ← faithful RU (dims 5×; ° U+00B0 ×1; х Cyr ×8); source typo «Термоература» → RU «Температура» (UA-опечатка как в b1 SKU7).

### blknotrip 0
_(нет)_

### blknochg 5
- **SKU 10 r11 ART 1149698386** Roller Grill GES 10 (бельгійські вафлі): c5==c7 genuine RU (Latin brand+model); c35!=c36 (758/763) — fixed НЕ тронут; soft-note +5.
- **SKU 11 r12 ART 1149704682** Roller Grill GES 20 (бельгійські вафлі): c5==c7 genuine RU; c35!=c36 (749/754) — fixed НЕ тронут; soft-note +5.
- **SKU 12 r13 ART 1149705731** Roller Grill GES 40 (плоскі вафлі): c5==c7 genuine RU; c35==c36 (781/781 идентично) — fixed НЕ тронут.
- **SKU 13 r14 ART 1149728461** Roller Grill GED 40 (двопостова для тонких вафель): c5==c7 genuine RU; c35!=c36 (807/816) — fixed НЕ тронут; soft-note +9.
- **SKU 15 r16 ART 476389250** GoodFood WB1S (для бельгийских вафель — c5/c7 уже genuine RU): c5==c7 genuine RU; c35!=c36 (581/604) — fixed НЕ тронут; soft-note +23.

### SKIP-НП 0
_(нет в b2)_
