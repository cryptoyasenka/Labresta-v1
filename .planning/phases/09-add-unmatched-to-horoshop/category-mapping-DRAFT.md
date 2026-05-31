# DRAFT for Yana's review — Option B. Shipped default is still Option A (unchanged). Wiring into the live chain is a follow-up only if Yana approves B.

This is a **measured what-if**, not a behaviour change. The shipped create-card chain
(`feed → analogy → fallback`, AI OFF = **Option A**) is untouched and the full suite is
still green (838 passed / 2 skipped — 835 baseline + 3 new opt-in-flag tests). The mapping
file (`category-mapping-draft.json`) is consulted **only** when you pass `--mapping` to the
audit script; with no flag the audit reproduces the baseline byte-for-byte.

## What Option B does

Of the **76** distinct NP-feed categories, **50 do NOT fuzzy-reconcile** to the store tree
(reconcile cutoff 80) — the feed uses a *different top-level taxonomy* (e.g. feed
`Холодильне обладнання/…` vs store `Холодильне та морозильне обладнання/…`), so the leaves
are close but the parent path diverges and the value never clears the cutoff. Option B is a
hand-built map: each of those 50 feed labels → the **single best real store «Раздел» label**.
A mapped label is rewritten to its store value *before* reconcile, so it exact-matches the
store set and resolves at **confidence 100** in the feed tier.

- **130** distinct store labels loaded from the canonical export `horoshop-export 26.05.26.xlsx` (via `read_category_corpus`).
- **46 / 50** mapped to a real store label · **4 / 50** `null` (genuine gap, no store home) · **10** of the 46 flagged **UNSURE** (need your eye).
- Every store value is **verbatim** from the 130-label set — no invented labels.

## Measured lift (read-only, same 320 unmatched НП, AI OFF)

| Tier | Baseline (Option A, no map) | With mapping (Option B what-if) |
|---|---|---|
| **feed** | 130 (40.6%) | **318 (99.4%)** |
| **analogy** | 175 (54.7%) | 2 (0.6%) |
| **fallback** | 15 (4.7%) | **0** |
| distinct feed cats reconciled | 26 / 76 | **72 / 76** |
| distinct feed cats UNRECONCILED | 50 | 4 (the 4 nulls) |

**Products moved → feed-at-100: +188** (173 from analogy, 15 from fallback). Zero regressions
(all 130 baseline-feed rows stay feed). **241** of 320 rows now resolve at confidence 100.

**The 2 rows that stay on analogy** are exactly the two `null`-mapped sterilizers
(`Стерилізатор ножів Hurakan HKN-UVA12`, `Стерилізатор яєць Hurakan HKN-UVE30`) — they
correctly fall through to a same-brand analog instead of being force-mapped to a wrong store
label. This validates the `null` calls. (The other 2 unreconciled categories —
`Паназійська кухня`, `Фільтри для води` — have no products in this 320-НП slice, which is why
4 categories remain unreconciled but only 2 products stay off the feed tier.)

> Interpretation for the decision: Option B would push the feed tier from **40.6% → 99.4%**
> auto-categorised-at-confidence-100, all but eliminating the analogy/fallback guesswork for
> NP — at the cost of maintaining a 50-row mapping table (and re-checking it when the feed or
> store taxonomy shifts). The 10 UNSURE rows below are where a wrong mapping would silently
> mis-shelve a card, so they are the real review surface.

## The 50 → store mapping

`UNSURE` = my best leaf-judgment but a borderline call (folded-into-a-broader-category,
size/variant ambiguity, or a partial-meaning match). `null` = genuine gap — no store label
fits; the chain falls through to analogy/fallback as today.

