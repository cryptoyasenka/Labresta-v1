# Architecture Research

**Domain:** Supplier price feed sync / marketplace price automation
**Researched:** 2026-02-26
**Confidence:** MEDIUM (training knowledge + project requirements analysis; no external sources reachable)

## Standard Architecture

### System Overview

```
┌──────────────────────────────────────────────────────────────────────┐
│                        EXTERNAL SOURCES                              │
│  ┌─────────────────┐   ┌─────────────────┐   ┌──────────────────┐   │
│  │ MARESTO YML URL │   │ Supplier 2 URL  │   │ Supplier N URL   │   │
│  └────────┬────────┘   └────────┬────────┘   └────────┬─────────┘   │
└───────────┼────────────────────┼────────────────────┼──────────────┘
            │  HTTP fetch (scheduled every 4h)        │
            ▼                    ▼                    ▼
┌──────────────────────────────────────────────────────────────────────┐
│                       INGESTION LAYER                                │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  Feed Fetcher & Parser                                         │  │
│  │  - HTTP GET with timeout/retry                                 │  │
│  │  - XML/YML parse → internal product schema                    │  │
│  │  - Schema validation (price, availability, brand, model)      │  │
│  └──────────────────────────────┬─────────────────────────────────┘  │
└─────────────────────────────────┼────────────────────────────────────┘
                                  │ normalized SupplierProduct[]
                                  ▼
┌──────────────────────────────────────────────────────────────────────┐
│                       MATCHING LAYER                                 │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  Fuzzy Match Engine                                            │  │
│  │  - candidate lookup by brand (exact) + model (fuzzy)          │  │
│  │  - confidence score 0.0–1.0                                   │  │
│  │  - auto-confirm above threshold (e.g. 0.9)                    │  │
│  │  - queue for human review below threshold                     │  │
│  └──────────────────────────────┬─────────────────────────────────┘  │
│                                  │                                   │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  Mapping Store (DB)                                            │  │
│  │  - confirmed: supplier_product_id ↔ prom_product_id           │  │
│  │  - rejected: explicitly ignored pairs                         │  │
│  │  - pending: awaiting human review                             │  │
│  └──────────────────────────────┬─────────────────────────────────┘  │
└─────────────────────────────────┼────────────────────────────────────┘
                                  │ matched pairs (supplier + prom product)
                                  ▼
┌──────────────────────────────────────────────────────────────────────┐
│                       PROCESSING LAYER                               │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  Pricing Engine                                                │  │
│  │  - load supplier discount config (% per supplier)             │  │
│  │  - final_price = supplier_retail × (1 − discount%)            │  │
│  │  - round to sensible precision (2 decimals, EUR)              │  │
│  └──────────────────────────────┬─────────────────────────────────┘  │
└─────────────────────────────────┼────────────────────────────────────┘
                                  │ priced product updates
                                  ▼
┌──────────────────────────────────────────────────────────────────────┐
│                       OUTPUT LAYER                                   │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  YML Feed Generator                                            │  │
│  │  - load base prom.ua catalog snapshot                         │  │
│  │  - overlay matched product updates (price, availability)      │  │
│  │  - emit prom.ua-compatible YML to /public/feed.yml            │  │
│  └──────────────────────────────┬─────────────────────────────────┘  │
└─────────────────────────────────┼────────────────────────────────────┘
                                  │ static file served over HTTP
                                  ▼
┌──────────────────────────────────────────────────────────────────────┐
│                       CONSUMER                                       │
│  prom.ua auto-import (polls /public/feed.yml every 4h)              │
└──────────────────────────────────────────────────────────────────────┘

MANAGEMENT PLANE (parallel, not in sync hot path)
┌──────────────────────────────────────────────────────────────────────┐
│                       WEB UI                                         │
│  ┌─────────────────┐  ┌──────────────────┐  ┌───────────────────┐   │
│  │    Dashboard    │  │ Supplier Manager  │  │  Match Reviewer   │   │
│  │  sync status    │  │  URL, discount%  │  │  confirm/reject   │   │
│  │  match counts   │  │  enable/disable  │  │  manual override  │   │
│  └─────────────────┘  └──────────────────┘  └───────────────────┘   │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │  Sync Log Viewer — timestamp, changes (price diffs, avail)    │ │
│  └─────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────┘

SCHEDULER (cron / setInterval / cron job on hosting)
  → triggers Feed Fetcher every 4 hours
  → triggers YML Generator after fetch+match completes
```

