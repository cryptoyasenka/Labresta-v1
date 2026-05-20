# chunk-055 cleanup wave2 batch 4 — SKU rows 26-33, all 16 columns

## Rules
- RU (c5/c7/c23/c25/c27/c29/c36/c38): drop Ё→Е, drop apostrophe between RU letters, replace UA lex via expanded dict.
- UA (c4/c6/c22/c24/c26/c28/c35/c37): fix зупинкі→зупинці; flag Ё.
- FLAG (not auto-fixed): UA-stem words remaining in RU after lex pass; Ё in UA.

## SKIP-НП (Hurakan, reverted)

- **r28 ART=2060698639** `Пила для розрізання мяса Hurakan HKN-SE1650M2` — SKIP-НП (бренд Hurakan ∈ список НП-эксклюзив). RU НЕ переписывается, тело из НП-фида merge позже.
- **r30 ART=2807599999** `Пила для розрізання мяса Hurakan HKN-SE1260` — SKIP-НП (Hurakan). RU НЕ переписывается.

Первый проход скрипта применил к этим строкам apos-drop + UA-lex; откачено из `.before_b4.xlsx`.

## Net changes: 0 (все UA-stems в r28/r30 = SKIP-НП territory)

Остальные SKU 25-32 (r26/r27/r29/r31/r32/r33) — без изменений (clean RU + clean UA).

## TODO для cleanup processor

Добавить SKIP-НП guard в `_w2_cleanup.py`: проверять brand c8 на наличие в SKIP_BRANDS списке → пропускать row полностью.
