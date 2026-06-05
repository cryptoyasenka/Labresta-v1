# Candidate triage — LabResta supplier↔product matches

**Generated:** 2026-06-05 by `scripts/triage_candidates_readonly.py` (READ-ONLY)

- Match table (`__tablename__`): **`product_matches`**
- Total candidates (status='candidate'): **301**
- Per-bucket counts:
  - recommend-CONFIRM: **61**
  - NEEDS-EYEBALL: **237**
  - recommend-REJECT: **3**
  - sum check: 301 == 301

## Mutation-proof status snapshot

BEFORE:

| status | count |
|---|---:|
| candidate | 301 |
| confirmed | 2362 |
| manual | 7 |
| rejected | 71 |

AFTER (must be identical):

| status | count |
|---|---:|
| candidate | 301 |
| confirmed | 2362 |
| manual | 7 |
| rejected | 71 |

**Identical:** True

## Method

Each candidate joined to `prom_products` (PP) and `supplier_products` (SP). Normalization reuses the live matcher (`app.services.matcher`): `normalize_model` (lowercase, strip non-alnum, fix Cyrillic homoglyphs, drop `/PL`), `meaningful_tokens` (after-brand token set, voltage tags removed), `extract_voltages` (incl. 1ф/3ф→voltage), `_extract_colors`. Decision order: voltage conflict→REJECT; color conflict→REJECT; brand mismatch→REJECT; then CONFIRM if (normalized names identical & score≥85) OR (SP article ∈ BOTH display_article AND name/name_ru, brand match, score≥80, no one-sided SKU-tail diff) OR (article==display_article, brand match, clean subset tokens, score≥90); then REJECT for suffix-variant near-miss (one-sided short-alpha/digit SKU tail) or anchor article absent from name+display with Jaccard token overlap <0.5; everything else → NEEDS-EYEBALL. Brand 'match' = exact or normalized containment; 'unknown' if either side blank (never auto-CONFIRM on unknown brand unless names are identical).

## recommend-CONFIRM (61)

### novyy-proekt (НП) (5)

| match_id | PP (id / article / display_article / brand) | PP name | SP (id / supplier / article / brand) | SP name | score | reason |
|---:|---|---|---|---|---:|---|
| 3352 | 3921 / `` / `` / Bartscher | Подрібнювач льоду Bartscher 135023 | 5142 / novyy-proekt (НП) / `135023` / Bartscher | Подрібнювач льоду Bartscher (135023) | 100 | normalized name identical (score 100) |
| 3357 | 4630 / `` / `40602300` / Sirman | ТЕРМОПАКУВАЛЬНИЙ АПАРАТ SIRMAN 45К СЕ | 5122 / novyy-proekt (НП) / `45К СЕ` / Sirman | Термопакувальний апарат Sirman 45к се | 100 | normalized name identical (score 100) |
| 4376 | 956 / `` / `A150512` / Bartscher | Підігрівач рису Bartscher A150512 | 4641 / novyy-proekt (НП) / `150512` / Bartscher | Марміт для риса (A150512) | 100 | article '150512' in display+name, brand match, score 100 |
| 3365 | 3298 / `` / `2214` / Robot Coupe | Овочерізка Robot Coupe CL55 з важелем | 4484 / novyy-proekt (НП) / `CL 55 230v` / Robot Coupe | Овочерізка Robot Coupe CL 55 з важелем 230в | 95 | identical token set (word-order diff), brand match, score 95 |
| 3369 | 3712 / `` / `56000B` / Robot Coupe | Соковитискач Robot Coupe J80 | 5131 / novyy-proekt (НП) / `J80 Ultra` / Robot Coupe | Соковижималка Robot Coupe J80 | 88 | normalized name identical (score 88) |

### rp-ukrayina (12)

| match_id | PP (id / article / display_article / brand) | PP name | SP (id / supplier / article / brand) | SP name | score | reason |
|---:|---|---|---|---|---:|---|
| 3729 | 3206 / `` / `` / Sirman | Куттер Sirman C9VV (9,4 л) | 6884 / rp-ukrayina / `` / Sirman | Куттер SIRMAN C 9 VV | 100 | identical token set (word-order diff), brand match, score 100 |
| 3730 | 2966 / `` / `211215D2` / Sirman | М'ясорубка SIRMAN TC-12 DENVER | 6887 / rp-ukrayina / `` / Sirman | М'ясорубка SIRMAN TC-12 DENVER | 100 | normalized name identical (score 100) |
| 3735 | 4902 / `` / `` / Sirman | Стерилізатор для ножів Sirman U.V.A. 16 W | 6911 / rp-ukrayina / `` / Sirman | Стерилізатор для ножів SIRMAN U.V.A. 16W | 100 | normalized name identical (score 100) |
| 3743 | 1193 / `` / `` / Unox | Піч пароконвекційна Unox XEFR03EUELDV | 6958 / rp-ukrayina / `` / Unox | Піч пароконвекційна UNOX XEFR-03EU-ELDV | 100 | normalized name identical (score 100) |
| 3748 | 1246 / `` / `` / Unox | Піч пароконвекційна Unox XEFR03HSELDP | 6959 / rp-ukrayina / `` / Unox | Піч пароконвекційна UNOX XEFR-03HS-ELDP | 100 | normalized name identical (score 100) |
| 3754 | 1243 / `` / `` / Unox | Піч пароконвекційна Unox XEFR04EUELDV | 6961 / rp-ukrayina / `` / Unox | Піч пароконвекційна UNOX XEFR-04EU-ELDV | 100 | normalized name identical (score 100) |
| 3760 | 1037 / `` / `` / Unox | Піч пароконвекційна UNOX XFT193 | 6986 / rp-ukrayina / `` / Unox | Піч пароконвекційна UNOX XFT193 | 100 | normalized name identical (score 100) |
| 3779 | 1244 / `` / `` / Unox | Піч пароконвекційна Unox XEFR10EUELRVDR | 6965 / rp-ukrayina / `` / Unox | Піч пароконвекційна UNOX XEFR-10EU-ELRV-DR | 100 | normalized name identical (score 100) |
| 3784 | 1249 / `` / `` / Unox | Піч подова Unox XEBDC02EUD | 6987 / rp-ukrayina / `` / Unox | Піч подова UNOX XEBDC-02EU-D | 100 | normalized name identical (score 100) |
| 3785 | 1248 / `` / `` / Unox | Піч подова Unox XEBDC01EUD | 6988 / rp-ukrayina / `` / Unox | Піч подова UNOX XEBDC-01EU-D | 100 | normalized name identical (score 100) |
| 3722 | 4169 / `` / `` / Airhot | Марміт для супу AIRHOT SB-5700 | 6685 / rp-ukrayina / `` / AIRHOT | Марміт для супу АIRHOT SB-5700 | 97 | normalized name identical (score 97) |
| 3723 | 4170 / `` / `` / Airhot | Марміт для супу AIRHOT SB-6000 | 6687 / rp-ukrayina / `` / AIRHOT | Марміт для супу АIRHOT SB-6000 | 97 | normalized name identical (score 97) |

### guder (44)

