# Category resolution — proposal & evidence (Phase 9, plan 09-02 / Task 6)

**For:** Yana (decision owner). **Status:** awaiting decision (this is Task 7).
**Decision context:** D3 — the create-card «Раздел» is assigned by analogy with
similar existing cards; AI (NVIDIA free tier) is an **option**, not a default
(REQ-06). This document gives you the real-data evidence to choose between
*ship-as-is (no AI)* / *enable AI* / *add a feed→store mapping table* before any
bulk import.

Everything below is measured, not estimated. Reproduce with:

```
./.venv/Scripts/python.exe scripts/audit_category_analogy.py \
  --export "horoshop-export 26.05.26.xlsx" \
  --np-feed .planning/plans/np-feed/np-feed.xlsx \
  --out instance/category-analogy-audit.csv
```

(Read-only, hard-guarded to local sqlite. Full per-row evidence in the CSV —
gitignored under `instance/`.)

---

## 1. What the chain does today (shipped in 09-02, AI OFF)

Three tiers behind one `category_resolver` interface, first non-empty wins,
fallback last so every card always gets a «Раздел»:

1. **feed** — for НП, take the article's feed «categories_uk» and *reconcile* it
   to the nearest store-tree label (exact match → 100; else token similarity of
   full path / leaf, cutoff 80). Never emits a category that isn't already in
   the store. The feed also backfills the card's UA/RU name + description, which
   the matcher DB doesn't hold for НП (FLAG-1 / decision D2).
2. **analogy** — copy the «Раздел» of the most similar **same-brand** export
   card (rapidfuzz token_sort_ratio over the product name, cutoff 60). Brand is a
   hard block: no brand → no analog. Reuses matcher *primitives* only, not
   `find_match_candidates` (its price/voltage gates over-reject same-category
   items).
3. **fallback** — the holding category «Новые товары / на разбор».

AI tier (`AICategoryResolver`) ships **disabled**: returns nothing, makes no
network call. Flipping it on is a one-argument change, no refactor (see §5).

---

## 2. Evidence — real run over 320 unmatched НП products

Corpus: `horoshop-export 26.05.26.xlsx` → **5632 cards, 130 store categories,
159 brands**. NP feed: `np-feed.xlsx` → **690 articles** (feed tier enabled).
Supplier: `novyy-proekt`, **320 products with no confirmed/manual match**.

### 2.1 How each card's category was assigned

| Tier | Cards | Share |
|---|---:|---:|
| feed (reconciled to store) | 130 | 40.6% |
| analogy (same-brand) | 175 | 54.7% |
| fallback (holding category) | 15 | 4.7% |
| **total** | **320** | **100%** |

**95.3% of cards get a real, store-valid category automatically.** Only 15 land
in the holding bucket.

### 2.2 Confidence distribution

**feed tier (n=130)** — high confidence, all ≥ 80:

| confidence | cards |
|---|---:|
| 90–100 | 94 |
| 80–89 | 36 |

**analogy tier (n=175)** — spread; the 60–69 band is the soft spot:

| confidence | cards |
|---|---:|
| 90–100 | 36 |
| 80–89 | 48 |
| 70–79 | 46 |
| 60–69 | 45 |

So ~84/175 analogy assignments (48%) clear 80; **45 sit at 60–69** — these are
the weakest, the ones a human spot-check (or AI) would most improve.

### 2.3 The 15 fallback cards (genuine gaps, not chain failures)

These brands have **no same-category analog** in the current export, so analogy
correctly declines rather than guess:

- **Sirman** Softcooker XP / XP S 1/1GN — sous-vide (no sous-vide card for Sirman)
- **Astoria** water softeners LT.8 / LT.12 / LT.16
- **TATRA** TVC 300 / TVC 800 vegetable cutters, TPP20F potato peeler
- **HURAKAN** HKN-PZLGV2S / HKN-PZLGV3S granite saladettes
- **Robot Coupe** CMP 350 V.V. stick mixer, 27164W grater plate
- **APACH** ASH15K DF blast chiller, **Bartscher** А100205 toaster, **CEADO** S98 citrus juicer

For these, either the export needs a representative card first, or the feed/
mapping must supply the category, or they go in by hand.

### 2.4 Feed ↔ store reconciliation delta (the key mapping signal)

