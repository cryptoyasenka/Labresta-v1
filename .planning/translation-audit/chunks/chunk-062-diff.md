# chunk-062 translation diff (81 SKU — грили контактні / роликові / теплові вітрини; W2 диапазон 055-085, продолжение chunk-061)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-062 (81 SKU)
**Apply key:** `Артикул` (scoped per row)
**Status:** IN PROGRESS 48/81 (blk триплет 17 / blknochg 29 / blknotrip 1 / SKIP-НП 1; Открытых вопросов 0)
**Worker:** W2 (параллельный воркер, диапазон chunk-055 … chunk-085; W1 ведёт chunk-001 … chunk-054)
**Scaffold:** chunk-062 scaffold (W2, продолжение chunk-061). chunk-061 ЗАКРЫТ 67/67 (blk триплет 29 / blknochg 34 / blknotrip 0 / SKIP-НП 4; OQ 0). chunk-062 = 81 SKU, openpyxl rows 2..82; первый SKU1 ART2424757446 «Гриль контактний SARO PG 1B», последний SKU81 ART2059507443 «Теплова вітрина Hurakan WD-120L». 11 батчей (б1-10 ×8 = 80, б11 = SKU81 ×1 финальный). SKIP-НП зонд по `Название` (NP-список HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA — Lat+Cyr): **6 hits — все HURAKAN**: SKU34 (ART736117487 «Гриль роликовий HURAKAN HKN-GW7M»), SKU53 (ART2375841678 «Гриль роликовий HURAKAN HKN-GW11M»), SKU54 (ART2375848556 «Гриль роликовий HURAKAN HKN-GW9M»), SKU66 (ART901422138 «Теплова вітрина HURAKAN HKN-WD2»), SKU67 (ART1168676811 «Теплова вітрина HURAKAN HKN-WD3M»), SKU81 (ART2059507443 «Теплова вітрина Hurakan WD-120L»). Эти SKU → SKIP-НП (тело из фида НП позже), вносятся в таблицу при обработке батчей б5 (SKU34) / б7 (SKU53/54) / б9 (SKU66/67) / б11 (SKU81). Прочие бренды (SARO и др.) НЕ в НП-списке — обрабатываются обычно.

Категории (эталон chunk-019 / chunk-061): **blk триплет** = `descUA==descRU` True И col5==col4 (UA-leak имя) И col7 (NAZVRU) genuine RU → col5←col7 + col36 полный тег-в-tag перевод source col35. **blknotrip** = lang-neutral бренд+код имя (col5==col4 не UA-leak) → переводится только col36. **blknochg** = `descUA!=descRU` (отдельный чистый genuine RU, col5==col7) → fixed.xlsx НЕ трогается; артефакты/опечатки soft-note (НЕ нумеруются). **SKIP-НП** = NP-эксклюзивный бренд (forward-only, тело из фида НП позже).

---

## Батч 1 (SKU 1-8, openpyxl rows 2-9) — 8/81

**Категории:** blk триплет 1 · blknochg 7 · blknotrip 0 · SKIP-НП 0 · OQ 0.

| SKU | row | ART | Имя (UA→RU) | Категория | fixed.xlsx |
|---|---|---|---|---|---|
| 1 | 2 | 2424757446 | Гриль контактний→контактный SARO PG 1B | blknochg (descUA≠descRU, col5==col7 genuine RU) | НЕ тронут (==src) |
| 2 | 3 | 2424795941 | Гриль контактний→контактный SILVER SS-20D | blknochg | НЕ тронут (==src) |
| 3 | 4 | 2424802108 | Гриль контактний→контактный SILVER 2131/1 | blknochg | НЕ тронут (==src) |
| 4 | 5 | 2447398478 | Гриль контактний EWT INOX CGR811EB → Гриль контактный EWT INOX CGR811EB | **blk триплет** (descUA==descRU True, col5==col4 UA-leak, col7 genuine RU) | **col5←col7 + col36 tag-в-tag RU (692→700)** |
| 5 | 6 | 2526650301 | Гриль саламандра GoodFood GS300 (lang-neutral) | blknochg (genuine RU col36) | НЕ тронут (==src) |
| 6 | 7 | 2526654600 | Гриль саламандра GoodFood GSEG58 (lang-neutral) | blknochg | НЕ тронут (==src) |
| 7 | 8 | 2528568664 | Машина для гамбургерів→гамбургеров GoodFood HGM01 | blknochg | НЕ тронут (==src) |
| 8 | 9 | 2528600639 | Машина для гамбургерів→гамбургеров GoodFood HGM02 | blknochg | НЕ тронут (==src) |

