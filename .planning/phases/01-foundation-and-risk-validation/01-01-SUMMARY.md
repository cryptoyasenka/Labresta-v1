---
phase: 01-foundation-and-risk-validation
plan: 01
subsystem: ui
tags: [flask, sqlalchemy, sqlite, bootstrap, crud]

# Dependency graph
requires: []
provides:
  - Flask app factory with blueprint registration
  - Supplier, PromProduct, SupplierProduct SQLAlchemy models
  - Supplier CRUD web UI (add, edit, toggle enable/disable)
  - Bootstrap 5 base template with navbar
  - Project skeleton with uv dependency management
affects: [01-02, 01-03, 01-04, 02-feed-ingestion]

# Tech tracking
tech-stack:
  added: [flask, flask-sqlalchemy, sqlalchemy, alembic, lxml, requests, python-dotenv, openpyxl, chardet, bootstrap-5.3-cdn]
  patterns: [app-factory, blueprint-registration, sqlalchemy-2.0-select, prg-pattern, server-side-validation]

key-files:
  created:
    - app/__init__.py
    - app/config.py
    - app/extensions.py
    - app/models/supplier.py
    - app/models/catalog.py
    - app/models/supplier_product.py
    - app/views/suppliers.py
    - app/views/catalog.py
    - app/views/main.py
    - app/templates/base.html
    - app/templates/index.html
    - app/templates/suppliers/list.html
    - app/templates/suppliers/form.html
    - app/templates/catalog/index.html
    - pyproject.toml
    - run.py
    - .env.example
  modified:
    - .gitignore

key-decisions:
  - "Used hatchling build backend with explicit packages=['app'] for uv compatibility"
  - "Model imports placed before db.create_all() in app factory to ensure table registration"
  - "Catalog blueprint created as placeholder to prevent import errors in create_app"

patterns-established:
  - "App factory pattern: create_app() in app/__init__.py with deferred extension init"
  - "Blueprint pattern: each view module exports a blueprint, registered in create_app"
  - "SQLAlchemy 2.0 style: db.session.execute(select(Model)) not Model.query"
  - "Timezone-aware timestamps: datetime.now(timezone.utc) for all defaults"
  - "PRG pattern: all POST routes redirect after success"

requirements-completed: [SUPP-01, SUPP-02]

# Metrics
duration: 5min
completed: 2026-02-26
---

# Phase 1 Plan 1: Flask Skeleton and Supplier CRUD Summary

**Flask app factory with SQLite, 3 ORM models (Supplier, PromProduct, SupplierProduct), and working supplier CRUD via Bootstrap 5 web UI**

## Performance

- **Duration:** 5 min
- **Started:** 2026-02-26T18:26:56Z
- **Completed:** 2026-02-26T18:31:36Z
- **Tasks:** 2
- **Files modified:** 18

## Accomplishments
- Flask app factory with blueprint registration, SQLite database, and instance path safety for Windows
- Three database models matching the research schema: Supplier, PromProduct, SupplierProduct with proper indexes and constraints
- Full supplier CRUD: list (with status badges), add, edit, toggle enable/disable -- all with server-side validation
- Bootstrap 5 base layout with responsive navbar, flash messages, and card-based index page

## Task Commits

Each task was committed atomically:

1. **Task 1: Create project skeleton with Flask app factory, config, and all DB models** - `991f07d` (feat)
2. **Task 2: Build supplier CRUD views and Bootstrap templates** - `bb95aee` (feat)

## Files Created/Modified
- `pyproject.toml` - Project metadata, dependencies, hatch build config
- `app/__init__.py` - Flask app factory with create_app()
- `app/config.py` - DefaultConfig with .env support, SQLite URI, FTP placeholders
- `app/extensions.py` - Shared SQLAlchemy instance
- `app/models/supplier.py` - Supplier model (name, feed_url, discount, enabled status, fetch tracking)
- `app/models/catalog.py` - PromProduct model (external_id, name, brand, model, article, price in cents)
- `app/models/supplier_product.py` - SupplierProduct model (supplier FK, unique constraint on supplier_id+external_id)
- `app/views/suppliers.py` - Supplier CRUD blueprint with validation
- `app/views/catalog.py` - Catalog placeholder blueprint
- `app/views/main.py` - Index page blueprint
- `app/templates/base.html` - Bootstrap 5 layout with navbar and flash messages
- `app/templates/index.html` - Welcome page with navigation cards
- `app/templates/suppliers/list.html` - Supplier table with status badges and actions
- `app/templates/suppliers/form.html` - Add/edit form with validation errors
- `app/templates/catalog/index.html` - Coming soon placeholder
- `.env.example` - Config template with all env vars documented
- `.gitignore` - Updated with instance/, .env, __pycache__, .venv
- `run.py` - Development server entry point
- `uv.lock` - Dependency lock file

## Decisions Made
- Used hatchling with explicit `packages = ["app"]` since project name (labresta-sync) does not match the package directory (app)
- Model imports placed in create_app before db.create_all() using `from app.models import ...` to avoid name shadowing (`import app.models` would rebind the local `app` variable)
- Created catalog blueprint placeholder in Task 1 (not Task 2) since create_app() imports it -- deviation Rule 3 (blocking issue)

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Created supplier and catalog blueprint placeholders in Task 1**
- **Found during:** Task 1 (verification step)
- **Issue:** create_app() imports suppliers_bp and catalog_bp, but those files were planned for Task 2. App failed to start.
- **Fix:** Created minimal placeholder blueprints in Task 1, replaced with full implementations in Task 2.
- **Files modified:** app/views/suppliers.py, app/views/catalog.py
- **Verification:** Flask app creates without errors
- **Committed in:** 991f07d (Task 1 commit)

**2. [Rule 1 - Bug] Fixed model import shadowing local `app` variable**
- **Found during:** Task 1 (verification step)
- **Issue:** `import app.models` inside create_app() rebound the local `app` variable (Flask instance) to the `app` module, causing create_app() to return the module instead of the Flask app.
- **Fix:** Changed to `from app.models import Supplier, PromProduct, SupplierProduct` which does not shadow the local variable.
- **Files modified:** app/__init__.py
- **Verification:** create_app() returns Flask instance, all tables created
- **Committed in:** 991f07d (Task 1 commit)

**3. [Rule 3 - Blocking] Added hatch build targets configuration**
- **Found during:** Task 1 (uv sync step)
- **Issue:** hatchling could not find package directory -- project name `labresta-sync` maps to `labresta_sync` but code is in `app/`.
- **Fix:** Added `[tool.hatch.build.targets.wheel] packages = ["app"]` to pyproject.toml.
- **Files modified:** pyproject.toml
- **Verification:** `uv sync` completes, 25 packages installed
- **Committed in:** 991f07d (Task 1 commit)

---

**Total deviations:** 3 auto-fixed (1 bug, 2 blocking)
**Impact on plan:** All fixes were necessary for the app to start. No scope creep.

## Issues Encountered
- Python 3.14 is installed on the system; uv was not pre-installed. Installed uv via `pip install uv` and ran via `python -m uv`. All dependencies resolved without compatibility issues on Python 3.14.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Flask app runs on localhost:5000 with supplier CRUD functional
- Database schema ready for catalog import (Plan 02) and feed parsing (Plan 03/04)
- Bootstrap UI template established for all future views
- All three tables (suppliers, prom_products, supplier_products) created and verified

## Self-Check: PASSED

- All 17 created files verified present on disk
- Commit 991f07d (Task 1) verified in git log
- Commit bb95aee (Task 2) verified in git log

---
*Phase: 01-foundation-and-risk-validation*
*Completed: 2026-02-26*
