# chunk-062 — ручная проверка для Yana (русский)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-062 (81 SKU)
**Apply key:** `Артикул` (scoped per row)
**Status:** IN PROGRESS 64/81 (blk триплет 22 / blknochg 38 / blknotrip 1 / SKIP-НП 3; Открытых вопросов 0)
**Worker:** W2 (параллельный, диапазон chunk-055 … chunk-085)
**Last updated:** chunk-062 батч 8 (SKU 57-64, openpyxl rows 58-65) — обработан, **64/81**. Категории: **blk триплет 2** (SKU58 Fimar Easy Line FY011 row59 / SKU59 EWT INOX HDRG-E7-2 row60 — descUA==descRU True + col5==col4 UA-leak «роликовий» + col7 genuine RU «роликовый» → col5←col7 + col36 tag-в-tag RU перевод source col35 replace-on-source; byte-exact PER-SKU: Fimar `&#39;` сняты, `Подвійний термостат`→`Двойной термостат`, `Підключення до електромережі: 220V`→`Подключение к электросети: 220V` 220V verbatim, `2.2` точка verbatim, секция «Розміри в упаковці»→«Размеры в упаковке», Ширина==Ширина не трогалась; EWT `1,4 кВт` запятая verbatim, `Габарити: Ш 325 х Г 550 х В 175 мм`→«Габариты:» кир.х U+0445 + Ш/Г/В verbatim) · **blknotrip 0** · **blknochg 6** (SKU57 Roller Grill RG 11 row58 / SKU60 GoodFood HDRG11 RED row61 / SKU61 GoodFood HDRG14 RED row62 / SKU62 Комплект стекла GoodFood HDRG9 row63 / SKU63 Frosty RTR-97L-2 row64 / SKU64 Frosty RTR-158L row65 — descUA!=descRU, col5 genuine RU==col7, col36 отдельное чистое RU, fixed rows 58/61/62/63/64/65 НЕ тронуты==source) · **SKIP-НП 0**. chunk-062-fixed.xlsx правлен rows 59/60 (blk триплет col5←col7+col36); rows 58/61/62/63/64/65 НЕ тронуты; reopen-verify VERIFY_062_B8 ALL PASS 78 чеков (b8 + REGR b1 SKU4 / b2 SKU9-16 / b3 SKU21·SKU24 / b4 SKU25-32 / b5 SKU33-40 / b6 SKU41-48 / b7 SKU49-57 — все intact, col36-UA 0, skeleton==src). Открытых вопросов батч не дал (модель-коды NAME UA↔RU согласованы). Soft-notes (НЕ нумеруются): SKU58 Fimar секция «Розміри в упаковці» дублирует размеры (нетто) — RU зеркалит UA-структуру tag-в-tag; SKU57 Roller Grill `&Oslash;` entity + RU «съёмный» с ё (blknochg НЕ трогаем, house-style no-ё к genuine RU не применяем); SKU63/64 Frosty pre-existing RU артефакты «вращяющиеся»/«обьем» (blknochg genuine RU НЕ переводились/НЕ правились). Глоссарий: б8 +2 net-new (кумул 487). Следующий: chunk-062 батч SKU 65-72 (NP-чек: SKU66 row67 + SKU67 row68 HURAKAN → SKIP-НП #4/#5 в этом батче б9).

Здесь собираю всё, что требует твоего подтверждения (не авто-фиксы). Авто-фиксы по locked-паттернам перечислены в сводках по батчам, отдельного подтверждения не требуют. Открытые вопросы накапливаются в нумерованный список и финализируются при закрытии chunk-062. SKIP-НП SKU (НП-эксклюзивные бренды) перечисляются отдельным списком — тело придёт из фида НП позже, RU не трогается.

---

## SKIP-НП chunk-062 (НП-эксклюзивные бренды — RU не переписан)

_(Бренд-состав chunk-062 определяется per-SKU по `Название` (колонка `Бренд` в источнике дублирует числовой `Артикул`, бренд по ней не читается). Зонд chunk-062: **6 NP-suspect hits** в НП-списке HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA → SKIP-НП: **HURAKAN ×6** — SKU34 (Артикул `736117487`), SKU53 (`2375841678`), SKU54 (`2375848556`), SKU66 (`901422138`), SKU67 (`1168676811`), SKU81 (`2059507443`) — вносятся в таблицу ниже при обработке соответствующих батчей (б5 SKU34 / б7 SKU53·54 / б9 SKU66·67 / б11 SKU81). Прочие бренды (SARO, …) НЕ в НП-списке — обрабатываются обычно.)_

| # | SKU | Артикул | Бренд | Название (UA) | Статус |
|---|---|---|---|---|---|
| 1 | 34 | 736117487 | HURAKAN | Гриль роликовий HURAKAN HKN-GW7M (7 роликів) | SKIP-НП (тело из фида НП позже) |
| 2 | 53 | 2375841678 | HURAKAN | Гриль роликовий HURAKAN HKN-GW11M 11 роликів | SKIP-НП (тело из фида НП позже) |
| 3 | 54 | 2375848556 | HURAKAN | Гриль роликовий HURAKAN HKN-GW9M 9 роликів | SKIP-НП (тело из фида НП позже) |
| _(б9 SKU66·67 / б11 SKU81)_ | | | | | |

---

## Открытые вопросы chunk-062

_(нумерация Открытых вопросов chunk-062 — отдельная. Пока 0. Кумул. контекст из других chunk (тоже ждут ответа Yana, НЕ блокируют): OQ#1 SKU 10 chunk-055 Hendi 843468/843499; OQ#1 SKU 67 chunk-056 Nuova Simonelli APPIA II V 1GR ↔ Appia Life V 1Gr рассинхрон модель-кода; OQ#1 SKU 31 chunk-058 Cancan 0103 — чужой товар в лид-абзаце genuine RU; OQ#1 SKU 89 chunk-059 FROSTY FB-010 — col5 чужой продукт + рассинхрон модель-кода 010/FB-010/BL-010Е. Полные версии — в соответствующих chunk-NN-MANUAL-REVIEW.md.)_
