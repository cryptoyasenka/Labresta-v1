# Phase 4: Management UI and Authentication - Research

**Researched:** 2026-02-28
**Domain:** Flask web UI, session-based authentication, dashboard with real-time updates
**Confidence:** HIGH

## Summary

Phase 4 adds a full management web UI to the existing headless sync pipeline. The project already uses Flask + Jinja2 + Bootstrap 5 (CDN) with a working `base.html` template, several blueprints (main, suppliers, catalog, feed), and SQLAlchemy models that include `ProductMatch.confirmed_by` (a string field designed for Phase 4 usernames). The existing `telegram_notifier.py` already sends messages via the Telegram Bot API using `requests` — the notification system needs to be extended, not built from scratch.

The standard Flask auth stack (Flask-Login + werkzeug password hashing + Flask-WTF CSRF) is mature, well-documented, and already partially supported by the project's existing `SECRET_KEY` configuration. The UI requires server-rendered pages (Jinja2 templates with Bootstrap 5), client-side interactivity for tables (sorting, filtering, pagination, bulk actions), Chart.js for dashboard graphs, Split.js for resizable panels, and either AJAX polling or SSE for auto-refresh.

**Primary recommendation:** Use Flask-Login for session management, werkzeug.security for password hashing, Flask-WTF for CSRF and forms, Chart.js 4 for dashboard charts, Split.js for resizable panels, and simple AJAX polling (setInterval + fetch) for dashboard auto-refresh. Avoid SSE complexity given SQLite backend and single-process deployment.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- Bootstrap 5 as CSS framework (CDN, works well with Flask/Jinja)
- Spacious, clean style — more whitespace, larger elements
- Light theme only (no dark mode)
- Top navbar for navigation, full-width content
- Resizable panels — operator can resize windows
- Scrollbars for long lists
- Adaptive content stretching to screen size
- Match review screen: table format with columns (supplier name | prom.ua catalog name | supplier price | calculated prom.ua price | confidence badge + percentage | status | last action who/when | actions)
- Confidence shown two ways: color badges (green High, yellow Medium, red Low) + numeric score (85%)
- Checkboxes per row for bulk actions (confirm/reject selected)
- Granular manual approve and configuration per match
- Pagination: 25/50/100 rows per page
- Default sort: by confidence (Low first — needs attention)
- Sort by click on any column header
- Full filter set: by status (pending/confirmed/rejected), by confidence (High/Med/Low), search by name
- Confirmation dialog before each action (confirm/reject match)
- Badge with pending review count in navigation (like unread)
- Diff highlighting of name differences — separate toggle button (on/off)
- Rejection flow: product goes to "unmatched" + system tries finding another pair
- Manual match via modal: click "Match manually" -> modal with catalog search + dropdown
- Configurable columns in modal: operator picks what to show (name, price, description, photo)
- "Remember match for future" — save pair for automatic application
- Table of remembered match rules: view, edit, delete
- Full manual product management (delete, force price, mark out-of-stock, set any status)
- Automatic modes work in parallel with manual management
- Export match table to CSV and Excel (respecting current filters)
- "Out of stock" badge in table + separate filter/list for out-of-stock products
- "Changed" indicator when supplier updated photo/description + separate changes section
- Old/new value diff view
- Notifications about new supplier products by configurable criteria (category, price, keywords)
- Notifications in UI and via Telegram
- Operator can enable/disable Telegram notifications in settings
- Dashboard: top widget cards (last sync time, match count, unmatched, pending review, errors)
- Configurable widgets: operator can add/remove widgets
- Sync progress bar with exact numbers (processed from supplier file, processed to prom.ua export, unmatched, full process stats)
- Countdown timer to next auto-sync
- Simple trend charts (matches, prices over last N days)
- Sync settings right on dashboard (auto-sync interval, matching thresholds) — collapsible panel
- Auto-refresh data (polling) + manual refresh button
- Clean event feed at bottom (errors, syncs, changes)
- Fine-tuning: operator can change match parameters, switch manual/automatic mode
- Separate logs section (detailed logs with filters)
- Separate sections for each aspect: products, matches, syncs, settings
- Each section with full detail beyond dashboard summary
- Email + password auth (simple login, no 2FA)
- Multiple users with roles: admin and operator
- Multiple admins — each can change access rights
- Account creation only by admin (no self-registration)
- Permanent session — logout only by button
- "Remember me" checkbox for returning to current session
- Auto-save state on unexpected shutdown (power outage)
- Full CRUD for user management: create, edit, deactivate, change password, assign role
- Show user activity: last login + processed match count
- Public YML URL accessible without auth

