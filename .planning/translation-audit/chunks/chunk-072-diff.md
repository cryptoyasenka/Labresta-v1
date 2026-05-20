# chunk-072 diff (W2, продолжение chunk-071)

**Status:** chunk-072 b1 DONE 8/89 (cum TRIP 6 / blknotrip 0 / blknochg 2 / blkfix 0 / SKIP-НП 0; 285 PASS / 0 FAIL) — next b2 (SKU 9-16, rows 10-17)
**Last updated:** chunk-072 b1 DONE 8/89

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

## b1 (SKU 1-8, rows 2-9) — 8/89

| # | SKU | row | ART | Brand+Model | Category | Изменения |
|---|-----|-----|-----|-------------|----------|-----------|
| 1 | 1 | 2 | 1173123408 | Hendi 826102 доска HACCP GN 1/2 белая | **TRIP** | c5←c7; c36 RU 1348 chars. Новая GN 1/2 серия 8261xx (dims 265x325x(H)12). **Source-quirk: `<h3>` «- біла Hendi 826102 - біла» double color** preserve → «- белая Hendi 826102 - белая». Reused GN12_TABLE + iframe C8b5szTz-0g (тот же что chunk-071 b10). |
| 2 | 2 | 3 | 1173129125 | Hendi 826126 доска HACCP GN 1/2 голубая (синяя) | **TRIP** | c5←c7; c36 RU 1340 chars. Normal `<h3>` (single color). Usage table «синий → рыба». |
| 3 | 3 | 4 | 1173132435 | Hendi 826157 доска HACCP GN 1/2 желтая | **TRIP** | c5←c7; c36 RU 1341 chars. Usage table «желтый → сырая птица». |
| 4 | 4 | 5 | 1173141822 | Hendi 826133 доска HACCP GN 1/2 зеленая | **TRIP** | c5←c7 «зелёная» **(Ё в c5 от source c7 — allowed)**; c36 RU 1342 chars «зеленая» без Ё. Usage table «зеленый → овощи». |
| 5 | 5 | 6 | 1173143617 | Hendi 826140 доска HACCP GN 1/2 коричневая | **TRIP** | c5←c7; c36 RU 1344 chars. **Source-quirk: `<h3>` «- коричневаяизготовлена» glued (RU+RU without space, plus UA «з поліетилену»)** preserve glue → «- коричневаяизготовлена из полиэтилена HDPE 500.» |
| 6 | 6 | 7 | 1173145385 | Hendi 826119 доска HACCP GN 1/2 красная | **TRIP** | c5←c7; c36 RU 1342 chars. Normal `<h3>` (no glue typo). |
| 7 | 7 | 8 | 2045395280 | GoodFood DH1 воронка-дозатор для соусов и кремов | **blknochg** | c5 уже RU == c7. c36 уже pure RU. UA только в c35 — forward-only, не трогаем. |
| 8 | 8 | 9 | 2046058563 | GoodFood CDM10 аппарат для декорирования тортов | **blknochg** | c5 уже RU == c7. c36 уже pure RU. UA только в c35 — forward-only, не трогаем. |

**Итого b1:** TRIP 6 + blknotrip 0 + blknochg 2 + blkfix 0 + SKIP-НП 0. Verify **285 PASS / 0 FAIL**.
**Cum после b1:** TRIP 6 + blknotrip 0 + blknochg 2 + blkfix 0 + SKIP-НП 0 = **8/89**. UNPROC = 81 (rows 10-90).
