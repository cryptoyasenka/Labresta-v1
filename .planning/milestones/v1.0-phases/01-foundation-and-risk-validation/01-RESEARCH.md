# Phase 1: Foundation and Risk Validation - Research

**Researched:** 2026-02-26
**Domain:** Flask/SQLite skeleton, prom.ua import behavior, supplier XML feed parsing, catalog CSV import, FTP upload
**Confidence:** MEDIUM (prom.ua docs blocked by 403 but verified via WebSearch summaries + third-party integrations; lxml/Flask verified via official docs)

## Summary

Phase 1 establishes the local Flask+SQLite application, resolves two blocking risks (prom.ua partial YML import behavior and MARESTO feed encoding), imports the prom.ua catalog, and provides basic supplier CRUD through a minimal web UI. The technical stack is well-understood: Flask app factory pattern, Flask-SQLAlchemy with SQLite, lxml for XML parsing, openpyxl/csv for catalog import, and Python's built-in ftplib for FTP upload. The two risks require manual verification against live services that cannot be fully automated.

The critical discovery from research: prom.ua import settings include a configurable option for products absent from the import file with four choices: "Leave unchanged", "Out of stock", "Hidden", or "Deleted". Setting this to "Leave unchanged" should protect the 5,950 unmanaged products. However, this MUST be verified with the actual 3-product test YML before building any automation -- the WebSearch-sourced information is MEDIUM confidence (prom.ua official docs return 403, so direct verification was not possible).

**Primary recommendation:** Build the Flask skeleton with app factory pattern and SQLite, implement catalog CSV/XLS import and supplier CRUD with minimal web UI, then execute the two manual risk spikes (prom.ua import mode test and MARESTO feed fetch) before proceeding to Phase 2.

<user_constraints>

## User Constraints (from CONTEXT.md)

### Locked Decisions
- App runs **locally on Windows PC** -- no VPS, no cloud
- Flask + SQLite run on the user's machine
- Generated YML file is **uploaded to shared hosting via FTP** (`labresta.com/feed.yml`)
- prom.ua fetches that static file automatically every 4h
- Web UI accessible at `localhost:5000` (admin only, no public exposure needed)
- Shared hosting: adm.tools account "labresta", domains `labresta.com` / `labresta.com.ua`
- Phase 1 includes a **minimal web UI** -- not CLI-only
- Required forms: add/edit supplier (URL, name, discount %), import catalog file, trigger manual sync
- User is not comfortable with CLI commands
- prom.ua catalog import supports **both CSV and XML** formats
- Import is **manual** in Phase 1: user downloads file from prom.ua, uploads through web UI
- Required fields to extract: product ID (prom.ua), name, brand, model, article number
- prom.ua import mode spike: upload a 3-product test YML to prom.ua and confirm unlisted products are left untouched (manual test against live store)
- MARESTO live feed: fetch `mrst.com.ua/include/price.xml`, confirm Cyrillic readable in SQLite, encoding detection for UTF-8 and Windows-1251
- FTP upload: push `feed.yml` to `labresta.com`, credentials in local config (not committed), configurable path

### Claude's Discretion
- Python project structure (directory layout, module names)
- SQLite schema details (exact column names, indexes)
- FTP library choice
- Flask app factory vs simple app pattern
- Windows Task Scheduler setup instructions (deferred to Phase 2)

### Deferred Ideas (OUT OF SCOPE)
- Auto-fetch prom.ua catalog via URL (if prom.ua provides one) -- investigate in Phase 2
- Windows Task Scheduler setup for auto-sync every 4h -- Phase 2
- Authentication / login for web UI -- Phase 4

</user_constraints>

<phase_requirements>

## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| AUTH-03 | Public YML feed URL accessible without authentication | FTP upload to shared hosting serves static file; no auth needed on hosting side. Flask route not required since file is on shared hosting, not served by Flask. |
| CATLG-01 | Admin can upload CSV export from prom.ua via UI | prom.ua exports XLS/CSV with known columns (see CSV Format section). Use openpyxl for XLS/XLSX, csv stdlib for CSV. Flask file upload form. |
| CATLG-02 | System parses and stores products (ID, name, brand, model, article) | Map prom.ua export columns: Ідентифікатор_товару -> external_id, Назва_позиції -> name, extract brand/model from name or characteristics. SQLite table with FTS for search. |
| SUPP-01 | Admin can add supplier: name, URL, discount % | Flask form + SQLAlchemy model. Minimal web UI with Bootstrap. |
| SUPP-02 | Admin can edit and enable/disable supplier | Same CRUD form with is_enabled boolean toggle. |
| SUPP-03 | System downloads and parses supplier YML feeds by URL | lxml XML parser with encoding detection (chardet fallback). requests with timeout for HTTP fetch. MARESTO adapter for field mapping. |
| SUPP-04 | System auto-detects feed encoding (UTF-8 / Windows-1251) | lxml handles encoding from XML declaration on raw bytes. chardet as fallback when declaration is missing or wrong. See Encoding Detection section. |

</phase_requirements>

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Flask | 3.1.x | Web framework, app factory | Minimal footprint for internal admin tool; official docs recommend app factory pattern |
| Flask-SQLAlchemy | 3.1.x | SQLAlchemy integration for Flask | Handles app context, session lifecycle; required for SQLAlchemy 2.0 compatibility |
| SQLAlchemy | 2.0.x | ORM / query builder | 2.0 unified API; abstracts SQLite so migration to Postgres is config-only |
| lxml | 5.x | XML/YML parsing | 5-10x faster than stdlib; handles encoding from XML declaration; recover mode for malformed feeds |
| requests | 2.32.x | HTTP feed fetching | Battle-tested; explicit timeout + retry; encoding detection from Content-Type |
| python-dotenv | 1.x | Config management | `.env` file for FTP credentials, DB path, secret key -- keeps secrets out of code |
| Jinja2 | 3.1.x | HTML templates | Bundled with Flask; server-rendered pages for the minimal UI |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| openpyxl | 3.1.x | Parse prom.ua XLS/XLSX exports | When user uploads .xlsx file from prom.ua admin |
| chardet | 5.x | Encoding detection fallback | When XML declaration is absent or HTTP Content-Type contradicts actual encoding |
| alembic | 1.13.x | Database migrations | Schema changes during development; avoids manual ALTER TABLE |
| Bootstrap | 5.3.x (CDN) | Minimal UI styling | Phase 1 forms and tables; no custom CSS needed |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| openpyxl | pandas | pandas is heavier (60MB+); openpyxl reads XLS/XLSX natively with zero extra deps |
| chardet | charset-normalizer | charset-normalizer is faster but chardet has better accuracy for single-byte Cyrillic encodings (cp1251, koi8-u) |
| ftplib (stdlib) | paramiko (SFTP) | ftplib is built-in Python, zero deps; use paramiko only if hosting requires SFTP |
| Bootstrap CDN | Tailwind | Bootstrap CDN requires zero build step; Phase 1 UI is throwaway scaffolding |
| Server-rendered Jinja2 | React/Vue SPA | Server-rendered is simpler for 3-4 forms; SPA is Phase 4 territory if needed |

**Installation:**
```bash
uv add flask flask-sqlalchemy sqlalchemy alembic lxml requests python-dotenv openpyxl chardet
uv add --dev pytest pytest-flask ruff
```

## Architecture Patterns

### Recommended Project Structure

```
labresta-sync/
├── app/
│   ├── __init__.py          # create_app() factory
│   ├── config.py            # Config classes (dev/prod)
│   ├── extensions.py        # db = SQLAlchemy(), shared extension instances
│   ├── models/
│   │   ├── __init__.py
│   │   ├── supplier.py      # Supplier model
│   │   ├── catalog.py       # PromProduct model (imported catalog)
│   │   └── supplier_product.py  # SupplierProduct model (parsed from feed)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── feed_fetcher.py  # HTTP fetch + encoding detection
│   │   ├── feed_parser.py   # lxml XML parse -> SupplierProduct
│   │   ├── catalog_import.py # CSV/XLS parse -> PromProduct
│   │   └── ftp_upload.py    # FTP upload to shared hosting
│   ├── views/
│   │   ├── __init__.py
│   │   ├── suppliers.py     # Supplier CRUD blueprint
│   │   ├── catalog.py       # Catalog import blueprint
│   │   └── main.py          # Index/dashboard blueprint
│   └── templates/
│       ├── base.html         # Bootstrap layout
│       ├── suppliers/
│       │   ├── list.html
│       │   └── form.html
│       └── catalog/
│           └── import.html
├── migrations/               # Alembic migrations
├── instance/                 # SQLite DB file (gitignored)
├── .env                      # FTP creds, SECRET_KEY (gitignored)
├── .env.example              # Template without secrets
├── pyproject.toml
└── tests/
```

