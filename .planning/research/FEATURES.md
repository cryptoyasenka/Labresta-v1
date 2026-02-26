# Feature Research

**Domain:** Supplier XML/YML feed sync tool for Ukrainian marketplaces (prom.ua / Horoshop)
**Researched:** 2026-02-26
**Confidence:** MEDIUM (network access unavailable; findings based on training data + project context analysis; key claims flagged)

---

## Feature Landscape

### Table Stakes (Users Expect These)

Features the operator of a sync tool assumes exist. Missing these = tool is not usable.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| YML feed ingestion from URL | Core function — supplier feed must be fetched by URL | LOW | HTTP GET + XML parse. prom.ua suppliers publish standard Yandex YML format. Confidence: HIGH |
| Scheduled feed refresh | Prices change daily; stale data defeats the purpose | LOW | Cron or interval-based scheduler. prom.ua re-imports every 4h, so refresh must be at most 4h | Confidence: HIGH |
| Generated YML output at stable URL | prom.ua reads YML from a URL on a schedule — this IS the integration mechanism | MEDIUM | Must be publicly accessible, stable URL. Confidence: HIGH |
| Price field in output YML | prom.ua import maps "price" field — required for price sync | LOW | Direct from supplier after markup calculation. Confidence: HIGH |
| Availability / stock field in output | prom.ua maps "available" field — required for in/out-of-stock sync | LOW | Map supplier availability signal to prom.ua's boolean "available". Confidence: HIGH |
| Product matching UI | 6,100+ products, no article codes — operator must review and confirm matches | HIGH | Most complex part of the system. See differentiators for fuzzy-match assist. Confidence: HIGH |
| Confirmed mapping persistence | Matches must survive feed refresh cycles | LOW | DB table: supplier_product_id ↔ store_product_id. Confidence: HIGH |
| Supplier management (CRUD) | Multiple suppliers with different URLs, discount rules | LOW | Simple admin form: URL, name, discount %, enabled toggle. Confidence: HIGH |
| Per-supplier discount/markup rule | Each supplier has different wholesale margin to apply | LOW | final_price = supplier_price * (1 - discount%). Confidence: HIGH |
| Sync status dashboard | Operator needs to verify the tool is running correctly | MEDIUM | Last sync time, match counts, error count, output feed freshness. Confidence: HIGH |
| Error visibility / basic logging | Feed fetch failures, parse errors must be visible — not silent | MEDIUM | Structured log per sync run: timestamp, supplier, items processed, errors. Confidence: HIGH |
| Handling of discontinued products | Items in prom.ua store but absent from supplier feed — must not silently zero out | MEDIUM | Configurable behavior: keep last known, mark unavailable, or flag for review. Confidence: HIGH |

---

### Differentiators (Competitive Advantage)

Features that distinguish this tool from a naive cron+script approach or generic feed tools. Aligned with the core challenge: fuzzy matching at scale.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Fuzzy match candidate suggestions | Brand + model extraction from freeform names; ranks likely matches rather than dumping raw lists | HIGH | Core IP of this tool. Levenshtein / token-based similarity on normalized names. Without this, operator manually reviews 6,100 rows. Confidence: MEDIUM (algorithm design is custom) |
| Normalized name tokens for matching | Pre-process supplier names and store names into comparable tokens (strip stopwords, normalize Cyrillic/Latin, extract brand + model number) | HIGH | Key to reducing false-positive matches. "стол холодильний 3 двері" vs "холодильний стол трьохдверний" → same brand+model extracted. Confidence: HIGH |
| Confidence score display per match | Show operator how confident the auto-match is (high/medium/low) before confirming | MEDIUM | Threshold-based auto-confirm for HIGH confidence matches; manual review queue for MEDIUM/LOW | Confidence: MEDIUM |
| Bulk match confirmation | Review and confirm/reject multiple candidate matches in one session | MEDIUM | Table with checkboxes + batch confirm/reject. Saves hours vs row-by-row. Confidence: HIGH |
| "Changed since last sync" log | Show operator exactly which prices/availability changed in last run | MEDIUM | Diff against previous snapshot. Reduces anxiety: "did it actually update?" | Confidence: HIGH |
| Unmapped product queue | Dedicated view: supplier items with no confirmed match, sorted by similarity score | MEDIUM | Operator can prioritize which unmatched items to resolve first. Confidence: HIGH |
| Manual override mapping | Operator can force-link any supplier item to any store product, bypassing fuzzy logic | LOW | Critical escape hatch — needed when names differ too much. Confidence: HIGH |
| Per-supplier field mapping config | Each supplier's YML may use different field names or conventions | MEDIUM | Config: which XPath/field is "price", "availability", "brand", "model". Rozetka vs prom.ua supplier feeds differ. Confidence: MEDIUM |
| Feed output field selection | Control which fields go into the output YML (price only? price + availability? + name?) | LOW | prom.ua import lets you choose which fields to update; tool should match that. Confidence: HIGH |
| Staleness alerting | Notify if a supplier feed hasn't refreshed in N hours (supplier-side outage) | LOW | Simple threshold check: if last_fetched_at > threshold, flag in dashboard. Confidence: HIGH |

