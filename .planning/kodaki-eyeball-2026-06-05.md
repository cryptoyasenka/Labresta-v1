# kodaki — NEEDS-EYEBALL refinement (2026-06-05)

Read-only refinement of the **kodaki (104)** subsection inside `## NEEDS-EYEBALL` of `candidate-triage-2026-06-05.md`. No DB or other file was modified; all 104 rows were verified against `product_matches` (correct pp_id/sp_id, every row `status=candidate`, none missing). The single #15 cross-check query (all prom_product_ids vs `status IN ('confirmed','manual')`) found 10 PPs already held.

**Counts:** 104 total — CONFIRM(clean) **55** / CONFIRM(judgment) **28** / AMBIGUOUS **0** / REJECT **21** (10 = #15 PP already taken, 11 = domain: suffix/model/product-type). CONFIRM total = 83.

Column order mirrors the source: catalog (PP) before supplier (SP). `1:1` = does this PP already hold a different confirmed/manual match (invariant #15).

| match_id | PP (brand + key tokens) | SP (brand + key tokens) | score | 1:1 | REC | reason |
|---:|---|---|---:|:--:|:--|---|
| 3645 | GI.Metal — Лопата для піци Gi Metal AF-37R/120 Aurora | GI.METAL — AF-37R/120 Лопата для піци | 100 | free | CONFIRM(judgment) | code AF-37R/120 exact; SP drops 'Aurora' series word + word-order |
| 3646 | GI.Metal — Лопата для піци Gi Metal AF-45R/120 Aurora | GI.METAL — AF-45R/120 Лопата для піци | 100 | free | CONFIRM(judgment) | code AF-45R/120 exact; SP drops 'Aurora' + word-order |
| 3654 | FROSTY — Плита індукційна FROSTY 70-KPP1 настільна | FROSTY — Плита індукційна 70-KPP1 (220 В) | 100 | free | CONFIRM(judgment) | code 70-KPP1 exact; PP adds 'настільна' |
| 3605 | Imperia — Тісторозкатка ручна HOME iPASTA SFOGLIATRICE cod.162 | IMPERIA — 162 Тісторозкатка iPASTA Sfogliatrice | 95 | free | CONFIRM(judgment) | code 162 exact; SP drops 'ручна/HOME', word-order |
| 3628 | FROSTY — Ніж-змішувач Frosty BLD300 | FROSTY — Ніж-змішувач BLD300 | 95 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3682 | FROSTY — Диск для овочерізки Frosty D12А | FROSTY — Диск для овочерізки D12А | 95 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3684 | FROSTY — Диск для овочерізки Frosty D10А | FROSTY — Диск для овочерізки D10А | 95 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3683 | FROSTY — Диск для овочерізки Frosty D12 | FROSTY — Диск для овочерізки D12А | 91 | free | REJECT | SP D12А matched exactly by m3682; this PP=D12 (missing 'А' suffix) — variant tail differs |
| 3685 | FROSTY — Диск для овочерізки Frosty D10 | FROSTY — Диск для овочерізки D10А | 91 | free | REJECT | SP D10А matched exactly by m3685's sibling m3684; this PP=D10 — suffix differs |
| 3585 | Fimar — Овочерізка Fimar TV2500 (220) | FIMAR — Овочерізка TV2500 (220 В) | 91 | held m432 | REJECT | PP held by m432:confirmed (#15) |
| 3586 | Fimar — Овочерізка Fimar TV3000 (220) | FIMAR — Овочерізка TV3000 (220 В) | 91 | held m433 | REJECT | PP held by m433:confirmed (#15) |
| 3587 | Fimar — Овочерізка Fimar TV4000 (220) | FIMAR — Овочерізка TV4000 (220 В) | 91 | held m780 | REJECT | PP held by m780:confirmed (#15) |
| 3648 | FROSTY — Апарат для приготування морозива Frosty ICM-15A | FROSTY — Апарат для приготування морозива ICM-15A (220 В) | 89 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3672 | FROSTY — Тісторозкатка -локшинорізка Frosty FDM180 | FROSTY — Тісторозкатка локшинорізка FDM180 (220 В) | 87 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3598 | Imperia — Тісторозкатка з мотором HOME iPASTA Electric cod.650 | IMPERIA — 650 Тісторозкатка iPASTA ELECTRIC (220 В) | 87 | free | CONFIRM(judgment) | code 650 exact; SP drops 'з мотором/HOME' |
| 3709 | FROSTY — Шафа холодильна Frosty RT235C-3, black | FROSTY — Шафа холодильна RT235C-3, black (220 В) | 87 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3710 | FROSTY — Шафа холодильна Frosty RT215C-3, black | FROSTY — Шафа холодильна RT215C-3, black (220 В) | 87 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3711 | FROSTY — Шафа холодильна Frosty RT280C-3, black | FROSTY — Шафа холодильна RT280C-3, black (220 В) | 87 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3615 | FROSTY — Тісторозкатка FROSTY M42A для коржів | FROSTY — Тісторозкатка для коржів M42A (220 В) | 87 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3635 | FROSTY — Плита індукційна WOK FROSTY G35-KA18 настільна | FROSTY — Плита індукційна WOK G35-KA18 (220 В) | 87 | free | CONFIRM(judgment) | code G35-KA18 exact (WOK both); PP adds 'настільна' |
| 3653 | Fimar — Тертка-подрiбнювач Fimar GR12/S 1ph | FIMAR — Тертка-подрiбнювач GR12/S 1ph (220 В) | 87 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3695 | FROSTY — Фритюрниця електрична Frosty EFS-6L-2 | FROSTY — Фритюрниця електрична EFS- 6L-2 (220 В) | 87 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3703 | FROSTY — Шафа холодильна Frosty RT-58B-1 Black | FROSTY — Шафа холодильна RT-58B-1, black (220 В) | 87 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3704 | FROSTY — Шафа холодильна Frosty RT-58B-3 Black | FROSTY — Шафа холодильна RT-58B-3, black (220 В) | 87 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3705 | FROSTY — Шафа холодильна Frosty RT-78B-1 Black | FROSTY — Шафа холодильна RT-78B-1, black (220 В) | 87 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3706 | FROSTY — Шафа холодильна Frosty RT-78B-3 Black | FROSTY — Шафа холодильна RT-78B-3, black (220 В) | 87 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3707 | FROSTY — Шафа холодильна Frosty RT-98B-1 Black | FROSTY — Шафа холодильна RT-98B-1, black (220 В) | 87 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3708 | FROSTY — Шафа холодильна Frosty RT-98B-3 Black | FROSTY — Шафа холодильна RT-98B-3, black (220 В) | 87 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3618 | FROSTY — Вітрина холодильна FROSTY RTW 130L-2 | FROSTY — Вітрина холодильна RTW 130L-2 (220 В) | 86 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3712 | FROSTY — Вітрина холодильна Frosty RTW-202C-4 | FROSTY — Вітрина холодильна RTW-202C-4 (220 В) | 86 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3713 | FROSTY — Вітрина холодильна Frosty RTW-202C-5 | FROSTY — Вітрина холодильна RTW-202C-5 (220 В) | 86 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3714 | FROSTY — Вітрина холодильна Frosty RTW-145C-5 | FROSTY — Вітрина холодильна RTW-145C-5 (220 В) | 86 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3716 | FROSTY — Вітрина холодильна Frosty RTW-186C-5 | FROSTY — Вітрина холодильна RTW-186C-5 (220 В) | 86 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3717 | FROSTY — Вітрина холодильна Frosty RTW-225C-5 | FROSTY — Вітрина холодильна RTW-225C-5 (220 В) | 86 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3656 | Imperia — Тісторозкатка з мотором HOME PASTAPRESTO cod.700 | IMPERIA — 700 Тісторозкатка PASTAPRESTO (220 В) | 86 | free | CONFIRM(judgment) | code 700 exact; SP drops 'з мотором/HOME' |
| 3694 | FROSTY — Фритюрниця електрична Frosty EFS-6L | FROSTY — Фритюрниця електрична EFS- 6L (220 В) | 86 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3718 | FROSTY — Вітрина для морозива Frosty RTD-87C | FROSTY — Вітрина для морозива RTD-87C (220 В) | 86 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3610 | FROSTY — Вітрина холодильна FROSTY ARC-100R | FROSTY — Вітрина холодильна ARC-100R (220 В) | 86 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3647 | FROSTY — Вітрина холодильна Frosty ARC-400R | FROSTY — Вітрина холодильна ARC-400R (220 В) | 86 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3666 | FROSTY — Шафа холодильна Frosty FL218 black | FROSTY — Шафа холодильна FL218, black (220 В) | 86 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3667 | FROSTY — Шафа холодильна FROSTY FL218 white | FROSTY — Шафа холодильна FL218, white (220 В) | 86 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3715 | FROSTY — Вітрина холодильна Frosty RTW-186C | FROSTY — Вітрина холодильна RTW-186C (220 В) | 86 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3597 | Imperia — Тісторозкатка ручна HOME iPASTA TITANIA cod.190 | IMPERIA — 190 Тісторозкатка TITANIA | 86 | free | CONFIRM(judgment) | code 190 exact (TITANIA); SP drops 'iPASTA/ручна/HOME' |
| 3599 | Staff — Батч фризер STAFF ВТМ 10А для твердого морозива, щербетів, граніті | STAFF — Фризер для твердого морозива ВТМ10А (220 В) | 86 | free | CONFIRM(judgment) | code ВТМ10А exact; 'Батч фризер' vs 'Фризер для твердого морозива' synonym |
| 3606 | FROSTY — Овочерізка FROSTY HLC-300 з 5 дисками в комплекті | FROSTY — Овочерізка HLC-300 (220 В) | 86 | free | CONFIRM(judgment) | code HLC-300 exact; PP is bundle '+5 дисків', SP base unit |
| 3608 | FROSTY — Вафельниця FROSTY WS-15-2 для бельгійських вафель | FROSTY — Вафельниця WS-15 (220 В) | 86 | free | REJECT | SP WS-15 matched exactly by m3609; this PP=WS-15-2 — '-2' suffix variant differs |
| 3609 | FROSTY — Вафельниця FROSTY WS-15 для бельгійських вафель | FROSTY — Вафельниця WS-15 (220 В) | 86 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3629 | FROSTY — Вінчик Frosty WIK250 | FROSTY — Вінчик WIK250 | 86 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3655 | FROSTY — Подрібнювач харчових відходів FROSTY BS-018 з пневмовимачем | FROSTY — Подрібнювач відходів BS-018 (220 В) | 86 | free | CONFIRM(judgment) | code BS-018 exact; PP adds 'харчових…з пневмовимачем' |
| 3669 | FROSTY — Піч подова FROSTY NES-12T з парозволоженням | FROSTY — Піч подова NES-12T (220 В) | 86 | free | CONFIRM(judgment) | code NES-12T exact; PP adds 'з парозволоженням' (both 220) |
| 3670 | FROSTY — Піч подова FROSTY NES-24T з парозволоженням | FROSTY — Піч подова NES-24T (380 В) | 86 | free | CONFIRM(judgment) | code NES-24T exact; PP adds 'з парозволоженням'; SP 380 В |
| 3671 | FROSTY — Піч подова FROSTY NES-36T з парозволоженням | FROSTY — Піч подова NES-36T (380 В) | 86 | free | CONFIRM(judgment) | code NES-36T exact; PP adds 'з парозволоженням'; SP 380 В |
| 3678 | FROSTY — Блендер FROSTY 010 | FROSTY — Двигун для блендера BL-010Е | 86 | free | REJECT | product-type differs: PP 'Блендер 010' vs SP 'Двигун для блендера BL-010Е' (motor, not blender); code 010 vs BL-010Е |
| 3686 | FROSTY — Шафа холодильна Frosty FTD200GSS | FROSTY — Шафа холодильна FTD200GSS (220 В) | 86 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3690 | FROSTY — Блендер FROSTY 010Е | FROSTY — Блендер професійний FBA-010 (220 В) | 86 | free | REJECT | PP code 010Е vs SP FBA-010; SP FBA-010 matched exactly by m3692 |
| 3692 | FROSTY — Блендер Frosty FBA-010 | FROSTY — Блендер професійний FBA-010 (220 В) | 86 | free | CONFIRM(judgment) | code FBA-010 exact; SP adds 'професійний' |
| 3696 | FROSTY — Вафельниця Frosty WBS-2B для бельгійських вафель | FROSTY — Вафельниця WBS- 2B (220 В) | 86 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3697 | FROSTY — Вафельниця Frosty WBS-22B для бельгійських вафель | FROSTY — Вафельниця WBS-22B (220 В) | 86 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3699 | FROSTY — Фаршеміс Frosty FDH-15N | FROSTY — Фаршезмішувач-тістоміс FDH-15N (220 В) | 86 | free | CONFIRM(judgment) | code FDH-15N exact; 'Фаршеміс' vs 'Фаршезмішувач-тістоміс' synonym |
| 3627 | FROSTY — Плита індукційна FROSTY G35-KP2 настільна | FROSTY — Плита індукційна G35-KP2 (220 В) | 85 | free | CONFIRM(judgment) | code G35-KP2 exact; PP adds 'настільна' |
| 3688 | FROSTY — Шафа морозильна Frosty FBD600SS | FROSTY — Шафа морозильна FBD600SS (220 В) | 85 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3638 | FROSTY — Гриль контактний Frosty SP-1A2 | FROSTY — Гриль контактний SP-1A2 (220 В) | 85 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3639 | FROSTY — Гриль контактний Frosty SP-2A1 | FROSTY — Гриль контактний SP-1A2 (220 В) | 85 | free | REJECT | PP SP-2A1 vs SP SP-1A2; SP-1A2 matched exactly by m3638 — model code differs |
| 3641 | FROSTY — Гриль контактний Frosty SP-1C2 | FROSTY — Гриль контактний SP-1C2 (220 В) | 85 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3649 | FROSTY — Спіральний тістоміс Frosty HS 20 двошвидкісний | FROSTY — Тістоміс спіральний HS 20 (220 В) | 85 | free | CONFIRM(judgment) | code HS 20 exact; word-order + SP drops 'двошвидкісний' |
| 3650 | FROSTY — Спіральний тістоміс Frosty HS 40 двошвидкісний | FROSTY — Тістоміс спіральний HS 40 (220 В) | 85 | free | CONFIRM(judgment) | code HS 40 exact; word-order + drops 'двошвидкісний' |
| 3657 | FROSTY — Спіральний тістоміс Frosty HS 30 двошвидкісний | FROSTY — Тістоміс спіральний HS 30 (220 В) | 85 | free | CONFIRM(judgment) | code HS 30 exact; word-order + drops 'двошвидкісний' |
| 3676 | FROSTY — Гриль контактний Frosty SP-2A3 | FROSTY — Гриль контактний SP-2A3 (220 В) | 85 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3617 | FROSTY — Тостер конвеєрний FROSTY CVT-03 | FROSTY — Тостер конвеєрний CVT-03 (220 В) | 84 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3591 | FROSTY — Міксер планетарний FROSTY B-10 | FROSTY — Міксер планетарний B-10 (220 В) | 84 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3592 | FROSTY — Міксер планетарний Frosty B10-B | FROSTY — Міксер планетарний B-10 (220 В) | 84 | free | REJECT | PP B10-B vs SP B-10; B-10 matched exactly by m3591 — '-B' suffix variant |
| 3593 | FROSTY — Міксер планетарний FROSTY B-20 | FROSTY — Міксер планетарний B-20 (220 В) | 84 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3594 | FROSTY — Міксер планетарний FROSTY B20-B | FROSTY — Міксер планетарний B-20 (220 В) | 84 | free | REJECT | PP B20-B vs SP B-20; matched exactly by m3593 — '-B' suffix variant |
| 3595 | FROSTY — Міксер планетарний FROSTY B-40 | FROSTY — Міксер планетарний B-40 (220 В) | 84 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3596 | FROSTY — Міксер планетарний Frosty B40-B | FROSTY — Міксер планетарний B-40 (220 В) | 84 | free | REJECT | PP B40-B vs SP B-40; matched exactly by m3595 — '-B' suffix variant |
| 3630 | FROSTY — Гриль контактний Frosty SP-1C1 | FROSTY — Гриль контактний SP-1C1 (220 В) | 84 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3632 | FROSTY — Стіл холодильний FROSTY PS300 саладета | FROSTY — Стіл холодильний PS300 (220 В) | 84 | free | CONFIRM(judgment) | code PS300 exact; PP adds 'саладета' |
| 3640 | FROSTY — Гриль контактний Frosty SP-1A1 | FROSTY — Гриль контактний SP-1A1 (220 В) | 84 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3644 | FROSTY — Гриль контактний Frosty SP-2A2 | FROSTY — Гриль контактний SP-2A2 (220 В) | 84 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3660 | FROSTY — Льодогенератор Frosty HZB-18F | FROSTY — Льодогенератор HZB-18F (220 В) | 84 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3679 | FROSTY — Піч конвекційна Frosty ESD-1A | FROSTY — Піч конвекційна ESD-1A (220 В) | 84 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3680 | FROSTY — Піч конвекційна Frosty ESD-4A | FROSTY — Піч конвекційна ESD-4A (220 В) | 84 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3681 | FROSTY — Піч конвекційна Frosty ESD-8A | FROSTY — Піч конвекційна ESD-8A (220 В) | 84 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3631 | FROSTY — Стіл холодильний FROSTY S900 саладета | FROSTY — Стіл холодильний S900 (220 В) | 84 | free | CONFIRM(judgment) | code S900 exact; PP adds 'саладета' |
| 3637 | FROSTY — Вітрина теплова FROSTY BV-808 | FROSTY — Вітрина теплова BV-808 (220 В) | 84 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3588 | Fimar — Тісторозкатка Fimar SI320 (220 В) | FIMAR — Тісторозкатка SI 320 (220 В) | 83 | held m246 | REJECT | PP held by m246:confirmed (#15) |
| 3589 | Fimar — Тісторозкатка Fimar SI420 (220 В) | FIMAR — Тісторозкатка SI 420 (220 В) | 83 | held m169 | REJECT | PP held by m169:confirmed (#15) |
| 3607 | FROSTY — Піч конвекційна Frosty EN-50 | FROSTY — Піч конвекційна EN-50 (220 В) | 83 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3590 | FROSTY — Міксер молочний FROSTY DM-B | FROSTY — Міксер молочний DM-B (220 В) | 83 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3634 | FROSTY — Стіл для піци FROSTY PS903 холодильний | FROSTY — Стіл для піци PS903 (220 В) | 83 | free | CONFIRM(judgment) | code PS903 exact; PP adds 'холодильний' |
| 3700 | FROSTY — Тісторозкатка Frosty FDM220M | FROSTY — Тісторозкатка локшинорізка FDM220M (220 В) | 82 | free | CONFIRM(judgment) | code FDM220M exact; SP adds 'локшинорізка' |
| 3633 | FROSTY — Вітрина для топингу Frosty VRX1800/330 | FROSTY — Вітрина для топінгу VRX1800/330 (220 В) | 79 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3698 | FROSTY — Тістоміс Frosty FSV-60L | FROSTY — Тістоміс спіральний FSV-60L (220 В) | 79 | free | CONFIRM(judgment) | code FSV-60L exact; SP adds 'спіральний' |
| 3677 | Staff — Машина мультифункціональна STAFF R 151 A Med | STAFF — Машина мультифункційна R 151 A Med (380 В) | 78 | held m2029 | REJECT | PP held by m2029:confirmed (#15) |
| 3600 | Fimar — М'ясорубка Fimar TR22/TE 1ph | FIMAR — М'ясорубка TR22/TE 1ph (220 В) | 77 | free | CONFIRM | model code byte-identical; brand match; SP differs only by dropped brand word + (220 В) spec |
| 3601 | Fimar — М'ясорубка Fimar 22TE (220) | FIMAR — М'ясорубка TR22/TE 1ph (220 В) | 77 | held m125 | REJECT | PP held by m125:confirmed (#15) |
| 3602 | Fimar — М'ясорубка Fimar 22TE (380) | FIMAR — М'ясорубка TR22/TE 3ph (380 В) | 77 | held m254 | REJECT | PP held by m254:confirmed (#15) |
| 3668 | Staff — Машина мультифункціональна STAFF R 51A | STAFF — Машина мультифункційна R  51A (220 В) | 74 | held m2030 | REJECT | PP held by m2030:confirmed (#15) |
| 3687 | FROSTY — Шафа холодильна Frosty FTD400 | FROSTY — Шафа холодильна FTD200GSS (220 В) | 74 | free | REJECT | PP FTD400 vs SP FTD200GSS; SP matched exactly by m3686 — model code differs |
| 3689 | FROSTY — Шафа морозильна Frosty FBD400 | FROSTY — Шафа морозильна FBD600SS (220 В) | 74 | free | REJECT | PP FBD400 vs SP FBD600SS; SP matched exactly by m3688 — model code differs |
| 3663 | FROSTY — Подрібнювач льоду Frosty IC80A | FROSTY — Льодоподрібнювач IC80A (220 В) | 74 | free | CONFIRM(judgment) | code IC80A exact; 'Подрібнювач льоду' vs 'Льодоподрібнювач' synonym |
| 3584 | Ceado — Подрібнювач льоду CEADO V90 | CEADO — Льодоподрібнювач V90 (220 В) | 73 | held m1357 | REJECT | PP held by m1357:confirmed (#15) |
| 3614 | FROSTY — Електросупниця 10 л FROSTY SB-6000S (супник) | FROSTY — Супник електричний SB-6000S (220 В) | 69 | free | CONFIRM(judgment) | code SB-6000S exact; 'Електросупниця' vs 'Супник електричний' synonym |
| 3636 | FROSTY — Апарат SOUS VIDE FROSTY SV250 | FROSTY — Прилад SOUS VIDE SV250 (220 В) | 68 | free | CONFIRM(judgment) | code SV250 exact; 'Апарат' vs 'Прилад' SOUS VIDE synonym |

## Decisions

**CONFIRM (clean) — 55:** 3590, 3591, 3593, 3595, 3600, 3607, 3609, 3610, 3615, 3617, 3618, 3628, 3629, 3630, 3633, 3637, 3638, 3640, 3641, 3644, 3647, 3648, 3653, 3660, 3666, 3667, 3672, 3676, 3679, 3680, 3681, 3682, 3684, 3686, 3688, 3694, 3695, 3696, 3697, 3703, 3704, 3705, 3706, 3707, 3708, 3709, 3710, 3711, 3712, 3713, 3714, 3715, 3716, 3717, 3718

**CONFIRM (judgment) — 28:** 3597, 3598, 3599, 3605, 3606, 3614, 3627, 3631, 3632, 3634, 3635, 3636, 3645, 3646, 3649, 3650, 3654, 3655, 3656, 3657, 3663, 3669, 3670, 3671, 3692, 3698, 3699, 3700
  (byte-identical model code; differ only by a synonym/dropped descriptor or bundle note — see per-row reason)

**AMBIGUOUS — 0:** none. Every row resolved as either byte-identical (CONFIRM) or a decisive #15 / suffix / model-code / product-type difference (REJECT).

**REJECT — 21:**
- #15 (PP already held by confirmed match) — 10: 3584 (→m1357), 3585 (→m432), 3586 (→m433), 3587 (→m780), 3588 (→m246), 3589 (→m169), 3601 (→m125), 3602 (→m254), 3668 (→m2030), 3677 (→m2029)
- domain (suffix / model code / product-type) — 11: 3592, 3594, 3596, 3608, 3639, 3678, 3683, 3685, 3687, 3689, 3690

## Notes on shared SP ids (1 SP → 2 PP rows)

Eleven SP ids appeared on two candidate rows each. In every pair the SP model code matched ONE PP byte-for-byte and differed from the other; the exact match was kept (CONFIRM) and the mismatch rejected as a domain near-miss. Pairs: D12А sp5675 (3682✓/3683✗), D10А sp5760 (3684✓/3685✗), WS-15 sp5980 (3609✓/3608✗), FTD200GSS sp5845 (3686✓/3687✗), FBD600SS sp6015 (3688✓/3689✗), FBA-010 sp5676 (3692✓/3690✗), SP-1A2 sp5642 (3638✓/3639✗), B-10 sp5221 (3591✓/3592✗), B-20 sp5306 (3593✓/3594✗), B-40 sp5391 (3595✓/3596✗), TR22/TE-1ph sp5467 (3600✓/3601✗→#15).
