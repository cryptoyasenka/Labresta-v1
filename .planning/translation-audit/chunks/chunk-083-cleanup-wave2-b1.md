# chunk-083 cleanup wave2 batch 1 — SKU rows 1-8, all 16 columns

## Rules
- RU (c5/c7/c23/c25/c27/c29/c36/c38): drop Ё→Е, drop apostrophe between RU letters, replace UA lex via expanded dict.
- UA (c4/c6/c22/c24/c26/c28/c35/c37): fix зупинкі→зупинці; flag Ё.
- FLAG (not auto-fixed): UA-stem words remaining in RU after lex pass; Ё in UA.

## r2 ART=2134369414 — SKIP-НП (brand=COLD)
- RU не переписывается, тело из НП-фида merge позже.

## r6 ART=655434908
- c25 RU: UA-lex→RU

