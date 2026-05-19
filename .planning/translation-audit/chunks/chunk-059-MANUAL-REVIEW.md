# chunk-059 — ручная проверка для Yana (русский)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-059 (96 SKU)
**Apply key:** `Артикул` (scoped per row)
**Status:** IN PROGRESS 32/96 (blk триплет 18 / blknochg 12 / blknotrip 0 / SKIP-НП 2; Открытых вопросов 0)
**Worker:** W2 (параллельный, диапазон chunk-055 … chunk-085)
**Last updated:** chunk-059 батч 4 (SKU 25-32) → 32/96. **2 SKIP-НП** — HURAKAN (НП-эксклюзивный бренд): SKU25 Арт 2503655839 `Міксер для молочних коктейлів HURAKAN HKN-FR1GD` · SKU26 Арт 2503663450 `Міксер для молочних коктейлів HURAKAN HKN-FR2GD`. Бренд **HURAKAN** ∈ НП-список (HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA), подтверждён по `Название` → forward-only: распознан → внесён в таблицу SKIP-НП ниже + тег в diff → следующий SKU; RU/перевод/зонд-скрипты/scratch-дамп НЕ применялись, ячейки chunk-059-fixed.xlsx не менялись (тело придёт из фида НП позже). **6 blknochg** — SKU27 GGM SML1 Арт 508329227 · SKU28 GGM SML3 Арт 508329228 · SKU29 Vema FL2005/L Арт 524929657 · SKU30 Quamar T2 inox (0,5 л) Арт 1160094133 · SKU31 Quamar T22 inox (2х0,5 л) Арт 1160105593 · SKU32 Hamilton Beach HMD400CE Арт 1205750702: `descUA==descRU` False, RU genuine отдельный самостоятельный, `nmRU==nazvRU` True (col5==col7 genuine RU), LIVE НЕ переписан, в chunk-059-fixed.xlsx строки НЕ трогаются == source. **blk триплет 0 / blknotrip 0** — в батче нет переписываемых строк → **chunk-059-fixed.xlsx НЕ трогался, apply/verify не выполнялись** (файл остаётся 18 blk rows = 8 b1 + 6 b2 + 4 b3 как после b3). GGM/Vema/Quamar/Hamilton Beach НЕ в НП-списке (подтверждено по `Название`); НП-suspect chunk-059 остаётся SKU91 б12 (Hurakan, Арт 2373825799). **Soft-note НЕ нумер. ~1**: SKU30/31 META keywords (col24/25) faithful UA↔RU содержат ключи чужой модели `Vema FL2006/L` внутри Quamar-товаров (SEO-стаффинг, не покупателю, META никогда не переписывается/не анализируется) — не нумерованный OQ; genuine RU SKU27/28 `Объем:` твёрдый знак Ъ корректно (quirk `Обьем` SKU12/16/17/18 здесь отсутствует); SKU29 genuine RU уже `об/мин` (LIVE как есть, не наша правка); SKU32 genuine RU чистый. META keywords (col24/25) faithful, не трогались. Soft-note ~1; новых нумерованных Открытых вопросов нет; **Открытых вопросов chunk-059 итого 0**. Глоссарий W2: 0 net-new (SKIP-НП + blknochg не порождают применённых UA→RU терминов — кумул. 276 без изменений, footer chunk-glossary-w2.md). Кумул. ждут Yana (отд. нумерация): OQ#1 SKU 10 chunk-055; OQ#1 SKU 67 chunk-056; OQ#1 SKU 31 chunk-058. Следующий: батч SKU 33-40 (openpyxl rows 34..41).

