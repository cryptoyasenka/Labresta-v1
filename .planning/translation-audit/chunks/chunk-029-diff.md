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

## SKU 25/79 — Минибар морозильный TEFCOLD UF200 (Артикул 646869605) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg pure — `desc UA==RU` **False** (genuine отдельный RU перевод 657/660 байт; supplier дал отдельный RU body для UF200 — стандартный mini-template UF-серии); `nm_ua`!=`nm_ru` (UA `Мінібар морозильний TEFCOLD UF200` vs RU `Минибар морозильный TEFCOLD UF200`); `nm_ru`==`nazv_ru` clean RU. **Tefcold НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. LIVE-магазин Horoshop, genuine RU body НЕ переписываем. LIVE source artefacts preserve verbatim: (1) supplier RU dr `<h2>Шкаф морозильный TEFCOLD UF200 отлично подойдет для размещения на небольшой площади. Используется для хранения замороженных продуктов.</h2>` + `<p>Технические характеристики:</p>` separator + 1ul/10li newline-separated metadata-list (standard UF-серия mini-template); (2) RU `-10&deg;С до -24&deg;С` Cyr С U+0421 entity supplier-provided (без space перед `&deg;`) — UA `-10&deg;С до -24&deg;С` идентично (`&deg;С` entity обе локали — POL2 НЕ trigger, нет U+02DA); (3) `2 фиксированных полки` SKU 25-specific (vs `3 pешетчатые` SKU 26/30/31 Lat-`p` artifact — SKU 25 без Lat-`p` потому что `фиксированных` другое слово); (4) `Габариты 600х600х850 мм` Cyr х U+0445 обе локали LIVE preserve (blknochg dim supplier-canonical); (5) UA `Об&#39;єм корисний 120 л` → RU `Объем полезный 120 л` (no ё — supplier выбрал `Объем` без ё, LIVE preserve); (6) `Электронный термостат` correctly translated. **ДЕСЯТЫЙ Tefcold blknochg в проекте** (после SKU 17/18/19 b3 = седьмой/восьмой/девятый; SKU 4/5/7 b1 + SKU 9 b2 + SKU 17/18/19 b3 + SKU 25 b4 = 7 Tefcold blknochg в chunk-029). Tefcold UF200 — морозильный шкаф/минибар 120 л 2 фиксированных полки белый корпус с замком (UF-серия mini-freezer для дома/баров). **Никаких POL1/POL2/POL4 fix-ов в SKU 25 НЕ требуется** — RU+UA bodies clean (нет `хладогент`/`автоотайка` typos, нет U+02DA ring above; `&deg;С` уже entity). Код `TEFCOLD UF200` Lat consistent. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=646869605)*

---

## SKU 26/79 — Минибар холодильный TEFCOLD UR200S (корпус нерж) (Артикул 982828094) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg pure — `desc UA==RU` **False** (genuine отдельный RU перевод 873/884 байт; supplier дал отдельный RU body для UR200S); `nm_ua`!=`nm_ru` (UA `Мінібар холодильна шафа TEFCOLD UR200S (корпус нерж)` — note **UA `холодильна шафа` 2-word vs RU `холодильный` 1-word** asymmetric translation supplier-side; RU `Минибар холодильный TEFCOLD UR200S (корпус нерж)`); `nm_ru`==`nazv_ru` clean. **Tefcold НЕ ∈ НП-эксклюзив**. LIVE-магазин Horoshop, genuine RU body НЕ переписываем. LIVE source artefacts preserve verbatim: (1) supplier RU dr `<p>Шкаф холодильный TEFCOLD UR200S отлично подойдет для размещения на небольшой площади. Используется для хранения продуктов.</p>` opening `<p>` вместо `<h2>` (mirror SKU 5 b1 + SKU 16 b2 same `<p>` opening pattern Tefcold/FROSTY supplier-side variability); (2) **SKU 26 LIVE artefact** `<li>3 pешетчатые белые полки; 2шт - 502x440 мм и 1шт - 502x211 мм</li>` — **Lat `p` U+0070** store-canonical (НЕ Cyr р U+0440) в `3 pешетчатые` — precedent chunk-027 b7 SKU 45/52/53 Tefcold + chunk-028 b1 SKU 1-7 Tefcold + chunk-029 b1 SKU 7 Tefcold UR200 (same hardware-platform UR-серия) Lat-`p` artifact preserve verbatim в blknochg (Horoshop OCR-style замена глифа, supplier давным-давно ввёл Lat `p`); inner-dim `502x440` + `502x211` уже **Lat x** U+0078 supplier-provided (rare — обычно Cyr х; SKU 26-specific supplier дал Lat x в полки-разм); (3) `Общий / полезный объем: 130 / 119 л` no-ё `объем` LIVE preserve (vs ё `объём` в других SKUs — supplier choice; LIVE preserve в blknochg); (4) RU `+2&deg;С до +10&deg;С` Cyr С `&deg;` entity LIVE preserve обе локали; (5) `Перенавешиваемая глухая дверь` correctly translated UA `Перевішувана глуха дверця`; (6) **дублированный `Замок`** в supplier dr — `<li>Замок</li>` встречается дважды в одном ul (после `Электронный термостат` и после `внутренняя отделка АБС`) — Horoshop metadata-list duplicate artifact (НЕ POL4 trigger; full-word repetition supplier-side rendering, идентично SKU 17/18/19 Tefcold dup pattern; УПС, UA-side тот же dup `Замок` дважды — symmetric LIVE preserve); (7) inner-dim `510 x 485 x 620 мм` + main-dim `600 x 600 x 850 мм` — **уже Lat x U+0078 supplier-provided** с пробелами вокруг + trailing single `мм` (SKU 26 supplier дал Lat x для main dims тоже — rare как SKU 16 b2 FROSTY BC-128 supplier-side Policy B/C-ish format; LIVE preserve в blknochg, НЕ Policy B/C форсим); (8) trailing `<p> </p>` empty paragraph артефакт обе локали LIVE preserve (Horoshop wysiwyg paste artifact). **ОДИННАДЦАТЫЙ Tefcold blknochg в проекте**. Tefcold UR200S — холодильный шкаф/минибар 130/119 л нержавеющая сталь корпус 3 решетчатые белые полки. **Никаких POL1/POL2/POL4 fix-ов в SKU 26 НЕ требуется** — body clean без typos (`хладогент`/`автоотайка` отсутствуют; `&deg;` entity ОК; Lat `p` = OCR glyph artifact preserve, НЕ letter-skip typo). UA `корисний` правильное укр. (нет typo `корисливий` как в SKU 27/28). META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=982828094)*

---

## SKU 27/79 — Минибар холодильный TEFCOLD BC85 (Артикул 982994827) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg pure — `desc UA==RU` **False** (genuine отдельный RU перевод 891/905 байт); `nm_ua`!=`nm_ru` (UA `Мінібар холодильний TEFCOLD BC85` vs RU `Минибар холодильный TEFCOLD BC85`); `nm_ru`==`nazv_ru` clean. **Tefcold НЕ ∈ НП-эксклюзив**. LIVE-магазин Horoshop, genuine RU body НЕ переписываем. LIVE source artefacts preserve verbatim: (1) supplier RU dr `<p>Мини-холодильник отлично подойдет для размещения на небольшой площади. Используется для хранения продуктов.</p>` opening `<p>` (mirror SKU 26 same `<p>` pattern); (2) **SKU 27 LIVE artefact** `<li>3 pешетчатые белые полки, размером 410 x 353 мм</li>` — **Lat `p` U+0070** store-canonical (НЕ Cyr р) — Tefcold Lat-`p` pattern continuation (precedent SKU 7 b1 + SKU 26 b4 + chunk-027/028 Tefcold series); inner-dim `410 x 353` уже **Lat x** supplier-provided; (3) **UA SKU 27 supplier typo `Загальний/корисливий об'єм: 92 / 85 л`** — UA `корисливий` (`корисливий` ≠ `корисний` — extra `-лив-` insert; должно быть `Загальний/корисний об'єм`); **POL4 НЕ trigger** для UA `корисливий` (POL4 список explicit typos = `хладогент`/`автоотайка`/`подстветки`/`двецею` — closed set, b4 НЕ расширяет; POL5 retroactive cleanup deferred ПОСЛЕ W1 STOP — `корисливий` candidate для POL5 expansion sweep); LIVE preserve UA `корисливий` artifact в b4; RU supplier dr `Общий / полезный объем: 92 / 85 л` clean (no `корисливий` calque — supplier translated correctly RU-side, asymmetric UA-typo vs RU-clean); (4) **distinct degree-glyph asymmetric translation**: UA `Діапазон температур від +2 °C до +10 °C` — **U+00B0 ° DEGREE SIGN** + space-before + **Lat C** U+0043 (supplier UA-side typographic choice); RU `Диапазон температур от +2&deg;С до +10&deg;С` — `&deg;` entity + no-space + **Cyr С** U+0421; **POL2 НЕ trigger** (UA U+00B0 ≠ U+02DA Polish ring above; precedent chunk-029 b3 SKU 23/24 Hendi same U+00B0 distinct codepoint LIVE preserve); LIVE preserve asymmetric supplier translation обе локали; (5) `Распашная стеклянная дверь` correctly translated UA `Відкривні скляні двері` (UA plural-fem `двері` → RU singular `дверь` semantic correctness для 1-дверного minibar; UA supplier-side grammar inconsistency `двері` plural noun для одной двери — same pattern как SKU 23 Hendi b3); (6) `Гнутая перенавешиваемая стеклянная дверь` correctly translated UA `Гнуті перенавішовані скляні двері`; (7) **дублированный `Замок`** в supplier dr (после `Электронный термостат` и после `внутренняя отделка АБС`) — same SKU 26 supplier rendering artifact LIVE preserve обе локали; (8) main-dim `503 x 567 x 775 мм` + inner-dim `410 x 415 x 630 мм` — **уже Lat x** supplier-provided обе локали (Tefcold BC85 supplier дал Lat x как SKU 26); (9) trailing `<p> </p>` artifact LIVE preserve. **ДВЕНАДЦАТЫЙ Tefcold blknochg в проекте**. Tefcold BC85 — мини-холодильник 92/85 л распашная стеклянная дверь со светодиодной подсветкой серая рама панель белый корпус. **Никаких POL1/POL2/POL4 fix-ов в SKU 27 НЕ требуется** — RU body clean (no `хладогент`/`автоотайка` typos; нет U+02DA); UA `корисливий` artifact preserve (POL4 closed-set list НЕ включает `корисливий`/`корисний` — этот typo candidate для POL5 retroactive expansion sweep post-W1-STOP). META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=982994827)*

---

## SKU 28/79 — Минибар холодильный TEFCOLD TM42 BLACK (Артикул 1153797472) — SOFT-fix `Хладогент`→`Хладагент` POL4 обе локали

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** `<li>Хладогент: NH3</li>`
**Стало:** `<li>Хладагент: NH3</li>`

**Поле:** Описание товара (UA)
**Было:** `<li>Хладогент: NH3</li>`
**Стало:** `<li>Хладагент: NH3</li>`

*(blknochg_soft — `desc UA==RU` **False** (genuine отдельный RU перевод 964/981 байт); `nm_ua`!=`nm_ru` (UA `Мінібар холодильний TEFCOLD TM42 BLACK` vs RU `Минибар холодильный TEFCOLD TM42 BLACK`); `nm_ru`==`nazv_ru` clean. **Tefcold НЕ ∈ НП-эксклюзив**. LIVE-магазин Horoshop, body genuine с POL4 typo fix. **POL4 ВТОРОЕ применение в проекте** (после SKU 10 b2 Hata DR200S `автоотайка`→`автооттайка` + `хладогент R290`→`хладагент R290` обе локали + POL2 U+02DA → b4 SKU 28 Tefcold TM42 BLACK `Хладогент: NH3`→`Хладагент: NH3` обе локали). POL4 explicit typo pattern: `хладогент` → `хладагент` (letter-swap `о`/`а`; mirror SKU 10 b2 same `хладогент`→`хладагент` POL4 pattern). **Asymmetric capitalization в SKU 28**: SKU 28 supplier dr использует Capitalize-first `Хладогент: NH3` (vs SKU 10 b2 lower-case `хладогент R290`); POL4 letter-swap pattern одинаков (`-о-` → `-а-` в middle stem), capitalization preserve (Capitalize-first → Capitalize-first). **POL4 на UA cell tooo**: UA supplier dr тоже использует `Хладогент: NH3` (asymmetric capitalization same Capitalize-first) → UA `Хладогент: NH3` → `Хладагент: NH3` POL4 SOFT-fix UA-side (note: UA `Хладагент` тоже валидное укр. написание; precedent SKU 10 b2 UA `хладогент`→`хладагент` mirror RU letter-swap). **POL4 НЕ trigger для других UA typos в SKU 28**: UA содержит **`Загальний/корисливий об'єм`** (typo `корисливий` ≠ `корисний`) + **`2 шишетчасті сірі полиці`** (typo `шишетчасті` ≠ `гратчасті`/`решітчасті` — двойная letter-skip + skip) — оба artefact preserve (POL4 closed-set list НЕ включает `корисливий`/`шишетчасті`; candidate для POL5 retroactive expansion post-W1-STOP); RU supplier dr correctly translate UA-typos: `Общий / полезный объем: 36 / 34 л` RU clean (asymmetric UA-typo vs RU-clean — same pattern как SKU 27); RU `2 pешетчатые серые полки` clean (но Lat `p` artifact). LIVE source artefacts preserve verbatim: (1) supplier RU dr `<p>Мини-холодильник отлично подойдет для размещения на небольшой площади. Используется для хранения продуктов.</p>` opening (mirror SKU 27); (2) **SKU 28 LIVE artefacts двойные Lat `p`**: RU `<li>1 pаспашная глухая дверь</li>` + `<li>2 pешетчатые серые полки</li>` — **двойной Lat `p` U+0070** store-canonical (`pаспашная` 1-pcs + `pешетчатые` 2-pcs); UA mirror **`1 pаспашні глухі двері`** + **`2 шишетчасті сірі полиці`** — UA-side первая li использует Lat `p` `pаспашні` (artifact для UA тоже, **новый паттерн** vs blknochg pure SKUs где UA cell остаётся untouched); LIVE preserve в blknochg_soft (POL4 НЕ trogает UA `pаспашні` artifact, только `Хладогент`); (3) RU `+2&deg;С до +12&deg;С` Cyr С `&deg;` entity vs UA `+2 °C до +12 °C` U+00B0 + space + Lat C — same SKU 27 asymmetric degree-glyph pattern; **POL2 НЕ trigger** (U+00B0 ≠ U+02DA); (4) `Абсорбционный` тип разморозки + `Хладагент: NH3` (после POL4 fix) — Tefcold TM42 использует **абсорбционное охлаждение** с NH3 аммиаком (same NH3 как SKU 17/19 b3 TM52/TM32G но другой охлаждающий принцип — абсорбционный vs компрессионный); (5) `Потребляемая энергия: 0.8 квт/24ч` real decimal preserve (POL `NN.00→NN` НЕ trigger — `0.8` уже singular digit); (6) inner-dim `316 x 245 x 459 мм` + main-dim `402 x 450 x 560 мм` — **уже Lat x** supplier-provided обе локали (Tefcold TM42 same Lat-x supplier-side pattern как SKU 26/27 BC-серия); (7) trailing `<p> </p>` artifact LIVE preserve. **ТРИНАДЦАТЫЙ Tefcold blknochg в проекте** (первый Tefcold blknochg_soft — до b4 все Tefcold в blknochg pure family). Tefcold TM42 BLACK — мини-холодильник 36/34 л 1 распашная глухая дверь чёрный корпус абсорбционное охлаждение NH3 (similar TM-серия sister TM44G SKU 29). **POL4 explicit fix-ы применены к SKU 28**: (1) RU `Хладогент: NH3` → `Хладагент: NH3` letter-swap `о`→`а`; (2) UA `Хладогент: NH3` → `Хладагент: NH3` mirror RU POL4 letter-swap (POL4 BOTH locales rule — UA + RU модифицируем когда typo в обеих локалях; UA-cell modification counter b4 += 1). **POL1 НЕ trigger** (blknochg_soft category, не blk триплет; POL1 scope = blk триплет only). **POL2 НЕ trigger** (U+00B0 distinct от U+02DA). **POL5 unchanged** (forward+retro deferred). META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=1153797472)*

---

## SKU 29/79 — Минибар холодильный TEFCOLD TM44G (Артикул 1153821370) — SOFT-fix `Хладогент`→`Хладагент` POL4 RU-only

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** `<li>Хладогент: NH3</li>`
**Стало:** `<li>Хладагент: NH3</li>`

*(blknochg_soft — `desc UA==RU` **False** (genuine отдельный RU перевод 1018/1029 байт); `nm_ua`!=`nm_ru` (UA `Мінібар холодильна шафа TEFCOLD TM44G` 2-word vs RU `Минибар холодильный TEFCOLD TM44G` 1-word — asymmetric translation как SKU 26 UR200S supplier-side variability); `nm_ru`==`nazv_ru` clean. **Tefcold НЕ ∈ НП-эксклюзив**. LIVE-магазин Horoshop, body genuine с POL4 typo fix RU-only. **POL4 ТРЕТЬЕ применение в проекте** (после SKU 10 b2 Hata + SKU 28 b4 Tefcold TM42 obе локали → SKU 29 b4 Tefcold TM44G **RU-only** asymmetric). **Asymmetric POL4 в SKU 29**: UA supplier dr использует **корректное** `<li>Хладагент: NH3</li>` (uppercase Capitalize-first, semantic-correct word `Хладагент`); RU supplier dr использует **typo** `<li>Хладогент: NH3</li>` (letter-swap `-о-` middle stem) — UA-side supplier translated correctly, RU-side supplier дал typo; **POL4 fix только RU** `Хладогент: NH3` → `Хладагент: NH3` letter-swap `о`→`а`; UA cell **НЕ модифицируется** (UA уже correct — нет typo чтобы fix-ить). Это **демонстрирует POL4 asymmetric scope**: POL4 BOTH locales **WHEN typo present BOTH locales** (mirror SKU 10 b2 + SKU 28 b4); POL4 ONLY-RU **WHEN typo only RU** (asymmetric — UA correct, не модифицируем); rule = fix where typo exists, preserve where correct. Precedent **chunk-029 b4 SKU 29** = ПЕРВОЕ asymmetric POL4 application в проекте (SKU 10 + 28 были symmetric обе локали). LIVE source artefacts preserve verbatim: (1) supplier RU dr `<p>Мини-холодильник TEFCOLD TM44G отлично подойдет для размещения на небольшой площади. Используется для хранения продуктов.</p>` opening (mirror SKU 27/28); (2) **SKU 29 LIVE artefact** `<li>2 pешетчатые серые полки</li>` — **Lat `p`** store-canonical (mirror SKU 28 b4 RU второй li Lat-p artifact; UA `2 сірі полиці-решітки` correct без Lat-p — UA-side supplier translated correctly как SKU 29 `Хладагент`; **asymmetric supplier translation** UA correct vs RU typos/glyph-artifacts — pattern SKU 29-specific); (3) RU `+5&deg;С до +12&deg;С` Cyr С `&deg;` entity vs UA `+5&deg;С до +12&deg;С` Cyr С `&deg;` entity — **симметрично** обе локали (vs SKU 27/28 asymmetric degree-glyph); supplier translated UA правильно с Cyr `&deg;С` (как RU) — distinct от SKU 27/28 UA U+00B0 + Lat C; SKU 29-specific supplier UA-side используют RU-style entity convention; (4) **`Регулируемые полки`** correctly translated UA `Регульовані полиці` (mirror; UA correct); (5) `Перенавешиваемая стеклянная дверь` correctly translated UA `Скляні двері, що перенавішуються`; (6) **`Бесшумная работа`** + **`Низкое энергопотребление`** + **`Светодиодная внутренняя подсветка`** дополнительные li (SKU 29 имеет more detailed metadata vs SKU 28 — TM44G premium-feature vs TM42 base; supplier-side feature-list variability внутри TM-серии); (7) UA-side `Об&#39;єм` `&#39;` entity apostrophe (как другие SKUs vs SKU 19 b3 `&rsquo;` U+2019 — supplier varying entity choice внутри Tefcold family); (8) inner-dim `312 x 250 x 455 мм` + main-dim `402 x 457 x 560 мм` — **уже Lat x** supplier-provided обе локали (consistent Tefcold supplier Lat-x pattern); (9) `Потребляемая энергия: 0.8 квт/24ч` real decimal preserve (same SKU 28); (10) trailing `<p> </p>` artifact LIVE preserve. **ЧЕТЫРНАДЦАТЫЙ Tefcold blknochg в проекте** (второй Tefcold blknochg_soft после SKU 28). Tefcold TM44G — мини-холодильник 36/35 л перенавешиваемая стеклянная дверь чёрный корпус NH3 аммиак абсорбционное охлаждение (sister-model SKU 28 TM42 но glass-door + premium feature-list). **POL4 explicit fix к SKU 29 (RU-only asymmetric)**: RU `Хладогент: NH3` → `Хладагент: NH3` letter-swap `о`→`а`; UA cell **untouched** (UA `Хладагент: NH3` correct — POL4 не модифицирует correct cell). **POL1 НЕ trigger** (blknochg_soft category, не blk триплет). **POL2 НЕ trigger** (`&deg;С` entity обе локали — нет U+02DA). **POL5 unchanged**. UA-cell modification counter b4 += 0 (SKU 29 asymmetric RU-only). META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=1153821370)*

