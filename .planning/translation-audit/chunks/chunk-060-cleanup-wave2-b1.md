# chunk-060 cleanup wave2 batch 1 — SKU rows 2-9, all 16 columns

## Rules
- RU (c5/c7/c23/c25/c27/c29/c36/c38): drop Ё→Е, drop apostrophe between RU letters, replace UA lex via expanded dict.
- UA (c4/c6/c22/c24/c26/c28/c35/c37): fix зупинкі→зупинці; flag Ё.
- FLAG (not auto-fixed): UA-stem words remaining in RU after lex pass; Ё in UA.

## r6 ART=663673968
- c25 RU: UA-lex→RU

## r7 ART=732422924 — SKIP-НП (brand=HURAKAN)
- RU не переписывается, тело из НП-фида merge позже.

## r8 ART=851150340
- c25 RU: UA-lex→RU

