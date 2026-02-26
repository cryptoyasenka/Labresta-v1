# Pitfalls Research

**Domain:** Supplier XML/YML feed sync, fuzzy product matching, e-commerce feed generation
**Researched:** 2026-02-26
**Confidence:** MEDIUM (WebSearch verified against multiple credible sources; prom.ua docs blocked 403)

---

## Critical Pitfalls

### Pitfall 1: Fuzzy Matching Produces Silent False Positives at Scale

**What goes wrong:**
The fuzzy matcher links the wrong products — e.g., a refrigerated display case from MARESTO matched to a different product with a similar name on prom.ua. Since the system automatically propagates prices and availability, wrong products get wrong prices published. Nobody notices until a customer orders and the price is grossly wrong.

**Why it happens:**
Fuzzy string similarity (Levenshtein, token overlap, etc.) scores high on name fragments that sound similar but are different products. "Стол холодильний 3 двері MARESTO" vs "Стол холодильний 2 двері BRAND" may score 85%+ similarity. Without a hard blocker on product-level attributes, the algorithm cannot differentiate them. This is especially dangerous when brand is the same but model numbers differ by one character.

**How to avoid:**
- Require BOTH brand match AND model number match as separate, weighted fields — not a single concatenated string
- Apply a confidence floor: never auto-approve matches below a configurable threshold (start at 90%)
- Route all matches through human review UI before the first activation — no auto-approve in MVP
- Store match confidence score with every match record; display it in the review UI
- Include a "must differ" guard: if two candidate products have different numeric suffixes in the model (e.g., "S500" vs "S501"), flag as uncertain even if overall score is high

**Warning signs:**
- Match queue has many items approved without review
- Price on prom.ua for a product deviates wildly from expected range
- Supplier product count doesn't match matched product count by large margin

**Phase to address:** Feed ingestion and matching phase (Phase 2 / Phase 3)

---

### Pitfall 2: Treating the YML Output as a Full Catalog Replacement

**What goes wrong:**
The generated YML contains only matched supplier products (~150 from MARESTO vs 6,100 on prom.ua). If prom.ua's auto-import is configured to replace the full catalog on every fetch, the 5,950 unmatched products get deleted or marked unavailable. This destroys the store catalog.

**Why it happens:**
Developers focus on generating a valid YML for the matched products without checking how prom.ua's import mode is configured. prom.ua import has two behavioral modes: update existing (merge) vs. full replace. The default or misconfigured mode causes deletion of omitted products.

**How to avoid:**
- Verify prom.ua import mode during Phase 1 (before building output generator): confirm the "update fields only" option applies only to products present in the feed, and that omitted products are untouched
- Generate the YML containing ONLY matched products, with explicit availability and price fields — never omit products to signal removal
- Test the import behavior manually with a 3-product YML before building automation
- Document the prom.ua import configuration as a required deploy step

**Warning signs:**
- Published product count on prom.ua drops sharply after first automated import
- Products not in the supplier feed become unavailable

**Phase to address:** Output generation spike / Phase 1 research task (before building)

---

### Pitfall 3: No Handling for Supplier Feed Unavailability — Silent Stale Data

**What goes wrong:**
The supplier feed URL goes down temporarily (server restart, maintenance, hosting issue). The sync job runs, gets an error or empty response, and either: (a) overwrites the database with empty/stale data, or (b) silently fails and nobody knows prices haven't updated in 48 hours.

**Why it happens:**
Early implementations focus on the happy path. Error handling is added later. By then, a supplier URL has already changed once and the system silently served stale prices for days.

**How to avoid:**
- Never overwrite existing price/availability data if the supplier fetch fails — keep last known good data
- Implement exponential backoff retry (at minimum 3 retries) before marking a feed as failed
- Record last successful fetch timestamp for each supplier
- Dashboard must prominently show feed status: last fetched, next scheduled, error if any
- Alert mechanism (even just a visible error banner on the dashboard) when a feed hasn't updated within 2x its configured interval

