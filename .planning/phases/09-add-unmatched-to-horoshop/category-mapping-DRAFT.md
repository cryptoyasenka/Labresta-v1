# DRAFT for Yana's review — Option B. Shipped default is still Option A (unchanged).

> **Option B is now reachable OPT-IN via the live UI (no code change to activate):** on
> `/feeds/add`, upload `category-mapping-draft.json` in the optional field «Мапінг категорій
> (.json)». **No upload = Option A default** (byte-for-byte unchanged). The same map is also
> consumable by the audit's `--mapping` flag. The wiring (resolver/`build_resolver`/
> `build_add_file`/view) shipped 2026-05-31 mirroring the optional `np_feed` upload; the
> shipped default is proven unchanged by the green suite.

This is still a **measured what-if** decision for Yana, not a forced behaviour change. The
shipped create-card chain (`feed → analogy → fallback`, AI OFF = **Option A**) is the default
and the full suite is green (**843 passed / 2 skipped** — 838 baseline + 5 new opt-in tests:
2 audit-flag + 3 resolver/factory + 2 view, see note). The mapping is consulted **only** when
the JSON is supplied (UI upload or `--mapping`); with nothing supplied both the live builder
and the audit reproduce the baseline byte-for-byte.

## What Option B does

Of the **76** distinct NP-feed categories, **50 do NOT fuzzy-reconcile** to the store tree
(reconcile cutoff 80) — the feed uses a *different top-level taxonomy* (e.g. feed
`Холодильне обладнання/…` vs store `Холодильне та морозильне обладнання/…`), so the leaves
are close but the parent path diverges and the value never clears the cutoff. Option B is a
hand-built map: each of those 50 feed labels → the **single best real store «Раздел» label**.
A mapped label is rewritten to its store value *before* reconcile, so it exact-matches the
store set and resolves at **confidence 100** in the feed tier.

