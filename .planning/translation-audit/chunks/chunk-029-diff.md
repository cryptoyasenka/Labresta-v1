# chunk-029 translation diff (79 SKU — холодильное оборудование + оборудование для пиццерии, продолжение chunk-028)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-029 (79 SKU, продолжение chunk-028)
**Apply key:** `Артикул` (scoped per row)
**Status:** IN PROGRESS 24/79

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

## SKU 9/79 — Минибар морозильный TEFCOLD UF200SG (стекло,нерж) (Артикул 1774197557) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg pure — `desc UA==RU` **False** (genuine отдельный корректный русский перевод поставщика 595/603 байт); `nm_ua`!=`nm_ru` (UA `Мінібар морозильний TEFCOLD UF200SG (скло,нерж)` vs RU `Минибар морозильный TEFCOLD UF200SG (стекло,нерж)`); `nm_ru`==`nazv_ru` clean RU (char-level UA_ONLY=∅). **Tefcold НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. LIVE-магазин Horoshop, genuine RU body НЕ переписываем (ячейки chunk-029-fixed без изменений). LIVE source artefacts preserve verbatim: (1) supplier RU dr `<h2>Шкаф морозильный TEFCOLD UF200SG отлично подойдет...</h2>` opening + h2+p+ul/11li mini-template freezer family; (2) RU `Диапазон температур от -10&deg;С до -24&deg;С` Cyr С U+0421 entity; (3) UA `скло` → RU `стекло` в parens nazv_ru/nm_ru translated correctly; (4) inner-dim `490 х 380 мм` Cyr х U+0445 LIVE preserve (blknochg → НЕ Policy B/C для inner-dims supplier-side); (5) main-dim `600х600х850 мм` Cyr х LIVE preserve (blknochg → supplier-canonical, НЕ Policy B/C). **ЧЕТВЁРТЫЙ Tefcold blknochg в chunk-029** (Tefcold ×16 candidate-series — после SKU 4/5/7 в b1). Tefcold UF200SG — морозильный шкаф 120 л со стеклянной дверью + нерж. корпус AISI 430 (комбо стекло+нерж в одном SKU). Никаких POL1/POL2/POL4 typo-fixов в SKU 9 НЕ требуется — RU+UA bodies clean. Код `TEFCOLD UF200SG` Lat upper → consistent. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=1774197557)*

---

## SKU 10/79 — Холодильный шкаф Hata DR200S S/S201 (Артикул 1861402673) — 🟡 RU LIVE; SOFT-fix typos (UA+RU)

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU) — SOFT-fix typos (POL4+POL2 2026-05-20: opечатки RU + U+02DA→&deg;)
**Было:** `хладогент R290`
**Стало:** `хладагент R290`

**Было:** `автоотайка`
**Стало:** `автооттайка`

**Было:** `0...+10˚С `
**Стало:** `0...+10&deg;С `

**Поле:** Описание товара (UA) — SOFT-fix typos (POL4+POL2 2026-05-20: opечатки UA + U+02DA→&deg;)
**Было:** `хладогент R290`
**Стало:** `хладагент R290`

**Было:** `0...+10˚С`
**Стало:** `0...+10&deg;С`

*(blknochg_soft — `desc UA==RU` **False** (genuine отдельный RU перевод 516/535 байт); `nm_ua`!=`nm_ru` (UA `Холодильна шафа Hata DR200S S/S201` vs RU `Холодильный шкаф Hata DR200S S/S201`); `nm_ru`==`nazv_ru` clean RU. **Hata НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. LIVE-магазин Horoshop, **но содержит явные typos в ОБОИХ локалях** требующие SOFT-фикса (POL4 NEW 2026-05-20 первое применение в проекте). **NEW POLICY 4 (blknochg LIVE SOFT-typos обе локали):** ранее blknochg = strict-preserve verbatim; теперь preserve LIVE **кроме очевидных опечаток** — фиксим в обоих UA+RU cells. SOFT UA-fixes: (a) `хладогент R290` → `хладагент R290` (UA-side typo `хладогент` встречается в обеих локалях supplier-side — letter-swap `о`/`а` consistent); (b) `0...+10˚С` → `0...+10&deg;С` (POL2 NEW: U+02DA Polish ring above → `&deg;` HTML entity, Cyr С после preserve). SOFT RU-fixes: (a) `автоотайка` → `автооттайка` (RU typo: missing удвоение `т` — должно быть `автооттайка` от `оттайка`); (b) `хладогент R290` → `хладагент R290`; (c) `0...+10˚С ` → `0...+10&deg;С ` (trailing space preserve — format artifact). **LIVE preserve verbatim** (POL4 explicit exclusions): (1) leading-space `<h2> Барный` RU artifact preserve (форматный артефакт, НЕ typo); (2) UA `автовідтайка` correct Ukrainian (proper UA spelling, НЕ trogаем); (3) Cyr х в `600х615х870 мм` обе локали LIVE preserve (blknochg → НЕ Policy B/C для inner-dim supplier-canonical); (4) main `220В` no-space обе локали preserve. Hata DR200S — барный компактный холодильный шкаф 140 л, корпус AISI 201 нерж. **ПЕРВОЕ применение POL4 в проекте** (SOFT-typo fix blknochg LIVE). **Hata НЕ ∈ НП-эксклюзив** (substring match nope — `Hata` НЕ ∈ NP-SET). META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=1861402673)*

---

## SKU 11/79 — Шкаф холодильный барный REEDNEE LG128 (Артикул 1861418399) — 🔴 RU=UA + Назв.мод (RU) UA-leak

**Поле:** Название модификации (RU)
**Было:** `Холодильна шафа барна REEDNEE LG128`
**Стало:** `Шкаф холодильный барный REEDNEE LG128`

**Поле:** Описание товара (RU)
**Было:** (полностью идентично UA — украинский текст)
**Стало:** (полный перевод RU тег-в-tag):

```
<h2>Барный холодильный шкаф REEDNEE LG128 со стеклянной дверцей в чёрном корпусе.</h2> <ul>
<li>объём 128 л</li>
<li>корпус чёрный, окрашенная сталь</li>
<li>внутренняя камера из алюминия</li>
<li>2 решётчатые полки с возможностью регулирования</li>
<li>1 стеклянная дверца</li>
<li>температурный режим 0...+10&deg;С</li>
<li>хладагент R600A</li>
<li>мощность 180 Вт</li>
<li>подключение 220В</li>
<li>габариты 600мм x 520мм x 850мм</li>
</ul>
```

**Поле:** Описание товара (UA) — SOFT-fix typos (POL1+POL2 2026-05-20: opечатки UA + U+02DA→&deg;)
**Было:** `двецею`
**Стало:** `дверцею`

**Было:** `хладогент R600A`
**Стало:** `хладагент R600A`

**Было:** `0...+10˚С`
**Стало:** `0...+10&deg;С`