---

## SKU 30/79 — Минибар холодильный TEFCOLD BC30 (Артикул 1153845669) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg pure — `desc UA==RU` **False** (genuine отдельный RU перевод 1230/1216 байт); `nm_ua`!=`nm_ru` (UA `Мінібар холодильний TEFCOLD BC30` vs RU `Минибар холодильный TEFCOLD BC30`); `nm_ru`==`nazv_ru` clean. **Tefcold НЕ ∈ НП-эксклюзив**. LIVE-магазин Horoshop, genuine RU body НЕ переписываем. LIVE source artefacts preserve verbatim: (1) supplier RU dr `<p>Мини-холодильник TEFCOLD BC30 отлично подойдет для размещения на небольшой площади. Используется для хранения напитков и продуктов.</p>` opening `<p>` (mirror SKU 27-29; **note `напитков и продуктов`** dual scope vs SKU 27 BC85 `продуктов` only — BC-серия для bottles/cans + food); (2) **SKU 30 LIVE artefact** `<li>Количество и тип полок: 2 pешетчатые черные полки. Размер полок: 275 x 205 мм</li>` — **Lat `p` U+0070** store-canonical в `pешетчатые` (continuation Tefcold Lat-`p` pattern SKU 7/26/27/28/29 — **шестой Lat-`p` в Tefcold семействе chunk-029**); inner-dim `275 x 205` уже **Lat x** supplier-provided; (3) `Стеклянная дверь` + `Самозакрывающаяся дверь` correctly translated UA `Скляні двері, які самі зачиняються` (UA supplier-side `двері` plural noun → RU singular `дверь` для 1-дверного minibar BC30 — same UA grammar inconsistency pattern SKU 23 Hendi + SKU 27 BC85; mirror translation semantically correct); (4) `Высокопрочное стекло` correctly translated UA `Високоміцне скло`; (5) **`Температурный диапазон: От +2 до +10 &deg;C`** — RU использует `От` (Capitalize) + Lat C + `&deg;` entity без space; UA `Температурний діапазон: Від 2 до 10 &deg;C` — note **UA missing `+` signs** перед числами (`Від 2 до 10` vs RU `От +2 до +10`) — supplier UA-side artifact LIVE preserve обе локали (asymmetric supplier translation; не POL trigger); (6) `Хладагент: R600a` correctly translated UA `Хладагент: R600a` (lowercase `a` consistent) — **POL4 НЕ trigger** (нет `хладогент` letter-swap typo в SKU 30 — supplier translated correctly обе локали; **distinguishes от SKU 28/29** где POL4 trigger из-за `Хладогент: NH3` typo); (7) `Уровень шума: 44 дб(А)` — UA `Уровень шума: 44 дб(А)` **RU calque в UA cell** — supplier UA-side **скопировал RU `Уровень шума`** (correct UA было бы `Рівень шуму`) — supplier UA-typo letter-level (но не в POL4 closed-set list — UA `Уровень шума` calque candidate для POL5 retroactive expansion sweep post-W1-STOP; LIVE preserve в b4); (8) `Внутренняя отделка: Крашеный алюминий, черный` correctly translated UA `Внутрішнє оздоблення: Фарбований алюміній, чорний` (mirror); (9) `Тип контроллера: Механический` correctly translated UA `Тип контролера: Механічний` (mirror); (10) inner-dim `280 x 271 x 380 мм` + main-dim `356 x 406 x 491 мм` — **уже Lat x** supplier-provided обе локали (consistent Tefcold pattern); (11) trailing `<p> </p>` artifact LIVE preserve. **ПЯТНАДЦАТЫЙ Tefcold blknochg в проекте** (третий Tefcold blknochg в b4 после SKU 25 + 26 + 27 — pure → pure → pure → soft → soft → pure → pure → pure pattern b4). Tefcold BC30 — мини-холодильник 22/20 л для bottles/cans (20×330мл + 20×500мл) распашная стеклянная дверь самозакрывающаяся чёрный корпус R600a механический контроллер. **Никаких POL1/POL2/POL4 fix-ов в SKU 30 НЕ требуется** — RU+UA bodies clean (нет `хладогент` typo — supplier translated correctly обе локали; нет U+02DA); LIVE preserve UA `Уровень шума` RU-calque artifact (POL4 closed-set list НЕ включает; POL5 retroactive candidate); LIVE preserve UA missing `+` signs `Від 2 до 10` (supplier choice, не typo). META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=1153845669)*

---

## SKU 31/79 — Минибар холодильный TEFCOLD BC60 (Артикул 1153849857) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg pure — `desc UA==RU` **False** (genuine отдельный RU перевод 1232/1212 байт); `nm_ua`!=`nm_ru` (UA `Мінібар холодильний TEFCOLD BC60` vs RU `Минибар холодильный TEFCOLD BC60`); `nm_ru`==`nazv_ru` clean. **Tefcold НЕ ∈ НП-эксклюзив**. LIVE-магазин Horoshop, genuine RU body НЕ переписываем. LIVE source artefacts preserve verbatim: (1) supplier RU dr `<p>Мини-холодильник TEFCOLD BC60 отлично подойдет для размещения на небольшой площади. Используется для хранения напитков и продуктов.</p>` opening `<p>` (mirror SKU 30 BC30 same BC-серия opening — sister-model larger 67/58 л variant); (2) **SKU 31 двойной Lat-`p` LIVE artefact** — RU `<li>Количество и тип дверей: 1 pаспашная стеклянная самозакрывающаяся дверь с подогревом</li>` + `<li>2 pешетчатые черные полки размером 340x270 мм</li>` — **двойной Lat `p` U+0070** store-canonical (`1 pаспашная` + `2 pешетчатые` — **седьмой и восьмой Lat-`p` в Tefcold семействе chunk-029**); inner-dim `340x270` уже **Lat x** supplier-provided **без пробелов** (vs SKU 30 `275 x 205` со-space — varying supplier convention); (3) **`Количество и тип дверей: 1 pаспашная стеклянная самозакрывающаяся дверь с подогревом`** — **SKU 31-specific feature** `с подогревом` (vs SKU 30 BC30 без подогрева — BC60 premium-variant) + `подогревом` doors-heating для anti-condensation на стекле в влажной среде; UA mirror `1 розпашна скляна дверь з підігрівом` correctly translated; (4) `Стеклянная дверь, которая сама закрывается` correctly translated UA `Скляні двері, що самі зачиняються` (UA supplier-side `двері` plural noun → RU singular `дверь` для 1-дверного — UA grammar inconsistency continuation pattern); (5) `Высокопрочное стекло` correctly translated UA `Високоміцне скло`; (6) `Температурный диапазон: от +2 до +10 &deg;C` — RU lowercase `от` (SKU 31-specific lowercase vs SKU 30 Capitalize `От`; varying supplier convention within Tefcold BC-серия) + Lat C + `&deg;` entity без space; UA `Температурний діапазон: від +2 до +10 &deg;C` lowercase `від` symmetric (SKU 31 supplier UA-side **есть `+` signs** unlike SKU 30 UA `Від 2 до 10` без `+` — supplier UA-side variability within BC-серия LIVE preserve); (7) `Хладагент: R600a` correctly translated UA `Хладагент: R600a` — **POL4 НЕ trigger** (нет typo; consistent с SKU 30 BC30 supplier-RU-cleanness pattern; **distinguishes от SKU 28/29 TM-серия** где `Хладогент` typo trigger); (8) `Уровень шума: 44 дб(А)` — UA `Уровень шума: 44 дб(А)` **RU calque** continuation SKU 30 pattern (UA correct было бы `Рівень шуму`; supplier-side calque artifact LIVE preserve в b4; POL5 retroactive candidate); (9) `Внутренняя отделка: Крашеный алюминий, черный` correctly translated UA `Внутрішнє оздоблення: Фарбований алюміній, чорний` (mirror SKU 30); (10) inner-dim `356 x 311 x 557 мм` + main-dim `432 x 496 x 668 мм` — **уже Lat x** supplier-provided обе локали (BC60 larger variant SKU 30 sister-model — 67/58 л vs 22/20 л; same supplier-side Lat-x convention); (11) `4 регулируемые ножки` correctly translated UA `4 регульовані ніжки`; (12) trailing `<p> </p>` artifact LIVE preserve. **ШЕСТНАДЦАТЫЙ Tefcold blknochg в проекте** (четвёртый Tefcold blknochg в b4: SKU 25/26/27/30/31 = pure; SKU 28/29 = soft; SKU 32 ниже = pure). Tefcold BC60 — мини-холодильник 67/58 л для bottles/cans (70×330мл + 55×500мл) распашная стеклянная самозакрывающаяся дверь с подогревом чёрный корпус R600a 2 решетчатые полки. **Никаких POL1/POL2/POL4 fix-ов в SKU 31 НЕ требуется** — RU+UA bodies clean (нет `хладогент` typo; нет U+02DA); LIVE preserve UA `Уровень шума` calque artifact (POL5 candidate post-W1-STOP). META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=1153849857)*

---

## SKU 32/79 — Морозильный шкаф Tefcold FS80CP/SUB ZE (Артикул 2053000938) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg pure — `desc UA==RU` **False** (genuine отдельный RU перевод 754/767 байт); `nm_ua`!=`nm_ru` (UA `Морозильна шафа Tefcold FS80CP/SUB ZE` vs RU `Морозильный шкаф Tefcold FS80CP/SUB ZE`; **note mixed-case `Tefcold`** vs uppercase `TEFCOLD` в SKU 25-31 — supplier-side capitalization variability внутри Tefcold family для FS-серии SKU 32 vs UF/UR/BC/TM серий SKU 25-31); `nm_ru`==`nazv_ru` clean. **Tefcold НЕ ∈ НП-эксклюзив**. LIVE-магазин Horoshop, genuine RU body НЕ переписываем. LIVE source artefacts preserve verbatim: (1) supplier RU dr `<p>Шкаф морозильный настольный FS80CP/SUB ZE Tefcold предназначен для кратковременного хранения, экспозиционирования и продаж напитков на барах ресторанов, кафе.</p>` opening `<p>` (mirror Tefcold supplier `<p>` pattern continuation; **SKU 32-specific narrative** дает context `на барах ресторанов, кафе` venue-detail unlike mini-bar SKU 25-31 home/bar context; supplier-side venue-specific marketing); (2) **SKU 32 supplier RU dr `Вмещает 60 банков 0.33мл и 48 банков 0.5мл или 40 бутылок 0.33мл и 40 бутылок ПЭТ 0.5мл.`** — **множественные supplier-side artefacts**: (a) **`банков`** plural-gen (RU correct grammar для счёта банок 60 шт = `60 банок` или `60 банков` — оба валидно; supplier выбрал `банков` LIVE preserve, UA mirror `60 банків` correct); (b) **`0.33мл`/`0.5мл`** — **unit typo** supplier-side: должно быть `0.33 л` / `0.5 л` (литры жидкости в банках; `мл` миллилитры — гипо-в-1000-раз неправильно для bottles/cans 330ml = 0.33 л NOT 0.33мл = 0.00033 л gross typo); LIVE preserve обе локали (supplier-side glyph-typo `л`→`мл` — closed-form typo NOT в POL4 list (`хладогент`/`автоотайка`/`подстветки`/`двецею`); POL5 retroactive expansion candidate post-W1-STOP — supplier unit-typo `мл` → `л` для cans/bottles); (c) **`банков 0.33мл`** vs **`пляшок 0.33мл`** UA-side — UA `банків` (plural-gen `банка` для can) + `пляшок` (plural-gen `пляшка` for bottle) **обе UA correct**; RU `банков`/`бутылок` обе RU correct (supplier UA-side semantic-correct `пляшок` bottles + `банків` cans; RU `банков` + `бутылок` mirror); **note RU `банков`** more natural в RU = `банок` (acc-pl) — но `банков` тоже валидно (gen-pl для inclusive count); supplier-side LIVE preserve обе локали; (3) supplier RU dr `<p><strong>Технические характеристики:</strong></p>` separator vs SKU 25-31 `<p>Технические характеристики:</p>` no-`<strong>` — **SKU 32-specific bold wrapping** for header (varying supplier convention within Tefcold family; UA mirror тоже с `<strong>` for symmetry); (4) `<li>Дверь Прозрачная</li>` + `<li>Открытие дверей Распашные</li>` — **SKU 32-specific noun-adjective inversion** `Дверь Прозрачная` vs SKU 27 BC85 `Распашная стеклянная дверь` — supplier-side metadata-list flat format (noun-attribute pairs) vs sentence-style descriptions; FS80CP supplier дал tabular-style metadata; (5) `<li>Температурный режим -8.. 0 &deg;C</li>` — **двойные точки `..`** (NOT тройные `...`) + Lat C + space-before-`&deg;` UA-side; SKU 32 specific double-dot artifact (precedent SKU 19 b3 TM32G UA `+5 .. +12` тоже двойные точки — Tefcold supplier UA-side artifact pattern; SKU 32 supplier same pattern BOTH UA + RU symmetric LIVE preserve); RU `-8.. 0 &deg;C` same двойные точки + space + Lat C; (6) **`Хладагент R600A`** uppercase `A` (vs SKU 30/31 BC30/BC60 `R600a` lowercase) — supplier-side capitalization variability within Tefcold R600 series LIVE preserve обе локали; (7) `<li>Тип охлаждения Динамическое</li>` neut-singular adjective inversion (vs SKU 28/29 `Тип охлаждения: динамический` masc-singular + colon — supplier-side format inconsistency within Tefcold family; FS80CP supplier дал no-colon flat-attribute style); (8) `<li>Электрическая мощность, Вт 85</li>` + `<li>Электрическое питание 220-230V</li>` + `<li>Длина, мм 480</li>` + similar `Глубина/Высота/Вес, мм/кг N` — **SKU 32 supplier dr no-colon flat-attribute style** all li (vs SKU 25-31 colon `: NN`); supplier-side format consistency within FS80CP metadata-list LIVE preserve; (9) **mod_name asymmetric translation**: UA `Морозильна шафа` 2-word vs RU `Морозильный шкаф` 2-word — обе локали 2-word symmetric (vs SKU 26/29 UR200S/TM44G UA `шафа` 2-word vs RU `шкаф` 1-word asymmetric); (10) `<li>Холодоагент R600A</li>` UA-side `Холодоагент` proper Ukrainian word (RU mirror `Хладагент R600A` — correct translation; **POL4 НЕ trigger** because нет `хладогент`/`Хладогент` letter-swap typo; supplier translated correctly обе локали; precedent SKU 30/31 same `Хладагент R600a` correct pattern). **СЕМНАДЦАТЫЙ Tefcold blknochg в проекте** (пятый Tefcold blknochg в b4 после SKU 25/26/27/30/31 pure + SKU 28/29 soft = 7 Tefcold blknochg в b4 одним батчем). Tefcold FS80CP/SUB ZE — морозильный настольный шкаф 55 л барный для напитков (60×0.33 + 48×0.5 банок ИЛИ 40×0.33 + 40×0.5 ПЭТ бутылок) распашная прозрачная дверь R600A температурный режим -8..0 &deg;C для bottles/cans display-cooling в барах ресторанов. **Никаких POL1/POL2/POL4 fix-ов в SKU 32 НЕ требуется** — RU+UA bodies clean (нет `хладогент` typo — supplier RU `Хладагент` correct + supplier UA `Холодоагент` correct; нет U+02DA); LIVE preserve supplier-side artefacts: `0.33мл`/`0.5мл` unit-typo (POL5 candidate `мл`→`л` for cans/bottles); `банков` plural-gen choice; `Дверь Прозрачная`/`Тип охлаждения Динамическое` noun-attribute inversion supplier-format; double-dots `-8.. 0`; `R600A` uppercase A; mixed-case `Tefcold` SKU 32-specific; **`<strong>` bold separator** SKU 32-specific. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=2053000938)*

