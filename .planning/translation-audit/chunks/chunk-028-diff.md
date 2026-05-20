# chunk-028 translation diff (61 SKU — холодильное оборудование, продолжение chunk-027)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-028 (61 SKU, продолжение chunk-027)
**Apply key:** `Артикул` (scoped per row)
**Status:** IN PROGRESS 8/61

**Состав (по типу товара):** первый SKU — Артикул `1154540778`, бренд TEFCOLD (`Морозильна шафа Tefcold UF600S (-18°...-22 °C, нерж.)`, раздел `Холодильне та морозильне обладнання/Шафи морозильні` — продолжение/повтор раздела chunk-027 `Морозильні шафи` с инвертированным порядком слов в названии раздела). Раздел `Шафи морозильні` занимает 14 SKU (SKU 1-14, бренды Tefcold ×7 + Gooder ×3 + Snaige ×3 + Tatra ×1), далее начинается новый раздел `Холодильне та морозильне обладнання/Морозильні столи` (45 SKU, SKU 15-59 — бренды Tefcold ×9 + FROSTY ×4 + Apach ×3 + REEDNEE ×3 + Tecnodom ×3 + Cooleq ×3 + Brillis ×3 + Gooder ×3 + Fagor ×3 + Tatra ×2 + Forcar ×2 + Hurakan ×2 + GoodFood ×2 + GGM Gastro International ×1 + Hendi ×1 + Forcold ×1), завершается раздел новым разделом `Холодильне та морозильне обладнання/Холодильні шафи для вина` (2 SKU, SKU 60-61 — Tefcold ×1 + GoodFood ×1; последний SKU 61 — Артикул `2108377745`, бренд GOODFOOD, `Вітрина холодильна для вина GoodFood RT400L2`). Тип товара определяется per-SKU. Бренды per-SKU (17 total): Tefcold/Gooder/Snaige/Tatra/Apach/FROSTY/REEDNEE/Tecnodom/Cooleq/Brillis/Fagor/Forcar/Hurakan/GoodFood/GGM Gastro International/Hendi/Forcold — из них Tatra (×3) + Apach (×3) + Fagor (×3) + Hurakan (×2) = 11 SKU → SKIP-НП по правилу forward-only (SKU 14/18/19 Tatra; SKU 15/16/17 Apach; SKU 40/43/44 Fagor; SKU 26/59 Hurakan).

**Standing rules** (inherited from chunk-001 — chunk-027):
- **SKIP-НП (forward-only, приоритет над переводом):** SKU бренда из НП-эксклюзивного списка (HURAKAN/Хуракан, APACH/Апач, FAGOR/Фагор, TATRA/Татра, COLD/Колд, PROJECT SYSTEMS, ASTORIA, ARRIS, MAXIMA — case-insensitive, латиница и кириллица; Tefcold/Forcold НЕ входят — substring `cold` ≠ standalone бренд `COLD`) → RU НЕ переписывается, ячейки SKU не меняются; помечается `SKIP-НП (brand=<X>, тело из фида НП позже)` в MANUAL-REVIEW; отдельная категория в N/N. Без ретро-прохода.
- UA term `жаркова`/`жарильна`/`смарочна` → `жарочна` (locked Yana 2026-05-14; registry `GLOBAL-SWEEP-zharkova.md` — аудит per-SKU, добавлять в реестр при встрече)
- RU machine artifact `жареная поверхность` → `жарочная поверхность`; `жареная для жарки` → `жарочная` (drop дубля)
- UA `Контейнер для сбору жиру` → `Контейнер для збирання жиру` (ONLY предлог); RU `Контейнер по сбору жира` → `для сбора`
- UA/RU `мм :` → `мм:`
- RU `от NN до NNN&deg;C` → `от NN&deg;C до NNN&deg;C` ТОЛЬКО если UA имеет оба &deg;C и значения совпадают; иначе FLAG
- decimal `N.N` → `N,N` обе локали (реальные дроби: меняется разделитель, точность сохранена; integers/already-comma — no-op)
- RU-leak UA `і`→`и`; 🔴 RU=UA полная укр. копия → AUTO full RU translate (структура HTML tag-в-tag, ✅ АВТО)
- Название модификации (RU) на украинском → AUTO перевод по Название (RU)
- Очевидный typo (удвоение/выпадение слога) → AUTO; однозначная машинная мистрансляция → AUTO + note
- UA→RU операторские термины: `Деко`→`Противень`, `Деко-решітка`→`Противень-решётка`, `Піч НВЧ`→`Печь СВЧ`, `Візок`→`Тележка`, `Решітка`→`Решётка`, `Перфорований лист`→`Противень перфорированный` (memory `feedback_labresta_ua_ru_translation_rules`)
- **4 формат-политики A/B/C → GLOBAL assembly-time pass — НЕ per-SKU diff, НЕ FLAG.** A вес `NN.00`→`NN кг.`/целое · B латинская `x`→кириллическая `х` в габаритах · C пробел перед `мм/см` (вкл. UA `18кВт`/`27кВт` слитно). Спека `.planning/translation-audit/GLOBAL-SWEEP-format.md`; применяется `apply_chunk_diff.py` при сборке master-xlsx ко всем чанкам. **В chunk-028 вес `NN.00` / латинскую `x` / `NNмм` НЕ диффать и НЕ флагать — закрыто глобально.**
- **F (структурный, per-SKU):** HTML `<br />`-склейка двух+ характеристик в одном `<li>` → раздельные `<li>` зеркально чистой стороне. Применять при встрече (ретро chunks 005-008 закрыт).
- FLAG (НЕ авто, → MANUAL-REVIEW русский): T5 surface conflict (текст/код vs spec); RU temp values ≠ UA; spec single vs text dual zone; UA title без дескриптора что есть в body+RU; source data error UA=RU → soft note / Открытые вопросы. **Вес `NN.00` БОЛЬШЕ НЕ флагается (policy A глобально).**

