# W2 Open Questions — Ответы Yana (2026-05-21)

Сводка решений по всем 9 открытым вопросам W2 (диапазон chunks 055-085).
Yana дала ответы через AskUserQuestion. Применяю правки atomic-коммитами.

## Таблица решений

| # | Chunk | SKU/Row | ART | Решение Yana | Действие W2 | Forward |
|---|---|---|---|---|---|---|
| 1 | 055 | r11 SKU10 | 2123250967 | Чёрный = `843499` (тело «Колір чорний»). r10 SKU9 (ART 2123249689) = белый 843468 — отдельная карточка консистентна. | Уже выровнено в fixed.xlsx ✓ (все имена → 843499). Ничего не делать. | — |
| 2 | 056 | r68 SKU67 | 627378718 | Канон `Appia Life V 1Gr` (опечатка в UA-имени `APPIA II V 1GR`). | RU уже корректно в genuine c5/c7 ✓ | UA col4+col6 `APPIA II V 1GR → Appia Life V 1Gr (1 група)` → W1 |
| 3 | 058 | r32 SKU31 | 2213082715 | Заменить лид-`<p>` RU (copy-paste из GoodFood FJ150) переводом UA-абзаца про Cancan 0103. | Правка col36 RU: первый `<p>` → «Пресс ручной для гранатов Cancan 0103. Предназначен для более лёгкого выжимания крупных гранатов, цитрусов и других фруктов для получения фреш-сока в кафе, буфетах, ресторанах.» Категория blknochg → blkfix. | — |
| 4 | 071 | b5 SKU39 | (find) | Один товар, канон `BCB10` (без NC). | Найти строку в chunk-071, поправить col5/col7 если есть NC. Категория blknochg → blkfix. | UA col4+col6 → W1 |
| 5 | 072 | r43 | 1930950687 | Hendi код `880906 → 470190` (это контейнер для еды). r38 ART 1166434765 оставить как Hendi 880906 контейнер для теста. | Правка col5+col7 RU: `Hendi 880906 → Hendi 470190`. Категория blknochg → blkfix. | UA полный перевод с RU про контейнер для еды → W1 |
| 6 | 074 | r39 | 1166344539 | `837306 = 9 л`, `837405 = 1,5 л` (НЕ 13,5 л как стояло в c7). Тело физически 9 л. | Pending: сверить через https://astim.in.ua/search. Если подтвердится — rollback c5 на «Кастрюля 9 л HENDI 837306» (= дубль r38 → отметка для удаления в Horoshop). | — |
| 7 | 075 | r40 | (GoodFood BCF40-HC) | Канон BCF40-HC (40 кг). Опечатка `BCF20-HC` в `<h2>` тела — поправить. Сверка: https://1gf.com.ua/Buy/shock_freezing/GoodFood_SHafa_shokovo_zamorozki_GF_BCF40_HC/33477.aspx | Правка col36 RU: `BCF20-HC → BCF40-HC` в `<h2>`. | — |
| 8 | 075 | r41 | (Tecnodom P-ATT10EA) | 15 кг (UA) канон. | Правка col36 RU: `12 кг → 15 кг` в характеристике производительности. | — |
| 9 | 085 | r21 | 1546893484 | Канон `ISV7P` (7 л). | RU col5+col7 уже = HKN-ISV7P ✓ (SKIP-НП — тело из НП-feed). | UA col4 `HKN-ISV5P → HKN-ISV7P` → W1. НП-feed merge: HKN-ISV7P |

## Application plan

**Apply order (atomic per chunk):**
1. `chunk-058-fixed.xlsx` r32 col36 — Cancan лид-абзац
2. `chunk-075-fixed.xlsx` r40+r41 col36 — BCF40 + 15 кг
3. `chunk-072-fixed.xlsx` r43 col5+col7 — Hendi 470190
4. `chunk-071-fixed.xlsx` SKU39 — BCB10 без NC (после поиска row#)
5. `chunk-074-fixed.xlsx` r39 — Hendi кастрюля (после webfetch verification)
6. Rebuild `w2-horoshop-import-055-085.xlsx` + `-TEST-1.xlsx`
7. Append `.planning/CURRENT-w2.md` → «W2 OQ ANSWERS APPLIED ✅»
8. Update each `chunk-NN-questions.md` (056, 058, 074, plus create 071/072/075/085) → status ANSWERED Yana 2026-05-21

**Forward к W1 (UA-правки):**
- 056 SKU67 r68: UA `APPIA II V 1GR → Appia Life V 1Gr (1 група)`
- 072 r43: UA полный retranslation с RU (контейнер для еды)
- 085 r21: UA `HKN-ISV5P → HKN-ISV7P`

**Forward к НП-feed merge:**
- 085 r21 Hurakan канон HKN-ISV7P

**Commit author:** `LabResta <labresta@labresta.ua>`
**Branch:** `translation-audit/w2` (НЕ main)
**No AI traces in commits**
