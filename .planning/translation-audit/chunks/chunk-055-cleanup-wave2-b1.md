# chunk-055 cleanup wave2 batch 1 — SKU 1-8 (rows 2-9), all 16 columns

## Rules
- RU (c5/c7/c23/c25/c27/c29/c36/c38): drop Ё→Е, drop apostrophe between RU letters, replace UA lex via dict (ковбасний→колбасный, яловичина→говядина, хенді→хенди, привід→привод, електричний→электрический).
- UA (c4/c6/c22/c24/c26/c28/c35/c37): fix зупинкі→зупинці; flag Ё.
- FLAGs (not auto-fixed): UA-stem words remaining in RU after lex pass; Ё in UA.

## r2 ART=2204681685
- c25 RU: UA-lex→RU
- c35 UA: UA-typo-fix(зупинкі→зупинці)

## r3 ART=2204686065
- c25 RU: UA-lex→RU
- c35 UA: UA-typo-fix(зупинкі→зупинці)

## r4 ART=2204691813
- c25 RU: UA-lex→RU
- c35 UA: UA-typo-fix(зупинкі→зупинці)

## r9 ART=2123243855
- c36 RU: Ё→Е

