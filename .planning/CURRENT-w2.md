# CURRENT-w2 — LabResta translation audit (W2 параллельный воркер)

**Last touched:** 2026-05-18
**Status:** chunk-055 scaffold готов, next батч SKU 1-8

## Диапазон W2
- ТОЛЬКО chunk-055 … chunk-085. НИКОГДА не трогать chunk-≤054 (W1) и не редактировать main.
- Ветка: `translation-audit/w2`. Push в `origin translation-audit/w2` (НЕ main).
- State-файл W2: этот файл. НЕ трогать `.planning/CURRENT.md` (W1).

## Status
- [x] CURRENT-w2.md создан (первый заход W2)
- [x] chunk-055 scaffold: `chunk-055-diff.md` + `chunk-055-MANUAL-REVIEW.md` + `chunk-glossary-w2.md`
- [x] chunk-055.xlsx source скопирован в W2 (gitignored, read-only)
- [ ] chunk-055 батч SKU 1-8 (next)
- [ ] chunk-055 батчи 9-86 (батч = 8 SKU)
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
chunk-055 батч SKU 1-8 (Артикул `2204681685` Sirman … вперёд). Прочитать memory `feedback_labresta_ua_ru_translation_rules`, эталон формата chunk-019-MANUAL-REVIEW.md + chunk-019-diff.md. Для каждого SKU: SKIP-НП-чек бренда → если в списке (Hurakan и др.) пометить SKIP-НП и дальше; иначе аудит UA+RU по правилам, запись в chunk-055-fixed.xlsx + chunk-055-diff.md + chunk-055-MANUAL-REVIEW.md. После батча: контент-коммит + CURRENT-w2 маркер + push origin translation-audit/w2.

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