| match_id | PP (id / article / display_article / brand) | PP name | SP (id / supplier / article / brand) | SP name | score | reason |
|---:|---|---|---|---|---:|---|
| 3815 | 2134 / `` / `` / Gooder | Вітрина кондитерська Gooder FC-400RA | 7160 / guder / `FC-400RA` / Gooder | Кондитерська вітрина FC-400RA Gooder | 100 | identical token set (word-order diff), brand match, score 100 |
| 3818 | 2506 / `` / `` / Gooder | Вітрина кондитерська Gooder FC-600RA | 7162 / guder / `FC-600RA` / Gooder | Кондитерська вітрина FC-600RA Gooder | 100 | identical token set (word-order diff), brand match, score 100 |
| 3819 | 2136 / `` / `` / Gooder | Вітрина кондитерська Gooder FC-400SA Cube | 7164 / guder / `FC-400SA` / Gooder | Кондитерська вітрина FC-400SA Cube Gooder | 100 | identical token set (word-order diff), brand match, score 100 |
| 3822 | 2509 / `` / `` / Gooder | Вітрина кондитерська Gooder FC-700SA Cube | 7166 / guder / `FC-700SA` / Gooder | Кондитерська вітрина FC-700SA Cube Gooder | 100 | identical token set (word-order diff), brand match, score 100 |
| 3827 | 2137 / `` / `` / Gooder | Вітрина кондитерська Gooder FC-400SCD Cube | 7171 / guder / `FC-400SCD` / Gooder | Кондитерська вітрина FC-400SCD Cube Gooder | 100 | identical token set (word-order diff), brand match, score 100 |
| 3830 | 2508 / `` / `` / Gooder | Вітрина кондитерська Gooder FC-600SCD Cube | 7173 / guder / `FC-600SCD` / Gooder | Кондитерська вітрина FC-600SCD Cube Gooder | 100 | identical token set (word-order diff), brand match, score 100 |
| 3846 | 2184 / `` / `` / Gooder | Вітрина кондитерська Gooder XC-275 CUBE | 7242 / guder / `XC-275 CUBE` / Gooder | Кондитерська вітрина XC-275 CUBE Gooder | 100 | identical token set (word-order diff), brand match, score 100 |
| 3849 | 2216 / `` / `` / Gooder | Морозильна скриня Gooder UDD 600 BK | 7244 / guder / `UDD 600 BK` / Gooder | Морозильна скриня  UDD 600 BK Gooder | 100 | identical token set (word-order diff), brand match, score 100 |
| 3857 | 2238 / `` / `` / Gooder | Вітрина холодильна Gooder XC-440С | 7278 / guder / `XC-440С` / Gooder | Вітрина  холодильна XC-440С Gooder | 100 | identical token set (word-order diff), brand match, score 100 |
| 3858 | 2245 / `` / `` / Gooder | Скриня морозильна Gooder UDD 500 SC | 7280 / guder / `UDD 500 SC` / Gooder | Морозильна скриня UDD 500 SC Gooder | 100 | identical token set (word-order diff), brand match, score 100 |
| 3859 | 2249 / `` / `` / Gooder | Холодильна вітрина-гірка Gooder XC-520 Cube | 7293 / guder / `XC-520 Cube` / Gooder | Холодильна вітрина-гірка XC-520 Cube Gooder | 100 | identical token set (word-order diff), brand match, score 100 |
| 3861 | 4105 / `` / `` / Gooder | Теплова вітрина Gooder XCR-45L | 7295 / guder / `XCR-45L` / Gooder | Теплова вітрина XCR-45L Gooder | 100 | identical token set (word-order diff), brand match, score 100 |
| 3864 | 2259 / `` / `` / Gooder | Морозильна скриня UDD 465 TDS Gooder | 7328 / guder / `UDD 465 TDS Gooder` / Gooder | Морозильна скриня UDD 465 TDS Gooder | 100 | normalized name identical (score 100) |
| 4384 | 2504 / `` / `` / Gooder | Вітрина кондитерська Gooder FC-500RA | 7161 / guder / `FC-500RA` / Gooder | Кондитерська вітрина FC-500RA Gooder | 100 | identical token set (word-order diff), brand match, score 100 |
| 4385 | 2142 / `` / `` / Gooder | Вітрина кондитерська Gooder FC-700RA | 7163 / guder / `FC-700RA` / Gooder | Кондитерська вітрина FC-700RA Gooder | 100 | identical token set (word-order diff), brand match, score 100 |
| 4386 | 2507 / `` / `` / Gooder | Вітрина кондитерська Gooder FC-600SA Cube | 7165 / guder / `FC-600SA` / Gooder | Кондитерська вітрина FC-600SA Cube Gooder | 100 | identical token set (word-order diff), brand match, score 100 |
| 4389 | 2139 / `` / `` / Gooder | Вітрина кондитерська Gooder FC-500SCD Cube | 7172 / guder / `FC-500SCD` / Gooder | Кондитерська вітрина FC-500SCD Cube Gooder | 100 | identical token set (word-order diff), brand match, score 100 |
| 4390 | 2141 / `` / `` / Gooder | Вітрина кондитерська Gooder FC-700SCD Cube | 7174 / guder / `FC-700SCD` / Gooder | Кондитерська вітрина FC-700SCD Cube Gooder | 100 | identical token set (word-order diff), brand match, score 100 |
| 4398 | 2138 / `` / `` / Gooder | Вітрина кондитерська Gooder FC-500SA Cube | 7210 / guder / `FC-500SA` / Gooder | Кондитерська вітрина FC-500SA Cube Gooder | 100 | identical token set (word-order diff), brand match, score 100 |
| 4412 | 2185 / `` / `` / Gooder | Вітрина кондитерська Gooder XC-375 CUBE | 7243 / guder / `XC-375 CUBE` / Gooder | Кондитерська вітрина XC-375 CUBE Gooder | 100 | identical token set (word-order diff), brand match, score 100 |
| 4420 | 1316 / `` / `` / Gooder | Моноблок SGM012P Gooder | 7271 / guder / `SGM012PGooder` / Gooder | Моноблок SGM012P Gooder | 100 | normalized name identical (score 100) |
| 4422 | 1318 / `` / `` / Gooder | Моноблок SGM008P Gooder | 7274 / guder / `SGM008PGooder` / Gooder | Моноблок SGM008P Gooder | 100 | normalized name identical (score 100) |
| 4423 | 2236 / `` / `` / Gooder | Вітрина холодильна Gooder XC-218L | 7276 / guder / `XC-218L` / Gooder | Вітрина  холодильна XC-218L Gooder | 100 | identical token set (word-order diff), brand match, score 100 |
| 4424 | 2237 / `` / `` / Gooder | Вітрина холодильна Gooder XC-238L | 7277 / guder / `XC-238L` / Gooder | Вітрина  холодильна XC-238L Gooder | 100 | identical token set (word-order diff), brand match, score 100 |
| 4426 | 2642 / `` / `` / Gooder | Скриня морозильна Gooder UDD 600 SC | 7281 / guder / `UDD 600 SC` / Gooder | Морозильна скриня UDD 600 SC Gooder | 100 | identical token set (word-order diff), brand match, score 100 |
| 4427 | 2215 / `` / `` / Gooder | Морозильна скриня Gooder UDD 500 BK | 7292 / guder / `UDD 500 BK` / Gooder | Морозильна скриня  UDD 500 BK Gooder | 100 | identical token set (word-order diff), brand match, score 100 |
| 4428 | 2250 / `` / `` / Gooder | Холодильна вітрина-гірка Gooder XC-720 Cube | 7294 / guder / `XC-720 Cube` / Gooder | Холодильна вітрина-гірка XC-720 Cube Gooder | 100 | identical token set (word-order diff), brand match, score 100 |
| 4429 | 4104 / `` / `` / Gooder | Теплова вітрина Gooder XCR-50L Cube | 7296 / guder / `XCR-50L Cube` / Gooder | Теплова вітрина XCR-50L Cube Gooder | 100 | identical token set (word-order diff), brand match, score 100 |
| 4432 | 2252 / `` / `` / Gooder | Вітрина холодильна XC-278L Gooder | 7325 / guder / `XC-278L` / Gooder | Вітрина холодильна XC-278L Gooder | 100 | normalized name identical (score 100) |
| 4434 | 2258 / `` / `` / Gooder | Морозильна скриня UDD 400 SC Gooder | 7327 / guder / `UDD 400 SC Gooder` / Gooder | Морозильна скриня UDD 400 SC Gooder | 100 | normalized name identical (score 100) |
| 4435 | 2257 / `` / `` / Gooder | Морозильна скриня UDD 365 TDS Gooder | 7329 / guder / `UDD 365 TDS Gooder` / Gooder | Морозильна скриня UDD 365 TDS Gooder | 100 | normalized name identical (score 100) |
| 3823 | 2135 / `` / `` / Gooder | Вітрина кондитерська Gooder FC-400RCD | 7167 / guder / `FC-400 RCD` / Gooder | Кондитерська вітрина FC-400RCD Gooder | 95 | identical token set (word-order diff), brand match, score 95 |
| 3826 | 2505 / `` / `` / Gooder | Вітрина кондитерська Gooder FC-500RCD | 7168 / guder / `FC-500 RCD` / Gooder | Кондитерська вітрина FC-500RCD Gooder | 95 | identical token set (word-order diff), brand match, score 95 |
| 3836 | 1398 / `` / `` / Gooder | Стіл холодильний Gooder S-903PZ | 7208 / guder / `S-903PZ Gooder` / Gooder | Холодильний стіл S-903PZ Gooder | 95 | identical token set (word-order diff), brand match, score 95 |
| 3839 | 1396 / `` / `` / Gooder | Стіл холодильний Gooder PZ2600TN | 7215 / guder / `PZ2600TN Gooder` / Gooder | Холодильний стіл PZ2600TN Gooder | 95 | identical token set (word-order diff), brand match, score 95 |
| 3852 | 2190 / `` / `` / Gooder | Вітрина холодильна Gooder BX-1290 Cube | 7245 / guder / `BX-1290 CubeGooder` / Gooder | Вітрина холодильна BX-1290 Cube Gooder | 95 | identical token set (word-order diff), brand match, score 95 |
| 3854 | 2192 / `` / `` / Gooder | Вітрина холодильна Gooder BX-2090 Cube | 7247 / guder / `BX-2090 CubeGooder` / Gooder | Вітрина холодильна BX-2090 Cube Gooder | 95 | identical token set (word-order diff), brand match, score 95 |
| 4387 | 2140 / `` / `` / Gooder | Вітрина кондитерська Gooder FC-600RCD | 7169 / guder / `FC-600 RCD` / Gooder | Кондитерська вітрина FC-600RCD Gooder | 95 | identical token set (word-order diff), brand match, score 95 |
| 4388 | 2143 / `` / `` / Gooder | Вітрина кондитерська Gooder FC-700RCD | 7170 / guder / `FC-700 RCD` / Gooder | Кондитерська вітрина FC-700RCD Gooder | 95 | identical token set (word-order diff), brand match, score 95 |
| 4397 | 1395 / `` / `` / Gooder | Стіл холодильний Gooder PS900 | 7209 / guder / `PS900 Gooder` / Gooder | Холодильний стіл PS900 Gooder | 95 | identical token set (word-order diff), brand match, score 95 |
| 4399 | 1397 / `` / `` / Gooder | Стіл холодильний Gooder PZ3600TN | 7216 / guder / `PZ3600TN Gooder` / Gooder | Холодильний стіл PZ3600TN Gooder | 95 | identical token set (word-order diff), brand match, score 95 |
| 4413 | 2191 / `` / `` / Gooder | Вітрина холодильна Gooder BX-1590 Cube | 7246 / guder / `BX-1590 CubeGooder` / Gooder | Вітрина холодильна BX-1590 Cube Gooder | 95 | identical token set (word-order diff), brand match, score 95 |
| 4418 | 2613 / `` / `` / Gooder | Вітрина саладетта Gooder VRX1200/330 | 7252 / guder / `VRX1200/330 Gooder` / Gooder | Вітрина саладетта VRX1200/330 Gooder | 95 | identical token set (word-order diff), brand match, score 95 |
| 4419 | 2614 / `` / `` / Gooder | Вітрина саладетта Gooder VRX1200/380 | 7253 / guder / `VRX1200/380 Gooder` / Gooder | Вітрина саладетта VRX1200/380 Gooder | 95 | identical token set (word-order diff), brand match, score 95 |

## NEEDS-EYEBALL (237)

### maresto (15)

| match_id | PP (id / article / display_article / brand) | PP name | SP (id / supplier / article / brand) | SP name | score | reason |
|---:|---|---|---|---|---:|---|
| 3787 | 2014 / `` / `` / Cuppone | Прес для піци Cuppone PZF/40DS, діаметр піци 40 см | 849 / maresto / `` / Cuppone | Прес для піци Cuppone PZF40DS | 100 | score 100; brand match; jacc 0.50; no SP article |
| 3788 | 3028 / `` / `` / Sirman | М'ясорубка SIRMAN TC 32 NEVADA 3PH non-CE + TOTAL UNGER | 1134 / maresto / `` / Sirman | М'ясорубка Sirman TC32 Nevada CE (380) | 100 | score 100; brand match; jacc 0.44; no SP article |
| 3790 | 3330 / `` / `` / Sirman | Слайсер Sirman TOPAZ 195 | 4189 / maresto / `` / Sirman | Слайсер Sirman TOPAZ 195 Normale | 100 | score 100; brand match; jacc 0.67; no SP article |
| 3793 | 4500 / `` / `` / Asber | Посудомийка купольна Asber GEX-H500 DD | 2959 / maresto / `` / ASBER | Посудомийна машина Asber GEXH500DD | 100 | score 100; brand match; jacc 1.00; no SP article; product-type word clash |
| 3794 | 1035 / `` / `` / Unox | Пароконвектомат Unox XV893 на 12 рівнів GN1/1 | 1865 / maresto / `` / Unox | Пароконвектомат Unox XV893 Cheflux | 100 | score 100; brand match; jacc 0.25; no SP article |
| 3795 | 1178 / `` / `` / Unox | Піч пароконвекційна Unox XEBC06EUE1RMMP, універсальна на 6 рівнів | 576 / maresto / `` / Unox | Піч пароконвекційна Unox XEBC06EUE1RMMP лінія ONE | 100 | score 100; brand match; jacc 0.45; no SP article |
| 3796 | 1179 / `` / `` / Unox | Піч пароконвекційна Unox XEBC10EUE1RMMP, універсальна на 10 рівнів | 577 / maresto / `` / Unox | Піч пароконвекційна Unox XEBC10EUE1RMMP лінія ONE | 100 | score 100; brand match; jacc 0.50; no SP article |
| 3797 | 1180 / `` / `` / Unox | Піч пароконвекційна Unox XEBC04EUE1RMMP, універсальна на 4 рівні | 580 / maresto / `` / Unox | Піч пароконвекційна Unox XEBC04EUE1RMMP лінія ONE | 100 | score 100; brand match; jacc 0.45; no SP article |
| 3798 | 1305 / `` / `` / Unox | Пароконвектомат Unox XEBC04EUEPRMMP 4 рівня | 581 / maresto / `` / Unox | Піч пароконвекційна Unox XEBC04EUEPRMMP лінія PLUS | 100 | score 100; brand match; jacc 0.43; no SP article; product-type word clash |
| 3799 | 1044 / `` / `` / Unox | Піч пароконвекційна Unox XV393 на 5 рівнів | 150 / maresto / `` / Unox | Пароконвектомат Unox XV393 Cheflux | 100 | score 100; brand match; jacc 0.33; no SP article; product-type word clash |
| 3800 | 1034 / `` / `` / Unox | Пароконвектомат Unox XV593 на 7 рівнів GN1/1 | 2871 / maresto / `` / Unox | Пароконвектомат Unox XV593 Cheflux | 100 | score 100; brand match; jacc 0.25; no SP article |
| 3791 | 1643 / `` / `` / Tecnodom | Стіл холодильний Tecnodom TF03MIDGNAL NEW | 4405 / maresto / `` / Tecnodom | Стіл холодильний Tecnodom TF03MIDGN | 92 | score 92; brand match; jacc 0.40; no SP article |
| 3792 | 3486 / `` / `` / Sirman | Пила стрічкова гастрономічна Sirman SO 1650 F3 (220) | 3829 / maresto / `` / Sirman | Пила стрічкова електрична Sirman SO1650F3 (220) | 87 | score 87; brand match; jacc 1.00; no SP article; product-type word clash |
| 3786 | 3707 / `` / `67003702` / Sirman | Соковичавниця шнекова Sirman Ektor 37 для твердих фруктів і овочів | 2709 / maresto / `` / Sirman | Соковижималка ел. Sirman Ektor 37 | 86 | score 86; brand match; jacc 0.33; no SP article; product-type word clash |
| 3789 | 2938 / `` / `` / Sirman | Прес макаронний SIRMAN Sinfonia 2 | 3352 / maresto / `` / Sirman | Машина для виробництва макароних виробів Sirman Sinfonia2 | 86 | score 86; brand match; jacc 1.00; no SP article; product-type word clash |

### novyy-proekt (НП) (22)

