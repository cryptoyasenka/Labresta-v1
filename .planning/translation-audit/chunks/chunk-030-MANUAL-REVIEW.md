# chunk-030 — ручная проверка для Yana (русский)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-030 (96 SKU)
**Apply key:** `Артикул` (scoped per row)
**Status:** IN PROGRESS 24/96

Здесь собираю всё, что требует твоего подтверждения (не авто-фиксы). Авто-фиксы по locked-паттернам перечислены в сводках по батчам, отдельного подтверждения не требуют. Открытые вопросы накапливаются в нумерованный список и финализируются при закрытии chunk-030. SKIP-НП SKU (НП-эксклюзивные бренды) помечаются здесь и не переписываются.

---

## Открытые вопросы chunk-030

1. **SKU 1 (Артикул 526929616, ITPIZZA ML6, b1)** — UA `Напруга: 380 Ст.` (Cyr `Ст.` U+0421+U+0442) — клавиатурный typo вместо канонической формы `Напруга: 380 В.` (cf. SKU 2 same brand ITPIZZA `Напруга: 380 В.` — single-source precedent). Out-of-precedent Rule A scope (только `Nдив`→`Nсм` точно по precedent chunk-029 b9 SKU 72). RU mirror verbatim `Напряжение: 380 Ст.`. **Решение Yana:** fix UA `380 Ст.`→`380 В.` (и RU mirror)? или preserve verbatim как supplier-side artifact?

2. **SKU 5 (Артикул 616390848, FROSTY F630, b1)** — UA `<li>завантаження: 6 піц O30 см</li>` — Latin `O` U+004F вместо `Ø` U+00D8 (символ диаметра). SKU 6/7 same brand FROSTY используют `Ø34 см` корректно — likely typo в SKU 5 только. Out-of-precedent Rule A. RU mirror verbatim `O30 см`. **Решение Yana:** fix UA `O30`→`Ø30` (и RU mirror)? или preserve verbatim?

3. **SKU 6 (Артикул 616390851, FROSTY M 9, b1)** — UA `<li>со стеклом и подсветкой</li>` (между `Ø34 см` и `2 термостата`) — Russian-leak в UA-cell (фраза 100% русская в украинском body). Supplier-side artefact (supplier выдал mixed UA+RU phrase, magazine скопировал as-is). Out-of-precedent Rule A. RU mirror verbatim. **Решение Yana:** translate UA → `зі склом і підсвічуванням` (canonical UA, cf. SKU 5 same brand UA `зі склом і підсвічуванням` правильная UA-форма)? или preserve verbatim как supplier-side artifact?

4. **SKU 7 (Артикул 616390852, FROSTY M 12, b1)** — UA `<li>со стеклом и подсветкой</li>` — Russian-leak в UA-cell, **mirror SKU 6** same brand same artefact. Out-of-precedent. RU mirror verbatim. **Решение Yana:** fix вместе с SKU 6 одним правилом (если решение SKU 6 = fix)? или preserve verbatim?

5. **SKU 20 (Артикул 665924706, GoodFood PO11, b3)** — UA `<p>Внимание! Перед введенням печі в експлуатацію її необхідно прогріти впродовж щонайменше 8 годин за 450 °C. </p>` — Russian-leak `Внимание!` (русское слово в украинском body; supplier продолжил по-украински). Out-of-precedent. **Решение Yana:** translate UA `Внимание!`→`Увага!` (canonical UA)? или preserve verbatim?

6. **SKU 20 (Артикул 665924706, GoodFood PO11, b3)** — RU `<li>Cмотровое окно.</li>` — Latin `C` U+0043 вместо Cyr `С` U+0421 в начале слова. Visual-ambiguity supplier typo. blknochg preserve в LIVE Horoshop body. **Решение Yana:** fix RU `Cмотровое`→`Смотровое` (Cyr С)? или preserve как LIVE artifact?

7. **SKU 21 (Артикул 878056222, GoodFood PO22, b3)** — UA `<li>Внимание! Перед введенням печі…</li>` Russian-leak `Внимание!` — **mirror SKU 20** same brand same artefact. **Решение Yana:** fix вместе с SKU 20?

8. **SKU 21 (Артикул 878056222, GoodFood PO22, b3)** — RU `<li>Cмотровое окно.</li>` Latin C — **mirror SKU 20** same brand same artefact. **Решение Yana:** fix вместе с SKU 20?

9. **SKU 23 (Артикул 945098467, FROSTY M12L, b3)** — UA `<li>со стеклом и подсветкой</li>` Russian-leak — **mirror SKU 6/7** (chunk-030 b1) same brand same artefact. **Решение Yana:** translate UA → `зі склом і підсвічуванням` (canonical UA)?

10. **SKU 24 (Артикул 945104692, FROSTY M18, b3)** — UA `<li>со стеклом и подсветкой</li>` Russian-leak — **mirror SKU 23** same brand same artefact. **Решение Yana:** fix вместе с SKU 23?

11. **SKU 24 (Артикул 945104692, FROSTY M18, b3)** — UA `<li>камера 105х105х15 мм</li>` — supplier dims typo (камера в 100 раз меньше реальной; M12L SKU 23 same brand `1050х700х150`; M18 на 18 пицц должна быть крупнее). Out-of-precedent Rule A. **Решение Yana:** fix UA → `1050х1050х150 мм`? или preserve?

---

**Last updated:** 2026-05-21 — chunk-030 scaffold (96 SKU; продолжение chunk-029; первый SKU Артикул `526929616` ITPIZZA `Піч для піци ITPIZZA ML6` — раздел `Обладнання для піцерії/Печі для піци` (pizza-equipment блок продолжается с chunk-029 SKU 39-79); 3 подраздела `Обладнання для піцерії` interleaved: Печі для піци 40 SKU + Аксесуари для піцерії 54 SKU + Преси для піци 2 SKU; 12 брендов: GI.Metal ×30 + Hendi ×24 + FROSTY ×13 + ITPIZZA ×6 + Moretti Forni ×6 + GGF ×5 + GoodFood ×4 + Hurakan ×2 + EWT INOX ×2 + Apach ×2 + Cuppone ×1 + REEDNEE ×1; последний SKU 96 Артикул `2385515101` Moretti Forni `Піч для піци Moretti Forni PM72.72`; SKIP-НП candidates 4 SKU: Hurakan ×2 SKU 27/84, Apach ×2 SKU 51/54). NEW DURABLE RULES (Yana 2026-05-21, в силе с chunk-030): Rule A UA forward-fix typos + Rule B global glyph-normalize forward `&deg;`→`°` + Cyr `С`→Lat `C` формат `50 °C`. chunk-029 ЗАКРЫТ 79/79 (`df949d7`). NEXT: батч SKU 1-8.