**Warning signs:**
- No "last updated" timestamp shown anywhere in the UI
- Sync job has no error logging
- Database has no field for "last_fetched_at" per supplier

**Phase to address:** Supplier sync engine phase (Phase 2)

---

### Pitfall 4: XML Encoding Mismatch Breaks Parser on First Real Feed

**What goes wrong:**
MARESTO's feed (or any subsequent supplier feed) declares UTF-8 in the XML header but is actually served as Windows-1251 (cp1251) — or vice versa. The parser throws an exception or silently produces garbled Ukrainian/Cyrillic product names. Product matching then fails entirely because names are mojibake.

**Why it happens:**
Suppliers in Ukraine and Russia commonly serve XML in Windows-1251 or KOI8-U. HTTP Content-Type headers often contradict the XML declaration. Developers write the parser against their own test file (UTF-8) and only discover the mismatch when the real feed is ingested.

**How to avoid:**
- Fetch the actual MARESTO feed before writing a single line of parser code — inspect encoding manually
- Detect encoding from both HTTP Content-Type header and XML declaration; prefer HTTP header per W3C standard but fallback-detect if mismatch
- Use a library that handles encoding detection (e.g., Python: `lxml` with charset detection; Node.js: `iconv-lite` with charset sniffing)
- Run the parser against the live feed URL in a test harness on Day 1 of the ingestion phase, not after the feature is "done"
- Log the raw bytes of the first 100 chars of every new supplier feed for diagnosis

**Warning signs:**
- Product names contain question marks, boxes, or Latin lookalikes of Cyrillic characters
- Parser succeeds but brand/model fields produce no fuzzy matches
- Integration test uses a manually created UTF-8 file, not the real supplier URL

**Phase to address:** Supplier ingestion — before parser is written (Phase 2)

---

### Pitfall 5: Floating-Point Price Calculation Errors Accumulate

**What goes wrong:**
Price is fetched from supplier as a float (e.g., `199.99`). Discount is applied as `price * (1 - 0.15)` using floating-point arithmetic. Result: `169.9915000000001` stored in DB. YML outputs `169.9915000000001`. prom.ua either rejects it or rounds incorrectly. Over many products and syncs, rounding errors compound and some prices are off by 1-2 cent.

**Why it happens:**
EUR prices with decimal cents cannot be represented exactly in binary floating point. This is a well-documented pitfall that developers routinely rediscover. In a retail pricing context, even 0.01 EUR difference can cause marketplace price validation failures.

**How to avoid:**
- Store prices as integers in the smallest currency unit (euro cents): `19999` for `199.99 EUR`
- Perform all discount calculations in integer cents, then round ONCE at the end
- Apply banker's rounding (round half to even) or always round up to protect margin
- Format price in YML output as `"%.2f" % (cents / 100)` — never format a float directly
- Write a unit test: `assert calculate_price(199.99, 0.15) == 169.99` before shipping

**Warning signs:**
- Price fields in database have type `FLOAT` or `DOUBLE` instead of `DECIMAL` or `INTEGER`
- No unit tests for the discount calculation function
- Price output shows more than 2 decimal places in YML

**Phase to address:** Pricing rules implementation phase (Phase 3)

---

### Pitfall 6: Discontinued / Renamed Products Cause Orphaned Matches

**What goes wrong:**
A product disappears from the supplier feed (discontinued, renamed, replaced). The matched link remains in the database. On next sync, the system either: (a) leaves the old price/availability unchanged indefinitely, or (b) marks the product unavailable because the supplier entry is gone — which may be correct, or may be wrong if it was just renamed.

**Why it happens:**
Sync systems are designed for the happy path of stable catalogs. Edge cases around product lifecycle — discontinuation, model year updates, rebranding — are discovered in production after matching has been running for months.

