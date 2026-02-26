# Stack Research

**Domain:** Supplier price sync / XML-YML feed aggregator for Ukrainian marketplace (prom.ua)
**Researched:** 2026-02-26
**Confidence:** MEDIUM — external tools unavailable; based on training data (cutoff Aug 2025) + known-stable library facts. Flag items marked LOW for validation before use.

---

## Decision: PHP on Shared Hosting vs Python/Node Web App

The critical fork in stack selection is the deployment target. The project constraint states "deploy on own hosting (PHP/FTP access typical)." Two viable paths exist:

**Path A — PHP on Shared Hosting:** Zero deployment friction. PHP is already running. No process manager needed. But: no native scheduler daemon (must use cron via hosting panel), XML parsing is verbose, fuzzy matching libraries are weak.

**Path B — Python App on VPS/cheap cloud:** Better libraries (lxml, rapidfuzz, APScheduler), clean async fetching, excellent ORM support. Requires a VPS or container host (Railway, Fly.io, Render free tier) — not shared hosting. Costs $5-7/month.

**Recommendation: Path B — Python (Flask + APScheduler + SQLite) deployed on a low-cost VPS or Render/Railway.**

Rationale: The fuzzy matching requirement (brand+model matching across inconsistent naming) is the core technical complexity of this project. Python's `rapidfuzz` library handles this elegantly. PHP has no comparable production-quality fuzzy match library. Additionally, APScheduler embedded in the app eliminates cron configuration complexity. The cost delta ($0 shared hosting vs ~$5/month VPS) is justified by the development velocity gain. If shared hosting is a hard requirement, see the PHP fallback section below.

---

## Recommended Stack (Path B — Python)

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| Python | 3.12+ | Runtime | 3.12 has significant performance improvements over 3.10/3.11; active LTS until Oct 2028. Standard for data processing tools. |
| Flask | 3.1.x | Web framework | Minimal footprint fits a single-developer internal tool. Full control over routing. No ORM coupling. FastAPI adds complexity (async) that doesn't pay off for a low-traffic admin UI. |
| SQLite | 3.x (bundled) | Database | 6,100 products + mappings fit comfortably in SQLite. Zero operational overhead — single file, no server. Upgradeable to PostgreSQL later via SQLAlchemy if needed. |
| SQLAlchemy | 2.0.x | ORM / query builder | 2.0 unified API. Provides abstraction so SQLite → PostgreSQL migration is a config change, not a rewrite. |
| APScheduler | 3.10.x | Feed sync scheduler | Embeds directly in the Flask process. Cron-style triggers. Persistent job store via SQLAlchemy. Avoids external cron dependency. |
| lxml | 5.x | XML/YML parsing | The standard Python XML library for production use. 5-10x faster than stdlib `xml.etree`. Handles malformed XML gracefully (common in supplier feeds). XPath support simplifies element extraction. |
| requests | 2.32.x | HTTP feed fetching | Battle-tested HTTP client. Handles redirects, timeouts, encoding detection. Use `requests` with explicit timeout + retry logic (not httpx — unnecessary complexity for sync fetching). |

### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| rapidfuzz | 3.x | Fuzzy string matching for brand+model | Always — this is the core of the matching algorithm. Pure Python with C extension speedup. Provides `fuzz.token_sort_ratio` which handles word-order differences ("стол холодильний" vs "холодильний стол"). |
| Jinja2 | 3.1.x | YML output generation | Bundled with Flask. Use Jinja2 templates to generate output YML — cleaner than string concatenation, avoids XML injection. |
| APScheduler | 3.10.x | Cron-style scheduling | See above. Use `BackgroundScheduler` with `SQLAlchemyJobStore` for persistence across restarts. |
| python-dotenv | 1.x | Environment variable management | Config (DB path, feed URLs, secret key) via `.env` file — keeps secrets out of code. |
| Werkzeug | 3.x | Bundled with Flask | Password hashing for basic admin auth. No need for separate auth library at this scale. |
| requests-cache | 1.2.x | Optional: HTTP response caching | Use if supplier feeds are slow or rate-limited. Caches responses with TTL. LOW confidence on exact version — verify on PyPI. |
| alembic | 1.13.x | Database migrations | Use with SQLAlchemy for schema changes during development. Avoids manual ALTER TABLE. |

