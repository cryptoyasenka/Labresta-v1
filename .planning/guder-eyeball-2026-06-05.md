# guder — NEEDS-EYEBALL refinement (2026-06-05)

Read-only refinement of the 36 doubtful `guder` candidates from the **NEEDS-EYEBALL** bucket of
`candidate-triage-2026-06-05.md` (the 44 clean confirms already live in the recommend-CONFIRM bucket).
No DB or other file was modified. Every row below was verified against `product_matches` (correct
pp_id/sp_id, all `status=candidate`, all 36 present).

**Key DB finding:** zero 1:1 (#15) conflicts — no PP in this set is held by any `confirmed`/`manual`
match, and no SP is held elsewhere. The task brief anticipated ~20 #15 rejects; there are **none**.
All rejects here are domain mismatches (rule b). Two SPs are multi-mapped *within* this candidate set
(7196 → m3831+m3832; 7086 → m4383+m3805+m3806) — the wrong members are rejected on domain grounds,
which also resolves those many-to-1 collisions.

Counts: **36 total — CONFIRM 6 / CONFIRM(judgment) 21 / AMBIGUOUS 4 (3 saladette + 1 redundant) / REJECT 5.**

The dominant pattern: the supplier (guder) names equipment by **temperature class** while the catalog
names it by **function** — `Шафа низькотемпературна`=`Морозильна шафа` (freezer), `Шафа
середньотемпературна`=`Холодильна шафа` (chiller), `Стіл … низькотемпературний`=`Стіл морозильний`.
These are domain synonyms with byte-identical model codes → CONFIRM(judgment). Some SP names carry the
Cyrillic-о homoglyph `Goоder` (rule (c) explicitly allows homoglyphs).

| match_id | PP (brand + key tokens) | SP (brand + key tokens) | score | 1:1 | REC | reason |
|---:|---|---|---:|:--:|:--|---|
| 3831 | Gooder · Морозильна шафа UDD 370 DTK **BK** | Gooder · Шафа низькотемп. UDD 370 DTK | 100 | clear | REJECT | BK variant suffix on PP; SP=7196 is non-BK unit (correct for m3832) — domain/suffix |
| 3832 | Gooder · Морозильна шафа UDD 370 DTK | Gooder · Шафа низькотемп. UDD 370 DTK | 100 | clear | CONFIRM(judgment) | model UDD 370 DTK identical; freezer≈low-temp synonym |
| 3834 | Gooder · Шафа холодильна USS 374 DTK | Gooder · Шафа середньотемп. USS 374 DTK | 100 | clear | CONFIRM(judgment) | model USS 374 DTK identical; chiller≈mid-temp synonym |
| 3835 | Gooder · Шафа холодильна USS 1200 DSC | Gooder · Шафа середньотемп. USS 1200 DSC | 100 | clear | CONFIRM(judgment) | model USS 1200 DSC identical; chiller≈mid-temp synonym |
| 4382 | (no brand) · Точильний камінь KING K80 #250/1000 | Gooder · ВІТРИНА ХОЛОДИЛЬНА КУПЕЦ ВХСп-1,25 | 100 | n/a | REJECT | sharpening stone vs fridge display; matched on junk article 125 — domain |
| 4383 | (no brand) · Точильний камінь KING DX1000 #1000 | Gooder · ВІТРИНА ХОЛОДИЛЬНА VSo-0,95 VENETO | 100 | n/a | REJECT | sharpening stone vs fridge display; junk article 123 — domain |
| 4403 | Gooder · Вітрина холодильна XCW-100L | Gooder · Вітрина холодильна настільна XCW-100L | 100 | clear | CONFIRM | same type word + model XCW-100L; SP adds "настільна"; Goоder homoglyph |
| 4404 | Gooder · Вітрина холодильна XCW-120LS | Gooder · Вітрина холодильна настільна XCW-120LS | 100 | clear | CONFIRM | identical modulo "настільна" + homoglyph |
| 4405 | Gooder · Вітрина холодильна XCW-160LS | Gooder · Вітрина холодильна настільна XCW-160LS | 100 | clear | CONFIRM | identical modulo "настільна" + homoglyph |
| 4406 | Gooder · Вітрина холодильна XCW-120 CUBE | Gooder · Вітрина холодильна настільна XCW-120 CUBE | 100 | clear | CONFIRM | identical modulo "настільна" |
| 4407 | Gooder · Вітрина холодильна XCW-160 CUBE | Gooder · Вітрина холодильна настільна XCW-160 CUBE | 100 | clear | CONFIRM | identical modulo "настільна" + homoglyph |
| 4430 | Gooder · Морозильна шафа BF400VG | Gooder · Шафа низькотемп. BF400VG | 100 | clear | CONFIRM(judgment) | model BF400VG identical; freezer≈low-temp synonym |
| 4433 | Gooder · Вітрина холодильна XCW-200 CUBE | Gooder · Вітрина холодильна настільна XCW-200 CUBE | 100 | clear | CONFIRM | identical modulo "настільна" |
| 3856 | Gooder · Моноблок морозильний SGL017P | Gooder · Моноблок SGL017P | 95 | clear | CONFIRM(judgment) | model SGL017P identical; SP drops temp qualifier |
| 4421 | Gooder · Моноблок холодильний SGM020P | Gooder · Моноблок SGM020P | 95 | clear | CONFIRM(judgment) | model SGM020P identical; SP drops temp qualifier |
| 3805 | Gooder · Холодильна шафа BR400V | Gooder · ВІТРИНА ХОЛОДИЛЬНА VSo-0,95 VENETO | 86 | n/a | REJECT | fridge cabinet vs VENETO display; junk article 123 — domain |
| 3806 | Gooder · Холодильна шафа BR400VG | Gooder · ВІТРИНА ХОЛОДИЛЬНА VSo-0,95 VENETO | 86 | n/a | REJECT | fridge cabinet vs VENETO display; junk article 123 — domain |
| 4414 | Gooder · Стіл холодильний GN2100TN | Gooder · Стіл холодильний середньотемп. GN2100TN | 86 | clear | CONFIRM(judgment) | model GN2100TN identical; both "холодильний", SP adds temp class |
| 4415 | Gooder · Стіл морозильний GN2100ВТ | Gooder · Стіл холодильний низькотемп. GN2100ВТ | 86 | clear | CONFIRM(judgment) | model GN2100ВТ identical; freezer≈low-temp synonym |
| 4416 | Gooder · Стіл морозильний GN3100ВТ | Gooder · Стіл холодильний низькотемп. GN3100ВТ | 86 | clear | CONFIRM(judgment) | model GN3100ВТ identical; freezer≈low-temp synonym |
| 4417 | Gooder · Стіл морозильний GN4100ВТ | Gooder · Стіл холодильний низькотемп. GN4100ВТ | 86 | clear | CONFIRM(judgment) | model GN4100ВТ identical; freezer≈low-temp synonym |
| 4400 | Gooder · Вітрина холодильна VRX2000/330 | Gooder · Вітрина **саладетта** VRX2000/330 | 80 | clear | AMBIGUOUS | model+capacity VRX2000/330 identical, but "саладетта" is a distinct subtype vs generic "холодильна" |
| 4401 | Gooder · Вітрина холодильна VRX1500/380 | Gooder · Вітрина **саладетта** VRX1500/380 | 80 | clear | AMBIGUOUS | model+capacity VRX1500/380 identical; saladette vs generic chiller display |
| 4402 | Gooder · Вітрина холодильна VRX1400/330 | Gooder · Вітрина **саладетта** VRX1400/330 | 80 | clear | AMBIGUOUS | model+capacity VRX1400/330 identical; saladette vs generic chiller display |
| 3833 | Gooder · Шафа холодильна USS 374 DTK BK | Gooder · Шафа середньотемп. USS 374 DTK BK | 78 | clear | CONFIRM(judgment) | model USS 374 DTK **BK** identical on BOTH sides; chiller≈mid-temp synonym |
| 4391 | Gooder · Холодильна шафа GN-1410TN | Gooder · Шафа середньотемп. GN-1410TN | 76 | clear | CONFIRM(judgment) | model GN-1410TN identical; chiller≈mid-temp synonym |
| 4392 | Gooder · Морозильна шафа GN-650BT | Gooder · Шафа низькотемп. GN-650BT | 75 | clear | CONFIRM(judgment) | model GN-650BT identical; freezer≈low-temp synonym |
| 4393 | Gooder · Шафа холодильна ВВT350S | Gooder · Шафа середньотемп. ВВT350S | 75 | clear | CONFIRM(judgment) | model ВВT350S identical; chiller≈mid-temp synonym |
| 4394 | Gooder · Шафа холодильна ВВT350H | Gooder · Шафа середньотемп. ВВT350H | 75 | clear | CONFIRM(judgment) | model ВВT350H identical; chiller≈mid-temp synonym |
| 4395 | Gooder · Шафа холодильна BBD230S | Gooder · Шафа середньотемп. BBD230S | 75 | clear | CONFIRM(judgment) | model BBD230S identical (S=both); chiller≈mid-temp synonym |
| 4396 | Gooder · Шафа холодильна BBD230H | Gooder · Шафа середньотемп. BBD230H | 75 | clear | CONFIRM(judgment) | model BBD230H identical (H=both); chiller≈mid-temp synonym |
| 4425 | Gooder · Холодильна шафа GN-650TN | Gooder · Шафа середньотемп. GN-650TN | 75 | clear | CONFIRM(judgment) | model GN-650TN identical; chiller≈mid-temp synonym |
| 4408 | Gooder · Вітрина кондитерська XC-58L | Gooder · Вітрина настільна холодильна XC-58L | 73 | clear | AMBIGUOUS | model XC-58L identical, but "кондитерська" (pastry) vs "холодильна/настільна" descriptor differs |
| 4409 | Gooder · Вітрина кондитерська XC-68L | Gooder · Вітрина настільна холодильна XC-68L | 73 | clear | CONFIRM(judgment) | model XC-68L identical; pastry display = tabletop chiller display (same unit, descriptor) |
| 4410 | Gooder · Вітрина кондитерська XC-78L | Gooder · Вітрина настільна холодильна XC-78L | 73 | clear | CONFIRM(judgment) | model XC-78L identical; same XC-series tabletop display |
| 4411 | Gooder · Вітрина кондитерська XC-98L | Gooder · Вітрина настільна холодильна XC-98L | 73 | clear | CONFIRM(judgment) | model XC-98L identical; same XC-series tabletop display |

## Decisions

### CONFIRM (clean) — 6
4403, 4404, 4405, 4406, 4407, 4433
(All "Вітрина холодильна" XCW-series; SP differs only by adding "настільна" + Cyrillic-о homoglyph "Goоder". Same product-type word, identical model.)

### CONFIRM (judgment) — 21
3832, 3834, 3835, 4430, 3856, 4421, 4414, 4415, 4416, 4417, 3833, 4391, 4392, 4393, 4394, 4395, 4396, 4425, 4409, 4410, 4411
(Model code byte-identical on both sides; the only difference is a domain-synonymous descriptor: temp-class vs function — низькотемпературна↔морозильна, середньотемпературна↔холодильна — or SP dropping/swapping a qualifier. XC-68/78/98L grouped here as pastry=tabletop-chiller display since the identical XC-58L sibling is the lone doubt.)

### AMBIGUOUS — 4
- 4400 — VRX2000/330: SP "саладетта" vs PP generic "холодильна вітрина"; subtype mismatch despite identical model+capacity
- 4401 — VRX1500/380: same saladette-vs-generic doubt
- 4402 — VRX1400/330: same saladette-vs-generic doubt
- 4408 — XC-58L: "кондитерська" (pastry) vs "настільна холодильна"; descriptor genuinely different (kept separate from XC-68/78/98L which I judged confirmable)

### REJECT — 5
**Domain mismatch (rule b) — 5:**
- 3831 — UDD 370 DTK **BK**: PP carries BK variant suffix, SP (7196) is the non-BK unit and is the correct match for m3832; confirming both would put SP 7196 on two PPs (M:1)
- 4382 — sharpening stone (KING K80) vs refrigerated display (КУПЕЦ); matched only on junk internal-id article "125"
- 4383 — sharpening stone (KING DX1000) vs refrigerated display (VENETO VSo-0,95); junk article "123"
- 3805 — fridge cabinet BR400V vs VENETO VSo-0,95 display; junk article "123"
- 3806 — fridge cabinet BR400VG vs VENETO VSo-0,95 display; junk article "123"

**#15 (PP already held) — 0** (none exist in this set)