*(blk триплет STANDARD + UA SOFT-fix — `desc UA==RU` **True** (🔴 RU=UA — RU = полная укр. копия тела 418/418 байт); `nm_ua`==`nm_ru` `Холодильна шафа барна REEDNEE LG128` (UA-leak — body-level `_has_ua` True via `Холодильна`/`шафа`/`барна` Cyr і + щ + а UA-specific chars); `nm_ru`!=`nazv_ru` genuine RU `Шкаф холодильный барный REEDNEE LG128` → AUTO Назв.мод (RU) = genuine `nazv_ru`. **ПЕРВЫЙ REEDNEE blk триплет в chunk-029** (precedent chunk-028 b3 SKU 24 REEDNEE freezer-table same REEDNEE brand same blk триплет pattern). **REEDNEE НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. Описание (RU) — авторский полный перевод тег-в-tag (структура UA зеркалится 1:1; 1 `<h2>` + 1 `<ul>` + 10 `<li>`; no `<p>Технические характеристики:`-блок header — UA источник без него, mirror verbatim; line-breaks `\n` после `<ul>` и между `<li>` preserve). SOFT применено к авторскому RU + UA-side фиксы (POL1+POL2 NEW 2026-05-20 первое применение в проекте): (1) `<h2>Барна холодильна шафа REEDNEE LG128 зі скляною **двецею** у чорному корпусі.</h2>`→`<h2>Барный холодильный шкаф REEDNEE LG128 со стеклянной **дверцей** в чёрном корпусе.</h2>` — **POL1 UA-typo fix:** UA `двецею` → `дверцею` (missing `р` letter-skip typo) + RU `дверцей` (instrumental case correct); ё U+0451 в `чёрном`; (2) `обсяг 128 л`→`объём 128 л` (UA `обсяг`→RU `объём`; ё U+0451); (3) `корпус чорний, фарбована сталь`→`корпус чёрный, окрашенная сталь` (ё); (4) `внутрішня камера з алюмінію`→`внутренняя камера из алюминия`; (5) `2 гратчасті полиці з можливістю регулювання`→`2 решётчатые полки с возможностью регулирования` (ё U+0451 в `решётчатые`); (6) `1 скляна дверця`→`1 стеклянная дверца`; (7) `температурний режим 0...+10˚С`→`температурный режим 0...+10&deg;С` **POL2 NEW**: U+02DA Polish ring above `˚` U+02DA → `&deg;` HTML entity (semantic-correct degree sign), Cyr С U+0421 после preserve обе локали; (8) `хладогент R600A`→`хладагент R600A` **POL1 UA-typo fix обе локали**: typo `хладогент` (letter-swap `о`/`а`) → `хладагент` обе локали (RU body + UA body); (9) `потужність 180 Вт`→`мощность 180 Вт` (Cyr В U+0412); (10) `підключення 220В`→`подключение 220В` (UA `220В` слитно mirror — supplier-style, НЕ применяем `Между числом и единицей пробел` rule в blk триплет mirror UA verbatim); (11) `габарити 600х520х850 мм` Cyr х U+0445 → `габариты 600мм x 520мм x 850мм` Lat x U+0078 + `мм` слитно per axis (**Policy B/C** — precedent chunk-028 b3 SKU 23 FROSTY + SKU 24 REEDNEE same Policy B/C для главных dim в blk триплет). **UA SOFT-fix (POL1+POL2 первое применение) — Описание товара (UA) cell modifications:** `двецею`→`дверцею` + `хладогент R600A`→`хладагент R600A` + U+02DA `0...+10˚С`→`0...+10&deg;С`. бренд REEDNEE Lat consistent. **REEDNEE НЕ ∈ НП-эксклюзив** (substring nope). META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=1861418399)*

---

## SKU 12/79 — Шкаф холодильный барный REEDNEE LG198S (Артикул 1861432292) — 🔴 RU=UA + Назв.мод (RU) UA-leak

**Поле:** Название модификации (RU)
**Было:** `Холодильна шафа барна REEDNEE LG198S`
**Стало:** `Шкаф холодильный барный REEDNEE LG198S`

**Поле:** Описание товара (RU)
**Было:** (полностью идентично UA — украинский текст)
**Стало:** (полный перевод RU тег-в-tag):

```
<h2>Барный холодильный шкаф REEDNEE LG198S с двумя стеклянными дверями в чёрном корпусе.</h2> <ul>
<li>объём 198 л</li>
<li>корпус чёрный, окрашенная сталь</li>
<li>внутренняя камера из алюминия</li>
<li>4 решётчатые полки с возможностью регулирования</li>
<li>2 стеклянные раздвижные двери</li>
<li>температурный режим 0...+10&deg;С</li>
<li>хладагент R600A</li>
<li>мощность 180 Вт</li>
<li>подключение 220В</li>
<li>габариты 900мм x 520мм x 850мм</li>
</ul>
```

**Поле:** Описание товара (UA) — SOFT-fix typos (POL1+POL2 2026-05-20: opечатки UA + U+02DA→&deg;)
**Было:** `хладогент R600A`
**Стало:** `хладагент R600A`

**Было:** `0...+10˚С`
**Стало:** `0...+10&deg;С`

*(blk триплет STANDARD + UA SOFT-fix — `desc UA==RU` **True** (🔴 RU=UA 434/434); `nm_ua`==`nm_ru` `Холодильна шафа барна REEDNEE LG198S` (UA-leak); `nm_ru`!=`nazv_ru` genuine RU `Шкаф холодильный барный REEDNEE LG198S` → AUTO Назв.мод (RU). **ВТОРОЙ REEDNEE blk триплет** (mirror SKU 11 same REEDNEE brand same blk pattern — но 198 л vs 128 л, 2 раздвижные двери vs 1 дверца, 4 полки vs 2). **REEDNEE НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. Описание (RU) — авторский полный перевод тег-в-tag (структура UA 1:1; 1h2 + 1ul/10li, no separate `<p>Технические характеристики:` — mirror UA). SOFT (POL1+POL2): (1) `<h2>Барна холодильна шафа REEDNEE LG198S з двома скляними дверима в чорному корпусі.</h2>`→`<h2>Барный холодильный шкаф REEDNEE LG198S с двумя стеклянными дверями в чёрном корпусе.</h2>` (ё; instrumental case `с двумя` RU correct grammar; `скляними` → `стеклянными`); (2) `обсяг 198 л`→`объём 198 л` (ё); (3) `корпус чорний, фарбована сталь`→`корпус чёрный, окрашенная сталь` (ё); (4) `внутрішня камера з алюмінію`→`внутренняя камера из алюминия`; (5) `4 гратчасті полиці з можливістю регулювання`→`4 решётчатые полки с возможностью регулирования` (ё); (6) `2 скляні розсувні двері`→`2 стеклянные раздвижные двери` (UA `розсувні` → RU `раздвижные`); (7) `0...+10˚С`→`0...+10&deg;С` **POL2** U+02DA→entity Cyr С; (8) `хладогент R600A`→`хладагент R600A` **POL1 обе локали** typo fix; (9) `потужність`→`мощность`; (10) `220В` слитно preserve; (11) `габарити 900х520х850 мм`→`габариты 900мм x 520мм x 850мм` Policy B/C Cyr х→Lat x + `мм` слитно per axis. **UA SOFT-fix (POL1+POL2)** — Описание товара (UA): `хладогент R600A`→`хладагент R600A` + `0...+10˚С`→`0...+10&deg;С` (нет `двецею` в SKU 12 UA — корректно `дверима`/`двері`). **REEDNEE НЕ ∈ НП-эксклюзив**. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=1861432292)*

---

## SKU 13/79 — Барный холодильный шкаф HURAKAN HKN-DB205S (Артикул 2060670686) — SKIP-НП (бренд НП-эксклюзив, тело из фида НП позже)

**Бренд:** Hurakan (НП-эксклюзивный — forward-only SKIP-правило)
**Поле:** Название модификации (RU)
**Было:** (ячейка не трогается — тело из фида НП позже)
**Стало:** не трогаем (SKIP-НП — тело из фида НП позже)

**Поле:** Описание товара (RU)
**Было:** (ячейка не трогается — тело из фида НП позже)
**Стало:** не трогаем (SKIP-НП — тело из фида НП позже)

*(SKIP-НП — `brand`=`Hurakan` ∈ {HURAKAN/Хуракан} word-boundary NP-hit → forward-only SKIP-правило: тело из фида НП позже, ячейки chunk-029-fixed.xlsx НЕ трогаем. **Hurakan ∈ НП-эксклюзивный список** (word-boundary NP-hit найден в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}) → forward-only SKIP-правило: тело из фида НП позже, ячейки chunk-029-fixed.xlsx не трогаем (Назв.мод RU + Описание RU без изменений). **ТРЕТИЙ SKIP-НП в chunk-029** (Hurakan ×5 candidate продолжается после SKU 2/8 b1 → SKU 13 b2). Source signature **`du==dr` True** + `nm_ua==nm_ru` UA word `Барна холодильна шафа HURAKAN HKN-DB205S` (UA-leak); `nazv_ru` clean RU `Барный холодильный шкаф HURAKAN HKN-DB205S` — desync nm vs nazv (precedent SKU 8 b1 + SKU 14 same pattern). **В SKIP-НП cells НЕ правим** (brand-rule overrides signature; POL3 strict). HKN-DB205S — барный холодильный шкаф 185 л со стеклянной дверью, вместимость 142 бутылки/банки. Кумул. SKIP-НП chunk-029 = 3 (после SKU 13). META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=2060670686)*

