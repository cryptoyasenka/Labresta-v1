# chunk-083 MANUAL REVIEW (W2)

**Source:** `.planning/translation-audit/chunks/chunk-083.xlsx` (RO)
**Working copy:** `.planning/translation-audit/chunks/chunk-083-fixed.xlsx` (gitignored)
**Range:** 62 SKU rows 2..63. ART 2134369414..2139111115.

**Категории:** TRIP / blknotrip / blknochg / blkfix / SKIP-НП.

**SKIP-НП preliminary (4, все HURAKAN, contiguous r51-r54):**
- r51 SKU=50 ART=2657537335 HURAKAN HKN-BCS143F (морозильная барная)
- r52 SKU=51 ART=2657577444 HURAKAN HKN-BCS143 (холодильная барная)
- r53 SKU=52 ART=2657582966 HURAKAN HKN-BC145 (холодильная барная)
- r54 SKU=53 ART=2657604599 HURAKAN HKN-UF100G (морозильная барная)

**Распределение батчей:**
- b1 (SKU 1-8, rows 2-9)
- b2 (SKU 9-16, rows 10-17)
- b3 (SKU 17-24, rows 18-25)
- b4 (SKU 25-32, rows 26-33)
- b5 (SKU 33-40, rows 34-41)
- b6 (SKU 41-48, rows 42-49)
- b7 (SKU 49-56, rows 50-57) — включая r51-r54 HURAKAN SKIP×4
- b8 FINAL (SKU 57-62, rows 58-63, 6 SKU)


## b1 (SKU 1-8, rows 2-9) — DONE 8/62

**Категории:** blk триплет 5 / blknotrip 0 / blknochg 3 / blkfix 0 / SKIP-НП 0.

### blk триплет (TRIP — c5 переписан с UA→RU + c36 полный RU перевод)

- **r3** SKU=2 ART=2567616405 SIRMAN SOAVE (51 бутылка, 2 зоны 5-12/12-18°C, R600a, реверсивные двери) — c5 «Шкаф холодильный для вина SIRMAN SOAVE». c36 переведен полностью.
- **r5** SKU=4 ART=2525995929 Sirman Lison (250 бутылок, 710 л, +5..+22°C, R600a, 1000×600×1900мм) — c5 «Винный шкаф Sirman Lison» (по c7-pattern). c36 переведен.
- **r6** SKU=5 ART=655434908 EWT INOX RT400L-2 (81 бутылка, +5..+18°C, R134a, на колесах) — c5 «Шкаф-витрина холодильная для вина EWT INOX RT400L-2». c36 переведен.
- **r7** SKU=6 ART=2084253148 REEDNEE RT400L-2 (81 бутылка, +5..+18°C, R290, на колесиках) — c5 «Шкаф холодильный для вина REEDNEE RT400L-2». c36 переведен.
- **r8** SKU=7 ART=1129158560 FROSTY BD-32 минибар (32 л, -13..-22°C, 1 полка, окраш. сталь) — c5 «Шкаф морозильный FROSTY BD-32 (минибар)». c36 переведен.

### blknochg (c5==c7 genuine RU, c36 unchanged)

- **r2** SKU=1 ART=2134369414 Tefcold CPP1380 для вина — c5==c7 RU clean. Замечание: c35==c36 (оба RU, len 1497) — нетипично, но c5/c36 RU clean.
- **r4** SKU=3 ART=2227197573 Tecfrigo Sommelier 481 (192 бутылки) — c5==c7 RU clean.
- **r9** SKU=8 ART=2037165266 Frosty FBB293F барный — c5==c7 RU clean.

**Verify:** 44 PASS / 0 FAIL. Без новых OQ.

**Cumulative chunk-083:** 8/62 (TRIP 5 / blknotrip 0 / blknochg 3 / blkfix 0 / SKIP-НП 0; 44 PASS / 0 FAIL).


## b2 (SKU 9-16, rows 10-17) — DONE 16/62

**Категории:** blk триплет 1 / blknotrip 0 / blknochg 7 / blkfix 0 / SKIP-НП 0.

### blk триплет (TRIP — c5 переписан с UA→RU + c36 полный RU перевод)

- **r13** SKU=12 ART=2043423499 Frosty FCB-90 (90 л, +4..+16°C, LED голубой, 0,075 кВт, 450×490×790 мм, 4 решетчатые полки, перевешиваемая дверь) — c5 «Шкаф холодильный для напитков Frosty FCB- 90» (по c7, с пробелом «FCB- 90»). c36 переведен полностью (c35==c36 source оба UA). Замечание: c4/c6/c7 содержат пробел «FCB- 90» (модель FCB-90 без пробела, но в источнике стабильно с пробелом — сохранено).

### blknochg (c5==c7 genuine RU, c36 unchanged)

- **r10** SKU=9 ART=2037343744 Frosty FBB320HS барный тридверный — c5==c7 RU clean.
- **r11** SKU=10 ART=2037360967 Frosty FBB220HS барный — c5==c7 RU clean.
- **r12** SKU=11 ART=2037368159 Frosty FBB150H барный — c5==c7 RU clean.
- **r14** SKU=13 ART=2043425566 Frosty JC-75 (для напитков) — c5==c7 RU clean.
- **r15** SKU=14 ART=2080625607 Frosty RT-99L — c5==c7 RU clean.
- **r16** SKU=15 ART=2106839174 Frosty FTD200 — c5==c7 RU clean.
- **r17** SKU=16 ART=2106849059 Frosty FBD200 морозильный — c5==c7 RU clean.

