# chunk-025 — ручная проверка для Yana (русский)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-025 (64 SKU)
**Apply key:** `Артикул` (scoped per row)
**Status:** IN PROGRESS 16/64

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

## Батч SKU 9-16 (16/64)

Артикулы: `2352435750` (Стол холодильный FROSTY PA 2100TN — **blk триплет**, FROSTY НЕ НП-эксклюзив, desc UA==RU True 552/552 🔴 RU=UA + nm_ru укр.-leak `і`, AUTO Назв.мод RU = genuine nazv_ru + Описание RU полный перевод тег-в-tag), `2448654996` (Стол холодильный Brillis PZ903 — **blknochg**, genuine RU LIVE-магазин), `2448656678` (Brillis СС2100 — **blknochg**), `2448658314` (Brillis СС3100 — **blknochg**), `2580508899` (GoodFood GF-S901-4D-H6C — **blknochg**), `595397996` (FROSTY SNACK 2100TN — **blknochg**), `595397997` (FROSTY SNACK 3100TN — **blknochg**), `701178117` (Холодильный стол COOLEQ S901 (0,9 м) — **blk триплет**, Cooleq НЕ НП-эксклюзив (Cooleq != COLD по границе слова), desc UA==RU True 300/300 🔴 RU=UA + nm_ru укр.-leak `і`, AUTO Назв.мод RU = genuine nazv_ru + Описание RU полный перевод тег-в-tag). Батч b9 chunk-025 — столы холодильные (blk триплет 2 + blknotrip 0 + blknochg 6 + blknochgeq 0 + SKIP-НП 0). Продолжение chunk-024 (закрыт 74/74).

### Стандартно применено (locked-паттерны, отдельного подтверждения не требуют)
- **blk триплет — 2.** SKU 9 `2352435750` FROSTY PA 2100TN: `desc UA==RU` **True** 552/552 (🔴 RU=UA), `nm_ru`==`nm_ua` укр.-leak `і`, `nm_ru`!=`nazv_ru` genuine. SKU 16 `701178117` Cooleq S901 (0,9 м): `desc UA==RU` **True** 300/300 (🔴 RU=UA), `nm_ru`==`nm_ua` укр.-leak `і`, `nm_ru`!=`nazv_ru` genuine (порядок слов источника: `Холодильный стол COOLEQ ...` — прилагательное первым, COOLEQ latin verbatim). **FROSTY/Cooleq НЕ ∈ НП-эксклюзивный список** (Cooleq != COLD по границе слова) → обычная обработка. AUTO: Назв.мод (RU) → genuine `nazv_ru`; Описание (RU) полный перевод тег-в-tag (SKU 9: 2 `<p>` / 1 `<ul>` / 7 `<li>` / 0 `<br>`; SKU 16: 1 `<p>` / 1 `<ul>` / 7 `<li>` / 0 `<br>`; переводы строк зеркально). Коды `FROSTY PA 2100TN` / `COOLEQ S901` идентичны UA↔RU → customer-facing рассинхрона НЕТ. SOFT (не нумеровано): SKU 9 `&deg;` ENTITY ×3 зеркально (буква после градуса зеркальна источнику: Cyrillic С U+0421 в `-2&deg;С`/`+43&deg;С`, latin C в `+8&deg;C`; spacing источника без пробела зеркально) + `&#39;` укр.-апостроф в `Об&#39;єм` → DROP (`Объём`) + latin x U+0078 ×2 в `1510мм x 800мм x 850мм` → Cyrillic х (пробелы источника зеркально); SKU 16 литер. ° U+00B0 ×1 в `+2...+8 °C` → `&deg;` (пробел перед градусом зеркально, latin C) + literal апостроф U+0027 в `Об'єм` → DROP (`Объём`) + latin x ×2 в `900x700x860` → Cyrillic х (без пробелов зеркально); `220В`(SKU9, без пробела)/`220 В`(SKU16, с пробелом) Cyrillic В voltage / `0,30`/`0,23` запятая / `Д*Ш*В` / `AISI-304` / `GN 1/1 ` хвост. пробел / `+2...+8` диапазон / run-on `обдування Матеріал` verbatim.
- **blknochg — 6 (LIVE-магазин Horoshop, genuine RU НЕ переписываем).** SKU 10-15 (`2448654996` Brillis PZ903, `2448656678` Brillis СС2100, `2448658314` Brillis СС3100, `2580508899` GoodFood GF-S901-4D-H6C, `595397996` FROSTY SNACK 2100TN, `595397997` FROSTY SNACK 3100TN): `desc UA==RU` **False** (в RU отдельный корректный русский перевод поставщика, НЕ укр. копия), `nm_ru`==`nazv_ru` чистый рус. (char-level UA-leak і/ї/є/ґ НЕТ), `nm_ru`!=`nm_ua` (укр. leak только в `nm_ua`). Бренды Brillis/GoodFood/FROSTY **НЕ ∈ НП-эксклюзивный список**. RU уже корректный русский — genuine RU-тело перезаписывать НЕЛЬЗЯ без явного go-ahead Yana + safe mode → Назв.мод (RU) и Описание (RU) НЕ трогаем (ячейки без изменений). Коды Brillis PZ903/СС2100/СС3100 / GoodFood GF-S901-4D-H6C / FROSTY SNACK 2100TN/3100TN идентичны UA↔RU genuine → customer-facing рассинхрона НЕТ. (`СС` в кодах Brillis = Cyrillic С×2 U+0421 verbatim.)
- **SKIP-НП — 0 (кумул. chunk-025 = 0).** Бренды батча FROSTY/Brillis/GoodFood/Cooleq — НЕ ∈ НП-эксклюзивный список (HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA, без регистра, латиница И кириллица; Cooleq != COLD по границе слова) → обычная обработка, без SKIP.
- **Классификация по `desc UA==RU`.** **blk триплет 2. blknotrip 0. blknochg 6. blknochgeq 0. SKIP-НП 0.**
- **META keywords (SKU 9-16):** оставлены faithful со всеми артефактами источника (META UA!=RU genuine; часть META частично содержит укр./смешанные формы — артефакт источника). META по правилу всегда faithful.

