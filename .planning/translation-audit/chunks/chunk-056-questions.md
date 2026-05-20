# chunk-056 — questions for Yana (W2) — ANSWERED

**Status:** OQ #1 ANSWERED Yana 2026-05-21 (через AskUserQuestion). Решения сохранены в `.planning/translation-audit/chunks/W2-OQ-ANSWERS.md` (commit `e2bd5ac`). См. блок «Решение Yana» в конце документа.


Нумерованные Открытые вопросы chunk-056 (customer-facing рассинхрон чисел/модель-кодов источника — НЕ авто-фиксятся, ждут решения Yana). Дублируются в chunk-056-MANUAL-REVIEW.md раздел «Открытые вопросы chunk-056». Soft-notes (НЕ нумерованные, genuine RU дефекты источника, LIVE не трогается) сюда НЕ выносятся — они в diff.md / MANUAL-REVIEW.

Кумулятивный контекст: OQ#1 SKU 10 chunk-055 (Hendi 843468 vs genuine-RU 843499) — отдельная нумерация другого chunk, тоже ждёт Yana.

---

## Открытый вопрос #1 — SKU 67 (Артикул 627378718), бренд Nuova Simonelli: рассинхрон модель-кода Назв UA ↔ genuine Назв RU (`APPIA II V 1GR` vs `Appia Life 1Gr V`)

**Поле:** Название (RU/UA) / Название модификации (RU/UA) — рассинхрон модель-кода

| Локаль / поле | Значение |
|---|---|
| Название (UA) | `Кавомашина Nuova Simonelli **APPIA II V 1GR** (1 група)` |
| Название (RU) — genuine, `descUA==descRU` False | `Кофемашина Nuova Simonelli **Appia Life 1Gr V** (1 группа)` |
| Название модификации (UA) | `Кавомашина Nuova Simonelli **APPIA II V 1GR** (1 група)` |
| Название модификации (RU) | `Кофемашина Nuova Simonelli **Appia Life 1Gr V** (1 группа)` |
| Описание (UA) — текст внутри | `Кавомашина професійна Nuova Simonelli **Appia Life V 1Gr** однопостова…` |
| Описание (RU) — текст внутри | `Кофемашина профессиональная Nuova Simonelli **Appia Life V 1Gr** однопостовая…` |

**Суть:** модель-код в UA-названии и UA-«Название модификации» = `APPIA II V 1GR`, но genuine русское название, русское «Название модификации» **и сам украинский текст описания** говорят `Appia Life V 1Gr` / `Appia Life 1Gr V`. То есть токен `APPIA II` встречается ТОЛЬКО в UA-названии — он расходится даже с собственным UA-описанием этого же SKU. Соседи по батчу — вся линейка Nuova Simonelli **Appia Life**: SKU 65 `APPIA LIFE S 2GR` (Артикул 627354544), SKU 66 `Appia Life 1Gr S` (627375875), SKU 68 `Appia Compact Life S 2GR` (627428248), SKU 69 `APPIA LIFE V 2GR` (627441867). Вариант «APPIA II» в линейке батча больше нигде не встречается. Это видно покупателю в карточке (UA-заголовок `APPIA II V 1GR`, тело UA-описания и вся RU-карточка `Appia Life V 1Gr`).

**Что сделано (по прецеденту OQ#1 SKU 10 chunk-055 / OQ#1 chunk-021 BCB10 vs BCB10 NC):** SKU 67 = blknochg (`descUA != descRU` False — genuine отдельный RU, lenUA=470 lenRU=756, RU с доп. iframe-видео). На LIVE-магазине рассинхрон модель-кода UA↔genuine-RU **без go-ahead Yana НЕ правится**. genuine «Название (RU)» НЕ переписано; «Название модификации (RU)» НЕ флипнуто; fixed.xlsx не трогается (blknochg и так не модифицируется). «Описание товара (RU)» — genuine отдельный RU, тоже не переписывается.

**Нужно решение Yana:** какой код верный для этого SKU — `APPIA II V 1GR` (UA-название) или `Appia Life V 1Gr` (UA-описание + вся RU-карточка)? Гипотеза: опечатка в UA-названии (вся остальная линейка и собственное UA-описание = Appia Life). После ответа: либо выровнять UA Назв/Назв.мод → `Appia Life V 1Gr` (если опечатка в UA-названии), либо подтвердить что это физически другая модель (APPIA II) и развести карточки. До решения карточка на LIVE в части модель-кода не трогается.

---

## Решение Yana (2026-05-21) — OQ #1 ANSWERED

**Канон:** `Appia Life V 1Gr` (опечатка в UA-имени `APPIA II V 1GR`). Вся линейка батча и собственное UA-описание используют `Appia Life`.

**W2 RU side (verified):** `chunk-056-fixed.xlsx` r68 col5/col7 = `Кофемашина Nuova Simonelli Appia Life 1Gr V (1 группа)` — RU уже совпадает с каноном (порядок токенов `1Gr V` vs `V 1Gr` — minor order variation, RU стилистически уже корректна).

**Forward к W1 (UA-правка):** `chunk-056-fixed.xlsx` r68 col4/col6 → выровнять на `Кавомашина Nuova Simonelli Appia Life V 1Gr (1 група)` (поправить опечатку `APPIA II V 1GR`). На момент проверки W2 fixed.xlsx уже содержит правильный UA `Appia Life V 1Gr` — возможно прошлый цикл уже синхронизировал; верифицировать в W1 worktree.


---
