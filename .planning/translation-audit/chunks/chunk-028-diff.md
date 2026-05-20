# chunk-028 translation diff (61 SKU — холодильное оборудование, продолжение chunk-027)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-028 (61 SKU, продолжение chunk-027)
**Apply key:** `Артикул` (scoped per row)
**Status:** IN PROGRESS 16/61

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

## SKU 9/61 — Морозильный шкаф Gooder SF600 (Артикул 2048291019) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg — `desc UA==RU` **False** (genuine отдельный корректный русский перевод поставщика, НЕ укр. копия); `nm_ua`!=`nm_ru` (UA `Морозильна шафа Gooder SF600` vs RU `Морозильный шкаф Gooder SF600`); `nm_ru`==`nazv_ru` clean RU `Морозильный шкаф Gooder SF600` (char-level UA_ONLY=∅). **Gooder НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. LIVE-магазин Horoshop, genuine RU body НЕ переписываем (ячейки chunk-028-fixed без изменений). genuine RU body faithful: 1p opening + ul + li блок-структура; `Морозильный шкаф Gooder SF600 работает в температурном режиме от -18&deg;С до -22&deg;С` (`&deg;С` HTML entity + Cyr С — UA↔RU обе локали используют entity-форму, format-симметрия для SKU 9); общий `об'ём` apostrophe drop в Horoshop genuine RU; bullets с UA-ярлыками `Вага`/`Об'єм` присутствуют в UA-стороне (партнёрский фид смешанный) — в RU корректно `Вес`/`Объём`. blknochg — НЕ переписываем, формат НЕ диффаем. Код `Gooder SF600` Lat → consistent UA↔RU body. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=2048291019)*

---

## SKU 10/61 — Морозильный шкаф Snaige CF27SM-T1000FQ (Артикул 2050356102) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg — `desc UA==RU` **False** (genuine отдельный корректный русский перевод поставщика, НЕ укр. копия); `nm_ua`!=`nm_ru` (UA `Морозильна шафа Snaige CF27SM-T1000FQ` vs RU `Морозильный шкаф Snaige CF27SM-T1000FQ`); `nm_ru`==`nazv_ru` clean RU `Морозильный шкаф Snaige CF27SM-T1000FQ` (char-level UA_ONLY=∅). **Snaige НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. LIVE-магазин Horoshop, genuine RU body НЕ переписываем (ячейки chunk-028-fixed без изменений). LIVE source artefacts preserve verbatim (blknochg → НЕ нормализуем): (1) UA-сторона `du` открывается русским абзацем (`<p>Морозильный шкаф SNAIGE CF27SM-T1000FQ работает в температурном режиме от -16&deg;С до -44&deg;С...`) — партнёрский фид Snaige склеил RU-prose в UA-сторону, затем UA bullets (`Вага: 55 кг`); RU-сторона `dr` чисто русская throughout (`Вес: 55 кг`); (2) брендовая капитализация UA-вступления `SNAIGE` allcaps vs RU `Snaige` titlecase (SKU 10 specific — per-SKU artefact в UA-стороне); (3) UA `С&deg;` postfix typo (Cyrillic С перед `&deg;`, ожид. `&deg;С` префикс) в UA-фрагменте `+43 С&deg;`; (4) format desync `&deg;`-entity в UA (3×) vs raw `°`-литерал в RU (3×) — Snaige supplier-side desync; (5) UA содержит `об&#39;єм` apos entity (HTML), в RU чисто `объём`. blknochg → ВСЕ артефакты `du` (UA-side) НЕ трогаем; `dr` уже корректный RU. Код `Snaige CF27SM-T1000FQ` Lat → consistent. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=2050356102)*

---

## SKU 11/61 — Морозильный шкаф Snaige CF27SM-T1CB0FQ (Артикул 2050373728) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg — `desc UA==RU` **False** (genuine отдельный русский перевод поставщика); `nm_ua`!=`nm_ru` (UA `Морозильна шафа Snaige CF27SM-T1CB0FQ` vs RU `Морозильный шкаф Snaige CF27SM-T1CB0FQ`); `nm_ru`==`nazv_ru` clean RU. **Snaige НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. LIVE-магазин Horoshop genuine — НЕ переписываем. LIVE artefacts preserve verbatim: (1) UA-сторона `du` открывается RU-prose без брендового префикса `<p>Морозильный шкаф CF27SM-T1CB0FQ работает...` (SKU 11 specific — brand-prefix dropped в UA-вступлении, в RU-стороне `dr` brand также отсутствует — symmetric для этого SKU); (2) UA-bullets `Вага`/`Вага в упаковці` после RU-prose (mixed bilingual UA-side genuine); (3) format desync `&deg;`-entity в UA (3×) vs raw `°`-литерал в RU (3×) Snaige supplier pattern. RU-сторона `dr` чисто русская throughout. blknochg → НЕ переписываем. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=2050373728)*