---

### Anti-Features (Commonly Requested, Often Problematic)

Features that seem natural to request but create disproportionate complexity or risk for v1.

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| Auto-add new supplier products to prom.ua catalog | "Why not import everything automatically?" | Creates unreviewed products in live store; product data quality (descriptions, categories, images) requires human judgment; prom.ua has moderation. PROJECT.md explicitly excludes this. | Keep new products in "unmatched" queue; operator adds to store manually then matches |
| Direct prom.ua API writes (price updates via API) | Faster than waiting 4h for YML re-import | API coupling locks tool to prom.ua; breaks Horoshop migration goal; API has rate limits and auth complexity; YML approach is explicitly chosen. | YML file output — platform-agnostic, explicitly chosen in PROJECT.md |
| Real-time price sync (sub-minute) | "I want instant price updates" | Supplier feeds don't update in real-time; prom.ua re-imports on 4h cycle anyway; polling faster than 1h is waste and may hit supplier rate limits | 1-4h schedule is sufficient for the use case |
| Auto-resolve fuzzy match conflicts | "Let AI decide uncertain matches automatically" | False positives at scale corrupt live product data; a 95%-confident wrong match updates wrong product's price | Always require human confirmation for medium/low confidence; only auto-confirm HIGH confidence |
| Multi-store / multi-account support | Seems like natural growth path | Adds multi-tenancy complexity (data isolation, auth, billing) before core is validated; this is a single-store internal tool | Single-store only for v1; if needed, run separate instances |
| Historical price analytics / charts | "Show me price trends" | Data warehousing, charting library, retention policy — none of this adds sync value | Keep a simple change log (what changed in last N syncs); full analytics is a separate product |
| Automatic image sync from supplier | Suppliers have images in YML | Image handling (download, store, serve, dedup) is a separate complexity domain; prom.ua has its own image hosting | Sync price + availability only; images managed manually |
| Bulk product rename / description sync | Supplier names might be "better" | Overwrites carefully curated store product data; catastrophic if wrong | Only sync price and availability; name/description edits are manual |

---

## Feature Dependencies

```
[Supplier Management (CRUD)]
    └──required by──> [Feed Ingestion Scheduler]
                          └──required by──> [Price Calculation Engine]
                                                └──required by──> [YML Output Generator]
                                                                      └──required by──> [prom.ua auto-import]

[Feed Ingestion Scheduler]
    └──required by──> [Sync Log / Change Diff]

[Store Product Catalog (imported/cached from prom.ua export)]
    └──required by──> [Fuzzy Match Candidate Engine]
                          └──required by──> [Matching UI]
                                                └──required by──> [Confirmed Mapping Store]
                                                                      └──required by──> [YML Output Generator]

[Confirmed Mapping Store]
    └──required by──> [Unmapped Product Queue]
    └──required by──> [Discontinued Product Handler]

[Fuzzy Match Candidate Engine]
    └──enhances──> [Manual Override Mapping]

[Sync Log]
    └──enhances──> [Staleness Alerting]
    └──enhances──> [Dashboard]
```

### Dependency Notes

- **YML Output requires Confirmed Mapping Store:** The output feed can only include products with a confirmed supplier↔store link. Without mappings, there's nothing to output.
- **Fuzzy Match Engine requires Store Catalog:** Matching candidates against prom.ua products requires a local copy of the store's product list (name, brand, model). This is a one-time import (from prom.ua export CSV or API) that must happen before any matching work begins.
- **Scheduler requires Supplier Management:** You cannot run scheduled fetches until at least one supplier with a valid URL is configured.
- **Change Diff requires previous snapshot:** The "changed since last sync" log requires storing the previous sync's price/availability values to compute a diff.
- **YML Output requires Price Calculation Engine:** Raw supplier prices must be transformed by the per-supplier discount rule before output.
- **Manual Override enhances Fuzzy Match:** The override is the fallback when the fuzzy engine produces no acceptable candidates; both feed the same Confirmed Mapping Store.

