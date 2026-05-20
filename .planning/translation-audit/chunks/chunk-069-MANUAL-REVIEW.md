# chunk-069 MANUAL REVIEW (W2)

**Status:** chunk-069 b5 DONE 40/61 (cum TRIP 11 + blknochg 24 + SKIP-НП 5; 187 PASS) — next b6 (SKU 41-48, rows 42-49)
**Last updated:** chunk-069 b5 DONE 40/61

## Структура

- Источник: `chunk-069.xlsx` (RO)
- Operating target: `chunk-069-fixed.xlsx` (gitignored, скопирован из source при scaffold)
- Diff: `chunk-069-diff.md`
- Glossary: см. сводный `chunk-glossary-w2.md`
- Questions: `chunk-069-questions.md` (создаётся только при возникновении вопросов)

## Категории SKU (как в chunk-019/067/068)

- **TRIP**: c5←c7 + c36 ← faithful RU body (skel preserved + dims preserved + no UA-mark + no Ё)
- **blknotrip**: c5←c7 only, c36 без изменений (когда c36 уже RU OK)
- **blknochg**: c5/c7/c36 без изменений (когда уже всё RU OK / source genuine)
- **SKIP-НП**: forward-only override, brand ∈ {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA} → fixed строка НЕ тронута

## Constraints (carry-over из chunk-068)

1. Source typos faithful: c5/c4/c6 — preserved verbatim; c36 body — preserved structural typos, fix только letter-misses в russian переводе.
2. Без Ё в RU c36: «Объем», «Ерш», «щеточки», «ножки», никогда Ё/ё.
3. UA `&#39;` → RU без апостр (drop).
4. «тэн» через «э».
5. «мытья» vs «мойки»: c5 ← c7 verbatim per row, не унифицировать между строками.
6. `<h2>` open+close adds 2× «2» dim tokens; preserve в skel.
7. Asber/ASBER: c5 source variants («Посудомийка купольна») перезаписываются по c7 standard «Посудомоечная машина ASBER ...» (live-store uniform).
8. Об'єм (RD) vs Ємність (DD): preserve ASBER source variant per row.
9. ATA/OZTI/Ozti/ADLER/Gooder/GGM/GGG/Hendi/Krupps brands НЕ в списке НП-эксклюзивных, обрабатываются обычно.
10. chunk-NN.xlsx source RO; modify chunk-NN-fixed.xlsx (gitignored *.XLSX).
11. W2 range: chunk-055..chunk-085 ONLY.
12. Use .planning/CURRENT-w2.md (NOT CURRENT.md = W1).
13. Batch = 8 SKU; 2 commits per batch (C1 content + C2 marker); push after C2.

## Батчи

chunk-069 = **61 SKU**, batches 8+8+8+8+8+8+8+5 (b1..b8):
- b1: SKU 1-8, rows 2-9
- b2: SKU 9-16, rows 10-17
- b3: SKU 17-24, rows 18-25
- b4: SKU 25-32, rows 26-33
- b5: SKU 33-40, rows 34-41
- b6: SKU 41-48, rows 42-49
- b7: SKU 49-56, rows 50-57
- b8: SKU 57-61, rows 58-62 (финал, 5 SKU)

## b1 (SKU 1-8, rows 2-9) — DONE 8/61

**Категории:** TRIP 4 + blknotrip 0 + blknochg 4 + SKIP-НП 0 = 8/8. Verify **101 PASS / 0 FAIL**.

**blknochg (4):**
- r2 SKU1 ART 2434135469 **ATA AT 901 купольная** (16-li body, кошик 500x500): c5==c7 RU OK, skel-eq True, dims-eq True; fixed НЕ изменена.
- r3 SKU2 ART 2434148483 **ATA AT 951 купольная** (16-li body): c5==c7 RU OK, skel-eq True, dims-eq True; fixed НЕ изменена.
- r4 SKU3 ART 2434159376 **ATA B 51 купольная** (16-li body): c5==c7 RU OK, skel-eq True, dims-eq True; fixed НЕ изменена.
- r5 SKU4 ART 2434170153 **Elframo LP 61 VE котломоечная** (11-nl body): c5==c7 RU OK, skel-eq True, dims-eq True; fixed НЕ изменена.