**Наблюдения по батчу SKU 25-32 (32/79) — chunk-029 (ЧЕТВЁРТЫЙ батч chunk-029 в разделе `Шафи настільні для бару, міні-бари (фрігобари)`; **ВТОРОЙ POL applications batch** в проекте после b2 (b3 был ЧИСТЫЙ POL non-trigger batch)):** **blk триплет 0** (нет UA-leak nm + UA==RU в b4 — все 8 SKU имеют distinct nm_ua/nm_ru clean translation + genuine RU body отдельный от UA; **первый POL-trigger batch без blk триплета** — POL applications в blknochg_soft category SKU 28/29, не blk триплет). **blkv 0; blknotrip 0; blknochgeq 0; SKIP-НП 0** (нет НП-эксклюзив брендов в b4 — все 8 SKU Tefcold, **НЕ ∈ NP-SET**; Hurakan ×5 завершено в b1+b2 chunk-029 SKU 2/8/13/14/15; кумул. SKIP-НП chunk-029 = 5 unchanged). **blknochg pure 6** (SKU 25 UF200 + SKU 26 UR200S + SKU 27 BC85 + SKU 30 BC30 + SKU 31 BC60 + SKU 32 FS80CP/SUB ZE — **десятый/одиннадцатый/двенадцатый/пятнадцатый/шестнадцатый/семнадцатый Tefcold blknochg в проекте**). **blknochg_soft 2** (SKU 28 TM42 BLACK + SKU 29 TM44G — **тринадцатый/четырнадцатый Tefcold blknochg**; **ВТОРОЕ+ТРЕТЬЕ применение POL4** в проекте после b2 SKU 10 Hata; **SKU 28 = POL4 symmetric обе локали** `Хладогент: NH3`→`Хладагент: NH3` letter-swap `о`→`а` UA + RU mirror; **SKU 29 = POL4 asymmetric RU-only** `Хладогент: NH3`→`Хладагент: NH3` (UA correct `Хладагент` — НЕ модифицируем; ПЕРВОЕ asymmetric POL4 application в проекте — demonstrates POL4 scope = fix where typo exists obob locales; preserve where correct). Классификация: blk триплет 0 + blkv 0 + blknotrip 0 + blknochgeq 0 + blknochg pure 6 + blknochg_soft 2 + SKIP-НП 0 = 8 ✓. **5 политик 2026-05-20 в b4 — POL applications + POL non-trigger validations:** **POL1** (UA-typo fix blk обе локали) **НЕ trigger** в b4 (blk триплет 0; POL1 scope = blk триплет only; **UA cells в blknochg_soft SKU 28 модифицируются через POL4 не POL1** — POL4 scope = blknochg LIVE SOFT typos обе локали). **POL2** (U+02DA→`&deg;`) **НЕ trigger** в b4 (нет U+02DA Polish ring above в любом SKU 25-32 UA/RU; источник использует `&deg;` HTML entity (SKU 25/26/29/30/31 обе локали) или **U+00B0 ° DEGREE SIGN** (SKU 27 UA `+2 °C` + SKU 28 UA `+2 °C`) **distinct codepoint** от U+02DA — LIVE preserve; precedent b3 validates U+00B0 ≠ U+02DA). **POL3** (SKIP-НП strict by brand) N/A для batch (нет НП-эксклюзив брендов в b4 — все 8 Tefcold). **POL4** (blknochg LIVE SOFT-typos) **ВТОРОЕ+ТРЕТЬЕ применение** — SKU 28 symmetric `Хладогент: NH3`→`Хладагент: NH3` обе локали; SKU 29 asymmetric RU-only `Хладогент: NH3`→`Хладагент: NH3` (UA correct preserve). POL4 scope demonstrated: fix where typo exists, preserve where correct — symmetric vs asymmetric application driven by typo-presence per locale (mirror SKU 10 b2 Hata symmetric; SKU 29 b4 first asymmetric demo). **POL4 НЕ trigger для другие UA artefacts**: SKU 27 UA `корисливий` (typo `корисний`) + SKU 28 UA `корисливий` + `шишетчасті` (typos `корисний`/`гратчасті`/`решітчасті`) + SKU 30/31 UA `Уровень шума` (RU calque `Рівень шуму` correct) — все **closed-set list НЕ включает** (`хладогент`/`автоотайка`/`подстветки`/`двецею`); POL5 retroactive expansion candidates post-W1-STOP. **POL5** unchanged (forward+retro deferred). **UA-cells modified counter b4 = 1** (SKU 28 UA `Хладогент: NH3`→`Хладагент: NH3` POL4 symmetric); кумул. UA-cells modified chunk-029 = **4 SKU** (10 b2 + 11 b2 + 12 b2 + 28 b4); кумул. UA-cells modified в проекте = **4 SKU** (b4 добавляет 1 SKU 28). **Tefcold ×17 в проекте** (b4 = 8-й/9-й/10-й/11-й/12-й/13-й/14-й/15-й/16-й/17-й — pardon: SKU 4/5/7 b1 + SKU 9 b2 + SKU 17/18/19 b3 + SKU 25/26/27/28/29/30/31/32 b4 = 4+1+3+8 = 16; correcting count: **семнадцатый Tefcold blknochg в проекте**: 0 chunk-029 b1 = 3 (SKU 4/5/7) + chunk-029 b2 = 1 (SKU 9) + chunk-029 b3 = 3 (SKU 17/18/19) + chunk-029 b4 = 8 (SKU 25-32 все 8 Tefcold) = 15 Tefcold в chunk-029; project-wide Tefcold blknochg count добавляются pre-chunk-029 chunks 016-028 Tefcold occurrences — счёт project-wide точно неизвестен в этой контексте; локальный chunk-029 счёт = 15 Tefcold blknochg в chunk-029 после b4). Открытых вопросов по батчу 0 (ledger chunk-029 остаётся 0; questions.md НЕ создаём). Кумул. SKIP-НП chunk-029 = 5 (b1 2 + b2 3 — unchanged в b3+b4, Hurakan ×5 закрыт). Кумул. UA-cells modified в проекте = 4 SKU (10/11/12 b2 + 28 b4). META always faithful (UA!=RU genuine — артефакты источника preserve 1:1: SKU 27 UA `корисливий` + SKU 28 UA `корисливий`/`шишетчасті` + SKU 30/31 UA `Уровень шума` calque + SKU 32 `0.33мл`/`банков` artefacts preserve). chunk-029 = 32/79. NEXT: chunk-029 b5 SKU 33-40.

*(scoped к row Артикул=2053000938)*

---


## SKU 33/79 — Минибар Tefcold TM32 BLACK (Артикул 2053486039) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg pure — `desc UA==RU` **False** (genuine отдельный RU перевод; UA `Міні-бар` 2-word vs RU `Мини-бар` 2-word symmetric narrative); `nm_ua`!=`nm_ru` (UA `Мінібар Tefcold TM32 BLACK` 1-word vs RU `Минибар Tefcold TM32 BLACK` 1-word symmetric — note mixed-case `Tefcold` vs uppercase `TEFCOLD` SKU 25-31 b4 mirror SKU 32 b4 FS80CP — supplier-side capitalization variability within Tefcold family; TM32 supplier выбрал mixed-case как FS-серия, vs TM42/TM44G b4 uppercase — varies even within TM-серия); `nm_ru`==`nazv_ru` clean. **Tefcold НЕ ∈ НП-эксклюзив**. LIVE-магазин Horoshop, genuine RU body НЕ переписываем. **ВОСЕМНАДЦАТЫЙ Tefcold blknochg в проекте** (после 17 в chunk-029 b1+b2+b3+b4 = SKU 4/5/7/9/17/18/19/25/26/27/28/29/30/31/32 = 15 в chunk-029; SKU 33 = ПЕРВЫЙ Tefcold blknochg в b5 после самого плотного 8-SKU Tefcold batch b4). LIVE source artefacts preserve verbatim: (1) supplier RU dr `<p>Мини-бар имеет изящный дизайн &ndash; снаружи он черного цвета, а внутри цвета антрацита, что придает ему ощущение премиум-класса.</p>` opening narrative `&ndash;` U+2013 HTML entity en-dash + premium-marketing language SKU 33-specific (vs SKU 25-32 b4 base technical opening) — TM32 BLACK premium-finish premium-marketing supplier convention; (2) supplier UA dr mirror `&#39;` HTML entity apostrophe `інтер&#39;єру` (vs SKU 19 b3 `&rsquo;` U+2019 — supplier varying entity choice within Tefcold family LIVE preserve); (3) **SKU 33 LIVE artefact**: RU `<li>Количество и тип дверей 1 pаспашная глухая дверь</li>` — **Lat `p` U+0070** в `pаспашная` store-canonical (continuation Tefcold Lat-`p` pattern SKU 7 b1 + SKU 26-31 b4; **девятый Lat-`p` в Tefcold семействе chunk-029**); (4) **SKU 33 второй Lat-`p`**: RU `<li>Количество и тип полок 1 pешетчатые серые полки</li>` — **Lat `p` U+0070** в `pешетчатые` (**десятый Lat-`p` в Tefcold семействе chunk-029** — двойной Lat-p обе строки RU mirror SKU 28/31 b4 двойной Lat-p); (5) **`<li>Хладагент NH3</li>`** correctly translated supplier-side BOTH locales (RU `Хладагент NH3` + UA `Хладагент NH3` — note UA-side `Хладагент` NOT `Холодоагент` mirror SKU 32 b4 UA `Холодоагент` — supplier UA-side variability within Tefcold family; SKU 33 UA `Хладагент` correct calque or partial-translate — **POL4 НЕ trigger** (нет letter-swap `Хладогент` typo в SKU 33; supplier translated correctly обе локали; distinguishes от SKU 28/29 b4 TM-серия где POL4 trigger — TM32 BLACK supplier-cleanness pattern matches BC-серия SKU 30/31 b4 не TM42/TM44G b4); (6) `<li>Тип охлаждения Абсорбционный</li>` + `<li>Тип разморозки Автоматический</li>` no-colon flat-attribute supplier-format SKU 33-specific (matches SKU 32 b4 FS80CP/SUB ZE no-colon convention; varying within Tefcold family — TM/FS series no-colon vs UF/UR/BC colon convention SKU 25-31 b4); (7) `<li>Уровень шума 0 дб(А)</li>` — RU `Уровень шума` correctly translated + UA mirror **`Рівень шуму 0 дб(А)`** correctly translated UA-side (vs SKU 30/31 b4 UA `Уровень шума` RU-calque semantic-translate-skip — SKU 33 UA-side supplier translated **correctly** `Рівень шуму`; distinguishes — supplier UA-side variability within Tefcold BC vs TM serial); (8) `<li>Хладагент NH3</li>` без `R717` prefix (vs SKU 28 b4 TM42 BLACK label `R717 NH3` — supplier-side variant choice; TM32 BLACK supplier dropped `R717` prefix LIVE preserve); (9) inner-dim `<li>Внутренний размер (ШxГxВ) 312 x 225 x 395 мм</li>` + main-dim `<li>Габаритный размер (Ш x Г x В) 402 x 438 x 500 мм</li>` + package-dim `<li>Размер в упаковке (ШxГxВ) 450 x 460 x 530 мм</li>` — **уже Lat x** supplier-provided обе локали (mirror SKU 28-31 b4 supplier-side Lat-x convention); SKU 33 has 3 dim lines (vs SKU 28-31 b4 fewer dim lines — TM-серия metadata variability); (10) `<li>Перенавешиваемая дверь Да</li>` flat-attribute + UA mirror `<li>Двері, що перенавішують Так</li>` correctly translated relative-clause (UA `що перенавішують` = relative-clause active-voice vs RU passive `Перенавешиваемая` — UA supplier translated structurally); (11) `<li>Кол-во на 40-футовый контейнер 384 шт</li>` RU abbreviation `Кол-во` (vs UA `Кількість на 40-футовий контейнер 384 шт` full word — supplier asymmetric abbreviation); (12) `0.62 квт/24ч` lowercase `квт` Wt-letter-case typo (correct unit `кВт`) supplier-side artefact обе локали LIVE preserve (POL5 candidate post-W1-STOP — letter-case unit typo; new POL5 artefact category in b5); (13) UA-side `Уровень шуму` typo? — actually UA `Рівень шуму 0 дб(А)` correct UA noun-genitive — clean. Tefcold TM32 BLACK — мини-бар 29/27 л абсорбционное **NH3 аммиак** 1 распашная глухая дверь черный корпус АБС RAL7005 4 регулируемые ножки LED-подсветка внутри. **Никаких POL1/POL2/POL4 fix-ов в SKU 33 НЕ требуется** — RU+UA bodies clean (нет U+02DA; нет POL4 closed-set typos; UA `Хладагент` supplier-side correct); LIVE preserve supplier-side artefacts: двойной Lat-`p` + `0.62 квт` letter-case unit typo + mixed-case `Tefcold` + premium-narrative opening `&ndash;` entity + `Хладагент NH3` сводный без `R717` prefix + UA `Рівень шуму` correctly translated (varies от SKU 30/31 b4 UA RU-calque). META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=2053486039)*

---

## SKU 34/79 — Барный холодильный шкаф Forcar BC1PB (Артикул 661388070) — RU SOFT-fix POL2 U+02DA RU-only asymmetric

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU) — SOFT-fix POL2 (2026-05-20: U+02DA→&deg; — ПЕРВОЕ asymmetric POL2 RU-only в проекте)
**Было:** `+2&hellip;+8˚С`
**Стало:** `+2&hellip;+8&deg;С`

*(blknochg_soft — `desc UA==RU` **False** (genuine отдельный RU перевод 1116/1041 байт; UA-side supplier translated separately U+00B0 ° + Lat C vs RU U+02DA `˚` + Cyr С — asymmetric supplier degree-glyph choice внутри SKU 34 single SKU); `nm_ua`!=`nm_ru` (UA `Барна холодильна шафа Forcar BC1PB` vs RU `Барный холодильный шкаф Forcar BC1PB`); `nm_ru`==`nazv_ru` clean RU. **ПЕРВЫЙ Forcar в проекте** — Forcar НЕ ∈ НП-эксклюзивный список (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. Forcar — итальянский производитель холодильного коммерческого оборудования. **ЧЕТВЁРТОЕ применение POL2 в проекте — ПЕРВОЕ asymmetric POL2 в проекте (RU-only)**. Mirror precedent **chunk-029 b4 SKU 29 POL4 ПЕРВОЕ asymmetric demo** (RU-only typo, UA correct preserve): SKU 34 b5 = same scope rule, но для POL2 — fix where U+02DA present per locale; preserve where correct codepoint (U+00B0 ≠ U+02DA). RU body содержит **`+2&hellip;+8˚С`** где `˚` = **U+02DA Polish ring above** → fix к `&deg;С` HTML entity (semantic-correct degree sign), Cyr С U+0421 preserve; UA body **`+2...+8 °C`** = **U+00B0 ° DEGREE SIGN + space + Lat C** — distinct codepoint preserve (precedent b3 SKU 23/24 Hendi + b4 SKU 27/28 — U+00B0 LIVE preserve когда distinct from U+02DA; **POL2 не модифицирует U+00B0**). LIVE source artefacts preserve verbatim: (1) RU body opening `<p>Барный холодильный шкаф используется в барах, ресторанах, кафе для хранения и демонстрации напитков в бутылках или жестяных банках по 0,33 л. Может встраиваться в барную стойку. </p>` decimal-comma `0,33 л` correctly translated + trailing space перед `</p>` artifact (varies от SKU 32 b4 unit-typo `0.33мл` gross 1000× scale — SKU 34 supplier translated correctly `0,33 л` decimal-comma + `л` unit; sanity-check distinguishes Forcar supplier-translate quality от FS80CP supplier-typo); (2) UA mirror opening `0,33 л` correctly translated `у пляшках або бляшанках по 0,33 л` — supplier UA-side faithful; (3) RU `+33&deg;C` U+00B0 → wait, source RU contains `+33&deg;C` HTML entity + Lat C within environmental temp spec; UA mirror `+33 °C` U+00B0 + space + Lat C — **asymmetric supplier-side**: RU `&deg;` entity vs UA U+00B0 standard codepoint within same SKU LIVE preserve обе локали для environmental temp (vs main temperature range RU U+02DA vs UA U+00B0 — supplier varied degree-glyph encoding per phrase even within single SKU); (4) UA `2 ґратчасті полиці розміром 520х315 мм` Cyr х U+0445 + supplier inner-dim Cyr х (NOT Policy B/C for blknochg category — blknochg preserves supplier-canonical inner-dim verbatim); RU mirror `2 решетчатые полки размером 520х315 мм` Cyr х symmetric; (5) UA `холодоагент R134a` UA-side proper Ukrainian noun correctly translated + RU `хладагент R134a` correctly translated — **POL4 НЕ trigger** (нет typo `Хладогент` letter-swap обе локали; UA correct `холодоагент`; RU correct `хладагент`); (6) main-dim UA `габарити 604х535х925 мм` + RU `габариты 604х535х925 мм` Cyr х symmetric supplier-canonical preserve (blknochg → main-dim LIVE preserve в blknochg category; Policy B/C ТОЛЬКО для blk триплет AUTHORED RU, не blknochg LIVE preserve); (7) UA-side `1 двері зі склом` plural noun `двері` для 1-дверного шкафа (UA grammar inconsistency mirror SKU 23 Hendi 233900 + SKU 27 BC85 + SKU 34 supplier-side UA-pluralization pattern); RU `1 дверь со стеклом` singular correctly translated; (8) UA `відтайка через зупинки компресора` correctly translated UA-specific noun `відтайка` (vs SKU 28 b4 supplier UA `автоотайка` typo — SKU 34 supplier translated correctly `відтайка` proper Ukrainian); (9) RU `0,16 кВт` decimal-comma + `кВт` correctly translated; UA mirror `0,16 кВт`; (10) UA-side `електронний блок керування` correctly translated; (11) RU `автоматическое испарение талой воды`+UA mirror `автоматичне випаровування талої води` correctly translated symmetric. **POL2 explicit fix к SKU 34 (RU-only asymmetric)**: RU `+2&hellip;+8˚С` → `+2&hellip;+8&deg;С` U+02DA→`&deg;` HTML entity (semantic-correct degree sign), Cyr С U+0421 preserve, `&hellip;` U+2026 ellipsis HTML entity preserve; UA cell **untouched** (UA `+2...+8 °C` U+00B0 ≠ U+02DA — POL2 не модифицирует distinct codepoint U+00B0). Это **демонстрирует POL2 asymmetric scope** (mirror SKU 29 b4 POL4 asymmetric scope rule): POL2 BOTH locales **WHEN U+02DA present BOTH locales** (mirror SKU 11/12 b2 ПЕРВОЕ POL2 symmetric обе локали; SKU 10 b2 Hata POL4+POL2 symmetric); POL2 ONLY-RU **WHEN U+02DA only RU** (asymmetric — UA correct codepoint U+00B0, не модифицируем). Precedent **chunk-029 b5 SKU 34** = ПЕРВОЕ asymmetric POL2 application в проекте (SKU 10 b2 + SKU 11 b2 + SKU 12 b2 были symmetric обе локали; SKU 34 b5 ПЕРВЫЙ RU-only asymmetric POL2). **POL1 НЕ trigger** (blknochg_soft category, не blk триплет; UA-typo `двецею`/`хладогент`/`автоотайка`/`подстветки` closed-set list — нет в SKU 34 UA cell; supplier UA-side translated correctly без POL1 closed-set typos). **POL4 НЕ trigger** (нет `Хладогент:NH3`/`хладогент` letter-swap typo обе локали; supplier translated correctly). **POL5 unchanged** (forward+retroactive deferred). UA-cell modification counter b5 += 0 (SKU 34 asymmetric RU-only — UA cell не модифицируем; mirror SKU 29 b4 asymmetric RU-only UA-cell mod += 0). Forcar BC1PB — барный холодильный шкаф 140 л 1 стеклянная дверь 2 решетчатые полки для bottles/cans 0,33 л R134a 0,16 кВт термоизоляция 40 мм 604х535х925 мм. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=661388070)*

---

## SKU 35/79 — Барный холодильный шкаф Forcar G-BC2PS (Артикул 661397602) — 🔴 RU=UA + Назв.мод (RU) UA-leak

**Поле:** Название модификации (RU)
**Было:** `Барна холодильна шафа Forcar G-BC2PS`
**Стало:** `Барный холодильный шкаф Forcar G-BC2PS`

**Поле:** Описание товара (RU)
**Было:** (полностью идентично UA — украинский текст)
**Стало:** (полный перевод RU тег-в-tag):

```
<p>Барный холодильный шкаф используется в барах, ресторанах, кафе для хранения и демонстрации напитков в бутылках или жестяных банках по 0,33 л. Может встраиваться в барную стойку. </p> <p>Технические характеристики:</p> <ul> <li>объём камеры 223 л</li> <li>температурный режим +2...+8 °C (при температуре окружающего воздуха до +33 °C и относительной влажности до 60%)</li> <li>2 раздвижные самозакрывающиеся стеклянные двери</li> <li>4 решётчатые полки размером 420мм x 320мм (полки регулируются по высоте)</li> <li>динамическое охлаждение</li> <li>оттайка путём остановки компрессора</li> <li>автоматическое испарение талой воды</li> <li>термоизоляция 40 мм</li> <li>замок на дверях</li> <li>подсветка в камере</li> <li>электронный блок управления</li> <li>хладагент R134a</li> <li>корпус снаружи выполнен из крашеной стали, внутри из алюминия</li> <li>габариты 920мм x 535мм x 925мм</li> <li>мощность 0,16 кВт</li> </ul>
```

*(blk триплет STANDARD — `desc UA==RU` **True** 🔴 (RU = полная укр. копия тела identical UA bytes — magazine скопировал UA в RU cell); `nm_ua`==`nm_ru` `Барна холодильна шафа Forcar G-BC2PS` (UA-leak — body-level `_has_ua` True via `Барна`/`холодильна`/`шафа` Cyr UA-specific chars); `nm_ru`!=`nazv_ru` genuine RU `Барный холодильный шкаф Forcar G-BC2PS` → AUTO Назв.мод (RU) = genuine `nazv_ru`. **ВТОРОЙ Forcar в проекте** — sister-model SKU 34 BC1PB (single 1-door variant); G-BC2PS = G prefix glass + BC2 = 2-door sliding-glass + PS = polished-stainless 223 л larger 2-дверная самозакрывающаяся sliding-version; ПЕРВЫЙ Forcar **blk триплет** (SKU 34 был Forcar blknochg_soft). **Forcar НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — НЕ ∈ NP-SET) → обычная обработка, НЕ SKIP-НП. Описание (RU) — авторский полный перевод тег-в-tag (структура UA зеркалится 1:1; 1 `<p>` opening narrative + 1 `<p>Технические характеристики:</p>` + 1 `<ul>` + 15 `<li>` mirror UA structure). SOFT применено к авторскому RU: (1) `<p>Барна холодильна шафа використовується в барах, ресторанах, кафе для зберігання та демонстрації напоїв у пляшках або бляшанках по 0,33 л. Може влаштовуватися в барну стійку. </p>`→`<p>Барный холодильный шкаф используется в барах, ресторанах, кафе для хранения и демонстрации напитков в бутылках или жестяных банках по 0,33 л. Может встраиваться в барную стойку. </p>` (decimal-comma `0,33 л` preserve + trailing space before `</p>` artifact mirror UA verbatim); (2) `<p>Технічні характеристики:</p>`→`<p>Технические характеристики:</p>`; (3) `об'єм камери 223 л`→`объём камеры 223 л` (ё U+0451 + apos drop + `камеры` gen-sing); (4) `температурний режим +2...+8 °C (за температури навколишнього повітря до +33 °C і відносної вологості до 60%)`→`температурный режим +2...+8 °C (при температуре окружающего воздуха до +33 °C и относительной влажности до 60%)` (U+00B0 ° + space + Lat C preserve **POL2 НЕ trigger** distinct codepoint U+00B0 ≠ U+02DA — авторский RU mirror UA verbatim для U+00B0 since UA-source clean U+00B0; varies от SKU 34 b5 RU где U+02DA fixed — SKU 35 RU AUTHORED mirror UA U+00B0 LIVE поскольку UA-source SKU 35 clean U+00B0 different supplier-translate path); (5) `2 розсувні самозакриті двері зі склом`→`2 раздвижные самозакрывающиеся стеклянные двери`; (6) `4 ґратчасті полиці розміром 420х320 мм (полиці регулюються за висотою)`→`4 решётчатые полки размером 420мм x 320мм (полки регулируются по высоте)` (ё U+0451 в `решётчатые` + **Policy B/C inner-dim Lat x + `мм` слитно per axis** — chunk-028 b3 SKU 23/24 precedent для inner-dim Policy B/C в blk триплет AUTHORED RU; varies от SKU 34 b5 blknochg где inner-dim Cyr х preserve — категория-driven); (7) `динамічне охолодження`→`динамическое охлаждение`; (8) `відтайка через зупинки компресора`→`оттайка путём остановки компрессора` (ё U+0451 в `путём`); (9) `автоматичне випаровування талої води`→`автоматическое испарение талой воды`; (10) `термоізоляція 40 мм`→`термоизоляция 40 мм`; (11) `замок на дверях`→`замок на дверях` (UA→RU lexical match identical); (12) `підсвітка в камері`→`подсветка в камере`; (13) `електронний блок керування`→`электронный блок управления`; (14) `холодоагент R134a`→`хладагент R134a` (UA→RU semantic noun-shift); (15) `корпус зовні виготовлений з фарбованою сталі, всередині з алюмінію`→`корпус снаружи выполнен из крашеной стали, внутри из алюминия`; (16) `габарити 920х535х925 мм`→`габариты 920мм x 535мм x 925мм` (**Policy B/C** для главных dim Cyr х→Lat x + `мм` слитно per axis — chunk-028 b3 SKU 23 FROSTY + SKU 24 REEDNEE precedent + chunk-029 b1 SKU 6 FROSTY BC-70 precedent для blk триплет main-dim Policy B/C); (17) `потужність 0,16 кВт`→`мощность 0,16 кВт` (decimal-comma preserve). **POL1 НЕ trigger** (UA cell SKU 35 clean — нет `двецею`/`хладогент`/`автоотайка`/`подстветки` в closed-set list; UA-side supplier-side correctly translated без POL1 closed-set typos). **POL2 НЕ trigger** (UA `+2...+8 °C` + `+33 °C` U+00B0 distinct codepoint — POL2 ТОЛЬКО U+02DA Polish ring above; RU AUTHORED mirror UA U+00B0 preserve symmetric обе локали — distinguishes от SKU 34 b5 RU U+02DA fix asymmetric since SKU 34 supplier RU имеет U+02DA а SKU 35 supplier UA clean U+00B0 → AUTHORED RU mirror U+00B0). **POL3 N/A** (Forcar НЕ ∈ NP-SET). **POL4 N/A** (blk триплет category, не blknochg). **POL5 unchanged**. UA-cell modification counter b5 += 0 (SKU 35 UA clean — нет POL1 trigger; UA cell не модифицируем). бренд Forcar Lat consistent. Forcar G-BC2PS — барный холодильный шкаф 223 л 2 раздвижные самозакрывающиеся стеклянные двери 4 регулируемые решетчатые полки для bottles/cans 0,33 л R134a 0,16 кВт термоизоляция 40 мм 920х535х925 мм sister-model SKU 34 BC1PB larger 2-door sliding-glass variant. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=661397602)*

