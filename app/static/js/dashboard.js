/* LabResta Sync — Dashboard polling, countdown, sync trigger, widget toggles */

(function () {
    'use strict';

    // --- Config ---
    const POLL_INTERVAL_NORMAL = 15000;   // 15 seconds
    const POLL_INTERVAL_SYNC = 5000;      // 5 seconds during sync
    const PROGRESS_POLL_INTERVAL = 2000;  // 2 seconds for progress
    const WIDGET_PREFS_KEY = 'dashboard_widget_prefs';

    // --- State ---
    let pollTimer = null;
    let progressTimer = null;
    let countdownSeconds = window._initialCountdownSeconds || null;
    let countdownTimer = null;
    let syncRunning = false;

    // --- Stage name mapping ---
    const stageNames = {
        fetching: 'Загрузка',
        parsing: 'Парсинг',
        saving: 'Сохранение',
        matching: 'Мэтчинг',
        yml_generation: 'YML генерация'
    };

    // =========================================================================
    // Widget Preferences
    // =========================================================================
    function loadWidgetPrefs() {
        try {
            const raw = localStorage.getItem(WIDGET_PREFS_KEY);
            return raw ? JSON.parse(raw) : {};
        } catch (e) {
            return {};
        }
    }

    function saveWidgetPrefs(prefs) {
        localStorage.setItem(WIDGET_PREFS_KEY, JSON.stringify(prefs));
    }

    function applyWidgetPrefs() {
        const prefs = loadWidgetPrefs();
        document.querySelectorAll('[data-widget-id]').forEach(function (el) {
            const id = el.getAttribute('data-widget-id');
            if (prefs[id] === false) {
                el.classList.add('d-none');
            } else {
                el.classList.remove('d-none');
            }
        });
        // Sync checkboxes
        document.querySelectorAll('.widget-toggle').forEach(function (cb) {
            var wid = cb.getAttribute('data-widget');
            if (prefs[wid] === false) {
                cb.checked = false;
            } else {
                cb.checked = true;
            }
        });
    }

    function initWidgetToggles() {
        applyWidgetPrefs();
        document.querySelectorAll('.widget-toggle').forEach(function (cb) {
            cb.addEventListener('change', function () {
                var prefs = loadWidgetPrefs();
                prefs[this.getAttribute('data-widget')] = this.checked;
                saveWidgetPrefs(prefs);
                applyWidgetPrefs();
            });
        });
    }

    // =========================================================================
    // Dashboard Data Polling
    // =========================================================================
    function fetchDashboardData() {
        fetch('/dashboard/stats')
            .then(function (r) { return r.json(); })
            .then(function (data) {
                updateWidgets(data);
                updateCountdown(data.next_sync_seconds);
                handleSyncState(data.sync_running);
            })
            .catch(function (err) {
                console.error('Dashboard poll error:', err);
            });

        // Also refresh journal
        fetch('/dashboard/journal')
            .then(function (r) { return r.json(); })
            .then(function (entries) {
                updateJournal(entries);
                updateEventFeed(entries);
            })
            .catch(function () {});
    }

    function updateWidgets(data) {
        // Last sync status
        var syncEl = document.getElementById('statLastSync');
        if (syncEl) {
            if (data.last_sync_status === 'success') {
                syncEl.innerHTML = '<span class="text-success">OK</span>';
            } else if (data.last_sync_status === 'error') {
                syncEl.innerHTML = '<span class="text-danger">ERR</span>';
            } else if (data.last_sync_status === 'running') {
                syncEl.innerHTML = '<span class="text-primary"><div class="spinner-border spinner-border-sm" role="status"></div></span>';
            } else {
                syncEl.innerHTML = '<span class="text-muted">--</span>';
            }
        }
        var syncTimeEl = document.getElementById('statLastSyncTime');
        if (syncTimeEl && data.last_sync_time) {
            syncTimeEl.textContent = data.last_sync_time.substring(0, 16);
        }

        // Counts
        setText('statMatched', data.matched_count);
        setText('statUnmatched', data.unmatched_count);
        setText('statPending', data.pending_review);

        // Errors
        var errEl = document.getElementById('statErrors');
        if (errEl) {
            var errCount = data.errors ? data.errors.length : 0;
            errEl.textContent = errCount;
            errEl.className = 'stat-number ' + (errCount > 0 ? 'text-danger' : 'text-muted');
        }
    }

    function setText(id, value) {
        var el = document.getElementById(id);
        if (el) el.textContent = value != null ? value : '--';
    }

    // =========================================================================
    // Sync State
    // =========================================================================
    function handleSyncState(running) {
        var btn = document.getElementById('triggerSyncBtn');
        var progressSection = document.getElementById('syncProgressSection');

        if (running && !syncRunning) {
            // Sync just started
            syncRunning = true;
            if (btn) {
                btn.disabled = true;
                btn.innerHTML = '<span class="spinner-border spinner-border-sm me-1" role="status"></span> Синхронизация...';
            }
            if (progressSection) progressSection.classList.remove('d-none');
            startProgressPolling();
            // Switch to faster polling
            restartPolling(POLL_INTERVAL_SYNC);
        } else if (!running && syncRunning) {
            // Sync just finished
            syncRunning = false;
            if (btn) {
                btn.disabled = false;
                btn.innerHTML = 'Запустить синхронизацию';
            }
            stopProgressPolling();
            // Brief delay then hide progress
            setTimeout(function () {
                if (progressSection) progressSection.classList.add('d-none');
            }, 3000);
            // Return to normal polling
            restartPolling(POLL_INTERVAL_NORMAL);
        }
    }

    // =========================================================================
    // Sync Progress Polling
    // =========================================================================
    function startProgressPolling() {
        stopProgressPolling();
        fetchProgress();
        progressTimer = setInterval(fetchProgress, PROGRESS_POLL_INTERVAL);
    }

    function stopProgressPolling() {
        if (progressTimer) {
            clearInterval(progressTimer);
            progressTimer = null;
        }
    }

    function fetchProgress() {
        fetch('/dashboard/sync/progress')
            .then(function (r) { return r.json(); })
            .then(function (data) {
                if (!data.running) return;
                updateProgressUI(data);
            })
            .catch(function () {});
    }

    function updateProgressUI(data) {
        var stages = data.stages || {};
        var stageOrder = ['fetching', 'parsing', 'saving', 'matching', 'yml_generation'];
        var doneCount = 0;
        var totalStages = stageOrder.length;

        for (var i = 0; i < stageOrder.length; i++) {
            var s = stages[stageOrder[i]];
            if (s && s.done) doneCount++;
        }

        // Current stage partial progress
        var currentStage = stages[data.stage];
        var partialProgress = 0;
        if (currentStage && currentStage.total && currentStage.total > 0) {
            partialProgress = currentStage.count / currentStage.total;
        }

        var pct = Math.round(((doneCount + partialProgress) / totalStages) * 100);
        pct = Math.min(pct, 100);

        var bar = document.getElementById('syncProgressBar');
        if (bar) {
            bar.style.width = pct + '%';
            bar.textContent = pct + '%';
        }

        // Update stats
        var fetching = stages.fetching;
        setText('progressFetched', fetching ? fetching.count : '--');

        var saving = stages.saving;
        setText('progressProcessed', saving ? (saving.created || 0) + (saving.updated || 0) : '--');

        setText('progressUnmatched', data.unmatched != null ? data.unmatched : '--');

        var stageName = stageNames[data.stage] || data.stage;
        if (currentStage && currentStage.total) {
            setText('progressStage', stageName + ' (' + currentStage.count + '/' + currentStage.total + ')');
        } else {
            setText('progressStage', stageName);
        }
    }

    // =========================================================================
    // Countdown Timer
    // =========================================================================
    function updateCountdown(seconds) {
        if (seconds != null && seconds >= 0) {
            countdownSeconds = seconds;
        }
    }

    function tickCountdown() {
        if (countdownSeconds == null) return;
        countdownSeconds = Math.max(0, countdownSeconds - 1);
        var el = document.getElementById('countdownValue');
        if (!el) return;

        if (countdownSeconds <= 0) {
            el.textContent = 'Синхронизация скоро запустится';
            return;
        }

        var h = Math.floor(countdownSeconds / 3600);
        var m = Math.floor((countdownSeconds % 3600) / 60);
        var s = countdownSeconds % 60;

        var parts = [];
        if (h > 0) parts.push(h + 'ч');
        if (m > 0 || h > 0) parts.push(m + 'м');
        parts.push(s + 'с');
        el.textContent = parts.join(' ');
    }

    // =========================================================================
    // Manual Sync Trigger
    // =========================================================================
    function triggerSync() {
        var btn = document.getElementById('triggerSyncBtn');
        if (btn) btn.disabled = true;

        fetchWithCSRF('/dashboard/sync/trigger', { method: 'POST' })
            .then(function (r) {
                if (r.status === 409) {
                    alert('Синхронизация уже запущена');
                    if (btn) btn.disabled = false;
                    return;
                }
                return r.json();
            })
            .then(function (data) {
                if (data && data.status === 'started') {
                    handleSyncState(true);
                    // Immediate poll
                    fetchDashboardData();
                }
            })
            .catch(function (err) {
                console.error('Sync trigger error:', err);
                if (btn) btn.disabled = false;
            });
    }

    // =========================================================================
    // Journal Updates
    // =========================================================================
    function updateJournal(entries) {
        var tbody = document.querySelector('#journalTable tbody');
        if (!tbody || !entries || entries.length === 0) return;

        var html = '';
        for (var i = 0; i < entries.length; i++) {
            var e = entries[i];
            var statusBadge = '';
            if (e.status === 'success') statusBadge = '<span class="badge bg-success">success</span>';
            else if (e.status === 'error') statusBadge = '<span class="badge bg-danger">error</span>';
            else if (e.status === 'running') statusBadge = '<span class="badge bg-primary">running</span>';
            else statusBadge = '<span class="badge bg-secondary">' + escapeHtml(e.status) + '</span>';

            html += '<tr>' +
                '<td>' + escapeHtml(e.supplier) + '</td>' +
                '<td>' + (e.started_at ? e.started_at.substring(0, 16) : '--') + '</td>' +
                '<td>' + (e.completed_at ? e.completed_at.substring(0, 16) : '--') + '</td>' +
                '<td>' + statusBadge + '</td>' +
                '<td>' + (e.products_fetched || 0) + '</td>' +
                '<td>' + (e.products_created || 0) + '</td>' +
                '<td>' + (e.products_updated || 0) + '</td>' +
                '<td>' + (e.products_disappeared || 0) + '</td>' +
                '<td>' + (e.match_candidates || 0) + '</td>' +
                '<td>' + (e.error_message ? '<span class="journal-error" title="' + escapeHtml(e.error_message) + '">' + escapeHtml(e.error_message) + '</span>' : '--') + '</td>' +
                '</tr>';
        }
        tbody.innerHTML = html;
    }

    function updateEventFeed(entries) {
        var feed = document.getElementById('eventFeed');
        if (!feed || !entries) return;

        var items = entries.slice(0, 10);
        if (items.length === 0) {
            feed.innerHTML = '<li class="list-group-item text-center text-muted">Нет событий</li>';
            return;
        }

        var html = '';
        for (var i = 0; i < items.length; i++) {
            var e = items[i];
            var icon = '';
            var text = '';
            if (e.status === 'success') {
                icon = '<span class="text-success">&#10003;</span>';
                text = escapeHtml(e.supplier) + ': синхронизация завершена (' + (e.products_fetched || 0) + ' получено, ' + (e.match_candidates || 0) + ' матчей)';
            } else if (e.status === 'error') {
                icon = '<span class="text-danger">&#10007;</span>';
                text = escapeHtml(e.supplier) + ': ошибка синхронизации';
            } else {
                icon = '<span class="text-primary">&#8635;</span>';
                text = escapeHtml(e.supplier) + ': синхронизация запущена';
            }

            var timeStr = e.started_at ? formatRelativeTime(e.started_at) : '';
            html += '<li class="list-group-item d-flex align-items-center gap-2">' +
                icon + '<span>' + text + '</span>' +
                '<span class="event-time ms-auto">' + timeStr + '</span>' +
                '</li>';
        }
        feed.innerHTML = html;
    }

    // =========================================================================
    // Helpers
    // =========================================================================
    function escapeHtml(str) {
        if (!str) return '';
        var div = document.createElement('div');
        div.appendChild(document.createTextNode(str));
        return div.innerHTML;
    }

    function formatRelativeTime(isoString) {
        try {
            var ts = new Date(isoString);
            var now = new Date();
            var diffMs = now - ts;
            var diffSec = Math.floor(diffMs / 1000);

            if (diffSec < 60) return 'только что';
            var diffMin = Math.floor(diffSec / 60);
            if (diffMin < 60) return diffMin + ' мин. назад';
            var diffHour = Math.floor(diffMin / 60);
            if (diffHour < 24) return diffHour + ' ч. назад';
            var diffDay = Math.floor(diffHour / 24);
            return diffDay + ' дн. назад';
        } catch (e) {
            return isoString ? isoString.substring(0, 16) : '';
        }
    }

    function restartPolling(interval) {
        if (pollTimer) clearInterval(pollTimer);
        pollTimer = setInterval(fetchDashboardData, interval);
    }

    // =========================================================================
    // Init
    // =========================================================================
    document.addEventListener('DOMContentLoaded', function () {
        // Widget toggles
        initWidgetToggles();

        // Sync button
        var syncBtn = document.getElementById('triggerSyncBtn');
        if (syncBtn) syncBtn.addEventListener('click', triggerSync);

        // Refresh button
        var refreshBtn = document.getElementById('refreshBtn');
        if (refreshBtn) refreshBtn.addEventListener('click', fetchDashboardData);

        // Start polling
        pollTimer = setInterval(fetchDashboardData, POLL_INTERVAL_NORMAL);

        // Start countdown
        countdownTimer = setInterval(tickCountdown, 1000);
        tickCountdown();

        // Check initial sync state
        if (document.getElementById('triggerSyncBtn') &&
            document.getElementById('triggerSyncBtn').disabled) {
            syncRunning = true;
            startProgressPolling();
        }
    });
})();
