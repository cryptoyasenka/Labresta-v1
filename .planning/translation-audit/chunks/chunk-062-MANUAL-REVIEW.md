# chunk-062 — ручная проверка для Yana (русский)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-062 (81 SKU)
**Apply key:** `Артикул` (scoped per row)
**Status:** IN PROGRESS 16/81 (blk триплет 1 / blknochg 15 / blknotrip 0 / SKIP-НП 0; Открытых вопросов 0)
**Worker:** W2 (параллельный, диапазон chunk-055 … chunk-085)
**Last updated:** chunk-062 батч 2 (SKU 9-16, openpyxl rows 10-17) — обработан, **16/81**. Категории: blk триплет 0 · **blknochg 8** (SKU9 GGM KGKB200 / SKU10 GGM KGKB300 / SKU11 Roller Grill MAJESTIC R / SKU12 MARS MTS-20 / SKU13 Spidocook SP010PR / SKU14 Pimak М070 / SKU15 Pimak М071-1 / SKU16 Sirman PD LR-RR — все descUA!=descRU, col5 genuine RU==col7, col36 отдельное чистое RU без UA-маркеров — LIVE НЕ переписан, fixed rows 10-17 НЕ тронуты==source) · blknotrip 0 · **SKIP-НП 0** (GGM/Roller Grill/MARS/Spidocook/Pimak/Sirman НЕ в НП-списке; первый НП — SKU34 HURAKAN в б5; SKIP-НП таблица без изменений). chunk-062-fixed.xlsx НЕ трогался в б2 (0 правок, все blknochg), reopen-verify VERIFY_062_B2 ALL PASS (rows 10-17 fixed==source, col5==col7, col36 UA-marker 0; b1 SKU4 row5 intact). Открытых вопросов батч не дал (модель-коды NAME UA↔RU согласованы, col5==col7 везде). Soft-notes (НЕ нумеруются, genuine-RU вариативность/артефакты source): SKU10 source-RU опечатка `нержаеющей` · SKU11 энтити-вариативность `+300 °C`→`+300&deg;С` byte-exact · SKU12 имя +«электрический» (модель-код MTS-20 консистентен col5==col7) + source-RU дубль `Индикатор включения`×2 · SKU13 склейки `Поверхности:верхняя`/`нижняягладкая` (source UA тоже склеено) + `<br>`→`<br />` + энтити `°C`→`&deg; С` · SKU16 редундантность `с регулировкой` + `Подключение, в 220 В` (прец. SKU1 б1) — все NAME консистентны, blknochg fixed НЕ тронут. Глоссарий: б2 +0 net-new (все blknochg НЕ переводились, кумул 463). Следующий: chunk-062 батч SKU 17-24.

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
