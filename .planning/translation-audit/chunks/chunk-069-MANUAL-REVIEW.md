# chunk-069 MANUAL REVIEW (W2)

**Status:** chunk-069 scaffold 0/61 (batch=8 b1..b8) — продолжение chunk-068 ЗАКРЫТ 50/50
**Last updated:** chunk-069 scaffold

## Структура

- Источник: `chunk-069.xlsx` (RO)
- Operating target: `chunk-069-fixed.xlsx` (gitignored, скопирован из source при scaffold)
- Diff: `chunk-069-diff.md`
- Glossary: см. сводный `chunk-glossary-w2.md`
- Questions: `chunk-069-questions.md` (создаётся только при возникновении вопросов)

## Категории SKU (как в chunk-019/067/068)

- **TRIP**: c5←c7 + c36 ← faithful RU body (skel preserved + dims preserved + no UA-mark + no Ё)
- **blknotrip**: c5←c7 only, c36 без изменений (когда c36 уже RU OK)
- **blknochg**: c5/c7/c36 без изменений (когда уже всё RU OK / source genuine)
- **SKIP-НП**: forward-only override, brand ∈ {HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA} → fixed строка НЕ тронута

## Constraints (carry-over из chunk-068)

1. Source typos faithful: c5/c4/c6 — preserved verbatim; c36 body — preserved structural typos, fix только letter-misses в russian переводе.
2. Без Ё в RU c36: «Объем», «Ерш», «щеточки», «ножки», никогда Ё/ё.
3. UA `&#39;` → RU без апостр (drop).
4. «тэн» через «э».
5. «мытья» vs «мойки»: c5 ← c7 verbatim per row, не унифицировать между строками.
6. `<h2>` open+close adds 2× «2» dim tokens; preserve в skel.
7. Asber/ASBER: c5 source variants («Посудомийка купольна») перезаписываются по c7 standard «Посудомоечная машина ASBER ...» (live-store uniform).
8. Об'єм (RD) vs Ємність (DD): preserve ASBER source variant per row.
9. ATA/OZTI/Ozti/ADLER/Gooder/GGM/GGG/Hendi/Krupps brands НЕ в списке НП-эксклюзивных, обрабатываются обычно.
10. chunk-NN.xlsx source RO; modify chunk-NN-fixed.xlsx (gitignored *.XLSX).
11. W2 range: chunk-055..chunk-085 ONLY.
12. Use .planning/CURRENT-w2.md (NOT CURRENT.md = W1).
13. Batch = 8 SKU; 2 commits per batch (C1 content + C2 marker); push after C2.

## Батчи

chunk-069 = **61 SKU**, batches 8+8+8+8+8+8+8+5 (b1..b8):
- b1: SKU 1-8, rows 2-9
- b2: SKU 9-16, rows 10-17
- b3: SKU 17-24, rows 18-25
- b4: SKU 25-32, rows 26-33
- b5: SKU 33-40, rows 34-41
- b6: SKU 41-48, rows 42-49
- b7: SKU 49-56, rows 50-57
- b8: SKU 57-61, rows 58-62 (финал, 5 SKU)

## Следующий шаг

**chunk-069 b1** (SKU 1-8, rows 2-9): probe → cp → apply → md → C1+C2 → push.