- **130** distinct store labels loaded from the canonical export `horoshop-export 26.05.26.xlsx` (via `read_category_corpus`).
- **46 / 50** mapped to a real store label · **4 / 50** `null` (genuine gap, no store home) · **10** of the 46 originally flagged **UNSURE**.
- **UNSURE triaged 2026-05-31 against real audit data → 4 promoted CONFIDENT, 3 deferred (0 products this import), 3 still UNSURE** (see the UNSURE section). No JSON value changed.
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
| 19 | Професійне електромеханічне обладнання/Подрібнювачі спецій | Електромеханічне обладнання/Куттери, бліксери, подрібнювачі, электротерки, сиротерки | UNSURE — 0 products this import (defer) |
| 20 | Професійне електромеханічне обладнання/Преси для піци та гамбургерів | Обладнання для піцерії/Преси для піци | ✅ confirmed (analogy agrees) |
| 21 | Професійне електромеханічне обладнання/Ручні міксери професійні | Електромеханічне обладнання/Міксери занурювальні (ручні) | |
| 22 | Професійне електромеханічне обладнання/Слайсери промислові | Електромеханічне обладнання/Слайсери | |
| 23 | Професійне електромеханічне обладнання/Тістоміси промислові | Електромеханічне обладнання/Тістоміси | |
| 24 | Професійне електромеханічне обладнання/Хліборізки промислові | Електромеханічне обладнання/Хліборізки | |
| 25 | Професійне електромеханічне обладнання/Шприці ковбасні | Електромеханічне обладнання/Шприци ковбасні (наповнювачі фаршу) | |
| 26 | Теплове обладнання/Апарати Sous-Vide | Теплове обладнання/Апарати Sous Vide (термостати) і печі повільного готування | |
| 27 | Теплове обладнання/Апарати для попкорну | Фаст-фуд, вулична торгівля/Апарати для приготування поп-корну | |
| 28 | Теплове обладнання/Апарати для солодкої вати | Фаст-фуд, вулична торгівля/Апарати для приготування цукрової вати | UNSURE — 0 products this import (defer) |
| 29 | Теплове обладнання/Вафельниці професійні | Фаст-фуд, вулична торгівля/Вафельниці | |
| 30 | Теплове обладнання/Газові плити професійні | Плити професійні (варильні поверхні)/Плити газові | |
| 31 | Теплове обладнання/Грилі для шаурми | Фаст-фуд, вулична торгівля/Обладнання для шаурми | |
| 32 | Теплове обладнання/Грилі контактні професійні | Фаст-фуд, вулична торгівля/Грилі контактні (притискні) | |
| 33 | Теплове обладнання/Електричні плити промислові | Плити професійні (варильні поверхні)/Плити електричні | |
| 34 | Теплове обладнання/Млинниці професійні | Фаст-фуд, вулична торгівля/Млинниці | |
| 35 | Теплове обладнання/Паназійська кухня | — | **null** |
| 36 | Теплове обладнання/Печі мікрохвильові професійні | Теплове обладнання/Мікрохвильові печі професійні | |
| 37 | Теплове обладнання/Підігрівачі настільні лампові | Теплове обладнання/Підігрівачі страв | ✅ confirmed (analogy agrees) |
| 38 | Теплове обладнання/Тостери професійні | Фаст-фуд, вулична торгівля/Тостери | |
| 39 | Теплове обладнання/Фритюрниці професійні | Теплове обладнання/Фритюрниці/Фритюрниці підлогові | ✅ confirmed (analogy majority 5/7) |
| 40 | Холодильне обладнання/Апарати для виготовлення морозива | Холодильне та морозильне обладнання/Апарати для морозива (фризера) і гранитори | |
| 41 | Холодильне обладнання/Барні холодильники | Холодильне та морозильне обладнання/Шафи настільні для бару, міні-бари (фрігобари) | |
| 42 | Холодильне обладнання/Вітрини вертикальні холодильні | — | **null** (heterogeneous 13 SKU → per-product analogy; verified fallback=0) |
| 43 | Холодильне обладнання/Вітрини для суші холодильні | Вітрини холодильні та морозильні для торгівлі/Вітрини для суші | |
| 44 | Холодильне обладнання/Вітрини кондитерські холодильні | Вітрини холодильні та морозильні для торгівлі/Кондитерські вітрини та шафи підлогові | |
| 45 | Холодильне обладнання/Вітрини холодильні | Вітрини холодильні та морозильні для торгівлі/Вітрини холодильні середньотемпературні (0°C....+7°C) | UNSURE — 0 products this import (defer) |
| 46 | Холодильне обладнання/Вітрини-надставки холодильні | Вітрини холодильні та морозильні для торгівлі/Вітрини та шафи настільні демонстраційні | ✅ confirmed (analogy majority 4/5) |
| 47 | Холодильне обладнання/Саладети | Холодильне та морозильне обладнання/Саладети, столи холодильні для піци та начинок | |
| 48 | Холодильне обладнання/Холодильні шафи для напоїв | Холодильне та морозильне обладнання/Шафи холодильні | ✅ confirmed (SKU: glass-door cabinets, not minibars) |
| 49 | Холодильне обладнання/Шафи для вина | Холодильне та морозильне обладнання/Холодильні шафи для вина | |
| 50 | Холодильне обладнання/Шафи шокової заморозки | Холодильне та морозильне обладнання/Апарати шокової заморозки (шокери) | |

