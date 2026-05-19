# chunk-061 — ручная проверка для Yana (русский)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-061 (67 SKU)
**Apply key:** `Артикул` (scoped per row)
**Status:** IN PROGRESS 40/67 (blk триплет 20 / blknochg 17 / blknotrip 0 / SKIP-НП 3; Открытых вопросов 0)
**Worker:** W2 (параллельный, диапазон chunk-055 … chunk-085)
**Last updated:** chunk-061 батч 5 (SKU 33-40, openpyxl rows 34-41) — обработан, **40/67**. Категории: **blk триплет 4** (SKU37 Frosty SP-1A1 / SKU38 SP-1A2 / SKU39 SP-1A3 / SKU40 SP-1C1 — col5==col4 UA-leak «контактний» UA-MARK regex False, descUA==descRU True, col7 genuine RU `Гриль контактный Frosty SP-1xx` → col5←col7 + col36 tag-в-tag RU через P1-P16 replace-from-source; reopen-verify col36!=col35 / UA-marker col36+col5 0 / col5==col7 genuineRU; APPLY MISMATCH 0 VERIFY ALL PASS len col36 r38=1030/r39=1134/r40=1136/r41=1134) · **blknochg 4** (SKU33 GoodFood ECG20RR / SKU34 GoodFood ECG201RF / SKU35 SIRMAN PD LR-LR / SKU36 SIRMAN PD RR-RR — descUA!=descRU, col5 уже genuine RU==col7, отдельное чистое RU — LIVE НЕ переписан, fixed rows 34/35/36/37 НЕ тронуты) · blknotrip 0 · **SKIP-НП 0** (NP-suspect остаток chunk-061: SKU48 TATRA EMP.102 Арт `2062003333` — вносится б6 row49). GoodFood/SIRMAN/Frosty НЕ в НП-списке. chunk-061-fixed.xlsx — load СУЩЕСТВУЮЩИЙ (НЕ re-copy), правленых rows этого батча = 4 (38/39/40/41 col5←col7+col36 blk триплет), rows 34/35/36/37 НЕ тронуты (== source), B1-B4 rows intact, reopen-verify OK (APPLY MISMATCH 0 / VERIFY ALL PASS). Открытых вопросов батч не дал: модель-коды NAME UA↔genuine-RU согласованы (GoodFood ECG20RR/ECG201RF; SIRMAN PD LR-LR/RR-RR; Frosty SP-1A1/1A2/1A3/1C1), чужих продуктов нет. Soft-notes (НЕ нумеруются): SKU35 SIRMAN PD LR-LR genuine-RU h2→p даунгрейд заголовка + «прилегают вплотную к плитам» (UA без «вплотную») — внутри-genuine-RU вариативность, NAME консистентен → НЕ рассинхрон · SKU36 RR-RR genuine-RU сохраняет `<h2>` · genuine-RU `&deg;С` entity / em-dash→дефис / `із`→`с` (SKU33/34/35/36 blknochg verbatim, fixed НЕ тронут). Глоссарий: б5 блок добавлен (+2 net-new кумул 452), см. footer chunk-glossary-w2.md. Следующий: chunk-061 батч 6 (SKU 41-48, openpyxl rows 42-49; SKU48 TATRA EMP.102 Арт `2062003333` → SKIP-НП #4).

Здесь собираю всё, что требует твоего подтверждения (не авто-фиксы). Авто-фиксы по locked-паттернам перечислены в сводках по батчам, отдельного подтверждения не требуют. Открытые вопросы накапливаются в нумерованный список и финализируются при закрытии chunk-061. SKIP-НП SKU (НП-эксклюзивные бренды) перечисляются отдельным списком — тело придёт из фида НП позже, RU не трогается.

---

## SKIP-НП chunk-061 (НП-эксклюзивные бренды — RU не переписан)

_(Бренд-состав chunk-061 определяется per-SKU по `Название` (колонка `Бренд` в источнике дублирует числовой `Артикул`, бренд по ней не читается). Зонд chunk-061: **4 NP-suspect hits** в НП-списке HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA → SKIP-НП: **HURAKAN ×3** — SKU28 (Артикул `1147792135`), SKU29 (`1147801726`), SKU30 (`1147802158`); **TATRA ×1** — SKU48 (`2062003333`) — вносятся в таблицу ниже при обработке соответствующих батчей (б4 SKU28·29·30 / б6 SKU48). Прочие бренды (Frosty, SARO, …) НЕ в НП-списке — обрабатываются обычно.)_

| # | SKU | Артикул | Бренд | Название (UA) | Статус |
|---|---|---|---|---|---|
| 1 | 28 | 1147792135 | HURAKAN | Гриль контактний HURAKAN HKN-PE22R | SKIP-НП (тело из фида НП позже) |
| 2 | 29 | 1147801726 | Hurakan | Гриль контактний Hurakan HKN-PE34R | SKIP-НП (тело из фида НП позже) |
| 3 | 30 | 1147802158 | HURAKAN | Гриль контактний HURAKAN HKN-PE44R | SKIP-НП (тело из фида НП позже) |

---

## Открытые вопросы chunk-061

_(нумерация Открытых вопросов chunk-061 — отдельная. Пока 0. Кумул. контекст из других chunk (тоже ждут ответа Yana, НЕ блокируют): OQ#1 SKU 10 chunk-055 Hendi 843468/843499; OQ#1 SKU 67 chunk-056 Nuova Simonelli APPIA II V 1GR ↔ Appia Life V 1Gr рассинхрон модель-кода; OQ#1 SKU 31 chunk-058 Cancan 0103 — чужой товар в лид-абзаце genuine RU; OQ#1 SKU 89 chunk-059 FROSTY FB-010 — col5 чужой продукт + рассинхрон модель-кода 010/FB-010/BL-010Е. Полные версии — в соответствующих chunk-NN-MANUAL-REVIEW.md.)_