**How to avoid:**
- When a supplier product is absent from the feed for N consecutive syncs (configurable, default: 2), flag the match as "unresolved" rather than silently acting on it
- Show flagged matches in the dashboard with actions: "mark as discontinued", "re-match to new product", "ignore"
- Never auto-delete matched pairs — only archive them; keep audit trail
- Store the supplier product's last-seen-in-feed timestamp per match record
- Add a "supplier products not seen this sync" counter to the sync log

**Warning signs:**
- No "last seen in feed" timestamp on matched product records
- No UI state for "match needs attention"
- Sync log doesn't report count of products present vs. missing vs. new

**Phase to address:** Matching database design (Phase 2) and matching review UI (Phase 3)

---

## Technical Debt Patterns

Shortcuts that seem reasonable but create long-term problems.

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Auto-approve high-confidence fuzzy matches without review | Faster initial population | Wrong products priced incorrectly; hard to audit | Never — always route through review UI first |
| Use `float` for price storage | Simple to implement | Accumulating rounding errors, YML output with excess decimals | Never — use integer cents or DECIMAL(10,2) |
| Parse XML with DOM (load entire file) | Simple code | OOM on large supplier feeds (1 MB+ XML can require 30 MB RAM in DOM) | Acceptable for feeds under 500 KB; use streaming (SAX/XMLReader) for larger feeds |
| Single hardcoded supplier URL | Works for MARESTO MVP | Cannot add second supplier without code change | Only for Phase 1 spike; must be config-driven by Phase 2 |
| Skip retry logic on feed fetch | Faster to write | One supplier hiccup causes missed sync with no visibility | Never skip — minimum 3 retries with backoff before failing |
| Generate YML by string concatenation | No library dependency | Unescaped special characters break XML validity | Never — use a proper XML serializer |
| Cron job runs on PHP shared hosting via HTTP ping | Easy to set up | PHP timeout kills long-running jobs; no reliable scheduling on congested shared hosts | Acceptable for MVP if job runs under 30s; plan migration to CLI cron for Phase 2 |

---

## Integration Gotchas

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| prom.ua YML auto-import | Assuming "import from URL" updates only listed products; in reality the import mode determines whether unlisted products are hidden | Verify import mode in prom.ua settings before enabling automation; test with a subset YML first |
| prom.ua YML auto-import | Setting update interval to less than 4 hours thinking it helps; prom.ua fetches on its own schedule (minimum ~4h) | Match sync schedule to prom.ua's actual fetch interval; don't over-sync |
| MARESTO feed URL | Treating URL as permanent; suppliers change URLs without notice | Store URL in config/DB, not hardcoded; validate URL accessibility on each sync and alert on 404/503 |
| MARESTO XML format | Assuming schema is stable; suppliers add/remove fields without notice | Parse defensively — treat all fields except core price/availability/id as optional with fallback defaults |
| XML special characters | Supplier names/descriptions contain `&`, `<`, `>`, `"` unescaped in feed | Sanitize on ingest; use CDATA sections or entity encoding in output YML |
| Horoshoip future migration | Building prom.ua-specific field mapping into core logic | Keep field mapping in a platform adapter layer; generate YML from a normalized internal model |

---

## Performance Traps

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| Loading full 6,100-product catalog into memory for every sync | Sync job times out or hits PHP memory limit | Process in batches of 500 products; use streaming XML parser for supplier feed | At ~1,000 products on shared hosting with 128MB PHP limit |
| Running fuzzy matching as O(n*m) — every supplier product vs every prom.ua product | Matching takes minutes on first run | Pre-filter by brand before running fuzzy on model; use indexed search (trigram index in SQLite/Postgres) | At 150 supplier products x 6,100 catalog = 915,000 comparisons; slow but survivable; breaks at multiple large suppliers |
| Regenerating full YML on every sync even when nothing changed | High I/O on hosting, slower prom.ua fetches | Check if price/availability changed before writing to file; track a "dirty" flag per product | At 6,100 products written every 4 hours on shared hosting |
| Sync job overlaps with itself (no job lock) | Duplicate writes, double price calculations, corrupted state | Implement a lock file or DB-level job lock before running sync | From day one if scheduler fires twice close together |