---

## SKU 1/61 — Морозильный шкаф Tefcold UF600S (-18°...-22°С, нерж.) (Артикул 1154540778) — RU корректен; правок нет (LIVE Horoshop genuine RU)

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg: `desc UA==RU` **False** (в RU-описании отдельный корректный русский перевод поставщика, НЕ укр. копия); `nm_ru`==`nazv_ru` `Морозильный шкаф Tefcold UF600S (-18°...-22°С, нерж.)` (чистый рус., char-level UA-leak і/ї/є/ґ НЕТ), `nm_ru`!=`nm_ua` (UA word-leak в `nm_ua` `Морозильна шафа` vs RU `Морозильный шкаф` — каноник). **Tefcold НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring; substring `cold` в `Tefcold` ≠ standalone бренд `COLD` — bnd-SET sравнение word-boundary regex) → обычная обработка, НЕ SKIP-НП. RU уже корректный русский — **LIVE-магазин Horoshop**, genuine RU-тело перезаписывать НЕЛЬЗЯ без явного go-ahead Yana + safe mode → Назв.мод (RU) и Описание (RU) НЕ трогаем (ячейки chunk-028-fixed без изменений). genuine RU тело/название faithful: тело 1341 UA → 1376 RU (genuine отдельный перевод). nm_ua/nm_ru temp-range pair EXTRA — UA `Морозильна шафа Tefcold UF600S (-18°...-22 °C, нерж.)` Lat C space-before-°C vs RU `Морозильный шкаф Tefcold UF600S (-18°...-22°С, нерж.)` Cyr С no-space (LIVE Horoshop nazv title artefact — РАЗНЫЕ форматы между UA/RU, blknochg preserve verbatim, НЕ unify). LIVE Lat-`p` Horoshop artefact в обоих локалях — UA `1 pозпашна` + RU `1 pаспашная` (Lat p U+0070 + Cyr остаток слова, поставщик store-canonical, не нормализуем); RU body `Хладагент` correct (UA-typo `Хладогент` отсутствует — SKU 1 без UA-typo) — артефакты источника 1:1, genuine RU зеркалится источником verbatim (blknochg — НЕ переписываем, формат НЕ диффаем). Код `Tefcold UF600S` идентичен UA↔RU genuine в названии → customer-facing рассинхрона названия НЕТ → НЕ нумеровано. META always faithful (META UA!=RU genuine). Открытых вопросов 0.)*

*(scoped к row Артикул=1154540778)*

---

