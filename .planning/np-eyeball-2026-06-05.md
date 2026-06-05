# НП (novyy-proekt) NEEDS-EYEBALL — refined triage 2026-06-05

Read-only refinement (subagent) of the 22 novyy-proekt rows in the NEEDS-EYEBALL bucket of
`candidate-triage-2026-06-05.md`. **No DB change.** Each row cross-checked against the 1:1
invariant (#15) live in `instance/labresta.db` (mode=ro) + domain mismatch heuristics.
Dossier column order is PP (catalog) before SP (supplier) — verified byte-for-byte, no swap.

**22 total → CONFIRM 0 / CONFIRM(judgment) 1 / AMBIGUOUS 3 / REJECT 18
(17 PP-taken #15 conflicts + 1 free-PP suffix-variant).**

| match_id | PP (brand + key tokens) | SP (brand + key tokens) | score | 1:1 | REC | reason |
|---:|---|---|---:|---|---|---|
| 4378 | Ceado M98/2 двохпостовий (міксер молочний) | Ceado M98/2 подвійний (міксер) | 75 | free | CONFIRM(judgment) | article M98/2 identical; двохпостовий≈подвійний synonym; PP free |
| 3363 | Apach APTE-77PLR комбінована | Apach APTE-77PLR/PL гл.+ребр. сталь | 100 | free | AMBIGUOUS | model tail /PL suffix; комбінована≈гл+ребр plausibly same |
| 3382 | Sirman Sirio 2 VV хром CC 900 | Sirman Sirio 2 VV хром CE | 100 | free | AMBIGUOUS | trailing code CC 900 vs CE differs |
| 3383 | Sirman SoftCooker XP S GN 2/3 (Sous Vide) | Sirman Softcooker XP | 100 | free | AMBIGUOUS | PP has S GN 2/3 size tail, SP bare |
| 3362 | Apach APTE-47PR гладка | Apach APTE-47PR/PL ребр. сталь | 100 | free | REJECT | model tail /PL differs + surface гладка vs ребр. (suffix-variant) |
| 3353 | Bartscher Рисоварка 12л 150529 | Bartscher Мультиварка 40-60 персон (150529) | 100 | taken(m5) | REJECT | PP held by m5:confirmed |
| 3358 | Bartscher Мікрохвильова піч 610836 | Bartscher Піч НВЧ 23л (610836) | 100 | taken(m42) | REJECT | PP held by m42:confirmed |
| 3384 | Bartscher Рисоварка 8л A150513 | Bartscher Мультиварка 25-40 персон (A150513) | 100 | taken(m43) | REJECT | PP held by m43:confirmed |
| 3354 | Asber GE500DD посудомийна фронтальна | Asber GE-500 DD посудомийка фронтальна | 85 | taken(m367) | REJECT | PP held by m367:confirmed |
| 4377 | Robot Coupe CL60 з важелем (овочерізка) | Robot Coupe CL 60 2 лійки (овочерізка) | 84 | taken(m784) | REJECT | PP held by m784:confirmed |
| 3377 | Robot Coupe MP450 Combi Ultra (заглибний) | Robot Coupe MP 450 Combi Ultra (ручний) | 90 | taken(m774) | REJECT | PP held by m774:confirmed |
| 3373 | Robot Coupe Mini MP240 Combi (погружний) | Robot Coupe Mini MP 240 Combi (ручний) | 89 | taken(m28) | REJECT | PP held by m28:confirmed |
| 3368 | Robot Coupe CMP300 Combi (заглибний) | Robot Coupe CMP 300 Combi (ручний) | 89 | taken(m737) | REJECT | PP held by m737:confirmed |
| 3374 | Robot Coupe Mini MP240VV (погружний) | Robot Coupe Mini MP 240 VV (ручний) | 89 | taken(m119) | REJECT | PP held by m119:confirmed |
| 3379 | Robot Coupe MP450 Ultra (заглибний) | Robot Coupe MP 450 Ultra (ручний) | 89 | taken(m121) | REJECT | PP held by m121:confirmed |
| 3366 | Robot Coupe CMP250 Combi (занурювальний) | Robot Coupe CMP 250 Combi (ручний) | 87 | taken(m23) | REJECT | PP held by m23:confirmed |
| 3367 | Robot Coupe CMP250VV (занурювальний) | Robot Coupe CMP 250 VV (ручний) | 86 | taken(m769) | REJECT | PP held by m769:confirmed |
| 3375 | Robot Coupe MP350 Combi Ultra (заглибний) | Robot Coupe MP 350 Ultra (ручний) | 85 | taken(m771) | REJECT | PP held by m771:confirmed; MP350 Combi Ultra vs MP 350 Ultra tail differs too |
| 3381 | Robot Coupe MP550 ULTRA 34820LH (погружний) | Robot Coupe MP 550 Ultra (ручний) | 85 | taken(m1087) | REJECT | PP held by m1087:manual |
| 3372 | Robot Coupe Mini MP190VV (заглибний) | Robot Coupe Mini MP 190 VV (ручний) | 84 | taken(m27) | REJECT | PP held by m27:confirmed |
| 3370 | Robot Coupe Mini MP160VV (занурювальний) | Robot Coupe Mini MP 160 VV (ручний) | 83 | taken(m25) | REJECT | PP held by m25:confirmed |
| 3371 | Robot Coupe Mini MP190 Combi з вінчиком | Robot Coupe Mini MP 190 Combi (ручний) | 81 | taken(m26) | REJECT | PP held by m26:confirmed |

## Decisions
- **CONFIRM (clean):** none (no byte-identical name pair).
- **CONFIRM (judgment, Yana eyeball):** m4378 — article `M98/2` byte-identical; «двохпостовий»≈«подвійний» synonym; PP free.
- **AMBIGUOUS (Yana eyeball):** m3363 (`/PL` suffix; комбінована≈гл+ребр), m3382 (trailing `CC 900` vs `CE`), m3383 (PP-only size tail `S GN 2/3`).
- **REJECT free-PP suffix-variant:** m3362 (`APTE-47PR` гладка ≠ `APTE-47PR/PL` ребр. — opposite surface). Left as candidate.
- **REJECT 17 PP-taken #15 conflicts:** 3353, 3358, 3384, 3354, 4377, 3377, 3373, 3368, 3374, 3379, 3366, 3367, 3375, 3381(manual), 3372, 3370, 3371. Each PP already held by another confirmed/manual supplier → keep-existing vs switch = **#15 policy** (NEEDS-YANA). Left untouched.

Note: 16 of the 17 #15 rejects are Robot Coupe — the candidate name is the immersion/«погружний» wording while the already-confirmed PP is the «ручний» (handheld) wording of the same model number. Same unit, descriptor differs, PP already taken → deterministic reject.
