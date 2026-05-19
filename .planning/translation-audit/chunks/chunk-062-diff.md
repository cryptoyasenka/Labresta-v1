# chunk-062 translation diff (81 SKU — грили контактні / роликові / теплові вітрини; W2 диапазон 055-085, продолжение chunk-061)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-062 (81 SKU)
**Apply key:** `Артикул` (scoped per row)
**Status:** IN PROGRESS 16/81 (blk триплет 1 / blknochg 15 / blknotrip 0 / SKIP-НП 0; Открытых вопросов 0)
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
