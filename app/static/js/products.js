/* LabResta Sync — Product management AJAX handlers */

/**
 * Mark a supplier product as unavailable (out of stock).
 * @param {number} productId - Product ID
 */
async function markUnavailable(productId) {
    try {
        const resp = await fetchWithCSRF(`/products/supplier/${productId}/mark-unavailable`, {
            method: 'POST',
        });
        const data = await resp.json();
        if (resp.ok && data.status === 'ok') {
            // Update row in-place
            const row = document.getElementById(`product-row-${productId}`);
            if (row) {
                // Update availability badge
                const badges = row.querySelectorAll('td');
                // Find the availability cell (index 6 in the table)
                const availCell = badges[6];
                if (availCell) {
                    availCell.innerHTML = '<span class="badge bg-danger">Нет в наличии</span>';
                }
                // Swap the button to "В наличии"
                const actionsCell = badges[9];
                if (actionsCell) {
                    const btn = actionsCell.querySelector('.btn-outline-warning');
                    if (btn) {
                        btn.className = 'btn btn-outline-success btn-sm';
                        btn.textContent = 'В наличии';
                        btn.setAttribute('onclick', `markAvailable(${productId})`);
                        btn.setAttribute('title', 'Отметить как в наличии');
                    }
                }
            }
        } else {
            alert(data.message || 'Ошибка при обновлении');
        }
    } catch (err) {
        alert('Ошибка сети: ' + err.message);
    }
}

/**
 * Mark a supplier product as available (back in stock).
 * @param {number} productId - Product ID
 */
async function markAvailable(productId) {
    try {
        const resp = await fetchWithCSRF(`/products/supplier/${productId}/mark-available`, {
            method: 'POST',
        });
        const data = await resp.json();
        if (resp.ok && data.status === 'ok') {
            const row = document.getElementById(`product-row-${productId}`);
            if (row) {
                const badges = row.querySelectorAll('td');
                const availCell = badges[6];
                if (availCell) {
                    availCell.innerHTML = '<span class="badge bg-success">В наличии</span>';
                }
                const actionsCell = badges[9];
                if (actionsCell) {
                    const btn = actionsCell.querySelector('.btn-outline-success');
                    if (btn) {
                        btn.className = 'btn btn-outline-warning btn-sm';
                        btn.textContent = 'Нет в наличии';
                        btn.setAttribute('onclick', `markUnavailable(${productId})`);
                        btn.setAttribute('title', 'Отметить как отсутствующий');
                    }
                }
            }
        } else {
            alert(data.message || 'Ошибка при обновлении');
        }
    } catch (err) {
        alert('Ошибка сети: ' + err.message);
    }
}

/**
 * Show the force-price modal for a product.
 * @param {number} productId - Product ID
 * @param {number} currentPriceCents - Current price in cents
 */
function showForcePrice(productId, currentPriceCents, currency) {
    currency = currency || 'UAH';
    document.getElementById('forcePriceProductId').value = productId;
    document.getElementById('forcePriceCurrency').value = currency;
    document.getElementById('forcePriceCurrencyLabel').textContent = 'Цена (' + currency + ')';
    document.getElementById('forcePriceValue').value = currentPriceCents > 0
        ? (currentPriceCents / 100).toFixed(2)
        : '';
    const modal = new bootstrap.Modal(document.getElementById('forcePriceModal'));
    modal.show();
}

/**
 * Submit the forced price from the modal.
 */
async function submitForcePrice() {
    const productId = document.getElementById('forcePriceProductId').value;
    const currency = document.getElementById('forcePriceCurrency').value || 'UAH';
    const priceValue = parseFloat(document.getElementById('forcePriceValue').value);

    if (isNaN(priceValue) || priceValue < 0) {
        alert('Введите корректную цену');
        return;
    }

    const priceCents = Math.round(priceValue * 100);

    try {
        const resp = await fetchWithCSRF(`/products/supplier/${productId}/force-price`, {
            method: 'POST',
            body: JSON.stringify({ price_cents: priceCents, currency: currency }),
        });
        const data = await resp.json();
        if (resp.ok && data.status === 'ok') {
            // Close modal
            const modalEl = document.getElementById('forcePriceModal');
            const modal = bootstrap.Modal.getInstance(modalEl);
            if (modal) modal.hide();

            // Update price in the row
            const row = document.getElementById(`product-row-${productId}`);
            if (row) {
                const cells = row.querySelectorAll('td');
                const priceCell = cells[5];
                if (priceCell) {
                    priceCell.innerHTML = `${priceValue.toFixed(2)} ${currency} <span class="badge bg-info">Принудительная</span>`;
                }
            }
        } else {
            alert(data.message || 'Ошибка при установке цены');
        }
    } catch (err) {
        alert('Ошибка сети: ' + err.message);
    }
}

/**
 * Soft-delete a supplier product with confirmation.
 * @param {number} productId - Product ID
 */
async function ignoreProduct(productId) {
    if (!confirm('Исключить товар из матчинга? Он пропадёт из /matches и из этого списка. Вернуть можно, включив «Показать исключённые».')) {
        return;
    }
    try {
        const resp = await fetchWithCSRF(`/products/supplier/${productId}/ignore`, {
            method: 'POST',
        });
        const data = await resp.json();
        if (resp.ok && data.status === 'ok') {
            location.reload();
        } else {
            alert(data.message || 'Ошибка');
        }
    } catch (err) {
        alert('Ошибка сети: ' + err.message);
    }
}

async function unignoreProduct(productId) {
    try {
        const resp = await fetchWithCSRF(`/products/supplier/${productId}/unignore`, {
            method: 'POST',
        });
        const data = await resp.json();
        if (resp.ok && data.status === 'ok') {
            location.reload();
        } else {
            alert(data.message || 'Ошибка');
        }
    } catch (err) {
        alert('Ошибка сети: ' + err.message);
    }
}

async function deleteProduct(productId) {
    if (!confirm('Удалить товар? Это действие можно отменить.')) {
        return;
    }

    try {
        const resp = await fetchWithCSRF(`/products/supplier/${productId}/delete`, {
            method: 'POST',
        });
        const data = await resp.json();
        if (resp.ok && data.status === 'ok') {
            const row = document.getElementById(`product-row-${productId}`);
            if (row) {
                row.classList.add('table-secondary');
                // Remove action buttons
                const cells = row.querySelectorAll('td');
                const actionsCell = cells[9];
                if (actionsCell) {
                    actionsCell.innerHTML = '<span class="badge bg-secondary">Удален</span>';
                }
                // Update status cell
                const statusCell = cells[7];
                if (statusCell) {
                    statusCell.innerHTML += ' <span class="badge bg-secondary">Удален</span>';
                }
                // Update availability
                const availCell = cells[6];
                if (availCell) {
                    availCell.innerHTML = '<span class="badge bg-danger">Нет в наличии</span>';
                }
            }
        } else {
            alert(data.message || 'Ошибка при удалении');
        }
    } catch (err) {
        alert('Ошибка сети: ' + err.message);
    }
}