| match_id | PP (id / article / display_article / brand) | PP name | SP (id / supplier / article / brand) | SP name | score | reason |
|---:|---|---|---|---|---:|---|
| 3353 | 972 / `` / `` / Bartscher | Рисоварка 12 л Bartscher 150529 | 4727 / novyy-proekt (НП) / `150529` / Bartscher | Мультиварка на 40-60 персон (150529) | 100 | score 100; brand match; jacc 0.00; anchor∈name; SP article is internal-id (not SKU) |
| 3358 | 717 / `` / `` / Bartscher | Мікрохвильова піч Bartscher 610836 | 4741 / novyy-proekt (НП) / `610836` / Bartscher | Піч нвч Bartscher 23л (610836) | 100 | score 100; brand match; jacc 0.00; anchor∈name; SP article is internal-id (not SKU); product-type word clash |
| 3362 | 315 / `` / `` / Apach | Поверхня для смаження APACH APTE-47PR, гладка | 4767 / novyy-proekt (НП) / `APTE-47PR/PL` / APACH | Поверхня для смаження Apach APTE-47PR/PL ребр. сталь | 100 | score 100; brand match; jacc 0.43; anchor∈name |
| 3363 | 316 / `` / `` / Apach | Поверхня для смаження APACH APTE-77PLR, комбінована | 4736 / novyy-proekt (НП) / `APTE-77PLR/PL` / APACH | Поверхня для смаження Apach APTE-77PLR/PL гл. + ребр. сталь | 100 | score 100; brand match; jacc 0.38; anchor∈name |
| 3382 | 3796 / `` / `` / Sirman | Міксер молочний Sirman Sirio 2 VV ХРОМ CC 900 | 5136 / novyy-proekt (НП) / `SIRIO 2` / Sirman | Міксер Sirman Sirio 2 VV хром CE | 100 | score 100; brand match; jacc 0.57; anchor∈name; product-type word clash |
| 3383 | 923 / `` / `` / Sirman | Термопроцесор Sirman SoftCooker XP S GN 2/3 (приготування за технологією Sous Vide) | 4896 / novyy-proekt (НП) / `SOFTCOOKER XP` / Sirman | Апарат низькотемпературного приготування Sirman Softcooker XP | 100 | score 100; brand match; jacc 0.33; anchor∈name; SP article is internal-id (not SKU); product-type word clash |
| 3384 | 948 / `` / `A150513` / Bartscher | Рисоварка 8 л Bartscher A150513 | 4728 / novyy-proekt (НП) / `А150.513` / Bartscher | Мультиварка Bartscher на 25-40 персон (A150513) | 100 | score 100; brand match; jacc 0.00; anchor∈display; anchor∈name; SP article is internal-id (not SKU); product-type word clash |
| 3377 | 3059 / `` / `34870L` / Robot Coupe | Міксер заглибний Robot Coupe MP450 Combi Ultra | 4498 / novyy-proekt (НП) / `MP 450 COMBI ULTRA` / Robot Coupe | Міксер ручний Robot Coupe MP 450 Combi Ultra | 90 | score 90; brand match; jacc 1.00; anchor∈name; product-type word clash |
| 3373 | 3051 / `` / `34780` / Robot Coupe | Міксер погружний Robot Coupe Mini MP240 Combi | 5137 / novyy-proekt (НП) / `MINI MP 240 COMBI` / Robot Coupe | Міксер ручний-міні Robot Coupe Mini MP 240 Combi | 89 | score 89; brand match; jacc 1.00; anchor∈name; product-type word clash |
| 3368 | 3054 / `` / `34310B` / Robot Coupe | Міксер заглибний Robot Coupe CMP300 Combi | 5045 / novyy-proekt (НП) / `CMP 300 COMBI` / Robot Coupe | Міксер ручний Robot Coupe CMP 300 Combi | 89 | score 89; brand match; jacc 1.00; anchor∈name; product-type word clash |
| 3374 | 3050 / `` / `34760` / Robot Coupe | Міксер погружний Robot Coupe Mini MP240VV | 5140 / novyy-proekt (НП) / `MINI MP 240 VV` / Robot Coupe | Міксер ручний-міні Robot Coupe Mini MP 240 VV | 89 | score 89; brand match; jacc 1.00; anchor∈name; product-type word clash |
| 3379 | 3105 / `` / `` / Robot Coupe | Міксер заглибний Robot Coupe MP450 Ultra | 4492 / novyy-proekt (НП) / `MP 450 ULTRA` / Robot Coupe | Міксер ручний Robot Coupe MP 450 Ultra | 89 | score 89; brand match; jacc 1.00; anchor∈name; product-type word clash |
| 3366 | 3056 / `` / `34300В` / Robot Coupe | Міксер занурювальний Robot Coupe CMP250 Combi | 4478 / novyy-proekt (НП) / `CMP 250 COMBI` / Robot Coupe | Міксер ручний Robot Coupe CMP 250 Combi | 87 | score 87; brand match; jacc 1.00; anchor∈name; product-type word clash |
| 3367 | 3053 / `` / `34240B` / Robot Coupe | Міксер занурювальний Robot Coupe CMP250VV | 5054 / novyy-proekt (НП) / `CMP 250 VV` / Robot Coupe | Міксер ручний Robot Coupe CMP 250 VV | 86 | score 86; brand match; jacc 1.00; anchor∈name; product-type word clash |
| 3375 | 3060 / `` / `34860L` / Robot Coupe | Міксер заглибний Robot Coupe MP350 Combi Ultra | 4499 / novyy-proekt (НП) / `MP 350` / Robot Coupe | Міксер ручний Robot Coupe MP 350 Ultra | 85 | score 85; brand match; jacc 0.75; anchor∈name; product-type word clash |
| 3381 | 3098 / `` / `` / Robot Coupe | Міксер погружний Robot Coupe MP550 ULTRA 34820LH | 4502 / novyy-proekt (НП) / `MP 550 ULTRA` / Robot Coupe | Міксер ручний Robot Coupe MP 550 Ultra | 85 | score 85; brand match; jacc 0.60; anchor∈name; product-type word clash |
| 3354 | 4505 / `` / `` / Asber | Посудомийна машина ASBER GE500DD фронтальна | 4657 / novyy-proekt (НП) / `19047938` / ASBER | Посудомийка фронтальна Asber GE-500 DD | 85 | score 85; brand match; jacc 0.75; SP article is internal-id (not SKU); product-type word clash |
| 3372 | 3049 / `` / `34750` / Robot Coupe | Міксер заглибний Robot Coupe Mini MP190VV | 5138 / novyy-proekt (НП) / `MINI MP 190 VV` / Robot Coupe | Міксер ручний-міні Robot Coupe Mini MP 190 VV | 84 | score 84; brand match; jacc 1.00; anchor∈name; product-type word clash |
| 4377 | 3300 / `` / `2319` / Robot Coupe | Овочерізка Robot Coupe CL60 з важелем | 4480 / novyy-proekt (НП) / `CL 60` / Robot Coupe | Овочерізка Robot Coupe CL 60 2 лійки | 84 | score 84; brand match; jacc 0.40; anchor∈name |
| 3370 | 3048 / `` / `34740` / Robot Coupe | Міксер занурювальний Robot Coupe Mini MP160VV | 4734 / novyy-proekt (НП) / `MINI MP 160 VV` / Robot Coupe | Міксер ручний-міні Robot Coupe Mini MP 160 VV | 83 | score 83; brand match; jacc 1.00; anchor∈name; product-type word clash |
| 3371 | 3052 / `` / `34770` / Robot Coupe | Міксер який Robot Coupe Mini MP190 Combi з вінчиком | 5141 / novyy-proekt (НП) / `MINI MP 190 COMBI` / Robot Coupe | Міксер ручний-міні Robot Coupe Mini MP 190 Combi | 81 | score 81; brand match; jacc 0.80; anchor∈name; product-type word clash |
| 4378 | 3786 / `` / `` / Ceado | Міксер молочний CEADO M98/2 двохпостовий | 5100 / novyy-proekt (НП) / `M98/2` / CEADO | Міксер Ceado подвійний M98/2 | 75 | score 75; brand match; jacc 0.60; anchor∈name; product-type word clash |

### kodaki (104)

