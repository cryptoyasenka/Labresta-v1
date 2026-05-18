# chunk-056 — ручная проверка для Yana (русский)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-056 (91 SKU)
**Apply key:** `Артикул` (scoped per row)
**Status:** IN PROGRESS 88/91 (blknochg 25 / blk триплет 61 / blknotrip 2 / SKIP-НП 0; Открытых вопросов 1)
**Worker:** W2 (параллельный, диапазон chunk-055 … chunk-085)
**Last updated:** батч 11 (SKU 81-88, Nuova Simonelli Oscar Mood Tank + Hendi Concept Line 211472 / PROFI LINE 208533 + Bartscher 190193 + Saro ECO + GGM KC2W / KC3S / KC3W) — 3 blk триплет (SKU 82/83/88, Назв.мод RU UA-leak → genuine Назв RU(col7) + полный RU desc replace-from-source, авто-фиксы по locked-паттернам) + 5 blknochg (SKU 81 Nuova Simonelli Oscar Mood Tank / 84 Saro ECO / 85 GGM KC2W / 86 GGM KC3S / 87 GGM KC3W — genuine отдельный RU, descUA != descRU, LIVE НЕ переписан, fixed.xlsx не трогается) + 0 blknotrip; реальные дроби SKU83 `6.5`→`6,5`/`7.82`→`7,82` (UA-копия → десятичная запятая), UA-уже-запятая `1,8`(SKU88) сохранена; габариты `307x330x (В) 450`(SKU82 Latin x+Cyrillic (В))/`204х380х425 мм`(SKU88 Cyrillic х=0x445)/genuine `205x385x435`(SKU84)/`750 х 620 х 510`/`960 х 620 х 510`(SKU85/86/87 genuine) — dim-integrity blk-триплетов byte-точно (src==res); UA-апостроф `&#39;`→0 в RU (SKU83 `Объем`/`интерьер`); валидатор UA_MARK: сняты 2 false-positive `Перколятор`(идентично UA/RU, как `темного дерева` b10) + `Контрольна`(префикс RU `Контрольная`); **Новых нумерованных Открытых вопросов в батче НЕТ**; **3 soft-note** (НЕ нумерованные OQ): SKU82 UA-источник тело `Кавоварку` при имени `Кавомашина`/genuine Назв RU `Кофемашина` (рассогл. тело/имя в UA-копии, переведено верно источнику, структурный source-quirk сохранён), SKU85/86/87 GGM genuine RU `изляция`→норма `изоляция` (UA зеркалит `ізляція`, консолидир. 1 soft-note на 3 SKU, прец. SKU63 b8), SKU81 genuine RU тело `кофеварка` при имени `Кофемашина` (зеркалит UA-источник, genuine отдельный рус., blknochg не трогается); soft-note 3; Открытых вопросов 1

Здесь собираю всё, что требует твоего подтверждения (не авто-фиксы). Авто-фиксы по locked-паттернам перечислены в сводках по батчам, отдельного подтверждения не требуют. Открытые вопросы накапливаются в нумерованный список и финализируются при закрытии chunk-056. SKIP-НП SKU (НП-эксклюзивные бренды) перечисляются отдельным списком — тело придёт из фида НП позже, RU не трогается.

---

## SKIP-НП chunk-056 (НП-эксклюзивные бренды — RU не переписан)

_(пусто. Бренд-состав chunk-056: Robot Coupe 39 / Fimar 14 / Hendi 12 / Nuova Simonelli 9 / FROSTY 7 / Bezzera 4 / GGM Gastro International 4 / Bartscher 1 / Saro 1 — ни один не в НП-списке HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA → ожидается SKIP-НП 0. Список обновляется per-батч при подтверждении бренда по `Название`. **Батч 1 (SKU 1-8): подтверждён бренд Fimar по `Название` (Диск для овочерізки FIMAR …) — НЕ в НП-списке, обработан обычно, SKIP-НП 0. Батч 2 (SKU 9-16): подтверждены Fimar (Z3/Z4/Z7/Z2), FROSTY (D8/D10), Robot Coupe (27070/27164) по `Бренд`/`Название` — НИ ОДИН не в НП-списке, SKIP-НП 0. Батч 3 (SKU 17-24): подтверждён бренд Robot Coupe (диски 28004/28016/28051/28052/28053/28054/28057/28058) по `Бренд`/`Название` — НЕ в НП-списке, обработан обычно, SKIP-НП 0. Батч 4 (SKU 25-32): подтверждён бренд Robot Coupe (диски 28059/28061/28062/28063/28064/28065/28101/28110) по `Бренд`/`Название` — НЕ в НП-списке, обработан обычно, SKIP-НП 0. Батч 5 (SKU 33-40): подтверждён бренд Robot Coupe (диски 28111/28114/28134/28135/28195/28197 + комплекты дисков 1960/1961) по `Бренд`/`Название` — НЕ в НП-списке, обработан обычно, SKIP-НП 0. Батч 6 (SKU 41-48): подтверждены Robot Coupe (28189/27069/28067) + FROSTY (E2/D8A/D10А/D12А/D20A) по `Бренд`/`Название` — НИ ОДИН не в НП-списке, обработан обычно, SKIP-НП 0. Батч 7 (SKU 49-56): подтверждены Robot Coupe (28173/28073/27219/28115/28113/1933/28208) + Fimar (E2) по `Бренд`/`Название` — НИ ОДИН не в НП-списке, обработан обычно, SKIP-НП 0. Батч 8 (SKU 57-64): подтверждены Robot Coupe (27786/28112/1945) + Fimar (A2) + Bezzera (Arcadia/ARCA1DE2NG3) + GGM Gastro International (Catarina KMF2) + Nuova Simonelli (OSCAR II) по `Бренд`/`Название` — НИ ОДИН не в НП-списке, обработан обычно, SKIP-НП 0. Батч 9 (SKU 65-72): подтверждены Nuova Simonelli (APPIA LIFE S 2GR / Appia Life 1Gr S / APPIA II V 1GR / Appia Compact Life S 2GR / APPIA LIFE V 2GR) + Hendi (208656 / 428245 / 208342) по `Бренд`/`Название` — НИ ОДИН не в НП-списке, обработан обычно, SKIP-НП 0. Батч 10 (SKU 73-80): подтверждены Hendi (208380 / 208649 / 208670 / 208731) + Nuova Simonelli (Appia Compact Life V 2GR / Oscar II AD) + Bezzera (B2016 DE/White / B2016 PM//White) по `Бренд`/`Название` — НИ ОДИН не в НП-списке, обработан обычно, SKIP-НП 0. Батч 11 (SKU 81-88): подтверждены Nuova Simonelli (Oscar Mood Tank) + Hendi (Concept Line 211472 / PROFI LINE 208533) + Bartscher (190193) + Saro (ECO) + GGM Gastro International (KC2W / KC3S / KC3W) по `Бренд`/`Название` — НИ ОДИН не в НП-списке, обработан обычно, SKIP-НП 0.**)_

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