---

## SKU 12/61 — Морозильный шкаф Snaige CF27SM-T1EP0F (Артикул 2050411507) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg — `desc UA==RU` **False** (genuine отдельный русский перевод поставщика); `nm_ua`!=`nm_ru` (UA `Морозильна шафа Snaige CF27SM-T1EP0F` vs RU `Морозильный шкаф Snaige CF27SM-T1EP0F`); `nm_ru`==`nazv_ru` clean RU. **Snaige НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. LIVE-магазин Horoshop genuine — НЕ переписываем. LIVE artefacts preserve verbatim: (1) UA-сторона `du` открывается RU-prose с `Snaige` titlecase `<p>Морозильный шкаф Snaige CF27SM-T1EP0F работает...` (SKU 12 specific — brand titlecase в UA-вступлении, vs SKU 10 SNAIGE allcaps + SKU 11 brand-drop — per-SKU desync капитализации внутри одной Snaige-серии Horoshop genuine); (2) UA-bullets после RU-prose mixed bilingual; (3) UA `С&deg;` postfix typo `+43 С&deg;` (Cyrillic С перед `&deg;`, ожид. `&deg;С`-префикс); (4) format desync `&deg;`-entity в UA (3×) vs raw `°`-литерал в RU (3×); (5) UA `об&#39;єм` apos entity. RU-сторона `dr` чисто русская throughout. blknochg → НЕ переписываем. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=2050411507)*

---

## SKU 13/61 — Морозильный шкаф Gooder GN-1410BT (Артикул 2048279085) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg — `desc UA==RU` **False** (genuine отдельный русский перевод поставщика, НЕ укр. копия); `nm_ua`!=`nm_ru` (UA `Морозильна шафа Gooder GN-1410BT` vs RU `Морозильный шкаф Gooder GN-1410BT`); `nm_ru`==`nazv_ru` clean RU. **Gooder НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. LIVE-магазин Horoshop genuine — НЕ переписываем. genuine RU body faithful: UA-сторона `du` нормальный Ukrainian opening (`<p>Морозильна шафа Gooder GN-1410BT працює в температурному режимі...` — НЕ Snaige-mixed-prose pattern; SKU 13 Gooder идёт обычной ua/ru симметрией opening prose); LIVE source artefacts: (1) UA `+16 до +30 С` без `&deg;` symbol — partial format (only Cyr С, no degree mark); (2) UA `Загальний об&#39;єм` apos entity; (3) UA↔RU обе локали используют `&deg;С` entity-форму в температурном режиме (формат-симметрия для SKU 13, vs Snaige 10-12 desync). RU-сторона `dr` чисто русская. blknochg → НЕ переписываем. Код `Gooder GN-1410BT` Lat → consistent. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=2048279085)*

---

## SKU 14/61 — Морозильный шкаф TATRA TRC1400BT (Артикул 2062029823) — SKIP-НП (бренд НП-эксклюзив, тело из фида НП позже)

**Бренд:** Tatra (НП-эксклюзивный — forward-only SKIP-правило)
**Поле:** Название модификации (RU)
**Было:** (ячейка не трогается — тело из фида НП позже)
**Стало:** не трогаем (SKIP-НП — тело из фида НП позже)

**Поле:** Описание товара (RU)
**Было:** (ячейка не трогается — тело из фида НП позже)
**Стало:** не трогаем (SKIP-НП — тело из фида НП позже)

*(SKIP-НП — `brand`=`Tatra` ∈ {TATRA/Татра} word-boundary NP-hit → forward-only SKIP-правило: тело из фида НП позже, ячейки chunk-028-fixed.xlsx НЕ трогаем (Назв.мод RU + Описание RU без изменений). **Tatra ∈ НП-эксклюзивный список** (word-boundary NP-hit найден в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}) → forward-only SKIP-правило: тело из фида НП позже, ячейки chunk-028-fixed.xlsx не трогаем (Назв.мод RU + Описание RU без изменений). **ПЕРВЫЙ SKIP-НП в chunk-028** (precedent — chunk-022/023/024+ TATRA/FAGOR/HURAKAN/APACH). Source signature `du==dr` True + `nm_ua==nm_ru` UA word `Морозильна шафа TATRA TRC1400BT` (UA-leak); `nazv_ru` clean RU `Морозильный шкаф TATRA TRC1400BT` — desync vs nm cells. В SKIP-НП cells **НЕ правим** (тело из фида НП позже всё перепишет). Кумул. SKIP-НП chunk-028 = 1 (после SKU 14). META always faithful. Открытых вопросов 0 в этом SKU — стандартный SKIP-НП паттерн.)*

