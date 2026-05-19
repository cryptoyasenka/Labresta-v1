# chunk-025 — ручная проверка для Yana (русский)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-025 (64 SKU)
**Apply key:** `Артикул` (scoped per row)
**Status:** IN PROGRESS 8/64

Здесь собираю всё, что требует твоего подтверждения (не авто-фиксы). Авто-фиксы по locked-паттернам перечислены в сводках по батчам, отдельного подтверждения не требуют. Открытые вопросы накапливаются в нумерованный список и финализируются при закрытии chunk-025. SKIP-НП SKU (НП-эксклюзивные бренды) помечаются здесь и не переписываются.

---

## Батч SKU 1-8 (8/64)

Артикулы: `976768460` (Стол холодильный FROSTY GN4100TN (ширина 700 мм) — **blk триплет**, FROSTY НЕ НП-эксклюзив, desc UA==RU True 1178/1178 🔴 RU=UA + nm_ru укр.-leak `і`, AUTO Назв.мод RU = genuine nazv_ru + Описание RU полный перевод тег-в-tag), `1892001780` (Стол холодильный HATA SNACKH2200TN S/S304 с ботром — **blknochg**, genuine RU LIVE-магазин, src-typo `ботром` faithful), `1892681270` (HATA SNACKH3100TN — **blknochg**), `1892683653` (HATA SNACKH2100TN — **blknochg**), `1892693130` (HATA SNACKH3200TN — **blknochg**), `2047025084` (Brillis BGN3-R290-EF — **blknochg**), `2120030480` (HATA GNH3100TN — **blknochg**), `2212706299` (GoodFood GF-S901-H6C — **blknochg**). Батч 1 chunk-025 — столы холодильные (blk триплет 1 + blknotrip 0 + blknochg 7 + blknochgeq 0 + SKIP-НП 0). Продолжение chunk-024 (закрыт 74/74).

### Стандартно применено (locked-паттерны, отдельного подтверждения не требуют)
- **blk триплет — 1.** SKU 1 `976768460` FROSTY GN4100TN: `desc UA==RU` **True** 1178/1178 (🔴 RU=UA, RU = полная укр. копия), `nm_ru`==`nm_ua` укр.-leak `і`, `nm_ru`!=`nazv_ru` genuine. **FROSTY НЕ ∈ НП-эксклюзивный список** → обычная обработка. AUTO: Назв.мод (RU) → genuine `nazv_ru` `Стол холодильный FROSTY GN4100TN (ширина 700 мм)`; Описание (RU) полный перевод тег-в-tag (3 `<p>` / 1 `<ul>` / 7 `<li>` / 3 литер. `<br>` / 2 `<img>` verbatim; переводы строк зеркально). Код `FROSTY GN4100TN` идентичен UA↔RU → customer-facing рассинхрона НЕТ. SOFT (не нумеровано): литеральный ° U+00B0 ×4 → `&deg;` (буква после градуса зеркальна источнику: Cyrillic С в `-2&deg;С`, latin C в `+8/+43 &deg;C`; spacing источника зеркально); latin x U+0078 ×2 в `2230x700x860` → Cyrillic х (homoglyph-разделитель размера, без пробелов; latin x в URL картинки / `640px`/`353px` style verbatim); `220 В` (Cyrillic В) / `0,35` / хвостовой пробел `<li>553 л. </li>` verbatim.
- **blknochg — 7 (LIVE-магазин Horoshop, genuine RU НЕ переписываем).** SKU 2-8 (`1892001780`/`1892681270`/`1892683653`/`1892693130` Hata SNACKH-серия, `2047025084` Brillis BGN3-R290-EF, `2120030480` Hata GNH3100TN, `2212706299` GoodFood GF-S901-H6C): `desc UA==RU` **False** (в RU отдельный корректный русский перевод поставщика, НЕ укр. копия), `nm_ru`==`nazv_ru` чистый рус. (char-level UA-leak і/ї/є/ґ НЕТ), `nm_ru`!=`nm_ua` (укр. leak только в `nm_ua`). Бренды Hata/Brillis/GoodFood **НЕ ∈ НП-эксклюзивный список**. RU уже корректный русский — genuine RU-тело перезаписывать НЕЛЬЗЯ без явного go-ahead Yana + safe mode → Назв.мод (RU) и Описание (RU) НЕ трогаем (ячейки без изменений). Коды SNACKH2200TN/SNACKH3100TN/SNACKH2100TN/SNACKH3200TN/GNH3100TN / Brillis BGN3-R290-EF / GoodFood GF-S901-H6C идентичны UA↔RU genuine → customer-facing рассинхрона НЕТ.
- **SKIP-НП — 0 (кумул. chunk-025 = 0).** Бренды батча FROSTY/Hata/Brillis/GoodFood — НЕ ∈ НП-эксклюзивный список (HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA, без регистра, латиница И кириллица) → обычная обработка, без SKIP.
- **Классификация по `desc UA==RU`.** **blk триплет 1. blknotrip 0. blknochg 7. blknochgeq 0. SKIP-НП 0.**
- **META keywords (SKU 1-8):** оставлены faithful со всеми артефактами источника (META UA!=RU genuine; часть META частично содержит укр./смешанные формы — артефакт источника). META по правилу всегда faithful.

