# chunk-029 translation diff (79 SKU — холодильное оборудование + оборудование для пиццерии, продолжение chunk-028)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-029 (79 SKU, продолжение chunk-028)
**Apply key:** `Артикул` (scoped per row)
**Status:** IN PROGRESS 0/79

**Состав (по типу товара):** первый SKU — Артикул `970938056`, бренд FROSTY (`Мінібар FROSTY KWS-52M`, раздел `Холодильне та морозильне обладнання/Шафи настільні для бару, міні-бари (фрігобари)` — НОВЫЙ раздел в проекте: настольные барные холодильные шкафы / мини-бары (фригобары); переход от `Холодильні шафи для вина` (chunk-028 SKU 60-61) → `Шафи настільні для бару, міні-бари` (chunk-029 SKU 1)). Раздел `Шафи настільні для бару, міні-бари (фрігобари)` занимает 38 SKU (SKU 1-38, бренды Tefcold ×16 + FROSTY ×5 + Hurakan ×5 + EWT INOX ×4 + REEDNEE ×3 + Hendi ×2 + Forcar ×2 + Hata ×1), далее начинается НОВЫЙ блок разделов `Обладнання для піцерії/...` (41 SKU, SKU 39-79 — ПЕРВЫЙ pizza-equipment блок в проекте; включает подразделы `Печі для піци`, `Преси для піци`, `Аксесуари для піцерії` с чередованием по SKU; бренды FROSTY ×8 + Apach ×6 + ITPIZZA ×5 + GI.Metal ×5 + Cuppone ×5 + GGF ×4 + Pizza Group ×2 + RESTO ITALIA ×2 + GGM Gastro International ×2 + Silver ×1). Последний SKU 79 — Артикул `526857503`, бренд APACH, `Піч для піци Apach AMM44X (380В)` (SKIP-НП). Тип товара определяется per-SKU. Бренды per-SKU (17 total): Tefcold/FROSTY/Hurakan/EWT INOX/REEDNEE/Hendi/Forcar/Hata/Apach/ITPIZZA/GI.Metal/Cuppone/GGF/Pizza Group/RESTO ITALIA/GGM Gastro International/Silver — из них Hurakan (×5) + Apach (×6) = 11 SKU → SKIP-НП по правилу forward-only (SKU 2/8/13/14/15 Hurakan; SKU 47/48/49/77/78/79 Apach). Plan 10 батчей: b1..b9 × 8 SKU + b10 LAST × 7 SKU (9×8=72 + 7 = 79).

**Standing rules** (inherited from chunk-001 — chunk-028):
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
- **4 формат-политики A/B/C → GLOBAL assembly-time pass — НЕ per-SKU diff, НЕ FLAG.** A вес `NN.00`→`NN кг.`/целое · B латинская `x`→кириллическая `х` в габаритах · C пробел перед `мм/см` (вкл. UA `18кВт`/`27кВт` слитно). Спека `.planning/translation-audit/GLOBAL-SWEEP-format.md`; применяется `apply_chunk_diff.py` при сборке master-xlsx ко всем чанкам. **В chunk-029 вес `NN.00` / латинскую `x` / `NNмм` НЕ диффать и НЕ флагать — закрыто глобально.**
- **F (структурный, per-SKU):** HTML `<br />`-склейка двух+ характеристик в одном `<li>` → раздельные `<li>` зеркально чистой стороне. Применять при встрече (ретро chunks 005-008 закрыт).
- FLAG (НЕ авто, → MANUAL-REVIEW русский): T5 surface conflict (текст/код vs spec); RU temp values ≠ UA; spec single vs text dual zone; UA title без дескриптора что есть в body+RU; source data error UA=RU → soft note / Открытые вопросы. **Вес `NN.00` БОЛЬШЕ НЕ флагается (policy A глобально).**

---
