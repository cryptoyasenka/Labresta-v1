# chunk-030 — ручная проверка для Yana (русский)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-030 (96 SKU)
**Apply key:** `Артикул` (scoped per row)
**Status:** IN PROGRESS 16/96

Здесь собираю всё, что требует твоего подтверждения (не авто-фиксы). Авто-фиксы по locked-паттернам перечислены в сводках по батчам, отдельного подтверждения не требуют. Открытые вопросы накапливаются в нумерованный список и финализируются при закрытии chunk-030. SKIP-НП SKU (НП-эксклюзивные бренды) помечаются здесь и не переписываются.

---

## Открытые вопросы chunk-030

1. **SKU 1 (Артикул 526929616, ITPIZZA ML6, b1)** — UA `Напруга: 380 Ст.` (Cyr `Ст.` U+0421+U+0442) — клавиатурный typo вместо канонической формы `Напруга: 380 В.` (cf. SKU 2 same brand ITPIZZA `Напруга: 380 В.` — single-source precedent). Out-of-precedent Rule A scope (только `Nдив`→`Nсм` точно по precedent chunk-029 b9 SKU 72). RU mirror verbatim `Напряжение: 380 Ст.`. **Решение Yana:** fix UA `380 Ст.`→`380 В.` (и RU mirror)? или preserve verbatim как supplier-side artifact?

2. **SKU 5 (Артикул 616390848, FROSTY F630, b1)** — UA `<li>завантаження: 6 піц O30 см</li>` — Latin `O` U+004F вместо `Ø` U+00D8 (символ диаметра). SKU 6/7 same brand FROSTY используют `Ø34 см` корректно — likely typo в SKU 5 только. Out-of-precedent Rule A. RU mirror verbatim `O30 см`. **Решение Yana:** fix UA `O30`→`Ø30` (и RU mirror)? или preserve verbatim?

3. **SKU 6 (Артикул 616390851, FROSTY M 9, b1)** — UA `<li>со стеклом и подсветкой</li>` (между `Ø34 см` и `2 термостата`) — Russian-leak в UA-cell (фраза 100% русская в украинском body). Supplier-side artefact (supplier выдал mixed UA+RU phrase, magazine скопировал as-is). Out-of-precedent Rule A. RU mirror verbatim. **Решение Yana:** translate UA → `зі склом і підсвічуванням` (canonical UA, cf. SKU 5 same brand UA `зі склом і підсвічуванням` правильная UA-форма)? или preserve verbatim как supplier-side artifact?

4. **SKU 7 (Артикул 616390852, FROSTY M 12, b1)** — UA `<li>со стеклом и подсветкой</li>` — Russian-leak в UA-cell, **mirror SKU 6** same brand same artefact. Out-of-precedent. RU mirror verbatim. **Решение Yana:** fix вместе с SKU 6 одним правилом (если решение SKU 6 = fix)? или preserve verbatim?

---

**Last updated:** 2026-05-21 — chunk-030 scaffold (96 SKU; продолжение chunk-029; первый SKU Артикул `526929616` ITPIZZA `Піч для піци ITPIZZA ML6` — раздел `Обладнання для піцерії/Печі для піци` (pizza-equipment блок продолжается с chunk-029 SKU 39-79); 3 подраздела `Обладнання для піцерії` interleaved: Печі для піци 40 SKU + Аксесуари для піцерії 54 SKU + Преси для піци 2 SKU; 12 брендов: GI.Metal ×30 + Hendi ×24 + FROSTY ×13 + ITPIZZA ×6 + Moretti Forni ×6 + GGF ×5 + GoodFood ×4 + Hurakan ×2 + EWT INOX ×2 + Apach ×2 + Cuppone ×1 + REEDNEE ×1; последний SKU 96 Артикул `2385515101` Moretti Forni `Піч для піци Moretti Forni PM72.72`; SKIP-НП candidates 4 SKU: Hurakan ×2 SKU 27/84, Apach ×2 SKU 51/54). NEW DURABLE RULES (Yana 2026-05-21, в силе с chunk-030): Rule A UA forward-fix typos + Rule B global glyph-normalize forward `&deg;`→`°` + Cyr `С`→Lat `C` формат `50 °C`. chunk-029 ЗАКРЫТ 79/79 (`df949d7`). NEXT: батч SKU 1-8.
