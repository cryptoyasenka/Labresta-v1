# chunk-029 translation diff (79 SKU — холодильное оборудование + оборудование для пиццерии, продолжение chunk-028)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-029 (79 SKU, продолжение chunk-028)
**Apply key:** `Артикул` (scoped per row)
**Status:** IN PROGRESS 8/79

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

## SKU 1/79 — Минибар FROSTY KWS-52M (Артикул 970938056) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg — `desc UA==RU` **False** (genuine отдельный корректный русский перевод поставщика); `nm_ua`!=`nm_ru` (UA `Мінібар FROSTY KWS-52M` vs RU `Минибар FROSTY KWS-52M`); `nm_ru`==`nazv_ru` clean RU (char-level UA_ONLY=∅). **FROSTY НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. LIVE-магазин Horoshop, genuine RU body НЕ переписываем (ячейки chunk-029-fixed без изменений). LIVE source artefacts preserve verbatim (blknochg → НЕ нормализуем): (1) supplier RU dr `+1...+10&deg;С` Cyr С U+0421 entity (no space before `&deg;`) vs UA du `+1...+10 °C` Lat C U+0043 (space before `°`) — desync supplier-side; (2) RU body `<li>3 полки-решетки</li>` no-ё vs UA `<li>3 полиці-решітки</li>` (supplier consistent). FROSTY mini-bar mini-template family: h2 + p + ul/9li no-img no-iframe; **ПЕРВЫЙ blknochg в chunk-029** в разделе `Шафи настільні для бару, міні-бари (фрігобари)` — НОВЫЙ раздел в проекте. Код `FROSTY KWS-52M` Lat → consistent. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=970938056)*

---

## SKU 2/79 — Барный холодильный шкаф HURAKAN HKN-GXDB250-SL (Артикул 2060677611) — SKIP-НП (бренд НП-эксклюзив, тело из фида НП позже)

**Бренд:** Hurakan (НП-эксклюзивный — forward-only SKIP-правило)
**Поле:** Название модификации (RU)
**Было:** (ячейка не трогается — тело из фида НП позже)
**Стало:** не трогаем (SKIP-НП — тело из фида НП позже)

**Поле:** Описание товара (RU)
**Было:** (ячейка не трогается — тело из фида НП позже)
**Стало:** не трогаем (SKIP-НП — тело из фида НП позже)

*(SKIP-НП — `brand`=`Hurakan` ∈ {HURAKAN/Хуракан} word-boundary NP-hit → forward-only SKIP-правило: тело из фида НП позже, ячейки chunk-029-fixed.xlsx НЕ трогаем (Назв.мод RU + Описание RU без изменений). **Hurakan ∈ НП-эксклюзивный список** (word-boundary NP-hit найден в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}) → forward-only SKIP-правило: тело из фида НП позже, ячейки chunk-029-fixed.xlsx не трогаем (Назв.мод RU + Описание RU без изменений). **ПЕРВЫЙ SKIP-НП в chunk-029** (Hurakan-серия начинается — Hurakan ×5 candidate в chunk-029 SKU 2/8/13/14/15). Source signature `du!=dr` genuine разный, `nm_ua!=nm_ru` (UA `Барна холодильна шафа HURAKAN HKN-GXDB250-SL` vs RU `Барный холодильный шкаф HURAKAN HKN-GXDB250-SL`); `nm_ru==nazv_ru` clean RU — но brand=Hurakan NP-hit → SKIP-НП **независимо** от состояния ячеек (правило forward-only по brand-membership, не по signature). HKN-GXDB250-SL — стеклянная барная холодильная витрина 250 л. Кумул. SKIP-НП chunk-029 = 1 (после SKU 2). META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=2060677611)*

---

## SKU 3/79 — Минибар FROSTY BC-90 (Артикул 468636015) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg — `desc UA==RU` **False** (genuine отдельный корректный русский перевод поставщика); `nm_ua`!=`nm_ru` (UA `Мінібар FROSTY BC-90` vs RU `Минибар FROSTY BC-90`); `nm_ru`==`nazv_ru` clean RU. **FROSTY НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. LIVE-магазин Horoshop, genuine RU body НЕ переписываем. LIVE source artefacts preserve verbatim: (1) supplier RU dr `+4...+10 &deg;С, морозильное отделение 0...-5&deg;С` Cyr С entity (space-before mix — `+4...+10 &deg;С` space, `0...-5&deg;С` no space) vs UA `+4...+10 °C, морозильна камера 0...-5 °C` Lat C; (2) RU `Одна перевешиваемая дверь` faithful translation UA `Перенавішуючі дверцята`; (3) FROSTY mini-bar mini-template family same as SKU 1: h2 + p + ul/9li no-img no-iframe; (4) `Две регулируемые полки размером...` faithful. **ВТОРОЙ blknochg в chunk-029** (mirror SKU 1 FROSTY KWS-52M same supplier template). FROSTY mini-bar series — supplier дал отдельный RU перевод для каждого SKU; magazine NEVER UA-копией. Код `FROSTY BC-90` Lat → consistent. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=468636015)*

