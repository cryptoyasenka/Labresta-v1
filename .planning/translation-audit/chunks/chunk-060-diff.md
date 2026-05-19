# chunk-060 translation diff (81 SKU — блендеры/подрібнювачі льоду/грили контактні; W2 диапазон 055-085, продолжение chunk-059)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-060 (81 SKU)
**Apply key:** `Артикул` (scoped per row)
**Status:** IN PROGRESS 16/81 (blk триплет 3 / blknochg 6 / blknotrip 6 / SKIP-НП 1; Открытых вопросов 0)
**Worker:** W2 (параллельный воркер, диапазон chunk-055 … chunk-085; W1 ведёт chunk-001 … chunk-054)

**Состав (по типу товара):** первый SKU — Артикул `635596866` (`Блендер Sirman DRAGONE VV`); последний SKU81 — Артикул `2309184793` (`Гриль контактний Frosty EGS-36FF`). Колонка `Бренд` в источнике дублирует `Артикул` (числовой) — бренд определяется по `Название` per-SKU при аудите батча. Тип: блендеры (SKU1-47) + подрібнювачі/млини для льоду (SKU48-66) + грили контактні (SKU67-81). **SKIP-НП (зонд по `Название`): 8 NP-suspect** — все **HURAKAN** в НП-списке → SKIP-НП (тело придёт из фида НП позже, RU не трогается; вносятся в таблицу при обработке соответствующих батчей): SKU6 Арт `732422924` (`Блендер HURAKAN HKN-BLW2 grey\red`) · SKU22 Арт `2111152648` (`Блендер Hurakan HKN-BLW2 grey`) · SKU30 Арт `2503647283` (`Блендер Hurakan HKN-HBH2000S`) · SKU31 Арт `2503651061` (`Блендер Hurakan HKN-HBH2000STH з шумопоглинаючим покриттям`) · SKU33 Арт `2566515692` (`Блендер Hurakan HKN-HBH850M PRO`) · SKU49 Арт `1133814407` (`Подрібнювач льоду HURAKAN HKN-TR65`) · SKU65 Арт `2599060225` (`Подрібнювач льоду HURAKAN HKN-TR65M`) · SKU73 Арт `1147786691` (`Гриль контактний HURAKAN HKN-PE22L`). **AIRHOT НЕ в НП-списке** (SKU48 `Подрібнювач льоду AIRHOT IC-1`, SKU72 `Гриль контактний AIRHOT CGL`) — обрабатывается обычно. Прочие бренды (Sirman, REEDNEE, Hendi, Hamilton Beach, EWT INOX, GoodFood, Frosty, Ceado/CEADO, Bartscher, SARO, Fimar, Vema, …) НЕ в НП-списке — обрабатываются обычно, подтверждается per-батч по `Название`. Батч = 8 SKU; 11 батчей (81/8 → б1-10 по 8 SKU = 80, б11 = SKU81 = 1 SKU). openpyxl rows 2..82 (row = SKU + 1).

**Глоссарий:** новые UA→RU термины — в общий накопительный `chunk-glossary-w2.md` (продолжается, **340 строк** после chunk-059; НЕ пересоздаётся) + по батчам ниже.

---

## Батч 1 — SKU 1-8 (openpyxl rows 2..9)

Категории: blk триплет 3 (SKU2/5/8) · blknotrip 2 (SKU3/4) · blknochg 2 (SKU1/7) · SKIP-НП 1 (SKU6). Наших правленых строк chunk-060 = 5 (rows 3/4/5/6/9). chunk-060-fixed.xlsx создан в этом батче (первый батч с правками, `Copy-Item` из источника).

### SKU1 — ART 635596866 — Блендер Sirman DRAGONE VV — blknochg

`descUA != descRU` (585/600), col7=col5=`Блендер Sirman DRAGONE VV, 2 скорости` — genuine отдельный RU (col4/col6 = `Блендер Sirman DRAGONE VV`, RU обогащён «, 2 скорости»). DSCRU — настоящий русский (профессиональный/двухскоростной/стаканом). UA-marker DSCRU нет. **fixed row2 НЕ тронут** (LIVE-RU не переписывается). ~soft-note НЕ нумеруется: артефакты genuine-RU `хромированый`, `ингридиентов` оставлены как есть (прецедент SKU18/38/39/85).

### SKU2 — ART 635596867 — Блендер Sirman Orione Q VV — blk триплет