## SKU 2/61 — Морозильный шкаф Tefcold UFSC370G (Артикул 1156073829) — RU корректен; правок нет (LIVE Horoshop genuine RU)

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg: `desc UA==RU` **False** (в RU-описании отдельный корректный русский перевод поставщика, НЕ укр. копия); `nm_ru`==`nazv_ru` `Морозильный шкаф Tefcold UFSC370G` (чистый рус., char-level UA-leak і/ї/є/ґ НЕТ), `nm_ru`!=`nm_ua` (UA word-leak в `nm_ua` `Морозильна шафа` vs RU `Морозильный шкаф` — каноник). **Tefcold НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring; substring `cold` в `Tefcold` ≠ standalone бренд `COLD` — bnd-SET sравнение word-boundary regex) → обычная обработка, НЕ SKIP-НП. RU уже корректный русский — **LIVE-магазин Horoshop**, genuine RU-тело перезаписывать НЕЛЬЗЯ без явного go-ahead Yana + safe mode → Назв.мод (RU) и Описание (RU) НЕ трогаем (ячейки chunk-028-fixed без изменений). genuine RU тело/название faithful: тело 1060 UA → 1092 RU (genuine отдельный перевод). LIVE Lat-`p` Horoshop artefact ТОЛЬКО в RU body `pаспашная` (UA body без Lat-p — desync per-SKU Horoshop, preserve verbatim); RU body `Хладагент` correct — артефакты источника 1:1, genuine RU зеркалится источником verbatim (blknochg — НЕ переписываем, формат НЕ диффаем). Код `Tefcold UFSC370G` идентичен UA↔RU genuine в названии → customer-facing рассинхрона названия НЕТ → НЕ нумеровано. META always faithful (META UA!=RU genuine). Открытых вопросов 0.)*

*(scoped к row Артикул=1156073829)*

---

## SKU 3/61 — Морозильный шкаф Tefcold UFSC371SD (UFSC370SD) (Артикул 1156077540) — RU корректен; правок нет (LIVE Horoshop genuine RU)

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg: `desc UA==RU` **False** (в RU-описании отдельный корректный русский перевод поставщика, НЕ укр. копия); `nm_ru`==`nazv_ru` `Морозильный шкаф Tefcold UFSC371SD (UFSC370SD)` (чистый рус., char-level UA-leak і/ї/є/ґ НЕТ), `nm_ru`!=`nm_ua` (UA word-leak в `nm_ua` `Морозильна шафа` vs RU `Морозильный шкаф` — каноник). **Tefcold НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring; substring `cold` в `Tefcold` ≠ standalone бренд `COLD` — bnd-SET sравнение word-boundary regex) → обычная обработка, НЕ SKIP-НП. RU уже корректный русский — **LIVE-магазин Horoshop**, genuine RU-тело перезаписывать НЕЛЬЗЯ без явного go-ahead Yana + safe mode → Назв.мод (RU) и Описание (RU) НЕ трогаем (ячейки chunk-028-fixed без изменений). genuine RU тело/название faithful: тело 1041 UA → 1082 RU (genuine отдельный перевод). LIVE Lat-`p` Horoshop artefact ТОЛЬКО в RU body `pаспашная`; UA body содержит HTML apostrophe entity `&#39;` для `об&#39;єм` (UA литеральная apos-entity LIVE); RU body уже `объём` ё drop апостроф (genuine LIVE) + `Хладагент` correct — артефакты источника 1:1, genuine RU зеркалится источником verbatim (blknochg — НЕ переписываем, формат НЕ диффаем). Код `Tefcold UFSC371SD (UFSC370SD)` идентичен UA↔RU genuine в названии — двойной артикул (UFSC371SD primary + UFSC370SD alias) consistent → customer-facing рассинхрона названия НЕТ → НЕ нумеровано. META always faithful (META UA!=RU genuine). Открытых вопросов 0.)*

*(scoped к row Артикул=1156077540)*

---