---

## SKU 36/79 — Минибар FROSTY BC-46 (Артикул 468633330) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg pure — `desc UA==RU` **False** (genuine отдельный RU перевод; UA `Міні холодильник` 2-word vs RU `Мини холодильник` 2-word symmetric narrative); `nm_ua`!=`nm_ru` (UA `Мінібар FROSTY BC-46` vs RU `Минибар FROSTY BC-46`); `nm_ru`==`nazv_ru` clean. **FROSTY НЕ ∈ НП-эксклюзив** (word-boundary NP-hit нет — НЕ ∈ NP-SET) → обычная обработка, НЕ SKIP-НП. LIVE-магазин Horoshop, genuine RU body НЕ переписываем. **FROSTY mini-bar/mini-fridge family** continuation pattern SKU 1 KWS-52M (b1 blknochg) + SKU 3 BC-90 (b1 blknochg) + SKU 6 BC-70 (b1 blk триплет) — SKU 36 BC-46 = ЧЕТВЁРТЫЙ FROSTY mini-fridge в chunk-029; SKU 36-specific feature **морозильное отделение** в дополнение к chilled-section vs SKU 1/3 chilled-only; BC-46 = 46 л SKU-specific smaller variant. LIVE source artefacts preserve verbatim: (1) supplier RU dr `<p>Мини холодильник отлично подойдет для размещения на небольшой площади. Используется для хранения напитков и продуктов, а также имеет морозильное отделение.</p>` opening narrative `Мини холодильник` 2-word + `имеет морозильное отделение` (morozka SKU 36-specific feature) — varies от SKU 1/3 chilled-only opening; (2) supplier UA dr mirror `<p>Міні холодильник чудово підійде для розміщення на невеликій площі. Використовується для зберігання напоїв і продуктів, а також має морозильне відділення.</p>` correctly translated UA-side faithful; (3) supplier RU `<li>Одна дверь</li>` + UA `<li>Одна двері</li>` — UA-side **plural noun `двері` для 1-дверного minibar** (UA grammar inconsistency pattern; mirror SKU 23 Hendi/SKU 27 BC85/SKU 34 Forcar BC1PB supplier UA-pluralization); RU singular `Одна дверь` correctly translated; (4) `<li>Одна регулируемая полка размером 380х190 мм </li>` Cyr х U+0445 supplier-canonical preserve (blknochg → inner-dim preserve verbatim) + trailing space перед `</li>` artifact LIVE preserve обе локали; (5) `<li>Объем 46 л.</li>` no-ё `Объем` (vs `Объём` U+0451 ё в SKU 35 b5 AUTHORED + chunk-027 various — supplier-side ё-letter variability; FROSTY BC-46 supplier dropped ё U+0451 to plain `Объем`); UA mirror `Об'єм 46 л.` apostrophe; SKU 36-specific period `46 л.` (vs SKU 28-31 b4 `46 л` no-period — supplier variant choice); (6) **`<li>Температурный режим +4...+10 &deg;С, морозильное отделение 0...-5&deg;С</li>`** — RU two-temp ranges (chilled chamber + freezer compartment) `&deg;` HTML entity Cyr С U+0421 both ranges; **`0...-5&deg;С` no-space before `&deg;`** SKU 36-specific (vs SKU 1/3/27 typical space-before-`&deg;` — supplier-side formatting variability); UA mirror `+4...+10 °С` U+00B0 ° + space + Cyr С + `0...-5 °C` U+00B0 + space + Lat C — **mixed UA degree-glyph**: chilled `°С` Cyr С vs freezer `°C` Lat C within same SKU LIVE preserve (supplier-side mixed Cyr/Lat С variability LIVE preserve обе локали); RU consistent `&deg;С` Cyr С both ranges; (7) `<li>Механический контроль температуры</li>` no-colon flat-attribute supplier-format (mirror SKU 31 b4 BC60 supplier no-colon); (8) `<li>Цвет черный</li>` no-ё `черный` (vs `чёрный` U+0451 ё в SKU 6 b1 BC-70 blk триплет AUTHORED — supplier-side ё-letter variability LIVE preserve в blknochg); UA mirror `Колір чорний` correctly translated; (9) `<li>Напряжение 220 В</li>` Cyr В U+0412 + space `220 В` (mirror SKU 27 b4 BC85 supplier no-slit `220 В` со-space variability LIVE preserve); UA mirror `Напруга 220 В`; (10) main-dim `<li>Габариты 445х470х450 мм</li>` Cyr х U+0445 supplier-canonical preserve (blknochg → main-dim LIVE preserve в blknochg category — Policy B/C ТОЛЬКО для blk триплет AUTHORED RU; varies от SKU 35 b5 blk триплет main-dim Lat x применили в AUTHORED RU); UA mirror `Габарити 445х470х450 мм` Cyr х symmetric. **POL2 НЕ trigger** в SKU 36: UA `°С`/`°C` U+00B0 + RU `&deg;С` HTML entity — оба distinct codepoint от U+02DA Polish ring above; POL2 ТОЛЬКО U+02DA; распределение `&deg;` entity / U+00B0 / U+2103 / U+02DA по supplier-side encoding LIVE preserve обе локали кроме U+02DA POL2 trigger. **POL4 НЕ trigger** (нет POL4 closed-set typos в SKU 36 — `хладогент`/`автоотайка`/`подстветки`/`двецею` отсутствуют). **POL1 НЕ trigger** (blknochg pure category, не blk триплет). **POL5 unchanged** (deferred). UA-cell modification counter b5 += 0. FROSTY BC-46 — мини-холодильник 46 л + морозильное отделение 1 регулируемая полка 380×190 мм чёрный механический температурный диапазон chilled +4...+10 °С / freezer 0...-5°С 220 В 445×470×450 мм Horoshop-LIVE preserve. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=468633330)*

---

## SKU 37/79 — Шкаф холодильный барный REEDNEE LG320S (Артикул 1861580300) — 🔴 RU=UA + Назв.мод (RU) UA-leak

**Поле:** Название модификации (RU)
**Было:** `Холодильна шафа барна REEDNEE LG320S`
**Стало:** `Шкаф холодильный барный REEDNEE LG320S`

**Поле:** Описание товара (RU)
**Было:** (полностью идентично UA — украинский текст)
**Стало:** (полный перевод RU тег-в-tag):

```
<h2>Барный холодильный шкаф REEDNEE LG320S с тремя стеклянными дверями в чёрном корпусе.</h2> <ul>
<li>объём 320 л</li>
<li>корпус чёрный, окрашенная сталь</li>
<li>внутренняя камера из алюминия</li>
<li>6 решётчатых полок с возможностью регулирования</li>
<li>3 стеклянные раздвижные двери</li>
<li>температурный режим 0...+10&deg;С</li>
<li>хладагент R600A</li>
<li>мощность 240 Вт</li>
<li>подключение 220В</li>
<li>габариты 1350мм x 520мм x 850мм</li>
</ul>
```

**Поле:** Описание товара (UA) — SOFT-fix typos (POL1+POL2 2026-05-20: opечатки UA + U+02DA→&deg;)
**Было:** `хладогент R600A`
**Стало:** `хладагент R600A`

**Было:** `0...+10˚С`
**Стало:** `0...+10&deg;С`

*(blk триплет STANDARD + UA SOFT-fix — `desc UA==RU` **True** 🔴 (RU = полная укр. копия тела 388/388 байт identical UA bytes — magazine скопировал UA в RU cell); `nm_ua`==`nm_ru` `Холодильна шафа барна REEDNEE LG320S` (UA-leak — body-level `_has_ua` True via `Холодильна`/`шафа`/`барна` Cyr UA-specific chars); `nm_ru`!=`nazv_ru` genuine RU `Шкаф холодильный барный REEDNEE LG320S` → AUTO Назв.мод (RU) = genuine `nazv_ru`. **ТРЕТИЙ REEDNEE blk триплет в проекте** (precedent **chunk-029 b2 SKU 11 REEDNEE LG128** + **chunk-029 b2 SKU 12 REEDNEE LG198S** ПЕРВЫЕ два REEDNEE blk триплета + b2 ПЕРВОЕ применение POL1+POL2; SKU 37 b5 LG320S = THIRD REEDNEE LG-серия sister-model — 320 л 3-дверная larger variant vs LG128 128 л 1-дверная и LG198S 198 л 2-дверная). **REEDNEE НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. Описание (RU) — авторский полный перевод тег-в-tag (структура UA зеркалится 1:1; 1 `<h2>` + 1 `<ul>` + 10 `<li>` mirror SKU 11/12 b2 REEDNEE template; no `<p>Технические характеристики:`-блок header — UA источник без него mirror verbatim; line-breaks `\n` после `<ul>` и между `<li>` preserve mirror SKU 11/12 b2). SOFT применено к авторскому RU + UA-side фиксы (POL1+POL2 ВТОРОЕ применение в проекте — после b2 SKU 11/12 ПЕРВОЕ применение): (1) `<h2>Барна холодильна шафа REEDNEE LG320S з трьома скляними дверима у чорному корпусі.</h2>`→`<h2>Барный холодильный шкаф REEDNEE LG320S с тремя стеклянными дверями в чёрном корпусе.</h2>` (`з трьома`→`с тремя` cardinal-numeral inversion + ё U+0451 в `чёрном` + instrumental `дверями`); (2) `обсяг 320 л`→`объём 320 л` (UA `обсяг`→RU `объём` ё U+0451); (3) `корпус чорний, фарбована сталь`→`корпус чёрный, окрашенная сталь` (ё U+0451); (4) `внутрішня камера з алюмінію`→`внутренняя камера из алюминия`; (5) `6 гратчастих полиць з можливістю регулювання`→`6 решётчатых полок с возможностью регулирования` (ё U+0451 в `решётчатых` plural-gen); (6) `3 скляні розсувні двері`→`3 стеклянные раздвижные двери` (UA-source имеет `двері` plural-noun для 3 дверей correctly applied — `3 стеклянные раздвижные двери` plural-acc); (7) `температурний режим 0...+10˚С`→`температурный режим 0...+10&deg;С` **POL2 ВТОРОЕ применение**: U+02DA Polish ring above `˚` → `&deg;` HTML entity (semantic-correct degree sign), Cyr С U+0421 после preserve обе локали (RU AUTHORED + UA SOFT-fix); (8) `хладогент R600A`→`хладагент R600A` **POL1 ВТОРОЕ применение обе локали**: typo `хладогент` (letter-swap `о`/`а`) → `хладагент` обе локали (RU AUTHORED clean + UA SOFT-fix); REEDNEE LG-серия supplier-side имеет POL1+POL2 typos consistent через все 3 SKU (LG128/LG198S/LG320S — supplier same-source same-typo across LG-серия LIVE preserve UA-side typo-pattern); (9) `потужність 240 Вт`→`мощность 240 Вт` (Cyr В U+0412); (10) `підключення 220В`→`подключение 220В` (UA `220В` слитно mirror — supplier-style, НЕ применяем `Между числом и единицей пробел` rule в blk триплет mirror UA verbatim — SKU 11/12 b2 same convention); (11) `габарити 1350х520х850 мм` Cyr х U+0445 → `габариты 1350мм x 520мм x 850мм` Lat x U+0078 + `мм` слитно per axis (**Policy B/C** — precedent chunk-028 b3 SKU 24 REEDNEE + chunk-029 b2 SKU 11/12 REEDNEE same Policy B/C для главных dim в blk триплет AUTHORED RU). **UA SOFT-fix (POL1+POL2 ВТОРОЕ применение) — Описание товара (UA) cell modifications:** `хладогент R600A`→`хладагент R600A` + U+02DA `0...+10˚С`→`0...+10&deg;С`. UA-cell modification counter b5 += 1 (SKU 37 POL1+POL2 UA modify). бренд REEDNEE Lat consistent. **REEDNEE НЕ ∈ НП-эксклюзив** (substring nope). REEDNEE LG320S — барный холодильный шкаф 320 л 3 стеклянные раздвижные двери 6 регулируемых решётчатых полок 240 Вт R600A 220 В 1350×520×850 мм; sister-model SKU 11 LG128 + SKU 12 LG198S b2 — supplier same-source same blk триплет signature `desc UA==RU` 🔴 + UA-leak nm_mod + POL1+POL2 closed-set UA typos consistent LG-серия pattern. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=1861580300)*

---

## SKU 38/79 — Витрина холодильная EWT INOX RT98B black (Артикул 2288279586) — 🔴 RU=UA + Назв.мод (RU) UA-leak

**Поле:** Название модификации (RU)
**Было:** `Вітрина холодильна EWT INOX RT98B black`
**Стало:** `Витрина холодильная EWT INOX RT98B black`

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

