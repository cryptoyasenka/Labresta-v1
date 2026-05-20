# chunk-084 — Manual Review (W2)

**Источник:** `chunk-084.xlsx` (71 SKU, rows 2-72)
**Фиксы:** `chunk-084-fixed.xlsx`
**Бранч:** translation-audit/w2 (W2 — параллельный воркер)
**Формат-эталон:** chunk-019 (категории blk триплет / blknotrip / blknochg / blkfix / SKIP-НП).

## Обзор

- 71 SKU rows 2..72
- 0 SKIP-НП preliminary (no HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA detected in c4/c5)
- Батч = 8 SKU; ожидается ~9 батчей (8+8+8+8+8+8+8+8+7)

## Категории

- **blk триплет** (TRIP): c5←c7 + c36 полный RU-перевод тела (c35==c36 source UA)
- **blknotrip**: c5←c7, тело c36 уже RU (без перевода)
- **blknochg**: c5==c7 genuine RU, c36 не менять
- **blkfix**: c5/c36 содержит UA остатки/typo → точечная правка
- **SKIP-НП**: бренд ∈ {HURAKAN, APACH, FAGOR, TATRA, COLD, PROJECT SYSTEMS, ASTORIA, ARRIS, MAXIMA} → ячейки не менять, тело из фида НП позже

## Прогресс

(заполняется по батчам)


## b1 (SKU 1-8, rows 2-9) — DONE 8/71

**Категории:** blk триплет 0 / blknotrip 0 / blknochg 7 / blkfix 1 / SKIP-НП 0.

### blknochg (c5==c7 genuine RU, c36 unchanged)

