# chunk-069 MANUAL REVIEW (W2)

**Status:** chunk-069 b2 DONE 16/61 (cum TRIP 6 + blknochg 10 + SKIP-НП 0; 117 PASS) — next b3 (SKU 17-24, rows 18-25)
**Last updated:** chunk-069 b2 DONE 16/61

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

