# chunk-069 DIFF (W2)

**Status:** b7 DONE 56/61 — батчи b1..b8 (8+8+8+8+8+8+8+5); next b8 (SKU 57-61, rows 58-62)
**Last updated:** chunk-069 b7 DONE 56/61

Source: `chunk-069.xlsx` (RO) → operating: `chunk-069-fixed.xlsx` (gitignored).
Batches заполняются после каждого закрытого батча.

## b1 (SKU 1-8, rows 2-9) — 8/61

| # | SKU | row | ART | Brand+Model | Category | Изменения |
|---|-----|-----|-----|-------------|----------|-----------|
| 1 | 1 | 2 | 2434135469 | ATA AT 901 купольная | blknochg | — |
| 2 | 2 | 3 | 2434148483 | ATA AT 951 купольная | blknochg | — |
| 3 | 3 | 4 | 2434159376 | ATA B 51 купольная | blknochg | — |
| 4 | 4 | 5 | 2434170153 | Elframo LP 61 VE котломоечная | blknochg | — |
| 5 | 5 | 6 | 651352472 | Krupps S1100E купольная | **TRIP** | c5←c7; c36 ← RU inline body (UNIKO-MID/умягчитель/13 li tech-char) |
| 6 | 6 | 7 | 664883808 | Krupps EL991E ELITECH котломоечная фронтальная | **TRIP** | c5←c7; c36 ← RU inline body (Acquatech/IKLOUD/ХАССП/11 li tech-char) |
| 7 | 7 | 8 | 664883809 | Krupps S540E фронтальная | **TRIP** | c5←c7; c36 ← RU inline body (11 li tech-char) |
| 8 | 8 | 9 | 923572273 | Krupps K1500E Koral купольная | **TRIP** | c5←c7; c36 ← RU 16-nl body, `<strong>` preserved, Перистальтический/Termostop (16 li tech-char) |

**Итого b1:** TRIP 4 + blknotrip 0 + blknochg 4 + SKIP-НП 0. Verify **101 PASS / 0 FAIL**.
**Cum после b1:** TRIP 4 + blknotrip 0 + blknochg 4 + SKIP-НП 0 = **8/61**.

## b2 (SKU 9-16, rows 10-17) — 16/61

| # | SKU | row | ART | Brand+Model | Category | Изменения |
|---|-----|-----|-----|-------------|----------|-----------|
| 1 | 9 | 10 | 923587067 | Krupps EVO121 туннельная | **TRIP** | c5←c7; c36 ← RU 14-nl body EVOLUTION линия `<ul>+<ol>+<ul>` 11 li tech-char |
| 2 | 10 | 11 | 1152270353 | Winterhalter UCM Glasswasher фронтальная | blknochg | — |
| 3 | 11 | 12 | 1160729445 | Krupps C537S DGT Advance фронтальная | blknochg | — |
| 4 | 12 | 13 | 1264689042 | Oztiryakiler OBM1080DPD купольная | blknochg | — |
| 5 | 13 | 14 | 1519082393 | Krupps EL951E | **TRIP** | c5←c7; c36 ← RU 11-nl body 10 li tech-char |
| 6 | 14 | 15 | 1813450895 | Ozti OBM 1080D PDRT помпа слива | blknochg | — |
| 7 | 15 | 16 | 1943696404 | Ozti OBM 1080D PDT помпа слива | blknochg | — |
| 8 | 16 | 17 | 2045404308 | Empero EMP.2000-SAG-R | blknochg | — |

**Итого b2:** TRIP 2 + blknotrip 0 + blknochg 6 + SKIP-НП 0. Verify **117 PASS / 0 FAIL**.
**Cum после b2:** TRIP 6 + blknotrip 0 + blknochg 10 + SKIP-НП 0 = **16/61**.

## b3 (SKU 17-24, rows 18-25) — 24/61

