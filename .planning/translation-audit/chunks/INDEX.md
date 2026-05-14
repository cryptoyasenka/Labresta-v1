# Translation chunks — UA/RU revision workflow

- Source: `horoshop-export 13.05.26.xlsx` (5632 SKU)
- Total chunks: **85**
- Target ~150,000 chars input per chunk (≈50K tokens)
- Bounds: 30-100 SKU per chunk

## Workflow per chunk

1. Open chunk-NN.xlsx — that's the source (do not modify)
2. Revise UA + RU operator text fields per memory rules `feedback_labresta_ua_ru_translation_rules.md`
3. Write chunk-NN-fixed.xlsx (same structure, edited cells)
4. Write chunk-NN-diff.md (human-readable list of changes)
5. If any doubts → chunk-NN-questions.md (Yana batch-answers)
6. Update status below: `pending → in_progress → done`

## Chunks

| # | File | SKU | Chars | First Артикул | Last Артикул | Brands | Status |
|--:|---|--:|--:|---|---|---|---|
| 001 | `chunk-001.xlsx` | 83 | 150,203 | `624348659` | `2176570515` | Airhot, Apach, Bartscher, FROSTY… | diff-drafted, awaiting Q's (`chunk-001-questions.md`) |
| 002 | `chunk-002.xlsx` | 74 | 150,956 | `2177174504` | `2073651788` | Airhot, Apach, Bartscher, Casta… | pending |
| 003 | `chunk-003.xlsx` | 69 | 151,509 | `2073655694` | `2440518198` | ATA, Ozti, Pimak, Ефес | pending |
| 004 | `chunk-004.xlsx` | 65 | 150,758 | `2440521644` | `2444232115` | ATA | pending |
| 005 | `chunk-005.xlsx` | 84 | 150,170 | `2444251187` | `2237514863` | ATA, Airhot, Apach, EWT INOX… | pending |
| 006 | `chunk-006.xlsx` | 62 | 150,203 | `2237515493` | `2593088022` | ATA, Casta, FROSTY, GGM Gastro International… | pending |
| 007 | `chunk-007.xlsx` | 60 | 154,403 | `2593094020` | `925656640` | ARRIS, ATA, Airhot, Apach… | pending |
| 008 | `chunk-008.xlsx` | 86 | 151,507 | `925686772` | `617666959` | ARRIS, Airhot, Apach, Bartscher… | pending |
| 009 | `chunk-009.xlsx` | 75 | 152,549 | `631394855` | `2461343617` | Airhot, Apach, Beckers, EWT INOX… | pending |
| 010 | `chunk-010.xlsx` | 74 | 150,851 | `2463597440` | `2554112901` | ATA, BEKO, Bartscher, Beckers… | pending |
| 011 | `chunk-011.xlsx` | 85 | 151,680 | `2554126657` | `881360570` | Airhot, Amitek, Apach, Bartscher… | pending |
| 012 | `chunk-012.xlsx` | 61 | 151,605 | `1149589807` | `1141036471` | ATA, Airhot, Apach, Casta… | pending |
| 013 | `chunk-013.xlsx` | 61 | 152,184 | `1141037624` | `908906059` | Alto-Shaam, Bertos, FROSTY, Hendi… | pending |
| 014 | `chunk-014.xlsx` | 70 | 151,320 | `1777550136` | `527390390` | Airhot, Alto-Shaam, Apach, Bartscher… | pending |
| 015 | `chunk-015.xlsx` | 36 | 153,140 | `530482300` | `443746913` | Apach, Brillis, FROSTY, Fagor… | pending |
| 016 | `chunk-016.xlsx` | 49 | 151,162 | `477739756` | `1104894508` | Apach, FROSTY, Hendi, Tecnodom… | pending |
| 017 | `chunk-017.xlsx` | 82 | 153,391 | `1104898340` | `1486019375` | Apach, Brillis, FROSTY, Hendi… | pending |
| 018 | `chunk-018.xlsx` | 37 | 151,678 | `1486023518` | `2234280531` | Apach, Brillis, FROSTY, Fagor… | pending |
| 019 | `chunk-019.xlsx` | 58 | 150,355 | `2234283469` | `659932976` | Brillis, FROSTY, Fagor, GoodFood… | pending |
| 020 | `chunk-020.xlsx` | 37 | 154,837 | `1130507122` | `1362456118` | Angelo Po, Giorik, Hendi, Rational… | pending |
| 021 | `chunk-021.xlsx` | 49 | 153,641 | `1386188382` | `2047048010` | Apach, Brillis, FROSTY, Gemm… | pending |
| 022 | `chunk-022.xlsx` | 66 | 151,594 | `2237341591` | `641208803` | Brillis, Cooleq, FROSTY, Forcar… | pending |
| 023 | `chunk-023.xlsx` | 77 | 150,681 | `507628801` | `1197569246` | Apach, Brema, Brillis, FROSTY… | pending |
| 024 | `chunk-024.xlsx` | 74 | 152,627 | `1197576635` | `595397994` | Apach, Brema, FROSTY, Fagor… | pending |
| 025 | `chunk-025.xlsx` | 64 | 151,056 | `976768460` | `2352423600` | Brillis, Cooleq, FROSTY, Fagor… | pending |
| 026 | `chunk-026.xlsx` | 70 | 150,190 | `2448348784` | `2538804263` | Bartscher, Brillis, CAB, Cooleq… | pending |
| 027 | `chunk-027.xlsx` | 53 | 152,757 | `2538822484` | `1154533678` | Brillis, CAB, EWT INOX, Fagor… | pending |
| 028 | `chunk-028.xlsx` | 61 | 152,369 | `1154540778` | `2108377745` | Apach, Brillis, Cooleq, FROSTY… | pending |
| 029 | `chunk-029.xlsx` | 79 | 150,289 | `970938056` | `526857503` | Apach, Cuppone, EWT INOX, FROSTY… | pending |
| 030 | `chunk-030.xlsx` | 96 | 151,568 | `526929616` | `2385515101` | Apach, Cuppone, EWT INOX, FROSTY… | pending |
| 031 | `chunk-031.xlsx` | 78 | 151,690 | `2463586270` | `463335311` | Cooleq, Cuppone, FROSTY, GGF… | pending |
| 032 | `chunk-032.xlsx` | 71 | 150,419 | `477615139` | `2048277030` | Brillis, Cold, Cooleq, EWT INOX… | pending |
| 033 | `chunk-033.xlsx` | 59 | 150,317 | `2048278116` | `2211468915` | Brillis, FROSTY, Forcold, GoodFood… | pending |
| 034 | `chunk-034.xlsx` | 66 | 151,485 | `2211483282` | `2089720815` | Brillis, Cooleq, EWT INOX, FROSTY… | pending |
| 035 | `chunk-035.xlsx` | 35 | 152,575 | `2089916345` | `2125044207` | Juka, UBC Group | pending |
| 036 | `chunk-036.xlsx` | 47 | 152,173 | `2125059380` | `2166569753` | UBC Group | pending |
| 037 | `chunk-037.xlsx` | 51 | 151,149 | `2166577121` | `625659539` | Hendi, UBC Group | pending |
| 038 | `chunk-038.xlsx` | 43 | 150,283 | `625659542` | `2091320822` | Hendi, Juka | pending |
| 039 | `chunk-039.xlsx` | 37 | 154,368 | `2092063583` | `2092802740` | Juka | pending |
| 040 | `chunk-040.xlsx` | 43 | 153,770 | `2092817704` | `2116295563` | Gooder, Juka, Tefcold, UBC Group | pending |
| 041 | `chunk-041.xlsx` | 36 | 151,849 | `2116298609` | `2117880322` | Tefcold | pending |
| 042 | `chunk-042.xlsx` | 33 | 152,748 | `2117883184` | `2118850268` | Tefcold | pending |
| 043 | `chunk-043.xlsx` | 51 | 151,958 | `2118857483` | `1224709415` | FROSTY, Forcold, GoodFood, Gooder… | pending |
| 044 | `chunk-044.xlsx` | 87 | 150,356 | `2044969447` | `1148939344` | Alimacchine, Apach, Bogazici Makina, EWT INOX… | pending |
| 045 | `chunk-045.xlsx` | 80 | 152,335 | `1148942659` | `945297087` | Alimacchine, Apach, Bogazici Makina, FROSTY… | pending |
| 046 | `chunk-046.xlsx` | 88 | 150,590 | `945396510` | `1145192746` | Alimacchine, Apach, Bernardi, EWT INOX… | pending |
| 047 | `chunk-047.xlsx` | 81 | 150,297 | `2230023327` | `1148371390` | Apach, Celme, EWT INOX, Everest… | pending |
| 048 | `chunk-048.xlsx` | 71 | 152,245 | `1148431271` | `880120314` | Apach, Bogazici Makina, Celme, Dadaux… | pending |
| 049 | `chunk-049.xlsx` | 64 | 152,348 | `880212653` | `459821396` | Apach, Dynamic, EWT INOX, FROSTY… | pending |
| 050 | `chunk-050.xlsx` | 82 | 150,627 | `459821397` | `506079659` | Apach, Bear Varimixer, Bogazici Makina, Celme… | pending |
| 051 | `chunk-051.xlsx` | 59 | 150,528 | `506084714` | `1816185277` | Airhot, Dadaux, FROSTY, Fama… | pending |
| 052 | `chunk-052.xlsx` | 72 | 152,391 | `2008338380` | `947362656` | Airhot, CANCAN, Celme, Dynamic… | pending |
| 053 | `chunk-053.xlsx` | 64 | 150,093 | `947366323` | `948503667` | Airhot, Beckers, CANCAN, Celme… | pending |
| 054 | `chunk-054.xlsx` | 69 | 152,046 | `2394148200` | `2204216810` | Airhot, Apach, Bogazici Makina, Dadaux… | pending |
| 055 | `chunk-055.xlsx` | 86 | 150,300 | `2204681685` | `2134945850` | Airhot, Dadaux, FROSTY, Fama… | pending |
| 056 | `chunk-056.xlsx` | 91 | 151,657 | `2134947110` | `902235891` | Bartscher, Bezzera, FROSTY, Fimar… | pending |
| 057 | `chunk-057.xlsx` | 54 | 151,700 | `902327287` | `525346665` | Apach, Casadio, GGM Gastro International, Hendi… | pending |
| 058 | `chunk-058.xlsx` | 78 | 150,955 | `667275373` | `1104474099` | Apach, Bartscher, Bezzera, CANCAN… | pending |
| 059 | `chunk-059.xlsx` | 96 | 150,648 | `2464184031` | `635596865` | Bartscher, CAB, Ceado, EWT INOX… | pending |
| 060 | `chunk-060.xlsx` | 81 | 152,069 | `635596866` | `2309184793` | Airhot, Bartscher, Ceado, EWT INOX… | pending |
| 061 | `chunk-061.xlsx` | 67 | 150,194 | `2309189086` | `2424751163` | Airhot, Bartscher, EWT INOX, FROSTY… | pending |
| 062 | `chunk-062.xlsx` | 81 | 150,304 | `2424757446` | `2059507443` | Airhot, Bartscher, EWT INOX, FROSTY… | pending |
| 063 | `chunk-063.xlsx` | 88 | 151,720 | `2059513121` | `2567549749` | Airhot, Bartscher, EWT INOX, FROSTY… | pending |
| 064 | `chunk-064.xlsx` | 85 | 150,647 | `2567629973` | `2060623567` | AVATHERM, Airhot, Bartscher, EWT INOX… | pending |
| 065 | `chunk-065.xlsx` | 81 | 150,534 | `2121426618` | `2447469404` | Airhot, EWT INOX, FROSTY, GGM Gastro International… | pending |
| 066 | `chunk-066.xlsx` | 90 | 151,374 | `2496038149` | `2153078504` | Airhot, Atalay, Bartscher, CB… | pending |
| 067 | `chunk-067.xlsx` | 74 | 152,685 | `2045345276` | `2033010783` | Adler, Airhot, Apach, Asber… | pending |
| 068 | `chunk-068.xlsx` | 50 | 152,585 | `2045399173` | `2434126712` | ATA, Adler, Apach, Asber… | pending |
| 069 | `chunk-069.xlsx` | 61 | 151,882 | `2434135469` | `2176086023` | ATA, Apach, Elframo, Empero… | pending |
| 070 | `chunk-070.xlsx` | 59 | 151,008 | `2176091387` | `500051832` | Apach, Dadaux, FROSTY, Forpark… | pending |
| 071 | `chunk-071.xlsx` | 83 | 152,192 | `500478925` | `1173086863` | Hendi | pending |
| 072 | `chunk-072.xlsx` | 89 | 153,475 | `1173123408` | `655405499` | FROSTY, Fagor, GI.Metal, GoodFood… | pending |
| 073 | `chunk-073.xlsx` | 61 | 151,522 | `655872902` | `2289327088` | Aga, Apach, Astra, Atalay… | pending |
| 074 | `chunk-074.xlsx` | 87 | 151,468 | `2289333310` | `2044217237` | Apach, Bartscher, CANCAN, FROSTY… | pending |
| 075 | `chunk-075.xlsx` | 54 | 151,072 | `2044220842` | `1090581793` | Apach, FROSTY, Fagor, GGM Gastro International… | pending |
| 076 | `chunk-076.xlsx` | 57 | 152,276 | `2106845309` | `2239472491` | Bartscher, Brillis, Cooleq, FROSTY… | pending |
| 077 | `chunk-077.xlsx` | 39 | 150,797 | `2239477693` | `1775843181` | Brillis, FROSTY, Forcar, GoodFood… | pending |
| 078 | `chunk-078.xlsx` | 53 | 152,212 | `1836114228` | `2140758985` | Gooder, Snaige, Tatra, Tefcold | pending |
| 079 | `chunk-079.xlsx` | 58 | 155,494 | `2140760718` | `2046767826` | Angelo Po, Brillis, FROSTY, GGM Gastro International… | pending |
| 080 | `chunk-080.xlsx` | 53 | 152,160 | `2106854043` | `2127214194` | Brillis, Cooleq, FROSTY, Fagor… | pending |
| 081 | `chunk-081.xlsx` | 52 | 150,182 | `2133530800` | `2217381714` | Brillis, Everlasting, FROSTY, Fagor… | pending |
| 082 | `chunk-082.xlsx` | 52 | 151,712 | `2217382425` | `2133540222` | Bartscher, FROSTY, Fagor, Hurakan… | pending |
| 083 | `chunk-083.xlsx` | 62 | 150,841 | `2134369414` | `2139111115` | EWT INOX, FROSTY, Forcar, GoodFood… | pending |
| 084 | `chunk-084.xlsx` | 71 | 150,289 | `2139115558` | `1225375800` | FROSTY, Forcar, GI.Metal, GoodFood… | pending |
| 085 | `chunk-085.xlsx` | 75 | 131,925 | `1536892541` | `2208407729` | Airhot, Dadaux, EWT INOX, FROSTY… | pending |

## Per-chunk artifacts (filled as work progresses)

- `chunk-NN.xlsx` — source slice (read-only)
- `chunk-NN-fixed.xlsx` — revised version
- `chunk-NN-diff.md` — change list
- `chunk-NN-questions.md` — Yana's batch-question file
