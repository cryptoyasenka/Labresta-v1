/* LabResta Sync -- Match Review interactions */

(function () {
    'use strict';

    // --- State ---
    const selectedIds = new Set();
    let saveTimeout = null;
    const STORAGE_KEY = 'match_review_state';
    const STATE_MAX_AGE_MS = 24 * 60 * 60 * 1000; // 24 hours

    // --- DOM refs ---
    const selectAllCb = document.getElementById('selectAll');
    const selectedCountEl = document.getElementById('selectedCount');
    const bulkConfirmBtn = document.getElementById('bulkConfirmBtn');
    const bulkRejectBtn = document.getElementById('bulkRejectBtn');
    const matchTable = document.getElementById('matchTable');
    const filterForm = document.getElementById('filterForm');

    // ========== Checkbox management ==========

    function getRowCheckboxes() {
        return matchTable ? matchTable.querySelectorAll('.row-checkbox') : [];
    }

    function updateBulkBar() {
        if (selectedCountEl) selectedCountEl.textContent = selectedIds.size;
        if (bulkConfirmBtn) bulkConfirmBtn.disabled = selectedIds.size === 0;
        if (bulkRejectBtn) bulkRejectBtn.disabled = selectedIds.size === 0;
    }

    if (selectAllCb) {
        selectAllCb.addEventListener('change', function () {
            const checked = this.checked;
            getRowCheckboxes().forEach(function (cb) {
                cb.checked = checked;
                var id = parseInt(cb.value, 10);
                if (checked) {
                    selectedIds.add(id);
                } else {
                    selectedIds.delete(id);
                }
            });
            updateBulkBar();
            scheduleSave();
        });
    }

    if (matchTable) {
        matchTable.addEventListener('change', function (e) {
            if (!e.target.classList.contains('row-checkbox')) return;
            var id = parseInt(e.target.value, 10);
            if (e.target.checked) {
                selectedIds.add(id);
            } else {
                selectedIds.delete(id);
                // Uncheck "select all" if any row unchecked
                if (selectAllCb) selectAllCb.checked = false;
            }
            updateBulkBar();
            scheduleSave();
        });
    }

    // ========== Individual confirm/reject ==========

    function showAlert(message, type) {
        var container = document.querySelector('.container-fluid');
        if (!container) return;
        var alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-' + type + ' alert-dismissible fade show';
        alertDiv.setAttribute('role', 'alert');
        alertDiv.innerHTML = message +
            '<button type="button" class="btn-close" data-bs-dismiss="alert"></button>';
        container.insertBefore(alertDiv, container.firstChild);
        // Auto-remove after 5 seconds
        setTimeout(function () {
            if (alertDiv.parentNode) alertDiv.remove();
        }, 5000);
    }

    var statusLabels = {
        candidate: 'Кандидат',
        confirmed: 'Подтвержден',
        rejected: 'Отклонен',
        manual: 'Ручной'
    };

    var statusClasses = {
        candidate: 'bg-secondary',
        confirmed: 'bg-success',
        rejected: 'bg-danger',
        manual: 'bg-info'
    };

    function updateRowStatus(matchId, newStatus) {
        var badge = document.getElementById('status-badge-' + matchId);
        if (badge) {
            badge.className = 'badge ' + (statusClasses[newStatus] || 'bg-secondary');
            badge.textContent = statusLabels[newStatus] || newStatus;
        }
        // Remove action buttons for terminal states
        if (newStatus === 'confirmed' || newStatus === 'rejected') {
            var actionsCell = document.getElementById('actions-' + matchId);
            if (actionsCell) actionsCell.innerHTML = '';
        }
    }

    if (matchTable) {
        matchTable.addEventListener('click', function (e) {
            var btn = e.target.closest('.confirm-btn, .reject-btn');
            if (!btn) return;

            var matchId = btn.getAttribute('data-id');
            var isConfirm = btn.classList.contains('confirm-btn');
            var action = isConfirm ? 'confirm' : 'reject';
            var msg = isConfirm
                ? 'Подтвердить этот матч?'
                : 'Отклонить этот матч?';

            if (!confirmAction(msg)) return;

            btn.disabled = true;
            // Disable sibling button too
            var row = btn.closest('tr');
            if (row) {
                row.querySelectorAll('.confirm-btn, .reject-btn').forEach(function (b) {
                    b.disabled = true;
                });
            }

            fetchWithCSRF('/matches/' + matchId + '/' + action, { method: 'POST' })
                .then(function (resp) {
                    if (!resp.ok) throw new Error('HTTP ' + resp.status);
                    return resp.json();
                })
                .then(function (data) {
                    if (data.status === 'ok') {
                        updateRowStatus(matchId, data.new_status);
                        showAlert(
                            isConfirm
                                ? 'Матч подтвержден'
                                : 'Матч отклонен' + (data.new_candidate_id ? '. Найден новый кандидат.' : ''),
                            isConfirm ? 'success' : 'warning'
                        );
                    } else {
                        throw new Error(data.message || 'Unknown error');
                    }
                })
                .catch(function (err) {
                    showAlert('Ошибка: ' + err.message, 'danger');
                    // Re-enable buttons
                    if (row) {
                        row.querySelectorAll('.confirm-btn, .reject-btn').forEach(function (b) {
                            b.disabled = false;
                        });
                    }
                });
        });
    }

    // ========== Bulk actions ==========

    function doBulkAction(action) {
        var ids = Array.from(selectedIds);
        var msg = action === 'confirm'
            ? 'Подтвердить ' + ids.length + ' матчей?'
            : 'Отклонить ' + ids.length + ' матчей?';

        if (!confirmAction(msg)) return;

        // Disable buttons during request
        if (bulkConfirmBtn) bulkConfirmBtn.disabled = true;
        if (bulkRejectBtn) bulkRejectBtn.disabled = true;

        fetchWithCSRF('/matches/bulk-action', {
            method: 'POST',
            body: JSON.stringify({ action: action, ids: ids })
        })
            .then(function (resp) {
                if (!resp.ok) throw new Error('HTTP ' + resp.status);
                return resp.json();
            })
            .then(function (data) {
                if (data.status === 'ok') {
                    // Reload page to reflect all changes
                    window.location.reload();
                } else {
                    throw new Error(data.message || 'Unknown error');
                }
            })
            .catch(function (err) {
                showAlert('Ошибка: ' + err.message, 'danger');
                if (bulkConfirmBtn) bulkConfirmBtn.disabled = selectedIds.size === 0;
                if (bulkRejectBtn) bulkRejectBtn.disabled = selectedIds.size === 0;
            });
    }

    if (bulkConfirmBtn) {
        bulkConfirmBtn.addEventListener('click', function () {
            doBulkAction('confirm');
        });
    }

    if (bulkRejectBtn) {
        bulkRejectBtn.addEventListener('click', function () {
            doBulkAction('reject');
        });
    }

    // ========== Sort by column click ==========
    // Column headers are already server-side links in the template.
    // No additional JS needed -- clicking the <a> navigates with sort params.

    // ========== Filter form: reset link ==========
    // The "Сбросить" link already points to the base URL via the template.

    // ========== Auto-save / restore state ==========

    function getCurrentState() {
        var statusEl = document.getElementById('statusFilter');
        var confidenceEl = document.getElementById('confidenceFilter');
        var searchEl = document.getElementById('searchInput');
        var perPageEl = document.getElementById('perPageSelect');

        return {
            filters: {
                status: statusEl ? statusEl.value : 'all',
                confidence: confidenceEl ? confidenceEl.value : 'all',
                search: searchEl ? searchEl.value : '',
                per_page: perPageEl ? perPageEl.value : '25'
            },
            page: getCurrentPage(),
            scrollPosition: window.scrollY,
            selectedIds: Array.from(selectedIds),
            timestamp: Date.now()
        };
    }

    function getCurrentPage() {
        var params = new URLSearchParams(window.location.search);
        return parseInt(params.get('page') || '1', 10);
    }

    function saveState() {
        try {
            var state = getCurrentState();
            localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
        } catch (e) {
            // localStorage may be unavailable
        }
    }

    function scheduleSave() {
        if (saveTimeout) clearTimeout(saveTimeout);
        saveTimeout = setTimeout(saveState, 500);
    }

    function restoreState() {
        try {
            var raw = localStorage.getItem(STORAGE_KEY);
            if (!raw) return;
            var state = JSON.parse(raw);

            // Check age
            if (Date.now() - state.timestamp > STATE_MAX_AGE_MS) {
                localStorage.removeItem(STORAGE_KEY);
                return;
            }

            // Only restore checkboxes if on the same page/filters
            // (filters are already in URL params, so they persist via server-side rendering)
            if (state.selectedIds && state.selectedIds.length > 0) {
                state.selectedIds.forEach(function (id) {
                    var cb = matchTable
                        ? matchTable.querySelector('.row-checkbox[value="' + id + '"]')
                        : null;
                    if (cb) {
                        cb.checked = true;
                        selectedIds.add(id);
                    }
                });
                updateBulkBar();
            }

            // Restore scroll position
            if (state.scrollPosition > 0) {
                setTimeout(function () {
                    window.scrollTo(0, state.scrollPosition);
                }, 100);
            }

            // Show restore toast if we actually restored something
            if (selectedIds.size > 0 || state.scrollPosition > 50) {
                showToast('Восстановлено предыдущее состояние');
            }
        } catch (e) {
            // Silently fail
        }
    }

    function showToast(message) {
        var toast = document.createElement('div');
        toast.className = 'position-fixed bottom-0 end-0 p-3';
        toast.style.zIndex = '1100';
        toast.innerHTML =
            '<div class="toast show align-items-center text-bg-light border" role="alert">' +
            '  <div class="d-flex">' +
            '    <div class="toast-body">' + message + '</div>' +
            '    <button type="button" class="btn-close me-2 m-auto" data-bs-dismiss="toast"></button>' +
            '  </div>' +
            '</div>';
        document.body.appendChild(toast);
        setTimeout(function () {
            if (toast.parentNode) toast.remove();
        }, 3000);
    }

    // Save on filter/pagination changes
    if (filterForm) {
        filterForm.addEventListener('change', scheduleSave);
    }
    window.addEventListener('scroll', scheduleSave);
    window.addEventListener('beforeunload', saveState);

    // Restore on page load
    restoreState();

})();
