# Phase 2 Research: Feed Ingestion and Matching Engine

**Phase:** 02-feed-ingestion-and-matching-engine
**Researched:** 2026-02-27
**Mode:** Ecosystem
**Overall confidence:** HIGH

## Executive Summary

Phase 2 builds the headless sync pipeline: scheduled feed fetching with retry logic, fuzzy matching of MARESTO supplier products against the prom.ua catalog, and persistence of confirmed matches. The tech stack is already decided (Python/Flask/SQLite/rapidfuzz) and Phase 1 delivered working feed_fetcher.py and feed_parser.py services. This phase layers scheduling, retry resilience, fuzzy matching, and a "disappeared product" detection mechanism on top.

The three core technical problems are: (1) reliable scheduled fetching with retry and "last known good" semantics, (2) fuzzy matching Ukrainian Cyrillic product names using rapidfuzz with appropriate scorer selection, and (3) tracking product disappearance across consecutive syncs. All three have well-established library solutions -- nothing here needs to be hand-rolled.

The biggest unknown flagged from Phase 1 is the fuzzy match false-positive rate on real Cyrillic product names. MARESTO has no `<model>` or `<vendorCode>` fields, so matching relies entirely on `name + vendor` comparisons. This means the matching strategy must be benchmarked against actual data before being integrated into the live pipeline.

## Standard Stack

Use these libraries. Do not substitute alternatives.

| Library | Version | Purpose | Confidence |
|---------|---------|---------|------------|
| rapidfuzz | >=3.0 | Fuzzy string matching (already in project) | HIGH |
| APScheduler | 3.x (3.11+) | Background job scheduling with interval triggers | HIGH |
| tenacity | >=8.0 | Retry decorator with exponential backoff for feed fetching | HIGH |
| Flask-APScheduler | >=1.13 | Thin Flask wrapper for APScheduler (app context, config loading) | MEDIUM |

### Why These Specific Libraries

**rapidfuzz over thefuzz/fuzzywuzzy:** Already decided in roadmap. 10-100x faster C++ backend, full Unicode/Cyrillic support, actively maintained (last release Jan 2026). Has `process.extract` for batch matching against choices list.

**APScheduler 3.x over 4.x:** APScheduler 4.x is a complete rewrite with async-first design. The Flask ecosystem (Flask-APScheduler) only supports 3.x. Use 3.x BackgroundScheduler for this synchronous Flask app. APScheduler 3.x has SQLAlchemyJobStore for job persistence with SQLite.

**tenacity over urllib3.Retry or manual loops:** tenacity provides clean decorator-based retry with exponential backoff, stop conditions, and retry filtering by exception type. Works at the application level (retry the entire fetch-parse operation), not just HTTP transport level. More readable than manual retry loops.

**Flask-APScheduler over plain APScheduler:** Provides automatic Flask app_context injection into scheduled jobs (critical -- without it, SQLAlchemy queries inside jobs fail with "application not registered on db" errors). Loads scheduler config from Flask config. Minimal overhead.

### Installation

```bash
uv add rapidfuzz apscheduler flask-apscheduler tenacity
```

Note: rapidfuzz may already be in pyproject.toml from roadmap planning. Verify before adding.

## Architecture Patterns

### Pattern 1: Fetch-Parse-Match Pipeline

The sync operation is a linear pipeline with clear stage boundaries:

```
Schedule Trigger
    |
    v
[1. Fetch Feed] -- tenacity retry wrapper around feed_fetcher.fetch_feed()
    |                On permanent failure: keep last_known_good, log error
    v
[2. Parse XML]  -- existing feed_parser.parse_supplier_feed()
    |                Returns list[dict] of supplier products
    v
[3. Upsert Products] -- existing feed_parser.save_supplier_products()
    |                     Updates last_seen_at timestamps
    v
[4. Detect Disappeared] -- compare last_seen_at vs current sync timestamp
    |                       Flag products missing 2+ consecutive syncs
    v
[5. Run Fuzzy Matcher] -- only for NEW/unmatched supplier products
    |                      Skip products with confirmed matches
    v
[6. Store Match Candidates] -- insert into match_candidates table
                                with confidence scores
```