*(scoped к row Артикул=2062029823)*

---

## SKU 15/61 — Стол морозильный Apach AFM 02 BT (Артикул 527344073) — SKIP-НП (бренд НП-эксклюзив, тело из фида НП позже)

**Бренд:** Apach (НП-эксклюзивный — forward-only SKIP-правило)
**Поле:** Название модификации (RU)
**Было:** (ячейка не трогается — тело из фида НП позже)
**Стало:** не трогаем (SKIP-НП — тело из фида НП позже)

**Поле:** Описание товара (RU)
**Было:** (ячейка не трогается — тело из фида НП позже)
**Стало:** не трогаем (SKIP-НП — тело из фида НП позже)

*(SKIP-НП — `brand`=`Apach` ∈ {APACH/Апач} word-boundary NP-hit → forward-only SKIP-правило: тело из фида НП позже, ячейки chunk-028-fixed.xlsx НЕ трогаем. **Apach ∈ НП-эксклюзивный список** (word-boundary NP-hit найден в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}) → forward-only SKIP-правило: тело из фида НП позже, ячейки chunk-028-fixed.xlsx не трогаем (Назв.мод RU + Описание RU без изменений). **ВТОРОЙ SKIP-НП в chunk-028** (после SKU 14 Tatra). Section transition: SKU 15 открывает новый раздел `Холодильне та морозильне обладнання/Морозильні столи` (Стіл морозильний) — SKU 1-14 шли разделом `Шафи морозильні`. Source signature `du!=dr`, `nm_ua!=nm_ru` (UA `Стіл морозильний Apach AFM 02 BT` vs RU `Стол морозильный Apach AFM 02 BT`); `nm_ru==nazv_ru` clean RU — но brand=Apach NP-hit → SKIP-НП **независимо** от состояния ячеек (правило forward-only по brand-membership, не по signature). Кумул. SKIP-НП chunk-028 = 2 (после SKU 15). META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=527344073)*

---

## SKU 16/61 — Стол морозильный Apach AFM 03 BT (Артикул 527347411) — SKIP-НП (бренд НП-эксклюзив, тело из фида НП позже)

**Бренд:** Apach (НП-эксклюзивный — forward-only SKIP-правило)
**Поле:** Название модификации (RU)
**Было:** (ячейка не трогается — тело из фида НП позже)
**Стало:** не трогаем (SKIP-НП — тело из фида НП позже)

**Поле:** Описание товара (RU)
**Было:** (ячейка не трогается — тело из фида НП позже)
**Стало:** не трогаем (SKIP-НП — тело из фида НП позже)

*(SKIP-НП — `brand`=`Apach` ∈ {APACH/Апач} word-boundary NP-hit → forward-only SKIP-правило: тело из фида НП позже, ячейки chunk-028-fixed.xlsx НЕ трогаем. **Apach ∈ НП-эксклюзивный список** (word-boundary NP-hit найден в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}) → forward-only SKIP-правило: тело из фида НП позже, ячейки chunk-028-fixed.xlsx не трогаем (Назв.мод RU + Описание RU без изменений). **ТРЕТИЙ SKIP-НП в chunk-028** (mirror SKU 15 — same brand Apach, следующая модель AFM 03 BT в разделе `Морозильні столи`). Source signature `du!=dr`, `nm_ua!=nm_ru` (UA `Стіл морозильний Apach AFM 03 BT` vs RU `Стол морозильный Apach AFM 03 BT`); `nm_ru==nazv_ru` clean RU — SKIP-НП **независимо** (brand-membership rule). Кумул. SKIP-НП chunk-028 = 3 (после SKU 16). META always faithful. Открытых вопросов 0.)*