### Заслуживает внимания (soft, без блокировки) — Открытых вопросов 0 (новых нумерованных в батче нет; NON-FLIP)
- **SKU 9 `&deg;` ENTITY ×3** (`-2&deg;С`/`+8&deg;C`/`+43&deg;С`) — литер. ° U+00B0 ×0 в источнике; `&deg;` mirrored verbatim. Буква после градуса зеркальна источнику: Cyrillic С (U+0421) в `-2&deg;С`/`+43&deg;С`, latin C в `+8&deg;C`; spacing источника (без пробела) зеркально → soft, не нумеруется.
- **SKU 9 `&#39;` укр.-апостроф** в `Об&#39;єм` → DROP в авторском RU (`Объём`) — укр. апостроф в RU не воспроизводим → soft, не нумеруется.
- **SKU 9 latin x U+0078 ×2** в `1510мм x 800мм x 850мм` → Cyrillic х U+0445 (homoglyph-разделитель размера, пробелы источника зеркально) → soft, не нумеруется.
- **SKU 16 литер. ° U+00B0 ×1** в `+2...+8 °C` → `&deg;` в авторском RU (locked-норм.: литеральный градус в авторском RU НЕ пишем). Пробел перед градусом зеркально, latin C после → soft, не нумеруется.
- **SKU 16 literal апостроф U+0027 ×1** в `Об'єм` → DROP в авторском RU (`Объём`) → soft, не нумеруется.
- **SKU 16 latin x U+0078 ×2** в `900x700x860` → Cyrillic х U+0445 (homoglyph-разделитель размера, без пробелов зеркально) → soft, не нумеруется.
- **SKU 11/12 Brillis `СС2100`/`СС3100`** — `СС` = Cyrillic С×2 (U+0421) в genuine `nazv_ru`/`nm_ru`; blknochg LIVE-магазин НЕ трогаем; код идентичен UA↔RU genuine → soft, не нумеруется.
- **SKU 10-15 genuine RU ≠ UA** — `desc UA==RU` False, genuine отдельный корректный русский перевод поставщика; LIVE-магазин → genuine RU НЕ переписываем, ячейки без изменений → soft, не нумеруется.
- **SKU 9-16: META RU частично укр./смешанные формы / META UA!=RU genuine** — META по правилу всегда faithful → soft, не нумеруется.

### Сводка батча

