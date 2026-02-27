---
status: diagnosed
trigger: "Investigate why the YML feed offers don't have a <url> element"
created: 2026-02-28T00:00:00Z
updated: 2026-02-28T00:00:00Z
---

## Current Focus

hypothesis: CONFIRMED — The <url> element was never implemented in either YML generator.
  The plan spec (03-02-PLAN.md) omitted <url> from the offer template, and the generators
  faithfully implemented what the plan specified.
test: Code audit of yml_generator.py, yml_test_generator.py, plan spec, research doc, and UAT report.
expecting: N/A — root cause confirmed.
next_action: Implement fix per recommendation below.

## Symptoms

expected: Each <offer> in the YML feed contains a <url> element (as required by prom.ua YML import format and as stated in UAT test 3).
actual: Offers only contain: name, price, currencyId, vendorCode. No <url> element.
errors: None (silent omission — generator runs successfully but produces incomplete XML).
reproduction: Call regenerate_yml_feed() or visit /feed/yml — inspect any <offer> element.
started: From initial implementation in commit 2d6b8bf (feat(03-02): add YML feed generator).

## Eliminated

- hypothesis: PromProduct model has a url column that is not being read.
  evidence: Inspected app/models/catalog.py in full. PromProduct has: id, external_id, name,
    brand, model, article, price, currency, imported_at. No url column exists.
  timestamp: 2026-02-28T00:00:00Z

- hypothesis: catalog_import.py strips a URL column during import.
  evidence: Inspected app/services/catalog_import.py in full. COLUMN_ALIASES maps
    Ukrainian/Russian headers to internal fields. No url/посилання/link mapping exists.
    The xlsx export (export-products-26-02-26_20-29-57.xlsx) would need to be checked for
    whether prom.ua actually exports a product URL column — but the absence of any url
    alias in the importer and the absence of any url column in the model confirms the
    data path never stored a URL.
  timestamp: 2026-02-28T00:00:00Z

- hypothesis: The <url> element exists in yml_test_generator.py but was accidentally dropped
    from yml_generator.py.
  evidence: Inspected both files. yml_test_generator.py (line 45-49) also has no <url>
    offer element. Both generators are consistent: neither emits a per-offer <url>.
    (The <shop><url> element is present in both, but that is the store URL, not a product URL.)
  timestamp: 2026-02-28T00:00:00Z

## Evidence

- timestamp: 2026-02-28T00:00:00Z
  checked: app/services/yml_generator.py lines 86-98
  found: offer element is built with: name, price, currencyId, vendorCode (conditional).
    No <url> SubElement call anywhere in the function.
  implication: The omission is unconditional — no code path produces a <url> element.

- timestamp: 2026-02-28T00:00:00Z
  checked: app/services/yml_test_generator.py lines 41-49
  found: offer element built identically: name, price, currencyId. No <url> element.
  implication: The gap is systemic across both generators, not a regression in one file.

- timestamp: 2026-02-28T00:00:00Z
  checked: app/models/catalog.py — PromProduct model definition
  found: Columns: id, external_id, name, brand, model, article, price, currency, imported_at.
    No url, page_url, or product_url column.
  implication: The URL cannot be sourced from the PromProduct record as the data
    was never imported or stored.

- timestamp: 2026-02-28T00:00:00Z
  checked: app/services/catalog_import.py — COLUMN_ALIASES dict
  found: Maps only: external_id, name, article, price, currency, brand.
    No url alias present. The prom.ua xlsx export may contain a product page URL
    column (e.g. "Посилання на сторінку товару") but it is not mapped or stored.
  implication: Even if the xlsx export contains a URL column, it is silently discarded
    during import and never reaches the database.

- timestamp: 2026-02-28T00:00:00Z
  checked: .planning/phases/03-pricing-engine-and-yml-output/03-02-PLAN.md — offer XML template
  found: The offer template in the plan spec (lines 194-200) shows:
    <offer id="{prom_product.external_id}" available="true|false">
        <name>...</name>
        <price>...</price>
        <currencyId>EUR</currencyId>
        <vendorCode>...</vendorCode>
    </offer>
    No <url> element in the plan spec.
  implication: The implementation correctly followed the plan. The plan itself was
    incomplete — it omitted <url> from the offer template.

