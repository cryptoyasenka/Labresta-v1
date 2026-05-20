# chunk-073 DIFF (W2, продолжение chunk-072)

**Status:** chunk-073 scaffold 0/61 — next b1 (SKU 1-8, rows 2-9)

**Объём:** 61 SKU rows 2..62.

**SKIP-НП preliminary (8 rows):** r13/14/15 FAGOR + r29/30/41/53 HURAKAN + r54 APACH.


## Batch 1 (SKU 1-8, rows 2-9)

### All 8 rows = blknochg (LG/Whirlpool/IRONNETTE прачечное оборудование)
- r2 IRONNETTE 103 HOLEK — гладильный каток (c5/c7 RU equal, c36 RU)
- r3 LG FH069FD3MS (13 кг) — стиральная промышленная
- r4 LG FH0C7FD3MS (18 кг) — стиральная промышленная. **Discrepancy observed:** c5/c7 заголовок «18 кг» vs c35/c36 описание «15-18 кг» — source-quirk, blknochg не правим.
- r5 LG RV1329C4T (15 кг) — промышленная сушильная
- r6 LG RV1329C4T+FH069FD3MS (13 кг) — стирально-сушильный стек. **Discrepancy observed:** c5/c7 модель «RV1329C4T+FH069FD3MS» vs c35/c36 в тексте «RV1329CD7P+FH069FD2FS» — source-quirk (другой код модели в описании), blknochg не правим.
- r7 Whirlpool ADN 488 (150 см) — гладильный каландр
- r8 WHIRLPOOL AWZ9HPS/PRO — сушильная конденсационная с тепловым насосом
- r9 LG RV1840CD4 (17 кг) — сушильная промышленная

### Verify b1: 40 PASS / 0 FAIL


## Batch 2 (SKU 9-16, rows 10-17)

### blknochg 5 (KENLE/LG/Grandimpianti/AGA прачечное)
- r10 KENLE F52 (52 кг) — промышленная стиральная с сенсорным экраном
- r11 LG FH0C7FD2MS+RV1840CD7 (18+17 кг) — стирально-сушильный стек
- r12 Grandimpianti GI 1418 E VT — гладильный каток с многоточечной системой упоров
- r16 AGA E 26 — сушильная индустриальная (AGA Tech SRL)
- r17 AGA E35 — сушильная индустриальная (AGA Tech SRL)

### SKIP-НП 3 (FAGOR прачечное — forward-only)
- r13 FAGOR LA-14 TP2 E — стиральная (Touch Plus, 29 программ, режим АКВАЧИСТКИ)
- r14 Fagor Compact LAP-10 TP2 E P — стиральная высокоскоростной отжим 11 кг
- r15 FAGOR SRP-10 M E COMPACT CONCEPT — сушильная

### Verify b2: 34 PASS / 0 FAIL


## Batch 3 (SKU 17-24, rows 18-25)

### All 8 rows = blknochg (Astra/GGM/AGA/KENLE/Whirlpool прачечное)
- r18 Astra KP-850 — каток гладильный для мини-прачечных/отелей
- r19 GGM MEI1500 (1,5 м) — каток гладильная машина
- r20 GGM MEI1500-33 (1,5 м) — каток гладильная машина
- r21 GGM MEI1250 (1,25 м) — каток гладильная машина
- r22 AGA E75 — сушильная индустриальная (AGA Tech SRL)
- r23 KENLE F22 — стиральная неподрессорная 22-24 кг с ПЛК-контроллером
- r24 Whirlpool ADN 486 (125 см) — гладильный каландр
- r25 Whirlpool ADN 490 (175 см) — гладильный каландр

### Verify b3: 40 PASS / 0 FAIL


## Batch 4 (SKU 25-32, rows 26-33)

### TRIP 4
- **r27 FROSTY BS-018 (пневмовыключатель)** — c5 «Подрібнювач...з пневмовимачем» (UA + typo) → «Измельчитель пищевых отходов FROSTY BS-018 с пневмовыключателем». c36 full RU rewrite (1200 мл, 4000 об/мин, нержавеющая сталь, в комплекте кнопка/шланг 95см/кабель/колено, 188х185x340 мм, 0,55 кВт, 220 В).
- **r31 Hendi 270158 (50 м²)** — c5 UA→RU «Инсектицидная ловушка Hendi 270158 (50 м²)». c36 full RU rewrite (2 УФ-лампы, 2000-2500 V, 335x90x260 мм, 26 Вт).
- **r32 Hendi 270165 (100 м²)** — аналог r31, 485x90x310 мм, 40 Вт.
- **r33 Hendi 270172 (150 м²)** — аналог r31, 640x90x360 мм, 45 Вт.

### blknochg 2
- r26 Whirlpool ADN 491 (200 см) — гладильный каландр
- r28 FROSTY BS-018R с сенсорным выключателем (вариант r27)

### SKIP-НП 2 (HURAKAN)
- r29 HURAKAN HKN-MID80 — инсектицидная лампа (forward-only)
- r30 HURAKAN HKN-FWD450A — измельчитель отходов (forward-only)

### Verify b4: 41 PASS / 0 FAIL
