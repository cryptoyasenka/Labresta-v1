"""HTTP feed fetcher — returns raw bytes to preserve encoding."""

import requests


def fetch_feed(url: str, timeout: int = 30) -> bytes:
    """Fetch a supplier feed URL and return raw bytes.

    CRITICAL: Always returns response.content (bytes), never .text (str).
    This prevents encoding corruption — the XML parser handles encoding
    detection from the raw byte stream and XML declaration.

    Args:
        url: Feed URL to fetch.
        timeout: Request timeout in seconds (default 30).

    Returns:
        Raw bytes of the HTTP response body.

    Raises:
        requests.HTTPError: On non-2xx status codes.
        requests.RequestException: On connection/timeout errors.
    """
    response = requests.get(
        url,
        timeout=timeout,
        headers={"User-Agent": "LabResta-Sync/1.0"},
    )
    response.raise_for_status()
    return response.content
