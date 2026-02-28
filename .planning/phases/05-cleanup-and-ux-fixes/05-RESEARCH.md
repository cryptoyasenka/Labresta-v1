# Phase 5: Cleanup and UX Fixes - Research

**Researched:** 2026-03-01
**Domain:** Dead code removal, Bootstrap 5 notification dropdown, role-based access control
**Confidence:** HIGH

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **Notification dropdown (bell icon):** Replace current link-to-page with a Bootstrap 5 dropdown in navbar. Show 5 most recent unread notifications. Dropdown is identical for admin and operator (same component for all roles). "Отметить все прочитанными" button in the dropdown header. "Все уведомления" link at the bottom navigates to full notification page. Click on bell icon or badge number opens the dropdown. Dropdown loads notifications via existing `/settings/api/notifications/unread` endpoint.
- **Badge behavior:** Badge (red pill with unread count) on the bell icon with global polling every 30 seconds. Move `updateNavbarBadge()` function from `notifications.js` into `base.html` so it runs on ALL pages. Add small x (close) button next to the badge number. Clicking x hides the badge until page reload (JS-only, no server call). Badge reappears on page navigation/reload if unread notifications still exist.
- **Dead code cleanup:** DELETE `app/services/yml_test_generator.py` and `scripts/generate_test_yml.py`. KEEP `app/services/ftp_upload.py` and `scripts/upload_test_yml.py` (may be needed for FTP delivery in future). KEEP `MatchRule` model (incomplete feature, not dead code). Update CLEAN-01 requirement: ftp_upload.py is intentionally kept. CLEAN-02 fulfilled by deleting yml_test_generator.py.
- **Notification permissions (roles):** All notifications are global (no per-user filtering). Operator sees all the same notifications as admin. Operator CANNOT manage notification rules (admin only). Remove `@admin_required` from API endpoints (`api_notifications_unread`, `api_notifications_mark_read`) so operators can use them. Keep `@admin_required` on rule management endpoints.
- **Operator notification page:** New simplified page for operator: notification list only, no rules management section. "Отметить все прочитанными" button at top of the list. Admin sees the full existing page (rules + notifications) as before. The `/settings/notifications` route shows different content based on `current_user.is_admin`.

### Claude's Discretion
- Empty state design for dropdown when no notifications exist
- Exact CSS/styling of the x dismiss button on badge
- Whether to extract badge polling into a separate JS file or inline in base.html
- Pagination/scrolling behavior on the operator's simplified notification page

### Deferred Ideas (OUT OF SCOPE)
None -- discussion stayed within phase scope.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| CLEAN-01 | Delete dead code: ftp_upload.py | **USER OVERRIDE:** ftp_upload.py is intentionally KEPT. Requirement will be updated to reflect this. No deletion needed. |
| CLEAN-02 | Delete dead code: yml_test_generator.py | Confirmed safe to delete. Two files: `app/services/yml_test_generator.py` and `scripts/generate_test_yml.py`. No runtime imports. Only cross-reference is the script importing the service. See "Dead Code Deletion" pattern. |
| UX-01 | notifications.js loads globally on all pages (badge polling works everywhere) | Move `updateNavbarBadge()` into `base.html` inline `<script>` block (after bootstrap.bundle.min.js). Currently only loaded on the notifications page via `{% block scripts %}`. See "Global Badge Polling" pattern. |
| UX-02 | Operators see bell icon and can access notifications without 403 | Three changes: (1) remove `@admin_required` from `/settings/notifications` route, add conditional rendering by role; (2) API endpoints already use `@login_required` only (verified -- no `@admin_required` on API endpoints); (3) convert bell icon from `<a href>` link to Bootstrap dropdown trigger. See "Notification Dropdown" and "Role-Based View" patterns. |
</phase_requirements>

## Summary

This phase addresses four requirements across two domains: dead code cleanup and notification UX fixes. The work is straightforward with no new dependencies needed.

**Dead code cleanup** is the simplest task. The user decided to keep `ftp_upload.py` (future FTP delivery) and `MatchRule` (incomplete feature), so only `yml_test_generator.py` and its companion script `generate_test_yml.py` need deletion. Grep confirms these files are only referenced by each other and by planning docs (which need no update). No runtime code, no tests, no imports from the main application.

