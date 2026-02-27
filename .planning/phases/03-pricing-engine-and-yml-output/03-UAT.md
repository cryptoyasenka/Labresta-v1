---
status: complete
phase: 03-pricing-engine-and-yml-output
source: 03-01-SUMMARY.md, 03-02-SUMMARY.md
started: 2026-02-28T12:00:00Z
updated: 2026-02-28T12:30:00Z
---

## Current Test

[testing complete]

## Tests

### 1. Pricing Unit Tests Pass
expected: Run `pytest tests/test_pricing.py` — all 14 tests pass with no failures or errors.
result: pass

### 2. YML Feed Endpoint Accessible
expected: Start the app and visit /feed/yml in browser. Page returns XML content (not a 404 or error). No login/auth required.
result: pass

### 3. YML Feed Contains Product Offers
expected: The XML at /feed/yml has a `<shop>` root with `<offers>` containing `<offer>` elements. Each offer has name, price, currencyId, url, and available attributes.
result: issue
reported: "offer не содержит элемент <url> — есть только name, price, currencyId и available"
severity: minor

### 4. Product Prices Reflect Discount and Rounding
expected: Offer prices in the YML feed are whole numbers (no decimals). If a supplier discount is configured, prices are reduced accordingly.
result: issue
reported: "Цена в фиде 108 EUR вместо ~1070 EUR. Причина — сматчен не тот товар поставщика (Противень Unox TG935 за 135 EUR вместо печи Unox XFT133 за 1073 EUR). Проблема матчинга фазы 2, не ценообразования."
severity: major

### 5. Out-of-Stock Products Marked Unavailable
expected: Products that are out of stock or have zero/invalid price show `available="false"` in the YML feed.
result: pass

### 6. YML Regenerates After Sync
expected: Run a sync. After sync completes, the YML file is updated. The sync log shows Stage 6/6 YML regeneration.
result: pass

## Summary

total: 6
passed: 4
issues: 2
pending: 0
skipped: 0

## Gaps

- truth: "Each offer in YML feed contains <url> element"
  status: failed
  reason: "User reported: offer не содержит элемент <url> — есть только name, price, currencyId и available"
  severity: minor
  test: 3
  root_cause: ""
  artifacts: []
  missing: []
  debug_session: ""

- truth: "Product prices in YML feed match expected pricing from supplier catalog"
  status: failed
  reason: "User reported: Цена в фиде 108 EUR вместо ~1070 EUR. Сматчен не тот товар поставщика (Противень Unox TG935 за 135 EUR вместо печи Unox XFT133 за 1073 EUR). Проблема матчинга фазы 2."
  severity: major
  test: 4
  root_cause: ""
  artifacts: []
  missing: []
  debug_session: ""