Each stage is a separate function. The pipeline runner calls them in sequence and handles errors at stage boundaries. If stage 1 fails after retries, stages 2-6 do not run. If stage 3 succeeds but stage 5 fails, the product data is still safely saved.

### Pattern 2: Match State Machine

Each supplier product has a match lifecycle:

```
UNMATCHED (new product, no match attempted)
    |
    v  [fuzzy matcher runs]
CANDIDATE (match candidates generated, awaiting human review)
    |
    +---> CONFIRMED (human approved match)
    |        -> never re-matched on subsequent syncs
    |
    +---> REJECTED (human rejected match)
    |        -> can be re-matched if new prom products appear
    |
    +---> MANUAL (human manually specified a match)
             -> never re-matched on subsequent syncs
```

Store this in a `product_matches` table, not as a column on supplier_products. A supplier product may have multiple candidate matches (ranked by score) awaiting review.

### Pattern 3: "Last Known Good" Feed Data

The fetch operation must never corrupt existing good data on failure:

```python
# WRONG - overwrites before confirming new data is valid
delete_all_products(supplier_id)
products = fetch_and_parse(url)
save_products(products)

# RIGHT - existing save_supplier_products already does upsert
# On failure, old data stays. On success, records are updated.
# The upsert pattern from Phase 1 already handles this correctly.
```

The existing `save_supplier_products()` in `feed_parser.py` already implements upsert semantics (update existing, insert new). This naturally preserves last-known-good data because it never deletes -- it only updates what it finds in the new feed.

### Pattern 4: Disappeared Product Detection via last_seen_at

Track disappearance using the existing `last_seen_at` column on `SupplierProduct`:

```python
from datetime import datetime, timezone, timedelta

def detect_disappeared_products(supplier_id: int, sync_interval_hours: int = 4):
    """Flag products not seen in the last 2 sync cycles."""
    # 2 consecutive misses = 2 * interval + buffer
    threshold = datetime.now(timezone.utc) - timedelta(hours=sync_interval_hours * 2 + 1)

    stale_products = db.session.execute(
        select(SupplierProduct)
        .where(
            SupplierProduct.supplier_id == supplier_id,
            SupplierProduct.last_seen_at < threshold,
            SupplierProduct.available == True  # only flag currently-available ones
        )
    ).scalars().all()

    for product in stale_products:
        product.available = False
        product.needs_review = True  # new column needed

    db.session.commit()
    return len(stale_products)
```

This approach is simpler and more reliable than maintaining a "consecutive miss counter" because it is stateless -- it does not depend on tracking individual sync runs. The `last_seen_at` timestamp is already updated by `save_supplier_products()` on every successful parse.

**Model change needed:** Add `needs_review = db.Column(db.Boolean, default=False)` to `SupplierProduct`.

## Don't Hand-Roll

These problems have solved library solutions. Do NOT build custom implementations.

| Problem | Use This | Why Not Hand-Roll |
|---------|----------|-------------------|
| Fuzzy string matching | `rapidfuzz.process.extract` | Optimized C++ backend, handles Unicode, 100x faster than pure Python Levenshtein |
| Retry with backoff | `tenacity` decorator | Manual retry loops are error-prone (forgetting to re-raise, missing backoff, no jitter) |
| Job scheduling | APScheduler `BackgroundScheduler` | Manual threading + sleep loops leak threads, miss error handling, no persistence |
| String preprocessing | `rapidfuzz.utils.default_process` | Handles lowercasing + stripping non-alphanum consistently across Unicode |

## Fuzzy Matching Strategy

### Scorer Selection

Use `rapidfuzz.fuzz.WRatio` as the primary scorer because:

1. **MARESTO has no model/vendorCode** -- matching is purely on product name + vendor/brand
2. Product names may have tokens in different order between MARESTO and prom.ua (e.g., "Espresso Machine DeLonghi" vs "DeLonghi Espresso Machine")
3. One catalog may have more detail in the name than the other (partial match scenario)
4. `WRatio` automatically applies the best combination of ratio, partial_ratio, token_sort_ratio, and token_set_ratio -- it handles all these cases

**Do NOT use plain `fuzz.ratio`** -- it fails on reordered tokens and partial matches.