### Claude's Discretion
- Specific charting library (Chart.js or analog)
- Polling implementation (interval, SSE vs AJAX)
- Event feed design
- Loading skeletons
- Exact dashboard card layout
- Panel resize implementation
- Technical implementation of session auto-save
- Notification system implementation (Telegram bot API)

### Deferred Ideas (OUT OF SCOPE)
- Improving matching algorithm (backend Phase 3) — reduce false match count
- Tracking photo/description changes in DB — backend detection logic (Phase 4 shows UI, but backend detection may require separate work)
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| AUTH-01 | Admin can log in with email and password | Flask-Login + werkzeug.security password hashing; User model with `set_password`/`check_password` |
| AUTH-02 | System supports 2-3 separate accounts (different logins) | User model with roles (admin/operator); Flask-Login `UserMixin`; admin-only user management |
| DASH-01 | Dashboard shows sync status: when ran, how many updated, errors | SyncRun model already tracks all this data; query latest SyncRun per supplier |
| DASH-02 | Dashboard shows counters: matched / unmatched / removed from sale | Aggregate queries on ProductMatch (status counts) and SupplierProduct (available=False) |
| DASH-03 | Admin can trigger manual sync from dashboard | Existing `run_full_sync()` in sync_pipeline.py; AJAX endpoint to trigger + progress reporting |
| DASH-04 | Sync journal: when, what changed (prices, availability) | SyncRun model already logs runs; extend with per-product change log or use existing fields |
| DASH-05 | Admin can view all supplier products with current prices and availability | SupplierProduct query with pagination, sorting, filtering |
| MATCH-02 | Admin can review proposals and confirm / reject / specify manually | Match review table with ProductMatch status transitions; modal for manual match |
| MATCH-04 | Admin sees prom.ua products without match — to decide whether to remove | Query PromProduct LEFT JOIN ProductMatch WHERE match is NULL |
| MATCH-05 | Admin sees supplier products (known brands) not in store — to decide whether to add | Query SupplierProduct with no confirmed match and available=True |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Flask-Login | >=0.6.3 | Session management, `@login_required`, user loading | De facto standard for Flask auth; already compatible with project's blueprint pattern |
| Flask-WTF | >=1.2 | CSRF protection, form validation | Integrates with WTForms; `CSRFProtect` for global CSRF on all POST/DELETE |
| werkzeug.security | (bundled with Flask) | `generate_password_hash` / `check_password_hash` | Already a dependency; uses PBKDF2:SHA256 by default — no extra dependency needed |
| Chart.js | 4.x (CDN) | Dashboard trend charts | Lightweight (60KB gzipped), no build step, works directly with Jinja2 data injection |
| Split.js | 1.6.x (CDN) | Resizable panels | 2KB gzipped, zero dependencies, works with CSS flexbox layouts |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| openpyxl | >=3.1 (already installed) | Excel export | CSV/XLSX export of match tables |
| requests | >=2.32 (already installed) | Telegram Bot API calls | Notification system (already used in `telegram_notifier.py`) |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Chart.js | Lightweight Charts (TradingView) | More complex, overkill for simple trend charts |
| Split.js | CSS resize property | Less control, no programmatic API, poor cross-browser |
| AJAX polling | Server-Sent Events (SSE) | SSE requires async workers (gunicorn+gevent); AJAX polling simpler with SQLite single-process |
| werkzeug PBKDF2 | bcrypt / argon2 | Stronger but adds dependency; PBKDF2 sufficient for admin-only panel |
| Flask-WTF forms | Manual HTML forms | Loses CSRF protection, validation; not worth the risk |