- timestamp: 2026-02-28T00:00:00Z
  checked: .planning/phases/03-pricing-engine-and-yml-output/03-RESEARCH.md — "Complete YML
    Structure for prom.ua" code example (lines 261-288)
  found: The research doc's canonical YML example also has no <url> in the offer elements.
    The research doc lists: name, price, currencyId, vendorCode — and explicitly notes
    "No categoryId — we are updating existing products, not creating new ones."
    The <url> field was not mentioned in the offer fields list at all.
  implication: The gap originated in the research phase. The YML spec review did not
    flag <url> as a required per-offer field. The implementation faithfully followed the
    (incomplete) research output.

- timestamp: 2026-02-28T00:00:00Z
  checked: .planning/phases/03-pricing-engine-and-yml-output/03-UAT.md — Test 3 result
  found: Test 3 expected "Each offer has name, price, currencyId, url, and available attributes."
    Result: issue. Reported: "offer не содержит элемент <url> — есть только name, price,
    currencyId и available."
  implication: The UAT independently confirmed the bug. The severity is marked "minor"
    but this depends on whether prom.ua requires <url> for a valid import — if it does,
    the feed will be rejected or produce unexpected results on import.

- timestamp: 2026-02-28T00:00:00Z
  checked: .planning/phases/03-pricing-engine-and-yml-output/03-CONTEXT.md — YML feed content
    decisions
  found: "Minimal fields: name, price, availability status" — the original design decision
    described a minimal field set that did not enumerate <url>.
  implication: The user's own design decision at context-gathering time said "minimal fields"
    without mentioning <url>. However, prom.ua import format requires <url> as a standard
    YML offer field. The design decision was made without consulting the full prom.ua YML spec.

## Resolution

root_cause: |
  The <url> element is absent from YML offers because:

  1. The PromProduct model has no url column — prom.ua product page URLs were never
     imported or stored. The catalog_import.py COLUMN_ALIASES dict does not map any
     URL column from the prom.ua xlsx export.

  2. The plan spec (03-02-PLAN.md) and research doc (03-RESEARCH.md) both omitted <url>
     from the offer template. The implementation faithfully followed the plan.

  3. The root origin is the research/design phase: the CONTEXT.md "minimal fields"
     decision (name, price, availability) did not include <url>, and the research
     did not flag it as required despite the prom.ua YML format treating it as standard.

  The gap is a design omission, not a coding error. The code is correct per its spec.

fix: |
  Two-part fix required:

  PART 1 — Store product URLs in the database:
  - Add `page_url` column (String, nullable) to PromProduct model.
  - Add migration: ALTER TABLE prom_products ADD COLUMN page_url VARCHAR(500).
  - Add "посилання_на_сторінку_товару" (Ukrainian) and "ссылка_на_страницу_товара"
    (Russian) to COLUMN_ALIASES in catalog_import.py mapping to "page_url".
  - Update save_catalog_products() to persist the page_url field.
  - Re-import the prom.ua catalog xlsx to populate URLs for existing products.

  PART 2 — Emit <url> in offer elements:
  - In app/services/yml_generator.py, after the <name> element, add:
      if pp.page_url:
          etree.SubElement(offer, "url").text = pp.page_url
  - Apply the same change to app/services/yml_test_generator.py for consistency.

  FALLBACK (if prom.ua export does not include a URL column):
  - If the xlsx export has no URL column, the URL must be constructed from the
    product's external_id. Check the actual prom.ua export file headers to confirm
    whether a URL column exists before implementing Part 1.
  - Construction pattern: https://labresta.prom.ua/p{external_id}.html
    (verify this URL pattern against actual prom.ua product pages first).

verification: |
  After fix:
  1. Import a fresh prom.ua catalog xlsx — confirm page_url is populated in the DB.
  2. Run regenerate_yml_feed() — inspect output XML for <url> elements inside <offer>.
  3. Validate the feed URLs resolve to real product pages on prom.ua.
  4. Confirm prom.ua import accepts the feed without errors.

files_changed:
  - app/models/catalog.py (add page_url column)
  - app/services/catalog_import.py (add url column alias)
  - app/services/yml_generator.py (emit <url> element)
  - app/services/yml_test_generator.py (emit <url> element for consistency)
  - migrations: new migration for page_url column
