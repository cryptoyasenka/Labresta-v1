/* LabResta Sync — common JS helpers */

/**
 * Get CSRF token from meta tag.
 * @returns {string} CSRF token value
 */
function getCSRFToken() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? meta.getAttribute('content') : '';
}

/**
 * Consistent confirmation dialog.
 * @param {string} message - Confirmation message
 * @returns {boolean} User confirmed
 */
function confirmAction(message) {
    return window.confirm(message);
}

/**
 * Fetch wrapper that auto-adds CSRF token and JSON content type.
 * @param {string} url - Request URL
 * @param {Object} options - Fetch options (method, body, etc.)
 * @returns {Promise<Response>}
 */
function fetchWithCSRF(url, options = {}) {
    const defaults = {
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
    };

    const merged = {
        ...defaults,
        ...options,
        headers: {
            ...defaults.headers,
            ...(options.headers || {}),
        },
    };

    return fetch(url, merged);
}

/**
 * Parse fetch Response as JSON, but synthesize a readable message when the
 * server returned HTML (session expired, 500 page, etc.) so callers don't
 * crash with "Unexpected token '<'".
 * @param {Response} resp
 * @returns {Promise<Object>} parsed body with injected __status
 */
function parseJsonOrFriendly(resp) {
    const ctype = (resp.headers.get('content-type') || '').toLowerCase();
    if (ctype.indexOf('application/json') !== -1) {
        return resp.json().then(function (data) {
            data.__status = resp.status;
            return data;
        });
    }
    // Non-JSON response (HTML error page, redirect to /login, etc.).
    return resp.text().then(function () {
        let message;
        if (resp.status === 0 || resp.status >= 502) {
            message = 'Сервер недоступен. Проверьте, что Flask работает.';
        } else if (resp.status === 401 || resp.status === 403) {
            message = 'Сессия истекла. Обновите страницу и войдите снова.';
        } else if (resp.status === 400) {
            message = 'Запрос отклонён (возможно, устарел CSRF-токен). Обновите страницу.';
        } else if (resp.status === 404) {
            message = 'Объект не найден. Обновите страницу — список мог измениться.';
        } else {
            message = 'Неожиданный ответ сервера (HTTP ' + resp.status + '). Посмотрите логи.';
        }
        return { status: 'error', message: message, __status: resp.status };
    });
}
