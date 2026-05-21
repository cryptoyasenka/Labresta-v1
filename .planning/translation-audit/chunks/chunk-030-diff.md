# chunk-030 translation diff (96 SKU — оборудование для пиццерии: печи + аксессуары + прессы, продолжение chunk-029)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-030 (96 SKU, продолжение chunk-029)
**Apply key:** `Артикул` (scoped per row)
**Status:** IN PROGRESS 0/96

**Состав (по типу товара):** первый SKU — Артикул `526929616`, бренд ITPIZZA (`Піч для піци ITPIZZA ML6`, раздел `Обладнання для піцерії/Печі для піци` — продолжение pizza-equipment блока, начатого в chunk-029 SKU 39-79). chunk-030 — целиком в разделе `Обладнання для піцерії` с 3 чередующимися подразделами: `Печі для піци` (40 SKU non-contiguous) + `Аксесуари для піцерії` (54 SKU) + `Преси для піци` (2 SKU). Section transitions interleaved (14 переходов): SKU 1-7 Печі / 8-19 Аксесуари / 20-28 Печі / 29-40 Аксесуари / 41 Печі / 42-46 Аксесуари / 47-49 Печі / 50 Преси / 51-53 Печі / 54 Преси / 55-78 Аксесуари / 79-90 Печі / 91 Аксесуари / 92-96 Печі. Бренды per-SKU (12 total): GI.Metal ×30 + Hendi ×24 + FROSTY ×13 + ITPIZZA ×6 + Moretti Forni ×6 + GGF ×5 + GoodFood ×4 + Hurakan ×2 + EWT INOX ×2 + Apach ×2 + Cuppone ×1 + REEDNEE ×1 — из них Hurakan (×2 SKU 27/84) + Apach (×2 SKU 51/54) = 4 SKU → SKIP-НП по правилу forward-only. Последний SKU 96 — Артикул `2385515101`, бренд Moretti Forni, `Піч для піци Moretti Forni PM72.72`. Тип товара определяется per-SKU.

**Standing rules** (inherited from chunk-001 — chunk-029, расширено durable rules Yana 2026-05-21):
- **SKIP-НП (forward-only, приоритет над переводом):** SKU бренда из НП-эксклюзивного списка (HURAKAN/Хуракан, APACH/Апач, FAGOR/Фагор, TATRA/Татра, COLD/Колд, PROJECT SYSTEMS, ASTORIA, ARRIS, MAXIMA — case-insensitive, латиница и кириллица; Tefcold/Forcold/EWT INOX/GoodFood/GGF/GI.Metal/Cuppone/REEDNEE/ITPIZZA/Moretti Forni/Hendi/FROSTY НЕ входят) → RU НЕ переписывается, ячейки SKU не меняются; помечается `SKIP-НП (brand=<X>, тело из фида НП позже)` в MANUAL-REVIEW; отдельная категория в N/N. Без ретро-прохода.
- **Rule A (Yana 2026-05-21, durable forward-only):** UA-cells МОЖНО модифицировать при явных typos/грамматических ошибках (forward-only, supplier-side faithful). Прецедент chunk-029 b9 SKU 72 ITPIZZA `32 див`→`32 см`.
- **Rule B (Yana 2026-05-21, durable forward global glyph-normalize):** HTML entity `&deg;` → Unicode `°` (U+00B0); Cyr `С` (U+0421) после градуса → Lat `C` (U+0043); итоговый формат `50 °C` во всех категориях, обе локали. Прецедент chunk-029 b9 GGF ×3 + b10 GGM ×2 (8 cells).
- UA term `жаркова`/`жарильна`/`смарочна` → `жарочна` (locked Yana 2026-05-14)
- RU machine artifact `жареная поверхность` → `жарочная поверхность`; `жареная для жарки` → `жарочная`
- UA `Контейнер для сбору жиру` → `Контейнер для збирання жиру` (ONLY предлог); RU `Контейнер по сбору жира` → `для сбора`
- UA/RU `мм :` → `мм:`
- RU `от NN до NNN&deg;C` → `от NN&deg;C до NNN&deg;C` ТОЛЬКО если UA имеет оба &deg;C и значения совпадают; иначе FLAG
- decimal `N.N` → `N,N` обе локали (реальные дроби: меняется разделитель, точность сохранена; integers/already-comma — no-op)
- RU-leak UA `і`→`и`; 🔴 RU=UA полная укр. копия → AUTO full RU translate (структура HTML tag-в-tag, ✅ АВТО)
- Название модификации (RU) на украинском → AUTO перевод по Название (RU)
- Очевидный typo (удвоение/выпадение слога) → AUTO; однозначная машинная мистрансляция → AUTO + note
- UA→RU операторские термины: `Деко`→`Противень`, `Деко-решітка`→`Противень-решётка`, `Піч НВЧ`→`Печь СВЧ`, `Візок`→`Тележка`, `Решітка`→`Решётка`, `Перфорований лист`→`Противень перфорированный` (memory `feedback_labresta_ua_ru_translation_rules`)
- **4 формат-политики A/B/C → GLOBAL assembly-time pass — НЕ per-SKU diff, НЕ FLAG.** A вес `NN.00`→`NN кг.`/целое · B латинская `x`→кириллическая `х` в габаритах · C пробел перед `мм/см` (вкл. UA `18кВт`/`27кВт` слитно). Спека `.planning/translation-audit/GLOBAL-SWEEP-format.md`; применяется `apply_chunk_diff.py` при сборке master-xlsx ко всем чанкам. **В chunk-030 вес `NN.00` / латинскую `x` / `NNмм` НЕ диффать и НЕ флагать — закрыто глобально.**
- **F (структурный, per-SKU):** HTML `<br />`-склейка двух+ характеристик в одном `<li>` → раздельные `<li>` зеркально чистой стороне. Применять при встрече.
- FLAG (НЕ авто, → MANUAL-REVIEW русский): T5 surface conflict (текст/код vs spec); RU temp values ≠ UA; spec single vs text dual zone; UA title без дескриптора что есть в body+RU; source data error UA=RU → soft note / Открытые вопросы. **Вес `NN.00` БОЛЬШЕ НЕ флагается (policy A глобально).**

---
