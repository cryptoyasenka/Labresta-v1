/* LabResta Sync — Notifications JS */

document.addEventListener('DOMContentLoaded', function () {
    // Criteria type hint updater
    const typeSelect = document.getElementById('criteriaTypeSelect');
    const valueInput = document.getElementById('criteriaValueInput');
    const hintText = document.getElementById('criteriaHint');

    if (typeSelect) {
        const hints = {
            keyword: { placeholder: 'espresso, latte, кофе', hint: 'Через запятую для нескольких слов' },
            brand: { placeholder: 'De\'Longhi', hint: 'Название бренда (частичное совпадение)' },
            price_range: { placeholder: '100000-500000', hint: 'Мин-макс в копейках (напр. 100000 = 1000.00)' },
            category: { placeholder: 'кофемашины', hint: 'Ключевое слово в названии (категории пока нет)' },
        };

        typeSelect.addEventListener('change', function () {
            const h = hints[this.value] || hints.keyword;
            if (valueInput) valueInput.placeholder = h.placeholder;
            if (hintText) hintText.textContent = h.hint;
        });
    }

    // Mark all unread notifications as read
    const markAllBtn = document.getElementById('markAllReadBtn');
    const notifList = document.getElementById('notificationsList');

    if (notifList) {
        const unread = notifList.querySelectorAll('.list-group-item-light');
        if (unread.length > 0 && markAllBtn) {
            markAllBtn.style.display = '';

            markAllBtn.addEventListener('click', function () {
                const ids = [];
                unread.forEach(function (el) {
                    const id = el.getAttribute('data-notification-id');
                    if (id) ids.push(parseInt(id, 10));
                });

                if (ids.length === 0) return;

                fetchWithCSRF('/settings/api/notifications/mark-read', {
                    method: 'POST',
                    body: JSON.stringify({ ids: ids }),
                })
                    .then(function (resp) { return resp.json(); })
                    .then(function (data) {
                        if (data.marked > 0) {
                            unread.forEach(function (el) {
                                el.classList.remove('list-group-item-light');
                                var badge = el.querySelector('.badge.bg-primary');
                                if (badge) badge.remove();
                            });
                            markAllBtn.style.display = 'none';
                            updateNavbarBadge();
                        }
                    })
                    .catch(function (err) {
                        console.error('Failed to mark notifications read:', err);
                    });
            });
        }
    }

    // Navbar notification badge polling (every 30 seconds)
    updateNavbarBadge();
    setInterval(updateNavbarBadge, 30000);
});

function updateNavbarBadge() {
    var badge = document.getElementById('notificationBadge');
    if (!badge) return;

    fetch('/settings/api/notifications/unread')
        .then(function (resp) { return resp.json(); })
        .then(function (data) {
            var count = data.length || 0;
            if (count > 0) {
                badge.textContent = count;
                badge.style.display = '';
            } else {
                badge.style.display = 'none';
            }
        })
        .catch(function () {
            // Silently fail — badge just won't update
        });
}