---

## MVP Definition

### Launch With (v1)

Minimum required to replace the current manual process and validate the core value proposition.

- [ ] **Supplier CRUD** — Add/edit/disable suppliers with URL and discount %. Required before anything else.
- [ ] **Feed ingestion + YML parse** — Fetch supplier YML, extract product id, name, price, availability. Core pipe.
- [ ] **Scheduled fetch** — Cron at 1h or 2h interval. Without this it's manual-only.
- [ ] **Store catalog import** — One-time import of prom.ua product list (CSV or manual paste) to enable matching. The fuzzy engine needs something to match against.
- [ ] **Fuzzy match candidates** — Auto-propose match candidates from store catalog for each supplier product (brand + model token similarity). The key differentiator — without this, mapping 150 products is tedious; with 5 suppliers it's impossible.
- [ ] **Matching UI: review + confirm/reject** — Web UI to review candidates, confirm or reject, manual override. The operator's primary daily-use screen.
- [ ] **Confirmed mapping store** — DB table persisting supplier_item ↔ store_product links.
- [ ] **Price calculation engine** — Apply per-supplier discount to supplier price.
- [ ] **YML output generation** — Produce valid prom.ua-compatible YML at a stable URL.
- [ ] **Sync log (basic)** — Last sync time, count of matched/unmatched, fetch errors. Minimum dashboard needed to know if it's working.
- [ ] **Discontinued product handler** — When a supplier item disappears from feed: mark as unavailable in output YML (not silently remove). Prevents ghost listings.

### Add After Validation (v1.x)

Once the core sync → match → output loop is proven with MARESTO:

- [ ] **Second supplier onboarding** — Validates that per-supplier config generalizes. Add once first supplier is fully matched.
- [ ] **Change diff log** — "What changed in last sync" view. Add when operator asks "did it actually update prices?"
- [ ] **Bulk match confirmation** — Add once the per-row review becomes tedious at scale (second supplier).
- [ ] **Confidence score display** — Add when operator wants to know which matches to trust vs verify.
- [ ] **Staleness alerting** — Add when supplier feeds have been unreliable.
- [ ] **Per-supplier field mapping config** — Add when second supplier has a different YML structure.

### Future Consideration (v2+)

Defer until product-market fit with current single store:

- [ ] **Horoshop output format** — YML is compatible now; Horoshop-specific fields (if any differ) only when migration is imminent.
- [ ] **Email / webhook alerts on sync errors** — Nice-to-have; dashboard check is sufficient initially.
- [ ] **Price floor / ceiling rules** — Per-product price guards to prevent margin-destroying updates. Only needed when pricing strategy becomes complex.
- [ ] **Multi-supplier conflict resolution** — When two suppliers match the same store product, which price wins? Only needed with 3+ active suppliers on overlapping SKUs.
- [ ] **Audit trail / price history** — Full history of every price change per product. Storage cost vs value tradeoff; add when requested.

---

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| Feed ingestion + YML parse | HIGH | LOW | P1 |
| Store catalog import (one-time) | HIGH | LOW | P1 |
| Supplier CRUD | HIGH | LOW | P1 |
| Scheduled fetch | HIGH | LOW | P1 |
| Price calculation (discount rule) | HIGH | LOW | P1 |
| YML output at stable URL | HIGH | LOW | P1 |
| Confirmed mapping store | HIGH | LOW | P1 |
| Fuzzy match candidate engine | HIGH | HIGH | P1 |
| Matching UI (review + confirm) | HIGH | MEDIUM | P1 |
| Discontinued product handler | HIGH | LOW | P1 |
| Sync log / dashboard (basic) | MEDIUM | MEDIUM | P1 |
| Change diff log | MEDIUM | MEDIUM | P2 |
| Bulk match confirmation | MEDIUM | LOW | P2 |
| Confidence score display | MEDIUM | LOW | P2 |
| Staleness alerting | MEDIUM | LOW | P2 |
| Per-supplier field mapping config | MEDIUM | MEDIUM | P2 |
| Manual override mapping | HIGH | LOW | P1 — technically simple, high value as escape hatch |
| Unmapped product queue view | MEDIUM | LOW | P2 |
| Price floor / ceiling rules | MEDIUM | MEDIUM | P3 |
| Multi-supplier conflict resolution | MEDIUM | MEDIUM | P3 |
| Audit trail / price history | LOW | HIGH | P3 |
| Horoshop-specific output | LOW | LOW | P3 |

