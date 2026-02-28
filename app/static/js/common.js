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
