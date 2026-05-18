# chunk-058 — ручная проверка для Yana (русский)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-058 (78 SKU)
**Apply key:** `Артикул` (scoped per row)
**Status:** IN PROGRESS 8/78 (blk триплет 3 / blknochg 4 / blknotrip 0 / SKIP-НП 1; Открытых вопросов 0)
**Worker:** W2 (параллельный, диапазон chunk-055 … chunk-085)
**Last updated:** chunk-058 батч 1 (SKU 1-8) → 8/78. **3 blk триплет** (SKU2 Thielmann Juice Master 42.6 Арт 962046952 · SKU4 BARTSCHER 150197 Арт 2033694809 · SKU6 Fimar Easy Line CJ6 Арт 472503239 — `descUA==descRU` True UA-копия; Назв.мод RU(col5) UA-leak `Соковичавниця/Соковижималка` → genuine Назв RU(col7) `Соковыжималка…`; полный тег-в-tag RU-перевод descRU col36; chunk-058 ПЕРВЫЙ батч с правками → `chunk-058-fixed.xlsx` создан из source, edit SKU2/4/6 by Артикул, reopen read_only VERIFY `=== ALL OK ===`). **4 blknochg** (SKU1 Remta PS08 Арт 667275373 · SKU5 FROSTY CJ5 Арт 468889199 · SKU7 Sirman Apollo Cromato Арт 518672419 · SKU8 FROSTY MJE-01 Арт 558012609 — `descUA==descRU` False, RU genuine отдельный, `nmRU==nazvRU` True, LIVE genuine RU НЕ переписан, в fixed.xlsx не трогаются == source). **1 SKIP-НП** (SKU3 Арт 1147746219 HURAKAN — НП-список по `Название`, RU не переписан, тело из фида НП позже; таблица ниже строка #1). blknotrip 0. **2 soft-note НЕ нумер.** (не OQ, genuine RU не переписываем): SKU1 имя `Преc/Пресc` латинская `c`(U+0063) вместо кир. `с` (consistent UA↔RU source-quirk; RU-описание корректно `Пресс`); SKU4 genuine Назв RU `Соковыжималка BARTSCHER 150197` короче UA (опускает `POWER FRESH`/`для твердих`), артикул `150197` консистентен (код в теле) → переформулировка названия, НЕ рассинхрон модель-кода. Реальная дробь SKU4 `12.9`→`12,9` (UA-копия); `3.000 об / хв` SKU4 = группировка тысяч → verbatim; `0,42`/`0,23`/`0,7` уже запятая verbatim. Апостроф backtick/`&#39;` SKU4 →0 RU. Габариты `190х310х380`/`260х450х505`/`290х220х415` кир.`х`(U+0445) no-op verbatim; `XXL`(SKU4) language-neutral Latin verbatim. META keywords faithful, не трогались. Новых нумер. Открытых вопросов chunk-058 НЕТ (итого 0). Глоссарий W2 кумул. 166 → **176** (+10 blk триплет SKU2/4/6).

**Last updated (предыдущий шаг):** chunk-057 ЗАКРЫТ 54/54 (blk триплет 3 / blknochg 49 / blknotrip 1 / SKIP-НП 1 SKU54 Apach ACS1 ECO). Глоссарий W2 кумул. 166 строк.

Здесь собираю всё, что требует твоего подтверждения (не авто-фиксы). Авто-фиксы по locked-паттернам перечислены в сводках по батчам, отдельного подтверждения не требуют. Открытые вопросы накапливаются в нумерованный список и финализируются при закрытии chunk-058. SKIP-НП SKU (НП-эксклюзивные бренды) перечисляются отдельным списком — тело придёт из фида НП позже, RU не трогается.

---

## SKIP-НП chunk-058 (НП-эксклюзивные бренды — RU не переписан)

_(Бренд-состав chunk-058 определяется per-SKU по `Название` (колонка `Бренд` в источнике дублирует числовой `Артикул`, бренд по ней не читается). Зонд chunk-058: **9 NP-suspect hits** в НП-списке HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA → ожидается SKIP-НП (вносятся в таблицу при обработке соответствующих батчей): **Hurakan ×6** — SKU3 (Артикул `1147746219`) `Соковижималка HURAKAN HKN-CS600H для твердих`, SKU23 (`1168646756`) `Соковижималка для твердих HURAKAN HKN-CFV60`, SKU27 (`2059483074`) `Соковитискач Hurakan HKN-CFV90`, SKU28 (`2059491212`) `Соковитискач для цитрусових Hurakan HKN-SPM`, SKU33 (`2503667792`) `Соковижималка HURAKAN HKN-CFV120 PRO`, SKU34 (`2503722319`) `Соковижималка для цитрусових HURAKAN HKN-AGRL з пресом`; **Apach ×3** — SKU54 (`659271594`) `Кавомолка бункерна Apach ACG1`, SKU77 (`1104472736`) `Міксер для молочних коктейлів Apach AMX1 ECO`, SKU78 (`1104474099`) `Міксер для молочних коктейлів Apach AMX2 ECO`. Прочие бренды (Remta, Thielmann, Bartscher, Frosty, Fimar, Sirman, CanCan, Hendi, GoodFood, Ceado, Robot Coupe, Vema, Quamar, Hamilton Beach, Zumex, Bezzera, Nuova Simonelli, Victoria Arduino, …) НЕ в НП-списке — обрабатываются обычно. Список и таблица обновляются per-батч при подтверждении бренда по `Название`.)_

| # | SKU | Артикул | Бренд | Название (UA) | Статус |
|---|---|---|---|---|---|
| 1 | 3 | 1147746219 | Hurakan | Соковижималка HURAKAN HKN-CS600H для твердих | SKIP-НП (тело из фида НП позже, RU не переписан) |

---

## Открытые вопросы chunk-058

_(нумерация Открытых вопросов chunk-058 — отдельная, начинается с #1 при первом сомнении. Кумул. контекст из других chunk (тоже ждут ответа Yana): OQ#1 SKU 10 chunk-055 Hendi 843468/843499; OQ#1 SKU 67 chunk-056 Nuova Simonelli APPIA II V 1GR ↔ Appia Life V 1Gr рассинхрон модель-кода. Полные версии вопросов — в chunk-055-MANUAL-REVIEW.md / chunk-056-MANUAL-REVIEW.md соответственно.)_

_(пусто — нумерованных Открытых вопросов chunk-058 пока нет.)_

---
