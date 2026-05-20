# chunk-069 DIFF (W2)

**Status:** b4 DONE 32/61 — батчи b1..b8 (8+8+8+8+8+8+8+5); next b5 (SKU 33-40, rows 34-41)
**Last updated:** chunk-069 b4 DONE 32/61

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