---

## SKU 14/79 — Барный холодильный шкаф HURAKAN HKN-DB125H (Артикул 2060675256) — SKIP-НП (бренд НП-эксклюзив, тело из фида НП позже)

**Бренд:** Hurakan (НП-эксклюзивный — forward-only SKIP-правило)
**Поле:** Название модификации (RU)
**Было:** (ячейка не трогается — тело из фида НП позже)
**Стало:** не трогаем (SKIP-НП — тело из фида НП позже)

**Поле:** Описание товара (RU)
**Было:** (ячейка не трогается — тело из фида НП позже)
**Стало:** не трогаем (SKIP-НП — тело из фида НП позже)

*(SKIP-НП — `brand`=`Hurakan` ∈ {HURAKAN/Хуракан} NP-hit → forward-only SKIP. **Hurakan ∈ НП-эксклюзивный список** (word-boundary NP-hit найден в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}) → forward-only SKIP-правило: тело из фида НП позже, ячейки chunk-029-fixed.xlsx не трогаем (Назв.мод RU + Описание RU без изменений). **ЧЕТВЁРТЫЙ SKIP-НП в chunk-029**. Source `du==dr` True + UA-leak `Барна холодильна шафа HURAKAN HKN-DB125H` в nm-cells; `nazv_ru` clean RU; brand-rule overrides signature. HKN-DB125H — барный холодильный шкаф 113 л (54 бутылки), корпус окрашенный металл, чёрный, стеклянная дверца. Кумул. SKIP-НП chunk-029 = 4 (после SKU 14). META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=2060675256)*

---

## SKU 15/79 — Барный холодильный шкаф HURAKAN HKN-GXDB315-SL (Артикул 2060681770) — SKIP-НП (бренд НП-эксклюзив, тело из фида НП позже)

**Бренд:** Hurakan (НП-эксклюзивный — forward-only SKIP-правило)
**Поле:** Название модификации (RU)
**Было:** (ячейка не трогается — тело из фида НП позже)
**Стало:** не трогаем (SKIP-НП — тело из фида НП позже)

**Поле:** Описание товара (RU)
**Было:** (ячейка не трогается — тело из фида НП позже)
**Стало:** не трогаем (SKIP-НП — тело из фида НП позже)

*(SKIP-НП — `brand`=`Hurakan` ∈ {HURAKAN/Хуракан} NP-hit → forward-only SKIP. **Hurakan ∈ НП-эксклюзивный список** (word-boundary NP-hit найден в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}) → forward-only SKIP-правило: тело из фида НП позже, ячейки chunk-029-fixed.xlsx не трогаем (Назв.мод RU + Описание RU без изменений). **ПЯТЫЙ SKIP-НП в chunk-029**. Source signature — `du!=dr` genuine разный (RU отдельный переведённый supplier — supplier для SKU 15 дал отдельный RU body, в отличие от SKU 13/14 UA-copy); `nm_ua!=nm_ru` (UA `Барна холодильна шафа HURAKAN HKN-GXDB315-SL` vs RU `Барный холодильный шкаф HURAKAN HKN-GXDB315-SL`); `nm_ru==nazv_ru` clean RU — но brand=Hurakan **NP-hit** → STILL SKIP-НП **независимо** от signature (POL3 brand-rule **strict** — Hurakan ВСЕГДА skip). Парадокс: signature suggests blknochg (clean RU + genuine translated body), но brand-rule overrides — тело из НП-фида потом всё перепишет в любом случае. HKN-GXDB315-SL — барный холодильный шкаф 314 л со стеклянной дверью + светодиодная подсветка + AISI 201 нерж. + R600а фреон + 224 бутылки/банки. Кумул. SKIP-НП chunk-029 = 5 (после SKU 15 — Hurakan ×5 candidate **завершено**: 2/8/13/14/15 — все 5 Hurakan SKU в chunk-029 распознаны). META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=2060681770)*

---

## SKU 16/79 — Минибар Frosty BC-128 (Артикул 2077843019) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg pure — `desc UA==RU` **False** (genuine отдельный RU перевод 863/870 байт); `nm_ua`!=`nm_ru` (UA `Мінібар Frosty BC-128` vs RU `Минибар Frosty BC-128`); `nm_ru`==`nazv_ru` clean RU. **FROSTY НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. LIVE-магазин Horoshop, genuine RU body НЕ переписываем. LIVE source artefacts preserve verbatim: (1) supplier RU dr `<p>Минибар Frosty BC-128 отлично подойдет...</p>` opening (note: SKU 16 supplier дал `<p>` opening вместо `<h2>` canonical FROSTY mini-template family SKU 1/3 b1 — **SKU 16-specific structure desync** mirror SKU 5 b1 same `<p>` opening pattern); (2) RU complete multi-ul template — основной ul + Полки ul + Материал ul (более detailed чем mini-template SKU 1/3); (3) `Размеры (Д*Ш*В): 520мм x 570мм x 795мм` already **Policy B/C-style supplier-provided**: Lat x + `мм` слитно per axis — supplier сам отформатировал по Policy B/C convention (rare case — обычно supplier даёт Cyr х + trailing single `мм`); (4) `Вес: 26.50` supplier-canonical preserve (POL `NN.00→NN кг` НЕ срабатывает — `26.50`=`26,5` real decimal weight, не integer-as-float); (5) inner-dims `420х270 мм` + `420х180 мм` Cyr х U+0445 LIVE preserve (blknochg → НЕ Policy B/C для inner-dims supplier-canonical); (6) `Минибар Frosty BC-128` (Lat lowercase `Frosty` varies: SKU 1/3 used uppercase `FROSTY KWS-52M`/`FROSTY BC-90`; SKU 16 supplier-style mixed-case `Frosty BC-128` — preserve supplier-canonical); (7) supplier-translated UA `Розміри (Д*Ш*В)` → RU `Размеры (Д*Ш*В)` already correct. **ВТОРОЙ FROSTY blknochg в chunk-029** (после SKU 1 KWS-52M + SKU 3 BC-90 b1 — но SKU 16 **BC-128** имеет морозильное отделение + complete multi-ul template). Никаких POL1/POL2/POL4 typo-fixов в SKU 16 НЕ требуется — RU+UA bodies clean (no `хладогент`/`автоотайка`/ring above/letter-skip typos). Код `Frosty BC-128` Lat mixed → consistent supplier-canonical. META always faithful. Открытых вопросов 0.)*

