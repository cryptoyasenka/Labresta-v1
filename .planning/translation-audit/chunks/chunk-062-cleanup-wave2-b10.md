# chunk-062 cleanup wave2 batch 10 — SKU rows 74-82, all 16 columns

## Rules
- RU (c5/c7/c23/c25/c27/c29/c36/c38): drop Ё→Е, drop apostrophe between RU letters, replace UA lex via expanded dict.
- UA (c4/c6/c22/c24/c26/c28/c35/c37): fix зупинкі→зупинці; flag Ё.
- FLAG (not auto-fixed): UA-stem words remaining in RU after lex pass; Ё in UA.

## r74 ART=582927430
- c25 RU: UA-lex→RU

## r75 ART=759811657
- c25 RU: UA-lex→RU

## r76 ART=1110596898
- c25 RU: UA-lex→RU

## r82 ART=2059507443 — SKIP-НП (brand=HURAKAN)
- RU не переписывается, тело из НП-фида merge позже.

