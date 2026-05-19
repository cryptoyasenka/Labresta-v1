# chunk-061 — ручная проверка для Yana (русский)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-061 (67 SKU)
**Apply key:** `Артикул` (scoped per row)
**Status:** IN PROGRESS 8/67 (blk триплет 7 / blknochg 1 / blknotrip 0 / SKIP-НП 0; Открытых вопросов 0)
**Worker:** W2 (параллельный, диапазон chunk-055 … chunk-085)
**Last updated:** chunk-061 батч 1 (SKU 1-8, openpyxl rows 2-9) — обработан, **8/67**. Категории: blk триплет 7 (SKU1 Frosty EGS-44 / SKU2 EGS-44FF — семейство chunk-060 б10/б11, LEAD/TAIL byte-verified из RU sibling chunk-060 SKU80 EGS-36; SKU3 EWT INOX CGR811E; SKU5 Bartscher A150670; SKU6 Bartscher A150674; SKU7 REEDNEE CGR11; SKU8 AIRHOT CG — все col5==col4 UA-форма «контактний» UA-leak, col7 genuine RU → col5←col7 + col36 полный tag-в-tag RU) · blknochg 1 (SKU4 Гриль контактний Spidocook SP020PR (склокераміка) — descUA!=descRU, NMRU/col7 уже genuine RU `Гриль контактный Spidocook SP020PR (стеклокерамика)`, отдельное чистое RU SHB Plus/стеклокерамика — LIVE НЕ переписан, fixed row 5 НЕ тронут) · blknotrip 0 · SKIP-НП 0. AIRHOT/Frosty/Bartscher/REEDNEE/EWT INOX/Spidocook НЕ в НП-списке. chunk-061-fixed.xlsx СОЗДАН (Copy-Item из source, первый батч с правками), правленых rows этого батча = 7 (2/3/4/6/7/8/9 col5←col7+col36), row 5 SKU4 НЕ тронут, reopen-verify OK (blk: col36!=col35 & UA-marker col36+col5 0 & col5==col7 genuineRU & col35==src; SKU1/2 FAM_LEAD/FAM_TAIL byte == chunk-060 SKU80 RU; blknochg row5 col5/col35/col36==src; APPLY MISMATCH 0 / VERIFY ALL PASS). Открытых вопросов батч не дал (модель-код NAME UA↔genuine-RU согласован, чужих продуктов нет; soft-notes НЕ нумеруются: typo «Смачна»=«Смажна»→жарочная SKU6, genuine-RU артефакт `&deg; С`/`<br />` SKU4). Глоссарий: +6 net-new (рифленая из чугуна · точек фаст фуд · Страна производитель · Подключение к электросети · Регулируемый термостат · ВКЛ/ВЫКЛ on/off; Frosty EGS family-reuse +0), кумулятив 438. Следующий: chunk-061 батч 2 (SKU 9-16, openpyxl rows 10-17).

Здесь собираю всё, что требует твоего подтверждения (не авто-фиксы). Авто-фиксы по locked-паттернам перечислены в сводках по батчам, отдельного подтверждения не требуют. Открытые вопросы накапливаются в нумерованный список и финализируются при закрытии chunk-061. SKIP-НП SKU (НП-эксклюзивные бренды) перечисляются отдельным списком — тело придёт из фида НП позже, RU не трогается.

---

## SKIP-НП chunk-061 (НП-эксклюзивные бренды — RU не переписан)

_(Бренд-состав chunk-061 определяется per-SKU по `Название` (колонка `Бренд` в источнике дублирует числовой `Артикул`, бренд по ней не читается). Зонд chunk-061: **4 NP-suspect hits** в НП-списке HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA → SKIP-НП: **HURAKAN ×3** — SKU28 (Артикул `1147792135`), SKU29 (`1147801726`), SKU30 (`1147802158`); **TATRA ×1** — SKU48 (`2062003333`) — вносятся в таблицу ниже при обработке соответствующих батчей (б4 SKU28·29·30 / б6 SKU48). Прочие бренды (Frosty, SARO, …) НЕ в НП-списке — обрабатываются обычно.)_

| # | SKU | Артикул | Бренд | Название (UA) | Статус |
|---|---|---|---|---|---|

---

## Открытые вопросы chunk-061

_(нумерация Открытых вопросов chunk-061 — отдельная. Пока 0. Кумул. контекст из других chunk (тоже ждут ответа Yana, НЕ блокируют): OQ#1 SKU 10 chunk-055 Hendi 843468/843499; OQ#1 SKU 67 chunk-056 Nuova Simonelli APPIA II V 1GR ↔ Appia Life V 1Gr рассинхрон модель-кода; OQ#1 SKU 31 chunk-058 Cancan 0103 — чужой товар в лид-абзаце genuine RU; OQ#1 SKU 89 chunk-059 FROSTY FB-010 — col5 чужой продукт + рассинхрон модель-кода 010/FB-010/BL-010Е. Полные версии — в соответствующих chunk-NN-MANUAL-REVIEW.md.)_
