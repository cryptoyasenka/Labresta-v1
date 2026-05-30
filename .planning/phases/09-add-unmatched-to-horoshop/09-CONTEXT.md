# Phase 9: Add unmatched supplier products to Horoshop (new-card create file) — Context

**Gathered:** 2026-05-30 (ночной режим, discuss-phase by Claude on Yana's 3 decisions)
**Status:** Ready for research → planning
**Branch:** `feat/horoshop-add-unmatched`

> Origin: Yana — «добавить возможность выбрать товары в матчере на которые нету матча у
> поставщика и создать файл для их добавления в хорошоп. Тут нужно всё: название, цена, скидка,
> наличие, описание, фото. Подумай что нужно. Пройдись через GSD в ночном режиме.»
> This file is the discuss artifact. It captures scope, Yana's decisions, the hard open problem
> (category), and hands a fact-grounded brief to research → plan → execute → verify.

<domain>
## Phase Boundary

Build, in `labresta-sync`, the ability to **select supplier products that have NO Horoshop card
(no confirmed/manual match)** and **generate a native-Horoshop XLSX that CREATES them as new cards**.
The create-file must carry EVERYTHING a new card needs:
- **название** (name, UA; RU where the source has it)
- **цена** (selling price = retail × brand discount, via existing pricing)
- **скидка** (old price when discounted — Horoshop shows strike-through)
- **наличие** (availability)
- **описание** (description UA; RU from feed where present)
- **фото** (gallery)
- **Артикул** (SKU = create key)
- **бренд**, **видимость** (visibility)
- **категория (Розділ)** — REQUIRED by Horoshop to create a card (see open problem ↓)

**In scope (Phase 1 — core, build autonomously):**
- A selection page (filters: supplier + brand, + checkboxes) listing unmatched products, mirroring
  the `/feeds/np` picker pattern.
- A create-file builder (mirror `np_horoshop_file.py`) emitting the native [КАТАЛОГ] XLSX for the
  ticked products, with all content fields above.
- RU description from the supplier feed where it exists (NP feed carries `description_ru`).
- Tests (unit, mirroring existing `test_np_*`), read-only over DB.

**In scope (Phase 2 — category, RESEARCH + PROPOSE, do NOT wire AI blindly):**
- Resolve each new product's **Розділ** "по принципу аналогичных позиций" (by analogy with similar
  existing Horoshop cards).
- Build + TEST the **analogy baseline** (data-driven, no AI) and a **safe fallback** (holding
  category). Research + PROPOSE the **AI option** (NVIDIA free API) with a concrete design — leave
  the "which strategy / wire it in" call to Yana ("надо подумать как правильно сделать").

**Out of scope:**
- Any actual import into the live store — that stays **Yana's hand + backup** (invariant #13,
  feedback_labresta_live_import). We only PRODUCE the file.
- Automatic matching of these products (separate effort — ~205 NP items are simply never-matched).
- Touching the binary YML availability mechanism (settled separately; MARESTO parked awaiting
  Horoshop support).
- Adding a persistent `category` column to PromProduct unless research proves it's the cleanest path
  (prefer generate-time read of the export, mirroring how NP content is joined at generate-time).

</domain>

<decisions>
## Yana's decisions (AskUserQuestion, 2026-05-30) — LOCKED

### D1 — Selection UX = filters + checkboxes
A page listing unmatched products with **filters (supplier + brand)** and **checkboxes**, like the
existing `/feeds/np`. Operator ticks rows (or whole brand), clicks generate, gets the XLSX.

### D2 — RU fields from the feed where present
«А в НП фиде разве нету ру перевода? если есть — оттудова нужно взять.» → take RU from the supplier
feed where it exists. The NP feed already carries **RU description** (`np_parser` reads col Q →
`description_ru`). Generalize: RU description from feed if available; NP = `description_ru`.
RU **name** is generally absent (NP feed maps no name column) → name_ru optional / blank where absent.

### D3 — Category (Розділ) by analogy — the HARD problem, research-led
«Нужно чтобы они садились в ПРАВИЛЬНУЮ категорию в хорошопе по принципу аналогичных позиций — это
более сложная задача, может есть смысл подключить АИ по апи в матчер — надо подумать как правильно
сделать.» → New cards must land in the CORRECT category by analogy with similar existing positions.
Possibly connect an AI API into the matcher. **This is the undecided part: research + propose,
do NOT build AI blindly.** Decision rule for the night: build core; build+test the non-AI analogy
baseline + safe fallback; design the AI option and present it for Yana's call.

## Claude's derived decisions (open to revision by research/plan)
- **Feature branch** `feat/horoshop-add-unmatched`; all night work here, Yana reviews + merges.
- **Mirror, don't reinvent:** the builder mirrors `np_horoshop_file.py`; the UI mirrors `/feeds/np`.
- **Generalize across suppliers** via the supplier+brand filter (not NP-only), since "unmatched"
  spans all suppliers; NP is just the supplier with a rich content feed.
