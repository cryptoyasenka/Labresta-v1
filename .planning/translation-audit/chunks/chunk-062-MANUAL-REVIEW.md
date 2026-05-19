# chunk-062 — ручная проверка для Yana (русский)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-062 (81 SKU)
**Apply key:** `Артикул` (scoped per row)
**Status:** IN PROGRESS 48/81 (blk триплет 17 / blknochg 29 / blknotrip 1 / SKIP-НП 1; Открытых вопросов 0)
**Worker:** W2 (параллельный, диапазон chunk-055 … chunk-085)
**Last updated:** chunk-062 батч 6 (SKU 41-48, openpyxl rows 42-49) — обработан, **48/81**. Категории: **blk триплет 7** (SKU41 AIRHOT RG-7 row42 / SKU43 Frosty R2-7 row44 / SKU44 Frosty R2-9 row45 / SKU45 Frosty WY-011 row46 / SKU46 REEDNEE HDRG-E11-2 row47 / SKU47 REEDNEE HDRG-E7-2 row48 / SKU48 AIRHOT RG-9 row49 — descUA==descRU True + col5==col4 UA-leak «роликовий» + col7 genuine RU «роликовый» → col5←col7 + col36 tag-в-tag RU перевод source col35 replace-on-source; byte-exact PER-SKU: AIRHOT RG-7 `0,15 кВт` ЗАПЯТАЯ lead vs `1.05 кВт` ТОЧКА li / `(°С)` U+00B0+кир.С / `580х330х215`; Frosty R2-7/R2-9 reuse b3 R2-5 tmpl `t&deg;`/`&deg;C`/`1,16`·`1,50 кВт`/`220 В`/Latin x dims/Вес dot 14.00·16.00; Frosty WY-011 `2,06 кВт/ 220В` склеен/Latin x dims/17.00; REEDNEE E11-2/E7-2 веса dot 12.6/13/9.5/10.5 + `220V` склеен + `Размеры в упаковке`-секция; AIRHOT RG-9 отд.суб-tmpl `+50...+300, &deg;С`/`1.65, кВт`/Latin x dims) · **blknotrip 0** · **blknochg 1** (SKU42 GoodFood HDRG9 RED row43 — descUA!=descRU, col5 genuine RU==col7, col36 отдельное чистое RU, fixed row43 НЕ тронут==source) · **SKIP-НП 0** (следующий НП SKU53/54 в б7). chunk-062-fixed.xlsx правлен rows 42/44/45/46/47/48/49 (blk триплет col5←col7+col36); row43 НЕ тронут; reopen-verify VERIFY_062_B6 ALL PASS 66 чеков (b6 + REGR b1 SKU4 / b2 SKU9-16 / b3 SKU21·SKU24 / b4 SKU25-32 / b5 SKU33-40·SKU34 SKIP-НП — все intact, col36-UA 0, skeleton==src). Открытых вопросов батч не дал (модель-коды NAME UA↔RU согласованы). Soft-notes (НЕ нумеруются): SKU42 GoodFood HDRG9 RED genuine RU добавляет «выдержит длительные нагрузки» vs UA — NAME консистентен blknochg fixed НЕ тронут. Глоссарий: б6 +4 net-new (кумул 483). Следующий: chunk-062 батч SKU 49-56 (NP-чек: SKU53 row54 + SKU54 row55 HURAKAN → SKIP-НП #2/#3).

Здесь собираю всё, что требует твоего подтверждения (не авто-фиксы). Авто-фиксы по locked-паттернам перечислены в сводках по батчам, отдельного подтверждения не требуют. Открытые вопросы накапливаются в нумерованный список и финализируются при закрытии chunk-062. SKIP-НП SKU (НП-эксклюзивные бренды) перечисляются отдельным списком — тело придёт из фида НП позже, RU не трогается.

---

## SKIP-НП chunk-062 (НП-эксклюзивные бренды — RU не переписан)

_(Бренд-состав chunk-062 определяется per-SKU по `Название` (колонка `Бренд` в источнике дублирует числовой `Артикул`, бренд по ней не читается). Зонд chunk-062: **6 NP-suspect hits** в НП-списке HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA → SKIP-НП: **HURAKAN ×6** — SKU34 (Артикул `736117487`), SKU53 (`2375841678`), SKU54 (`2375848556`), SKU66 (`901422138`), SKU67 (`1168676811`), SKU81 (`2059507443`) — вносятся в таблицу ниже при обработке соответствующих батчей (б5 SKU34 / б7 SKU53·54 / б9 SKU66·67 / б11 SKU81). Прочие бренды (SARO, …) НЕ в НП-списке — обрабатываются обычно.)_

| # | SKU | Артикул | Бренд | Название (UA) | Статус |
|---|---|---|---|---|---|
| 1 | 34 | 736117487 | HURAKAN | Гриль роликовий HURAKAN HKN-GW7M (7 роликів) | SKIP-НП (тело из фида НП позже) |
| _(б7 SKU53·54 / б9 SKU66·67 / б11 SKU81)_ | | | | | |

---

## Открытые вопросы chunk-062

_(нумерация Открытых вопросов chunk-062 — отдельная. Пока 0. Кумул. контекст из других chunk (тоже ждут ответа Yana, НЕ блокируют): OQ#1 SKU 10 chunk-055 Hendi 843468/843499; OQ#1 SKU 67 chunk-056 Nuova Simonelli APPIA II V 1GR ↔ Appia Life V 1Gr рассинхрон модель-кода; OQ#1 SKU 31 chunk-058 Cancan 0103 — чужой товар в лид-абзаце genuine RU; OQ#1 SKU 89 chunk-059 FROSTY FB-010 — col5 чужой продукт + рассинхрон модель-кода 010/FB-010/BL-010Е. Полные версии — в соответствующих chunk-NN-MANUAL-REVIEW.md.)_