**Installation:**
```bash
uv add flask-login flask-wtf
```

Chart.js and Split.js loaded via CDN in templates — no Python package needed.

## Architecture Patterns

### Recommended Project Structure
```
app/
├── __init__.py              # create_app (add login_manager, csrf init)
├── extensions.py            # db, login_manager, csrf instances
├── config.py                # Add session config, remember cookie duration
├── models/
│   ├── user.py              # NEW: User model with UserMixin
│   ├── match_rule.py        # NEW: Remembered match rules
│   ├── notification_rule.py # NEW: Notification criteria
│   ├── ...existing models...
├── views/
│   ├── auth.py              # NEW: login/logout blueprint
│   ├── dashboard.py         # NEW: dashboard blueprint
│   ├── matches.py           # NEW: match review blueprint
│   ├── products.py          # NEW: product management blueprint
│   ├── logs.py              # NEW: logs blueprint
│   ├── settings.py          # NEW: settings/user management blueprint
│   ├── feed.py              # EXISTING: public YML — NO login_required
│   ├── ...existing views...
├── services/
│   ├── telegram_notifier.py # EXTEND: add notification rule checking
│   ├── notification_service.py # NEW: notification rule engine
│   ├── export_service.py    # NEW: CSV/XLSX export logic
│   ├── ...existing services...
├── templates/
│   ├── base.html            # MODIFY: add login state, nav badges, auth nav items
│   ├── auth/
│   │   ├── login.html       # Login form
│   ├── dashboard/
│   │   ├── index.html       # Main dashboard with widgets
│   ├── matches/
│   │   ├── review.html      # Match review table
│   │   ├── rules.html       # Remembered match rules table
│   │   ├── unmatched.html   # Products without matches
│   ├── products/
│   │   ├── supplier.html    # Supplier products list
│   │   ├── catalog.html     # Catalog products list
│   ├── settings/
│   │   ├── users.html       # User management
│   │   ├── sync.html        # Sync settings
│   │   ├── notifications.html # Notification rules
│   ├── logs/
│   │   ├── index.html       # Log viewer
├── static/
│   ├── css/
│   │   ├── app.css          # Custom styles (spacious layout, badges)
│   ├── js/
│   │   ├── dashboard.js     # Polling, chart init, countdown timer
│   │   ├── matches.js       # Table interactions, bulk actions, diff toggle
│   │   ├── common.js        # Confirmation dialogs, CSRF token helper
```

### Pattern 1: Flask-Login Integration with Application Factory
**What:** Initialize Flask-Login in the application factory alongside existing extensions.
**When to use:** All authenticated views.
**Example:**
```python
# app/extensions.py
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Please log in to access this page."

csrf = CSRFProtect()

# app/__init__.py (additions to create_app)
from app.extensions import login_manager, csrf

login_manager.init_app(app)
csrf.init_app(app)

# User loader callback
from app.models.user import User

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
```

### Pattern 2: User Model with Password Hashing
**What:** SQLAlchemy User model implementing Flask-Login's UserMixin.
**When to use:** Authentication and authorization.
**Example:**
```python
# app/models/user.py
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="operator")  # admin | operator
    is_active = db.Column(db.Boolean, default=True)
    last_login_at = db.Column(db.DateTime, nullable=True)
    matches_processed = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        return self.role == "admin"
```

### Pattern 3: Role-Based Access Control Decorator
**What:** Custom decorator for admin-only routes.
**When to use:** User management, settings that only admins should change.
**Example:**
```python
from functools import wraps
from flask import abort
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
```

### Pattern 4: AJAX Polling for Dashboard Auto-Refresh
**What:** Client-side periodic fetch to a JSON API endpoint.
**When to use:** Dashboard stats, sync status, event feed.
**Example:**
```javascript
// static/js/dashboard.js
let pollInterval = null;

function startPolling(intervalMs = 15000) {
    fetchDashboardData();  // Immediate first call
    pollInterval = setInterval(fetchDashboardData, intervalMs);
}

async function fetchDashboardData() {
    const response = await fetch('/api/dashboard/stats', {
        headers: { 'X-CSRFToken': getCSRFToken() }
    });
    if (response.ok) {
        const data = await response.json();
        updateWidgets(data);
    }
}
```