| match_id | PP (id / article / display_article / brand) | PP name | SP (id / supplier / article / brand) | SP name | score | reason |
|---:|---|---|---|---|---:|---|
| 3645 | 1943 / `` / `AF-37R/120` / GI.Metal | Лопата для піци Gi Metal AF-37R/120 Aurora | 6394 / kodaki / `000005977` / GI.METAL | AF-37R/120 Лопата для піци | 100 | score 100; brand match; jacc 0.50; SP article is internal-id (not SKU) |
| 3646 | 1945 / `` / `AF-45R/120` / GI.Metal | Лопата для піци Gi Metal AF-45R/120 Aurora | 5210 / kodaki / `000005979` / GI.METAL | AF-45R/120 Лопата для піци | 100 | score 100; brand match; jacc 0.50; SP article is internal-id (not SKU) |
| 3654 | 51 / `` / `70-KPP1` / FROSTY | Плита індукційна FROSTY 70-KPP1 настільна | 6068 / kodaki / `000006436` / FROSTY | Плита індукційна 70-KPP1 (220 В) | 100 | score 100; brand match; jacc 0.50; SP article is internal-id (not SKU) |
| 3605 | 2847 / `` / `` / Imperia | Тісторозкатка ручна HOME iPASTA SFOGLIATRICE cod.162 | 5484 / kodaki / `000003892` / IMPERIA | 162 Тісторозкатка iPASTA Sfogliatrice | 95 | score 95; brand match; jacc 0.57; SP article is internal-id (not SKU) |
| 3628 | 3091 / `` / `` / FROSTY | Ніж-змішувач Frosty BLD300 | 6085 / kodaki / `000005579` / FROSTY | Ніж-змішувач BLD300 | 95 | score 95; brand match; jacc 0.50; SP article is internal-id (not SKU) |
| 3682 | 3595 / `` / `` / FROSTY | Диск для овочерізки Frosty D12А | 5675 / kodaki / `000008402` / FROSTY | Диск для овочерізки D12А | 95 | score 95; brand match; jacc 0.40; SP article is internal-id (not SKU) |
| 3684 | 3594 / `` / `` / FROSTY | Диск для овочерізки Frosty D10А | 5760 / kodaki / `000008403` / FROSTY | Диск для овочерізки D10А | 95 | score 95; brand match; jacc 0.40; SP article is internal-id (not SKU) |
| 3683 | 3520 / `` / `` / FROSTY | Диск для овочерізки Frosty D12 | 5675 / kodaki / `000008402` / FROSTY | Диск для овочерізки D12А | 91 | score 91; brand match; jacc 0.40; SP article is internal-id (not SKU) |
| 3685 | 3564 / `` / `` / FROSTY | Диск для овочерізки Frosty D10 | 5760 / kodaki / `000008403` / FROSTY | Диск для овочерізки D10А | 91 | score 91; brand match; jacc 0.40; SP article is internal-id (not SKU) |
| 3585 | 3279 / `` / `` / Fimar | Овочерізка Fimar TV2500 (220) | 5469 / kodaki / `000001491` / FIMAR | Овочерізка TV2500 (220 В) | 91 | score 91; brand match; jacc 0.67; SP article is internal-id (not SKU) |
| 3586 | 3280 / `` / `` / Fimar | Овочерізка Fimar TV3000 (220) | 5638 / kodaki / `000001493` / FIMAR | Овочерізка TV3000 (220 В) | 91 | score 91; brand match; jacc 0.67; SP article is internal-id (not SKU) |
| 3587 | 3263 / `` / `` / Fimar | Овочерізка Fimar TV4000 (220) | 5808 / kodaki / `000001495` / FIMAR | Овочерізка TV4000 (220 В) | 91 | score 91; brand match; jacc 0.67; SP article is internal-id (not SKU) |
| 3648 | 1694 / `` / `` / FROSTY | Апарат для приготування морозива Frosty ICM-15A | 6224 / kodaki / `000006158` / FROSTY | Апарат для приготування морозива ICM-15A (220 В) | 89 | score 89; brand match; jacc 0.43; SP article is internal-id (not SKU) |
| 3672 | 2878 / `` / `` / FROSTY | Тісторозкатка -локшинорізка Frosty FDM180 | 5885 / kodaki / `000007494` / FROSTY | Тісторозкатка локшинорізка FDM180 (220 В) | 87 | score 87; brand match; jacc 0.50; SP article is internal-id (not SKU) |
| 3598 | 2848 / `` / `` / Imperia | Тісторозкатка з мотором HOME iPASTA Electric cod.650 | 6496 / kodaki / `000001918` / IMPERIA | 650 Тісторозкатка iPASTA ELECTRIC (220 В) | 87 | score 87; brand match; jacc 0.57; SP article is internal-id (not SKU) |
| 3709 | 5543 / `` / `` / FROSTY | Шафа холодильна Frosty RT235C-3, black | 6533 / kodaki / `000009079` / FROSTY | Шафа холодильна RT235C-3, black (220 В) | 87 | score 87; brand match; jacc 0.71; SP article is internal-id (not SKU) |
| 3710 | 5542 / `` / `` / FROSTY | Шафа холодильна Frosty RT215C-3, black | 5267 / kodaki / `000009080` / FROSTY | Шафа холодильна RT215C-3, black (220 В) | 87 | score 87; brand match; jacc 0.71; SP article is internal-id (not SKU) |
| 3711 | 5544 / `` / `` / FROSTY | Шафа холодильна Frosty RT280C-3, black | 5352 / kodaki / `000009081` / FROSTY | Шафа холодильна RT280C-3, black (220 В) | 87 | score 87; brand match; jacc 0.71; SP article is internal-id (not SKU) |
| 3615 | 2854 / `` / `` / FROSTY | Тісторозкатка FROSTY M42A для коржів | 5461 / kodaki / `000004587` / FROSTY | Тісторозкатка для коржів M42A (220 В) | 87 | score 87; brand match; jacc 0.83; SP article is internal-id (not SKU) |
| 3635 | 35 / `` / `` / FROSTY | Плита індукційна WOK FROSTY G35-KA18 настільна | 5813 / kodaki / `000005847` / FROSTY | Плита індукційна WOK G35-KA18 (220 В) | 87 | score 87; brand match; jacc 0.50; SP article is internal-id (not SKU) |
| 3653 | 3190 / `` / `` / Fimar | Тертка-подрiбнювач Fimar GR12/S 1ph | 6248 / kodaki / `000006312` / FIMAR | Тертка-подрiбнювач GR12/S 1ph (220 В) | 87 | score 87; brand match; jacc 0.71; SP article is internal-id (not SKU) |
| 3695 | 647 / `` / `` / FROSTY | Фритюрниця електрична Frosty EFS-6L-2 | 6194 / kodaki / `000008950` / FROSTY | Фритюрниця електрична EFS- 6L-2 (220 В) | 87 | score 87; brand match; jacc 0.67; SP article is internal-id (not SKU) |
| 3703 | 5535 / `` / `` / FROSTY | Шафа холодильна Frosty RT-58B-1 Black | 5436 / kodaki / `000009073` / FROSTY | Шафа холодильна RT-58B-1, black (220 В) | 87 | score 87; brand match; jacc 0.71; SP article is internal-id (not SKU) |
| 3704 | 5536 / `` / `` / FROSTY | Шафа холодильна Frosty RT-58B-3 Black | 6114 / kodaki / `000009074` / FROSTY | Шафа холодильна RT-58B-3, black (220 В) | 87 | score 87; brand match; jacc 0.71; SP article is internal-id (not SKU) |
| 3705 | 5537 / `` / `` / FROSTY | Шафа холодильна Frosty RT-78B-1 Black | 6199 / kodaki / `000009075` / FROSTY | Шафа холодильна RT-78B-1, black (220 В) | 87 | score 87; brand match; jacc 0.71; SP article is internal-id (not SKU) |
| 3706 | 5538 / `` / `` / FROSTY | Шафа холодильна Frosty RT-78B-3 Black | 6284 / kodaki / `000009076` / FROSTY | Шафа холодильна RT-78B-3, black (220 В) | 87 | score 87; brand match; jacc 0.71; SP article is internal-id (not SKU) |
| 3707 | 5540 / `` / `` / FROSTY | Шафа холодильна Frosty RT-98B-1 Black | 6367 / kodaki / `000009077` / FROSTY | Шафа холодильна RT-98B-1, black (220 В) | 87 | score 87; brand match; jacc 0.71; SP article is internal-id (not SKU) |
| 3708 | 5539 / `` / `` / FROSTY | Шафа холодильна Frosty RT-98B-3 Black | 6450 / kodaki / `000009078` / FROSTY | Шафа холодильна RT-98B-3, black (220 В) | 87 | score 87; brand match; jacc 0.71; SP article is internal-id (not SKU) |
| 3618 | 2087 / `` / `` / FROSTY | Вітрина холодильна FROSTY RTW 130L-2 | 5981 / kodaki / `000004968` / FROSTY | Вітрина холодильна RTW 130L-2 (220 В) | 86 | score 86; brand match; jacc 0.67; SP article is internal-id (not SKU) |
| 3712 | 2228 / `` / `` / FROSTY | Вітрина холодильна Frosty RTW-202C-4 | 5776 / kodaki / `000009086` / FROSTY | Вітрина холодильна RTW-202C-4 (220 В) | 86 | score 86; brand match; jacc 0.67; SP article is internal-id (not SKU) |
| 3713 | 2227 / `` / `` / FROSTY | Вітрина холодильна Frosty RTW-202C-5 | 5861 / kodaki / `000009087` / FROSTY | Вітрина холодильна RTW-202C-5 (220 В) | 86 | score 86; brand match; jacc 0.67; SP article is internal-id (not SKU) |
| 3714 | 2226 / `` / `` / FROSTY | Вітрина холодильна Frosty RTW-145C-5 | 5946 / kodaki / `000009088` / FROSTY | Вітрина холодильна RTW-145C-5 (220 В) | 86 | score 86; brand match; jacc 0.67; SP article is internal-id (not SKU) |
| 3716 | 2224 / `` / `` / FROSTY | Вітрина холодильна Frosty RTW-186C-5 | 6115 / kodaki / `000009090` / FROSTY | Вітрина холодильна RTW-186C-5 (220 В) | 86 | score 86; brand match; jacc 0.67; SP article is internal-id (not SKU) |
| 3717 | 2225 / `` / `` / FROSTY | Вітрина холодильна Frosty RTW-225C-5 | 6200 / kodaki / `000009091` / FROSTY | Вітрина холодильна RTW-225C-5 (220 В) | 86 | score 86; brand match; jacc 0.67; SP article is internal-id (not SKU) |
| 3656 | 2829 / `` / `` / Imperia | Тісторозкатка з мотором HOME PASTAPRESTO cod.700 | 5568 / kodaki / `000006486` / IMPERIA | 700 Тісторозкатка PASTAPRESTO (220 В) | 86 | score 86; brand match; jacc 0.50; SP article is internal-id (not SKU) |
| 3694 | 543 / `` / `` / FROSTY | Фритюрниця електрична Frosty EFS-6L | 6362 / kodaki / `000008949` / FROSTY | Фритюрниця електрична EFS- 6L (220 В) | 86 | score 86; brand match; jacc 0.60; SP article is internal-id (not SKU) |
| 3718 | 2222 / `` / `` / FROSTY | Вітрина для морозива Frosty RTD-87C | 6285 / kodaki / `000009092` / FROSTY | Вітрина для морозива RTD-87C (220 В) | 86 | score 86; brand match; jacc 0.50; SP article is internal-id (not SKU) |
| 3610 | 2072 / `` / `` / FROSTY | Вітрина холодильна FROSTY ARC-100R | 5556 / kodaki / `000004238` / FROSTY | Вітрина холодильна ARC-100R (220 В) | 86 | score 86; brand match; jacc 0.60; SP article is internal-id (not SKU) |
| 3647 | 2062 / `` / `` / FROSTY | Вітрина холодильна Frosty ARC-400R | 6401 / kodaki / `000006066` / FROSTY | Вітрина холодильна ARC-400R (220 В) | 86 | score 86; brand match; jacc 0.50; SP article is internal-id (not SKU) |
| 3666 | 5520 / `` / `` / FROSTY | Шафа холодильна Frosty FL218 black | 6327 / kodaki / `000007093` / FROSTY | Шафа холодильна FL218, black (220 В) | 86 | score 86; brand match; jacc 0.60; SP article is internal-id (not SKU) |
| 3667 | 5530 / `` / `` / FROSTY | Шафа холодильна FROSTY FL218 white | 6411 / kodaki / `000007094` / FROSTY | Шафа холодильна FL218, white (220 В) | 86 | score 86; brand match; jacc 0.60; SP article is internal-id (not SKU) |
| 3715 | 2223 / `` / `` / FROSTY | Вітрина холодильна Frosty RTW-186C | 6031 / kodaki / `000009089` / FROSTY | Вітрина холодильна RTW-186C (220 В) | 86 | score 86; brand match; jacc 0.60; SP article is internal-id (not SKU) |
| 3597 | 2849 / `` / `` / Imperia | Тісторозкатка ручна HOME iPASTA TITANIA cod.190 | 5483 / kodaki / `000001895` / IMPERIA | 190 Тісторозкатка TITANIA | 86 | score 86; brand match; jacc 0.43; SP article is internal-id (not SKU) |
| 3599 | 1697 / `` / `` / Staff | Батч фризер STAFF ВТМ 10А для твердого морозива, щербетів, граніті | 5823 / kodaki / `000002316` / STAFF | Фризер для твердого морозива ВТМ10А (220 В) | 86 | score 86; brand match; jacc 0.62; SP article is internal-id (not SKU) |
| 3606 | 3273 / `` / `` / FROSTY | Овочерізка FROSTY HLC-300 з 5 дисками в комплекті | 5308 / kodaki / `000004105` / FROSTY | Овочерізка HLC-300 (220 В) | 86 | score 86; brand match; jacc 0.33; SP article is internal-id (not SKU) |
| 3608 | 4310 / `` / `` / FROSTY | Вафельниця FROSTY WS-15-2 для бельгійських вафель | 5980 / kodaki / `000004143` / FROSTY | Вафельниця WS-15 (220 В) | 86 | score 86; brand match; jacc 0.14; SP article is internal-id (not SKU) |
| 3609 | 4330 / `` / `` / FROSTY | Вафельниця FROSTY WS-15 для бельгійських вафель | 5980 / kodaki / `000004143` / FROSTY | Вафельниця WS-15 (220 В) | 86 | score 86; brand match; jacc 0.33; SP article is internal-id (not SKU) |
| 3629 | 3094 / `` / `` / FROSTY | Вінчик Frosty WIK250 | 6254 / kodaki / `000005582` / FROSTY | Вінчик WIK250 | 86 | score 86; brand match; jacc 0.67; SP article is internal-id (not SKU) |
| 3655 | 4884 / `` / `` / FROSTY | Подрібнювач харчових відходів FROSTY BS-018 з пневмовимачем | 5918 / kodaki / `000006438` / FROSTY | Подрібнювач відходів BS-018 (220 В) | 86 | score 86; brand match; jacc 0.40; SP article is internal-id (not SKU) |
| 3669 | 1176 / `` / `` / FROSTY | Піч подова FROSTY NES-12T з парозволоженням | 5663 / kodaki / `000007471` / FROSTY | Піч подова NES-12T (220 В) | 86 | score 86; brand match; jacc 0.50; SP article is internal-id (not SKU) |
| 3670 | 1175 / `` / `` / FROSTY | Піч подова FROSTY NES-24T з парозволоженням | 5748 / kodaki / `000007472` / FROSTY | Піч подова NES-24T (380 В) | 86 | score 86; brand match; jacc 0.50; SP article is internal-id (not SKU) |
| 3671 | 1177 / `` / `` / FROSTY | Піч подова FROSTY NES-36T з парозволоженням | 5833 / kodaki / `000007473` / FROSTY | Піч подова NES-36T (380 В) | 86 | score 86; brand match; jacc 0.50; SP article is internal-id (not SKU) |
| 3678 | 3862 / `` / `` / FROSTY | Блендер FROSTY 010 | 5371 / kodaki / `000008327` / FROSTY | Двигун для блендера BL-010Е | 86 | score 86; brand match; jacc 0.20; SP article is internal-id (not SKU) |
| 3686 | 5502 / `` / `` / FROSTY | Шафа холодильна Frosty FTD200GSS | 5845 / kodaki / `000008410` / FROSTY | Шафа холодильна FTD200GSS (220 В) | 86 | score 86; brand match; jacc 0.60; SP article is internal-id (not SKU) |
| 3690 | 3857 / `` / `` / FROSTY | Блендер FROSTY 010Е | 5676 / kodaki / `000008533` / FROSTY | Блендер професійний FBA-010 (220 В) | 86 | score 86; brand match; jacc 0.25; SP article is internal-id (not SKU) |
| 3692 | 3886 / `` / `` / FROSTY | Блендер Frosty FBA-010 | 5676 / kodaki / `000008533` / FROSTY | Блендер професійний FBA-010 (220 В) | 86 | score 86; brand match; jacc 0.50; SP article is internal-id (not SKU) |
| 3696 | 4346 / `` / `` / FROSTY | Вафельниця Frosty WBS-2B для бельгійських вафель | 6281 / kodaki / `000008969` / FROSTY | Вафельниця WBS- 2B (220 В) | 86 | score 86; brand match; jacc 0.43; SP article is internal-id (not SKU) |
| 3697 | 4347 / `` / `` / FROSTY | Вафельниця Frosty WBS-22B для бельгійських вафель | 6364 / kodaki / `000008970` / FROSTY | Вафельниця WBS-22B (220 В) | 86 | score 86; brand match; jacc 0.43; SP article is internal-id (not SKU) |
| 3699 | 3442 / `` / `` / FROSTY | Фаршеміс Frosty FDH-15N | 5605 / kodaki / `000009054` / FROSTY | Фаршезмішувач-тістоміс FDH-15N (220 В) | 86 | score 86; brand match; jacc 0.60; SP article is internal-id (not SKU) |
| 3627 | 34 / `` / `` / FROSTY | Плита індукційна FROSTY G35-KP2 настільна | 6152 / kodaki / `000005484` / FROSTY | Плита індукційна G35-KP2 (220 В) | 85 | score 85; brand match; jacc 0.57; SP article is internal-id (not SKU) |
| 3688 | 5288 / `` / `` / FROSTY | Шафа морозильна Frosty FBD600SS | 6015 / kodaki / `000008421` / FROSTY | Шафа морозильна FBD600SS (220 В) | 85 | score 85; brand match; jacc 0.60; SP article is internal-id (not SKU) |
| 3638 | 3988 / `` / `` / FROSTY | Гриль контактний Frosty SP-1A2 | 5642 / kodaki / `000005928` / FROSTY | Гриль контактний SP-1A2 (220 В) | 85 | score 85; brand match; jacc 0.67; SP article is internal-id (not SKU) |
| 3639 | 3992 / `` / `` / FROSTY | Гриль контактний Frosty SP-2A1 | 5642 / kodaki / `000005928` / FROSTY | Гриль контактний SP-1A2 (220 В) | 85 | score 85; brand match; jacc 0.67; SP article is internal-id (not SKU) |
| 3641 | 3991 / `` / `` / FROSTY | Гриль контактний Frosty SP-1C2 | 5812 / kodaki / `000005930` / FROSTY | Гриль контактний SP-1C2 (220 В) | 85 | score 85; brand match; jacc 0.67; SP article is internal-id (not SKU) |
| 3649 | 2729 / `` / `` / FROSTY | Спіральний тістоміс Frosty HS 20 двошвидкісний | 5828 / kodaki / `000006164` / FROSTY | Тістоміс спіральний HS 20 (220 В) | 85 | score 85; brand match; jacc 0.40; SP article is internal-id (not SKU) |
| 3650 | 2731 / `` / `` / FROSTY | Спіральний тістоміс Frosty HS 40 двошвидкісний | 5913 / kodaki / `000006165` / FROSTY | Тістоміс спіральний HS 40 (220 В) | 85 | score 85; brand match; jacc 0.40; SP article is internal-id (not SKU) |
| 3657 | 2730 / `` / `` / FROSTY | Спіральний тістоміс Frosty HS 30 двошвидкісний | 6335 / kodaki / `000006599` / FROSTY | Тістоміс спіральний HS 30 (220 В) | 85 | score 85; brand match; jacc 0.40; SP article is internal-id (not SKU) |
| 3676 | 3994 / `` / `` / FROSTY | Гриль контактний Frosty SP-2A3 | 6172 / kodaki / `000007805` / FROSTY | Гриль контактний SP-2A3 (220 В) | 85 | score 85; brand match; jacc 0.67; SP article is internal-id (not SKU) |
| 3617 | 4462 / `` / `` / FROSTY | Тостер конвеєрний FROSTY CVT-03 | 5564 / kodaki / `000004821` / FROSTY | Тостер конвеєрний CVT-03 (220 В) | 84 | score 84; brand match; jacc 0.50; SP article is internal-id (not SKU) |
| 3591 | 3123 / `` / `` / FROSTY | Міксер планетарний FROSTY B-10 | 5221 / kodaki / `000001630` / FROSTY | Міксер планетарний B-10 (220 В) | 84 | score 84; brand match; jacc 0.50; SP article is internal-id (not SKU) |
| 3592 | 3133 / `` / `` / FROSTY | Міксер планетарний Frosty B10-B | 5221 / kodaki / `000001630` / FROSTY | Міксер планетарний B-10 (220 В) | 84 | score 84; brand match; jacc 0.50; SP article is internal-id (not SKU) |
| 3593 | 3124 / `` / `` / FROSTY | Міксер планетарний FROSTY B-20 | 5306 / kodaki / `000001632` / FROSTY | Міксер планетарний B-20 (220 В) | 84 | score 84; brand match; jacc 0.50; SP article is internal-id (not SKU) |
| 3594 | 3150 / `` / `` / FROSTY | Міксер планетарний FROSTY B20-B | 5306 / kodaki / `000001632` / FROSTY | Міксер планетарний B-20 (220 В) | 84 | score 84; brand match; jacc 0.50; SP article is internal-id (not SKU) |
| 3595 | 3125 / `` / `` / FROSTY | Міксер планетарний FROSTY B-40 | 5391 / kodaki / `000001635` / FROSTY | Міксер планетарний B-40 (220 В) | 84 | score 84; brand match; jacc 0.50; SP article is internal-id (not SKU) |
| 3596 | 3164 / `` / `` / FROSTY | Міксер планетарний Frosty B40-B | 5391 / kodaki / `000001635` / FROSTY | Міксер планетарний B-40 (220 В) | 84 | score 84; brand match; jacc 0.50; SP article is internal-id (not SKU) |
| 3630 | 3990 / `` / `` / FROSTY | Гриль контактний Frosty SP-1C1 | 6235 / kodaki / `000005587` / FROSTY | Гриль контактний SP-1C1 (220 В) | 84 | score 84; brand match; jacc 0.60; SP article is internal-id (not SKU) |
| 3632 | 1376 / `` / `` / FROSTY | Стіл холодильний FROSTY PS300 саладета | 5494 / kodaki / `000005757` / FROSTY | Стіл холодильний PS300 (220 В) | 84 | score 84; brand match; jacc 0.40; SP article is internal-id (not SKU) |
| 3640 | 3987 / `` / `` / FROSTY | Гриль контактний Frosty SP-1A1 | 5727 / kodaki / `000005929` / FROSTY | Гриль контактний SP-1A1 (220 В) | 84 | score 84; brand match; jacc 0.60; SP article is internal-id (not SKU) |
| 3644 | 3993 / `` / `` / FROSTY | Гриль контактний Frosty SP-2A2 | 5982 / kodaki / `000005932` / FROSTY | Гриль контактний SP-2A2 (220 В) | 84 | score 84; brand match; jacc 0.60; SP article is internal-id (not SKU) |
| 3660 | 1518 / `` / `` / FROSTY | Льодогенератор Frosty HZB-18F | 6487 / kodaki / `000006758` / FROSTY | Льодогенератор HZB-18F (220 В) | 84 | score 84; brand match; jacc 0.75; SP article is internal-id (not SKU) |
| 3679 | 1023 / `` / `` / FROSTY | Піч конвекційна Frosty ESD-1A | 5420 / kodaki / `000008357` / FROSTY | Піч конвекційна ESD-1A (220 В) | 84 | score 84; brand match; jacc 0.60; SP article is internal-id (not SKU) |
| 3680 | 1022 / `` / `` / FROSTY | Піч конвекційна Frosty ESD-4A | 5505 / kodaki / `000008358` / FROSTY | Піч конвекційна ESD-4A (220 В) | 84 | score 84; brand match; jacc 0.60; SP article is internal-id (not SKU) |
| 3681 | 1187 / `` / `` / FROSTY | Піч конвекційна Frosty ESD-8A | 5589 / kodaki / `000008359` / FROSTY | Піч конвекційна ESD-8A (220 В) | 84 | score 84; brand match; jacc 0.60; SP article is internal-id (not SKU) |
| 3631 | 1374 / `` / `` / FROSTY | Стіл холодильний FROSTY S900 саладета | 6506 / kodaki / `000005753` / FROSTY | Стіл холодильний S900 (220 В) | 84 | score 84; brand match; jacc 0.40; SP article is internal-id (not SKU) |
| 3637 | 4092 / `` / `` / FROSTY | Вітрина теплова FROSTY BV-808 | 6317 / kodaki / `000005907` / FROSTY | Вітрина теплова BV-808 (220 В) | 84 | score 84; brand match; jacc 0.50; SP article is internal-id (not SKU) |
| 3588 | 2864 / `` / `` / Fimar | Тісторозкатка Fimar SI320 (220 В) | 5366 / kodaki / `000001523` / FIMAR | Тісторозкатка SI 320 (220 В) | 83 | score 83; brand match; jacc 0.67; SP article is internal-id (not SKU) |
| 3589 | 2913 / `` / `` / Fimar | Тісторозкатка Fimar SI420 (220 В) | 5451 / kodaki / `000001524` / FIMAR | Тісторозкатка SI 420 (220 В) | 83 | score 83; brand match; jacc 0.67; SP article is internal-id (not SKU) |
| 3607 | 1188 / `` / `` / FROSTY | Піч конвекційна Frosty EN-50 | 5394 / kodaki / `000004139` / FROSTY | Піч конвекційна EN-50 (220 В) | 83 | score 83; brand match; jacc 0.50; SP article is internal-id (not SKU) |
| 3590 | 3775 / `` / `` / FROSTY | Міксер молочний FROSTY DM-B | 5724 / kodaki / `000001548` / FROSTY | Міксер молочний DM-B (220 В) | 83 | score 83; brand match; jacc 0.50; SP article is internal-id (not SKU) |
| 3634 | 1370 / `` / `` / FROSTY | Стіл для піци FROSTY PS903 холодильний | 5829 / kodaki / `000005766` / FROSTY | Стіл для піци PS903 (220 В) | 83 | score 83; brand match; jacc 0.33; SP article is internal-id (not SKU) |
| 3700 | 2887 / `` / `` / FROSTY | Тісторозкатка Frosty FDM220M | 5690 / kodaki / `000009055` / FROSTY | Тісторозкатка локшинорізка FDM220M (220 В) | 82 | score 82; brand match; jacc 0.50; SP article is internal-id (not SKU) |
| 3633 | 2103 / `` / `` / FROSTY | Вітрина для топингу Frosty VRX1800/330 | 5660 / kodaki / `000005764` / FROSTY | Вітрина для топінгу VRX1800/330 (220 В) | 79 | score 79; brand match; jacc 0.50; SP article is internal-id (not SKU) |
| 3698 | 2780 / `` / `` / FROSTY | Тістоміс Frosty FSV-60L | 5687 / kodaki / `000009012` / FROSTY | Тістоміс спіральний FSV-60L (220 В) | 79 | score 79; brand match; jacc 0.60; SP article is internal-id (not SKU) |
| 3677 | 1727 / `` / `` / Staff | Машина мультифункціональна STAFF R 151 A Med | 5753 / kodaki / `000008011` / STAFF | Машина мультифункційна R 151 A Med (380 В) | 78 | score 78; brand match; jacc 0.67; SP article is internal-id (not SKU) |
| 3600 | 2997 / `` / `` / Fimar | М'ясорубка Fimar TR22/TE 1ph | 5467 / kodaki / `000003207` / FIMAR | М'ясорубка TR22/TE 1ph (220 В) | 77 | score 77; brand match; jacc 0.83; SP article is internal-id (not SKU) |
| 3601 | 2979 / `` / `` / Fimar | М'ясорубка Fimar 22TE (220) | 5467 / kodaki / `000003207` / FIMAR | М'ясорубка TR22/TE 1ph (220 В) | 77 | score 77; brand match; jacc 0.33; SP article is internal-id (not SKU) |
| 3602 | 2975 / `` / `` / Fimar | М'ясорубка Fimar 22TE (380) | 5551 / kodaki / `000003208` / FIMAR | М'ясорубка TR22/TE 3ph (380 В) | 77 | score 77; brand match; jacc 0.33; SP article is internal-id (not SKU) |
| 3668 | 1726 / `` / `` / Staff | Машина мультифункціональна STAFF R 51A | 5993 / kodaki / `000007286` / STAFF | Машина мультифункційна R  51A (220 В) | 74 | score 74; brand match; jacc 0.60; SP article is internal-id (not SKU) |
| 3687 | 5061 / `` / `` / FROSTY | Шафа холодильна Frosty FTD400 | 5845 / kodaki / `000008410` / FROSTY | Шафа холодильна FTD200GSS (220 В) | 74 | score 74; brand match; jacc 0.20; SP article is internal-id (not SKU) |
| 3689 | 5269 / `` / `` / FROSTY | Шафа морозильна Frosty FBD400 | 6015 / kodaki / `000008421` / FROSTY | Шафа морозильна FBD600SS (220 В) | 74 | score 74; brand match; jacc 0.20; SP article is internal-id (not SKU) |
| 3663 | 3933 / `` / `271599` / FROSTY | Подрібнювач льоду Frosty IC80A | 6316 / kodaki / `000006955` / FROSTY | Льодоподрібнювач IC80A (220 В) | 74 | score 74; brand match; jacc 0.75; SP article is internal-id (not SKU) |
| 3584 | 3920 / `` / `` / Ceado | Подрібнювач льоду CEADO V90 | 6143 / kodaki / `000001388` / CEADO | Льодоподрібнювач V90 (220 В) | 73 | score 73; brand match; jacc 0.67; SP article is internal-id (not SKU) |
| 3614 | 4119 / `` / `` / FROSTY | Електросупниця 10 л FROSTY SB-6000S (супник) | 5884 / kodaki / `000004522` / FROSTY | Супник електричний SB-6000S (220 В) | 69 | score 69; brand match; jacc 0.60; SP article is internal-id (not SKU) |
| 3636 | 920 / `` / `` / FROSTY | Апарат SOUS VIDE FROSTY SV250 | 5408 / kodaki / `000005871` / FROSTY | Прилад SOUS VIDE SV250 (220 В) | 68 | score 68; brand match; jacc 0.40; SP article is internal-id (not SKU) |

