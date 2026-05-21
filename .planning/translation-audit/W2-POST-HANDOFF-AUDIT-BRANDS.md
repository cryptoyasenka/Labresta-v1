# W2 post-handoff audit v2 — slavified brand names (cyrillic) in fixed.xlsx 055-085

**Дата:** 2026-05-21
**Триггер:** Yana заметила «хенди» (кириллица) на live SKU `Тендерайзер Hendi 843468`.
**Скоп:** все 31 chunk W2 (055-085, 2168 SKU), 8 trans cols.
**v2 fix:** word-boundary regex (\b) исключает FP типа `максима` в `максимальный`.

## Summary

| Brand (canon) | Cells found | c36 desc RU | c35 desc UA | c25 kw RU | c5/c7 names RU | SKU live (in bundle) |
|---|---|---|---|---|---|---|
| **Apach** | 18 | 0 | 0 | 9 | 0 | 1 |
| **Bartscher** | 26 | 0 | 0 | 13 | 0 | 12 |
| **Ceado** | 18 | 0 | 0 | 9 | 0 | 4 |
| **Fagor** | 6 | 0 | 0 | 3 | 0 | 1 |
| **Forcar** | 7 | 0 | 0 | 4 | 0 | 4 |
| **GoodFood** | 132 | 0 | 0 | 64 | 0 | 28 |
| **Hendi** | 555 | 4 | 5 | 272 | 0 | 268 |
| **Hurakan** | 35 | 0 | 0 | 16 | 0 | 0 |
| **Krupps** | 61 | 0 | 0 | 31 | 0 | 30 |
| **Pavoni** | 14 | 0 | 0 | 7 | 0 | 7 |
| **Saro** | 12 | 0 | 0 | 6 | 0 | 6 |
| **Sirman** | 34 | 0 | 0 | 17 | 0 | 16 |
| **Tatra** | 2 | 0 | 0 | 1 | 0 | 0 |
| **Tefcold** | 24 | 0 | 0 | 12 | 0 | 2 |
| **TOTAL** | **944** |  |  |  |  | **379** |

## Per-brand detail — c36 (Описание товара RU) ONLY, главный SEO surface

> c25 (META keywords) кириллица — допустима (Yana ack), не фиксим.
> c35 (UA descriptions) — forward к W1 (W2 UA не правит).

### Hendi  — 4 ячеек в c36 / 4 unique SKU / 4 live в bundle

**По чанкам:** 055=4

**Sample 5:**

- `chunk-055` r9 ART=2123243855 (✓ LIVE) match=`хенди` — `...<p>Современный размягчитель мяса хенди, особенно полезен для приготовления мяса на гриле. Продукция Hendi отличае...`
- `chunk-055` r10 ART=2123249689 (✓ LIVE) match=`хенди` — `...<p>Современный размягчитель мяса хенди, особенно полезен для приготовления мяса на гриле. Продукция Hendi отличае...`
- `chunk-055` r11 ART=2123250967 (✓ LIVE) match=`хенди` — `...<p>Современный размягчитель мяса хенди, особенно полезен для приготовления мяса на гриле. Продукция Hendi отличае...`
- `chunk-055` r12 ART=2123251224 (✓ LIVE) match=`хенди` — `...<p>Современный размягчитель мяса хенди, особенно полезен для приготовления мяса на гриле. Продукция Hendi отличае...`

**ИТОГО c36 (descriptions RU) — уникальных SKU затронуто: 4**
**Из них LIVE в bundle сейчас: 4**

## Per-brand — c5/c7 (Названия RU) — критическая зона (имя товара)

**ИТОГО c5/c7: 0 ячеек**

## c25 META keywords (RU) — distribution (NOT to fix, Yana ack)

| Brand | Cells in c25 |
|---|---|
| Apach | 9 |
| Bartscher | 13 |
| Ceado | 9 |
| Fagor | 3 |
| Forcar | 4 |
| GoodFood | 64 |
| Hendi | 272 |
| Hurakan | 16 |
| Krupps | 31 |
| Pavoni | 7 |
| Saro | 6 |
| Sirman | 17 |
| Tatra | 1 |
| Tefcold | 12 |

## Tautology check (c36) — одновременно cyr + lat одного бренда в той же ячейке

**Найдено 4 ячеек c36 c cyr+lat одного бренда:**

- `chunk-055` r9 ART=2123243855 (✓ LIVE) — `Hendi` + cyr `хенди` — `...<p>Современный размягчитель мяса хенди, особенно полезен для приготовления мяса на гриле. Продукция Hendi отличается высоким качеством и универсальностью, представленная модель рекомендована для использования на профессиональной кухн...`
- `chunk-055` r10 ART=2123249689 (✓ LIVE) — `Hendi` + cyr `хенди` — `...<p>Современный размягчитель мяса хенди, особенно полезен для приготовления мяса на гриле. Продукция Hendi отличается высоким качеством и универсальностью, представленная модель рекомендованная для использования на профессиональной ку...`
- `chunk-055` r11 ART=2123250967 (✓ LIVE) — `Hendi` + cyr `хенди` — `...<p>Современный размягчитель мяса хенди, особенно полезен для приготовления мяса на гриле. Продукция Hendi отличается высоким качеством и универсальностью, представленная модель рекомендованная для использования на профессиональной ку...`
- `chunk-055` r12 ART=2123251224 (✓ LIVE) — `Hendi` + cyr `хенди` — `...<p>Современный размягчитель мяса хенди, особенно полезен для приготовления мяса на гриле. Продукция Hendi отличается высоким качеством и универсальностью, представленная модель рекомендованная для использования на профессиональной ку...`

## Proposed fix plan

1. **c36 (descriptions RU) — regex replace cyr→latin:**
   - Для каждого бренда: word-boundary case-insensitive replace cyr-variant → canonical latin
   - После replace проверить tautology (Hendi…Hendi одним абзацем) — рерайт лид-предложения
2. **c5/c7 (names RU) — точечный fix:**
   - Если имя модификации/название содержит cyr-бренд — fix вручную с учётом склонения
3. **c25 META keywords (RU) — НЕ ТРОГАТЬ** (Yana ack)
4. **c35 UA descriptions — forward к W1** (W2 UA не правит)
5. **Patch-bundle build:**
   - rows из 9-col fixed.xlsx, в которых c36 или c5/c7 изменились patch-passом
   - + 14 unchanged-but-live SKU (бренд cyr был в Horoshop до W2, мы пропустили) → вытащить из horoshop-export, fix, добавить
   - Schema 9 cols как основной bundle (важно: НЕ оставлять пустые → wipe)
6. **Спот-чек patch-bundle** (5-10 SKU live) → full re-import только этого patch

## Files

- Audit script v2: `.planning/translation-audit/_audit_brands_v2.py`
- This report (v2 overwrote v1): `W2-POST-HANDOFF-AUDIT-BRANDS.md`
- Pending: `_w2_apply_brand_fix.py` + `w2-horoshop-import-PATCH-brands.xlsx` (на след. сессии после approval)