```python
# app/views/dashboard.py — JSON API endpoint
@dashboard_bp.route("/api/dashboard/stats")
@login_required
def dashboard_stats():
    """Return dashboard stats as JSON for AJAX polling."""
    # ... aggregate queries ...
    return jsonify({
        "last_sync_time": ...,
        "matched_count": ...,
        "unmatched_count": ...,
        "pending_review": ...,
        "errors": ...,
        "next_sync_seconds": ...,
    })
```

### Pattern 5: Export Endpoint (CSV/XLSX)
**What:** Stream file downloads from query results.
**When to use:** Match table export with filters.
**Example:**
```python
import csv
import io
from flask import make_response, send_file
from openpyxl import Workbook

@matches_bp.route("/matches/export/csv")
@login_required
def export_csv():
    # Apply same filters as current view
    matches = get_filtered_matches(request.args)
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Supplier", "Catalog", "Score", "Status"])
    for m in matches:
        writer.writerow([m.supplier_product.name, m.prom_product.name, m.score, m.status])
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=matches.csv"
    response.headers["Content-Type"] = "text/csv; charset=utf-8-sig"
    return response

@matches_bp.route("/matches/export/xlsx")
@login_required
def export_xlsx():
    matches = get_filtered_matches(request.args)
    wb = Workbook()
    ws = wb.active
    ws.append(["Supplier", "Catalog", "Score", "Status"])
    for m in matches:
        ws.append([m.supplier_product.name, m.prom_product.name, m.score, m.status])
    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return send_file(buf, as_attachment=True, download_name="matches.xlsx",
                     mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
```

### Pattern 6: Permanent Session with "Remember Me"
**What:** Flask-Login's remember cookie for persistent sessions.
**When to use:** Login form with "remember me" checkbox.
**Example:**
```python
from flask_login import login_user

@auth_bp.route("/login", methods=["POST"])
def login():
    user = User.query.filter_by(email=form.email.data).first()
    if user and user.check_password(form.password.data):
        remember = form.remember.data  # Checkbox value
        login_user(user, remember=remember)
        # ...

# config.py additions
REMEMBER_COOKIE_DURATION = timedelta(days=365)  # "Permanent" session
REMEMBER_COOKIE_SECURE = False  # Set True in production with HTTPS
REMEMBER_COOKIE_HTTPONLY = True
PERMANENT_SESSION_LIFETIME = timedelta(days=365)
```

### Anti-Patterns to Avoid
- **Storing plaintext passwords:** Always use `generate_password_hash` — never store raw password strings.
- **Missing CSRF on AJAX:** AJAX POST/DELETE requests must include `X-CSRFToken` header; use `csrf.exempt()` only on the public feed endpoint.
- **Adding `@login_required` to feed endpoint:** The YML feed at `/feed/yml` MUST remain public (AUTH-03).
- **Blocking the main thread with sync:** Manual sync trigger must run in a background thread or use the existing APScheduler, not block the HTTP request.
- **Querying all matches without pagination:** With thousands of products, always paginate using `db.paginate()` (Flask-SQLAlchemy 3.x built-in).
- **JavaScript state without server persistence:** Session auto-save must write to a server-side store (cookie or DB), not just localStorage, to survive power outages.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Password hashing | Custom hash function | `werkzeug.security.generate_password_hash` | Salt management, algorithm upgrades, timing attacks |
| Session management | Cookie manipulation | Flask-Login `login_user` / `logout_user` | Session fixation, cookie signing, user loading |
| CSRF protection | Manual token generation | Flask-WTF `CSRFProtect` | Token lifecycle, AJAX integration, exemption for public endpoints |
| Table pagination | Manual OFFSET/LIMIT | `db.paginate()` (Flask-SQLAlchemy 3.x) | Page metadata, edge cases, template helpers |
| Resizable panels | Custom drag handlers | Split.js | Cross-browser drag, touch support, min/max sizes |
| Charts | Canvas drawing | Chart.js | Responsive, tooltips, animations, data binding |
| Excel generation | Manual OOXML | openpyxl (already installed) | Formatting, encoding, streaming |