### Заслуживает внимания (soft, без блокировки) — Открытых вопросов 0 (новых нумерованных в батче нет; NON-FLIP)
- **SKU 1 литеральный ° U+00B0 ×4** (`+43 °C` p-блок; `-2°С`/`+8 °C`/`+43 °C` li-режим) → `&deg;` в авторском RU (locked-норм.: литеральный градус в авторском RU НЕ пишем). Буква после градуса зеркальна источнику: Cyrillic С (U+0421) в `-2&deg;С`, latin C в `+8 &deg;C`/`+43 &deg;C`; spacing источника (`-2°С` без пробела / `+8 °C` с пробелом) зеркально → soft, не нумеруется.
- **SKU 1 latin x U+0078 ×2** в `2230x700x860` → Cyrillic х U+0445 (homoglyph-разделитель размера, без пробелов). Latin x в URL картинки (`...xolodilnik...`) и `640px`/`353px` в style — verbatim (НЕ разделитель размера) → soft, не нумеруется.
- **SKU 2 genuine `nazv_ru` src-typo `ботром`** (вместо `бортом` — перестановка букв) — genuine RU, **LIVE-магазин Horoshop**, перезаписывать НЕЛЬЗЯ без go-ahead Yana → ячейку НЕ трогаем; src-typo faithful; код `SNACKH2200TN` идентичен UA↔RU genuine — customer-facing рассинхрона кода/артикула НЕТ → soft, не нумеруется.
- **SKU 2-8 genuine RU ≠ UA** — `desc UA==RU` False, genuine отдельный корректный русский перевод поставщика; LIVE-магазин → genuine RU НЕ переписываем, ячейки без изменений → soft, не нумеруется.
- **SKU 1-8: META RU частично укр./смешанные формы / META UA!=RU genuine** — META по правилу всегда faithful → soft, не нумеруется.

### Сводка батча

