# chunk-028 translation diff (61 SKU — холодильное оборудование, продолжение chunk-027)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-028 (61 SKU, продолжение chunk-027)
**Apply key:** `Артикул` (scoped per row)
**Status:** IN PROGRESS 0/61

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