**Key insight:** The Flask ecosystem has mature, battle-tested solutions for every piece of this phase. The complexity is in integration and UI polish, not in building primitives.

## Common Pitfalls

### Pitfall 1: CSRF Token Missing on AJAX Requests
**What goes wrong:** POST/DELETE AJAX requests return 400 "CSRF token missing" errors.
**Why it happens:** Flask-WTF's CSRFProtect validates all state-changing requests. AJAX calls don't automatically include the token.
**How to avoid:** Include a meta tag `<meta name="csrf-token" content="{{ csrf_token() }}">` in base.html. In JavaScript, read it and set `X-CSRFToken` header on all fetch/XMLHttpRequest calls.
**Warning signs:** Forms work but AJAX actions (confirm match, trigger sync) fail with 400 errors.

### Pitfall 2: Feed Endpoint Blocked by Authentication
**What goes wrong:** prom.ua can no longer fetch the YML feed because `@login_required` is applied too broadly.
**Why it happens:** Developer applies `@login_required` at blueprint level or forgets to exempt the feed.
**How to avoid:** The feed blueprint is ALREADY separate (`feed_bp`). Never add `@login_required` to it. Never register it with a `before_request` auth check.
**Warning signs:** prom.ua stops updating, YML URL returns 302 redirect to login.

### Pitfall 3: Long-Running Sync Blocks Request
**What goes wrong:** Manual sync button makes the browser hang for 30+ seconds, then times out.
**Why it happens:** `run_full_sync()` executes synchronously in the request handler.
**How to avoid:** Trigger sync via existing APScheduler (`scheduler.add_job()` with immediate trigger) or use `threading.Thread`. Return immediately with a "sync started" response. Poll for completion status via separate endpoint.
**Warning signs:** Browser spinner doesn't stop, nginx/gunicorn request timeout errors.

### Pitfall 4: SQLite Locking During Concurrent Writes
**What goes wrong:** Database locked errors when admin approves matches while scheduler runs sync.
**Why it happens:** SQLite allows one writer at a time. WAL mode helps but doesn't eliminate write contention.
**How to avoid:** WAL mode is already configured. Keep write transactions short. Use `db.session.commit()` frequently rather than batching thousands of writes. The existing pattern of individual commits in the sync pipeline already handles this.
**Warning signs:** "database is locked" errors in logs, especially during manual sync + UI operations.

### Pitfall 5: Bootstrap CDN Version Mismatch
**What goes wrong:** JS components (modals, tooltips, dropdowns) don't work or behave inconsistently.
**Why it happens:** base.html already loads Bootstrap 5.3.3 CSS and JS from CDN. Adding a different version creates conflicts.
**How to avoid:** Use the SAME version (5.3.3) already in base.html. Do not add additional Bootstrap CSS/JS links in child templates.
**Warning signs:** Modals don't open, dropdowns don't close, console errors about missing Bootstrap functions.

### Pitfall 6: Seed Admin User Not Created
**What goes wrong:** After deployment, no one can log in because there are no users in the database.
**Why it happens:** The User table is created by `db.create_all()` but starts empty.
**How to avoid:** Add a Flask CLI command (`flask create-admin`) that creates the initial admin user. Also check on first request if no users exist and show setup page — but CLI command is the primary mechanism.
**Warning signs:** Login page works but all credentials are rejected.

## Code Examples

### Flask-Login User Loader Setup
```python
# Source: Flask-Login official docs (https://flask-login.readthedocs.io/)
# In app/extensions.py
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = "auth.login"

# In app/__init__.py create_app()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
```

### CSRF Meta Tag + JavaScript Helper
```html
<!-- In base.html <head> -->
<meta name="csrf-token" content="{{ csrf_token() }}">
```

```javascript
// static/js/common.js
function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

// Use in fetch calls:
fetch(url, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken()
    },
    body: JSON.stringify(data)
});
```