**Наблюдения по батчу SKU 9-16 (16/61) — chunk-028 (батч-морозильные шкафы Gooder ×2 / Snaige ×3 + Tatra ×1 (SKIP-НП) + section transition к `Морозильні столи` с Apach ×2 (SKIP-НП); продолжение раздела `Холодильне та морозильне обладнання/Шафи морозильні` для SKU 9-14, новый раздел `Холодильне та морозильне обладнання/Морозильні столи` для SKU 15-16):** **blk триплет 0. blknotrip 0. blkv 0. blknochg 5 (SKU 9 Gooder SF600 + SKU 10/11/12 Snaige CF27SM-T1000FQ/T1CB0FQ/T1EP0F + SKU 13 Gooder GN-1410BT — LIVE Horoshop genuine RU). blknochgeq 0. SKIP-НП 3 (SKU 14 Tatra TRC1400BT — ПЕРВЫЙ SKIP-НП в chunk-028; SKU 15 Apach AFM 02 BT + SKU 16 Apach AFM 03 BT — раздел `Морозильні столи`).** SKU 9 `2048291019` Gooder SF600 — **blknochg** LIVE Horoshop (1p opening + ul + li блок; `&deg;С` HTML entity + Cyr С UA↔RU симметрично; partner-feed mixed bilingual UA-bullets с UA-ярлыками `Вага`/`Об'єм`). Gooder **НЕ ∈ НП-эксклюзив**. SKU 10 `2050356102` Snaige CF27SM-T1000FQ — **blknochg** LIVE (UA-сторона `du` открывается RU-prose `<p>Морозильный шкаф SNAIGE...` allcaps брендa + UA-bullets `Вага: 55 кг`; `С&deg;` postfix typo `+43 С&deg;`; format desync UA `&deg;` (3×) vs RU raw `°` (3×); UA `об&#39;єм` apos entity). Snaige **НЕ ∈ НП-эксклюзив**. SKU 11 `2050373728` Snaige CF27SM-T1CB0FQ — **blknochg** LIVE (UA `du` RU-prose без брендового префикса `<p>Морозильный шкаф CF27SM-T1CB0FQ работает...`; format desync UA `&deg;` (3×) vs RU raw `°` (3×) Snaige supplier pattern). Snaige **НЕ ∈ НП-эксклюзив**. SKU 12 `2050411507` Snaige CF27SM-T1EP0F — **blknochg** LIVE (UA `du` RU-prose с `Snaige` titlecase `<p>Морозильный шкаф Snaige CF27SM-T1EP0F`; per-SKU desync капитализации внутри одной Snaige-серии Horoshop: SKU 10 SNAIGE allcaps / SKU 11 brand-drop / SKU 12 Snaige titlecase — genuine artefact; UA `С&deg;` postfix typo; format desync UA `&deg;` vs RU raw `°`). Snaige **НЕ ∈ НП-эксклюзив**. SKU 13 `2048279085` Gooder GN-1410BT — **blknochg** LIVE (UA `du` нормальный Ukrainian opening `<p>Морозильна шафа Gooder GN-1410BT працює в температурному режимі...` — НЕ Snaige-mixed-prose pattern; UA-format `+30 С` без `&deg;` symbol partial; UA `об&#39;єм` apos entity; UA↔RU обе локали используют `&deg;С` entity-форму температурном режиме — формат-симметрия). Gooder **НЕ ∈ НП-эксклюзив**. SKU 14 `2062029823` Tatra TRC1400BT — **SKIP-НП** (brand=`Tatra` ∈ {TATRA/Татра} word-boundary NP-hit; cells unchanged). **ПЕРВЫЙ SKIP-НП в chunk-028**. Source signature `du==dr` True + `nm_ua==nm_ru` UA word `Морозильна шафа TATRA TRC1400BT` (UA-leak) vs `nazv_ru` clean RU — desync в SKIP-НП cells **НЕ правим** (тело из фида НП позже всё перепишет). SKU 15 `527344073` Apach AFM 02 BT — **SKIP-НП** (brand=`Apach` ∈ {APACH/Апач} NP-hit; cells unchanged). **ВТОРОЙ SKIP-НП в chunk-028**. **Section transition внутри батча**: SKU 15 открывает новый раздел `Холодильне та морозильне обладнання/Морозильні столи` (Стіл морозильний UA) — SKU 1-14 шли разделом `Шафи морозильні`. SKU 16 `527347411` Apach AFM 03 BT — **SKIP-НП** (mirror SKU 15, same brand). **ТРЕТИЙ SKIP-НП в chunk-028**. **Открытых вопросов по батчу: 0** (b1 0 + b2 0; ledger chunk-028 = 0). Кумулятивно chunk-028 = **0** (questions.md chunk-028 пока НЕ создаём — нет OQ). Кумулятивно SKIP-НП chunk-028 = **3** (b1 0 + b2 3). NEXT: chunk-028 b3 SKU 17-24.

*(scoped к row Артикул=527347411)*

---