*(blk триплет STANDARD — `desc UA==RU` **True** 🔴 (758/758 байт identical UA bytes — magazine скопировал UA в RU cell mirror SKU 22 b3 RT98B white 758/758); `nm_ua`==`nm_ru` `Вітрина холодильна EWT INOX RT98B black` (UA-leak); `nm_ru`!=`nazv_ru` clean RU `Витрина холодильная EWT INOX RT98B black` → AUTO Назв.мод RU. **ЧЕТВЁРТЫЙ EWT INOX blk триплет в проекте** (после **chunk-029 b3 SKU 20 RT78B black** + **chunk-029 b3 SKU 21 RT78B white** + **chunk-029 b3 SKU 22 RT98B white** ПЕРВЫЕ три EWT INOX в b3); SKU 38 b5 = **RT98B black** sister-model SKU 22 b3 RT98B **white** — same RT98B 98 л larger cabinet (vs RT78B 78 л smaller) + black/white label asymmetric (mirror SKU 20/21 b3 RT78B black/white pair → SKU 22/38 b3/b5 RT98B white/black pair completes EWT INOX RT-серия 4-variant family). **EWT INOX НЕ ∈ НП-эксклюзивный список** (word-boundary NP-hit нет — сравнение = членство в бренд-SET {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA}, НЕ substring) → обычная обработка, НЕ SKIP-НП. Описание (RU) — AUTHORED 1:1 mirror SKU 22 b3 RT98B white template (same двойной ul template SKU 20/21/22 b3) — **ТОЛЬКО** label change `white`→`black` в `<p>` opening narrative? — Actually nope, opening narrative SKU 38 UA `<p>Шафа-вітрина холодильна EWT INOX RT98B призначена для демонстрації та продажу товарів.</p>` НЕ упоминает black/white внутри body — label остаётся только в nm/nazv/nm_mod; всё body identical SKU 22 b3 RT98B white — same 98 л + 4 полки + R600a + 38 кг + 1110 мм + 1180 мм package. Differences vs SKU 22 b3 SKU-specific: 0 — body bytes identical (UA source 758 bytes mirror SKU 22 b3 758 bytes); single `black`/`white` distinguishing label live в nm-cells только. SOFT применено к авторскому RU (mirror SKU 20/21/22 b3 RT-серия template) — 11 SOFT-fix-translations identical SKU 22 b3 verbatim: (1) `<p>Шафа-вітрина холодильна EWT INOX RT98B призначена для демонстрації та продажу товарів.</p>`→`<p>Шкаф-витрина холодильная EWT INOX RT98B предназначена для демонстрации и продажи товаров.</p>` (note feminine-genitive `холодильная` mirror SKU 22 RT98B white narrative `Шкаф-витрина холодильная` feminine-noun + `предназначена` feminine-singular — RU `Шкаф-витрина` гендерная двойственность в RU между masc `шкаф` и fem `витрина`; supplier-side narrative выбрал fem-agreement `Шкаф-витрина холодильная предназначена` consistent SKU 20/21/22 b3 + SKU 38 b5); (2) `<p>Технічні характеристики:</p>`→`<p>Технические характеристики:</p>`; (3) `4 полиці, регульовані за висотою.`→`4 полки, регулируемые по высоте.`; (4) `Цифрова панель управління.`→`Цифровая панель управления.`; (5) `Корпус - пластик.`→`Корпус - пластик.` (lexical match identical UA→RU); (6) `Об&#39;єм 98 л.`→`Объём 98 л.` (HTML entity apos drop + ё U+0451 + supplier `л.` period preserve); (7) `Температурний режим 0...+12 ℃.`→`Температурный режим 0...+12 &deg;С.` (UA U+2103 ℃ precomposed DEGREE CELSIUS → RU `&deg;С` HTML entity + Cyr С U+0421 per POL2 convention; **POL2 НЕ trigger в UA** — UA source contains U+2103 ℃ precomposed distinct codepoint от U+02DA Polish ring above POL2 normalize ТОЛЬКО U+02DA; UA cell preserved verbatim U+2103 ℃ — POL2 distinct-codepoint scope validation continuation b3 EWT INOX precedent); (8) `Холодоагент R600a.`→`Хладагент R600a.` (UA→RU semantic noun-shift); (9) `Динамічне охолодження.`→`Динамическое охлаждение.`; (10) `Верхнє підсвічування і 2 LED стрічки з боків.`→`Верхняя подсветка и 2 LED-ленты по бокам.` (LED-hyphenation RU mirror SKU 22 b3 + plural-acc `по бокам`); (11) `Вага (нетто), кг: 38`→`Вес (нетто), кг: 38` (integer кг no decimal mirror SKU 22 b3 RT98B white 38 кг); (12) `Довжина (нетто), мм: 428`→`Длина (нетто), мм: 428`; (13) `Ширина (нетто), мм: 386`→`Ширина (нетто), мм: 386` (lexical match identical); (14) `Висота (нетто), мм: 1110`→`Высота (нетто), мм: 1110` (taller cabinet RT98B vs RT78B 960мм; identical SKU 22 b3 RT98B white 1110мм); (15) `Потужність електрична, кВт: 0.17`→`Мощность электрическая, кВт: 0.17`; (16) `Підключення до електромережі: 220V`→`Подключение к электросети: 220V` (Lat V U+0056 preserve); (17) packaging `<p>Розміри в упаковці </p>`→`<p>Размеры в упаковке </p>` (trailing space перед `</p>` artifact mirror UA verbatim — supplier-side packaging-block trailing-space LIVE preserve mirror SKU 20/21/22 b3); (18) `Вага 41`→`Вес 41` (integer kg mirror SKU 22 b3 41 kg packaging); (19) `Глибина 435`→`Глубина 435` (matches SKU 22 b3 packaging depth); (20) `Ширина 475`→`Ширина 475` (lexical match); (21) `Висота 1180`→`Высота 1180` (taller packaging для taller cabinet — mirror SKU 22 b3 RT98B white 1180mm packaging). **POL1/POL2 НЕ trigger** UA остаётся untouched (UA source clean U+2103 ℃ distinct codepoint от U+02DA Polish ring above POL2 не trigger; UA-side нет POL1 closed-set typos `двецею`/`хладогент`/`автоотайка`/`подстветки` — supplier UA-side correctly translated). **POL3 N/A** (EWT INOX НЕ ∈ NP-SET). **POL4 N/A** (blk триплет category, не blknochg). **POL5 unchanged**. UA-cell modification counter b5 += 0 (SKU 38 UA clean). EWT INOX **НЕ ∈ НП-эксклюзив**. **EWT INOX RT-серия 4-variant family completion**: SKU 20 b3 RT78B **black** + SKU 21 b3 RT78B **white** + SKU 22 b3 RT98B **white** + SKU 38 b5 RT98B **black** = full RT78/RT98 ×black/white 2×2 matrix через chunk-029 b3+b5. EWT INOX RT98B black — холодильная витрина 98 л larger cabinet variant black-label sister SKU 22 RT98B white + sister-model RT78B SKU 20/21 4 регулируемых полки R600a 38 кг 220V 1110мм. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=2288279586)*

---

## SKU 39/79 — Печь для пиццы FROSTY F11 (Артикул 499979896) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg pure — `desc UA==RU` **False** (genuine отдельный RU перевод; UA `Піч для піци двосекційна` opening vs RU `Печь для пиццы двухсекционная` correctly translated symmetric); `nm_ua`!=`nm_ru` (UA `Піч для піци FROSTY F11` vs RU `Печь для пиццы FROSTY F11`); `nm_ru`==`nazv_ru` clean. **FROSTY НЕ ∈ НП-эксклюзив** (word-boundary NP-hit нет — НЕ ∈ NP-SET) → обычная обработка, НЕ SKIP-НП. LIVE-магазин Horoshop, genuine RU body НЕ переписываем. **НОВЫЙ домен: FROSTY печи для пиццы** — переход от `Шафи настільні для бару, міні-бари` chilling-domain → pizza-baking-domain внутри chunk-029 b5 (SKU 39/40 FROSTY печи pizza family; SKU 41+ потенциально продолжение pizza-domain или другая категория — b6 проверит). FROSTY F11 — двухсекционная электрическая печь для пиццы 2 камеры 350×410×75 мм 2 пиццы по Ø34 см 3,5 кВт 220 В 510×590×350 мм. LIVE source artefacts preserve verbatim: (1) supplier RU dr `<p>Печь для пиццы двухсекционная.</p>` opening simple-narrative (vs SKU 1/3/6/36 BC-серия mini-fridge marketing-narrative — pizza-domain supplier dr минималистичный opening); UA mirror `<p>Піч для піци двосекційна.</p>` correctly translated; (2) `<li>2 камеры по 350х410х75 мм</li>` Cyr х U+0445 inner-dim supplier-canonical preserve (blknochg → inner-dim LIVE preserve); UA mirror `<li>2 камери по 350х410х75 мм</li>` symmetric Cyr х; (3) **`<li>загрузка 2 пиццы по &Oslash;34 см</li>`** — `&Oslash;` HTML entity для Ø U+00D8 LATIN CAPITAL LETTER O WITH STROKE (diameter symbol) RU supplier-side LIVE preserve обе локали (UA mirror `&Oslash;34 см` — но wait, проверить UA source: UA contains `Ø34` literal U+00D8 codepoint vs RU `&Oslash;` HTML entity — supplier-side asymmetric encoding choice для diameter symbol LIVE preserve обе локали; entity-vs-codepoint mirror SKU 27/28 b4 degree-glyph asymmetric — supplier-side encoding variability); (4) **SKU 39 critical UA-side artifact `<li>со стеклом и подсветкой</li>`** — **UA cell содержит RU phrase verbatim** without translate (correct UA `зі склом та підсвічуванням`) **NEW semantic-translate-skip артефакт b5** mirror SKU 30/31 b4 UA `Уровень шума` RU-calque pattern (NEW artefact category from b4 — POL5 retroactive expansion candidate semantic-translate-skip whole-phrase). LIVE preserve UA-side verbatim (POL5 candidate post-W1-STOP — semantic translate-skip whole-phrase `со стеклом и подсветкой` UA RU-leak); (5) `<li>4 термостата для раздельного управления ТЭНами</li>` RU + UA mirror `<li>4 термостати для роздільного керування ТЕНами</li>` correctly translated UA-side; (6) `<li>температура до 350&deg;C</li>` RU `&deg;` HTML entity + Lat C **no-space** перед `&deg;` SKU 39-specific (vs SKU 36 b5 BC-46 `0...-5&deg;С` no-space + +4...+10 `&deg;С` no-space similar — supplier-side no-space convention в pizza-domain + chiller-domain symmetric); UA mirror `<li>температура до 350 °C</li>` U+00B0 ° + **space** + Lat C — **asymmetric supplier-side degree-glyph**: RU `&deg;` HTML entity vs UA U+00B0 codepoint + space — LIVE preserve обе локали; (7) `<li>механическое управление</li>` no-colon flat-attribute (mirror SKU 36 b5 BC-46 `Механический контроль температуры` no-colon supplier-format pattern); UA mirror `<li>механічне керування</li>`; (8) `<li>мощность 3,5 кВт</li>` decimal-comma `3,5 кВт`; UA mirror `<li>потужність 3,5 кВт</li>`; (9) `<li>напряжение 220 В</li>` Cyr В U+0412 + space (mirror SKU 27 b4 BC85 + SKU 36 b5 BC-46 `220 В` со-space supplier convention); UA mirror `<li>напруга 220 В</li>`; (10) `<li>фасад - нержавеющая сталь</li>` RU + UA mirror `<li>фасад — неіржавка сталь</li>` U+2014 em-dash UA-side (vs RU `-` hyphen ASCII) — **asymmetric supplier-side dash-glyph**: UA U+2014 em-dash vs RU U+002D ASCII hyphen LIVE preserve обе локали (supplier-side punctuation variability — Ukrainian typographic em-dash convention vs RU simpler hyphen); (11) main-dim `<li>габариты 510х590х350 мм</li>` Cyr х U+0445 supplier-canonical preserve (blknochg → main-dim LIVE preserve в blknochg category — Policy B/C ТОЛЬКО для blk триплет AUTHORED RU); UA mirror `<li>габарити 510х590х350 мм</li>` symmetric Cyr х. **POL2 НЕ trigger** SKU 39: RU `&deg;` HTML entity + UA U+00B0 ° codepoint — оба distinct от U+02DA Polish ring above; POL2 ТОЛЬКО U+02DA. **POL4 НЕ trigger** (нет POL4 closed-set typos `хладогент`/`автоотайка`/`подстветки`/`двецею` в SKU 39 — pizza-domain без cooling-terms; mechanic-control no-frost-related-typos). **POL1 НЕ trigger** (blknochg pure category). **POL5 unchanged** (deferred — но **SKU 39 generates NEW POL5 candidate `со стеклом и подсветкой` UA RU-leak semantic-translate-skip whole-phrase**; mirror SKU 30/31 b4 UA `Уровень шума` RU-calque new artefact category from b4 — continuation b5 same semantic-translate-skip pattern в pizza-domain). UA-cell modification counter b5 += 0. FROSTY F11 — двухсекционная пицца-печь 2 камеры 350×410×75 мм 2 пиццы Ø34 см 4 термостата ТЭНы 350°C механическое управление 3,5 кВт 220 В нержавеющая сталь фасад 510×590×350 мм Horoshop-LIVE preserve. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=499979896)*

---

## SKU 40/79 — Печь для пиццы FROSTY F6 (Артикул 616390842) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg pure — `desc UA==RU` **False** (genuine отдельный RU перевод; UA `Піч для піци односекційна` opening vs RU `Печь для пиццы односекционная` correctly translated symmetric); `nm_ua`!=`nm_ru` (UA `Піч для піци FROSTY F6` vs RU `Печь для пиццы FROSTY F6`); `nm_ru`==`nazv_ru` clean. **FROSTY НЕ ∈ НП-эксклюзив** (word-boundary NP-hit нет — НЕ ∈ NP-SET) → обычная обработка, НЕ SKIP-НП. LIVE-магазин Horoshop, genuine RU body НЕ переписываем. **SKU 40 ВТОРОЙ FROSTY печь для пиццы в b5** sister SKU 39 F11 (F11 = 2-секционная 2 пиццы; F6 = 1-секционная 6 пицц — larger single chamber для 6× Ø34 пицц одновременно); SKU 40 = FROSTY F6 односекционная электрическая печь для пиццы 1 камера 700×1050×130 мм 6 пицц по Ø34 см 7,2 кВт 380 В 935×1250×330 мм. **SKU 40-specific**: 380 В (vs SKU 39 F11 220 В — F6 larger 7,2 кВт три-фазное промышленное питание). LIVE source artefacts preserve verbatim: (1) supplier RU dr `<p>Печь для пиццы односекционная на 6 пицц.</p>` opening simple-narrative + venue-detail `на 6 пицц` SKU 40-specific volume context; UA mirror `<p>Піч для піци односекційна на 6 піц.</p>` correctly translated; (2) `<li>камера 700х1050х130 мм</li>` Cyr х inner-dim supplier-canonical preserve (blknochg); UA mirror Cyr х symmetric; (3) `<li>загрузка: 6 пицц Ø34 см</li>` — **SKU 40 UA + RU literal `Ø` U+00D8 codepoint** (NOT `&Oslash;` HTML entity SKU 39 RU asymmetric — SKU 40 supplier выбрал literal codepoint обе локали LIVE preserve; varies от SKU 39 RU `&Oslash;` entity choice — supplier-side encoding variability between FROSTY F11/F6 even though same FROSTY brand same pizza-domain — supplier translated each SKU independently with different entity choice); + `<li>загрузка: 6 пицц Ø34 см</li>` RU colon-separator `загрузка:` (vs SKU 39 RU `загрузка 2 пиццы` no-colon — supplier-side colon-variability within SKU 39/40 pair); (4) **SKU 40 critical UA-side artifact `<li>со стеклом и подсветкой</li>`** — **UA cell содержит RU phrase verbatim** без translate (correct UA `зі склом та підсвічуванням`) **continuation SKU 39 b5 NEW semantic-translate-skip артефакт** consistent FROSTY печи family pattern (vs SKU 30/31 b4 UA `Уровень шума` RU-calque BC-серия pattern — FROSTY pizza-домен supplier UA-side translate-skip ТА ЖЕ phrase `со стеклом и подсветкой` ОБЕ pizza-SKUs SKU 39/40); SKU 40 = ВТОРОЙ semantic-translate-skip whole-phrase POL5 candidate в b5 (cumulative b5 = 2 candidates SKU 39/40 same phrase). LIVE preserve UA-side verbatim (POL5 candidate post-W1-STOP); (5) `<li>2 термостата для раздельного управления ТЭНами</li>` RU + UA `<li>2 термостати для роздільного керування ТЕНами</li>` correctly translated (SKU 40 = 2 термостата vs SKU 39 = 4 термостата — larger single chamber требует меньше термостатов); (6) `<li>температура до 450&deg;C</li>` RU `&deg;` HTML entity + Lat C **no-space** перед `&deg;` (mirror SKU 39 supplier RU `350&deg;C` no-space convention); UA mirror `<li>температура до 450 °C</li>` U+00B0 + **space** + Lat C — **asymmetric supplier-side degree-glyph continuation** consistent SKU 39 b5 pattern (RU `&deg;` entity / UA U+00B0 codepoint within same FROSTY печи family); (7) `<li>механическое управление</li>` no-colon flat-attribute mirror SKU 39 b5 pattern; UA mirror `<li>механічне керування</li>`; (8) `<li>мощность 7,2 кВт</li>` decimal-comma `7,2 кВт`; UA mirror `<li>потужність 7,2 кВт</li>`; (9) **`<li>напряжение 380 В</li>`** — **SKU 40-specific 380 В** three-phase industrial power (vs SKU 39 F11 220 В single-phase domestic — larger F6 7,2 кВт требует three-phase 380 В power; supplier-side correctly distinguishes); UA mirror `<li>напруга 380 В</li>`; (10) `<li>фасад - нержавеющая сталь</li>` RU mirror SKU 39 b5 ASCII hyphen + UA mirror `<li>фасад — неіржавка сталь</li>` U+2014 em-dash UA-side **asymmetric dash-glyph continuation** consistent SKU 39 b5 supplier punctuation pattern; (11) main-dim `<li>габариты 935x1250х330 мм</li>` — **mixed Lat x + Cyr х within single dim line** SKU 40-specific: `935` + **Lat x** U+0078 + `1250` + **Cyr х** U+0445 + `330 мм` — supplier-side intra-line mixed-x-glyph LIVE preserve (NEW artefact in b5 — mixed Lat/Cyr x within single габариты-string — varies от SKU 36/39 b5 + b4 supplier-side single-glyph convention); UA mirror `<li>габарити 935x1250х330 мм</li>` Cyr х + Lat x mirror — symmetric supplier-side same-mixed-glyph обе локали. **POL2 НЕ trigger** SKU 40: RU `&deg;` HTML entity + UA U+00B0 ° codepoint — оба distinct от U+02DA. **POL4 НЕ trigger** (pizza-domain без cooling-typos). **POL1 НЕ trigger** (blknochg pure). **POL5 unchanged** (deferred — но SKU 40 **continuation NEW POL5 candidate** `со стеклом и подсветкой` UA RU-leak whole-phrase semantic-translate-skip mirror SKU 39 b5 — FROSTY pizza-печи family pattern; кумул. b5 POL5 candidates = 2 SKU same phrase). UA-cell modification counter b5 += 0. FROSTY F6 — односекционная пицца-печь 1 камера 700×1050×130 мм 6 пицц Ø34 см 2 термостата ТЭНы 450°C механическое управление 7,2 кВт **380 В three-phase** нержавеющая сталь фасад 935×1250×330 мм sister-model SKU 39 F11 larger 6-pizza single-chamber industrial-power Horoshop-LIVE preserve. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=616390842)*

