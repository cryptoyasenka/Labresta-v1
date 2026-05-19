# chunk-062 — ручная проверка для Yana (русский)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-062 (81 SKU)
**Apply key:** `Артикул` (scoped per row)
**Status:** IN PROGRESS 32/81 (blk триплет 6 / blknochg 25 / blknotrip 1 / SKIP-НП 0; Открытых вопросов 0)
**Worker:** W2 (параллельный, диапазон chunk-055 … chunk-085)
**Last updated:** chunk-062 батч 4 (SKU 25-32, openpyxl rows 26-33) — обработан, **32/81**. Категории: **blk триплет 4** (SKU29 AIRHOT RG-5 row30 / SKU30 Hendi 268735 (14) row31 / SKU31 Hendi 268506 (7) row32 / SKU32 Hendi 268605 (9) row33 — descUA==descRU True + col5==col4 UA-leak `роликовий` + col7 genuine RU `роликовый` → col5←col7 + col36 tag-в-tag RU перевод source col35 (replace-on-source: SKU29 411→413, SKU30 677→670, SKU31 603→595, SKU32 603→595); byte-exact PER-SKU — SKU29 `(°С)` U+00B0+кир.С/`+50/+300`/`580х250х215` кир.х/литер.`'`→plain · SKU30 `150°C` U+00B0+лат.C/`520x591x175` **ЛАТ.x U+0078**/`1,48 кВт` · SKU31 `520х325х175` **КИР.х U+0445**/`0,74 кВт` · SKU32 `520х400х175` **КИР.х**/`0,94 кВт`; все `0,15/0,75 кВт`·`220 В`·`42/45 см` запятая-десятич verbatim; SKU30 содержит строку `Раздельное управление ТЭНами`, SKU31/32 — нет) · **blknotrip 0** · **blknochg 4** (SKU25 GGM HDGJ7 (HDK7) / SKU26 GGM HDGJ11 / SKU27 GoodFood HDRG5 RED / SKU28 GoodFood HDRG7 RED — descUA!=descRU, col5 genuine RU==col7, col36 отдельное чистое RU — LIVE НЕ переписан, fixed rows 26/27/28/29 НЕ тронуты==source) · **SKIP-НП 0** (GGM/GoodFood/AIRHOT/Hendi НЕ в НП-списке; первый НП — SKU34 HURAKAN в б5). chunk-062-fixed.xlsx правлен rows 30/31/32/33 (blk триплет col5←col7 + col36); blknochg rows 26-29 НЕ тронуты; reopen-verify VERIFY_062_B4 ALL PASS 57 чеков (b4 blk триплет 5×4 + blknochg 4 + REGR b1 SKU4 row5 + b2 SKU9-16 rows10-17 + b3 SKU21 row22/SKU24 row25 — все intact, col36-UA 0, skeleton==src). Открытых вопросов батч не дал (модель-коды NAME UA↔RU согласованы: AIRHOT RG-5 / Hendi 268735·268506·268605 col5←col7 идентичны). Soft-notes (НЕ нумеруются): SKU25 склейка `1.4кВт` · SKU27/28 энтити `°C`→`&deg;С` · SKU28 склейка `(3 ролика +4 ролика)`+drop-тире · SKU30/31/32 source-UA RU-leak `Непрігорающая поверхню роликів`→чистый RU в рамках tag-в-tag — все NAME консистентны, blknochg fixed НЕ тронут. Глоссарий: б4 +6 net-new (кумул 474). Следующий: chunk-062 батч SKU 33-40 (**SKU34 row35 ART736117487 HURAKAN → SKIP-НП #1**).

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