---

## SKU 4/79 — Минибар морозильный TEFCOLD UF200S (нерж.) (Артикул 646908262) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg — `desc UA==RU` **False** (genuine отдельный корректный русский перевод поставщика); `nm_ua`!=`nm_ru` (UA `Мінібар морозильний TEFCOLD UF200S (нерж.)` vs RU `Минибар морозильный TEFCOLD UF200S (нерж.)`); `nm_ru`==`nazv_ru` clean RU. **Tefcold НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. LIVE-магазин Horoshop, genuine RU body НЕ переписываем. LIVE source artefacts preserve verbatim: (1) supplier RU dr `<li>Без подстветки</li>` typo source preserve (precedent chunk-027 b7/chunk-028 b1 Tefcold supplier src-typos: store-canonical опечатки RU body не правим в blknochg); (2) RU `Диапазон температур от -10&deg;C до -25&deg;C` Lat C; (3) `<h2>Морозильный шкаф TEFCOLD UF200S отлично подойдет...</h2>` opening — supplier translated полный RU body независимо от UA. Tefcold UF200S — морозильный шкаф 120 л (нержавеющая сталь корпус). **ПЕРВЫЙ Tefcold blknochg в chunk-029** (Tefcold ×16 в chunk-029 candidate — mini-bar/freezer subseries). Код `TEFCOLD UF200S` Lat upper → consistent. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=646908262)*

---

## SKU 5/79 — Минибар морозильный TEFCOLD UF200G (стекло) (Артикул 646911261) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg — `desc UA==RU` **False** (genuine отдельный корректный русский перевод поставщика); `nm_ua`!=`nm_ru` (UA `Мінібар морозильний TEFCOLD UF200G (скло)` vs RU `Минибар морозильный TEFCOLD UF200G (стекло)`); `nm_ru`==`nazv_ru` clean RU. **Tefcold НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. LIVE-магазин Horoshop, genuine RU body НЕ переписываем. LIVE source artefacts preserve verbatim: (1) supplier RU dr opening `<p>Мини-холодильник отлично подойдет...</p>` (НЕ `<h2>` как SKU 4 — **SKU 5-specific structure desync**: supplier дал `<p>` opening вместо `<h2>` mini-template canonical в этой SKU); (2) RU `&deg;С` Cyr С entity vs UA `°C` Lat C — per-SKU mix; (3) UA `скло` → RU `стекло` correctly translated в `nazv_ru/nm_ru` parens. **ВТОРОЙ Tefcold blknochg в chunk-029** (mirror SKU 4 same Tefcold mini-bar freezer family — но стеклянная дверь vs нержавеющая сталь). Tefcold UF200G — морозильный шкаф 120 л со стеклянной дверью с подогревом (supplier дал full LED illumination + glass-door spec в RU). Код `TEFCOLD UF200G` Lat upper → consistent. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=646911261)*

---

## SKU 6/79 — Минибар FROSTY BC-70 (Артикул 756820696) — 🔴 RU=UA + Назв.мод (RU) UA-leak

**Поле:** Название модификации (RU)
**Было:** `Мінібар FROSTY BC-70`
**Стало:** `Минибар FROSTY BC-70`

**Поле:** Описание товара (RU)
**Было:** (полностью идентично UA — украинский текст)
**Стало:** (полный перевод RU тег-в-tag):

```
<h2>Минибар FROSTY BC-70 отлично подойдет для размещения на небольшой площади. Используется для хранения напитков и продуктов, а также имеет морозильное отделение.</h2> <p>Технические характеристики:</p> <ul>
<li>Одна дверь</li>
<li>Одна регулируемая полка размером 360x270 мм </li>
<li>Объём 72 л.</li>
<li>Температурный режим +4...+10 &deg;C, морозильное отделение 0...-5 &deg;C</li>
<li>Механический контроль температуры</li>
<li>Цвет чёрный</li>
<li>Напряжение 220 В</li>
<li>Габариты 445мм x 490мм x 635мм</li>
</ul>
```