`descUA == descRU` True (1205/1205) — UA-leak в RU; col5==col4=`Блендер Sirman Orione Q VV, 2 швидкості` (UA), col7=`Блендер Sirman Orione Q VV, 2 скорости` (genuine RU). **Авто-фикс:** col5←col7 (`Блендер Sirman Orione Q VV, 2 скорости`); col36 ← полный tag-в-tag RU перевод DSCUA (h2 + p×3 + ul/li×5 + p>iframe). iframe-блок (`//www.youtube.com/embed/ALyCH8oSrYE…`) verbatim. dims `232x230x486` латинская x verbatim. power `0,75 кВт` verbatim. `NVR`/`АБС`/`ABS` verbatim. UA-typo `регулатор`→RU `регулятор`. len 1205→1239.

### SKU3 — ART 660007480 — Блендер REEDNEE CBS10/CMES — blknotrip

`descUA == descRU` True (503/503), но col4==col5==col6==col7=`Блендер REEDNEE CBS10/CMES` — language-neutral (бренд+код, НЕ UA-leak). **Авто-фикс:** только col36 ← RU перевод DSCUA; col5 НЕ тронут (остаётся `Блендер REEDNEE CBS10/CMES`). apostrophe U+0027 `об'ємом`→`объемом` (апостроф снят). dims `200х230х490` кириллическая х verbatim. power `1,6 кВт` verbatim. `"pulse"` verbatim. len 503→514.

### SKU4 — ART 660007481 — Блендер REEDNEE CBS30/CMES — blknotrip

`descUA == descRU` True (546/546), col4==col5==col6==col7=`Блендер REEDNEE CBS30/CMES` language-neutral. **Авто-фикс:** только col36; col5 НЕ тронут. `<br />` verbatim. entity `об&#39;ємом`→`объемом` (entity снят → plain). power `1,86кВт` (без пробела) faithful verbatim. dims `230х220х540` кириллическая х verbatim. `об / хв` (с пробелами) → `об / мин` (пробелы сохранены). len 546→556.

### SKU5 — ART 663673968 — Блендер Hendi 230718 — blk триплет

`descUA == descRU` True (618/618) UA-leak; col5==col4=`Блендер високої потужності Hendi 230718` (UA), col7=`Блендер высокой мощности Hendi 230718` (genuine RU). **Авто-фикс:** col5←col7 (`Блендер высокой мощности Hendi 230718`); col36 ← RU перевод (p + ul/li×8). `&ndash;` verbatim. `-40C до +90 C` форма verbatim. dims `270х250х550` кириллическая х verbatim. ~soft-note НЕ нумеруется: source UA-typo `8350-24800 про./мін.` → RU нормализован `8350-24800 об./мин.`; склеенное `стаканобъемом 2,5 л` (источник уже частично RU) → `стакан объемом 2,5 л`. len 618→611.

### SKU6 — ART 732422924 — Блендер HURAKAN HKN-BLW2 grey\red — SKIP-НП #1

Бренд **HURAKAN** ∈ НП-список → **SKIP-НП**. RU не переписан, зонд/скрипт/анализ не делались. **fixed row7 НЕ тронут.** Тело придёт из фида НП позже. Внесён в таблицу SKIP-НП MANUAL-REVIEW строкой #1.

### SKU7 — ART 851150340 — Блендер Hamilton Beach HBH650CE — blknochg

`descUA != descRU` (572/592), col4==col5==col6==col7=`Блендер Hamilton Beach HBH650CE` language-neutral. DSCRU — настоящий русский (`с уникальной системой Wave ~ Action ™, благодаря которой…`). UA-marker DSCRU нет. **fixed row8 НЕ тронут.** ~soft-note НЕ нумеруется: артефакты genuine-RU `от от 50`, dims `178хх230хх457` (двойная х) оставлены как есть (прецедент).

### SKU8 — ART 1128494721 — Блендер EWT INOX MJD2508 — blk триплет

`descUA == descRU` True (504/504) UA-leak; col5==col4=`Блендер EWT INOX MJD2508 з подрібнювачем льоду` (UA), col7=`Блендер EWT INOX MJD2508 с измельчителем льда` (genuine RU). **Авто-фикс:** col5←col7 (`Блендер EWT INOX MJD2508 с измельчителем льда`); col36 ← RU перевод (h2 + p + ul/li×7). apostrophe U+0027 `об'ємом`→`объемом`. dims `290х285х540` кириллическая х verbatim. `"pulse"` verbatim. len 504→514.

