# chunk-057 — ручная проверка для Yana (русский)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-057 (54 SKU)
**Apply key:** `Артикул` (scoped per row)
**Status:** IN PROGRESS 40/54 (blk триплет 3 / blknochg 36 / blknotrip 1 / SKIP-НП 0; Открытых вопросов 0)
**Worker:** W2 (параллельный, диапазон chunk-055 … chunk-085)
**Last updated:** батч 5 (SKU 33-40 — Nuova Simonelli: Musica Lux · Appia Life XT 2Gr V / 3Gr S / 3Gr V · Aurelia Wave 2Gr S/V · Aurelia Wave T3 2Gr/3Gr) — **8 blknochg** (все `descUA==descRU` False — RU genuine отдельный самостоятельный русский текст; `nmRU==nazvRU` True — Назв.мод RU(col5) == genuine Назв RU(col7), UA-leak нет; LIVE genuine RU НЕ переписываем, fixed.xlsx НЕ трогается — остаётся как после батча 1) + **0 blk триплет** + **0 blknotrip** + **0 SKIP-НП**. Подтверждено по `Название`: Nuova Simonelli НЕ в НП-списке HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA → обработан обычно, SKIP-НП 0. Переводимых UA-копий в батче нет → реальных `.`-дробей не нормализовали, новых glossary-терминов не извлекали (genuine RU не переписывается). META keywords не трогались. **Новых нумерованных Открытых вопросов в батче НЕТ**; **0 soft-note** — имена col4-7 консистентны UA↔RU во всех 8, рассинхрона model-кода нет, структурных пропусков нет (SKU33 genuine RU короче на 6 символов = мелкая компрессия формулировок, 27 `<li>` параллельны UA↔RU). Мелкие наблюдения (НЕ soft-note, UA col35 / META не трогаются): SKU37 UA-источник `Напруга, 220` без `В`; SKU38/39/40 UA-источник `Напруга, 230-380` без `В` (genuine RU корректно `Напряжение, В …`); SKU33/36/38/39/40 genuine RU `<li>обратный клапан</li>` строчное «обратный» (авторский стиль); SKU36 UA `Колір чорний` без двоеточия. Открытых вопросов 0 (кумул. ждут Yana: OQ#1 SKU10 chunk-055; OQ#1 SKU67 chunk-056 — отдельная нумерация). +0 строк глоссария (батч полностью blknochg; кумул. 166 без изменений).

**Last updated (предыдущий шаг):** батч 4 (SKU 25-32 — Victoria Arduino: Eagle One Prima PRO/EXP/Prima · 358 White Eagle Digit 2GR/3GR · 358 White Eagle T3 2GR/3GR + Nuova Simonelli Musica Standart AD) — **8 blknochg** (genuine RU отдельный, `nmRU==nazvRU` True, LIVE НЕ переписан, fixed.xlsx НЕ трогался) + 0 blk триплет + 0 blknotrip + 0 SKIP-НП; Victoria Arduino + Nuova Simonelli НЕ в НП-списке → обычная обработка. 1 soft-note НЕ нумер. (SKU32 Артикул 2101838139 Nuova Simonelli Musica Standart AD — genuine RU короче UA, опускает строку-заголовок списка UA `<li>Оснащення бойлера:</li>`; имена col4-7 консистентны → НЕ нумер. OQ). +0 строк глоссария (кумул. 166 без изменений).

Здесь собираю всё, что требует твоего подтверждения (не авто-фиксы). Авто-фиксы по locked-паттернам перечислены в сводках по батчам, отдельного подтверждения не требуют. Открытые вопросы накапливаются в нумерованный список и финализируются при закрытии chunk-057. SKIP-НП SKU (НП-эксклюзивные бренды) перечисляются отдельным списком — тело придёт из фида НП позже, RU не трогается.

---

## SKIP-НП chunk-057 (НП-эксклюзивные бренды — RU не переписан)

_(Бренд-состав chunk-057 определяется per-SKU по `Название` (колонка `Бренд` в источнике дублирует числовой `Артикул`, бренд по ней не читается). Зонд chunk-057: NP-suspect hit 1 → **SKU54 (Артикул `525346665`) `Соковижималка для цитрусових Apach ACS1 ECO`** — бренд **Apach** в НП-списке HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA → ожидается SKIP-НП (вносится в таблицу при обработке батча 7, SKU 49-54). Прочие бренды (Hendi, Victoria Arduino, …) НЕ в НП-списке — обрабатываются обычно. Список и таблица обновляются per-батч при подтверждении бренда по `Название`. **Батч 1 (SKU 1-8): подтверждены Hendi (кофемашина 208991 / нок-боксы 208335 · 208618 / подставка кофемолки 208694) + Victoria Arduino (Black Eagle Maverick Gravimetric/Volumetric 2GR/3GR) по `Название` — НИ ОДИН не в НП-списке, обработан обычно, SKIP-НП 0.** **Батч 2 (SKU 9-16): подтверждён Victoria Arduino (Black Eagle VA388 Gravimetric/Volumetric 2GR/3GR · Eagle One 2GR/3GR · Eagle Tempo T3 2GR/3GR) по `Название` — НЕ в НП-списке, обработан обычно (8 blknochg), SKIP-НП 0.** **Батч 3 (SKU 17-24): подтверждён Victoria Arduino (Eagle Tempo Digit 2GR/3GR · 358 White Eagle Leva 2GR/3GR · Adonis 2GR/3GR · Adonis 1905 2GR/3GR) по `Название` — НЕ в НП-списке, обработан обычно (8 blknochg), SKIP-НП 0.** **Батч 4 (SKU 25-32): подтверждены Victoria Arduino (Eagle One Prima PRO/EXP/Prima · 358 White Eagle Digit 2GR/3GR · 358 White Eagle T3 2GR/3GR) + Nuova Simonelli (Musica Standart AD) по `Название` — НЕ в НП-списке, обработан обычно (8 blknochg), SKIP-НП 0.** **Батч 5 (SKU 33-40): подтверждён Nuova Simonelli (Musica Lux · Appia Life XT 2Gr V / 3Gr S / 3Gr V · Aurelia Wave 2Gr S/V · Aurelia Wave T3 2Gr/3Gr) по `Название` — НЕ в НП-списке, обработан обычно (8 blknochg), SKIP-НП 0.**)_

| # | SKU | Артикул | Бренд | Название (UA) | Статус |
|---|---|---|---|---|---|

---

## Открытые вопросы chunk-057

_(нумерация Открытых вопросов chunk-057 — отдельная, начинается с #1 при первом сомнении. Кумул. контекст из других chunk (тоже ждут ответа Yana): OQ#1 SKU 10 chunk-055 Hendi 843468/843499; OQ#1 SKU 67 chunk-056 Nuova Simonelli APPIA II V 1GR ↔ Appia Life V 1Gr рассинхрон модель-кода. Полные версии вопросов — в chunk-055-MANUAL-REVIEW.md / chunk-056-MANUAL-REVIEW.md соответственно.)_

_(пусто — нумерованных Открытых вопросов chunk-057 пока нет.)_

---