**Last updated (chunk-059 б3 — предыдущий шаг):** chunk-059 батч 3 (SKU 17-24) → 24/96 COMMITTED. **4 blk триплет** молочные миксеры (SKU21 Hendi 221617 · SKU22 Hamilton Beach HMD400RCE · SKU23 Sirman Sirio 2 VV ХРОМ 900CC · SKU24 Bartscher 135105 — `descUA==descRU` True, col5←col7 genuine + col36 тег-в-tag RU; dims label-only кир.х `300х195х530` SKU23, `&divide;` verbatim, trailing-space packaging-блок SKU22/24, ` : ` пробел verbatim, реальные `4.76`/`16.3`/`6.22` и т.д.→`,`). **4 blknochg** SKU17 Goodfood MFD33 · SKU18 Goodfood MFD44 · SKU19 Sirman Sirio 1 CC 900 · SKU20 Sirman Sirio 2 900CC (genuine отдельный RU, `nmRU==nazvRU` True, LIVE НЕ переписан, fixed.xlsx не трогается). blknotrip 0 / SKIP-НП 0. **chunk-059-fixed.xlsx загружен СУЩЕСТВУЮЩИЙ** + 4 blk rows (18 всего), reopen-verify `=== ALL OK ===`. ~4 soft-note НЕ нумер. (SKU17/18 `Обьем стакана :`, SKU20/23 `CC 900↔900CC`); Открытых вопросов chunk-059 итого 0. Глоссарий W2 +10 → 276.

Здесь собираю всё, что требует твоего подтверждения (не авто-фиксы). Авто-фиксы по locked-паттернам перечислены в сводках по батчам, отдельного подтверждения не требуют. Открытые вопросы накапливаются в нумерованный список и финализируются при закрытии chunk-059. SKIP-НП SKU (НП-эксклюзивные бренды) перечисляются отдельным списком — тело придёт из фида НП позже, RU не трогается.

---

## SKIP-НП chunk-059 (НП-эксклюзивные бренды — RU не переписан)

_(Бренд-состав chunk-059 определяется per-SKU по `Название` (колонка `Бренд` в источнике дублирует числовой `Артикул`, бренд по ней не читается). Зонд chunk-059: **3 NP-suspect hits** в НП-списке HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA → SKIP-НП: **Hurakan ×3** — SKU25 (Артикул `2503655839`) `Міксер для молочних коктейлів HURAKAN HKN-FR1GD` (батч 4 — **обработан, внесён в таблицу ниже #1**), SKU26 (`2503663450`) `Міксер для молочних коктейлів HURAKAN HKN-FR2GD` (батч 4 — **обработан, #2**), SKU91 (`2373825799`) `Блендер Hurakan HKN-HBH850M PRO COVER` (батч 12 — **впереди**). Прочие бренды (Bartscher, Frosty, EWT INOX, Hamilton Beach, Sirman, CEADO, JAU, Goodfood, Fimar, Hendi, GGM, Vema, Quamar, SARO, UGOLINI, CAB, Sirman, …) НЕ в НП-списке — обрабатываются обычно. Список и таблица обновляются per-батч при подтверждении бренда по `Название`.)_

| # | SKU | Артикул | Бренд | Название (UA) | Статус |
|---|---|---|---|---|---|
| 1 | SKU25 | 2503655839 | HURAKAN | Міксер для молочних коктейлів HURAKAN HKN-FR1GD | SKIP-НП (тело придёт из фида НП позже, RU не трогался) |
| 2 | SKU26 | 2503663450 | HURAKAN | Міксер для молочних коктейлів HURAKAN HKN-FR2GD | SKIP-НП (тело придёт из фида НП позже, RU не трогался) |

---

## Открытые вопросы chunk-059

_(нумерация Открытых вопросов chunk-059 — отдельная, начинается с #1 при первом сомнении. Кумул. контекст из других chunk (тоже ждут ответа Yana): OQ#1 SKU 10 chunk-055 Hendi 843468/843499; OQ#1 SKU 67 chunk-056 Nuova Simonelli APPIA II V 1GR ↔ Appia Life V 1Gr рассинхрон модель-кода; OQ#1 SKU 31 chunk-058 Cancan 0103 — чужой товар (GoodFood FJ150) в лид-абзаце genuine RU-описания. Полные версии вопросов — в chunk-055-MANUAL-REVIEW.md / chunk-056-MANUAL-REVIEW.md / chunk-058-MANUAL-REVIEW.md соответственно.)_

_(Пока пусто — Открытых вопросов chunk-059 нет. Первый вопрос получит #1.)_
