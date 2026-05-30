# Phase 9: Add unmatched supplier products to Horoshop (new-card create file) — Research

**Researched:** 2026-05-30 (ночной режим, GSD researcher)
**Domain:** Native-Horoshop XLSX *create*-file generation for supplier products that have no live card; category-by-analogy resolution
**Confidence:** HIGH on create-schema, price path, models, filter/query design, builder shape (all read from disk). MEDIUM on category-by-analogy quality (sound design, needs the real-data sample to prove). One genuinely empirical unknown remains: which exact header string Horoshop's importer keys category from on a *create* (see Q1 / Open for Yana).

> Tooling note: the Bash tool stalled intermittently late in this session (empty returns). Every
> load-bearing fact below was read directly from disk while the tool was live: all 4 xlsx header rows
> via `openpyxl`, `np_horoshop_file.py`, `maresto_horoshop_file.py`, `pricing.py`, `feed.py`,
> `catalog_import.py`, `catalog.py`, `supplier_product.py`, `supplier.py`,
> `supplier_brand_discount.py`, `product_match.py`, `np_parser.py`, `kodaki_adapter.py`, and the
> `matcher.py` function inventory. The only items NOT pinned: the canary's data-cell *literal* for
> `[КАТАЛОГ] Отображать` (read it at plan time — file is on disk) and the live help.horoshop docs page
> (cyclic language redirect; prior research already extracted the required-fields rule from it).

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions (Yana, AskUserQuestion 2026-05-30)
- **D1 — Selection UX = filters + checkboxes.** A page listing unmatched products with filters
  (**supplier + brand**) and **checkboxes**, exactly like the existing `/feeds/np`. Operator ticks
  rows (or a whole brand), clicks generate, gets the XLSX.
- **D2 — RU fields from the feed where present.** Take RU from the supplier feed where it exists.
  The NP feed carries **RU description** (`np_parser` col Q → `description_ru`). Generalize: RU
  description from feed if available. RU **name** is generally absent (NP feed maps no name column)
  → `name_ru` optional / blank where absent.
- **D3 — Category (Розділ) by analogy = the HARD problem, research-led.** New cards must land in the
  CORRECT category by analogy with similar existing positions. AI API (NVIDIA) is a *possibility* to
  research and propose — **do NOT wire AI blindly**. Night rule: build core; build+test the non-AI
  analogy baseline + safe fallback; design the AI option and present it for Yana's call.

### Claude's Discretion (open to revision by research/plan)
- Feature branch `feat/horoshop-add-unmatched`; all night work here, Yana reviews + merges.
- Mirror, don't reinvent: builder mirrors `np_horoshop_file.py`; UI mirrors `/feeds/np`.
- Generalize across suppliers via the supplier+brand filter (not NP-only).
- Category as a pluggable resolver (strategy interface): `analogy` (baseline) → `fallback`
  (holding category) now; `ai` (NVIDIA) as a future plug Yana enables.

### Deferred Ideas (OUT OF SCOPE)
- Any actual import into the live store — stays **Yana's hand + backup** (invariant #13). We only
  PRODUCE the file. **Do not propose auto-import.**
- Automatic matching of the ~205 never-matched NP products (separate effort).
- Touching the binary YML availability mechanism (MARESTO parked awaiting Horoshop support).
- Final category strategy (analogy-only vs +AI vs hybrid) + AI enablement — **Yana decides
  post-proposal.**
- Persisting a `category` column in PromProduct *unless research proves it's the cleanest path*
  (research recommends generate-time read — see Q6).
- Whether the picker sets/honors the existing `mark_new` / `needs_catalog_add` flag.
</user_constraints>

<phase_requirements>
## Phase Requirements (success criteria from CONTEXT.md, treated as REQ IDs)

| ID | Description | Research Support |
|----|-------------|------------------|
| REQ-01 | Logged-in operator opens a page, filters unmatched products by supplier + brand, ticks rows, downloads a native-Horoshop XLSX | Q7 (query) + Q1 (schema). Mirror `/feeds/np` (`feed.py:186-253`). |
| REQ-02 | XLSX on a "New products: Import" run creates cards carrying name, price, discount (old price), availability, description (UA+RU where feed has it), photos, Артикул, brand, visibility, **Розділ** | Q1 (create schema), Q2 (required/recommended fields), Q3 (price path) |
| REQ-03 | Every row has a category (analogy where confident, fallback otherwise) — no row missing the REQUIRED Розділ | Q4 (analogy), Q5 (strategy compare), Q6 (generate-time read) |
| REQ-04 | Builder is read-only over the DB; no live import performed by the app | Mirror `np_horoshop_file.py` (read-only); Q7 queries are `select`-only |
| REQ-05 | Tests pass (`./.venv/Scripts/python.exe -m pytest`), mirroring existing builder tests | Validation Architecture section |
| REQ-06 | A written category proposal (analogy vs AI vs hybrid) + real-data evidence left for Yana; AI not default without her go-ahead | Q5 + "Open for Yana" section |
</phase_requirements>

## Summary

A new Horoshop card is created by a normal native-schema XLSX import with "New products: Import".
The **canonical schema lives on disk** in the dealer export `horoshop-export 20.05.26.xlsx` (sheet
`Sheet1`, **59 columns, Russian UI locale**; byte-identical header row to `horoshop-export
13.05.26.xlsx`). The header row IS the schema. The three create-required fields are present as bare
top-level headers: **`Артикул`** (col 0, the match key), **`Название (UA)`** (col 5), and
**`Раздел`** (col 8 — the category / "Розділ"; the export is RU-localized so it reads **`Раздел`**,
not `Розділ`). Visibility is **`Отображать`** (col 12).

The proven **import** dialect (live-validated `canary-HKN-PICO12M.xlsx`, and the shipped
`np_horoshop_file.py` + `maresto_horoshop_file.py` builders) prefixes catalog leaves with
**`[КАТАЛОГ] `** and uses a bare `Артикул` key, sheet **`Worksheet`**. So the create file is the
existing NP builder pattern **plus the columns the update-files deliberately omit**: `Название (UA)`
(+RU), `[КАТАЛОГ] Бренд`, `[КАТАЛОГ] Отображать`, **and a category column**. The update-files omit
these on purpose ("Horoshop only updates columns present"); a *create* file must include them.

Price for an **unmatched** SupplierProduct does NOT go through `compute_match_pricing(match)` (there
is no match). Use the existing pure pricing primitives directly: `resolve_discount_percent(None,
supplier, sp.brand)` → base discount, then `calculate_price_eur(sp.price_cents, eff_d)` for the sell
price; old price = `sp.price_cents/100` when a real discount applies. This is exactly what
`compute_match_pricing` does internally, minus the per-match-override branch. All needed `Supplier`
fields (`pricing_mode`, `discount_percent`, `min_margin_uah`, `cost_rate`, `eur_rate_uah`) and the
`SupplierBrandDiscount` shape (`brand`, `discount_percent`) are **verified in the models**.