### rp-ukrayina (50)

| match_id | PP (id / article / display_article / brand) | PP name | SP (id / supplier / article / brand) | SP name | score | reason |
|---:|---|---|---|---|---:|---|
| 3734 | 3010 / `` / `212270Z43` / Sirman | М'ясорубка SIRMAN TC-22 Nevada Total Unger (380) | 6888 / rp-ukrayina / `` / Sirman | М'ясорубка SIRMAN TC-22 Е | 100 | score 100; brand match; jacc 0.40; no SP article |
| 3740 | 1181 / `` / `` / Unox | Піч конвекційна Unox XB693MP універсальна на 6 рівнів | 6967 / rp-ukrayina / `` / Unox | Піч пароконвекційна UNOX XB693-MP | 100 | score 100; brand match; jacc 0.43; no SP article |
| 3741 | 1182 / `` / `` / Unox | Піч конвекційна Unox XB893MP універсальна | 6969 / rp-ukrayina / `` / Unox | Піч пароконвекційна UNOX XB893-MP | 100 | score 100; brand match; jacc 0.75; no SP article |
| 3742 | 1097 / `` / `` / Unox | Пароконвектомат UNOX XEVC0311E1RM лінія ONE на 3 рівні | 6942 / rp-ukrayina / `` / Unox | Пароконвектомат UNOX XEVC-0311-E1RM | 100 | score 100; brand match; jacc 0.50; no SP article |
| 3744 | 1194 / `` / `` / Unox | Піч пароконвекційна Unox XEFR03HSELDV Stefania | 6960 / rp-ukrayina / `` / Unox | Піч пароконвекційна UNOX XEFR-03HS-ELDV | 100 | score 100; brand match; jacc 0.75; no SP article |
| 3745 | 1049 / `` / `` / Unox | Піч конвекційна Unox XF003 Roberta | 6978 / rp-ukrayina / `` / Unox | Піч пароконвекційна UNOX XF003 | 100 | score 100; brand match; jacc 0.67; no SP article |
| 3746 | 1242 / `` / `` / Unox | Піч пароконвекційна UNOX XFT183 | 6985 / rp-ukrayina / `` / Unox | Піч пароконвекційна UNOX XFT183 новинка | 100 | score 100; brand match; jacc 0.67; no SP article |
| 3747 | 1045 / `` / `` / Unox | Піч конвекційна Unox XF013 | 6979 / rp-ukrayina / `` / Unox | Піч пароконвекційна UNOX XF013 новинка | 100 | score 100; brand match; jacc 0.67; no SP article |
| 3749 | 1096 / `` / `` / Unox | Пароконвектомат UNOX XECC0523E1RM лінія ONE на 5 рівнів | 6941 / rp-ukrayina / `` / Unox | Пароконвектомат UNOX XECC-0523-E1RM | 100 | score 100; brand match; jacc 0.50; no SP article |
| 3750 | 1041 / `` / `` / Unox | Пароконвектомат UNOX XEVC1011E1RM лінія ONE | 6951 / rp-ukrayina / `` / Unox | Пароконвектомат UNOX XEVC-1011-E1RM | 100 | score 100; brand match; jacc 0.71; no SP article |
| 3751 | 1102 / `` / `` / Unox | Пароконвектомат Unox XEBC10EUE1RM лінія ONE | 6975 / rp-ukrayina / `` / Unox | Піч пароконвекційна UNOX XEBC-10EU-E1RM | 100 | score 100; brand match; jacc 0.71; no SP article; product-type word clash |
| 3752 | 1197 / `` / `` / Unox | Піч пароконвекційна Unox XEFR06EUELRVDR VITTORIA | 6964 / rp-ukrayina / `` / Unox | Піч пароконвекційна UNOX XEFR-06EU-ELRV-DR | 100 | score 100; brand match; jacc 0.75; no SP article |
| 3753 | 1036 / `` / `` / Unox | Піч конвекційна Unox XF043 | 6982 / rp-ukrayina / `` / Unox | Піч пароконвекційна UNOX XF043 | 100 | score 100; brand match; jacc 1.00; no SP article |
| 3755 | 1047 / `` / `` / Unox | Піч конвекційна Unox XB 893 на 10 рівнів | 6968 / rp-ukrayina / `` / Unox | Піч пароконвекційна UNOX XB893 | 100 | score 100; brand match; jacc 0.40; no SP article |
| 3756 | 1046 / `` / `` / Unox | Піч конвекційна Unox XB693 на 6 рівнів | 6966 / rp-ukrayina / `` / Unox | Піч пароконвекційна UNOX XB693 | 100 | score 100; brand match; jacc 0.40; no SP article |
| 3757 | 1033 / `` / `` / Unox | Піч конвекційна Unox XF023 | 6980 / rp-ukrayina / `` / Unox | Піч пароконвекційна UNOX XF023 | 100 | score 100; brand match; jacc 1.00; no SP article |
| 3758 | 1195 / `` / `` / Unox | Пароконвекційна піч Unox XEFR04HSELDV Arianna | 6963 / rp-ukrayina / `` / Unox | Піч пароконвекційна UNOX XEFR-04HS-ELDV | 100 | score 100; brand match; jacc 0.75; no SP article |
| 3759 | 1043 / `` / `` / Unox | Піч конвекційна Unox XFT133 з парозволоженням | 6984 / rp-ukrayina / `` / Unox | Піч пароконвекційна UNOX XFT133 | 100 | score 100; brand match; jacc 0.67; no SP article |
| 3761 | 5005 / `` / `` / Unox | Шафа розстійна Unox XEBPC12EUB, на 12 листів 600х400 | 6992 / rp-ukrayina / `` / Unox | Шафа розстійна UNOX XEBPC-12EU-B | 100 | score 100; brand match; jacc 0.50; no SP article |
| 3762 | 313 / `` / `` / Unox | Розстоєчна шафа Unox XEKPT08EUC, на 8 дек 600х400 | 6994 / rp-ukrayina / `` / Unox | Шафа розстійна UNOX XEKPT-08EU-C | 100 | score 100; brand match; jacc 0.43; no SP article; product-type word clash |
| 3763 | 5004 / `` / `` / Unox | Шафа розстійна Unox XEKPT08HSC, 8 дек 460х330 | 6995 / rp-ukrayina / `` / Unox | Шафа розстійна UNOX XEKPT-08HS-C | 100 | score 100; brand match; jacc 0.43; no SP article |
| 3764 | 5002 / `` / `` / Unox | Шафа розстійна Unox XEKPT10EUC, на 10 дек 600х400 | 6996 / rp-ukrayina / `` / Unox | Шафа розстійна UNOX XEKPT-10EU-C | 100 | score 100; brand match; jacc 0.50; no SP article |
| 3765 | 309 / `` / `` / Unox | Розстоєчна шафа Unox XL 413, на 12 дек 600х400 | 6997 / rp-ukrayina / `` / Unox | Шафа розстійна UNOX XL413 | 100 | score 100; brand match; jacc 0.33; no SP article; product-type word clash |
| 3766 | 307 / `` / `` / Unox | Розстоєчна шафа Unox XLT133, на 8 дек 460х330 | 6998 / rp-ukrayina / `` / Unox | Шафа розстійна UNOX XLT133 | 100 | score 100; brand match; jacc 0.29; no SP article; product-type word clash |
| 3767 | 308 / `` / `` / Unox | Розстоєчна шафа Unox XLT193, на 8 дек 600х400 | 6999 / rp-ukrayina / `` / Unox | Шафа розстійна UNOX XLT193 | 100 | score 100; brand match; jacc 0.33; no SP article; product-type word clash |
| 3768 | 1086 / `` / `` / Unox | Пароконвектомат Unox XEBL16EUE1RS лінія ONE | 6977 / rp-ukrayina / `` / Unox | Піч пароконвекційна UNOX XEBL-16EU-E1RS | 100 | score 100; brand match; jacc 0.71; no SP article; product-type word clash |
| 3774 | 1038 / `` / `` / Unox | Пароконвектомат UNOX XEVC0711E1RM лінія ONE | 6948 / rp-ukrayina / `` / Unox | Пароконвектомат UNOX XEVC-0711-E1RM | 100 | score 100; brand match; jacc 0.71; no SP article |
| 3775 | 1050 / `` / `` / Unox | Пароконвектомат Unox XEVC0711EPRM лінія PLUS | 6949 / rp-ukrayina / `` / Unox | Пароконвектомат UNOX XEVC-0711-EPRM | 100 | score 100; brand match; jacc 0.60; no SP article |
| 3776 | 1039 / `` / `` / Unox | Пароконвектомат Unox XEVC1011EZRM лінія ZERO | 6953 / rp-ukrayina / `` / Unox | Пароконвектомат UNOX XEVC-1011-EZRM | 100 | score 100; brand match; jacc 0.60; no SP article |
| 3777 | 1105 / `` / `` / Unox | Пароконвектомат Unox XEVC0711EZRM лінія ZERO | 6950 / rp-ukrayina / `` / Unox | Пароконвектомат UNOX XEVC-0711-EZRM | 100 | score 100; brand match; jacc 0.60; no SP article |
| 3778 | 1101 / `` / `` / Unox | Пароконвектомат Unox XEBC06EUE1RM лінія ONE | 6973 / rp-ukrayina / `` / Unox | Піч пароконвекційна UNOX XEBC-06EU-E1RM | 100 | score 100; brand match; jacc 0.71; no SP article; product-type word clash |
| 3780 | 1112 / `` / `` / Unox | Пароконвектомат UNOX XEVL2011E1RS лінія ONE | 6954 / rp-ukrayina / `` / Unox | Пароконвектомат UNOX XEVL-2011-E1RS | 100 | score 100; brand match; jacc 0.71; no SP article |
| 3781 | 1099 / `` / `` / Unox | Пароконвектомат UNOX XEVC0511EPRM лінія PLUS | 6945 / rp-ukrayina / `` / Unox | Пароконвектомат UNOX XEVC-0511-EPRM | 100 | score 100; brand match; jacc 0.60; no SP article |
| 3782 | 1114 / `` / `` / Unox | Пароконвектомат UNOX XEVC1011EPRM лінія PLUS | 6952 / rp-ukrayina / `` / Unox | Пароконвектомат UNOX XEVC-1011-EPRM | 100 | score 100; brand match; jacc 0.60; no SP article |
| 3783 | 1100 / `` / `` / Unox | Пароконвектомат UNOX XEBC04EUE1RM лінія ONE | 6971 / rp-ukrayina / `` / Unox | Піч пароконвекційна UNOX XEBC-04EU-E1RM | 100 | score 100; brand match; jacc 0.71; no SP article; product-type word clash |
| 4381 | 500 / `` / `` / Airhot | Гриль-саламанандра AIRHOT SGE-580 Salamander з жарковою поверхнею | 6672 / rp-ukrayina / `` / AIRHOT | Гриль саламандра AIRHOT SGE-580 з поверхнею для смаження | 100 | score 100; brand match; jacc 0.43; no SP article; product-type word clash |
| 3724 | 2803 / `` / `` / Gastromix | Тістоміс HS20B GASTROMIX | 6813 / rp-ukrayina / `` / GASTROMIX | Тістоміс спіральний GASTROMIX HS20B | 95 | score 95; brand match; jacc 0.00; no SP article; product-type word clash |
| 3726 | 1104 / `` / `` / Unox | Пароконвектомат Unox XEVC0511EZRM/9.3 лінія ZERO | 6946 / rp-ukrayina / `` / Unox | Пароконвектомат UNOX XEVC-0511-EZRM | 95 | score 95; brand match; jacc 0.43; no SP article |
| 3736 | 3960 / `` / `A2301` / Sirman | Гриль контактний SIRMAN CORT RR однопостовой | 6874 / rp-ukrayina / `` / Sirman | Гриль контактний SIRMAN CORT RR | 95 | score 95; brand match; jacc 0.67; no SP article |
| 3772 | 1040 / `` / `` / Unox | Пароконвектомат UNOX XEVC0511E1RM/9.3 лінія ONE | 6943 / rp-ukrayina / `` / Unox | Пароконвектомат UNOX XEVC-0511-E1RM | 95 | score 95; brand match; jacc 0.56; no SP article |
| 3725 | 2679 / `` / `` / Gastromix | Тістоміс HS40B GASTROMIX | 6813 / rp-ukrayina / `` / GASTROMIX | Тістоміс спіральний GASTROMIX HS20B | 89 | score 89; brand match; jacc 0.00; no SP article; product-type word clash |
| 3727 | 1103 / `` / `` / Unox | Пароконвектомат Unox XEVC0511EZRMLP/7 лінія ZERO | 6946 / rp-ukrayina / `` / Unox | Пароконвектомат UNOX XEVC-0511-EZRM | 88 | score 88; brand match; jacc 0.29; no SP article |
| 3773 | 1098 / `` / `` / Unox | Пароконвектомат UNOX XEVC0511E1RMLP/7 лінія ONE | 6944 / rp-ukrayina / `` / Unox | Пароконвектомат UNOX XEVC-0511-E1RM-LP | 87 | score 87; brand match; jacc 0.62; no SP article |
| 3728 | 3204 / `` / `40800502P` / Sirman | Куттер Sirman C4VV (3,3 л) | 6881 / rp-ukrayina / `` / Sirman | Куттер SIRMAN C-TRONIC 4 VV новинка | 86 | score 86; brand match; jacc 0.60; no SP article |
| 3731 | 3781 / `` / `65026502` / Sirman | Міксер молочний Sirman Sirio 2 | 6891 / rp-ukrayina / `` / Sirman | Міксер для молочних коктейлів SIRMAN SIRIO 2 | 81 | score 81; brand match; jacc 1.00; no SP article; product-type word clash |
| 3769 | 1063 / `` / `` / Unox | Деко перфороване UNOX TG 310 (460х330) | 6929 / rp-ukrayina / `` / Unox | TG310 Противень перфорований UNOX 460x330 | 74 | score 74; brand match; jacc 0.00; no SP article; product-type word clash |
| 3771 | 1066 / `` / `` / Unox | Деко перфороване UNOX TG 410 (600х400) | 6931 / rp-ukrayina / `` / Unox | TG410 Противень перфорований UNOX 600x400 | 74 | score 74; brand match; jacc 0.00; no SP article; product-type word clash |
| 3732 | 3793 / `` / `65522602` / Sirman | Міксер молочний Sirman Sirio 2 CC 900 | 6891 / rp-ukrayina / `` / Sirman | Міксер для молочних коктейлів SIRMAN SIRIO 2 | 74 | score 74; brand match; jacc 0.50; no SP article; product-type word clash |
| 3770 | 1064 / `` / `` / Unox | Деко гладке UNOX TG 405 (600х400) | 6930 / rp-ukrayina / `` / Unox | TG405 Противень гладкий UNOX 600x400 | 71 | score 71; brand match; jacc 0.00; no SP article; product-type word clash |
| 3733 | 3796 / `` / `` / Sirman | Міксер молочний Sirman Sirio 2 VV ХРОМ CC 900 | 6891 / rp-ukrayina / `` / Sirman | Міксер для молочних коктейлів SIRMAN SIRIO 2 | 68 | score 68; brand match; jacc 0.33; no SP article; product-type word clash |