**TRIP (4) — c35==c36 UA duplicated, обе колонки переведены:**
- r6 SKU5 ART 651352472 **Krupps S1100E купольная** (inline body): c5←c7 «Посудомоечная машина Krupps S1100E купольная»; c36 ← faithful RU (1527 chars UA → RU, 13 li tech-char, dims `1/1.,415,310,390,4,60/40/30/15,60/90/120/240,1,26,60х50х10,1,18,50х50х10,1,4,1,1,18,620х7700х1900,9,0,380,2`).
- r7 SKU6 ART 664883808 **Krupps EL991E ELITECH котломоечная фронтальная** (inline body, 2684 chars): c5←c7 «(серия ELITECH LINEl) для габаритной посуды»; c36 ← faithful RU (11 li tech-char, ELITECH/Acquatech System/ХАССП/Wi-Fi IKLOUD).
- r8 SKU7 ART 664883809 **Krupps S540E фронтальная** (inline body): c5←c7; c36 ← faithful RU (11 li tech-char, UNIKO-MID/умягчитель).
- r9 SKU8 ART 923572273 **Krupps K1500E Koral купольная** (16-nl body): c5←c7 «(серия Koral)»; c36 ← faithful RU (16 li tech-char, `<strong>` blocks preserved, Перистальтический/Termostop, dims `500x600x410,1/1,600×400.,400,310,395,60,1320,60/90/120/300,500х600,...,720x770x1435/1900,7,04,4,5,5,4,1,64,380,2`).

**TRIP:** 4. **SKIP-НП:** 0. **OQ:** 0.

**Verify breakdown:** 61 ART regression + 4 blknochg × 3 = 12 + 4 TRIP × 7 = 28 = **101 PASS / 0 FAIL**.

**Cum после b1:** TRIP 4 + blknotrip 0 + blknochg 4 + SKIP-НП 0 = **8/61**. Next b2 (SKU 9-16, rows 10-17).

## b2 (SKU 9-16, rows 10-17) — DONE 16/61

TRIP 2 + blknochg 6 + SKIP-НП 0 = 8/8. Verify **117 PASS / 0 FAIL**.

**TRIP (2):**
- r10 SKU9 ART 923587067 **Krupps EVO121 туннельная** (c35==c36 UA dup, 1149 chars, 14 nl): c5←c7; c36 ← faithful RU body (EVOLUTION линия, 11 li + 3 ol, dims `60/120/500х500/450/500x500x100/18/500x500x100/4/1750x770x1825/24,2/1,5/2,0/10,5`).
- r14 SKU13 ART 1519082393 **Krupps EL951E** (c35==c36 UA dup, 490 chars, 11 nl): c5←c7; c36 ← faithful RU body (10 li tech-char, dims `951/670х600/120/150/240/540/445/2/775х810х1360/7,4/380`).

**blknochg (6):**
- r11 SKU10 ART 1152270353 Winterhalter UCM Glasswasher фронтальная: c5==c7 RU OK, c36 без UA-mark, skel-eq False source variance; fixed НЕ изменена.
- r12 SKU11 ART 1160729445 Krupps C537S DGT Advance фронтальная: c5==c7 RU OK; fixed НЕ изменена.
- r13 SKU12 ART 1264689042 Oztiryakiler OBM1080DPD купольная: c5==c7 RU OK; fixed НЕ изменена.
- r15 SKU14 ART 1813450895 Ozti OBM 1080D PDRT помпа слива купольная: c5==c7 RU OK; fixed НЕ изменена.
- r16 SKU15 ART 1943696404 Ozti OBM 1080D PDT помпа слива купольная: c5==c7 RU OK; fixed НЕ изменена.
- r17 SKU16 ART 2045404308 Empero EMP.2000-SAG-R: c5==c7 RU OK; fixed НЕ изменена.

**SKIP-НП:** 0. **OQ:** 0.

**Cum после b2:** TRIP 6 + blknotrip 0 + blknochg 10 + SKIP-НП 0 = **16/61**.

## b3 (SKU 17-24, rows 18-25) — DONE 24/61

TRIP 3 + blknotrip 0 + blknochg 4 + SKIP-НП 1 = 8/8. Verify **179 PASS / 0 FAIL**.

