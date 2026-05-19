# chunk-060 — ручная проверка для Yana (русский)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-060 (81 SKU)
**Apply key:** `Артикул` (scoped per row)
**Status:** IN PROGRESS 24/81 (blk триплет 8 / blknochg 6 / blknotrip 8 / SKIP-НП 2; Открытых вопросов 0)
**Worker:** W2 (параллельный, диапазон chunk-055 … chunk-085)
**Last updated:** chunk-060 батч 3 (SKU 17-24, openpyxl rows 18..25) — обработан, 24/81. Категории: blk триплет 5 (SKU17 Frosty FBA-010 / SKU18 FBA-C280B / SKU19 FBA-2180B / SKU20 FBA-1180B / SKU21 FBA-C280P — col5==col4 UA-leak, col7 genuine RU `+ профессиональный` → col5←col7 + col36 переведён tag-в-tag) · blknotrip 2 (SKU23 Ceado В185 / SKU24 Ceado В280 — col4==col5==col6==col7 бренд+код language-neutral, descUA==descRU UA-leak в desc → только col36, col5 оставлен) · SKIP-НП 1 (SKU22 Hurakan HKN-BLW2 grey — таблица #2) · blknochg 0. chunk-060-fixed.xlsx загружен СУЩЕСТВУЮЩИЙ (НЕ копировался), правленых rows этого батча = 7 (18-22 col5←col7+col36; 24/25 col36-only), reopen-verify OK (rows 18-22 col36!=col35 & UA-marker DSCRU 0 & col5==col7 genuineRU & col5 UA-marker 0; rows 24/25 col36!=col35 & UA-marker 0 & col5==srcCol5; SKIP row 23 col35==src & col36==src & col5==src; prior b1+b2 3/4/5/6/9/13/14/15/16 целы). Family-норма boilerplate (soft-note НЕ нумер., прец. chunk-059 б12 SKU89 FROSTY FB-010): `льодоподрібнювач`→`льдокрошитель`, `перетворений на сніг`→`превращён в крошку` (canonical = genuine RU SKU22 этого же chunk). Открытых вопросов батч не дал. Глоссарий +8 кумул 364. Следующий: chunk-060 батч SKU 25-32 (openpyxl rows 26..33; SKIP-НП SKU30 ART2503647283 + SKU31 ART2503651061 Hurakan — б4). _(пред.: б1 SKU 1-8 8/81 blk3 SKU2/5/8+blknotrip2 SKU3/4+blknochg2 SKU1/7+SKIP1 SKU6 #1 C1 01ea0ce; б2 SKU 9-16 16/81 blknotrip4 SKU12-15+blknochg4 SKU9/10/11/16 C1 1aa8f97/C2 81c18e8.)_

Здесь собираю всё, что требует твоего подтверждения (не авто-фиксы). Авто-фиксы по locked-паттернам перечислены в сводках по батчам, отдельного подтверждения не требуют. Открытые вопросы накапливаются в нумерованный список и финализируются при закрытии chunk-060. SKIP-НП SKU (НП-эксклюзивные бренды) перечисляются отдельным списком — тело придёт из фида НП позже, RU не трогается.

---

## SKIP-НП chunk-060 (НП-эксклюзивные бренды — RU не переписан)

_(Бренд-состав chunk-060 определяется per-SKU по `Название` (колонка `Бренд` в источнике дублирует числовой `Артикул`, бренд по ней не читается). Зонд chunk-060: **8 NP-suspect hits** в НП-списке HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA → SKIP-НП: **HURAKAN ×8** — SKU6 (Артикул `732422924`), SKU22 (`2111152648`), SKU30 (`2503647283`), SKU31 (`2503651061`), SKU33 (`2566515692`), SKU49 (`1133814407`), SKU65 (`2599060225`), SKU73 (`1147786691`) — вносятся в таблицу ниже при обработке соответствующих батчей (б1 SKU6 / б3 SKU22 / б4 SKU30·31 / б5 SKU33 / б7 SKU49 / б9 SKU65 / б10 SKU73). **AIRHOT НЕ в НП-списке** (SKU48 `Подрібнювач льоду AIRHOT IC-1`, SKU72 `Гриль контактний AIRHOT CGL`) — обработан обычно. Прочие бренды (Sirman, REEDNEE, Hendi, Hamilton Beach, EWT INOX, GoodFood, Frosty, Ceado/CEADO, Bartscher, SARO, Fimar, Vema, …) НЕ в НП-списке — обработаны обычно.)_

| # | SKU | Артикул | Бренд | Название (UA) | Статус |
|---|---|---|---|---|---|
| 1 | SKU6 | 732422924 | HURAKAN | Блендер HURAKAN HKN-BLW2 grey\red | SKIP-НП (тело придёт из фида НП позже, RU не трогался) |
| 2 | SKU22 | 2111152648 | HURAKAN | Блендер Hurakan HKN-BLW2 grey | SKIP-НП (тело придёт из фида НП позже, RU не трогался; descUA!=descRU, но НП-правило приоритет — fixed row 23 не тронут) |

---

## Открытые вопросы chunk-060

_(нумерация Открытых вопросов chunk-060 — отдельная. Пока 0. Кумул. контекст из других chunk (тоже ждут ответа Yana): OQ#1 SKU 10 chunk-055 Hendi 843468/843499; OQ#1 SKU 67 chunk-056 Nuova Simonelli APPIA II V 1GR ↔ Appia Life V 1Gr рассинхрон модель-кода; OQ#1 SKU 31 chunk-058 Cancan 0103 — чужой товар в лид-абзаце genuine RU; OQ#1 SKU 89 chunk-059 FROSTY FB-010 — col5 чужой продукт + рассинхрон модель-кода 010/FB-010/BL-010Е. Полные версии — в соответствующих chunk-NN-MANUAL-REVIEW.md.)_
