# chunk-085 — открытые вопросы (W2) — ANSWERED

**Status:** ANSWERED Yana 2026-05-21 (через AskUserQuestion). Решения сохранены в `.planning/translation-audit/chunks/W2-OQ-ANSWERS.md` (commit `e2bd5ac`).

---

## Открытый вопрос #18 — r21 (ART 1546893484) Hurakan HKN-ISV5P / HKN-ISV7P mismatch

**SKU:** row 21, ART=1546893484, Hurakan шприц колбасный

**Symptom:**
- c4/c6 UA: `Шприц ковбасний Hurakan HKN-ISV5P BLACK` (UA говорит ISV5P, 5 л)
- c5/c7 RU: `Шприц колбасный Hurakan HKN-ISV7P BLACK` (RU canonical говорит ISV7P, 7 л)
- Категория **SKIP-НП** (бренд Hurakan ∈ список НП-эксклюзив): тело из НП-фида позже, W2 не трогает.

**Решение Yana (2026-05-21):**
- **Канон:** `ISV7P` (7 л). UA опечатка `HKN-ISV5P`.
- W2 RU side: c5/c7 RU уже = `HKN-ISV7P` ✓ (никаких правок не требуется).

**Forward к W1 (UA-правки):**
- `chunk-085-fixed.xlsx` r21 col4/col6 → `Шприц ковбасний Hurakan HKN-ISV7P BLACK` (выровнять на канон).

**Forward к НП-фиду merge:**
- Hurakan SKU r21 (ART 1546893484): canonical model code `HKN-ISV7P`. При merge тела из НП-feed использовать ISV7P-вариант, не ISV5P. Cumulative SKIP-НП chunk-085 (для merge): r3 HKN-ISV5P (BLACK 5 л — отдельная SKU), r20 HKN-ISH5P, **r21 HKN-ISV7P (canon — OQ #18 ANSWERED)**, r32 HKN-ISV7P, r69 HKN-EF16 чебуречница.

---