## SKU 4/61 — Морозильный шкаф Tefcold UFSC370G Black снято с производства (Артикул 1774252015) — RU корректен; правок нет (LIVE Horoshop genuine RU)

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg: `desc UA==RU` **False** (в RU-описании отдельный корректный русский перевод поставщика, НЕ укр. копия); `nm_ru`==`nazv_ru` `Морозильный шкаф Tefcold UFSC370G Black снято с производства` (чистый рус., char-level UA-leak і/ї/є/ґ НЕТ), `nm_ru`!=`nm_ua` (UA word-leak в `nm_ua` `Морозильна шафа` vs RU `Морозильный шкаф` — каноник). **Tefcold НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring; substring `cold` в `Tefcold` ≠ standalone бренд `COLD` — bnd-SET sравнение word-boundary regex) → обычная обработка, НЕ SKIP-НП. RU уже корректный русский — **LIVE-магазин Horoshop**, genuine RU-тело перезаписывать НЕЛЬЗЯ без явного go-ahead Yana + safe mode → Назв.мод (RU) и Описание (RU) НЕ трогаем (ячейки chunk-028-fixed без изменений). genuine RU тело/название faithful: тело 1083 UA → 1091 RU (genuine отдельный перевод). LIVE Lat-`p` Horoshop artefact ТОЛЬКО в RU body `pаспашная`; **UA body src-typo `Хладогент` desync vs RU correct `Хладагент`** (LIVE поставщик забыл выровнять UA-typo при переводе UA→RU — артефакт UA-стороны, blknochg preserve verbatim, НЕ нормализуем UA); UA body содержит HTML apostrophe entity `&#39;`; **nm_ru EXTRA-суффикс `снято с производства`** (в `nm_ua` нет — LIVE Horoshop статус model discontinuation authored RU-only extra, blknochg НЕ переписываем — это marketing-flag не перевод-десинк) — артефакты источника 1:1, genuine RU зеркалится источником verbatim (blknochg — НЕ переписываем, формат НЕ диффаем). Код `Tefcold UFSC370G Black` идентичен UA↔RU; nm_ru title включает extra `снято с производства` (LIVE marketing-flag) — Horoshop поставщик добавил статус только в RU title → customer-facing рассинхрона названия НЕТ → НЕ нумеровано. META always faithful (META UA!=RU genuine). Открытых вопросов 0.)*

*(scoped к row Артикул=1774252015)*

---

## SKU 5/61 — Морозильный шкаф Tefcold NF2500G (Артикул 1775858995) — RU корректен; правок нет (LIVE Horoshop genuine RU)

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg: `desc UA==RU` **False** (в RU-описании отдельный корректный русский перевод поставщика, НЕ укр. копия); `nm_ru`==`nazv_ru` `Морозильный шкаф Tefcold NF2500G` (чистый рус., char-level UA-leak і/ї/є/ґ НЕТ), `nm_ru`!=`nm_ua` (UA word-leak в `nm_ua` `Морозильна шафа` vs RU `Морозильный шкаф` — каноник). **Tefcold НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring; substring `cold` в `Tefcold` ≠ standalone бренд `COLD` — bnd-SET sравнение word-boundary regex) → обычная обработка, НЕ SKIP-НП. RU уже корректный русский — **LIVE-магазин Horoshop**, genuine RU-тело перезаписывать НЕЛЬЗЯ без явного go-ahead Yana + safe mode → Назв.мод (RU) и Описание (RU) НЕ трогаем (ячейки chunk-028-fixed без изменений). genuine RU тело/название faithful: тело 1332 UA → 1268 RU (genuine отдельный перевод). NO Lat-`p` artefact (SKU 5/6 single-glass-door NF2500G другая модель — Horoshop не пробросил Lat-p); UA body содержит HTML apostrophe entity `&#39;`; **BOTH-locale src-typo: UA `об&#39;єм`→`б&#39;єм` (пропущена `о` префикс) И RU `объём`→`бьем` (пропущена `о` + апостроф/ё drop)** — оба поставщик-typo LIVE preserve verbatim (blknochg, НЕ нормализуем; не блокируем — это source artefact в обоих локалях); RU body `Хладагент` correct — артефакты источника 1:1, genuine RU зеркалится источником verbatim (blknochg — НЕ переписываем, формат НЕ диффаем). Код `Tefcold NF2500G` идентичен UA↔RU genuine в названии → customer-facing рассинхрона названия НЕТ → НЕ нумеровано. META always faithful (META UA!=RU genuine). Открытых вопросов 0.)*

*(scoped к row Артикул=1775858995)*

---

