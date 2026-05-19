# chunk-061 — ручная проверка для Yana (русский)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-061 (67 SKU)
**Apply key:** `Артикул` (scoped per row)
**Status:** IN PROGRESS 64/67 (blk триплет 29 / blknochg 31 / blknotrip 0 / SKIP-НП 4; Открытых вопросов 0)
**Worker:** W2 (параллельный, диапазон chunk-055 … chunk-085)
**Last updated:** chunk-061 батч 8 (SKU 57-64, openpyxl rows 58-65) — обработан, **64/67**. Категории: **blk триплет 3** (SKU59 Frosty EGS-18FF row60 / SKU60 Frosty EGS-36DF row61 / SKU61 Frosty EGS-44DF row62 — col5==col4 UA-leak «контактний», descUA==descRU True, col7 genuine RU `Гриль контактный …` → col5←col7 + col36 tag-в-tag перевод source col35; преамбула+Технические характеристики byte-идентичны byte-verified RU sibling chunk-061 SKU1 Frosty EGS-44 (b1-committed fixed col36, PRE_RU_FULL substring-assert), спец-блок детерминированно по locked-правилам; reopen-verify col36!=col35 / UA-marker col36+col5 0 / col5==col7 genuineRU; APPLY MISMATCH 0 VERIFY ALL PASS) · **blknochg 5** (SKU57 Silver SS-20 / SKU58 Silver SS-20DН / SKU62 MARS MTS-12G / SKU63 MARS MTS-20G / SKU64 SARO PG 1 — descUA!=descRU, col5 уже genuine RU==col7, отдельное чистое RU — LIVE НЕ переписан, fixed rows 58/59/63/64/65 НЕ тронуты) · blknotrip 0 · **SKIP-НП 0** (Silver/Frosty/MARS/SARO НЕ в НП-списке; SKIP-НП таблица без изменений — остаётся 4: HURAKAN×3 б4 + TATRA×1 SKU48 б6). chunk-061-fixed.xlsx — load СУЩЕСТВУЮЩИЙ (НЕ re-copy), правленых rows этого батча = 3 (60/61/62 col5←col7+col36 blk триплет), rows 58/59/63/64/65 НЕ тронуты (== source), B1-B7 rows intact, reopen-verify OK (APPLY MISMATCH 0 / VERIFY ALL PASS; единственный UA-residue col36 rows 2..65 = rows 29/30/31/49 = SKU28/29/30/48 SKIP-НП, ожидаемо). Открытых вопросов батч не дал: модель-коды NAME UA↔genuine-RU согласованы (Silver SS-20/SS-20DН; Frosty EGS-18FF/EGS-36DF/EGS-44DF; MARS MTS-12G/MTS-20G; SARO PG 1), чужих продуктов нет. Soft-notes (НЕ нумеруются): SKU57 Silver SS-20 genuine-RU `<p>Технические характеристики:</p>` (`<strong>` опущен vs UA) + UA-форма-leak `Тип поверхности ребриста` (ожид. «ребристая») — NAME консистентен, прец. SKU56 б7 / SKU27 б4 / SKU35 б5 · SKU63 MARS MTS-20G genuine RU опускает хвост `<li>Поверхні &ndash; ребристі</li>`+`Однопостовий.` (структурная вариативность, NAME консистентен). Глоссарий: б8 footer добавлен (+0 net-new кумул 460 — Frosty EGS семейство уже в накопл. из 061 б1), см. footer chunk-glossary-w2.md. Следующий: chunk-061 батч 9 (SKU 65-67, openpyxl rows 66-68 — финальный, 3 SKU → 67/67 → закрытие chunk-061).

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
