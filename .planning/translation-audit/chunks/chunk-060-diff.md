# chunk-060 translation diff (81 SKU — блендеры/подрібнювачі льоду/грили контактні; W2 диапазон 055-085, продолжение chunk-059)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-060 (81 SKU)
**Apply key:** `Артикул` (scoped per row)
**Status:** IN PROGRESS 48/81 (blk триплет 9 / blknochg 17 / blknotrip 17 / SKIP-НП 5; Открытых вопросов 0)
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

## Батч 3 — SKU 17-24 (openpyxl rows 18..25)

Категории: blk триплет 5 (SKU17/18/19/20/21) · blknotrip 2 (SKU23/24) · SKIP-НП 1 (SKU22) · blknochg 0. Наших правленых строк chunk-060 в этом батче = 7 (rows 18-22 col5←col7 + col36; rows 24/25 col36-only). chunk-060-fixed.xlsx — загружен СУЩЕСТВУЮЩИЙ (НЕ копировался). Бренды: Frosty ×5 (SKU17-21), Hurakan ×1 (SKU22 SKIP-НП #2), Ceado ×2 (SKU23/24) — Frosty/Ceado НЕ в НП-списке.

### SKU17 — ART 2094281203 — Блендер Frosty FBA-010 — blk триплет
`descUA == descRU` True (703/703) UA-leak в desc; col5==col4=`Блендер Frosty FBA-010` (UA-leak), col7=`Блендер Frosty FBA-010 профессиональный` (genuine RU). **Авто-фикс:** col5←col7 (`Блендер Frosty FBA-010 профессиональный`); col36 ← полный tag-в-tag RU перевод DSCUA (h2 + p×2 + ul/li×9). entity `&#39;` снят (`м'яких`→`мягких` plain). `&ndash;` verbatim. dims `220мм x 195мм x 500мм` латинская x verbatim, `220В` verbatim. реальная дробь UA-копии `тех. дані: 1.60 кВт`→`тех. данные: 1,60 кВт`. Вес `вага: 5.50` unitless → политика A verbatim (`вес: 5.50`, точка сохранена). Family-норма (soft-note, НЕ нумер., прец. chunk-059 б12 SKU89 FROSTY FB-010): `льодоподрібнювач`→`льдокрошитель`, `перетворений на сніг`→`превращён в крошку` (canonical = genuine RU SKU22 этого же chunk). `об / хв`→`об / мин` (пробелы сохранены). len 703→709.

### SKU18 — ART 2094302011 — Блендер Frosty FBA-C280B — blk триплет
`descUA == descRU` True (710/710) UA-leak; col5==col4=`Блендер Frosty FBA-C280B`, col7=`Блендер Frosty FBA-C280B профессиональный` (genuine RU). **Авто-фикс:** col5←col7; col36 ← RU перевод (h2 + p×2 + ul/li×9). `&#39;` снят, `&ndash;` verbatim, dims латин. x verbatim. дробь `1.80 кВт`→`1,80 кВт`. Вес `Вага: 6.00`→`Вес: 6.00` политика A verbatim. Family-норма крошка/льдокрошитель (soft-note). `об/хв.`→`об/мин.`. `регулюв.`→`регулир.`. len 710→717.

### SKU19 — ART 2094309326 — Блендер Frosty FBA-2180B — blk триплет
`descUA == descRU` True (752/752) UA-leak; col5==col4=`Блендер Frosty FBA-2180B`, col7=`Блендер Frosty FBA-2180B профессиональный`. **Авто-фикс:** col5←col7; col36 ← RU перевод (h2 + p×2 + ul/li×10, +`захисний звукоізоляційний кожух`→`защитный звукоизоляционный кожух`). `&#39;` снят, `&ndash;` verbatim. дробь `2.00 кВт`→`2,00 кВт`. Вес `вага: 15.50`→`вес: 15.50` политика A verbatim. Family-норма крошка/льдокрошитель. len 752→760.

### SKU20 — ART 2094312594 — Блендер Frosty FBA-1180B — blk триплет
`descUA == descRU` True (710/710) UA-leak; col5==col4=`Блендер Frosty FBA-1180B`, col7=`Блендер Frosty FBA-1180B профессиональный`. **Авто-фикс:** col5←col7; col36 ← RU перевод (h2 + p×2 + ul/li×9). `&#39;` снят, `&ndash;` verbatim. дробь `2.00 кВт`→`2,00 кВт`. Вес `вага: 6.00`→`вес: 6.00` политика A verbatim. Family-норма крошка/льдокрошитель. len 710→717.

### SKU21 — ART 2094318196 — Блендер Frosty FBA-C280P — blk триплет
`descUA == descRU` True (710/710) UA-leak; col5==col4=`Блендер Frosty FBA-C280P`, col7=`Блендер Frosty FBA-C280P профессиональный`. **Авто-фикс:** col5←col7; col36 ← RU перевод (h2 + p×2 + ul/li×9). `&#39;` снят, `&ndash;` verbatim. дробь `1.80 кВт`→`1,80 кВт`. Вес `вага: 6.00`→`вес: 6.00` политика A verbatim. Family-норма крошка/льдокрошитель. len 710→717.

### SKU22 — ART 2111152648 — Блендер Hurakan HKN-BLW2 grey — SKIP-НП #2
**HURAKAN** в НП-списке → **SKIP-НП** (тело придёт из фида НП позже, RU не трогается). `descUA != descRU` (669/670) — у товара уже есть отдельное genuine RU-описание, но по правилу SKIP-НП НП-эксклюзивных брендов RU **не переписывается** независимо от категории. chunk-060-fixed.xlsx row 23 НЕ тронут (col35==src, col36==src, col5==src — подтверждено reopen-verify). Внесён в таблицу SKIP-НП chunk-060-MANUAL-REVIEW.md как #2. Forward-only, к обработанному не возвращаемся.

### SKU23 — ART 2135562194 — Блендер Ceado В185 — blknotrip
`descUA == descRU` True (504/504), col4==col5==col6==col7=`Блендер Ceado В185` language-neutral (бренд+код, НЕ UA-leak). **Авто-фикс:** только col36 ← RU перевод DSCUA (p + ul/li×10); col5 НЕ тронут. реальные дроби UA-копии `1.5 л`→`1,5 л`, `1.30 КВт`→`1,30 КВт` (casing `КВт` source-quirk verbatim), `4.9 кг`→`4,9 кг`. dims `195 x 180 x 470 мм` латинская x verbatim, `220В` verbatim. `нержавіючої сталі`→`нержавеющей стали`, `склянка`→`стакан`, `Леза`→`Лезвия`, `Dynamic Spin` verbatim. len 504→515.

### SKU24 — ART 2135564738 — Блендер Ceado В280 — blknotrip
`descUA == descRU` True (553/553), col4==col5==col6==col7=`Блендер Ceado В280` language-neutral. **Авто-фикс:** только col36; col5 НЕ тронут. entity `Об&#39;ємом`→`Объемом` (entity снят → plain). реальная дробь `1.70 КВт`→`1,70 КВт`, `4.9 кг`→`4,9 кг`. `1,5 л` уже запятая verbatim. dims `195 x 180 x 450 мм` латинская x verbatim. `Електронна панель керування`→`Электронная панель управления`, `об / хв`→`об / мин` (пробелы сохранены), `кришки`→`крышки`, `Dynamic Spin` verbatim. len 553→559.

**Наблюдения по батчу SKU 17-24 (батч 3).** Блендеры, 3 бренда: Frosty ×5 (SKU17-21), Hurakan ×1 (SKU22 SKIP-НП #2), Ceado ×2 (SKU23/24) — Frosty/Ceado НЕ в НП-списке. Паттерн чёткий: blk триплет 5 (Frosty FBA-* — col5==col4 UA-leak + col7 genuine RU `+ профессиональный` → col5←col7 + col36 переведён tag-в-tag); blknotrip 2 (Ceado В185/В280 — col4==col5==col6==col7 бренд+код language-neutral → только col36, col5 оставлен); SKIP-НП 1 (HURAKAN SKU22 — RU не переписан, forward-only, #2); blknochg 0. Family-норма boilerplate (soft-note НЕ нумер., прец. chunk-059 б12 SKU89 FROSTY FB-010 — тот же FROSTY-семейный текст): `льодоподрібнювач`→`льдокрошитель`, `перетворений на сніг`→`превращён в крошку` — canonical-форма подтверждена genuine RU SKU22 этого же chunk («если предварительно лед был превращен в крошку. Для этого используется льдокрошитель»). Verbatim-токены соблюдены: `&#39;`/U+0027 апостроф снят (SKU17-21/24), `&ndash;` (SKU17-21), `<h2>`/`<p>`/`<ul>`/`<li>` структура byte-точно, латинская x в габаритах, `220В`/`КВт` casing source-quirk verbatim; реальные дроби UA-копий конвертированы `1.60/1.80/2.00/1.30/1.70 → запятая`, вес unitless `5.50/6.00/15.50` политика A verbatim (точка сохранена), вес с единицей `4.9 кг→4,9 кг`. UA→RU термины батча — в глоссарии (+8 net-new). Открытых вопросов батч не дал (рассинхрона модель-кода NAME UA↔genuine-RU и чужих продуктов в name-полях нет; col7 `+ профессиональный` — корректное RU-обогащение, NAZVUA/NAZVRU согласованы). Reopen-verify: rows 18-22 col36!=col35 True, UA-marker DSCRU 0, col5==col7(genuineRU) True, col5 UA-marker 0; rows 24/25 col36!=col35 True, UA-marker DSCRU 0, col5==srcCol5 (не тронут) True; SKIP row 23 col35==src & col36==src & col5==src True; prior b1+b2 rows 3/4/5/6/9/13/14/15/16 целы (col36!=col35 True, UA-marker DSCRU 0).

---

## Батч 4 — SKU 25-32 (openpyxl rows 26..33)

Блендеры. 4 бренда: Hamilton Beach ×2 (SKU25/26), GoodFood ×2 (SKU27/28), Bartscher ×1 (SKU29), Hurakan ×2 (SKU30/31 SKIP-НП #3/#4), SARO ×1 (SKU32). Категории: blknotrip 3 (SKU25/26/29 — col4==col5==col6==col7 бренд+код language-neutral + descUA==descRU UA-leak → только col36, col5 оставлен); blknochg 3 (SKU27/28/32 — descUA!=descRU, genuine отдельное RU уже есть → fixed НЕ тронут); SKIP-НП 2 (Hurakan SKU30 #3 + SKU31 #4 — RU не переписан, forward-only). blk триплет 0.

### SKU25 — ART 2150769520 — Блендер Hamilton Beach HBF600SCE — blknotrip
`descUA == descRU` True (719/719), col4==col5==col6==col7=`Блендер Hamilton Beach HBF600SCE` language-neutral (бренд+код, НЕ UA-leak). **Авто-фикс:** только col36 ← RU перевод DSCUA (p×2 + ul/li×18); col5 НЕ тронут. `&#39;` снят (`м&#39;яких`→`мягких`, `Об&#39;єм`→`Объем`). Мощность с единицей `кВт: 0.75`→`кВт: 0,75` (запятая). Вес без единицы `Вага 6.5`→`Вес 6.5` политика A verbatim (точка сохранена). `Вага (нетто), кг: 6` — целое, без дроби. `220V` language-neutral verbatim. `нержавіючої сталі`→`нержавеющей стали`. len 719→717.

### SKU26 — ART 2150784658 — Блендер Hamilton Beach HBH455CE — blknotrip
`descUA == descRU` True (668/668), col4==col5==col6==col7=`Блендер Hamilton Beach HBH455CE` language-neutral. **Авто-фикс:** только col36; col5 НЕ тронут. `Об&#39;ємом`→`объемом` (entity снят). дробь `1,4 л` уже запятая verbatim. Вес с единицей `кг: 4.8`→`кг: 4,8`, мощность `кВт: 1.8`→`кВт: 1,8` (запятая). Вес без единицы `Вага 5.3`→`Вес 5.3` политика A verbatim. `220V` verbatim. len 668→653.

### SKU27 — ART 2363057312 — Блендер GoodFood BL1500 — blknochg
`descUA != descRU` (1120/1138) — у товара уже есть отдельное genuine RU-описание (clean, UA-marker 0; `Мощный стационарный блендер идеально подходит … детского питания.` + тех.хар. h3/ul/li). Категория **blknochg**: chunk-060-fixed.xlsx row 28 НЕ тронут (col35==src, col36==src, col5==src). col4==col5==col6==col7=`Блендер GoodFood BL1500` language-neutral. Этот genuine RU служит canonical lead-абзацем для SKU29 Bartscher (тот же стац-блендер boilerplate).

### SKU28 — ART 2363063339 — Блендер GoodFood BL1500 COVER — blknochg
`descUA != descRU` (1285/1305) — genuine отдельное RU уже есть (clean, +абзац про звукопоглощающий бокс/кожух). Категория **blknochg**: row 29 НЕ тронут. col4==col5==col6==col7 language-neutral.

### SKU29 — ART 2464197796 — Блендер Bartscher 150182 — blknotrip
`descUA == descRU` True (891/891), col4==col5==col6==col7=`Блендер Bartscher 150182` language-neutral. **Авто-фикс:** только col36 ← RU перевод (p + h3 + ul/li×14 + p + ul/li×4); col5 НЕ тронут. Lead-абзац `Потужний стаціонарний блендер …` переведён по **canonical genuine RU SKU27** этого же chunk (`Мощный стационарный блендер идеально подходит для приготовления смузи, муссов … детского питания.`) — family-норма стац-блендер boilerplate. `Об&#39;єм`→`Объем` (entity снят), дробь `2,875 л` уже запятая verbatim. Вес с единицей `кг: 9.08`→`кг: 9,08`, мощность `кВт: 1.68`→`кВт: 1,68` (запятая). Вес без единицы `Вага 10`→`Вес 10` (целое). `об/хв`→`об/мин`, `Швидкість обертання`→`Скорость вращения`, `Країна виробник: Німеччина`→`Страна производитель: Германия`, `Ніж 6-лопатевий`→`Нож 6-лопастной`. `220V` verbatim. len 891→899.

### SKU30 — ART 2503647283 — Блендер Hurakan HKN-HBH2000S — SKIP-НП #3
**HURAKAN** в НП-списке → **SKIP-НП** (тело придёт из фида НП позже, RU не трогается). `descUA == descRU` True (511/511). chunk-060-fixed.xlsx row 31 НЕ тронут (col35==src, col36==src, col5==src — reopen-verify). Внесён в таблицу SKIP-НП chunk-060-MANUAL-REVIEW.md как #3. Forward-only.

### SKU31 — ART 2503651061 — Блендер Hurakan HKN-HBH2000STH з шумопоглинаючим покриттям — SKIP-НП #4
**HURAKAN** в НП-списке → **SKIP-НП**. `descUA == descRU` True (547/547); NAZVRU(col7)=`Блендер Hurakan HKN-HBH2000STH с шумопоглощающим покрытием` (частичный RU в col7), но по правилу SKIP-НП НП-эксклюзивных брендов RU **не переписывается** независимо. row 32 НЕ тронут (col35==src, col36==src, col5==src). Внесён в таблицу SKIP-НП как #4. Forward-only.

### SKU32 — ART 2538743961 — Блендер SARO TM-800 Black — blknochg
`descUA != descRU` (609/871) — у товара есть отдельное genuine RU-описание (русский текст clean, UA-marker 0), но обёрнуто в **Google-Translate-виджет артефакт**: `<p aria-label="Перекладений текст: …" data-placeholder="Переклад" data-ved="…" dir="ltr" id="tw-target-text">` + `<p dir="ltr">`. Категория **blknochg**: артефакт-разметка НЕ переписывается и НЕ нумеруется как Открытый вопрос (прец. SKU18/38/39/85 — артефакты/опечатки в genuine RU не правим), chunk-060-fixed.xlsx row 33 НЕ тронут (col35==src, col36==src, col5==src — reopen-verify). col4==col5==col6==col7=`Блендер SARO TM-800 Black` language-neutral. _Наблюдение для Yana (не блокер): RU-контент корректен, но в HTML-атрибутах остался мусор GT-виджета — на усмотрение при ручной вычитке._

**Наблюдения по батчу SKU 25-32 (батч 4).** Все 8 — блендеры. Паттерн: blknotrip 3 (Hamilton Beach SKU25/26, Bartscher SKU29 — col4==col5==col6==col7 бренд+код language-neutral + descUA==descRU UA-leak → только col36, col5 оставлен); blknochg 3 (GoodFood SKU27/28, SARO SKU32 — descUA!=descRU, genuine отдельное RU → fixed НЕ тронут; SKU32 genuine RU обёрнут в GT-виджет-артефакт, не правим/не нумеруем); SKIP-НП 2 (Hurakan SKU30 #3 + SKU31 #4 — forward-only). blk триплет 0. Family-норма стац-блендер boilerplate: lead-абзац `Потужний стаціонарний блендер …` для SKU29 Bartscher переведён по canonical genuine RU SKU27 GoodFood BL1500 этого же chunk (тот же стац-блендер семейный текст). Verbatim соблюдён: `&#39;`/U+0027 апостроф снят (SKU25/26/29), `<p>`/`<h3>`/`<ul>`/`<li>` byte-точно, `220V` language-neutral verbatim; реальные дроби UA-копий с единицей конвертированы (`кВт: 0.75/1.8/1.68`→запятая, `кг: 4.8/9.08`→запятая), дроби уже-запятая verbatim (`1,4 л`/`2,875 л`), вес без единицы политика A verbatim (`Вага 6.5/5.3`→`Вес 6.5/5.3` точка сохранена, целые `6`/`10` без дроби). UA→RU термины батча — в глоссарии (новые + зеркало). Открытых вопросов батч не дал (рассинхрона модель-кода NAME UA↔RU и чужих продуктов в name-полях нет; SKU32 GT-артефакт — soft-наблюдение, не нумерованный OQ). Reopen-verify: blknotrip rows 26/27/30 col36!=col35 True, UA-marker DSCRU 0, col5==srcCol5 (не тронут) True, col35==src True (len 719→717/668→653/891→899); SKIP rows 31/32 col35==src & col36==src & col5==src True; blknochg rows 28/29/33 col35==src & col36==src & col5==src True; prior b1+b2+b3 rows 3/4/5/6/9/13/14/15/16/18/19/20/21/22/24/25 целы (col36!=col35 True, UA-marker DSCRU 0).

---

## Батч 5 — SKU 33-40 (openpyxl rows 34..41)

Блендеры. 4 бренда: Hamilton Beach ×5 (SKU34/35/38/39/40), SIRMAN ×1 (SKU36), Fimar ×1 (SKU37), Hurakan ×1 (SKU33 SKIP-НП #5). Категории: blknotrip 2 (SKU35/37 — col4==col5==col6==col7 бренд+код language-neutral + descUA==descRU UA-leak → только col36, col5 оставлен); blknochg 5 (SKU34/36/38/39/40 — descUA!=descRU, genuine отдельное RU уже есть → fixed НЕ тронут); SKIP-НП 1 (Hurakan SKU33 #5 — RU не переписан, forward-only). blk триплет 0. Наших правленых строк chunk-060 в этом батче = 2 (rows 36/38, col36-only). chunk-060-fixed.xlsx — загружен СУЩЕСТВУЮЩИЙ (НЕ копировался).

### SKU33 — ART 2566515692 — Блендер Hurakan HKN-HBH850M PRO — SKIP-НП #5
**HURAKAN** в НП-списке → **SKIP-НП** (тело придёт из фида НП позже, RU не трогается). `descUA == descRU` True (701/701). chunk-060-fixed.xlsx row 34 НЕ тронут (col35==src, col36==src, col5==src — reopen-verify). Внесён в таблицу SKIP-НП chunk-060-MANUAL-REVIEW.md как #5. Forward-only, к обработанному не возвращаемся.

### SKU34 — ART 2643094350 — Блендер Hamilton Beach HBB255CE УЦІНКА — blknochg
`descUA != descRU` (452/412) — у товара есть отдельное genuine RU-описание (clean, UA-marker 0; `объем стакана 1,4 л / 2 скорости / корпус - пластик / …`). NAME-поля: col4==col6=`…HBB255CE УЦІНКА` (UA), col5==col7=`…HBB255CE УЦЕНКА` (RU) — `УЦІНКА`→`УЦЕНКА` согласованный перевод суффикса уценки, **НЕ рассинхрон модель-кода**. Категория **blknochg**: row 35 НЕ тронут. ~soft-note НЕ нумер.: порядок пунктов в genuine RU отличается от UA-порядка (`объем стакана` первым) — genuine, не правится (прец. SKU18/38/39/85).

### SKU35 — ART 2558262837 — Блендер Hamilton Beach HBF500SCE — blknotrip
`descUA == descRU` True (715/715), col4==col5==col6==col7=`Блендер Hamilton Beach HBF500SCE` language-neutral (бренд+код, НЕ UA-leak). **Авто-фикс:** только col36 ← RU перевод DSCUA (p×2 + ul/li×12 + p + ul/li×4); col5 НЕ тронут. `&#39;` снят (`м&#39;яких`→`мягких`, `об&#39;ємом`→`объемом`). Lead-абзац стац-блендер boilerplate по canonical (`…используется для приготовления коктейлей, смузи и супов-пюре из мягких овощей.`). Мощность с единицей `кВт: 0.74`→`кВт: 0,74` (запятая). Вес без единицы `Вага 6.2`→`Вес 6.2` политика A verbatim (точка сохранена). `Вага (нетто), кг: 6` — целое, без дроби. `220V` language-neutral verbatim. `Металічне щеплення`→`Металлическое сцепление`, `Варіатор швидкості`→`Вариатор скорости`. Идентичные RU-фрагменты (`Ширина (нетто), мм: 230`, `Ширина 700`) не трогались. len 715→706.

### SKU36 — ART 1205290053 — Блендер SIRMAN ORIONE FIVE VV — blknochg
`descUA != descRU` (933/939) — у товара уже есть отдельное genuine RU-описание (clean, UA-marker 0; `Блендер профессиональный SIRMAN ORIONE FIVE VV используется для взбивания соусов, муссов … рентабельность.` + ul/li×13). col4==col5==col6==col7=`Блендер SIRMAN ORIONE FIVE VV` language-neutral. Категория **blknochg**: row 37 НЕ тронут.

### SKU37 — ART 477582204 — Блендер Fimar FR150I — blknotrip
`descUA == descRU` True (393/393), col4==col5==col6==col7=`Блендер Fimar FR150I` language-neutral. **Авто-фикс:** только col36 ← RU перевод DSCUA (h2 + ul/li×8); col5 НЕ тронут. apostrophe U+0027 `об'ємом`→`объемом` снят; `літра`→`литра` (дробь `1,5` уже запятая verbatim). Мощность `0,35 кВт` уже запятая faithful verbatim. dims `210х490` кириллическая х verbatim. `пофарбований корпус`→`окрашенный корпус`, `чотирилопатевий знімний ніж`→`четырехлопастной съемный нож`, `корок на кришці`→`пробка на крышке`, `мікровимикач`→`микровыключатель`. `</ul> <p> </p>` структура byte-точно. len 393→396.

### SKU38 — ART 477605336 — Блендер Hamilton Beach HBH 850 CE — blknochg
`descUA != descRU` (400/403) — genuine отдельное RU уже есть (clean, UA-marker 0; `Блендер Hamilton Beach HBH 850 CE объемом 1,8 литра.` + ul/li×10). col4==col5==col6==col7=`Блендер Hamilton Beach HBH 850 CE` language-neutral. Категория **blknochg**: row 39 НЕ тронут.

### SKU39 — ART 635596863 — Блендер Hamilton Beach HBH450CE — blknochg
`descUA != descRU` (547/563) — genuine отдельное RU уже есть (русский clean, система `Wave ~ Action &trade;`). col4==col5==col6==col7=`Блендер Hamilton Beach HBH450CE` language-neutral. Категория **blknochg**: row 40 НЕ тронут. ~soft-note НЕ нумер. (прец. SKU18/38/39/85): genuine-RU артефакты — склейка `HBH 450 CEс` (код+«с») и dims `165хх229хх432` (двойная х) оставлены как есть.

### SKU40 — ART 635596864 — Блендер Hamilton Beach HBH550CE — blknochg
`descUA != descRU` (509/525) — genuine отдельное RU уже есть (русский clean, `Wave ~ Action &trade;`). col4==col5==col6==col7=`Блендер Hamilton Beach HBH550CE` language-neutral. Категория **blknochg**: row 41 НЕ тронут. ~soft-note НЕ нумер. (прец.): те же артефакты `HBH 550 CEс` / dims `178хх230хх457` (двойная х) оставлены как есть.

**Наблюдения по батчу SKU 33-40 (батч 5).** Все 8 — блендеры. 4 бренда: Hamilton Beach ×5 (SKU34/35/38/39/40), SIRMAN ×1 (SKU36), Fimar ×1 (SKU37), Hurakan ×1 (SKU33 SKIP-НП #5). Паттерн: blknotrip 2 (Hamilton Beach SKU35, Fimar SKU37 — col4==col5==col6==col7 бренд+код language-neutral + descUA==descRU UA-leak → только col36 переведён tag-в-tag, col5 оставлен); blknochg 5 (SKU34 Hamilton Beach УЦЕНКА, SKU36 SIRMAN, SKU38/39/40 Hamilton Beach — descUA!=descRU, genuine отдельное RU clean → fixed НЕ тронут); SKIP-НП 1 (Hurakan SKU33 #5 — forward-only). blk триплет 0. Family-норма стац-блендер boilerplate: lead-абзац SKU35 переведён по canonical (`…используется для приготовления коктейлей, смузи и супов-пюре из мягких овощей.`, та же форма что SKU33 family / прец. b4 SKU27/29). Verbatim соблюдён: `&#39;`/U+0027 апостроф снят (SKU35/37), `<h2>`/`<p>`/`<ul>`/`<li>` byte-точно, кириллическая х в `210х490` (SKU37) verbatim, `220V` language-neutral verbatim; мощность с единицей `кВт: 0.74`→`кВт: 0,74` (SKU35), мощность уже-запятая `0,35 кВт` faithful (SKU37), вес без единицы политика A verbatim (`Вага 6.2`→`Вес 6.2` точка сохранена, целое `6` без дроби, SKU35); идентичные RU-фрагменты (`Ширина (нетто), мм: 230`, `Ширина 700` SKU35) не трогались. Открытых вопросов батч не дал (рассинхрона модель-кода NAME UA↔genuine-RU и чужих продуктов в name-полях нет; SKU34 `УЦІНКА`/`УЦЕНКА` — согласованный перевод суффикса уценки, не рассинхрон; SKU39/40 genuine-RU артефакты `CEс`/двойная х — soft-note прец., не нумерованный OQ). Reopen-verify: blknotrip rows 36/38 col36!=col35 True, UA-marker DSCRU 0, col5==srcCol5 (не тронут) True, col35==src True (len 715→706 / 393→396); SKIP row 34 col35==src & col36==src & col5==src True; blknochg rows 35/37/39/40/41 col35==src & col36==src & col5==src True; prior b1-b4 rows 3/4/5/6/9/13/14/15/16/18/19/20/21/22/24/25/26/27/30 целы (col36!=col35 True, UA-marker DSCRU 0).

---

## Батч 6 — SKU 41-48 (openpyxl rows 42..49)

Все 8 — блендеры (SKU48 — подрібнювач льоду / льдокрошитель). Бренды: Hamilton Beach ×3 (SKU41/43/47), Fimar ×2 (SKU44/45), Vema ×1 (SKU42), CEADO ×1 (SKU46), AIRHOT ×1 (SKU48). НП-брендов в диапазоне нет (CEADO/AIRHOT НЕ в НП-списке; ближайший HURAKAN — SKU49 #6 в б7).

### SKU41 — ART 851140491 — Блендер Hamilton Beach HBH750CE Eclipse — blknochg
`descUA != descRU` (454/472) — genuine отдельное RU уже есть (clean, UA-marker 0; `Блендер профессиональный Hamilton Beach HBH 750 CE Eclipse производительностью от 75 коктейлей в день.` + ul/li×8). col4==col5==col6==col7=`Блендер Hamilton Beach HBH750CE Eclipse` language-neutral. Категория **blknochg**: row 42 НЕ тронут.

### SKU42 — ART 921248925 — Блендер Vema FR2055 — blknochg
`descUA != descRU` (597/606) — genuine отдельное RU уже есть (clean, UA-marker 0; `Блендер профессиональный Vema FR2055 для приготовления соусов…` + p + ul/li×6). col4==col5==col6==col7 НЕ выполняется: NMRU/NAZVRU=`Блендер Vema FR2055 профессиональный` vs NMUA/NAZVUA=`Блендер Vema FR2055`. ~soft-note НЕ нумер.: RU добавляет описательный суффикс «профессиональный» — genuine RU-вариант (та же модель FR2055, не рассинхрон модель-кода; прец. SKU34 `УЦІНКА`→`УЦЕНКА` согласованный дескриптор). Категория **blknochg**: row 43 НЕ тронут.

### SKU43 — ART 1244062721 — Блендер Hamilton Beach HBF500CE — blknotrip
`descUA == descRU` True (490/490), col4==col5==col6==col7=`Блендер Hamilton Beach HBF500CE (1,4 л)` language-neutral. **Авто-фикс:** только col36 ← RU перевод DSCUA (h2 + p + ul/li×9); col5 НЕ тронут. apostrophe U+0027 `об'ємом`→`объемом` снят; `1,4 літра`→`1,4 литра`; мощность `0,74 кВт` уже запятая faithful verbatim; dims `178х229х483` кириллическая х verbatim. `Знімний дозатор`→`Съемный дозатор`, `Датчик встановлення стакана`→`Датчик установки стакана`, `Гумові наконечники на ніжках`→`Резиновые наконечники на ножках`, `ніжки-опори запобігають ковзанню`→`ножки-опоры предотвращают скольжение`. len 490→495.

### SKU44 — ART 1449237425 — Блендер Fimar Easy Line BL008 — blknochg
`descUA != descRU` (355/360) — genuine отдельное RU уже есть (clean, UA-marker 0; `Блендер Fimar Easy Line BL008 объемом 2 литра.` + ul/li×8). col4==col5==col6==col7=`Блендер Fimar Easy Line BL008` language-neutral. Категория **blknochg**: row 45 НЕ тронут.

### SKU45 — ART 1501504635 — Блендер Fimar Easy Line BL020B — blknotrip
`descUA == descRU` True (374/374), col4==col5==col6==col7=`Блендер Fimar Easy Line BL020B` language-neutral. **Авто-фикс:** только col36 ← RU перевод DSCUA (h2 + ul/li×8); col5 НЕ тронут. entity `об&#39;ємом`→`объемом` снят; dims `220х190х490` кириллическая х verbatim; `1,5 кВт` уже запятая faithful; `кнопка "pulse"` латиница в кавычках verbatim; `пульсовий режим`→`пульсовый режим`, `аварійний мікровимикач`→`аварийный микровыключатель` (b1 вариант), `швидкість 28000 об/хв`→`скорость 28000 об/мин`. len 374→371.

### SKU46 — ART 2054740600 — Блендер CEADO B285 — blknotrip
`descUA == descRU` True (514/514), col4==col5==col6==col7=`Блендер CEADO B285` language-neutral. CEADO **НЕ** в НП-списке → обрабатывается обычно. **Авто-фикс:** только col36 ← RU перевод DSCUA (p + ul/li×8); col5 НЕ тронут. entity `Об&#39;ємом`→`Объемом` снят; `220 В` напряжение verbatim; вес с единицей `Вага 8,8 кг`→`Вес 8,8 кг` уже запятая faithful; dims `195х220х485` кириллическая х verbatim; `<li> </li>` whitespace-only идентичен — не тронут. ~soft-note: `льодяником`→`льдокрошителем` (семантика «измельчитель льда»; genuine-RU SKU42 использует «льдокрошителем»). `Кількість чаш`→`Количество чаш`, `Матеріал чаші`→`Материал чаши`, `панель керування`→`панель управления`. len 514→522.

### SKU47 — ART 2364410519 — Блендер Hamilton Beach HBH855CE — blknotrip
`descUA == descRU` True (837/837), col4==col5==col6==col7=`Блендер Hamilton Beach HBH855CE` language-neutral. **Авто-фикс:** только col36 ← RU перевод DSCUA (p + h3 + ul/li×17, из них 2 пропущены как идентичные RU); col5 НЕ тронут. ~soft-note: мощность с единицей UA-копия `кВт: 2.2`→`кВт: 2,2` точка→запятая (прец. b5 SKU35 `кВт: 0,74`); вес целое `кг: 13` без изменения, `Вага 9`→`Вес 9` без единицы политика A (целое, только метка); идентичные RU-фрагменты `<li>Ширина (нетто), мм: 312</li>` и `<li>Ширина 400</li>` не трогались (нет UA-маркера, уже валидный RU — прец. b5 SKU35 `Ширина 700`); `220V` verbatim; `Висота`→`Высота` / `Глибина`→`Глубина` (и→ы, UA-написание переведено). `Звуковбирний кожух`→`Звукопоглощающий кожух`, `Країна виробник`→`Страна производитель`, `Розміри в упаковці`→`Размеры в упаковке` (b5). len 837→846.

### SKU48 — ART 1033489145 — Подрібнювач льоду AIRHOT IC-1 → Льдокрошитель AIRHOT IC-1 — blk триплет
`descUA == descRU` True (253/253), col5==col4=`Подрібнювач льоду AIRHOT IC-1` (UA-leak в NAME), col7 (NAZVRU)=`Льдокрошитель AIRHOT IC-1` genuine RU → **blk триплет**. AIRHOT **НЕ** в НП-списке → обрабатывается обычно. **Авто-фикс:** col5 ← col7 `Льдокрошитель AIRHOT IC-1`; col36 ← полный RU перевод DSCUA (lead plain-text без тега + ul/li×6); col35 НЕ тронут. `Льодокрошувач`→`Льдокрошитель`, `Подрібнює лід до стану "сніга"`→`Измельчает лед до состояния "снега"`, `продуктивність … кг/год`→`производительность … кг/час`, `неіржавка сталь`→`нержавеющая сталь`. `корпус — сталь` идентичен RU/UA (нет UA-маркера, em-dash verbatim) — не тронут; dims `420х200х105` кириллическая х verbatim; `вага 5 кг`→`вес 5 кг` (целое с единицей). len 253→266.

**Наблюдения по батчу SKU 41-48 (батч 6).** blknochg 3 (SKU41/42/44 — descUA!=descRU, genuine отдельное RU clean → fixed НЕ тронут; SKU42 ~soft-note NMRU суффикс «профессиональный»); blknotrip 4 (SKU43/45/46/47 — col4==col5==col6==col7 language-neutral + descUA==descRU UA-leak → только col36 tag-в-tag, col5 оставлен); blk триплет 1 (SKU48 — col5==col4 UA-leak + col7 genuine RU `Льдокрошитель` → col5←col7 + col36 полный RU); SKIP-НП 0. Verbatim соблюдён: `&#39;`/U+0027 апостроф снят (SKU43/45/46), `<h2>`/`<p>`/`<h3>`/`<ul>`/`<li>` byte-точно, кириллическая х в dims verbatim (SKU43/45/46/47/48), `220V`/`220 В` напряжение verbatim, em-dash `—` verbatim (SKU48); мощность с единицей UA-копия `кВт: 2.2`→`кВт: 2,2` (SKU47), уже-запятая `0,74`/`1,5`/`0,3` кВт faithful; вес с единицей уже-запятая `8,8 кг` faithful, целое `кг: 13`/`Вага 9`/`5 кг` без дроби; идентичные RU-фрагменты (`Ширина (нетто), мм: 312`, `Ширина 400` SKU47; `корпус — сталь` SKU48; `<li> </li>` SKU46) не трогались. Открытых вопросов батч не дал (рассинхрона модель-кода NAME UA↔genuine-RU и чужих продуктов нет; SKU42 NMRU суффикс «профессиональный» — согласованный дескриптор genuine RU, не рассинхрон, прец. SKU34; SKU48 UA-leak в col5 → штатный blk триплет, не OQ). Reopen-verify: blknotrip rows 44/46/47/48 col36!=col35 True, UA-marker DSCRU 0, col5==srcCol5 (не тронут) True, col35==src True; blk триплет row 49 col36!=col35 True, UA-marker col36 0, col5==col7 (`Льдокрошитель AIRHOT IC-1`) True, UA-marker col5 0, col35==src True; blknochg rows 42/43/45 col35==src & col36==src & col5==src True; prior b1-b5 rows 3/4/5/6/9/13/14/15/16/18/19/20/21/22/24/25/26/27/30/36/38 целы (col36!=col35 True, UA-marker DSCRU 0).

---