### Development Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| uv | Fast Python package manager (replaces pip + venv) | `uv` from Astral is the 2025 standard for Python project setup. `uv sync` installs deps from lockfile in seconds. Use `pyproject.toml` as the single source of truth. |
| pyproject.toml | Project metadata + dependency declaration | Standard since PEP 517/518. Replaces `requirements.txt` for managed projects. |
| pytest | Test runner | Standard. Use for unit tests on the matching algorithm — the highest-risk component. |
| gunicorn | WSGI server for production | 1-2 worker processes sufficient for internal admin UI. Used behind nginx or directly on VPS. |
| nginx | Reverse proxy + static file serving | Serves the generated YML file at a public URL. Flask serves admin UI; nginx handles static output and SSL. |

---

## Installation

```bash
# Install uv (if not present)
pip install uv

# Initialize project
uv init labresta-sync
cd labresta-sync

# Core
uv add flask sqlalchemy alembic apscheduler lxml requests rapidfuzz python-dotenv

# Production server
uv add gunicorn

# Dev dependencies
uv add --dev pytest pytest-flask black ruff
```

---

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| Flask | FastAPI | If you need async feed fetching at scale (10+ suppliers fetched concurrently). FastAPI's async model would let you fetch all suppliers in parallel. For 5 suppliers, Flask + sequential requests is fine. |
| Flask | Django | If the project grows to multi-user, permissions, complex admin. Django admin is powerful but Django's weight is unjustified for a single-user sync tool. |
| SQLite | PostgreSQL | When multiple processes write simultaneously (won't happen here) or dataset exceeds ~50GB. SQLite WAL mode handles concurrent reads fine for this use case. |
| APScheduler | Celery + Redis | Celery is the right answer for high-volume task queues. For 5 suppliers every 4 hours, it's massive overkill. APScheduler embedded in Flask is 1/10th the operational complexity. |
| lxml | stdlib xml.etree | Use stdlib only for simple, well-formed XML. Supplier YML feeds often have encoding issues or minor malformation — lxml's error recovery handles these silently. |
| rapidfuzz | fuzzywuzzy | fuzzywuzzy is deprecated (the author created rapidfuzz as its replacement). rapidfuzz is 10-100x faster and has no `python-Levenshtein` dependency issues. |
| requests | httpx | httpx adds async complexity. For scheduled sync (not real-time), synchronous requests with timeout is simpler and sufficient. |
| gunicorn | uwsgi | uwsgi has more configuration surface area. gunicorn works out of the box with Flask and is the community default for Python web apps on Linux. |

---

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| fuzzywuzzy | Deprecated by its own author; slower; has a pip install warning about python-Levenshtein | rapidfuzz |
| xml.etree.ElementTree (stdlib) | No error recovery for malformed XML, no XPath, slower than lxml | lxml |
| Django | Heavyweight for a single-user internal tool; admin UI adds complexity rather than removing it | Flask |
| Celery | Requires Redis/RabbitMQ broker, separate worker process, monitoring. Massive ops burden for 5 scheduled jobs | APScheduler |
| PHP (for Path B) | No production-quality fuzzy matching library; XML parsing is verbose; scheduler requires system cron | Python |
| Node.js / Express | JavaScript XML parsing libraries are weaker than lxml; rapidfuzz has no Node equivalent with same quality | Python |
| Scrapy | Designed for web scraping, not structured feed processing. Adds unnecessary complexity | requests + lxml |

---

## Stack Patterns by Variant

**If shared hosting is a hard requirement (no VPS budget):**
- Use PHP 8.2+ with Composer
- XML parsing: `SimpleXML` (bundled) or `sabre/xml` via Composer
- Database: MySQL (provided by shared hosts) + PDO
- Fuzzy matching: Roll a custom PHP implementation using `similar_text()` + `levenshtein()` — no good library exists; matching quality will be lower
- Scheduler: cPanel cron job calling a PHP CLI script
- Web UI: Plain PHP with Bootstrap 5 — no framework needed at this size
- YML output: PHP's `DOMDocument` or Twig templates
- MEDIUM confidence: PHP path is viable but matching quality is the key risk

**If 10+ suppliers are added and concurrent fetching becomes important:**
- Add `httpx` with `asyncio` for concurrent feed fetching
- Or keep Flask + `concurrent.futures.ThreadPoolExecutor` for simpler parallelism without async rewrite
- APScheduler supports this without replacement

**If the app needs to be public-facing (not just internal admin):**
- Add Flask-Login for session management
- Add CSRF protection (Flask-WTF)
- Current recommendation assumes private/internal access only

---

## YML Format Reference (Yandex Market Language)

The output YML and input supplier feeds follow the Yandex Market Language standard, which prom.ua and Horoshop both support.

**Core structure (MEDIUM confidence — based on training data, verify against prom.ua docs):**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE yml_catalog SYSTEM "shops.dtd">
<yml_catalog date="2026-02-26 12:00">
  <shop>
    <name>LabResta</name>
    <company>LabResta</company>
    <url>https://prom.ua/...</url>
    <currencies>
      <currency id="EUR" rate="1"/>
    </currencies>
    <categories>
      <category id="1">Холодильне обладнання</category>
    </categories>
    <offers>
      <offer id="SUPPLIER_ID" available="true">
        <name>Назва товару</name>
        <price>1299.00</price>
        <currencyId>EUR</currencyId>
        <categoryId>1</categoryId>
        <vendor>Бренд</vendor>
        <model>Модель</model>
        <vendorCode>АРТИКУЛ</vendorCode>
        <description>Опис</description>
      </offer>
    </offers>
  </shop>
</yml_catalog>
```

**Key fields for this project:**
- `id` on `<offer>` — must match prom.ua's external ID or be stable across syncs
- `available` — `true`/`false` for stock status
- `price` — decimal, no currency symbol
- `currencyId` — must match a declared `<currency>`
- `vendor` + `model` — key for fuzzy matching strategy

**prom.ua import behavior (MEDIUM confidence):**
- prom.ua accepts YML at a URL, polls every 4 hours
- You select which fields to update on import (price, availability, name — choose price + availability only)
- prom.ua matches offers by the `id` attribute in `<offer>` — this is the external key
- The `id` in the output YML must be stable (use the prom.ua product ID you've matched to)

---

## Version Compatibility

| Package | Compatible With | Notes |
|---------|-----------------|-------|
| Flask 3.1.x | Python 3.8–3.13 | Flask 3.x dropped Python 3.7. Use 3.12 for performance. |
| SQLAlchemy 2.0.x | Flask 3.x via flask-sqlalchemy 3.1.x | Use `flask-sqlalchemy>=3.1` — earlier versions are SQLAlchemy 1.x only |
| APScheduler 3.10.x | Python 3.8+ | APScheduler 4.x is in pre-release as of 2025 — stick with 3.10.x stable |
| lxml 5.x | Python 3.8–3.13 | Pre-built wheels on PyPI for all platforms — no compilation needed |
| rapidfuzz 3.x | Python 3.8–3.13 | C extension auto-installed; falls back to pure Python if compiler unavailable |
| alembic 1.13.x | SQLAlchemy 2.0.x | alembic 1.13+ required for SQLAlchemy 2.0 full compatibility |

**Note on APScheduler 4.x:** APScheduler 4.x (async-first API) was in development/alpha as of mid-2025. Do NOT use 4.x — the API changed significantly. Pin to `apscheduler>=3.10,<4.0`.

---

## Shared Hosting Fallback (PHP Path) — Full Spec

If VPS is not an option, here is the complete PHP stack:

### PHP Core Technologies

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| PHP | 8.2+ | Runtime | 8.2 is standard on cPanel hosts in 2025. JIT, fibers, typed properties. |
| MySQL | 5.7+ / MariaDB 10.6+ | Database | Provided by all shared hosts. Use InnoDB tables. |
| Composer | 2.x | Dependency manager | Essential — do not manage PHP deps manually. |

### PHP Supporting Libraries

| Library | Composer Package | Purpose |
|---------|-----------------|---------|
| sabre/xml | `sabre/xml` ^4.0 | Clean XML read/write. Better API than DOMDocument. |
| Twig | `twig/twig` ^3.0 | YML template rendering. Separates logic from output. |
| Symfony Console | `symfony/console` ^7.0 | CLI runner for the sync command invoked by cron. |

**PHP fuzzy matching:** No production-quality library exists. Use PHP's built-in `similar_text()` + `levenshtein()` with a scoring function. Matching quality will be lower than Python's rapidfuzz — expect more manual corrections needed in the UI.

**PHP scheduler:** cPanel cron job → `php /home/user/labresta/artisan sync` (or similar CLI entry point) every 4 hours.

---

## Sources

- Training knowledge on Python ecosystem (Flask, SQLAlchemy, APScheduler, lxml, rapidfuzz) — MEDIUM confidence overall; versions verified as of training cutoff Aug 2025
- YML/Yandex Market Language format — MEDIUM confidence; verify current spec at https://yandex.ru/support/partnermarket/export/yml.html
- prom.ua import behavior — MEDIUM confidence; verify at https://support.prom.ua (Ukrainian)
- APScheduler 4.x pre-release status — LOW confidence on exact release date; pin to 3.10.x as safety measure
- rapidfuzz as replacement for fuzzywuzzy — HIGH confidence; documented by the author at https://github.com/maxbachmann/RapidFuzz

---

*Stack research for: LabResta Sync — supplier XML/YML price sync tool*
*Researched: 2026-02-26*