**blk триплет SKU4 EWT INOX CGR811EB:** col5←col7 `Гриль контактный EWT INOX CGR811EB`; col36 = полный tag-в-tag RU перевод source col35 (692→700 симв). Byte-exact: `℃` (U+2103) сохранён verbatim, `220V` сохранён verbatim (не нормализуется в `220 В`), скелет тегов/переводов строк идентичен source. UA-маркеров в col5/col36 нет.

**Soft-notes (genuine-RU вариативность / артефакты source — НЕ нумеруются, НЕ OQ; blknochg → fixed НЕ тронут, LIVE НЕ переписан):**
- SKU1 SARO PG 1B: genuine-RU col36 — UA `<li>Підключення, в 220</li>` → RU `<li>Подключение, в 220 В</li>` (RU добавляет ` В`); UA `&#39;` (`м&#39;яса`) → RU plain `мяса`; RU кавычки `&laquo;&raquo;` (UA прямые `"..."`). NAME консистентен (SARO PG 1B), прец. SKU65 б9 c061.
- SKU2 SILVER SS-20D: source-RU артефакт — `<li>Пластиковая защита верхней пружины пластиковая защита верхней пружины</li>` (фраза продублирована в исходном RU; UA одна `Пластиковий захист верхньої пружини`). NAME консистентен.
- SKU3 SILVER 2131/1: source-артефакт в обоих UA/RU — склейка `…5 хот догов.Верхняя часть гриля…` (пропущен пробел после точки, в UA аналогично `…5 хот дога.Верхняя частина…`). NAME консистентен.

---

## Батч 2 (SKU 9-16, openpyxl rows 10-17) — 16/81

**Категории:** blk триплет 0 · blknochg 8 · blknotrip 0 · SKIP-НП 0 · OQ 0.

| SKU | row | ART | Имя (UA→RU) | Категория | fixed.xlsx |
|---|---|---|---|---|---|
| 9 | 10 | 421619023 | Гриль контактний→контактный GGM KGKB200 | blknochg (descUA≠descRU, col5==col7 genuine RU) | НЕ тронут (==src) |
| 10 | 11 | 421619025 | Гриль контактний→контактный GGM KGKB300 | blknochg | НЕ тронут (==src) |
| 11 | 12 | 1150098817 | Гриль контактний→контактный Roller Grill MAJESTIC R | blknochg | НЕ тронут (==src) |
| 12 | 13 | 2313017114 | Гриль контактний MARS MTS-20 → Гриль контактный электрический MARS MTS-20 | blknochg | НЕ тронут (==src) |
| 13 | 14 | 971531626 | Гриль контактний Spidocook SP010PR (склокераміка→стеклокерамика) | blknochg | НЕ тронут (==src) |
| 14 | 15 | 1009207703 | Гриль контактний→контактный Pimak М070 електричний→электрический | blknochg | НЕ тронут (==src) |
| 15 | 16 | 1009213198 | Гриль контактний→контактный Pimak М071-1 електричний→электрический | blknochg | НЕ тронут (==src) |
| 16 | 17 | 2204173347 | Гриль контактний→контактный Sirman PD LR-RR | blknochg | НЕ тронут (==src) |

