# chunk-074 Open Questions (W2) — ANSWERED

## OQ #3 — chunk-074 b5 r39: HENDI кастрюля mismatch — ANSWERED Yana 2026-05-21

**SKU:** row 39, ART=1166344539

**Symptoms (before fix):**
- c4 NMUA / c5 NMRU: «Каструля 9 л HENDI 837306» (identical to r38 c5)
- c7 NZRU: «Кастрюля 13,5 л HENDI 837405» (canonical RU — different volume + different art)
- c36 DSCRU: body describes **9 л 837306** with dimensions ø240x200 мм, толщина 0,6 мм (identical to r38 body)

**Source-bug analysis:** Looks like copy-paste leftover from r38 build process — c5/c36 не были обновлены, только c7 переписан под правильный продукт. Тело физически 9л версию (габариты ø240x200) а не 13,5 л.

**Action taken (b5 apply, до OQ):**
- c5 ← c7 = «Кастрюля 13,5 л HENDI 837405» (TRIP standard, c7 canonical RU).
- c36 → hendi_pot_capsule_body(9, '837306', '240x200 мм', '0,6') — переведено UA→RU literally, описание ссылается на 9 л 837306 (preserve source-bug).
- **Результат (до Yana ответа):** label «13,5 л 837405» vs body «9 л 837306 ø240x200» — несоответствие в live store.

**Решение Yana (2026-05-21):**
- `837306` = **9 л** (НЕ 13,5 л как стояло в c7 source — c7 source value был ошибочный).
- `837405` = **1,5 л** (НЕ 13,5 л).
- Тело физически 9 л → Option B verbatim: rollback c5/c7 RU = «Кастрюля 9 л HENDI 837306» (= дубль r38 в каталоге).
- Sanity-check link от Yana: https://astim.in.ua/search (для HENDI кодов 837306 / 837405).

**Applied (W2 RU side):**
- `chunk-074-fixed.xlsx` r39 col5 → `Кастрюля 9 л HENDI 837306` (rollback c5 на источник UA-волюм).
- `chunk-074-fixed.xlsx` r39 col7 → `Кастрюля 9 л HENDI 837306` (правка ошибочного c7 source canonical).
- c36 body остаётся as-is (физически описывает 9 л).
- **Caveat для Horoshop:** r39 (ART 1166344539) теперь идентичен r38 (ART 1166341286) по продукту — две Horoshop-карточки на одну SKU. Yana отметила для удаления дубликата в Horoshop.

---

## Cumulative open questions (across chunks, see chunk-NN-questions.md per chunk)
- #1 (c071 → реально c021 W1) SKU39 BCB10 vs BCB10 NC — ANSWERED Yana «один товар BCB10»; **out of W2 scope** (chunk-021 = W1)
- #2 (c072 b6) r43 Hendi 880906 catalog mismatch — ANSWERED Yana 880906=тесто r38 / 470190=еда r43 (см. chunk-072-questions.md)
- #3 (c074 b5) r39 ART=1166344539 9 л 837306 vs 13,5 л 837405 — ANSWERED above
