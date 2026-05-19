# chunk-066 — diff (W2)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-066 (90 SKU, rows 2..91; ART 2496038149 … 2153078504)
**Apply key:** `Артикул` (col1, scoped per row)
**Worker:** W2 (параллельный, диапазон chunk-055 … chunk-085); продолжение chunk-065
**Status:** b5 DONE 40/90 (b6 предстоит; b1..b11 по 8 SKU + b12=SKU89-90 2 SKU)

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


## b3 — SKU 17-24 (rows 18-25) — DONE 24/24 (cum)

**Verify:** REGR 16 (b1+b2) + ART 90 + TRIP 3 + BLKNOCHG 5 = 114 PASS / 0 FAIL.

### blk триплет 3
- **SKU 17 r18 ART 660007483** EWT INOX FY5 для бельгійських (об'ємних) вафель, форма "серце": c5←c7 + c36 ← faithful RU (skel==UA, dims 5×, ° ×1, ASCII " ×2 «сердце»). Source typo «Термоература» → RU «Температура» (повтор b1/b2).
- **SKU 23 r24 ART 2309296632** Млинниця Frosty CMS-400 електрична 1-постова: c5←c7 + c36 ← faithful RU (skel==UA, dims 11×, &delta; / &ordm; / &deg; preserved). «смаженим» → «жареным», «для смаження» → «для жарки». «деревяний шпатель» typo → «деревянный шпатель».
- **SKU 24 r25 ART 2309302468** Млинниця Frosty CMS-400-2 електрична (двопостова &Oslash;400+&Oslash;400): c5←c7 + c36 ← faithful RU (skel==UA, dims 13×, &Oslash; ×2, &delta; ×1, &ordm; ×1, &deg; ×1). Soft-note: source body «1-постова» при модели CMS-400-2 — preserve faithful. «Облданання постачається» typo → RU «Оборудование поставляется».

### blknotrip 0
_(нет)_

### blknochg 5
- **SKU 18 r19 ART 1124671670** GoodFood WB30N (орешница): c5==c7 genuine RU; c35!=c36 (634/643) — fixed НЕ тронут.
- **SKU 19 r20 ART 1110591707** FROSTY VP-81: c5==c7 genuine RU; c35!=c36 (240/251) — fixed НЕ тронут.
- **SKU 20 r21 ART 1110593978** FROSTY VP-2Y40: c5==c7 genuine RU; c35!=c36 (240/251) — fixed НЕ тронут.
- **SKU 21 r22 ART 1489906398** Silver PNK 01 (для панкейков): c5==c7 genuine RU; c35!=c36 (432/443) — fixed НЕ тронут.
- **SKU 22 r23 ART 2126950074** Frosty ECM-400-2 (двопостава, &Oslash;400+&Oslash;400 / &delta;=20): c5==c7 genuine RU; c35!=c36 (498/510) — fixed НЕ тронут.

### SKIP-НП 0
_(нет в b3)_


## b4 — SKU 25-32 (rows 26-33) — DONE 32/32 (cum)

**Verify:** REGR 24 (b1+b2+b3) + ART 90 + TRIP 4 + BLKNOCHG 4 = 221 PASS / 0 FAIL.

### blk триплет 4
- **SKU 26 r27 ART 470824217** AIRHOT BE-1 (однопостова): c5←c7 «Блинница AIRHOT BE-1»; c36 ← faithful RU (skel==UA, dims c35==c36 5×: 390/220/3/490х450х230/18; х Cyr ×4; em-dash ×1; no entities). Паттерны: «Однопостова→Однопостовая», «Діаметр поверхні→Диаметр поверхности», «корпус виготовлений із неіржавкої сталі→корпус выполнен из нержавеющей стали», «жаркова поверхня — з чавуну→жарочная поверхность — из чугуна», «Вага: (без паковання)→Вес: (без упаковки)».
- **SKU 27 r28 ART 470824365** AIRHOT BE-2 (двопостова): c5←c7 «Блинница AIRHOT BE-2»; c36 ← faithful RU (skel==UA, dims 5×: 390/220/6/490х860х230/33). Идентично BE-1 шаблону + «Двопостова→Двухпостовая».
- **SKU 29 r30 ART 660007482** EWT INOX ECM-2 (двома робочими поверхнями): c5←c7 «Блинница электрическая EWT INOX ECM-2»; c36 ← faithful RU (skel==UA, dims 8×: 400/70/300/220/6/450/880/230; х Cyr ×2). «Кожна поверхня має окреме керування→Каждая поверхность имеет отдельное управление», «Температурний режим від 70 до 300 градусів→Температурный режим от 70 до 300 градусов».
- **SKU 30 r31 ART 965420572** EWT INOX ECM-1 (однією робочою): c5←c7 «Блинница электрическая EWT INOX ECM-1»; c36 ← faithful RU (skel==UA, dims 6×: 400/220/3/450/490/230; \n ×4). Source body «Млин електричний» (UA-artifact, alt spelling Млинниця) → faithful RU «Блинница электрическая». «перекидання млинця→переворачивания блина».

### blknotrip 0
_(нет)_

### blknochg 4
- **SKU 25 r26 ART 425078240** GGM CGK40-1: c5==c7 genuine RU; c35!=c36 (291/297) — fixed НЕ тронут; soft-note +6.
- **SKU 28 r29 ART 593835712** GoodFood CM10R: c5==c7 genuine RU; c35!=c36 (377/389) — fixed НЕ тронут; soft-note +12.
- **SKU 31 r32 ART 1399602189** GoodFood CM20R (двупостова→двухпостовая в genuine RU): c5==c7 genuine RU; c35!=c36 (411/405) — fixed НЕ тронут; soft-note -6 (c35 длиннее).
- **SKU 32 r33 ART 1489981958** Silver PNK 04 (для панкейков): c5==c7 genuine RU; c35!=c36 (451/464) — fixed НЕ тронут; soft-note +13.

### SKIP-НП 0
_(нет в b4)_


## b5 — SKU 33-40 (rows 34-41) — DONE 40/40 (cum)

**Verify:** REGR 32 (b1+b2+b3+b4) + ART 90 + TRIP 2 + BLKNOCHG 5 + SKIP-НП 1 = 248 PASS / 0 FAIL.

### blk триплет 2
- **SKU 35 r36 ART 2126943339** Frosty ECM-400-1 (1-постова, &Oslash;400, &delta;=20): c5←c7 «Блинница электрическая Frosty ECM-400-1»; c36 ← faithful RU (skel==UA, dims c35==c36 10×: 400/20/0/300/3,0/220/450/485/240/15.50; &Oslash; ×1, &delta; ×1, &deg; ×2; x Lat ×2 «мм x мм»; * ×2 «Д*Ш*В»; \n ×12). «з антипригарним смаженим покриттям→с антипригарным жареным покрытием», «Гумові ніжки→Резиновые ножки», «Піддон→Поддон», «Тех. дані→Тех. данные», «Розміри (Д*Ш*В)→Размеры (Д*Ш*В)», «корпус: нержавіюча сталь→корпус: нержавеющая сталь». Повтор шаблона b3 SKU23/24 CMS-400.
- **SKU 37 r38 ART 1131916120** Hendi 212028 однопостовая (UA-RU mix в c5/c7 source): c5←c7 «Блинница электрическая Hendi 212028 однопостовая» (preserve verbatim «однопостовая»); c36 ← faithful RU (skel==UA, dims 7×: 400/400/50/250/470x509x/161/3000; lowercase ø ×1 Latin slashed-o, ° symbol ×1, x Lat ×2/х Cyr ×3; \n ×11; ASCII apos `'` ×1 в UA «Дерев'яний» → strip в RU «Деревянный»). «Деко ø400 мм→Противень ø400 мм», «з керамічним покриттям→с керамическим покрытием», «плавним регулюванням→плавной регулировкой», «З захистом від перегріву і термостатом EGО→С защитой от перегрева и термостатом EGО» (последний символ Cyrillic О preserved verbatim).

### blknotrip 0
_(нет)_

### blknochg 5
- **SKU 33 r34 ART 1491737311** GoodFood CM10N: c5==c7 genuine RU; c35!=c36 (379/391) — fixed НЕ тронут; soft-note +12.
- **SKU 34 r35 ART 1973306904** GGM CGJ40-2 (двопостова, 927/974): c5==c7 genuine RU; c35!=c36 (длинный body) — fixed НЕ тронут; soft-note +47.
- **SKU 38 r39 ART 425078241** GGM CGK40-2: c5==c7 genuine RU; c35!=c36 (291/297) — fixed НЕ тронут; шаблон SKU25 b4 GGM CGK40-1.
- **SKU 39 r40 ART 1151639954** Roller Grill CSE 400 (1-постова): c5==c7 genuine RU; c35!=c36 (381/399) — fixed НЕ тронут; soft-note +18.
- **SKU 40 r41 ART 1151641832** Roller Grill CDE 400 (двопостова 2х400 мм): c5==c7 genuine RU; c35!=c36 (406/427) — fixed НЕ тронут; soft-note +21.

### SKIP-НП 1
- **SKU 36 r37 ART 2503734240** HURAKAN HKN-CSE400P (млинниця одинарна): fixed row 37 НЕ тронут, тело из фида НП позже. prelim→confirmed #2.
