# chunk-062 — ручная проверка для Yana (русский)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-062 (81 SKU)
**Apply key:** `Артикул` (scoped per row)
**Status:** IN PROGRESS 8/81 (blk триплет 1 / blknochg 7 / blknotrip 0 / SKIP-НП 0; Открытых вопросов 0)
**Worker:** W2 (параллельный, диапазон chunk-055 … chunk-085)
**Last updated:** chunk-062 батч 1 (SKU 1-8, openpyxl rows 2-9) — обработан, **8/81**. Категории: **blk триплет 1** (SKU4 EWT INOX CGR811EB row5 — descUA==descRU True + col5==col4 UA-leak + col7 genuine RU → col5←col7 `Гриль контактный EWT INOX CGR811EB` + col36 tag-в-tag RU перевод source col35 692→700, `℃`/`220V` byte-exact verbatim) · **blknochg 7** (SKU1 SARO PG 1B / SKU2 SILVER SS-20D / SKU3 SILVER 2131/1 / SKU5 GoodFood GS300 / SKU6 GoodFood GSEG58 / SKU7 GoodFood HGM01 / SKU8 GoodFood HGM02 — descUA!=descRU, col5 genuine/lang-neutral RU==col7, отдельное чистое RU — LIVE НЕ переписан, fixed rows 2/3/4/6/7/8/9 НЕ тронуты==source) · blknotrip 0 · **SKIP-НП 0** (SARO/SILVER/EWT INOX/GoodFood НЕ в НП-списке; первый НП — SKU34 HURAKAN в б5; SKIP-НП таблица без изменений). chunk-062-fixed.xlsx СОЗДАН в б1 (`cp chunk-062.xlsx chunk-062-fixed.xlsx`), правлен row5 (SKU4), reopen-verify VERIFY_062_B1 ALL PASS (SKU4 c5==c7/c36 ok/UA-marker 0; blknochg rows 2/3/4/6/7/8/9 fixed==source). Открытых вопросов батч не дал (модель-коды NAME UA↔RU согласованы). Soft-notes (НЕ нумеруются): SKU1 `Підключення, в 220`→`Подключение, в 220 В` + `&#39;`→plain + `&laquo;&raquo;` (genuine-RU вариативность, прец. SKU65 б9 c061) · SKU2 source-RU дубль `Пластиковая защита верхней пружины` ×2 · SKU3 склейка `.Верхняя` (артефакт source UA+RU) — NAME консистентен, blknochg fixed НЕ тронут. Глоссарий: б1 footer +3 net-new (кумул 463). Следующий: chunk-062 батч SKU 9-16.

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
