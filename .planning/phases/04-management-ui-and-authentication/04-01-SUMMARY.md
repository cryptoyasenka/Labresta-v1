---
phase: 04-management-ui-and-authentication
plan: 01
subsystem: auth
tags: [flask-login, flask-wtf, csrf, session-auth, bootstrap5]

# Dependency graph
requires:
  - phase: 03-pricing-engine-and-yml-output
    provides: "ProductMatch model with candidate status for pending review badge"
provides:
  - "User model with email/password auth and admin/operator roles"
  - "Flask-Login session management with remember-me support"
  - "CSRF protection via Flask-WTF on all forms and AJAX"
  - "Auth blueprint with login/logout routes"
  - "create-admin CLI command"
  - "Auth-aware base template with pending review badge"
  - "@login_required on all management routes"
  - "Public feed endpoint preserved without auth"
affects: [04-02, 04-03, 04-04, 04-05, 04-06, 04-07]

# Tech tracking
tech-stack:
  added: [flask-login, flask-wtf, wtforms, split.js]
  patterns: [login_required decorator, CSRF meta tag, context processor for badge counts, fetchWithCSRF JS helper]

key-files:
  created:
    - app/models/user.py
    - app/views/auth.py
    - app/templates/auth/login.html
    - app/static/css/app.css
    - app/static/js/common.js
  modified:
    - app/extensions.py
    - app/__init__.py
    - app/config.py
    - app/models/__init__.py
    - app/cli.py
    - app/templates/base.html
    - app/views/main.py
    - app/views/suppliers.py
    - app/views/catalog.py
    - pyproject.toml

key-decisions:
  - "Flask-Login with session cookies over JWT for server-rendered app simplicity"
  - "CSRF meta tag pattern for AJAX requests via fetchWithCSRF helper"
  - "Light navbar (bg-white border-bottom) replacing dark theme per user decision"
  - "Split.js CDN added to base template for future resizable panels"
  - "Context processor for pending_review_count badge on every page load"

patterns-established:
  - "@login_required on all management routes, feed stays public"
  - "CSRF token in meta tag + fetchWithCSRF() for AJAX POST requests"
  - "Context processor pattern for global template variables"

requirements-completed: [AUTH-01, AUTH-02]

# Metrics
duration: 4min
completed: 2026-02-28
---

# Phase 04 Plan 01: Auth Foundation Summary

**Flask-Login session auth with User model, CSRF protection, login/logout flow, create-admin CLI, and auth-aware Bootstrap 5 navbar with pending review badge**

## Performance

- **Duration:** 4 min
- **Started:** 2026-02-28T15:42:55Z
- **Completed:** 2026-02-28T15:47:20Z
- **Tasks:** 3
- **Files modified:** 15

## Accomplishments
- User model with email/password hashing (werkzeug), admin/operator roles, and Flask-Login UserMixin
- Login/logout flow with remember-me, CSRF protection, and flash messages in Russian
- Auth-aware navbar with pending review badge count, light theme, and full-width layout
- All management routes protected with @login_required; feed endpoint remains public
- create-admin CLI command for initial admin user setup

## Task Commits

Each task was committed atomically:

1. **Task 1: Install auth dependencies, create User model, configure Flask-Login and CSRF** - `c18219e` (feat)
2. **Task 2: Create login/logout views, auth blueprint, and create-admin CLI command** - `c3e0db7` (feat)
3. **Task 3: Upgrade base template with auth navigation, pending review badge, and global styles** - `eec7699` (feat)

## Files Created/Modified
- `app/models/user.py` - User model with password hashing, roles, UserMixin
- `app/views/auth.py` - Auth blueprint: login (GET/POST) and logout routes
- `app/templates/auth/login.html` - Bootstrap 5 login form with CSRF token
- `app/static/css/app.css` - Spacious clean styles, confidence badge classes
- `app/static/js/common.js` - CSRF helper, fetchWithCSRF, confirmAction
- `app/extensions.py` - Added LoginManager and CSRFProtect instances
- `app/__init__.py` - Wired auth extensions, user_loader, auth_bp, context processor
- `app/config.py` - Session/remember-me cookie configuration
- `app/models/__init__.py` - Added User import
- `app/cli.py` - Added create-admin CLI command
- `app/templates/base.html` - Auth-aware navbar, CSRF meta, Split.js, custom CSS/JS
- `app/views/main.py` - Added @login_required to index
- `app/views/suppliers.py` - Added @login_required to all routes
- `app/views/catalog.py` - Added @login_required to all routes
- `pyproject.toml` - Added flask-login and flask-wtf dependencies

## Decisions Made
- Flask-Login session cookies chosen over JWT for simplicity in server-rendered Flask app
- CSRF meta tag pattern established for AJAX requests via fetchWithCSRF JS helper
- Light navbar (bg-white border-bottom) per user design decision
- Split.js CDN added to base template early for resizable panels in Plan 02/05
- Context processor for pending_review_count queries ProductMatch candidates on every authenticated page load

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Created auth blueprint and login template in Task 1 scope**
- **Found during:** Task 1 (app factory references auth_bp)
- **Issue:** app/__init__.py imports auth_bp which doesn't exist yet, blocking verification
- **Fix:** Created full auth.py, login.html, and CLI ahead of Task 2 to unblock app creation
- **Files modified:** app/views/auth.py, app/templates/auth/login.html, app/cli.py
- **Verification:** App creates successfully, login page returns 200
- **Committed in:** c3e0db7 (Task 2 commit)

---

**Total deviations:** 1 auto-fixed (1 blocking)
**Impact on plan:** Auth blueprint created slightly earlier than planned to unblock app factory. No scope creep.

## Issues Encountered
- uv binary not found in bash PATH on Windows; used .venv/Scripts/pip3.exe directly to install dependencies
- Login POST returns 400 in test client due to CSRF protection (expected behavior, confirms CSRF works)

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Auth foundation complete; all subsequent plans can use @login_required freely
- create-admin CLI ready for initial admin user creation
- Pending review badge wired to ProductMatch candidate count for match review UI

---
*Phase: 04-management-ui-and-authentication*
*Completed: 2026-02-28*