- **Category as a pluggable resolver** (strategy interface): `analogy` (baseline) → `fallback`
  (holding category) now; `ai` (NVIDIA) as a future plug Yana enables.

</decisions>

<specifics>
## Facts grounded this session (read from code, not memory)

### Horoshop create-file schema (triangulated)
- **Create REQUIRES: SKU (Артикул) + Назва + Розділ (category).** Source: prior research
  `.planning/RESEARCH-horoshop-availability-and-new-offers.md` (from help.horoshop.ua) — "Required
  fields for a NEW product: SKU + Title (Назва) + Category (Розділ). Matching key = SKU."
- Import modal distinguishes New (Import / Do not import) vs Existing (Update / Do not update) — so a
  create-file is a normal native import with "New products: Import".
- **The canonical native column names live on disk:** `horoshop-export*.xlsx`
  (`horoshop-export-extended.xlsx`, `horoshop-export 20.05.26.xlsx`, etc.) — their header row IS the
  schema, INCLUDING the category column and the visibility column. Research must read these headers
  to nail exact strings (e.g. is it `Розділ` / `[КАТАЛОГ] Розділ` / `Категорія`; visibility header).
- Update-file proven mapping (from `np_horoshop_file.py`): bare `Артикул` (key) + `[КАТАЛОГ] <leaf>`
  columns (`Цена`, `Старая цена`, `Валюта`, `Наличие`, `Галерея`, `Описание товара (UA)`,
  `Описание товара (RU)`), sheet "Worksheet", `Наличие` ∈ {«В наличии», «Нет в наличии»}.

### Category data EXISTS but is dropped on import
- `PromProduct` (in `app/models/catalog.py`, NOT `prom_product.py`) has **NO category field**.
  Columns: external_id, name, name_ru, brand, model, article, display_article, price, currency,
  page_url, image_url, images, description_ua, description_ru, operator_decision.
- `catalog_import.py` `COLUMN_ALIASES` maps Horoshop export headers (артикул→external_id,
  назва (ua)→name, ціна→price, фото→image_url, галерея→images, опис товару (ua)→description_ua, …)
  but **has NO category alias** → the export's category column is read but discarded.
  **⇒ Every existing card's category is recoverable from the Horoshop export file on disk.**
- Prior art: `Кодаки поставщик категории.xlsx` + `app/services/kodaki_adapter.py` (supplier→category
  mapping) — research should check if reusable.

### Data sources for the create-file (per product)
- `SupplierProduct` (`app/models/supplier_product.py`): name (UA), brand, article (=vendorCode),
  price_cents, currency, available, stock_status, description (UA), image_url, images (JSON), params
  (JSON), is_deleted, ignored.
- NP rich content (desc_ua / **desc_ru** / photos / brand) comes from a SEPARATE NP feed via
  `np_parser.parse_np_feed(path)` keyed by article — NP `SupplierProduct.description` may be empty,
  so for NP take description (UA+RU) + photos from the feed. NP feed maps NO name column.
- Pricing: `app/services/pricing.py:compute_match_pricing` + brand discounts (retail × discount →
  selling; oldprice = retail when discounted). NOTE: pricing helpers are match-centric — for an
  UNMATCHED product there is no ProductMatch, so research/plan must confirm the price path for a
  bare SupplierProduct (likely supplier.discount_percent + sp.price_cents directly).

### "No match" definition (verified earlier this session)
- `ProductMatch.status` ∈ {candidate, confirmed, rejected, manual}; `published` default True.
- **Unmatched = no ProductMatch with status in {confirmed, manual}.** (A candidate/rejected match
  still means "no live card linked".) Earlier audit: 205 NP items across the 9 brands are
  SP_NO_MATCH.
- Existing related flag: `mark_new` (`/matches/mark-new/<sp_id>`, audit «Позначено для додавання»)
  already marks SPs "to add" — research should decide whether the new picker reuses/sets it.

</specifics>

<code_context>
## Reusable assets (mirror these — do not rewrite from scratch)

- **`app/services/np_horoshop_file.py`** (261 lines) — native-schema XLSX builder: proven [КАТАЛОГ]
  headers, `_shape_rows()`, `_workbook_bytes()`, read-only `_query_*`, manifest with per-brand
  counts. THE template for the create-file builder.
- **`app/services/maresto_horoshop_file.py`** — sibling builder (price + «Наличие» status column).
- **`app/views/feed.py`** — `/feeds/np` picker: `NP_BRANDS`, `_np_brand_match_counts`,
  `np_file_page` (GET picker), `np_file_generate` (POST → fetch feed → temp → build → send_file →
  log_action). THE template for the selection page + generate route. `@login_required`.
