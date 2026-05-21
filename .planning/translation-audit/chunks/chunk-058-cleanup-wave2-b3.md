# chunk-058 cleanup wave2 batch 3 — SKU rows 18-25, all 16 columns

## Rules
- RU (c5/c7/c23/c25/c27/c29/c36/c38): drop Ё→Е, drop apostrophe between RU letters, replace UA lex via expanded dict.
- UA (c4/c6/c22/c24/c26/c28/c35/c37): fix зупинкі→зупинці; flag Ё.
- FLAG (not auto-fixed): UA-stem words remaining in RU after lex pass; Ё in UA.

## r18 ART=876948655
- c25 RU: UA-lex→RU
- c36 RU: Ё→Е

## r19 ART=918322927
- c25 RU: UA-lex→RU

## r20 ART=921147306
- c25 RU: UA-lex→RU

## r21 ART=1020880040
- c25 RU: UA-lex→RU
- c36 RU: Ё→Е

## r22 ART=1125783148
- c25 RU: UA-lex→RU

## r24 ART=1168646756 — SKIP-НП (brand=HURAKAN)
- RU не переписывается, тело из НП-фида merge позже.

