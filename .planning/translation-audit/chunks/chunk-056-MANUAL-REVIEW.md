# chunk-056 — ручная проверка для Yana (русский)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-056 (91 SKU)
**Apply key:** `Артикул` (scoped per row)
**Status:** IN PROGRESS 72/91 (blknochg 16 / blk триплет 55 / blknotrip 1 / SKIP-НП 0; Открытых вопросов 1)
**Worker:** W2 (параллельный, диапазон chunk-055 … chunk-085)
**Last updated:** батч 9 (SKU 65-72, Nuova Simonelli APPIA LIFE S 2GR / Appia Life 1Gr S / APPIA II V 1GR / Appia Compact Life S 2GR / APPIA LIFE V 2GR + Hendi 208656 фильтры / 428245 диспенсер / 208342 нок-бокс) — 2 blk триплет (SKU 70/71 Hendi, Назв.мод RU UA-leak → genuine + полный RU desc replace-from-source, авто-фиксы по locked-паттернам) + 1 blknotrip (SKU 72 Hendi нок-бокс — Назв/Назв.мод RU = бренд+код `Нок-бокс GN1/4 Hendi 208342` language-neutral == UA, триплет НЕ требуется, только Описание RU = UA-копия → полный RU-перевод) + 5 blknochg (SKU 65/66/67/68/69 кофемашины Nuova Simonelli — genuine отдельный RU, descUA != descRU, LIVE НЕ переписан, fixed.xlsx не трогается); габариты `Ø250x(H)70мм`(SKU70)/`190x240x(H)410 мм`(SKU71)/`265x162x(H): 100 мм`(SKU72) Latin x(0078) — dim-integrity check byte-точно (src==res); UA-апостроф `об'ємом`→`объемом` SKU71→0; UA-копия quirks нормализованы в RU `расправленного`(SKU70)/`кавовій таблетки`→`кофейной таблетки`(SKU72); **🔶 Открытый вопрос #1 (chunk-056):** SKU67 Nuova Simonelli — Назв/Назв.мод UA `APPIA II V 1GR` ↔ genuine RU `Appia Life 1Gr V` (UA-описание само = `Appia Life V 1Gr`), customer-facing рассинхрон модель-кода → numbered OQ, НЕ авто-фикс (см. chunk-056-questions.md); **1 soft-note** (НЕ нумерованный OQ): SKU66 genuine RU `теплообмеником`→норма `теплообменником` (UA-источник корректен `теплообмінником`, дефект только в genuine RU, прец. soft-note SKU56/62/63); soft-note 1; Открытых вопросов 1

Здесь собираю всё, что требует твоего подтверждения (не авто-фиксы). Авто-фиксы по locked-паттернам перечислены в сводках по батчам, отдельного подтверждения не требуют. Открытые вопросы накапливаются в нумерованный список и финализируются при закрытии chunk-056. SKIP-НП SKU (НП-эксклюзивные бренды) перечисляются отдельным списком — тело придёт из фида НП позже, RU не трогается.

---

## SKIP-НП chunk-056 (НП-эксклюзивные бренды — RU не переписан)

_(пусто. Бренд-состав chunk-056: Robot Coupe 39 / Fimar 14 / Hendi 12 / Nuova Simonelli 9 / FROSTY 7 / Bezzera 4 / GGM Gastro International 4 / Bartscher 1 / Saro 1 — ни один не в НП-списке HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA → ожидается SKIP-НП 0. Список обновляется per-батч при подтверждении бренда по `Название`. **Батч 1 (SKU 1-8): подтверждён бренд Fimar по `Название` (Диск для овочерізки FIMAR …) — НЕ в НП-списке, обработан обычно, SKIP-НП 0. Батч 2 (SKU 9-16): подтверждены Fimar (Z3/Z4/Z7/Z2), FROSTY (D8/D10), Robot Coupe (27070/27164) по `Бренд`/`Название` — НИ ОДИН не в НП-списке, SKIP-НП 0. Батч 3 (SKU 17-24): подтверждён бренд Robot Coupe (диски 28004/28016/28051/28052/28053/28054/28057/28058) по `Бренд`/`Название` — НЕ в НП-списке, обработан обычно, SKIP-НП 0. Батч 4 (SKU 25-32): подтверждён бренд Robot Coupe (диски 28059/28061/28062/28063/28064/28065/28101/28110) по `Бренд`/`Название` — НЕ в НП-списке, обработан обычно, SKIP-НП 0. Батч 5 (SKU 33-40): подтверждён бренд Robot Coupe (диски 28111/28114/28134/28135/28195/28197 + комплекты дисков 1960/1961) по `Бренд`/`Название` — НЕ в НП-списке, обработан обычно, SKIP-НП 0. Батч 6 (SKU 41-48): подтверждены Robot Coupe (28189/27069/28067) + FROSTY (E2/D8A/D10А/D12А/D20A) по `Бренд`/`Название` — НИ ОДИН не в НП-списке, обработан обычно, SKIP-НП 0. Батч 7 (SKU 49-56): подтверждены Robot Coupe (28173/28073/27219/28115/28113/1933/28208) + Fimar (E2) по `Бренд`/`Название` — НИ ОДИН не в НП-списке, обработан обычно, SKIP-НП 0. Батч 8 (SKU 57-64): подтверждены Robot Coupe (27786/28112/1945) + Fimar (A2) + Bezzera (Arcadia/ARCA1DE2NG3) + GGM Gastro International (Catarina KMF2) + Nuova Simonelli (OSCAR II) по `Бренд`/`Название` — НИ ОДИН не в НП-списке, обработан обычно, SKIP-НП 0. Батч 9 (SKU 65-72): подтверждены Nuova Simonelli (APPIA LIFE S 2GR / Appia Life 1Gr S / APPIA II V 1GR / Appia Compact Life S 2GR / APPIA LIFE V 2GR) + Hendi (208656 / 428245 / 208342) по `Бренд`/`Название` — НИ ОДИН не в НП-списке, обработан обычно, SKIP-НП 0.**)_

