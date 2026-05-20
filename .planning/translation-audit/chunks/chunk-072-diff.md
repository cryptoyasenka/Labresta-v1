# chunk-072 diff (W2, продолжение chunk-071)

**Status:** chunk-072 scaffold (0/89) — next b1 (SKU 1-8, rows 2-9)
**Last updated:** chunk-072 scaffold

**Источник:** `.planning/translation-audit/chunks/chunk-072.xlsx` (89 SKU, rows 2..90, ART 1173123408..2197264833).
**Фикс-таргет:** `.planning/translation-audit/chunks/chunk-072-fixed.xlsx` (gitignored).
**Бренды:** Hendi 88 (NORMAL) + **FAGOR 1 SKIP-НП** (r83 сушильная машина FAGOR SCP-10).
**Категории товаров:** доски разделочные HACCP GN 1/2 + малая серия, точильные камни/станки, термометры с зондом, контейнеры, сифоны, янагиба-ножи, сушильные машины (НП).

## Workflow
- Batch=8 SKU; 2 commits/batch (C1 content + C2 marker); push после C2.
- TRIP=c5←c7 + c36 RU faithful; blknotrip=c5←c7 only; blknochg=без изменений; blkfix=c36 minor (Ё→Е и т.п.).
- SKIP-НП forward-only: пометить в MR, не трогать xlsx.
- Без Ё в c36; UA `&#39;` AND literal `'` → drop; «тэн»→«э».
- Source typos faithful в c5/title; structural typos preserved.
- chunk-NN.xlsx RO; modify chunk-NN-fixed.xlsx.

## Coverage plan
- b1..b11 = 88 SKU; b12 финал = 1 SKU. Возможна корректировка под классификации.
- SKIP-НП candidate: r83 (FAGOR SCP-10 M E 1P COMPACT CONCEPT сушильная машина).