- **r2** SKU=1 ART=2139115558 Tefcold FS80CP (настольный, 60 л, R600A) — c5==c7 RU clean, c36 RU полный (1165 chars).
- **r3** SKU=2 ART=2139127391 Tefcold SCU1220 — c5==c7 RU clean, c36 RU полный (1079 chars).
- **r4** SKU=3 ART=2139145953 Tefcold FSC100 — c5==c7 RU clean, c36 RU полный (1186 chars). **Замечание (OQ #14):** c35 UA и c36 RU body начинаются с "Шафа/Шкаф ... настільна/настольный FS80CP Tefcold..." — модель в прозе FS80CP, а c4/c5/c6/c7 = FSC100. Source typo (либо прозу скопировали с r2, либо c4-c7 ошибочно). Не правлено (blknochg forward-only).
- **r5** SKU=4 ART=2140074926 Tefcold VOC100 (холодильник для напитков) — c5==c7 RU clean, c36 RU полный (901 chars).
- **r7** SKU=6 ART=2141740167 Tefcold UF200V морозильный — c5==c7 RU clean, c36 RU полный (1166 chars).
- **r8** SKU=7 ART=2141746935 Tefcold UF200VS морозильный — c5==c7 RU clean, c36 RU полный (1145 chars).
- **r9** SKU=8 ART=2141750051 Tefcold UF100GCP морозильный — c5==c7 RU clean, c36 RU полный (1017 chars).

### blkfix (точечная правка c36 prose)

- **r6** SKU=5 ART=2141730389 Tefcold UF50GCP морозильный (48 л, R290, 154 Вт) — c5==c7 RU clean (no change), но c36 RU **начиналась с тела другого продукта** "Морозильный шкаф GoodFood RTD99L &ndash; профессиональное коммерческое..." (это body GoodFood RTD99L из chunk-083 r25). Specs list в c36 матчил c35 UF50GCP (R290, 48 л, 154 Вт), но prose-первый параграф contaminated. Переписан prose как faithful RU UA→RU c35: "Шкаф морозильный настольный UF50GCP Tefcold предназначен для кратковременного хранения, экспонирования и продажи продуктов." + полный список спеков. Новая длина c36: 908. **Замечание (OQ #15).**

### Открытые вопросы (новые в b1)

- **OQ #14 (W2 cum #14):** r4 SKU=3 Tefcold FSC100 — body prose (c35 UA + c36 RU faithfully translated) ссылается на модель "FS80CP" вместо "FSC100". Source feed contamination. Specs (60 л, +2..+10°C, R600A, 655×390×930, 46 кг) совпадают со специфическими параметрами FSC100, либо это дубликат body r2 FS80CP. Требует Yana подтверждения какая прозу-стартовая модель правильная.
- **OQ #15 (W2 cum #15):** r6 SKU=5 Tefcold UF50GCP — c36 RU исходно содержал body GoodFood RTD99L (chunk-083 r25). Translator copy-paste error / source contamination. Body переписан в b1 как faithful RU перевод c35. Yana может проверить точность нового RU prose.

**Verify:** 28 PASS / 0 FAIL.

**Cumulative chunk-084:** 8/71 (TRIP 0 / blknotrip 0 / blknochg 7 / blkfix 1 / SKIP-НП 0; 28 PASS / 0 FAIL).


## b2 (SKU 9-16, rows 10-17) — DONE 16/71

**Категории:** blk триплет 4 / blknotrip 0 / blknochg 4 / blkfix 0 / SKIP-НП 0.

### blk триплет (c5←c7 + c36 полный RU-перевод тела)

- **r14** SKU=13 ART=1407668964 FROSTY SGD150 (барный минибар, 142 л, +2..+8°C, 0,2 кВт, 600×515×905) — c5 UA "Шафа барна FROSTY SGD150" → "Шкаф барный FROSTY SGD150"; c35==c36 source оба UA → c36 переведён полностью (445 chars).
- **r15** SKU=14 ART=1553834006 Forcar G-ER200GSS нерж (мини-холодильник, 130 л, +2..+8°C, R600А, 220 В, 600×585×855) — c5 UA → "Шкаф холодильный Forcar G-ER200GSS нерж"; c36 переведён (654 chars; source имел &#39;, в новом RU без него).
- **r16** SKU=15 ART=2106844926 Frosty FTD200GSS (холодильный шкаф, 127 л, 0/+8°C, 0,20 кВт/220В, 600×635×835, 39 кг) — c5 UA → "Шкаф холодильный Frosty FTD200GSS"; c36 переведён (813 chars).
- **r17** SKU=16 ART=2336659589 Forcar G-EF200GSS (морозильный шкаф, 130 л, -18..-22°C, R290, 0.36 кВт/220V, 600×585×855, 44 кг, Италия) — c5 UA → "Шкаф морозильный Forcar G-EF200GSS"; c36 переведён полный (1160 chars, включая блок размеров в упаковке).

### blknochg (c5==c7 genuine RU, c36 unchanged)

- **r10** SKU=9 ART=2141758489 Tefcold UF200VG морозильный — c5==c7 RU clean, c36 RU полный (1159 chars).
- **r11** SKU=10 ART=2143864042 Tefcold UF200VSG морозильный — c5==c7 RU clean, c36 RU полный (1171 chars).
- **r12** SKU=11 ART=2143869122 Tefcold GF200VSG (настольный охладитель бокалов) — c5==c7 RU clean, c36 RU полный (1248 chars).
- **r13** SKU=12 ART=1365900407 Forcar G-EF200 (барный морозильный) — c5==c7 RU clean, c35==c36 оба RU (поставщик сразу подал RU body, без UA-исходника).

**Verify:** 40 PASS / 0 FAIL. Без новых OQ.

**Cumulative chunk-084:** 16/71 (TRIP 4 / blknotrip 0 / blknochg 11 / blkfix 1 / SKIP-НП 0; 68 PASS / 0 FAIL).


## b3 (SKU 17-24, rows 18-25) — DONE 24/71

**Категории:** blk триплет 6 / blknotrip 0 / blknochg 2 / blkfix 0 / SKIP-НП 0.

### blk триплет (c5←c7 + c36 полный RU-перевод)

- **r19** SKU=18 ART=659974142 Hendi 525630 — щётка для чистки печей для пиццы, латунная проволока, стальной скребок, деревянная ручка с болтовым креплением, 255×1030 мм. c36 len=198.
- **r20** SKU=19 ART=1162911905 Hendi 617700 — щипцы-держатель форм для пиццы, никелированная сталь, длина 190 мм. c36 len=145.
- **r21** SKU=20 ART=2103339094 Gi Metal AC-SP — щётка для чистки печи, поворотная прямоугольная со скребком, медная щетина, деревянная основа, анодированная синяя ручка, общая длина 1600 мм, вес 0.67 кг. c5←c7 verbatim с Latin "c" в "чиcтки" (source typo, OQ #16). c36 len=407.
- **r23** SKU=22 ART=2103354458 Gi Metal ACH-SP — щётка поворотная прямоугольная (50×160 мм), ручка 1270 мм, медная щетина / деревянная основа / алюминиевая ручка, 0.56 кг. c5 Latin c. c36 len=334.
- **r24** SKU=23 ART=2103358291 Gi Metal AC-SPN2 — щётка поворотная прямоугольная со скребком (60×200 мм), ручка 1600 мм, натуральная щетина / деревянная основа / анодированная синяя ручка, 0.67 кг. c5 Latin c. c36 len=359.
- **r25** SKU=24 ART=2103360984 Gi Metal AC-SPG2 — щётка для гриля, н/с щетина, ручка из высокопрочного полимера, 310×60 мм, 0,290 кг. c36 len=379. (NB: source имеет внутреннее противоречие — intro «щетиною з нержавіючої сталі» vs spec «Залізна щетина»; переведено faithfully.)

### blknochg (c5==c7 genuine RU, c36 unchanged)

- **r18** SKU=17 ART=2106843857 Frosty FTD200SS — c5==c7 RU clean, c36 RU полный (821 chars).
- **r22** SKU=21 ART=2103351965 Gi Metal AC-SPT — c5==c7 (оба с Latin c "чиcтки"), c36 RU полный (340 chars, source имеет Ё — не правлено, blknochg).

### Открытые вопросы (новые в b3)

- **OQ #16 (W2 cum #16):** r21/r22/r23/r24 SKU=20/21/22/23 — c7 RU (и c5 после ←c7) содержит "Щетка для чиcтки" с Latin "c" вместо Cyrillic "с". Source typo в feed RU. Per rule c5←c7 verbatim — Latin c пропагирован в c5. В новом c36 RU использован правильный Cyrillic "чистки". Yana может решить, нужно ли фиксить c7 в исходном фиде.

**Verify:** 48 PASS / 0 FAIL.

**Cumulative chunk-084:** 24/71 (TRIP 10 / blknotrip 0 / blknochg 13 / blkfix 1 / SKIP-НП 0; 116 PASS / 0 FAIL).


## b4 (SKU 25-32, rows 26-33) — DONE 32/71

**Категории:** blk триплет 2 / blknotrip 0 / blknochg 6 / blkfix 0 / SKIP-НП 0.

### blk триплет (c5←c7 + c36 полный RU-перевод тела)

- **r26** SKU=25 ART=2103366019 Gi Metal AC-SPGT2 — щетка для гриля со щетиной из нержавеющей стали и ручкой из высокопрочного полимера, размер 310×60 мм, вес 0,290 кг. c35==c36 source UA → c36 переведен полностью (401 chars). NB: source имеет внутреннее противоречие (intro «нержавіюча сталь» vs spec «Залізна щетина») — переведено faithfully.
- **r30** SKU=29 ART=2106846093 FROSTY FL-58 (шкаф настольный холодильный, 58 л, 0..+12°C, 0,19 кВт, 452×406×816 мм, стекло с 4 сторон, LED-подсветка, 2 полки, черный) — c5 UA → "Шкаф-витрина холодильная FROSTY FL-58, black"; c35==c36 source UA с &#39; → c36 переведен полностью (521 chars, без &#39;).

### blknochg (c5==c7 genuine RU, c36 unchanged)

- **r27** SKU=26 ART=2106845076 FROSTY RT58L-1D (черная с замком) — c5==c7 RU clean, c36 RU полный (609 chars).
- **r28** SKU=27 ART=2106850214 FROSTY RT78L-1D — c5==c7 RU clean, c36 RU полный (627 chars).
- **r29** SKU=28 ART=2106852266 FROSTY RT280L (кондитерский демонстрационный) — c5==c7 RU clean, c36 RU полный (530 chars).
- **r31** SKU=30 ART=2106848574 FROSTY FL-98 (шкаф настольный, аналог FL-58) — c5==c7 RU clean, c36 RU полный (523 chars).
- **r32** SKU=31 ART=2106849283 FROSTY FL238 — c5==c7 RU clean, c36 RU полный (529 chars).
- **r33** SKU=32 ART=2106850943 FROSTY RT235L (кондитерский демонстрационный) — c5==c7 RU clean, c36 RU полный (555 chars).

**Verify:** 40 PASS / 0 FAIL. Без новых OQ.

**Cumulative chunk-084:** 32/71 (TRIP 12 / blknotrip 0 / blknochg 19 / blkfix 1 / SKIP-НП 0; 156 PASS / 0 FAIL).


## b5 (SKU 33-40, rows 34-41) — DONE 40/71

**Категории:** blk триплет 3 / blknotrip 0 / blknochg 5 / blkfix 0 / SKIP-НП 0.

### blk триплет (c5←c7 + c36 полный RU-перевод тела)

- **r34** SKU=33 ART=2072212305 Frosty FL218 black (холодильный шкаф, 218 л, стекло 4 стороны, 0..+12°C, 0,25 кВт/220В, 515×485×1595 мм, 73 кг) — c5 UA → "Шкаф холодильный Frosty FL218 black"; c35==c36 source UA с &#39; → c36 переведен полностью (825 chars).
- **r39** SKU=38 ART=641916589 REEDNEE RT78B white (шкаф-витрина настольный холодильный, R600a, 78 л, 0..+12°C, 0,17 кВт, 428×386×960 мм) — c5 UA → "Шкаф-витрина холодильная REEDNEE RT78B white"; c35==c36 UA → c36 переведен (524 chars). **NB: source h2 ссылается на «REEDNEE RT78L», а c4/c5/c7 = RT78B — source typo, переведено faithfully (OQ #17).**
- **r40** SKU=39 ART=930809748 REEDNEE RT98B white (шкаф-витрина настольный холодильный, двойное стекло, 98 л, 4 полки, замок, 0,17 кВт, 428×386×1110 мм) — c5 UA → "Шкаф-витрина холодильная REEDNEE RT98B white"; c35==c36 UA с &#39; → c36 переведен (619 chars).

### blknochg (c5==c7 genuine RU, c36 unchanged)

- **r35** SKU=34 ART=2072213285 Frosty FL288 black — c5==c7 RU clean, c36 RU полный (848 chars).
- **r36** SKU=35 ART=2219904786 SCAN RTC 237 we (витрина холодильная) — c5==c7 RU clean, c36 RU полный (560 chars).
- **r37** SKU=36 ART=665783835 FROSTY RT235L white (кондитерский) — c5==c7 RU clean, c36 RU полный (502 chars).
- **r38** SKU=37 ART=498259916 FROSTY RT78L-1D белая с замком — c5==c7 RU clean, c36 RU полный (590 chars).
- **r41** SKU=40 ART=1086819137 GoodFood RT78L черная — c5==c7 RU clean, c36 RU полный (828 chars, source c35 UA но c36 already translated).

### Открытые вопросы (новые в b5)

- **OQ #17 (W2 cum #17):** r39 SKU=38 REEDNEE RT78B white — source c35/c36 h2 содержит «REEDNEE RT78L» вместо RT78B (c4/c5/c7 = RT78B). Likely source typo в UA prose. Переведено faithfully (RU h2 также "REEDNEE RT78L"). Yana может решить, нужно ли поправить c36 RU модель на RT78B.

**Verify:** 44 PASS / 0 FAIL.

**Cumulative chunk-084:** 40/71 (TRIP 15 / blknotrip 0 / blknochg 24 / blkfix 1 / SKIP-НП 0; 200 PASS / 0 FAIL).