*(blk триплет STANDARD — `desc UA==RU` **True** (🔴 RU=UA — RU = полная укр. копия тела); `nm_ua`==`nm_ru` `Мінібар FROSTY BC-70` (UA-leak — body-level `_has_ua` True via `Мінібар` — Cyr і U+0456 + Cyr і U+0456 inside `Мінібар`); `nm_ru`!=`nazv_ru` genuine RU `Минибар FROSTY BC-70` → AUTO Назв.мод (RU) = genuine `nazv_ru`. **ПЕРВЫЙ blk триплет в chunk-029** (раздел `Шафи настільні для бару, міні-бари (фрігобари)` — НОВЫЙ раздел в проекте, mini-bar FROSTY mini-template family по структуре идентичен FROSTY KWS-52M из SKU 1 blknochg + FROSTY BC-90 из SKU 3 blknochg, **но разные SKU**: SKU 1/3 supplier дал отдельный RU body dr genuine; SKU 6 supplier дал UA-only тело — magazine скопировал UA в RU cell). **FROSTY НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. Описание (RU) — авторский полный перевод тег-в-tag (структура UA зеркалится 1:1; 1 `<h2>` + 1 `<p>` + 1 `<ul>` + 9 `<li>`, line-breaks `\n` после `<ul>` и между `<li>` preserve verbatim; no `<img>`, no iframe, no voltage explicit отдельно; voltage в ul/li `220 В`). SOFT применено к авторскому RU: `<h2>Мінібар FROSTY BC-70 чудово підійде для розміщення на невеликій площі. Використовується для зберігання напоїв і продуктів, а також має морозильне відділення.</h2>`→`<h2>Минибар FROSTY BC-70 отлично подойдет для размещения на небольшой площади. Используется для хранения напитков и продуктов, а также имеет морозильное отделение.</h2>` (mirror SKU 1/3 supplier RU opening шаблон same FROSTY mini-bar family); `Технічні характеристики:`→`Технические характеристики:`; `Одна двері`→`Одна дверь` (UA `двері` plural-form-as-singular numeral construct → RU singular `дверь` correct grammar); `Одна регульована полиця розміром 360х270 мм`→`Одна регулируемая полка размером 360x270 мм` (inner-dim Cyr х U+0445 → Lat x U+0078; trailing single `мм` preserve как в UA; trailing space inside `</li>` обёртки verbatim; precedent chunk-028 b3 SKU 24 REEDNEE `330х430 мм` → `330x430 мм`); `Об'єм 72 л.`→`Объём 72 л.` (drop straight-apos U+0027; ё U+0451 в `объём`); `Температурний режим +4...+10 °C, морозильне відділення 0...-5 °C`→`Температурный режим +4...+10 &deg;C, морозильное отделение 0...-5 &deg;C` (SOFT `°` U+00B0 → `&deg;` entity x2; Lat C preserve; space-before `&deg;` faithful UA pattern); `Механічний контроль температури`→`Механический контроль температуры`; `Колір чорний`→`Цвет чёрный` (ё U+0451 в `чёрный`); `Напруга 220 В`→`Напряжение 220 В` (Cyr В U+0412 preserve); `Габарити 445х490х635 мм`→`Габариты 445мм x 490мм x 635мм` (Policy B/C — Cyr х U+0445 → Lat x U+0078 + `мм` слитно per axis; chunk-028 b3 SKU 23 FROSTY `1360x700x860` → `1360мм x 700мм x 860мм` precedent + SKU 24 REEDNEE `1360x700x850 мм` → `1360мм x 700мм x 850мм` same Policy B/C). бренд/модель/`л`/`мм`/`В`/`л.` НЕ переводим; HTML-entities `&deg;` (x2) genuine HTML. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=756820696)*

---

