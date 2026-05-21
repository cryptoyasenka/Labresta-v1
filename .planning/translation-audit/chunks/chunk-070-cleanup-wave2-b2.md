# chunk-070 cleanup wave2 batch 2 — SKU rows 10-17, all 16 columns

## Rules
- RU (c5/c7/c23/c25/c27/c29/c36/c38): drop Ё→Е, drop apostrophe between RU letters, replace UA lex via expanded dict.
- UA (c4/c6/c22/c24/c26/c28/c35/c37): fix зупинкі→зупинці; flag Ё.
- FLAG (not auto-fixed): UA-stem words remaining in RU after lex pass; Ё in UA.

## r10 ART=639913426 — SKIP-НП (brand=APACH)
- RU не переписывается, тело из НП-фида merge позже.

## r15 ART=647442349
- c25 RU: UA-lex→RU

## r16 ART=1009188903
- c25 RU: UA-lex→RU

## r17 ART=646844871
- c25 RU: UA-lex→RU

