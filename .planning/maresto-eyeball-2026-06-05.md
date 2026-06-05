# maresto NEEDS-EYEBALL — refined triage 2026-06-05

Read-only refinement (subagent) of the 15 maresto rows in the NEEDS-EYEBALL bucket of
`candidate-triage-2026-06-05.md`. **No DB change.** Each row cross-checked against the 1:1
invariant (#15) live in `instance/labresta.db` (mode=ro) + domain mismatch heuristics.

**15 total → CONFIRM-candidates 3 (1 clean + 2 judgment) / AMBIGUOUS 1 / REJECT 11
(10 PP-taken #15 conflicts + 1 suffix-variant).**

| match_id | SP (brand + key tokens) | PP (brand + key tokens) | score | 1:1 | REC | reason |
|---:|---|---|---:|---|---|---|
| 3787 | Cuppone — Прес для піци PZF40DS | Cuppone — Прес для піци PZF/40DS, діаметр 40 см | 100 | free | CONFIRM | same model PZF40DS, only hyphen + size descriptor differ |
| 3790 | Sirman — Слайсер TOPAZ 195 **Normale** | Sirman — Слайсер TOPAZ 195 | 100 | free | AMBIGUOUS | SP has "Normale" variant tail PP lacks; don't auto-confirm variant |
| 3798 | Unox — Піч пароконв. XEBC04EUEPRMMP лінія PLUS | Unox — Пароконвектомат XEBC04EUEPRMMP 4 рівня | 100 | free | CONFIRM(judgment) | identical model code; "Піч пароконв."≈"Пароконвектомат", 4 рівня matches code |
| 3791 | Tecnodom — Стіл холод. TF03MIDGN | Tecnodom — Стіл холод. TF03MID**GNAL** NEW | 92 | free | REJECT | model suffix differs (GN vs GNAL) — near-miss suffix variant |
| 3786 | Sirman — Соковижималка ел. Ektor 37 | Sirman — Соковичавниця шнекова Ektor 37 (тверді фрукти) | 86 | free | CONFIRM(judgment) | same model Ektor 37; Соковижималка≈Соковичавниця (juicer synonym), low score |
| 3788 | Sirman — М'ясорубка TC32 Nevada CE (380) | Sirman — М'ясорубка TC 32 NEVADA 3PH non-CE | 100 | taken(m4379) | REJECT | PP held by m4379:confirmed (#15) |
| 3793 | ASBER — Посудомийна GEXH500DD | Asber — Посудомийка купольна GEX-H500 DD | 100 | taken(m1568) | REJECT | PP held by m1568:confirmed |
| 3794 | Unox — Пароконвектомат XV893 Cheflux | Unox — Пароконвектомат XV893 на 12 рівнів | 100 | taken(m3256) | REJECT | PP held by m3256:confirmed |
| 3795 | Unox — Піч пароконв. XEBC06EUE1RMMP лінія ONE | Unox — Піч пароконв. XEBC06EUE1RMMP 6 рівнів | 100 | taken(m3738) | REJECT | PP held by m3738:confirmed |
| 3796 | Unox — Піч пароконв. XEBC10EUE1RMMP лінія ONE | Unox — Піч пароконв. XEBC10EUE1RMMP 10 рівнів | 100 | taken(m3739) | REJECT | PP held by m3739:confirmed |
| 3797 | Unox — Піч пароконв. XEBC04EUE1RMMP лінія ONE | Unox — Піч пароконв. XEBC04EUE1RMMP 4 рівні | 100 | taken(m3737) | REJECT | PP held by m3737:confirmed |
| 3799 | Unox — Пароконвектомат XV393 Cheflux | Unox — Піч пароконв. XV393 на 5 рівнів | 100 | taken(m3255) | REJECT | PP held by m3255:confirmed |
| 3800 | Unox — Пароконвектомат XV593 Cheflux | Unox — Пароконвектомат XV593 на 7 рівнів | 100 | taken(m3257) | REJECT | PP held by m3257:confirmed |
| 3792 | Sirman — Пила стрічкова SO1650F3 (220) | Sirman — Пила стрічкова гастр. SO 1650 F3 (220) | 87 | taken(m3239) | REJECT | PP held by m3239:confirmed |
| 3789 | Sirman — Машина макаронна Sinfonia2 | Sirman — Прес макаронний Sinfonia 2 | 86 | taken(m1800) | REJECT | PP held by m1800:confirmed |

## Decisions
- **CONFIRM (clean):** m3787.
- **CONFIRM (judgment, Yana eyeball):** m3798, m3786.
- **AMBIGUOUS (Yana eyeball):** m3790 (Normale variant tail).
- **REJECT suffix-variant:** m3791 (free PP, but TF03MIDGN ≠ TF03MIDGNAL). Recommend leave as candidate or reject; NOT confirm.
- **10 PP-taken #15 conflicts:** m3788, 3793, 3794, 3795, 3796, 3797, 3799, 3800, 3792, 3789. Each PP already held by another confirmed supplier → keep-existing vs switch-to-maresto is the separate **#15 policy** decision (NEEDS-YANA). Left untouched.

Same supplier (Sirman/Unox/etc.) appears on both sides because the catalog PP names were originally built from one supplier; maresto now offers the same units → many collide on already-confirmed PPs.