## SKU 7/79 — Минибар холодильный TEFCOLD UR200 (Артикул 982822688) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg — `desc UA==RU` **False** (genuine отдельный корректный русский перевод поставщика); `nm_ua`!=`nm_ru` (UA `Мінібар холодильна шафа TEFCOLD UR200` vs RU `Минибар холодильный TEFCOLD UR200`); `nm_ru`==`nazv_ru` clean RU. **Tefcold НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. LIVE-магазин Horoshop, genuine RU body НЕ переписываем. LIVE source artefacts preserve verbatim: (1) supplier RU dr `<h2>Холодильный шкаф TEFCOLD UR200 отлично подойдет...</h2>` opening (note: supplier dropped `Минибар` префикс в opening, оставил только `Холодильный шкаф` — desync vs nazv_ru `Минибар холодильный` — blknochg → НЕ правим); (2) `<li>Перенавешиваемая глухая дверь</li>` genuine RU (НЕ Перевешиваемая); (3) **SKU 7 LIVE artefact** `<li>3 pешетчатые белые полки</li>` Lat `p` U+0070 store-canonical (НЕ Cyr р U+0440) — precedent chunk-027 b7 SKU 45/52/53 Tefcold + chunk-028 b1 SKU 1-7 Tefcold same Lat-`p` Horoshop artifact на уровне магазина, blknochg → preserve verbatim, НЕ правим; (4) supplier RU temp ranges `&deg;С` Cyr С entity; (5) `Замок` faithful, `Общий / полезный объём` ё ok. **ТРЕТИЙ Tefcold blknochg в chunk-029** (Tefcold ×16 candidate-series). Tefcold UR200 — холодильный шкаф (НЕ морозильный) 200 л со стеклянной дверью без подсветки. Код `TEFCOLD UR200` Lat upper → consistent. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=982822688)*

---

## SKU 8/79 — Барный холодильный шкаф HURAKAN HKN-DB335S (Артикул 1013162766) — SKIP-НП (бренд НП-эксклюзив, тело из фида НП позже)

**Бренд:** Hurakan (НП-эксклюзивный — forward-only SKIP-правило)
**Поле:** Название модификации (RU)
**Было:** (ячейка не трогается — тело из фида НП позже)
**Стало:** не трогаем (SKIP-НП — тело из фида НП позже)

**Поле:** Описание товара (RU)
**Было:** (ячейка не трогается — тело из фида НП позже)
**Стало:** не трогаем (SKIP-НП — тело из фида НП позже)

*(SKIP-НП — `brand`=`Hurakan` ∈ {HURAKAN/Хуракан} word-boundary NP-hit → forward-only SKIP-правило: тело из фида НП позже, ячейки chunk-029-fixed.xlsx НЕ трогаем. **Hurakan ∈ НП-эксклюзивный список** (word-boundary NP-hit найден в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}) → forward-only SKIP-правило: тело из фида НП позже, ячейки chunk-029-fixed.xlsx не трогаем (Назв.мод RU + Описание RU без изменений). **ВТОРОЙ SKIP-НП в chunk-029** (вторая Hurakan-серия — HKN-DB335S после HKN-GXDB250-SL SKU 2). Source signature **`du==dr` True** + `nm_ua==nm_ru` UA word `Барна холодильна шафа HURAKAN HKN-DB335S` (UA-leak в nm-cells); `nazv_ru` clean RU `Барный холодильный шкаф HURAKAN HKN-DB335S` — desync vs nm-cells (precedent SKU 8 Hurakan Tatra/Apach SKIP-НП в chunk-028 b3 SKU 18/19 — тот же паттерн `du==dr` True + UA-leak в nm-cells). В SKIP-НП cells **НЕ правим** (тело из фида НП позже всё перепишет — brand-rule overrides signature). Кумул. SKIP-НП chunk-029 = 2 (после SKU 8). META always faithful. Открытых вопросов 0.)*