**Наблюдения по батчу SKU 9-16 (16/79) — chunk-029 (ВТОРОЙ батч chunk-029 в разделе `Шафи настільні для бару, міні-бари (фрігобари)`; **ПЕРВОЕ применение 5 новых политик 2026-05-20** Yana lock):** **blk триплет 2 (SKU 11 + 12 REEDNEE — ПЕРВЫЙ+ВТОРОЙ REEDNEE blk триплет chunk-029). blknotrip 0. blkv 0. blknochg pure 2 (SKU 9 Tefcold UF200SG + SKU 16 FROSTY BC-128). blknochg_soft 1 (SKU 10 Hata DR200S — **ПЕРВОЕ применение POL4 SOFT-typo fix LIVE в проекте**). blknochgeq 0. SKIP-НП 3 (SKU 13/14/15 Hurakan — ЗАВЕРШЕНИЕ Hurakan ×5 candidate в chunk-029: 2/8/13/14/15).** **5 НОВЫХ ПОЛИТИК 2026-05-20 (первое применение в b2):** **POL1** UA-typo fix в blk триплете в **ОБОИХ** UA+RU локалях (SKU 11 `двецею`→`дверцею` UA + SKU 11/12 `хладогент`→`хладагент` UA). **POL2** U+02DA Polish ring above `˚` → `&deg;` HTML entity обе локали (SKU 10/11/12: `0...+10˚С`→`0...+10&deg;С` с Cyr С preserve). **POL3** SKIP-НП strict by brand — unchanged (Hurakan ВСЕГДА skip; SKU 15 Hurakan signature suggests blknochg но brand-rule overrides). **POL4** blknochg LIVE SOFT-typos обе локали (SKU 10 `автоотайка`→`автооттайка` RU + `хладогент`→`хладагент` обе; preserve `<h2> ` leading-space artifact + Lat `p` glyph artifacts). **POL5** scope = forward (b2 onwards) + retroactive cleanup 016-028 after W1 STOP. SKU 9 `1774197557` Tefcold UF200SG — **blknochg pure** LIVE Horoshop (четвёртый Tefcold blknochg chunk-029 после SKU 4/5/7 b1). h2+p+ul/11li mini-template freezer + glass+нерж AISI 430. **Никаких POL1/POL2/POL4 fix-ов НЕ требуется** (bodies clean). Tefcold НЕ ∈ НП-эксклюзив. SKU 10 `1861402673` Hata DR200S — **blknochg_soft** LIVE Horoshop **+ SOFT-fix typos POL4 первое применение в проекте**: RU `автоотайка`→`автооттайка` + `хладогент`→`хладагент` + U+02DA→`&deg;`; UA `хладогент`→`хладагент` + U+02DA→`&deg;`. LIVE preserve: leading `<h2> ` + UA `автовідтайка` correct + Cyr х в dims. Hata НЕ ∈ НП-эксклюзив. SKU 11 `1861418399` REEDNEE LG128 — **blk триплет ПЕРВЫЙ REEDNEE chunk-029** (precedent chunk-028 b3 SKU 24 REEDNEE freezer-table): `desc UA==RU` True 🔴 + nm UA-leak `Холодильна шафа барна REEDNEE LG128`, AUTO Назв.мод RU `Шкаф холодильный барный REEDNEE LG128`; AUTHORED RU 1h2+1ul/10li 1:1 тег-в-tag; SOFT: ё U+0451 + Cyr х→Lat x Policy B/C dims `600мм x 520мм x 850мм` + U+02DA→`&deg;` (POL2) + `хладогент`→`хладагент` POL1; **UA SOFT-fix POL1+POL2**: `двецею`→`дверцею` (typo) + `хладогент`→`хладагент` + `0...+10˚С`→`0...+10&deg;С`. REEDNEE НЕ ∈ НП-эксклюзив. SKU 12 `1861432292` REEDNEE LG198S — **blk триплет ВТОРОЙ REEDNEE** (mirror SKU 11 same brand 198 л 2 раздвижные двери 4 полки): AUTHORED RU 1h2+1ul/10li; SOFT-fix same pattern POL2 ring + POL1 хладагент обе локали + Policy B/C dims `900мм x 520мм x 850мм`. SKU 13 `2060670686` Hurakan HKN-DB205S — **SKIP-НП ТРЕТИЙ** (`du==dr` True + nm UA-leak; brand-rule overrides). SKU 14 `2060675256` Hurakan HKN-DB125H — **SKIP-НП ЧЕТВЁРТЫЙ** (`du==dr` True + nm UA-leak). SKU 15 `2060681770` Hurakan HKN-GXDB315-SL — **SKIP-НП ПЯТЫЙ** (`du!=dr` genuine translated + `nm_ua!=nm_ru` clean RU — но brand-rule overrides signature; POL3 strict; Hurakan ×5 candidate **ЗАВЕРШЕНО** в chunk-029: 2/8/13/14/15). SKU 16 `2077843019` FROSTY BC-128 — **blknochg pure** LIVE Horoshop (ВТОРОЙ FROSTY blknochg chunk-029 после SKU 1/3 b1, но SKU 16 BC-128 имеет морозильное отделение + complete multi-ul template). **SKU 16-specific structure desync**: supplier дал `<p>` opening вместо `<h2>` canonical (mirror SKU 5 b1 same `<p>` pattern). `Размеры (Д*Ш*В): 520мм x 570мм x 795мм` already Policy B/C supplier-provided. `Вес: 26.50` real decimal preserve. **Никаких POL1/POL2/POL4 fix-ов НЕ требуется** в SKU 16. FROSTY НЕ ∈ НП-эксклюзив. **Открытых вопросов по батчу: 0** (b2 0). Кумулятивно chunk-029 = **0** (b1 0 + b2 0). Кумулятивно SKIP-НП chunk-029 = **5** (b1 2 + b2 3 — Hurakan ×5 завершено). NEXT: chunk-029 b3 SKU 17-24.

*(scoped к row Артикул=2077843019)*

---

## SKU 17/79 — Минибар Tefcold TM52 BLACK (Артикул 2112246982) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg pure — `desc UA==RU` **False** (genuine отдельный корректный русский перевод поставщика 983/988 байт); `nm_ua`!=`nm_ru` (UA `Мінібар Tefcold TM52 BLACK` vs RU `Минибар Tefcold TM52 BLACK`); `nm_ru`==`nazv_ru` clean RU. **Tefcold НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. LIVE-магазин Horoshop, genuine RU body НЕ переписываем (ячейки chunk-029-fixed без изменений). LIVE source artefacts preserve verbatim: (1) supplier RU dr `<p>Минибар TM52 BLACK Tefcold - мини-холодильник для хранения алкогольных и безалкогольных напитков...</p>` + `<p><strong>Технические характеристики:</strong></p>` separator + 1ul/22li metadata-list template (расширенный template — больше li чем у других minibar SKU); (2) supplier dup `Светодиодная внутренняя подсветка светодиодная подсветка` — Horoshop metadata-list duplicate-output артефакт (НЕ typo letter-skip/letter-swap → POL4 НЕ trigger; full-word repetition = supplier-side rendering artifact); (3) similar dup `Крашеный металл Крашеный металл` LIVE preserve; (4) RU `+2 ... +12 &deg;C` уже `&deg;` entity supplier-provided + **Lat C** U+0043 (НЕ Cyr С — supplier choice; LIVE preserve, НЕ нормализуем в blknochg); (5) RU `Хладагент R717 (NH3)` правильно переведено (UA `Холодоагент R717 (NH3)`); (6) необычный фреон R717=NH3 аммиак (ammonia industrial refrigerant — rare для minibar; вместо R600A/R134A типичных). **СЕДЬМОЙ Tefcold blknochg в проекте** (после SKU 4/5/7 b1 chunk-029 + SKU 9 b2 chunk-029 = 4 Tefcold blknochg chunk-029; добавляем SKU 17/18/19 b3 → 7 Tefcold blknochg). Tefcold TM52 BLACK — минибар 42 л 1 дверь (Глухая non-glass), цвет чёрный, для отелей/баров/дома. Никаких POL1/POL2/POL4 fix-ов в SKU 17 НЕ требуется — RU+UA bodies clean (no `хладогент`/`автоотайка` typos, no U+02DA ring above). Код `Tefcold TM52 BLACK` Lat consistent. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=2112246982)*

---