**Все 8 blknochg:** `descUA!=descRU` для каждого SKU, col5 genuine RU == col7, col36 — отдельное чистое RU без UA-маркеров → fixed.xlsx НЕ тронут (0 правок; reopen-verify VERIFY_062_B2 ALL PASS rows 10-17 ==source; b1 SKU4 row5 intact). blk триплет 0 / blknotrip 0 / SKIP-НП 0 (GGM/Roller Grill/MARS/Spidocook/Pimak/Sirman НЕ в НП-списке; первый НП SKU34 HURAKAN в б5).

**Soft-notes (genuine-RU вариативность / артефакты source — НЕ нумеруются, НЕ OQ; blknochg → fixed НЕ тронут, LIVE НЕ переписан):**
- SKU10 GGM KGKB300: source-RU опечатка `нержаеющей` (вместо `нержавеющей`; UA корректно `неіржавкої`). NAME консистентен (GGM KGKB300, col5==col7).
- SKU11 Roller Grill MAJESTIC R: genuine-RU энтити-вариативность — UA `+300 °C` (U+00B0 + C) → RU `+300&deg;С` (энтити `&deg;` + кир. С), byte-exact как в source RU. h2-заголовок сохранён обеими сторонами. NAME консистентен.
- SKU12 MARS MTS-20: имя расширено в RU — col5/col7 `Гриль контактный электрический MARS MTS-20` (UA `Гриль контактний MARS MTS-20`, +«электрический»); модель-код MTS-20 консистентен col5==col7 → soft-note НЕ OQ. source-RU дубль `<li>Индикатор включения; Индикатор включения.</li>` (UA одна `Індикатор увімкнення.`).
- SKU13 Spidocook SP010PR: genuine-RU склейки как в source — `Поверхности:верхняя` (UA `Поверхні: верхня`), `нижняягладкая` (source UA тоже склеено `нижнягладка`); `<br>`→`<br />`; энтити-вариативность `800 °C`→`800 &deg; С`, `400 °C`→`400&deg;С` byte-exact как в source RU. NAME консистентен.
- SKU16 Sirman PD LR-RR: genuine-RU редундантность `Регулируемые верхние плиты с регулировкой` (UA `Регульовані верхні плити` — RU добавляет `с регулировкой`); `<li>Підключення, в 220</li>`→`<li>Подключение, в 220 В</li>` (RU добавляет ` В`, прец. SKU1 б1). NAME консистентен.

---

## Батч 3 (SKU 17-24, openpyxl rows 18-25) — 24/81

**Категории:** blk триплет 1 · blknotrip 1 · blknochg 6 · SKIP-НП 0 · OQ 0.

| SKU | row | ART | Имя (UA→RU) | Категория | fixed.xlsx |
|---|---|---|---|---|---|
| 17 | 18 | 2330328269 | Гриль контактний→контактный електричний→электрический PIMAK М071-2-X | blknochg (descUA≠descRU, col5==col7 genuine RU) | НЕ тронут (==src) |
| 18 | 19 | 971514822 | Гриль контактний→контактный Spidocook SP020R (склокераміка→стеклокерамика) | blknochg | НЕ тронут (==src) |
| 19 | 20 | 971527924 | Гриль контактний→контактный Spidocook SP010PT (склокераміка→стеклокерамика) | blknochg | НЕ тронут (==src) |
| 20 | 21 | 1577135536 | Гриль контактний→контактный SIRMAN CORT LR однопостовой | blknochg | НЕ тронут (==src) |
| 21 | 22 | 2566545482 | Гриль саламандра Bartscher 101552 (lang-neutral) | **blknotrip** (descUA==descRU True, имя lang-neutral) | **только col36 ← RU перевод (851→847); col5 НЕ тронут** |
| 22 | 23 | 675290475 | Гриль контактний→контактный GoodFood ECG11 Panini | blknochg | НЕ тронут (==src) |
| 23 | 24 | 2429608904 | Гриль саламандра GoodFood GS650L (lang-neutral) | blknochg (descUA≠descRU genuine RU) | НЕ тронут (==src) |
| 24 | 25 | 2042441371 | Гриль роликовий Frosty R2-5 → Гриль роликовый Frosty R2-5 | **blk триплет** (descUA==descRU True, col5==col4 UA-leak `роликовий`, col7 genuine RU `роликовый`) | **col5←col7 + col36 tag-в-tag RU (688→685)** |