| # | Feed label | Store label | Flag |
|---|---|---|---|
| 1 | Допоміжне обладнання/Подрібнювачі відходів | — | **null** |
| 2 | Допоміжне обладнання/Стерилізатори для ножів | — | **null** |
| 3 | Допоміжне обладнання/Стерилізатори для яєць | — | **null** |
| 4 | Обладнання для барів/Блендери професійні | Барне обладнання/Блендери | |
| 5 | Обладнання для барів/Електрокип'ятильники | Фаст-фуд, вулична торгівля/Електрокип'ятильники, чаєроздавачі | |
| 6 | Обладнання для барів/Кавомолки професійні | Барне обладнання/Кавомолки | |
| 7 | Обладнання для барів/Соковижималки | Барне обладнання/Соковитискачі та преси для цитрусових | |
| 8 | Обладнання для м'ясних цехiв/М'ясорубки виробничі | Електромеханічне обладнання/М'ясорубки промислові | |
| 9 | Обладнання для м'ясних цехiв/Фаршемiшалки виробничі | Електромеханічне обладнання/Фаршемішалки | |
| 10 | Обладнання для пекарських цехів/Тісторозкатки пекарські | Електромеханічне обладнання/Тісторозкатувальні машини | |
| 11 | Пакувальне обладнання/Апарати термопакувальні | Пакувальне обладнання, вакууматори/Термопакувальні машини, трейсилери для лотків | |
| 12 | Печі і пароконвектомати/Конвекційні печі | Печі конвекційні та пароконвектомати/Печі конвекційні і пароконвекційні | |
| 13 | Посудомийне обладнання промислове/Фільтри для води | Посудомийне обладнання/Аксесуари та допоміжне обладнання для посудомийних машин | **UNSURE** |
| 14 | Професійне електромеханічне обладнання/Картоплечистки промислові | Електромеханічне обладнання/Картоплечистки і овочечистки | |
| 15 | Професійне електромеханічне обладнання/Кутери професійні | Електромеханічне обладнання/Куттери, бліксери, подрібнювачі, электротерки, сиротерки | |
| 16 | Професійне електромеханічне обладнання/Овочерізки професійні | Електромеханічне обладнання/Овочерізки та машини для переробки овочів | |
| 17 | Професійне електромеханічне обладнання/Пили для м'яса | Електромеханічне обладнання/Пилки стрічкові для м'яса | |
| 18 | Професійне електромеханічне обладнання/Планетарні міксери | Електромеханічне обладнання/Міксери планетарні | |
| 19 | Професійне електромеханічне обладнання/Подрібнювачі спецій | Електромеханічне обладнання/Куттери, бліксери, подрібнювачі, электротерки, сиротерки | **UNSURE** |
| 20 | Професійне електромеханічне обладнання/Преси для піци та гамбургерів | Обладнання для піцерії/Преси для піци | **UNSURE** |
| 21 | Професійне електромеханічне обладнання/Ручні міксери професійні | Електромеханічне обладнання/Міксери занурювальні (ручні) | |
| 22 | Професійне електромеханічне обладнання/Слайсери промислові | Електромеханічне обладнання/Слайсери | |
| 23 | Професійне електромеханічне обладнання/Тістоміси промислові | Електромеханічне обладнання/Тістоміси | |
| 24 | Професійне електромеханічне обладнання/Хліборізки промислові | Електромеханічне обладнання/Хліборізки | |
| 25 | Професійне електромеханічне обладнання/Шприці ковбасні | Електромеханічне обладнання/Шприци ковбасні (наповнювачі фаршу) | |
| 26 | Теплове обладнання/Апарати Sous-Vide | Теплове обладнання/Апарати Sous Vide (термостати) і печі повільного готування | |
| 27 | Теплове обладнання/Апарати для попкорну | Фаст-фуд, вулична торгівля/Апарати для приготування поп-корну | |
| 28 | Теплове обладнання/Апарати для солодкої вати | Фаст-фуд, вулична торгівля/Апарати для приготування цукрової вати | **UNSURE** |
| 29 | Теплове обладнання/Вафельниці професійні | Фаст-фуд, вулична торгівля/Вафельниці | |
| 30 | Теплове обладнання/Газові плити професійні | Плити професійні (варильні поверхні)/Плити газові | |
| 31 | Теплове обладнання/Грилі для шаурми | Фаст-фуд, вулична торгівля/Обладнання для шаурми | |
| 32 | Теплове обладнання/Грилі контактні професійні | Фаст-фуд, вулична торгівля/Грилі контактні (притискні) | |
| 33 | Теплове обладнання/Електричні плити промислові | Плити професійні (варильні поверхні)/Плити електричні | |
| 34 | Теплове обладнання/Млинниці професійні | Фаст-фуд, вулична торгівля/Млинниці | |
| 35 | Теплове обладнання/Паназійська кухня | — | **null** |
| 36 | Теплове обладнання/Печі мікрохвильові професійні | Теплове обладнання/Мікрохвильові печі професійні | |
| 37 | Теплове обладнання/Підігрівачі настільні лампові | Теплове обладнання/Підігрівачі страв | **UNSURE** |
| 38 | Теплове обладнання/Тостери професійні | Фаст-фуд, вулична торгівля/Тостери | |
| 39 | Теплове обладнання/Фритюрниці професійні | Теплове обладнання/Фритюрниці/Фритюрниці підлогові | **UNSURE** |
| 40 | Холодильне обладнання/Апарати для виготовлення морозива | Холодильне та морозильне обладнання/Апарати для морозива (фризера) і гранитори | |
| 41 | Холодильне обладнання/Барні холодильники | Холодильне та морозильне обладнання/Шафи настільні для бару, міні-бари (фрігобари) | |
| 42 | Холодильне обладнання/Вітрини вертикальні холодильні | Вітрини холодильні та морозильні для торгівлі/Гірки-регали пристінні | **UNSURE** |
| 43 | Холодильне обладнання/Вітрини для суші холодильні | Вітрини холодильні та морозильні для торгівлі/Вітрини для суші | |
| 44 | Холодильне обладнання/Вітрини кондитерські холодильні | Вітрини холодильні та морозильні для торгівлі/Кондитерські вітрини та шафи підлогові | |
| 45 | Холодильне обладнання/Вітрини холодильні | Вітрини холодильні та морозильні для торгівлі/Вітрини холодильні середньотемпературні (0°C....+7°C) | **UNSURE** |
| 46 | Холодильне обладнання/Вітрини-надставки холодильні | Вітрини холодильні та морозильні для торгівлі/Вітрини та шафи настільні демонстраційні | **UNSURE** |
| 47 | Холодильне обладнання/Саладети | Холодильне та морозильне обладнання/Саладети, столи холодильні для піци та начинок | |
| 48 | Холодильне обладнання/Холодильні шафи для напоїв | Холодильне та морозильне обладнання/Шафи холодильні | **UNSURE** |
| 49 | Холодильне обладнання/Шафи для вина | Холодильне та морозильне обладнання/Холодильні шафи для вина | |
| 50 | Холодильне обладнання/Шафи шокової заморозки | Холодильне та морозильне обладнання/Апарати шокової заморозки (шокери) | |

