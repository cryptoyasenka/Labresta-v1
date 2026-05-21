# chunk-082 OQ #12 apply — 2026-05-21

**Status:** APPLIED (per Yana decision via AskUserQuestion, ref W2-OQ-ANSWERS.md).

## Правка

- **SKU:** r35 ART=2043415778 Frosty H 168D (винный шкаф, 430 л, 2 зоны)
- **Поле:** col36 RU body (характеристика bottle range)
- **Замена (1 вхождение):** `68-169 бутылок` → `68-168 бутылок`
- **Причина:** имя модели H168D = max 168 bottles. Source UA «169-68» — off-by-one опечатка (high-low reversed). Канон 168.
- Категория r35 переходит blknochg → blkfix.

## Forward к W1

- col35 UA body: «місткість 169-68 пляшок» → «місткість 68-168 пляшок» (синхронизация с RU + reorder low-high).
