# chunk-080 cleanup wave2 batch 2 — SKU rows 9-16, all 16 columns

## Rules
- RU (c5/c7/c23/c25/c27/c29/c36/c38): drop Ё→Е, drop apostrophe between RU letters, replace UA lex via expanded dict.
- UA (c4/c6/c22/c24/c26/c28/c35/c37): fix зупинкі→зупинці; flag Ё.
- FLAG (not auto-fixed): UA-stem words remaining in RU after lex pass; Ё in UA.

## r11 ART=1090611117
- c25 RU: UA-lex→RU

## r14 ART=1395554157
- c25 RU: UA-lex→RU

## r15 ART=1505341914 — SKIP-НП (brand=TATRA)
- RU не переписывается, тело из НП-фида merge позже.