**Verify:** 28 PASS / 0 FAIL. Без новых OQ.

**Cumulative chunk-083:** 16/62 (TRIP 6 / blknotrip 0 / blknochg 10 / blkfix 0 / SKIP-НП 0; 72 PASS / 0 FAIL).


## b3 (SKU 17-24, rows 18-25) — DONE 24/62

**Категории:** blk триплет 5 / blknotrip 0 / blknochg 3 / blkfix 0 / SKIP-НП 0.

### blk триплет (TRIP — c5 переписан с UA→RU + c36 полный RU перевод)

- **r21** SKU=20 ART=2326903957 SCAN SK145 E (145 л, +0..+10°C, 1 кВт, н/с, Дания, 595×595×820 мм) — c5 «Шкаф холодильный SCAN SK145 E» (по c7, источник c5 «Шафа барна холодильна» — barна качество избыточно, тело без barна). c36 переведен полностью (c35==c36 source оба UA).
- **r22** SKU=21 ART=2326905846 SCAN SF 115 X (115 л, -16..-22°C, 3 ящика, Дания, 595×595×820 мм, 0,76 кВт) — c5 «Шкаф морозильный SCAN SF 115 X» (по c7, источник c5 «глухі двері н/с» — описательно, не вариант SKU; нормализовано к c7-baseline). c36 переведен.
- **r23** SKU=22 ART=807739653 FROSTY SGD315SL (341 л, +2..+8°C, 0,26 кВт, 1355×515×870 мм, стеклянные двери-купе) — c5 «Шкаф барный FROSTY SGD315SL». c36 переведен. Замечание: модель SGD315SL но тело упоминает 341 л — несоответствие в названии vs тело, но переводим как есть.
- **r24** SKU=23 ART=953785561 Forcar G-ER200SS (130 л, +2..+8°C, R600A, 600×585×855 мм, 0,15 кВт, барный холодильный) — c5 «Шкаф холодильный Forcar G-ER200SS». c36 переведен. Замечание: см. OQ #6 c076 r24 G-ER200SS vs G-ER400 — здесь модель G-ER200SS body consistent с 130 л; OQ не reopen.
- **r25** SKU=24 ART=953793828 Forcar G-EF200SS (120 л, -18..-22°C, R600A, 600×585×855 мм, 0,15 кВт, барный морозильный) — c5 «Шкаф морозильный Forcar G-EF200SS». c36 переведен.

### blknochg (c5==c7 genuine RU, c36 unchanged)

- **r18** SKU=17 ART=2106851586 Frosty FBD200SS морозильный — c5==c7 RU clean.
- **r19** SKU=18 ART=2106853346 Frosty FBD200GSS морозильный — c5==c7 RU clean.
- **r20** SKU=19 ART=2110094971 GoodFood RTD99L морозильный — c5==c7 RU clean.

**Verify:** 44 PASS / 0 FAIL. Без новых OQ.

**Cumulative chunk-083:** 24/62 (TRIP 11 / blknotrip 0 / blknochg 13 / blkfix 0 / SKIP-НП 0; 116 PASS / 0 FAIL).


## b4 (SKU 25-32, rows 26-33) — DONE 32/62

**Категории:** blk триплет 5 / blknotrip 0 / blknochg 3 / blkfix 0 / SKIP-НП 0.

### blk триплет (TRIP — c5 переписан с UA→RU + c36 полный RU перевод)

- **r26** SKU=25 ART=1551462571 REEDNEE DR200SL минибар (140 л, +0..+10°C, R600A, 595×637×830 мм, 46 кг, 0,32 кВт) — c5 «Шкаф холодильный REEDNEE DR200SL». c36 переведен (c35==c36 source оба UA).
- **r27** SKU=26 ART=1551464669 REEDNEE F200SS минибар (97 л, -18..-23°C, R600A, 600×635×835 мм, 0,32 кВт, 2 фиксированные полки) — c5 «Шкаф морозильный REEDNEE F200SS». c36 переведен.
- **r31** SKU=30 ART=2043422036 Frosty FCB-75 (66 л, +4..+16°C, LED, 0,066 кВт, 430×470×745 мм, 4+1 решетчатые полки) — c5 «Шкаф холодильный для напитков Frosty FCB- 75» (по c7, пробел «FCB- 75»). c36 переведен.
- **r32** SKU=31 ART=2044229779 Frosty SGD250SL барный (227 л, +2..+8°C, 0,245 кВт, 920×515×905 мм, стеклянные раздвижные двери) — c5 «Шкаф барный Frosty SGD250SL». c36 переведен.
- **r33** SKU=32 ART=2048298541 Gooder BBD230H (208 л, 0..+8°C, R600a, 0,133 кВт, 900×520×900 мм, Китай) — c5 «Шкаф холодильный Gooder BBD230H». c36 переведен.

### blknochg (c5==c7 genuine RU, c36 unchanged)

- **r28** SKU=27 ART=1771771748 Whirlpool ADN 140 (со стеклянной дверью) — c5==c7 RU clean.
- **r29** SKU=28 ART=1771823382 Whirlpool ADN 140B (со стеклянной дверью) — c5==c7 RU clean.
- **r30** SKU=29 ART=1775900988 HATA DF200S S/S201 морозильный минибар — c5==c7 RU clean.

**Verify:** 44 PASS / 0 FAIL. Без новых OQ.

**Cumulative chunk-083:** 32/62 (TRIP 16 / blknotrip 0 / blknochg 16 / blkfix 0 / SKIP-НП 0; 160 PASS / 0 FAIL).
