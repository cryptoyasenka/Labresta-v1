# chunk-061 — ручная проверка для Yana (русский)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-061 (67 SKU)
**Apply key:** `Артикул` (scoped per row)
**Status:** ЗАКРЫТ 67/67 (blk триплет 29 / blknochg 34 / blknotrip 0 / SKIP-НП 4; Открытых вопросов 0)
**Worker:** W2 (параллельный, диапазон chunk-055 … chunk-085)
**Last updated:** chunk-061 батч 9 (SKU 65-67, openpyxl rows 66-68) — обработан, **ЗАКРЫТ 67/67**. Финальный батч (3 SKU). Категории: blk триплет 0 · **blknochg 3** (SKU65 SARO PG 2 row66 / SKU66 SARO BUSSO T2 row67 / SKU67 SARO BUSSO T1 row68 — descUA!=descRU, col5 уже genuine/lang-neutral RU==col7, отдельное чистое RU — LIVE НЕ переписан, fixed rows 66/67/68 НЕ тронуты == source) · blknotrip 0 · **SKIP-НП 0** (SARO НЕ в НП-списке; SKIP-НП таблица без изменений — остаётся 4: HURAKAN×3 б4 + TATRA×1 SKU48 б6). chunk-061-fixed.xlsx — load СУЩЕСТВУЮЩИЙ, правленых rows этого батча = 0 (все 3 blknochg), B1-B8 rows intact, reopen-verify VERIFY_B9 ALL PASS (rows 66/67/68 fixed==source c5+c36, UA-marker col36 0; b8 rows 60/61/62 intact c5==c7/UA 0/c36!=src; SKIP-НП rows 29/30/31/49 col36 UA-residue ожидаемо). Открытых вопросов батч не дал: модель-коды NAME UA↔RU согласованы (SARO PG 2; SARO BUSSO T2/T1 lang-neutral «Гриль-тостер …»). Soft-notes (НЕ нумеруются): SKU65 SARO PG 2 genuine-RU `<p>Технические характеристики:</p>` (`<strong>` опущен vs UA) + `<li>Подключение, в 220 В</li>` (UA `220`) — NAME консистентен, прец. SKU56 б7 / SKU57 б8 · SKU67 SARO BUSSO T1 `<li>Подключение, в 220 В</li>` (UA `220`) — структурная вариативность genuine RU, NAME консистентен. Глоссарий: б9 footer добавлен (+0 net-new кумул 460 — SARO PG 2/BUSSO T1/T2 genuine RU НЕ переводились, blknochg), см. footer chunk-glossary-w2.md. **chunk-061 ЗАКРЫТ: 67/67 (blk триплет 29 / blknochg 34 / blknotrip 0 / SKIP-НП 4; Открытых вопросов 0). Все 67 SKU rows 2..68 обработаны. Следующий: chunk-062 scaffold (W2, продолжение chunk-061) … chunk-085 (НЕПРЕРЫВНЫЙ режим).**

Здесь собираю всё, что требует твоего подтверждения (не авто-фиксы). Авто-фиксы по locked-паттернам перечислены в сводках по батчам, отдельного подтверждения не требуют. Открытые вопросы накапливаются в нумерованный список и финализируются при закрытии chunk-061. SKIP-НП SKU (НП-эксклюзивные бренды) перечисляются отдельным списком — тело придёт из фида НП позже, RU не трогается.

---

## SKIP-НП chunk-061 (НП-эксклюзивные бренды — RU не переписан)

_(Бренд-состав chunk-061 определяется per-SKU по `Название` (колонка `Бренд` в источнике дублирует числовой `Артикул`, бренд по ней не читается). Зонд chunk-061: **4 NP-suspect hits** в НП-списке HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA → SKIP-НП: **HURAKAN ×3** — SKU28 (Артикул `1147792135`), SKU29 (`1147801726`), SKU30 (`1147802158`); **TATRA ×1** — SKU48 (`2062003333`) — вносятся в таблицу ниже при обработке соответствующих батчей (б4 SKU28·29·30 / б6 SKU48). Прочие бренды (Frosty, SARO, …) НЕ в НП-списке — обрабатываются обычно.)_

| # | SKU | Артикул | Бренд | Название (UA) | Статус |
|---|---|---|---|---|---|
| 1 | 28 | 1147792135 | HURAKAN | Гриль контактний HURAKAN HKN-PE22R | SKIP-НП (тело из фида НП позже) |
| 2 | 29 | 1147801726 | Hurakan | Гриль контактний Hurakan HKN-PE34R | SKIP-НП (тело из фида НП позже) |
| 3 | 30 | 1147802158 | HURAKAN | Гриль контактний HURAKAN HKN-PE44R | SKIP-НП (тело из фида НП позже) |
| 4 | 48 | 2062003333 | TATRA | Гриль контактний TATRA EMP.102 | SKIP-НП (тело из фида НП позже) |

---

## Открытые вопросы chunk-061

_(нумерация Открытых вопросов chunk-061 — отдельная. Пока 0. Кумул. контекст из других chunk (тоже ждут ответа Yana, НЕ блокируют): OQ#1 SKU 10 chunk-055 Hendi 843468/843499; OQ#1 SKU 67 chunk-056 Nuova Simonelli APPIA II V 1GR ↔ Appia Life V 1Gr рассинхрон модель-кода; OQ#1 SKU 31 chunk-058 Cancan 0103 — чужой товар в лид-абзаце genuine RU; OQ#1 SKU 89 chunk-059 FROSTY FB-010 — col5 чужой продукт + рассинхрон модель-кода 010/FB-010/BL-010Е. Полные версии — в соответствующих chunk-NN-MANUAL-REVIEW.md.)_
