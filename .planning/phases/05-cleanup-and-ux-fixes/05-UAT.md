---
status: testing
phase: 05-cleanup-and-ux-fixes
source: 05-01-SUMMARY.md, 05-02-SUMMARY.md
started: 2026-03-01T12:00:00Z
updated: 2026-03-01T12:00:00Z
---

## Current Test

number: 1
name: Bell Icon Opens Notification Dropdown
expected: |
  Click the bell icon in the navbar. A Bootstrap dropdown appears showing up to 5 recent unread notifications. Each item shows notification text. A "Mark all read" link is visible at the bottom.
awaiting: user response

## Tests

### 1. Bell Icon Opens Notification Dropdown
expected: Click the bell icon in the navbar. A Bootstrap dropdown appears showing up to 5 recent unread notifications with text. A "Mark all read" link is visible at the bottom.
result: [pending]

### 2. Global Badge Polling
expected: Navigate to any page (dashboard, matches, products, etc.) while logged in. The bell icon shows a badge with the unread notification count. The count refreshes automatically (every 30 seconds) without page reload.
result: [pending]

### 3. Badge Dismiss Button
expected: When the badge is visible on the bell icon, click the small (x) button on the badge. The badge disappears. The dropdown does NOT open (dismiss only hides the badge).
result: [pending]

### 4. Mark All Read from Dropdown
expected: Open the bell dropdown, click "Mark all read". All notifications are marked as read, the badge count resets to 0 or the badge disappears.
result: [pending]

### 5. Operator Notification Page Access
expected: Log in as an operator-role user. Navigate to the notifications page in settings. The page loads successfully (no 403 error). You see a list of notifications with a "Mark all read" button.
result: [pending]

### 6. Operator vs Admin Notification View
expected: As operator: the notifications page shows only the notification list and mark-all-read button — no rule management section. As admin: the notifications page shows the full management interface with notification rules.
result: [pending]

## Summary

total: 6
passed: 0
issues: 0
pending: 6
skipped: 0

## Gaps

[none yet]
