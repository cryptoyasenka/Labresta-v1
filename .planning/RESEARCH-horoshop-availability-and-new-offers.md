# Research — Horoshop availability statuses + new-offer card creation

**Date:** 2026-05-29 (ночной режим, autonomous prep).
**Purpose:** Pre-answer the two open questions that block the deferred backlog features
**MARESTO 4-value stock status** and **Phase G (auto «+Horoshop»)** — so that
`/gsd:discuss-phase` can start with facts, not guesses. **This is research, NOT a locked
plan.** Scoping/decisions belong to discuss-phase with Yana.

Sources (Horoshop help center — help.horoshop.ua; the platform's international engine brand
renders as "Cartum" on these pages, same product):
- Availability statuses: https://help.horoshop.ua/en/articles/5723914-availability-statuses-and-stock-accounting
- Import from file: https://help.horoshop.ua/en/articles/1684865-importing-products-from-a-file

---

## Q1 — Does Horoshop support more than binary available/not-available? (blocks MARESTO stock)

**YES.** Horoshop is not limited to the binary `available="true|false"` our YML emits today.

- **3 default statuses**, each with an action:
  - **In stock** — ordering allowed
  - **Out of stock** — waiting-list signup
  - **Coming soon** (= очікується / під замовлення equivalent) — waiting-list signup
- **Custom statuses** can be created (contact Horoshop support to wire the action).
- On import, status is set via a field matched to the system value **«Наявність» (Catalog: Availability)**.
- Key quote: *"if the import file contains other values besides the standard availability
  statuses, they will be created as new statuses, but without an action assigned."*
  → arbitrary status strings (e.g. «Під замовлення») can be pushed; Horoshop auto-creates the
  status, but its storefront *action* must be configured once in admin.

### Mapping MARESTO `<stock>` → Horoshop (proposed, for discuss-phase)
MARESTO XML `<stock>` has 4 values (counts were point-in-time at 2026-04-15 planning, will drift):
| MARESTO `<stock>` | meaning | proposed Horoshop status | orderable? |
|---|---|---|---|
| In stock | в наличии | In stock | yes |
| Running low | заканчивается | In stock (or custom «Закінчується») | yes |
| Reserved | ожидается / под заказ | **Coming soon** (or custom «Під замовлення») | waiting-list |
| Out of stock | нет | Out of stock | waiting-list |

### ⚠️ Critical design nuance — YML vs XLSX path
The docs describe the multi-status mechanism for the **tabular (XLS/XLSX)** import («Наявність»
column). For **YML**, the standard `<offer available="true|false">` attribute is **binary** —
the docs do NOT confirm a YML tag that carries a named availability status.
**Two viable routes — needs an empirical mini-test (per "test integrations empirically"):**
1. **Reuse the XLSX path we already built.** The НП file-generator (`app/services/np_horoshop_file.py`,
   shipped 2026-05-29) already emits a native Horoshop **XLSX with a «Наявність» column**. A MARESTO
   stock-status push could reuse that exact mechanism (text «Наявність» column, 4 values) instead of
   fighting the binary YML attribute. **This is the lower-risk route.**
2. Try a YML `<param name="Наявність">Під замовлення</param>` (or similar) and verify with a
   minimal real import whether Horoshop reads it into the «Наявність» field. Unconfirmed — must test.

**Recommendation for discuss-phase:** lean route 1 (XLSX «Наявність» column, reusing np_horoshop_file
infrastructure) unless a 1-row YML-param test proves route 2 works.

---

## Q2 — Can import CREATE new product cards from new offers? (blocks Phase G)

**YES.** Import creates brand-new cards, not just updates.

- **Required fields for a NEW product:** **SKU** (unique id) + **Title (Назва)** + **Category (Розділ)**.
- **Matching key:** SKU/article (= our `pp.external_id` / Horoshop artikul = old Prom ID).
- **Import action settings (modal):**
  - New products (in file, not on site) → **Import / Do not import**
  - Existing products (in file and on site) → Update / Do not update
  - Out-of-stock (on site, absent from file) → No action / Hide / Change availability status
- Availability on import set via the «Наявність» field **or** «Кількість» (quantity) if stock-tracking on.

### Implication for Phase G (for discuss-phase)
The existing `mark_new` flag (`/matches/mark-new/<sp_id>`, audit label «Позначено для додавання»)
already marks supplier products as "to add". The missing piece is a **new-offers export file**
(YML or XLSX) containing, per flagged SP: **SKU + Назва + Розділ** (+ price + availability), which
Yana imports with "New products: Import". Open sub-question for Yana: what **Розділ (category)** does
a freshly-added SP map to? — SP feeds may not carry a Horoshop category, so category assignment
(default catch-all category vs. per-supplier mapping vs. manual) is the real design decision.

---

## Net effect on the backlog
Both features are now **unblocked at the research level**. Remaining before code:
1. `/gsd:discuss-phase` for each (they are >1h features — CLAUDE.md п.2 forbids code first).
2. One empirical 1-row import test to confirm the availability mechanism (route 1 vs 2 above).
3. Yana decisions: (a) custom status «Під замовлення» action in Horoshop admin; (b) category
   assignment policy for new-offer cards.

Live-store rule still applies: any real import is Yana's hand, with go-ahead
(see feedback_labresta_live_import).
