# CURRENT-w2 — LabResta translation audit (W2 параллельный воркер)

**Last touched:** 2026-05-18 (батч 5 SKU 33-40)
**Status:** chunk-055 батч 5 (SKU 33-40) COMMITTED 40/86, Открытый вопрос #1 (SKU 10 модель-код), next батч SKU 41-48

> **РЕЖИМ: НЕПРЕРЫВНЫЙ НОЧНОЙ (Yana 2026-05-18).** НЕ останавливаться после одного батча. После коммита+push сразу следующий батч (range +8), пока весь диапазон chunk-055…085 не закрыт. Контекст переполнился → снапшот+auto-compact+restore из этого файла, продолжать. Cron 15m = только страховка на смерть сессии. Стоп только: весь диапазон готов, ИЛИ нужен ответ Yana (тогда зафиксировать OQ и идти дальше по остальным SKU). См. memory `feedback-w2-continuous-night-mode`.

## Диапазон W2
- ТОЛЬКО chunk-055 … chunk-085. НИКОГДА не трогать chunk-≤054 (W1) и не редактировать main.
- Ветка: `translation-audit/w2`. Push в `origin translation-audit/w2` (НЕ main).
- State-файл W2: этот файл. НЕ трогать `.planning/CURRENT.md` (W1).