**Notification UX** requires three coordinated changes: (1) extracting the `updateNavbarBadge()` polling function into `base.html` so it runs globally, (2) converting the bell icon from a page link into a Bootstrap 5 dropdown showing recent notifications, and (3) making the notifications page accessible to operators with a simplified view (no rules management). The existing codebase already uses Bootstrap 5 dropdowns in the navbar (Товары, Настройки menus), provides `fetchWithCSRF()` in `common.js` for AJAX, and has a context processor injecting `unread_notification_count` on every page. The API endpoints (`/api/notifications/unread` and `/api/notifications/mark-read`) already use `@login_required` without `@admin_required`, so they are already accessible to operators. The only route that needs its decorator changed is the main `/settings/notifications` page view.

**Primary recommendation:** Execute in order: (1) delete dead code first (zero risk, clean diff), (2) implement global badge polling, (3) build the notification dropdown, (4) fix the operator notifications page. Each step is independently verifiable.

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Bootstrap 5.3.3 | CDN (already loaded) | Dropdown component, badge styling, responsive layout | Already in project via `base.html` CDN links |
| Flask/Jinja2 | current (already installed) | Route handling, template conditional rendering | Already the project's web framework |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| bootstrap.bundle.min.js | 5.3.3 (CDN, already loaded) | Dropdown JS behavior via `data-bs-toggle="dropdown"` | Dropdown opens/closes automatically; no custom JS needed for toggle |
| common.js (project) | N/A | `fetchWithCSRF()` for AJAX POST with CSRF token | Mark-all-read button in dropdown |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Inline `<script>` in base.html for badge polling | Separate `notification-badge.js` file | User left this to Claude's discretion. Inline is simpler (one less HTTP request, no cache issues), but separate file is cleaner. **Recommend inline** since it is ~25 lines and tightly coupled to the badge HTML. |

## Architecture Patterns

### Recommended Approach

Changes are localized to these files:

```
app/
├── views/settings.py           # Remove @admin_required from notifications(), add role check
├── templates/
│   ├── base.html               # Bell → dropdown, inline badge polling JS, dismiss button
│   └── settings/
│       └── notifications.html  # Conditional rendering: admin sees full page, operator sees list only
├── static/
│   ├── js/notifications.js     # Remove updateNavbarBadge (moved to base.html); keep rule-form JS
│   └── css/app.css             # Optional: dismiss button styling
├── services/
│   └── yml_test_generator.py   # DELETE
scripts/
└── generate_test_yml.py        # DELETE
```

### Pattern 1: Bootstrap 5 Navbar Dropdown (Notification Bell)

**What:** Convert the bell icon `<a>` tag into a dropdown trigger with a `<ul class="dropdown-menu">` containing notification items.

**When to use:** The project already uses this exact pattern for "Товары" and "Настройки" nav items.

**Example (from existing codebase at `base.html:36-47`):**
```html
<li class="nav-item dropdown">
    <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
        Товары
    </a>
    <ul class="dropdown-menu">
        <li><a class="dropdown-item" href="...">Товары поставщиков</a></li>
        ...
    </ul>
</li>
```

**Applied to bell icon:**
```html
<li class="nav-item dropdown">
    <a class="nav-link position-relative" href="#" role="button"
       data-bs-toggle="dropdown" aria-expanded="false" id="notificationDropdown">
        <!-- bell SVG (existing) -->
        <svg ...>...</svg>
        <span class="badge bg-danger rounded-pill position-absolute top-0 start-100 translate-middle"
              id="notificationBadge" style="...">
            {{ unread_notification_count or '' }}
            <button type="button" class="btn-close btn-close-white ms-1"
                    style="font-size: 0.5em;" id="dismissBadge"
                    onclick="event.stopPropagation(); this.parentElement.style.display='none';">
            </button>
        </span>
    </a>
    <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="notificationDropdown"
        style="min-width: 350px;" id="notificationDropdownMenu">
        <li class="dropdown-header d-flex justify-content-between align-items-center">
            <strong>Уведомления</strong>
            <button class="btn btn-link btn-sm p-0" id="dropdownMarkAllRead">
                Отметить все прочитанными
            </button>
        </li>
        <li><hr class="dropdown-divider"></li>
        <!-- Notification items loaded via JS -->
        <li id="notificationDropdownEmpty" class="text-center text-muted py-3">
            Нет новых уведомлений
        </li>
        <li><hr class="dropdown-divider"></li>
        <li class="text-center">
            <a class="dropdown-item" href="{{ url_for('settings.notifications') }}">
                Все уведомления
            </a>
        </li>
    </ul>
</li>
```

**Key detail:** The dropdown content is populated on open via JS fetching `/settings/api/notifications/unread`. The `dropdown-menu-end` class ensures the dropdown aligns to the right edge (since the bell is on the right side of the navbar).