## SKU 18/79 — Oхладитель кег Tefcold CKC6 (Артикул 2113688076) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg pure — `desc UA==RU` **False** (genuine отдельный RU перевод 934/930 байт); `nm_ua`!=`nm_ru` (UA `Охолоджувач кег Tefcold CKC6` vs RU `Oхладитель кег Tefcold CKC6` — **Lat O** U+004F вместо Cyr О в начале nm_ru/nazv_ru — supplier-side OCR-style артефакт glyph замена; LIVE preserve verbatim — НЕ trogаем); `nm_ru`==`nazv_ru` clean (оба с одинаковым Lat O). **Tefcold НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. LIVE-магазин Horoshop, genuine RU body НЕ переписываем. LIVE source artefacts preserve verbatim: (1) **Lat O glyph artifact** в `Oхладитель` U+004F (НЕ U+041E Cyr О) — Horoshop OCR-style glyph замена (precedent chunk-028 b5 SKU 4 EBASE + chunk-025 + Hata DR200S leading-space — pattern Horoshop OCR mishaps preserve verbatim); (2) supplier RU dr `<p>Охладитель кег CKC6 Tefcold - специальный холодильник, предназначенный для хранения и продажи напитков...</p>` — note дальше в body уже Cyr О `Охладитель` (только nm/nazv с Lat O — desync glyph-level между title и body); (3) supplier dup `Двери Глухие двери Глухие` partial-repetition + `Крашеный металл Крашеный металл` full-repetition — Horoshop metadata-list artifacts LIVE preserve (НЕ POL4 trigger); (4) температурный режим `+2 ... +10 &deg;C` уже `&deg;` entity + Lat C supplier-provided; (5) `Хладагент R600A` правильно переведено; (6) `Глибина` UA → `Длина` RU (size-axis label name) supplier-translated correctly. **ВОСЬМОЙ Tefcold blknochg в проекте** (после SKU 17 = седьмой). Tefcold CKC6 — охладитель кег 267 л, 2 двери, вмещает 6×20л или 1×50л кега для пива/просекко (бар/ресторан). Никаких POL1/POL2/POL4 fix-ов в SKU 18 НЕ требуется. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=2113688076)*

---

## SKU 19/79 — Минибар Tefcold TM32G BLACK (Артикул 2128174985) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg pure — `desc UA==RU` **False** (genuine отдельный RU перевод 947/1004 байт — RU длиннее UA на 57 байт); `nm_ua`!=`nm_ru` (UA `Мінібар Tefcold TM32G BLACK` vs RU `Минибар Tefcold TM32G BLACK`); `nm_ru`==`nazv_ru` clean RU. **Tefcold НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. LIVE-магазин Horoshop, genuine RU body НЕ переписываем. LIVE source artefacts preserve verbatim: (1) supplier RU dr `<p>Минибар TM32G BLACK Tefcold - мини-холодильник...</p>` + h2-style narrative + 1ul/22li metadata-list template (similar SKU 17 TM52 BLACK сестра-модель); (2) supplier dup `Светодиодная внутренняя подсветка светодиодная подсветка` Horoshop artifact LIVE preserve; (3) supplier dup `Двери Прозрачные двери` partial + `Крашеный металл Крашеный металл` full repetition LIVE preserve; (4) **UA artifact** `+5 .. +12 &deg;C` UA имеет **двойные точки** `..` (NOT тройные `...`) — supplier UA-side артефакт, RU в supplier translation уже нормализовано до `+5 ... +12 &deg;C` (тройные точки — supplier RU-side correction); LIVE preserve UA `..` artifact + LIVE preserve RU `...` correct (asymmetric supplier translation); (5) **UA artifact `Об&rsquo;єм`** — UA SKU 19 использует `&rsquo;` (U+2019 RIGHT SINGLE QUOTATION MARK) entity вместо `&#39;` (apostrophe) как другие SKUs; supplier-side entity choice — LIVE preserve; (6) `Хладагент R717 (NH3)` — снова аммиак R717 как SKU 17; sister-models TM52/TM32G используют одну hardware-platform; (7) `Глухая` SKU 17 → `Прозрачные` SKU 19 (TM32G — стеклянная glass-door variant). **ДЕВЯТЫЙ Tefcold blknochg в проекте** (после SKU 17 седьмой + SKU 18 восьмой). Tefcold TM32G BLACK — минибар 27 л 1 дверь (стеклянная glass-door variant TM-серии). Никаких POL1/POL2/POL4 fix-ов в SKU 19 НЕ требуется (UA `..` artifact = supplier choice, НЕ typo; `&rsquo;` entity = supplier choice). META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=2128174985)*

---

## SKU 20/79 — Витрина холодильная EWT INOX RT78B black (Артикул 2198692061) — 🔴 RU=UA + Назв.мод (RU) UA-leak

**Поле:** Название модификации (RU)
**Было:** `Вітрина холодильна EWT INOX RT78B black`
**Стало:** `Витрина холодильная EWT INOX RT78B black`

**Поле:** Описание товара (RU)
**Было:** (полностью идентично UA — украинский текст)
**Стало:** (полный перевод RU тег-в-tag):

```
<p>Шкаф-витрина холодильная EWT INOX RT78B предназначена для демонстрации и продажи товаров.</p> <p>Технические характеристики:</p> <ul>
<li>3 полки, регулируемые по высоте.</li>
<li>Цифровая панель управления.</li>
<li>Корпус - пластик.</li>
<li>Объём 78л.</li>
<li>Температурный режим 0...+12 &deg;С.</li>
<li>Хладагент R600a.</li>
<li>Динамическое охлаждение.</li>
<li>Верхняя подсветка и 2 LED-ленты по бокам.</li>
<li>Вес (нетто), кг: 33.8</li>
<li>Длина (нетто), мм: 428</li>
<li>Ширина (нетто), мм: 386</li>
<li>Высота (нетто), мм: 960</li>
<li>Мощность электрическая, кВт: 0.17</li>
<li>Подключение к электросети: 220V</li>
</ul> <p>Размеры в упаковке </p> <ul>
<li>Вес 36.2</li>
<li>Глубина 435</li>
<li>Ширина 475</li>
<li>Высота 1040</li>
</ul>
```

*(blk триплет STANDARD — `desc UA==RU` **True** (🔴 RU=UA — RU = полная укр. копия тела 758/758 байт); `nm_ua`==`nm_ru` `Вітрина холодильна EWT INOX RT78B black` (UA-leak — body-level `_has_ua` True via Cyr і U+0456 в `Вітрина`/`холодильна`); `nm_ru`!=`nazv_ru` genuine RU `Витрина холодильная EWT INOX RT78B black` → AUTO Назв.мод (RU) = genuine `nazv_ru`. **ПЕРВЫЙ EWT INOX blk триплет в проекте** (новый бренд для каталога LabResta — EWT INOX холодильные витрины-шкафы, plastic body + LED подсветка). **EWT INOX НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. Описание (RU) — авторский полный перевод тег-в-tag (структура UA зеркалится 1:1; **1p narrative + 1p `Технические характеристики:` separator + 1ul/14li основной + 1p `Размеры в упаковке ` (trailing space LIVE preserve UA) + 1ul/4li упаковка**; новая структура: **TWO ul** (technical + packaging) — отличается от EWT INOX от REEDNEE SKU 11/12 b2 single-ul шаблон). SOFT применено к авторскому RU (POL не применяется к UA в b3 — нет UA typos и нет U+02DA): (1) `<p>Шафа-вітрина холодильна EWT INOX RT78B призначена для демонстрації та продажу товарів.</p>`→`<p>Шкаф-витрина холодильная EWT INOX RT78B предназначена для демонстрации и продажи товаров.</p>` (UA `шафа-вітрина` → RU `шкаф-витрина` compound noun translate); (2) `<p>Технічні характеристики:</p>`→`<p>Технические характеристики:</p>`; (3) `3 полиці, регульовані за висотою.`→`3 полки, регулируемые по высоте.`; (4) `Цифрова панель управління.`→`Цифровая панель управления.`; (5) `Корпус - пластик.`→`Корпус - пластик.` (identical RU+UA — single word `Корпус`/`Корпус` same; `пластик` same UA+RU); (6) `Об&#39;єм 78л.`→`Объём 78л.` (UA `Об&#39;єм` с apostrophe entity → RU `Объём` без apostrophe + ё U+0451; LIVE preserve `78л.` no-space supplier-canonical); (7) `Температурний режим 0...+12 ℃.`→`Температурный режим 0...+12 &deg;С.` (**U+2103 ℃ DEGREE CELSIUS** в UA — distinct от U+02DA Polish ring above; POL2 целит ТОЛЬКО U+02DA, НЕ U+2103 — UA cell **НЕ модифицируем**; в AUTHORED RU нормализуем до `&deg;С` для consistency canvas-проекта Cyr С U+0421 после); (8) `Холодоагент R600a.`→`Хладагент R600a.` (UA `Холодоагент` → RU `Хладагент`; Lat `a` в `R600a` LIVE preserve glyph supplier-canonical); (9) `Динамічне охолодження.`→`Динамическое охлаждение.`; (10) `Верхнє підсвічування і 2 LED стрічки з боків.`→`Верхняя подсветка и 2 LED-ленты по бокам.` (UA `стрічки` → RU `ленты`; добавляем дефис `LED-ленты` RU-canonical writing convention); (11) `Вага (нетто)`→`Вес (нетто)`; (12) `Довжина` → `Длина`; `Глибина` → `Глубина` в упаковке (UA axis labels translated); (13) `Потужність електрична`→`Мощность электрическая`; (14) `Підключення до електромережі`→`Подключение к электросети` (UA `електромережі` → RU `электросети`); (15) `<p>Розміри в упаковці </p>`→`<p>Размеры в упаковке </p>` (UA **trailing space** before `</p>` LIVE preserve — supplier artifact mirror exactly). **POL1 НЕ trigger** (нет UA typos типа `двецею`/`хладогент` в SKU 20-22 EWT INOX). **POL2 НЕ trigger** (UA U+2103 не равно U+02DA — distinct codepoints; UA cell остаётся `0...+12 ℃` верное). **UA cell НЕ модифицируем** в b3 (chunk-029 UA-cells modified counter остаётся 3 SKU = 10/11/12 b2). EWT INOX **НЕ ∈ НП-эксклюзив** (substring nope). META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=2198692061)*

