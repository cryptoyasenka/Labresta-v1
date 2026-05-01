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
    var bulkRecalcDiscountBtn = document.getElementById('bulkRecalcDiscountBtn');
    var bulkClampMarginBtn = document.getElementById('bulkClampMarginBtn');
    var customFeedBtn = document.getElementById('customFeedBtn');
    var customFeedCountEl = document.getElementById('customFeedCount');
    var matchTable = document.getElementById('matchTable');
    var filterForm = document.getElementById('filterForm');
    var diffToggleBtn = document.getElementById('diffToggleBtn');

    // ========== Sticky header offset (filter bar height -> CSS var for thead) ==========

    var stickyHeader = document.getElementById('matchesStickyHeader');
    if (stickyHeader) {
        var updateStickyOffset = function () {
            var h = stickyHeader.getBoundingClientRect().height;
            document.documentElement.style.setProperty(
                '--matches-sticky-top-offset', h + 'px'
            );
        };
        updateStickyOffset();
        window.addEventListener('resize', updateStickyOffset);
        // Re-measure after fonts/images finish loading (navbar wrapping, etc.)
        if (document.readyState !== 'complete') {
            window.addEventListener('load', updateStickyOffset);
        }
    }

    // ========== Checkbox management ==========

    function getRowCheckboxes() {
        return matchTable ? matchTable.querySelectorAll('.row-checkbox') : [];
    }

    function updateBulkBar() {
        if (selectedCountEl) selectedCountEl.textContent = selectedIds.size;
        if (bulkConfirmBtn) bulkConfirmBtn.disabled = selectedIds.size === 0;
        if (bulkRejectBtn) bulkRejectBtn.disabled = selectedIds.size === 0;
        if (bulkRecalcDiscountBtn) bulkRecalcDiscountBtn.disabled = selectedIds.size === 0;
        if (bulkClampMarginBtn) bulkClampMarginBtn.disabled = selectedIds.size === 0;
        if (customFeedBtn) customFeedBtn.disabled = selectedIds.size === 0;
        if (customFeedCountEl) customFeedCountEl.textContent = selectedIds.size;
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

    // Alerts are pinned to the top of the VIEWPORT (not document). When the
    // operator scrolls deep into a long match list and an action fails, the
    // old container-top alert was rendered above the visible area and missed
    // entirely — the action silently "didn't work". Fixed positioning +
    // longer timeout for errors ensures they're always seen.
    function showAlert(message, type) {
        var alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-' + type + ' alert-dismissible fade show shadow js-floating-alert';
        alertDiv.setAttribute('role', 'alert');
        alertDiv.style.position = 'fixed';
        alertDiv.style.top = '72px';
        alertDiv.style.left = '50%';
        alertDiv.style.transform = 'translateX(-50%)';
        alertDiv.style.zIndex = '1080';
        alertDiv.style.maxWidth = '90vw';
        alertDiv.style.minWidth = '320px';
        // Stack multiple alerts vertically instead of overlapping.
        var existing = document.querySelectorAll('.js-floating-alert');
        if (existing.length) {
            var offset = 72;
            existing.forEach(function (el) {
                offset += el.offsetHeight + 8;
            });
            alertDiv.style.top = offset + 'px';
        }
        // Text only — error messages may splice in names from supplier feeds
        // (uncontrolled source), so never innerHTML. Callers that want
        // formatting should build DOM nodes after calling showAlert.
        alertDiv.appendChild(document.createTextNode(message));
        var closeBtn = document.createElement('button');
        closeBtn.type = 'button';
        closeBtn.className = 'btn-close';
        closeBtn.setAttribute('data-bs-dismiss', 'alert');
        alertDiv.appendChild(closeBtn);
        document.body.appendChild(alertDiv);
        // Errors/warnings linger longer — operator needs time to read them.
        var timeoutMs = (type === 'danger' || type === 'warning') ? 10000 : 5000;
        setTimeout(function () {
            if (alertDiv.parentNode) alertDiv.remove();
        }, timeoutMs);
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
        var actionsCell = document.getElementById('actions-' + matchId);
        if (!actionsCell) return;
        if (newStatus === 'rejected') {
            actionsCell.innerHTML = '';
        } else if (newStatus === 'confirmed' || newStatus === 'manual') {
            // Replace candidate-action buttons with «Отменить матч» so operator
            // can revert without page reload (phase B requirement).
            actionsCell.querySelectorAll('.confirm-btn, .reject-btn, .confirm-update-btn').forEach(function (b) {
                b.remove();
            });
            if (!actionsCell.querySelector('.unconfirm-btn')) {
                var unBtn = document.createElement('button');
                unBtn.className = 'btn btn-sm btn-outline-warning unconfirm-btn';
                unBtn.setAttribute('data-id', matchId);
                unBtn.title = 'Вернуть матч в статус кандидата (если подтвердили по ошибке)';
                unBtn.textContent = 'Отменить матч';
                actionsCell.insertBefore(unBtn, actionsCell.firstChild);
            }
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

            // Handle details button
            if (e.target.closest('.details-btn')) {
                e.stopPropagation();
                var detailsBtn = e.target.closest('.details-btn');
                openDetailsModal(detailsBtn.getAttribute('data-id'));
                return;
            }

            // Handle confirm + update button
            if (e.target.closest('.confirm-update-btn')) {
                e.stopPropagation();
                var cuBtn = e.target.closest('.confirm-update-btn');
                handleConfirmUpdate(cuBtn);
                return;
            }

            // Handle unconfirm button (revert confirmed → candidate)
            if (e.target.closest('.unconfirm-btn')) {
                e.stopPropagation();
                var uBtn = e.target.closest('.unconfirm-btn');
                handleUnconfirm(uBtn);
                return;
            }

            // Handle unpublish / republish (phase C — keep match, toggle feed inclusion)
            if (e.target.closest('.unpublish-btn')) {
                e.stopPropagation();
                handleFeedToggle(e.target.closest('.unpublish-btn'), 'unpublish');
                return;
            }
            if (e.target.closest('.republish-btn')) {
                e.stopPropagation();
                handleFeedToggle(e.target.closest('.republish-btn'), 'republish');
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
                row.querySelectorAll('.confirm-btn, .reject-btn, .confirm-update-btn').forEach(function (b) {
                    b.disabled = true;
                });
            }

            fetchWithCSRF('/matches/' + matchId + '/' + action, { method: 'POST' })
                .then(parseJsonOrFriendly)
                .then(function (data) {
                    if (data.status === 'ok') {
                        if (!isConfirm && row) {
                            // Reject deletes the match on the server.
                            // Drop the row so it doesn't linger under the candidate filter.
                            row.parentNode && row.parentNode.removeChild(row);
                            selectedIds.delete(parseInt(matchId, 10));
                            updateBulkBar();
                            showAlert(
                                'Матч отклонен' + (data.new_candidate_id
                                    ? '. Найден новый кандидат — обновите страницу.'
                                    : '.'),
                                'warning'
                            );
                        } else {
                            updateRowStatus(matchId, data.new_status);
                            showAlert('Матч подтвержден', 'success');
                        }
                    } else {
                        throw new Error(data.message || ('HTTP ' + (data.__status || '?')));
                    }
                })
                .catch(function (err) {
                    showAlert('Ошибка: ' + err.message, 'danger');
                    if (row) {
                        row.querySelectorAll('.confirm-btn, .reject-btn, .confirm-update-btn').forEach(function (b) {
                            b.disabled = false;
                        });
                    }
                });
        });
    }

    // ========== Confirm + Update Name ==========

    function handleConfirmUpdate(btn) {
        var matchId = btn.getAttribute('data-id');
        var row = btn.closest('tr');
        var supplierName = row ? row.getAttribute('data-supplier-name') : '';
        var promName = row ? row.getAttribute('data-prom-name') : '';

        if (!confirmAction('Подтвердить матч и обновить название каталога?\n\nБыло: ' + promName + '\nСтанет: ' + supplierName)) return;

        btn.disabled = true;
        if (row) {
            row.querySelectorAll('.confirm-btn, .reject-btn, .confirm-update-btn').forEach(function (b) {
                b.disabled = true;
            });
        }

        fetchWithCSRF('/matches/' + matchId + '/confirm-update', { method: 'POST' })
            .then(parseJsonOrFriendly)
            .then(function (data) {
                if (data.status === 'ok') {
                    updateRowStatus(matchId, data.new_status);
                    // Update the catalog name cell in the table
                    if (row) {
                        var promId = row.getAttribute('data-prom-id');
                        var siblings = promId && matchTable
                            ? matchTable.querySelectorAll('tr[data-prom-id="' + promId + '"]')
                            : [row];
                        siblings.forEach(function (r) {
                            var promCell = r.querySelector('.prom-name-cell');
                            if (promCell && !r.dataset.feedName) {
                                var ns = promCell.querySelector('.prom-name-text');
                                if (ns) ns.textContent = data.new_name;
                            }
                            r.setAttribute('data-prom-name', data.new_name);
                        });
                    }
                    // Build diff message showing old → new name
                    var msg = '<strong>Матч підтверджено + назву оновлено</strong><br>';
                    msg += '<span class="text-decoration-line-through text-danger">' + escapeHtml(data.old_name) + '</span><br>';
                    msg += '<span class="text-success">' + escapeHtml(data.new_name) + '</span>';
                    if (data.name_ru) msg += '<br><small class="text-muted">RU: ' + escapeHtml(data.name_ru) + '</small>';
                    showAlert(msg, 'success');
                } else {
                    throw new Error(data.message || 'Unknown error');
                }
            })
            .catch(function (err) {
                showAlert('Ошибка: ' + err.message, 'danger');
                if (row) {
                    row.querySelectorAll('.confirm-btn, .reject-btn, .confirm-update-btn').forEach(function (b) {
                        b.disabled = false;
                    });
                }
            });
    }

    // ========== Unconfirm (revert confirmed → candidate) ==========

    function handleUnconfirm(btn) {
        var matchId = btn.getAttribute('data-id');
        if (!confirmAction('Вернуть матч в статус кандидата?\n\nЕсли хотите выбрать другой товар каталога, потом нажмите «Сопоставить вручную».')) return;

        btn.disabled = true;

        fetchWithCSRF('/matches/' + matchId + '/unconfirm', { method: 'POST' })
            .then(function (resp) {
                if (!resp.ok) throw new Error('HTTP ' + resp.status);
                return resp.json();
            })
            .then(function (data) {
                if (data.status === 'ok') {
                    showAlert('Подтверждение отменено', 'warning');
                    // Reload to restore candidate action buttons
                    setTimeout(function () { window.location.reload(); }, 600);
                } else {
                    throw new Error(data.message || 'Unknown error');
                }
            })
            .catch(function (err) {
                showAlert('Ошибка: ' + err.message, 'danger');
                btn.disabled = false;
            });
    }

    // ========== Feed management (phase C) ==========

    function handleFeedToggle(btn, action) {
        var matchId = btn.getAttribute('data-id');
        var row = btn.closest('tr[data-match-id]');
        btn.disabled = true;
        fetchWithCSRF('/matches/' + matchId + '/' + action, { method: 'POST' })
            .then(function (resp) {
                return resp.json().then(function (data) {
                    if (!resp.ok) throw new Error(data.message || 'HTTP ' + resp.status);
                    return data;
                });
            })
            .then(function (data) {
                // Replace button with its counterpart
                var newBtn = document.createElement('button');
                if (action === 'unpublish') {
                    newBtn.className = 'btn btn-sm btn-dark republish-btn';
                    newBtn.textContent = 'Вернуть в фид';
                    newBtn.title = 'Вернуть в фид — на следующем «Обновить фид» попадёт в YML';
                    showAlert('Матч #' + matchId + ' снят с фида. Нажмите «Обновить фид» для пересборки YML.', 'warning');
                } else {
                    newBtn.className = 'btn btn-sm btn-outline-dark unpublish-btn';
                    newBtn.textContent = 'Снять с фида';
                    newBtn.title = 'Снять с фида (оставить матч в БД, убрать из labresta-feed.yml)';
                    showAlert('Матч #' + matchId + ' вернётся в фид на следующем «Обновить фид».', 'info');
                }
                newBtn.setAttribute('data-id', matchId);
                btn.parentNode.replaceChild(newBtn, btn);

                // Update «В фиде» cell immediately
                if (row) {
                    var feedCell = row.querySelector('.in-feed-cell');
                    if (feedCell) {
                        if (action === 'unpublish') {
                            feedCell.innerHTML = '<span class="badge bg-warning text-dark" title="Снят с фида">&#8856;</span>';
                            feedCell.setAttribute('title', 'Нет в фиде (снят вручную)');
                        } else {
                            feedCell.innerHTML = '<span class="badge bg-secondary">&mdash;</span>';
                            feedCell.setAttribute('title', 'Нет в фиде — нажмите «Обновить фид»');
                        }
                    }
                }
            })
            .catch(function (err) {
                showAlert('Ошибка: ' + err.message, 'danger');
                btn.disabled = false;
            });
    }

    var regenerateFeedBtn = document.getElementById('regenerateFeedBtn');
    var regenerateFeedStatus = document.getElementById('regenerateFeedStatus');
    if (regenerateFeedBtn) {
        regenerateFeedBtn.addEventListener('click', function () {
            regenerateFeedBtn.disabled = true;
            var originalLabel = regenerateFeedBtn.textContent;
            regenerateFeedBtn.textContent = 'Генерация...';
            if (regenerateFeedStatus) regenerateFeedStatus.textContent = '';

            fetchWithCSRF('/matches/regenerate-feed', { method: 'POST' })
                .then(function (resp) {
                    return resp.json().then(function (data) {
                        if (!resp.ok) throw new Error(data.message || 'HTTP ' + resp.status);
                        return data;
                    });
                })
                .then(function (data) {
                    var msg = 'Фид обновлён: ' + data.total + ' офферов (' +
                              data.available + ' в наличии, ' + data.unavailable + ' нет)';
                    if (regenerateFeedStatus) regenerateFeedStatus.textContent = msg;
                    showAlert(msg, 'success');
                    // Reload so in_feed column reflects new state.
                    setTimeout(function () { window.location.reload(); }, 1200);
                })
                .catch(function (err) {
                    showAlert('Ошибка регенерации фида: ' + err.message, 'danger');
                    regenerateFeedBtn.disabled = false;
                    regenerateFeedBtn.textContent = originalLabel;
                });
        });
    }

    // Phase K.4 — custom feed from selected matches
    var customFeedModal = null;
    var customFeedModalEl = document.getElementById('customFeedModal');
    if (customFeedModalEl) customFeedModal = new bootstrap.Modal(customFeedModalEl);
    var customFeedNameInput = document.getElementById('customFeedNameInput');
    var customFeedCountModalEl = document.getElementById('customFeedCountModal');
    var customFeedResultEl = document.getElementById('customFeedResult');
    var customFeedUrlOutput = document.getElementById('customFeedUrlOutput');
    var customFeedCopyBtn = document.getElementById('customFeedCopyBtn');
    var customFeedErrorEl = document.getElementById('customFeedError');
    var customFeedGenerateBtn = document.getElementById('customFeedGenerateBtn');

    if (customFeedBtn && customFeedModal) {
        customFeedBtn.addEventListener('click', function () {
            if (selectedIds.size === 0) return;
            if (customFeedNameInput) customFeedNameInput.value = '';
            if (customFeedResultEl) customFeedResultEl.classList.add('d-none');
            if (customFeedErrorEl) customFeedErrorEl.classList.add('d-none');
            if (customFeedCountModalEl) customFeedCountModalEl.textContent = selectedIds.size;
            if (customFeedGenerateBtn) {
                customFeedGenerateBtn.disabled = false;
                customFeedGenerateBtn.textContent = 'Сгенерировать фид';
            }
            customFeedModal.show();
        });
    }

    if (customFeedGenerateBtn) {
        customFeedGenerateBtn.addEventListener('click', function () {
            if (selectedIds.size === 0) return;
            customFeedGenerateBtn.disabled = true;
            customFeedGenerateBtn.textContent = 'Генерация...';
            if (customFeedErrorEl) customFeedErrorEl.classList.add('d-none');

            var payload = {
                match_ids: Array.from(selectedIds),
                name: customFeedNameInput ? customFeedNameInput.value.trim() : ''
            };
            fetchWithCSRF('/matches/regenerate-custom', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            })
                .then(function (resp) {
                    return resp.json().then(function (data) {
                        if (!resp.ok) throw new Error(data.message || 'HTTP ' + resp.status);
                        return data;
                    });
                })
                .then(function (data) {
                    if (customFeedUrlOutput) customFeedUrlOutput.value = data.url || '';
                    if (customFeedResultEl) customFeedResultEl.classList.remove('d-none');
                    customFeedGenerateBtn.disabled = false;
                    customFeedGenerateBtn.textContent = 'Сгенерировать ещё раз';
                })
                .catch(function (err) {
                    if (customFeedErrorEl) {
                        customFeedErrorEl.textContent = 'Ошибка: ' + err.message;
                        customFeedErrorEl.classList.remove('d-none');
                    }
                    customFeedGenerateBtn.disabled = false;
                    customFeedGenerateBtn.textContent = 'Сгенерировать фид';
                });
        });
    }

    if (customFeedCopyBtn && customFeedUrlOutput) {
        customFeedCopyBtn.addEventListener('click', function () {
            customFeedUrlOutput.select();
            customFeedUrlOutput.setSelectionRange(0, customFeedUrlOutput.value.length);
            var done = function () {
                var prev = customFeedCopyBtn.textContent;
                customFeedCopyBtn.textContent = 'Скопировано';
                customFeedCopyBtn.classList.add('btn-success');
                customFeedCopyBtn.classList.remove('btn-outline-secondary');
                setTimeout(function () {
                    customFeedCopyBtn.textContent = prev;
                    customFeedCopyBtn.classList.remove('btn-success');
                    customFeedCopyBtn.classList.add('btn-outline-secondary');
                }, 1500);
            };
            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(customFeedUrlOutput.value).then(done).catch(function () {
                    document.execCommand('copy');
                    done();
                });
            } else {
                document.execCommand('copy');
                done();
            }
        });
    }

    // ========== Details Comparison Modal ==========

    var detailsModal = null;
    var detailsModalEl = document.getElementById('detailsModal');
    if (detailsModalEl) {
        detailsModal = new bootstrap.Modal(detailsModalEl);
    }

    function openDetailsModal(matchId) {
        if (!detailsModal) return;

        var body = document.getElementById('detailsModalBody');
        body.innerHTML = '<div class="text-center py-4"><div class="spinner-border text-primary"></div><p class="mt-2 text-muted">Загрузка...</p></div>';
        detailsModal.show();

        fetch('/matches/' + matchId + '/details')
            .then(function (resp) {
                if (!resp.ok) throw new Error('HTTP ' + resp.status);
                return resp.json();
            })
            .then(function (data) {
                renderDetailsModal(body, data);
            })
            .catch(function (err) {
                body.innerHTML = '<div class="alert alert-danger">Ошибка загрузки: ' + escapeHtml(err.message) + '</div>';
            });
    }

    function renderDetailsModal(container, data) {
        var sp = data.supplier;
        var pp = data.catalog;
        var match = data.match;

        var html = '<div class="row" data-match-id="' + match.id + '">';

        // --- Names comparison (editable on catalog side) ---
        html += '<div class="col-12 mb-3">';
        html += '<h6>Названия <small class="text-muted">(поля каталога можно редактировать)</small></h6>';
        html += '<table class="table table-sm table-bordered">';
        html += '<thead><tr><th width="20%"></th><th width="40%">Поставщик</th><th width="40%">Каталог Horoshop</th></tr></thead>';
        html += '<tbody>';
        html += '<tr><td><strong>UA</strong></td>';
        html += '<td>' + escapeHtml(sp.name || '-') + '</td>';
        html += '<td' + (sp.name !== pp.name ? ' class="table-warning"' : '') + '>';
        html += '<textarea class="form-control form-control-sm prom-edit-field" rows="2" data-field="name">' + escapeHtml(pp.name || '') + '</textarea>';
        html += '</td></tr>';
        html += '<tr><td><strong>RU</strong></td>';
        html += '<td class="text-muted">—</td>';
        html += '<td><textarea class="form-control form-control-sm prom-edit-field" rows="2" data-field="name_ru">' + escapeHtml(pp.name_ru || '') + '</textarea></td></tr>';
        html += '<tr><td><strong>Арт. виробника</strong></td>';
        html += '<td>' + escapeHtml(sp.article || '—') + '</td>';
        html += '<td class="font-monospace">' + escapeHtml(pp.display_article || '—') + '</td></tr>';
        html += '</tbody></table></div>';

        // --- Photos ---
        html += '<div class="col-12 mb-3">';
        html += '<h6>Фото</h6>';
        html += '<div class="row">';
        html += '<div class="col-6">';
        html += '<p class="text-muted small mb-1">Поставщик (' + (sp.images ? sp.images.length : 0) + ' фото)</p>';
        if (sp.images && sp.images.length > 0) {
            sp.images.forEach(function (url) {
                html += '<a href="' + escapeHtml(url) + '" target="_blank"><img src="' + escapeHtml(url) + '" class="img-thumbnail me-1 mb-1" style="max-height:100px;max-width:100px;" onerror="this.style.display=\'none\'"></a>';
            });
        } else {
            html += '<span class="text-muted">Нет фото</span>';
        }
        html += '</div>';
        html += '<div class="col-6">';
        html += '<p class="text-muted small mb-1">Каталог (' + (pp.images ? pp.images.length : 0) + ' фото)</p>';
        if (pp.image_url) {
            html += '<a href="' + escapeHtml(pp.image_url) + '" target="_blank"><img src="' + escapeHtml(pp.image_url) + '" class="img-thumbnail me-1 mb-1" style="max-height:100px;max-width:100px;" onerror="this.style.display=\'none\'"></a>';
        }
        if (!pp.image_url && (!pp.images || pp.images.length === 0)) {
            html += '<span class="text-muted">Нет фото</span>';
        }
        html += '</div></div></div>';

        // --- Characteristics ---
        html += '<div class="col-12 mb-3">';
        html += '<h6>Характеристики поставщика</h6>';
        if (sp.params && Object.keys(sp.params).length > 0) {
            html += '<table class="table table-sm table-bordered"><thead><tr><th>Параметр</th><th>Значение</th></tr></thead><tbody>';
            Object.keys(sp.params).forEach(function (key) {
                html += '<tr><td>' + escapeHtml(key) + '</td><td>' + escapeHtml(sp.params[key]) + '</td></tr>';
            });
            html += '</tbody></table>';
        } else {
            html += '<p class="text-muted">Нет характеристик в фиде поставщика</p>';
        }
        html += '</div>';

        // --- Description (editable on catalog side) ---
        html += '<div class="col-12 mb-3">';
        html += '<h6>Описание <small class="text-muted">(каталог Horoshop — можно редактировать)</small></h6>';
        html += '<div class="row">';
        html += '<div class="col-6"><p class="text-muted small mb-1">Поставщик (только чтение)</p>';
        html += '<div class="border rounded p-2 small" style="max-height:200px;overflow:auto;">' + (sp.description || '<span class="text-muted">Нет</span>') + '</div></div>';
        html += '<div class="col-6"><p class="text-muted small mb-1">Каталог UA</p>';
        html += '<textarea class="form-control form-control-sm prom-edit-field" rows="6" data-field="description_ua" placeholder="HTML описания (UA)">' + escapeHtml(pp.description_ua || '') + '</textarea>';
        html += '</div>';
        html += '</div>';
        html += '<div class="row mt-2">';
        html += '<div class="col-6"></div>';
        html += '<div class="col-6"><p class="text-muted small mb-1">Каталог RU</p>';
        html += '<textarea class="form-control form-control-sm prom-edit-field" rows="4" data-field="description_ru" placeholder="HTML описания (RU)">' + escapeHtml(pp.description_ru || '') + '</textarea>';
        html += '</div>';
        html += '</div></div>';

        // --- Match info ---
        html += '<div class="col-12">';
        html += '<div class="d-flex gap-2 align-items-center">';
        html += '<span class="badge ' + (statusClasses[match.status] || 'bg-secondary') + '">' + (statusLabels[match.status] || match.status) + '</span>';
        html += '<span>Конфиденс: <strong>' + match.score.toFixed(0) + '%</strong></span>';
        if (match.name_synced) {
            html += '<span class="badge bg-info">Название обновлено</span>';
        }
        html += '</div></div>';

        html += '</div>';
        container.innerHTML = html;

        // Reset the save status indicator whenever a new match is loaded
        var statusEl = document.getElementById('detailsModalSaveStatus');
        if (statusEl) statusEl.textContent = '';
        var saveBtn = document.getElementById('detailsModalSaveBtn');
        if (saveBtn) saveBtn.disabled = false;
    }

    // ========== Details modal save (edit catalog fields) ==========

    var detailsSaveBtn = document.getElementById('detailsModalSaveBtn');
    if (detailsSaveBtn) {
        detailsSaveBtn.addEventListener('click', function () {
            var body = document.getElementById('detailsModalBody');
            if (!body) return;
            var wrapper = body.querySelector('[data-match-id]');
            if (!wrapper) return;
            var matchId = wrapper.getAttribute('data-match-id');
            if (!matchId) return;

            var payload = {};
            wrapper.querySelectorAll('.prom-edit-field').forEach(function (el) {
                var field = el.getAttribute('data-field');
                if (field) payload[field] = el.value;
            });

            if (!payload.name || !payload.name.trim()) {
                showDetailsStatus('Название UA не может быть пустым', 'danger');
                return;
            }

            detailsSaveBtn.disabled = true;
            showDetailsStatus('Сохранение...', 'muted');

            fetchWithCSRF('/matches/' + matchId + '/update-prom', {
                method: 'POST',
                body: JSON.stringify(payload)
            })
                .then(function (resp) {
                    if (!resp.ok) {
                        return resp.json().then(function (data) {
                            throw new Error(data.message || 'HTTP ' + resp.status);
                        }).catch(function () {
                            throw new Error('HTTP ' + resp.status);
                        });
                    }
                    return resp.json();
                })
                .then(function (data) {
                    if (data.status !== 'ok') {
                        throw new Error(data.message || 'Unknown error');
                    }
                    var updatedCount = data.updated ? Object.keys(data.updated).length : 0;
                    if (updatedCount === 0) {
                        showDetailsStatus('Нет изменений', 'muted');
                    } else {
                        showDetailsStatus('✓ Сохранено (' + updatedCount + ' полей)', 'success');
                    }

                    // Reflect the new UA name in the row of the match table so
                    // the operator immediately sees the fix without a reload.
                    if (data.updated && 'name' in data.updated && matchTable) {
                        var currentRow = matchTable.querySelector('tr[data-match-id="' + matchId + '"]');
                        var promId = currentRow ? currentRow.getAttribute('data-prom-id') : null;
                        var rowsToUpdate = promId
                            ? matchTable.querySelectorAll('tr[data-prom-id="' + promId + '"]')
                            : (currentRow ? [currentRow] : []);
                        rowsToUpdate.forEach(function (r) {
                            var promCell = r.querySelector('.prom-name-cell');
                            if (promCell && !r.dataset.feedName) {
                                var ns = promCell.querySelector('.prom-name-text');
                                if (ns) ns.textContent = data.updated.name;
                            }
                            r.setAttribute('data-prom-name', data.updated.name);
                        });
                    }
                })
                .catch(function (err) {
                    showDetailsStatus('Ошибка: ' + err.message, 'danger');
                })
                .finally(function () {
                    detailsSaveBtn.disabled = false;
                });
        });
    }

    function showDetailsStatus(message, kind) {
        var el = document.getElementById('detailsModalSaveStatus');
        if (!el) return;
        el.textContent = message;
        el.className = 'me-auto small ' + (
            kind === 'success' ? 'text-success' :
            kind === 'danger' ? 'text-danger' :
            'text-muted'
        );
    }

    // ========== Bulk actions ==========

    function doBulkAction(action) {
        var ids = Array.from(selectedIds);
        var msg;
        if (action === 'confirm') msg = 'Подтвердить ' + ids.length + ' матчей?';
        else if (action === 'reject') msg = 'Отклонить ' + ids.length + ' матчей?';
        else if (action === 'recalc_discount') msg = 'Пересчитать скидку для ' + ids.length + ' матчей (по формуле мин. маржа 500 грн)?';

        if (!confirmAction(msg)) return;

        if (bulkConfirmBtn) bulkConfirmBtn.disabled = true;
        if (bulkRejectBtn) bulkRejectBtn.disabled = true;
        if (bulkRecalcDiscountBtn) bulkRecalcDiscountBtn.disabled = true;

        fetchWithCSRF('/matches/bulk-action', {
            method: 'POST',
            body: JSON.stringify({ action: action, ids: ids })
        })
            .then(function (resp) {
                return resp.json().then(function (data) {
                    data.__status = resp.status;
                    return data;
                });
            })
            .then(function (data) {
                if (data.status === 'ok') {
                    if (data.skipped_claimed && data.skipped_claimed.length > 0) {
                        showAlert(
                            'Применено: ' + data.processed +
                            '. Пропущено из-за занятого каталожного товара: ' +
                            data.skipped_claimed.length + '. Страница обновится.',
                            'warning'
                        );
                        setTimeout(function () { window.location.reload(); }, 2500);
                    } else {
                        window.location.reload();
                    }
                } else {
                    throw new Error(data.message || ('HTTP ' + (data.__status || '?')));
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

    if (bulkRecalcDiscountBtn) {
        bulkRecalcDiscountBtn.addEventListener('click', function () {
            doBulkAction('recalc_discount');
        });
    }

    function doClampMarginDryRun() {
        var ids = Array.from(selectedIds);
        if (ids.length === 0) return;
        bulkClampMarginBtn.disabled = true;
        var originalText = bulkClampMarginBtn.textContent;
        bulkClampMarginBtn.textContent = 'Расчёт…';

        fetchWithCSRF('/matches/bulk-action', {
            method: 'POST',
            body: JSON.stringify({ action: 'clamp_margin', ids: ids, dry_run: true })
        })
            .then(function (resp) { return resp.json(); })
            .then(function (data) {
                if (data.status !== 'ok') {
                    throw new Error(data.message || 'Ошибка dry-run');
                }
                showClampPreviewModal(data.preview || [], ids);
            })
            .catch(function (err) {
                showAlert('Ошибка: ' + err.message, 'danger');
            })
            .finally(function () {
                bulkClampMarginBtn.disabled = selectedIds.size === 0;
                bulkClampMarginBtn.textContent = originalText;
            });
    }

    function showClampPreviewModal(preview, allIds) {
        var modal = document.getElementById('clampPreviewModal');
        if (!modal) {
            modal = document.createElement('div');
            modal.id = 'clampPreviewModal';
            modal.className = 'modal fade';
            modal.tabIndex = -1;
            modal.innerHTML =
                '<div class="modal-dialog modal-xl modal-dialog-scrollable">' +
                '<div class="modal-content">' +
                '<div class="modal-header">' +
                '<h5 class="modal-title">Применение min-margin (предпросмотр)</h5>' +
                '<button type="button" class="btn-close" data-bs-dismiss="modal"></button>' +
                '</div>' +
                '<div class="modal-body" id="clampPreviewBody"></div>' +
                '<div class="modal-footer">' +
                '<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>' +
                '<button type="button" class="btn btn-warning" id="clampPreviewApplyBtn">Применить</button>' +
                '</div>' +
                '</div></div>';
            document.body.appendChild(modal);
        }
        var body = modal.querySelector('#clampPreviewBody');
        if (preview.length === 0) {
            body.innerHTML = '<p class="text-muted">Среди выбранных матчей нет кандидатов для клэмпа ' +
                '(все либо имеют ручной % скидки, либо не confirmed/manual, либо без цены).</p>';
        } else {
            var rows = preview.map(function (p) {
                var changed = Math.abs(p.base_discount - p.effective_discount) > 0.001;
                return '<tr' + (changed ? ' class="table-warning"' : '') + '>' +
                    '<td>' + p.match_id + '</td>' +
                    '<td>' + (p.supplier_product_name || '').replace(/</g, '&lt;') + '</td>' +
                    '<td class="text-end">' + p.base_discount.toFixed(1) + '%</td>' +
                    '<td class="text-end"><strong>' + p.effective_discount.toFixed(1) + '%</strong></td>' +
                    '<td class="text-end">' + p.margin_uah.toFixed(0) + '</td>' +
                    '<td>' + (p.clamp_applied ? '<span class="badge bg-warning text-dark">clamp</span>' : '') + '</td>' +
                    '</tr>';
            }).join('');
            var changedCount = preview.filter(function (p) {
                return Math.abs(p.base_discount - p.effective_discount) > 0.001;
            }).length;
            body.innerHTML =
                '<p>Будет зафиксировано в <strong>' + preview.length + '</strong> матчах ' +
                '(из них скидка изменится у <strong>' + changedCount + '</strong>). ' +
                'Матчи с заданным вручную % пропущены.</p>' +
                '<div class="table-responsive"><table class="table table-sm">' +
                '<thead><tr><th>#</th><th>Товар</th><th class="text-end">База %</th><th class="text-end">Итог %</th>' +
                '<th class="text-end">Маржа UAH</th><th>Пометка</th></tr></thead>' +
                '<tbody>' + rows + '</tbody></table></div>';
        }
        var applyBtn = modal.querySelector('#clampPreviewApplyBtn');
        applyBtn.disabled = preview.length === 0;
        applyBtn.onclick = function () {
            applyBtn.disabled = true;
            applyBtn.textContent = 'Применяется…';
            fetchWithCSRF('/matches/bulk-action', {
                method: 'POST',
                body: JSON.stringify({ action: 'clamp_margin', ids: allIds })
            })
                .then(function (resp) { return resp.json(); })
                .then(function (data) {
                    if (data.status !== 'ok') throw new Error(data.message || 'Ошибка');
                    window.location.reload();
                })
                .catch(function (err) {
                    showAlert('Ошибка: ' + err.message, 'danger');
                    applyBtn.disabled = false;
                    applyBtn.textContent = 'Применить';
                });
        };
        var bs = window.bootstrap && window.bootstrap.Modal
            ? window.bootstrap.Modal.getOrCreateInstance(modal)
            : null;
        if (bs) bs.show();
    }

    if (bulkClampMarginBtn) {
        bulkClampMarginBtn.addEventListener('click', doClampMarginDryRun);
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
            // Target only the name span to preserve the name_ru block below it
            var nameSpan = promCell.querySelector('.prom-name-text');
            if (nameSpan) nameSpan.innerHTML = result.bHtml;
            else promCell.innerHTML = result.bHtml;
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
            // Target only the name span to preserve the name_ru block below it
            var nameSpan = promCell.querySelector('.prom-name-text');
            if (nameSpan) nameSpan.textContent = row.getAttribute('data-prom-name') || '';
            else promCell.textContent = row.getAttribute('data-prom-name') || '';
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

    var currentSupplierAvailable = false;

    function openManualMatchModal(btn) {
        var supplierId = btn.getAttribute('data-supplier-id');
        var supplierName = btn.getAttribute('data-supplier-name');
        var supplierBrand = btn.getAttribute('data-supplier-brand');
        var supplierPrice = btn.getAttribute('data-supplier-price');
        var supplierCurrency = btn.getAttribute('data-supplier-currency') || 'EUR';
        currentSupplierAvailable = btn.getAttribute('data-supplier-available') === 'true';

        document.getElementById('selectedSupplierProductId').value = supplierId;
        document.getElementById('modalSupplierName').textContent = supplierName;
        document.getElementById('modalSupplierBrand').textContent = supplierBrand || '-';
        document.getElementById('modalSupplierPrice').textContent =
            supplierPrice ? (supplierPrice + ' ' + supplierCurrency) : '-';

        var availEl = document.getElementById('modalSupplierAvailability');
        if (availEl) {
            if (currentSupplierAvailable) {
                availEl.innerHTML = '<span class="badge bg-success">В наличии</span>';
            } else {
                availEl.innerHTML = '<span class="badge bg-secondary">Нет в наличии</span>';
            }
        }

        // Reset modal state
        document.getElementById('catalogSearchInput').value = '';
        document.getElementById('catalogResultsList').innerHTML = '';
        document.getElementById('catalogSearchPlaceholder').style.display = '';
        document.getElementById('selectedProductAlert').classList.add('d-none');
        document.getElementById('selectedPromProductId').value = '';
        var submitBtnEl = document.getElementById('submitManualMatch');
        submitBtnEl.disabled = true;
        submitBtnEl.textContent = 'Сопоставить';
        document.getElementById('rememberMatchCheck').checked = false;
        selectedPromProductId = null;

        // Clear any leftover feedback from a previous open
        var fbEl = document.getElementById('manualMatchFeedback');
        if (fbEl) {
            fbEl.className = 'alert d-none mb-0';
            fbEl.textContent = '';
        }

        if (manualMatchModal) manualMatchModal.show();
    }

    // Auto-open manual-match modal when /matches was loaded with
    // ?manual_for_sp=<id> — used by /products/supplier «Сопоставить» button
    // to target a specific SupplierProduct rather than rely on fuzzy name search.
    var autoTrigger = document.getElementById('autoManualMatch');
    if (autoTrigger && manualMatchModal) {
        // Defer so all other listeners/modal bindings are ready.
        setTimeout(function () { openManualMatchModal(autoTrigger); }, 50);
    }

    function showManualMatchFeedback(message, kind) {
        var el = document.getElementById('manualMatchFeedback');
        if (!el) return;
        el.textContent = message;
        el.className = 'alert mb-0 alert-' + (kind || 'info');
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
                    var notFoundHtml = '<div class="text-center p-3">' +
                        '<p class="text-muted mb-2">Товар не найден в каталоге Horoshop</p>';
                    if (currentSupplierAvailable) {
                        notFoundHtml += '<button type="button" class="btn btn-sm btn-outline-warning" id="markForCatalogBtn">' +
                            'Позначити для додавання в каталог</button>' +
                            '<p class="text-muted small mt-1">Товар в наличии у поставщика, но отсутствует в Horoshop</p>';
                    } else {
                        notFoundHtml += '<p class="text-muted small">Товар не в наличии у поставщика</p>';
                    }
                    notFoundHtml += '</div>';
                    list.innerHTML = notFoundHtml;
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

    // Mark supplier product for catalog addition
    document.addEventListener('click', function (e) {
        if (!e.target.matches('#markForCatalogBtn')) return;
        var spId = document.getElementById('selectedSupplierProductId').value;
        if (!spId) return;
        e.target.disabled = true;
        e.target.textContent = 'Збереження...';

        fetchWithCSRF('/matches/mark-new/' + spId, { method: 'POST' })
            .then(function (resp) {
                if (!resp.ok) {
                    return resp.json().then(function (d) { throw new Error(d.message || 'HTTP ' + resp.status); });
                }
                return resp.json();
            })
            .then(function (data) {
                showManualMatchFeedback('Товар позначено для додавання в каталог', 'success');
                e.target.textContent = 'Позначено';
                setTimeout(function () { window.location.reload(); }, 1500);
            })
            .catch(function (err) {
                e.target.disabled = false;
                e.target.textContent = 'Позначити для додавання в каталог';
                showManualMatchFeedback('Помилка: ' + err.message, 'danger');
            });
    });

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

            if (!supplierProductId || !promProductId) {
                showManualMatchFeedback('Сначала выберите товар каталога из списка', 'warning');
                return;
            }

            submitBtn.disabled = true;
            submitBtn.textContent = 'Сохранение...';
            showManualMatchFeedback('Отправка запроса...', 'info');

            fetchWithCSRF('/matches/manual', {
                method: 'POST',
                body: JSON.stringify({
                    supplier_product_id: parseInt(supplierProductId, 10),
                    prom_product_id: parseInt(promProductId, 10),
                    remember: remember
                })
            })
                .then(function (resp) {
                    if (resp.status === 409) {
                        return resp.json().then(function (data) {
                            showManualMatchFeedback(
                                (data.message || 'Товар уже сопоставлен') + ' Страница обновится...',
                                'warning'
                            );
                            submitBtn.textContent = 'Уже сопоставлено';
                            setTimeout(function () { window.location.reload(); }, 2000);
                            return { status: '__handled__' };
                        });
                    }
                    if (!resp.ok) {
                        return resp.json().then(function (data) {
                            throw new Error(data.message || 'HTTP ' + resp.status);
                        }).catch(function () {
                            throw new Error('HTTP ' + resp.status);
                        });
                    }
                    return resp.json();
                })
                .then(function (data) {
                    if (data.status === '__handled__') return;
                    if (data.status !== 'ok') {
                        throw new Error(data.message || 'Unknown error');
                    }
                    submitBtn.textContent = '✓ Сохранено';
                    showManualMatchFeedback(
                        '✓ Ручной матч создан' + (remember ? '. Правило сохранено.' : '') + '. Страница обновится...',
                        'success'
                    );
                    // Give the user enough time to read the success banner before
                    // we reload. Previously we reloaded 1s after hiding the modal,
                    // but the container-level alert was hidden behind the backdrop,
                    // so the user saw nothing. Now the banner lives inside the
                    // modal body and stays visible for the full delay.
                    setTimeout(function () {
                        window.location.reload();
                    }, 1500);
                })
                .catch(function (err) {
                    submitBtn.disabled = false;
                    submitBtn.textContent = 'Сопоставить';
                    showManualMatchFeedback('Ошибка: ' + err.message, 'danger');
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

    // ========== Rebind modal (Phase E) ==========

    var rebindModal = null;
    var rebindModalEl = document.getElementById('rebindModal');
    if (rebindModalEl) {
        rebindModal = new bootstrap.Modal(rebindModalEl);
    }
    var rebindSearchTimer = null;

    function openRebindModal(btn) {
        var matchId = btn.getAttribute('data-match-id');
        var oldSpName = btn.getAttribute('data-old-sp-name');
        var oldSupplier = btn.getAttribute('data-old-supplier');
        var ppName = btn.getAttribute('data-pp-name');
        var ppBrand = btn.getAttribute('data-pp-brand') || '';

        document.getElementById('rebindMatchId').value = matchId;
        document.getElementById('rebindPpBrand').value = ppBrand;
        document.getElementById('rebindNewSpId').value = '';
        document.getElementById('rebindPpName').textContent = ppName;
        document.getElementById('rebindOldSupplier').textContent = oldSupplier || '—';
        document.getElementById('rebindOldSpName').textContent = oldSpName;
        document.getElementById('rebindSearchInput').value = '';
        document.getElementById('rebindResultsList').innerHTML = '';
        document.getElementById('rebindSearchPlaceholder').style.display = '';
        document.getElementById('rebindSelectedAlert').classList.add('d-none');
        document.getElementById('rebindDiff').innerHTML = '';
        var fb = document.getElementById('rebindFeedback');
        fb.className = 'alert d-none mb-0';
        fb.textContent = '';
        var submit = document.getElementById('submitRebind');
        submit.disabled = true;
        submit.textContent = 'Переподвязать';

        if (rebindModal) rebindModal.show();
    }

    document.addEventListener('click', function (e) {
        var btn = e.target.closest('.rebind-btn');
        if (!btn) return;
        openRebindModal(btn);
    });

    function showRebindFeedback(msg, kind) {
        var el = document.getElementById('rebindFeedback');
        if (!el) return;
        el.textContent = msg;
        el.className = 'alert mb-0 alert-' + (kind || 'info');
    }

    function renderRebindResults(items) {
        var list = document.getElementById('rebindResultsList');
        var placeholder = document.getElementById('rebindSearchPlaceholder');
        var currentMatchId = parseInt(document.getElementById('rebindMatchId').value, 10);
        var targetPpBrand = (document.getElementById('rebindPpBrand').value || '').toLowerCase();

        if (!items.length) {
            placeholder.style.display = '';
            placeholder.textContent = 'Ничего не найдено';
            list.innerHTML = '';
            return;
        }
        placeholder.style.display = 'none';

        var html = '';
        items.forEach(function (sp) {
            var brandMatch = sp.brand && targetPpBrand && sp.brand.toLowerCase() === targetPpBrand;
            var brandBadge = sp.brand
                ? '<span class="badge ' + (brandMatch ? 'bg-success' : 'bg-warning text-dark') + ' me-1">' + escapeHtml(sp.brand) + '</span>'
                : '';
            var claimLabel = '';
            if (sp.active_match_id && sp.active_match_id !== currentMatchId) {
                claimLabel = '<span class="badge bg-danger ms-1" title="Этот товар уже подтверждён на другой каталог — сначала отмените тот матч">уже матч #' + sp.active_match_id + '</span>';
            }
            var availBadge = sp.available
                ? '<span class="badge bg-success-subtle text-success">В наличии</span>'
                : '<span class="badge bg-secondary-subtle text-muted">Нет</span>';

            html += '<a href="#" class="list-group-item list-group-item-action rebind-result-item" ' +
                'data-sp-id="' + sp.id + '" ' +
                'data-sp-name="' + escapeHtml(sp.name) + '" ' +
                'data-sp-brand="' + escapeHtml(sp.brand) + '" ' +
                'data-sp-supplier="' + escapeHtml(sp.supplier_name) + '" ' +
                'data-sp-claimed="' + (sp.active_match_id && sp.active_match_id !== currentMatchId ? '1' : '0') + '">' +
                '<div class="d-flex justify-content-between align-items-start">' +
                '  <div class="me-2" style="min-width:0">' +
                '    <div class="text-truncate"><strong>' + escapeHtml(sp.name) + '</strong></div>' +
                '    <small class="text-muted">' + brandBadge +
                     escapeHtml(sp.supplier_name) +
                     (sp.article ? ' · арт. ' + escapeHtml(sp.article) : '') +
                     claimLabel +
                '    </small>' +
                '  </div>' +
                '  <div class="text-end small flex-shrink-0">' +
                '    <div>' + (sp.price_eur ? escapeHtml(sp.price_eur) + ' EUR' : '—') + '</div>' +
                '    <div>' + availBadge + '</div>' +
                '  </div>' +
                '</div>' +
                '</a>';
        });
        list.innerHTML = html;
    }

    var rebindSearchInput = document.getElementById('rebindSearchInput');
    if (rebindSearchInput) {
        rebindSearchInput.addEventListener('input', function () {
            var q = this.value.trim();
            if (rebindSearchTimer) clearTimeout(rebindSearchTimer);
            if (q.length < 2) {
                document.getElementById('rebindResultsList').innerHTML = '';
                var ph = document.getElementById('rebindSearchPlaceholder');
                ph.style.display = '';
                ph.textContent = 'Введите запрос для поиска товаров поставщиков';
                return;
            }
            rebindSearchTimer = setTimeout(function () {
                fetch('/matches/search-suppliers?q=' + encodeURIComponent(q))
                    .then(function (r) {
                        if (!r.ok) throw new Error('HTTP ' + r.status);
                        return r.json();
                    })
                    .then(renderRebindResults)
                    .catch(function (err) {
                        document.getElementById('rebindResultsList').innerHTML =
                            '<p class="text-danger text-center p-2">Ошибка поиска: ' + err.message + '</p>';
                    });
            }, 300);
        });
    }

    document.addEventListener('click', function (e) {
        var item = e.target.closest('.rebind-result-item');
        if (!item) return;
        e.preventDefault();

        if (item.getAttribute('data-sp-claimed') === '1') {
            showRebindFeedback(
                'Этот товар уже подтверждён на другой каталог. Сначала отмените тот матч в списке.',
                'warning'
            );
            return;
        }

        var spId = item.getAttribute('data-sp-id');
        var spName = item.getAttribute('data-sp-name');
        var spBrand = item.getAttribute('data-sp-brand');
        var spSupplier = item.getAttribute('data-sp-supplier');
        var targetBrand = document.getElementById('rebindPpBrand').value || '';

        document.getElementById('rebindNewSpId').value = spId;
        document.getElementById('rebindSelectedName').textContent = spName + ' (' + spSupplier + ')';

        var diffHtml = '';
        if (spBrand && targetBrand) {
            var same = spBrand.toLowerCase() === targetBrand.toLowerCase();
            diffHtml = 'Бренд поставщика: <strong>' + escapeHtml(spBrand) + '</strong> ' +
                (same
                    ? '<span class="badge bg-success">совпадает с каталогом</span>'
                    : '<span class="badge bg-warning text-dark">отличается от каталога (' + escapeHtml(targetBrand) + ')</span>');
        } else if (spBrand) {
            diffHtml = 'Бренд поставщика: <strong>' + escapeHtml(spBrand) + '</strong>';
        } else {
            diffHtml = '<span class="text-muted">Бренд поставщика не указан</span>';
        }
        document.getElementById('rebindDiff').innerHTML = diffHtml;
        document.getElementById('rebindSelectedAlert').classList.remove('d-none');
        document.getElementById('submitRebind').disabled = false;

        var list = document.getElementById('rebindResultsList');
        list.querySelectorAll('.list-group-item').forEach(function (li) { li.classList.remove('active'); });
        item.classList.add('active');
    });

    var rebindClearBtn = document.getElementById('rebindClearSelected');
    if (rebindClearBtn) {
        rebindClearBtn.addEventListener('click', function () {
            document.getElementById('rebindNewSpId').value = '';
            document.getElementById('rebindSelectedAlert').classList.add('d-none');
            document.getElementById('submitRebind').disabled = true;
            var list = document.getElementById('rebindResultsList');
            if (list) {
                list.querySelectorAll('.list-group-item').forEach(function (li) { li.classList.remove('active'); });
            }
        });
    }

    var submitRebindBtn = document.getElementById('submitRebind');
    if (submitRebindBtn) {
        submitRebindBtn.addEventListener('click', function () {
            var matchId = document.getElementById('rebindMatchId').value;
            var newSpId = document.getElementById('rebindNewSpId').value;
            if (!matchId || !newSpId) {
                showRebindFeedback('Выберите нового поставщика из списка', 'warning');
                return;
            }
            submitRebindBtn.disabled = true;
            submitRebindBtn.textContent = 'Сохранение...';
            showRebindFeedback('Отправка запроса...', 'info');

            fetchWithCSRF('/matches/' + matchId + '/rebind', {
                method: 'POST',
                body: JSON.stringify({ new_supplier_product_id: parseInt(newSpId, 10) })
            })
                .then(function (resp) {
                    return resp.json().then(function (data) {
                        return { ok: resp.ok, status: resp.status, data: data };
                    });
                })
                .then(function (r) {
                    if (!r.ok) {
                        submitRebindBtn.disabled = false;
                        submitRebindBtn.textContent = 'Переподвязать';
                        showRebindFeedback(r.data.message || ('HTTP ' + r.status), 'danger');
                        return;
                    }
                    submitRebindBtn.textContent = '✓ Сохранено';
                    showRebindFeedback(
                        '✓ Переподвязано. Старый матч #' + r.data.old_match_id +
                        ' → новый матч #' + r.data.new_match_id + '. Страница обновится...',
                        'success'
                    );
                    setTimeout(function () { window.location.reload(); }, 1500);
                })
                .catch(function (err) {
                    submitRebindBtn.disabled = false;
                    submitRebindBtn.textContent = 'Переподвязать';
                    showRebindFeedback('Ошибка: ' + err.message, 'danger');
                });
        });
    }

    // Save on filter/pagination changes
    if (filterForm) {
        filterForm.addEventListener('change', scheduleSave);
    }
    window.addEventListener('scroll', scheduleSave);
    window.addEventListener('beforeunload', saveState);

    // Restore on page load
    restoreState();

    // ========== Alternative suppliers (cross-supplier overlap expand) ==========

    function escapeHtml(s) {
        return String(s == null ? '' : s)
            .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
    }

    function renderAlternatives(alts, currentMatchId, currentStatus) {
        if (!alts.length) {
            return '<div class="p-2 text-muted small">Других поставщиков нет.</div>';
        }
        var swapsToRebind = currentStatus === 'confirmed' || currentStatus === 'manual';
        var swapLabel = swapsToRebind ? 'Переподвязать сюда' : 'Подтвердить вместо текущего';
        var swapAction = swapsToRebind ? 'rebind' : 'confirm';
        var rows = alts.map(function (a) {
            var availBadge = a.sp_available
                ? '<span class="badge bg-success">в наличии</span>'
                : '<span class="badge bg-secondary">нет</span>';
            var price = a.sp_price_eur != null
                ? a.sp_price_eur.toFixed(2) + ' ' + escapeHtml(a.sp_currency)
                : '&mdash;';
            var statusBadgeClass = a.status === 'confirmed' ? 'bg-success'
                : a.status === 'manual' ? 'bg-info' : 'bg-secondary';
            return '<tr>' +
                '<td><span class="badge bg-dark">' + escapeHtml(a.supplier_name) + '</span></td>' +
                '<td>' + escapeHtml(a.sp_name) + '</td>' +
                '<td>' + price + '</td>' +
                '<td>' + availBadge + '</td>' +
                '<td><small>' + a.score.toFixed(0) + '%</small></td>' +
                '<td><span class="badge ' + statusBadgeClass + '">' + escapeHtml(a.status) + '</span></td>' +
                '<td class="text-end">' +
                    '<button class="btn btn-sm btn-outline-info details-btn" data-id="' + a.match_id + '">Детали</button> ' +
                    '<button class="btn btn-sm btn-outline-primary alt-swap-btn" ' +
                           'data-current-match-id="' + currentMatchId + '" ' +
                           'data-alt-match-id="' + a.match_id + '" ' +
                           'data-alt-sp-id="' + a.sp_id + '" ' +
                           'data-action="' + swapAction + '">' + swapLabel + '</button> ' +
                    '<button class="btn btn-sm btn-outline-danger reject-btn" data-id="' + a.match_id + '">Отклонить</button>' +
                '</td>' +
            '</tr>';
        }).join('');
        return '<div style="background-color:#fff8e1;padding:8px 16px;border-left:4px solid #ffc107;">' +
            '<table class="table table-sm mb-0"><thead><tr>' +
                '<th>Поставщик</th><th>Название у поставщика</th><th>Цена</th><th>Наличие</th>' +
                '<th>Конф.</th><th>Статус</th><th class="text-end">Действия</th>' +
            '</tr></thead><tbody>' + rows + '</tbody></table></div>';
    }

    if (matchTable) {
        matchTable.addEventListener('click', function (e) {
            var btn = e.target.closest('.alt-badge');
            if (!btn) return;
            e.preventDefault();
            var matchId = btn.dataset.matchId;
            var parentRow = btn.closest('tr');
            var existing = parentRow.nextElementSibling;
            if (existing && existing.classList.contains('alternatives-row') &&
                existing.dataset.parentMatchId === matchId) {
                existing.remove();
                btn.classList.remove('active');
                return;
            }
            // Only one expanded sub-row at a time.
            document.querySelectorAll('.alternatives-row').forEach(function (r) { r.remove(); });
            document.querySelectorAll('.alt-badge.active').forEach(function (b) { b.classList.remove('active'); });

            fetch('/matches/' + matchId + '/alternatives', { credentials: 'same-origin' })
                .then(function (r) { return r.json(); })
                .then(function (data) {
                    if (data.status !== 'ok') return;
                    var subRow = document.createElement('tr');
                    subRow.className = 'alternatives-row';
                    subRow.dataset.parentMatchId = matchId;
                    var td = document.createElement('td');
                    td.colSpan = 16;
                    td.className = 'p-0';
                    td.innerHTML = renderAlternatives(
                        data.alternatives, data.current_match_id, data.current_match_status
                    );
                    subRow.appendChild(td);
                    parentRow.parentNode.insertBefore(subRow, parentRow.nextSibling);
                    btn.classList.add('active');
                });
        });

        // Swap action: rebind (when current is confirmed/manual) or confirm
        // (when current is candidate — backend rejects current via 1pp↔1SP
        // invariant if needed; we explicitly reject the current candidate
        // first to keep it clean).
        matchTable.addEventListener('click', function (e) {
            var btn = e.target.closest('.alt-swap-btn');
            if (!btn) return;
            e.preventDefault();
            var currentId = btn.dataset.currentMatchId;
            var altId = btn.dataset.altMatchId;
            var altSpId = btn.dataset.altSpId;
            var action = btn.dataset.action;
            btn.disabled = true;
            btn.textContent = 'Применяю…';

            var promise;
            if (action === 'rebind') {
                promise = fetch('/matches/' + currentId + '/rebind', {
                    method: 'POST',
                    credentials: 'same-origin',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ new_supplier_product_id: parseInt(altSpId, 10) }),
                });
            } else {
                // candidate-current: reject current, then confirm alt.
                promise = fetch('/matches/' + currentId + '/reject', {
                    method: 'POST', credentials: 'same-origin',
                }).then(function () {
                    return fetch('/matches/' + altId + '/confirm', {
                        method: 'POST', credentials: 'same-origin',
                    });
                });
            }
            promise.then(function (r) { return r.json ? r.json() : r; })
                .then(function (data) {
                    if (data && data.status === 'error') {
                        alert(data.message || 'Не удалось переключить поставщика');
                        btn.disabled = false;
                        btn.textContent = action === 'rebind' ? 'Переподвязать сюда' : 'Подтвердить вместо текущего';
                        return;
                    }
                    window.location.reload();
                })
                .catch(function (err) {
                    alert('Ошибка: ' + err.message);
                    btn.disabled = false;
                });
        });
    }

})();
