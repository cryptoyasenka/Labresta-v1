# chunk-060 — ручная проверка для Yana (русский)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-060 (81 SKU)
**Apply key:** `Артикул` (scoped per row)
**Status:** IN PROGRESS 48/81 (blk триплет 9 / blknochg 17 / blknotrip 17 / SKIP-НП 5; Открытых вопросов 0)
**Worker:** W2 (параллельный, диапазон chunk-055 … chunk-085)
**Last updated:** chunk-060 батч 6 (SKU 41-48, openpyxl rows 42..49) — обработан, 48/81. Категории: blknotrip 4 (SKU43 Hamilton Beach HBF500CE / SKU45 Fimar Easy Line BL020B / SKU46 CEADO B285 / SKU47 Hamilton Beach HBH855CE — col4==col5==col6==col7 бренд+код language-neutral, descUA==descRU UA-leak → только col36, col5 оставлен) · blknochg 3 (SKU41 Hamilton Beach HBH750CE Eclipse / SKU42 Vema FR2055 / SKU44 Fimar Easy Line BL008 — descUA!=descRU genuine отдельное RU уже есть → fixed НЕ тронут; SKU42 NMRU суффикс «профессиональный» — согласованный дескриптор, прец. SKU34) · blk триплет 1 (SKU48 AIRHOT IC-1 — col5==col4 UA-leak `Подрібнювач льоду`, col7 genuine RU `Льдокрошитель AIRHOT IC-1` → col5←col7 + col36 полный RU) · SKIP-НП 0. CEADO/AIRHOT НЕ в НП-списке (ближайший HURAKAN — SKU49 #6 в б7). chunk-060-fixed.xlsx загружен СУЩЕСТВУЮЩИЙ (НЕ копировался), правленых rows этого батча = 5 (44/46/47/48 col36-only blknotrip + 49 col5+col36 blk триплет), reopen-verify OK (blknotrip rows 44/46/47/48 col36!=col35 & UA-marker DSCRU 0 & col5==srcCol5 не тронут & col35==src; blk триплет row 49 col36!=col35 & UA-marker col36/col5 0 & col5==col7 & col35==src; blknochg rows 42/43/45 col35==src & col36==src & col5==src; prior b1-b5 3/4/5/6/9/13/14/15/16/18/19/20/21/22/24/25/26/27/30/36/38 целы). Открытых вопросов батч не дал (SKU42 NMRU суффикс «профессиональный» — согласованный дескриптор genuine RU, не рассинхрон модель-кода; SKU48 UA-leak col5 → штатный blk триплет, не OQ). Глоссарий обновлён. Следующий: chunk-060 батч SKU 49-56 (openpyxl rows 50..57; SKU49 HURAKAN HKN-TR65 = SKIP-НП #6). _(пред.: б1 SKU 1-8 8/81 blk3 SKU2/5/8+blknotrip2 SKU3/4+blknochg2 SKU1/7+SKIP1 SKU6 #1 C1 01ea0ce; б2 SKU 9-16 16/81 blknotrip4 SKU12-15+blknochg4 SKU9/10/11/16 C1 1aa8f97/C2 81c18e8; б3 SKU 17-24 24/81 blk5 SKU17-21+blknotrip2 SKU23/24+SKIP1 SKU22 #2 C1 b76cff3/C2 9b7eab7; б4 SKU 25-32 32/81 blknotrip3 SKU25/26/29+blknochg3 SKU27/28/32+SKIP2 SKU30/31 #3/#4 C1 23d3e25/C2 ba95a38; б5 SKU 33-40 40/81 blknotrip2 SKU35/37+blknochg5 SKU34/36/38/39/40+SKIP1 SKU33 #5 C1 6ca3189/C2 b64ea0c.)_

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
| 5 | SKU33 | 2566515692 | HURAKAN | Блендер Hurakan HKN-HBH850M PRO | SKIP-НП (тело придёт из фида НП позже, RU не трогался; descUA==descRU True, но НП-правило приоритет — fixed row 34 не тронут) |

---

## Открытые вопросы chunk-060

_(нумерация Открытых вопросов chunk-060 — отдельная. Пока 0. Кумул. контекст из других chunk (тоже ждут ответа Yana): OQ#1 SKU 10 chunk-055 Hendi 843468/843499; OQ#1 SKU 67 chunk-056 Nuova Simonelli APPIA II V 1GR ↔ Appia Life V 1Gr рассинхрон модель-кода; OQ#1 SKU 31 chunk-058 Cancan 0103 — чужой товар в лид-абзаце genuine RU; OQ#1 SKU 89 chunk-059 FROSTY FB-010 — col5 чужой продукт + рассинхрон модель-кода 010/FB-010/BL-010Е. Полные версии — в соответствующих chunk-NN-MANUAL-REVIEW.md.)_