---

## SKU 21/79 — Витрина холодильная EWT INOX RT78B white (Артикул 2198699235) — 🔴 RU=UA + Назв.мод (RU) UA-leak

**Поле:** Название модификации (RU)
**Было:** `Вітрина холодильна EWT INOX RT78B white`
**Стало:** `Витрина холодильная EWT INOX RT78B white`

**Поле:** Описание товара (RU)
**Было:** (полностью идентично UA — украинский текст)
**Стало:** (полный перевод RU тег-в-tag):

```
<p>Шкаф-витрина холодильная EWT INOX RT78B предназначена для демонстрации и продажи товаров.</p> <p>Технические характеристики:</p> <ul>
<li>3 полки, регулируемые по высоте.</li>
<li>Цифровая панель управления.</li>
<li>Корпус - пластик.</li>
<li>Объём 78л.</li>
<li>Температурный режим 0...+12 &deg;С.</li>
<li>Хладагент R600a.</li>
<li>Динамическое охлаждение.</li>
<li>Верхняя подсветка и 2 LED-ленты по бокам.</li>
<li>Вес (нетто), кг: 33.8</li>
<li>Длина (нетто), мм: 428</li>
<li>Ширина (нетто), мм: 386</li>
<li>Высота (нетто), мм: 960</li>
<li>Мощность электрическая, кВт: 0.17</li>
<li>Подключение к электросети: 220V</li>
</ul> <p>Размеры в упаковке </p> <ul>
<li>Вес 36.2</li>
<li>Глубина 435</li>
<li>Ширина 475</li>
<li>Высота 1040</li>
</ul>
```

*(blk триплет STANDARD — mirror SKU 20 (same EWT INOX RT78B same body 758/758 байт identical → supplier дал одинаковое RU=UA копию для обоих цветов; **только `nm_ua`==`nm_ru` отличается black vs white**). `desc UA==RU` **True** 🔴 + nm UA-leak `Вітрина холодильна EWT INOX RT78B white`; AUTO Назв.мод RU `Витрина холодильная EWT INOX RT78B white`. **ВТОРОЙ EWT INOX blk триплет** (mirror SKU 20 same brand same RT78B-model). **EWT INOX НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. Описание (RU) **идентично SKU 20** (HTML21 = HTML20 — supplier дал одинаковое supplier-canonical описание для RT78B black + RT78B white цветов; tot же продукт разные цвета корпуса; description не отличается, только название). Все 15 SOFT-fix-translations identical SKU 20. **POL1/POL2 НЕ trigger** UA cell остаётся untouched. EWT INOX **НЕ ∈ НП-эксклюзив**. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=2198699235)*

---

## SKU 22/79 — Витрина холодильная EWT INOX RT98B white (Артикул 2288293724) — 🔴 RU=UA + Назв.мод (RU) UA-leak

**Поле:** Название модификации (RU)
**Было:** `Вітрина холодильна EWT INOX RT98B white`
**Стало:** `Витрина холодильная EWT INOX RT98B white`

**Поле:** Описание товара (RU)
**Было:** (полностью идентично UA — украинский текст)
**Стало:** (полный перевод RU тег-в-tag):

```
<p>Шкаф-витрина холодильная EWT INOX RT98B предназначена для демонстрации и продажи товаров.</p> <p>Технические характеристики:</p> <ul>
<li>4 полки, регулируемые по высоте.</li>
<li>Цифровая панель управления.</li>
<li>Корпус - пластик.</li>
<li>Объём 98 л.</li>
<li>Температурный режим 0...+12 &deg;С.</li>
<li>Хладагент R600a.</li>
<li>Динамическое охлаждение.</li>
<li>Верхняя подсветка и 2 LED-ленты по бокам.</li>
<li>Вес (нетто), кг: 38</li>
<li>Длина (нетто), мм: 428</li>
<li>Ширина (нетто), мм: 386</li>
<li>Высота (нетто), мм: 1110</li>
<li>Мощность электрическая, кВт: 0.17</li>
<li>Подключение к электросети: 220V</li>
</ul> <p>Размеры в упаковке </p> <ul>
<li>Вес 41</li>
<li>Глубина 435</li>
<li>Ширина 475</li>
<li>Высота 1180</li>
</ul>
```

*(blk триплет STANDARD — `desc UA==RU` **True** 🔴 (756/756 байт — 2 байта короче SKU 20/21 за счёт `98 л` vs `78л` spacing); `nm_ua`==`nm_ru` `Вітрина холодильна EWT INOX RT98B white` (UA-leak); `nm_ru`!=`nazv_ru` clean RU `Витрина холодильная EWT INOX RT98B white` → AUTO Назв.мод RU. **ТРЕТИЙ EWT INOX blk триплет** (RT98B — sister-model к RT78B, **98 л larger variant**, 4 полки vs 3, higher cabinet 1110мм vs 960мм, packaging 1180мм vs 1040мм). **EWT INOX НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. Описание (RU) — AUTHORED 1:1 mirror UA structure (same двойной ul template SKU 20/21). Differences vs SKU 20: (1) `4 полиці` → `4 полки` (4 shelves в higher cabinet, vs 3); (2) `Об&#39;єм 98 л.` → `Объём 98 л.` (UA пробел перед `л.` SKU 22-specific spacing — vs SKU 20/21 `78л.` no-space; supplier varying convention внутри EWT INOX family); (3) `Вага (нетто), кг: 38` → `Вес (нетто), кг: 38` (integer кг, no decimal); (4) `Висота (нетто), мм: 1110` → `Высота (нетто), мм: 1110` (taller cabinet); (5) packaging `Вага 41` → `Вес 41`; `Висота 1180` → `Высота 1180` (larger packaging для taller cabinet). Все остальные 11 SOFT-fix-translations identical SKU 20. **POL1/POL2 НЕ trigger** UA остаётся untouched. EWT INOX **НЕ ∈ НП-эксклюзив**. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=2288293724)*

---

## SKU 23/79 — Холодильный минибар Hendi 233900 (Артикул 1158533303) — 🔴 RU=UA + Назв.мод (RU) UA-leak

**Поле:** Название модификации (RU)
**Было:** `Холодильний мінібар Hendi 233900`
**Стало:** `Холодильный минибар Hendi 233900`

**Поле:** Описание товара (RU)
**Было:** (полностью идентично UA — украинский текст)
**Стало:** (полный перевод RU тег-в-tag):