### Component Responsibilities

| Component | Responsibility | Typical Implementation |
|-----------|----------------|------------------------|
| Feed Fetcher | HTTP GET supplier URL, download XML/YML blob | Node.js `fetch` or `axios` with timeout |
| Feed Parser | Parse XML/YML → internal SupplierProduct schema | `fast-xml-parser` or `xml2js` |
| Schema Normalizer | Map supplier-specific field names to internal fields | Thin adapter per supplier |
| Fuzzy Match Engine | Score supplier products against prom catalog products | `fuse.js` or custom Levenshtein on brand+model tokens |
| Mapping Store | Persist confirmed/rejected/pending match pairs | SQLite table: `product_mappings` |
| Pricing Engine | Apply per-supplier discount formula | Pure function, config-driven |
| YML Feed Generator | Build prom.ua-compatible YML from matched + priced data | Template or XML builder |
| Scheduler | Run sync pipeline on cadence | `node-cron` or OS cron + HTTP trigger endpoint |
| Web API | REST endpoints for UI and scheduler trigger | Express or Fastify |
| Web UI | Browser interface for management | React + Tanstack Query, or server-rendered |
| Database | Persist all state: suppliers, mappings, catalog snapshot, logs | SQLite (shared hosting) or Postgres |
| Static File Server | Serve generated feed.yml at public URL | Hosting's Apache/nginx, or Express static |

## Recommended Project Structure

```
src/
├── ingestion/              # Feed fetching and parsing
│   ├── fetcher.ts          # HTTP fetch with retry/timeout
│   ├── parser.ts           # XML/YML → internal schema
│   └── adapters/           # Per-supplier field name mappings
│       └── maresto.ts      # MARESTO-specific normalization
├── matching/               # Fuzzy matching engine
│   ├── engine.ts           # Core fuzzy match logic
│   ├── scorer.ts           # Confidence scoring
│   └── normalizer.ts       # Text normalization (lowercase, strip punctuation)
├── pricing/                # Pricing rule application
│   └── engine.ts           # discount % → final price calculation
├── output/                 # YML feed generation
│   ├── generator.ts        # Assemble output YML
│   └── schema.ts           # prom.ua YML field definitions
├── scheduler/              # Sync orchestration
│   └── pipeline.ts         # Orchestrates fetch → match → price → generate
├── db/                     # Database layer
│   ├── schema.ts           # Table definitions
│   ├── migrations/         # Schema migrations
│   └── repos/              # Repository functions per entity
│       ├── suppliers.ts
│       ├── mappings.ts
│       ├── catalog.ts
│       └── sync-log.ts
├── api/                    # REST API (management plane)
│   ├── routes/
│   │   ├── suppliers.ts    # CRUD supplier configs
│   │   ├── mappings.ts     # Review/confirm/reject matches
│   │   ├── sync.ts         # Trigger sync, fetch logs
│   │   └── feed.ts         # Serve generated YML (or redirect to static)
│   └── server.ts
├── ui/                     # Web UI (if bundled)
│   ├── pages/
│   └── components/
└── shared/
    ├── types.ts            # Shared domain types
    └── config.ts           # Environment config loader
```

### Structure Rationale

- **ingestion/:** Isolated so each supplier can have its own adapter without touching matching logic
- **matching/:** Self-contained; testable independently with fixture data
- **pricing/:** Pure functions only — easy to test, easy to swap formulas
- **output/:** Knows only prom.ua YML format; receives already-priced data
- **scheduler/:** Thin orchestrator — calls ingestion → matching → pricing → output in order
- **db/repos/:** Repository pattern keeps SQL out of business logic
- **api/:** Management plane entirely separate from sync pipeline — sync can run headlessly

## Architectural Patterns

### Pattern 1: Pipeline (Linear ETL)

**What:** Each sync run flows strictly through stages: Fetch → Parse → Match → Price → Generate. Each stage receives input, produces output, passes to next stage.

**When to use:** Always for the sync hot path. Data moves in one direction; stages are decoupled.

**Trade-offs:** Simple, testable, debuggable. Each stage can be tested with fixtures. No partial-update complexity.

**Example:**
```typescript
// scheduler/pipeline.ts
export async function runSyncPipeline(supplierId: string) {
  const rawFeed = await fetchFeed(supplier.url);
  const products = parseFeed(rawFeed, supplier.adapter);
  const matched = await applyMappings(products, supplierId);
  const priced = applyPricing(matched, supplier.discountPercent);
  await generateYmlFeed(priced);
  await logSyncRun(supplierId, { matched: matched.length, timestamp: new Date() });
}
```

