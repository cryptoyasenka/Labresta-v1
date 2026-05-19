# chunk-060 — ручная проверка для Yana (русский)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-060 (81 SKU)
**Apply key:** `Артикул` (scoped per row)
**Status:** IN PROGRESS 16/81 (blk триплет 3 / blknochg 6 / blknotrip 6 / SKIP-НП 1; Открытых вопросов 0)
**Worker:** W2 (параллельный, диапазон chunk-055 … chunk-085)
**Last updated:** chunk-060 батч 2 (SKU 9-16, openpyxl rows 10..17) — обработан, 16/81. Категории: blknochg 4 (SKU9 Hamilton Beach HBH755CE / SKU10 GoodFood PROFI BL2500 / SKU11 GoodFood PROFI BL3900 / SKU16 GoodFood BL2000 SOFT — descUA!=descRU genuine отдельный RU, fixed НЕ тронут) · blknotrip 4 (SKU12 Hamilton Beach HBF1100SCE / SKU13 HBF600CE / SKU14 HBB255CE / SKU15 HBB255SCE — col4==col5==col6==col7 бренд+код language-neutral, descUA==descRU UA-leak в desc → только col36 переведён tag-в-tag, col5 оставлен) · blk триплет 0 · SKIP-НП 0 (HURAKAN в SKU 9-16 нет, следующий SKU22 б3). chunk-060-fixed.xlsx загружен СУЩЕСТВУЮЩИЙ (НЕ копировался), правленых rows этого батча = 4 (13/14/15/16, col36-only), reopen-verify OK (col36!=col35, UA-marker DSCRU 0, col5==srcCol5 language-neutral; blknochg rows 10/11/12/17 не тронуты col35==src & col36==src; prior b1 rows 3/4/5/6/9 целы). Открытых вопросов батч не дал. Глоссарий +N кумул. Следующий: chunk-060 батч SKU 17-24 (openpyxl rows 18..25; SKIP-НП SKU22 ART2111152648 Hurakan HKN-BLW2 grey #2). _(пред.: батч 1 SKU 1-8 8/81 — blk триплет 3 SKU2/5/8 + blknotrip 2 SKU3/4 + blknochg 2 SKU1/7 + SKIP-НП 1 SKU6 таблица #1; chunk-060-fixed.xlsx создан Copy-Item, rows 3/4/5/6/9 reopen-verify OK; C1 01ea0ce.)_

Здесь собираю всё, что требует твоего подтверждения (не авто-фиксы). Авто-фиксы по locked-паттернам перечислены в сводках по батчам, отдельного подтверждения не требуют. Открытые вопросы накапливаются в нумерованный список и финализируются при закрытии chunk-060. SKIP-НП SKU (НП-эксклюзивные бренды) перечисляются отдельным списком — тело придёт из фида НП позже, RU не трогается.

---

## SKIP-НП chunk-060 (НП-эксклюзивные бренды — RU не переписан)

_(Бренд-состав chunk-060 определяется per-SKU по `Название` (колонка `Бренд` в источнике дублирует числовой `Артикул`, бренд по ней не читается). Зонд chunk-060: **8 NP-suspect hits** в НП-списке HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA → SKIP-НП: **HURAKAN ×8** — SKU6 (Артикул `732422924`), SKU22 (`2111152648`), SKU30 (`2503647283`), SKU31 (`2503651061`), SKU33 (`2566515692`), SKU49 (`1133814407`), SKU65 (`2599060225`), SKU73 (`1147786691`) — вносятся в таблицу ниже при обработке соответствующих батчей (б1 SKU6 / б3 SKU22 / б4 SKU30·31 / б5 SKU33 / б7 SKU49 / б9 SKU65 / б10 SKU73). **AIRHOT НЕ в НП-списке** (SKU48 `Подрібнювач льоду AIRHOT IC-1`, SKU72 `Гриль контактний AIRHOT CGL`) — обработан обычно. Прочие бренды (Sirman, REEDNEE, Hendi, Hamilton Beach, EWT INOX, GoodFood, Frosty, Ceado/CEADO, Bartscher, SARO, Fimar, Vema, …) НЕ в НП-списке — обработаны обычно.)_

| # | SKU | Артикул | Бренд | Название (UA) | Статус |
|---|---|---|---|---|---|
| 1 | SKU6 | 732422924 | HURAKAN | Блендер HURAKAN HKN-BLW2 grey\red | SKIP-НП (тело придёт из фида НП позже, RU не трогался) |

---

## Открытые вопросы chunk-060

_(нумерация Открытых вопросов chunk-060 — отдельная. Пока 0. Кумул. контекст из других chunk (тоже ждут ответа Yana): OQ#1 SKU 10 chunk-055 Hendi 843468/843499; OQ#1 SKU 67 chunk-056 Nuova Simonelli APPIA II V 1GR ↔ Appia Life V 1Gr рассинхрон модель-кода; OQ#1 SKU 31 chunk-058 Cancan 0103 — чужой товар в лид-абзаце genuine RU; OQ#1 SKU 89 chunk-059 FROSTY FB-010 — col5 чужой продукт + рассинхрон модель-кода 010/FB-010/BL-010Е. Полные версии — в соответствующих chunk-NN-MANUAL-REVIEW.md.)_
