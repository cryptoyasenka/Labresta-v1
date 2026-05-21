# chunk-058 cleanup wave2 batch 1 — SKU rows 2-9, all 16 columns

## Rules
- RU (c5/c7/c23/c25/c27/c29/c36/c38): drop Ё→Е, drop apostrophe between RU letters, replace UA lex via expanded dict.
- UA (c4/c6/c22/c24/c26/c28/c35/c37): fix зупинкі→зупинці; flag Ё.
- FLAG (not auto-fixed): UA-stem words remaining in RU after lex pass; Ё in UA.

## r3 ART=962046952
- c25 RU: UA-lex→RU
- c36 RU: Ё→Е

## r4 ART=1147746219 — SKIP-НП (brand=HURAKAN)
- RU не переписывается, тело из НП-фида merge позже.

## r5 ART=2033694809
- c36 RU: Ё→Е

## r7 ART=472503239
- c36 RU: Ё→Е

## r8 ART=518672419
- c25 RU: UA-lex→RU