**blk триплет SKU24 Frosty R2-5:** col5←col7 `Гриль роликовый Frosty R2-5`; col36 = полный tag-в-tag RU перевод source col35 (688→685). Byte-exact: `t&deg;` / `+50/+250&deg;C` энтити verbatim, `0,85 кВт/ 220 В` (запятая-десятич + spacing), `Д * Ш * В`, `585мм x 270мм x 380мм` (Latin x U+0078), `Вес: 12.00` (точка-десятич policy-A), `L=430 мм`. `&#39;` (`рум&#39;яної`/`м&#39;ясних`) → RU plain (`румяной`/`мясных`). skeleton==src, UA-маркеров 0.

**blknotrip SKU21 Bartscher 101552:** имя lang-neutral `Гриль саламандра Bartscher 101552` (col5==col4==col7, без UA-символов) → col5 НЕ тронут; col36 ← полный tag-в-tag RU перевод source col35 (851→847; descUA==descRU был полный UA). Byte-exact: `400х304`/`400х570х515` (кир. х), `1/3` (size-fraction), `3 кВт, 220 В`, `65%`, `41 кг`. `&#39;` (`м&#39;яса`/`пам&#39;яті`) → RU plain. skeleton==src, UA-маркеров 0.

**Soft-notes (genuine-RU вариативность / артефакты source — НЕ нумеруются, НЕ OQ; blknochg → fixed НЕ тронут, LIVE НЕ переписан):**
- SKU18 Spidocook SP020R: genuine-RU `<br>`→`<br />`; энтити-вариативность `800 °C`→`800 &deg; С`, `400 °C`→`400&deg;С` byte как в source RU; source-RU опечатка `рифленная` (двойн. н). NAME консистентен (col5==col7).
- SKU19 Spidocook SP010PT: genuine-RU `<br>`→`<br />`; энтити `800 °C`→`800 &deg; С`, `400 °C`→`400&deg;С`. NAME консистентен.
- SKU20 SIRMAN CORT LR: genuine-RU обёртка `<li><b>…</b></li>` (UA plain `<li>…</li>`) на строке плит; `&ndash;` сохранён обеими сторонами; имя содержит lowercase `однопостовой` (консистентно UA/RU col5==col7). NAME консистентен.
- SKU22 GoodFood ECG11 Panini: genuine-RU энтити-вариативность `50°С-300°С`→`50&deg;С-300&deg;С`. NAME консистентен.
- SKU23 GoodFood GS650L: genuine-RU (descUA≠descRU, col36 чистый RU); имя lang-neutral `Гриль саламандра GoodFood GS650L` (col5==col4==col7). blknochg → fixed НЕ тронут.

---
## Батч 4 (SKU 25-32, openpyxl rows 26-33) — 32/81

**Категории:** blk триплет 4 · blknochg 4 · blknotrip 0 · SKIP-НП 0 · OQ 0.