### Matching Algorithm

```python
from rapidfuzz import process, fuzz, utils

def find_match_candidates(
    supplier_product_name: str,
    supplier_brand: str | None,
    prom_products: list[dict],  # [{id, name, brand}, ...]
    score_cutoff: float = 55.0,
    limit: int = 5,
) -> list[dict]:
    """Find fuzzy match candidates for a supplier product.

    Strategy:
    1. If brand matches exactly, search only within that brand's products (blocking)
    2. If no brand or no brand match, search all products
    3. Use WRatio scorer with default_process for Unicode normalization
    """
    # Step 1: Brand-based blocking (reduces search space dramatically)
    if supplier_brand:
        brand_filtered = [
            p for p in prom_products
            if p.get("brand") and
               fuzz.ratio(
                   supplier_brand.lower(),
                   p["brand"].lower()
               ) > 80
        ]
        if brand_filtered:
            prom_products = brand_filtered

    # Step 2: Extract best matches using WRatio
    choices = {p["id"]: p["name"] for p in prom_products}

    results = process.extract(
        supplier_product_name,
        choices,
        scorer=fuzz.WRatio,
        processor=utils.default_process,
        score_cutoff=score_cutoff,
        limit=limit,
    )

    # results = [(name, score, prom_id), ...]
    return [
        {"prom_product_id": prom_id, "score": score, "prom_name": name}
        for name, score, prom_id in results
    ]
```

### Key Decisions

**score_cutoff = 55.0** -- Start conservative. This is the minimum score to even consider a match as a candidate. All candidates still require human review in MVP. This threshold can be tuned after benchmarking against real MARESTO + prom.ua pairs.

**Brand-based blocking** -- If both supplier and prom product have a brand, first filter to same-brand products. This dramatically reduces the comparison space (from 5,950 prom products to maybe 50-200 per brand) and improves both speed and accuracy.

**Confidence tiers for UI (Phase 4):**
- HIGH: score >= 85 (likely exact match with minor variations)
- MEDIUM: score 70-84 (probable match, needs verification)
- LOW: score 55-69 (possible match, likely needs rejection)

### Benchmarking Requirement

**CRITICAL:** Before integrating into the live pipeline, run the matcher against a sample of real MARESTO + prom.ua product pairs and measure:
1. How many true matches score above 85? (Should be auto-confirmable in v2)
2. How many false positives score above 55? (Determines if cutoff needs raising)
3. Are there true matches below 55 that are being missed?

This was flagged as a blocker in STATE.md and must be addressed as a task in this phase's plan.

## Scheduling Architecture

### APScheduler + Flask Setup

```python
# app/scheduler.py
from flask_apscheduler import APScheduler

scheduler = APScheduler()

def init_scheduler(app):
    """Initialize scheduler with Flask app.

    CRITICAL: Only start scheduler in the main process.
    Flask debug mode runs a reloader that spawns a child process,
    causing jobs to execute twice.
    """
    app.config["SCHEDULER_API_ENABLED"] = False  # no REST API needed
    scheduler.init_app(app)

    # Only start if not in reloader child process
    import os
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true" or not app.debug:
        scheduler.start()
```

### Job Registration

```python
# Register the sync job
@scheduler.task("interval", id="sync_feeds", hours=4, misfire_grace_time=900)
def scheduled_sync():
    """Fetch all enabled supplier feeds and run matching."""
    from app.services.sync_pipeline import run_full_sync
    run_full_sync()
```

### Double-Execution Prevention

The most common APScheduler + Flask pitfall is **double execution in debug mode**. Flask's reloader starts two processes. Prevent this by:

1. Checking `WERKZEUG_RUN_MAIN` environment variable (set only in the reloader child)
2. In production, this is not an issue (single process with gunicorn/waitress)

### SQLite Job Store

For this MVP with a single process, the default MemoryJobStore is sufficient. Do NOT add SQLAlchemyJobStore complexity unless persistence across restarts is required. The interval job is re-registered on every app startup anyway.

If job persistence is needed later:
```python
app.config["SCHEDULER_JOBSTORES"] = {
    "default": SQLAlchemyJobStore(url="sqlite:///instance/jobs.sqlite")
}
```