### Pattern 2: Adapter per Supplier

**What:** Each supplier gets a thin adapter that maps their field names/formats to the internal `SupplierProduct` type. The rest of the pipeline is supplier-agnostic.

**When to use:** From day 1 — even MARESTO alone warrants an adapter so the parser is not hardcoded to one schema.

**Trade-offs:** Small overhead per supplier added. Prevents the parser from becoming a god function with `if (supplier === 'maresto') ...` branches.

**Example:**
```typescript
// ingestion/adapters/maresto.ts
export function adaptMaresto(raw: any): SupplierProduct {
  return {
    supplierId: raw.id,
    brand: raw.vendor,          // MARESTO calls it "vendor"
    model: raw.model,
    retailPrice: parseFloat(raw.price),
    available: raw.available === 'true',
    currency: raw.currencyId ?? 'EUR',
  };
}
```

### Pattern 3: Three-State Mapping (confirmed / pending / rejected)

**What:** Every supplier-to-catalog pairing exists in one of three states. Only `confirmed` mappings make it into the output YML. `pending` flows to the UI review queue. `rejected` is remembered so the matcher doesn't re-suggest it.

**When to use:** Essential from the first sync. Without it, every re-sync would re-propose already-reviewed matches.

**Trade-offs:** Requires DB; adds UI surface area. The alternative (no persistent state) means human review work is never saved — unacceptable.

**Example:**
```typescript
type MappingState = 'confirmed' | 'pending' | 'rejected';

interface ProductMapping {
  id: number;
  supplierProductId: string;
  supplierId: string;
  promProductId: string;
  state: MappingState;
  confidence: number;       // 0.0–1.0 from fuzzy engine
  confirmedAt?: Date;
  confirmedBy?: string;     // 'auto' | 'user'
}
```

### Pattern 4: Confidence-Threshold Auto-Confirm

**What:** Fuzzy matches above a high threshold (e.g. 0.92) are auto-confirmed without human review. Matches between a low threshold (e.g. 0.6) and the high are queued for human review. Below the low threshold are discarded.

**When to use:** Necessary to avoid drowning the user in 150 review decisions on first sync with MARESTO alone — at 5+ suppliers this becomes 500+ decisions.

**Trade-offs:** Risk of false auto-confirms. Mitigate by making the high threshold conservative (0.90–0.95) and logging every auto-confirm for audit.

## Data Flow

### Sync Pipeline Flow (scheduled, every 4h)

```
[Scheduler trigger]
       |
       v
[Feed Fetcher] --- HTTP GET ---> [Supplier URL]
       |                              |
       |         raw XML/YML body     |
       | <----------------------------+
       |
       v
[Feed Parser + Adapter]
       |
       | SupplierProduct[] (normalized)
       v
[Mapping Store lookup]
       |
       +-- Already confirmed? --> [Pricing Engine] --> [YML Generator]
       |
       +-- Not seen before? -----> [Fuzzy Match Engine]
                                         |
                              confidence score
                                         |
                    +--------------------+--------------------+
                    |                                         |
               >= threshold                           < threshold
                    |                                         |
             auto-confirm                          queue as 'pending'
             save to DB                            save to DB
                    |
                    v
             [Pricing Engine]
                    |
                    v
             [YML Generator]
                    |
             write /public/feed.yml
                    |
                    v
             [Sync Log] — append run record
```

### Human Review Flow (on-demand via UI)

```
[User opens Match Reviewer in browser]
       |
       v
[API: GET /mappings?state=pending]
       |
       | pending MappingProposal[]
       v
[User confirms / rejects / overrides prom_product_id]
       |
       v
[API: PATCH /mappings/:id]
       |
       | update state in DB
       v
[Next sync run picks up confirmed mappings normally]
```

### Output Generation Flow

```
[Confirmed + priced product updates]
       |
       v
[Load prom.ua catalog snapshot from DB]
       |
       v
[Overlay: for each matched product,
  replace price and availability
  with supplier-derived values]
       |
       v
[Serialize to YML]
  <yml version="2">
    <shop>
      <offers>
        <offer id="...">
          <price>1234.50</price>
          <currencyId>EUR</currencyId>
          <available>true</available>
          ...
        </offer>
      </offers>
    </shop>
  </yml>
       |
       v
[Write to /public/feed.yml atomically]
  (write to feed.yml.tmp, then rename)
```