Of the distinct НП feed categories seen, **26 reconciled to the store tree, 50
did NOT** (cutoff 80). The reason is structural: the feed uses a *different
top-level taxonomy* than the store. Examples (feed label → no store match):

- `Холодильне обладнання/Саладети` — store has `Холодильне та морозильне обладнання/…`
- `Теплове обладнання/Фритюрниці професійні` — store splits heat equipment differently
- `Професійне електромеханічне обладнання/Слайсери промислові` — store uses `Електромеханічне обладнання/…`
- `Обладнання для барів/Блендери професійні`, `Обладнання для м'ясних цехiв/М'ясорубки виробничі`, …

The leaf names are often close, but the parent path differs enough that
full-path similarity stays under cutoff. **These 50 are exactly the categories a
mapping table would fix** (full list in the Appendix). Until mapped, those НП
articles fall through feed → analogy (same-brand) → fallback — which is why
analogy still carries the majority.

---

## 3. Options for Yana

### Option A — Ship as-is, **no AI** (recommended for the first import)

Use the chain exactly as shipped. 95.3% auto-categorised, 4.7% to the holding
bucket for manual triage.

- **Pros:** zero new dependencies, zero network, fully deterministic and
  reproducible, already tested (843 passed). The holding bucket is small and
  visible — you can re-categorise those 15 in Horoshop after import.
- **Cons:** the 45 analogy cards at 60–69 confidence are plausible-but-unverified;
  the 50 unreconciled feed categories don't benefit the feed tier yet.
- **Best when:** you want to move now and clean up a small tail by hand.

### Option B — Add a feed→store **mapping table** (highest precision for НП)

> **Now reachable OPT-IN via the live UI (since 2026-05-31, no code change to activate):** upload `category-mapping-draft.json` on `/feeds/add` (optional «Мапінг категорій (.json)» field) — no upload = Option A default, unchanged. Draft map + UNSURE triage: `category-mapping-DRAFT.md`.

Author a small dict mapping the 50 unreconciled feed categories → their store
labels (one-time, ~50 lines; the leaf usually makes the target obvious). The
feed tier then reconciles far more НП articles at confidence 100.

- **Pros:** deterministic and exact for НП; directly raises the feed share and
  shrinks both the 60–69 analogy band and the fallback bucket; no AI, no network.
- **Cons:** ~1–2h of human mapping (best done by you — you know the store tree);
  needs a re-run to re-measure; only helps НП (other suppliers carry no feed).
- **Best when:** НП is the long-term bucket and you want it right, not just close.

### Option C — Enable the **AI tier** (NVIDIA free) as a *last-resort* before fallback

Insert AI between analogy and fallback: only the cards that feed+analogy can't
place (currently the 15 fallback + optionally the 60–69 band) get an AI
suggestion, constrained to the 130 real store categories.

- **Pros:** can rescue genuine gaps (§2.3) where no same-brand analog exists;
  catches edge cases A/B miss.
- **Cons:** **not built** — `AICategoryResolver.resolve` raises
  `NotImplementedError` when enabled; needs implementation + a real NVIDIA key +
  prompt design + its own tests; introduces a network dependency and
  non-determinism; must be constrained to the store label set or it will invent
  categories Horoshop can't create. **I did not wire any live AI call** (your
  call, REQ-06).
- **Best when:** after A or B, if the residual tail is still too large to triage
  by hand.

**My recommendation:** ship **A** now (or **A + a 1–2 row canary** below), then
do **B** as the next pass since НП is the durable bucket. Treat **C** as opt-in
only if a measured residual justifies the build + network dependency.