---

## Security Mistakes

| Mistake | Risk | Prevention |
|---------|------|------------|
| Exposing YML feed URL without any protection | Competitor scrapes your exact prices with margin applied, enabling undercutting automation | Add a secret token to the YML URL (e.g., `/feed/abc123.yml`); not secret but adds friction |
| Storing supplier feed URLs with credentials in version control | Credentials exposed if repo is ever public or shared | Store feed URLs (especially if they contain auth tokens) in environment config, not code |
| No input validation on supplier management UI | An admin input of a malicious URL could trigger SSRF if the sync engine fetches arbitrary URLs | Validate that supplier URLs are HTTP/HTTPS, resolve to expected domains; block private IP ranges if fetching server-side |
| Sync log exposed publicly | Reveals internal product counts, matched IDs, price calculation details | Require authentication for all dashboard routes including logs |

---

## UX Pitfalls

| Pitfall | User Impact | Better Approach |
|---------|-------------|-----------------|
| Showing match confidence as a raw number (e.g., 0.87) | User doesn't know if 0.87 is good or bad | Show as "High / Medium / Low" with color coding, plus the actual matched strings side-by-side |
| Auto-scrolling match review queue to first item after approve/reject | User loses place in long queue, slow review | Stay at current scroll position, mark item as reviewed in-place, load next |
| No filter on match review (shows all 150 at once) | Overwhelming; hard to find unreviewed items | Default to "unreviewed" filter; show count badges: Unreviewed / Approved / Rejected / Flagged |
| Sync status buried in a log table | User doesn't know if prices are current without digging | Prominent dashboard card: "Last synced: 2h ago | Next: in 2h | Status: OK" |
| No confirmation before approving a match | Easy to accidentally approve wrong matches | Single-click approve is fine, but provide easy 1-click "undo last approval" |

---

## "Looks Done But Isn't" Checklist

- [ ] **Feed ingestion:** Parser works on dev fixture file — verify it works on the LIVE supplier URL with actual encoding/schema before marking done
- [ ] **Fuzzy matching:** Algorithm returns results — verify false positive rate by manually checking 20 random matches before enabling for production
- [ ] **Price calculation:** Formula calculates correct number — verify with integer cents implementation and a unit test covering edge cases (0% discount, 100% discount, prices with exactly .5 cents)
- [ ] **YML generation:** File is valid XML — validate against W3C XML validator AND import it manually into prom.ua as a test before enabling auto-import
- [ ] **Scheduled sync:** Cron job is set up — verify it actually runs by checking logs after the first scheduled interval, not just at setup time
- [ ] **Discontinued product handling:** Sync runs without errors — verify behavior when a product is removed from the supplier feed: does availability update, does matched pair persist or break?
- [ ] **prom.ua import mode:** Feed URL is configured in prom.ua — verify in prom.ua admin which fields are being updated and that unlisted products are NOT removed

---

## Recovery Strategies

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| False positive matches published to prom.ua | HIGH | Audit all approved matches; manually identify wrong ones; reject and re-match; force sync to overwrite incorrect prices |
| YML import wipes catalog | HIGH | Restore from prom.ua backup if available; reconfigure import mode; re-import full catalog from original source |
| Stale prices from silent feed failure | MEDIUM | Identify last successful sync timestamp; manually trigger sync; check prices on prom.ua for affected supplier products |
| Encoding corruption in product names | MEDIUM | Wipe ingested supplier data; fix parser encoding detection; re-ingest from scratch |
| Floating-point price errors in production | MEDIUM | Recalculate all prices using corrected integer-cent logic; force sync to overwrite YML; reimport on prom.ua |
| Orphaned matches (discontinued products) | LOW | Run audit query for matches where supplier product absent from last N syncs; bulk-flag as "needs review" |