## Status
- [x] CURRENT-w2.md создан (первый заход W2)
- [x] chunk-055 scaffold: `chunk-055-diff.md` + `chunk-055-MANUAL-REVIEW.md` + `chunk-glossary-w2.md`
- [x] chunk-055.xlsx source скопирован в W2 (gitignored, read-only)
- [x] chunk-055 батч SKU 1-8 → 8/86 (blknochg 4 / blk триплет 2 / blknotrip 2 / SKIP-НП 0; OQ 0)
- [x] chunk-055 батч SKU 9-16 → 16/86 (blknotrip 4 / blk триплет 2 / blknochg 2 / SKIP-НП 0; OQ#1 SKU 10 модель-код)
- [x] chunk-055 батч SKU 17-24 → 24/86 (blknochg 3 / blk триплет 5 / blknotrip 0 / SKIP-НП 0; OQ 0, кумул. OQ#1 SKU 10)
- [x] chunk-055 батч SKU 25-32 → 32/86 (blk триплет 3 / blknochg 3 / SKIP-НП 2 (Hurakan 27/29) / blknotrip 0; OQ 0, кумул. OQ#1 SKU 10)
- [x] chunk-055 батч SKU 33-40 → 40/86 (blknochg 7 (Dadaux 33-37 + Sirman 38/39) / blk триплет 1 (Fimar SE1550 SKU 40) / SKIP-НП 0 / blknotrip 0; OQ 0, кумул. OQ#1 SKU 10)
- [ ] chunk-055 батч SKU 41-48 (next)
- [ ] chunk-055 батчи 49-86 (батч = 8 SKU)
- [ ] chunk-056 … chunk-085

## chunk-055 факты
- 86 SKU. Первый: Артикул `2204681685` Sirman `Ковбасний шприц Sirman IS V 15 IDRA (220В)`. Последний: `2134945850` Fimar `Диск для овочерізки FIMAR E8`.
- Бренды: FROSTY 33, Fimar 19, Sirman 11, Dadaux 8, Hendi 5, GoodFood 5, **Hurakan 2 (SKIP-НП)**, KT 1, Fama 1, Airhot 1.
- SKIP-НП в этом чанке: 2 × Hurakan (RU не трогать, пометить в MANUAL-REVIEW, считать отдельной категорией в N/N).

## Open files
- `.planning/translation-audit/chunks/chunk-055-diff.md` — diff (0/86)
- `.planning/translation-audit/chunks/chunk-055-MANUAL-REVIEW.md` — ручная проверка (0/86)
- `.planning/translation-audit/chunks/chunk-glossary-w2.md` — сводный глоссарий W2
- `.planning/translation-audit/chunks/chunk-055.xlsx` — source (read-only, gitignored)
- `.planning/translation-audit/chunks/chunk-055-fixed.xlsx` — ещё не создан (создаётся при первом батче)

## Next step
chunk-055 батч SKU 41-48. Дамп: `C:/Projects/labresta-sync/.venv/Scripts/python.exe` + openpyxl, range(41,49) по `.planning/translation-audit/chunks/chunk-055.xlsx`. Для каждого SKU: SKIP-НП-чек бренда (Hurakan/Apach/Fagor/Tatra/Cold/PROJECT SYSTEMS/Astoria/Arris/Maxima — case-insensitive, лат+кир; **KT/Fimar/Dadaux/GoodFood и пр. НЕ в списке → обычная обработка**) → если в списке пометить «SKIP-НП (brand=X…)» в MANUAL-REVIEW, ячейки fixed.xlsx не менять, считать отд. категорией; иначе W1-методология: `desc UA==RU` False→blknochg (genuine, LIVE не переписывать) / True→полный тег-в-tag RU-перевод (blk триплет если Назв.мод RU=nm_ua UA-leak а Назв RU genuine; blknotrip если Назв/Назв.мод бренд+код language-neutral). META keywords всегда faithful (RU genuine). Модель-код Назв UA↔genuine-RU рассинхрон → нумерованный Открытый вопрос (НЕ авто-фикс LIVE, прецедент SKU 10 OQ#1 / W1 chunk-021). **decimal: реальные дроби `N.N`→`N,N` обе локали ТОЛЬКО UA-копии (blk/blknotrip); вес `NN.00` = формат-политика A глобально → verbatim, НЕ диффать/НЕ флипать per-SKU.** Латин.x габариты глоб.B verbatim; кир.х множители no-op. **fixed.xlsx: load СУЩЕСТВУЮЩИЙ chunk-055-fixed.xlsx (НЕ копировать из source — затрёт прошлые батчи), edit by Артикул, save, verify.** + chunk-055-diff.md (entries + batch-summary, Status header N/86) + chunk-055-MANUAL-REVIEW.md (Status, OQ если есть, Last updated) + chunk-glossary-w2.md (новые термины, proposed) + .planning/CURRENT-w2.md. После батча: контент-коммит (diff/MR/glossary, НЕ fixed.xlsx/НЕ CURRENT-w2) → коммит CURRENT-w2 маркер → push origin translation-audit/w2.

## Workflow напоминание
- Источник: `chunk-NN.xlsx` (read-only, копируется из `C:/Projects/labresta-sync/.planning/translation-audit/chunks/` — gitignored). Python: `C:/Projects/labresta-sync/.venv/Scripts/python.exe` (в W2 .venv нет).
- Выход: `chunk-NN-fixed.xlsx` (gitignored) + `chunk-NN-diff.md` + `chunk-NN-MANUAL-REVIEW.md` (в git). Сомнения → `chunk-NN-questions.md`.
- Батч = 8 SKU. Между чанками: scaffold-коммит «chunk-NNN scaffold (W2, продолжение chunk-NNN-1)».
- ЗАПРЕЩЕНО: Status в INDEX.md; коммит/push в main; следы AI в коммитах (автор только Yana, без Co-Authored-By/Generated with Claude); хардкод секретов.

## Decisions / constraints
- W2 .venv отсутствует → используется python main-воркт ри `C:/Projects/labresta-sync/.venv/Scripts/python.exe` (openpyxl 3.1.5 OK).
- chunk-NN.xlsx gitignored (`*.xlsx`), source копируется из main worktree, в W2 read-only.
- chunk-glossary-w2.md — новый файл (у W1 нет отдельного сводного, термины внутри его MANUAL-REVIEW). W1-глоссарий = READ-ONLY референс.
- INDEX.md Status НЕ править (W1 владеет статус-доской).