### guder (36)

| match_id | PP (id / article / display_article / brand) | PP name | SP (id / supplier / article / brand) | SP name | score | reason |
|---:|---|---|---|---|---:|---|
| 3831 | 1750 / `` / `` / Gooder | Морозильна шафа Gooder UDD 370 DTK BK | 7196 / guder / `UDD370DTK` / Gooder | Шафа низькотемпературна UDD 370 DTK Gooder | 100 | score 100; brand match; jacc 0.00; anchor∈name; product-type word clash |
| 3832 | 1751 / `` / `` / Gooder | Морозильна шафа Gooder UDD 370 DTK | 7196 / guder / `UDD370DTK` / Gooder | Шафа низькотемпературна UDD 370 DTK Gooder | 100 | score 100; brand match; jacc 0.00; anchor∈name; product-type word clash |
| 3834 | 5090 / `` / `` / Gooder | Шафа холодильна Gooder USS 374 DTK | 7199 / guder / `USS374DTK` / Gooder | Шафа середньотемпературна USS 374 DTK Gooder | 100 | score 100; brand match; jacc 0.00; anchor∈name; product-type word clash |
| 3835 | 5088 / `` / `` / Gooder | Шафа холодильна Gooder USS 1200 DSC | 7200 / guder / `USS1200DSC` / Gooder | Шафа середньотемпературна USS 1200 DSC Gooder | 100 | score 100; brand match; jacc 0.00; anchor∈name; product-type word clash |
| 4382 | 4829 / `` / `125` /  | Точильний камінь #250/1000 комбінований KING K80 | 7033 / guder / `МХМКУПЕЦ125` / Gooder | ВІТРИНА ХОЛОДИЛЬНА КУПЕЦ ВХСп-1, 25 (220 В) | 100 | score 100; brand unknown; jacc 0.00; anchor∈display; SP article is internal-id (not SKU) |
| 4383 | 4828 / `` / `123` /  | Точильний камінь #1000 KING DX1000 | 7086 / guder / `123` / Gooder | ВІТРИНА ХОЛОДИЛЬНА  VSo-0,95 GK VENETO  фарбована, відкрита | 100 | score 100; brand unknown; jacc 0.00; anchor∈display; SP article is internal-id (not SKU) |
| 4403 | 2104 / `` / `` / Gooder | Вітрина холодильна XCW-100L Gooder | 7233 / guder / `XCW-100L` / Gooder | Вітрина холодильна настільна XCW-100L Goоder | 100 | score 100; brand match; jacc 0.00; anchor∈name |
| 4404 | 2628 / `` / `` / Gooder | Вітрина холодильна XCW-120LS Gooder | 7234 / guder / `XCW-120LS` / Gooder | Вітрина холодильна настільна XCW-120LS Goоder | 100 | score 100; brand match; jacc 0.00; anchor∈name |
| 4405 | 2178 / `` / `` / Gooder | Вітрина холодильна XCW-160LS Gooder | 7235 / guder / `XCW-160LS` / Gooder | Вітрина холодильна настільна XCW-160LS Goоder | 100 | score 100; brand match; jacc 0.00; anchor∈name |
| 4406 | 2176 / `` / `` / Gooder | Вітрина холодильна XCW-120 CUBE Gooder | 7236 / guder / `XCW-120CUBE` / Gooder | Вітрина холодильна настільна XCW-120 CUBE Gooder | 100 | score 100; brand match; jacc 0.00; anchor∈name |
| 4407 | 2177 / `` / `` / Gooder | Вітрина холодильна XCW-160 CUBE Gooder | 7237 / guder / `XCW-160CUBE` / Gooder | Вітрина холодильна настільна XCW-160 CUBE Goоder | 100 | score 100; brand match; jacc 0.43; anchor∈name |
| 4430 | 1756 / `` / `` / Gooder | Морозильна шафа BF400VG Gooder | 7309 / guder / `BF400VG Gooder` / Gooder | Шафа низькотемпературна BF400VG Gooder | 100 | score 100; brand match; jacc 0.00; anchor∈name; product-type word clash |
| 4433 | 2253 / `` / `` / Gooder | Вітрина холодильна XCW-200 CUBE Gooder | 7326 / guder / `XCW-200 CUBE` / Gooder | Вітрина холодильна настільна XCW-200 CUBE Gooder | 100 | score 100; brand match; jacc 0.00; anchor∈name |
| 3856 | 1331 / `` / `` / Gooder | Моноблок морозильний Gooder SGL017P | 7273 / guder / `SGL017PGooder` / Gooder | Моноблок SGL017P Gooder | 95 | score 95; brand match; jacc 0.00; product-type word clash |
| 4421 | 1332 / `` / `` / Gooder | Моноблок холодильний Gooder SGM020P | 7272 / guder / `SGM020PGooder` / Gooder | Моноблок SGM020P Gooder | 95 | score 95; brand match; jacc 0.00; product-type word clash |
| 3805 | 1449 / `` / `` / Gooder | Холодильна шафа BR400V Gooder | 7086 / guder / `123` / Gooder | ВІТРИНА ХОЛОДИЛЬНА  VSo-0,95 GK VENETO  фарбована, відкрита | 86 | score 86; brand match; jacc 0.00; SP article is internal-id (not SKU) |
| 3806 | 1450 / `` / `` / Gooder | Холодильна шафа BR400VG Gooder | 7086 / guder / `123` / Gooder | ВІТРИНА ХОЛОДИЛЬНА  VSo-0,95 GK VENETO  фарбована, відкрита | 86 | score 86; brand match; jacc 0.00; SP article is internal-id (not SKU) |
| 4414 | 1630 / `` / `` / Gooder | Стіл холодильний Gooder GN2100TN | 7248 / guder / `GN2100TNGooder` / Gooder | Стіл холодильний середньотемпературний GN2100TN Gooder | 86 | score 86; brand match; jacc 0.00; product-type word clash |
| 4415 | 1798 / `` / `` / Gooder | Стіл морозильний Gooder GN2100ВТ | 7249 / guder / `GN2100ВТGooder` / Gooder | Стіл холодильний низькотемпературний GN2100ВТ Gooder | 86 | score 86; brand match; jacc 0.00; product-type word clash |
| 4416 | 1799 / `` / `` / Gooder | Стіл морозильний Gooder GN3100ВТ | 7250 / guder / `GN3100ВТGooder` / Gooder | Стіл холодильний низькотемпературний GN3100ВТ Gooder | 86 | score 86; brand match; jacc 0.00; product-type word clash |
| 4417 | 1815 / `` / `` / Gooder | Стіл морозильний Gooder GN4100ВТ | 7251 / guder / `GN4100ВТGooder` / Gooder | Стіл холодильний низькотемпературний GN4100ВТ Gooder | 86 | score 86; brand match; jacc 0.00; product-type word clash |
| 4400 | 2146 / `` / `` / Gooder | Вітрина холодильна Gooder VRX2000/330 | 7217 / guder / `VRX2000/330 Gooder` / Gooder | Вітрина саладетта VRX2000/330 Gooder | 80 | score 80; brand match; jacc 0.00; product-type word clash |
| 4401 | 2145 / `` / `` / Gooder | Вітрина холодильна Gooder VRX1500/380 | 7218 / guder / `VRX1500/380 Gooder` / Gooder | Вітрина саладетта VRX1500/380 Gooder | 80 | score 80; brand match; jacc 0.00; product-type word clash |
| 4402 | 2144 / `` / `` / Gooder | Вітрина холодильна Gooder VRX1400/330 | 7219 / guder / `VRX1400/330 Gooder` / Gooder | Вітрина саладетта VRX1400/330 Gooder | 80 | score 80; brand match; jacc 0.00; product-type word clash |
| 3833 | 5089 / `` / `` / Gooder | Шафа холодильна Gooder USS 374 DTK BK | 7198 / guder / `USS374DTKBK` / Gooder | Шафа середньотемпературна USS 374 DTK BK Gooder | 78 | score 78; brand match; jacc 0.00; anchor∈name; product-type word clash |
| 4391 | 1444 / `` / `` / Gooder | Холодильна шафа Gooder GN-1410TN | 7201 / guder / `GN-1410TN Gooder` / Gooder | Шафа середньотемпературна GN-1410TN Gooder | 76 | score 76; brand match; jacc 0.00; product-type word clash |
| 4392 | 1743 / `` / `` / Gooder | Морозильна шафа Gooder GN-650BT | 7202 / guder / `GN-650BT Gooder` / Gooder | Шафа низькотемпературна GN-650BT Gooder | 75 | score 75; brand match; jacc 0.00; product-type word clash |
| 4393 | 5460 / `` / `` / Gooder | Шафа холодильна Gooder ВВT350S | 7204 / guder / `ВВT350S Gooder` / Gooder | Шафа середньотемпературна ВВT350S Gooder | 75 | score 75; brand match; jacc 0.00; product-type word clash |
| 4394 | 5459 / `` / `` / Gooder | Шафа холодильна Gooder ВВT350H | 7205 / guder / `ВВT350H Gooder` / Gooder | Шафа середньотемпературна ВВT350H Gooder | 75 | score 75; brand match; jacc 0.00; product-type word clash |
| 4395 | 5458 / `` / `` / Gooder | Шафа холодильна Gooder BBD230S | 7206 / guder / `BBD230S Gooder` / Gooder | Шафа середньотемпературна BBD230S Gooder | 75 | score 75; brand match; jacc 0.00; one-sided SKU diff ['bbd', 's']; product-type word clash |
| 4396 | 5457 / `` / `` / Gooder | Шафа холодильна Gooder BBD230H | 7207 / guder / `BBD230H Gooder` / Gooder | Шафа середньотемпературна BBD230H Gooder | 75 | score 75; brand match; jacc 0.00; one-sided SKU diff ['bbd', 'h']; product-type word clash |
| 4425 | 1443 / `` / `` / Gooder | Холодильна шафа Gooder GN-650TN | 7279 / guder / `GN-650TNGooder` / Gooder | Шафа середньотемпературна GN-650TN Gooder | 75 | score 75; brand match; jacc 0.00; product-type word clash |
| 4408 | 2186 / `` / `` / Gooder | Вітрина кондитерська Gooder XC-58L | 7238 / guder / `XC-58LGooder` / Gooder | Вітрина настільна холодильна XC-58L Gooder | 73 | score 73; brand match; jacc 0.00; product-type word clash |
| 4409 | 2187 / `` / `` / Gooder | Вітрина кондитерська Gooder XC-68L | 7239 / guder / `XC-68LGooder` / Gooder | Вітрина настільна холодильна XC-68L Gooder | 73 | score 73; brand match; jacc 0.00; product-type word clash |
| 4410 | 2188 / `` / `` / Gooder | Вітрина кондитерська Gooder XC-78L | 7240 / guder / `XC-78LGooder` / Gooder | Вітрина настільна холодильна XC-78L Gooder | 73 | score 73; brand match; jacc 0.00; product-type word clash |
| 4411 | 2189 / `` / `` / Gooder | Вітрина кондитерська Gooder XC-98L | 7241 / guder / `XC-98LGooder` / Gooder | Вітрина настільна холодильна XC-98L Gooder | 73 | score 73; brand match; jacc 0.00; product-type word clash |

