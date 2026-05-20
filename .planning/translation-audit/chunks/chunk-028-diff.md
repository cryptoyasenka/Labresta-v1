# chunk-028 translation diff (61 SKU — холодильное оборудование, продолжение chunk-027)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-028 (61 SKU, продолжение chunk-027)
**Apply key:** `Артикул` (scoped per row)
**Status:** IN PROGRESS 56/61

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

## SKU 17/61 — Стол морозильный Apach AFM 04 BT четырехдверный (Артикул 595397992) — SKIP-НП (бренд НП-эксклюзив, тело из фида НП позже)

**Бренд:** Apach (НП-эксклюзивный — forward-only SKIP-правило)
**Поле:** Название модификации (RU)
**Было:** (ячейка не трогается — тело из фида НП позже)
**Стало:** не трогаем (SKIP-НП — тело из фида НП позже)

**Поле:** Описание товара (RU)
**Было:** (ячейка не трогается — тело из фида НП позже)
**Стало:** не трогаем (SKIP-НП — тело из фида НП позже)

*(SKIP-НП — `brand`=`Apach` ∈ {APACH/Апач} word-boundary NP-hit → forward-only SKIP-правило: тело из фида НП позже, ячейки chunk-028-fixed.xlsx НЕ трогаем (Назв.мод RU + Описание RU без изменений). **Apach ∈ НП-эксклюзивный список** (word-boundary NP-hit найден в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}) → forward-only SKIP-правило: тело из фида НП позже, ячейки chunk-028-fixed.xlsx не трогаем (Назв.мод RU + Описание RU без изменений). **ЧЕТВЁРТЫЙ SKIP-НП в chunk-028** (после SKU 14 Tatra + SKU 15/16 Apach в b2; SKU 17 продолжает Apach-серию AFM 02→03→04 BT в разделе `Морозильні столи`). Source signature `du!=dr` False (du!=dr genuine разный), `nm_ua!=nm_ru` (UA `Стіл морозильний Apach AFM 04 BT чотиридверний` vs RU `Стол морозильный Apach AFM 04 BT четырехдверный`); `nm_ru==nazv_ru` clean RU — но brand=Apach NP-hit → SKIP-НП **независимо** от состояния ячеек (правило forward-only по brand-membership, не по signature). Кумул. SKIP-НП chunk-028 = 4 (после SKU 17). META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=595397992)*

---

## SKU 18/61 — Стол морозильный TATRA TRC02BT (Артикул 2062025984) — SKIP-НП (бренд НП-эксклюзив, тело из фида НП позже)

**Бренд:** Tatra (НП-эксклюзивный — forward-only SKIP-правило)
**Поле:** Название модификации (RU)
**Было:** (ячейка не трогается — тело из фида НП позже)
**Стало:** не трогаем (SKIP-НП — тело из фида НП позже)

**Поле:** Описание товара (RU)
**Было:** (ячейка не трогается — тело из фида НП позже)
**Стало:** не трогаем (SKIP-НП — тело из фида НП позже)

*(SKIP-НП — `brand`=`Tatra` ∈ {TATRA/Татра} word-boundary NP-hit → forward-only SKIP-правило: тело из фида НП позже, ячейки chunk-028-fixed.xlsx НЕ трогаем. **Tatra ∈ НП-эксклюзивный список** (word-boundary NP-hit найден в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}) → forward-only SKIP-правило: тело из фида НП позже, ячейки chunk-028-fixed.xlsx не трогаем (Назв.мод RU + Описание RU без изменений). **ПЯТЫЙ SKIP-НП в chunk-028** (вторая Tatra-серия — TRC02BT после TRC1400BT b2; раздел `Морозильні столи`). Source signature **`du==dr` True** + `nm_ua==nm_ru` UA word `Стіл морозильний TATRA TRC02BT` (UA-leak); `nazv_ru` clean RU `Стол морозильный TATRA TRC02BT` — desync vs nm cells (precedent SKU 14 Tatra TRC1400BT b2 — тот же паттерн). В SKIP-НП cells **НЕ правим** (тело из фида НП позже всё перепишет). Кумул. SKIP-НП chunk-028 = 5 (после SKU 18). META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=2062025984)*

---

## SKU 19/61 — Стол морозильный TATRA TRC03BT (Артикул 2062029113) — SKIP-НП (бренд НП-эксклюзив, тело из фида НП позже)

**Бренд:** Tatra (НП-эксклюзивный — forward-only SKIP-правило)
**Поле:** Название модификации (RU)
**Было:** (ячейка не трогается — тело из фида НП позже)
**Стало:** не трогаем (SKIP-НП — тело из фида НП позже)

**Поле:** Описание товара (RU)
**Было:** (ячейка не трогается — тело из фида НП позже)
**Стало:** не трогаем (SKIP-НП — тело из фида НП позже)

*(SKIP-НП — `brand`=`Tatra` ∈ {TATRA/Татра} word-boundary NP-hit → forward-only SKIP-правило: тело из фида НП позже, ячейки chunk-028-fixed.xlsx НЕ трогаем. **Tatra ∈ НП-эксклюзивный список** (word-boundary NP-hit найден в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}) → forward-only SKIP-правило: тело из фида НП позже, ячейки chunk-028-fixed.xlsx не трогаем (Назв.мод RU + Описание RU без изменений). **ШЕСТОЙ SKIP-НП в chunk-028** (mirror SKU 18, same brand Tatra, следующая модель TRC03BT в разделе `Морозильні столи`). Source signature **`du==dr` True** + `nm_ua==nm_ru` UA word `Стіл морозильний TATRA TRC03BT` (UA-leak); `nazv_ru` clean RU — same desync pattern как SKU 18 + SKU 14. В SKIP-НП cells **НЕ правим**. Кумул. SKIP-НП chunk-028 = 6 (после SKU 19). META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=2062029113)*

---

## SKU 20/61 — Морозильный стол FROSTY SNACK 2100BT (ширина 600 мм) (Артикул 508918198) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg — `desc UA==RU` **False** (genuine отдельный корректный русский перевод поставщика, НЕ укр. копия); `nm_ua`!=`nm_ru` (UA `Морозильний стіл FROSTY SNACK 2100BT (ширина 600 мм)` vs RU `Морозильный стол FROSTY SNACK 2100BT (ширина 600 мм)`); `nm_ru`==`nazv_ru` clean RU (char-level UA_ONLY=∅). **FROSTY НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. LIVE-магазин Horoshop, genuine RU body НЕ переписываем (ячейки chunk-028-fixed без изменений). LIVE source artefacts preserve verbatim (blknochg → НЕ нормализуем): (1) supplier RU dr uses hyphen `-` separators вместо em-dash UA `—` (`Ширина стола - 600 мм` RU vs UA `Ширина стола — 600 мм`) — desync supplier-side, в RU genuine; (2) RU dr `&deg;С` entity Cyr С (`+43&deg;С`) vs UA du `°C` Lat C raw literal (`+43 °C`) — format desync supplier-side; (3) RU `-18&deg; C....-22&deg; C` (Lat C, no &deg;С after 22) vs UA `-18° C....-22 °C` (Lat C, mix); (4) RU `объем (л)` без ё literal vs UA `об'єм (л)` straight-apos; (5) dims `1360x600x860` UA Lat x no мм identical to RU genuine — supplier consistent; (6) `полки-решетки` без ё в RU genuine vs UA `полиці-решітки`. blknochg → ВСЕ артефакты `dr` (RU-side) НЕ трогаем; авторский перевод НЕ генерим. Код `FROSTY SNACK 2100BT` Lat → consistent. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=508918198)*

---

## SKU 21/61 — Стол морозильный Forcar GN3100BT (Артикул 508918203) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg — `desc UA==RU` **False** (genuine отдельный русский перевод поставщика); `nm_ua`!=`nm_ru` (UA `Стіл морозильний тридверний Forcar GN3100BT, Італія` vs RU `Стол морозильный Forcar GN3100BT`); `nm_ru`==`nazv_ru` clean RU (char-level UA_ONLY=∅). **Forcar НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. LIVE-магазин Horoshop genuine — НЕ переписываем. **SKU 21-specific desync**: UA-сторона `nm_ua`/`nazv_ua` содержит EXTRA-материал `тридверний` + `, Італія` (UA-вариант brand-origin + door-count description), которого нет в RU `nm_ru`/`nazv_ru` — supplier UA-side добавил extra qualifiers, RU-сторона осталась минимальной `Стол морозильный Forcar GN3100BT`. Это desync UA/RU cells supplier-side, blknochg → **НЕ правим** (RU minimal-name acceptable). LIVE artefacts dr verbatim: (1) hyphen `-` separators в RU genuine supplier (FROSTY/Forcar consistent pattern same template family — Italian supplier feed); (2) `&deg;С` entity Cyr С + Lat C mix format; (3) RU `Электронная панель управления, автоматическое размораживание и испарение талой воды` — full sentence supplier translated. Forcar дочерний к FROSTY supplier (same template family Italy). blknochg → НЕ переписываем. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=508918203)*

---

## SKU 22/61 — Морозильный стол FROSTY SNACK 3100BT (ширина 600 мм) (Артикул 616390857) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg — `desc UA==RU` **False** (genuine отдельный русский перевод поставщика); `nm_ua`!=`nm_ru` (UA `Морозильний стіл FROSTY SNACK 3100BT (ширина 600 мм)` vs RU `Морозильный стол FROSTY SNACK 3100BT (ширина 600 мм)`); `nm_ru`==`nazv_ru` clean RU. **FROSTY НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. LIVE-магазин Horoshop genuine — НЕ переписываем. **mirror SKU 20** (FROSTY SNACK same template, 3 doors vs 2, ширина 600мм, dims 1795x600x860): supplier RU dr consistent same pattern (hyphen separators, `&deg;С` Cyr entity, Lat C in temp range mix, `объем (л)` no-ё, `полки-решетки` no-ё, dims Lat x trailing no мм). RU-сторона `dr` чисто русская throughout. blknochg → НЕ переписываем. Код `FROSTY SNACK 3100BT` Lat → consistent. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=616390857)*

---

## SKU 23/61 — Стол морозильный FROSTY GN 2100BT (ширина 700 мм) (Артикул 976770291) — 🔴 RU=UA + Назв.мод (RU) UA-leak

**Поле:** Название модификации (RU)
**Было:** `Стіл морозильний FROSTY GN 2100BT (ширина 700 мм)`
**Стало:** `Стол морозильный FROSTY GN 2100BT (ширина 700 мм)`

**Поле:** Описание товара (RU)
**Было:** (полностью идентично UA — украинский текст)
**Стало:** (полный перевод RU тег-в-tag):

```
<p>Двухдверный морозильный стол без борта. Может использоваться в составе кухонной линии. Ширина стола — 700 мм. Максимальная t&deg; окружающей среды +43 &deg;C. </p> <p>Удобная регулировка ножек — телескопические опоры из нержавеющей стали.</p> <p>Регулируемые по высоте направляющие под полки стандарта GN1/1, в комплекте 2 полки-решётки.</p> <ul> <li>Столешница и корпус: нержавеющая сталь AISI 304</li> <li>Количество дверей: 2</li> <li>Температурный режим: -18&deg; C....-22 &deg;C</li> <li>Тип охлаждения: динамический</li> <li>Цифровой термостат</li> <li>Полезный объём (л): 282.</li> <li>Мощность: 0,65 кВт.</li> <li>Подключение к электросети: 220 В</li> <li>Габаритные размеры: 1360мм x 700мм x 860мм</li> </ul>
```

*(blk триплет STANDARD — `desc UA==RU` **True** (🔴 RU=UA — RU = полная укр. копия тела); `nm_ua`==`nm_ru` `Стіл морозильний FROSTY GN 2100BT (ширина 700 мм)` (UA-leak — body-level `_has_ua` True via `Стіл`/`морозильний`/`ширина`); `nm_ru`!=`nazv_ru` genuine RU `Стол морозильный FROSTY GN 2100BT (ширина 700 мм)` → AUTO Назв.мод (RU) = genuine `nazv_ru`. **ПЕРВЫЙ blk триплет в chunk-028** (раздел `Морозильні столи` — Стіл морозильний UA по структуре идентичен `Морозильний стіл` FROSTY SNACK 2100BT из SKU 20 blknochg, но **разные SKU**: SKU 20 ширина 600 мм + supplier RU дублированный, SKU 23 ширина 700 мм + RU=UA копия без supplier-side перевода — supplier дал UA-only тело без русского варианта, magazine скопировал UA в RU cell). **FROSTY НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. Описание (RU) — авторский полный перевод тег-в-tag (структура UA зеркалится 1:1; 3 `<p>` + 1 `<ul>` + 9 `<li>`, no `<img>`, no iframe, no voltage explicit). SOFT применено к авторскому RU: `Дводверний морозильний стіл без борту.`→`Двухдверный морозильный стол без борта.` (`-ий` UA → `-ый` RU; `борту` [без] genit. UA → `борта` [без] genit. RU); `Може використовуватися в складі кухонної лінії.`→`Может использоваться в составе кухонной линии.`; `Ширина стола — 700 мм.` em-dash preserve U+2014 (Policy A — em-dash unchanged); `Максимальна t° довкілля +43 °C.`→`Максимальная t&deg; окружающей среды +43 &deg;C.` (SOFT `°` U+00B0 → `&deg;` entity x2; Lat C preserve; trailing space inside `</p>` обёртки verbatim); `Зручне регулювання ніжок — телескопічні опори з неіржавкої сталі.`→`Удобная регулировка ножек — телескопические опоры из нержавеющей стали.`; `Регульовані за висотою напрямні під полиці стандарту GN1/1, у комплекті 2 полиці-решітки.`→`Регулируемые по высоте направляющие под полки стандарта GN1/1, в комплекте 2 полки-решётки.` (`решітки` UA → `решётки` RU с ё U+0451); `Стільниця та корпус: неіржавка сталь AISI 304`→`Столешница и корпус: нержавеющая сталь AISI 304`; `Кількість дверей: 2`→`Количество дверей: 2`; `Температурний режим: -18° C....-22 °C`→`Температурный режим: -18&deg; C....-22 &deg;C` (SOFT `°`→`&deg;`; Lat C verbatim; 4-точечное `....` preserve); `Тип охолодження: динамічний`→`Тип охлаждения: динамический`; `Цифровий термостат`→`Цифровой термостат`; `Корисний об'єм (л): 282.`→`Полезный объём (л): 282.` (drop straight-apos U+0027; ё U+0451); `Потужність: 0,65 кВт.`→`Мощность: 0,65 кВт.` (decimal comma faithful); `Під'єднання до електромережі: 220 В`→`Подключение к электросети: 220 В` (drop apos; Cyr В U+0412 + space faithful); `Габаритні розміри: 1360x700x860`→`Габаритные размеры: 1360мм x 700мм x 860мм` (Policy B/C — UA Lat x already, `мм` слитно per axis + Lat x separator; chunk-027 SKU 40 REEDNEE GN1410BT precedent: `1480х830х2010 мм` → `1480мм x 830мм x 2010мм`). бренд/модель/`л`/`Вт`/`мм`/`В`/`кВт` НЕ переводим; HTML-entities `&deg;` (x4) genuine HTML. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=976770291)*

---

## SKU 24/61 — Стол морозильный REEDNEE GN2100BT (Артикул 1045628525) — 🔴 RU=UA + Назв.мод (RU) UA-leak

**Поле:** Название модификации (RU)
**Было:** `Стіл морозильний REEDNEE GN2100BT`
**Стало:** `Стол морозильный REEDNEE GN2100BT`

**Поле:** Описание товара (RU)
**Было:** (полностью идентично UA — украинский текст)
**Стало:** (полный перевод RU тег-в-tag):

```
<h2>Двухдверный морозильный стол REEDNEE GN2100BT без борта.</h2> <p>Может использоваться в составе кухонной линии. Ширина стола — 700 мм.</p> <ul>
<li>Количество дверей: 2</li>
<li>Внутренняя и внешняя отделка — нержавеющая сталь</li>
<li>Температурный режим: -18&deg;C....-22 &deg;C</li>
<li>В комплекте 2 полки-решётки 330x430 мм.</li>
<li>Автоматическое размораживание</li>
<li>Хладагент R290</li>
<li>Динамическое охлаждение</li>
<li>Электронная панель управления</li>
<li>Полезный объём: 282 л</li>
<li>Мощность: 0,26 кВт.</li>
<li>Подключение к электросети: 220 В</li>
<li>Габаритные размеры: 1360мм x 700мм x 850мм</li>
</ul>
```

*(blk триплет STANDARD — `desc UA==RU` **True** (🔴 RU=UA — RU = полная укр. копия тела); `nm_ua`==`nm_ru` `Стіл морозильний REEDNEE GN2100BT` (UA-leak; body-level `_has_ua` True via `Стіл`/`морозильний`/`Внутрішнє`/`зовнішнє`/`оздоблення`/`неіржавка`/`полиці`/`решітки`/`У комплекті`/`Автоматичне розморожування`/`Хладагент`/`Динамічне охолодження`/`Електронна`/`панель керування`/`Корисний об'єм`/`Потужність`/`Під'єднання`/`електромережі`/`Габаритні розміри`); `nm_ru`!=`nazv_ru` genuine RU `Стол морозильный REEDNEE GN2100BT` → AUTO Назв.мод (RU) = genuine `nazv_ru`. **ВТОРОЙ blk триплет в chunk-028** + **прямой precedent chunk-027 b5 SKU 40 REEDNEE GN1410BT** (same brand REEDNEE, same supplier template `<h2>` opening + ul/12li, idential blk триплет паттерн). **REEDNEE НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. Описание (RU) — авторский полный перевод тег-в-tag (структура UA зеркалится 1:1; 1 `<h2>` + 1 `<p>` + 1 `<ul>` + 12 `<li>`, line-breaks `\n` после `<ul>` и между `<li>` preserve verbatim; no `<img>`, no iframe, no voltage explicit отдельно). SOFT применено к авторскому RU: `Дводверний морозильний стіл REEDNEE GN2100BT без борту.`→`Двухдверный морозильный стол REEDNEE GN2100BT без борта.`; `Може використовуватися в складі кухонної лінії. Ширина стола — 700 мм.` em-dash preserve U+2014 (Policy A); `Кількість дверей: 2`→`Количество дверей: 2`; `Внутрішнє та зовнішнє оздоблення — неіржавка сталь`→`Внутренняя и внешняя отделка — нержавеющая сталь` (em-dash preserve); `Температурний режим: -18°C....-22 °C`→`Температурный режим: -18&deg;C....-22 &deg;C` (SOFT `°`→`&deg;`; Lat C verbatim; 4-точечное `....` preserve; пробелы вокруг `&deg;` faithful UA pattern); `У комплекті 2 полиці-решітки 330х430 мм.`→`В комплекте 2 полки-решётки 330x430 мм.` (Policy B/C inner-dim — Cyr х U+0445 → Lat x U+0078; trailing single `мм` preserve как в UA; `решітки` → `решётки` ё U+0451); `Автоматичне розморожування`→`Автоматическое размораживание`; `Хладагент R290` НЕ переводим (R290 — refrigerant code; `Хладагент` UA/RU identical); `Динамічне охолодження`→`Динамическое охлаждение`; `Електронна панель керування`→`Электронная панель управления`; `Корисний об'єм: 282 л`→`Полезный объём: 282 л` (drop straight-apos; ё U+0451); `Потужність: 0,26 кВт.`→`Мощность: 0,26 кВт.` (decimal comma faithful); `Під'єднання до електромережі: 220 В`→`Подключение к электросети: 220 В` (drop apos); `Габаритні розміри: 1360x700x850 мм`→`Габаритные размеры: 1360мм x 700мм x 850мм` (Policy B/C — UA Lat x already; supplier UA single trail `мм` → RU `мм` слитно per axis + Lat x separator; chunk-027 SKU 40 REEDNEE GN1410BT precedent exact match `1480х830х2010 мм` → `1480мм x 830мм x 2010мм`). бренд/модель/`R290`/`л`/`мм`/`В`/`кВт` НЕ переводим; HTML-entities `&deg;` (x3) genuine HTML. META always faithful. Открытых вопросов 0.)*

