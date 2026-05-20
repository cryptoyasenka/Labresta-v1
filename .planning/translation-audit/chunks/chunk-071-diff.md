# chunk-071 diff (W2, продолжение chunk-070)

**Status:** chunk-071 scaffold — 0/83 (TRIP 0 / blknotrip 0 / blknochg 0 / blkfix 0 / SKIP-НП 0)
**Last updated:** chunk-071 scaffold

**Источник:** `.planning/translation-audit/chunks/chunk-071.xlsx` (83 SKU, rows 2..84, ART 500478925..1173086863).
**Фикс-таргет:** `.planning/translation-audit/chunks/chunk-071-fixed.xlsx` (gitignored).
**Бренды:** все 83 — **Hendi** (NORMAL, не SKIP-НП). 0 SKIP-НП.
**Категории товаров:** балончики для сифонов, газовые горелки крем-брюле, доски разделочные HACCP, тёрки, мандолины, воронки-дозаторы, термометры с зондом, точила.

## Workflow
- Batch=8 SKU; 2 commits/batch (C1 content + C2 marker); push после C2.
- TRIP=c5←c7 + c36 RU faithful; blknotrip=c5←c7 only; blknochg=без изменений; blkfix=c36 minor (Ё→Е и т.п.).
- Без Ё в c36; UA `&#39;` AND literal `'` → drop; «тэн»→«э».
- Source typos faithful в c5/title; structural typos preserved.
- chunk-NN.xlsx RO; modify chunk-NN-fixed.xlsx.