### astim (10)

| match_id | PP (id / article / display_article / brand) | PP name | SP (id / supplier / article / brand) | SP name | score | reason |
|---:|---|---|---|---|---:|---|
| 4436 | 4820 / `` / `103` /  | Ніж ЯНАГИБА 24 см SEKIRYU SR-240S | 12850 / astim / `103` /  | Шестерня ковбасного шприца 282571, 282588, 282090, 282595, 282601, 282618 | 100 | score 100; brand unknown; jacc 0.00; anchor∈display; SP article is internal-id (not SKU) |
| 4437 | 4811 / `` / `470190` / Hendi | Контейнер для тіста 14 л Hendi 880906, 600x400х(H)70 мм | 9211 / astim / `470190` /  | Контейнер для їжі GN 1/1 – 2 шт. - Код 470190 | 100 | score 100; brand unknown; jacc 0.00; anchor∈display; SP article is internal-id (not SKU) |
| 4444 | 3708 / `` / `695906` / Hendi | Соковижималка (прес) для цитрусових Hendi | 12007 / astim / `695906` /  | Соковитискач для цитрусових, 225x180x510(H) мм | 100 | score 100; brand unknown; jacc 0.00; anchor∈display; SP article is internal-id (not SKU) |
| 4445 | 935 / `` / `Z CZE1996951` / Hendi | Тирса (тріска) для копчення Hendi (250 гр) | 12550 / astim / `Z CZE1996951` /  | Тріска для копчення - дуб, 150 г | 100 | score 100; brand unknown; jacc 0.00; anchor∈display |
| 4438 | 1938 / `` / `617908` / Hendi | Форма для піци Hendi 617908 з алюмінієвим покриттям ø240x(H)25 мм | 8376 / astim / `525197` / HENDI | Дерев'яна лопатка для млинців, HENDI | 86 | score 86; brand match; jacc 0.00; SP article is internal-id (not SKU); product-type word clash |
| 4439 | 1939 / `` / `617953` / Hendi | Форма для піци Hendi 617953 з алюмінієвим покриттям ø360x(H)25 мм | 8376 / astim / `525197` / HENDI | Дерев'яна лопатка для млинців, HENDI | 86 | score 86; brand match; jacc 0.00; SP article is internal-id (not SKU); product-type word clash |
| 4440 | 1940 / `` / `617984` / Hendi | Форма для піци Hendi 617984 з алюмінієвим покриттям ø500x(H)38 мм | 8376 / astim / `525197` / HENDI | Дерев'яна лопатка для млинців, HENDI | 86 | score 86; brand match; jacc 0.00; SP article is internal-id (not SKU); product-type word clash |
| 4441 | 4705 / `` / `975862` / Hendi | Сифон для вершків Hendi 975862 Kurt Scheller Edition блакитний | 7700 / astim / `596883` / HENDI | Відкривачка для пляшок настінна, HENDI | 86 | score 86; brand match; jacc 0.00; SP article is internal-id (not SKU); product-type word clash |
| 4442 | 4706 / `` / `975855` / Hendi | Сифон для вершків Hendi 975855 Kurt Scheller Edition жовтий | 7700 / astim / `596883` / HENDI | Відкривачка для пляшок настінна, HENDI | 86 | score 86; brand match; jacc 0.00; SP article is internal-id (not SKU); product-type word clash |
| 4443 | 4707 / `` / `975879` / Hendi | Сифон для вершків Hendi 975879 Kurt Scheller Edition зелений | 7700 / astim / `596883` / HENDI | Відкривачка для пляшок настінна, HENDI | 86 | score 86; brand match; jacc 0.00; SP article is internal-id (not SKU); product-type word clash |