## SKU 6/61 — Морозильный шкаф Tefcold NF2500G RAL7024 (Артикул 1775900559) — RU корректен; правок нет (LIVE Horoshop genuine RU)

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg: `desc UA==RU` **False** (в RU-описании отдельный корректный русский перевод поставщика, НЕ укр. копия); `nm_ru`==`nazv_ru` `Морозильный шкаф Tefcold NF2500G RAL7024` (чистый рус., char-level UA-leak і/ї/є/ґ НЕТ), `nm_ru`!=`nm_ua` (UA word-leak в `nm_ua` `Морозильна шафа` vs RU `Морозильный шкаф` — каноник). **Tefcold НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring; substring `cold` в `Tefcold` ≠ standalone бренд `COLD` — bnd-SET sравнение word-boundary regex) → обычная обработка, НЕ SKIP-НП. RU уже корректный русский — **LIVE-магазин Horoshop**, genuine RU-тело перезаписывать НЕЛЬЗЯ без явного go-ahead Yana + safe mode → Назв.мод (RU) и Описание (RU) НЕ трогаем (ячейки chunk-028-fixed без изменений). genuine RU тело/название faithful: тело 1384 UA → 1317 RU (genuine отдельный перевод). NO Lat-`p` artefact (mirror SKU 5 NF2500G модель + RAL7024 color suffix). **BOTH-locale src-typo `б&#39;єм`/`бьем` mirror SKU 5** (поставщик-typo обоих локалях LIVE preserve verbatim); RU body `Хладагент` correct — артефакты источника 1:1, genuine RU зеркалится источником verbatim (blknochg — НЕ переписываем, формат НЕ диффаем). Код `Tefcold NF2500G RAL7024` идентичен UA↔RU; RAL7024 цвет-индекс RAL палитры (графит) — store-canonical model variant → customer-facing рассинхрона названия НЕТ → НЕ нумеровано. META always faithful (META UA!=RU genuine). Открытых вопросов 0.)*

*(scoped к row Артикул=1775900559)*

---

## SKU 7/61 — Морозильный шкаф Tefcold UFFS370SD (Артикул 1836014743) — RU корректен; правок нет (LIVE Horoshop genuine RU)

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg: `desc UA==RU` **False** (в RU-описании отдельный корректный русский перевод поставщика, НЕ укр. копия); `nm_ru`==`nazv_ru` `Морозильный шкаф Tefcold UFFS370SD` (чистый рус., char-level UA-leak і/ї/є/ґ НЕТ), `nm_ru`!=`nm_ua` (UA word-leak в `nm_ua` `Морозильна шафа` vs RU `Морозильный шкаф` — каноник). **Tefcold НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring; substring `cold` в `Tefcold` ≠ standalone бренд `COLD` — bnd-SET sравнение word-boundary regex) → обычная обработка, НЕ SKIP-НП. RU уже корректный русский — **LIVE-магазин Horoshop**, genuine RU-тело перезаписывать НЕЛЬЗЯ без явного go-ahead Yana + safe mode → Назв.мод (RU) и Описание (RU) НЕ трогаем (ячейки chunk-028-fixed без изменений). genuine RU тело/название faithful: тело 1094 UA → 1083 RU (genuine отдельный перевод). LIVE Lat-`p` Horoshop artefact ТОЛЬКО в RU body `pаспашная` (UA body содержит корректное `розпашні` Cyr р — desync per-SKU); UA body содержит HTML apostrophe entity `&#39;` для `об&#39;єм`; RU body `Хладагент` correct — артефакты источника 1:1, genuine RU зеркалится источником verbatim (blknochg — НЕ переписываем, формат НЕ диффаем). Код `Tefcold UFFS370SD` идентичен UA↔RU genuine в названии → customer-facing рассинхрона названия НЕТ → НЕ нумеровано. META always faithful (META UA!=RU genuine). Открытых вопросов 0.)*

*(scoped к row Артикул=1836014743)*

---

## SKU 8/61 — Морозильный шкаф Gooder SF400 (Артикул 2048289117) — RU корректен; правок нет (LIVE Horoshop genuine RU)

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg: `desc UA==RU` **False** (в RU-описании отдельный корректный русский перевод поставщика, НЕ укр. копия); `nm_ru`==`nazv_ru` `Морозильный шкаф Gooder SF400` (чистый рус., char-level UA-leak і/ї/є/ґ НЕТ), `nm_ru`!=`nm_ua` (UA word-leak в `nm_ua` `Морозильна шафа` vs RU `Морозильный шкаф` — каноник). **Gooder НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. RU уже корректный русский — **LIVE-магазин Horoshop**, genuine RU-тело перезаписывать НЕЛЬЗЯ без явного go-ahead Yana + safe mode → Назв.мод (RU) и Описание (RU) НЕ трогаем (ячейки chunk-028-fixed без изменений). genuine RU тело/название faithful: тело 849 UA → 837 RU (genuine отдельный перевод). NO Lat-`p` artefact (Gooder SF400 модель, не Tefcold); NO apos entity; **BOTH-locale src-typo `Хлодоген: R290`** (вместо `Хладагент`) — поставщик-typo LIVE preserve verbatim в обоих локалях UA+RU (blknochg НЕ нормализуем; источник artefact обеих сторон) — артефакты источника 1:1, genuine RU зеркалится источником verbatim (blknochg — НЕ переписываем, формат НЕ диффаем). Код `Gooder SF400` идентичен UA↔RU genuine в названии → customer-facing рассинхрона названия НЕТ → НЕ нумеровано. META always faithful (META UA!=RU genuine). Открытых вопросов 0.)*