**Primary recommendation:** Build one new builder `app/services/add_horoshop_file.py` (mirror
`np_horoshop_file.py`) + one picker view (mirror `/feeds/np`). Resolve category at **generate-time**
by reading the on-disk Horoshop export (the column `catalog_import.py` drops) — **no PromProduct
schema migration**. Ship a `category_resolver` strategy interface with `analogy` + `fallback` built
and an `ai` stub; default to the **`analogy → fallback` chain**, AI disabled. Run the analogy
resolver over a real sample of unmatched products and table the results for Yana (REQ-06).

**Primary recommendation (one-liner):** Clone the NP builder/picker; add name+brand+visibility+category
columns; price unmatched SPs via the pure `pricing.py` functions; resolve category at generate-time
from the uploaded export via a pluggable resolver (analogy→fallback, AI gated).

---

## Q1 — Canonical native CREATE schema (header strings read from disk)

### File-by-file (openpyxl on the project venv, UTF-8)

**`horoshop-export 20.05.26.xlsx`** — sheet **`Sheet1`**, **59 cols** (full dealer export = canonical
catalog schema; header row identical to `horoshop-export 13.05.26.xlsx`, also verified). Headers are
**bare top-level Russian** names (no `[КАТАЛОГ] ` prefix in the export). Indexed:

```
[00] Артикул                          ← CREATE KEY
[01] Родительский артикул
[02] Артикул для отображения на сайте    (= display_article, manufacturer SKU)
[03] Название модификации (UA)
[04] Название модификации (RU)
[05] Название (UA)                     ← CREATE REQUIRED (title)
[06] Название (RU)
[07] Бренд
[08] Раздел                           ← CATEGORY column = "Розділ". CREATE REQUIRED.
[09] Цена
[10] Старая цена
[11] Валюта
[12] Отображать                       ← VISIBILITY column
[13] Наличие
[14] Дополнительные разделы              (additional categories, multi)
[15] Фото
[16] Галерея
[17] Обзор 360
[18] Алиас
[19] Ссылка
[20] Дата добавления
[21..28] HTML title / META keywords / META description / h1   (UA+RU pairs)
[29] Поставщик
[30] Иконки
[31] Знижка %
[32] Популярность
[33] Количество
[34] Описание товара (UA)
[35] Описание товара (RU)
[36] Короткое описание (UA)
[37] Короткое описание (RU)
[38] Цвет
[39] Тип гарантии
[40] Гарантийный срок, мес.
[41] Дата и время окончания акции
[42] Текст акции (UA)
[43] Текст акции (RU)
[44] Описание для маркетплейсов (UA)
[45] Описание для маркетплейсов (RU)
[46] Выгружать на маркетплейсы
[47] Состояние товара
[48] Только для взрослых
[49] Код УКТ ВЭД
[50] Срок доставки предзаказа в днях
[51] «Оплата частями» ПриватБанка
[52] «Покупка частями» от monobank
[53] Код налоговой группы Вчасно.Каса
[54] Уникальный код налога
[55] Штрихкод
[56] Код производителя товара (MPN)
[57] На складе для Prom
[58] Электронный товар
```

**`.planning/plans/np-feed/canary-HKN-PICO12M.xlsx`** — sheet **`Worksheet`**, **26 cols**. This is
the **live-proven IMPORT dialect** (CANARY-IMPORT-GUIDE §7: 11/12 auto-mapped, zero UA→RU
corruption). Catalog fields carry the **`[КАТАЛОГ] `** prefix; key is bare `Артикул`:

```
[00] id
[01] Артикул                               ← bare key
[02] [КАТАЛОГ] Цена
[03] [КАТАЛОГ] Галерея
[04] [КАТАЛОГ] Наличие
[05] [КАТАЛОГ] Отображать                  ← VISIBILITY (import dialect, [КАТАЛОГ]-prefixed) — LIVE-PROVEN
[06] [КАТАЛОГ] Название модификации (UA)
[07] [КАТАЛОГ] Описание товара (UA)
[08] categories_uk                         ← CATEGORY in this live-proven import file (NOT [КАТАЛОГ] Раздел)
[09] [КАТАЛОГ] Бренд
[10..14] attr_contry_uk / attr_dimensions_uk / attr_power_uk / attr_voltage_uk / attr_weight_uk
[15] [КАТАЛОГ] Название модификации (RU)
[16] [КАТАЛОГ] Описание товара (RU)
[17] categories_ru                         ← RU category counterpart
[18..23] attr_brend_ru / attr_contry_ru / attr_dimensions_ru / attr_power_ru / attr_voltage_ru / attr_weight_ru
[24] [КАТАЛОГ] Старая цена
[25] [КАТАЛОГ] Валюта
```

**`horoshop-import-mini-5.xlsx`** — sheet **`Sheet`**, **9 cols**, **bare** (no `[КАТАЛОГ] ` prefix):
`Артикул`, `Название модификации (RU)`, `META keywords (UA)`, `META keywords (RU)`,
`Описание товара (RU)`, `Название (RU)`, `Описание товара (UA)`, `Название (UA)`,
`Название модификации (UA)`. A descriptions/titles-only **update** file — proves a narrow bare-header
file is also accepted, but it does not create (no SKU+category+price intent).

**`horoshop-export-extended.xlsx`** — **corrupt: `BadZipFile: Bad magic number`** (not a valid
.xlsx). Use `horoshop-export 20.05.26.xlsx` as the canonical reference. Do not depend on -extended.

### The exact category + visibility headers (the core answer)

| Concept | Export header (bare) | Import-dialect header | Evidence |
|---|---|---|---|
| **Category / Розділ** | **`Раздел`** (col 8) | `[КАТАЛОГ] Раздел` *(by the prefix rule)* **OR** `categories_uk` + `categories_ru` *(what the live canary actually used)* | export col 8; canary cols 8/17 |
| **Visibility** | **`Отображать`** (col 12) | **`[КАТАЛОГ] Отображать`** (canary col 5, **live-proven**) | export col 12; canary col 5 |

**Key nuance — the export is RU-localized.** CONTEXT/REQUIREMENTS say `Розділ` (UA), but the actual
dealer export on disk is **Russian**, so the column is **`Раздел`**. The shipped `np_horoshop_file.py`
already emits RU leaves (`[КАТАЛОГ] Наличие`, `Описание товара (UA/RU)`) that auto-map live → the
store's importer recognizes the RU qualified names. Use **RU** leaf names in the create file (match
the proven canary): `[КАТАЛОГ] Название (UA)`, `[КАТАЛОГ] Бренд`, `[КАТАЛОГ] Отображать`.