### Key Data Flows

1. **Supplier → Catalog:** Unidirectional. Supplier data updates catalog records. Catalog data is never pushed back to supplier.
2. **Mapping confirmation:** Bidirectional between UI and DB. Human decisions persist in DB; sync reads DB state.
3. **Feed delivery:** Pull-only. prom.ua polls the static file. We never push to prom.ua.
4. **Catalog snapshot:** Load once from prom.ua export CSV/YML at setup. Updated manually when products are added/removed from the store.

## Fuzzy Matching Component — Detailed

This is the highest-complexity component in the system. It deserves its own breakdown.

### Matching Strategy

```
Input: SupplierProduct { brand, model }
       PromProduct[] { name, brand, model? }

Step 1: Pre-filter by brand
  - Normalize brand strings (lowercase, strip punctuation, common aliases)
  - Exact brand match reduces candidate set from 6100 to ~50-200

Step 2: Fuzzy match model within brand group
  - Normalize model strings (lowercase, strip extra words like "3-door")
  - Compute similarity score (Levenshtein ratio or token set ratio)
  - Rank candidates by score

Step 3: Threshold decision
  - score >= 0.92 → auto-confirm
  - score 0.60–0.91 → queue for review (show top 3 candidates)
  - score < 0.60 → discard (no reasonable match)
```

### Normalization is Critical

Text normalization before matching prevents false negatives:

```typescript
function normalizeForMatching(s: string): string {
  return s
    .toLowerCase()
    .replace(/[-_]/g, ' ')           // hyphens and underscores to spaces
    .replace(/\d+-door/g, '')        // remove "3-door", "4-door" variants
    .replace(/\s+/g, ' ')            // collapse whitespace
    .trim();
}
// "Холодильний стол трьохдверний" → "холодильний стол трьохдверний"
// "стол холодильний 3 двері" → "стол холодильний 3 двері"
// (token set matching handles word order differences)
```

### Recommended Library: fuse.js

Token-set or partial-ratio strategies (as in `fuse.js` or `rapidfuzz`) handle:
- Word order differences ("холодильний стол" vs "стол холодильний")
- Minor spelling variants
- Extra/missing words

fuse.js is lightweight (works in Node.js, no native deps), well-maintained, and directly supports threshold configuration.

**Confidence:** MEDIUM (fuse.js is well-known; suitability for Ukrainian text confirmed by algorithm analysis — no native-dependency issues for Cyrillic text)

## Scaling Considerations

This is an internal tool for one store with 6,100 products and 5+ suppliers. Scaling to millions of users is not relevant. The relevant scaling axis is catalog size and supplier count.

| Scale | Architecture Adjustments |
|-------|--------------------------|
| 1 supplier, 150 products | Current design is sufficient. SQLite, single process. |
| 5 suppliers, ~750 products | Still fine. Add adapter per supplier. Run pipeline sequentially per supplier. |
| 20+ suppliers, 5000+ supplier products | Consider queuing pipeline per supplier (run one at a time, not parallel) to avoid memory spikes and DB write contention. |
| Catalog grows to 50k+ products | Fuzzy matching on 50k candidates per supplier product becomes slow. Add indexed brand lookup to cut candidate set first. This is already in the recommended strategy above. |

### Scaling Priorities

1. **First bottleneck:** Fuzzy matching against large unfiltered candidate set. Fix: pre-filter by brand before running Levenshtein. Already designed this way.
2. **Second bottleneck:** YML file generation for 6100 products. Fix: generate incrementally or cache unchanged products. At 6100 products this is unlikely to be slow even naively.
3. **Third bottleneck:** Concurrent sync runs stepping on each other. Fix: simple mutex / lock file prevents concurrent runs. A scheduler with job state tracking prevents double-triggering.

## Anti-Patterns

### Anti-Pattern 1: Monolithic Parser with Per-Supplier Branches

**What people do:** Write one large parser with `if (supplierName === 'maresto') { ... } else if (...) { ... }` inside.

**Why it's wrong:** Every new supplier requires editing the parser. Hard to test individual suppliers. Grows to hundreds of lines of conditionals.

**Do this instead:** Adapter pattern — one adapter file per supplier, all conforming to the same interface. Parser calls `adapter.normalize(rawProduct)`.

### Anti-Pattern 2: Re-Running Fuzzy Match on Every Sync

**What people do:** Every sync discards all mappings and re-runs fuzzy match from scratch.