### Pattern 1: App Factory with Deferred Extension Init

**What:** Extensions (SQLAlchemy, etc.) are instantiated at module level but bound to app inside `create_app()`.
**When to use:** Always -- enables testing with separate app instances.

```python
# app/extensions.py
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# app/__init__.py
from flask import Flask
from app.extensions import db

def create_app(config_name='default'):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(f'app.config.{config_name}')

    db.init_app(app)

    from app.views.suppliers import suppliers_bp
    from app.views.catalog import catalog_bp
    from app.views.main import main_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(suppliers_bp, url_prefix='/suppliers')
    app.register_blueprint(catalog_bp, url_prefix='/catalog')

    return app
```

Source: [Flask Application Factories docs](https://flask.palletsprojects.com/en/stable/patterns/appfactories/)

### Pattern 2: Encoding-Safe XML Parsing

**What:** Always pass raw bytes to lxml, never decode to string first. lxml reads the XML declaration encoding and handles it internally.
**When to use:** Every time a supplier feed is fetched.

```python
# app/services/feed_fetcher.py
import requests
from lxml import etree
import chardet

def fetch_and_parse_feed(url: str, timeout: int = 30) -> etree._Element:
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    raw_bytes = response.content  # bytes, NOT .text

    # Try lxml native parsing first (respects XML declaration encoding)
    try:
        root = etree.fromstring(raw_bytes)
        return root
    except etree.XMLSyntaxError:
        pass

    # Fallback: detect encoding with chardet, re-encode if needed
    detected = chardet.detect(raw_bytes)
    encoding = detected.get('encoding', 'utf-8')
    parser = etree.XMLParser(encoding=encoding, recover=True)
    root = etree.fromstring(raw_bytes, parser=parser)
    return root
```

Source: [lxml Parsing docs](https://lxml.de/parsing.html)

### Pattern 3: prom.ua Catalog Import (CSV/XLS)

**What:** Parse the prom.ua export file and extract product ID, name, brand, model, article number into the local database.
**When to use:** When user uploads catalog file through the web UI.

```python
# app/services/catalog_import.py
import csv
import io
from openpyxl import load_workbook

# prom.ua XLS/CSV column names (Ukrainian)
COLUMN_MAP = {
    'Ідентифікатор_товару': 'external_id',      # prom.ua product identifier
    'Назва_позиції': 'name',                      # product name
    'Код_товару': 'article',                       # article/SKU
    'Ціна': 'price',
    'Валюта': 'currency',
    # Brand and model are typically extracted from the name
    # or from characteristics columns
}

def parse_xlsx(file_path: str) -> list[dict]:
    wb = load_workbook(file_path, read_only=True)
    ws = wb['Export Products Sheet']
    headers = [cell.value for cell in next(ws.iter_rows(min_row=1, max_row=1))]
    products = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        product = dict(zip(headers, row))
        products.append(product)
    return products
```

### Anti-Patterns to Avoid

- **Decoding XML to string before parsing:** lxml must receive raw bytes to correctly handle encoding declarations. Passing `response.text` loses encoding info.
- **Hardcoding prom.ua column names without validation:** Column names may change between export versions. Validate headers on import and report unrecognized columns.
- **Storing FTP credentials in code or config.py:** Use `.env` file loaded via python-dotenv. Add `.env` to `.gitignore`.
- **Monolithic route handlers:** Keep Flask views thin -- delegate to service functions for parsing, importing, fetching.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| XML parsing with encoding | Custom byte-level parser | lxml with chardet fallback | Encoding edge cases (BOM, mislabeled headers) are endless |
| XLS/XLSX reading | Manual zip + XML parsing | openpyxl | XLS format is complex binary; XLSX is zipped XML with relationships |
| CSV parsing | Manual string.split(',') | Python csv stdlib | Handles quoting, escaping, newlines in fields |
| FTP upload | Raw socket programming | ftplib (stdlib) | Built into Python; handles binary transfer mode, passive mode |
| HTML templating | String concatenation | Jinja2 (Flask built-in) | Auto-escaping prevents XSS; template inheritance for layout |
| Database migrations | Manual ALTER TABLE | Alembic | Tracks migration history; generates diffs from model changes |

**Key insight:** Phase 1 is all about integrating well-understood libraries, not building novel algorithms. The risk is in the external services (prom.ua behavior, MARESTO encoding), not the code.

## Common Pitfalls

### Pitfall 1: Decoding XML Before Parsing (Encoding Corruption)

**What goes wrong:** Developer calls `response.text` (which decodes using requests' guessed encoding) then passes the string to lxml. If requests guesses wrong (e.g., assumes ISO-8859-1 when feed is cp1251), Cyrillic characters become mojibake. lxml then raises ValueError on a Unicode string with XML encoding declaration.
**Why it happens:** `response.text` is the natural first choice. The bug is invisible when testing with UTF-8 feeds.
**How to avoid:** Always use `response.content` (bytes). Let lxml read the XML declaration encoding. Add chardet as a fallback.
**Warning signs:** Product names in SQLite contain question marks, boxes, or Latin characters that look like Cyrillic.

### Pitfall 2: prom.ua Import Mode Misconfiguration

**What goes wrong:** The YML feed contains only 150 matched products. prom.ua's import setting for "products not in file" is set to "Hidden" or "Deleted" instead of "Leave unchanged." On first auto-import, 5,950 products disappear from the store.
**Why it happens:** The import mode setting is buried in prom.ua admin and may default to a destructive option. Nobody tests with a partial feed before enabling auto-import.
**How to avoid:** Phase 1 manual test with 3-product YML. Verify the exact setting. Document it with a screenshot. Never proceed to automation without this verification.
**Warning signs:** N/A -- this is a one-time catastrophic failure with no warning.

### Pitfall 3: prom.ua CSV Column Names Vary by Language/Version

**What goes wrong:** The parser expects `Назва_позиції` but the exported file has `Название_позиции` (Russian) or the column order differs between XLS and CSV exports.
**Why it happens:** prom.ua supports Ukrainian and Russian interfaces. The export column names match the UI language. Column names also have underscores and may vary slightly.
**How to avoid:** Normalize column headers on import (strip whitespace, lowercase). Map both Ukrainian and Russian variants. Validate that required columns exist before processing; show clear error if they don't.
**Warning signs:** Import silently creates products with NULL names or external IDs.

### Pitfall 4: SQLite on Windows Path Issues

**What goes wrong:** The SQLite database URI uses forward slashes but Windows paths have backslashes. Or the `instance/` folder doesn't exist on first run.
**Why it happens:** Flask's `instance_relative_config` and SQLAlchemy's URI parsing handle paths differently on Windows.
**How to avoid:** Use `os.path.join(app.instance_path, 'labresta.db')` for the database path. Ensure `create_app()` calls `os.makedirs(app.instance_path, exist_ok=True)`. Use `sqlite:///` with three slashes for relative paths.
**Warning signs:** "OperationalError: unable to open database file" on first run.

### Pitfall 5: FTP Upload Without Error Handling

**What goes wrong:** FTP upload fails silently (connection timeout, wrong credentials, disk full on hosting) and nobody knows the YML file on hosting is stale.
**Why it happens:** ftplib operations are wrapped in a try/except that swallows errors.
**How to avoid:** Log FTP upload result (success + timestamp, or failure + error). Store last successful upload timestamp. In future phases, show it on dashboard.
**Warning signs:** prom.ua reports "feed not updated" but no error is visible in the app.

## Code Examples

### Flask App Factory with SQLite on Windows

```python
# app/__init__.py
import os
from flask import Flask
from app.extensions import db

def create_app(config_name='default'):
    app = Flask(__name__, instance_relative_config=True)

    # Ensure instance folder exists (Windows-safe)
    os.makedirs(app.instance_path, exist_ok=True)

    # SQLite path using instance folder
    db_path = os.path.join(app.instance_path, 'labresta.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-me')

    db.init_app(app)

    # Register blueprints
    from app.views.main import main_bp
    from app.views.suppliers import suppliers_bp
    from app.views.catalog import catalog_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(suppliers_bp, url_prefix='/suppliers')
    app.register_blueprint(catalog_bp, url_prefix='/catalog')

    # Create tables on first run
    with app.app_context():
        db.create_all()

    return app
```

Source: [Flask Application Factories](https://flask.palletsprojects.com/en/stable/patterns/appfactories/)

### SQLite Schema (SQLAlchemy Models)

```python
# app/models/supplier.py
from app.extensions import db
from datetime import datetime, timezone

class Supplier(db.Model):
    __tablename__ = 'suppliers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    feed_url = db.Column(db.String(500), nullable=False)
    discount_percent = db.Column(db.Float, default=0.0)  # e.g. 15.0 for 15%
    is_enabled = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))
    last_fetched_at = db.Column(db.DateTime, nullable=True)
    last_fetch_status = db.Column(db.String(50), nullable=True)  # 'success', 'error'
    last_fetch_error = db.Column(db.Text, nullable=True)

# app/models/catalog.py
class PromProduct(db.Model):
    __tablename__ = 'prom_products'

    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.String(255), unique=True, nullable=False)  # Ідентифікатор_товару
    name = db.Column(db.String(500), nullable=False)                       # Назва_позиції
    brand = db.Column(db.String(200), nullable=True)
    model = db.Column(db.String(200), nullable=True)
    article = db.Column(db.String(255), nullable=True)                     # Код_товару
    price = db.Column(db.Integer, nullable=True)                           # cents (integer)
    currency = db.Column(db.String(10), default='EUR')
    imported_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        db.Index('ix_prom_products_brand', 'brand'),
        db.Index('ix_prom_products_name', 'name'),
    )

# app/models/supplier_product.py
class SupplierProduct(db.Model):
    __tablename__ = 'supplier_products'

    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)
    external_id = db.Column(db.String(255), nullable=False)  # offer id from feed
    name = db.Column(db.String(500), nullable=False)
    brand = db.Column(db.String(200), nullable=True)          # <vendor> from YML
    model = db.Column(db.String(200), nullable=True)
    article = db.Column(db.String(255), nullable=True)        # <vendorCode>
    price_cents = db.Column(db.Integer, nullable=True)        # retail price in cents
    currency = db.Column(db.String(10), default='EUR')
    available = db.Column(db.Boolean, default=True)
    last_seen_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    supplier = db.relationship('Supplier', backref='products')

    __table_args__ = (
        db.UniqueConstraint('supplier_id', 'external_id', name='uq_supplier_product'),
    )
```

### FTP Upload

```python
# app/services/ftp_upload.py
import ftplib
import os

def upload_to_ftp(local_path: str, remote_path: str,
                  host: str, username: str, password: str) -> dict:
    """Upload a file to shared hosting via FTP.

    Returns dict with 'success' bool and 'error' string if failed.
    """
    try:
        with ftplib.FTP(host, timeout=30) as ftp:
            ftp.login(username, password)
            # Navigate to remote directory
            remote_dir = os.path.dirname(remote_path)
            if remote_dir:
                ftp.cwd(remote_dir)
            # Upload in binary mode
            filename = os.path.basename(remote_path)
            with open(local_path, 'rb') as f:
                ftp.storbinary(f'STOR {filename}', f)
            return {'success': True, 'error': None}
    except Exception as e:
        return {'success': False, 'error': str(e)}
```

Source: [Python ftplib docs](https://docs.python.org/3/library/ftplib.html)

### Catalog CSV/XLS Import with Column Name Normalization

```python
# app/services/catalog_import.py
import csv
import io
from openpyxl import load_workbook

# Both Ukrainian and Russian column name variants
COLUMN_ALIASES = {
    # external_id
    'ідентифікатор_товару': 'external_id',
    'идентификатор_товара': 'external_id',
    # name
    'назва_позиції': 'name',
    'название_позиции': 'name',
    # article
    'код_товару': 'article',
    'код_товара': 'article',
    # price
    'ціна': 'price',
    'цена': 'price',
    # currency
    'валюта': 'currency',
}

def normalize_header(header: str) -> str:
    """Lowercase, strip whitespace, normalize for lookup."""
    return header.strip().lower()

def map_headers(raw_headers: list[str]) -> dict[int, str]:
    """Map column indices to internal field names."""
    mapping = {}
    for i, h in enumerate(raw_headers):
        normalized = normalize_header(h)
        if normalized in COLUMN_ALIASES:
            mapping[i] = COLUMN_ALIASES[normalized]
    return mapping
```

## prom.ua Import Behavior -- Research Findings

### How prom.ua Matches Products During YML Import

**Confidence: MEDIUM** (verified via WebSearch summaries; prom.ua official docs return 403)

prom.ua matches products in a YML import file to existing products using the `id` attribute on `<offer>` elements. This `id` maps to the "Ідентифікатор_товару" (external_id) field in prom.ua's internal database. This field is NOT visible in the prom.ua web interface -- it can only be viewed/changed via XLS export/import.

**Critical implication:** The output YML must use the prom.ua product's `Ідентифікатор_товару` as the `offer id`, NOT the supplier's product ID. This is how prom.ua knows which existing product to update.

### Import Settings for Products Absent from File

**Confidence: MEDIUM** (consistent across multiple WebSearch sources)

When configuring YML import, prom.ua offers four options for products published on the site but absent from the import file:

1. **"Залишити без змін"** (Leave unchanged) -- products not in the file are untouched
2. **"Немає в наявності"** (Out of stock) -- absent products marked out of stock
3. **"Приховані"** (Hidden) -- absent products moved to hidden status
4. **"Видалені"** (Deleted) -- absent products moved to deleted status

**For this project: MUST be set to "Залишити без змін" (Leave unchanged).** This is the only safe option for a partial feed covering ~150 of 6,100 products.

### Selective Field Updates

prom.ua allows choosing which fields to update during import:
- Назва (Name)
- Ціна (Price)
- Фото (Photo)
- Наявність (Availability)
- Кількість (Quantity)
- Опис (Description)
- Група (Category)
- Ключові слова (Keywords)
- Характеристики (Characteristics)
- Знижки (Discounts)

**For this project: select ONLY Ціна (Price) and Наявність (Availability).** Do not update name, description, or other fields -- those are manually managed on prom.ua.

### Auto-Update from URL

- prom.ua fetches the YML file from a URL automatically
- Key fields (price, availability) update every 4 hours
- Other fields (name, description) update once daily (at night)
- Only ONE auto-update URL link is supported
- Additional links can only be updated manually

### The Blocking Risk Test Procedure

1. Export current catalog from prom.ua to XLS -- note product count and a few specific products NOT in the test YML
2. Create a minimal YML file with exactly 3 existing prom.ua products (using their real Ідентифікатор_товару as offer id)
3. In prom.ua admin, go to Import settings
4. Set "Products absent from file" to "Залишити без змін" (Leave unchanged)
5. Select only "Ціна" and "Наявність" for field updates
6. Upload the 3-product YML manually
7. After import completes, verify: the 3 products updated correctly AND all other products remain unchanged
8. Document the result with screenshots

## prom.ua CSV/XLS Export Format

### Known Column Names

**Confidence: MEDIUM-HIGH** (verified via Elbuz integration docs + WebSearch)

The export file contains two sheets (XLS/XLSX) or a single flat file (CSV):

**Export Products Sheet columns:**
- `Код_товару` -- Product code / article / SKU
- `Назва_позиції` -- Product name (max 100 chars)
- `Ключові_слова` -- Search queries (max 255 chars)
- `Опис` -- Description (max 12,160 chars)
- `Тип_товару` -- Product type
- `Ціна` -- Price
- `Ціна_від` -- Price from
- `Валюта` -- Currency (EUR, UAH, USD, etc.)
- `Одиниця_виміру` -- Unit of measurement
- `Мінімальна_кількість_замовлення` -- Minimum order quantity
- `Оптова_ціна` -- Wholesale price
- `Мінімальне_замовлення_опт` -- Minimum wholesale order
- `Кількість` -- Quantity
- `Посилання_зображення` -- Image link
- `Наявність` -- Availability
- `Знижка` -- Discount
- `Виробник` -- Manufacturer / Brand
- `Країна_виробник` -- Country of manufacture
- `Ідентифікатор_товару` -- Product identifier (external_id, up to 255 alphanumeric, REQUIRED for matching)
- `Унікальний_ідентифікатор` -- Unique identifier (prom.ua internal numeric ID from URL, auto-generated)
- `Назва_Характеристики` / `Розмірність_Характеристики` / `Значення_Характеристики` -- Characteristics blocks (repeating)

**Required fields for import:** Назва_позиції, Ключові_слова, Опис, Ідентифікатор_товару

**For Phase 1 extraction (CATLG-02), map:**
- `Ідентифікатор_товару` -> `external_id` (PRIMARY KEY for matching in Phase 3 YML output)
- `Назва_позиції` -> `name`
- `Виробник` -> `brand` (may be empty -- fallback: extract from name)
- `Код_товару` -> `article`
- `Ціна` -> `price` (store as integer cents)
- Brand + model extraction from `Назва_позиції` is a Phase 2 concern (fuzzy matching)

**Note:** Column names may appear in Russian (`Название_позиции`, `Идентификатор_товара`) depending on the user's prom.ua language setting. The import service must handle both variants.

## MARESTO Feed -- Research Findings

### What We Know

**Confidence: LOW** (could not fetch the live URL; no documentation found online)

- Feed URL: `https://mrst.com.ua/include/price.xml`
- Expected format: YML (Yandex Market Language) based on the `.xml` extension and prom.ua ecosystem
- Expected encoding: likely UTF-8 or Windows-1251 (common for Ukrainian suppliers)
- Expected fields (from YML standard): `<offer id="..." available="true/false">`, `<name>`, `<price>`, `<vendor>`, `<model>`, `<vendorCode>`, `<currencyId>`

### What We Don't Know (Must Verify in Phase 1)

1. **Actual encoding** -- could be UTF-8, Windows-1251, or KOI8-U
2. **Actual field names** -- may use non-standard element names
3. **Category structure** -- may or may not include categories
4. **Product count** -- expected ~150 but unverified
5. **Feed availability** -- URL may require specific User-Agent or may be rate-limited

### Day 1 Verification Task

Write a standalone Python script that:
1. Fetches `https://mrst.com.ua/include/price.xml` with requests (raw bytes)
2. Prints the first 200 bytes (to check encoding declaration and BOM)
3. Parses with lxml (bytes mode)
4. Prints 3 sample product names (verifying Cyrillic renders correctly)
5. Lists all unique element names within `<offer>` tags (to map the actual schema)
6. Stores results in SQLite and re-reads to confirm no encoding corruption

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| SQLAlchemy 1.x query style | SQLAlchemy 2.0 select() style | 2023 | Use `db.session.execute(select(Model))` not `Model.query` |
| Flask-SQLAlchemy `Model.query` | `db.session.execute(select(Model))` | Flask-SQLAlchemy 3.1 | Old style still works but new style is recommended |
| requirements.txt | pyproject.toml + uv | 2024-2025 | Use `uv add` not `pip install`; single source of truth |
| APScheduler 3.x | APScheduler 3.10.x (pin < 4.0) | 2025 | 4.x is async-first, API changed; stay on 3.10.x |
| `app.run(debug=True)` | `flask --app run` CLI | Flask 2.3+ | Use CLI for development; `app.run()` only in `__main__` guard |

## Open Questions

1. **MARESTO feed actual schema and encoding**
   - What we know: URL is `mrst.com.ua/include/price.xml`, likely YML format
   - What's unclear: Actual encoding, field names, product count, availability
   - Recommendation: Day 1 task -- fetch and inspect the live feed. Cannot proceed with parser implementation without this.

2. **prom.ua import mode behavior with auto-update URL**
   - What we know: Setting exists for "leave unchanged" for absent products
   - What's unclear: Whether this setting applies identically for manual upload vs. auto-update from URL. The prom.ua limitation note says "for multiple links, 'not in file = leave unchanged' does not work correctly."
   - Recommendation: Test manual upload first. Verify auto-update behavior separately before enabling it in Phase 3.

3. **prom.ua export column names -- exact list**
   - What we know: Key columns identified from integration docs
   - What's unclear: Whether the user's prom.ua account exports in Ukrainian or Russian column names
   - Recommendation: Ask user to export a sample file before building the parser. Handle both language variants.

4. **Brand extraction from product names**
   - What we know: The `Виробник` (Manufacturer) column may be empty for some products. Brand + model is often embedded in `Назва_позиції`.
   - What's unclear: What percentage of products have the Виробник field filled
   - Recommendation: Phase 1 imports what's available. Phase 2 tackles name parsing for brand/model extraction during matching.

5. **FTP or FTPS on shared hosting**
   - What we know: adm.tools hosting provides FTP access
   - What's unclear: Whether plain FTP or FTPS (FTP over TLS) is required/available
   - Recommendation: Try plain FTP first (ftplib). If blocked, use `ftplib.FTP_TLS` instead.

## Sources

### Primary (HIGH confidence)
- [Flask Application Factories](https://flask.palletsprojects.com/en/stable/patterns/appfactories/) -- app factory pattern, blueprint registration
- [lxml Parsing documentation](https://lxml.de/parsing.html) -- encoding handling, bytes vs string, recover mode, XMLParser options
- [Python ftplib documentation](https://docs.python.org/3/library/ftplib.html) -- FTP upload, binary mode, FTP_TLS
- [Flask-SQLAlchemy docs](https://flask-sqlalchemy.palletsprojects.com/) -- SQLAlchemy 2.0 integration with Flask

### Secondary (MEDIUM confidence)
- [prom.ua import docs (WebSearch summary)](https://support.prom.ua/hc/uk/articles/360004963478) -- import settings, absent product handling (4 options), selective field updates. Note: direct access returned 403; information from WebSearch extraction.
- [prom.ua YML format docs (WebSearch summary)](https://support.prom.ua/hc/uk/articles/360004963538) -- YML structure requirements. Note: 403 on direct access.
- [prom.ua product update docs (WebSearch summary)](https://support.prom.ua/hc/uk/articles/360005438598) -- auto-update frequency (4h for key fields), force update option.
- [Elbuz prom.ua integration](https://elbuz.com/en/docs-export-prom-tiu) -- XLS/CSV column names, required fields, identifier behavior.
- [SalesDrive prom.ua external_id guide](https://salesdrive.ua/blog/prom-external-id/) -- how Ідентифікатор_товару maps to offer id in YML.
- [TradeEVO prom.ua import guide](https://tradeevo.com/import-ta-avtomatychne-onovlennya-tovariv-na-prom/) -- step-by-step import with settings.

### Tertiary (LOW confidence)
- MARESTO feed structure -- no documentation found; must be verified by fetching the live URL
- prom.ua behavior with multiple auto-update links -- single source mentions limitation; needs verification

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- Flask, SQLAlchemy, lxml, ftplib are stable, well-documented libraries
- Architecture: HIGH -- app factory + blueprints is the documented Flask pattern
- prom.ua import behavior: MEDIUM -- consistent across multiple third-party sources but official docs inaccessible (403)
- MARESTO feed: LOW -- no documentation available; must verify against live URL
- Pitfalls: MEDIUM -- based on domain expertise + verified patterns from prior research

**Research date:** 2026-02-26
**Valid until:** 2026-03-26 (stable domain; prom.ua import settings unlikely to change)