| SKU | row | ART | Имя (UA→RU) | Категория | fixed.xlsx |
|---|---|---|---|---|---|
| 25 | 26 | 421691093 | Гриль роликовий→роликовый GGM HDGJ7 (HDK7) | blknochg (descUA≠descRU, col5==col7 genuine RU) | НЕ тронут (==src) |
| 26 | 27 | 421691095 | Гриль роликовий→роликовый GGM HDGJ11 | blknochg | НЕ тронут (==src) |
| 27 | 28 | 477239522 | Гриль роликовий→роликовый GoodFood HDRG5 RED | blknochg | НЕ тронут (==src) |
| 28 | 29 | 505240557 | Гриль роликовий→роликовый GoodFood HDRG7 RED | blknochg | НЕ тронут (==src) |
| 29 | 30 | 545492967 | Гриль роликовий AIRHOT RG-5 → Гриль роликовый AIRHOT RG-5 | **blk триплет** (descUA==descRU True, col5==col4 UA-leak `роликовий`, col7 genuine RU `роликовый`) | **col5←col7 + col36 tag-в-tag RU (411→413)** |
| 30 | 31 | 648021543 | Гриль роликовий Hendi 268735 (14 роликів) → Гриль роликовый Hendi 268735 (14 роликов) | **blk триплет** (descUA==descRU True, col5==col4 UA-leak, col7 genuine RU) | **col5←col7 + col36 tag-в-tag RU (677→670)** |
| 31 | 32 | 648044354 | Гриль роликовий Hendi 268506 (7 роликів) → Гриль роликовый Hendi 268506 (7 роликов) | **blk триплет** | **col5←col7 + col36 tag-в-tag RU (603→595)** |
| 32 | 33 | 648048867 | Гриль роликовий Hendi 268605 (9 роликів) → Гриль роликовый Hendi 268605 (9 роликов) | **blk триплет** | **col5←col7 + col36 tag-в-tag RU (603→595)** |

**blk триплет SKU29 AIRHOT RG-5:** col5←col7 `Гриль роликовый AIRHOT RG-5`; col36 = полный tag-в-tag RU перевод source col35 (replace-on-source, 411→413). Byte-exact verbatim: `(°С)` (литер. U+00B0 + кир. С) сохранён, `+50/+300` verbatim, `0,15 кВт`/`0,75 кВт` (запятая-десятич), `220 В`, `45 см`, `580х250х215 мм` (кир. х U+0445). Литер. апостроф `'` (`м'ясних`) → RU plain (`мясных`). skeleton==src, UA-маркеров 0.

**blk триплет SKU30/31/32 Hendi 268735/268506/268605:** col5←col7 `Гриль роликовый Hendi <код> (<N> роликов)`; col36 = полный tag-в-tag RU перевод source col35 (общий roller-grill блок Hendi). SKU30 — 14 роликов, **есть** строка `Раздельное управление ТЭНами (включение только половины роликов)`; SKU31 (7) / SKU32 (9) — этой строки **нет** в source. Byte-exact verbatim PER-SKU: `150°C` (литер. U+00B0 + лат. C), размеры **SKU30 `520x591x175` ЛАТ. x (U+0078)** · **SKU31 `520х325х175` КИР. х (U+0445)** · **SKU32 `520х400х175` КИР. х** — сохранены посимвольно; `1,48`/`0,74`/`0,94 кВт` (запятая-десятич), `42 см`. skeleton==src, UA-маркеров 0.

**Soft-notes (genuine-RU вариативность / артефакты source — НЕ нумеруются, НЕ OQ; blknochg → fixed НЕ тронут, LIVE НЕ переписан):**
- SKU25 GGM HDGJ7 (HDK7): genuine-RU склейка `1.4кВт` (без пробела, точка-десятич; UA источник с пробелом). NAME консистентен (col5==col7 `Гриль роликовый GGM HDGJ7 (HDK7)`). blknochg → fixed НЕ тронут.
- SKU26 GGM HDGJ11: genuine-RU чистый (descUA≠descRU lenUA==lenRU 305). NAME консистентен. blknochg → fixed НЕ тронут.
- SKU27 GoodFood HDRG5 RED: genuine-RU энтити-вариативность `°C`→`&deg;С` (как в source RU). NAME консистентен. blknochg → fixed НЕ тронут.
- SKU28 GoodFood HDRG7 RED: genuine-RU энтити `°C`→`&deg;С`; source-склейка `(3 ролика +4 ролика)` + drop тире (genuine RU артефакт source, UA аналогично). NAME консистентен. blknochg → fixed НЕ тронут.
- SKU30/31/32 Hendi: source UA col35 содержит RU-leak-артефакт `Непрігорающая поверхню роликів` (полу-RU в UA-описании) — переведён в чистый RU `Непригорающая поверхность роликов` в рамках tag-в-tag (blk триплет, не отдельный soft-note: UA-сторона source, не genuine-RU).