**Use a separate SQLite file for the job store**, not the main app database. This avoids locking conflicts between the scheduler and the web request handler.

## Retry Strategy

### Feed Fetch with Tenacity

```python
# app/services/feed_fetcher.py (enhanced)
import logging
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log,
)
import requests

logger = logging.getLogger(__name__)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=2, min=4, max=30),
    retry=retry_if_exception_type((
        requests.ConnectionError,
        requests.Timeout,
        requests.HTTPError,
    )),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    reraise=True,
)
def fetch_feed_with_retry(url: str, timeout: int = 30) -> bytes:
    """Fetch feed with automatic retry on transient failures.

    Retry schedule: attempt 1 immediately, then wait 4s, then 8s.
    Total max wait: ~12 seconds across 3 attempts.
    """
    return fetch_feed(url, timeout)
```

**Key decisions:**
- 3 attempts total (1 initial + 2 retries) -- matches SUPP-06 requirement
- Exponential backoff starting at 4 seconds -- gives the server time to recover
- Only retry on connection/timeout/HTTP errors -- not on XML parse errors (those are not transient)
- `reraise=True` -- after all retries exhausted, raise the original exception for the pipeline to handle

## Database Schema Changes

### New Table: product_matches

```sql
CREATE TABLE product_matches (
    id INTEGER PRIMARY KEY,
    supplier_product_id INTEGER NOT NULL REFERENCES supplier_products(id),
    prom_product_id INTEGER NOT NULL REFERENCES prom_products(id),
    score REAL NOT NULL,  -- fuzzy match confidence 0-100
    status TEXT NOT NULL DEFAULT 'candidate',  -- candidate|confirmed|rejected|manual
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    confirmed_at TIMESTAMP,
    confirmed_by TEXT,  -- username, for Phase 4

    UNIQUE(supplier_product_id, prom_product_id)
);

CREATE INDEX ix_product_matches_status ON product_matches(status);
CREATE INDEX ix_product_matches_supplier_product ON product_matches(supplier_product_id);
```

### New Table: sync_runs (audit trail)

```sql
CREATE TABLE sync_runs (
    id INTEGER PRIMARY KEY,
    supplier_id INTEGER NOT NULL REFERENCES suppliers(id),
    started_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP,
    status TEXT NOT NULL DEFAULT 'running',  -- running|success|error
    products_fetched INTEGER DEFAULT 0,
    products_created INTEGER DEFAULT 0,
    products_updated INTEGER DEFAULT 0,
    products_disappeared INTEGER DEFAULT 0,
    match_candidates_generated INTEGER DEFAULT 0,
    error_message TEXT,

    CONSTRAINT fk_supplier FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
);

CREATE INDEX ix_sync_runs_supplier ON sync_runs(supplier_id);
```

### Column Addition: supplier_products.needs_review

```sql
ALTER TABLE supplier_products ADD COLUMN needs_review BOOLEAN DEFAULT FALSE;
```

## Common Pitfalls

### Pitfall 1: APScheduler Double Execution in Debug Mode (CRITICAL)

**What goes wrong:** Flask debug mode spawns a reloader process. APScheduler starts in both the parent and child process, causing every scheduled job to run twice.
**Prevention:** Check `os.environ.get("WERKZEUG_RUN_MAIN")` before starting the scheduler. Only start in the child process (`== "true"`) or when not in debug mode.
**Detection:** Duplicate sync_runs entries with identical started_at timestamps.

### Pitfall 2: SQLAlchemy Session Not Available in Scheduled Jobs

**What goes wrong:** APScheduler jobs run in a background thread without Flask's app context. Any SQLAlchemy operation raises "RuntimeError: No application found."
**Prevention:** Use Flask-APScheduler (not plain APScheduler). It automatically wraps jobs in `app.app_context()`. Alternatively, manually push context: `with app.app_context():`.
**Detection:** RuntimeError in scheduler logs.

### Pitfall 3: SQLite Concurrent Write Locking

**What goes wrong:** A scheduled sync writes to SQLite at the same time as a web request. SQLite locks the entire database on writes, causing "database is locked" errors.
**Prevention:** Use WAL (Write-Ahead Logging) mode for SQLite. Add to app config or run once: `PRAGMA journal_mode=WAL;`. This allows concurrent reads during writes.
**Detection:** "OperationalError: database is locked" in logs.

