# chunk-061 — ручная проверка для Yana (русский)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-061 (67 SKU)
**Apply key:** `Артикул` (scoped per row)
**Status:** IN PROGRESS 48/67 (blk триплет 23 / blknochg 21 / blknotrip 0 / SKIP-НП 4; Открытых вопросов 0)
**Worker:** W2 (параллельный, диапазон chunk-055 … chunk-085)
**Last updated:** chunk-061 батч 6 (SKU 41-48, openpyxl rows 42-49) — обработан, **48/67**. Категории: **blk триплет 3** (SKU41 Frosty SP-1C2 row42 / SKU43 Frosty SP-2A2 row44 / SKU44 Frosty SP-2A3 row45 — col5==col4 UA-leak «контактний» UA-MARK regex False, descUA==descRU True, col7 genuine RU `Гриль контактный Frosty SP-xxx` → col5←col7 + col36 tag-в-tag RU через COMMON+variant replace-from-source; reopen-verify col36!=col35 / UA-marker col36+col5 0 / col5==col7 genuineRU; APPLY MISMATCH 0 VERIFY ALL PASS len col36 r42=1116/r44=1117/r45=1119) · **blknochg 4** (SKU42 Frosty SP-2A1 / SKU45 GoodFood WB888RHB / SKU46 GoodFood ECG20EA / SKU47 GoodFood GS450L — descUA!=descRU, col5 уже genuine RU==col7 (SKU47 lang-neutral name col5==col4==col7), отдельное чистое RU — LIVE НЕ переписан, fixed rows 43/46/47/48 НЕ тронуты) · blknotrip 0 · **SKIP-НП 1** (SKU48 TATRA EMP.102 Арт `2062003333` — бренд TATRA ∈ НП-список → #4, тело из фида НП позже, fixed row49 НЕ тронут). Frosty/GoodFood НЕ в НП-списке. chunk-061-fixed.xlsx — load СУЩЕСТВУЮЩИЙ (НЕ re-copy), правленых rows этого батча = 3 (42/44/45 col5←col7+col36 blk триплет), rows 43/46/47/48/49 НЕ тронуты (== source), B1-B5 rows intact, reopen-verify OK (APPLY MISMATCH 0 / VERIFY ALL PASS). Открытых вопросов батч не дал: модель-коды NAME UA↔genuine-RU согласованы (Frosty SP-1C2/SP-2A1/SP-2A2/SP-2A3; GoodFood WB888RHB/ECG20EA/GS450L; TATRA EMP.102), чужих продуктов нет. Soft-notes (НЕ нумеруются): SKU42 genuine-RU «2 верхние рабочие поверхности» (UA «2 робочі поверхні» без «верхние») · SKU47 GS450L genuine-RU «лоток для оружия жира» (UA `зброу` — машинный артефакт genuine RU) · genuine-RU `&deg;С` entity / `3,6кВт`·`2,8кВт` без пробела (SKU42/45/46/47 blknochg verbatim, fixed НЕ тронут). Глоссарий: б6 блок добавлен (+0 net-new кумул 452), см. footer chunk-glossary-w2.md. Следующий: chunk-061 батч 7 (SKU 49-56, openpyxl rows 50-57).

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
