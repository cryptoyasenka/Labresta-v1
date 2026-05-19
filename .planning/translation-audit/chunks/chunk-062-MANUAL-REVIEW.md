# chunk-062 — ручная проверка для Yana (русский)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-062 (81 SKU)
**Apply key:** `Артикул` (scoped per row)
**Status:** IN PROGRESS 24/81 (blk триплет 2 / blknochg 21 / blknotrip 1 / SKIP-НП 0; Открытых вопросов 0)
**Worker:** W2 (параллельный, диапазон chunk-055 … chunk-085)
**Last updated:** chunk-062 батч 3 (SKU 17-24, openpyxl rows 18-25) — обработан, **24/81**. Категории: **blk триплет 1** (SKU24 Frosty R2-5 row25 — descUA==descRU True + col5==col4 UA-leak `роликовий` + col7 genuine RU `роликовый` → col5←col7 `Гриль роликовый Frosty R2-5` + col36 tag-в-tag RU перевод 688→685, `t&deg;`/`+50/+250&deg;C`/`0,85 кВт/ 220 В`/`585мм x 270мм x 380мм` byte-exact, `&#39;`→plain) · **blknotrip 1** (SKU21 Bartscher 101552 row22 — descUA==descRU True, имя lang-neutral `Гриль саламандра Bartscher 101552` без UA-символов → col5 НЕ тронут, только col36 ← RU перевод 851→847, `400х304`/`1/3`/`3 кВт, 220 В` byte-exact, `&#39;`→plain) · **blknochg 6** (SKU17 PIMAK М071-2-X / SKU18 Spidocook SP020R / SKU19 Spidocook SP010PT / SKU20 SIRMAN CORT LR / SKU22 GoodFood ECG11 Panini / SKU23 GoodFood GS650L — descUA!=descRU, col5 genuine/lang-neutral RU==col7, col36 отдельное чистое RU — LIVE НЕ переписан, fixed rows 18/19/20/21/23/24 НЕ тронуты==source) · **SKIP-НП 0** (PIMAK/Spidocook/SIRMAN/Bartscher/GoodFood/Frosty НЕ в НП-списке; первый НП — SKU34 HURAKAN в б5). chunk-062-fixed.xlsx правлен row22 (SKU21 col36) + row25 (SKU24 col5+col36); blknochg rows НЕ тронуты; reopen-verify VERIFY_062_B3 ALL PASS (SKU21/24 ok, col36-UA 0, skeleton==src; b1 SKU4 row5 + b2 rows10-17 intact). Открытых вопросов батч не дал (модель-коды NAME UA↔RU согласованы). Soft-notes (НЕ нумеруются): SKU18 `<br>`→`<br />`+энтити+`рифленная` · SKU19 `<br>`→`<br />`+энтити · SKU20 `<li><b>…</b></li>`-обёртка+`&ndash;` · SKU22 `50°С`→`50&deg;С` · SKU23 lang-neutral имя GoodFood GS650L — все NAME консистентны, blknochg fixed НЕ тронут. Глоссарий: б3 +5 net-new (кумул 468). Следующий: chunk-062 батч SKU 25-32.

Здесь собираю всё, что требует твоего подтверждения (не авто-фиксы). Авто-фиксы по locked-паттернам перечислены в сводках по батчам, отдельного подтверждения не требуют. Открытые вопросы накапливаются в нумерованный список и финализируются при закрытии chunk-062. SKIP-НП SKU (НП-эксклюзивные бренды) перечисляются отдельным списком — тело придёт из фида НП позже, RU не трогается.

---

## SKIP-НП chunk-062 (НП-эксклюзивные бренды — RU не переписан)

_(Бренд-состав chunk-062 определяется per-SKU по `Название` (колонка `Бренд` в источнике дублирует числовой `Артикул`, бренд по ней не читается). Зонд chunk-062: **6 NP-suspect hits** в НП-списке HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA → SKIP-НП: **HURAKAN ×6** — SKU34 (Артикул `736117487`), SKU53 (`2375841678`), SKU54 (`2375848556`), SKU66 (`901422138`), SKU67 (`1168676811`), SKU81 (`2059507443`) — вносятся в таблицу ниже при обработке соответствующих батчей (б5 SKU34 / б7 SKU53·54 / б9 SKU66·67 / б11 SKU81). Прочие бренды (SARO, …) НЕ в НП-списке — обрабатываются обычно.)_

| # | SKU | Артикул | Бренд | Название (UA) | Статус |
|---|---|---|---|---|---|
| _(вносятся при обработке батчей б5 / б7 / б9 / б11)_ | | | | | |

---

## Открытые вопросы chunk-062

_(нумерация Открытых вопросов chunk-062 — отдельная. Пока 0. Кумул. контекст из других chunk (тоже ждут ответа Yana, НЕ блокируют): OQ#1 SKU 10 chunk-055 Hendi 843468/843499; OQ#1 SKU 67 chunk-056 Nuova Simonelli APPIA II V 1GR ↔ Appia Life V 1Gr рассинхрон модель-кода; OQ#1 SKU 31 chunk-058 Cancan 0103 — чужой товар в лид-абзаце genuine RU; OQ#1 SKU 89 chunk-059 FROSTY FB-010 — col5 чужой продукт + рассинхрон модель-кода 010/FB-010/BL-010Е. Полные версии — в соответствующих chunk-NN-MANUAL-REVIEW.md.)_
