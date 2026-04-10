/* LabResta Sync -- Match Review interactions */

(function () {
    'use strict';

    // --- State ---
    var selectedIds = new Set();
    var saveTimeout = null;
    var STORAGE_KEY = 'match_review_state';
    var STATE_MAX_AGE_MS = 24 * 60 * 60 * 1000; // 24 hours
    var diffActive = false;
    var searchDebounceTimer = null;
    var selectedPromProductId = null;

    // --- DOM refs ---
    var selectAllCb = document.getElementById('selectAll');
    var selectedCountEl = document.getElementById('selectedCount');
    var bulkConfirmBtn = document.getElementById('bulkConfirmBtn');
    var bulkRejectBtn = document.getElementById('bulkRejectBtn');
    var matchTable = document.getElementById('matchTable');
    var filterForm = document.getElementById('filterForm');
    var diffToggleBtn = document.getElementById('diffToggleBtn');

    // ========== Split.js resizable panels ==========

    var tablePanel = document.getElementById('matchTablePanel');
    var detailPanel = document.getElementById('matchDetailPanel');

    if (tablePanel && detailPanel && typeof Split !== 'undefined') {
        Split(['#matchTablePanel', '#matchDetailPanel'], {
            sizes: [70, 30],
            minSize: [400, 200],
            gutterSize: 8,
            direction: 'horizontal'
        });
    }

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
            var checked = this.checked;
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
        if (newStatus === 'confirmed' || newStatus === 'rejected') {
            var actionsCell = document.getElementById('actions-' + matchId);
            if (actionsCell) actionsCell.innerHTML = '';
        }
    }

    if (matchTable) {
        matchTable.addEventListener('click', function (e) {
            // Handle manual match button
            if (e.target.closest('.manual-match-btn')) {
                e.stopPropagation();
                openManualMatchModal(e.target.closest('.manual-match-btn'));
                return;
            }

            var btn = e.target.closest('.confirm-btn, .reject-btn');
            if (!btn) {
                // Click on row (not on buttons) -- show detail panel
                var row = e.target.closest('tr[data-match-id]');
                if (row && !e.target.closest('button, input, a')) {
                    showMatchDetail(row);
                }
                return;
            }

            var matchId = btn.getAttribute('data-id');
            var isConfirm = btn.classList.contains('confirm-btn');
            var action = isConfirm ? 'confirm' : 'reject';
            var msg = isConfirm
                ? 'Подтвердить этот матч?'
                : 'Отклонить этот матч?';

            if (!confirmAction(msg)) return;

            btn.disabled = true;
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

    // ========== Detail panel ==========

    function showMatchDetail(row) {
        var detailContent = document.getElementById('detailContent');
        if (!detailContent) return;

        var supplierName = row.getAttribute('data-supplier-name') || '-';
        var supplierBrand = row.getAttribute('data-supplier-brand') || '-';
        var supplierPrice = row.getAttribute('data-supplier-price') || '-';
        var supplierCurrency = row.getAttribute('data-supplier-currency') || 'EUR';
        var promName = row.getAttribute('data-prom-name') || '-';
        var promBrand = row.getAttribute('data-prom-brand') || '-';
        var promPrice = row.getAttribute('data-prom-price') || '-';
        var score = row.getAttribute('data-score') || '-';
        var status = row.getAttribute('data-status') || '-';
        var matchId = row.getAttribute('data-match-id');
        var discountPercent = row.getAttribute('data-discount-percent') || '';
        var supplierDefault = row.getAttribute('data-supplier-default-discount') || '0';
        var confirmedBy = row.getAttribute('data-confirmed-by') || '';

        // Highlight selected row
        if (matchTable) {
            matchTable.querySelectorAll('tr.table-active').forEach(function(r) {
                r.classList.remove('table-active');
            });
        }
        row.classList.add('table-active');

        var html =
            '<h6 class="border-bottom pb-2 mb-3">Детали матча</h6>' +
            '<div class="mb-3">' +
            '  <h6 class="text-muted mb-1">Товар поставщика</h6>' +
            '  <p class="mb-1"><strong>' + escapeHtml(supplierName) + '</strong></p>' +
            '  <small class="text-muted">Бренд: ' + escapeHtml(supplierBrand) + '</small><br>' +
            '  <small class="text-muted">Цена: ' + escapeHtml(supplierPrice) + ' ' + escapeHtml(supplierCurrency) + '</small>' +
            '</div>' +
            '<div class="mb-3">' +
            '  <h6 class="text-muted mb-1">Товар prom.ua</h6>' +
            '  <p class="mb-1"><strong>' + escapeHtml(promName) + '</strong></p>' +
            '  <small class="text-muted">Бренд: ' + escapeHtml(promBrand) + '</small><br>' +
            '  <small class="text-muted">Цена: ' + escapeHtml(promPrice) + ' EUR</small>' +
            '</div>' +
            '<div class="mb-3">' +
            '  <h6 class="text-muted mb-1">Сопоставление</h6>' +
            '  <p class="mb-1">Конфиденс: <strong>' + escapeHtml(score) + '%</strong></p>' +
            '  <p class="mb-0">Статус: <span class="badge ' + (statusClasses[status] || 'bg-secondary') + '">' +
            (statusLabels[status] || status) + '</span></p>' +
            '</div>';

        // Rule indicator
        if (confirmedBy.indexOf('rule:') === 0) {
            html += '<div class="mb-3"><span class="badge bg-warning bg-opacity-25 text-dark border">&#9889; Авто-подтверждено правилом</span></div>';
        }

        // Discount section for confirmed/manual matches
        if (status === 'confirmed' || status === 'manual') {
            html += '<div class="mb-3">' +
                '<h6 class="text-muted mb-1">Скидка (%)</h6>' +
                '<div class="input-group input-group-sm">' +
                '  <input type="number" id="discountInput" class="form-control" ' +
                '    min="0" max="100" step="0.1" value="' + escapeHtml(discountPercent) + '" ' +
                '    placeholder="' + escapeHtml(supplierDefault) + '%" data-match-id="' + matchId + '">' +
                '  <span class="input-group-text">%</span>' +
                '  <button class="btn btn-outline-secondary" id="clearDiscountBtn" type="button">Сбросить</button>' +
                '</div>' +
                '<div id="discountWarning" class="mt-1 small text-warning d-none"></div>' +
                '<div id="pricePreview" class="mt-1 small text-muted"></div>' +
                '</div>';
        }

        detailContent.innerHTML = html;

        // Show initial price preview if discount input is present
        if (status === 'confirmed' || status === 'manual') {
            updatePricePreview(discountPercent);
        }
    }

    function escapeHtml(str) {
        var div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    // ========== Discount management ==========

    var discountSaveTimer = null;

    document.addEventListener('input', function(e) {
        if (e.target.id !== 'discountInput') return;
        var val = e.target.value.trim();

        // Show warning for unusual values
        var warningEl = document.getElementById('discountWarning');
        if (warningEl) {
            if (val !== '' && (parseFloat(val) > 50 || parseFloat(val) === 0)) {
                warningEl.textContent = parseFloat(val) > 50
                    ? 'Внимание: скидка больше 50%'
                    : 'Внимание: скидка равна 0%';
                warningEl.classList.remove('d-none');
            } else {
                warningEl.classList.add('d-none');
            }
        }

        // Live price preview
        updatePricePreview(val);

        // Debounced save (500ms)
        if (discountSaveTimer) clearTimeout(discountSaveTimer);
        discountSaveTimer = setTimeout(function() {
            saveDiscount(e.target.getAttribute('data-match-id'), val);
        }, 500);
    });

    function updatePricePreview(discountVal) {
        var previewEl = document.getElementById('pricePreview');
        if (!previewEl) return;

        var activeRow = matchTable ? matchTable.querySelector('tr.table-active') : null;
        if (!activeRow) return;

        var priceStr = activeRow.getAttribute('data-supplier-price');
        var currency = activeRow.getAttribute('data-supplier-currency') || 'EUR';
        var supplierDefault = activeRow.getAttribute('data-supplier-default-discount') || '0';

        if (!priceStr) {
            previewEl.textContent = '';
            return;
        }

        var price = parseFloat(priceStr);
        var discount = discountVal !== '' ? parseFloat(discountVal) : parseFloat(supplierDefault);

        if (isNaN(price) || isNaN(discount)) {
            previewEl.textContent = '';
            return;
        }

        var calcPrice = price * (1 - discount / 100);
        previewEl.textContent = 'Расч. цена: ' + calcPrice.toFixed(2) + ' ' + currency +
            (discountVal === '' ? ' (скидка поставщика ' + supplierDefault + '%)' : '');
    }

    function saveDiscount(matchId, val) {
        if (!matchId) return;
        var discountPercent = val !== '' ? parseFloat(val) : null;

        // Validate range
        if (discountPercent !== null && (discountPercent < 0 || discountPercent > 100)) return;

        var input = document.getElementById('discountInput');
        if (input) input.disabled = true;

        fetchWithCSRF('/matches/' + matchId + '/discount', {
            method: 'POST',
            body: JSON.stringify({ discount_percent: discountPercent })
        })
        .then(function(resp) {
            if (!resp.ok) throw new Error('HTTP ' + resp.status);
            return resp.json();
        })
        .then(function(data) {
            if (data.status === 'ok') {
                // Update the data attribute on the row
                var row = matchTable ? matchTable.querySelector('tr[data-match-id="' + matchId + '"]') : null;
                if (row) {
                    row.setAttribute('data-discount-percent', data.discount_percent !== null ? data.discount_percent : '');
                }
            } else {
                showAlert('Ошибка: ' + (data.message || 'Unknown error'), 'danger');
            }
        })
        .catch(function(err) {
            showAlert('Ошибка сохранения скидки: ' + err.message, 'danger');
        })
        .finally(function() {
            if (input) input.disabled = false;
        });
    }

    document.addEventListener('click', function(e) {
        if (e.target.id !== 'clearDiscountBtn') return;
        var input = document.getElementById('discountInput');
        if (!input) return;
        input.value = '';
        var matchId = input.getAttribute('data-match-id');

        // Update preview
        updatePricePreview('');

        // Clear warning
        var warningEl = document.getElementById('discountWarning');
        if (warningEl) warningEl.classList.add('d-none');

        // Save immediately (null = clear override)
        if (discountSaveTimer) clearTimeout(discountSaveTimer);
        saveDiscount(matchId, '');
    });

    // ========== Diff highlighting ==========

    // Restore diff toggle state from localStorage
    var savedDiffState = localStorage.getItem('match_diff_active');
    if (savedDiffState === 'true') {
        diffActive = true;
        if (diffToggleBtn) diffToggleBtn.classList.add('active');
        applyDiffHighlighting();
    }

    if (diffToggleBtn) {
        diffToggleBtn.addEventListener('click', function () {
            diffActive = !diffActive;
            localStorage.setItem('match_diff_active', diffActive ? 'true' : 'false');
            this.classList.toggle('active', diffActive);

            if (diffActive) {
                applyDiffHighlighting();
            } else {
                removeDiffHighlighting();
            }
        });
    }

    function applyDiffHighlighting() {
        if (!matchTable) return;
        var rows = matchTable.querySelectorAll('tbody tr[data-match-id]');
        rows.forEach(function (row) {
            var supplierCell = row.querySelector('.supplier-name-cell');
            var promCell = row.querySelector('.prom-name-cell');
            if (!supplierCell || !promCell) return;

            var supplierName = row.getAttribute('data-supplier-name') || '';
            var promName = row.getAttribute('data-prom-name') || '';

            var result = charDiff(supplierName, promName);
            supplierCell.innerHTML = result.aHtml;
            promCell.innerHTML = result.bHtml;
        });
    }

    function removeDiffHighlighting() {
        if (!matchTable) return;
        var rows = matchTable.querySelectorAll('tbody tr[data-match-id]');
        rows.forEach(function (row) {
            var supplierCell = row.querySelector('.supplier-name-cell');
            var promCell = row.querySelector('.prom-name-cell');
            if (!supplierCell || !promCell) return;

            supplierCell.textContent = row.getAttribute('data-supplier-name') || '';
            promCell.textContent = row.getAttribute('data-prom-name') || '';
        });
    }

    /**
     * Simple character-level diff between two strings.
     * Returns {aHtml, bHtml} with <mark> tags around differing characters.
     */
    function charDiff(a, b) {
        var aLower = a.toLowerCase();
        var bLower = b.toLowerCase();
        var aHtml = '';
        var bHtml = '';
        var maxLen = Math.max(a.length, b.length);

        for (var i = 0; i < maxLen; i++) {
            var charA = a[i] || '';
            var charB = b[i] || '';
            var charAL = aLower[i] || '';
            var charBL = bLower[i] || '';

            if (charAL !== charBL) {
                if (charA) aHtml += '<mark>' + escapeHtml(charA) + '</mark>';
                if (charB) bHtml += '<mark>' + escapeHtml(charB) + '</mark>';
            } else {
                if (charA) aHtml += escapeHtml(charA);
                if (charB) bHtml += escapeHtml(charB);
            }
        }

        return { aHtml: aHtml, bHtml: bHtml };
    }

    // ========== Manual match modal ==========

    var manualMatchModal = null;
    var manualMatchModalEl = document.getElementById('manualMatchModal');
    if (manualMatchModalEl) {
        manualMatchModal = new bootstrap.Modal(manualMatchModalEl);
    }

    function openManualMatchModal(btn) {
        var supplierId = btn.getAttribute('data-supplier-id');
        var supplierName = btn.getAttribute('data-supplier-name');
        var supplierBrand = btn.getAttribute('data-supplier-brand');
        var supplierPrice = btn.getAttribute('data-supplier-price');
        var supplierCurrency = btn.getAttribute('data-supplier-currency') || 'EUR';

        document.getElementById('selectedSupplierProductId').value = supplierId;
        document.getElementById('modalSupplierName').textContent = supplierName;
        document.getElementById('modalSupplierBrand').textContent = supplierBrand || '-';
        document.getElementById('modalSupplierPrice').textContent =
            supplierPrice ? (supplierPrice + ' ' + supplierCurrency) : '-';

        // Reset modal state
        document.getElementById('catalogSearchInput').value = '';
        document.getElementById('catalogResultsList').innerHTML = '';
        document.getElementById('catalogSearchPlaceholder').style.display = '';
        document.getElementById('selectedProductAlert').classList.add('d-none');
        document.getElementById('selectedPromProductId').value = '';
        document.getElementById('submitManualMatch').disabled = true;
        document.getElementById('rememberMatchCheck').checked = false;
        selectedPromProductId = null;

        if (manualMatchModal) manualMatchModal.show();
    }

    // Catalog search with debounce
    var catalogSearchInput = document.getElementById('catalogSearchInput');
    if (catalogSearchInput) {
        catalogSearchInput.addEventListener('input', function () {
            var q = this.value.trim();
            if (searchDebounceTimer) clearTimeout(searchDebounceTimer);

            if (q.length < 2) {
                document.getElementById('catalogResultsList').innerHTML = '';
                document.getElementById('catalogSearchPlaceholder').style.display = '';
                return;
            }

            searchDebounceTimer = setTimeout(function () {
                searchCatalog(q);
            }, 300);
        });
    }

    function searchCatalog(query) {
        fetch('/matches/search-catalog?q=' + encodeURIComponent(query))
            .then(function (resp) {
                if (!resp.ok) throw new Error('HTTP ' + resp.status);
                return resp.json();
            })
            .then(function (products) {
                var list = document.getElementById('catalogResultsList');
                var placeholder = document.getElementById('catalogSearchPlaceholder');

                if (!products.length) {
                    list.innerHTML = '<p class="text-muted text-center p-2">Ничего не найдено</p>';
                    placeholder.style.display = 'none';
                    return;
                }

                placeholder.style.display = 'none';
                var html = '';
                products.forEach(function (p) {
                    html += '<a href="#" class="list-group-item list-group-item-action catalog-result-item" ' +
                        'data-product-id="' + p.id + '" data-product-name="' + escapeHtml(p.name) + '">' +
                        '<div class="d-flex justify-content-between">' +
                        '  <strong class="text-truncate" style="max-width:60%">' + escapeHtml(p.name) + '</strong>' +
                        '  <span class="text-muted">' + escapeHtml(p.price ? p.price + ' EUR' : '') + '</span>' +
                        '</div>' +
                        '<small class="text-muted">' +
                        (p.brand ? 'Бренд: ' + escapeHtml(p.brand) + ' | ' : '') +
                        (p.article ? 'Артикул: ' + escapeHtml(p.article) : '') +
                        '</small>' +
                        '</a>';
                });
                list.innerHTML = html;
            })
            .catch(function (err) {
                document.getElementById('catalogResultsList').innerHTML =
                    '<p class="text-danger text-center p-2">Ошибка поиска: ' + err.message + '</p>';
            });
    }

    // Select catalog product from results
    document.addEventListener('click', function (e) {
        var item = e.target.closest('.catalog-result-item');
        if (!item) return;
        e.preventDefault();

        selectedPromProductId = item.getAttribute('data-product-id');
        var productName = item.getAttribute('data-product-name');

        document.getElementById('selectedPromProductId').value = selectedPromProductId;
        document.getElementById('selectedProductName').textContent = productName;
        document.getElementById('selectedProductAlert').classList.remove('d-none');
        document.getElementById('submitManualMatch').disabled = false;

        // Highlight selected item
        var list = document.getElementById('catalogResultsList');
        list.querySelectorAll('.list-group-item').forEach(function (li) {
            li.classList.remove('active');
        });
        item.classList.add('active');
    });

    // Clear selected product
    var clearBtn = document.getElementById('clearSelectedProduct');
    if (clearBtn) {
        clearBtn.addEventListener('click', function () {
            selectedPromProductId = null;
            document.getElementById('selectedPromProductId').value = '';
            document.getElementById('selectedProductAlert').classList.add('d-none');
            document.getElementById('submitManualMatch').disabled = true;

            var list = document.getElementById('catalogResultsList');
            if (list) {
                list.querySelectorAll('.list-group-item').forEach(function (li) {
                    li.classList.remove('active');
                });
            }
        });
    }

    // Submit manual match
    var submitBtn = document.getElementById('submitManualMatch');
    if (submitBtn) {
        submitBtn.addEventListener('click', function () {
            var supplierProductId = document.getElementById('selectedSupplierProductId').value;
            var promProductId = document.getElementById('selectedPromProductId').value;
            var remember = document.getElementById('rememberMatchCheck').checked;

            if (!supplierProductId || !promProductId) return;

            submitBtn.disabled = true;

            fetchWithCSRF('/matches/manual', {
                method: 'POST',
                body: JSON.stringify({
                    supplier_product_id: parseInt(supplierProductId, 10),
                    prom_product_id: parseInt(promProductId, 10),
                    remember: remember
                })
            })
                .then(function (resp) {
                    if (!resp.ok) throw new Error('HTTP ' + resp.status);
                    return resp.json();
                })
                .then(function (data) {
                    if (data.status === 'ok') {
                        if (manualMatchModal) manualMatchModal.hide();
                        showAlert('Ручной матч создан' + (remember ? '. Правило сохранено.' : ''), 'success');
                        // Reload to reflect changes
                        setTimeout(function () {
                            window.location.reload();
                        }, 1000);
                    } else {
                        throw new Error(data.message || 'Unknown error');
                    }
                })
                .catch(function (err) {
                    showAlert('Ошибка: ' + err.message, 'danger');
                    submitBtn.disabled = false;
                });
        });
    }

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

            if (Date.now() - state.timestamp > STATE_MAX_AGE_MS) {
                localStorage.removeItem(STORAGE_KEY);
                return;
            }

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

            if (state.scrollPosition > 0) {
                setTimeout(function () {
                    window.scrollTo(0, state.scrollPosition);
                }, 100);
            }

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
