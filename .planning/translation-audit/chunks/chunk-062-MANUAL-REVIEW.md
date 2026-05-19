# chunk-062 — ручная проверка для Yana (русский)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-062 (81 SKU)
**Apply key:** `Артикул` (scoped per row)
**Status:** IN PROGRESS 72/81 (blk триплет 27 / blknochg 39 / blknotrip 1 / SKIP-НП 5; Открытых вопросов 0)
**Worker:** W2 (параллельный, диапазон chunk-055 … chunk-085)
**Last updated:** chunk-062 батч 9 (SKU 65-72, openpyxl rows 66-73) — обработан, **72/81**. Категории: **blk триплет 5** (SKU68 Frosty SWS-3S row69 / SKU69 Frosty SWS-580 row70 / SKU70 EWT INOX BM2 row71 / SKU71 Frosty RTR-120L row72 / SKU72 Frosty RTR-160L row73 — descUA==descRU True + col5==col4 UA-leak «Вітрина теплова» + col7 genuine RU «Витрина тепловая» → col5←col7 + col36 tag-в-tag RU перевод replace-on-source; byte-exact PER-SKU: SWS `+30&deg;С до +85&deg;C` кир.С/лат.C verbatim, `0,80`/`0,8 кВт/ 220В` запятая+glued, лат.x размеры, `Вага:`→`Вес:` точка, висячие пробелы в li сохранены; EWT/RTR `°C` U+00B0+лат.C, RTR `об'ємом`→«объемом») · **blknotrip 0** · **blknochg 1** (SKU65 FROSTY RTR-137L row66 — descUA!=descRU, col5 genuine RU==col7, col36 отдельное чистое RU, fixed row66 НЕ тронут==source) · **SKIP-НП 2** (SKU66 HURAKAN HKN-WD2 row67 Артикул 901422138 #4 / SKU67 HURAKAN HKN-WD3M row68 Артикул 1168676811 #5 — НП-эксклюзив forward-only, RU НЕ переписан, fixed rows 67/68 НЕ тронуты, тело из НП-фида позже). chunk-062-fixed.xlsx правлен rows 69/70/71/72/73 (blk триплет col5←col7+col36); rows 66/67/68 НЕ тронуты; reopen-verify VERIFY_062_B9 ALL PASS (b9 + REGR b1-b8 intact, col36-UA 0, skeleton==src). Открытых вопросов батч не дал (модель-коды NAME UA↔RU согласованы). Soft-notes (НЕ нумеруются): SKU65 FROSTY RTR-137L pre-existing genuine RU артефакт «обьем» + знак ℃ U+2103 (blknochg НЕ трогаем); SKU69 Frosty SWS-580 «Тени з термостатом»→«Тэны с термостатом» (ТЕН→ТЭН). Глоссарий: б9 +2 net-new (кумул 489). Следующий: chunk-062 батч SKU 73-80 (NP-чек: в б10 НП нет — последний НП SKU81 row82 HURAKAN → SKIP-НП #6 в б11 финал).

Здесь собираю всё, что требует твоего подтверждения (не авто-фиксы). Авто-фиксы по locked-паттернам перечислены в сводках по батчам, отдельного подтверждения не требуют. Открытые вопросы накапливаются в нумерованный список и финализируются при закрытии chunk-062. SKIP-НП SKU (НП-эксклюзивные бренды) перечисляются отдельным списком — тело придёт из фида НП позже, RU не трогается.

---

## SKIP-НП chunk-062 (НП-эксклюзивные бренды — RU не переписан)

_(Бренд-состав chunk-062 определяется per-SKU по `Название` (колонка `Бренд` в источнике дублирует числовой `Артикул`, бренд по ней не читается). Зонд chunk-062: **6 NP-suspect hits** в НП-списке HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA → SKIP-НП: **HURAKAN ×6** — SKU34 (Артикул `736117487`), SKU53 (`2375841678`), SKU54 (`2375848556`), SKU66 (`901422138`), SKU67 (`1168676811`), SKU81 (`2059507443`) — вносятся в таблицу ниже при обработке соответствующих батчей (б5 SKU34 / б7 SKU53·54 / б9 SKU66·67 / б11 SKU81). Прочие бренды (SARO, …) НЕ в НП-списке — обрабатываются обычно.)_

| # | SKU | Артикул | Бренд | Название (UA) | Статус |
|---|---|---|---|---|---|
| 1 | 34 | 736117487 | HURAKAN | Гриль роликовий HURAKAN HKN-GW7M (7 роликів) | SKIP-НП (тело из фида НП позже) |
| 2 | 53 | 2375841678 | HURAKAN | Гриль роликовий HURAKAN HKN-GW11M 11 роликів | SKIP-НП (тело из фида НП позже) |
| 3 | 54 | 2375848556 | HURAKAN | Гриль роликовий HURAKAN HKN-GW9M 9 роликів | SKIP-НП (тело из фида НП позже) |
| 4 | 66 | 901422138 | HURAKAN | Теплова вітрина HURAKAN HKN-WD2 | SKIP-НП (тело из фида НП позже) |
| 5 | 67 | 1168676811 | HURAKAN | Теплова вітрина HURAKAN HKN-WD3M | SKIP-НП (тело из фида НП позже) |
| _(б11 SKU81)_ | | | | | |

---

## Открытые вопросы chunk-062

_(нумерация Открытых вопросов chunk-062 — отдельная. Пока 0. Кумул. контекст из других chunk (тоже ждут ответа Yana, НЕ блокируют): OQ#1 SKU 10 chunk-055 Hendi 843468/843499; OQ#1 SKU 67 chunk-056 Nuova Simonelli APPIA II V 1GR ↔ Appia Life V 1Gr рассинхрон модель-кода; OQ#1 SKU 31 chunk-058 Cancan 0103 — чужой товар в лид-абзаце genuine RU; OQ#1 SKU 89 chunk-059 FROSTY FB-010 — col5 чужой продукт + рассинхрон модель-кода 010/FB-010/BL-010Е. Полные версии — в соответствующих chunk-NN-MANUAL-REVIEW.md.)_