**TRIP (3):**
- r20 SKU19 ART 2126106102 **Krupps EL985E (котломоечная) для габаритной посуды** (c35==c36 UA dup, 2639 chars, инлайн body): c5←c7 «Посудомоечная машина Krupps EL985E (котломоечная) для габаритной посуды»; c36 ← faithful RU body (`<h2>` + 3 `<p>` + `<ul>` с 11 li tech-char). Содержит UNIKO/ELITECH/Acquatech System/Wi-Fi IKLOUD/Termostop/ХАССП. Dims: 30 корзин/час, 1780 тарелок/час, 700×825×655(h), 680мм, 850x725x100, 1000x860x1805, 13 кВт, 380 В, 2,5-3,0 л, 120/150/240/540 сек. UA «м&#39;ясних» → «мясных» (drop apostrophe). UA «електроененергії» (typo extra «не») → «электроэнергии» (letter-miss fix). Без Ё.
- r22 SKU21 ART 2538744328 **Frosty AP1 400V котломоечная** (c35==c36 UA dup, 3255 chars, 12 `<p>` + 4 `<ul>` структура): c5←c7 «Машина котломоечная Frosty AP1 400V»; c36 ← faithful RU body. h=650 мм, размеры 720×780×1730 мм, корзина 560х630х100h, 9,9 кВт/380В, 30 корзин/час, 26 тарелок (опц.), 37 л бак, soft touch, AISI 304. UA typo «дл» (3 дл 6 л) → «до» (3 до 6 л) letter-miss fix. UA «обсяг» → «объем» (без Ё). UA «&ordm;С» preserved. Без Ё.
- r23 SKU22 ART 2538759109 **Frosty AP2 400V котломоечная** (c35==c36 UA dup, 3255 chars, тот же template как r22): c5←c7 «Машина котломоечная Frosty AP2 400V»; c36 ← faithful RU body. h=850 мм (versus r22 650), размеры 720×780×1930 (versus r22 1730), всё остальное идентично. Без Ё.

**blknochg (4):**
- r18 SKU17 ART 2045406113 Empero EMP.3000-SAG-R: c5==c7 RU OK, c36 без UA-mark, fixed НЕ изменена.
- r19 SKU18 ART 2110099464 Empero EMP.1000-F: c5==c7 RU OK; fixed НЕ изменена.
- r21 SKU20 ART 2191298201 Empero EMP.1000-SDF: c5==c7 RU OK; fixed НЕ изменена.
- r25 SKU24 ART 1548982581 Frosty C18 камерный вакуумный упаковщик: c5==c7 RU OK, c36 без UA-mark; fixed НЕ изменена.

**SKIP-НП (1):**
- r24 SKU23 ART 1168653006 **HURAKAN HKN-CNW460 PRO** термоупаковочный аппарат (Стол горячий): brand HURAKAN ∈ SKIP-НП list → forward-only, fixed строка НЕ тронута (тело из НП-фида позже). c5 src «Термопакувальний апарат Hurakan HKN-CNW460 PRO*» содержит UA «Термопакувальний» и звездочку — НЕ переписываем.

**OQ:** 0.

**Verify breakdown:** 61 ART regression + 4 b1-TRIP × 4 (modified c5/c36 + no-UA + no-Ё) = 16 + 4 b1-blknochg × 3 = 12 + 2 b2-TRIP × 4 = 8 + 6 b2-blknochg × 3 = 18 + 4 b3-blknochg × 4 (c5/c36/c7 + RU OK) = 16 + 1 SKIP-НП × 7 (all cols) = 7 + 3 b3-TRIP × ~14 (c5 match + body content checks + skel-eq + dim differentials) ≈ 41 = **179 PASS / 0 FAIL**.

**Cum после b3:** TRIP 9 + blknotrip 0 + blknochg 14 + SKIP-НП 1 = **24/61**. Next b4 (SKU 25-32, rows 26-33).

## b4 (SKU 25-32, rows 26-33) — DONE 32/61

TRIP 2 + blknotrip 0 + blknochg 5 + SKIP-НП 1 = 8/8. Verify **179 PASS / 0 FAIL**.