**Наблюдения по батчу SKU 33-40 (40/79) — chunk-029 (ПЯТЫЙ батч chunk-029; **ТРЕТИЙ POL applications batch** в проекте после b2 (POL1+POL2 первое) и b4 (POL4 второе+третье); b3 был ЧИСТЫЙ POL non-trigger batch; b1 и b5 = mix):** **blk триплет 3** (SKU 35 Forcar G-BC2PS **ВТОРОЙ Forcar в проекте** ПЕРВЫЙ Forcar blk триплет; SKU 37 REEDNEE LG320S **ТРЕТИЙ REEDNEE blk триплет** completing LG-серия LG128/LG198S/LG320S family через b2+b5 — supplier same-source same blk триплет signature `desc UA==RU` 🔴 + UA-leak nm_mod + POL1+POL2 closed-set UA typos consistent LG-серия pattern; SKU 38 EWT INOX RT98B black **ЧЕТВЁРТЫЙ EWT INOX blk триплет** completing RT-серия RT78B black/white + RT98B white/black 2×2 4-variant family через chunk-029 b3+b5). **blkv 0; blknotrip 0; blknochgeq 0; SKIP-НП 0** (нет НП-эксклюзив брендов в b5 — все 8 SKU Tefcold/Forcar/FROSTY/REEDNEE/EWT INOX, **НЕ ∈ NP-SET**; Hurakan ×5 завершено в b1+b2 chunk-029 SKU 2/8/13/14/15; кумул. SKIP-НП chunk-029 = 5 unchanged). **blknochg pure 4** (SKU 33 Tefcold TM32 BLACK **ВОСЕМНАДЦАТЫЙ Tefcold blknochg** ПЕРВЫЙ Tefcold blknochg в b5 после самого плотного 8-Tefcold batch b4 — mixed-case `Tefcold` mirror SKU 32 b4 FS-серия capitalization + двойной Lat-`p` обе строки RU + `Хладагент NH3` correctly translated supplier-side BOTH locales POL4 НЕ trigger TM-серия contrast SKU 28/29 b4 supplier-cleanness pattern; SKU 36 FROSTY BC-46 **ЧЕТВЁРТЫЙ FROSTY mini-fridge** в chunk-029 (SKU 1 KWS-52M/SKU 3 BC-90/SKU 6 BC-70/SKU 36 BC-46) — 46 л + морозильное отделение mixed UA degree-glyph chilled `°С` vs freezer `°C` within same SKU LIVE preserve; SKU 39 FROSTY F11 + SKU 40 FROSTY F6 — **НОВЫЙ домен FROSTY печи для пиццы** в chunk-029 (pizza-baking-domain переход от chilling-domain BC-серия + минибар family) — 2-секционная F11 220 В / 1-секционная F6 380 В three-phase industrial; FROSTY family domain-shift SKU 36 chiller→SKU 39/40 pizza-oven). **blknochg_soft 1** (SKU 34 Forcar BC1PB **ПЕРВЫЙ Forcar в проекте** ПЕРВЫЙ Forcar blknochg_soft; **ЧЕТВЁРТОЕ применение POL2 в проекте — ПЕРВОЕ asymmetric POL2 в проекте (RU-only)**: RU `+2&hellip;+8˚С`→`+2&hellip;+8&deg;С` U+02DA → `&deg;` HTML entity Cyr С preserve; UA `+2...+8 °C` U+00B0 + Lat C distinct codepoint preserve POL2 не модифицирует distinct codepoint U+00B0 ≠ U+02DA — UA-cell mod b5 += 0 mirror SKU 29 b4 POL4 asymmetric scope rule per-locale typo-driven fix preserve where correct). Классификация: blk триплет 3 + blkv 0 + blknotrip 0 + blknochgeq 0 + blknochg pure 4 + blknochg_soft 1 + SKIP-НП 0 = 8 ✓. **5 политик 2026-05-20 в b5 — POL applications + POL non-trigger validations:** **POL1** (blk триплет UA-typo fix обе локали) **ВТОРОЕ применение в проекте** — SKU 37 REEDNEE LG320S UA `хладогент R600A`→`хладагент R600A` letter-swap `о`/`а` обе локали (RU AUTHORED + UA SOFT-fix); REEDNEE LG-серия supplier same-source same POL1 typo pattern (mirror SKU 11/12 b2 ПЕРВОЕ POL1 application LG-серия same pattern). **POL2** (U+02DA→`&deg;`) **ЧЕТВЁРТОЕ применение в проекте** — SKU 34 b5 Forcar **ПЕРВОЕ asymmetric POL2 в проекте (RU-only)** RU `+2&hellip;+8˚С`→`+2&hellip;+8&deg;С` UA preserve U+00B0; SKU 37 b5 REEDNEE symmetric обе локали `0...+10˚С`→`0...+10&deg;С` (RU AUTHORED + UA SOFT-fix mirror SKU 11/12 b2 symmetric LG-серия). POL2 scope demonstrated: BOTH locales WHEN U+02DA present BOTH locales (SKU 37 symmetric mirror SKU 11/12 b2); ONLY-RU WHEN U+02DA only RU (SKU 34 asymmetric ПЕРВЫЙ — UA correct codepoint U+00B0 ≠ U+02DA preserve). **POL3** (SKIP-НП strict by brand) N/A для batch (нет НП-эксклюзив брендов в b5 — все 8 = Tefcold/Forcar/FROSTY/REEDNEE/EWT INOX). **POL4** (blknochg LIVE SOFT-typos) **НЕ trigger** в b5 (нет `хладогент`/`Хладогент`/`автоотайка`/`подстветки`/`двецею` closed-set typos в blknochg SKU 33/36/39/40 RU+UA bodies; SKU 33 Tefcold TM32 `Хладагент NH3` supplier-side correctly translated BOTH locales — TM32 BC-серия-like supplier-cleanness pattern distinguishes от SKU 28/29 b4 TM42/TM44G POL4 trigger; SKU 34 Forcar blknochg_soft но POL2 trigger NOT POL4 — Forcar BC1PB supplier-cleanness для cooling-terms тоже). **POL5** (forward + retro 016-028 после W1 STOP) unchanged. b5 ∈ forward scope chunk-029 onwards. Retroactive cleanup deferred до W1 STOP (chunk-054 CLOSED 54/54). **b5 generates 1 new POL5 candidate** (`со стеклом и подсветкой` UA RU-leak whole-phrase semantic-translate-skip SKU 39/40 FROSTY печи для пиццы family — same artefact category SKU 30/31 b4 UA `Уровень шума` RU-calque semantic-translate-skip; cumulative POL5 candidates whole-phrase translate-skip = 2 phrases × multiple SKUs from b4+b5). **UA-cells modified counter b5 = 1** (SKU 37 REEDNEE LG320S UA POL1+POL2 symmetric); кумул. UA-cells modified chunk-029 = **5 SKU** (10 b2 + 11 b2 + 12 b2 + 28 b4 + 37 b5); кумул. UA-cells modified в проекте = **5 SKU** (b5 добавляет 1 SKU 37). **Brand-distribution в b5**: Tefcold ×1 (SKU 33) + Forcar ×2 (SKU 34/35 — ПЕРВЫЕ Forcar в проекте) + FROSTY ×3 (SKU 36 mini-fridge + SKU 39/40 pizza-oven family — domain-shift внутри FROSTY brand) + REEDNEE ×1 (SKU 37 завершает LG-серия) + EWT INOX ×1 (SKU 38 завершает RT-серия). **Two new brand-families introduced в b5**: Forcar (NEW в проекте — итальянский холодильный бренд) + FROSTY pizza-печи domain (внутри уже-известного FROSTY brand). **Two existing brand-families completed в b5**: REEDNEE LG-серия (LG128/LG198S/LG320S = 1/2/3-дверная progression через b2+b5) + EWT INOX RT-серия (RT78B black/white + RT98B white/black 2×2 4-variant family через b3+b5). Открытых вопросов по батчу 0 (ledger chunk-029 остаётся 0; questions.md НЕ создаём). Кумул. SKIP-НП chunk-029 = 5 (b1 2 + b2 3 — unchanged в b3+b4+b5, Hurakan ×5 закрыт). Кумул. UA-cells modified в проекте = 5 SKU (10/11/12 b2 + 28 b4 + 37 b5). META always faithful (UA!=RU genuine — артефакты источника preserve 1:1: SKU 33 Tefcold двойной Lat-`p` + mixed-case `Tefcold` + `0.62 квт` letter-case unit typo + UA `Рівень шуму` correctly translated varies от b4 supplier-side calque; SKU 34 Forcar asymmetric supplier degree-glyph RU U+02DA vs UA U+00B0; SKU 36 FROSTY BC-46 mixed UA chilled `°С` Cyr С vs freezer `°C` Lat C asymmetric supplier degree-glyph + `Объем` no-ё supplier-side ё-letter variability; SKU 39/40 FROSTY pizza-oven `со стеклом и подсветкой` UA RU-leak whole-phrase + RU `&deg;C` no-space vs UA U+00B0 space asymmetric + RU em-dash UA hyphen punctuation asymmetric + SKU 39 `&Oslash;` entity / SKU 40 literal Ø codepoint supplier encoding variability within FROSTY pizza family + SKU 40 mixed Lat-x/Cyr-х within single габариты-string NEW artefact category in b5; SKU 38 EWT INOX U+2103 ℃ precomposed UA distinct codepoint POL2 не trigger). chunk-029 = 40/79. NEXT: chunk-029 b6 SKU 41-48.

*(scoped к row Артикул=616390842)*

---


## SKU 41/79 — Печь для пиццы FROSTY F66 (Артикул 616390847) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg pure — `desc UA==RU` **False** (genuine отдельный RU перевод 363/375 байт; UA `Піч для піци двосекційна на 12 піц` vs RU `Печь для пиццы двусекционная на 12 пицц` symmetric narrative; F66 = двухсекционная электрическая печь 2 камеры 700×1050×130 мм для 12 пицц Ø34 см 14,4 кВт **380 В three-phase industrial** sister-family SKU 39 F11 двухсекционная **220 В domestic** + SKU 40 F6 односекционная **380 В three-phase** — F66 = ВТОРАЯ 380 В three-phase FROSTY pizza-печь в b6 после SKU 40 F6 b5); `nm_ua`!=`nm_ru` (UA `Піч для піци FROSTY F66` vs RU `Печь для пиццы FROSTY F66`); `nm_ru`==`nazv_ru` clean. **FROSTY НЕ ∈ НП-эксклюзив** (word-boundary NP-hit нет — НЕ ∈ NP-SET) → обычная обработка, НЕ SKIP-НП. **ТРЕТЬЯ FROSTY pizza-печь в проекте** (SKU 39 F11 + SKU 40 F6 b5 + SKU 41 F66 b6 = 3 SKU FROSTY pizza-oven family). LIVE source artefacts preserve verbatim: (1) **критический UA-side artefact continuation** `<li>со стеклом и подсветкой</li>` UA cell содержит RU phrase verbatim без translate (correct UA `зі склом та підсвічуванням`) — **ТРЕТЬЯ POL5 candidate cumulative b5+b6 = 3 SKU same phrase** semantic-translate-skip mirror SKU 39/40 b5 same artefact category; FROSTY pizza-печи family **consistent supplier-side UA RU-leak whole-phrase pattern** across F11/F6/F66 — supplier same-source same-translate-skip; (2) supplier asymmetric degree-glyph: RU `до 450&deg;C` HTML entity no-space + Lat C vs UA `до 450 °C` U+00B0 + space + Lat C LIVE preserve обе локали (mirror SKU 39 b5 supplier-side same asymmetric encoding pattern within FROSTY pizza family); (3) supplier asymmetric dash-glyph: RU `фасад - нержавеющая сталь` ASCII hyphen U+002D vs UA `фасад — неіржавка сталь` U+2014 em-dash LIVE preserve обе локали (mirror SKU 39 b5 supplier punctuation variability); (4) main-dim `<li>габариты 935x1250х600 мм</li>` (RU) + UA mirror `<li>габарити 935x1250х600 мм</li>` — **mixed Lat-x/Cyr-х within single габариты-string** обе локали `935` `x` Lat U+0078 + `1250` `х` Cyr U+0445 + `600` LIVE preserve (continuation SKU 40 b5 mixed-x intra-line artefact category; consistent FROSTY supplier-side intra-line mixed-x-glyph pattern); (5) `<li>2 камери по 700х1050х130 мм</li>` (UA) + RU mirror `2 камеры по 700х1050х130 мм` Cyr х symmetric (inner-dim blknochg → LIVE preserve verbatim, не применяем Policy B/C); (6) `<li>4 термостата </li>` trailing space перед `</li>` LIVE preserve обе локали (supplier-side trailing-space artefact mirror SKU 39 b5 `<li>4 термостата </li>` consistent same supplier pattern); (7) RU `<li>напряжение 380 В</li>` Cyr В U+0412 + UA `<li>напруга 380 В</li>` symmetric — F66 220→380 В industrial step-up vs SKU 39 F11 220 В domestic (F66 14,4 кВт требует three-phase same as SKU 40 F6 7,2 кВт but F66 larger heat-load); (8) загрузка `6+6 пицц Ø34 см` Ø U+00D8 literal codepoint обе локали (supplier mixed entity/literal pattern — SKU 41 RU `Ø` literal symmetric с UA, vs SKU 39 RU `&Oslash;` entity asymmetric с UA `Ø` literal — F66 supplier translated each SKU independently with different entity choice mirror SKU 40 obeя literal). **POL2 НЕ trigger** (RU `&deg;` HTML entity + UA U+00B0 distinct codepoints — оба ≠ U+02DA Polish ring above; POL2 normalize ТОЛЬКО U+02DA). **POL1 НЕ trigger** (blknochg pure, не blk триплет). **POL4 НЕ trigger** (нет `хладогент`/`автоотайка`/`подстветки`/`двецею` closed-set typos в SKU 41 — pizza-oven domain отличается от refrigerator-domain где POL4 trigger). **POL3 N/A** (FROSTY НЕ ∈ NP-SET). **POL5 unchanged** (forward+retroactive deferred). UA-cell modification counter b6 += 0. FROSTY F66 — двухсекционная электрическая пицца-печь 12 пицц Ø34 см 2 камеры 700×1050×130 мм 4 термостата 450°C 14,4 кВт 380 В нерж.сталь 935×1250×600 mm LIVE Horoshop preserve. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=616390847)*

---

## SKU 42/79 — Пресс для пиццы FROSTY PF33 (Артикул 916924594) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg pure — `desc UA==RU` **False** (genuine отдельный RU перевод 1906/2083 байт; UA `Прес для піци використовується для приготування тестових заготівок для піци — коростів` vs RU `Пресс для пиццы используется для приготовления тестовых заготовок для пиццы - карстов` symmetric narrative — supplier translated полностью отдельно UA/RU bodies); `nm_ua`!=`nm_ru` (UA `Прес для піци FROSTY PF33` vs RU `Пресс для пиццы FROSTY PF33`); `nm_ru`==`nazv_ru` clean. **FROSTY НЕ ∈ НП-эксклюзив** (word-boundary NP-hit нет — НЕ ∈ NP-SET) → обычная обработка, НЕ SKIP-НП. **НОВЫЙ домен FROSTY pizza-PRESS** в проекте (расширение pizza-domain b5+b6: pizza-печи SKU 39/40 b5 + SKU 41 b6 + pizza-PRESS SKU 42 b6 — domain-shift внутри FROSTY brand от pizza-oven к pizza-press machinery). PF33 = горячий пресс для пиццы карстов 33 cm диаметр заготовки 9 секунд cycle-time RoHS-сертифицированный 1,5 кВт 380 В единая фаза industrial. LIVE source artefacts preserve verbatim: (1) RU body opening `Пресс для пиццы используется для приготовления тестовых заготовок для пиццы - карстов` — RU `- ` ASCII hyphen + space vs UA `— ` U+2014 em-dash + space — supplier-side asymmetric dash-glyph LIVE preserve обе локали (mirror SKU 39/40 b5 + SKU 41 b6 FROSTY-wide asymmetric RU-ASCII / UA-em-dash punctuation pattern — supplier consistent same-pattern across FROSTY family); (2) **5x U+00B0 ° в UA cell**: `150 °C`/`170 °C`/`+130 °C`/`+6 °C`/`+20 °C` distinct codepoints — POL2 НЕ trigger (U+00B0 ≠ U+02DA Polish ring above; POL2 normalize ТОЛЬКО U+02DA Polish ring above; SKU 42 UA supplier-clean U+00B0 + space + Lat C standard codepoint); (3) **5x `&deg;` HTML entity в RU cell**: RU mirror `150&deg;C`/`170&deg;C`/`+130&deg;C`/`+6&deg;C`/`+20&deg;C` no-space supplier-style asymmetric encoding pattern — RU `&deg;` HTML entity vs UA U+00B0 standard codepoint LIVE preserve обе локали (supplier-side asymmetric encoding choice mirror SKU 39 b5 + SKU 41 b6 FROSTY consistent supplier translate-time entity/codepoint variability); (4) **критический UA META artefact** `прес півці` typo в META keywords (correct UA `прес півці` ambiguous noun-construction — supplier UA-side META typo LIVE preserve POL5 retroactive META category candidate); (5) **критический UA META artefact** `піцу карста` (correct UA `піцу карста` ambiguous Cyrillic transliteration vs IT pizza-press terminology) — supplier UA-side META lexical-artefact LIVE preserve обе локали (mirror SKU 30/31 b4 supplier UA-side semantic-skip pattern); (6) RU `карст` lexical adoption Italian `crust` — supplier-side adopted English `crust` через UA `карст` Cyrillic-transliteration → RU `карст` calque LIVE preserve обе локали (NEW lexical category для pizza-PRESS domain — supplier UA-side adopted English-via-Cyrillic Italian-tech-term `crust`/`carst`); (7) `<p>Час формування однієї заготовки становить не більш ніж дев'ять секунд` apostrophe в `дев'ять` U+0027 ASCII (correct UA нужен `'` U+2019 right-single-quote) — supplier-side ASCII apostrophe LIVE preserve UA-side artefact (mirror SKU 19 b3 Tefcold UA `&rsquo;` entity supplier-vary внутри Tefcold + SKU 33 b5 supplier `&#39;` entity — supplier ASCII vs entity vs proper U+2019 variability); (8) RU `Время формирования одной заготовки составляет-не более девяти секунд` — RU `составляет-не` no-space hyphen artefact (correct RU `составляет, не более` или `составляет не более`) — supplier-side RU formatting-typo LIVE preserve (NEW supplier-typo category в b6 — RU body formatting-error symmetric с UA semantic-translate-skip); (9) `RoHS` европейская сертификация preserve обе локали Lat consistent. **POL2 НЕ trigger** (5x U+00B0 distinct codepoint UA + 5x `&deg;` HTML entity RU — ни одной U+02DA Polish ring above; POL2 normalize ТОЛЬКО U+02DA). **POL1/POL4 НЕ trigger** (blknochg pure, не blk триплет; closed-set list `хладогент`/`автоотайка`/`подстветки`/`двецею` отсутствует в SKU 42 pizza-PRESS domain). **POL3 N/A** (FROSTY НЕ ∈ NP-SET). **POL5 unchanged**. UA-cell modification counter b6 += 0. FROSTY PF33 — горячий пресс для пиццы карстов 33 cm 9 sec формирование RoHS-сертифицированный 1,5 кВт 380 В industrial LIVE Horoshop preserve. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=916924594)*

---

## SKU 43/79 — Печь для пиццы ITPIZZA ML66L (Артикул 953820895) — 🔴 RU=UA + Назв.мод (RU) UA-leak

**Поле:** Название модификации (RU)
**Было:** `Піч для піци ITPIZZA ML66L`
**Стало:** `Печь для пиццы ITPIZZA ML66L`

**Поле:** Описание товара (RU)
**Было:** (полностью идентично UA — украинский текст)
**Стало:** (полный перевод RU тег-в-tag):