```python
# In create_app() or config
from sqlalchemy import event

@event.listens_for(db.engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.close()
```

### Pitfall 4: Fuzzy Matching All Products on Every Sync

**What goes wrong:** Running the matcher against ALL supplier products every sync wastes time and regenerates candidates for already-confirmed matches.
**Prevention:** Only match products that have NO confirmed/manual match in product_matches. Filter query: `WHERE supplier_product_id NOT IN (SELECT supplier_product_id FROM product_matches WHERE status IN ('confirmed', 'manual'))`.
**Detection:** Sync runs take progressively longer as the catalog grows. Confirmed matches appear as duplicate candidates.

### Pitfall 5: Encoding Mismatch in String Comparison

**What goes wrong:** Cyrillic strings that look identical compare differently due to Unicode normalization forms (NFC vs NFD). For example, a Cyrillic "i" might be composed vs precomposed.
**Prevention:** Use `rapidfuzz.utils.default_process` as the processor parameter. It normalizes strings before comparison. Additionally, consider applying `unicodedata.normalize("NFC", s)` during feed parsing and catalog import.
**Detection:** Products with visually identical names score below 100.

### Pitfall 6: Disappearance False Positives from Temporary Feed Outages

**What goes wrong:** MARESTO feed is temporarily empty or returns partial data. The system flags all products as "disappeared" after 2 syncs of missing data.
**Prevention:** Before running disappearance detection, sanity-check the feed: if the product count drops by more than 50% from the previous sync, log a warning and skip disappearance detection. The feed is likely broken, not the catalog.
**Detection:** Large number of products suddenly flagged as needs_review.

```python
def should_run_disappearance_check(supplier_id: int, current_count: int) -> bool:
    """Don't flag disappearances if feed looks broken."""
    previous_count = db.session.execute(
        select(func.count(SupplierProduct.id))
        .where(SupplierProduct.supplier_id == supplier_id)
    ).scalar()

    if previous_count and current_count < previous_count * 0.5:
        logger.warning(
            f"Feed product count dropped >50% ({previous_count} -> {current_count}). "
            f"Skipping disappearance detection."
        )
        return False
    return True
```

### Pitfall 7: Not Committing Sync Run Record on Pipeline Failure

**What goes wrong:** If the pipeline crashes mid-way, the sync_run record stays in "running" status forever.
**Prevention:** Use try/finally to always update the sync_run record's status and completed_at, even on failure.

## Code Examples

### Full Sync Pipeline Runner

```python
# app/services/sync_pipeline.py
import logging
from datetime import datetime, timezone

from sqlalchemy import select, func

from app.extensions import db
from app.models.supplier import Supplier
from app.models.supplier_product import SupplierProduct
from app.models.sync_run import SyncRun
from app.models.product_match import ProductMatch
from app.models.catalog import PromProduct
from app.services.feed_fetcher import fetch_feed_with_retry
from app.services.feed_parser import parse_supplier_feed, save_supplier_products
from app.services.matcher import find_match_candidates

logger = logging.getLogger(__name__)

def run_full_sync(supplier_id: int | None = None):
    """Run the complete sync pipeline for one or all enabled suppliers."""
    if supplier_id:
        suppliers = [db.session.get(Supplier, supplier_id)]
    else:
        suppliers = db.session.execute(
            select(Supplier).where(Supplier.is_enabled == True)
        ).scalars().all()

    for supplier in suppliers:
        if supplier:
            _sync_single_supplier(supplier)


def _sync_single_supplier(supplier: Supplier):
    """Pipeline: fetch -> parse -> save -> detect disappeared -> match."""
    sync_run = SyncRun(
        supplier_id=supplier.id,
        started_at=datetime.now(timezone.utc),
        status="running",
    )
    db.session.add(sync_run)
    db.session.commit()

    try:
        # Stage 1: Fetch with retry
        raw_bytes = fetch_feed_with_retry(supplier.feed_url)

        # Stage 2: Parse
        products = parse_supplier_feed(raw_bytes, supplier.id)

        # Stage 3: Upsert
        result = save_supplier_products(products)
        sync_run.products_fetched = len(products)
        sync_run.products_created = result["created"]
        sync_run.products_updated = result["updated"]

        # Stage 4: Detect disappeared products
        if should_run_disappearance_check(supplier.id, len(products)):
            disappeared = detect_disappeared_products(supplier.id)
            sync_run.products_disappeared = disappeared

        # Stage 5+6: Fuzzy match new/unmatched products
        candidates = run_matching_for_supplier(supplier.id)
        sync_run.match_candidates_generated = candidates

        sync_run.status = "success"
        sync_run.completed_at = datetime.now(timezone.utc)
        db.session.commit()

    except Exception as e:
        logger.exception(f"Sync failed for supplier {supplier.id}")
        sync_run.status = "error"
        sync_run.error_message = str(e)[:1000]
        sync_run.completed_at = datetime.now(timezone.utc)
        db.session.commit()
```