| SKU | Артикул | Тип | Назв.мод | Прочее |
|---|---|---|---|---|
| 1 | 976768460 | **blk триплет** | `Стіл холодильний FROSTY GN4100TN (ширина 700 мм)` → `Стол холодильный FROSTY GN4100TN (ширина 700 мм)` (genuine nazv_ru) | FROSTY НЕ НП-эксклюзив; `desc UA==RU` **True** 1178/1178 🔴 RU=UA + `nm_ru` укр.-leak `і`; Описание RU полный перевод тег-в-tag (3 p / 1 ul / 7 li / 3 br / 2 img); ° U+00B0 ×4→`&deg;`, latin x ×2→Cyrillic х (SOFT); код `FROSTY GN4100TN` идентичен UA↔RU |
| 2 | 1892001780 | **blknochg** | без изменений (genuine чистый рус.) | Hata НЕ НП-эксклюзив; `desc UA==RU` **False** 529/511; genuine RU LIVE-магазин НЕ переписываем; src-typo `ботром` faithful (код `SNACKH2200TN` идентичен UA↔RU) |
| 3 | 1892681270 | **blknochg** | без изменений | Hata; `desc UA==RU` **False** 525/507; genuine RU LIVE НЕ трогаем; код `SNACKH3100TN` идентичен UA↔RU |
| 4 | 1892683653 | **blknochg** | без изменений | Hata; `desc UA==RU` **False** 530/512; genuine RU LIVE НЕ трогаем; код `SNACKH2100TN` идентичен UA↔RU |
| 5 | 1892693130 | **blknochg** | без изменений | Hata; `desc UA==RU` **False** 525/506; genuine RU LIVE НЕ трогаем; код `SNACKH3200TN` идентичен UA↔RU |
| 6 | 2047025084 | **blknochg** | без изменений | Brillis НЕ НП-эксклюзив; `desc UA==RU` **False** 2224/2238; genuine RU LIVE НЕ трогаем; код `Brillis BGN3-R290-EF` идентичен UA↔RU |
| 7 | 2120030480 | **blknochg** | без изменений | Hata; `desc UA==RU` **False** 523/504; genuine RU LIVE НЕ трогаем; код `GNH3100TN` идентичен UA↔RU |
| 8 | 2212706299 | **blknochg** | без изменений | GoodFood НЕ НП-эксклюзив; `desc UA==RU` **False** 845/853; genuine RU LIVE НЕ трогаем; код `GoodFood GF-S901-H6C` идентичен UA↔RU; батч 8/64 |

Открытых вопросов по батчу: **0** (новых нумерованных нет; NON-FLIP — placeholder остаётся; SKU 1 blk триплет авто-перевод укр. копии + Назв.мод-leak триплет к genuine nazv_ru, код language-neutral; SKU 2-8 genuine RU ≠ UA LIVE-магазин НЕ переписываем; SKU 2 src-typo `ботром` faithful; ° U+00B0→`&deg;` / latin x→Cyrillic х SOFT; коды FROSTY GN4100TN/SNACKH*/GNH3100TN/BGN3-R290-EF/GF-S901-H6C идентичны UA↔RU — customer-facing рассинхрона названия/кода не порождает). blk триплет 1; blknotrip 0; blknochg 7; blknochgeq 0; SKIP-НП 0. Кумулятивно по chunk-025: **0** (новых нумерованных Открытых вопросов нет; placeholder остаётся). Кумулятивно SKIP-НП по chunk-025: **0** (b1 SKIP-НП 0). **chunk-025 — 8/64, далее батч SKU 9-16.**

---

## Открытые вопросы chunk-025

_(пока пусто — наполняется при аудите батчей)_

---

**Last updated:** 2026-05-19 — chunk-025 батч SKU 1-8 (8/64): FROSTY GN4100TN (blk триплет) + Hata SNACKH2200TN/SNACKH3100TN/SNACKH2100TN/SNACKH3200TN/GNH3100TN + Brillis BGN3-R290-EF + GoodFood GF-S901-H6C (blknochg ×7) — **blk триплет 1 + blknotrip 0 + blknochg 7 + blknochgeq 0 + SKIP-НП 0**. SKU 1 AUTO: Назв.мод RU = genuine nazv_ru + Описание RU полный перевод тег-в-tag; SKU 2-8 genuine RU LIVE-магазин НЕ переписываем (ячейки без изменений; SKU 2 src-typo `ботром` faithful). Коды FROSTY GN4100TN/SNACKH*/GNH3100TN/BGN3-R290-EF/GF-S901-H6C идентичны UA↔RU — customer-facing рассинхрона НЕТ. META always faithful. Открытых вопросов chunk-025 = 0 (NON-FLIP). Кумулятивно SKIP-НП chunk-025 = 0. chunk-025 = 8/64. NEXT: батч SKU 9-16.