### Pattern 2: Global Badge Polling (Inline in base.html)

**What:** Move the `updateNavbarBadge()` function and its `setInterval` from `notifications.js` into `base.html` so it executes on every page.

**Current state (broken):** `notifications.js` is loaded only via `{% block scripts %}` in `notifications.html`. Badge polling only works on the notification settings page.

**Fix:** Add an inline `<script>` block in `base.html` after `common.js` is loaded:

```html
<script src="{{ url_for('static', filename='js/common.js') }}"></script>
{% if current_user.is_authenticated %}
<script>
(function() {
    function updateNavbarBadge() {
        var badge = document.getElementById('notificationBadge');
        if (!badge) return;
        fetch('/settings/api/notifications/unread')
            .then(function(r) { return r.json(); })
            .then(function(data) {
                var count = data.length || 0;
                if (count > 0) {
                    badge.textContent = count;
                    badge.style.display = '';
                } else {
                    badge.style.display = 'none';
                }
            })
            .catch(function() {});
    }
    // Also populate dropdown on open
    var dropdown = document.getElementById('notificationDropdown');
    if (dropdown) {
        dropdown.addEventListener('show.bs.dropdown', loadDropdownNotifications);
    }
    updateNavbarBadge();
    setInterval(updateNavbarBadge, 30000);
})();
</script>
{% endif %}
```

**Why inline:** The function is ~20 lines, tightly coupled to the badge HTML element in the same file, and must run on every page. A separate file adds an HTTP request and cache management for minimal benefit.

### Pattern 3: Role-Based Conditional Template Rendering

**What:** The `/settings/notifications` route removes `@admin_required`, uses `@login_required` only, and the template renders different content based on `current_user.is_admin`.

**Route change in `settings.py`:**
```python
@settings_bp.route("/notifications")
@login_required
def notifications():
    """Notification page: full management for admin, list-only for operator."""
    recent = get_recent_notifications(limit=20)
    if current_user.is_admin:
        rules = db.session.execute(
            select(NotificationRule).order_by(NotificationRule.created_at.desc())
        ).scalars().all()
        return render_template(
            "settings/notifications.html",
            rules=rules,
            recent_notifications=recent,
        )
    # Operator: simplified view
    return render_template(
        "settings/notifications_operator.html",
        recent_notifications=recent,
    )
```

**Alternative (single template with conditionals):** Wrap the rules section and management buttons in `{% if current_user.is_admin %}` blocks. This avoids a new template but makes the existing template more complex. The existing template already has modals and rule forms tightly integrated, so a **separate operator template** is cleaner and easier to maintain.

### Pattern 4: Dismiss Badge Button

**What:** Small x button on the badge that hides it until page reload.

**Implementation:** The x button uses `onclick="event.stopPropagation(); this.parentElement.style.display='none';"` -- pure JS, no server call. On next page load or navigation, the context processor re-injects `unread_notification_count`, and the badge reappears if count > 0.

**Key detail:** `event.stopPropagation()` prevents the click from opening the dropdown.

### Anti-Patterns to Avoid
- **Do NOT load notifications.js globally:** It contains notification-page-specific code (rule form hints, markAllBtn for the page list). Only the `updateNavbarBadge()` function should be global. The rest stays page-specific.
- **Do NOT create a custom dropdown from scratch:** Bootstrap 5's dropdown component handles positioning, keyboard navigation, outside-click-to-close, and accessibility. Use `data-bs-toggle="dropdown"`.
- **Do NOT use separate API endpoint for dropdown:** The existing `/api/notifications/unread` already returns the data needed for the dropdown (id, message, created_at, is_read).
- **Do NOT put the dismiss x button inside a separate element from the badge:** It must be inside the badge `<span>` so hiding the badge hides the x too.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Dropdown toggle/positioning | Custom JS show/hide logic | Bootstrap 5 `data-bs-toggle="dropdown"` | Handles edge cases: viewport overflow, keyboard nav, screen readers, outside-click-close |
| CSRF-protected AJAX | Manual header injection | `fetchWithCSRF()` from `common.js` | Already in project, handles token extraction from meta tag |
| Badge count on every page | Duplicate server-side code | Context processor in `app/__init__.py` | Already injects `unread_notification_count` into every template context |

**Key insight:** Every building block already exists in the codebase. The phase is about wiring existing pieces together correctly, not building new infrastructure.

## Common Pitfalls