| SKU | Артикул | Тип | Назв.мод | Прочее |
|---|---|---|---|---|
| 9 | 2352435750 | **blk триплет** | `Стіл холодильний FROSTY PA 2100TN` → `Стол холодильный FROSTY PA 2100TN` (genuine nazv_ru) | FROSTY НЕ НП-эксклюзив; `desc UA==RU` **True** 552/552 🔴 RU=UA + `nm_ru` укр.-leak `і`; Описание RU полный перевод тег-в-tag (2 p / 1 ul / 7 li / 0 br); `&deg;`×3 зеркально, `&#39;`→DROP, latin x ×2→Cyrillic х (SOFT); `220В` без пробела; код `FROSTY PA 2100TN` идентичен UA↔RU |
| 10 | 2448654996 | **blknochg** | без изменений (genuine чистый рус.) | Brillis НЕ НП-эксклюзив; `desc UA==RU` **False** 1011/1021; genuine RU LIVE-магазин НЕ переписываем; код `PZ903` идентичен UA↔RU |
| 11 | 2448656678 | **blknochg** | без изменений | Brillis; `desc UA==RU` **False** 887/890; genuine RU LIVE НЕ трогаем; код `СС2100` (Cyrillic С×2) идентичен UA↔RU |
| 12 | 2448658314 | **blknochg** | без изменений | Brillis; `desc UA==RU` **False** 887/890; genuine RU LIVE НЕ трогаем; код `СС3100` (Cyrillic С×2) идентичен UA↔RU |
| 13 | 2580508899 | **blknochg** | без изменений | GoodFood НЕ НП-эксклюзив; `desc UA==RU` **False** 877/859; genuine RU LIVE НЕ трогаем; код `GF-S901-4D-H6C` идентичен UA↔RU |
| 14 | 595397996 | **blknochg** | без изменений | FROSTY НЕ НП-эксклюзив; `desc UA==RU` **False** 1031/1038; genuine RU LIVE НЕ трогаем; код `SNACK 2100TN` идентичен UA↔RU |
| 15 | 595397997 | **blknochg** | без изменений | FROSTY; `desc UA==RU` **False** 1031/1038; genuine RU LIVE НЕ трогаем; код `SNACK 3100TN` идентичен UA↔RU |
| 16 | 701178117 | **blk триплет** | `Холодильний стіл COOLEQ S901 (0,9 м)` → `Холодильный стол COOLEQ S901 (0,9 м)` (genuine nazv_ru) | Cooleq НЕ НП-эксклюзив (Cooleq != COLD по границе слова); `desc UA==RU` **True** 300/300 🔴 RU=UA + `nm_ru` укр.-leak `і`; Описание RU полный перевод тег-в-tag (1 p / 1 ul / 7 li / 0 br); ° U+00B0 ×1→`&deg;`, U+0027→DROP, latin x ×2→Cyrillic х (SOFT); `220 В` с пробелом; `AISI-304` verbatim; код `COOLEQ S901` идентичен UA↔RU; батч 16/64 |

Открытых вопросов по батчу: **0** (новых нумерованных нет; NON-FLIP — placeholder остаётся; SKU 9/16 blk триплет авто-перевод укр. копии + Назв.мод-leak триплет к genuine nazv_ru, код language-neutral; SKU 10-15 genuine RU ≠ UA LIVE-магазин НЕ переписываем; `&deg;`/° U+00B0→`&deg;` / `&#39;`/U+0027→DROP / latin x→Cyrillic х SOFT; коды FROSTY PA 2100TN/COOLEQ S901/Brillis PZ903/СС2100/СС3100/GF-S901-4D-H6C/SNACK 2100TN/3100TN идентичны UA↔RU — customer-facing рассинхрона названия/кода не порождает). blk триплет 2; blknotrip 0; blknochg 6; blknochgeq 0; SKIP-НП 0. Кумулятивно по chunk-025: **0** (новых нумерованных Открытых вопросов нет; placeholder остаётся). Кумулятивно SKIP-НП по chunk-025: **0** (b1 0 + b9 0). **chunk-025 — 16/64, далее батч SKU 17-24.**

---

## Открытые вопросы chunk-025

_(пока пусто — наполняется при аудите батчей)_

---

**Last updated:** 2026-05-19 — chunk-025 батч SKU 9-16 (16/64): FROSTY PA 2100TN + Cooleq S901 (blk триплет ×2) + Brillis PZ903/СС2100/СС3100 + GoodFood GF-S901-4D-H6C + FROSTY SNACK 2100TN/3100TN (blknochg ×6) — **blk триплет 2 + blknotrip 0 + blknochg 6 + blknochgeq 0 + SKIP-НП 0**. SKU 9/16 AUTO: Назв.мод RU = genuine nazv_ru + Описание RU полный перевод тег-в-tag; SKU 10-15 genuine RU LIVE-магазин НЕ переписываем (ячейки без изменений). Коды FROSTY PA 2100TN/COOLEQ S901/Brillis PZ903/СС2100/СС3100/GF-S901-4D-H6C/SNACK 2100TN/3100TN идентичны UA↔RU — customer-facing рассинхрона НЕТ. META always faithful. Открытых вопросов chunk-025 = 0 (NON-FLIP). Кумулятивно SKIP-НП chunk-025 = 0. chunk-025 = 16/64. NEXT: батч SKU 17-24.
