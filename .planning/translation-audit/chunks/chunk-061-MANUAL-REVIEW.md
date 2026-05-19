# chunk-061 — ручная проверка для Yana (русский)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-061 (67 SKU)
**Apply key:** `Артикул` (scoped per row)
**Status:** IN PROGRESS 32/67 (blk триплет 16 / blknochg 13 / blknotrip 0 / SKIP-НП 3; Открытых вопросов 0)
**Worker:** W2 (параллельный, диапазон chunk-055 … chunk-085)
**Last updated:** chunk-061 батч 4 (SKU 25-32, openpyxl rows 26-33) — обработан, **32/67**. Категории: **blk триплет 3** (SKU26 Hendi 263501 / SKU27 Hendi 263907 / SKU31 Hendi 263709 — col5==col4 UA-leak «контактний», descUA==descRU True, col7 genuine RU → col5←col7 + col36 tag-в-tag RU; reopen-verify col36!=col35 / UA-marker col36+col5 0 / col5==col7 genuineRU; APPLY MISMATCH 0 VERIFY ALL PASS) · **blknochg 2** (SKU25 SILVER 2130/1 / SKU32 Spidocook SP015PR — descUA!=descRU, col5 уже genuine RU==col7, отдельное чистое RU — LIVE НЕ переписан, fixed rows 26/33 НЕ тронуты) · blknotrip 0 · **SKIP-НП 3** (SKU28 HKN-PE22R / SKU29 HKN-PE34R / SKU30 HKN-PE44R — HURAKAN, НП-эксклюзив, RU не переписан, fixed rows 29/30/31 НЕ тронуты, тело придёт из фида НП позже — внесены в SKIP-НП-таблицу #1/#2/#3). Hendi/SILVER/Spidocook НЕ в НП-списке. chunk-061-fixed.xlsx — load СУЩЕСТВУЮЩИЙ (НЕ re-copy), правленых rows этого батча = 3 (27/28/32 col5←col7+col36 blk триплет), rows 26/29/30/31/33 НЕ тронуты (== source), B1-B3 rows intact, reopen-verify OK (APPLY MISMATCH 0 / VERIFY ALL PASS). Открытых вопросов батч не дал: модель-коды NAME UA↔genuine-RU согласованы (Hendi 263501/263907/263709; SILVER 2130/1; Spidocook SP015PR), чужих продуктов нет. Soft-notes (НЕ нумеруются): SKU27 тело-лид ссылается на sibling-модель «Hendi 263808» (артефакт копипаста исходной UA-копии, NAME 263907 согласован → НЕ рассинхрон, переведено verbatim) · genuine-RU артефакты `&deg;С`/`&deg;C`/`&sup3;`/`<br />`/`800 &deg; С`/`3.0 кВт`/no-space-двоеточие (SKU25/SKU31/SKU32 blknochg+blk триплет verbatim, fixed НЕ тронут где blknochg). Глоссарий: б4 блок добавлен (+2 net-new кумул 450), см. footer chunk-glossary-w2.md. Следующий: chunk-061 батч 5 (SKU 33-40, openpyxl rows 34-41).

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