```
<p>Печь для пиццы имеет две секции на 12 пицц диаметром до 35 см, в каждый ярус по 6 пицц загрузка. Фронтальная панель изготовлена из высококачественной нержавеющей стали. Боковые и задняя панели изготовлены из окрашенной стали. Жаропрочное стекло дверц камеры выпечки. Внутренняя подсветка камеры выпечки. Поверхность для выпечки изготовлена из огнеупорного материала (шамот)</p> <p>Технические характеристики:</p> <ul>
<li>натуральный под</li>
<li>температурный режим от 50&deg;С до 500&deg;С</li>
<li>внутренний размер камеры: 1080мм x 720мм x 140мм.</li>
<li>габариты: 1360мм x 955мм x 745мм</li>
<li>мощность: 18,0 кВт.</li>
<li>Напряжение: 380 В.</li>
<li>Вес: 213 кг</li>
</ul>
```

*(blk триплет STANDARD — `desc UA==RU` **True** 🔴 (RU = полная укр. копия тела 651/651 байт identical UA bytes — magazine скопировал UA в RU cell); `nm_ua`==`nm_ru` `Піч для піци ITPIZZA ML66L` (UA-leak — body-level `_has_ua` True via `Піч`/`піци` Cyr UA-specific chars); `nm_ru`!=`nazv_ru` genuine RU `Печь для пиццы ITPIZZA ML66L` → AUTO Назв.мод (RU) = genuine `nazv_ru`. **ПЕРВЫЙ ITPIZZA в проекте** — NEW brand-family Italian pizza-oven итальянский производитель **профессиональных** pizza-печей; ITPIZZA НЕ ∈ NP-SET word-boundary nope → обычная обработка, НЕ SKIP-НП. ML66L = двухсекционная подовая (натуральный под — шамот-камень) электрическая печь 2 яруса 12 пицц diameter до 35 см 18 кВт 380 В three-phase industrial 213 кг 1360×955×745 mm main-dim 1080×720×140 mm inner-dim per ярус (vs SKU 41 FROSTY F66 same 12 пицц но FROSTY 14,4 кВт + 935×1250×600 mm — ITPIZZA ML66L larger 18 кВт + larger main-dim + шамот-камень + heavy 213 кг = professional segment vs FROSTY consumer/SMB pizza-oven). Описание (RU) — авторский полный перевод тег-в-tag (структура UA зеркалится 1:1; 1 `<p>` opening narrative + 1 `<p>Технические характеристики:</p>` + 1 `<ul>` + 7 `<li>` mirror UA structure). SOFT применено к авторскому RU: (1) `<p>Піч для піци має дві секції на 12 піц діаметром до 35 см, в кожен ярус по 6 піц завантаження. Фронтальна панель виготовлена з високоякісної нержавейющей сталі. Бічні і задня панелі виготовлені з пофарбованої сталі. Жароміцне скло дверцят камери випічки. Внутрішня підсвітка камери випічки. Поверхня для випічки виготовлена з вогнетривкого матеріалу (шамот)</p>`→`<p>Печь для пиццы имеет две секции на 12 пицц диаметром до 35 см, в каждый ярус по 6 пицц загрузка. Фронтальная панель изготовлена из высококачественной нержавеющей стали. Боковые и задняя панели изготовлены из окрашенной стали. Жаропрочное стекло дверц камеры выпечки. Внутренняя подсветка камеры выпечки. Поверхность для выпечки изготовлена из огнеупорного материала (шамот)</p>` — note UA-source `високоякісної нержавейющої сталі` artefact mix (UA `високоякісної` correct UA-adj + RU-stem `нержавейющої` instead of correct UA `неіржавкої` — supplier UA-side **mixed UA/RU-stem artefact** LIVE source artefact; AUTHORED RU normalize `нержавеющей стали` correctly translated); `(шамот)` UA refractory-material noun preserve обе локали — Italian `chamotte` Cyrillic-transliteration shared lexicon; (2) `<p>Технічні характеристики:</p>`→`<p>Технические характеристики:</p>`; (3) `натуральний під`→`натуральный под` (UA `під` = hearth/oven-floor, RU semantic match `под` — pizza-oven domain SKU 43-specific terminology vs SKU 41 FROSTY F66 `2 камери` chamber-construction; ML66L шамот-под = traditional Italian-style refractory-stone oven-floor); (4) `температурний режим від 50&deg;С до 500&deg;С`→`температурный режим от 50&deg;С до 500&deg;С` `&deg;` HTML entity Cyr С U+0421 preserve обе локали + `від`→`от` + `до`→`до` symmetric numerical range — **POL2 НЕ trigger** (UA `&deg;` HTML entity уже clean — POL2 normalize U+02DA Polish ring above, но `&deg;` HTML entity = semantic-correct preserve verbatim mirror SKU 33 b5 supplier-clean entity pattern); (5) `внутрішній розмір камери: 1080x720x140 мм.`→`внутренний размер камеры: 1080мм x 720мм x 140мм.` Lat x уже supplier-provided UA U+0078 — AUTHORED RU **Policy B/C** inner-dim Lat x + `мм` слитно per axis + trailing period preserve (chunk-028 b3 SKU 23/24 + chunk-029 b1 SKU 6 + b2 SKU 11/12 + b5 SKU 35/37 precedent inner-dim Policy B/C в blk триплет AUTHORED RU; varies от blknochg где inner-dim LIVE preserve verbatim — категория-driven); (6) `габарити: 1360x955x745 мм`→`габариты: 1360мм x 955мм x 745мм` Lat x уже supplier-provided UA + **Policy B/C** для главных dim Lat x + `мм` слитно per axis (chunk-029 b1 SKU 6 FROSTY BC-70 + b2 SKU 11/12 REEDNEE + b5 SKU 35/37 precedent main-dim Policy B/C в blk триплет AUTHORED RU); (7) `потужність: 18,0 кВт.`→`мощность: 18,0 кВт.` decimal-comma preserve + trailing period preserve; (8) `Напруга: 380 В.`→`Напряжение: 380 В.` Cyr В U+0412 + trailing period preserve (vs SKU 35/37 b5 capitalized supplier-format SKU 43-specific); (9) `Вага: 213 кг`→`Вес: 213 кг` capitalized (varies от b5 lowercase — supplier-format SKU 43-specific capitalization within `<li>`). **POL1 НЕ trigger** (UA cell SKU 43 clean — нет `двецею`/`хладогент`/`автоотайка`/`подстветки` в closed-set list; UA artefact `нержавейющої` UA-stem-mix НЕ в POL1 closed-set; supplier UA-side correctly translated big-picture без POL1 closed-set typos). **POL2 НЕ trigger** (UA `&deg;С` HTML entity уже clean per POL2 convention — distinct от U+02DA Polish ring above; AUTHORED RU mirror UA `&deg;С` preserve symmetric обе локали — distinguishes от SKU 34 b5 RU U+02DA fix asymmetric since SKU 43 source supplier-clean entity-encoded). **POL3 N/A** (ITPIZZA НЕ ∈ NP-SET). **POL4 N/A** (blk триплет category, не blknochg). **POL5 unchanged** (forward+retroactive deferred). UA-cell modification counter b6 += 0 (SKU 43 UA clean — нет POL1 trigger; UA cell не модифицируем — single AUTHORED RU + AUTO Назв.мод RU). бренд ITPIZZA Lat consistent. ITPIZZA ML66L — двухсекционная подовая электрическая печь 12 пицц диаметром 35 см 2 яруса 1080×720×140 mm inner-per-ярус 18 кВт 380 В шамот-под 213 кг 1360×955×745 mm main-dim professional Italian pizza-oven NEW brand-family extension. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=953820895)*

---

## SKU 44/79 — Лопата поворотная для пиццы Gi Metal R-20/120 (Артикул 1282324980) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg pure — `desc UA==RU` **False** (genuine отдельный RU перевод 361/376 байт; UA `Лопата поворотна для піци Gi Metal R-20/120` vs RU `Лопата поворотная для пиццы Gi Metal R-20/120` symmetric narrative); `nm_ua`!=`nm_ru` (UA `Лопата поворотна для піци Gi Metal R-20/120` vs RU `Лопата поворотная для пиццы Gi Metal R-20/120`); `nm_ru`==`nazv_ru` clean. **ПЕРВЫЙ Gi Metal в проекте** — NEW brand-family итальянский производитель **профессиональных pizza-аксессуаров** (лопаты, тримачи, ножи); Gi Metal НЕ ∈ NP-SET word-boundary nope → обычная обработка, НЕ SKIP-НП. R-20/120 = вращающаяся (поворотная) лопата для извлечения готовой пиццы и для поворачивания в печи Ø200 мм диаметр полотна 1200 мм длина ручки 0,78 кг разборный пластмассовый держатель из нержавеющей стали — accessory-category отличается от pizza-печь/pizza-press machinery SKU 39-43 b5+b6. LIVE source artefacts preserve verbatim: (1) supplier RU dr `<p>Лопата поворотная для пиццы Gi Metal R-20/120.</p> <p>Лопата для изъятия готовой пиццы и для поворачивания в печи.</p>` symmetric с UA `<p>Лопата поворотна для піци Gi Metal R-20/120.</p> <p>Лопата для вилучення готової піци та для обертання в печі.</p>` correctly translated; (2) **supplier asymmetric Ø-glyph encoding**: RU `Диаметр полотна, мм - &oslash; 200` `&oslash;` HTML entity U+00F8 latin small o with stroke (small ø lowercase entity) vs UA `Діаметр полотна, мм — ø 200` literal U+00F8 ø lowercase codepoint — supplier-side asymmetric entity-vs-codepoint variability LIVE preserve обе локали (varies от SKU 39 b5 FROSTY F11 `&Oslash;` capital Ø U+00D8 entity vs literal — Gi Metal SKU 44 supplier translate-time chose lowercase ø U+00F8 instead of capital Ø U+00D8 — supplier-side ø-letter-case variability LIVE preserve; **POL2 НЕ trigger** для Ø/ø — POL2 normalize ТОЛЬКО U+02DA Polish ring above); (3) **RU dash-glyph asymmetry**: RU `мм - &oslash; 200` ASCII hyphen + space U+002D vs UA `мм — ø 200` U+2014 em-dash + space — supplier-side asymmetric dash-glyph LIVE preserve обе локали (continuation FROSTY family pattern SKU 39/40 b5 + SKU 41 b6 — Italian-supplier-side consistent asymmetric RU-ASCII / UA-em-dash punctuation across brands Gi Metal); (4) `Вес 0,78кг` RU no-space перед `кг` artefact vs `0,73 кг` UA с space — supplier-side **asymmetric unit-space**: RU no-space `0,78кг` artefact vs UA `0,78 кг` standard space (mirror UA `0,73 кг` SKU 45 same pattern — Gi Metal supplier RU translate-time no-space artefact LIVE preserve обе локали); (5) decimal-comma `0,78` preserve обе локали (correctly translated metric-decimal-format); (6) `Розмір` UA `<p><b>Розміри, мм:</b> 1390х200</p>` Cyr х U+0445 + RU mirror `<p><b>Размеры, мм:</b> 1390х200</p>` Cyr х symmetric (blknochg → main-dim LIVE preserve verbatim не применяем Policy B/C); (7) UA META artefact `піцерійна` (correct UA `піцерійна` artefact noun-construction — supplier UA-side META lexical-artefact LIVE preserve POL5 retroactive META category candidate); (8) UA META `хендді` artefact (correct UA-transliteration English `handy` — supplier UA-side META Cyrillic-transliteration English-tech-term LIVE preserve continuation lexical-adoption pattern). **POL2 НЕ trigger** (нет U+02DA Polish ring above; Ø/ø ≠ degree-glyph). **POL1/POL4 НЕ trigger** (blknochg pure, не blk триплет; closed-set list `хладогент`/`автоотайка`/`подстветки`/`двецею` отсутствует в SKU 44 accessory-domain). **POL3 N/A** (Gi Metal НЕ ∈ NP-SET). **POL5 unchanged**. UA-cell modification counter b6 += 0. Gi Metal R-20/120 — поворотная лопата для пиццы Ø200 mm полотно 1200 mm ручка 0,78 кг разборный пластиковый держатель нержавеющая сталь 1390×200 mm main-dim NEW brand-family accessory-domain LIVE Horoshop preserve. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=1282324980)*

---

## SKU 45/79 — Лопата поворотная для пиццы Gi Metal R-20F/120 (Артикул 1282331745) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg pure — `desc UA==RU` **False** (genuine отдельный RU перевод 387/401 байт; UA `Лопата поворотна для піци Gi Metal R-20F/120` vs RU `Лопата поворотная для пиццы Gi Metal R-20F/120` symmetric); `nm_ua`!=`nm_ru` (UA `Лопата поворотна для піци Gi Metal R-20F/120` vs RU `Лопата поворотная для пиццы Gi Metal R-20F/120`); `nm_ru`==`nazv_ru` clean. **ВТОРОЙ Gi Metal в проекте** — sister-model SKU 44 R-20/120 + SKU 45 R-20F/120 (R-20 серия) — F suffix = **просеивающий борт** sieve-feature добавлен (UA `Відсіює зайве борошно` + RU `Отсеивает лишнюю муку`) vs SKU 44 base no-sieve; R-20F/120 0,73 кг lighter than R-20/120 0,78 kg — F-feature reduces weight from extra-fabrication path. Gi Metal R-серия НЕ ∈ NP-SET → обычная обработка. LIVE source artefacts mirror SKU 44 pattern + SKU 45-specific F-feature line: (1) **mirror SKU 44 supplier asymmetric Ø-glyph encoding** RU `мм - &oslash; 200` HTML entity lowercase + UA `мм — ø 200` literal codepoint — Gi Metal supplier consistent SKU 44/45 same pattern within R-серия; (2) **mirror SKU 44 RU dash-glyph asymmetry** RU ASCII hyphen `мм -` vs UA U+2014 em-dash `мм —` — supplier consistent pattern; (3) **F-feature line UA-only artefact**: UA `Відсіює зайве борошно.` (Ukrainian `Відсіює` = "sifts/sieves", `зайве` = "excess") + RU mirror `Отсеивает лишнюю муку.` correctly translated symmetric — SKU 45-specific F-feature description sentence varies от SKU 44 (R-20/120 без sieve, R-20F/120 with sieve) — supplier-side sister-model-feature-line addition pattern; (4) `Вага 0,73 кг` UA standard space vs RU `Вес 0,73кг` no-space `кг` artefact — same supplier-side asymmetric unit-space pattern SKU 44 LIVE preserve обе локали; (5) RU `<p>Лопата и ручка из нержавеющей стали. Пластмассовый держатель на ручке подвижный, разборный(удобный для мытья) и заменяемый.` — RU `разборный(` no-space перед `(` artefact + symmetric с UA `розбірний (` standard space перед `(` — supplier-side asymmetric paren-space (RU paren-attached vs UA paren-spaced LIVE preserve обе локали); (6) Cyr х `1390х200` главные dim symmetric blknochg preserve; (7) decimal-comma `0,73` preserve обе локали (correctly translated metric format). **POL2 НЕ trigger** (нет U+02DA). **POL1/POL3/POL4/POL5 не применяется**. UA-cell modification counter b6 += 0. Gi Metal R-20F/120 — поворотная лопата для пиццы с просеивающим бортом Ø200 mm полотно 1200 mm ручка 0,73 кг разборный пластиковый держатель нержавеющая сталь 1390×200 mm sister-model SKU 44 R-20/120 + F-feature sieve-extra mirror LIVE Horoshop preserve. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=1282331745)*

---

## SKU 46/79 — Набор для пиццы Gi Metal BASIC 2 (Артикул 1282375589) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg pure — `desc UA==RU` **False** (genuine отдельный RU перевод 262/269 байт; UA `Набір для піци Gi Metal BASIC 2 включає:` vs RU `Набор для пиццы Gi Metal BASIC 2 включает:` symmetric kit-listing); `nm_ua`!=`nm_ru` (UA `Набір для піци Gi Metal BASIC 2` vs RU `Набор для пиццы Gi Metal BASIC 2`); `nm_ru`==`nazv_ru` clean. **ТРЕТИЙ Gi Metal в проекте** — kit/bundle category vs SKU 44/45 single-accessory R-серия; BASIC 2 = **kit-bundle** 6 items: (1) лопата AE-32R базовая (RU `лопата` UA `лопата` symmetric); (2) поворотная лопата F-20 sister-of SKU 44/45 R-20-серия (RU `лопата поворотная F-20` UA `лопата поворотна F-20`); (3) щётка ACH-SP для чистки печи (RU `щетка` UA `щітка`); (4) держатель/тримач для лопат ACH-PP (RU `держатель` UA `тримач`); (5) нож для пиццы AC-ROM AC-ST2M+AC-ST4M+AC-TPM комплект-набор (RU `нож` UA `ніж`); (6) маслянка/масленка нержавеющая ОL10I+VP40 (RU `Масленка` UA `Маслянка`). Gi Metal НЕ ∈ NP-SET → обычная обработка. LIVE source artefacts preserve verbatim: (1) **Cyr О vs Lat O within SKU code**: UA+RU `ОL10I` — `О` U+041E Cyr capital О + Lat `L` `1` `0` `I` mixed — supplier-side Cyr-Latin mixed-glyph within product-code LIVE preserve обе локали (NEW artefact category в b6 — supplier intra-code Cyr/Lat-letter variability); (2) UA `Маслянка нерж.ОL10I+VP40` no-space `нерж.О` artefact dot-attached abbreviation + RU `Масленка нерж.ОL10I+VP40` mirror — supplier-side asymmetric abbreviation-dot-spacing LIVE preserve обе локали; (3) UA META `піцерійна` typo continuation SKU 44 supplier META lexical-artefact pattern; (4) UA META `хендді` artefact Cyrillic-transliteration English `handy` continuation supplier META transliteration pattern; (5) UA META `Amica` Italian-brand-reference (Italian pizza-equipment heritage brand) preserve обе локали Lat consistent; (6) RU body kit-listing 1:1 mirror UA structure 1 `<p>` + 1 `<ul>` + 6 `<li>` — supplier symmetric kit-format. **POL2 НЕ trigger** (нет U+02DA; нет degree-glyph в kit-listing). **POL1/POL3/POL4/POL5 не применяется**. UA-cell modification counter b6 += 0. Gi Metal BASIC 2 — kit-bundle 6 items для professional pizzaiolo workflow: лопата AE-32R + поворотная F-20 + щётка ACH-SP + держатель ACH-PP + нож AC-ROM (3 blade options) + маслянка нержавеющая ОL10I+VP40 LIVE Horoshop preserve. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=1282375589)*

---

## SKU 49/79 — Печь для пиццы конвейерная APACH AMT 50 (Артикул 1504744336) — SKIP-НП (NP-эксклюзив)

**Поле:** Все ячейки
**Было:** UA-leak (`desc UA==RU` False но `nm_ua`==`nm_ru` True UA-leak)
**Стало:** без изменений — тело из фида НП позже

*(SKIP-НП — brand=Apach ∈ NP-эксклюзив SET (word-boundary Lat caps + Cyr match `Apach` U+0041..U+0068). POL3 правило activated: НЕ переписываем RU, НЕ trogaem UA, cells в `chunk-029-fixed.xlsx` не модифицируем. **ТРЕТИЙ Apach в chunk-029** (после b6 SKU 47/48 AMT 40 + AMT 65). AMT 50 = конвейерная pizza-печь sister-model AMT-серия 35-45 піц/год Ø45 cm 14,2 кВт 380 В 320°С 230 кг 1860×1210×1030. mirror b6 SKU 47/48 SKIP-НП формат. Open questions 0.)*

*(scoped к row Артикул=1504744336)*

---

