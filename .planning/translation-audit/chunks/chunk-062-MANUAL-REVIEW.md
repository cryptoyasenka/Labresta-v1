# chunk-062 — ручная проверка для Yana (русский)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-062 (81 SKU)
**Apply key:** `Артикул` (scoped per row)
**Status:** IN PROGRESS 56/81 (blk триплет 20 / blknochg 32 / blknotrip 1 / SKIP-НП 3; Открытых вопросов 0)
**Worker:** W2 (параллельный, диапазон chunk-055 … chunk-085)
**Last updated:** chunk-062 батч 7 (SKU 49-56, openpyxl rows 50-57) — обработан, **56/81**. Категории: **blk триплет 3** (SKU49 AIRHOT RG-11 row50 / SKU50 AIRHOT RG-5S row51 / SKU51 AIRHOT RG-7S row52 — descUA==descRU True + col5==col4 UA-leak «роликовий» + col7 genuine RU «роликовый» → col5←col7 + col36 tag-в-tag RU перевод source col35 replace-on-source; byte-exact PER-SKU: RG-11 reuse RG-9 b6 структ.шаблон `+50...+300, &deg;С`/`1.65, кВт`/Latin x `560x485x178`·`610x530x210`; RG-5S/RG-7S «із захисним екраном»→«с защитным экраном» `+50...+250, &deg;С` Latin x, RG-5S `0.96 кВт` 8.2/9.5 `580x250x420`·`620x320x460` / RG-7S `1.33 кВт` 10/12 `580x330x420`·`620x390x460`; `&#39;` сняты) · **blknotrip 0** · **blknochg 3** (SKU52 GoodFood GLASS HDRG11 row53 / SKU55 GGM HDGJ5 row56 / SKU56 Roller Grill RG 7 row57 — descUA!=descRU, col5 genuine RU==col7, col36 отдельное чистое RU, fixed rows 53/56/57 НЕ тронуты==source) · **SKIP-НП 2** (SKU53 HURAKAN HKN-GW11M row54 Артикул 2375841678 #2 / SKU54 HURAKAN HKN-GW9M row55 Артикул 2375848556 #3 — НП-эксклюзив forward-only, RU НЕ переписан, fixed rows 54/55 НЕ тронуты, тело из НП-фида позже). chunk-062-fixed.xlsx правлен rows 50/51/52 (blk триплет col5←col7+col36); rows 53/54/55/56/57 НЕ тронуты; reopen-verify VERIFY_062_B7 ALL PASS 56 чеков (b7 + REGR b1 SKU4 / b2 SKU9-16 / b3 SKU21·SKU24 / b4 SKU25-32 / b5 SKU33-40 / b6 SKU41-48 — все intact, col36-UA 0, skeleton==src). Открытых вопросов батч не дал (модель-коды NAME UA↔RU согласованы). Soft-notes (НЕ нумеруются): SKU49 RG-11 структурно идентичен RG-9 (b6) — RU replace-on-source по byte-verified RG-9 шаблону, грам. число роликов (6/5 → роликов) скорректировано · SKU50/51 RG-5S/RG-7S shield-вариант, лид «із захисним екраном» в RU «с защитным экраном» в порядке UA · blknochg SKU52/55/56 genuine RU (Roller Grill `&Oslash;` entity verbatim) НЕ переводились. Глоссарий: б7 +2 net-new (кумул 485). Следующий: chunk-062 батч SKU 57-64 (NP-чек: следующий НП SKU66 row67 + SKU67 row68 в б9).

Здесь собираю всё, что требует твоего подтверждения (не авто-фиксы). Авто-фиксы по locked-паттернам перечислены в сводках по батчам, отдельного подтверждения не требуют. Открытые вопросы накапливаются в нумерованный список и финализируются при закрытии chunk-062. SKIP-НП SKU (НП-эксклюзивные бренды) перечисляются отдельным списком — тело придёт из фида НП позже, RU не трогается.

---

## SKIP-НП chunk-062 (НП-эксклюзивные бренды — RU не переписан)

_(Бренд-состав chunk-062 определяется per-SKU по `Название` (колонка `Бренд` в источнике дублирует числовой `Артикул`, бренд по ней не читается). Зонд chunk-062: **6 NP-suspect hits** в НП-списке HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA → SKIP-НП: **HURAKAN ×6** — SKU34 (Артикул `736117487`), SKU53 (`2375841678`), SKU54 (`2375848556`), SKU66 (`901422138`), SKU67 (`1168676811`), SKU81 (`2059507443`) — вносятся в таблицу ниже при обработке соответствующих батчей (б5 SKU34 / б7 SKU53·54 / б9 SKU66·67 / б11 SKU81). Прочие бренды (SARO, …) НЕ в НП-списке — обрабатываются обычно.)_

| # | SKU | Артикул | Бренд | Название (UA) | Статус |
|---|---|---|---|---|---|
| 1 | 34 | 736117487 | HURAKAN | Гриль роликовий HURAKAN HKN-GW7M (7 роликів) | SKIP-НП (тело из фида НП позже) |
| 2 | 53 | 2375841678 | HURAKAN | Гриль роликовий HURAKAN HKN-GW11M 11 роликів | SKIP-НП (тело из фида НП позже) |
| 3 | 54 | 2375848556 | HURAKAN | Гриль роликовий HURAKAN HKN-GW9M 9 роликів | SKIP-НП (тело из фида НП позже) |
| _(б9 SKU66·67 / б11 SKU81)_ | | | | | |

---

## Открытые вопросы chunk-062

_(нумерация Открытых вопросов chunk-062 — отдельная. Пока 0. Кумул. контекст из других chunk (тоже ждут ответа Yana, НЕ блокируют): OQ#1 SKU 10 chunk-055 Hendi 843468/843499; OQ#1 SKU 67 chunk-056 Nuova Simonelli APPIA II V 1GR ↔ Appia Life V 1Gr рассинхрон модель-кода; OQ#1 SKU 31 chunk-058 Cancan 0103 — чужой товар в лид-абзаце genuine RU; OQ#1 SKU 89 chunk-059 FROSTY FB-010 — col5 чужой продукт + рассинхрон модель-кода 010/FB-010/BL-010Е. Полные версии — в соответствующих chunk-NN-MANUAL-REVIEW.md.)_