| # | SKU | row | ART | Brand+Model | Category | Изменения |
|---|-----|-----|-----|-------------|----------|-----------|
| 1 | 17 | 18 | 2045406113 | Empero EMP.3000-SAG-R | blknochg | — |
| 2 | 18 | 19 | 2110099464 | Empero EMP.1000-F | blknochg | — |
| 3 | 19 | 20 | 2126106102 | Krupps EL985E (котломоечная) для габаритной посуды | **TRIP** | c5←c7; c36 ← RU body (`<h2>` + 3 `<p>` + 11 li tech-char), Acquatech/UNIKO/IKLOUD/ХАССП, dims `30/1780/680/120/150/240/540/850x725x100/8/5/18/1000x860x1805/13/380/2,5-3,0` |
| 4 | 20 | 21 | 2191298201 | Empero EMP.1000-SDF | blknochg | — |
| 5 | 21 | 22 | 2538744328 | Frosty AP1 400V котломоечная (h=650) | **TRIP** | c5←c7; c36 ← RU body (12 `<p>` + 4 `<ul>` blocks: 3+14+3+2 li), h=650, dims `650/400х600/26/30/3-6/37/15/60/2/4/9,9/380/720x780x1730/155/560х630х100h`, typo «дл»→«до» |
| 6 | 22 | 23 | 2538759109 | Frosty AP2 400V котломоечная (h=850) | **TRIP** | c5←c7; c36 ← RU body (same template как r22 с h=850 + 1930мм высота) |
| 7 | 23 | 24 | 1168653006 | HURAKAN HKN-CNW460 PRO термоупаковочный | **SKIP-НП** | — (НП forward-only; fixed строка не тронута) |
| 8 | 24 | 25 | 1548982581 | Frosty C18 камерный вакуумный упаковщик | blknochg | — |

**Итого b3:** TRIP 3 + blknotrip 0 + blknochg 4 + SKIP-НП 1. Verify **179 PASS / 0 FAIL**.
**Cum после b3:** TRIP 9 + blknotrip 0 + blknochg 14 + SKIP-НП 1 = **24/61**.

## b4 (SKU 25-32, rows 26-33) — 32/61

| # | SKU | row | ART | Brand+Model | Category | Изменения |
|---|-----|-----|-----|-------------|----------|-----------|
| 1 | 25 | 26 | 2060699885 | HURAKAN HKN-CNW430 термоупаковочная | **SKIP-НП** | — (НП forward-only; fixed строка не тронута) |
| 2 | 26 | 27 | 454521621 | GGM VTB320 вакуумный упаковщик 16 л/мин | blknochg | — |
| 3 | 27 | 28 | 454521622 | GGM VTB420 вакуумный упаковщик 28 л/мин | blknochg | — |
| 4 | 28 | 29 | 489839797 | REEDNEE SW450L «горячий стол» упаковщик | **TRIP** | c5←c7 «Упаковщик "горячий стол" REEDNEE SW450L»; c36 ← RU body (`<h2>` + 7 li tech-char), dims `390х124/450/70-90&deg;С/380,400,430,450/7/620x515x160` |
| 5 | 29 | 30 | 490566373 | Lavezzini Gofer 200x400 пакеты гофрированные | **TRIP** | c5←c7 «Пакеты гофрированные Lavezzini 200x400 (упаковка 100 шт.)»; c36 ← RU body (`<p>` + 3 li: 100шт/полиэтилен/200х400) |
| 6 | 30 | 31 | 490575794 | Frosty 150x250 пакеты гофрированные | blknochg | — |
| 7 | 31 | 32 | 490581287 | Frosty 200x300 пакеты гофрированные | blknochg | — |
| 8 | 32 | 33 | 490587113 | Frosty 250x350 пакеты гофрированные | blknochg | — |

**Итого b4:** TRIP 2 + blknotrip 0 + blknochg 5 + SKIP-НП 1. Verify **179 PASS / 0 FAIL**.
**Cum после b4:** TRIP 11 + blknotrip 0 + blknochg 19 + SKIP-НП 2 = **32/61**.

## b5 (SKU 33-40, rows 34-41) — 40/61

