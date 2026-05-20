# chunk-072 MANUAL REVIEW (W2, продолжение chunk-071)

**Status:** chunk-072 b1 DONE 8/89 (cum TRIP 6 / blknotrip 0 / blknochg 2 / blkfix 0 / SKIP-НП 0; 285 PASS / 0 FAIL) — next b2 (SKU 9-16, rows 10-17)
**Last updated:** chunk-072 b1 DONE 8/89

**Объём:** 89 SKU rows 2..90. Hendi 88 (NORMAL) + FAGOR 1 SKIP-НП (r83).

**Категории:**
- Доски разделочные HACCP GN 1/2 (продолжение chunk-071, серия 8261xx меньшая GN 1/2 + ещё серии)
- Точильные камни/станки (массово в начале/середине)
- Термометры с зондом
- Контейнеры, сифоны для крема/мусса
- Янагиба-ножи (японские)
- Прочее кондитерское (формы, насадки)
- НП: r83 сушильная машина FAGOR SCP-10

**SKIP-НП candidates:**
- r83 (FAGOR SCP-10 M E 1P COMPACT CONCEPT сушильная машина) — пометить, не трогать xlsx

**Cumulative state:** TRIP 0 + blknotrip 0 + blknochg 0 + blkfix 0 + SKIP-НП 0 = 0/89.

## b1 (SKU 1-8, rows 2-9) — 8/89

**Категории:** TRIP 6 (HACCP GN 1/2 boards 8261xx series) + blknochg 2 (GoodFood DH1 воронка + GoodFood CDM10 аппарат декорирования).

**TRIP detail (6 досок GN 1/2):**
- **r2 Hendi 826102 белая** — **Source-quirk: `<h3>` double color «- біла Hendi 826102 - біла»** preserve faithful → «- белая Hendi 826102 - белая».
- **r3 Hendi 826126 голубая (синяя)** — Normal single-color `<h3>`. Usage rows: синий → рыба.
- **r4 Hendi 826157 желтая** — Usage желтый → сырая птица.
- **r5 Hendi 826133 зеленая** — c7 уже имеет Ё «зелёная» → c5 takes Ё (Ё в c5 allowed); c36 uses «зеленая» без Ё.
- **r6 Hendi 826140 коричневая** — **Source-quirk: glued «коричневаяизготовлена»** (RU слова без пробела, plus UA prep «з поліетилену») preserve glue → «- коричневаяизготовлена из полиэтилена HDPE 500.» Не разделять.
- **r7 Hendi 826119 красная** — Normal (no glue typo).

**Новый GN 1/2 template (отличия от chunk-071 b10 GN 1/1):**
- Dims: 265x325x(H)12 мм (vs 530x325x(H)15 GN 1/1)
- `<h3>` структура: «Доска разделочная HACCP GN 1/2 Hendi <SKU> - <color> изготовлена из полиэтилена HDPE 500.» (с описанием материала встроенным в заголовок)
- Body: 5 bullet items (Соответствуют HACCP / Двусторонние / Одна с желобком другая гладкая / Закругленные кромки / Размер) — короче чем b10 (6 items)
- Body line: «Гладкая с одной стороны и с вырезом, предотвращающим вытекание сока с другой стороны» (та же что b10)
- Reused iframe C8b5szTz-0g (тот же что chunk-071 b10 — НЕ новый!)
- Новая GN12_TABLE: 826102/826119/826126/826133/826140/826157/826164 с dims 265x325x(H)12

**blknochg detail:**
- **r8 GoodFood DH1** — воронка-дозатор для соусов и кремов: c5 уже RU (==c7), c36 уже pure RU (UA только в c35). Forward-only.
- **r9 GoodFood CDM10** — аппарат для декорирования тортов: c5 уже RU (==c7), c36 уже pure RU (UA только в c35). Forward-only.

**Терминология b1 (новые UA→RU):**
- «GN 1/2» → «GN 1/2» (keep)
- «Відповідають нормам HACCP» → «Соответствуют нормам HACCP»
- «Двосторонні» → «Двусторонние»
- «Одна сторона з жолобком, інша гладка» → «Одна сторона с желобком, другая гладкая»
- «Розмір» → «Размер»

**Открытые вопросы b1:** 0 новых.
**Source-quirks preserved в b1:**
- r2: `<h3>` double color «- біла Hendi 826102 - біла» preserve
- r5: c7 has Ё «зелёная» → c5 takes Ё (allowed); c36 без Ё
- r6: glued «коричневаяизготовлена» preserve (RU+RU без пробела)
- r8/r9: blknochg — c5 RU == c7, c36 pure RU; UA только в c35 forward-only

**Verify:** 285 PASS / 0 FAIL.