## SKU 50/79 — Печь для пиццы Frosty WP2ST (Артикул 2037446783) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg pure — `desc UA==RU` **False** (genuine отдельный RU перевод ~720/730 байт; UA `Пекти для піци двокамерна FROSTY WP2ST` archaic UA verb form `Пекти` supplier UA-source artefact LIVE preserve vs RU `Печь для пиццы двухкамерная FROSTY WP2ST` correctly translated); `nm_ua`!=`nm_ru`; `nm_ru`==`nazv_ru` clean. **WP-серия NEW model line в FROSTY pizza-печь family** (после F-серия SKU 39/40 b5 + SKU 41 b6 + теперь WP-серия SKU 50/51 b7 + HGD-серия SKU 52/53 b7 — FROSTY pizza-oven brand-portfolio расширяется до **четырёх model lines** в проекте). FROSTY НЕ ∈ NP-SET → обычная обработка. WP2ST = двухкамерная электромеханическая пицца-печь 2 камеры 400×400×125 мм для 2 пицц Ø40 см на камеру + 3 термостата + температурный диапазон 50-300°С + таймер 60 мин. LIVE source artefacts preserve verbatim: (1) **критический UA-source artefact** `Пекти для піци` archaic UA verb instead of standard `Піч для піци` — supplier UA-side LIVE preserve обе локали верно translated (continuation pattern — SKU 50/51/52/53 same UA artefact `Пекти` 4 SKU FROSTY pizza-печь WP/HGD series consistent); (2) supplier symmetric `&deg;` HTML entity обе локали `от 50 &deg; C до 300 &deg; C` UA + RU `от 50&deg;C до 300&deg;C` no-space RU vs UA с space — supplier asymmetric &deg;-spacing pattern LIVE preserve; (3) **`со стеклом и подсветкой` UA RU-leak continuation pattern** SKU 50/51/52/53 b7 + previous b5/b6 — кумул. 7 SKU FROSTY pizza-печи same supplier semantic-translate-skip phrase (POL5 candidate); (4) `&Oslash;40см` HTML entity capital Ø supplier symmetric обе локали (varies от Gi Metal SKU 44/45 b6 `&oslash;` lowercase — FROSTY-family chose `&Oslash;` capital consistent в pizza-печь body); (5) `400х400х125 мм` Cyr х symmetric (inner-dim blknochg LIVE preserve не применяем Policy B/C); (6) `<strong>Технічні характеристики:</strong>` HTML `<strong>` tag preserve обе локали; (7) RU `<li>Электромеханическое управление</li>` symmetric translated. **POL2 НЕ trigger** (нет U+02DA, оба `&deg;` HTML entity). **POL1/POL4 НЕ trigger** (blknochg pure pizza-domain). **POL3 N/A** (FROSTY НЕ ∈ NP-SET). UA-cell mod b7 += 0. WP2ST LIVE Horoshop preserve. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=2037446783)*

---

## SKU 51/79 — Печь для пиццы Frosty WP1ST (Артикул 2037461007) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg pure — `desc UA==RU` **False**; `nm_ua`!=`nm_ru`; `nm_ru`==`nazv_ru` clean. **WP-серия sister SKU 50** WP1ST = однокамерная version WP2ST: 1 камера 400×400×125 мм для 1 пицца Ø40 см + 2 термостата + 50-300°С + таймер 60 мин. LIVE preserve mirror SKU 50: `Пекти` UA archaic + `&deg;` HTML entity + `&Oslash;` capital + `со стеклом и подсветкой` UA RU-leak phrase + `400х400х125 мм` Cyr х inner-dim. **POL non-triggered** mirror SKU 50. UA-cell mod b7 += 0. WP1ST LIVE Horoshop preserve. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=2037461007)*

---

## SKU 52/79 — Печь для пиццы Frosty HGD-202S (Артикул 2037466306) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg pure — `desc UA==RU` **False**; `nm_ua`!=`nm_ru`; `nm_ru`==`nazv_ru` clean. **HGD-серия NEW model line в FROSTY pizza-печь family** — SKU 52/53 HGD-серия + SKU 50/51 WP-серия + SKU 39/40/41 F-серия = **5+2+2 model lines** FROSTY pizza-oven portfolio расширение в b7. HGD-202S = двухкамерная HGD-серия 2 камеры 630×430×180 мм для 4 пицц Ø30 см на камеру + 4 термостата + раздельное регулирование верхних/нижних ТЭНов + 50-300°С + таймер 60 мин. LIVE preserve mirror SKU 50/51 supplier-side pattern: `Пекти` UA archaic + `&deg;` HTML entity asymmetric spacing + `&Oslash;30см` capital + `со стеклом и подсветкой` UA RU-leak + `630х430х180 мм` Cyr х inner-dim. **HGD-серия distinguishes от WP-серия**: HGD больший размер камеры (630×430 vs 400×400) + раздельное регулирование верх/низ ТЭНов (WP не имеет) + 4 термостата (vs 3 в WP2ST). **POL non-triggered** mirror SKU 50. UA-cell mod b7 += 0. HGD-202S LIVE Horoshop preserve. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=2037466306)*

---

## SKU 53/79 — Печь для пиццы Frosty HGD-101S (Артикул 2037472151) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg pure — `desc UA==RU` **False**; `nm_ua`!=`nm_ru`; `nm_ru`==`nazv_ru` clean. **HGD-серия sister SKU 52** HGD-101S = однокамерная version HGD-202S: 1 камера 630×430×180 мм для 2 пиццы Ø30 см + 2 термостата + раздельное регулирование верх/низ ТЭНов + 50-300°С + таймер 60 мин. LIVE preserve mirror SKU 52 supplier pattern: `Пекти` UA archaic + `&deg;` HTML entity + `&Oslash;` capital + `со стеклом и подсветкой` UA RU-leak. **POL non-triggered** mirror SKU 50. UA-cell mod b7 += 0. HGD-101S LIVE Horoshop preserve. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=2037472151)*

---

## SKU 54/79 — Лопата для пиццы квадратная Gi Metal A-32RF/120 (Артикул 2102780616) — 🔴 RU=UA + Назв.мод (RU) UA-leak

**Поле:** Название модификации (RU)
**Было:** `Лопата для піци квадратна Gi Metal A-32RF/120`
**Стало:** `Лопата для пиццы квадратная Gi Metal A-32RF/120`

**Поле:** Описание товара (RU)
**Было:** (полностью идентично UA — украинский текст)
**Стало:** (полный перевод RU тег-в-tag):

```
<p>Лопата для пиццы AZZURRA. Лёгкая гибкая лопата для загрузки пиццы выполнена полностью из алюминиевого сплава. Ручка лопаты овальной формы значительно облегчает её вес</p> <ul>
<li>перфорированная, прямоугольная</li>
<li>цвет ручки: голубой, электро</li>
<li>размер лопаты: 330х330 мм</li>
<li>длина ручки: 1200 мм</li>
<li>размеры (Д*Ш*В): 330мм x 330мм x 1560мм</li>
<li>вес: 0.63 кг</li>
</ul> <p>Материал:</p> <ul>
<li>корпус: алюминиевый анодированный сплав</li>
</ul> <p> </p>
```

*(blknotrip — `desc UA==RU` **True** 🔴 (RU = полная UA копия 428/428 байт identical — magazine скопировал UA в RU cell); `nm_ua`==`nm_ru` `Лопата для піци квадратна Gi Metal A-32RF/120` (UA-leak в RU nm); `nm_ru`!=`nazv_ru` genuine RU `Лопата для пиццы квадратная Gi Metal A-32RF/120` → AUTO Назв.мод (RU) = `nazv_ru`. **A-серия NEW model line в Gi Metal family** (после R-серия SKU 44/45 b6 + BASIC 2 kit SKU 46 b6 + теперь A-серия SKU 54 b7 + I-серия SKU 55 b7 = Gi Metal portfolio расширение до 4 model lines). Gi Metal НЕ ∈ NP-SET → обычная обработка. A-32RF/120 = квадратная перфорированная алюминиевая загрузочная лопата AZZURRA-series Italian-color-line (голубой/blue электро) для пиццы 330×330 mm полотно + 1200 mm ручка + 1560 mm full length + 0.63 кг lightweight aluminum anodized. AUTHORED RU 1:1 mirror UA structure 1 `<p>` opening + 1 `<ul>/6li` + 1 `<p>Материал:</p>` + 1 `<ul>/1li` + 1 `<p> </p>` trailing whitespace `<p>`. SOFT применено: (1) UA `Лопата для піци AZZURRA. Легка гнучка лопата для завантаження піци виконана повністю з алюмінієвого сплаву` → RU `Лопата для пиццы AZZURRA. Лёгкая гибкая лопата для загрузки пиццы выполнена полностью из алюминиевого сплава` correctly translated `AZZURRA` Italian color-line name preserve Lat; (2) UA `Ручка лопати овальної форми значно полегшує її вагу` → RU `Ручка лопаты овальной формы значительно облегчает её вес` correctly translated; (3) `перфорована, прямокутна` → `перфорированная, прямоугольная`; (4) `колір ручки: блакитний, електро` → `цвет ручки: голубой, электро` `електро`→`электро` correctly translated electric-blue color modifier; (5) `розмір лопати: 330х330 мм` → `размер лопаты: 330х330 мм` Cyr х inner-blade-dim LIVE preserve verbatim (blknotrip не blk триплет — Policy B/C не применяем к inner-dim); (6) `довжина ручки: 1200 мм` → `длина ручки: 1200 мм`; (7) `розміри (Д*Ш*В): 330мм x 330мм x 1560мм` → `размеры (Д*Ш*В): 330мм x 330мм x 1560мм` supplier-formatted Lat x + `мм` слитно per axis уже supplier-provided UA — Policy B/C-compatible mirror в RU 1:1; (8) `вага: 0.63 кг` → `вес: 0.63 кг` ASCII dot decimal preserve (supplier inconsistent decimal-format — varies от запятая comma decimal SKU 32 b4 + SKU 44/45 b6 Gi Metal R-серия — A-серия supplier translate-time chose ASCII dot decimal `0.63` instead of comma `0,63` — POL5 candidate decimal-format inconsistency continuation); (9) `Матеріал:` → `Материал:`; (10) `корпус: алюмінієвий анодований сплав` → `корпус: алюминиевый анодированный сплав` correctly translated technical-term. **POL1 НЕ trigger** (UA cell SKU 54 clean без `двецею`/`хладогент`/`автоотайка`/`подстветки` closed-set typos). **POL2 НЕ trigger** (нет U+02DA, нет degree-glyph в accessory body). **POL3 N/A** (Gi Metal НЕ ∈ NP-SET). **POL4 N/A** (blknotrip category accessory-domain). **POL5 unchanged**. UA-cell mod b7 += 0 (SKU 54 UA clean — single AUTHORED RU + AUTO Назв.мод). Gi Metal A-32RF/120 — квадратная перфорированная алюминиевая лопата AZZURRA 330×330 mm полотно 1200 mm ручка 1560 mm full 0.63 кг lightweight aluminum anodized NEW A-серия Gi Metal accessory pizza-loading. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=2102780616)*

---

## SKU 55/79 — Лопата для пиццы Gi Metal I-20 (Артикул 2375875203) — 🔴 RU=UA + Назв.мод (RU) UA-leak

**Поле:** Название модификации (RU)
**Было:** `Лопата для піци Gi Metal I-20`
**Стало:** `Лопата для пиццы Gi Metal I-20`

**Поле:** Описание товара (RU)
**Было:** (полностью идентично UA — украинский текст)
**Стало:** (полный перевод RU тег-в-tag):

```
<p>Поворотная лопата для извлечения готовой пиццы.</p> <ul>
<li>Пластмассовый держатель на ручке подвижный, разборный</li>
<li>Длина ручки: 1500 мм</li>
<li>Материал: лопата и ручка - нержавеющая сталь</li>
<li>Размеры (Д*Ш*В): 200мм x 200мм x 1710мм</li>
<li>Вес: 0.81</li>
</ul>
```

*(blknotrip — `desc UA==RU` **True** 🔴 (RU = полная UA копия 247/247 байт identical); `nm_ua`==`nm_ru` `Лопата для піци Gi Metal I-20` (UA-leak в RU nm); `nm_ru`!=`nazv_ru` genuine RU → AUTO Назв.мод (RU) = `nazv_ru`. **I-серия NEW model line в Gi Metal family** (sister-distinguishes от A-серия SKU 54 = AZZURRA-color-blade + R-серия SKU 44/45 = rotation-handle). Gi Metal НЕ ∈ NP-SET → обычная обработка. I-20 = поворотная лопата для извлечения готовой пиццы 200×200 mm полотно (квадратное steel blade) + 1500 mm ручка + 1710 mm full length + 0.81 кг нерж.сталь stainless steel + разборный пластмассовый держатель. AUTHORED RU 1:1 mirror UA structure 1 `<p>` opening + 1 `<ul>/5li`. SOFT применено: (1) UA `Поворотна лопата для вилучення готової піци.` → RU `Поворотная лопата для извлечения готовой пиццы.`; (2) `Пластмасовий тримач на ручці рухливий, розбірний` → `Пластмассовый держатель на ручке подвижный, разборный` correctly translated `тримач`→`держатель` semantic-match holder-bracket terminology; (3) `Довжина ручки: 1500 мм` → `Длина ручки: 1500 мм` capitalized; (4) `Матеріал: лопата та ручка - нержавіюча сталь` → `Материал: лопата и ручка - нержавеющая сталь` ASCII hyphen + space mirror supplier formatting; (5) `Розміри (Д*Ш*В): 200мм x 200мм x 1710мм` → `Размеры (Д*Ш*В): 200мм x 200мм x 1710мм` supplier-formatted Lat x + `мм` слитно per axis уже UA-supplied; (6) `Вага: 0.81` → `Вес: 0.81` ASCII dot decimal preserve **supplier-typo missing `кг` unit** LIVE preserve обе локали (NEW supplier-typo category в b7 — supplier UA-source missing unit symbol after numeric — RU mirror preserve без unit-completion); (7) UA `вилучення`→`извлечения` extraction-noun correctly translated; (8) UA `обертання` rotation context implicit removed в short-body version. **POL1 НЕ trigger** (UA cell SKU 55 clean без closed-set typos). **POL2 НЕ trigger** (нет U+02DA, нет degree-glyph). **POL3 N/A** (Gi Metal НЕ ∈ NP-SET). **POL4 N/A** (blknotrip accessory-domain). **POL5 unchanged**. UA-cell mod b7 += 0 (SKU 55 UA clean). Gi Metal I-20 — поворотная лопата для извлечения готовой пиццы 200×200 mm полотно 1500 mm ручка 1710 mm full 0.81 кг нерж.сталь NEW I-серия Gi Metal accessory pizza-extraction. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=2375875203)*

---

## SKU 56/79 — Печь для пиццы Silver PF-62 G газовая (Артикул 2424820545) — RU корректен; правок нет

**Поле:** Название модификации (RU)
**Было:** (чистый рус. бренд+код, украинского leak нет)
**Стало:** без изменений

**Поле:** Описание товара (RU)
**Было:** (RU уже корректный русский перевод — НЕ 🔴 RU=UA)
**Стало:** без изменений

*(blknochg pure — `desc UA==RU` **False** (genuine отдельный RU перевод ~830/870 байт; UA `Пекти для піци Silver PF-62 G ідеально підходить як для свіжої, так і замороженої піци` archaic UA `Пекти` continuation pattern + LIVE preserve vs RU `Печь для пиццы Silver PF-62 G идеально подходит как для свежей, так и замороженной пиццы` correctly translated); `nm_ua`!=`nm_ru` (UA `Піч для піци Silver PF-62 G газова` vs RU `Печь для пиццы Silver PF-62 G газовая`); `nm_ru`==`nazv_ru` clean. **Silver NEW brand-family в проекте** (Italian-supplier pizza-печь газовая) — sister-distinguishes от FROSTY электрические/конвейерные family same pizza-печь category но Silver gas-fired vs FROSTY electric. Silver НЕ ∈ NP-SET → обычная обработка. PF-62 G = одноярусная газовая пицца-печь на 4 пиццы Ø30 cm + камень-под (refractory-stone каменный подовый камень) + 7 кВт газовой мощности + электронная система зажигания + непрерывный контроль пламени + газ балонный или природный 0,741 m³/час + диапазон 50-350°С + 980×910×560 mm + 65 кг + хромированные ножки. LIVE source artefacts preserve verbatim: (1) UA `Пекти для піци Silver PF-62 G` archaic UA `Пекти` continuation FROSTY family pattern SKU 50-53 b7 — **5 SKU same UA artefact `Пекти`** в b7 cumul (4 FROSTY + 1 Silver) supplier-side same UA-source same-archaic-verb pattern; (2) UA `&Oslash; 30 см` + RU `&Oslash; 30 см` HTML entity capital symmetric supplier choice consistent с pizza-печь family; (3) **UA `&#39;` ASCII apostrophe entity x3** `полум&#39;я`/`Кам&#39;яний`/`Кам&#39;яний` — supplier UA-side `&#39;` apostrophe entity LIVE preserve (correct UA `'` U+2019 right-single-quote — supplier `&#39;` entity-encoded variability continuation pattern SKU 33 b5 + SKU 42 b6 supplier ASCII vs entity vs proper U+2019 variability); (4) `<li>Термометр Є</li>` UA `Є` U+0404 Cyrillic capital ukrainian letter (archaic Old-Slavonic form `Є`=is/есть в church-slavonic) supplier UA-side artefact LIVE preserve vs RU `<li>Термометр Есть</li>` correctly translated semantic-noun (RU sense `есть` = "is present") — supplier semantic-translate UA shortform → RU full-noun pattern; (5) `<li>Витрата газу, кг / год 0,741m3/год.</li>` UA whitespace `, ` + ` / ` asymmetric vs RU `<li>Расход газа, кг/час 0,741m3/час.</li>` no-space slash + no-space `m3` mixed Lat-3 numerical compact-format — supplier UA verbose / RU compact unit-format variability LIVE preserve; (6) `<li>Кам&#39;яний подовий камінь.</li>` → `<li>Каменный подовый камень.</li>` `Кам&#39;яний`=`Каменный` translated `&#39;` apostrophe entity dropped in RU correctly (correct RU без apostrophe); (7) UA `Безперервний контроль полум&#39;я.` → RU `Непрерывный контроль пламени.`; (8) UA `Електронна система запалювання.` → RU `Электронная система зажигания.`; (9) UA `Підключення до балонного газу або природного газу.` → RU `Подключение к баллонному газу или природному газу.`; (10) `Хромовані ніжки` → `Хромированные ножки`; (11) `980x910x560` mixed Lat x dim symmetric supplier-formatted обе локали; (12) `62x62x15мм` inner-dim Lat x supplier-formatted symmetric (blknochg → main+inner dims LIVE preserve verbatim не применяем Policy B/C). **POL1 НЕ trigger** (blknochg pure, не blk триплет; closed-set typos `двецею`/`хладогент`/`автоотайка`/`подстветки` отсутствуют в SKU 56 pizza-печь газовая domain). **POL2 НЕ trigger** (нет U+02DA, оба `Є`/`&#39;` ≠ degree-glyph). **POL3 N/A** (Silver НЕ ∈ NP-SET). **POL4 N/A** (pizza-domain без refrigerator-terminology closed-set). **POL5 unchanged** (forward+retroactive deferred). UA-cell mod b7 += 0. Silver PF-62 G — одноярусная газовая пицца-печь 4 пиццы Ø30 cm каменный-под 7 кВт газ балонный/природный 0,741 m³/час 50-350°С 65 кг 980×910×560 хромированные ножки NEW brand-family Silver Italian gas-fired pizza-печь. META always faithful. Открытых вопросов 0.)*

*(scoped к row Артикул=2424820545)*

---