| # | SKU | row | ART | Brand+Model | Category | Изменения |
|---|-----|-----|-----|-------------|----------|-----------|
| 1 | 33 | 34 | 490598501 | Frosty 300x400 пакеты гофрированные | blknochg | — |
| 2 | 34 | 35 | 568706697 | Orved Evox 30 вакуумный упаковщик 8м3/час | blknochg | — |
| 3 | 35 | 36 | 593842902 | GGM VMKH-300 вакуумный упаковщик 14,4 м3/час | blknochg | — |
| 4 | 36 | 37 | 593842903 | GGM VMKH-400Z вакуумный упаковщик 20 м3/час | blknochg | — |
| 5 | 37 | 38 | 639913421 | Apach AVM254 вакуумный 4 м³/час | **SKIP-НП** | — (НП forward-only; fixed строка не тронута) |
| 6 | 38 | 39 | 639913422 | Apach AVM308 вакуумный 8 м³/час | **SKIP-НП** | — (НП forward-only; fixed строка не тронута) |
| 7 | 39 | 40 | 639913425 | Apach AVM412 вакуумный 12 м³/час | **SKIP-НП** | — (НП forward-only; fixed строка не тронута) |
| 8 | 40 | 41 | 646844865 | PERS.PETROS LEVAC 3 вакуумный упаковщик | blknochg | — |

**Итого b5:** TRIP 0 + blknotrip 0 + blknochg 5 + SKIP-НП 3. Verify **187 PASS / 0 FAIL**.
**Cum после b5:** TRIP 11 + blknotrip 0 + blknochg 24 + SKIP-НП 5 = **40/61**.

## b6 (SKU 41-48, rows 42-49) — 48/61

| # | SKU | row | ART | Brand+Model | Category | Изменения |
|---|-----|-----|-----|-------------|----------|-----------|
| 1 | 41 | 42 | 646844867 | PERS.PETROS (Orved) С254 камерный вакуумный упаковщик | blknochg | — |
| 2 | 42 | 43 | 647420654 | Hendi Budget Line 975350 (планка 310 мм) безкамерный | **TRIP** | c5←c7; c36 ← RU inline body (`<ul>` + 11 li tech-char: 2 цикла/рулон/310мм/2мм/попадание влаги/11л/мин/подъёмная крышка/уровень шума/вес 1,74кг/планка 310мм/390x160x92) |
| 3 | 43 | 44 | 647442350 | Lavezzini Mini Mini полуавтомат безкамерный | **TRIP** | c5←c7; c36 ← RU inline body (`<ul>` + 6 li tech-char: 20л/мин/планка 350/0,25кВт/220В/370x260x130/13кг) |
| 4 | 44 | 45 | 647442351 | Lavezzini Optima камерный (10 м3/час) | **TRIP** | c5←c7; c36 ← RU inline body (`<ul>` + 7 li tech-char: 10м3/час/планка 350/камера 360х400x190/220В/0,45кВт/530х420х400/40кг), сохранены влагозащитная панель + съёмная планка + гладкие пакеты + инертный газ |
| 5 | 45 | 46 | 647442352 | Lavezzini Unica камерный (12 м3/час) | **TRIP** | c5←c7; c36 ← RU inline body (`<ul>` + 7 li tech-char: 12м3/час/планка 400/камера 410х450x220/220В/0,9кВт/550х470х430/55кг), формат идентичен r45 с увеличенными dims |
| 6 | 46 | 47 | 732719290 | HURAKAN HKN-VAC400 вакуумный 20 м3/час | **SKIP-НП** | — (НП forward-only; fixed строка не тронута) |
| 7 | 47 | 48 | 878084280 | Lavezzini Universal камерный + внешнее вакуумирование (6 м3/час) | **TRIP** | c5←c7; c36 ← RU body (`<p>+<p>+<ul>` 8 li tech-char: 6м3/час/гладкие пакеты/планка 300/камера 310х350x120/220В/0,35кВт/530х370х250/32кг), сохранён 2-й `<p>` про доп. режим внешнего вакуумирования с перфорированными продуктами |
| 8 | 48 | 49 | 916970592 | Lavezzini Gofer 150x350 пакеты гофрированные | **TRIP** | c5←c7 «Пакеты гофрированные Lavezzini 150x350 (упаковка 100 шт.)»; c36 ← RU body (`<p>` + 3 li: 100шт/полиэтилен/150х350) same template как r30 |

