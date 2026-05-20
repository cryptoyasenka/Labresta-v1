# chunk-074 Open Questions (W2)

## OQ #3 — chunk-074 b5 r39: HENDI кастрюля mismatch

**SKU:** row 39, ART=1166344539

**Symptoms:**
- c4 NMUA / c5 NMRU: «Каструля 9 л HENDI 837306» (identical to r38 c5)
- c7 NZRU: «Кастрюля 13,5 л HENDI 837405» (canonical RU — different volume + different art)
- c36 DSCRU: body describes **9 л 837306** with dimensions ø240x200 мм, толщина 0,6 мм (identical to r38 body)

**Source-bug analysis:** Looks like copy-paste leftover from r38 build process — c5/c36 не были обновлены, только c7 переписан под правильный продукт. Тело физически описывает 9л версию (габариты ø240x200) а не 13,5 л.

**Action taken (b5 apply):**
- c5 ← c7 = «Кастрюля 13,5 л HENDI 837405» (TRIP standard, c7 canonical RU).
- c36 → hendi_pot_capsule_body(9, '837306', '240x200 мм', '0,6') — переведено UA→RU literally, описание ссылается на 9 л 837306 (preserve source-bug).
- **Результат:** label «13,5 л 837405» vs body «9 л 837306 ø240x200» — несоответствие в live store.

**Need decision from Yana:**
1. **Option A** (c7 правильный, body wrong): rewrite c36 body referencing 13,5 л 837405 + новые габариты/толщина (нужны данные из HENDI каталога).
2. **Option B** (c7 ошибочный, body правильный): rollback c5 = «Кастрюля 9 л HENDI 837306» (= r38 c5), сохранить body. Дубль r38 в каталоге.
3. **Option C**: third product entirely — нужны корректные данные.

**Pending until:** Yana provides decision.

---

## Cumulative open questions (across chunks, see chunk-NN-questions.md per chunk)
- #1 (c071 b5) SKU39 BCB10 vs BCB10 NC
- #2 (c072 b6) r43 Hendi 880906 catalog mismatch
- #3 (c074 b5) r39 ART=1166344539 9 л 837306 vs 13,5 л 837405 — see above