**Наблюдения по батчу SKU 1-8 (8/79) — chunk-029 (ПЕРВЫЙ батч chunk-029; смешанный blk триплет + blknochg + SKIP-НП в НОВОМ разделе `Холодильне та морозильне обладнання/Шафи настільні для бару, міні-бари (фрігобари)` — НОВЫЙ раздел в проекте: настольные барные холодильные шкафы / мини-бары (фригобары); переход от `Холодильні шафи для вина` chunk-028 SKU 60-61 → `Шафи настільні для бару, міні-бари` chunk-029 SKU 1):** **blk триплет 1 (SKU 6 FROSTY BC-70 — ПЕРВЫЙ blk триплет в chunk-029). blknotrip 0. blkv 0. blknochg 5 (SKU 1 FROSTY KWS-52M + SKU 3 FROSTY BC-90 + SKU 4 Tefcold UF200S + SKU 5 Tefcold UF200G + SKU 7 Tefcold UR200 — LIVE Horoshop genuine). blknochgeq 0. SKIP-НП 2 (SKU 2 Hurakan HKN-GXDB250-SL + SKU 8 Hurakan HKN-DB335S — Hurakan ×5 candidate начинается).** SKU 1 `970938056` FROSTY KWS-52M — **blknochg** LIVE Horoshop FROSTY mini-bar mini-template family (h2 + p + ul/9li). Supplier RU dr с `+1...+10&deg;С` Cyr С no-space-before vs UA `+1...+10 °C` Lat C — desync supplier-side. FROSTY **НЕ ∈ НП-эксклюзив**. **ПЕРВЫЙ blknochg в chunk-029**. SKU 2 `2060677611` Hurakan HKN-GXDB250-SL — **SKIP-НП** (brand=`Hurakan` ∈ {HURAKAN/Хуракан} NP-hit; cells unchanged). **ПЕРВЫЙ SKIP-НП в chunk-029** (Hurakan-серия начинается — Hurakan ×5 candidate в chunk-029 SKU 2/8/13/14/15). Source `du!=dr` genuine разный — но brand-rule overrides signature. SKU 3 `468636015` FROSTY BC-90 — **blknochg** LIVE Horoshop (mirror SKU 1 same FROSTY mini-bar template, BC-90 имеет морозильное отделение в отличие от KWS-52M). FROSTY **НЕ ∈ НП-эксклюзив**. SKU 4 `646908262` Tefcold UF200S — **blknochg** LIVE Horoshop Tefcold mini-bar freezer (нержавеющая сталь). **SKU 4-specific LIVE typo**: supplier RU dr `<li>Без подстветки</li>` opечатка (Без подс**т**ветки вместо Без подсветки) store-canonical — precedent chunk-027 b7/chunk-028 b1 Tefcold src-typos preserve verbatim в blknochg. Tefcold **НЕ ∈ НП-эксклюзив**. **ПЕРВЫЙ Tefcold blknochg в chunk-029**. SKU 5 `646911261` Tefcold UF200G — **blknochg** LIVE Horoshop Tefcold mini-bar freezer (стеклянная дверь). **SKU 5-specific structure desync**: supplier дал `<p>` opening (Мини-холодильник отлично подойдет...) вместо canonical `<h2>` mini-template — blknochg → НЕ правим. UA `скло` → RU `стекло` correctly translated в nazv_ru parens. Tefcold **НЕ ∈ НП-эксклюзив**. SKU 6 `756820696` FROSTY BC-70 — **blk триплет** **ПЕРВЫЙ blk триплет в chunk-029** (1h2 + 1p + 1ul/9li, no `<img>`/iframe/voltage-explicit отдельно; voltage в ul/li `220 В`): `desc UA==RU` True 🔴, `nm_ua==nm_ru` UA word `Мінібар FROSTY BC-70` UA-leak, `nm_ru!=nazv_ru` → AUTO Назв.мод (RU) = `Минибар FROSTY BC-70`; Описание (RU) авторский 1:1 тег-в-tag UA; **отличие от blknochg SKU 1/3 (same FROSTY mini-bar family)**: SKU 1 (KWS-52M) + SKU 3 (BC-90) supplier дал отдельный RU body dr genuine, SKU 6 (BC-70) supplier дал UA-only тело — magazine скопировал UA в RU cell (same FROSTY brand но разные supplier-paths внутри одного бренда). FROSTY **НЕ ∈ НП-эксклюзив**. SKU 7 `982822688` Tefcold UR200 — **blknochg** LIVE Horoshop Tefcold холодильный шкаф 200 л (НЕ морозильный — refrigerator). **SKU 7 LIVE artefact**: supplier RU dr `<li>3 pешетчатые белые полки</li>` Lat `p` U+0070 store-canonical (precedent chunk-027 b7 SKU 45/52/53 + chunk-028 b1 SKU 1-7 Tefcold same Lat-`p` Horoshop artifact). Tefcold **НЕ ∈ НП-эксклюзив**. SKU 8 `1013162766` Hurakan HKN-DB335S — **SKIP-НП** (mirror SKU 2 Hurakan brand; ВТОРОЙ SKIP-НП). Source `du==dr` True + UA-leak в nm-cells — same pattern как chunk-028 b3 SKU 18/19 Tatra (brand-rule overrides signature). **Открытых вопросов по батчу: 0** (b1 0). Кумулятивно chunk-029 = **0** (questions.md chunk-029 пока НЕ создаём — нет OQ). Кумулятивно SKIP-НП chunk-029 = **2** (b1 2 Hurakan). NEXT: chunk-029 b2 SKU 9-16.

*(scoped к row Артикул=1013162766)*

---