```
<h2>Холодильный минибар Hendi 233900 с температурным режимом от +2°С до +10°С.</h2>
<p>Технические характеристики:</p>
<ul>
<li>объём 118 л</li>
<li>габариты: 500мм x 500мм x 900мм</li>
<li>стальной корпус, камера внутри из экструдированного алюминия</li>
<li>закалённая стеклянная дверь с пластиковой рамой</li>
<li>с замком</li>
<li>статическое охлаждение, поддерживаемое вентилятором</li>
<li>автоматическое размораживание, генератор расположен под камерой</li>
<li>светодиодное освещение</li>
<li>цифровой дисплей</li>
<li>электронный термостат</li>
<li>4 регулируемые нескользящие ножки</li>
<li>2 хромированные полки</li>
</ul>
```

*(blk триплет STANDARD — `desc UA==RU` **True** 🔴 (608/608 байт); `nm_ua`==`nm_ru` `Холодильний мінібар Hendi 233900` (UA-leak — Cyr і U+0456 в `Холодильний`/`мінібар`); `nm_ru`!=`nazv_ru` genuine RU `Холодильный минибар Hendi 233900` → AUTO Назв.мод RU. **ПЕРВЫЙ Hendi blk триплет в проекте** (новый бренд для каталога LabResta — Hendi профессиональный кухонный/барный equipment, польская/немецкая компания). **Hendi НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. Описание (RU) — авторский полный перевод тег-в-tag (структура UA зеркалится 1:1; **1h2 narrative + 1p `Технические характеристики:` separator + 1ul/12li**; newline-separated `<li>` каждая на отдельной строке — **отличается от EWT INOX SKU 20-22** где `<li>` inline в `<ul>` блоке; structural diversity supplier-side между EWT INOX и Hendi). SOFT применено к авторскому RU: (1) `<h2>Холодильний мінібар Hendi 233900 з температурним режимом від +2°С до +10°С.</h2>`→`<h2>Холодильный минибар Hendi 233900 с температурным режимом от +2°С до +10°С.</h2>` (UA `від ... до ...` → RU `от ... до ...`; **U+00B0 ° DEGREE SIGN** в UA — **distinct от U+02DA Polish ring above** и distinct от U+2103 ℃ DEGREE CELSIUS; POL2 целит ТОЛЬКО U+02DA, НЕ U+00B0 — LIVE preserve `°С` Cyr С U+0421 в обоих локалях); (2) `<p>Технічні характеристики:</p>`→`<p>Технические характеристики:</p>`; (3) `обсяг 118 л`→`объём 118 л` (lowercase — mid-h2-sentence не capitalized; UA `обсяг` → RU `объём` ё U+0451); (4) `габарити: 500х500х900 мм`→`габариты: 500мм x 500мм x 900мм` (**Policy B/C** Cyr х U+0445 → Lat x U+0078 + `мм` слитно per axis — precedent chunk-028 b3 SKU 23 FROSTY + SKU 24 REEDNEE + chunk-029 b2 SKU 11/12 REEDNEE; lowercase `габариты` mid-list); (5) `сталевий корпус, камера всередині з екструдованого алюмінію`→`стальной корпус, камера внутри из экструдированного алюминия` (UA `сталевий` → RU `стальной`; `всередині` → `внутри`); (6) `загартована скляні двері з пластиковою рамою`→`закалённая стеклянная дверь с пластиковой рамой` (**UA supplier-side артефакт**: `загартована` singular fem + `скляні двері` plural — grammatical inconsistency UA-side; RU translate как singular `дверь` для 1-дверного минибара — semantic correctness > literal mirror; ё U+0451 в `закалённая`); (7) `з замком`→`с замком`; (8) `статичне охолодження, підтримуване вентилятором`→`статическое охлаждение, поддерживаемое вентилятором`; (9) `автоматичне розморожування, генератор розташований під камерою`→`автоматическое размораживание, генератор расположен под камерой` (UA `розташований` past-participle → RU `расположен` short-form); (10) `світлодіодне освітлення`→`светодиодное освещение`; (11) `цифровий дисплей`→`цифровой дисплей`; (12) `електронний термостат`→`электронный термостат`; (13) `4 регульовані нековзні ніжки`→`4 регулируемые нескользящие ножки` (UA `регульовані` → RU `регулируемые`; `нековзні` → `нескользящие`); (14) `2 хромовані полиці`→`2 хромированные полки` (UA `хромовані полиці` → RU `хромированные полки`). **POL1 НЕ trigger** (нет UA typos). **POL2 НЕ trigger** (U+00B0 ≠ U+02DA). **UA cell НЕ модифицируем** в b3. Hendi **НЕ ∈ НП-эксклюзив** (substring nope — `Hendi` НЕ ∈ NP-SET). META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=1158533303)*

---

## SKU 24/79 — Холодильный минибар Hendi 233917 (Артикул 1158547556) — 🔴 RU=UA + Назв.мод (RU) UA-leak

**Поле:** Название модификации (RU)
**Было:** `Холодильний мінібар Hendi 233917`
**Стало:** `Холодильный минибар Hendi 233917`

**Поле:** Описание товара (RU)
**Было:** (полностью идентично UA — украинский текст)
**Стало:** (полный перевод RU тег-в-tag):

```
<h2>Холодильный минибар Hendi 233917 с температурным режимом от +2°С до +10°С.</h2>
<p>Технические характеристики:</p>
<ul>
<li>объём 228 л</li>
<li>габариты: 900мм x 500мм x 900мм</li>
<li>стальной корпус, камера внутри из экструдированного алюминия</li>
<li>2 раздвижные двери из закалённого стекла с пластиковой рамой</li>
<li>с замком</li>
<li>статическое охлаждение, поддерживаемое вентилятором</li>
<li>автоматическое размораживание, генератор расположен под камерой</li>
<li>светодиодное освещение</li>
<li>цифровой дисплей</li>
<li>электронный термостат</li>
<li>4 регулируемые нескользящие ножки</li>
<li>4 хромированные полки</li>
</ul>
```

*(blk триплет STANDARD — `desc UA==RU` **True** 🔴 (621/621 байт — 13 байт длиннее SKU 23 за счёт `2 розсувні двері з загартованим склом` longer phrase vs `загартована скляні двері`); `nm_ua`==`nm_ru` `Холодильний мінібар Hendi 233917` (UA-leak); `nm_ru`!=`nazv_ru` clean RU `Холодильный минибар Hendi 233917` → AUTO Назв.мод RU. **ВТОРОЙ Hendi blk триплет** (mirror SKU 23 same Hendi brand same h2-p-ul шаблон). **Hendi НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. Описание (RU) — AUTHORED 1:1 mirror UA structure (same 1h2+1p+1ul/12li шаблон). Differences vs SKU 23: (1) h2 `Hendi 233917` (vs 233900); (2) `обсяг 228 л` → `объём 228 л` (larger 228 л vs 118 л — двухдверный variant); (3) `габарити: 900х500х900 мм` → `габариты: 900мм x 500мм x 900мм` (Policy B/C; 900мм длина vs 500мм SKU 23 — wider 2-door cabinet); (4) 4-й li **заменён**: `загартована скляні двері з пластиковою рамою` (singular в SKU 23) → `2 розсувні двері з загартованим склом з пластиковою рамою` → RU `2 раздвижные двери из закалённого стекла с пластиковой рамой` (двойные раздвижные двери SKU 24-specific; ё U+0451 в `закалённого`; UA `розсувні` → RU `раздвижные`); (5) последняя li `4 хромированные полки` (vs `2 хромированные полки` SKU 23 — больше полок в larger variant). Все остальные SOFT-translations identical SKU 23. **POL1/POL2 НЕ trigger**. **UA cell НЕ модифицируем**. Hendi **НЕ ∈ НП-эксклюзив**. META always faithful. Открытых вопросов 0.)*