### CLI Trigger for Manual Sync

```python
# app/cli.py
import click
from flask.cli import with_appcontext

@click.command("sync")
@click.option("--supplier-id", type=int, default=None, help="Sync specific supplier")
@with_appcontext
def sync_command(supplier_id):
    """Run sync pipeline manually."""
    from app.services.sync_pipeline import run_full_sync
    run_full_sync(supplier_id)
    click.echo("Sync complete.")
```

Register in app factory:
```python
# In create_app()
from app.cli import sync_command
app.cli.add_command(sync_command)
```

Usage: `uv run flask sync` or `uv run flask sync --supplier-id 1`

### Matcher Integration

```python
# app/services/matcher.py
from rapidfuzz import process, fuzz, utils
from sqlalchemy import select

from app.extensions import db
from app.models.supplier_product import SupplierProduct
from app.models.catalog import PromProduct
from app.models.product_match import ProductMatch

SCORE_CUTOFF = 55.0
MATCH_LIMIT = 5

def run_matching_for_supplier(supplier_id: int) -> int:
    """Generate match candidates for unmatched supplier products.

    Returns count of new candidates generated.
    """
    # Get unmatched supplier products
    matched_ids = db.session.execute(
        select(ProductMatch.supplier_product_id)
        .where(ProductMatch.status.in_(["confirmed", "manual"]))
    ).scalars().all()

    unmatched = db.session.execute(
        select(SupplierProduct)
        .where(
            SupplierProduct.supplier_id == supplier_id,
            SupplierProduct.id.notin_(matched_ids) if matched_ids else True,
            SupplierProduct.available == True,
        )
    ).scalars().all()

    if not unmatched:
        return 0

    # Load all prom products for matching
    prom_products = db.session.execute(
        select(PromProduct)
    ).scalars().all()

    prom_list = [
        {"id": p.id, "name": p.name, "brand": p.brand}
        for p in prom_products
    ]

    total_candidates = 0

    for sp in unmatched:
        candidates = find_match_candidates(
            supplier_product_name=sp.name,
            supplier_brand=sp.brand,
            prom_products=prom_list,
            score_cutoff=SCORE_CUTOFF,
            limit=MATCH_LIMIT,
        )

        for c in candidates:
            # Skip if candidate already exists
            existing = db.session.execute(
                select(ProductMatch).where(
                    ProductMatch.supplier_product_id == sp.id,
                    ProductMatch.prom_product_id == c["prom_product_id"],
                )
            ).scalar_one_or_none()

            if not existing:
                match = ProductMatch(
                    supplier_product_id=sp.id,
                    prom_product_id=c["prom_product_id"],
                    score=c["score"],
                    status="candidate",
                )
                db.session.add(match)
                total_candidates += 1

    db.session.commit()
    return total_candidates
```

## Phase-Specific Warnings

