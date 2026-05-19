# chunk-060 — ручная проверка для Yana (русский)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-060 (81 SKU)
**Apply key:** `Артикул` (scoped per row)
**Status:** IN PROGRESS 32/81 (blk триплет 8 / blknochg 9 / blknotrip 11 / SKIP-НП 4; Открытых вопросов 0)
**Worker:** W2 (параллельный, диапазон chunk-055 … chunk-085)
**Last updated:** chunk-060 батч 4 (SKU 25-32, openpyxl rows 26..33) — обработан, 32/81. Категории: blknotrip 3 (SKU25 Hamilton Beach HBF600SCE / SKU26 HBH455CE / SKU29 Bartscher 150182 — col4==col5==col6==col7 бренд+код language-neutral, descUA==descRU UA-leak → только col36, col5 оставлен) · blknochg 3 (SKU27 GoodFood BL1500 / SKU28 BL1500 COVER / SKU32 SARO TM-800 Black — descUA!=descRU genuine отдельное RU уже есть → fixed НЕ тронут; SKU32 genuine RU обёрнут в Google-Translate-виджет-артефакт, не правим/не нумеруем, прец. SKU18/38/39/85) · SKIP-НП 2 (SKU30 Hurakan HKN-HBH2000S #3 / SKU31 Hurakan HKN-HBH2000STH #4 — таблица) · blk триплет 0. chunk-060-fixed.xlsx загружен СУЩЕСТВУЮЩИЙ (НЕ копировался), правленых rows этого батча = 3 (26/27/30 col36-only), reopen-verify OK (blknotrip rows 26/27/30 col36!=col35 & UA-marker DSCRU 0 & col5==srcCol5 не тронут & col35==src; SKIP rows 31/32 col35==src & col36==src & col5==src; blknochg rows 28/29/33 col35==src & col36==src & col5==src; prior b1+b2+b3 3/4/5/6/9/13/14/15/16/18/19/20/21/22/24/25 целы). Family-норма стац-блендер boilerplate: lead-абзац SKU29 Bartscher переведён по canonical genuine RU SKU27 GoodFood BL1500 этого же chunk. Открытых вопросов батч не дал (SKU32 GT-артефакт — soft-наблюдение, не нумерованный OQ). Глоссарий обновлён. Следующий: chunk-060 батч SKU 33-40 (openpyxl rows 34..41; SKIP-НП SKU33 ART2566515692 Hurakan #5 — б5). _(пред.: б1 SKU 1-8 8/81 blk3 SKU2/5/8+blknotrip2 SKU3/4+blknochg2 SKU1/7+SKIP1 SKU6 #1 C1 01ea0ce; б2 SKU 9-16 16/81 blknotrip4 SKU12-15+blknochg4 SKU9/10/11/16 C1 1aa8f97/C2 81c18e8; б3 SKU 17-24 24/81 blk5 SKU17-21+blknotrip2 SKU23/24+SKIP1 SKU22 #2 C1 b76cff3/C2 9b7eab7.)_

Здесь собираю всё, что требует твоего подтверждения (не авто-фиксы). Авто-фиксы по locked-паттернам перечислены в сводках по батчам, отдельного подтверждения не требуют. Открытые вопросы накапливаются в нумерованный список и финализируются при закрытии chunk-060. SKIP-НП SKU (НП-эксклюзивные бренды) перечисляются отдельным списком — тело придёт из фида НП позже, RU не трогается.

---

## SKIP-НП chunk-060 (НП-эксклюзивные бренды — RU не переписан)

_(Бренд-состав chunk-060 определяется per-SKU по `Название` (колонка `Бренд` в источнике дублирует числовой `Артикул`, бренд по ней не читается). Зонд chunk-060: **8 NP-suspect hits** в НП-списке HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA → SKIP-НП: **HURAKAN ×8** — SKU6 (Артикул `732422924`), SKU22 (`2111152648`), SKU30 (`2503647283`), SKU31 (`2503651061`), SKU33 (`2566515692`), SKU49 (`1133814407`), SKU65 (`2599060225`), SKU73 (`1147786691`) — вносятся в таблицу ниже при обработке соответствующих батчей (б1 SKU6 / б3 SKU22 / б4 SKU30·31 / б5 SKU33 / б7 SKU49 / б9 SKU65 / б10 SKU73). **AIRHOT НЕ в НП-списке** (SKU48 `Подрібнювач льоду AIRHOT IC-1`, SKU72 `Гриль контактний AIRHOT CGL`) — обработан обычно. Прочие бренды (Sirman, REEDNEE, Hendi, Hamilton Beach, EWT INOX, GoodFood, Frosty, Ceado/CEADO, Bartscher, SARO, Fimar, Vema, …) НЕ в НП-списке — обработаны обычно.)_

| # | SKU | Артикул | Бренд | Название (UA) | Статус |
|---|---|---|---|---|---|
| 1 | SKU6 | 732422924 | HURAKAN | Блендер HURAKAN HKN-BLW2 grey\red | SKIP-НП (тело придёт из фида НП позже, RU не трогался) |
| 2 | SKU22 | 2111152648 | HURAKAN | Блендер Hurakan HKN-BLW2 grey | SKIP-НП (тело придёт из фида НП позже, RU не трогался; descUA!=descRU, но НП-правило приоритет — fixed row 23 не тронут) |
| 3 | SKU30 | 2503647283 | HURAKAN | Блендер Hurakan HKN-HBH2000S | SKIP-НП (тело придёт из фида НП позже, RU не трогался; fixed row 31 не тронут) |
| 4 | SKU31 | 2503651061 | HURAKAN | Блендер Hurakan HKN-HBH2000STH з шумопоглинаючим покриттям | SKIP-НП (тело придёт из фида НП позже, RU не трогался; NAZVRU частично RU, но НП-правило приоритет — fixed row 32 не тронут) |

---

## Открытые вопросы chunk-060

_(нумерация Открытых вопросов chunk-060 — отдельная. Пока 0. Кумул. контекст из других chunk (тоже ждут ответа Yana): OQ#1 SKU 10 chunk-055 Hendi 843468/843499; OQ#1 SKU 67 chunk-056 Nuova Simonelli APPIA II V 1GR ↔ Appia Life V 1Gr рассинхрон модель-кода; OQ#1 SKU 31 chunk-058 Cancan 0103 — чужой товар в лид-абзаце genuine RU; OQ#1 SKU 89 chunk-059 FROSTY FB-010 — col5 чужой продукт + рассинхрон модель-кода 010/FB-010/BL-010Е. Полные версии — в соответствующих chunk-NN-MANUAL-REVIEW.md.)_
