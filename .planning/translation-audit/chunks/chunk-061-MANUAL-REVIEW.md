# chunk-061 — ручная проверка для Yana (русский)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-061 (67 SKU)
**Apply key:** `Артикул` (scoped per row)
**Status:** IN PROGRESS 16/67 (blk триплет 13 / blknochg 3 / blknotrip 0 / SKIP-НП 0; Открытых вопросов 0)
**Worker:** W2 (параллельный, диапазон chunk-055 … chunk-085)
**Last updated:** chunk-061 батч 2 (SKU 9-16, openpyxl rows 10-17) — обработан, **16/67**. Категории: blk триплет 6 (SKU9 AIRHOT DCG / SKU10 SIRMAN CORT RR / SKU12 Hendi 263600 / SKU13 Hendi 263662 / SKU14 Hendi 263655 / SKU15 Hendi 263808 — col5==col4 UA-форма «контактний»(/ «однопостовий» SKU10) UA-leak при UA-MARK regex False, col7 genuine RU → col5←col7 + col36 полный tag-в-tag RU) · blknochg 2 (SKU11 GoodFood ECG10 Panini RED / SKU16 SILVER 2129 — descUA!=descRU, col5 уже genuine RU == col7, отдельное чистое RU описание — LIVE НЕ переписан, fixed rows 12/17 НЕ тронуты) · blknotrip 0 · SKIP-НП 0. AIRHOT/SIRMAN/GoodFood/Hendi/SILVER НЕ в НП-списке. chunk-061-fixed.xlsx — load СУЩЕСТВУЮЩИЙ (НЕ re-copy), правленых rows этого батча = 6 (10/11/13/14/16 ... 13/14/15/16 col5←col7+col36), rows 12/17 НЕ тронуты, B1 rows 2-9 intact, reopen-verify OK (blk: col36!=col35 & UA-marker col36+col5 0 & col5==col7 genuineRU & col35==src; blknochg rows 12/17 col5/col35/col36==src; B1 spot row2col5/row5 intact; APPLY MISMATCH 0 / VERIFY ALL PASS). Открытых вопросов батч не дал (модель-коды NAME UA↔genuine-RU согласованы, чужих продуктов нет; soft-notes НЕ нумеруются: genuine-RU артефакты `&times;`/`&deg;С`/typo `положениии` SKU11, ё `подойдёт`/`&deg;С` SKU16 — blknochg fixed НЕ тронут). Глоссарий: б2 блок добавлен, кумулятив см. footer chunk-glossary-w2.md. Следующий: chunk-061 батч 3 (SKU 17-24, openpyxl rows 18-25).

Здесь собираю всё, что требует твоего подтверждения (не авто-фиксы). Авто-фиксы по locked-паттернам перечислены в сводках по батчам, отдельного подтверждения не требуют. Открытые вопросы накапливаются в нумерованный список и финализируются при закрытии chunk-061. SKIP-НП SKU (НП-эксклюзивные бренды) перечисляются отдельным списком — тело придёт из фида НП позже, RU не трогается.

---

## SKIP-НП chunk-061 (НП-эксклюзивные бренды — RU не переписан)

_(Бренд-состав chunk-061 определяется per-SKU по `Название` (колонка `Бренд` в источнике дублирует числовой `Артикул`, бренд по ней не читается). Зонд chunk-061: **4 NP-suspect hits** в НП-списке HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA → SKIP-НП: **HURAKAN ×3** — SKU28 (Артикул `1147792135`), SKU29 (`1147801726`), SKU30 (`1147802158`); **TATRA ×1** — SKU48 (`2062003333`) — вносятся в таблицу ниже при обработке соответствующих батчей (б4 SKU28·29·30 / б6 SKU48). Прочие бренды (Frosty, SARO, …) НЕ в НП-списке — обрабатываются обычно.)_

| # | SKU | Артикул | Бренд | Название (UA) | Статус |
|---|---|---|---|---|---|

---

## Открытые вопросы chunk-061

_(нумерация Открытых вопросов chunk-061 — отдельная. Пока 0. Кумул. контекст из других chunk (тоже ждут ответа Yana, НЕ блокируют): OQ#1 SKU 10 chunk-055 Hendi 843468/843499; OQ#1 SKU 67 chunk-056 Nuova Simonelli APPIA II V 1GR ↔ Appia Life V 1Gr рассинхрон модель-кода; OQ#1 SKU 31 chunk-058 Cancan 0103 — чужой товар в лид-абзаце genuine RU; OQ#1 SKU 89 chunk-059 FROSTY FB-010 — col5 чужой продукт + рассинхрон модель-кода 010/FB-010/BL-010Е. Полные версии — в соответствующих chunk-NN-MANUAL-REVIEW.md.)_