| Task Area | Likely Pitfall | Mitigation |
|-----------|---------------|------------|
| Scheduler setup | Double execution in debug mode | Check WERKZEUG_RUN_MAIN env var |
| Scheduler setup | No app context in background thread | Use Flask-APScheduler, not plain APScheduler |
| SQLite writes | Concurrent locking from scheduler + web | Enable WAL mode via PRAGMA |
| Fuzzy matching | Matching confirmed products again | Filter by match status before running matcher |
| Fuzzy matching | Poor Cyrillic comparison | Use utils.default_process + NFC normalization |
| Disappeared detection | False positives from broken feed | Sanity-check product count drop > 50% |
| Retry logic | Retrying parse errors (not transient) | Only retry ConnectionError/Timeout/HTTPError |
| Sync pipeline | Orphaned "running" sync_run on crash | try/finally to always update sync_run status |

## Implications for Roadmap

### Suggested Task Ordering

1. **Database schema changes first** -- Add product_matches table, sync_runs table, needs_review column. Everything else depends on these.
2. **Retry-enhanced feed fetching** -- Layer tenacity on existing feed_fetcher.py. Small change, high value.
3. **Sync pipeline runner** -- Orchestrates fetch/parse/save with sync_run audit trail. The core "plumbing."
4. **Fuzzy matching benchmark** -- Run matcher against real MARESTO + prom.ua data. MUST happen before integrating matcher into pipeline. This resolves the blocker from STATE.md.
5. **Fuzzy matching integration** -- Wire matcher into sync pipeline. Depends on benchmark results for threshold tuning.
6. **Disappeared product detection** -- Implement staleness check with sanity guard.
7. **Scheduler setup** -- Wire APScheduler to trigger sync pipeline on interval. Last because manual CLI sync works for testing everything above.
8. **CLI manual sync command** -- Simple Flask CLI command. Can be done alongside step 3.

### Research Flags

- **Fuzzy matching threshold (SCORE_CUTOFF):** The 55.0 default is a starting point. The benchmark task must validate this against real data and adjust. LOW confidence on the specific number.
- **Brand blocking effectiveness:** Depends on how consistently brands are named between MARESTO and prom.ua. May need looser brand matching (fuzzy brand comparison at >80 threshold). MEDIUM confidence.
- **4-hour sync interval:** Acceptable for MVP. MARESTO feed update frequency is unknown -- may need adjustment based on observation.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Scheduling (APScheduler) | HIGH | Well-documented, standard Flask pattern, known pitfalls documented |
| Retry (tenacity) | HIGH | Mature library, straightforward decorator pattern |
| Fuzzy matching (rapidfuzz API) | HIGH | API well-documented, Unicode support confirmed |
| Fuzzy matching (threshold tuning) | LOW | Must benchmark against real Cyrillic data -- unknown false positive rate |
| Disappeared detection | MEDIUM | Simple timestamp approach, but feed reliability assumptions untested |
| SQLite concurrency | HIGH | WAL mode is the standard solution, well-proven |

## Sources

- [RapidFuzz GitHub](https://github.com/rapidfuzz/RapidFuzz) -- library overview, Unicode support
- [RapidFuzz 3.14.3 Documentation - process module](https://rapidfuzz.github.io/RapidFuzz/Usage/process.html) -- extract/extractOne API
- [RapidFuzz 3.14.3 Documentation - fuzz module](https://rapidfuzz.github.io/RapidFuzz/Usage/fuzz.html) -- WRatio, token_sort_ratio, token_set_ratio
- [APScheduler 3.x User Guide](https://apscheduler.readthedocs.io/en/3.x/userguide.html) -- BackgroundScheduler, job stores
- [APScheduler 3.x FAQ](https://apscheduler.readthedocs.io/en/3.x/faq.html) -- double execution, multi-process warnings
- [Flask-APScheduler GitHub](https://viniciuschiele.github.io/flask-apscheduler/) -- Flask integration, app context handling
- [APScheduler double execution issue #521](https://github.com/agronholm/apscheduler/issues/521) -- debug mode pitfall
- [Flask-APScheduler debug mode issue #139](https://github.com/viniciuschiele/flask-apscheduler/issues/139) -- double execution in debug
- [Tenacity GitHub](https://github.com/jd/tenacity) -- retry library
- [Tenacity Documentation](https://tenacity.readthedocs.io/) -- retry patterns, exponential backoff
- [APScheduler SQLAlchemy Job Store docs](https://apscheduler.readthedocs.io/en/3.x/modules/jobstores/sqlalchemy.html) -- SQLite job persistence