---
## Батч 5 (SKU 33-40, openpyxl rows 34-41) — 40/81

**Категории:** blk триплет 4 · blknochg 3 · blknotrip 0 · SKIP-НП 1 · OQ 0.

| SKU | row | ART | Имя (UA→RU) | Категория | fixed.xlsx |
|---|---|---|---|---|---|
| 33 | 34 | 648054935 | Гриль роликовий Hendi 268704 (11 роликів) → Гриль роликовый Hendi 268704 (11 роликов) | **blk триплет** (descUA==descRU True, col5==col4 UA-leak, col7 genuine RU) | **col5←col7 + col36 tag-в-tag RU (677→670)** |
| 34 | 35 | 736117487 | Гриль роликовий HURAKAN HKN-GW7M (7 роликів) | **SKIP-НП #1** (HURAKAN — НП-эксклюзив) | НЕ тронут (тело из фида НП позже) |
| 35 | 36 | 759815061 | Комплект скла→стекла на роликовий→роликовый гриль GoodFood GLASS HDRG5 | blknochg (descUA≠descRU, col5==col7 genuine RU) | НЕ тронут (==src) |
| 36 | 37 | 759815518 | Комплект скла→стекла на роликовий→роликовый гриль GoodFood GLASS HDRG7 | blknochg | НЕ тронут (==src) |
| 37 | 38 | 930800964 | Гриль роликовий→роликовый REEDNEE HDRG-E9-2 | blknochg | НЕ тронут (==src) |
| 38 | 39 | 1110582495 | Гриль роликовий FROSTY WY-005 → Гриль роликовый FROSTY WY-005 | **blk триплет** (descUA==descRU True, col5==col4 UA-leak `роликовий`, col7 genuine RU `роликовый`) | **col5←col7 + col36 tag-в-tag RU (369→376)** |
| 39 | 40 | 1110586122 | Гриль роликовий FROSTY WY-007 → Гриль роликовый FROSTY WY-007 | **blk триплет** | **col5←col7 + col36 tag-в-tag RU (369→376)** |
| 40 | 41 | 1110586977 | Гриль роликовий FROSTY WY-009 → Гриль роликовый FROSTY WY-009 | **blk триплет** | **col5←col7 + col36 tag-в-tag RU (369→376)** |

**blk триплет SKU33 Hendi 268704 (11):** col5←col7 `Гриль роликовый Hendi 268704 (11 роликов)`; col36 = полный tag-в-tag RU перевод source col35 (тот же Hendi roller-grill блок, что b4 SKU30 — **есть** строка `Раздельное управление ТЭНами (включение только половины роликов)`). Byte-exact verbatim: `150°C` (литер. U+00B0 + лат. C), `520x477x175` **ЛАТ. x (U+0078)**, `1,18 кВт` (запятая-десятич), `42 см`. skeleton==src, UA-маркеров 0.

**blk триплет SKU38/39/40 FROSTY WY-005/007/009:** col5←col7 `Гриль роликовый FROSTY WY-00N`; col36 = полный tag-в-tag RU перевод source col35 (общий FROSTY_WY блок). Byte-exact verbatim PER-SKU: размеры **все ЛАТ. x (U+0078)** — SKU38 `590x250x420` · SKU39 `590x330x420` · SKU40 `590x400x420`; мощность **SKU38 `0,96 кВт` ЗАПЯТАЯ-десятич** vs **SKU39 `1.33 кВт` / SKU40 `1.69 кВт` ТОЧКА-десятич** (сохранены как в source, НЕ нормализованы); `50 °C`/`250 °C` (пробел + литер. U+00B0 + лат. C); em-dash `Ролики — хромированная сталь`; `220 В`. skeleton==src (вкл. `\n`-разделители между `<li>`), UA-маркеров 0.