### Paginated Query with Flask-SQLAlchemy 3.x
```python
# Source: Flask-SQLAlchemy docs (https://flask-sqlalchemy.readthedocs.io/)
@matches_bp.route("/matches")
@login_required
def match_list():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 25, type=int)
    # Clamp per_page to allowed values
    per_page = per_page if per_page in (25, 50, 100) else 25

    query = ProductMatch.query.order_by(ProductMatch.score.asc())
    pagination = db.paginate(db.select(ProductMatch).order_by(ProductMatch.score.asc()),
                             page=page, per_page=per_page)
    return render_template("matches/review.html", pagination=pagination)
```

### Chart.js Integration via Jinja2
```html
<!-- In dashboard template -->
<canvas id="matchTrendChart" width="400" height="200"></canvas>

<script src="https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js"></script>
<script>
const ctx = document.getElementById('matchTrendChart').getContext('2d');
new Chart(ctx, {
    type: 'line',
    data: {
        labels: {{ chart_labels | tojson }},
        datasets: [{
            label: 'Matched',
            data: {{ chart_data_matched | tojson }},
            borderColor: '#198754',
        }]
    },
    options: { responsive: true }
});
</script>
```

### Manual Sync Trigger (Non-Blocking)
```python
import threading
from app.services.sync_pipeline import run_full_sync

@dashboard_bp.route("/api/sync/trigger", methods=["POST"])
@login_required
def trigger_sync():
    """Trigger manual sync in background thread."""
    thread = threading.Thread(target=_run_sync_in_context,
                              args=(current_app._get_current_object(),))
    thread.daemon = True
    thread.start()
    return jsonify({"status": "started"})

def _run_sync_in_context(app):
    with app.app_context():
        run_full_sync()
```

### Countdown Timer to Next Sync
```javascript
// Calculate from APScheduler next_run_time
function updateCountdown(nextSyncTimestamp) {
    const now = Date.now() / 1000;
    let remaining = Math.max(0, nextSyncTimestamp - now);

    const hours = Math.floor(remaining / 3600);
    const minutes = Math.floor((remaining % 3600) / 60);
    const seconds = Math.floor(remaining % 60);

    document.getElementById('countdown').textContent =
        `${hours}h ${minutes}m ${seconds}s`;

    if (remaining > 0) {
        requestAnimationFrame(() => setTimeout(() => updateCountdown(nextSyncTimestamp), 1000));
    }
}
```