**Наблюдения по батчу SKU 1-8 (8/61) — chunk-028 (раздел `Холодильне та морозильне обладнання/Шафи морозильні` — продолжение/повтор chunk-027 раздела `Морозильні шафи` с инвертированным порядком слов в названии раздела):** **blk триплет 0. blkv 0. blknotrip 0. blknochgeq 0. blknochg 8 (ВСЕ). SKIP-НП 0.** Бренды b1: Tefcold ×7 (SKU 1-7) + Gooder ×1 (SKU 8). **Tefcold НЕ ∈ НП-эксклюзив** (substring `cold` в `Tefcold` ≠ standalone бренд `COLD` — сравнение word-boundary regex по бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}); **Gooder НЕ ∈ НП-эксклюзив** (нет в списке вообще). All 8 SKU `desc UA==RU` **False** (RU отдельный корректный русский перевод поставщика LIVE-магазин Horoshop, НЕ укр. копия), `nm_ru`==`nazv_ru` чистый рус. (UA-leak і/ї/є/ґ НЕТ), `nm_ru`!=`nm_ua` (UA name `Морозильна шафа` vs RU `Морозильный шкаф` — каноник). LIVE source artefacts preserve verbatim (blknochg, НЕ нормализуем): (1) Lat-`p` Horoshop artefact `p` U+0070 + Cyr остаток в `pаспашная`/`pозпашна` — SKU 1 в обоих локалях, SKU 2/3/4/7 только в RU (desync per-SKU). (2) Src-typo UA-сторона `Хладогент` vs RU correct `Хладагент` SKU 4 (поставщик не выровнял). (3) BOTH-locale src-typo `б&#39;єм`/`бьем` (пропущена `о` префикс) SKU 5 + mirror SKU 6 RAL7024 — поставщик-typo обоих локалях preserve verbatim. (4) BOTH-locale src-typo `Хлодоген: R290` SKU 8 Gooder (вместо `Хладагент`) — поставщик-typo обоих локалях. (5) UA HTML apostrophe entity `&#39;` SKU 3/4/5/6/7 — UA литеральная apos-entity LIVE. (6) nm_ru EXTRA-суффикс `снято с производства` SKU 4 (в nm_ua нет — LIVE Horoshop marketing-flag model discontinuation authored RU-only extra). (7) nm UA/RU temp-range pair desync SKU 1: UA `(-18°...-22 °C, нерж.)` Lat C space-before-°C vs RU `(-18°...-22°С, нерж.)` Cyr С no-space — LIVE Horoshop nazv title artefact (РАЗНЫЕ форматы между UA/RU, preserve verbatim, НЕ unify). genuine RU-тело перезаписывать НЕЛЬЗЯ без явного go-ahead Yana + safe mode → ячейки chunk-028-fixed без изменений (xlsx блокирован, blknochg-only batch). META always faithful (META UA!=RU genuine — артефакты источника 1:1). **SKIP-НП = 0** в b1 (Tefcold/Gooder — ни один НЕ ∈ НП-эксклюзив; первый Tatra SKU 14 будет b2 SKIP-НП). Открытых вопросов по батчу: **0** (ledger chunk-028 стартует с 0; b1 ничего не добавляет — все artefacts источника LIVE preserve verbatim, blknochg НЕ нормализуем; ни одного customer-facing UA↔genuine-RU рассинхрона названия и ни одного body↔name code/article desync; src-typo `Хладогент`/`б&#39;єм`/`бьем`/`Хлодоген` precedent chunk-027 (Cyr В+М glitch, `мороженного` double-н typo) — source artefact LIVE НЕ нормализуем; questions.md chunk-028 НЕ создаём пока, плейсхолдер MR достаточен). Кумулятивно по chunk-028: **0** (ledger стартует с 0). Кумулятивно SKIP-НП chunk-028 = **0** (b1 0). NEXT: chunk-028 b2 SKU 9-16.

*(scoped к row Артикул=2048289117)*

---
