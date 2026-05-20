# chunk-069 DIFF (W2)

**Status:** b2 DONE 16/61 — батчи b1..b8 (8+8+8+8+8+8+8+5); next b3 (SKU 17-24, rows 18-25)
**Last updated:** chunk-069 b2 DONE 16/61

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