**Priority key:**
- P1: Must have for launch
- P2: Should have, add when possible
- P3: Nice to have, future consideration

---

## Competitor Feature Analysis

Direct competitors in the Ukrainian market are not well-documented in public sources (most are bespoke scripts or freelance projects). Analysis is based on generic supplier sync tools and prom.ua ecosystem patterns.

| Feature | Generic feed sync tools (e.g., WooCommerce plugins) | Bespoke prom.ua scripts (common approach) | Our Approach |
|---------|------------------------------------------------------|-------------------------------------------|--------------|
| Fuzzy product matching | Usually exact ID match only — useless without article codes | Manual CSV mapping tables maintained by hand | Fuzzy name matching + UI — eliminates manual CSV hell |
| Per-supplier discount rules | Usually global markup only | Hardcoded per-supplier in code | Config UI per supplier — no code changes needed |
| Web UI for mapping management | Some have it | Almost never — direct DB edits | Full UI — required given 150+ items per supplier |
| Discontinued product handling | Rarely handled explicitly | Silent removal or crashes | Explicit handler: mark unavailable, flag in UI |
| Output format flexibility | WooCommerce-centric | prom.ua hardcoded | YML standard → works for prom.ua and Horoshop |
| Change visibility | Often none | None | Change diff log in v1.x |
| Multi-supplier at different discount rates | Usually complex config | Copy-paste scripts per supplier | Supplier CRUD with per-supplier discount |

**Confidence: LOW** — No direct competitor research was possible (network access denied). Analysis based on training data knowledge of WooCommerce feed sync ecosystem and general Ukrainian marketplace tooling patterns.

---

## Key Observations for Roadmap

1. **The fuzzy matching engine is the entire value of this project.** Everything else (feed ingestion, YML output, scheduler) is commodity plumbing that could be scripted in an afternoon. The matching UI and algorithm are what make this worth building vs a cron script.

2. **Store catalog import is a hidden prerequisite.** Before any matching can happen, the system needs a local copy of prom.ua's 6,100 products. This is a one-time bootstrapping step that must come before matching UI development. Source: prom.ua CSV export. Not complex, but must be in Phase 1.

3. **The MVP is small.** One supplier (MARESTO, ~150 items) × one operator = the entire initial load. Match 150 items once, let it sync. The system doesn't need to be robust until you add the second supplier.

4. **Multi-supplier introduces the hard problems.** Same store product matched from two suppliers: which price? What if supplier B has it cheaper? Conflict resolution is a v2 problem deliberately deferred.

5. **prom.ua's 4h re-import cycle is a natural constraint.** There is no user value in syncing more often than every hour. The scheduler should be configurable (1h default, 4h max recommended) but not obsessively fast.

6. **Discontinued product handling must be in v1.** If a supplier removes an item from their feed and the system silently stops updating availability, the prom.ua listing stays "in stock" indefinitely. This is a business problem (false sales) not a nice-to-have.

---

## Sources

- Project context: `C:/Projects/labresta-sync/.planning/PROJECT.md` (authoritative — defines scope, constraints, requirements) — Confidence: HIGH
- prom.ua YML import format: Based on training data knowledge of Yandex Market Language (YML) standard and prom.ua's documented support for it — Confidence: MEDIUM (unverified in this session, network access denied)
- Horoshop YML compatibility: Based on training data — Horoshop uses the same YML/Yandex dialect as prom.ua for feed import — Confidence: MEDIUM (unverified)
- Fuzzy matching algorithm patterns: Training data (Levenshtein distance, token-set ratio, string normalization for Ukrainian/Cyrillic product names) — Confidence: MEDIUM
- Competitor feature analysis: Training data + inference from WooCommerce/OpenCart ecosystem — Confidence: LOW (no direct competitor research possible)
- Ukrainian marketplace ecosystem (prom.ua import behavior, 4h cycle): Training data — Confidence: MEDIUM

**Note:** All external research (WebSearch, WebFetch, Bash/Brave Search) was denied in this environment. Findings rely on training data and project context analysis. Claims that could shift with live research are marked with their confidence level. Recommend verifying prom.ua YML field specifications against live prom.ua documentation before implementation.

---
*Feature research for: Supplier XML/YML sync tool — prom.ua / Horoshop (LabResta Sync)*
*Researched: 2026-02-26*