## recommend-REJECT (3)

### novyy-proekt (НП) (2)

| match_id | PP (id / article / display_article / brand) | PP name | SP (id / supplier / article / brand) | SP name | score | reason |
|---:|---|---|---|---|---:|---|
| 3355 | 3591 / `` / `` / Robot Coupe | Комплект дисків для картопляного пюре Robot Coupe 28189 | 4792 / novyy-proekt (НП) / `28189` / Robot Coupe | Насадка для приготування картопляного пюре 2 мм Robot Coupe (28189) | 79 | suffix-variant near-miss, differing SKU tokens ['28189'] |
| 3356 | 3605 / `` / `` / Robot Coupe | Комплект дисків для картопляного пюре Robot Coupe 28208 | 4711 / novyy-proekt (НП) / `28208` / Robot Coupe | Насадка для приготування картопляного пюре 3 мм Robot Coupe (28208) | 79 | suffix-variant near-miss, differing SKU tokens ['28208'] |

### guder (1)

| match_id | PP (id / article / display_article / brand) | PP name | SP (id / supplier / article / brand) | SP name | score | reason |
|---:|---|---|---|---|---:|---|
| 4431 | 1755 / `` / `` / Gooder | Морозильна шафа BF400V Gooder | 7309 / guder / `BF400VG Gooder` / Gooder | Шафа низькотемпературна BF400VG Gooder | 70 | manufacturer SKU 'BF400VG Gooder' absent from PP name+display, weak token overlap (full jacc 0.43) |

## one-to-one cross-check (CLAUDE.md invariant #15 / 1 pp ↔ 1 supplier)

**Re-run any time:** `./.venv/Scripts/python.exe scripts/triage_one_to_one_check.py` (read-only).

The buckets above score each candidate on the PromProduct↔SupplierProduct **text axis only** (article / name / brand / score). They do **not** check whether the PromProduct *already holds* a confirmed/manual match. A PP may hold at most **one** supplier (invariant #15 / `feedback_labresta_one_to_one`), so a text-perfect candidate on an already-matched PP is a **conflict, not safe-to-confirm** — confirming it would create a forbidden M:1.

Cross-check result (DB read-only, status snapshot identical before/after → zero mutation):

- candidates on an already-matched PP: **97 / 301** (across all three buckets)
- within **recommend-CONFIRM (61)**: **15** rows are one-to-one conflicts → only **46 are safe-to-confirm**
- conflict `match_id`s in CONFIRM: `3352, 3357, 3365, 3369, 3729, 3730, 3735, 3743, 3748, 3754, 3760, 3779, 3784, 3785, 4376`

| match_id | PP | already-held confirmed match (id:status) |
|---:|---:|---|
| 3352 | 3921 | 267:confirmed |
| 3357 | 4630 | 996:confirmed |
| 3365 | 3298 | 129:confirmed |
| 3369 | 3712 | 351:confirmed |
| 3729 | 3206 | 761:confirmed |
| 3730 | 2966 | 840:confirmed |
| 3735 | 4902 | 1710:confirmed |
| 3743 | 1193 | 631:confirmed |
| 3748 | 1246 | 647:confirmed |
| 3754 | 1243 | 621:confirmed |
| 3760 | 1037 | 228:confirmed |
| 3779 | 1244 | 635:confirmed |
| 3784 | 1248 | 716:confirmed |
| 3785 | 1249 | 794:confirmed |
| 4376 | 956 | 143:confirmed |

> `m3730` (PP2966 → held 840) and `m3760` (PP1037 → held 228) are the CONFIRM-bucket instances of issue **#15** (text-perfect supplier-conflict). **Decision = Yana's hand** (which supplier wins the PP): switching a PP to a new supplier means rejecting/replacing the existing confirmed match, a policy call this autonomous run does NOT make.

**Operator takeaway:** treat **46** (= 61 − 15) as the only short-list eligible for fast hand-confirm; the other **15** are supplier-conflict decisions, and the **237** NEEDS-EYEBALL rows still need a human read. Nothing here is auto-confirmed (invariant #3).