### `null` — genuine gaps (4) — no store label exists; stay on analogy/fallback
- **Допоміжне обладнання/Подрібнювачі відходів** — no waste-disposer category in the store tree.
- **Допоміжне обладнання/Стерилізатори для ножів** — no sterilizer category (store has knife *sharpeners*, not sterilizers). NP has 1 product here → stays analogy.
- **Допоміжне обладнання/Стерилізатори для яєць** — no egg-sterilizer category. NP has 1 product here → stays analogy.
- **Теплове обладнання/Паназійська кухня** — "Pan-Asian cuisine" is a marketing bucket, not an equipment leaf; no store equivalent. (No products in this 320-НП slice.)

### `UNSURE` — best-guess, need Yana's eye (10) — a wrong call here mis-shelves the card
- **#13 Фільтри для води** → dishwasher *accessories* category. Water filters are a dishwasher consumable; there is no dedicated water-filter category. Confirm this is where you'd shelve standalone water filters.
- **#19 Подрібнювачі спецій** → folded into the broad `Куттери, бліксери, подрібнювачі…`. No dedicated spice-grinder leaf.
- **#20 Преси для піци та гамбургерів** → `Обладнання для піцерії/Преси для піци`. The pizza half fits; the *hamburger-press* half has no store home — split SKUs may be needed.
- **#28 Апарати для солодкої вати** → `…/цукрової вати` (cotton candy; "солодка вата" = "цукрова вата"). Confident on the meaning, flagged per brief.
- **#37 Підігрівачі настільні лампові** → generic `Підігрівачі страв`. Store has no *lamp-type* warmer leaf; folded into generic warmers.
- **#39 Фритюрниці професійні** → `Фритюрниці підлогові` (chose floor-standing as the "professional" default; store splits настільні/підлогові and the feed gives no size — could be the wrong half).
- **#42 Вітрини вертикальні холодильні** → `Гірки-регали пристінні` (vertical ≈ wall gorki). Could instead be `Вітрини холодильні середньотемпературні`.
- **#45 Вітрини холодильні** → `Вітрини холодильні середньотемпературні (0…+7°C)` (assumed chilled/mid-temp for the generic "холодильні вітрини").
- **#46 Вітрини-надставки холодильні** → `Вітрини та шафи настільні демонстраційні` (counter add-on ≈ table-top demo display).
- **#48 Холодильні шафи для напоїв** → generic `Шафи холодильні` (drinks-specific cabinets folded into generic fridge cabinets).

## Reproduce (read-only; prod-guard intact — aborts on any non-sqlite / rlwy / railway / postgres / psycopg URL)

Baseline (Option A — byte-for-byte unchanged, no mapping):
```
./.venv/Scripts/python.exe scripts/audit_category_analogy.py \
  --export "horoshop-export 26.05.26.xlsx" \
  --np-feed .planning/plans/np-feed/np-feed.xlsx
```

With the Option B draft mapping (what-if):
```
./.venv/Scripts/python.exe scripts/audit_category_analogy.py \
  --export "horoshop-export 26.05.26.xlsx" \
  --np-feed .planning/plans/np-feed/np-feed.xlsx \
  --mapping .planning/phases/09-add-unmatched-to-horoshop/category-mapping-draft.json
```

Full suite (shipped behaviour gate): `./.venv/Scripts/python.exe -m pytest -q` → **838 passed, 2 skipped**.

## If Yana approves B (follow-up only — NOT done here)
Wiring would live in the create-card builder, not the audit script: pass the same
feed→store map into the feed getter (or a thin pre-reconcile step) the builder hands to
`build_resolver(..., feed_category_getter=...)`. No change to `category_resolver.py` is
required — a mapped label already exact-matches the store set and resolves at 100. The 10
UNSURE rows should be confirmed/edited first, and the table re-checked whenever the NP feed
or the store taxonomy changes.