**Наблюдения по батчу SKU 1-8 (батч 1).** Блендеры, 7 брендов: Sirman ×2, REEDNEE ×2, Hendi ×1, HURAKAN ×1 (SKIP-НП), Hamilton Beach ×1, EWT INOX ×1. Паттерн UA-leak/genuine разделился чётко: blk триплет там, где col5==col4 UA + col7 genuine RU (SKU2/5/8 — col5←col7 + col36 переведён tag-в-tag); blknotrip там, где col5 language-neutral бренд+код REEDNEE (SKU3/4 — только col36, col5 оставлен); blknochg там, где DSCRU уже настоящий русский с обогащением и `descUA!=descRU` (SKU1/7 — fixed НЕ тронут, genuine-артефакты не правятся). SKIP-НП: HURAKAN SKU6 (#1, forward-only). Verbatim-токены соблюдены: iframe (SKU2), `&ndash;` (SKU5), `&#39;`/U+0027 апостроф снят в переводе (SKU3/4/8), кириллическая х в габаритах, латинская x (SKU2), `"pulse"`, мощность `0,75/1,6/1,86/1,8 кВт`/`1680 Вт` faithful. UA→RU термины батча — в глоссарии. Открытых вопросов батч не дал (рассинхрона модель-кода NAME UA↔genuine-RU и чужих продуктов в name-полях нет). Reopen-verify: rows 3/4/5/6/9 col36!=col35 True, UA-marker DSCRU 0, blk col5==col7 True; rows 2/7/8 не тронуты (len источника сохранён).

---

## Батч 2 — SKU 9-16 (openpyxl rows 10..17)

Категории: blknochg 4 (SKU9/10/11/16) · blknotrip 4 (SKU12/13/14/15) · blk триплет 0 · SKIP-НП 0. Наших правленых строк chunk-060 в этом батче = 4 (rows 13/14/15/16, col36-only). chunk-060-fixed.xlsx — загружен СУЩЕСТВУЮЩИЙ (НЕ копировался). HURAKAN в SKU 9-16 нет (следующий SKIP-НП SKU22 б3). Бренды: Hamilton Beach ×5, GoodFood ×3 — НЕ в НП-списке.

### SKU9 — ART 1205744362 — Блендер Hamilton Beach HBH755CE — blknochg

`descUA != descRU` (604/620), col4==col5==col6==col7=`Блендер Hamilton Beach HBH755CE` language-neutral. DSCRU — настоящий русский (профессиональный/коктейлей/двухскоростной/нержавеющей). UA-marker DSCRU нет. **fixed row10 НЕ тронут.** ~soft-note НЕ нумеруется: genuine-RU артефакт `объем стакана2.0 л` (склейка без пробела) + `2.0` без запятой оставлены как есть (прецедент SKU18/38/39/85).

### SKU10 — ART 1233833423 — Блендер GoodFood PROFI BL2500, 2,5 л — blknochg

`descUA != descRU` (616/624), col4==col5==col6==col7=`Блендер GoodFood PROFI BL2500, 2,5 л` language-neutral. DSCRU — настоящий русский (профессиональный/ягодно-фруктовых/толкатель/смены ножей). UA-marker нет. **fixed row11 НЕ тронут.** genuine RU использует дефис `15 000 - 26 000` (в UA-копии em-dash) — genuine, не правится.

### SKU11 — ART 1233836827 — Блендер GoodFood PROFI BL3900, 3,9 л — blknochg

`descUA != descRU` (616/624), col4==col5==col6==col7=`Блендер GoodFood PROFI BL3900, 3,9 л` language-neutral. DSCRU — настоящий русский (тот же паттерн, что SKU10, объём 3,9 л, габариты 280х245х520). UA-marker нет. **fixed row12 НЕ тронут.**

### SKU12 — ART 1244055784 — Блендер Hamilton Beach HBF1100SCE (4 л) — blknotrip

`descUA == descRU` True (530/530), но col4==col5==col6==col7=`Блендер Hamilton Beach HBF1100SCE (4 л)` — language-neutral (бренд+код+объём, НЕ UA-leak). **Авто-фикс:** только col36 ← RU перевод DSCUA; col5 НЕ тронут. apostrophe U+0027 `об'ємом`→`объемом` снят. `Варіатор швидкості`→`Вариатор скорости`. dims `226х378х481` кириллическая х verbatim. power `2,6 кВт` verbatim. len 530→534.

### SKU13 — ART 1244067797 — Блендер Hamilton Beach HBF600CE (1,8 л) — blknotrip

`descUA == descRU` True (488/488), col4==col5==col6==col7=`Блендер Hamilton Beach HBF600CE (1,8 л)` language-neutral. **Авто-фикс:** только col36; col5 НЕ тронут. apostrophe U+0027 `об'ємом`→`объемом` снят. `виготовлений`→`изготовлен`. dims `178х229х457` кириллическая х verbatim. power `2,2 кВт` verbatim. len 488→494.

### SKU14 — ART 1864717024 — Блендер Hamilton Beach HBB255CE — blknotrip

`descUA == descRU` True (901/901), col4==col5==col6==col7=`Блендер Hamilton Beach HBB255CE` language-neutral. **Авто-фикс:** только col36; col5 НЕ тронут. entity `об&#39;ємних`→`объемных` снят. `Wave ~ Action&trade;` verbatim, `&ndash;` verbatim, `<br />` verbatim. реальные дроби UA-копии `1.6 л.с.`→`1,6 л.с.`, `вага 4.25 кг`→`вес 4,25 кг`. dims `165х203х406` кириллическая х verbatim. len 901→913.

### SKU15 — ART 1864730099 — Блендер Hamilton Beach HBB255SCE — blknotrip

`descUA == descRU` True (986/986), col4==col5==col6==col7=`Блендер Hamilton Beach HBB255SCE` language-neutral. **Авто-фикс:** только col36; col5 НЕ тронут. entity `об&#39;ємних`→`объемных` снят. `Wave ~ Action&trade;`/`&ndash;`/`<h2>`/`<p><br />` verbatim. реальные дроби UA-копии `1.6 л.с.`→`1,6 л.с.`, `вага 4.35 кг`→`вес 4,35 кг`. `склянка з нержавіючої сталі`→`стакан из нержавеющей стали`, `2 швидкості`→`2 скорости`. dims `165х203х393` кириллическая х verbatim. len 986→998.

### SKU16 — ART 2045376818 — Блендер GoodFood BL2000 SOFT — blknochg

`descUA != descRU` (2221/2197), col4==col5==col6==col7=`Блендер GoodFood BL2000 SOFT` language-neutral. DSCRU — настоящий русский (Запрограммированные режимы/Рекомендации по эксплуатации/измельчением). UA-marker нет. **fixed row17 НЕ тронут.** ~soft-note НЕ нумеруется: genuine-RU артефакты `скачать в чашу` (вместо «загрузить») и несогласованное тире `2-4`/`2&ndash;5` оставлены как есть (прецедент).

**Наблюдения по батчу SKU 9-16 (батч 2).** Блендеры, 2 бренда: Hamilton Beach ×5 (SKU9/12/13/14/15), GoodFood ×3 (SKU10/11/16) — оба НЕ в НП-списке. Паттерн: blknotrip 4 (SKU12-15 — col4==col5==col6==col7 бренд+код language-neutral, descUA==descRU UA-leak в desc → только col36 переведён tag-в-tag, col5 оставлен); blknochg 4 (SKU9/10/11/16 — descUA!=descRU, DSCRU уже настоящий русский, fixed НЕ тронут, genuine-артефакты не правятся). blk триплет 0 (ни одного UA-leak в name-полях). SKIP-НП 0 (HURAKAN нет, следующий SKU22 б3). Verbatim-токены соблюдены: `&#39;`/U+0027 апостроф снят (SKU12/13/14/15), `Wave ~ Action&trade;` (SKU14/15), `&ndash;` (SKU14/15/16), `<br />`/`<h2>`/`<p>` структура byte-точно, кириллическая х в габаритах, power `2,2/2,6 кВт` faithful; реальные дроби UA-копий `1.6 л.с.→1,6`, `4.25/4.35 кг→4,25/4,35` (blknotrip переводимые). UA→RU термины батча — в глоссарии. Открытых вопросов батч не дал. Reopen-verify: rows 13/14/15/16 col36!=col35 True, UA-marker DSCRU 0, col5==srcCol5 (language-neutral) True; blknochg rows 10/11/12/17 не тронуты (col35==src & col36==src True); prior b1 rows 3/4/5/6/9 целы (col36!=col35 True, blk col5==col7 True).

---