### Pitfall 1: Dropdown Click Propagation with Dismiss Button
**What goes wrong:** Clicking the x dismiss button on the badge also opens/closes the dropdown.
**Why it happens:** The badge is inside the dropdown trigger `<a>` element. Click events bubble up.
**How to avoid:** Use `event.stopPropagation()` on the dismiss button's click handler.
**Warning signs:** Badge disappears but dropdown also opens/closes when clicking x.

### Pitfall 2: Badge Polling Fires Before DOM Ready
**What goes wrong:** `updateNavbarBadge()` runs before `#notificationBadge` element exists in DOM.
**Why it happens:** Inline script placed in `<head>` or before the navbar HTML.
**How to avoid:** Place the inline script AFTER the navbar HTML and after `bootstrap.bundle.min.js`. Alternatively, wrap in `DOMContentLoaded`.
**Warning signs:** Badge never updates despite API returning data.

### Pitfall 3: notifications.js Conflicts with Inline Badge Code
**What goes wrong:** Two competing `setInterval(updateNavbarBadge, 30000)` calls running when on the notification page.
**Why it happens:** Both inline base.html code and notifications.js define/call `updateNavbarBadge`.
**How to avoid:** Remove `updateNavbarBadge()` definition and its `setInterval` from `notifications.js`. Keep only the rule-form JS and the page-specific mark-all-read handler in that file.
**Warning signs:** Network tab shows double API calls every 30 seconds on the notification page.

### Pitfall 4: Operator Still Gets 403 on Notification Page
**What goes wrong:** Operator clicks "Все уведомления" link in dropdown and gets 403.
**Why it happens:** Forgot to remove `@admin_required` from the `notifications()` route in `settings.py`.
**How to avoid:** Verify the route uses `@login_required` only, and the admin check is inside the function body (not a decorator).
**Warning signs:** Dropdown works fine for operators, but the full page link returns 403.

### Pitfall 5: Dropdown Content Not Refreshing
**What goes wrong:** Dropdown shows stale notification data from the first open.
**Why it happens:** Notifications are loaded on first dropdown open but never refreshed.
**How to avoid:** Load notifications on EVERY dropdown open using Bootstrap's `show.bs.dropdown` event.
**Warning signs:** New notifications appear in badge count but not in dropdown until page refresh.

### Pitfall 6: CSRF Token Missing on Dropdown Mark-All-Read
**What goes wrong:** 400 Bad Request when clicking "mark all read" in the dropdown.
**Why it happens:** Using raw `fetch()` instead of `fetchWithCSRF()` for the POST request.
**How to avoid:** Use `fetchWithCSRF()` from `common.js` (loaded before the inline script in base.html).
**Warning signs:** Mark-all-read works on the full notification page but fails in the dropdown.

## Code Examples

### Dead Code Deletion (git rm)
```bash
git rm app/services/yml_test_generator.py
git rm scripts/generate_test_yml.py
```
No other files import these. Planning docs reference them but those are historical records.

### Bootstrap Dropdown Event Listener (Load Notifications on Open)
```javascript
// Source: Bootstrap 5.3 docs — Dropdown events
// https://getbootstrap.com/docs/5.3/components/dropdowns/#events
var dropdownEl = document.getElementById('notificationDropdown');
dropdownEl.addEventListener('show.bs.dropdown', function() {
    fetch('/settings/api/notifications/unread')
        .then(function(r) { return r.json(); })
        .then(function(data) {
            renderDropdownNotifications(data.slice(0, 5));
        });
});
```

### Role-Conditional Route (Remove Decorator, Check Inside)
```python
# BEFORE (broken for operators):
@settings_bp.route("/notifications")
@login_required
@admin_required
def notifications():
    ...

# AFTER (works for all roles):
@settings_bp.route("/notifications")
@login_required
def notifications():
    recent = get_recent_notifications(limit=20)
    if current_user.is_admin:
        rules = db.session.execute(
            select(NotificationRule).order_by(NotificationRule.created_at.desc())
        ).scalars().all()
        return render_template("settings/notifications.html", rules=rules, recent_notifications=recent)
    return render_template("settings/notifications_operator.html", recent_notifications=recent)
```

### Mark All Read from Dropdown (Using Existing fetchWithCSRF)
```javascript
document.getElementById('dropdownMarkAllRead').addEventListener('click', function() {
    // Get IDs from loaded dropdown items
    var items = document.querySelectorAll('#notificationDropdownMenu .notification-item');
    var ids = [];
    items.forEach(function(el) {
        var id = el.getAttribute('data-id');
        if (id) ids.push(parseInt(id, 10));
    });
    if (ids.length === 0) return;

    fetchWithCSRF('/settings/api/notifications/mark-read', {
        method: 'POST',
        body: JSON.stringify({ ids: ids }),
    })
    .then(function(r) { return r.json(); })
    .then(function(data) {
        if (data.marked > 0) {
            updateNavbarBadge();
            // Clear dropdown items visually
        }
    });
});
```