**TRIP (2):**
- r29 SKU28 ART 489839797 **REEDNEE SW450L «горячий стол»** (c35==c36 UA dup, 584 chars, h2+7 li): c5←c7 «Упаковщик "горячий стол" REEDNEE SW450L»; c36 ← faithful RU body. Тефлоновая поверхность 390х124 мм, ширина пленки 450 мм, температура 70-90°С, термонож, стретч-пленка ПВХ 380/400/430/450 мм, вес 7 кг, габариты 620x515x160 мм. Без Ё.
- r30 SKU29 ART 490566373 **Lavezzini Gofer 200x400 пакеты гофрированные** (c35==c36 UA dup, 148 chars, p+3 li): c5←c7 «Пакеты гофрированные Lavezzini 200x400 (упаковка 100 шт.)» (источник c5 был «Пакет Lavezzini Gofer 200x400 ( пакунок 100 шт.)» — UA «пакунок», переписали по c7); c36 ← faithful RU body «Пакеты гофрированные для вакуумного упаковщика. упаковка 100 шт. материал — полиэтилен размер 200х400 мм».

**blknochg (5):**
- r27 SKU26 ART 454521621 GGM VTB320 вакуумный упаковщик 16 л/мин: c5==c7 RU OK; fixed НЕ изменена.
- r28 SKU27 ART 454521622 GGM VTB420 вакуумный упаковщик 28 л/мин: c5==c7 RU OK; fixed НЕ изменена.
- r31 SKU30 ART 490575794 Frosty 150x250 пакеты гофрированные: c5==c7 RU OK; fixed НЕ изменена.
- r32 SKU31 ART 490581287 Frosty 200x300 пакеты гофрированные: c5==c7 RU OK; fixed НЕ изменена.
- r33 SKU32 ART 490587113 Frosty 250x350 пакеты гофрированные: c5==c7 RU OK; fixed НЕ изменена.

**SKIP-НП (1):**
- r26 SKU25 ART 2060699885 **HURAKAN HKN-CNW430** термоупаковочная машина: brand HURAKAN ∈ SKIP-НП list → forward-only, fixed строка НЕ тронута.

**OQ:** 0.

**Cum после b4:** TRIP 11 + blknotrip 0 + blknochg 19 + SKIP-НП 2 = **32/61**. Next b5 (SKU 33-40, rows 34-41).

## b5 (SKU 33-40, rows 34-41) — DONE 40/61

TRIP 0 + blknotrip 0 + blknochg 5 + SKIP-НП 3 = 8/8. Verify **187 PASS / 0 FAIL**. Чисто SKIP-НП + blknochg батч, ни одного TRIP — никаких изменений в chunk-069-fixed.xlsx.

**blknochg (5):**
- r34 SKU33 ART 490598501 Frosty 300x400 пакеты гофрированные (паковання 100 шт./полиэтилен/300х400): c5==c7 RU OK, c36 без UA-mark; fixed НЕ изменена.
- r35 SKU34 ART 568706697 Orved Evox 30 вакуумный упаковщик 8м3/час: c5==c7 RU OK; fixed НЕ изменена.
- r36 SKU35 ART 593842902 GGM VMKH-300 вакуумный упаковщик 14,4 м3/час: c5==c7 RU OK; fixed НЕ изменена.
- r37 SKU36 ART 593842903 GGM VMKH-400Z вакуумный упаковщик 20 м3/час: c5==c7 RU OK; fixed НЕ изменена.
- r41 SKU40 ART 646844865 PERS.PETROS LEVAC 3 вакуумный упаковщик: c5==c7 RU OK; fixed НЕ изменена.

**SKIP-НП (3) — Apach forward-only:**
- r38 SKU37 ART 639913421 **Apach AVM254** вакуумный пакувальник 4 м³/час: brand Apach ∈ SKIP-НП list → forward-only, fixed строка НЕ тронута. c5/c35/c36 source содержат UA «Вакуумний пакувальник», «м3/год» — НЕ переписываем.
- r39 SKU38 ART 639913422 **Apach AVM308** вакуумный пакувальник 8 м³/час: brand Apach → SKIP-НП. fixed НЕ тронута.
- r40 SKU39 ART 639913425 **Apach AVM412** вакуумный пакувальник 12 м³/час: brand Apach → SKIP-НП. fixed НЕ тронута.

**OQ:** 0.

**Cum после b5:** TRIP 11 + blknotrip 0 + blknochg 24 + SKIP-НП 5 = **40/61**. Next b6 (SKU 41-48, rows 42-49).