**Is create-import schema == export schema (round-trip)?** No. The **export** uses bare top-level RU
headers (`Раздел`, `Отображать`, `Цена`…). The **import Horoshop auto-maps** is the
**`[КАТАЛОГ] `-prefixed** dialect (np_horoshop_file docstring: auto-map happens "ONLY when the column
header equals the field's qualified name — `[КАТАЛОГ] <leaf>`, or a bare top-level name like
`Артикул`"). So: **key = bare `Артикул`; catalog leaves = `[КАТАЛОГ] <leaf>`.** A raw round-trip of
the bare export is NOT the proven import path; the `[КАТАЛОГ]` dialect is.

> **OPEN (empirical — see Open for Yana):** category import header. The export column is `Раздел`, so
> `[КАТАЛОГ] Раздел` is the natural create header — BUT the only file proven live used
> `categories_uk`/`categories_ru` (bare, no prefix) for category. The planner must NOT guess: a
> 1–2-row canary import (Yana's hand) decides whether `[КАТАЛОГ] Раздел` lands the card in the right
> section or whether `categories_uk`/`_ru` is required. **Make the category header a single
> switchable constant.** HIGH confidence the column is the only open detail; MEDIUM on which exact
> header string the importer keys on. (NB: `categories_uk` came from np.com.ua's own dealer export,
> so it is a known-good Horoshop category column — the safer default of the two.)

---

## Q2 — Is category required to create a card? + full field list

**Category IS required.** Prior research (`.planning/RESEARCH-horoshop-availability-and-new-offers.md`
Q2, from help.horoshop.ua "Importing products from a file"): *"Required fields for a NEW product:
SKU + Title (Назва) + Category (Розділ). Matching key = SKU."* The category column exists in the
export (`Раздел`, col 8), confirming the catalog stores it; `catalog_import.py` simply has no alias
for it (Q6), so our DB never captured it. (Live docs re-verification was blocked by a cyclic
language-redirect on help.horoshop.com; the rule stands from the prior research extraction.)

### Fields for a clean new card (create file column set)

| Field | Header (import dialect) | Required? | Source for unmatched SP |
|---|---|---|---|
| SKU / key | `Артикул` (bare) | **REQUIRED** (key) | `SupplierProduct.article` (== feed Артикул / `<vendorCode>`) — see note |
| Title UA | `[КАТАЛОГ] Название (UA)` | **REQUIRED** | `SupplierProduct.name` |
| Category | `[КАТАЛОГ] Раздел` *(or `categories_uk`/`_ru`)* | **REQUIRED** | category resolver (Q4) |
| Price | `[КАТАЛОГ] Цена` | strongly recommended | pricing (Q3) |
| Old price | `[КАТАЛОГ] Старая цена` | optional (strike-through) | retail when discounted (Q3) |
| Currency | `[КАТАЛОГ] Валюта` | recommended | `sp.currency` ∈ {EUR,UAH} else EUR |
| Availability | `[КАТАЛОГ] Наличие` | recommended | `В наличии` / `Нет в наличии` |
| Visibility | `[КАТАЛОГ] Отображать` | recommended for create | see note |
| Brand | `[КАТАЛОГ] Бренд` | recommended | `sp.brand` (NP: feed `attr_brend_uk`) |
| Title RU | `[КАТАЛОГ] Название (RU)` | optional | blank (NP feed has no name col — D2) |
| Gallery | `[КАТАЛОГ] Галерея` | recommended | `sp.images` JSON / NP feed photos |
| Main photo | `[КАТАЛОГ] Фото` | optional (gallery often enough) | `sp.image_url` |
| Desc UA | `[КАТАЛОГ] Описание товара (UA)` | recommended | `sp.description` / NP feed desc_uk |
| Desc RU | `[КАТАЛОГ] Описание товара (RU)` | recommended | NP feed `description_ru` (D2) |

**Notes:**
- **`Артикул` (key) for a NEW card = supplier article.** For NP the *update*-file uses
  `PromProduct.external_id` because the card already exists. For a **create**, there is no
  PromProduct, so the key is the **supplier's article** (`SupplierProduct.article`, == `<vendorCode>`,
  == the NP feed `Артикул`). It becomes the new card's external_id in Horoshop. **Skip + report rows
  with empty article** (mirror `np_parser`/`maresto_horoshop_file._shape_rows` `skipped_no_artikul`).
- **`Отображать` value (plan-time read).** Need the literal Horoshop expects (likely `Да`/`Нет` or
  `+`/`-`). The canary has the column (col 5) with a real value — **read the canary data row at plan
  time** (`.planning/plans/np-feed/canary-HKN-PICO12M.xlsx`; this session's Bash stalled before
  printing it). Default proposal: use the canary's literal for "visible"; if still unknown, **omit
  the column** and let Horoshop default new cards to its configured visibility (omitting is lower-risk
  than guessing a wrong literal that hides every card — see Pitfall 4).
- **Currency:** mirror `np_horoshop_file.py:218` — `sp.currency if in ("EUR","UAH") else "EUR"`.

---

## Q3 — Price / discount path for an UNMATCHED SupplierProduct

There is **no `ProductMatch`**, so `compute_match_pricing(match)` (`pricing.py:228`) doesn't apply —
it dereferences `match.supplier_product` and `match.discount_percent`. Its internals are pure and
reusable. The unmatched path == `compute_match_pricing` **minus the match-override branch**.

**Functions to call (all in `app/services/pricing.py`, verified):**
1. **Base discount:** `resolve_discount_percent(match_discount=None, supplier=sp.supplier,
   brand=sp.brand)` (`pricing.py:83`). With `match_discount=None` it reads `supplier.pricing_mode`:
   - `per_brand` → looks up `supplier.brand_discounts` (rows with `.brand` + `.discount_percent`)
     case-insensitively by `sp.brand`, falling back to `supplier.discount_percent`.
   - else (`flat` / `auto_margin` / other) → `supplier.discount_percent`.
2. **Min-margin clamp (only if `supplier.min_margin_uah > 0`):**
   `clamp_discount_for_min_margin(base_d, sp.price_cents, rate, min_margin, cost_rate)`
   (`pricing.py:130`). `rate = resolve_eur_rate(supplier)` (`pricing.py:15`); **`rate = 1.0` when
   `sp.currency == "UAH"`** (keep math in UAH), exactly as `compute_match_pricing` does
   (`pricing.py:244`). `cost_rate = supplier.cost_rate or 0.75`.
3. **Sell price EUR:** `calculate_price_eur(sp.price_cents, eff_d)` (`pricing.py:35`) → tenths,
   half-up.
4. **Old price (strike-through):** retail = `sp.price_cents / 100`. Emit `f"{retail:.1f}"` **only
   when** `retail > sell + 0.05` (a real discount), else `""` — copy the exact rule from
   `np_horoshop_file.py:135-139` / `maresto_horoshop_file.py:104`.

**Cleanest reuse — extract a shared helper.** Match path and unmatched path differ only in where the
discount comes from. Recommended: a small pure function in `pricing.py`, e.g.
`compute_supplier_product_pricing(sp, match_discount=None) -> dict | None` returning
`{price_eur, retail_eur, oldprice, currency, base_discount, effective_discount}`, called by BOTH
`compute_match_pricing` (passing `match.discount_percent`) and the new builder. This preserves the
"price the operator approves == price emitted" invariant (`pricing.py:186-198`) and avoids the P-3
divergence bug class. If a refactor is too invasive for this phase, the builder may inline steps 1–4
(all pure) — but a shared helper is the correct K2/K3 move.

**Where discount lives (verified in models):**
- Per-supplier default: **`Supplier.discount_percent`** (Float, `supplier.py:37`; read at
  `pricing.py:116`).
- Per-supplier mode: **`Supplier.pricing_mode`** ∈ {`flat`, `per_brand`, `auto_margin`}
  (`supplier.py:49-54`).
- Margin knobs: **`Supplier.min_margin_uah`** (default 500.0, `supplier.py:42`), **`cost_rate`**
  (default 0.75, `supplier.py:45`), **`eur_rate_uah`** (default 51.15, `supplier.py:38`).
- Per-brand override: **`SupplierBrandDiscount`** (`supplier_brand_discount.py`): columns
  `supplier_id`, `brand` (String, NOT NULL), `discount_percent` (Float, NOT NULL); relationship
  **`Supplier.brand_discounts`** (backref, cascade all/delete-orphan); unique `(supplier_id, brand)`.
  Loaded via `selectinload(Supplier.brand_discounts)` in `np_horoshop_file.py:198` /
  `maresto_horoshop_file.py:146`.
- MARESTO uses `auto_margin`/`calculate_auto_discount` (`pricing.py:275`, CLAUDE.md #12). For
  unmatched products in `flat`/`per_brand` suppliers the path above is correct; for an `auto_margin`
  supplier, follow `calculate_auto_discount(sp.price_cents, rate)` directly.

---

## Q4 — Category-by-analogy feasibility (the hard problem)

### What the matcher gives us (read from `matcher.py`)

`matcher.py` is a fuzzy **supplier→catalog** matcher: `rapidfuzz` WRatio + brand blocking + a chain
of gates (type gate, model/article boost, voltage, containment, transliteration, bracket
discriminator). Tunables: `SCORE_CUTOFF=60`, `MATCH_LIMIT=3`, `MODEL_BOOST_POINTS=10`,
`BRAND_MATCH_THRESHOLD=80`, `MAX_PRICE_RATIO=3.0`. Verified **reusable public/helper functions**
(line numbers from the inventory):
- `meaningful_tokens(text) -> set[str]` (`:802`) — token set after brand/noise stripping.
- `extract_model_from_name(name, brand) -> str` (`:309`), `extract_product_type(name, brand)`
  (`:901`), `_transliterate_cyr(text)` (`:894`), `normalize_text` (`:208`), plus glue/morph helpers
  (`:588`, `:654`, `:683`).
- `find_match_candidates(...)` (`:929`) — the full pipeline (uses `fuzz.WRatio` + all gates).

### Is matcher's similarity reusable as-is? **No — but its primitives are.**

- The full pipeline is purpose-built for **SP↔PP correctness** with **price/voltage gates** that are
  *wrong* for category-analogy — we WANT to match across price tiers and voltages (a 220V and 380V
  slicer are the same *category*). Using the whole pipeline would over-reject (CLAUDE.md invariants
  #1, #9, #15 are correctness gates, not category gates).
- **Reusable:** the brand block + name normalization + token similarity. For category-by-analogy the
  right shape is: among existing cards **of the same brand**, pick the card with the highest
  **name/article token similarity** (`fuzz.token_sort_ratio` over `meaningful_tokens`, with
  `_transliterate_cyr` for Cyrillic/Latin mixes) and copy its category. This reuses the helpers
  without the reject gates.

### Proposed analogy algorithm (no AI)

1. **Build the category corpus at generate-time (Q6):** read the on-disk Horoshop export → per row
   capture `{external_id, name, brand, display_article, Раздел}` (the `Раздел` column
   `catalog_import.py` drops). This is the "existing cards with known category" corpus.
2. **Block by brand:** candidate set = export rows where `normalize(brand) == normalize(sp.brand)`.
   If `sp.brand` empty → low precision; go straight to fallback (Q5b) instead of matching all rows.
3. **Rank by name similarity:** score each candidate with `fuzz.token_sort_ratio` over
   `meaningful_tokens(sp.name)` vs `meaningful_tokens(card.name)` (+ optional model/article boost via
   `extract_model_from_name`). Take top-1.
4. **Confidence + threshold:** `confidence = top1_score`. If `>= ANALOGY_CUTOFF` (start at 60, tune
   on real data) → use that card's `Раздел`. Else → **fallback** category (Q5b). Record chosen
   category + confidence + analog card id in the manifest for audit.
5. **"Test the theory":** run steps 1–4 over a real sample of the ~205 unmatched NP products (LOCAL
   sqlite only) and table `{sp.name, brand, chosen Раздел, confidence, analog card}` for Yana — the
   evidence REQ-06 demands.

**Confidence: MEDIUM.** The approach is sound and reuses proven primitives; real quality depends on
how cleanly brands cluster into single categories in the export. The sample run (step 5) converts
this to a defensible recommendation — do it.

### `kodaki_adapter.py` + `Кодаки поставщик категории.xlsx` — reusable prior art?

**Both checked this session. Verdict: NOT reusable for category resolution.**
- **`kodaki_adapter.py` is NOT a category mapping.** It is a **feed-format adapter** that rewrites
  non-YML supplier XML (Kodaki/Gooder/Astim) into YML so `feed_parser` can ingest it
  (`apply_supplier_adapter` dispatches by URL host). It carries no Horoshop category logic. The only
  category-adjacent thing: the **Astim** adapter passes the supplier's own `<category>`/`<subcategory>`
  through as `<param>` values "for operator context" (`astim_to_yml`) — i.e. raw supplier strings,
  not Horoshop `Раздел`. Not a mapping table.
- **`Кодаки поставщик категории.xlsx` is CORRUPT** (`KeyError: no item 'xl/sharedStrings.xml'` —
  same corruption class as `horoshop-export-extended.xlsx`). Could not read its shape. **Do not plan
  around it.** If Yana re-exports a clean copy and it turns out to be a curated `{brand/keyword →
  Раздел}` table, it can later become a higher-precision **`mapping` strategy** tier ahead of
  `analogy` — but treat that as optional/deferred, not a phase-9 dependency.

---

## Q5 — Category strategy comparison

| Strategy | How | Pros | Cons | Verdict |
|---|---|---|---|---|
| **(a) Analogy from export (no AI)** | brand-block + name token similarity vs export `Раздел` corpus (Q4) | zero external deps; deterministic; testable; uses live category truth | quality varies; needs threshold tuning; weak when brand spans many categories or SP brand empty | **BUILD — default tier 1** |
| **(b) Safe holding-category fallback** | one constant category (e.g. «Новые товары / на разбор») for low-confidence / no-analogy rows | lowest risk; guarantees every row has a Раздел (REQ-03); Yana re-sorts in admin | extra manual re-sort step | **BUILD — default tier 2 (always present)** |
| **(c) AI (NVIDIA free)** | give model the existing category list + product name/desc → classify into a leaf | handles no-brand / novel items; potentially higher accuracy than fuzzy | external dep + key + latency + 40 RPM cap; non-determinism; must validate | **RESEARCH + PROPOSE ONLY — Yana-gated** |

### AI option design (NVIDIA `build.nvidia.com`)

- **Endpoint (memory `reference_nvidia_build_api`):** OpenAI-compatible base
  `https://integrate.api.nvidia.com/v1`, 40 RPM free tier, ~80 models. **Verify endpoint + pick a
  current model name at wire time** (a quick WebSearch) — do NOT hardcode a model now. A small
  instruct model (e.g. a Llama-3.x-instruct on NVIDIA) suffices for classification.
- **Prompt shape:** system = "assign the product to exactly one category from this list"; user = the
  **flat deduped list of existing `Раздел` values** (from the export — this is the allowed label set,
  so the model can't invent a category) + the product `{name, brand, short desc}`; constrain output
  to one label; **validate it's in the set, else → fallback**.
- **Cost/quality/latency:** free; ~1 call/product; 40 RPM ⇒ ~205 products in <6 min with simple rate
  limiting; non-deterministic ⇒ keep a confidence/needs-review flag for Yana's audit.
- **Plug point:** the `category_resolver` **strategy interface** (below). AI is just another tier;
  off by default, enabled by config/flag once Yana approves.

### Recommended default for the build

**Chain: `mapping?` → `analogy` → `fallback`.** Build `analogy` + `fallback` now. (`mapping` only if
Yana provides a clean Kodaki-style table — corrupt now, so out of phase-9 scope.) Ship the **`ai`
tier as a stub** behind the same interface so enabling it later is a config flip, not a refactor.
Default config = **AI disabled**. Satisfies D3 (no blind AI), REQ-03 (every row gets a category),
REQ-06 (proposal + real-data evidence).

### Strategy interface (proposed)

```python
# app/services/category_resolver.py
class CategoryResolver(Protocol):
    def resolve(self, sp, *, brand: str | None) -> "CategoryResult": ...
# CategoryResult = {category: str | None, confidence: float, source: str, analog_id: str | None}
def build_resolver(export_rows, *, strategies=("analogy", "fallback"),
                   fallback_category="Новые товары / на разбор") -> CategoryResolver: ...
```

---

## Q6 — Persist category in PromProduct vs read at generate-time

**Recommendation: read at generate-time from the on-disk Horoshop export. Do NOT add a PromProduct
`category` column.**

Reasoning:
- **The data is already recoverable.** `catalog_import.py` `COLUMN_ALIASES` (verified, lines 20-56)
  has **no alias for `Раздел`/`Дополнительные разделы`** — the export's category column is read by
  `parse_xlsx` then discarded by `map_headers` (only aliased columns survive). So **every existing
  card's category lives in `horoshop-export*.xlsx` on disk**. (`catalog.py` confirms `PromProduct`
  has no category field; fields: external_id, name, name_ru, brand, model, article, display_article,
  price, currency, page_url, image_url, images, description_ua, description_ru, operator_decision*.)
- **Mirrors the existing two-channel / generate-time design.** NP content (desc/photos) is **joined
  at generate-time** from the live feed via `np_parser`, not persisted (np_horoshop_file docstring +
  catalog_import "two-channel separation"). Category-by-analogy is the same pattern: join an external
  artifact at build time. Consistency > a new column.
- **Freshness.** Categories change in Horoshop admin; a persisted column drifts and needs a sync
  path. Reading the latest export at generate-time is always current.
- **Migration risk.** A column means a migration on **live sqlite** + touching `catalog_import.py`
  save/preview + `CATALOG_FIELDS` — which has a documented footgun: listing a field there made
  imports null it (see the `article` comment at `catalog_import.py:231-237`, CLAUDE.md #2). Avoid
  that blast radius for a phase that only *produces a file*.

**Cost of generate-time:** the operator supplies a recent export (an upload field on the picker, or a
configured path). Minor UX add, and it matches how `/feeds/np` already fetches a feed at
generate-time. **If Yana later wants persistence** (to skip the upload), add a `category` alias +
nullable column then — a separate, deferred decision (CONTEXT.md defers it).

**Generate-time input mechanism (recommend):** an **upload field** on the picker for the Horoshop
export xlsx (parsed read-only into the `{external_id|name|brand → Раздел}` corpus), mirroring how
`np_file_generate` writes the fetched feed to a temp file and builds from a local path
(`feed.py:226-231`). Keep the builder pure over local paths (no network), exactly like
`build_np_file(selected_brands, feed_path)`.

---

## Q7 — Filter data source + querying unmatched products

### Suppliers + brands for the picker

- **Suppliers:** `select(Supplier)` (the `/feeds/np` page hardcodes NP; generalize to a supplier
  dropdown). `SupplierProduct.supplier` relationship + `Supplier.products` backref exist
  (`supplier_product.py:40`).
- **Brands per supplier:** `select(distinct(SupplierProduct.brand)).where(SupplierProduct.supplier_id
  == sid, SupplierProduct.is_deleted.is_(False), SupplierProduct.ignored.is_(False))`. Derive the
  brand list from the DB (not the hardcoded `NP_BRANDS`) so it works for any supplier. Normalize/group
  case-insensitively like `_np_brand_match_counts` (`feed.py:179-183`).

### Querying UNMATCHED products efficiently (invert `_np_brand_match_counts` / `_query_np_priced`)

"Unmatched" = **no `ProductMatch` with `status in {confirmed, manual}`** (CONTEXT.md "No match"
definition; `ProductMatch.status` ∈ {candidate, confirmed, rejected, manual}, verified
`product_match.py:22-27`). A candidate/rejected match still means "no live card linked", so they
count as unmatched. Mirror the NP join but invert with NOT-EXISTS (single read-only query):

```python
from sqlalchemy import select, exists
linked = (
    select(ProductMatch.id)
    .where(
        ProductMatch.supplier_product_id == SupplierProduct.id,
        ProductMatch.status.in_(("confirmed", "manual")),
    )
    .correlate(SupplierProduct)
)
unmatched = db.session.execute(
    select(SupplierProduct)
    .where(
        SupplierProduct.supplier_id == sid,
        SupplierProduct.is_deleted.is_(False),
        SupplierProduct.ignored.is_(False),
        ~exists(linked),                      # ← inversion of the NP "has confirmed/manual" filter
        # optional brand filter:
        # func.lower(func.trim(SupplierProduct.brand)).in_(selected_brands_norm),
    )
    .order_by(SupplierProduct.brand, SupplierProduct.name)
).scalars().all()
```

- **Per-brand counts for the page** (instant, DB-only — mirror `_np_brand_match_counts`,
  `feed.py:165-183`, but with `~exists(linked)` and `group_by(SupplierProduct.brand)`).
- **`published` flag:** the NP query also filters `ProductMatch.published.is_(True)`. For *unmatched*
  it's irrelevant (we assert no confirmed/manual match exists at all). Do **not** add it to the
  NOT-EXISTS, or a `published=False` confirmed match would wrongly read as "unmatched".
- **Existing flags (CONTEXT defers the decision):** `SupplierProduct.needs_catalog_add`
  (server_default 0, `supplier_product.py:28`) and the `/matches/mark-new/<sp_id>` audit «Позначено
  для додавання» already mark SPs "to add". The picker MAY pre-tick rows where `needs_catalog_add` is
  true and/or surface it as a column. **Recommend:** read-only for now (don't mutate on generate —
  keeps builder read-only, REQ-04). Leave set/honor to Yana (deferred).

---

## Recommended approach (planner-ready)

### New files (mirror existing, don't reinvent)
1. **`app/services/add_horoshop_file.py`** — the create-file builder. Mirror `np_horoshop_file.py` /
   `maresto_horoshop_file.py`: module-level `[КАТАЛОГ]`-prefixed `HEADERS` constant (now *with*
   `Название (UA/RU)`, `Бренд`, `Отображать`, and the category header constant), pure `_shape_rows()`,
   pure `_workbook_bytes()`, read-only `_query_unmatched(supplier_id, brands)`, and
   `build_add_file(supplier_id, selected_brands, export_path, *, np_feed_path=None) -> (bytes,
   manifest)`. Sheet `Worksheet`. Key = bare `Артикул` from `sp.article`; skip+report empty article.
2. **`app/services/category_resolver.py`** — strategy interface + `analogy` + `fallback` (+ `ai`
   stub). Pure; takes the export-derived corpus. (Q5)
3. **A picker view** — mirror `/feeds/np` (`feed.py:186-253`): GET page (supplier dropdown + brand
   checkboxes + row checkboxes + export upload field), POST generate (parse uploaded export → corpus →
   `build_add_file` → `send_file` + `log_action`). `@login_required`. New blueprint or extend
   `feed_bp` (e.g. `/feeds/add` + `/feeds/add/generate`).
4. **Templates** — mirror `feeds/np.html`.
5. **Tests** — `tests/test_add_horoshop_file.py` + `tests/test_category_resolver.py` + a view test,
   mirroring `tests/test_np_*` (read-only, local sqlite). See Validation Architecture.

### Core builder row shape (per ticked, unmatched SP)
```
Артикул                         = sp.article            # bare key; skip if empty
[КАТАЛОГ] Название (UA)          = sp.name
[КАТАЛОГ] Название (RU)          = "" (NP feed has no name col; D2)
[КАТАЛОГ] Бренд                  = sp.brand
[КАТАЛОГ] Раздел  (or categories_uk/_ru — empirically decide)  = resolver.resolve(sp).category
[КАТАЛОГ] Цена                  = f"{price_eur:.1f}"     # Q3
[КАТАЛОГ] Старая цена            = oldprice or ""         # Q3 (retail when discounted)
[КАТАЛОГ] Валюта                 = sp.currency in {EUR,UAH} else EUR
[КАТАЛОГ] Наличие                = "В наличии"/"Нет в наличии"   # from sp.available (bool)
[КАТАЛОГ] Отображать             = <visible literal from canary>  # or omit if literal unknown
[КАТАЛОГ] Галерея                = ";".join(photos)       # sp.images JSON / NP feed photos
[КАТАЛОГ] Описание товара (UA)   = sp.description / NP feed desc_uk
[КАТАЛОГ] Описание товара (RU)   = NP feed description_ru  # D2
```
Availability: `sp.available` is a direct bool (`supplier_product.py:18`), so a bare
`"В наличии" if sp.available else "Нет в наличии"` suffices (NP/MARESTO builders used a match-derived
helper only because they had a match; no match here).

### Category strategy recommendation
Default **chain `analogy` → `fallback`** (add `mapping` only if Yana supplies a clean table), AI
**disabled** (stubbed behind the interface). Resolve at **generate-time** from the uploaded export.
Produce the real-data analogy sample table for Yana (REQ-06).

### Persist vs generate-time recommendation
**Generate-time read of the export. No PromProduct schema migration.** (Q6.)

---

## Don't Hand-Roll

| Problem | Don't build | Use instead | Why |
|---|---|---|---|
| Native Horoshop XLSX shape | new header guesses | the live-proven `[КАТАЛОГ] ` headers from `np_horoshop_file.py` / `maresto_horoshop_file.py` / canary | retyping from memory risks UA→RU corruption (the exact bug the canary avoided) |
| Discount → sell price | new math | `pricing.py` `resolve_discount_percent` + `calculate_price_eur` (+ clamp) | single source of truth; divergence = P-3 bug class |
| Picker page + generate flow | new pattern | clone `/feeds/np` (`feed.py`) | proven temp-file → build → send_file → log_action |
| Name normalization for analogy | new tokenizer | `matcher.py` `meaningful_tokens` / `extract_model_from_name` / `_transliterate_cyr` | already handles glue/morph/Cyrillic |
| Feed content lookup (NP) | new parser | `np_parser.parse_np_feed` | fixed-column contract + header sanity-check |

**Key insight:** this phase is ~90% *assembly of existing, live-proven parts*. The only genuinely new
logic is the category resolver — and even that reuses matcher primitives.

## Common Pitfalls

1. **Wrong category header → cards land in wrong/no section.** Export says `Раздел`; the only
   live-proven import used `categories_uk`/`_ru`. **Decide empirically with a 1–2 row canary (Yana's
   hand)** before any bulk import. Make the header a single switchable constant.
2. **UA vs RU header locale.** The export is **Russian** (`Раздел`, `Отображать`, `Цена`). Use RU
   leaf names (the proven canary did) — don't emit UA `Розділ`/`Відображати`.
3. **Empty `sp.article` → uncreatable row.** Skip + report (mirror `np_parser` /
   `maresto_horoshop_file` `skipped_no_artikul`). The key for a *create* is the supplier article, not
   a PromProduct external_id.
4. **Wrong `Отображать` literal → every new card hidden.** Don't guess; read it from the canary data
   row, or omit the column and rely on Horoshop's default.
5. **Reusing the full matcher pipeline for analogy → over-rejection.** Its price/voltage gates reject
   same-category items. Use only the brand block + token similarity.
6. **Mutating DB on generate → breaks read-only invariant (REQ-04).** Don't set `needs_catalog_add`
   on generate unless Yana asks.
7. **Prod DB.** Any sample/test run must be LOCAL sqlite; abort if the URL contains
   `rlwy|railway|postgres|psycopg` (CLAUDE.md #10/#13; `scripts/generate_maresto_availability.py`
   guard; `app/__init__.py:20-31` `TESTING=1`+prod → RuntimeError).
8. **Corrupt input files on disk.** `horoshop-export-extended.xlsx` and `Кодаки поставщик
   категории.xlsx` are corrupt (no sharedStrings). Use `horoshop-export 20.05.26.xlsx`; ignore the
   Kodaki categories file unless Yana re-exports it cleanly.

## Code Examples

**Unmatched-SP pricing (assemble from verified pure functions):**
```python
# Source: app/services/pricing.py (resolve_discount_percent:83, calculate_price_eur:35,
#         clamp_discount_for_min_margin:130, resolve_eur_rate:15) — mirrors compute_match_pricing:228
def price_unmatched(sp):
    supplier = sp.supplier
    base_d = float(resolve_discount_percent(None, supplier, getattr(sp, "brand", None)) or 0.0)
    rate = resolve_eur_rate(supplier)
    if getattr(sp, "currency", "EUR") == "UAH":
        rate = 1.0
    eff_d = base_d
    min_margin = float(getattr(supplier, "min_margin_uah", 0.0) or 0.0)
    if min_margin > 0 and sp.price_cents:
        cost_rate = float(getattr(supplier, "cost_rate", 0.75) or 0.75)
        eff_d = float(clamp_discount_for_min_margin(base_d, sp.price_cents, rate, min_margin, cost_rate))
    sell = calculate_price_eur(sp.price_cents, eff_d)
    retail = (sp.price_cents or 0) / 100.0
    oldprice = f"{retail:.1f}" if retail > sell + 0.05 else ""
    return sell, oldprice
```

**Native xlsx writer (copy verbatim from the proven builders):**
```python
# Source: np_horoshop_file.py:171-182 / maresto_horoshop_file.py:119-130
def _workbook_bytes(rows, HEADERS):
    wb = openpyxl.Workbook(); ws = wb.active; ws.title = "Worksheet"
    ws.append(HEADERS)
    for r in rows: ws.append([r[h] for h in HEADERS])
    buf = io.BytesIO(); wb.save(buf); wb.close(); return buf.getvalue()
```

**Unmatched query (NOT-EXISTS inversion):** see Q7.

## State of the Art

| Old approach | Current approach | Impact |
|---|---|---|
| YML feed for content | native `[КАТАЛОГ] ` XLSX (Channel 2) | YML drops `description_ru` + corrupts name UA→RU; XLSX auto-maps cleanly (proven live 2026-05-19) |
| Category persisted? | never captured (no alias) | category recoverable only from the export on disk → read at generate-time |
| Availability | binary YML attr | named «Наличие» status column via `[КАТАЛОГ] Наличие` (MARESTO builder) — for a *create* a simple yes/no is enough |

## Open Questions

1. **Category import header — `[КАТАЛОГ] Раздел` vs `categories_uk`/`categories_ru`.** Export uses
   `Раздел`; the only live-proven import used `categories_uk`/`_ru` (and that file came from a real
   Horoshop dealer export, so `categories_uk` is known-good). *Recommendation:* default to
   `categories_uk`(+`categories_ru`) as a single switchable constant; Yana runs a 1–2 row canary to
   confirm before bulk. (MEDIUM)
2. **`Отображать` visible literal.** Need the exact string. *Recommendation:* read the canary data row
   at plan time; else omit and rely on default. (LOW until canary row read)
3. **`ANALOGY_CUTOFF` value + real quality.** *Recommendation:* start at 60 (matcher's cutoff), tune
   on the real-data sample run; that run is the deliverable for Yana. (MEDIUM)
4. **Clean Kodaki category table?** Current file corrupt. If Yana re-exports, evaluate as a `mapping`
   tier. (Deferred)

## Environment Availability

| Dependency | Required by | Available | Version | Fallback |
|---|---|---|---|---|
| Python venv | build + tests | ✓ | 3.14.3 (`.venv/Scripts/python.exe`) | — |
| openpyxl | read export / write xlsx | ✓ | 3.1.5 | — |
| rapidfuzz | analogy similarity | ✓ (matcher dep) | — | pure-Python token overlap |
| local sqlite | sample/test (read-only) | ✓ | WAL | — |
| NVIDIA API | AI category tier (Yana-gated, optional) | ✗ (key not configured) | — | analogy + fallback (default) — AI off |

**Missing with fallback:** NVIDIA API — AI tier off by default; analogy+fallback cover REQ-03.
**Missing, blocking:** none. (`horoshop-export-extended.xlsx` and `Кодаки поставщик категории.xlsx`
are corrupt — use `horoshop-export 20.05.26.xlsx`; not blocking.)

## Validation Architecture

> nyquist_validation key absent from `.planning/config.json` → treated as enabled. `workflow.verifier:
> true`, `workflow.plan_check: true`.

### Test Framework
| Property | Value |
|---|---|
| Framework | pytest (`tests/`, shared session fixture in `tests/conftest.py`, prod-DB guard `app/__init__.py:20-31`) |
| Config | pytest invoked via venv; **NOT** uv/`uv run` |
| Quick run | `./.venv/Scripts/python.exe -m pytest tests/test_add_horoshop_file.py -x` |
| Full suite | `./.venv/Scripts/python.exe -m pytest` (269+ tests must stay green) |

### Phase Requirements → Test Map
| Req | Behavior | Type | Automated command | File exists? |
|---|---|---|---|---|
| REQ-01 | picker lists unmatched, filters by supplier+brand, login_required | view | `pytest tests/test_views_add_horoshop.py -x` | ❌ Wave 0 |
| REQ-02 | builder emits all create columns incl. category, correct `[КАТАЛОГ]` headers, sheet `Worksheet` | unit | `pytest tests/test_add_horoshop_file.py -x` | ❌ Wave 0 |
| REQ-02 | price/oldprice for unmatched SP correct (flat / per_brand / clamp / UAH) | unit | `pytest tests/test_add_horoshop_file.py -k pricing -x` | ❌ Wave 0 |
| REQ-03 | every row has a category (analogy hit or fallback); threshold honored | unit | `pytest tests/test_category_resolver.py -x` | ❌ Wave 0 |
| REQ-04 | builder/query writes nothing to DB | unit | `pytest tests/test_add_horoshop_file.py -k readonly -x` | ❌ Wave 0 |
| REQ-06 | analogy sample over real data (evidence for Yana) | manual | run resolver script on LOCAL sqlite, table for Yana | n/a |

### Sampling Rate
- **Per task commit:** the new test file's quick run.
- **Per wave merge:** full suite.
- **Phase gate:** full suite green before `/gsd:verify-work`.

### Wave 0 Gaps
- [ ] `tests/test_add_horoshop_file.py` — builder shape, headers, pricing, availability, read-only (REQ-02/04)
- [ ] `tests/test_category_resolver.py` — analogy block+rank, fallback, threshold, source/confidence (REQ-03)
- [ ] `tests/test_views_add_horoshop.py` — picker GET + generate POST, login_required (REQ-01)
- [ ] Reuse existing `tests/conftest.py` fixtures (no new framework install needed)

## Project Constraints (from CLAUDE.md)

- **#13 Live-store guard / invariant #13:** any customer-visible change needs explicit go-ahead;
  Horoshop import is **Yana's hand + backup**. The app only produces the file — **no auto-import.**
- **#10 Testing safety guard:** prod-DB-wipe history; `TESTING=1` + prod URI → `RuntimeError`
  (`app/__init__.py:20-31`). Any sample run = LOCAL sqlite; abort on `rlwy|railway|postgres|psycopg`.
- **#11 Naming:** `PromProduct`/`prom_products` is legacy — **do not rename**; UI/comments say
  Horoshop.
- **#2 1pp↔1 active match + article footgun** (`catalog_import.py:231-237`): never add a field to
  `CATALOG_FIELDS` that the file might blank — relevant only if persistence is ever chosen (it isn't,
  Q6).
- **#12 Auto-discount formula** (`pricing.py` `calculate_auto_discount`) — used by `auto_margin`
  suppliers (MARESTO); honor it for unmatched `auto_margin` SPs.
- **п.1 Tests / п.3 read-first / K2 simplicity / K3 surgical:** mirror existing builders; add only
  what REQ needs; don't refactor working matcher gates.
- **Order of work:** finishing existing supplier pipelines precedes *new suppliers* — this phase adds
  a cross-supplier *file generator*, not a new supplier, so it's in scope.

## Sources

### Primary (HIGH — read from disk this session)
- `horoshop-export 20.05.26.xlsx` + `horoshop-export 13.05.26.xlsx` (openpyxl) — 59-col export schema;
  category = `Раздел` (col 8), visibility = `Отображать` (col 12).
- `.planning/plans/np-feed/canary-HKN-PICO12M.xlsx` — live-proven `[КАТАЛОГ] ` import dialect:
  `categories_uk`/`categories_ru`, `[КАТАЛОГ] Отображать`, sheet `Worksheet`.
- `horoshop-import-mini-5.xlsx` — bare-header update-file example.
- `app/services/np_horoshop_file.py` (261 ln) — builder template, proven headers, read-only query.
- `app/services/maresto_horoshop_file.py` (195 ln) — sibling builder; confirms `[КАТАЛОГ]` pattern,
  skip-no-artikul/no-price manifest, oldprice rule.
- `app/services/pricing.py` (324 ln) — all price/discount functions.
- `app/views/feed.py` (254 ln) — `/feeds/np` picker + generate flow.
- `app/services/catalog_import.py` — `COLUMN_ALIASES` (no category alias → category dropped).
- `app/models/catalog.py` — PromProduct has no category field.
- `app/models/supplier.py` — `discount_percent`, `pricing_mode`, `min_margin_uah`, `cost_rate`,
  `eur_rate_uah` verified.
- `app/models/supplier_brand_discount.py` — `brand`, `discount_percent`, `Supplier.brand_discounts`.
- `app/models/product_match.py` — `status` enum {candidate,confirmed,rejected,manual}, `published`,
  `uq_match_pair`.
- `app/models/supplier_product.py` — `article`, `price_cents`, `available`, `brand`, `images`,
  `description`, `is_deleted`, `ignored`, `needs_catalog_add`.
- `app/services/np_parser.py` — feed content lookup (desc_uk/desc_ru/photos).
- `app/services/kodaki_adapter.py` — confirmed: feed-format adapter, NOT a category map.
- `app/services/matcher.py` — thresholds + reusable primitive inventory.
- `.planning/RESEARCH-horoshop-availability-and-new-offers.md` — create requires SKU+Назва+Розділ.

### Secondary (MEDIUM)
- NVIDIA endpoint/model (memory `reference_nvidia_build_api`) — verify at wire time.

### Tertiary (LOW — needs validation / blocked)
- Live help.horoshop docs page — blocked by cyclic language redirect; required-fields rule taken from
  prior research.
- `Кодаки поставщик категории.xlsx` — corrupt (no sharedStrings), shape unknown.
- Canary `[КАТАЛОГ] Отображать` data-cell literal — read at plan time.

## Metadata

**Confidence breakdown:**
- Create schema / category+visibility headers: **HIGH** (read from disk). One empirical detail — which
  category header the importer keys on for a create — is **MEDIUM** (resolve via canary).
- Price path for unmatched SP: **HIGH** (pure functions + all model fields verified).
- Filter/query design: **HIGH** (direct inversion of verified NP queries; enum verified).
- Models/builders/adapters: **HIGH** (all read this session).
- Category-by-analogy: **MEDIUM** (sound + reuses primitives; quality needs the real-data sample).
- Kodaki prior-art reuse: **resolved NO** (adapter is feed-format; categories file corrupt).

**Research date:** 2026-05-30
**Valid until:** ~2026-06-29 (stable internal code). Re-verify the category import header empirically
before any live import; re-verify the NVIDIA endpoint/model if/when AI is enabled.
