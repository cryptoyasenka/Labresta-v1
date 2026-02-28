---
phase: 04-management-ui-and-authentication
plan: 07
subsystem: notifications
tags: [notifications, telegram, ui, crud, settings]
dependency_graph:
  requires: [04-01, 04-06]
  provides: [notification-rules, notification-service, telegram-toggle]
  affects: [sync-pipeline, navbar, settings]
tech_stack:
  added: []
  patterns: [rule-based-matching, grouped-telegram-notifications, navbar-badge-polling]
key_files:
  created:
    - app/models/notification_rule.py
    - app/services/notification_service.py
    - app/templates/settings/notifications.html
    - app/static/js/notifications.js
  modified:
    - app/models/__init__.py
    - app/__init__.py
    - app/services/sync_pipeline.py
    - app/views/settings.py
    - app/templates/base.html
decisions:
  - NotificationRule criteria types: keyword, brand, price_range, category (category reserved for future)
  - Grouped Telegram messages per rule (max 10 products) to avoid spam
  - Global Telegram toggle affects all active rules simultaneously
  - Soft-delete for rules (is_active=False) preserves notification history
  - 30s polling interval for navbar badge updates
metrics:
  duration: 4 min
  completed: "2026-02-28"
---

# Phase 4 Plan 7: Notification Rules and Alerts Summary

Configurable notification rules matching new supplier products by keyword, brand, price range, or category with dual delivery (UI + Telegram) and grouped messaging to avoid spam.

## What Was Built

### Task 1: NotificationRule model and notification service
**Commit:** d227dcc

- **NotificationRule model** with criteria_type (keyword, brand, price_range, category), criteria_value, telegram/ui enable flags, is_active soft-delete
- **Notification model** for UI notification storage with rule_id, supplier_product_id, message, is_read
- **notification_service.py** with check_and_notify() rule engine, get_unread_notifications(), mark_notifications_read(), get_unread_count()
- **Sync pipeline integration** -- after save stage, newly created products are checked against active rules
- **Context processor** injects unread_notification_count into every authenticated page

### Task 2: Notification settings UI with rule CRUD and Telegram toggle
**Commit:** 46d3f1f

- **Settings endpoints** for notifications CRUD: list, create, edit, soft-delete rules
- **Global Telegram toggle** that enables/disables Telegram on all active rules at once
- **API endpoints** /api/notifications/unread (JSON for badge) and /api/notifications/mark-read
- **notifications.html** template with rules table (type badges, status badges), recent notifications list, create/edit modals
- **notifications.js** with criteria type hints, mark-all-read functionality, 30s badge polling
- **Navbar bell icon** with unread count badge, link to notifications settings in admin dropdown

## Deviations from Plan

None -- plan executed exactly as written.

## Decisions Made

1. **Grouped Telegram per rule (max 10 products)** -- one message per rule listing matching products, capped at 10 to stay within Telegram message limits
2. **Global Telegram toggle** -- toggles telegram_enabled on all active rules at once rather than a separate config table
3. **Soft-delete rules** -- setting is_active=False preserves associated notification history
4. **30s polling for navbar badge** -- lightweight JSON endpoint, no WebSocket complexity for MVP
5. **Category criteria as name search** -- since product categories don't exist yet, falls back to keyword-in-name matching

## Verification Results

- App creates successfully with new models and tables
- Notifications page requires authentication (302 redirect)
- All imports verified (NotificationRule, Notification, check_and_notify, get_unread_notifications)

## Self-Check: PASSED

- FOUND: app/models/notification_rule.py
- FOUND: app/services/notification_service.py
- FOUND: app/templates/settings/notifications.html
- FOUND: app/static/js/notifications.js
- FOUND: commit d227dcc (Task 1)
- FOUND: commit 46d3f1f (Task 2)
