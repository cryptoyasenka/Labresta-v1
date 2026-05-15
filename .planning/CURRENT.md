# CURRENT — labresta-sync (Flask supplier sync app)

**Last touched:** 2026-05-16 — **chunk-011 IN PROGRESS 32/85** (batch SKU 25-32 `b8b6450`; prev batches 1-8 `13e4c00`/9-16 `1b7807a`/17-24 `9e0a308`; CURRENT 32/85 — этот коммит). chunk-011 = 85 SKU фритюрницы, Ефес-доминанта (52); diff+MR — зеркало chunk-010 headers (формат-классы A/B/C globally-closed, F per-SKU; locked-правила). SKU 1-8: Unox решётки GRP705/711/806 (1-3) 🔴 RU=UA full translate + Назв.мод (RU) UA-leak `Решітка`→`Решетка` + decimals 0,59/8,5/0,3/0,8 (SKU 3 `дека`→`противня`/`НЕМА`→`НЕТ`); Ефес ШПЕ-1 (4) не 🔴, decimal 6,72 UA+RU + RU `<style>` MSO-артефакт удалён (AUTO+откат-нота), 380 В faithful; Ефес тепловой-Д 600*1100/1200/1300/1400 (5-8) — без правок (RU самостоятелен), soft note SKU 5/6 (RU без UA-строки «Можливість вертикального приготування»). SKU 9-16: Ефес тепловой-Д 600*1500/1600/1700/1800 + 700*1100/1200/1300/1400 (Артикул 2075052706/2075061709/2075067407/2075080939/2075087566/2075090995/2075093593/2075096543) — вся серия без правок (RU самостоятельный корректный перевод, не 🔴, decimals нет, Назв./Назв.мод (RU) корректны, 220 В faithful, UA↔RU симметричны). Soft note (батч-ур.): дрейф пунктуации/регистра спец-строк SKU 9-10 (`Температурний режим &deg;C`/`…нержавіюча сталь`) vs 11-16 (`Температурний режим, &deg;C`/`…, Нержавіюча сталь`) — внутри строки UA↔RU симметрично, faithful; серия тепловой-Д 5-16 — строка «Можливість вертикального приготування» только в UA 5/6 (асимметрия источника, решение за Yana). SKU 17-24: Ефес тепловой-Д 700*1500/1600/1700/1800 + 800*1100/1200/1300/1400 (Артикул 2075098239/2075100842/2075102975/2075104011/2075104949/2075107012/2075107733/2075108466) — вся серия без правок (RU самостоятельный корректный перевод, не 🔴, decimals/Назв.мод UA-leak нет, 220 В faithful, UA↔RU симметричны); формат спец-строк единообразен (с запятой/заглавная — как SKU 11-16, дрейфа внутри батча нет); серия 5-24 «Можливість» по-прежнему только UA 5/6 (рекуррентно). SKU 25-32: серия разветвилась — 25-28 тепловой-Д 800*1500/1600/1700/1800 (2075110613/2075111305/2075112900/2075114112), 29-32 новая суб-серия тепловой-С 600*1000/1100/1200/1300 (2075120127/2075127028/2075127138/2075127691; рабочая поверхность+шкаф, мощность-диапазон `1…2`, без объёма). Язык RU везде корректен, авто-правок нет (🔴/Назв.мод UA-leak/реальных дробей нет). 🔶 Числовые расхождения источника (числа НЕ трогаю, locked, soft notes в MR): SKU 27 UA-ширина 1600≠1700 (RU верен), SKU 28 UA-мощность 2.00≠3 (RU консистентен серии; `.00` целочисл.артефакт, не дробь), SKU 31 RU-ширина 1100≠1200 (customer-facing RU-ошибка, решение по источнику за Yana). UA META-ярлык `тепловий-Д` на товарах -С (SKU 29-32) — рекуррентный рассинхрон, META faithful. Напряжение/META faithful. Открытых вопросов chunk-011 нет. — chunk-010 ✅ COMPLETE 74/74 — ЗАКРЫТ (close `4817211`; prev `39ec108`/`9ebddd3`/`b0f8fb2`/`6af012a`/`f74b417`/`caa65e4`/`ae27913`/`e673b0c`/`13de4a6`/`57bf021`/`1ccb456`; scaffold `6b464b0`). chunk-009 ✅ COMPLETE 75/75 (`73c666a`/`7884e65`) — закрыт; открытый Q1 (SKU 24 Beckers FB 6 LT/LTA) + soft-note SKU 60 Silver 2704 `25`/`2,5` кВт ждут Yana, НЕ блокируют. **chunk-010** = 74 SKU фритюрницы, ATA-доминанта; diff+MR — зеркало chunk-009 headers (формат-классы A/B/C globally-closed, F per-SKU). SKU 1-16: Bartscher/FROSTY/Hurakan/Hendi 🔴 RU=UA + Назв.мод UA-leak + decimals; GGM/Mars чисты; Saro/Ozti RU `квт`→`кВт`+`НАСТРОЙНОЕ`→`НАСТОЛЬНОЕ`. SKU 17-46 (сплошной ATA): ATA `кВт` корректен; рекуррентный ATA-газ RU-артефакт `&brvbar;Газовый`→`Газовый` (SKU 21/22 + все 25-38 газ, AUTO; электр. SKU 39-48 — `&brvbar;` нет); SKU 30 RU `2 емкостные`→`2 емкости`, SKU 39 RU `Электрическая мощность, 8000`→`…, Вт 8000`, SKU 44 RU модель-код тела `K7EFE1015`→`K7EFG0515` (5:1 sibling-единогласн. AUTO); decimal SKU 18 `18,1`/25 `11,5`/35 `11,5`/40 `36,2`/45 `17,4` (UA+RU); SKU 20 + SKU 42 F-класс (UA `<br/>`-склейка `<li>`→раздельные, зеркало RU). SKU 47 GAM (нов.бренд): RU `Выполена`→`Выполнена` + `190°C.Верхний`→`…. Верхний` AUTO; soft note Назв.(RU) без «4+4 л» + UA `Виготовлений` (согласование). SKU 48 Kogast (нов.бренд): 🔴 RU=UA full translate + Назв.мод RU UA-leak → Название(RU). SKU 49-56 (смеш. бренды): 🔴 RU=UA full translate в 49 Bertos/50 Kogast/52 Frosty FE8L/53 REEDNEE/56 REEDNEE-СВЧ (+Назв.мод RU UA-leak); decimal `9,20` SKU 51/52 Frosty (UA+RU); SKU 54/55 GoodFood — без правок. SKU 57-64 (все 8 — печи СВЧ/микроволновки в чанке фритюрниц, обработ. по факту): 🔴 RU=UA full translate в 57 Bartscher/58 Scan/59 Bartscher/60 REEDNEE/61 Fimar/63 Hendi/64 Hendi (+Назв.мод RU UA-leak; 60/61 `Піч НВЧ`→`Печь СВЧ`, 61 +дескриптор, 63 +«без тарелки»); SKU 62 BEKO — без правок (RU корректен). SKU 65-72 (65-70 СВЧ, 71 Pansystem противень, 72 Unox противень-решётка): 🔴 RU=UA full translate в 65/66/67/69/70/71/72 (+Назв.мод RU UA-leak; 66 +«промышленная», 69 CAPS, 71/72 `Деко`→`Противень`); SKU 68 Saro — самост. RU (не 🔴): decimal `1,4`(UA+RU)+RU `0,9кВт`→`0,9 кВт`; decimal `0,771` SKU 72 (UA+RU). SKU 73-74 (финал, Unox bakeware): 🔴 RU=UA full translate в обоих + Назв.мод RU UA-leak (73 `Решітка`→`Решетка`, 74 `Деко`→`Противень`); decimal SKU 73 `0,7`, SKU 74 `1,2`/`1,21` (UA+RU). 🔴 RU=UA: SKU 1-6, 48-50, 52-53, 56-61, 63-67, 69-74. Open questions — нет. `380-400V`/`220-230V`/`220 В`/`380 В`/газ диапазоны faithful. Soft notes (накопл.): SKU3 «ел.наст.» Назв.(UA), SKU6 UA-артефакты, SKU7 UA `градусов`, SKU9 «без електрична»+Mars запятая, SKU10-16 UA `квт`+Ozti `<br/>` в `<p>`, SKU17 UA `НАПОЛЬНЕ` русизм, SKU18-46 ATA UA русизмы `сбору`/`корзина`, SKU30 UA `ємністі`, SKU35/37 UA `упраління`, SKU47 GAM Назв.(RU)/`Виготовлений`, SKU53 UA `Отбрасываемая`/`управління` микс, SKU56 UA `5 степеней мощности`, SKU57 UA `Гастільна`(вероятно `Настільна`), SKU58 UA `Напруга 1000 Вт` mislabel, SKU62 источник `2450 Гц`(вероятно МГц), SKU63 UA `Мікрохвольова` опечатка. Открытых вопросов chunk-010 нет. **NEXT: chunk-011 SKU 33-40** → `cd /c/Projects/labresta-sync && .venv/Scripts/python.exe scripts/_dump_batch.py 011 33 40` → Read `.planning/scratch_skubatch.txt` → аудит ~8 SKU по locked-правилам → append chunk-011-diff.md (Status→`IN PROGRESS 40/85`, блоки перед финальным `---`; tail-anchor = последний `*(scoped к row Артикул=2075127691)*` + `---`) + chunk-011-MANUAL-REVIEW.md (Status→`IN PROGRESS 40/85`, `## Батч SKU 33-40` перед `## Открытые вопросы chunk-011`, обновить `**Last updated:**`) → `git add` 2 файла + `git -c commit.gpgsign=false commit -q` + `git push -q` → CURRENT.md line 3 sync (+commit+push) → dump следующий батч, loop ~8 SKU/batch до 85/85 → закрыть chunk-011 (Status→COMPLETE 85/85 + секция закрытия в diff+MR) → chunk-012 (зеркало chunk-011 scaffold)… SKIP chunk-001 навсегда. Ночной режим: неоднозначность → soft note (рус.) в MR, НЕ блокировать. НЕ эмитить `AUTO_CONTINUE: DONE` — работа продолжается. _(История chunk-009 ниже сохранена.)_