---

## Pitfall-to-Phase Mapping

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| False positive fuzzy matches | Matching engine + review UI phase | 20-match manual audit shows <5% false positive rate before going live |
| YML overwrites prom.ua catalog | Pre-build research spike (Phase 1) | Manual test: import 3-product YML, confirm 6,097 other products untouched |
| Silent feed failure / stale data | Supplier sync engine (Phase 2) | Kill supplier URL, verify dashboard shows error and data is NOT updated |
| XML encoding mismatch | Day 1 of ingestion phase (Phase 2) | Parser produces correct Cyrillic brand/model names from live MARESTO URL |
| Floating-point price errors | Pricing rules phase (Phase 3) | Unit tests pass for all price edge cases; YML shows exactly 2 decimal places |
| Discontinued product handling | Matching DB design (Phase 2) + review UI (Phase 3) | Remove product from test feed, verify system flags match rather than silently breaking |
| prom.ua import mode misconfiguration | Output generation + deploy phase | Manual smoke test: full import cycle on prom.ua with subset feed, verify catalog intact |
| Sync job overlap | Sync scheduling phase (Phase 2) | Trigger two sync jobs simultaneously; verify second one waits or aborts cleanly |

---

## Sources

- [Common Mistakes In Fuzzy Data Matching — WinPure](https://winpure.com/fuzzy-matching-common-mistakes/) — MEDIUM confidence
- [10 E-commerce Integration Mistakes UK Retailers Keep Making — Red Eagle](https://redeagle.tech/blog/ecommerce-integration-mistakes-and-how-to-avoid-them) — MEDIUM confidence
- [The 10 Most Common Mistakes Suppliers Make in Online Retail — TYRIOS](https://www.tyrios.io/en/blog/blog/266-the-10-most-common-mistakes-that-suppliers-and-manufacturers-make-in-online-retail.html) — MEDIUM confidence
- [Augmenting AI-powered Product Matching with Human Expertise — DataWeave](https://dataweave.com/blog/augmenting-ai-powered-product-matching-with-human-expertise-to-achieve-unparalleled-accuracy) — MEDIUM confidence
- [Fuzzy Matching 101 — Data Ladder](https://dataladder.com/fuzzy-matching-101/) — MEDIUM confidence
- [Floating Point Numbers & Currency Rounding Errors — Atomic Object](https://spin.atomicobject.com/currency-rounding-errors/) — HIGH confidence (multiple corroborating sources)
- [Floats Don't Work For Storing Cents — Modern Treasury](https://www.moderntreasury.com/journal/floats-dont-work-for-storing-cents) — HIGH confidence
- [Processing Large XML Files — Assertis Tech](https://medium.com/@assertis/processing-large-xml-files-fa23b271e06d) — MEDIUM confidence
- [Character Encoding Detection — feedparser docs](https://pythonhosted.org/feedparser/character-encoding.html) — MEDIUM confidence
- [The Hidden Costs of Data Synchronization Failures — Productsup](https://www.productsup.com/blog/the-hidden-costs-of-data-synchronization-failures-in-ecommerce/) — MEDIUM confidence
- [Keeping WooCommerce Product Feeds in Sync — G7Cloud](https://g7cloud.com/knowledge-base/woocommerce-ecommerce/woocommerce-product-feeds-stock-sync-uk-hosting-cron/) — MEDIUM confidence
- [Diagnosing Feeds: How to Identify and Fix Errors — site2b.ua](https://www.site2b.ua/en/web-blog-en/diagnosing-feeds-how-to-identify-and-fix-errors.html) — MEDIUM confidence
- prom.ua YML import docs (support.prom.ua) — returned 403; requirements inferred from third-party integrations — LOW confidence; verify directly in prom.ua admin

---

*Pitfalls research for: Supplier XML/YML sync, fuzzy product matching, YML feed generation for prom.ua*
*Researched: 2026-02-26*