**Наблюдения по батчу SKU 17-24 (24/79) — chunk-029 (ТРЕТИЙ батч chunk-029 в разделе `Шафи настільні для бару, міні-бари (фрігобари)`; **ЧИСТЫЙ батч — никаких НОВЫХ применений 5 политик 2026-05-20** — все 5 POL уже применены первый раз в b2):** **blk триплет 5 (SKU 20+21+22 EWT INOX RT78B black/white + RT98B white **ПЕРВЫЕ EWT INOX в проекте** + SKU 23+24 Hendi 233900+233917 **ПЕРВЫЕ Hendi в проекте** — два новых бренда blk-классифицированы одним batch). blknotrip 0. blkv 0. blknochg pure 3 (SKU 17 Tefcold TM52 BLACK + SKU 18 Tefcold CKC6 + SKU 19 Tefcold TM32G BLACK — **седьмой/восьмой/девятый Tefcold blknochg в проекте**). blknochg_soft 0. blknochgeq 0. SKIP-НП 0 (Hurakan ×5 уже завершено в b2; в b3 нет НП-эксклюзив брендов).** **5 политик 2026-05-20 в b3: НЕ-применения / preserve unchanged:** **POL1** (UA-typo fix blk обе локали) **НЕ trigger** — нет typos типа `двецею`/`хладогент` в UA cells SKU 17-24 (Tefcold supplier UA уже clean: `Холодоагент` правильное укр. написание; EWT INOX/Hendi UA тоже clean — нет letter-skip/swap typos). **POL2** (U+02DA→`&deg;`) **НЕ trigger** — источник в b3 использует U+2103 ℃ DEGREE CELSIUS (SKU 20-22 EWT INOX `0...+12 ℃`) или U+00B0 ° DEGREE SIGN (SKU 23-24 Hendi `+2°С до +10°С`), **но НЕ U+02DA Polish ring above** — POL2 целит ТОЛЬКО U+02DA (distinct codepoints, НЕ нормализуем U+2103/U+00B0). В AUTHORED RU bodies для blk триплет SKU 20-22 нормализуем до `&deg;С` для проектной consistency, но UA cells остаются untouched. **POL3** (SKIP-НП strict by brand) unchanged — нет НП-эксклюзив брендов в b3 (Hurakan ×5 завершено b1+b2). **POL4** (blknochg LIVE SOFT-typos) **НЕ trigger** — нет typos в b3 blknochg bodies SKU 17/18/19 (supplier RU clean: правильное `Хладагент` без `хладогент` typo, нет `автоотайка`, нет U+02DA). **POL5** unchanged. **UA-cells modified counter b3 = 0** (chunk-029 кумул. UA-cells modified остаётся 3 SKU = 10/11/12 b2 — НЕ растёт в b3). SKU 17 `2112246982` Tefcold TM52 BLACK — **blknochg pure** LIVE Horoshop (седьмой Tefcold blknochg в проекте после SKU 4/5/7 b1 + SKU 9 b2). Minibar 42 л 1 Глухая дверь + R717 (NH3) аммиак refrigerant (rare для minibar). p+p+ul/22li metadata-list расширенный template + supplier dup `Светодиодная подсветка светодиодная подсветка` LIVE preserve (Horoshop artifact, НЕ POL4 trigger). **Никаких POL fix-ов НЕ требуется** (body clean). Tefcold НЕ ∈ НП-эксклюзив. SKU 18 `2113688076` Tefcold CKC6 — **blknochg pure** LIVE Horoshop (восьмой Tefcold blknochg). Охладитель кег 267 л 2 двери 6×20л/1×50л кега для пива/просекко. **LIVE preserve Lat O glyph artifact** `Oхладитель` U+004F в nm/nazv (НЕ Cyr О U+041E) — Horoshop OCR-style замена; body уже Cyr О `Охладитель` correctly — desync glyph-level title vs body LIVE preserve. **Никаких POL fix-ов НЕ требуется**. SKU 19 `2128174985` Tefcold TM32G BLACK — **blknochg pure** LIVE Horoshop (девятый Tefcold blknochg). Sister-model TM52 BLACK SKU 17 same hardware-platform но glass-door variant (Прозрачные vs Глухие) + 27 л меньше + R717 аммиак тот же. **UA artifact `+5 .. +12`** двойные точки (vs тройные SKU 17/18) + **UA `Об&rsquo;єм`** U+2019 entity вместо `&#39;` — supplier-side choices LIVE preserve. RU supplier имеет тройные точки `+5 ... +12` correctly (asymmetric supplier translation). **Никаких POL fix-ов**. SKU 20 `2198692061` EWT INOX RT78B black — **blk триплет ПЕРВЫЙ EWT INOX в проекте** (новый бренд). `desc UA==RU` True 🔴 (758/758) + nm UA-leak `Вітрина холодильна EWT INOX RT78B black`, AUTO Назв.мод RU `Витрина холодильная EWT INOX RT78B black`; AUTHORED RU 1p+1p+1ul/14li+1p+1ul/4li (**TWO ul** technical + packaging — отличается от REEDNEE SKU 11/12 b2 single-ul шаблон); SOFT: ё U+0451 в `Объём` + Cyr `Шкаф-витрина холодильная` translation + `LED-ленты` RU-canonical дефис + trailing-space `<p>Размеры в упаковке </p>` LIVE preserve UA artifact + AUTHORED RU `&deg;С` normalize (UA `℃` U+2103 LIVE preserve — POL2 НЕ trigger). EWT INOX НЕ ∈ НП-эксклюзив. SKU 21 `2198699235` EWT INOX RT78B white — **blk триплет ВТОРОЙ EWT INOX** (mirror SKU 20 same RT78B-model разные цвета); supplier дал **идентичный body 758/758** для black + white цветов (HTML21 == HTML20 — только nm differs); все 14 SOFT-translations identical SKU 20. SKU 22 `2288293724` EWT INOX RT98B white — **blk триплет ТРЕТИЙ EWT INOX** (RT98B sister-model к RT78B, **98 л larger**, 4 полки vs 3, higher cabinet 1110мм vs 960мм, packaging 1180мм vs 1040мм). Same TWO-ul шаблон. SKU 22-specific differences vs SKU 20: `4 полки`, `Объём 98 л.` (пробел перед `л.` — supplier UA-spacing SKU 22-specific vs `78л.` no-space SKU 20/21), `Вес 38` (integer), `Высота 1110/1180`. SKU 23 `1158533303` Hendi 233900 — **blk триплет ПЕРВЫЙ Hendi в проекте** (новый бренд — Hendi профессиональный кухонный/барный equipment). `desc UA==RU` True 🔴 (608/608) + nm UA-leak `Холодильний мінібар Hendi 233900`, AUTO Назв.мод RU `Холодильный минибар Hendi 233900`. AUTHORED RU **1h2+1p+1ul/12li newline-separated `<li>`** — **отличается от EWT INOX SKU 20-22 inline-`<li>` шаблон**; structural diversity supplier-side между EWT INOX и Hendi. SOFT: ё U+0451 в `закалённая стеклянная дверь` + lowercase `объём 118 л` mid-list + Policy B/C `500мм x 500мм x 900мм` Lat x + UA `загартована скляні двері` (UA supplier grammar inconsistency singular fem `загартована` + plural `двері`) → RU singular `закалённая стеклянная дверь` semantic correctness > literal mirror + **U+00B0 ° DEGREE SIGN** в обоих локалях LIVE preserve (POL2 НЕ trigger — distinct от U+02DA). Hendi НЕ ∈ НП-эксклюзив. SKU 24 `1158547556` Hendi 233917 — **blk триплет ВТОРОЙ Hendi** (mirror SKU 23; 228 л larger двухдверный variant — `2 розсувні двері` → `2 раздвижные двери из закалённого стекла`; `900х500х900 мм` Policy B/C; `4 хромированные полки` vs 2). Same Hendi шаблон + same h2 `+2°С до +10°С` U+00B0 preserve. **Открытых вопросов по батчу: 0** (b3 0). Кумулятивно chunk-029 = **0** (b1 0 + b2 0 + b3 0). Кумулятивно SKIP-НП chunk-029 = **5** (b1 2 + b2 3 — Hurakan ×5 завершено, b3 не добавляет). Кумулятивно UA-cells modified в проекте = **3 SKU** (10/11/12 b2 — b3 не добавляет, UA cells в b3 untouched). NEXT: chunk-029 b4 SKU 25-32.

*(scoped к row Артикул=1158547556)*

---