> **RECOVERY 2026-05-15:** Yana случайно закрыла терминал в самом конце chunk-008. Финальный батч SKU 81-86 уже был дописан в `chunk-008-diff.md` на диске (некоммичен, +92 строки), но MANUAL-REVIEW-секция, заголовки `80/86→86/86` и коммит не были сделаны. Контент сверен против locked-правил перевода (консистентен), доделан прерванный атомарный шаг: MANUAL-REVIEW SKU 81-86 + закрытие chunk-008 + оба заголовка → COMPLETE 86/86 ✅ + commit+push. **NEXT: chunk-009** — `.venv/Scripts/python.exe scripts/chunk_to_json.py 009` → mirror header chunk-008 (locked-паттерны + FLAG-правила) → loop ~8 SKU/batch. SKIP chunk-001 (заблокирован 8 вопросами Yana). Открытые вопросы chunk-008 = Q1-Q5 (веса `NN.00` + габариты SKU 39) в `chunk-008-MANUAL-REVIEW.md` — ждут Yana, не блокируют chunk-009.

> **4 ФОРМАТ-ПОЛИТИКИ LOCKED 2026-05-15** (Yana batch-решение после сводки вопросов chunk-005..008; закреплены в memory `feedback_labresta_ua_ru_translation_rules.md`):
> - **A** вес `NN.00`: HTML `Вага: NN.00`→`NN кг.` (как SKU 63/64); числовая колонка→целое `NN`. Реальные дроби не трогать.
> - **B** латинская `x` в габаритах→кириллическая `х` (`450x290x350`→`450х290х350`), UA+RU, **GLOBAL**.
> - **C** `330мм`→`330 мм` (пробел перед единицей), **GLOBAL**.
> - **F** HTML `<br />`-склейка в одном `<li>`→раздельные `<li>` зеркально чистой стороне, **GLOBAL**.
>
> **chunk-008 Q1/Q2/Q4/Q5 (веса) → RESOLVED политикой A.** Q3 (SKU 39 ZL1-8L 270 vs 275мм) → раунд 2.
>
> **RETRO-СВИП:** ✅ **A/B/C → спека готова** `.planning/translation-audit/GLOBAL-SWEEP-format.md` (универсальный детерминированный assembly-time pass, НЕ per-SKU diff — плотность B=592/C=299/A=139 в 001-008 только). Применяется `apply_chunk_diff.py` при сборке master-xlsx ко всем полям всех 85 чанков; требование+юнит-тесты в спеке. **F (структурный, per-SKU, зеркалить чистую сторону) — ✅ ЗАВЕРШЁН:** ✅ chunk-007 SKU 9 (commit `3560dfe`) · ✅ chunk-006 SKU 11/14/48/49/52 (commit `e7589bc`, SKU 49 = split+восстановление хвоста по sibling) · ✅ chunk-005 SKU 26/27/44 (RU перестроена зеркально чистой UA; SKU 44 GGM EGK55 = канонический референс класса). **Ретро-свип F полностью закрыт — все F-кейсы chunks 005-008 разрешены.**
>
> **РАУНД 2 открытых вопросов (НЕ решены):** E фактура R-код vs «гладкая» (chunk-005 SKU 24 / chunk-006 SKU 46 / chunk-007 SKU 7/40) · D chunk-008 SKU 39 · G chunk-006 SKU 51/55/56/54 · H chunk-006 SKU 23/25/26/27 Ozti объём (сверить supplier_products) · J точечные (chunk-007 SKU 8/13/17/18/26/37/52/53/54 + chunk-008 SKU 74 Kogast). Презентовать классами как раунд 1.
>
> **NEXT после ретро+раунд2:** chunk-009 — `.venv/Scripts/python.exe scripts/chunk_to_json.py 009` → mirror header chunk-008 + 4 новые политики → loop ~8 SKU/batch. SKIP chunk-001 (8 вопросов Yana).

