# chunk-059 — ручная проверка для Yana (русский)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-059 (96 SKU)
**Apply key:** `Артикул` (scoped per row)
**Status:** IN PROGRESS 8/96 (blk триплет 8 / blknochg 0 / blknotrip 0 / SKIP-НП 0; Открытых вопросов 0)
**Worker:** W2 (параллельный, диапазон chunk-055 … chunk-085)
**Last updated:** chunk-059 батч 1 (SKU 1-8) → 8/96. **8 blk триплет** — молочные миксеры: SKU1 Bartscher 135102 Арт 2464184031 · SKU2 FROSTY DM-B Арт 468643964 · SKU3 FROSTY DM-B-20 Арт 468645381 · SKU4 EWT INOX EMM10/CMES Арт 468646757 · SKU5 EWT INOX EMM20/CMES Арт 468647695 · SKU6 Hamilton Beach HMD200CE Арт 498177236 · SKU7 Sirman Sirio 1 Арт 524929658 · SKU8 Sirman Sirio 2 Арт 524929659. Во всех 8: `descUA==descRU` True (UA-копия в RU-описании), `nmRU==nazvRU` False (col5 = UA-leak `Міксер молочний…`, col7 = genuine RU `Миксер молочный…`) → триплет: col5 ← col7 (genuine RU имя), col36 = полный тег-в-tag RU-перевод по шаблону молочного миксера (склянка→стакан, неіржавкої/нержавіючої сталі→нержавеющей стали, об'єм/об&#39;єм→объем апостроф снят, швидкість→скорость, об/хв→об/мин, матеріал: алюміній→материал: алюминий, габарити→габариты, потужність→мощность, напруга→напряжение). Габариты `NNNхNNN` + токены `0,40х2`/`2х0,55`/`2x0,1` — слайс байт-точно из source DSCUA (кир.х U+0445 / лат.x U+0078 НЕ нормируются); `&mdash;` (SKU8) verbatim; реальные `.`-дроби→`,` только в переводимой UA-копии SKU1 (`7.45`→`7,45`, `0.8`→`0,8`). **chunk-059-fixed.xlsx СОЗДАН** (cp source → fixed, первый батч с blk-правками) + 8 rows col5+col36 by Артикул; reopen-verify `=== ALL OK ===` (fixed.col36≠src ровно 8 ARTs, col5 ровно 8, col35/DSCUA не тронут 0 diffs, residUA=[] украинских остатков нет). Ни один бренд НЕ в НП-списке (Bartscher/FROSTY/EWT INOX/Hamilton Beach/Sirman) → обычная обработка; НП-зонд Hurakan ×3 (SKU25/26 батч 4, SKU91 батч 12) ещё впереди. META keywords (col24/25) faithful, не трогались. Soft-note 0; новых нумерованных Открытых вопросов нет; **Открытых вопросов chunk-059 итого 0**. Глоссарий W2 пополнен (footer chunk-glossary-w2.md). Кумул. ждут Yana (отд. нумерация): OQ#1 SKU 10 chunk-055; OQ#1 SKU 67 chunk-056; OQ#1 SKU 31 chunk-058. Следующий: батч SKU 9-16 (openpyxl rows 10..17).

**Last updated (chunk-059 scaffold — предыдущий шаг):** chunk-059 scaffold (W2, продолжение chunk-058) COMMITTED. Источник 96 SKU скопирован, зонд по `Название`: 3 NP-suspect Hurakan ×3 (SKU25 Арт 2503655839 / SKU26 Арт 2503663450 — батч 4; SKU91 Арт 2373825799 — батч 12). chunk-059-diff.md + chunk-059-MANUAL-REVIEW.md созданы IN PROGRESS 0/96. chunk-glossary-w2.md НЕ пересоздан (общий 246). chunk-058 ЗАКРЫТ 78/78 (OQ#1 SKU31 ждёт Yana).

Здесь собираю всё, что требует твоего подтверждения (не авто-фиксы). Авто-фиксы по locked-паттернам перечислены в сводках по батчам, отдельного подтверждения не требуют. Открытые вопросы накапливаются в нумерованный список и финализируются при закрытии chunk-059. SKIP-НП SKU (НП-эксклюзивные бренды) перечисляются отдельным списком — тело придёт из фида НП позже, RU не трогается.

---

## SKIP-НП chunk-059 (НП-эксклюзивные бренды — RU не переписан)

_(Бренд-состав chunk-059 определяется per-SKU по `Название` (колонка `Бренд` в источнике дублирует числовой `Артикул`, бренд по ней не читается). Зонд chunk-059: **3 NP-suspect hits** в НП-списке HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA → ожидается SKIP-НП (вносятся в таблицу при обработке соответствующих батчей): **Hurakan ×3** — SKU25 (Артикул `2503655839`) `Міксер для молочних коктейлів HURAKAN HKN-FR1GD` (батч 4), SKU26 (`2503663450`) `Міксер для молочних коктейлів HURAKAN HKN-FR2GD` (батч 4), SKU91 (`2373825799`) `Блендер Hurakan HKN-HBH850M PRO COVER` (батч 12). Прочие бренды (Bartscher, Frosty, EWT INOX, Hamilton Beach, Sirman, CEADO, JAU, Goodfood, Fimar, Hendi, GGM, Vema, Quamar, SARO, UGOLINI, CAB, Sirman, …) НЕ в НП-списке — обрабатываются обычно. Список и таблица обновляются per-батч при подтверждении бренда по `Название`.)_

| # | SKU | Артикул | Бренд | Название (UA) | Статус |
|---|---|---|---|---|---|

---

## Открытые вопросы chunk-059

_(нумерация Открытых вопросов chunk-059 — отдельная, начинается с #1 при первом сомнении. Кумул. контекст из других chunk (тоже ждут ответа Yana): OQ#1 SKU 10 chunk-055 Hendi 843468/843499; OQ#1 SKU 67 chunk-056 Nuova Simonelli APPIA II V 1GR ↔ Appia Life V 1Gr рассинхрон модель-кода; OQ#1 SKU 31 chunk-058 Cancan 0103 — чужой товар (GoodFood FJ150) в лид-абзаце genuine RU-описания. Полные версии вопросов — в chunk-055-MANUAL-REVIEW.md / chunk-056-MANUAL-REVIEW.md / chunk-058-MANUAL-REVIEW.md соответственно.)_

_(Пока пусто — Открытых вопросов chunk-059 нет. Первый вопрос получит #1.)_