**Наблюдения по батчу SKU 17-24 (24/61) — chunk-028 (батч-морозильные столы Apach (SKIP-НП) ×1 + Tatra (SKIP-НП) ×2 + FROSTY ×3 + Forcar ×1 + REEDNEE ×1; раздел `Холодильне та морозильне обладнання/Морозильні столи` — продолжение section transition с b2 SKU 15-16):** **blk триплет 2 (SKU 23 FROSTY GN 2100BT 700мм + SKU 24 REEDNEE GN2100BT — ПЕРВЫЕ blk триплет в chunk-028). blknotrip 0. blkv 0. blknochg 3 (SKU 20 FROSTY SNACK 2100BT + SKU 21 Forcar GN3100BT + SKU 22 FROSTY SNACK 3100BT — LIVE Horoshop genuine RU). blknochgeq 0. SKIP-НП 3 (SKU 17 Apach AFM 04 BT + SKU 18 Tatra TRC02BT + SKU 19 Tatra TRC03BT — продолжение Apach/Tatra-серий разделом `Морозильні столи`).** SKU 17 `595397992` Apach AFM 04 BT чотиридверний/четырехдверный — **SKIP-НП** (brand=`Apach` ∈ {APACH/Апач} NP-hit; cells unchanged). ЧЕТВЁРТЫЙ SKIP-НП в chunk-028 (продолжение Apach AFM серии после SKU 15 AFM 02 + SKU 16 AFM 03). Source signature `du!=dr` genuine разный, `nm_ua!=nm_ru` desync (UA `чотиридверний` vs RU `четырехдверный`); cells unchanged. SKU 18 `2062025984` Tatra TRC02BT — **SKIP-НП** (brand=`Tatra` NP-hit). ПЯТЫЙ SKIP-НП. Source `du==dr` True + `nm_ua==nm_ru` UA word `Стіл морозильний TATRA TRC02BT` UA-leak vs `nazv_ru` clean RU — same desync pattern как SKU 14 Tatra TRC1400BT b2. SKU 19 `2062029113` Tatra TRC03BT — **SKIP-НП** (mirror SKU 18). ШЕСТОЙ SKIP-НП. SKU 20 `508918198` FROSTY SNACK 2100BT (ширина 600мм) — **blknochg** LIVE Horoshop (supplier RU dr — hyphen `-` separators вместо em-dash; `&deg;С` Cyr entity + Lat C mix; `объем (л)` no-ё; `полки-решетки` no-ё; dims `1360x600x860` Lat x no мм; FROSTY supplier template Italy). FROSTY **НЕ ∈ НП-эксклюзив**. SKU 21 `508918203` Forcar GN3100BT — **blknochg** LIVE Horoshop (supplier RU dr same template family Italy; **SKU 21-specific desync**: UA `nm_ua/nazv_ua` содержит EXTRA `тридверний, Італія` отсутствующее в RU `nm_ru/nazv_ru` minimal `Стол морозильный Forcar GN3100BT` — supplier UA-side extra qualifiers, RU-side минимум). Forcar **НЕ ∈ НП-эксклюзив**. SKU 22 `616390857` FROSTY SNACK 3100BT (ширина 600мм) — **blknochg** LIVE Horoshop (mirror SKU 20 same template, 3 doors vs 2, dims 1795x600x860). FROSTY **НЕ ∈ НП-эксклюзив**. SKU 23 `976770291` FROSTY GN 2100BT (ширина 700мм) — **blk триплет** **ПЕРВЫЙ blk триплет в chunk-028** (3p + 1ul/9li, no `<img>`/iframe/voltage-explicit): `desc UA==RU` True 🔴, `nm_ua==nm_ru` UA word `Стіл морозильний FROSTY GN 2100BT (ширина 700 мм)` UA-leak, `nm_ru!=nazv_ru` → AUTO Назв.мод (RU) = `Стол морозильный FROSTY GN 2100BT (ширина 700 мм)`; Описание (RU) авторский 1:1; **отличие от blknochg SKU 20**: SKU 20 ширина 600мм (другой SKU, тот же шаблон) имеет supplier RU dr, а SKU 23 ширина 700мм supplier дал UA-only тело — magazine скопировал UA в RU cell. FROSTY **НЕ ∈ НП-эксклюзив**. SKU 24 `1045628525` REEDNEE GN2100BT — **blk триплет** (1h2 + 1p + 1ul/12li, no `<img>`/iframe/voltage-explicit отдельно; voltage в ul/li `220 В`): `desc UA==RU` True 🔴, `nm_ua==nm_ru` UA word `Стіл морозильний REEDNEE GN2100BT` UA-leak, `nm_ru!=nazv_ru` → AUTO Назв.мод (RU) = `Стол морозильный REEDNEE GN2100BT`; Описание (RU) авторский 1:1; **прямой precedent chunk-027 b5 SKU 40 REEDNEE GN1410BT** (same brand REEDNEE, same supplier template `<h2>` opening + ul/12li, identical blk триплет паттерн). REEDNEE **НЕ ∈ НП-эксклюзив**. **ВТОРОЙ blk триплет в chunk-028**. **Открытых вопросов по батчу: 0** (b1 0 + b2 0 + b3 0; ledger chunk-028 = 0). Кумулятивно chunk-028 = **0** (questions.md chunk-028 пока НЕ создаём — нет OQ). Кумулятивно SKIP-НП chunk-028 = **6** (b1 0 + b2 3 + b3 3). NEXT: chunk-028 b4 SKU 25-32.

*(scoped к row Артикул=1045628525)*

---

## SKU 25/61 — Стол морозильный REEDNEE GN3100BT (Артикул 1045631303) — 🔴 RU=UA + Назв.мод (RU) UA-leak

**Поле:** Название модификации (RU)
**Было:** `Стіл морозильний REEDNEE GN3100BT`
**Стало:** `Стол морозильный REEDNEE GN3100BT`

**Поле:** Описание товара (RU)
**Было:** (полностью идентично UA — украинский текст)
**Стало:** (полный перевод RU тег-в-tag):

```
<h2>Трёхдверный морозильный стол REEDNEE GN3100BT без борта.</h2> <p>Может использоваться в составе кухонной линии. Ширина стола — 700 мм.</p> <ul>
<li>объём 417 л</li>
<li>3 решётчатые полки 330x430 мм</li>
<li>3 двери</li>
<li>температурный режим -18...-22 &deg;С</li>
<li>автоматическое размораживание</li>
<li>хладагент R290</li>
<li>динамическое охлаждение</li>
<li>электронная панель управления</li>
<li>внутренняя и внешняя отделка — нержавеющая сталь</li>
<li>мощность: 0,6 кВт.</li>
<li>подключение к электросети: 220 В</li>
<li>габаритные размеры: 1795мм x 700мм x 850мм</li>
</ul>
```

*(blk триплет STANDARD — `desc UA==RU` **True** (🔴 RU=UA — RU = полная укр. копия тела); `nm_ua`==`nm_ru` `Стіл морозильний REEDNEE GN3100BT` (UA-leak; body-level `_has_ua` True via `Стіл`/`морозильний`); `nm_ru`!=`nazv_ru` genuine RU `Стол морозильный REEDNEE GN3100BT` → AUTO Назв.мод (RU) = genuine `nazv_ru`. **ТРЕТИЙ blk триплет в chunk-028** + **прямой precedent SKU 24 REEDNEE GN2100BT b3** (same brand REEDNEE, same supplier template `<h2>` opening + `<p>` + `<ul>`/12`<li>`, 3-door variant vs 2-door; chunk-027 b5 SKU 40 REEDNEE GN1410BT — 4-door variant). **REEDNEE НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. Описание (RU) — авторский полный перевод тег-в-tag (структура UA зеркалится 1:1; 1 `<h2>` + 1 `<p>` + 1 `<ul>` + 12 `<li>`, line-breaks `\n` после `<ul>` и между `<li>` preserve verbatim). SOFT применено к авторскому RU: `Тридверний морозильний стіл REEDNEE GN3100BT без борту.`→`Трёхдверный морозильный стол REEDNEE GN3100BT без борта.` (ё U+0451 в `Трёхдверный`; `борту`→`борта`); `Може використовуватися в складі кухонної лінії. Ширина стола — 700 мм.` em-dash preserve U+2014 (Policy A); `об'єм 417 л`→`объём 417 л` (drop straight-apos U+0027; ё); `3 ґратчасті полиці 330х430 мм`→`3 решётчатые полки 330x430 мм` (UA-only `ґ` U+0491 → drop в RU; ё в `решётчатые`; Cyr х U+0445 → Lat x U+0078 в `330x430`; trailing single `мм` preserve); `3 двері`→`3 двери`; **SKU 25-SPECIFIC supplier OCR corruption**: UA `-18...-22 ⁇ С` содержит U+2047 (DOUBLE QUESTION MARK) между `-22` и `С` — supplier data quality issue, очевидно degraded `°` U+00B0 (adjacent SKU 30/31/32 Cooleq patterns: `-10&deg;С...-20&deg;С` SKU 30, `-10&deg;C....-20&deg;C` SKU 31, `-18&deg;С...-20&deg;С` SKU 32 — все используют `&deg;` entity); нормализуем corruption к canonical → `температурный режим -18...-22 &deg;С` (3-точечное `...` preserve; Cyr С verbatim); `автоматичне розморожування`→`автоматическое размораживание`; `холодоагент R290`→`хладагент R290` (UA typo `холодоагент` с лишним `о` — должно быть `холодагент`; canonical RU `хладагент`; R290 refrigerant code НЕ переводим); `динамічне охолодження`→`динамическое охлаждение`; `електронна панель керування`→`электронная панель управления`; `внутрішнє та зовнішнє оздоблення — неіржавка сталь`→`внутренняя и внешняя отделка — нержавеющая сталь` (gender shift neut. UA `оздоблення` → fem. RU `отделка` — agreement с adj `внутренняя`/`внешняя`; em-dash preserve); `потужність: 0,6 кВт.`→`мощность: 0,6 кВт.` (decimal comma faithful); `під'єднання до електромережі: 220 В`→`подключение к электросети: 220 В` (drop apos); `габаритні розміри: 1795x700x850 мм`→`габаритные размеры: 1795мм x 700мм x 850мм` (Policy B/C — UA Lat x already; supplier UA single trail `мм` → RU `мм` слитно per axis + Lat x separator; precedent SKU 24 b3 `1360x700x850 мм` → `1360мм x 700мм x 850мм`). бренд/модель/`R290`/`л`/`мм`/`В`/`кВт` НЕ переводим; HTML-entities `&deg;` (x1) genuine HTML. META always faithful. Открытых вопросов 0 — `⁇` U+2047 corruption нормализован inline как supplier data quality artefact, soft observation.)*

*(scoped к row Артикул=1045631303)*

---

## SKU 26/61 — Стол морозильный HURAKAN HKN-GXFC2GN (ширина 700 мм) (Артикул 1082407888) — SKIP-НП (бренд НП-эксклюзив, тело из фида НП позже)

**Бренд:** Hurakan (НП-эксклюзивный — forward-only SKIP-правило)
**Поле:** Название модификации (RU)
**Было:** (ячейка не трогается — тело из фида НП позже)
**Стало:** не трогаем (SKIP-НП — тело из фида НП позже)

**Поле:** Описание товара (RU)
**Было:** (ячейка не трогается — тело из фида НП позже)
**Стало:** не трогаем (SKIP-НП — тело из фида НП позже)

*(SKIP-НП — `brand`=`Hurakan` ∈ {HURAKAN/Хуракан} word-boundary NP-hit → forward-only SKIP-правило: тело из фида НП позже, ячейки chunk-028-fixed.xlsx НЕ трогаем (Назв.мод RU + Описание RU без изменений). **Hurakan ∈ НП-эксклюзивный список** (word-boundary NP-hit найден в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}) → forward-only SKIP-правило: тело из фида НП позже, ячейки chunk-028-fixed.xlsx не трогаем (Назв.мод RU + Описание RU без изменений). **СЕДЬМОЙ SKIP-НП в chunk-028** + **ПЕРВЫЙ Hurakan в chunk-028** (scaffold rollup ожидает Hurakan ×2 across SKU 26+59; SKU 59 — следующий Hurakan позже). Source signature **`du==dr` True** (supplier UA скопирован в RU как single body) + `nm_ua`!=`nm_ru` desync: UA `Стіл морозильний HURAKAN HKN-GXFC2GN (ширина 700 мм)` (allcaps brand + `(ширина 700 мм)` suffix) vs RU `Стіл морозильний Hurakan HKN-GXFC2GN 2-дверний` (Titlecase brand + `2-дверний` door-count suffix вместо ширина-suffix); **ОБА nm_ua и nm_ru содержат UA-leak `Стіл морозильний`** + UA `2-дверний` в nm_ru — magazine копирует UA-варианты brand с разной структурой в UA-side vs RU-side cells, но РУС обе copy-leak остались украинскими. `nazv_ru` clean RU `Стол морозильный HURAKAN HKN-GXFC2GN (ширина 700 мм)` — desync vs nm_ru — но brand-rule overrides signature, SKIP-НП **НЕ правим** ячейки (тело из фида НП позже всё перепишет, включая UA-leak в nm_ru). Кумул. SKIP-НП chunk-028 = 7 (после SKU 26). META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=1082407888)*

---

## SKU 27/61 — Стол морозильный Tecnodom TF02MIDBT (Артикул 1091477214) — 🔴 RU=UA + Назв.мод (RU) UA-leak

**Поле:** Название модификации (RU)
**Было:** `Стіл морозильний Tecnodom TF02MIDBT`
**Стало:** `Стол морозильный Tecnodom TF02MIDBT`

**Поле:** Описание товара (RU)
**Было:** (полностью идентично UA — украинский текст)
**Стало:** (полный перевод RU тег-в-tag):

```
<h2>Двухдверный морозильный Tecnodom TF02MIDBT стол без борта.</h2> <p>Может использоваться в составе кухонной линии. Толщина изоляции &mdash; 60 мм. Ширина стола &mdash; 700 мм. Максимальная температура окружающей среды +43 &deg;C. Электронный блок управления, автоматическое размораживание.</p> <p>Удобная регулировка ножек &mdash; телескопические опоры из нержавеющей стали.</p> <p>Регулируемые по высоте направляющие под полки стандарта GN1/1, в комплекте 2 полки-решётки.</p> <ul>
<li>Столешница и корпус: нержавеющая сталь AISI 304</li>
<li>Количество дверей: 2</li>
<li>Температурный режим: -18&deg; C....-22 &deg;C</li>
<li>Тип охлаждения: динамический</li>
<li>Цифровой термостат</li>
<li>Полезный объём: 310 л</li>
<li>Мощность: 0,655 кВт.</li>
<li>Подключение к электросети: 220 В</li>
<li>Габаритные размеры: 1420мм x 715мм x 920мм</li>
</ul>
```

