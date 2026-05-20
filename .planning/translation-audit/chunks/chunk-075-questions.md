# chunk-075 — открытые вопросы (W2) — ANSWERED

**Status:** ANSWERED Yana 2026-05-21 (через AskUserQuestion). Решения сохранены в `.planning/translation-audit/chunks/W2-OQ-ANSWERS.md` (commit `e2bd5ac`).

---

## Открытый вопрос #1 — r40 (GoodFood BCF40-HC) — опечатка в лид-абзаце genuine RU `<p>`

**SKU:** row 40, ART=2276609641, `Шкаф шоковой заморозки GoodFood GF-BCF40-HC`

**Symptom:**
- c5/c7 NMRU + NAZVRU: `GoodFood GF-BCF40-HC` (канон, 40 кг)
- c36 DSCRU лид-`<p>`: `<p>Шкаф шоковой заморозки GoodFood GF-BCF20-HC предназначен для быстрого охлаждения…` — опечатка `BCF20-HC` (это модель 20 кг, другая карточка)
- Yana sanity-check: https://1gf.com.ua/Buy/shock_freezing/GoodFood_SHafa_shokovo_zamorozki_GF_BCF40_HC/33477.aspx — GoodFood BCF40-HC канон

**Решение Yana (2026-05-21):** канон BCF40-HC (40 кг). Опечатку в лид-`<p>` поправить.

**Applied:** `chunk-075-fixed.xlsx` r40 col36 → replace `BCF20-HC` → `BCF40-HC` (одно вхождение).

---

## Открытый вопрос #2 — r41 (Tecnodom P-ATT10EA) — рассинхрон производительности UA↔RU

**SKU:** row 41, ART=2598216958, `Шокер Tecnodom P-ATT10EA`

**Symptom:**
- c35 UA: `охолодження 20 кг … заморожування 15 кг`
- c36 RU: `охлаждение 20 кг … заморозка 12 кг` — рассинхрон по заморозке (UA=15, RU=12)

**Решение Yana (2026-05-21):** канон `15 кг` (UA). RU поправить.

**Applied:** `chunk-075-fixed.xlsx` r41 col36 → replace `заморозка 12 кг` → `заморозка 15 кг`. `охлаждение 20 кг` оставлено как есть (выровнено с UA).

---