**[history below]** chunk-008 SKU 73-80 batch: 3 напольные Apach APFE-47/2P/PL 544855953 / Kogast EFT7/14 544855956 / Bertos E7F10-8M 544855957 + 5 настольных Airhot EF10+10 554663073 / EF4 554663074 / EF4+4 554663075 / EF6 554663076 / EF6+6 554663077 — все 8 одинаковый класс: Назв.мод RU UA-leak→приведено к Название RU + 🔴 RU=UA full translate (украинская копия в RU-поле, HTML тег-в-тег вкл. `\n` в `<ul>` и `&laquo;&raquo;`; напряжение `380 В` напольные / `220 В` настольные НЕ трогаем — locked 220/380=разные SKU). SKU 73 decimal `10.5`→`10,5` кВт (UA+RU); SKU 74 decimal `11.1`→`11,1` кВт (UA+RU) + RU-leak `корзини`→`кошики` в публичном UA-поле (cross-language, sibling SKU 73 = `кошики`, откат по запросу) + soft note дефекты UA-источника идентичны в UA+RU (faithful): `Виконання покриття.` обрезанная фраза / `горіння осіли залишків` (`осіли`→`осілих`?) / падеж `з хромованою сталевого дроту` (sibling SKU 73 корректен `з хромованого сталевого дроту`) — на решение Yana. SKU 79/80 латинская `x` в габаритах (`450x290x310`/`570x450x310`) сохранена faithful — косметика на решение Yana. Открытых вопросов батч НЕ добавил (Q1-Q5 без изменений). NEXT: chunk-008 SKU 81-86 ФИНАЛ batch (dump `d[80:86]`, 6 SKU → 86/86, затем chunk-008 COMPLETE: оба header → `COMPLETE 86/86 ✅`, далее chunk-009 `scripts/chunk_to_json.py 009`). chunk-008 SKU 65-72 batch: GGM EFH8+8/EFK344-12/EFK643 + GoodFood EF4/EF44/EF6/EF66 + Apach APFE-47P/PL — 7 SKU без правок (RU настоящие переводы, не копии): SKU 65 GGM EFH8+8 428056895 / 66 EFK344-12 428056896 / 67 EFK643 428056897 (дескриптор `, защита от перегрева` корректен) / 68 GoodFood EF4 477220534 (UA+RU оба с градусами, диапазон совпадает) / 69 GoodFood EF44 477223241 / 70 EF6 477225151 / 71 EF66 477227393. SKU 72 Apach APFE-47P/PL 544855952 (підлогова, 380 В): Назв.мод RU UA-leak `Фритюрниця Apach APFE-47P/PL`→`Электрическая фритюрница Apach APFE-47P/PL` (приведено к Название RU) + 🔴 RU=UA full translate (украинская копия, HTML тег-в-тег; `380 В` напряжение не трогаем — locked 220/380=разные SKU). decimal правок нет (всё уже с запятой). soft note SKU 69/70/71: UA градус только у верхней границы (`від 60 до 200 °C`), RU корректно содержит оба (`от 60°С до 200°С`), значения совпадают 60/200 — публичное UA-поле faithful, авто-реструктуризация не применяется; доп. SKU 69 `105х240х105мм` без пробела (источник UA+RU faithful). Открытых вопросов батч НЕ добавил (Q1-Q5 без изменений). NEXT: chunk-008 SKU 73-80 batch (dump `d[72:80]`). chunk-008 SKU 57-64 batch: Bartscher A162412E + GAM F9+9V/F9V + REEDNEE EF081 + GGM EFH4/EFH8/EFK343-8/EFH4+4 кластер фритюрниц — 🔴 RU=UA full translate (украинская копия, HTML тег-в-тег) SKU 57 Bartscher A162412E 428056884 / 58 GAM F9+9V 428056885 / 59 GAM F9V 428056886 (`<h2>`) / 60 REEDNEE EF081 428056888 (`<h2>`); Назв.мод RU UA-leak→приведено к Название RU SKU 57/58/59/60; нормализация склейки в RU-переводе: SKU 57 `кошики.Підходить`→`корзины. Подходит`, SKU 58 `ручки`→`Ручки` после точки (UA-источник публично оставлен faithful — soft note добавить пробел?); decimal правок нет (мощности уже с запятой `6,5`/`3,25`/`2,5` кВт); SKU 61 GGM EFH4 428056891 / 62 EFH8 428056892 / 63 EFK343-8 428056893 / 64 EFH4+4 428056894 без правок (RU настоящие переводы, не копии). soft note SKU 61: габарит `264 м х 380 мм х 306 мм` первая величина без второго `м` (`264 м`, ошибка источника, UA+RU faithful) + UA один `&deg;C`, RU зеркалит одинарную форму (значения совпадают, авто-реструктуризация диапазона не применяется). soft note SKU 64: Название (RU) + Назв.мод (RU) `Фритюрница GGM EFH4+4` без дескриптора `4+4 л` (есть в UA `Фритюрниця 4+4 л GGM EFH4+4`; язык RU корректный, не UA-leak; публичное поле авто не правлено, аналог SKU 44 — на ревью Yana добавить `4+4 л`?). Открытых вопросов батч НЕ добавил (Q1-Q5 без изменений). NEXT: chunk-008 SKU 65-72 batch (dump `d[64:72]`). chunk-008 SKU 49-56 batch: FROSTY EFS-131V/EFS-26 + Bartscher A162812E + GAM F4/F8/F8+8 + REEDNEE EF062/EF082L кластер фритюрниц — 🔴 RU=UA full translate (украинская копия, HTML тег-в-тег вкл. `<h2>`) SKU 49 FROSTY EFS-131V 2301279584 / 51 Bartscher A162812E 2463601177 / 52 GAM F4 428056878 / 54 GAM F8+8 428056881 / 55 REEDNEE EF062 428056882 / 56 REEDNEE EF082L 428056883; Назв.мод RU UA-leak→приведено к Название RU SKU 49/51/52/54/55/56; decimal `.`→`,` UA+RU реальные дробные (НЕ NN.00) SKU 49 `7,80` / 51 нетто-вес `12,5` + мощность `6,5`; SKU 53 GAM F8 428056880 RU typo `Выполена`→`Выполнена` + пропущен пробел `190°C. Верхний` (RU корректно переведён, не копия — транспарентные авто-правки, откат по запросу); SKU 50 FROSTY EFS-26 2301284453 без правок (RU настоящий перевод, не копия). soft note SKU 50: UA+RU склейка двух характеристик `температурний режим … +190°C- Зливна трубка з краном` в одном `<li>` через `- ` (артефакт источника, структурная правка не авто, faithful — на ревью Yana разбить на два `<li>`?). ⚠️ открытый вопрос 5: SKU 50 вес `38.00` формат NN.00 (предложение `38`, тот же класс что Q1 `45.00` / Q2 `33.00` / Q4 `10.00`). NEXT: chunk-008 SKU 57-64 batch (dump `d[56:64]`). chunk-008 SKU 41-48 batch: FROSTY EFS-серия + REEDNEE/Hurakan/EFE кластер фритюрниц — 🔴 RU=UA full translate (украинская копия) SKU 42 REEDNEE EF101 2084240296 / 44 FROSTY EFE-8 2126980645 / 45 EFS-4L 2301256894 / 46 EFS-6L 2301261823 / 47 EFS-8L 2301263657 / 48 EFS-8L-2 2301264278 (однотипный шаблон EFS, висячие пробелы/`&ndash;`/`℃`/`220V` тег-в-тег); Назв.мод RU UA-leak→приведено к Название RU SKU 42/44/45/46/47/48 (SKU 44 + добавлен пропущенный «электрическая»); decimal `.`→`,` UA+RU реальные дробные веса (НЕ NN.00) SKU 42 упаковка `6,5` / 44 `5,50` / 45 `4,50` / 46 `4,60` / 47 `5,30` / 48 `9,80`; SKU 43 Hurakan HKN-FR6L 2104586731 cross-language RU-leak в UA публичном поле → `Холодная зона`→`Холодна зона` + `корзина`→`кошик` (транспарентно, откат по запросу; RU-описание корректно переведено, не копия); SKU 41 FROSTY ZL2-8L 2043372931 без правок (RU настоящий перевод, не копия; габариты/температура/мощность ОК). soft note SKU 44: Название (UA) `Фритюрниця Frosty EFE-8` без дескриптора «електрична» (есть в RU+тело) — публичное UA-поле, не правил, ждёт Yana. ⚠️ открытый вопрос 4: SKU 41 вес `10.00` формат NN.00 (предложение `10`, тот же класс что Q1 SKU 7 `45.00` / Q2 SKU 25 `33.00`). NEXT: chunk-008 SKU 49-56 batch (dump `d[48:56]`). chunk-008 SKU 33-40 batch: FROSTY фритюрницы кластер — SKU 33 FROSTY EF-102V 617666960 без правок (RU корректно переведён, не копия; soft note пробел `325мм` vs `325 мм`); SKU 34 FROSTY EF-172V 617666961 без правок (габариты UA/RU совпадают); SKU 35 Bartscher 165118 индукц. 1582657493 Назв.мод RU UA-leak `Фритюрниця індукційна`→`Фритюрница индукционная` + 🔴 RU=UA full translate (soft notes: `Напруга 220 Ст.` артефакт вместо `В`; `від +60 до +190°С` градус только сверху — locked-симметризация не применяется); decimal `.`→`,` UA+RU реальные дробные веса (НЕ NN.00) SKU 36 FE6L 2043343102 `5,60` / 37 FE6L-2 2043347193 `10,20` / 38 FE8L 2043348489 `5,60` / 39 ZL1-8L 2043363414 `5,50` / 40 ZL2 2043367095 `8,50`; SKU 37 UA typo `Зємні`→`З'ємні` (форма семейства FROSTY FE, транспарентно — публичное UA-поле, откат по запросу) + soft note висячий `6+6 л. -`. ⚠️ открытый вопрос 3: SKU 39 FROSTY ZL1-8L габариты UA `270мм x 430мм x 330мм` vs RU `275мм x 430мм x 330мм` (длина 270 vs 275) — какое верно, ждёт Yana. NEXT: chunk-008 SKU 41-48 batch (dump `d[40:48]`). chunk-008 SKU 25-32 batch: кластер вапо-грилей ARRIS Grillvapor + Frosty/Bartscher/Airhot — 🔴 RU=UA full translate SKU 25 FROSTY GL 60GS 2042403452 / 26 ARRIS GE519EL TOP 2177212402 (`<font>` вложенность) / 27 ARRIS GV817EL 2177221942 / 28 ARRIS GV855EL TOP 2177226262 / 29 Bartscher 151512 2463608004 / 30 Airhot EF10 554663072 / 31 Airhot EF8+8 554663079; Назв.мод RU UA-leak→перевод SKU 25 (`лавовий`)/26/27/28 (`водяній ванні`)/30/31 (`Фритюрниця`); decimal `.`→`,` UA+RU SKU 27 `10,4` / 28 `7,6` / 29 `47,7` (47.7 — реальная дробь, не NN.00); SKU 32 FROSTY EF-101V 617666958 без правок (RU корректно переведён, не копия; soft note пробел `325мм` vs `325 мм`). ⚠️ открытый вопрос 2: SKU 25 вес `33.00` формат NN.00 (предложение `33`, тот же класс что Q1 SKU 7 `45.00`). Soft note SKU 31: название `8+8 л` vs тело `Кожна об'ємом по 6 літрів` (2×6 л) — расхождение источника UA+RU, faithful. NEXT: chunk-008 SKU 33-40 batch (dump `d[32:40]`). chunk-008 SKU 17-24 batch: SKU 17 Roller Grill SEM 600 PDS 1153763826 typo `саламанандра`→`саламандра` UA ×3 (аналог SKU 16, RU корректен); SKU 18 Sirman Salamandra Mobile PRO 1/2 G 1557025542 🔴 RU=UA full translate (twin SKU 5); SKU 19-24 серия Pimak M170/70SD-M170 (1131882516/1131909790/1131911806/1131941088/1131942349/1131948163) — ЧИСТАЯ, все 6 RU корректно переведены (не копии), Названия корректны, мощности целые, без правок. Открытых вопросов батч не добавил (только Q1 SKU 7 вес `45.00`). NEXT: chunk-008 SKU 25-32 batch (dump `d[24:32]`). chunk-008 SKU 9-16 batch: Hendi Salamander/угольные грили кластер — 🔴 RU=UA full translate SKU 9 Airhot SGE-570 2460109996 / SKU 10 Hendi 150603 PATIO 900625827 / SKU 12 Hendi 264409 1162383611 / SKU 13 Hendi 264706 1162393164 / SKU 14 Hendi 264119 2121019658; Название мод. RU UA-leak→перевод SKU 10/12; SKU 9 cross-language leak (3 русские строки в UA-spec → укр + typo `вверх`→`верх`, транспарентная заметка — публичное UA-поле); SKU 16 Roller Grill SEM 600 Q typo `саламанандра`→`саламандра` UA ×3 (RU корректен); SKU 11 Hendi 238608 без правок (RU корректно переведён, soft note: UA `220-250C` без ° vs RU `220-250˚C`); SKU 15 Roller Grill 140 D без правок (RU корректно переведён); soft note SKU 14 `Размеры (мм): 610x310x` усечённая высота источника. Открытых вопросов батч не добавил (остаётся только Q1 SKU 7 вес `45.00`). NEXT: chunk-008 SKU 17-24 batch (dump `d[16:24]`). chunk-008 SKU 1-8 batch: 🔴 RU=UA full translate кластер (SKU 1 ARRIS GV 870 EL 925686772 + SKU 2 Hurakan HKN-SAL450H 927869275 twin chunk-007 SKU 57 + SKU 3 Airhot SGE-580 1131875858 + SKU 4 FROSTY VLB-826 1132488173 + SKU 5 Sirman Mobile PRO 1/1 G 1557035491 + SKU 6 Hurakan HKN-SLE580 2060590919 + SKU 7 FROSTY FLG-600 2309200640) — лавовые/Salamander/вапогрили дефект-кластер как chunk-007, структура HTML тег-в-тег; Название мод. RU UA-leak→перевод SKU 1/3/4/7; SKU 3 опечатка `саламанандра`→`саламандра` + UA `жаркова/жарка/жарячна`→`жарочна` (новые написания того же locked-класса) + decimal `2.4`→`2,4`; SKU 8 Saro LYNN 2331734259 `квт`→`кВт` + decimal `2.5`→`2,5` (RU уже корректно переведён, не копия). ⚠️ открытый вопрос 1: SKU 7 вес `45.00` формат NN.00 (предложение `45`, аналог chunk-007 SKU 44 `84.00`, chunk-005 `28.00`). NEXT: chunk-008 SKU 9-16 batch (dump `d[8:16]`), loop ~8/batch до 86/86, далее chunk-009→085, SKIP chunk-001. chunk-008: 86 SKU, FROSTY-доминанта (24) + Airhot 10 + GGM Gastro 7 + Pimak 6 + Hendi/GAM ×5 + ARRIS/Bartscher/REEDNEE/GoodFood ×4 + Hurakan/Roller Grill ×3 + Sirman/Apach ×2 + Saro/Kogast/Bertos ×1. chunk-008.json сгенерён (`scripts/chunk_to_json.py 008`); chunk-008-diff.md + chunk-008-MANUAL-REVIEW.md headers созданы (mirror chunk-007, locked-паттерны + FLAG-правила скопированы). NEXT: TaskCreate "chunk-008 SKU 1-8 batch" → dump `d[0:8]` → аудит → diff+MANUAL-REVIEW append → header 0/86→8/86 → CURRENT.md → commit+push. Loop ~8 SKU/batch до 86/86, далее chunk-009 → 085, SKIP chunk-001. chunk-007 COMPLETE 60/60 ✅ — chunk-007 SKU 57-60 ФИНАЛ: SKU 57 Hurakan HKN-SAL650H 🔴 RU=UA full translate; SKU 58 Hendi RESTO 150801 Название мод. UA-leak→RU + 🔴 full translate; SKU 59 GoodFood GS600 UA typo `саламанандра`→`саламандра` + decimal `2.2`→`2,2` (RU корректно переведён, не копия); SKU 60 ARRIS GV 470 EL Название мод. UA-leak→RU + 🔴 RU=UA full translate (большой `<font>`-блок, структура tag-в-tag, `смаженої решітки`→`жарочной решётки`). chunk-007 итог: ATA 38 + FROSTY 9 + Kogast/GoodFood/Airhot/Hurakan ×2 + Apach/Casta/Tatra/Hendi/ARRIS ×1, 13 открытых вопросов в chunk-007-MANUAL-REVIEW.md. ДАЛЕЕ: chunk-008 (`scripts/chunk_to_json.py 008`, mirror header chunk-007), loop 008→085, SKIP chunk-001. chunk-007 SKU 49-56 batch: FROSTY/Hurakan/Tatra/Airhot лавовые грили + Salamander — SKU 50 Hurakan typo `ЛОВЫЙ`→`ЛАВОВЫЙ` (Назв+мод RU) + машинная мистрансляция `скамья`→`лава` (RU body, укр. «лава»=lava); SKU 52 Tatra TSL.66 🔴 RU=UA full translate (soft Q12 «Гірки»); SKU 56 Airhot SGE-938 🔴 RU=UA full translate + typo `саламанандра`→`саламандра` + decimal `2.2`→`2,2` (аналог SKU 46); SKU 55 decimal `34.70`→`34,70` (UA+RU); SKU 49/51/53 без правок; flags: SKU 54 UA title без «електро» (Q11), SKU 52 «Гірки» (Q12), SKU 53/54 решётка `0х0 мм` источник (Q13). chunk-007 SKU 41-48 batch: FROSTY/Kogast/Casta/GoodFood/Airhot микс (ATA хвост закончился) — SKU 41 UA жаркова→жарочна; SKU 42 Kogast EZT47PL / 43 Casta L7KTE1BAL / 44 FROSTY GRT36B / 46 Airhot SGE-460 🔴 RU=UA full translate + Название мод. UA-leak→RU; SKU 46 typo саламанандра→саламандра + decimal 2.8→2,8; SKU 45/47/48 без правок; flags: SKU 44 вес 84.00 (вопрос 10). chunk-007 SKU 33-40 batch: 6×ATA K7EFB (хвост серии) sweep — RU `жареная`→`жарочная` (6/6) + UA `сбору`→`збирання` (SKU 33-38); SKU 33/34/37/38 RU `по сбору`→`для сбора` + `от 120 до 320&deg;C`→`от 120&deg;C до 320&deg;C` (значения совпадают); SKU 33/35 UA `мм :`→`мм:`; SKU 39 Kogast EZT40R 🔴 RU=UA полная укр. копия → full translate (вся карточка) + Название мод. UA-leak→RU; SKU 40 Apach APTE-77PL 🔴 RU=UA full translate + UA `жаркова`→`жарочна` + Название мод. UA-leak + ⚠️ T5 surface conflict (текст/код=гладкая vs spec=ребристая, открытый вопрос 8); SKU 37 ⚠️ `2,9 літр`→`2,9 літра` форма (открытый вопрос 9). chunk-007 SKU 25-32 batch: 8×ATA (K4EFRS10 + K6EFL/K6EFR + K7EFB серии) sweep — RU `жареная`→`жарочная` (8/8) + UA `сбору`→`збирання` (8/8); SKU 27/29/30/31/32 UA `мм :`→`мм:`; SKU 27/29 decimal `3.6`→`3,6`, SKU 28/30 `7.2`→`7,2`; SKU 26 RU `по сбору`→`для сбора` + `от 90 до 300&deg;C`→`от 90&deg;C до 300&deg;C` + 🔴 RU spec-блок целиком UA→RU full translate (12 строк, АВТО, открытый вопрос 7). chunk-007 SKU 17-24 batch: 8×ATA (K4EFBP10VV + K4EFLS/K4EFRS серии) sweep — RU `жареная`→`жарочная` (8/8) + UA `сбору`→`збирання` (8/8); SKU 20/21/23 RU `по сбору`→`для сбора` + `от 90 до 300&deg;C`→`от 90&deg;C до 300&deg;C`; SKU 19/20/21/24 decimal `6.5`→`6,5`; flags: SKU 17/18 RU temp 90-300 vs UA 120-320 (накопл. с SKU 13 → 3 SKU серии K4EFBP), SKU 17/18 UA `Два контейнера` форма (накопл. с SKU 15/16 → 4 SKU). chunk-007 SKU 9-16 batch: 8×ATA (C2EFR10 + K4EFBP05/10 серии) sweep — RU `жареная`→`жарочная` (8/8) + UA `сбору`→`збирання` (8/8); SKU 10 RU `по сбору`→`для сбора` + `от 90 до`→`от 90&deg;C до` + `мм :`→`мм:`; SKU 13/14 RU `по сбору`→`для сбора`; SKU 14 RU `от 120 до 320&deg;C`→`от 120&deg;C до 320&deg;C` (значения совпадают); SKU 9/10 decimal `8.2`→`8,2`; SKU 16 RU-leak `і`→`и`; flags: SKU 9 RU `<br />` склейка, SKU 10 spec/text dual-zone, SKU 13 RU temp значения 90-300 vs UA 120-320 (siblings 120-320), SKU 15/16 UA `Два контейнера` форма. chunk-007 SKU 1-8 batch: 8×ATA продолжение серии (K7GFB/C2EFL/C2EFR газ+электро) единый sweep — RU `жареная`→`жарочная` (8/8) + UA `сбору`→`збирання` (8/8); SKU 1/2 drop дубля `для жарки`; SKU 4/6/8 RU `по сбору`→`для сбора` + RU `от 90 до`→`от 90&deg;C до` + UA `мм :`→`мм:`; ВСЕ 8 decimal comma `13.8/4.1/8.2`→`13,8/4,1/8,2` (UA+RU, locked rule); SKU 7 ⚠️ T5 surface conflict (модель C2EF**R** но текст/RU-spec `гладкая` — flag); SKU 8 ⚠️ T6 body code `C2EFL05VV`→`C2EFR05VV` (авто-фикс, всё остальное согласовано на R). chunk-007.json сгенерён (`scripts/chunk_to_json.py 007`, 60 SKU: ATA 38, FROSTY 9, +tail). SKU 57-62 final batch: 6×ATA финальный sweep — RU `жареная`→`жарочная` + UA `сбору жиру`→`збирання жиру` (6/6); SKU 58/60/61 UA `мм :`→`мм:`; SKU 60 RU `от 150 до 315&deg;C`→`от 150&deg;C до 315&deg;C` (пропущенный знак градуса при нижней границе диапазона, симметризация с UA); SKU 61/62 NEW UA/RU `13.8`→`13,8` (decimal comma для дробной теплової потужності — locked rule Yana 2026-05-14, первое появление дроби в chunks 005/006). **chunk-006 закрыт.** Бренд-микс закрыт: ATA (34 — большинство, sweep ATA standard family); Ozti (9); Frosty (4); Silver (2 — `Isikgaz`→`Silver` brand body); Saro/GGM/Hendi/Roller Grill (по 2); Oztiryakiler/Heidebrenner/Casta/Sirman/Pimak (по 1). 9 открытых вопросов для Yana — финальная сводка в `chunk-006-MANUAL-REVIEW.md`. SKU 49-56 batch: 8×ATA продолжение/хвост — RU `жареная`→`жарочная` + UA `сбору жиру`→`збирання жиру` (8/8); SKU 49 UA `входить в.`(truncated)→`входять в комплект.` + ⚠️ RU HTML defect `<br />` склейка двух характеристик в одном `<li>` (5-й случай); SKU 50 UA typo `Вага, кг: 104мм`→`104` (артефакт `мм` от соседнего поля); SKU 51/55/56 RU `по сбору`→`для сбора` + ⚠️ RU dropped UA `Плавний нахил у бік відведення жиру` (3 SKU); SKU 52 UA `мм :`→`мм:` + ⚠️ RU HTML defect (6-й случай); SKU 54 ⚠️ UA `2 зони нагріву` vs RU `Зона нагрева` mismatch (spec подтверждает 2 зоны). Осталось 6 SKU до конца chunk-006. SKU 41-48 batch: 8×ATA продолжение единый sweep — RU `жареная`→`жарочная` + UA `сбору`→`збирання` (8/8); SKU 41 NEW RU `Глубина, мм :`→`мм:` (стилист. протекла в RU); SKU 47/48 NEW UA `от 150°C`→`від 150°C` (RU-leak предлог); SKU 46 ⚠️ T5 конфликт текст `гладка` vs spec `Ребриста` (модель код R = Ribbed) — flag; SKU 48 ⚠️ HTML structural defect — UA spec в одном `<li>` через `<br />` вместо 11 отдельных (4-й случай в chunk-005/006). Осталось 14 SKU до конца chunk-006. SKU 33-40 batch: 8×ATA (полностью ATA серия) единый sweep — RU `жареная`→`жарочная` (8/8) + UA `сбору`→`збирання` (8/8); 5 SKU также drop дубля `жареная для жарки`→`жарочная`; SKU 37 NEW UA-leak `Поверхность ребриста`→`ребристая`; SKU 38/40 NEW предлог `по сбору`→`для сбора`; SKU 33/34 продолжение стилист. `Глибина, мм :`→`мм:`. Master template ATA однородный — ожидается продолжение на SKU 41-50. SKU 25-32 batch: 3×Ozti OGG (SKU 25 partial семейный + RU `РИФЛЕНА`→`РИФЛЁНАЯ` UA-leak; SKU 26/27 `квт`→`кВт` + ⚠️ Об'єм 205/130 л flag); SKU 28 Pimak — без правок (META `смажена` отложен); 4×ATA (SKU 29-32) — RU machine mistranslation `жареная поверхность`→`жарочная поверхность` (4 SKU) + UA-leak `сбору жиру`→`збирання жиру` (4 SKU) + SKU 32 стилист. `Глибина, мм :`→`мм:`. Ожидается повтор ATA паттерна на SKU 33+ (34 ATA SKU всего). SKU 17-24 batch: Roller Grill PSF 600E lead-fix (UA `Смажувальна`→`Поверхня для смаження`); SIRMAN TOP L-L T1 RU=UA copy full translate + Название мод. UA-leak; 6×Ozti OGE/OGG (SKU 18/20/21/22/23/24) семейный typo-set sweep (UA `захиствід`/`квт`→`кВт`; RU `НАСТЕЛЬНАЯ`/`380 В В`/`квт`); SKU 21 RU `РИФЛЕНА`→`РИФЛЁНАЯ` UA-leak; SKU 23 ⚠️ Об'єм 100 л подозрительно для жарочной поверхности; SKU 24 RU `ГЛАДКА`→`ГЛАДКАЯ` UA-leak. Подозрение: вся Ozti OGE/OGG серия с одного master template — проверять SKU 25+ на тот же набор. Global sweep `жаркова/жарильна/смарочна` done (`GLOBAL-SWEEP-zharkova.md` — 23 fixed in chunk-005, 23 pending in chunks 006/007/008/060/061/062/066/075). chunk-006 SKU 1-8 batch: Silver 2606/2150DZ T6 brand body-Title `Isikgaz`→`Silver`, UA `Смажена`→`Поверхня для смаження` lead-fix, 4×FROSTY GES-550/732/760/762 full RU translates + Название мод. UA-leak fixes, 2×Saro PADUA/COMO typos (`&deg;; C`, `квт`→`кВт`, падеж `комбінованої`→`комбінованій`, RU стилист `для жарки×2`). Last commits: `20a7631` SKU 65-72 batch, `8bfc008` SKU 57-64 batch, `88420e2` SKU 49-56, `62dd2aa` retro v2, `c7d2c7d` retro v1. SKU 73-84 final batch добавлен (2×Frosty EGE-730F/FG UA typos `Жиросбірник`/`комібнована` + RU full translates + `Вага: 28.00` flagged; SKU 75 Silver 2151 DZ `SILVER`→`Silver` Title canonicalize; SKU 76 Oztiryakiler стандартный RU translate; SKU 77 GoodFood EG73FM RU+UA lead `одной`→`двумя` (`<li>`=2 зоны, зеркальная SKU 70/71); SKU 78-84 семи Silver моделей body `Isikgaz NNNN`→`Silver NNNN` brand canonicalize) — pending commit. chunk-005 COMPLETE 84/84. chunk-004 DONE 65/65, chunk-003 DONE 69/69, chunk-002 DONE 74/74. chunk-001 blocked by 8 Yana-questions.

**Night-mode workflow (Yana 2026-05-15):** "пиши все что требует моего потверждения в файл на русском языке, собирай такие проблемы - я завтра утром изучу. А ты продолжай работать над поиском ошибьок и их исправлением дальше, делай переводы." → не блокироваться на ambiguity, всё в `chunk-005-MANUAL-REVIEW.md` (русский), продолжать SKU 57-84 + global sweep.

**Waiting on Yana (2 decisions in MANUAL-REVIEW.md):**
1. SKU 24 APTE-47PR Название: гладка → ребриста (supplier+body согласны)? Y/N
2. SKU 26/27/44 HTML structural defects: перестроить `<li>` блоки или оставить?

Plus 8 auto-applied retro-fixes для подтверждения (SKU 19/25/32/35/38/52/53 + SKU 9 watts).

**STILL BLOCKED от SKU 49-56 batch** до решения Yana или explicit go-ahead. Файл `.planning/translation-audit/chunks/chunk-005-MANUAL-REVIEW.md` — единая точка входа для её обзора.

## ✅ DONE 2026-05-14 — Cat H closed + clean Horoshop XLSX upload + DB hygiene

**Cat H (11 коллизий) — закрыт:**
- 7 Hendi-vs-non-Hendi очищены в БД + Horoshop CMS (Yana). Tasks #2/#4/#5/#6/#7/#11 completed.
- 4 внутри-бренда (Ozti, Sirman ×3, FROSTY) оставлены — это ручные коды, могут совпасть с будущим feed'ом.
- Verification: `scripts/verify_cat_h_article_ownership.py` (commit `d45b510`) — 6 артикулов реально в Астим feed (Hendi distributor).

**XLSX upload 13.05.26 — успешно:**
- CSRF fix (commit `d9a53a5`): template `app/templates/catalog/import.html` теперь содержит `<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">`. Раньше форма была без токена, любой POST падал.
- Backup сделан до загрузки: `backups/pre-catalog-import_2026-05-13_1658.json` (5683 PPs + 2689 matches, 20.8 MB).
- Импорт: 5632 строк → 0 новых, 5632 обновлено, 0 пропущено.
- Verifier `scripts/verify_after_catalog_import.py` (commit `cfafb8d`): все 9 проверок green. 7 Cat H PPs остались display_article=NULL post-import.

**bench_pp* мусор удалён:**
- 50 синтетических строк (IDs 5684-5733, brand=Sirman, name="Sirman Mantegna NN", price=1000 EUR, created 2026-04-26 20:29:13 одной транзакцией) — артефакт perf-benchmark скрипта, прогнавшегося против прода. Не в Horoshop, 0 matches.
- Audit `scripts/audit_bench_pp_pollution.py` (commit `5d8277d`) → подтвердил scope.
- Delete `scripts/delete_bench_pp_pollution.py` (commit `a5a6a56`) → 50 удалено с --apply (2026-05-14 06:10).
- Total PromProducts: 5683 → **5633**. Verifier baseline скорректирован.

**Текущее состояние БД:**
- 5633 PromProducts (всё реальный Horoshop каталог)
- 2689 ProductMatches (2546 confirmed/manual)
- 6 suppliers: MARESTO 861, НП 373, Кодаки 559, РП 187, Гудер 79, Астим 487 (= 2546 total)
- 12890 SupplierProducts

## Backlog (следующее)
1. **UA→RU перевод каталога** — IN PROGRESS 2026-05-15. **Chunk-001:** 83/83 source audit done, ЗАБЛОКИРОВАН 8 вопросами Yana в `.planning/translation-audit/chunks/chunk-001-questions.md`. **Chunk-002:** 74/74 source audit DONE (last commit `259a943`, 9 SKU batches). **Chunk-003:** PENDING (next). Workflow per batch: `python -c "..."` dump 5-8 SKU из `chunk-NNN.json` → Read `.planning/scratch_skubatch.txt` → Edit-append `chunk-NNN-diff.md` перед final `---` → commit. После всех чанков (003-085): `scripts/apply_chunk_diff.py` (openpyxl, key Артикул) собирает master-fixed.xlsx → drift check vs fresh Horoshop re-export → Yana ручная загрузка `/catalog/import` + `backup_before_catalog_import.py` сначала.
2. **Починка характеристик в Horoshop CMS** — NEXT после перевода. На странице товара (пример: `labresta.com.ua/ru/parokonvektomat-unox-xevc0711e1rm-liniia-one/`) 4 свойства отображаются **зачёркнутыми**: `Номінальна напруга`, `Страна производитель`, `Вид обладнання`, `Номінальна споживана потужність`. Причина: свойства в Horoshop CMS помечены как архивные/неактивные (значения остались привязанными к товарам, но Property labels выведены из активного списка). Также часть свойств UA-only без RU-перевода имени. Скоуп: пройти **Каталог → Свойства товаров** в Horoshop, восстановить активный статус + дозаполнить UA+RU имена для всех зачёркнутых свойств. Рекомендованный вариант A (unarchive + переименование) безопаснее B (создать новые + перепривязать значения). Подзадача-помощь от меня: когда будем чистить описания товаров в XLSX-чанках — отдельно собрать таблицу всех уникальных `Характеристика → значение` из HTML-описаний с готовыми UA+RU вариантами как референс для импорта свойств в CMS.
3. **Прогресс-бар на /catalog/import** — UX улучшение. Корень: catalog_import делает 5632 индивидуальных SELECT+UPDATE round-trip через Railway proxy ~80-120 сек, впритык gunicorn timeout 120s. Решение: `INSERT ... ON CONFLICT DO UPDATE` одной операцией → импорт упадёт до ~5-10 сек, прогресс-бар не нужен.
4. **AD46 cleanup** — 3 PPs убрать из Horoshop (PP#1007/1015/1008). Apach AD46MV/DV/D ≠ AD46M/MI/DI ECO.
5. **Cat B sibling (13 шт.)** — per-row через `/matches/` UI.
6. **Cat B-reverse (8 шт.)** — per-row решение.
7. **Phase L smoke-test** — `/matches/?supplier_id=4`, выделить 5-10 НП кандидатов, подтвердить, проверить #conflictResolveModal.
8. **Manual Astim review** (7 fuzzy + 3 reject).

## Memory rule установлено
- `feedback_labresta_backup_before_catalog_import.md` — перед каждой XLSX загрузкой backup + offer restore.
- TODO: добавить memory "не запускать perf-benchmark против прода без явного флага" (после bench_pp инцидента).

---

## ⏸ Prior session — 2026-05-13 (Cat H plan rewritten, Horoshop pass ждёт Yana)

**CSRF fix pushed (commit `d9a53a5`):** `app/templates/catalog/import.html` form was missing
`<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">`. Every POST /catalog/import
failed with "The CSRF token is missing" — that template hadn't been used in months. Fix is one
line, pushed to main, Railway redeploys ~1-2 min after push.

**Post-upload verifier (commit `cfafb8d`):** `scripts/verify_after_catalog_import.py` —
read-only check after Yana's upload. Confirms 7 Cat H PPs still NULL, counts unchanged
(PPs ≥ 5683, matches = 2689, suppliers = 6), spot-checks fields. Points to restore command
if anything fails.

**Backup taken pre-upload (commit `e9fed2a`):** `backups/pre-catalog-import_2026-05-13_1658.json`
— 5683 PPs + 2689 matches, 20.8 MB. Restore via `scripts/restore_pp_from_backup.py`.

**Cat H DB clears already applied (commit `44279fe`):** 7 PPs cleared in DB. Yana also cleared
the Horoshop cards (her words 2026-05-13). If both halves done correctly, post-upload verifier
will pass.

**Next concrete actions:**
1. Yana retries XLSX upload via `/catalog/import` (fresh page load to pick up new csrf_token)
2. If 200 OK: Yana runs `.venv/Scripts/python.exe scripts/verify_after_catalog_import.py`
3. If verifier passes: I close tasks #2/#4/#5/#6/#7/#11 (Cat H done)
4. If verifier fails: restore via `scripts/restore_pp_from_backup.py backups/pre-catalog-import_2026-05-13_1658.json --apply`

**Файлы (committed, deployed):**
- `app/templates/catalog/import.html` — CSRF token added
- `scripts/verify_after_catalog_import.py` — new post-upload verifier
- `scripts/backup_before_catalog_import.py` + `scripts/restore_pp_from_backup.py` — pre-import safety
- `scripts/clear_cat_h_hendi_display_articles.py` — Cat H clear script (already applied)

---

## ⏸ Prior session — 2026-05-13 (Cat H plan rewritten, Horoshop pass ждёт Yana)

**Cat H финализирован.** Правило Yana 2026-05-13: правим **только** Hendi-vs-не-Hendi коллизии. Внутри-бренда (Ozti↔Ozti, Sirman↔Sirman, FROSTY↔FROSTY) НЕ ТРОГАТЬ — там display_article это ручные коды, для Sirman/Ozti они могут совпасть с будущим feed'ом когда подключим поставщика.

**Финальный план — 7 правок (clear display_article):**
- PP#347 Spidocook SP300 (`203149` Hendi) → очистить
- PP#80 Fimar PFD27 (`239766` Hendi) → очистить
- PP#154 Roller Grill PIS 30 (`239780` Hendi) → очистить
- PP#958 FROSTY RC-30 (`240403` Hendi) → очистить
- PP#3933 FROSTY IC80A (`271599` Hendi) → очистить
- PP#3932 GoodFood ICE777 (`271599` Hendi) → очистить
- PP#4179 Saro SKZ-12 (`860526` Hendi) → очистить

**Verification:** `scripts/verify_cat_h_article_ownership.py` (2026-05-13, read-only prod-DB) — все 6 артикулов реально из Астим feed (Hendi distributor); 5 внутри-бренда артикулов нет ни у одного поставщика (Yana-entered).

**Не трогаем:** Ozti `0830.00020.00`, Sirman `40752102P` / `40802852F` / `66520502K1.2`, FROSTY `212004` — внутри-бренда коллизии. FROSTY VP-81/VP-2Y40 уже phase8_orphan, отдельная UI-задача (не Cat H).

**Файлы (commit pending):**
- `.planning/dossiers/cat-h/HOROSHOP-WALKTHROUGH.md` — переписан под 7 clear-only
- `.planning/dossiers/cat-h/ANSWERS.md` — переписан под финальный план
- `scripts/verify_cat_h_article_ownership.py` — новый verify-скрипт

**Предыдущие commits на ветке (suffix-style план, теперь obsolete):** `ef29a1c` lookup, `028689b` sirman.com, `d52733e` CURRENT, `d88777c` UA shops, `dc46ca3` #10 suffix, `92bb23f` #8 closed, `bed9fb7` CURRENT update, `6f64c17` HOROSHOP-WALKTHROUGH (suffix). Не откатываю — следующий коммит просто фиксирует финальный план.

**Не закрыто:** Tasks в TaskList — pending до физической правки 7 PPs в Horoshop CMS (диагноз готов, action за Yana).

**Следующее после Horoshop pass** (выбор Yana из TODO-NEXT.md):
1. AD46 cleanup — 3 PPs убрать (PP#1007/1015/1008)
2. Cat B sibling (13 шт.) — per-row через UI
3. Cat B-reverse (8 шт.) — per-row
4. Phase L smoke-test
5. Manual Astim review (7 fuzzy + 3 reject)

---

## Session 2026-05-09 — auto_sync_enabled (commits `1e91fcc`, `9f3b3bc`, `a0d6599`)

---

---

## Session 2026-05-09 — auto_sync_enabled (commits `1e91fcc`, `9f3b3bc`, `a0d6599`)
- **Кнопка «Обновить данные» удалена** с дашборда (только перерисовывала виджеты, путала оператора). Page и так auto-poll'ит.
- **`Supplier.auto_sync_enabled`** (bool, default True, NOT NULL) + Postgres миграция `migrate_add_supplier_auto_sync_pg.py` в `railway.toml` startCommand. Прод: миграция отработала, в логах `auto_sync_enabled migration: done.`
- **`run_full_sync(supplier_id=None, *, manual=False)`** — крон (`manual=False`) фильтрует `auto_sync_enabled=True`; ручные кнопки (`manual=True`) и per-supplier path игнорируют флаг.
- **Toggle endpoint** `POST /suppliers/<id>/toggle-auto-sync` + badge `Авто-синк OFF` (warning) + кнопка «Авто-синк OFF/ON» в `/suppliers/`.
- **MARESTO snapped on prod** через UI (`auto_sync_enabled=False`) — крон больше не дёргает 403'ящий feed. Verified в БД: `(1, 'MARESTO', True, False)`, остальные `True`.
- **Tests**: 6 в `tests/test_sync_pipeline_auto_sync.py` (cron skip, manual include, per-supplier ignore, is_enabled=False guard, toggle endpoint flip + 404). Suite 677→683 passed.

## Audit results (2026-05-09 — night session)
- `.planning/matching-audit-report.md` (commit `fc466f7`): A=0 B=13 B-rev=9 C=0 D=267 E=0 F=0 G=0 H=11
- `.planning/article-anchor-verify.md` (commit `ee914d6`): 487 three-way + 417 two-way + **4 rule violations** + 1641 no-anchor (fuzzy/manual)
- 4 violations отозваны (все были `confirmed_by='Admin'` manual): match#6611 (Hendi щепа 250г vs 150г SP), #6383 (Hendi цитрус-пресс), #1100 (Sirman STORM VV), #1102 (Sirman CICLONE 36 VT). Re-verify: 0 violations осталось, total confirmed 2549→2545.
- `.planning/no-anchor-verify.md` (commit `cce9cac`): **1641 confirmed без article-anchor — clean**. 1636/1641 OK по brand+voltage+model-token; 0 brand mismatches, 0 voltage disjoint, 5 no_model_token все вручную проверены — все валидные (Rational SCC→iCC rebrand с display_article anchor на PP-стороне; Sirman 1/2 vs I/2 typo; Ugolini MINIGEL с переставленными словами).

## Per-row dossiers (commit `02318e3`)
**`.planning/dossiers/INDEX.md`** — 42 dossier-файла собраны из прода:
- `cat-h/` 11 шт. — каждый duplicate display_article с обоими PP, фото, ценами, описаниями
- `cat-b/` 13 шт. — PP + suffix-кандидат-SP с voltage check
- `cat-b-rev/` 9 шт. (был 8, prod refresh +1)
- `astim-fuzzy/` 9 шт. (был 7, prod refresh +2)

Регенерация: `.venv/Scripts/python.exe scripts/build_dossiers.py --cat all`

## TODO для Yana завтра
См. **`.planning/TODO-NEXT.md`** (commit `7c96966`+). Приоритет:
1. Cat H — 11 cross-brand display_article дублей в Horoshop (catalog hygiene, ручками)
2. Catalog cleanup — 3 AD46 PPs (PP#1007/1015/1008) убрать из Horoshop
3. Cat B sibling (13 шт.) — per-row через `/matches/` UI
4. Cat B-reverse (8 шт.) — per-row решение

**Status:** Прозвонены 14 URL-вариантов np.com.ua/dealer-export (`scripts/_probe_np_url_variants.py` — temp, удалён). Финальный вывод: **поставщик np.com.ua не выгружает APL/APKE/AFM 02-03 ни в одном формате/параметре**. Любой из {`filetype=xlsx|csv|xml|yml`} × {без `platform`, `platform=prom|opencart|woocommerce|horoshop`} × {`with_all=1|with_full=1|include_disabled=1|include_unavailable=1`} = тот же набор 690 уникальных SKU. `platform=horoshop` режет вдвое (691 строк) только потому что фильтрует одну локаль (UA), без него — 1382 строки = 690 RU + 691 UA версий тех же товаров. Apach = 158 уникальных (316 RU+UA). APL: 0 hit. APKE: 0 hit. AFM 02/03: 0 hit. AD46: только AD46MI ECO / AD46M ECO / AD46DI ECO (AD46MV/DV отсутствуют — Yana подтвердила). **Проблема НЕ в URL и НЕ в парсере. Поставщик технически не экспортирует часть каталога**. Phase M apply остаётся ЗАБЛОКИРОВАН.

## Open files
- (none — Phase L и Phase M закрыты at commit level, awaits manual smoke-test)

## Next step
1. **Yana — Phase L smoke-test:** открыть `/matches/?supplier_id=4`, выделить 5-10 НП кандидатов, нажать «Подтвердить». Должен появиться `#conflictResolveModal` с per-row кнопками **Оставить** / **Переключить** вместо старого toast'а. По каждой строке клик → должна faded'нуться + статус «Кандидат отклонён» / «Переключено». Закрыть → reload.
2. **Phase M apply — ЗАБЛОКИРОВАН. Технических вариантов больше нет.** URL-варианты исчерпаны (см. Status). Остались два пути: **(A)** написать поставщику np.com.ua с просьбой расширить дилер-экспорт (показать им скрин дилерского портала где APL/APKE/AFM 02 есть, а в XLSX их нет — спросить почему `dealer_id=69781` выдаёт неполный набор), **(B)** scrape дилерского портала по логину manager@labresta.com — но Cloudflare блокирует headless Chromium, нужен реальный браузер с DPAPI cookie или ручной экспорт по сессии. **Для Apach — не применять Phase M ни на одном уровне** пока не дополним фид. Альтернатива: per-brand whitelist в `flag_orphan_pps` — пропускать Apach до починки.
3. **Phase N — diagnostic step done, matcher change deferred:** скрипт `scripts/diagnose_sibling_gap.py` (commit `bdaca6c`) классифицирует unmatched PP в 4 категории: Cat A (exact-anchor SP — gate filtered), Cat B (SP=anchor+suffix), Cat B-reverse (PP=SP+suffix), Cat None (no nearby SP). На local-DB Hurakan/supplier_id=2 (stale): 4/5/4/18. **Yana — прогнать на проде:** `railway run python scripts/diagnose_sibling_gap.py --brand Hurakan --supplier-id 4` чтобы увидеть реальные числа и решить — стоит ли матчер модифицировать. Локалка показала важный сюрприз: некоторые Cat A SPs **уже привязаны к другим PP** (duplicate Horoshop card problem — PP#3864 vs PP#3902), что матчер-изменение НЕ решит. Для них нужен другой workflow (rebind или slim card cleanup).
2. **Yana — UI триаж 10 настоящих orphans Phase 8:** `/matches/deletion-candidates?tab=orphan` (badge=10), фильтр по бренду, **Видалено / Залишити / Запит**.
3. **Manual Astim review** (carry-over): отклонить m=6620, 6618, 6611 + подтвердить 7 fuzzy candidates на `/matches/?supplier_id=8&status=candidate`.
4. **MARESTO unblock** (опционально): MARESTO всё ещё 0/4509 fresh на проде (id=1 в `dead_supplier_ids`). Whitelist Railway egress IP через support, либо local-fetch скрипт.
5. **Open question (deferred):** должен ли `suppliers_fetch_all` передавать `exclude_dead_suppliers=True`? Решение за Yana — risk decision (auto-cron должен ли стрелять пока MARESTO навсегда мёртв?). Текущий код — OFF (safe default). НЕ автономно.

## Phase L commits (тонкая ночь)
- `7f442d7` backend — `_build_conflict_payload` + enriched `skipped_claimed` + `POST /matches/resolve-conflict` (keep/switch) + 11 tests
- `14367b4` frontend — `#conflictResolveModal` в `review.html` + `populateConflictModal/resolveConflict/buildConflictRow` в `matches.js`. Backward-compat fallback на старый toast если payload без `entry.candidate`.

## Phase N diag commit (после M)
- `bdaca6c` — `scripts/diagnose_sibling_gap.py` read-only классификатор unmatched PP. Local Hurakan/sup_id=2 baseline: 4 Cat A (DL800/DL775 silver+black/HBH850M PRO COVER/BLW2 grey — но 3/4 SP уже в другом PP), 5 Cat B (DHD10G/12G/16G→GM, CFV60→M, TR65→M — но TR65 SP уже в PP#3934), 4 Cat B-reverse (IP40FM/WNC160CDW/ISV5P×2), 18 Cat None.

## Phase M commit
- `0b9b5e2` — `feat(phase-M): orphan flag for PP without display_article via name scan`. Helpers `_supplier_article_strings` / `_build_sp_article_boundary_re` / `_any_sp_article_in_pp_name` + fallback ветка в `flag_orphan_pps` когда `disp` пуст. 5 новых тестов. Total 21/21 orphan_detector + 677/677 suite.
- `938ed00` docs(planning) — CURRENT update Phase M done.

## Phase 8 commits (today)
- `51d274c` Task 1 — service + 11 tests
- `11aa107` Task 2 — wire-in + CLI
- `cd1e91b` Task 3 — UI tab + brand filter + clear-flag endpoint
- `3f9f07a` fix — skip no-display-article + `--exclude-dead-suppliers`
- `d27a7e0` SUMMARY (initial)
- `fb89ace` follow-up fix: keep dead in anchor + clear-on-recovery + 3 new tests (APPLIED to prod via railway run + DATABASE_PUBLIC_URL: 16 cleared, 10 remain)

## Prod audit (2026-05-08, scripts/verify_prod.py)
- Astim: 487 confirmed, 10 candidates (3 display_art_dup, 7 fuzzy false-pos)
- MARESTO: 857 confirmed, 10 candidates (но sync error всегда — см ниже)
- Кодаки: 559 conf, 9 cand. Гудер: 76, 2. РП: 187, 56. НП: 371, 21.
- Total candidates=108, badge=14 (correct по logic — исключает PP с другим confirmed match)
- 0 stuck SyncRuns. 0 M:1 violations. 17 truly-orphan Hendi PP (Phase 8 baseline).

## Three problems found and resolved (2026-05-08)
1. **YML 404 на проде — FIXED** (commit `4f15e58`). Root cause: Railway эфемерная FS стирает `instance/feeds/` при каждом deploy. Fix: `scripts/regenerate_yml_on_startup.py` в startCommand перед gunicorn (с `|| echo` fallback). Verified: `/feed/yml` HTTP 200, 7.4 MB, 2548 offers.
2. **MARESTO sync падает 403 Forbidden — KNOWN ISSUE** (commit `4f89bda` диагностический скрипт). Root cause: `mrst.com.ua/include/price.xml` возвращает 200 OK с локалки, но 403 с Railway. Заголовки парсера нормальные (Chrome 124 UA + Referer). Это IP-блок (Cloudflare WAF против Railway-диапазона). Не наш баг. Fix потребовал бы whitelist на стороне MARESTO или прокси.
3. **Stage 4 deletion_candidate=0 везде — НЕ БАГ**. Логика корректна: триггер срабатывает только если SP не виден ≥9h И есть confirmed/manual match. Все суппортеры свежие; MARESTO падает на Stage 1 (403) до Stage 4 не доходит. 17 orphan Hendi PP — отдельная история (никогда не были в фиде Astim) → Phase 8 закроет именно этот gap.

## Decisions made earlier today (2026-05-08)
- 484 Astim R0 confirms applied via `apply_rules(apply=True, confirmed_by='manual:astim_first_apply')`. Per-rule: только R0 fired. r4_rejects=0.
- YML push в Horoshop = pull-модель (Horoshop сам тянет по URL), активного FTP push в `sync_pipeline.run_full_sync` нет. Stage 7 пишет YML только локально.
- 9 не-confirmed Astim candidates — R0 path B провалился потому что артикул только в `display_article`, не в `pp.name`. Path A провалился потому что `pp.article=None`. По правилу всё корректно. Yana подтвердит вручную.
- 26 Hendi PP без confirmed match. 17 из них в фиде Astim отсутствуют → real gap → Phase 8.
- Stuck SyncRun id=36, 37 (от 2026-05-05) помечены `failed` чтобы UI спиннер разблокировать.

## Constraints (carried over)
- LIVE store, никакого активного FTP push без go-ahead.
- 1 PP ↔ 1 confirmed supplier match (M:1 forbidden).
- 100% name match НЕ bulletproof — only identical names safe to bulk-confirm.
- Voltage variants (220 vs 380) = different SKU, never auto-match.

## Apply result (2026-05-08)
- `confirmed`: 484 (all Astim R0 — article anchor + display_article match)
- `singles`: 689, `multis`: 19, `skipped_claimed`: 91
- `per_rule`: `R0:article-name+display_article` = 484 (only rule that fired)
- `r4_rejects`: 0, `rejected`: 0
- 19 multis did not auto-confirm (R3 conditions not met — expected, leaves them for manual UI review)

## Constraints / decisions
- **LIVE store** — never push full Horoshop import without explicit go-ahead + safe-mode plan
- Horoshop only, never prom.ua
- 1 caталожный товар ↔ 1 confirmed supplier match (M:1 forbidden)
- 100% name match is NOT bulletproof — only identical names safe to bulk-confirm
- Voltage variants (220 vs 380) = different SKU, never auto-match
- `<oldprice>` in YML overrides Horoshop card "Знижка %" (fixed 2026-04-23, commit `ed8182f`)
- Finish Maresto first before adding new suppliers
- Proper fix > workaround: clean data via merge/delete scripts, не оставлять сирот
- 491 tests at commit `6908d11`

**Last commit:** 2026-05-08 — `feat(phase-N): diagnostic script for sibling-gap analysis` (`bdaca6c`)
**Memory pointers:**
- `~/.claude/projects/C--Users-Yana/memory/project_labresta.md`
- `~/.claude/projects/C--Users-Yana/memory/project_labresta_horoshop_import.md`
- `~/.claude/projects/C--Users-Yana/memory/project_labresta_feed_mgmt_plan.md`

## Existing .planning artifacts
_Phase plans already exist in this dir — check `ls .planning/` before starting; CURRENT.md complements them with right-now state._