**Итого b6:** TRIP 6 + blknotrip 0 + blknochg 1 + SKIP-НП 1. Verify **229 PASS / 0 FAIL**.
**Cum после b6:** TRIP 17 + blknotrip 0 + blknochg 25 + SKIP-НП 6 = **48/61**.

## b7 (SKU 49-56, rows 50-57) — 56/61

| # | SKU | row | ART | Brand+Model | Category | Изменения |
|---|-----|-----|-----|-------------|----------|-----------|
| 1 | 49 | 50 | 916971482 | Lavezzini Gofer 250x350 пакеты гофрированные | **TRIP** | c5←c7 «Пакеты гофрированные Lavezzini 250x350 (упаковка 100 шт.)»; c36 ← RU body (`<p>` + 3 li: 100шт/полиэтилен/250х350) same template как r30/r49 |
| 2 | 50 | 51 | 916972344 | Lavezzini Gofer 300x400 пакеты гофрированные | **TRIP** | c5←c7 «Пакеты гофрированные Lavezzini 300x400 (упаковка 100 шт.)»; c36 ← RU body 3 li 300х400 |
| 3 | 51 | 52 | 916973058 | Lavezzini Smooth 300x400 пакеты гладкие | **TRIP** | c5←c7 «Пакеты гладкие Lavezzini Smooth 300x400 (упаковка 100 шт.)»; c36 ← RU body `<p>` + 3 li (100шт/полиэтилен/300х400) — гладкий вариант |
| 4 | 52 | 53 | 1171045019 | REEDNEE DZ260 вакуумный упаковщик камерный | **TRIP** | c5←c7; c36 ← RU body (`<h2>` + `<p>` + `<ul>` 8 li tech-char: 385х280х50/планка 260/10м3/час/0,37кВт/502х330х380), сохранены: полуавтоматический/настольный/электронная панель/гладкие пакеты/влагосодержащий продукт |
| 5 | 53 | 54 | 1176134094 | Hurakan HKN-VAC260 (260 мм планка) | **SKIP-НП** | — (НП forward-only; fixed строка не тронута) |
| 6 | 54 | 55 | 1238245270 | REEDNEE DZ400 вакуумный упаковщик камерный | **TRIP** | c5←c7; c36 ← RU body (`<h2>` + `<p>` + `<ul>` 9 li tech-char: 440х420х70/+«одна сварочная планка»/планка 390/20м3/час/0,9кВт/540х490х500), same template как r53 с увеличенными dims |
| 7 | 55 | 56 | 1581264554 | FROSTY VM300TE/A вакууматор 10 куб.м/час | **TRIP** | c5 unchanged (c4==c5==c7 RU OK «Вакууматор FROSTY VM300TE/A»); c36 ← RU body (`<h2>` + `<p>` + `<ul>` 14 li tech-char: 300х405х50+55h/шов 260x8/цикл 10-20с/0,4кВт/220В/370x510x370), сохранены: нержавеющая сталь/цельнотянутая конструкция/округленные углы/куполообразная крышка/газовые амортизаторы/плексиглас/механический манометр/10 программ/TOOL KIT |
| 8 | 56 | 57 | 1581275926 | FROSTY VM400TE/A вакууматор 20 куб.м/час | **TRIP** | c5 unchanged; c36 ← RU body (`<h2>` + `<p>` + `<ul>` 15 li tech-char: +«1 запаечная планка»/430х430х75+55h/шов 400x10/цикл 10-25с/0,9кВт/220В/480x530x470), формат идентичен r56 с `&mdash;` сохранён |

**Итого b7:** TRIP 7 + blknotrip 0 + blknochg 0 + SKIP-НП 1. Verify **245 PASS / 0 FAIL**.
**Cum после b7:** TRIP 24 + blknotrip 0 + blknochg 25 + SKIP-НП 7 = **56/61**.