**SKIP-НП SKU34 HURAKAN HKN-GW7M (#1):** бренд HURAKAN — НП-эксклюзив (forward-only приоритет над переводом). RU НЕ переписан, fixed.xlsx row35 НЕ тронут (col5/col36 == source); тело придёт из фида НП позже. Внесён в SKIP-НП-таблицу chunk-062-MANUAL-REVIEW.md строкой #1.

**Soft-notes (genuine-RU вариативность / артефакты source — НЕ нумеруются, НЕ OQ; blknochg → fixed НЕ тронут, LIVE НЕ переписан):**
- SKU35 GoodFood GLASS HDRG5: genuine-RU склейка `4мм` (UA `4 мм` с пробелом); genuine-RU лид сохраняет UA-форму `Комплект стекла на роликовий гриль` / `на гриль роликовый HDRG5` (смешение `роликовий`/`роликовый` — артефакт source genuine RU). NAME консистентен (col5==col7). blknochg → fixed НЕ тронут.
- SKU36 GoodFood GLASS HDRG7: то же (склейка `4мм` + UA-форма `роликовий` в genuine-RU лиде). NAME консистентен. blknochg → fixed НЕ тронут.
- SKU37 REEDNEE HDRG-E9-2: genuine-RU чистый (`Роликовый гриль на 9 роликов, выполненных из нержавеющей стали…`, descUA≠descRU 279/280). NAME консистентен. blknochg → fixed НЕ тронут.

---

## Батч 6 (SKU 41-48, openpyxl rows 42-49) — 48/81

| SKU | row | ART | Бренд | Категория | Действие |
|---|---|---|---|---|---|
| 41 | 42 | 1131859949 | AIRHOT RG-7 | blk триплет | col5←col7 + col36 tag-в-tag RU 671→675 |
| 42 | 43 | 1405209774 | GoodFood HDRG9 RED | blknochg | fixed НЕ тронут==src |
| 43 | 44 | 2042445668 | Frosty R2-7 | blk триплет | col5←col7 + col36 688→685 |
| 44 | 45 | 2042447087 | Frosty R2-9 | blk триплет | col5←col7 + col36 688→685 |
| 45 | 46 | 2042448092 | Frosty WY-011 | blk триплет | col5←col7 + col36 679→676 |
| 46 | 47 | 2084246571 | REEDNEE HDRG-E11-2 | blk триплет | col5←col7 + col36 893→879 |
| 47 | 48 | 2084251135 | REEDNEE HDRG-E7-2 | blk триплет | col5←col7 + col36 933→918 |
| 48 | 49 | 2193257140 | AIRHOT RG-9 | blk триплет | col5←col7 + col36 797→794 |

**blk триплет 7 + blknochg 1.** descUA==descRU True + col5==col4 UA-leak «роликовий» + col7 genuine RU «роликовый» → col5←col7 + col36 tag-в-tag RU перевод source col35 (replace-on-source). byte-exact PER-SKU: AIRHOT RG-7 `0,15 кВт` ЗАПЯТАЯ (lead) vs `1.05 кВт` ТОЧКА (li) · `(°С)` U+00B0+кир.С · `580х330х215` · Frosty R2-7/R2-9 reuse b3 SKU24 R2-5 tmpl (`t&deg;`/`&deg;C`/`1,16`·`1,50 кВт` ЗАПЯТАЯ/`220 В`/Latin x `585мм x …`/Вес dot `14.00`·`16.00`) · Frosty WY-011 `2,06 кВт/ 220В` склеен/Latin x `590мм x 480мм x 420мм`/`17.00` · REEDNEE HDRG-E11-2/E7-2 веса dot (`12.6`/`13`/`9.5`/`10.5`)/`220V` склеен/`Размеры в упаковке`-секция · AIRHOT RG-9 отд. суб-tmpl `+50...+300, &deg;С`/`1.65, кВт`/Latin x `560x410x178`·`610x440x210`. SKIP-НП 0 (следующий НП SKU53/54 в б7). Soft-notes (НЕ нумеруются): SKU42 GoodFood HDRG9 RED genuine RU добавляет clause «выдержит длительные нагрузки» vs UA — NAME консистентен, blknochg fixed НЕ тронут. OQ 0.

---