- **`app/services/np_parser.py`** — content lookup `article → {brand, description, description_ru,
  photos}` (sheet "Worksheet", fixed columns, header sanity-check). Extend/reuse for feed content.
- **`app/services/catalog_import.py`** — Horoshop export parser + `COLUMN_ALIASES` (where to add a
  category alias if research chooses the persist path; or read header positions for generate-time).
- **`app/services/matcher.py`** — fuzzy similarity (type gate, model boost, token_sort_ratio). Reuse
  its similarity to find "analogous" existing cards for category-by-analogy.
- **`app/services/pricing.py`** — `compute_match_pricing`, effective discount, oldprice logic.
- **`app/services/feed_fetcher.py`** — `fetch_feed_with_retry` (SSRF-guarded) for live feed pull.

## Tests / run
- `./.venv/Scripts/python.exe -m pytest` (NOT `uv run`). Mirror `tests/test_np_*`.
- Local sqlite only for any script; HARD-GUARD against prod DB (see
  `scripts/generate_maresto_availability.py`: abort if url not local sqlite / contains
  rlwy|railway|postgres|psycopg). feedback_labresta_no_benchmark_against_prod.

## Sample files on disk (research reads headers from these)
- `horoshop-export-extended.xlsx`, `horoshop-export 20.05.26.xlsx`, `horoshop-export 13.05.26.xlsx`
  — native export = canonical schema incl. category + visibility columns.
- `horoshop-import-mini-5.xlsx`, `.planning/plans/np-feed/canary-HKN-PICO12M.xlsx` — proven import
  format examples.
- `Кодаки поставщик категории.xlsx` — supplier→category prior art.

</code_context>

<open_problem_category>
## THE hard problem — Розділ assignment (Yana's D3, decide-after-research)

Horoshop REQUIRES a category to create a card, but our DB stores none and supplier feeds don't carry
a Horoshop category. So the create-file MUST attach a Розділ per row. Options to research, prototype,
compare, and PRESENT (do not silently pick the AI path):

1. **Analogy baseline (no AI, preferred default to BUILD + TEST):**
   read category-per-card from the Horoshop export on disk → for each new product, find the most
   similar existing card(s) (reuse `matcher.py` similarity on brand + name/article) → copy their
   category; attach a confidence. "Test the theory": run it over a real sample of unmatched products
   and report how sane the assigned categories look (evidence for Yana).
2. **Safe fallback:** a single holding category (e.g. «Новые товары / на разбор») for low-confidence
   / no-analogy rows, so every card still gets created and Yana re-sorts in admin. Lowest risk.
3. **AI option (RESEARCH + PROPOSE only — Yana decides):** NVIDIA free API
   (build.nvidia.com, 40 RPM, OpenAI-compat `integrate.api.nvidia.com/v1`, see
   reference_nvidia_build_api) classifies a product into the existing Horoshop category tree (give
   the model the tree + product name/desc). Design it, cost/quality/latency trade-offs, where it
   plugs (a `category_resolver` strategy), but DO NOT make it the default without Yana's go-ahead.

**Deliverable for Yana:** a short comparison (analogy vs fallback vs AI vs hybrid) + the analogy
results on real data, so she makes the call. Build core + analogy baseline + fallback; gate AI.

</open_problem_category>

<success_criteria>
## Phase success criteria
1. A logged-in operator can open a page, filter unmatched products by supplier + brand, tick rows,
   and download a native-Horoshop XLSX.
2. The XLSX, on a "New products: Import" run, would create cards carrying name, price, discount
   (old price), availability, description (UA + RU where the feed has it), photos, Артикул, brand,
   visibility, and a Розділ for every row.
3. Every row has a category (analogy where confident, fallback otherwise) — no row missing the
   REQUIRED Розділ.
4. Builder is read-only over the DB; no live import is performed by the app (Yana's hand + backup).
5. Tests pass (`./.venv/Scripts/python.exe -m pytest`), mirroring existing builder tests.
6. A written category proposal (analogy vs AI vs hybrid) + real-data evidence is left for Yana's
   decision; AI is not wired as default without her go-ahead.

</success_criteria>

<deferred>
## Deferred / Yana-decision items
- Final category strategy (analogy-only vs +AI vs hybrid) and AI enablement — Yana decides post-proposal.
- Persisting category in PromProduct (schema migration) vs generate-time read of export — research recommends.
- Auto-matching the ~205 never-matched NP products — separate effort.
- Whether the picker should set/honor the existing `mark_new` flag.

</deferred>

---
*Phase: 09-add-unmatched-to-horoshop · Context gathered 2026-05-30 (autonomous discuss).*