> **Update (2026-05-31) — converged & verified.** Option B is now built, wired
> opt-in, and **measured with #42 nulled: feed 312/320 = 97.5% conf-100, analogy
> 8, fallback 0** (no card orphaned). Integrity-checked against the export:
> **all 45 non-null targets are verbatim store labels (0 misses), all 5 nulls are
> genuine gaps.** UNSURE triage resolved: **#13 + #48 SKU-corroborated → CONFIRM;
> #42 nulled** (heterogeneous SKUs — vetoable). Full suite **843 passed, 2
> skipped**. Specifics: `category-mapping-DRAFT.md`. Your call stays A / B / C
> (REQ-06/D3); the import remains your hand + backup (invariant #13).

---

## 4. Before any bulk import — canary (invariant #13)

The builder is read-only and the import stays your hand. Before importing 320
cards:

1. Generate the file from `/feeds/add` (supplier НП, pick 1–2 brands, upload the
   export + optionally the НП feed).
2. **Backup** the store, import **1 row** first, verify in Horoshop: card
   created, «Раздел» correct, UA+RU name/description present, visible, price/
   old-price/availability sane.
3. Only then bulk-import the rest (feedback_labresta_live_import).

---

## 5. How to flip AI on later (no refactor)

```python
build_resolver(
    corpus,
    strategies=("feed", "analogy", "ai", "fallback"),  # add "ai" before fallback
    feed_category_getter=getter,
    ai_enabled=True,                 # currently False everywhere
    ai_model="<nvidia-model-id>",
)
```

Plus: implement `AICategoryResolver.resolve` (constrain output to
`store_categories`), set `NVIDIA_API_KEY`, add tests. Nothing else changes.

---

## Appendix — 50 unreconciled НП feed categories (need a store mapping for Option B)

```
Допоміжне обладнання/Подрібнювачі відходів
Допоміжне обладнання/Стерилізатори для ножів
Допоміжне обладнання/Стерилізатори для яєць
Обладнання для барів/Блендери професійні
Обладнання для барів/Електрокип'ятильники
Обладнання для барів/Кавомолки професійні
Обладнання для барів/Соковижималки
Обладнання для м'ясних цехiв/М'ясорубки виробничі
Обладнання для м'ясних цехiв/Фаршемiшалки виробничі
Обладнання для пекарських цехів/Тісторозкатки пекарські
Пакувальне обладнання/Апарати термопакувальні
Печі і пароконвектомати/Конвекційні печі
Посудомийне обладнання промислове/Фільтри для води
Професійне електромеханічне обладнання/Картоплечистки промислові
Професійне електромеханічне обладнання/Кутери професійні
Професійне електромеханічне обладнання/Овочерізки професійні
Професійне електромеханічне обладнання/Пили для м'яса
Професійне електромеханічне обладнання/Планетарні міксери
Професійне електромеханічне обладнання/Подрібнювачі спецій
Професійне електромеханічне обладнання/Преси для піци та гамбургерів
Професійне електромеханічне обладнання/Ручні міксери професійні
Професійне електромеханічне обладнання/Слайсери промислові
Професійне електромеханічне обладнання/Тістоміси промислові
Професійне електромеханічне обладнання/Хліборізки промислові
Професійне електромеханічне обладнання/Шприці ковбасні
Теплове обладнання/Апарати Sous-Vide
Теплове обладнання/Апарати для попкорну
Теплове обладнання/Апарати для солодкої вати
Теплове обладнання/Вафельниці професійні
Теплове обладнання/Газові плити професійні
Теплове обладнання/Грилі для шаурми
Теплове обладнання/Грилі контактні професійні
Теплове обладнання/Електричні плити промислові
Теплове обладнання/Млинниці професійні
Теплове обладнання/Паназійська кухня
Теплове обладнання/Печі мікрохвильові професійні
Теплове обладнання/Підігрівачі настільні лампові
Теплове обладнання/Тостери професійні
Теплове обладнання/Фритюрниці професійні
Холодильне обладнання/Апарати для виготовлення морозива
Холодильне обладнання/Барні холодильники
Холодильне обладнання/Вітрини вертикальні холодильні
Холодильне обладнання/Вітрини для суші холодильні
Холодильне обладнання/Вітрини кондитерські холодильні
Холодильне обладнання/Вітрини холодильні
Холодильне обладнання/Вітрини-надставки холодильні
Холодильне обладнання/Саладети
Холодильне обладнання/Холодильні шафи для напоїв
Холодильне обладнання/Шафи для вина
Холодильне обладнання/Шафи шокової заморозки
```

*(Store top-level labels to map onto, from the export's 130 categories: e.g.
«Холодильне та морозильне обладнання/…», «Електромеханічне обладнання/…»,
«Теплове обладнання/…», «Печі конвекційні та пароконвектомати/…». The leaf
usually identifies the target.)*