| # | SKU | Артикул | Бренд | Название (UA) | Статус |
|---|---|---|---|---|---|

---

## Открытые вопросы chunk-056

_(нумерация Открытых вопросов chunk-056 — отдельная. Кумул. контекст: OQ#1 SKU 10 chunk-055 Hendi 843468/843499 — другой chunk, тоже ждёт ответа Yana. Полная версия вопроса ниже также в chunk-056-questions.md.)_

### Открытый вопрос #1 — SKU 67 (Артикул 627378718), бренд Nuova Simonelli: рассинхрон модель-кода Назв UA ↔ genuine Назв RU

**Поле:** Название (RU/UA) / Название модификации (RU/UA) — рассинхрон модель-кода

| Локаль / поле | Значение |
|---|---|
| Название (UA) | `Кавомашина Nuova Simonelli APPIA II V 1GR (1 група)` |
| Название (RU) — genuine, `descUA==descRU` False | `Кофемашина Nuova Simonelli Appia Life 1Gr V (1 группа)` |
| Название модификации (UA) | `Кавомашина Nuova Simonelli APPIA II V 1GR (1 група)` |
| Название модификации (RU) | `Кофемашина Nuova Simonelli Appia Life 1Gr V (1 группа)` |
| Описание (UA) — текст внутри | `Кавомашина професійна Nuova Simonelli Appia Life V 1Gr однопостова…` |
| Описание (RU) — текст внутри | `Кофемашина профессиональная Nuova Simonelli Appia Life V 1Gr однопостовая…` |

**Суть:** модель-код в UA-названии и UA-«Название модификации» = `APPIA II V 1GR`, но genuine русское название, русское «Название модификации» **и сам украинский текст описания** говорят `Appia Life V 1Gr` / `Appia Life 1Gr V`. Токен `APPIA II` встречается ТОЛЬКО в UA-названии — расходится даже с собственным UA-описанием. Соседи по батчу — вся линейка Nuova Simonelli **Appia Life**: SKU 65 `APPIA LIFE S 2GR`, SKU 66 `Appia Life 1Gr S`, SKU 68 `Appia Compact Life S 2GR`, SKU 69 `APPIA LIFE V 2GR`; «APPIA II» больше нигде. Customer-facing (UA-заголовок vs тело UA + вся RU-карточка).

**Что сделано (прец. OQ#1 SKU 10 chunk-055 / OQ#1 chunk-021 BCB10 vs BCB10 NC):** SKU 67 = blknochg (`descUA != descRU` False — genuine отдельный RU). Рассинхрон модель-кода UA↔genuine-RU на LIVE **без go-ahead Yana НЕ правится**. genuine «Название (RU)» НЕ переписано; «Название модификации (RU)» НЕ флипнуто; fixed.xlsx не трогается (blknochg).

**Нужно решение Yana:** какой код верный — `APPIA II V 1GR` (UA-название) или `Appia Life V 1Gr` (UA-описание + вся RU-карточка)? Гипотеза: опечатка в UA-названии. После ответа: либо выровнять UA Назв/Назв.мод → `Appia Life V 1Gr`, либо подтвердить что это другая модель и развести карточки. До решения LIVE в части модель-кода не трогается.

---