*(blk триплет STANDARD — `desc UA==RU` **True** (🔴 RU=UA — RU = полная укр. копия тела); `nm_ua`==`nm_ru` `Стіл морозильний Tecnodom TF02MIDBT` (UA-leak; body-level `_has_ua` True via `Стіл`/`морозильний`); `nm_ru`!=`nazv_ru` genuine RU `Стол морозильный Tecnodom TF02MIDBT` → AUTO Назв.мод (RU) = genuine `nazv_ru`. **ЧЕТВЁРТЫЙ blk триплет в chunk-028** + **прямой precedent SKU 23 FROSTY GN 2100BT 700мм b3** (same структура 3-`<p>` template). **Tecnodom НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. Tecnodom — Italian supplier brand same template family как FROSTY/Forcar (b3 blknochg SKU 20-22), но в данном случае supplier дал UA-only тело без отдельного RU перевода (magazine скопировал UA в RU cell, отсюда desc UA==RU True); **отличие от blknochg SKU 28 Tecnodom TF03MIDBT** (same brand same template, 3-door variant): SKU 27 (2-door) — supplier UA-only тело → blk триплет; SKU 28 (3-door) — supplier дал отдельный RU dr → blknochg. Same brand-template, разные supplier-paths внутри одного бренда (как FROSTY SKU 20 blknochg vs SKU 23 blk триплет в b3). Supplier UA uses HTML-entities throughout (`&mdash;` em-dash entity, `&deg;` degree entity, `&#39;` apos entity — отличие от SKU 25 REEDNEE который использует literal U+2014 em-dash + raw apos U+0027). Описание (RU) — авторский полный перевод тег-в-tag (структура UA зеркалится 1:1; 1 `<h2>` + 3 `<p>` + 1 `<ul>` + 9 `<li>`, line-breaks `\n` после `<ul>` и между `<li>` preserve). SOFT применено к авторскому RU: `Дводверний морозильний Tecnodom TF02MIDBT стіл без борту.`→`Двухдверный морозильный Tecnodom TF02MIDBT стол без борта.` (word-order preserve как UA — model code между прилаг. и noun; `борту`→`борта`); `Може використовуватися в складі кухонної лінії.`→`Может использоваться в составе кухонной линии.`; `Товщина ізоляції &mdash; 60 мм. Ширина стола &mdash; 700 мм. Максимальна температура довкілля +43 &deg;C.`→`Толщина изоляции &mdash; 60 мм. Ширина стола &mdash; 700 мм. Максимальная температура окружающей среды +43 &deg;C.` (`&mdash;` entity preserve в обеих позициях; `&deg;` entity preserve; Lat C verbatim); `Електронний блок керування, автоматичне розморожування.`→`Электронный блок управления, автоматическое размораживание.`; `Зручне регулювання ніжок &mdash; телескопічні опори з нержавіючої сталі.`→`Удобная регулировка ножек &mdash; телескопические опоры из нержавеющей стали.` (`&mdash;` entity preserve); `Регульовані за висотою напрямні під полиці стандарту GN1/1, у комплекті 2 полиці-решітки.`→`Регулируемые по высоте направляющие под полки стандарта GN1/1, в комплекте 2 полки-решётки.` (`решітки` → `решётки` ё U+0451); `Стільниця та корпус: нержавіюча сталь AISI 304`→`Столешница и корпус: нержавеющая сталь AISI 304`; `Кількість дверей: 2`→`Количество дверей: 2`; `Температурний режим: -18&deg; C....-22 &deg;C`→`Температурный режим: -18&deg; C....-22 &deg;C` (entity + Lat C + space pattern preserve precedent SKU 23 b3); `Тип охолодження: динамічний`→`Тип охлаждения: динамический`; `Цифровий термостат`→`Цифровой термостат`; `Корисний об&#39;єм: 310 л`→`Полезный объём: 310 л` (drop &#39; entity-apos; ё U+0451); `Потужність: 0,655 кВт.`→`Мощность: 0,655 кВт.` (decimal comma faithful); `Під&#39;єднання до електромережі: 220 В`→`Подключение к электросети: 220 В` (drop &#39; entity-apos); `Габаритні розміри: 1420x715x920 мм`→`Габаритные размеры: 1420мм x 715мм x 920мм` (Policy B/C — UA Lat x already; per-axis `мм` слитно). бренд/модель/`AISI 304`/`GN1/1`/`л`/`мм`/`В`/`кВт` НЕ переводим; HTML-entities `&mdash;` (x3) + `&deg;` (x3) + drop `&#39;` (x2). META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=1091477214)*

---

## SKU 28/61 — Стол морозильный Tecnodom TF03MIDBT (Артикул 1091487308) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg — `desc UA==RU` **False** (genuine отдельный корректный русский перевод поставщика, НЕ укр. копия — длина dr 822 vs du 832); `nm_ua`!=`nm_ru` (UA `Стіл морозильний Tecnodom TF03MIDBT` vs RU `Стол морозильный Tecnodom TF03MIDBT`); `nm_ru`==`nazv_ru` clean RU (char-level UA_ONLY=∅). **Tecnodom НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. LIVE-магазин Horoshop, genuine RU body НЕ переписываем (ячейки chunk-028-fixed без изменений). **Отличие от blk триплет SKU 27 Tecnodom TF02MIDBT** (same brand same template family, 2-door variant): SKU 27 (2-door) — supplier UA-only тело (desc UA==RU True) → blk триплет; SKU 28 (3-door) — supplier дал отдельный RU dr (desc UA==RU False) → blknochg. LIVE source artefacts preserve verbatim (Tecnodom Italian supplier template family same как FROSTY/Forcar b3): (1) supplier RU dr uses hyphen `-` separators вместо UA em-dash entity `&mdash;` (`Толщина изоляции - 60 мм. Ширина стола - 700 мм.` RU vs UA `Товщина ізоляції &mdash; 60 мм. Ширина стола &mdash; 700 мм.`) — format desync supplier-side, в RU genuine; (2) RU dr `+43&deg;С` Cyr С (entity + Cyr С) vs UA du `+43 &deg;C` Lat C — temp postfix desync supplier-side; (3) RU dr `-18&deg; C....-22&deg; C` Lat C double + space-after-entity asymmetry vs UA `-18&deg; C....-22 &deg;C` — minor format desync; (4) RU `полезный объем` без ё vs UA `Корисний об&#39;єм` (entity-apos); (5) RU `полки-решетки` без ё vs UA `полиці-решітки`; (6) dims `1870x715x920` UA Lat x identical to RU genuine — supplier consistent. blknochg → ВСЕ артефакты `dr` (RU-side) НЕ трогаем; авторский перевод НЕ генерим. Код `Tecnodom TF03MIDBT` Lat → consistent. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=1091487308)*

---

## SKU 29/61 — Стол-саладетта морозильный Tefcold SA910BT (Артикул 1154445638) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg — `desc UA==RU` **False** (genuine отдельный русский перевод поставщика, разная длина dr 974 vs du 961); `nm_ua`!=`nm_ru` (UA `Стіл-саладетта морозильний Tefcold SA910BT` vs RU `Стол-саладетта морозильный Tefcold SA910BT`); `nm_ru`==`nazv_ru` clean RU (char-level UA_ONLY=∅). **Tefcold НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. Substring `COLD` присутствует в `TEFCOLD`, но word-boundary regex `(?<![A-Za-zА-Яа-яЁё])COLD(?![A-Za-zА-Яа-яЁё])` НЕ срабатывает (`COLD` следует за `F` — буква, lookbehind fails). Durable constraint: `Tefcold/Forcold/Forcar НЕ SKIP` (substring `cold`/`for` ≠ standalone NP word). LIVE-магазин Horoshop, genuine RU body НЕ переписываем. Tefcold — Danish supplier (vs Italian FROSTY/Forcar/Tecnodom), DIFFERENT template family: dr structure 1`<p>` + 1`<ul>`/22`<li>` (расширенная spec-таблица 22 items vs FROSTY 9, Tecnodom 9-10 items); LIVE artefacts dr verbatim: (1) supplier RU dr `Двухдверный морозильный стол -саладетта Tefcold SA910BT.` — leading стол `-саладетта` (space-hyphen-suffix prefix); (2) `2 pешетчатые` RU dr содержит **Lat p** U+0070 вместо Cyr р U+0440 (`pешетчатые` латинская p — supplier OCR-artefact в LIVE RU dr); (3) `&deg;C` Lat C single entry в RU dr (`От -20 до -10 &deg;C`); (4) `Уровень шума: 42 дб(А)` идентичен UA/RU (cyrillic preserve); (5) inner-dim `830 x 515 x 500 мм` + габ `943 x 700 x 877 мм` — UA/RU оба используют **space-x-space** separator (НЕ Policy B/C inline-x), supplier consistent format; (6) `R290` refrigerant code identical; (7) `6.95 квт/24ч` (decimal **dot** вместо comma; `квт` строчные; `24ч` слитно) — supplier consistent UA/RU. blknochg → ВСЕ артефакты preserve verbatim (включая Lat p typo в `pешетчатые`); НЕ переписываем. **Tefcold НЕ ∈ НП-эксклюзив** (substring `COLD` в `TEFCOLD` НЕ word-boundary NP-hit — `COLD` preceded by `F` letter; durable constraint `Tefcold/Forcold/Forcar НЕ SKIP`). Код `Tefcold SA910BT` Lat → consistent. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=1154445638)*

---

## SKU 30/61 — Морозильный стол COOLEQ GN2100BT (1,36 м) (Артикул 1395790396) — 🔴 RU=UA + Назв.мод (RU) UA-leak

**Поле:** Название модификации (RU)
**Было:** `Морозильний стіл COOLEQ GN2100BT (1,36 м)`
**Стало:** `Морозильный стол COOLEQ GN2100BT (1,36 м)`

**Поле:** Описание товара (RU)
**Было:** (полностью идентично UA — украинский текст)
**Стало:** (полный перевод RU тег-в-tag):

```
<h2>Морозильный стол COOLEQ GN2100BT без борта двухдверный. </h2> <ul>
<li>Объём: 314 л</li>
<li>Температурный режим: -10&deg;С...-20&deg;С</li>
<li>Столешница и корпус из нержавеющей стали</li>
<li>Габаритные размеры: 1360мм x 700мм x 860мм</li>
<li>Мощность: 0,62 кВт</li>
<li>Напряжение: 220 В</li>
</ul>
```

*(blk триплет STANDARD — `desc UA==RU` **True** (🔴 RU=UA); `nm_ua`==`nm_ru` `Морозильний стіл COOLEQ GN2100BT (1,36 м)` (UA-leak; body-level `_has_ua` True via `Морозильний`/`стіл`); `nm_ru`!=`nazv_ru` genuine RU `Морозильный стол COOLEQ GN2100BT (1,36 м)` → AUTO Назв.мод (RU) = genuine `nazv_ru`. **ПЯТЫЙ blk триплет в chunk-028** + **ПЕРВЫЙ Cooleq blk триплет в chunk-028**. **Cooleq НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. Cooleq — НЕ Italian template family (FROSTY/Forcar/Tecnodom), отдельный supplier-template — minimal compact UL (1`<h2>` + 1`<ul>` + 6`<li>`, no `<p>`, no `<img>`, no iframe). Описание (RU) — авторский полный перевод тег-в-tag (структура UA зеркалится 1:1; trailing space внутри `<h2>...дводверний. </h2>` обёртки preserve verbatim как UA single-space-before-close). SOFT применено к авторскому RU: `Морозильний стіл COOLEQ GN2100BT без борту дводверний. `→`Морозильный стол COOLEQ GN2100BT без борта двухдверный. ` (trailing space inside `</h2>` preserve; `борту`→`борта`; word-order preserve UA — adj-noun-без-borta-qualifier); `Об&#39;єм: 314 л`→`Объём: 314 л` (drop &#39; entity-apos; ё U+0451); `Температурний режим: -10&deg;С...-20&deg;С`→`Температурный режим: -10&deg;С...-20&deg;С` (Cyr С postfix preserve verbatim; 3-точечное `...` preserve — отличие от 4-точечного SKU 23/24/27 Italy template); `Столешня та корпус з нержавіючої сталі`→`Столешница и корпус из нержавеющей стали` (UA `Столешня` — supplier russism-typo, canonical UA должно быть `Стільниця`; нормализуем к canonical RU `Столешница`); `Габаритні розміри: 1360x700x860 мм`→`Габаритные размеры: 1360мм x 700мм x 860мм` (Policy B/C — UA Lat x already; per-axis `мм` слитно — exact match SKU 23 FROSTY GN 2100BT 700мм b3 dims); `Потужність: 0,62 кВт`→`Мощность: 0,62 кВт` (no trailing dot — UA verbatim); `Напруга: 220 В`→`Напряжение: 220 В`. бренд/модель/`л`/`мм`/`В`/`кВт` НЕ переводим; HTML-entities `&deg;` (x2) genuine HTML. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=1395790396)*

---

## SKU 31/61 — Стол морозильный COOLEQ GN3100BT (Артикул 1398723073) — 🔴 RU=UA + Назв.мод (RU) UA-leak

**Поле:** Название модификации (RU)
**Было:** `Стіл морозильний COOLEQ GN3100BT`
**Стало:** `Стол морозильный COOLEQ GN3100BT`

**Поле:** Описание товара (RU)
**Было:** (полностью идентично UA — украинский текст)
**Стало:** (полный перевод RU тег-в-tag):

```
<h2>Стол морозильный COOLEQ GN3100BT предназначен для приготовления и хранения продуктов в замороженном виде.</h2> <p>Трёхдверный морозильный стол без борта. Электронная панель управления, автоматическое размораживание и испарение талой воды.</p> <ul>
<li>Столешница и корпус: нержавеющая сталь </li>
<li>Количество дверей: 3</li>
<li>Температурный режим: -10&deg;C....-20&deg;C</li>
<li>Тип охлаждения: динамика</li>
<li>Цифровой термостат</li>
<li>Объём: 465 л</li>
<li>Мощность: 0,62 кВт.</li>
<li>Габариты: 1795мм x 700мм x 860мм</li>
</ul>
```

*(blk триплет STANDARD — `desc UA==RU` **True** (🔴 RU=UA); `nm_ua`==`nm_ru` `Стіл морозильний COOLEQ GN3100BT` (UA-leak); `nm_ru`!=`nazv_ru` genuine RU `Стол морозильный COOLEQ GN3100BT` → AUTO Назв.мод (RU) = genuine `nazv_ru`. **ШЕСТОЙ blk триплет в chunk-028** + **ВТОРОЙ Cooleq blk триплет в chunk-028** (3-door variant vs SKU 30 2-door). **Cooleq НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. Cooleq supplier-template variant: SKU 31 расширенная — 1`<h2>` + 1`<p>` + 1`<ul>`/8`<li>` (с дополнительным `<p>`-уточнением vs SKU 30 minimal). Описание (RU) — авторский 1:1 тег-в-tag. SOFT применено: `Стіл морозильний COOLEQ GN3100BT призначений для приготування та зберігання продуктів у замороженому вигляді.`→`Стол морозильный COOLEQ GN3100BT предназначен для приготовления и хранения продуктов в замороженном виде.`; `Тридверний морозильний стіл без борту.`→`Трёхдверный морозильный стол без борта.` (ё в `Трёхдверный`; `борту`→`борта`); **SKU 31-SPECIFIC UA typo**: `Електрона панель керування` — supplier UA содержит typo `Електрона` (один `н`, canonical UA должно быть `Електронна`); нормализуем к canonical RU `Электронная панель управления` (НЕ carry-over supplier typo — переводим к правильной RU форме); `автоматичне розморожування та випаровування талої води.`→`автоматическое размораживание и испарение талой воды.`; trailing space внутри `<li>Столешниця та корпус: нержавіюча сталь </li>`→`<li>Столешница и корпус: нержавеющая сталь </li>` (preserve trailing space verbatim как UA); `Кількість дверей: 3`→`Количество дверей: 3`; `Температурний режим: -10&deg;C....-20&deg;C`→`Температурный режим: -10&deg;C....-20&deg;C` (Lat C verbatim; 4-точечное `....` preserve — отличие от SKU 30 Cyr С + 3-точечное; supplier inconsistent внутри одного бренда); **SKU 31-SPECIFIC supplier brevity**: `Тип охолодження: динаміка` — substantive form вместо adjective `динамічний` (other SKU); нормализуем semantic shift к `Тип охлаждения: динамика` (preserve substantive form); `Цифровий термостат`→`Цифровой термостат`; `Об&#39;єм: 465 л`→`Объём: 465 л` (drop &#39;; ё); `Потужність: 0,62 кВт.`→`Мощность: 0,62 кВт.` (decimal comma; trailing dot preserve — отличие от SKU 30 no-dot); `Габарити: 1795x700x860 мм`→`Габариты: 1795мм x 700мм x 860мм` (Policy B/C; UA `Габарити:` short form preserve в RU `Габариты:` — supplier brevity choice; exact match SKU 25 REEDNEE GN3100BT dims 1795x700x850 кроме высоты 860 vs 850). бренд/модель/`л`/`мм`/`В`/`кВт` НЕ переводим; HTML-entities `&deg;` (x2) + drop `&#39;` (x1). META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=1398723073)*

---

## SKU 32/61 — Морозильный стол COOLEQ SS45BT (0,9 м) (Артикул 1755813685) — 🔴 RU=UA + Назв.мод (RU) UA-leak

**Поле:** Название модификации (RU)
**Было:** `Морозильний стіл COOLEQ SS45BT (0,9 м)`
**Стало:** `Морозильный стол COOLEQ SS45BT (0,9 м)`

**Поле:** Описание товара (RU)
**Было:** (полностью идентично UA — украинский текст)
**Стало:** (полный перевод RU тег-в-tag):

```
<h2>Морозильный стол COOLEQ SS45BT без борта двухдверный.<br />
В стол встроен морозильный шкаф с искусственным охлаждением внутреннего объёма. Столешница из нержавеющей стали выполняет функцию рабочей поверхности повара.</h2> <ul>
<li>Объём: 257 л</li>
<li>Температурный режим: -18&deg;С...-20&deg;С</li>
<li>Столешница из нержавеющей стали</li>
<li>Корпус из нержавеющей стали</li>
<li>Агрегат расположен снизу</li>
<li>Статическое охлаждение</li>
<li>Без борта</li>
<li>2 двери (каждая секция укомплектована 1 полкой и 1 парой направляющих под GN1/1)</li>
<li>Габаритные размеры: 900мм x 700мм x 860мм</li>
<li>Мощность: 0,32 кВт</li>
<li>Напряжение: 220 В</li>
<li>Фреон R290 75г</li>
</ul>
```

*(blk триплет STANDARD — `desc UA==RU` **True** (🔴 RU=UA); `nm_ua`==`nm_ru` `Морозильний стіл COOLEQ SS45BT (0,9 м)` (UA-leak; `_has_ua` True via `Морозильний`/`стіл`); `nm_ru`!=`nazv_ru` genuine RU `Морозильный стол COOLEQ SS45BT (0,9 м)` → AUTO Назв.мод (RU) = genuine `nazv_ru`. **СЕДЬМОЙ blk триплет в chunk-028** + **ТРЕТИЙ Cooleq blk триплет в chunk-028** (SS45BT 0.9м variant — компактная 2-door с встроенной морозильной шафой). **Cooleq НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. Cooleq supplier-template variant: SKU 32 multi-line `<h2>` с `<br />` inline + 1`<ul>`/12`<li>` (расширенная spec — отличие от SKU 30/31 single-line h2). Описание (RU) — авторский 1:1 тег-в-tag (структура UA зеркалится 1:1; `<br />\n` inside `<h2>` preserve verbatim). SOFT применено: `Морозильний стіл COOLEQ SS45BT без борту дводверний.<br />\nУ стіл вбудовано морозильну шафу зі штучним охолодженням внутрішнього об&#39;єму. Стільниця з нержавіючої сталі виконує функцію робочої поверхні кухаря.</h2>`→`Морозильный стол COOLEQ SS45BT без борта двухдверный.<br />\nВ стол встроен морозильный шкаф с искусственным охлаждением внутреннего объёма. Столешница из нержавеющей стали выполняет функцию рабочей поверхности повара.</h2>` (preposition shift `У стіл`→`В стол`; voice shift `вбудовано` neut-passive UA → `встроен` masc-passive RU agreement с `шкаф`; gender shift `шафа` fem. UA → `шкаф` masc. RU; `штучним` → `искусственным`; drop &#39; в `об'єму`→`объёма` с ё; `Стільниця` → `Столешница`; `неіржавкої`→`нержавеющей`; `кухаря` → `повара` — canonical RU profession term); `Об&#39;єм: 257 л`→`Объём: 257 л`; `Температурний режим: -18&deg;С...-20&deg;С`→`Температурный режим: -18&deg;С...-20&deg;С` (Cyr С + 3-точечное preserve — match SKU 30 Cooleq pattern); `Стільниця з нержавіючої сталі`→`Столешница из нержавеющей стали`; `Корпус із нержавіючої сталі`→`Корпус из нержавеющей стали` (UA `із` vs `з` preposition variant → RU canonical `из`); `Агрегат розташований знизу`→`Агрегат расположен снизу`; `Статичне охолодження`→`Статическое охлаждение`; `Без борту`→`Без борта`; `2 двері (кожна секція укомплектована 1 полицею та 1 парою направляючих під GN1/1)`→`2 двери (каждая секция укомплектована 1 полкой и 1 парой направляющих под GN1/1)` (declension shift instr. `полицею`→`полкой`, `парою`→`парой`); `Габаритні розміри: 900x700x860 мм`→`Габаритные размеры: 900мм x 700мм x 860мм` (Policy B/C); `Потужність: 0,32 кВт`→`Мощность: 0,32 кВт` (no trailing dot — match SKU 30); `Напруга: 220 В`→`Напряжение: 220 В`; `Фреон R290 75г`→`Фреон R290 75г` (UA/RU identical; `Фреон` cyrillic identical; R290 code preserve; `75г` слитно — supplier weight notation preserve). бренд/модель/`R290`/`GN1/1`/`л`/`мм`/`В`/`кВт`/`г` НЕ переводим; HTML-entities `&deg;` (x2) + drop `&#39;` (x2). META always faithful. Открытых вопросов 0.)*

**Наблюдения по батчу SKU 25-32 (32/61) — chunk-028 (батч-морозильные столы REEDNEE ×1 + Hurakan SKIP-НП ×1 + Tecnodom ×2 + Tefcold ×1 + Cooleq ×3; раздел `Холодильне та морозильне обладнання/Морозильні столи` — продолжение b3 SKU 17-24):** **blk триплет 5 (SKU 25 REEDNEE GN3100BT + SKU 27 Tecnodom TF02MIDBT + SKU 30 Cooleq GN2100BT 1.36м + SKU 31 Cooleq GN3100BT + SKU 32 Cooleq SS45BT 0.9м). blknotrip 0. blkv 0. blknochg 2 (SKU 28 Tecnodom TF03MIDBT + SKU 29 Tefcold SA910BT — LIVE Horoshop genuine RU). blknochgeq 0. SKIP-НП 1 (SKU 26 Hurakan HKN-GXFC2GN — СЕДЬМОЙ SKIP-НП в chunk-028, ПЕРВЫЙ Hurakan).** SKU 25 `1045631303` REEDNEE GN3100BT — **blk триплет** **ТРЕТИЙ blk триплет в chunk-028** + **прямой precedent SKU 24 b3** (same brand REEDNEE same template `<h2>`+`<p>`+ul/12li, 3-door variant vs 2-door): `desc UA==RU` True 🔴, `nm_ua==nm_ru` UA-leak `Стіл морозильний REEDNEE GN3100BT`, `nm_ru!=nazv_ru` → AUTO Назв.мод RU; Описание RU авторский 1:1; **SKU 25-SPECIFIC supplier OCR corruption**: U+2047 `⁇` DOUBLE QUESTION MARK между `-22` и `С` в temp-segment (supplier data quality issue, очевидно degraded `°`) — нормализуем inline к `&deg;С` canonical (опираясь на adjacent SKU 30/31/32 Cooleq supplier patterns с `&deg;` entity); SOFT: ё в `Трёхдверный`/`объём`/`решётчатые`, drop apos, Cyr х→Lat x в inner-dim `330x430`, em-dash preserve, Policy B/C `1795мм x 700мм x 850мм`, UA typo `холодоагент` (лишний `о`) → canonical RU `хладагент`. REEDNEE **НЕ ∈ НП-эксклюзив**. SKU 26 `1082407888` Hurakan HKN-GXFC2GN — **SKIP-НП** (brand=`Hurakan` ∈ {HURAKAN/Хуракан} NP-hit; **СЕДЬМОЙ SKIP-НП в chunk-028** + **ПЕРВЫЙ Hurakan**; scaffold rollup ожидает Hurakan ×2 — SKU 59 следующий Hurakan позже; source `du==dr` True + `nm_ua!=nm_ru` desync ALLCAPS HURAKAN+(ширина 700 мм) vs Titlecase Hurakan+2-дверний — ОБА nm_ua/nm_ru имеют UA-leak `Стіл морозильний`; cells unchanged — тело из фида НП позже всё перепишет включая UA-leak). SKU 27 `1091477214` Tecnodom TF02MIDBT — **blk триплет** **ЧЕТВЁРТЫЙ blk триплет в chunk-028** (2-door; Italian supplier template family same как FROSTY/Forcar но supplier дал UA-only тело, magazine скопировал UA в RU cell; `desc UA==RU` True 🔴, `nm_ua==nm_ru` UA-leak; Описание RU авторский 1`<h2>`+3`<p>`+ul/9li 1:1; HTML-entities `&mdash;`/`&deg;`/`&#39;` preserve throughout — отличие от SKU 25 REEDNEE который использует literal U+2014 em-dash + raw apos U+0027). Tecnodom **НЕ ∈ НП-эксклюзив**. **Отличие SKU 27 vs SKU 28 same brand Tecnodom**: SKU 27 (2-door TF02MIDBT) — supplier UA-only → blk триплет; SKU 28 (3-door TF03MIDBT) — supplier дал отдельный RU dr → blknochg. SKU 28 `1091487308` Tecnodom TF03MIDBT — **blknochg** LIVE Horoshop (supplier RU dr genuine; same Italian template family — hyphen `-` separators вместо UA em-dash entity `&mdash;`, `&deg;С` Cyr С vs UA Lat C, `полезный объем` без ё, `полки-решетки` без ё, dims `1870x715x920` Lat x identical; НЕ переписываем). SKU 29 `1154445638` Tefcold SA910BT — **blknochg** LIVE Horoshop (Danish supplier — DIFFERENT template family vs Italian FROSTY/Forcar/Tecnodom; extended spec 1`<p>`+ul/22li; supplier RU dr содержит **Lat p** U+0070 в `pешетчатые` вместо Cyr р — supplier OCR artefact в LIVE RU dr; `space-x-space` separator в dims `830 x 515 x 500 мм` supplier consistent UA/RU; `6.95 квт/24ч` decimal dot + строчные ед.изм supplier choice; НЕ переписываем). **Tefcold НЕ ∈ НП-эксклюзив** (substring `COLD` в `TEFCOLD` НЕ word-boundary — durable constraint `Tefcold/Forcold/Forcar НЕ SKIP`). SKU 30 `1395790396` Cooleq GN2100BT (1,36 м) — **blk триплет** **ПЯТЫЙ blk триплет в chunk-028** + **ПЕРВЫЙ Cooleq blk триплет**: minimal 1`<h2>` + ul/6li (no `<p>`), trailing space `</h2>` preserve, Cyr С postfix + 3-точечное `...` (Cooleq inconsistent vs SKU 31 Lat C + 4-точечное внутри одного бренда); SOFT applied. Cooleq **НЕ ∈ НП-эксклюзив**. SKU 31 `1398723073` Cooleq GN3100BT — **blk триплет** **ШЕСТОЙ blk триплет** + **ВТОРОЙ Cooleq** (3-door variant): 1`<h2>` + 1`<p>` + ul/8li, **SKU 31-SPECIFIC UA typo** `Електрона` (один `н`, canonical `Електронна`) → нормализуем к canonical RU `Электронная`; **supplier brevity** `Тип охолодження: динаміка` substantive form → RU `Тип охлаждения: динамика` semantic preserve; `Габарити:` short form → RU `Габариты:`; trailing space внутри `<li>...нержавіюча сталь </li>` preserve. SKU 32 `1755813685` Cooleq SS45BT (0,9 м) — **blk триплет** **СЕДЬМОЙ blk триплет** + **ТРЕТИЙ Cooleq** (multi-line `<h2>` с `<br />` inline; extended ul/12li; `Фреон R290 75г` preserve UA/RU identical; preposition `У стіл`→`В стол`; gender shift `шафа` fem→`шкаф` masc; `кухар`→`повар` canonical). **Открытых вопросов по батчу: 0** (b1 0 + b2 0 + b3 0 + b4 0; ledger chunk-028 = 0). Кумулятивно chunk-028 = **0** (questions.md chunk-028 пока НЕ создаём — нет OQ; SKU 25 supplier OCR-artefact `⁇` U+2047 → soft observation, нормализован inline, не нумеруется). Кумулятивно SKIP-НП chunk-028 = **7** (b1 0 + b2 3 + b3 3 + b4 1). NEXT: chunk-028 b5 SKU 33-40.

*(scoped к row Артикул=1755813685)*

---

## SKU 33/61 — Морозильный стол FROSTY GN 3100BT (ширина 700 мм) (Артикул 1905663779) — 🔴 RU=UA + Назв.мод (RU) UA-leak

**Поле:** Название модификации (RU)
**Было:** `Морозильний стіл FROSTY GN 3100BT (ширина 700 мм)`
**Стало:** `Морозильный стол FROSTY GN 3100BT (ширина 700 мм)`

**Поле:** Описание товара (RU)
**Было:** (полностью идентично UA — украинский текст)
**Стало:** (полный перевод RU тег-в-tag):

```
<h2>Трёхдверный морозильный стол FROSTY GN 3100BT без борта.</h2> <p>Может использоваться в составе кухонной линии. Ширина стола - 700 мм. Максимальная t&deg; окружающей среды +43&deg;С.</p> <ul>
<li>Столешница: нержавеющая сталь</li>
<li>Количество дверей: 3</li>
<li>Температурный режим: -18&deg; C....-22&deg; C</li>
<li>Тип охлаждения: динамический</li>
<li>Цифровой термостат</li>
<li>Объём (л): 417</li>
<li>Мощность: 0,65 кВт.</li>
<li>Подключение к электросети: 220 В</li>
<li>Габаритные размеры: 1795мм x 700мм x 860мм</li>
</ul>
```

*(blk триплет STANDARD — `desc UA==RU` **True** (🔴 RU=UA — RU = полная укр. копия тела); `nm_ua`==`nm_ru` `Морозильний стіл FROSTY GN 3100BT (ширина 700 мм)` (UA-leak; body-level `_has_ua` True via `Морозильний`/`стіл`); `nm_ru`!=`nazv_ru` genuine RU `Морозильный стол FROSTY GN 3100BT (ширина 700 мм)` → AUTO Назв.мод (RU) = genuine `nazv_ru`. **ВОСЬМОЙ blk триплет в chunk-028** + **прямой precedent SKU 23 FROSTY GN 2100BT 700мм b3** (same brand FROSTY, same Italian template `<h2>` + `<p>` + `<ul>`/9`<li>`, 3-door variant vs 2-door; 700мм wide variant consistent). **FROSTY НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. Описание (RU) — авторский полный перевод тег-в-tag (структура UA зеркалится 1:1; 1 `<h2>` + 1 `<p>` + 1 `<ul>` + 9 `<li>`, line-breaks `\n` после `<ul>` и между `<li>` preserve verbatim). SOFT применено к авторскому RU: `Трьохдверний морозильний стіл FROSTY GN 3100BT без борту.`→`Трёхдверный морозильный стол FROSTY GN 3100BT без борта.` (ё U+0451 в `Трёхдверный`; `борту`→`борта`); `Може використовуватися в складі кухонних лінії.` (UA typo — должно быть `кухонної лінії` sing. genit.; supplier source error) → `Может использоваться в составе кухонной линии.` (canonical RU sing. genit. — нормализуем UA typo, НЕ carry-over `кухонных`); `Ширина столу - 700 мм.`→`Ширина стола - 700 мм.` (hyphen `-` separator preserve — supplier choice; sing. genit. `столу`→`стола`); `Максимальна t&deg; навколишнього середовища +43&deg;С.`→`Максимальная t&deg; окружающей среды +43&deg;С.` (`t&deg;` entity сокращение preserve verbatim; `&deg;С` Cyr С postfix preserve); `Стільниця: нержавіюча сталь`→`Столешница: нержавеющая сталь`; `Кількість дверей: 3`→`Количество дверей: 3`; `Температурний режим: -18&deg; C....-22&deg; C`→`Температурный режим: -18&deg; C....-22&deg; C` (entity + Lat C + space-after-entity pattern preserve verbatim — precedent SKU 23 FROSTY b3 + SKU 27 Tecnodom b4 same Italian template; 4-точечное `....` preserve); `Тип охолодження: динамічний`→`Тип охлаждения: динамический`; `Цифровий термостат`→`Цифровой термостат`; `Об&#39;єм (л): 417`→`Объём (л): 417` (drop &#39; entity-apos; ё U+0451; parenthesized unit `(л)` preserve); `Потужність: 0,65 кВт.`→`Мощность: 0,65 кВт.` (decimal comma faithful); `Підключення до електромережі: 220 В`→`Подключение к электросети: 220 В` (Cyr В preserve); `Габаритні розміри: 1795x700x860`→`Габаритные размеры: 1795мм x 700мм x 860мм` (Policy B/C — UA Lat x already, supplier UA БЕЗ trailing `мм` единицы — добавляем `мм` слитно per axis; precedent SKU 23 FROSTY b3 same template). бренд/модель/`л`/`мм`/`В`/`кВт` НЕ переводим; HTML-entities `&deg;` (x4) + drop `&#39;` (x1). META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=1905663779)*

---

## SKU 34/61 — Стол морозильный Brillis BGL2-R290 (Артикул 2047034342) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg — `desc UA==RU` **False** (genuine отдельный корректный русский перевод поставщика, разная длина dr 2015 vs du 1986); `nm_ua`!=`nm_ru` (UA `Стіл морозильний Brillis BGL2-R290` vs RU `Стол морозильный Brillis BGL2-R290`); `nm_ru`==`nazv_ru` clean RU (char-level UA_ONLY=∅). **Brillis НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. LIVE-магазин Horoshop, genuine RU body НЕ переписываем (ячейки chunk-028-fixed без изменений). **ПЕРВЫЙ Brillis в chunk-028** + **ПЕРВЫЙ Brillis в проекте** — нет precedent batch/chunk; supplier-template family новый (отличный от Italian FROSTY/Forcar/Tecnodom + Danish Tefcold + Cooleq + REEDNEE seen so far). LIVE artefacts preserve verbatim из supplier dr genuine RU body (1986 chars UA / 2015 chars RU — RU чуть длиннее, что соответствует expected expansion от UA→RU). blknochg → ВСЕ артефакты `dr` (RU-side) НЕ трогаем; авторский перевод НЕ генерим. **Brillis НЕ ∈ НП-эксклюзив** (`Brillis` не содержит NP-key substring как word — ни одна из NP-key ключевых стрингов не появляется в `BRILLIS` через word-boundary regex). Код `Brillis BGL2-R290` Lat → consistent. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=2047034342)*

---

## SKU 35/61 — Стол морозильный Tefcold SK6310BT/+SP (Артикул 2053463226) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg — `desc UA==RU` **False** (genuine отдельный русский перевод поставщика, разная длина dr 1320 vs du 1340); `nm_ua` `Стіл морозильний Tefcold SK6310BT/+SP` (UA) != `nm_ru` `Стол морозильный Tefcold SK6310BT/+SP` (clean RU, == `nazv_ru`); `nm_ru` clean RU без UA-leak. **Tefcold НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. Substring `COLD` присутствует в `TEFCOLD`, но word-boundary regex `(?<![A-Za-zА-Яа-яЁё])COLD(?![A-Za-zА-Яа-яЁё])` НЕ срабатывает (`COLD` следует за `F` — буква, lookbehind fails). Durable constraint: `Tefcold/Forcold/Forcar НЕ SKIP` (substring `cold`/`for` ≠ standalone NP word). body-RU dr 1320 chars genuine отдельный supplier RU перевод (НЕ копия du) — **parallel pattern к b4 SKU 29 Tefcold SA910BT** same Danish supplier family. **ВТОРОЙ Tefcold в chunk-028** + **ВТОРОЙ Tefcold в проекте** (b4 SKU 29 — ПЕРВЫЙ). Danish supplier template family extended spec (длинная spec-таблица; supplier consistent internal format Danish family). SK6310BT/+SP variant — `/+SP` suffix добавочный к base SK6310BT (SKU 36 — base без `/+SP`). blknochg → ВСЕ артефакты `dr` (RU-side) НЕ трогаем; авторский перевод НЕ генерим. Код `Tefcold SK6310BT/+SP` Lat → consistent. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=2053463226)*

---

## SKU 36/61 — Стол морозильный Tefcold SK6310BT (Артикул 2053475845) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg — `desc UA==RU` **False** (genuine отдельный русский перевод поставщика, разная длина dr 1280 vs du 1302); `nm_ua` `Стіл морозильний Tefcold SK6310BT` (UA) != `nm_ru` `Стол морозильный Tefcold SK6310BT` (clean RU, == `nazv_ru`); `nm_ru` clean RU без UA-leak. **Tefcold НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. Substring `COLD` присутствует в `TEFCOLD`, но word-boundary regex `(?<![A-Za-zА-Яа-яЁё])COLD(?![A-Za-zА-Яа-яЁё])` НЕ срабатывает (`COLD` следует за `F` — буква, lookbehind fails). Durable constraint: `Tefcold/Forcold/Forcar НЕ SKIP` (substring `cold`/`for` ≠ standalone NP word). body-RU dr 1280 chars genuine отдельный supplier RU перевод → классификация = **blknochg** по body-level desc UA!=RU; cells stay unchanged. **ТРЕТИЙ Tefcold в chunk-028** + **ТРЕТИЙ Tefcold в проекте** + **mirror SKU 35 без `/+SP` suffix**: SKU 35 = SK6310BT/+SP variant (extended spec), SKU 36 = SK6310BT base (compact spec — 20 chars короче). Same Danish supplier template family как b4 SKU 29 Tefcold SA910BT + b5 SKU 35 Tefcold SK6310BT/+SP. blknochg → ВСЕ артефакты dr НЕ трогаем. Код `Tefcold SK6310BT` Lat → consistent. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=2053475845)*

---

## SKU 37/61 — Стол морозильный Forcar G-SS45BT (Артикул 2082652131) — 🔴 RU=UA + Назв.мод (RU) UA-leak

**Поле:** Название модификации (RU)
**Было:** `Стіл морозильний Forcar G-SS45BT`
**Стало:** `Стол морозильный Forcar G-SS45BT`

**Поле:** Описание товара (RU)
**Было:** (полностью идентично UA — украинский текст)
**Стало:** (полный перевод RU тег-в-tag):

```
<p>Морозильный стол Forcar G-SS45BT предназначен для хранения продуктов питания и полуфабрикатов на предприятиях общественного питания и торговли.</p> <p><strong>Характеристики:</strong></p> <ul>
<li>2 двери,</li>
<li>рабочая поверхность из нержавеющей стали,</li>
<li>объём 240 л,</li>
<li>1 решётчатая полка GN 1/1 с пластиковым покрытием в каждом отделении,</li>
<li>температура -12 ... -18 &deg; С (при tнар до +33 &deg; С),</li>
<li>внутренняя и внешняя отделка &ndash; нерж. сталь,</li>
<li>хладагент R290,</li>
<li>толщина теплоизоляции 55 мм,</li>
<li>статическое охлаждение,</li>
<li>электронная панель управления,</li>
<li>запускающееся вручную размораживание,</li>
<li>автоматическое испарение талой воды</li>
<li>Вес (нетто), кг: 82</li>
<li>Длина (нетто), мм: 943</li>
<li>Ширина (нетто), мм: 700</li>
<li>Высота (нетто), мм: 850</li>
<li>Мощность электрическая, кВт: 0.25</li>
<li>Подключение к электросети: 220V</li>
</ul>
```

*(blk триплет STANDARD — `desc UA==RU` **True** (🔴 RU=UA — RU = полная укр. копия тела, оба длиной 958); `nm_ua`==`nm_ru` `Стіл морозильний Forcar G-SS45BT` (UA-leak; body-level `_has_ua` True via `Стіл`/`морозильний`); `nm_ru`!=`nazv_ru` genuine RU `Стол морозильный Forcar G-SS45BT` → AUTO Назв.мод (RU) = genuine `nazv_ru`. **ДЕВЯТЫЙ blk триплет в chunk-028** + **parallel pattern within brand**: b3 SKU 21 Forcar GN3100BT — **blknochg** same brand (supplier дал genuine RU dr), SKU 37 Forcar G-SS45BT — **blk триплет** (supplier UA-only тело, magazine скопировал UA в RU cell). Same brand Forcar, разные supplier-paths — parallel к b3 SKU 20/23 FROSTY (b3 SKU 20 FROSTY 600мм — blknochg, b3 SKU 23 FROSTY 700мм — blk триплет; same brand разные ширина-variants и разные supplier-paths) и b4 SKU 27/28 Tecnodom (TF02MIDBT 2-door — blk триплет, TF03MIDBT 3-door — blknochg). **Forcar НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. Substring `FOR` присутствует в `FORCAR` как префикс, но word-boundary regex для NP-keys `HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA` не содержит standalone `FOR`. Durable constraint: `Tefcold/Forcold/Forcar НЕ SKIP`. Forcar — Italian supplier brand same template family как FROSTY/Tecnodom, но в данном случае supplier дал UA-only тело без отдельного RU перевода (magazine скопировал UA в RU cell). Описание (RU) — авторский полный перевод тег-в-tag (структура UA зеркалится 1:1; 1 `<p>` + 1 `<p>/<strong>` + 1 `<ul>` + 18 `<li>`, line-breaks `\n` после `<ul>` и между `<li>` preserve verbatim). SOFT применено к авторскому RU: `Морозильний стіл Forcar G-SS45BT призначений для зберігання продуктів харчування та напівфабрикатів на підприємствах громадського харчування та торгівлі.`→`Морозильный стол Forcar G-SS45BT предназначен для хранения продуктов питания и полуфабрикатов на предприятиях общественного питания и торговли.`; `<strong>Характеристики:</strong>` preserve verbatim; `2 двері,`→`2 двери,`; `робоча поверхня з нержавіючої сталі,`→`рабочая поверхность из нержавеющей стали,`; `об&#39;єм 240 л,`→`объём 240 л,` (drop &#39; entity-apos; ё U+0451); `1 гратчаста полиця GN 1/1 з пластиковим покриттям у кожному відділенні,`→`1 решётчатая полка GN 1/1 с пластиковым покрытием в каждом отделении,` (ё в `решётчатая`); `температура -12 ... -18 &deg; С (при tнар до +33 &deg; С),`→identical (Cyr С postfix; tнар сокращение preserve); `внутрішнє та зовнішнє оздоблення &ndash; нерж. сталь,`→`внутренняя и внешняя отделка &ndash; нерж. сталь,` (gender shift neut. UA `оздоблення`→fem. RU `отделка` — agreement с adj `внутренняя`/`внешняя`; `&ndash;` en-dash entity preserve — отличие от SKU 25/27 где `&mdash;` em-dash entity, supplier choice variant); `холодоагент R290,`→`хладагент R290,` (UA typo `холодоагент` с лишним `о` — должно быть `холодагент`; canonical RU `хладагент`; R290 refrigerant code preserve); `товщина термоізоляції 55 мм,`→`толщина теплоизоляции 55 мм,`; `статичне охолодження,`→`статическое охлаждение,`; `електронна панель управління,`→`электронная панель управления,`; `що запускається вручну розморожування,`→`запускающееся вручную размораживание,` (gerund-verb construction UA → adj-noun RU; voice preserve passive — `запускающееся` part. ср. рода согласовано с подразумеваемым `размораживание`); `автоматичне випаровування талої води`→`автоматическое испарение талой воды`; `Вага (нетто), кг: 82`→`Вес (нетто), кг: 82`; `Довжина (нетто), мм: 943`→`Длина (нетто), мм: 943`; `Ширина (нетто), мм: 700`→identical; `Висота (нетто), мм: 850`→`Высота (нетто), мм: 850`; `Потужність електрична, кВт: 0.25`→`Мощность электрическая, кВт: 0.25` (decimal **dot** preserve — supplier choice; **SKU 37-SPECIFIC** отличие от других SKU 33/38/39 которые используют decimal comma; per-axis supplier-format preserve verbatim); `Підключення до електромережі: 220V`→`Подключение к электросети: 220V` (**SKU 37-SPECIFIC** `220V` без пробела между значением и единицей + Lat V — supplier choice preserve verbatim; отличие от других SKU 33/38 которые используют `220 В` Cyr В с пробелом). бренд/модель/`R290`/`GN 1/1`/`л`/`мм`/`кг`/`кВт`/`V` НЕ переводим; HTML-entities `&deg;` (x2) + `&ndash;` (x1) + drop `&#39;` (x1). META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=2082652131)*

---

## SKU 38/61 — Стол морозильный Gooder GN2100ВТ (Артикул 2199328286) — 🔴 RU=UA + Назв.мод (RU) UA-leak

**Поле:** Название модификации (RU)
**Было:** `Стіл морозильний Gooder GN2100ВТ`
**Стало:** `Стол морозильный Gooder GN2100ВТ`

**Поле:** Описание товара (RU)
**Было:** (полностью идентично UA — украинский текст)
**Стало:** (полный перевод RU тег-в-tag):

```
<p>Стол холодильный низкотемпературный Gooder GN2100ВТ предназначен для хранения продуктов питания и полуфабрикатов на предприятиях общественного питания и торговли.</p> <p><strong>Характеристики:</strong></p> <ul>
<li>Относительная влажность : 55%;</li>
<li>Вес: 113 кг;</li>
<li>Вес в упаковке: 123 кг;</li>
<li>Диапазон температуры окружающей среды: +16 до +30 С&deg;;</li>
<li>Общий объём л: 282 л;</li>
<li>Количество полок: 2;</li>
<li>Класс энергопотребления: Е;</li>
<li>Климатический класс: 4;</li>
<li>Корпус: Нержавеющая сталь снаружи и внутри (AISI 304);</li>
<li>Страна производитель: Китай;</li>
<li>Размеры (ДxШxВ): 1360мм x 700мм x 860мм;</li>
<li>Система охлаждения: Динамическая;</li>
<li>Темп.режим: -18&deg;C....-22&deg;C;</li>
<li>Торговая марка: Gooder;</li>
<li>Автоматические двери,</li>
<li>Цифровой термостат;</li>
<li>Хладагент: R290;</li>
</ul>
```

*(blk триплет STANDARD — `desc UA==RU` **True** (🔴 RU=UA — RU = полная укр. копия тела, оба длиной 869); `nm_ua`==`nm_ru` `Стіл морозильний Gooder GN2100ВТ` (UA-leak; body-level `_has_ua` True via `Стіл`/`морозильний`); `nm_ru`!=`nazv_ru` genuine RU `Стол морозильный Gooder GN2100ВТ` → AUTO Назв.мод (RU) = genuine `nazv_ru`. **ДЕСЯТЫЙ blk триплет в chunk-028** + **ПЕРВЫЙ Gooder в chunk-028** + **ПЕРВЫЙ Gooder в проекте** — нет precedent batch/chunk; supplier-template family новый (характерные UA typos `Климатичний`/`Хлодоген`/`всередені` — supplier с слабой UA грамотностью; нормализуем к canonical RU). **Gooder НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. **Cyrillic `ВТ` в коде модели** `GN2100ВТ` — Cyr В U+0412 + Т U+0422 (НЕ Lat BT U+0042+U+0054) — preserve verbatim per supplier choice (verify byte-exact против nazv_ru). Описание (RU) — авторский полный перевод тег-в-tag (структура UA зеркалится 1:1; 1 `<p>` + 1 `<p>/<strong>` + 1 `<ul>` + 17 `<li>`, line-breaks `\n` после `<ul>` и между `<li>` preserve verbatim). SOFT применено к авторскому RU: `Стіл холодильний низькотемпературний Gooder GN2100ВТ призначений для зберігання продуктів харчування та напівфабрикатів на підприємствах громадського харчування та торгівлі.`→`Стол холодильный низкотемпературный Gooder GN2100ВТ предназначен для хранения продуктов питания и полуфабрикатов на предприятиях общественного питания и торговли.`; `<strong>Характеристики:</strong>` preserve verbatim; **space-colon** `Відносна вологість : 55%;`→`Относительная влажность : 55%;` (space перед двоеточием supplier choice preserve verbatim; trailing `;` preserve per-li throughout 17 li); `Вага: 113 кг;`→`Вес: 113 кг;`; `Вага в упаковці: 123 кг;`→`Вес в упаковке: 123 кг;`; `Діапазон температури навколишнього середовища: +16 до +30 С&deg;;`→`Диапазон температуры окружающей среды: +16 до +30 С&deg;;` (`С&deg;` postfix-Cyr-С + entity ORDER preserve — supplier choice verbatim, inverse order vs SKU 38 throughout); `Загальний об&#39;єм л: 282 л;`→`Общий объём л: 282 л;` (drop apos-entity; ё; `л` дублируется UA-style → RU preserve verbatim); `Кількість полок: 2;`→`Количество полок: 2;`; `Клас енергоспоживання: Е;`→`Класс энергопотребления: Е;`; **UA typo normalize**: `Климатичний клас: 4;` (UA typo — canonical UA `Кліматичний`) → `Климатический класс: 4;` (canonical RU; UA typo НЕ carry-over); **UA typo normalize**: `Корпус: Нержавіюча сталь ззовні і всередені (AISI 304);` (UA typo `всередені` — должно быть `всередині`) → `Корпус: Нержавеющая сталь снаружи и внутри (AISI 304);` (canonical RU; UA typo normalize); `Країна виробник: Китай;`→`Страна производитель: Китай;`; `Розміри (ДхШхВ): 1360х700х860;`→`Размеры (ДxШxВ): 1360мм x 700мм x 860мм;` (Cyr х U+0445 → Lat x U+0078 в header `ДxШxВ` AND в значении; Policy B/C `мм` слитно per axis; trailing `;` preserve); `Система охолодження: Динамічна;`→`Система охлаждения: Динамическая;`; `Темп.режим: -18&deg;C....-22&deg;C;`→identical (Lat C verbatim; 4-точечное `....` preserve; trailing `;`); `Торгова марка: Gooder;`→`Торговая марка: Gooder;`; `Автоматичні двері,`→`Автоматические двери,` (note: trailing `,` вместо `;` — supplier inconsistency внутри 17-li списка preserve verbatim); `Цифровий термостат;`→`Цифровой термостат;`; **UA typo normalize**: `Хлодоген: R290;` (UA typo — должно быть `Хладоген`/canonical RU `Хладагент`) → `Хладагент: R290;` (canonical RU; supplier UA-side typo `Хлодоген` нормализуем к правильному RU термину; **SKU 38-SPECIFIC** + paralleled SKU 39 same brand same typo). бренд/модель/`AISI 304`/`R290`/`л`/`кг`/`мм` НЕ переводим; Cyrillic `ВТ` (Cyr В+Т) в `GN2100ВТ` preserve verbatim; HTML-entities `&deg;` (x2) + drop `&#39;` (x1). META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=2199328286)*

---

## SKU 39/61 — Стол морозильный Gooder GN3100ВТ (Артикул 2199337912) — 🔴 RU=UA + Назв.мод (RU) UA-leak

**Поле:** Название модификации (RU)
**Было:** `Стіл морозильний Gooder GN3100ВТ`
**Стало:** `Стол морозильный Gooder GN3100ВТ`

**Поле:** Описание товара (RU)
**Было:** (полностью идентично UA — украинский текст)
**Стало:** (полный перевод RU тег-в-tag):

```
<p>Стол холодильный низкотемпературный Gooder GN3100ВТ предназначен для хранения продуктов питания и полуфабрикатов на предприятиях общественного питания и торговли.</p> <p><strong>Характеристики:</strong></p> <ul>
<li>Относительная влажность : 55%;</li>
<li>Вес: 130 кг;</li>
<li>Вес в упаковке: 140 кг;</li>
<li>Диапазон температуры окружающей среды: +16 до +30 С&deg;;</li>
<li>Общий объём л: 417 л;</li>
<li>Количество полок: 3;</li>
<li>Класс энергопотребления: Е;</li>
<li>Климатический класс: 4;</li>
<li>Корпус: Нержавеющая сталь снаружи и внутри (AISI 304);</li>
<li>Страна производитель: Китай;</li>
<li>Размеры (ДxШxВ): 1795мм x 700мм x 860мм;</li>
<li>Система охлаждения: Динамическая;</li>
<li>Потребление электроэнергии: 9,33 кВт/д;</li>
<li>Темп.режим: -18&deg;C....-22&deg;C;</li>
<li>Торговая марка: Gooder; Автоматические двери,</li>
<li>Цифровой термостат;</li>
<li>Хладагент: R290</li>
</ul>
```

*(blk триплет STANDARD — `desc UA==RU` **True** (🔴 RU=UA — RU = полная укр. копия тела, оба длиной 907); `nm_ua`==`nm_ru` `Стіл морозильний Gooder GN3100ВТ` (UA-leak; body-level `_has_ua` True); `nm_ru`!=`nazv_ru` genuine RU `Стол морозильный Gooder GN3100ВТ` → AUTO Назв.мод (RU) = genuine `nazv_ru`. **ОДИННАДЦАТЫЙ blk триплет в chunk-028** + **ВТОРОЙ Gooder в chunk-028** + **mirror SKU 38 3-door variant** (SKU 38 = 2-door GN2100ВТ, SKU 39 = 3-door GN3100ВТ same brand same supplier-template). **Gooder НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. **Cyrillic `ВТ` в `GN3100ВТ`** (Cyr В+Т) preserve verbatim. Описание (RU) — авторский полный перевод тег-в-tag (1 `<p>` + 1 `<p>/<strong>` + 1 `<ul>` + 17 `<li>`, mirror SKU 38 + diffs). **Diffs vs SKU 38**: (1) `Вага: 130 кг;` (vs SKU 38 113) → `Вес: 130 кг;`; (2) `Вага в упаковці: 140 кг;` (vs SKU 38 123) → `Вес в упаковке: 140 кг;`; (3) `Загальний об&#39;єм л: 417 л;` (vs SKU 38 282) → `Общий объём л: 417 л;`; (4) `Кількість полок: 3;` (vs SKU 38 2) → `Количество полок: 3;`; (5) `Розміри (ДхШхВ): 1795х700х860;` (vs SKU 38 1360х700х860) → `Размеры (ДxШxВ): 1795мм x 700мм x 860мм;`; (6) **INSERT after Розміри** `<li>Споживання електроенергії: 9,33 кВт/д;</li>` → `<li>Потребление электроэнергии: 9,33 кВт/д;</li>` (decimal comma; `кВт/д` единица preserve verbatim; **SKU 39-SPECIFIC** extra li отсутствует в SKU 38 2-door); (7) **COLLAPSE li** (как у supplier UA source): `<li>Торгова марка: Gooder; Автоматичні двері,</li>` (две сущности в одном li, разделены `;` — supplier collapse choice SKU 39 vs separate li в SKU 38) → `<li>Торговая марка: Gooder; Автоматические двери,</li>` (preserve supplier collapse verbatim); (8) **LAST li без trailing `;`** `<li>Хлодоген: R290</li>` (vs SKU 38 `Хлодоген: R290;` с `;` — supplier inconsistency mirror 39 vs 38) → `<li>Хладагент: R290</li>` (UA typo `Хлодоген` normalize к canonical RU `Хладагент` same SKU 38; БЕЗ trailing `;` per SKU 39 supplier choice). Все остальные li mirror SKU 38 verbatim translations. SOFT applied same as SKU 38: space-colon `Відносна вологість :` preserve; UA typos `Климатичний`/`всередені`/`Хлодоген` normalize к canonical RU; Cyr х U+0445 → Lat x U+0078 в `ДxШxВ` AND в `1795x700x860`; Policy B/C `мм` слитно per axis; `&deg;C` Lat C + 4-точечное preserve; trailing-comma в `Автоматические двери,` preserve. бренд/модель/`AISI 304`/`R290`/`л`/`кг`/`мм`/`кВт/д` НЕ переводим; Cyrillic `ВТ` в `GN3100ВТ` preserve; HTML-entities `&deg;` (x2) + drop `&#39;` (x1). META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=2199337912)*

---

## SKU 40/61 — Морозильный стол FAGOR MFN-135 EXP (Артикул 2204095479) — SKIP-НП (бренд НП-эксклюзив, тело из фида НП позже)

**Бренд:** Fagor (НП-эксклюзивный — forward-only SKIP-правило)
**Поле:** Название модификации (RU)
**Было:** (ячейка не трогается — тело из фида НП позже)
**Стало:** не трогаем (SKIP-НП — тело из фида НП позже)

**Поле:** Описание товара (RU)
**Было:** (ячейка не трогается — тело из фида НП позже)
**Стало:** не трогаем (SKIP-НП — тело из фида НП позже)

*(SKIP-НП — `brand`=`Fagor` ∈ {FAGOR/Fagor/Фагор} word-boundary NP-hit → forward-only SKIP-правило: тело из фида НП позже, ячейки chunk-028-fixed.xlsx НЕ трогаем (Назв.мод RU + Описание RU без изменений). **Fagor ∈ НП-эксклюзивный список** (word-boundary NP-hit найден в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}) → forward-only SKIP-правило: тело из фида НП позже, ячейки chunk-028-fixed.xlsx не трогаем (Назв.мод RU + Описание RU без изменений). **ВОСЬМОЙ SKIP-НП в chunk-028** + **ПЕРВЫЙ Fagor в chunk-028** + **ПЕРВЫЙ Fagor в проекте** — нет precedent batch/chunk; supplier-template family новый. Source signature: `du==dr` True 628/628 + `nm_ua`!=`nm_ru` desync (UA `Морозильний стіл FAGOR MFN-135 EXP` allcaps brand vs RU `Стіл морозильний Fagor 2-х дверний MFN-135 EXP` Titlecase brand + UA-leak `Стіл морозильний` + UA `дверний` suffix); **ОБА nm-cells содержат UA-leak** (UA `Морозильний стіл` в nm_ua + UA-leak `Стіл морозильний` + UA `дверний` в nm_ru); `nazv_ru` clean RU `Морозильный стол FAGOR MFN-135 EXP` — но brand-rule overrides signature, SKIP-НП **НЕ правим** ячейки (тело из фида НП позже всё перепишет, включая UA-leak в nm_ru + 2-х дверний). Кумул. SKIP-НП chunk-028 = 8 (после SKU 40). META always faithful. Открытых вопросов 0.)*

**Наблюдения по батчу SKU 33-40 (40/61) — chunk-028 (батч-морозильные столы FROSTY ×1 + Brillis ×1 + Tefcold ×2 + Forcar ×1 + Gooder ×2 + Fagor SKIP-НП ×1; раздел `Холодильне та морозильне обладнання/Морозильні столи` — продолжение b4 SKU 25-32):** **blk триплет 4 (SKU 33 FROSTY GN 3100BT 700мм + SKU 37 Forcar G-SS45BT + SKU 38 Gooder GN2100ВТ + SKU 39 Gooder GN3100ВТ). blknotrip 0. blkv 0. blknochg 3 (SKU 34 Brillis BGL2-R290 + SKU 35 Tefcold SK6310BT/+SP + SKU 36 Tefcold SK6310BT — LIVE Horoshop genuine RU). blknochgeq 0. SKIP-НП 1 (SKU 40 Fagor MFN-135 EXP — ВОСЬМОЙ SKIP-НП в chunk-028, ПЕРВЫЙ Fagor).** SKU 33 `1905663779` FROSTY GN 3100BT (ширина 700 мм) — **blk триплет** **ВОСЬМОЙ blk триплет в chunk-028** + **прямой precedent SKU 23 FROSTY GN 2100BT 700мм b3** (same brand FROSTY same Italian template `<h2>`+`<p>`+ul/9li, 3-door variant vs 2-door, 700мм wide variant consistent): `desc UA==RU` True 🔴, `nm_ua==nm_ru` UA-leak `Морозильний стіл FROSTY GN 3100BT (ширина 700 мм)`, `nm_ru!=nazv_ru` → AUTO Назв.мод RU; Описание RU авторский 1:1; UA typo `кухонних лінії` (должно быть `кухонної лінії` sing. genit.) → canonical RU `кухонной линии`; SOFT: ё в `Трёхдверный`/`Объём`, drop apos-entity, Policy B/C `1795мм x 700мм x 860мм` (precedent SKU 23 b3), `t&deg;` сокращение + Lat C + 4-точечное `....` (Italian template family). FROSTY **НЕ ∈ НП-эксклюзив**. SKU 34 `2047034342` Brillis BGL2-R290 — **blknochg** LIVE Horoshop (supplier RU dr genuine 2015 vs UA du 1986 — RU чуть длиннее, expected expansion; nm_ru clean RU без UA-leak; **ПЕРВЫЙ Brillis в проекте**; supplier-template family новый — НЕ Italian/Danish/Cooleq/REEDNEE seen so far; НЕ переписываем). **Brillis НЕ ∈ НП-эксклюзив**. SKU 35 `2053463226` Tefcold SK6310BT/+SP — **blknochg** LIVE Horoshop (supplier RU dr genuine 1320 vs UA du 1340; nm_ru clean RU `Стол морозильный Tefcold SK6310BT/+SP` (==`nazv_ru`, без UA-leak); body-RU genuine отдельный supplier перевод → классификация blknochg по body-level desc UA!=RU; **parallel pattern к b4 SKU 29 Tefcold SA910BT** same Danish supplier family; SK6310BT/+SP — extended variant с `/+SP` suffix; cells stay unchanged). **Tefcold НЕ ∈ НП-эксклюзив** (substring `COLD` в `TEFCOLD` НЕ word-boundary NP-hit; durable constraint). SKU 36 `2053475845` Tefcold SK6310BT — **blknochg** LIVE Horoshop **mirror SKU 35 без `/+SP` suffix** (dr 1280 vs du 1302; nm_ru clean RU same SKU 35; compact spec — 20 chars короче чем SKU 35 extended). **Tefcold НЕ ∈ НП-эксклюзив**. SKU 37 `2082652131` Forcar G-SS45BT — **blk триплет** **ДЕВЯТЫЙ blk триплет в chunk-028** + **parallel pattern within brand Forcar**: b3 SKU 21 Forcar GN3100BT — **blknochg** same brand (supplier дал genuine RU dr), SKU 37 Forcar G-SS45BT — **blk триплет** (supplier UA-only тело, magazine скопировал UA в RU cell; `desc UA==RU` True 🔴, `nm_ua==nm_ru` UA-leak; Описание RU авторский 1`<p>`+1`<p>/<strong>`+ul/18li 1:1; **SKU 37-SPECIFIC**: decimal **dot** `0.25` (vs SKU 33/38/39 comma) + `220V` Lat V без пробела (vs SKU 33/38 `220 В` Cyr В с пробелом) — supplier choice preserve verbatim; `холодоагент`→`хладагент` UA typo normalize; `&ndash;` en-dash entity preserve — отличие от SKU 25/27 `&mdash;` em-dash; gerund-verb `що запускається вручну розморожування`→adj-noun RU `запускающееся вручную размораживание`). **Forcar НЕ ∈ НП-эксклюзив** (substring `FOR` не standalone NP key; durable constraint `Tefcold/Forcold/Forcar НЕ SKIP`). SKU 38 `2199328286` Gooder GN2100ВТ — **blk триплет** **ДЕСЯТЫЙ blk триплет** + **ПЕРВЫЙ Gooder в chunk-028** + **ПЕРВЫЙ Gooder в проекте**: 1`<p>` + 1`<p>/<strong>` + ul/17li; **Cyrillic `ВТ` в коде модели** (Cyr В U+0412 + Т U+0422, не Lat BT) preserve verbatim; supplier UA typos многократные `Климатичний`/`всередені`/`Хлодоген` (canonical UA `Кліматичний`/`всередині`/`Хладоген`) → нормализуем к canonical RU `Климатический`/`внутри`/`Хладагент` (НЕ carry-over supplier typos); space-colon `Відносна вологість :` preserve verbatim supplier choice; `С&deg;` inverse-order postfix-Cyr-С + entity preserve supplier choice (vs `&deg;С` order в SKU 33/40); Policy B/C `1360мм x 700мм x 860мм` Cyr х→Lat x в header `ДxШxВ` AND value. **Gooder НЕ ∈ НП-эксклюзив**. SKU 39 `2199337912` Gooder GN3100ВТ — **blk триплет** **ОДИННАДЦАТЫЙ blk триплет** + **ВТОРОЙ Gooder** **mirror SKU 38 3-door variant** + **SKU 39-SPECIFIC diffs**: extra li `Споживання електроенергії: 9,33 кВт/д;`→`Потребление электроэнергии: 9,33 кВт/д;` (decimal comma; `кВт/д` единица preserve verbatim); collapsed li `Торгова марка: Gooder; Автоматичні двері,` (две сущности в одном li — supplier choice SKU 39 vs separate li в SKU 38); LAST li без trailing `;`: `Хлодоген: R290` → `Хладагент: R290` (supplier inconsistency mirror 39 vs 38 + UA typo normalize); weight/dims diffs 130/140/417/3/1795х700х860 (vs 113/123/282/2/1360х700х860 SKU 38). SKU 40 `2204095479` Fagor MFN-135 EXP — **SKIP-НП** (brand=`Fagor` ∈ {FAGOR/Fagor/Фагор} NP-hit; **ВОСЬМОЙ SKIP-НП в chunk-028** + **ПЕРВЫЙ Fagor в проекте**; source `du==dr` True 628/628 + `nm_ua!=nm_ru` desync ALLCAPS FAGOR vs Titlecase Fagor+`2-х дверний` UA suffix — ОБА nm-cells имеют UA-leak; cells unchanged — тело из фида НП позже всё перепишет). **Открытых вопросов по батчу: 0** (b1 0 + b2 0 + b3 0 + b4 0 + b5 0; ledger chunk-028 = 0). Кумулятивно chunk-028 = **0** (questions.md chunk-028 пока НЕ создаём — нет OQ; supplier UA typos `Климатичний`/`всередені`/`Хлодоген`/`кухонних лінії` → soft normalize к canonical RU inline, не нумеруются). Кумулятивно SKIP-НП chunk-028 = **8** (b1 0 + b2 3 + b3 3 + b4 1 + b5 1). NEXT: chunk-028 b6 SKU 41-48.

*(scoped к row Артикул=2204095479)*

---

## SKU 41/61 — Стол морозильный GoodFood GF-GN2100BT-HC (Артикул 2212710231) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg — `desc UA==RU` **False** (genuine отдельный корректный русский перевод поставщика, разная длина dr 821 vs du 790); `nm_ua`!=`nm_ru` (UA `Стіл морозильний GoodFood GF-GN2100BT-HC` vs RU `Стол морозильный GoodFood GF-GN2100BT-HC`); `nm_ru`==`nazv_ru` clean RU (char-level UA_ONLY=∅). **GoodFood НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. Substring `FOOD`/`GOOD` НЕ в NP-keys (NP-keys = HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA standalone words; `GOOD`/`FOOD` отсутствуют как standalone NP-keys). LIVE-магазин Horoshop, genuine RU body НЕ переписываем (ячейки chunk-028-fixed без изменений). **ПЕРВЫЙ GoodFood в chunk-028** + **ПЕРВЫЙ GoodFood в проекте** — нет precedent batch/chunk; supplier-template family новый (отличный от Italian FROSTY/Forcar/Tecnodom + Danish Tefcold + Cooleq + REEDNEE + Brillis + Gooder seen so far). LIVE artefacts preserve verbatim из supplier dr genuine RU body (790 chars UA / 821 chars RU — RU чуть длиннее, что соответствует expected expansion от UA→RU). blknochg → ВСЕ артефакты `dr` (RU-side) НЕ трогаем; авторский перевод НЕ генерим. Код `GoodFood GF-GN2100BT-HC` Lat → consistent. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=2212710231)*

---

## SKU 42/61 — Стол морозильный GoodFood GF-GN3100BT-HC (Артикул 2212715970) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg — `desc UA==RU` **False** (genuine отдельный русский перевод поставщика, разная длина dr 842 vs du 794); `nm_ua`!=`nm_ru`; `nm_ru`==`nazv_ru` clean RU без UA-leak. **GoodFood НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. Substring `FOOD`/`GOOD` НЕ в NP-keys (NP-keys = HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA standalone words; `GOOD`/`FOOD` отсутствуют как standalone NP-keys). LIVE Horoshop genuine RU body НЕ переписываем. **ВТОРОЙ GoodFood в chunk-028** + **mirror SKU 41 3-door variant** (SKU 41 = 2-door GF-GN2100BT-HC, SKU 42 = 3-door GF-GN3100BT-HC same brand same supplier-template family — GF-GN21/31 pattern параллель к Tefcold SK6310BT/SK6310BT/+SP пары SKU 35/36 b5 mirror без/с suffix). Supplier RU dr 842 chars vs SKU 41 dr 821 — slight expansion для 3-door variant (доп. spec для extra двери). blknochg → ВСЕ артефакты dr НЕ трогаем; авторский перевод НЕ генерим. Код `GoodFood GF-GN3100BT-HC` Lat → consistent. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=2212715970)*

---

## SKU 43/61 — Стол морозильный Fagor MFN-180 EXP (Артикул 2282947003) — SKIP-НП (бренд НП-эксклюзив, тело из фида НП позже)

**Бренд:** Fagor (НП-эксклюзивный — forward-only SKIP-правило)
**Поле:** Название модификации (RU)
**Было:** (ячейка не трогается — тело из фида НП позже)
**Стало:** не трогаем (SKIP-НП — тело из фида НП позже)

**Поле:** Описание товара (RU)
**Было:** (ячейка не трогается — тело из фида НП позже)
**Стало:** не трогаем (SKIP-НП — тело из фида НП позже)

*(SKIP-НП — `brand`=`Fagor` ∈ {FAGOR/Fagor/Фагор} word-boundary NP-hit → forward-only SKIP-правило: тело из фида НП позже, ячейки chunk-028-fixed.xlsx НЕ трогаем (Назв.мод RU + Описание RU без изменений). **Fagor ∈ НП-эксклюзивный список** (word-boundary NP-hit найден в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}) → forward-only SKIP-правило: тело из фида НП позже, ячейки chunk-028-fixed.xlsx не трогаем (Назв.мод RU + Описание RU без изменений). **ДЕВЯТЫЙ SKIP-НП в chunk-028** + **ВТОРОЙ Fagor в chunk-028** + **ВТОРОЙ Fagor в проекте** после b5 SKU 40 MFN-135 EXP ПЕРВЫЙ Fagor. SKU 43 MFN-180 EXP — mirror SKU 40 MFN-135 EXP **same suffix EXP**, 180 vs 135 size variant внутри одной Fagor MFN-серии. Source signature: `du==dr` True 587/587 + `nm_ua`!=`nm_ru` desync (UA `Стіл морозильний Fagor MFN-180 EXP` без extra qualifiers vs RU `Стіл морозильний Fagor 3-х дверний MFN-180 EXP` Titlecase brand + UA-leak `Стіл морозильний` + UA `3-х дверний` insertion — ВТОРОЙ Fagor mirror SKU 40 pattern UA-leak в nm_ru с добавленным `3-х дверний`); ОБА nm-cells содержат UA-leak (UA `Стіл морозильний` в nm_ua + UA-leak `Стіл морозильний` + UA `3-х дверний` в nm_ru); `nazv_ru` clean RU `Стол морозильный Fagor MFN-180 EXP` — но brand-rule overrides signature, SKIP-НП НЕ правим ячейки (тело из фида НП позже всё перепишет, включая UA-leak в nm_ru + 3-х дверний). META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=2282947003)*

---

## SKU 44/61 — Стол морозильный Fagor CCN-2G GR (Артикул 2375839553) — SKIP-НП (бренд НП-эксклюзив, тело из фида НП позже)

**Бренд:** Fagor (НП-эксклюзивный — forward-only SKIP-правило)
**Поле:** Название модификации (RU)
**Было:** (ячейка не трогается — тело из фида НП позже)
**Стало:** не трогаем (SKIP-НП — тело из фида НП позже)

**Поле:** Описание товара (RU)
**Было:** (ячейка не трогается — тело из фида НП позже)
**Стало:** не трогаем (SKIP-НП — тело из фида НП позже)

*(SKIP-НП — `brand`=`Fagor` NP-hit word-boundary. **Fagor ∈ НП-эксклюзивный список** (word-boundary NP-hit найден в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}) → forward-only SKIP-правило: тело из фида НП позже, ячейки chunk-028-fixed.xlsx не трогаем (Назв.мод RU + Описание RU без изменений). **ДЕСЯТЫЙ SKIP-НП в chunk-028** + **ТРЕТИЙ Fagor в chunk-028** + **ТРЕТИЙ Fagor в проекте**. SKU 44 CCN-2G GR — другая Fagor series **CCN** (Cool/Cooling-Cabinet-Negative или similar Fagor model naming convention), отличается от MFN-серии SKU 40/43 — same brand Fagor разные supplier-series. Source signature: `du!=dr` 449/440 supplier дал отдельный RU body (vs SKU 40/43 `du==dr` True) — НО brand=Fagor NP-hit → SKIP-НП **независимо** от состояния ячеек (`du!=dr` body-level не релевантен для brand-rule SKIP-НП, ячейки всё равно перепишутся фидом НП позже); `nm_ua`!=`nm_ru` (UA `Стіл морозильний Fagor CCN-2G GR` vs RU `Стол морозильный Fagor CCN-2G GR` — nm_ru clean RU без UA-leak); `nazv_ru` clean RU — но brand-rule overrides signature, cells unchanged. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=2375839553)*

---

## SKU 45/61 — Стол морозильный Brillis СN2100 (Артикул 2448658777) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg — `desc UA==RU` **False** (genuine отдельный русский перевод поставщика; **same length** dr 934 == du 934 char-count match, НО content differs — supplier RU body отдельный, не копия UA — verified `same=False` в probe); `nm_ua`!=`nm_ru`; `nm_ru`==`nazv_ru` clean RU без UA-leak. **Brillis НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. **ВТОРОЙ Brillis в chunk-028** + **ВТОРОЙ Brillis в проекте** (b5 SKU 34 Brillis BGL2-R290 — ПЕРВЫЙ). SKU 45 СN2100 — **другая Brillis series** distinct от BGL2-R290: **Cyrillic С** U+0421 в коде model `СN2100` (НЕ Latin C U+0043) — preserve verbatim per supplier choice (verify byte-exact против nazv_ru `Стол морозильный Brillis СN2100`). 2-door variant (mirror SKU 46 3-door); same supplier-template family как SKU 34 Brillis (новый supplier-template family, отличный от Italian/Danish/Cooleq/REEDNEE/GoodFood/Gooder seen so far). **Edge case**: dr.len == du.len 934 **в точности равны** — supplier создал RU body почти равной длины с UA (что нетипично; обычно RU ~10-30 chars длиннее UA), но `same=False` → content differs → genuine separate RU body. blknochg → ВСЕ артефакты dr НЕ трогаем. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=2448658777)*

---

## SKU 46/61 — Стол морозильный Brillis СN3100 (Артикул 2448660375) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg — `desc UA==RU` **False** (genuine; same length dr 934 == du 934 НО content differs — verified `same=False`); `nm_ua`!=`nm_ru`; `nm_ru`==`nazv_ru` clean RU без UA-leak. **Brillis НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. **ТРЕТИЙ Brillis в chunk-028** + **ТРЕТИЙ Brillis в проекте** + **mirror SKU 45 3-door variant** (SKU 45 = 2-door СN2100, SKU 46 = 3-door СN3100). **Cyrillic С** U+0421 в коде `СN3100` preserve verbatim — same convention SKU 45. Same supplier-template family как SKU 45 + SKU 34 b5 (Brillis новый supplier-family). Edge case dr.len == du.len 934 — supplier создал RU body равной длины с UA (parallel SKU 45 pattern); content differs → genuine separate RU. blknochg → ВСЕ артефакты dr НЕ трогаем. Код `Brillis СN3100` (Cyr С) → consistent с SKU 45. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=2448660375)*

---

## SKU 47/61 — Стол морозильный Tecnodom TF02MIDBTAL (Артикул 2545751551) — 🔴 RU=UA + Назв.мод (RU) UA-leak

**Поле:** Название модификации (RU)
**Было:** `Стіл морозильний Tecnodom TF02MIDBTAL`
**Стало:** `Стол морозильный Tecnodom TF02MIDBTAL`

**Поле:** Описание товара (RU)
**Было:** (полностью идентично UA — украинский текст)
**Стало:** (полный перевод RU тег-в-tag):

```
<p>Стол морозильный Tecnodom TF02MIDBTAL.</p> <p><strong>Технические характеристики:</strong></p> <ul>
<li>Столешница и корпус: нержавеющая сталь.</li>
<li>Количество дверей: 2.</li>
<li>1 полка GN1/1 в каждом отделении.</li>
<li>Температурный режим: -18&deg; C....-22 &deg;C.</li>
<li>Хладагент R452А.</li>
<li>Электронный блок управления.</li>
<li>Автоматическое размораживание.</li>
<li>Полезный объём: 310 л</li>
<li>Мощность: 0,66 кВт.</li>
<li>Подключение к электросети: 220 В</li>
<li>Габаритные размеры: 1420мм x 700мм x 1020мм</li>
</ul>
```

*(blk триплет STANDARD — `desc UA==RU` **True** (🔴 RU=UA — RU = полная укр. копия тела, оба длиной 548); `nm_ua`==`nm_ru` `Стіл морозильний Tecnodom TF02MIDBTAL` (UA-leak; body-level `_has_ua` True via `Стіл`/`морозильний`); `nm_ru`!=`nazv_ru` genuine RU `Стол морозильный Tecnodom TF02MIDBTAL` → AUTO Назв.мод (RU) = genuine `nazv_ru`. **ДВЕНАДЦАТЫЙ blk триплет в chunk-028** + **ВТОРОЙ Tecnodom blk триплет в chunk-028** + **AL/ALU variant к base SKU 27 TF02MIDBT b4** (SKU 27 ПЕРВЫЙ Tecnodom blk триплет): same brand Tecnodom same Italian template family, **разные модели и разные supplier-templates** — SKU 27 TF02MIDBT (1h2+3p+1ul/9li, `&mdash;` em-dash + `&deg;` x2 + `&#39;` HTML entities) vs SKU 47 TF02MIDBTAL (1p+1p/strong+1ul/11li, no h2, no `&mdash;` — другая supplier-template structure для AL variant; **отличие**: 11 li vs 9 li, 1 p prefix vs h2+3 p prefix). **Tecnodom НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. Описание (RU) — авторский полный перевод тег-в-tag (структура UA зеркалится 1:1; 1 `<p>` + 1 `<p>/<strong>` + 1 `<ul>` + 11 `<li>`, line-breaks `\n` после `<ul>` и между `<li>` preserve verbatim). SOFT применено к авторскому RU: `<p>Стіл морозильний Tecnodom TF02MIDBTAL.</p>`→`<p>Стол морозильный Tecnodom TF02MIDBTAL.</p>`; `<p><strong>Технічні характеристики:</strong></p>`→`<p><strong>Технические характеристики:</strong></p>`; `Стільниця та корпус: нержавіюча сталь.`→`Столешница и корпус: нержавеющая сталь.` (UA `та`→`и`; gender shift `нержавіюча`→`нержавеющая`); `Кількість дверей: 2.`→`Количество дверей: 2.`; **UA typo normalize**: `1 поличка GN1/1 в кожному відділені.` (UA typo `відділені` — canonical UA `відділенні`) → `1 полка GN1/1 в каждом отделении.` (canonical RU; `поличка`→`полка` lexical; `GN1/1` gastronorm format preserve); `Температурний режим: -18&deg; C....-22 &deg;C.`→identical (Lat C verbatim; 4-точечное `....` preserve; **supplier asymmetric spacing** `-18&deg; C` space-AFTER-entity vs `-22 &deg;C` space-BEFORE-entity preserve verbatim — supplier inconsistency внутри одного li); **UA typo normalize**: `Холодоагент R452А.` (UA typo — canonical UA `Холодагент`, лишний `о`) → `Хладагент R452А.` (canonical RU; R452А refrigerant code preserve verbatim — Cyr А U+0410 после `R452`); `Електронний блок управління.`→`Электронный блок управления.`; `Автоматичне розморожування.`→`Автоматическое размораживание.`; `Корисний об&#39;єм: 310 л`→`Полезный объём: 310 л` (drop &#39; entity-apos; ё U+0451; **no trailing period** preserve); `Потужність: 0,66 кВт.`→`Мощность: 0,66 кВт.` (decimal comma; trailing period preserve); `Під&#39;єднання до електромережі: 220 В`→`Подключение к электросети: 220 В` (drop &#39; в `Під'єднання`→`Подключение`; Cyr В preserve; **no trailing period**); `Габаритні розміри: 1420x700x1020 мм`→`Габаритные размеры: 1420мм x 700мм x 1020мм` (Policy B/C — UA Lat x already; supplier UA с trailing single `мм` — drop trailing + добавляем `мм` слитно per axis; **same pattern как b4 SKU 27 TF02MIDBT** `1420x715x920 мм`→`1420мм x 715мм x 920мм` — Tecnodom Italy template-family policy consistency). бренд/модель/`R452А`/`GN1/1`/`л`/`мм`/`В`/`кВт` НЕ переводим; HTML-entities `&deg;` (x2) + drop `&#39;` (x2). META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=2545751551)*

---

## SKU 48/61 — Стол морозильный четырехдверный GGM GTS227, (2223х700 мм) (Артикул 508918206) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg — `desc UA==RU` **False** (genuine отдельный русский перевод поставщика, разная длина dr 837 vs du 815); `nm_ua`!=`nm_ru` (UA `Стіл морозильний чотиридверний GGM GTS227, (2223х700 мм)` vs RU `Стол морозильный четырехдверный GGM GTS227, (2223х700 мм)` — Cyr х U+0445 в `2223х700` mirror UA/RU); `nm_ru`==`nazv_ru` clean RU без UA-leak. **GGM Gastro International НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. Substring `GASTRO`/`INTERNATIONAL` НЕ в NP-keys standalone; full brand string не матчит ни одну NP-key через word-boundary regex. LIVE Horoshop genuine RU body НЕ переписываем. **ПЕРВЫЙ GGM Gastro International в chunk-028** + **ПЕРВЫЙ GGM в проекте** — нет precedent batch/chunk; supplier-template family новый (отличный от Italian FROSTY/Forcar/Tecnodom + Danish Tefcold + Cooleq + REEDNEE + Brillis + GoodFood + Gooder seen so far). Brand string `GGM Gastro International` — full multi-word brand name (vs short single-word brands seen ранее); `GASTRO`/`INTERNATIONAL` substrings НЕ в NP-keys standalone, word-boundary regex не матчит. **4-door variant** model code `GGM GTS227` с inline-dims `2223х700 мм` в самом nazv_ru/nm — необычный паттерн (dims в имени продукта vs обычное отдельное поле). LIVE artefacts preserve verbatim (815 chars UA / 837 chars RU — RU чуть длиннее expected expansion). blknochg → ВСЕ артефакты dr НЕ трогаем; авторский перевод НЕ генерим. META always faithful. Открытых вопросов 0.)*

**Наблюдения по батчу SKU 41-48 (48/61) — chunk-028 (батч-морозильные столы GoodFood ×2 + Fagor SKIP-НП ×2 + Brillis ×2 + Tecnodom ×1 + GGM Gastro International ×1; раздел `Холодильне та морозильне обладнання/Морозильні столи` — продолжение b5 SKU 33-40):** **blk триплет 1 (SKU 47 Tecnodom TF02MIDBTAL). blknotrip 0. blkv 0. blknochg 5 (SKU 41 GoodFood GF-GN2100BT-HC + SKU 42 GoodFood GF-GN3100BT-HC + SKU 45 Brillis СN2100 + SKU 46 Brillis СN3100 + SKU 48 GGM Gastro International GGM GTS227 — LIVE Horoshop genuine RU). blknochgeq 0. SKIP-НП 2 (SKU 43 Fagor MFN-180 EXP + SKU 44 Fagor CCN-2G GR — ДЕВЯТЫЙ-ДЕСЯТЫЙ SKIP-НП в chunk-028, ВТОРОЙ-ТРЕТИЙ Fagor в проекте).** SKU 41 `2212710231` GoodFood GF-GN2100BT-HC — **blknochg** LIVE Horoshop (**ПЕРВЫЙ GoodFood в проекте**; supplier-template family новый — НЕ Italian/Danish/Cooleq/REEDNEE/Brillis/Gooder seen so far; supplier RU dr genuine 821 vs UA du 790; nm_ru clean RU без UA-leak; НЕ переписываем). **GoodFood НЕ ∈ НП-эксклюзив** (substring `GOOD`/`FOOD` НЕ standalone NP key). SKU 42 `2212715970` GoodFood GF-GN3100BT-HC — **blknochg** LIVE Horoshop **mirror SKU 41 3-door variant** (SKU 41 = 2-door GF-GN2100BT-HC, SKU 42 = 3-door GF-GN3100BT-HC same brand same supplier-template — GF-GN21/31 pattern); supplier RU dr 842 vs SKU 41 dr 821 — slight expansion для 3-door extra spec; nm_ru clean RU без UA-leak; cells unchanged. SKU 43 `2282947003` Fagor MFN-180 EXP — **SKIP-НП** (brand=`Fagor` ∈ {FAGOR/Fagor/Фагор} NP-hit; **ДЕВЯТЫЙ SKIP-НП в chunk-028** + **ВТОРОЙ Fagor в проекте** + **mirror SKU 40 MFN-135 EXP b5 ПЕРВЫЙ Fagor**: 180 vs 135 size variant внутри одной Fagor MFN-серии same suffix EXP; source `du==dr` True 587/587 + `nm_ua!=nm_ru` desync (UA simple vs RU Titlecase Fagor+UA-leak `Стіл морозильний`+UA `3-х дверний` insertion — mirror SKU 40 pattern UA-leak в nm_ru с добавленным `3-х дверний`); ОБА nm-cells UA-leak; cells unchanged — тело из фида НП позже всё перепишет). SKU 44 `2375839553` Fagor CCN-2G GR — **SKIP-НП** (brand=Fagor NP-hit; **ДЕСЯТЫЙ SKIP-НП** + **ТРЕТИЙ Fagor**; **CCN-серия** distinct от MFN-серии SKU 40/43 — Fagor разные supplier-series внутри одного бренда; source `du!=dr` 449/440 supplier дал отдельный RU body НО brand=Fagor NP-hit → SKIP-НП **независимо** от `du!=dr` body-level; nm_ru clean RU `Стол морозильный Fagor CCN-2G GR` без UA-leak; cells unchanged). SKU 45 `2448658777` Brillis СN2100 — **blknochg** LIVE Horoshop (**ВТОРОЙ Brillis в chunk-028** + **ВТОРОЙ Brillis в проекте** после b5 SKU 34 Brillis BGL2-R290 ПЕРВЫЙ; SKU 45 СN2100 другая Brillis series distinct от BGL2-R290; **Cyrillic С** U+0421 в коде model `СN2100` (НЕ Lat C) preserve verbatim per supplier; 2-door mirror SKU 46 3-door; **edge case** dr.len == du.len 934 в точности равны supplier-side формирование, content differs verified `same=False` → genuine separate RU body; nm_ru clean RU; cells unchanged). **Brillis НЕ ∈ НП-эксклюзив**. SKU 46 `2448660375` Brillis СN3100 — **blknochg** LIVE Horoshop **mirror SKU 45 3-door variant** (СN2100→СN3100, Cyr С preserve same convention SKU 45); dr.len == du.len 934 edge case parallel SKU 45; nm_ru clean RU; cells unchanged. SKU 47 `2545751551` Tecnodom TF02MIDBTAL — **blk триплет** **ДВЕНАДЦАТЫЙ blk триплет в chunk-028** + **ВТОРОЙ Tecnodom blk триплет** + **AL/ALU variant к base SKU 27 TF02MIDBT b4** ПЕРВЫЙ Tecnodom blk триплет (same brand Tecnodom same Italian template family, **разные модели и разные supplier-templates**: SKU 27 TF02MIDBT 1h2+3p+1ul/9li с `&mdash;`/`&deg;`/`&#39;` HTML entities vs SKU 47 TF02MIDBTAL 1p+1p/strong+1ul/11li без `&mdash;`/h2 — другая supplier-template structure для AL variant; **+2 li vs SKU 27**); `desc UA==RU` True 🔴 + `nm_ua==nm_ru` UA-leak `Стіл морозильний Tecnodom TF02MIDBTAL`, `nm_ru!=nazv_ru` clean RU `Стол морозильный Tecnodom TF02MIDBTAL` → AUTO Назв.мод (RU) = nazv_ru; Описание (RU) авторский 1p+1p/strong+ul/11li 1:1; **SKU 47-SPECIFIC**: **supplier asymmetric spacing** `-18&deg; C` (space-AFTER-entity) vs `-22 &deg;C` (space-BEFORE-entity) внутри одного li preserve verbatim; UA typo `Холодоагент` (лишний `о`)→canonical RU `Хладагент`; UA typo `відділені`→canonical RU `отделении`; Policy B/C `1420x700x1020 мм`→`1420мм x 700мм x 1020мм` (drop trailing single `мм` + per-axis `мм` слитно — same pattern b4 SKU 27 Tecnodom TF02MIDBT); R452А refrigerant Cyr А U+0410 preserve verbatim; drop `&#39;` x2 в `об'єм`/`Під'єднання`; поличка→полка lexical; UA `та`→`и` conjunction). **Tecnodom НЕ ∈ НП-эксклюзив**. SKU 48 `508918206` GGM Gastro International GGM GTS227 — **blknochg** LIVE Horoshop (**ПЕРВЫЙ GGM в проекте**; supplier-template family новый — multi-word brand `GGM Gastro International` vs short single-word brands seen so far; **4-door variant** model code `GGM GTS227` с **inline-dims** `2223х700 мм` (Cyr х U+0445) в самом nazv_ru/nm — необычный паттерн dims в имени продукта vs обычное отдельное поле; supplier RU dr 837 vs UA du 815; nm_ru clean RU `Стол морозильный четырехдверный GGM GTS227, (2223х700 мм)` без UA-leak; cells unchanged). **GGM Gastro International НЕ ∈ НП-эксклюзив** (substring `GASTRO`/`INTERNATIONAL` НЕ в NP-keys standalone). **Открытых вопросов по батчу: 0** (b1 0 + b2 0 + b3 0 + b4 0 + b5 0 + b6 0; ledger chunk-028 = 0). Кумулятивно chunk-028 = **0** (questions.md chunk-028 пока НЕ создаём — нет OQ; supplier UA typos `Холодоагент`/`відділені` → soft normalize к canonical RU inline, не нумеруются). Кумулятивно SKIP-НП chunk-028 = **10** (b1 0 + b2 3 + b3 3 + b4 1 + b5 1 + b6 2). NEXT: chunk-028 b7 SKU 49-56.

*(scoped к row Артикул=508918206)*

---

## SKU 49/61 — Стол морозильный Hendi 233399 Kitchen Line 600-я серия (Артикул 961986157) — 🔴 RU=UA + Назв.мод (RU) UA-leak

**Поле:** Название модификации (RU)
**Было:** `Стіл морозильний Hendi 233399 Kitchen Line 600-я серія`
**Стало:** `Стол морозильный Hendi 233399 Kitchen Line 600-я серия`

**Поле:** Описание товара (RU)
**Было:** (полностью идентично UA — украинский текст)
**Стало:** (полный перевод RU тег-в-tag):

```
<p>Стол морозильный с тремя дверцами. Корпус и внутренняя камера изготовлены из нержавеющей стали AISI 304, устойчивой к воздействию жиров и органических кислот (задняя внешняя стенка – из гальванической стали), внутренние углы закруглены, что облегчает чистку шкафа.<br/>
Данная модель способна выдержать даже очень высокую температуру окружающей среды (до +43°С и влажности до 65%). <br/> Толщина изоляционного материала: 50 мм. Автоматический отвод конденсата.</p>
<p>Технические характеристики:</p>
<ul>
<li>Температурный режим: -12°С...-22°C </li>
<li>климатический класс: N</li>
<li>Беспроблемная работа при температуре окружающей среды до +38°C</li>
<li>Динамическое охлаждение</li>
<li>В комплекте 1 полка на дверь (2x 430x428 мм + 1x 490x428 мм) с допустимой нагрузкой около 15 кг на каждую полку (при равномерном распределении веса)</li>
<li>Вместимость: 390 л. </li>
<li>Габариты: 1800x600x(H)850 мм.</li>
<li>Мощность: 0,5 кВт.</li>
<li>Напряжение: 220 В.</li>
<li>Количество дверей: 3</li>
<li>Ножки регулируются по высоте.</li>
<li>Хладагент: R134a</li>
</ul>
<p><img alt="" src="/content/uploads/images/961986157/770316093_770316093.jpeg" style="width:640px;height:353px"/> </p>
```

*(blk триплет **mixed-bilingual subtype** — `desc UA==RU` **True** 1186/1186 (du==dr identical) **+ UA-leak в body** char-level verified `і` U+0456 присутствует в обоих du и dr; supplier copy **half-translated abandoned mid-UL**: intro 1p + first 3 li + last li `Хладагент: R134a` genuine RU, **средние 8 li (Динамічне охолодження ... Ніжки регулюються по висоті)** UA-leak. `nm_ua`==`nm_ru` `Стіл морозильний Hendi 233399 Kitchen Line 600-я серія` UA-leak; `nm_ru`!=`nazv_ru` clean RU `Стол морозильный Hendi 233399 Kitchen Line 600-я серия` → AUTO Назв.мод (RU) = genuine `nazv_ru`. **Body — полный авторский RU**: RU-portion (intro 1p + first 3 li + last li R134a + img p) preserve verbatim; UA-portion (8 средних li) translate UA→RU 1:1 inline; **SOFT** supplier copy defects normalize: `близько 15 кожну полицю` (unit omitted) → `около 15 кг на каждую полку` add `кг` per refrigeration shelf-load convention; `Місткість: 390 к.` (unit truncated) → `Вместимость: 390 л.` per Kitchen Line 600 series capacity standard (refrigeration volume в литрах); `1 полиці` (supplier UA singular gen.sg ambiguous между «1 полка» и общим «полок») preserve literal `1 полка на дверь` — НЕ ре-интерпретируем supplier semantic. **Lat `x` U+0078** в dim-value `1800x600x(H)850` preserve verbatim (supplier использует Lat `x` НЕ Cyr `х` — отличие от Gooder SKU 38/39/55 где `х` Cyr → нормализуем к Lat `x`; Hendi supplier-side уже Lat `x` — оставляем). decimal comma `0,5 кВт` preserve. **Hendi НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. **ПЕРВЫЙ Hendi в проекте** — нет precedent batch/chunk; supplier-template family новый (Kitchen Line 600-я серия, 3-door morozilny с горизонтально-вытянутым корпусом 1800x600x850). **Lesson saved**: snapshot decision «blknmfix — 0 UA chars verified» был **wrong** — probe head (first 300 chars) показывал genuine RU intro, но char-level full-body scan нашёл UA `і` в средних 8 li; **durable rule**: для du==dr identical body всегда char-level full-body UA scan, НЕ head-only. **Mixed-bilingual subtype** (supplier abandoned translation mid-UL) — НОВАЯ supplier-side pattern; обработали как standard blk триплет (full body author RU). META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=961986157)*

---

## SKU 50/61 — Стол морозильный Tefcold CF7210 (Артикул 1154439882) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg — `desc UA==RU` **False** (genuine отдельный корректный русский перевод поставщика; dr 1374 vs du 1368); `nm_ua`!=`nm_ru` (UA `Стіл морозильний Tefcold CF7210` vs RU `Стол морозильный Tefcold CF7210`); `nm_ru`==`nazv_ru` clean RU (char-level UA_ONLY=∅). **Tefcold НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. LIVE Horoshop genuine RU body НЕ переписываем (ячейки chunk-028-fixed без изменений). Tefcold CF7210 — **2-door variant** Tefcold CF-серии (CF=Counter Freezer); supplier-template family Danish Tefcold (продолжение b5 SKU 35/36 Tefcold SK6210BT family и других Tefcold в проекте). LIVE artefacts preserve verbatim. blknochg → ВСЕ артефакты `dr` (RU-side) НЕ трогаем; авторский перевод НЕ генерим. Код `Tefcold CF7210` Lat → consistent. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=1154439882)*

---

## SKU 51/61 — Стол морозильный Tefcold CF7310 (Артикул 2053453675) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg — `desc UA==RU` **False** (genuine; dr 1314 vs du 1336 — RU чуть короче UA, нетипично но допустимо); `nm_ua`!=`nm_ru`; `nm_ru`==`nazv_ru` clean RU без UA-leak. **Tefcold НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. LIVE Horoshop genuine RU НЕ переписываем. **Mirror SKU 50 3-door variant** (Tefcold CF7210 2-door → CF7310 3-door same supplier-template — CF72/73 pattern parallel к SK62/63 pairs). blknochg → ВСЕ артефакты dr НЕ трогаем; авторский перевод НЕ генерим. Код `Tefcold CF7310` Lat → consistent. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=2053453675)*

---

## SKU 52/61 — Стол морозильный Tefcold CF7410 (Артикул 2053467056) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg — `desc UA==RU` **False** (genuine; dr 1274 vs du 1298 — RU чуть короче UA same pattern as SKU 51); `nm_ua`!=`nm_ru`; `nm_ru`==`nazv_ru` clean RU без UA-leak. **Tefcold НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. LIVE Horoshop genuine RU НЕ переписываем. **Mirror SKU 50/51 4-door variant** (CF72/73/74 pattern — CF7410 = 4-door extension same supplier-template family). blknochg → ВСЕ артефакты dr НЕ трогаем. Код `Tefcold CF7410` Lat → consistent. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=2053467056)*

---

## SKU 53/61 — Стол морозильный Tefcold SK6210BT/+SP (Артикул 2053468272) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg — `desc UA==RU` **False** (genuine; dr 1284 vs du 1307 — RU чуть короче UA); `nm_ua`!=`nm_ru`; `nm_ru`==`nazv_ru` clean RU без UA-leak. **Tefcold НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. LIVE Horoshop genuine RU НЕ переписываем. SKU 53 Tefcold SK6210BT/+SP — **другая Tefcold series SK-серии** distinct от CF-серии SKU 50/51/52; `/+SP` sibling-suffix mirror b5 SKU 35/36 Tefcold SK6310BT/+SP pattern (SP=Splash Protection или similar option). `BT` Lat в коде модели preserve verbatim — distinct от Cyr `ВТ` в SKU 54/55 Gooder. blknochg → ВСЕ артефакты dr НЕ трогаем. Код `Tefcold SK6210BT/+SP` Lat (BT Lat) → consistent. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=2053468272)*

---

## SKU 54/61 — Стол морозильный Tefcold SK6410ВТ/+SP (Артикул 2113716261) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg — `desc UA==RU` **False** (genuine; dr 1000 vs du 986 — RU чуть длиннее UA expected expansion); `nm_ua`!=`nm_ru`; `nm_ru`==`nazv_ru` clean RU без UA-leak. **Tefcold НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. LIVE Horoshop genuine RU НЕ переписываем. SKU 54 Tefcold SK6410ВТ/+SP — **4-door variant SK-серии** (SK62/64 pattern parallel к CF72/74) **+ Cyrillic `ВТ`** U+0412+U+0422 в коде model `SK6410ВТ` (НЕ Lat `BT` как в SKU 53 SK6210BT) preserve verbatim — supplier-side latin/cyrillic mix в коде, **same convention** как Gooder ВТ в SKU 38/39 b5 и SKU 55 GN4100ВТ b7. blknochg → ВСЕ артефакты dr НЕ трогаем. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=2113716261)*

---

## SKU 55/61 — Стол морозильный Gooder GN4100ВТ (Артикул 2199341644) — 🔴 RU=UA + Назв.мод (RU) UA-leak

**Поле:** Название модификации (RU)
**Было:** `Стіл морозильний Gooder GN4100ВТ`
**Стало:** `Стол морозильный Gooder GN4100ВТ`

**Поле:** Описание товара (RU)
**Было:** (полностью идентично UA — украинский текст)
**Стало:** (полный перевод RU тег-в-tag):

```
<p>Стол холодильный низкотемпературный Gooder GN4100ВТ предназначен для хранения продуктов питания и полуфабрикатов на предприятиях общественного питания и торговли.</p> <p><strong>Характеристики:</strong></p> <ul>
<li>Относительная влажность : 55%;</li>
<li>Вес: 145 кг;</li>
<li>Вес в упаковке: 155 кг;</li>
<li>Диапазон температуры окружающей среды: +16 до +30 С&deg;;</li>
<li>Общий объём л: 553 л;</li>
<li>Количество полок: 4;</li>
<li>Класс энергопотребления: Е;</li>
<li>Климатический класс: 4;</li>
<li>Корпус: Нержавеющая сталь снаружи и внутри (AISI 304);</li>
<li>Страна-производитель: Китай;</li>
<li>Размеры (ДxШxВ): 2230мм x 700мм x 860мм;</li>
<li>Система охлаждения: Динамическая;</li>
<li>Потребление электроэнергии: 10,89 кВт/д;</li>
<li>Темп.режим: -18&deg;C....-22&deg;C; Торговая марка: Gooder; Автоматические двери,</li>
<li>Цифровой термостат;</li>
<li>Хладагент: R290</li>
</ul>
```

*(blk триплет STANDARD — `desc UA==RU` **True** (🔴 RU=UA — RU = полная укр. копия тела, оба длиной 899); `nm_ua`==`nm_ru` `Стіл морозильний Gooder GN4100ВТ` (UA-leak; body-level `_has_ua` True via `Стіл`/`морозильний`); `nm_ru`!=`nazv_ru` genuine RU `Стол морозильный Gooder GN4100ВТ` → AUTO Назв.мод (RU) = genuine `nazv_ru`. **ЧЕТЫРНАДЦАТЫЙ blk триплет в chunk-028** + **ТРЕТИЙ Gooder blk триплет в chunk-028** + **4-door variant к base SKU 38/39 b5 Gooder GN2100ВТ/GN3100ВТ family** (same brand Gooder same Chinese supplier-template family, **4-door extension** к 2/3-door siblings GN21/31/41 pattern). **Gooder НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. Описание (RU) — авторский полный перевод тег-в-tag (структура UA зеркалится 1:1; 1 `<p>` + 1 `<p>/<strong>` + 1 `<ul>` + 16 `<li>` collapsed; line-breaks `\n` после `<ul>` и между `<li>` preserve verbatim). SOFT применено к авторскому RU **1:1 from b5 SKU 38/39 Gooder precedent**: `Стіл холодильний низькотемпературний...призначений для зберігання...` → `Стол холодильный низкотемпературный...предназначен для хранения...` (4-door specific intro); **inverse postfix-Cyr+entity** `+16 до +30 С&deg;;` preserve verbatim (НЕ `&deg;С` — supplier-specific postfix order); **space-colon** `Відносна вологість :` → `Относительная влажность :` preserve supplier-side spacing; **Cyr `х` U+0445 → Lat `x` U+0078** в dim-header `(ДхШхВ)→(ДxШxВ)` AND value `2230х700х860→2230мм x 700мм x 860мм` Policy B/C; drop `&#39;` в `об&#39;єм`→`объём` ё; **Cyr `ВТ`** U+0412+U+0422 в коде `GN4100ВТ` preserve verbatim (same supplier convention SKU 38/39 b5); **UA typo normalize**: `Климатичний` (UA typo — canonical UA `Кліматичний`) → `Климатический` (canonical RU); `всередені` (UA typo — canonical UA `всередині`) → `внутри` (canonical RU); `Хлодоген` (UA spelling mishmash — canonical UA `Холодоагент`) → `Хладагент` (canonical RU); UA→RU lexicon: `Загальний об'єм`→`Общий объём`, `Кількість полок`→`Количество полок`, `Клас енергоспоживання`→`Класс энергопотребления`, `Країна виробник`→`Страна-производитель`, `Система охолодження: Динамічна`→`Система охлаждения: Динамическая`, `Споживання електроенергії: 10,89 кВт/д`→`Потребление электроэнергии: 10,89 кВт/д` (decimal comma preserve; `кВт/д` unit preserve); **collapsed-li three-in-one supplier signature** `Темп.режим: -18&deg;C....-22&deg;C; Торгова марка: Gooder; Автоматичні двері,` (3-in-1 supplier inline) → `Темп.режим: -18&deg;C....-22&deg;C; Торговая марка: Gooder; Автоматические двери,` preserve verbatim (4-точечное `....`, supplier semicolons, trailing comma); `Цифровий термостат`→`Цифровой термостат`; бренд/модель/`R290`/`л`/`мм`/`%`/`AISI 304`/`Е` (Cyr Е class) preserve verbatim; HTML-entities `&deg;` (x3 — `+30 С&deg;`, `-18&deg;C`, `-22&deg;C`) preserve verbatim. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=2199341644)*

---

## SKU 56/61 — Стол морозильный Tefcold GF72 (Артикул 2245882346) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg — `desc UA==RU` **False** (genuine; dr 1016 vs du 982 — RU чуть длиннее UA expected expansion); `nm_ua`!=`nm_ru`; `nm_ru`==`nazv_ru` clean RU без UA-leak. **Tefcold НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. LIVE Horoshop genuine RU НЕ переписываем. SKU 56 Tefcold GF72 — **другая Tefcold series GF-серии** distinct от CF-серии SKU 50/51/52 и SK-серии SKU 53/54 (GF=Glass Freezer или Gastronorm Freezer); single SKU GF-серии в b7. blknochg → ВСЕ артефакты dr НЕ трогаем. Код `Tefcold GF72` Lat → consistent. META always faithful. Открытых вопросов 0.)*

**Наблюдения по батчу SKU 49-56 (56/61) — chunk-028 (батч-морозильные столы Hendi ×1 + Tefcold ×6 + Gooder ×1; раздел `Холодильне та морозильне обладнання/Морозильні столи` — продолжение b6 SKU 41-48):** **blk триплет 2 (SKU 49 Hendi 233399 mixed-bilingual subtype + SKU 55 Gooder GN4100ВТ standard). blknotrip 0. blkv 0. blknochg 6 (SKU 50 Tefcold CF7210, SKU 51 Tefcold CF7310, SKU 52 Tefcold CF7410, SKU 53 Tefcold SK6210BT/+SP, SKU 54 Tefcold SK6410ВТ/+SP, SKU 56 Tefcold GF72 — LIVE Horoshop genuine RU). blknochgeq 0. SKIP-НП 0 (no Fagor/Hurakan/etc в b7).** SKU 49 `961986157` Hendi 233399 Kitchen Line 600-я серія — **blk триплет mixed-bilingual subtype**: source signature `du==dr` True 1186/1186 (identical) **+ UA-leak в body** char-level verified (`і` U+0456 присутствует в обоих du и dr — supplier half-translated abandoned mid-UL); intro 1p + first 3 li + last li R134a genuine RU, **средние 8 li UA-leak** (`Динамічне охолодження`/`У комплекті`/`Місткість`/`Габарити`/`Потужність`/`Напруга`/`Кількість дверей`/`Ніжки регулюються`); `nm_ua==nm_ru` UA-leak `Стіл морозильний Hendi 233399 Kitchen Line 600-я серія`, `nm_ru!=nazv_ru` clean RU `Стол морозильный Hendi 233399 Kitchen Line 600-я серия` → AUTO Назв.мод (RU) = nazv_ru; Описание (RU) — авторский полный RU body (RU-portion preserve verbatim + UA-portion translate); **SOFT supplier copy defects normalize**: `близько 15 кожну полицю` (unit omitted) → `около 15 кг на каждую полку` add `кг`; `Місткість: 390 к.` (unit truncated) → `Вместимость: 390 л.` per Kitchen Line 600 capacity standard; `1 полиці` preserve literal `1 полка`. Lat `x` в dim-value preserve verbatim (Hendi supplier-side Lat, distinct от Gooder Cyr `х` → Lat `x` нормализация в SKU 55). **ПЕРВЫЙ Hendi в проекте** — нет precedent batch/chunk; supplier-template family новый (Kitchen Line 600-я серия, 3-door morozilny 1800x600x850). **Hendi НЕ ∈ НП-эксклюзив**. **Lesson**: snapshot «blknmfix — 0 UA chars verified» был **wrong** — probe head (first 300 chars) показывал RU intro но char-level full-body scan нашёл UA `і` в средних 8 li; **durable rule**: для du==dr identical body всегда char-level full-body UA scan, НЕ head-only. **Mixed-bilingual subtype** (supplier abandoned translation mid-UL) — НОВАЯ supplier-side pattern; обработали как standard blk триплет (full body author RU). SKU 50 `1154439882` Tefcold CF7210 — **blknochg** LIVE Horoshop (Tefcold НЕ НП-эксклюзив; **2-door variant** CF-серии Danish Tefcold; supplier RU dr 1374 vs UA du 1368; nm_ru clean RU без UA-leak; cells unchanged). SKU 51 `2053453675` Tefcold CF7310 — **blknochg** LIVE Horoshop **mirror SKU 50 3-door variant** (CF72/73 pattern parallel к SK62/63); supplier RU dr 1314 vs UA du 1336 (RU чуть короче UA нетипично но допустимо); nm_ru clean RU; cells unchanged. SKU 52 `2053467056` Tefcold CF7410 — **blknochg** LIVE Horoshop **4-door variant CF-серии** (CF72/73/74 pattern); supplier RU dr 1274 vs UA du 1298; cells unchanged. SKU 53 `2053468272` Tefcold SK6210BT/+SP — **blknochg** LIVE Horoshop **другая Tefcold series SK-серии** distinct от CF-серии SKU 50/51/52; `/+SP` sibling-suffix mirror b5 SKU 35/36 Tefcold SK6310BT/+SP pattern; `BT` Lat в коде preserve verbatim — distinct от Cyr `ВТ` в SKU 54/55; supplier RU dr 1284 vs UA du 1307; cells unchanged. SKU 54 `2113716261` Tefcold SK6410ВТ/+SP — **blknochg** LIVE Horoshop **4-door variant SK-серии** (SK62/64 pattern parallel к CF72/74) **+ Cyrillic `ВТ`** U+0412+U+0422 в коде `SK6410ВТ` (НЕ Lat `BT` как SKU 53) preserve verbatim — supplier-side latin/cyrillic mix **same convention** как Gooder ВТ в SKU 38/39 b5 и SKU 55 b7; supplier RU dr 1000 vs UA du 986 expected expansion; cells unchanged. SKU 55 `2199341644` Gooder GN4100ВТ — **blk триплет STANDARD** **ЧЕТЫРНАДЦАТЫЙ blk триплет в chunk-028** + **ТРЕТИЙ Gooder blk триплет** + **4-door variant к base SKU 38/39 b5 Gooder GN2100ВТ/GN3100ВТ family** (same brand Gooder same Chinese supplier-template, 4-door extension GN21/31/41 pattern); `desc UA==RU` True 🔴 + `nm_ua==nm_ru` UA-leak `Стіл морозильний Gooder GN4100ВТ`, `nm_ru!=nazv_ru` clean RU → AUTO Назв.мод (RU) = nazv_ru; Описание (RU) авторский 1p+1p/strong+ul/16li 1:1 from b5 SKU 38/39 Gooder precedent; **SKU 55-SPECIFIC**: **inverse postfix-Cyr+entity** `С&deg;` preserve (НЕ `&deg;С`); **space-colon** `Відносна вологість :` preserve; **Cyr `х` U+0445 → Lat `x` U+0078** в dim-header `(ДхШхВ)→`(ДxШxВ)` AND value `2230х700х860→2230мм x 700мм x 860мм` Policy B/C; **Cyr `ВТ`** в коде `GN4100ВТ` preserve verbatim; UA typos normalize: `Климатичний`→`Климатический`, `всередені`→`внутри`, `Хлодоген`→`Хладагент` (supplier UA spelling mishmash); **collapsed-li three-in-one** `Темп.режим: -18&deg;C....-22&deg;C; Торгова марка: Gooder; Автоматичні двері,` preserve structure verbatim with translate; `Цифровий термостат`→`Цифровой термостат`; HTML-entities `&deg;` x3 preserve. **Gooder НЕ ∈ НП-эксклюзив**. SKU 56 `2245882346` Tefcold GF72 — **blknochg** LIVE Horoshop **другая Tefcold series GF-серии** distinct от CF-серии SKU 50/51/52 и SK-серии SKU 53/54 (GF=Glass Freezer или Gastronorm Freezer); single SKU GF-серии в b7; supplier RU dr 1016 vs UA du 982 expected expansion; nm_ru clean RU; cells unchanged. **Открытых вопросов по батчу: 0** (b1 0 + b2 0 + b3 0 + b4 0 + b5 0 + b6 0 + b7 0; ledger chunk-028 = 0). Кумулятивно chunk-028 = **0** (questions.md chunk-028 пока НЕ создаём — нет OQ; SKU 49 supplier copy defects `близько 15 без units`/`Місткість: 390 к.` soft normalize к canonical RU inline, не нумеруются; SKU 55 supplier UA typos `Климатичний`/`всередені`/`Хлодоген` → soft normalize к canonical RU inline, не нумеруются). Кумулятивно SKIP-НП chunk-028 = **10** (b1 0 + b2 3 + b3 3 + b4 1 + b5 1 + b6 2 + b7 0). NEXT: chunk-028 b8 SKU 57-61 (LAST 5-SKU батч → закрытие 61/61).

*(scoped к row Артикул=2245882346)*

---
