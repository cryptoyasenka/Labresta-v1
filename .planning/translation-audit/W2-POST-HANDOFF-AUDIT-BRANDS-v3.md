# W2 post-handoff audit v3 — RU + UA cyrillic brand audit (всё 8 trans cols, 31 chunks)

**Дата:** 2026-05-21
**Триггер:** Yana показала что UA остался cyrillic «хенді» после patch v1 (RU только).
**v3 fix:** добавлены UA-variants (хенді с і, сірман, итд) + проверка c35 симметрично с c36.

## Summary by brand × column (только non-zero)

| Brand | c4 name_mod UA | c5 name_mod RU | c6 name UA | c7 name RU | c24 kw UA | c25 kw RU | c35 desc UA | c36 desc RU | LIVE SKU |
|---|---|---|---|---|---|---|---|---|---|
| **Apach** | · | · | · | · | 9 | 9 | · | · | 1 |
| **Bartscher** | · | · | · | · | 13 | 13 | · | · | 12 |
| **Ceado** | · | · | · | · | 9 | 9 | · | · | 4 |
| **Fagor** | · | · | · | · | 3 | 3 | · | · | 1 |
| **Forcar** | · | · | · | · | 3 | 4 | · | · | 4 |
| **GoodFood** | · | · | · | · | 68 | 64 | · | · | 28 |
| **Hendi** | · | · | · | · | 274 | 272 | · | · | 264 |
| **Hurakan** | · | · | · | · | 19 | 16 | · | · | 0 |
| **Krupps** | · | · | · | · | 30 | 31 | · | · | 30 |
| **Pavoni** | · | · | · | · | 7 | 7 | · | · | 7 |
| **Saro** | · | · | · | · | 6 | 6 | · | · | 6 |
| **Sirman** | · | · | · | · | 17 | 17 | · | · | 16 |
| **Tatra** | · | · | · | · | 1 | 1 | · | · | 0 |
| **Tefcold** | · | · | · | · | 12 | 12 | · | · | 2 |

**Уникальных SKU c хитом в c35 (UA desc): 0** — НУЖЕН UA fix (живут на сайте: 0)
**Уникальных SKU c хитом в c36 (RU desc): 0** — RU fix частично применён (Hendi 4 patched в v1)
**Уникальных SKU c хитом в c4/c5/c6/c7 (names): 0**

## c35 (Описание товара UA) — главная зона UA для SEO

## c36 (Описание товара RU) — post-v1-patch state

## c4-c7 (Названия UA + RU) — должно быть 0 для bundle live
