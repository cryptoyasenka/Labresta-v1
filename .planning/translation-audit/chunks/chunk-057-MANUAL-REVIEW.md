# chunk-057 — ручная проверка для Yana (русский)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-057 (54 SKU)
**Apply key:** `Артикул` (scoped per row)
**Status:** IN PROGRESS 16/54 (blk триплет 3 / blknochg 12 / blknotrip 1 / SKIP-НП 0; Открытых вопросов 0)
**Worker:** W2 (параллельный, диапазон chunk-055 … chunk-085)
**Last updated:** батч 2 (SKU 9-16 — Victoria Arduino: Black Eagle VA388 Gravimetric 2GR/3GR · Volumetric 2GR/3GR · Eagle One 2GR/3GR · Eagle Tempo T3 2GR/3GR) — **8 blknochg** (все `descUA==descRU` False — RU genuine отдельный самостоятельный русский текст; `nmRU==nazvRU` True — Назв.мод RU(col5) == genuine Назв RU(col7), UA-leak нет; LIVE genuine RU НЕ переписываем, fixed.xlsx НЕ трогается — остаётся как в источнике) + **0 blk триплет** + **0 blknotrip** + **0 SKIP-НП**. Подтверждено по `Название`: Victoria Arduino НЕ в НП-списке HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA → обработан обычно, SKIP-НП 0. Переводимых UA-копий в батче нет → реальных `.`-дробей не нормализовали, новых glossary-терминов не извлекали (genuine RU не переписывается), апостроф/габариты-инварианты не применялись (нет правок). META keywords не трогались. **Новых нумерованных Открытых вопросов в батче НЕТ**; **2 soft-note** (НЕ нумер. OQ, genuine RU не переписываем — только заметка): SKU9 (Артикул 2099721135) UA-остаток-фрагмент 3-й `<p>3 бойлери: 1 паровий - 11 л + бойлер на кожну групу - 0,6 л + ТЕН у кожній групі.</p>` внутри самостоятельного genuine RU (descUA отличается; UA-источник тот же абзац с `шкірну/шкірній` — UA source-mistranslation «each», RU зеркалит корректное `кожну/кожній`); SKU14 (Артикул 2099927652) дублирование модели `Eagle One Eagle One` в открывающем `<p>` — консистентно в UA и genuine RU (language-neutral source-quirk). Мелкие наблюдения (НЕ soft-note, UA col35 не трогается): SKU13/15 UA-источник `Потужність, квт N.0` строчное `квт` при корректном genuine RU `Мощность, кВт N.0`. Открытых вопросов 0 (кумул. ждут Yana: OQ#1 SKU10 chunk-055; OQ#1 SKU67 chunk-056 — отдельная нумерация). +0 строк глоссария (батч полностью blknochg; кумул. 166 без изменений).

**Last updated (предыдущий шаг):** батч 1 (SKU 1-8 — Hendi кофемашина PROFI LINE XXL 208991 + нок-боксы GN1/6 208335 · круглый 208618 + подставка кофемолки 208694; Victoria Arduino Black Eagle Maverick Gravimetric/Volumetric 2GR/3GR) — **3 blk триплет** (SKU1 Назв.мод RU(col5) UA-leak `Кавомашина`→genuine Назв RU(col7) `Кофемашина` + смешанная UA/RU UA-копия desc переведена replace-from-source; SKU3 `круглий`→`круглый`; SKU4 `Підставка для кавомолки`→`Подставка для кофемолки`) + **1 blknotrip** (SKU2 нок-бокс GN1/6 208335) + **4 blknochg** (SKU5-8 Victoria Arduino Black Eagle Maverick — genuine отдельный RU desc, LIVE НЕ переписан) + **0 SKIP-НП**. Faithful-фикс `Зроблений/зроблений`→`Сделан/сделан` (SKU2/SKU4), НЕ `Изготовлен`. Норм. source-typo SKU1 `208991серии`→`208991 серии` + `подачі пари 3-120 з`→`…3-120 с`; UA grammar quirk SKU3 `Прогумоване підставу і краю`. 3 soft-note НЕ нумер. (SKU1 смешанная UA/RU UA-копия; SKU5-8 Latin `Volumentric`; SKU8 UA-остаток `<p>T3 Genius…</p>` в genuine RU). +12 строк глоссария (кумул. 154 → 166).

Здесь собираю всё, что требует твоего подтверждения (не авто-фиксы). Авто-фиксы по locked-паттернам перечислены в сводках по батчам, отдельного подтверждения не требуют. Открытые вопросы накапливаются в нумерованный список и финализируются при закрытии chunk-057. SKIP-НП SKU (НП-эксклюзивные бренды) перечисляются отдельным списком — тело придёт из фида НП позже, RU не трогается.

---

## SKIP-НП chunk-057 (НП-эксклюзивные бренды — RU не переписан)

_(Бренд-состав chunk-057 определяется per-SKU по `Название` (колонка `Бренд` в источнике дублирует числовой `Артикул`, бренд по ней не читается). Зонд chunk-057: NP-suspect hit 1 → **SKU54 (Артикул `525346665`) `Соковижималка для цитрусових Apach ACS1 ECO`** — бренд **Apach** в НП-списке HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA → ожидается SKIP-НП (вносится в таблицу при обработке батча 7, SKU 49-54). Прочие бренды (Hendi, Victoria Arduino, …) НЕ в НП-списке — обрабатываются обычно. Список и таблица обновляются per-батч при подтверждении бренда по `Название`. **Батч 1 (SKU 1-8): подтверждены Hendi (кофемашина 208991 / нок-боксы 208335 · 208618 / подставка кофемолки 208694) + Victoria Arduino (Black Eagle Maverick Gravimetric/Volumetric 2GR/3GR) по `Название` — НИ ОДИН не в НП-списке, обработан обычно, SKIP-НП 0.** **Батч 2 (SKU 9-16): подтверждён Victoria Arduino (Black Eagle VA388 Gravimetric/Volumetric 2GR/3GR · Eagle One 2GR/3GR · Eagle Tempo T3 2GR/3GR) по `Название` — НЕ в НП-списке, обработан обычно (8 blknochg), SKIP-НП 0.**)_

| # | SKU | Артикул | Бренд | Название (UA) | Статус |
|---|---|---|---|---|---|

---

## Открытые вопросы chunk-057

_(нумерация Открытых вопросов chunk-057 — отдельная, начинается с #1 при первом сомнении. Кумул. контекст из других chunk (тоже ждут ответа Yana): OQ#1 SKU 10 chunk-055 Hendi 843468/843499; OQ#1 SKU 67 chunk-056 Nuova Simonelli APPIA II V 1GR ↔ Appia Life V 1Gr рассинхрон модель-кода. Полные версии вопросов — в chunk-055-MANUAL-REVIEW.md / chunk-056-MANUAL-REVIEW.md соответственно.)_

_(пусто — нумерованных Открытых вопросов chunk-057 пока нет.)_

---