### Diff Highlighting Between Names
```javascript
// Simple character-level diff for name comparison toggle
function highlightDiff(str1, str2) {
    let result1 = '', result2 = '';
    const maxLen = Math.max(str1.length, str2.length);
    for (let i = 0; i < maxLen; i++) {
        const c1 = str1[i] || '';
        const c2 = str2[i] || '';
        if (c1 !== c2) {
            result1 += `<mark>${c1}</mark>`;
            result2 += `<mark>${c2}</mark>`;
        } else {
            result1 += c1;
            result2 += c2;
        }
    }
    return { highlighted1: result1, highlighted2: result2 };
}
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Flask-Login 0.4 with `is_authenticated()` method | Flask-Login 0.6+ with `is_authenticated` property | 2020+ | No parentheses in templates: `{% if current_user.is_authenticated %}` |
| Manual CSRF tokens | Flask-WTF 1.2 CSRFProtect global init | 2023+ | Global protection, explicit exemption for public endpoints |
| `db.session.query(Model)` | `db.session.execute(select(Model))` | SQLAlchemy 2.0 (2023) | Project already uses new style — continue with `select()` |
| `query.paginate()` (deprecated) | `db.paginate(select(...))` | Flask-SQLAlchemy 3.x | New pagination API compatible with SQLAlchemy 2.0 selects |
| Chart.js 2.x with `moment.js` | Chart.js 4.x (no moment dependency) | 2022+ | Tree-shakeable, smaller bundle, better defaults |

**Deprecated/outdated:**
- `flask.ext.login` import style: removed in Flask 1.0+; use `flask_login` directly
- `@login_manager.token_loader`: removed; use `@login_manager.user_loader` only
- `Pagination.items` attribute: still works but `Pagination.__iter__()` is preferred in Flask-SQLAlchemy 3.x

## Open Questions

1. **Session auto-save on power outage**
   - What we know: Flask sessions are server-side (signed cookie). The operator wants state preserved if power cuts.
   - What's unclear: Exactly which "state" to save — filter selections? Unsaved form data? Page position?
   - Recommendation: Use `localStorage` for UI state (filters, page, scroll position) + periodic auto-save to DB for match review progress. On page load, restore from localStorage first, then from DB if localStorage is empty. This survives browser crashes and power outages (DB persists, localStorage persists on disk).

2. **Sync progress bar with exact numbers**
   - What we know: `run_full_sync()` processes stages sequentially and updates `SyncRun` fields.
   - What's unclear: Granular per-product progress would require the sync pipeline to write progress to a shared store during execution.
   - Recommendation: Use a simple approach — write stage progress to a DB row or a temporary file during sync. Poll from the UI. Stages are: fetching (0%), parsing (20%), saving (40%), matching (60%), YML generation (80%), complete (100%). Per-product granularity adds complexity for minimal benefit at current data scale (~6000 products).

3. **Notification rules engine complexity**
   - What we know: User wants configurable criteria (category, price, keywords) for new product notifications via both UI and Telegram.
   - What's unclear: Full rule engine complexity vs. simple filter presets.
   - Recommendation: Start with a simple notification_rules table (criteria_type, criteria_value, telegram_enabled, ui_enabled). Evaluate after initial implementation whether a more complex rule DSL is needed. Current product count (~6000) doesn't warrant complex event processing.

4. **Change tracking for photo/description**
   - What we know: Context.md lists this as a UI feature, but also defers the backend detection logic.
   - What's unclear: Whether the backend already stores historical values to diff against.
   - Recommendation: The current models do NOT store previous values. Phase 4 UI can show a "changed" badge if a `last_modified_at` field is added to SupplierProduct and compared across syncs. Full diff (old vs new) would require a product_changes audit table. Flag this as potentially requiring backend work beyond pure UI.

## Sources

### Primary (HIGH confidence)
- [Flask-Login 0.7.0 documentation](https://flask-login.readthedocs.io/) — session management, UserMixin, login_required, remember me
- [Flask-WTF 1.2.x CSRF documentation](https://flask-wtf.readthedocs.io/en/latest/csrf/) — CSRFProtect, AJAX token handling
- [werkzeug.security](https://tedboy.github.io/flask/generated/werkzeug.generate_password_hash.html) — password hashing with PBKDF2
- [Chart.js official](https://www.chartjs.org/) — Chart.js 4.x API
- [Split.js official](https://split.js.org/) — resizable panel library
- Existing codebase analysis: `app/__init__.py`, `app/extensions.py`, `app/models/`, `app/views/`, `app/services/telegram_notifier.py`

### Secondary (MEDIUM confidence)
- [Flask-SSE no-deps pattern](https://maxhalford.github.io/blog/flask-sse-no-deps/) — SSE without Redis (evaluated, not recommended for this project)
- [Flask CSV download](https://matthewmoisen.com/blog/how-to-download-a-csv-file-in-flask/) — export patterns
- [Bootstrap 5 + Split.js CodePen](https://codepen.io/govind_chopade/pen/eYvzMmX) — integration example

### Tertiary (LOW confidence)
- [Telegram Bot send message patterns](https://gist.github.com/dlaptev/7f1512ee80b7e511b0435d3ba95d88cc) — Telegram notification sending (already implemented in project, just extending)

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — Flask-Login, Flask-WTF, werkzeug.security are the de facto standards with no serious competitors for this use case
- Architecture: HIGH — project already uses the correct patterns (blueprints, factory, SQLAlchemy 2.0 style); Phase 4 extends these naturally
- Pitfalls: HIGH — well-documented pitfalls from Flask ecosystem; verified against existing codebase patterns

**Research date:** 2026-02-28
**Valid until:** 2026-03-28 (stable ecosystem, no fast-moving parts)
