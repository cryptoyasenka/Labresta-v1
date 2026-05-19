# chunk-062 — ручная проверка для Yana (русский)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-062 (81 SKU)
**Apply key:** `Артикул` (scoped per row)
**Status:** IN PROGRESS 40/81 (blk триплет 10 / blknochg 28 / blknotrip 1 / SKIP-НП 1; Открытых вопросов 0)
**Worker:** W2 (параллельный, диапазон chunk-055 … chunk-085)
**Last updated:** chunk-062 батч 5 (SKU 33-40, openpyxl rows 34-41) — обработан, **40/81**. Категории: **blk триплет 4** (SKU33 Hendi 268704 (11) row34 — Hendi roller-grill блок как b4 SKU30, есть `Раздельное управление ТЭНами`; SKU38 FROSTY WY-005 row39 / SKU39 WY-007 row40 / SKU40 WY-009 row41 — общий FROSTY_WY блок; descUA==descRU True + col5==col4 UA-leak `роликовий` + col7 genuine RU `роликовый` → col5←col7 + col36 tag-в-tag RU перевод source col35 (replace-on-source: SKU33 677→670, SKU38/39/40 369→376); byte-exact PER-SKU — SKU33 `150°C` U+00B0+лат.C/`520x477x175` **ЛАТ.x U+0078**/`1,18 кВт`; FROSTY размеры все **ЛАТ.x** `590x250x420`/`590x330x420`/`590x400x420`, мощность **SKU38 `0,96 кВт` ЗАПЯТАЯ** vs **SKU39 `1.33`/SKU40 `1.69 кВт` ТОЧКА-десятич** (как в source, НЕ нормализованы), `50 °C`/`250 °C` пробел+U+00B0+лат.C, em-dash `хромированная сталь`, `220 В`) · **blknotrip 0** · **blknochg 3** (SKU35 GoodFood GLASS HDRG5 row36 / SKU36 GLASS HDRG7 row37 / SKU37 REEDNEE HDRG-E9-2 row38 — descUA!=descRU, col5 genuine RU==col7, col36 отдельное чистое RU, fixed rows 36/37/38 НЕ тронуты==source) · **SKIP-НП 1** (SKU34 HURAKAN HKN-GW7M row35 ART736117487 — НП-эксклюзив forward-only, RU НЕ переписан, fixed row35 НЕ тронут, тело из НП-фида позже — SKIP-НП-таблица #1). chunk-062-fixed.xlsx правлен rows 34/39/40/41 (blk триплет col5←col7+col36); rows 35/36/37/38 НЕ тронуты; reopen-verify VERIFY_062_B5 ALL PASS 50 чеков (b5 + REGR b1 SKU4 / b2 SKU9-16 / b3 SKU21·SKU24 / b4 SKU25-32 — все intact, col36-UA 0, skeleton==src). Открытых вопросов батч не дал (модель-коды NAME UA↔RU согласованы). Soft-notes (НЕ нумеруются): SKU35/36 GoodFood GLASS genuine-RU склейка `4мм` + UA-форма `роликовий` в genuine-RU лиде · SKU37 REEDNEE clean genuine RU — все NAME консистентны, blknochg fixed НЕ тронут. Глоссарий: б5 +5 net-new (кумул 479). Следующий: chunk-062 батч SKU 41-48 (NP-чек: следующий НП SKU53/54 в б7).

Здесь собираю всё, что требует твоего подтверждения (не авто-фиксы). Авто-фиксы по locked-паттернам перечислены в сводках по батчам, отдельного подтверждения не требуют. Открытые вопросы накапливаются в нумерованный список и финализируются при закрытии chunk-062. SKIP-НП SKU (НП-эксклюзивные бренды) перечисляются отдельным списком — тело придёт из фида НП позже, RU не трогается.

---

## SKIP-НП chunk-062 (НП-эксклюзивные бренды — RU не переписан)

_(Бренд-состав chunk-062 определяется per-SKU по `Название` (колонка `Бренд` в источнике дублирует числовой `Артикул`, бренд по ней не читается). Зонд chunk-062: **6 NP-suspect hits** в НП-списке HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA → SKIP-НП: **HURAKAN ×6** — SKU34 (Артикул `736117487`), SKU53 (`2375841678`), SKU54 (`2375848556`), SKU66 (`901422138`), SKU67 (`1168676811`), SKU81 (`2059507443`) — вносятся в таблицу ниже при обработке соответствующих батчей (б5 SKU34 / б7 SKU53·54 / б9 SKU66·67 / б11 SKU81). Прочие бренды (SARO, …) НЕ в НП-списке — обрабатываются обычно.)_

| # | SKU | Артикул | Бренд | Название (UA) | Статус |
|---|---|---|---|---|---|
| 1 | 34 | 736117487 | HURAKAN | Гриль роликовий HURAKAN HKN-GW7M (7 роликів) | SKIP-НП (тело из фида НП позже) |
| _(б7 SKU53·54 / б9 SKU66·67 / б11 SKU81)_ | | | | | |

---

## Открытые вопросы chunk-062

_(нумерация Открытых вопросов chunk-062 — отдельная. Пока 0. Кумул. контекст из других chunk (тоже ждут ответа Yana, НЕ блокируют): OQ#1 SKU 10 chunk-055 Hendi 843468/843499; OQ#1 SKU 67 chunk-056 Nuova Simonelli APPIA II V 1GR ↔ Appia Life V 1Gr рассинхрон модель-кода; OQ#1 SKU 31 chunk-058 Cancan 0103 — чужой товар в лид-абзаце genuine RU; OQ#1 SKU 89 chunk-059 FROSTY FB-010 — col5 чужой продукт + рассинхрон модель-кода 010/FB-010/BL-010Е. Полные версии — в соответствующих chunk-NN-MANUAL-REVIEW.md.)_