## Codebase Findings (Verified)

### Current Bug Analysis

**UX-01 bug (badge not global):**
- `notifications.js` defines `updateNavbarBadge()` and starts 30s polling (lines 66-67, 70-88)
- `notifications.js` is loaded ONLY in `notifications.html` via `{% block scripts %}` (line 245)
- Therefore badge polling only runs on the notifications settings page
- Context processor in `app/__init__.py:68-93` already provides `unread_notification_count` for initial render on all pages, but the 30s AJAX refresh never fires elsewhere

**UX-02 bug (operator 403):**
- Bell icon is visible to ALL authenticated users (base.html:71-81, outside the `{% if current_user.is_admin %}` block)
- Bell links to `{{ url_for('settings.notifications') }}` (base.html:73)
- `notifications()` route has `@admin_required` decorator (settings.py:222)
- Operator clicks bell -> 403 Forbidden
- API endpoints (`api_notifications_unread`, `api_notifications_mark_read`) already use `@login_required` only (settings.py:351, 367) -- no fix needed there

### Files to Delete (CLEAN-02)
- `app/services/yml_test_generator.py` -- 63 lines, development utility, imports lxml and PromProduct
- `scripts/generate_test_yml.py` -- 41 lines, CLI script that imports yml_test_generator
- No runtime code imports either file
- No tests reference either file

### Files to KEEP (User Decision - CLEAN-01 Override)
- `app/services/ftp_upload.py` -- user decided to keep for potential future FTP delivery
- `scripts/upload_test_yml.py` -- companion script, kept with ftp_upload.py
- `MatchRule` model -- incomplete feature, not dead code

### Existing Infrastructure to Reuse
| Asset | Location | How to Reuse |
|-------|----------|--------------|
| Bootstrap dropdown pattern | `base.html:36-47` (Товары menu) | Same HTML structure for bell dropdown |
| `fetchWithCSRF()` | `common.js:27-44` | AJAX POST for mark-all-read in dropdown |
| `unread_notification_count` context var | `app/__init__.py:85-91` | Initial badge count on every page (already works) |
| `get_recent_notifications()` | `notification_service.py:118-131` | Operator's simplified notification page |
| `get_unread_notifications()` | `notification_service.py:62-76` | Already used by API endpoint for dropdown |
| Bell SVG + badge HTML | `base.html:74-79` | Extend with dropdown wrapper |
| `@admin_required` decorator | `settings.py:21-30` | Keep on rule management routes only |

## Open Questions

1. **Dropdown notification item click behavior**
   - What we know: Dropdown shows 5 recent unread notifications with "Все уведомления" link at bottom
   - What's unclear: Should clicking a notification item in the dropdown mark it as read? Should it navigate somewhere?
   - Recommendation: Clicking a notification item should mark it as read and do nothing else (notifications are informational, about new products, not navigational). If uncertain, keep simple -- just display them.

2. **Operator page pagination**
   - What we know: User left this to Claude's discretion
   - What's unclear: How many notifications to show, whether to add pagination
   - Recommendation: Show 50 most recent notifications (same `get_recent_notifications(limit=50)`). No pagination needed for v1.1 -- the list won't be excessively long for a small team.

## Sources

### Primary (HIGH confidence)
- Direct codebase analysis of all relevant files (base.html, settings.py, notifications.js, common.js, notification_service.py, __init__.py, user.py, notification_rule.py, yml_test_generator.py, generate_test_yml.py)
- Bootstrap 5.3 documentation (dropdown component, events, badge component) -- patterns already demonstrated in project codebase

### Secondary (MEDIUM confidence)
- v1.0 audit findings in `.planning/milestones/v1.0-MILESTONE-AUDIT.md` confirming dead code status
- v1.1 research docs in `.planning/research/` (ARCHITECTURE.md, FEATURES.md, PITFALLS.md) confirming import analysis

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- no new libraries, all existing Bootstrap 5 + Flask
- Architecture: HIGH -- patterns already in codebase (dropdown, context processor, fetchWithCSRF)
- Pitfalls: HIGH -- all derived from direct code inspection, common Bootstrap/JS patterns
- Dead code analysis: HIGH -- grep confirms zero runtime references

**Research date:** 2026-03-01
**Valid until:** 2026-04-01 (stable -- no external dependencies changing)
