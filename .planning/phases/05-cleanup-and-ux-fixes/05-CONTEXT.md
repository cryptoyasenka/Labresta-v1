# Phase 5: Cleanup and UX Fixes - Context

**Gathered:** 2026-03-01
**Status:** Ready for planning

<domain>
## Phase Boundary

Dead code removal and notification system fixes so all user roles can use notifications correctly. The notification bell and badge must work for both admin and operator roles. Dead code identified in the v1.0 audit is removed.

</domain>

<decisions>
## Implementation Decisions

### Notification dropdown (колокольчик)
- Replace current link-to-page with a Bootstrap dropdown in navbar
- Show 5 most recent unread notifications in the dropdown
- Dropdown is identical for admin and operator — same component for all roles
- "Отметить все прочитанными" button in the dropdown header
- "Все уведомления" link at the bottom of dropdown → navigates to full notification page
- Click on bell icon OR badge number opens the dropdown
- Dropdown loads notifications via existing `/settings/api/notifications/unread` endpoint

### Badge behavior
- Badge (red pill with unread count) on the bell icon — global polling every 30 seconds
- Move `updateNavbarBadge()` function from `notifications.js` into `base.html` so it runs on ALL pages
- Add small × (close) button next to the badge number
- Clicking × hides the badge until page reload (JS-only, no server call)
- Badge reappears on page navigation/reload if unread notifications still exist

### Dead code cleanup
- DELETE: `app/services/yml_test_generator.py` and `scripts/generate_test_yml.py`
- KEEP: `app/services/ftp_upload.py` and `scripts/upload_test_yml.py` (may be needed for FTP delivery in future)
- KEEP: `MatchRule` model — incomplete feature, not dead code, may be useful for matcher improvements
- Update CLEAN-01 requirement: ftp_upload.py is intentionally kept
- CLEAN-02 fulfilled by deleting yml_test_generator.py

### Notification permissions (roles)
- All notifications are global — no per-user filtering (notifications are about new products, not personal)
- Operator sees all the same notifications as admin
- Operator CANNOT manage notification rules (create/edit/delete) — admin only, as current behavior
- Remove `@admin_required` from the notification API endpoints (`api_notifications_unread`, `api_notifications_mark_read`) so operators can use them
- Keep `@admin_required` on rule management endpoints

### Operator notification page
- New simplified page for operator: notification list only, no rules management section
- "Отметить все прочитанными" button at top of the list
- Admin sees the full existing page (rules + notifications) as before
- The `/settings/notifications` route shows different content based on `current_user.is_admin`

### Claude's Discretion
- Empty state design for dropdown when no notifications exist
- Exact CSS/styling of the × dismiss button on badge
- Whether to extract badge polling into a separate JS file or inline in base.html
- Pagination/scrolling behavior on the operator's simplified notification page

</decisions>

<specifics>
## Specific Ideas

- Badge dismiss (×) should be visually small and unobtrusive — similar to closing a browser tab
- The dropdown should feel like a standard Bootstrap 5 dropdown menu — compact, clean

</specifics>

<code_context>
## Existing Code Insights

### Reusable Assets
- `notifications.js`: Has `updateNavbarBadge()` function with 30s polling — extract and move to base.html
- `notifications.js`: Has `markAllReadBtn` click handler — reuse pattern for dropdown "mark all read"
- `base.html:73-80`: Existing bell SVG icon with badge `#notificationBadge` — extend with dropdown
- Context processor in `app/__init__.py:68-93`: Already provides `unread_notification_count` globally

### Established Patterns
- Bootstrap 5 dropdowns already used in navbar (Товары, Настройки) — same pattern for notification bell
- `fetchWithCSRF()` function in `common.js` for AJAX POST requests
- `@admin_required` decorator in `settings.py` for access control
- `@login_required` on API endpoints — operators already authenticated

### Integration Points
- `settings.py:350-363`: API endpoint `/api/notifications/unread` — currently `@login_required` only, no admin check needed
- `settings.py:365-376`: API endpoint `/api/notifications/mark-read` — currently `@login_required` only
- `settings.py:220-233`: Full notifications page — needs conditional rendering based on role
- `base.html:71-81`: Bell icon area — convert from link to dropdown trigger

</code_context>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 05-cleanup-and-ux-fixes*
*Context gathered: 2026-03-01*
