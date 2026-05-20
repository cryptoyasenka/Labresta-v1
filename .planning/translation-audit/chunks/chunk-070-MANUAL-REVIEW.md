# chunk-070 MANUAL REVIEW (W2)

**Status:** chunk-070 scaffold 0/59 (batch=8 b1..b8, b8=3 финал)
**Last updated:** chunk-070 scaffold (W2, продолжение chunk-069)

## Структура

- Источник: `chunk-070.xlsx` (RO, 59 SKU rows 2..60)
- Operating target: `chunk-070-fixed.xlsx` (gitignored, скопирован из source при scaffold)
- Diff: `chunk-070-diff.md`
- Glossary: см. сводный `chunk-glossary-w2.md`
- Questions: `chunk-070-questions.md` (создаётся только при возникновении вопросов)

## Категории SKU (как в chunk-019/067/068/069)

- **TRIP**: c5←c7 + c36 ← faithful RU body (skel preserved + dims preserved + no UA-mark + no Ё)
- **blknotrip**: c5←c7 only, c36 без изменений (когда c36 уже RU OK)
- **blknochg**: c5/c7/c36 без изменений (когда уже всё RU OK / source genuine)
- **SKIP-НП**: forward-only override, brand ∈ {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA} → fixed строка НЕ тронута (тело из фида НП позже)

## Constraints (carry-over из chunk-069)

1. Source typos faithful: c5/c4/c6 — preserved verbatim; c36 body — preserved structural typos, fix только letter-misses в russian переводе.
2. Без Ё в RU c36: «Объем», «Ерш», «щеточки», «ножки», никогда Ё/ё.
3. UA `&#39;` → RU без апостр (drop). Literal `'` тоже drop.
4. «тэн» через «э» (не «тен»/«тэн» через «е»).
5. HTML entities preserved: `&Oslash;`, `&deg;`, `&mdash;`, `&ndash;`, `&times;` — нетронуты.
6. Skeleton preserved: `<p>`/`<ul>`/`<li>`/`<strong>`/`<br>` структура 1:1 с UA.
7. Размерности и числа preserved verbatim: длины, мощности, м3/час, кВт, Вт, мм, см, кг.

## SKIP-НП SKUs (планируется)

- b1: r3 HURAKAN HKN-VAC400E
- b2: r10 APACH AVM420

## Открытые вопросы

(будут добавлены по ходу батчей)