**Why it's wrong:** All human review decisions are lost on every sync. Users must re-confirm the same matches every 4 hours. Unusable.

**Do this instead:** Persist confirmed and rejected mappings in DB. On each sync, only run fuzzy match on new supplier products (no existing mapping). Confirmed mappings go directly to pricing step.

### Anti-Pattern 3: Overwriting the Entire Output YML

**What people do:** Regenerate the entire catalog YML from scratch each sync, replacing all 6100 products.

**Why it's wrong:** prom.ua interprets a full re-upload as "these are ALL my products" and may deactivate products not in the feed. Also, products not covered by any supplier get wiped.

**Do this instead:** Build the output YML as a patch — only include matched products (the ones the sync manages). prom.ua's selective import (import only price/availability fields, not product existence) handles this correctly. Document clearly which fields the import is configured to update.

### Anti-Pattern 4: Storing Supplier Raw XML in the Database

**What people do:** Dump the raw XML blob into a database column for "auditability."

**Why it's wrong:** Bloats the database. Raw supplier data is transient — the normalized form is what matters for the system.

**Do this instead:** Log the fetch timestamp and product count per sync run. Store only the normalized, processed data. If raw XML audit is needed, write it to a rotating log file, not the DB.

### Anti-Pattern 5: No Atomic File Write for the Output Feed

**What people do:** Open `feed.yml`, truncate, write new content. If process crashes mid-write, prom.ua downloads a corrupted partial file.

**Why it's wrong:** prom.ua polling at the exact moment of write gets a broken XML document, causing import failure.

**Do this instead:** Write to `feed.yml.tmp`, then `rename()` (atomic on POSIX filesystems). prom.ua always sees either the old complete file or the new complete file.

## Integration Points

### External Services

| Service | Integration Pattern | Notes |
|---------|---------------------|-------|
| MARESTO YML feed | HTTP GET on schedule | URL: https://mrst.com.ua/include/price.xml — check robots.txt; add User-Agent header |
| prom.ua auto-import | Static file served at public URL | prom.ua polls every 4h; configure import to update only price + availability fields |
| Shared hosting | FTP deploy or SSH + cron | Cron job or node-cron inside the app process |

### Internal Boundaries

| Boundary | Communication | Notes |
|----------|---------------|-------|
| Scheduler → Pipeline | Direct function call (same process) | No queue needed at this scale |
| Pipeline → DB | Repository functions (typed wrappers over SQL) | Never raw SQL in pipeline code |
| API → DB | Same repositories as pipeline uses | Shared schema, separate entry points |
| API → Pipeline | Synchronous HTTP endpoint `POST /sync/trigger` | Returns immediately; runs pipeline async |
| UI → API | REST + JSON | No WebSockets needed; polling for sync status is fine |

## Build Order Implications

The component dependencies dictate this build sequence:

```
1. DB schema + migrations
        ↓
2. Feed Fetcher + MARESTO Adapter + Parser
        ↓ (can test with fixture XML)
3. Mapping Store (DB repos: suppliers, mappings, catalog)
        ↓
4. Fuzzy Match Engine
        ↓ (can test independently with fixture catalog)
5. Pricing Engine
        ↓ (pure function, simplest component)
6. YML Feed Generator
        ↓
7. Sync Pipeline (orchestrates 2–6)
        ↓
8. Scheduler
        ↓
9. Web API (exposes management endpoints)
        ↓
10. Web UI (consumes API)
```

**Rationale:** Each component in the list depends only on components above it. This means:
- After step 6, you have a working headless sync tool — testable end-to-end with a script
- Steps 7–8 make it automated
- Steps 9–10 make it manageable without editing config files
- The UI is last because the pipeline must work correctly first; don't build UI for a broken sync

## Sources

- Project requirements: `C:/Projects/labresta-sync/.planning/PROJECT.md` (HIGH confidence — direct requirements)
- ETL pipeline patterns: training knowledge, industry standard (MEDIUM confidence)
- Fuzzy matching strategies: training knowledge on fuse.js and text similarity algorithms (MEDIUM confidence)
- prom.ua YML import behavior: project context / requirements (MEDIUM confidence — verify prom.ua docs on field-selective import)
- Atomic file write pattern: POSIX rename(2) standard, well-established (HIGH confidence)
- Adapter pattern: Gang of Four, industry standard (HIGH confidence)

---
*Architecture research for: Supplier XML/YML price feed sync system (LabResta Sync)*
*Researched: 2026-02-26*
