# chunk-055 cleanup wave2 batch 2 — SKU rows 10-17, all 16 columns

## Rules
- RU (c5/c7/c23/c25/c27/c29/c36/c38): drop Ё→Е, drop apostrophe between RU letters, replace UA lex via expanded dict.
- UA (c4/c6/c22/c24/c26/c28/c35/c37): fix зупинкі→зупинці; flag Ё.
- FLAG (not auto-fixed): UA-stem words remaining in RU after lex pass; Ё in UA.

## r10 ART=2123249689
- c36 RU: Ё→Е; UA-lex→RU

## r11 ART=2123250967
- c36 RU: Ё→Е; UA-lex→RU

## r12 ART=2123251224
- c36 RU: Ё→Е; UA-lex→RU

## r14 ART=1171174076
- c25 RU: UA-lex→RU (`промішленній→промышленной`, `профессиональній→профессиональной` — hybrid typos: RU stem + UA `і`)
- c36 RU: Ё→Е