### `null` — genuine gaps (5) — no store label exists; stay on analogy/fallback
- **Допоміжне обладнання/Подрібнювачі відходів** — no waste-disposer category in the store tree.
- **Допоміжне обладнання/Стерилізатори для ножів** — no sterilizer category (store has knife *sharpeners*, not sterilizers). NP has 1 product here → stays analogy.
- **Допоміжне обладнання/Стерилізатори для яєць** — no egg-sterilizer category. NP has 1 product here → stays analogy.
- **Теплове обладнання/Паназійська кухня** — "Pan-Asian cuisine" is a marketing bucket, not an equipment leaf; no store equivalent. (No products in this 320-НП slice.)
- **Холодильне обладнання/Вітрини вертикальні холодильні** (#42) — heterogeneous bucket (confectionery SW 504 + 10× upright display HKN-UPD* + tabletop RT 82 BE + cabinet RTC 237 + demo RT 82 WE); **no single store leaf fits all 13** → nulled 2026-05-31, routed to per-product analogy (re-measured: fallback stayed 0, all classified by same-brand cards).

### Integrity check (2026-05-31, read-only — verified, not asserted)

Checked the JSON directly against the export's **130 distinct `[КАТАЛОГ] Раздел`** values:
- **[A] All 45 non-null targets are verbatim store labels — 0 misses.** Every Option-B category already exists in Horoshop, so no card can land in a non-existent section (invariant #13 / live-store safety).
- **[B] All 5 nulls confirmed genuine gaps.** Keyword scans returned only false-positives: *Подрібнювачі відходів* → ice-crushers / food-cutters (not waste disposers); *Стерилізатори ножів* → knife sharpeners / knife inventory (not sterilizers); *Стерилізатори яєць* & *Паназійська кухня* → no store label at all; *#42* → only `…/Гірки-регали пристінні` (the wall-multideck label the 13 SKUs don't fit — re-confirms the null). The probe was throwaway and read-only; it changed no values.

### `UNSURE` — triaged against real audit data (2026-05-31)

Triage method (read-only, baseline Option-A audit `instance/category-analogy-audit.csv` + the NP feed, prod-guard intact): for each UNSURE feed label I counted how many of the **320 unmatched НП products** actually carry it this import, and — for the affected rows — what «Раздел» the **analogy tier picked independently** (no mapping). The audit CSV carries `chosen_category`/`source`/`confidence` per article; it has no per-row feed-category column, so the feed label per article was re-joined from the NP feed (`categories_uk`). Outcome below.

**Result: 4 promoted to CONFIDENT (analogy agrees), 3 deferred (0 products this import), 3 then deepened with the actual SKUs (2026-05-31) → #13 + #48 SKU-corroborated (CONFIRM), #42 nulled in the JSON.** #42's 13 SKUs are heterogeneous (none is a wall-multideck), so by this draft's own null-rule it falls through to per-product analogy. **Re-measured with #42 nulled: feed 312/320 = 97.5% conf-100, analogy 8 (2.5%), fallback 0** — every card still gets a store-valid category (was 99.4% when #42 was force-mapped, but those 6 rows were mis-shelved to Гірки-регали). Per-row evidence in the "Still flagged" bullets below.

**Promoted to CONFIDENT — analogy independently picked the SAME store label as the draft:**
- **#20 Преси для піци та гамбургерів** — 1 product; analogy → `Обладнання для піцерії/Преси для піци` = draft value, exact agreement. (The hamburger-press caveat is moot: the one affected card is a pizza press.) **CONFIDENT.**
- **#37 Підігрівачі настільні лампові** — 3 products; analogy → `Теплове обладнання/Підігрівачі страв` (3/3) = draft value, exact agreement. **CONFIDENT.**
- **#39 Фритюрниці професійні** — 7 products; analogy majority → `…/Фритюрниці підлогові` (5/7) = draft value; the other 2/7 analogs are `…/Фритюрниці настільні` (the size variant the feed doesn't disambiguate). Draft pick = analogy majority. **CONFIDENT** (note: 2 настільні cards exist among НП — if size matters those 2 may want the настільні leaf, but the draft's підлогові default is the analogy-backed plurality).
- **#46 Вітрини-надставки холодильні** — 5 products; analogy majority → `…/Вітрини та шафи настільні демонстраційні` (4/5) = draft value; 1/5 → `…/Кондитерські вітрини та шафи підлогові`. Draft pick = analogy majority. **CONFIDENT.**

**Deferred — 0 affected products this import (no card uses the mapping now; safe to leave, re-check if the feed adds such SKUs):**
- **#19 Подрібнювачі спецій** — 0 products this import — defer, no card uses it.
- **#28 Апарати для солодкої вати** — 0 products this import — defer, no card uses it. (Meaning "солодка вата"="цукрова вата" is still correct; just unexercised.)
- **#45 Вітрини холодильні** — 0 products this import — defer, no card uses it.

**Still flagged — deepened 2026-05-31 with the actual SKUs behind each (read-only NP-feed pull). The SKUs corroborate the draft for #13 and #48 (recommend confirm) and isolate #42 as the one genuine open call:**
- **#13 Фільтри для води — SKU-corroborated → recommend CONFIRM.** The 3 products are all **ASTORIA water *softeners*** (Пом'якшувач води LT.8/12/16, arts 26030–26032), not generic filters. The store tree has **no water-filter/softener leaf at all** (verified: 0 of 130 labels match фільтр/вод). Commercial water softeners are classic dishwasher/coffee-machine water-treatment consumables, so the draft target `Посудомийне обладнання/Аксесуари та допоміжне обладнання для посудомийних машин` is a sound functional home. (Analogy gave no signal — these are the §2.3 fallback gap.) Alternative: leave to holding if you'd rather shelve softeners separately.
- **#42 Вітрини вертикальні холодильні — the one genuine open call → recommend `null` or per-SKU.** The feed category is **heterogeneous**: COLD SW 504 is a *confectionery* display, SCAN RT 82 BE is *tabletop*, RT 82 WE is *demo*, RTC 237 is an upright *cabinet*, and 10× HURAKAN HKN-UPD* are upright glass display cases. A single map to `…/Гірки-регали пристінні` (wall multideck) would **mis-shelve most of them** — which is exactly why analogy split (4/6 кондитерські, 2/6 настільні). By this draft's own null-rule ("no single store label fits"), #42 is now **nulled in the JSON (done 2026-05-31).** The 13 SKUs route to per-product analogy (same-brand Hurakan/Scan/Atena export cards classify each); re-measured fallback stayed **0**, so none is orphaned. *Exact* per-SKU store labels would need a small code change (the mapping is keyed by feed-category, not by article) — flag it if you want that.
- **#48 Холодильні шафи для напоїв — SKU-corroborated → recommend CONFIRM.** All SKUs are **upright glass-door cabinets** (4× HURAKAN HKN-BC* «Шафа холодильна, скляні розпашні двері» + SCAN SD 430 BE demo) — full-height drinks coolers, **not** tabletop minibars. So the analogy's unanimous `…/Шафи настільні для бару, міні-бари (фрігобари)` pick is a **name-similarity misfire**, and the draft generic `Холодильне та морозильне обладнання/Шафи холодильні` is the correct shape. Confirm the draft.

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

Full suite (shipped behaviour gate): `./.venv/Scripts/python.exe -m pytest -q` → **843 passed, 2 skipped**.

## Activating Option B (now opt-in — no code change)
The wiring is **done and shipped** (2026-05-31), mirroring the optional `np_feed` upload:
- **Live UI:** `/feeds/add` → upload `category-mapping-draft.json` in the optional «Мапінг
  категорій (.json)» field, alongside the export (+ optionally the НП feed) → the file tier
  rewrites each mapped feed label to its store value before reconcile (mapped → confidence
  100). **No upload = Option A**, the shipped default, byte-for-byte unchanged.
- **Programmatic:** `build_add_file(..., category_mapping_path=<path>.json)` →
  `build_resolver(..., category_mapping=<dict>)` → `FeedCategoryResolver(..., mapping=<dict>)`.
  The JSON is parsed with the SAME `_load_mapping` rules as the audit (`_`-keys + null/blank
  dropped). `category_resolver.py` rewrites via `mapping.get(label, label)` — the identical
  expression the audit's getter uses — so a mapped label exact-matches the store set at 100.

Before relying on it: confirm the **3 still-UNSURE** rows (#13/#42/#48 — a wrong call there
silently mis-shelves a card) and re-check the whole table whenever the NP feed or the store
taxonomy shifts. The **4 promoted** rows are corroborated by the analogy tier on this import.
