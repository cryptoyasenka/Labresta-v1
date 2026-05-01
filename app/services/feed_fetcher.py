"""HTTP feed fetcher — returns raw bytes to preserve encoding."""

import logging
from urllib.parse import urlparse

import requests
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

logger = logging.getLogger(__name__)


def _is_retryable(exc: BaseException) -> bool:
    """Retry only on transient errors — never on 4xx (rate limit, auth, not-found)."""
    if isinstance(exc, requests.HTTPError):
        return exc.response is not None and exc.response.status_code >= 500
    return isinstance(exc, (requests.ConnectionError, requests.Timeout))


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
    parsed = urlparse(url)
    origin = f"{parsed.scheme}://{parsed.netloc}"
    response = requests.get(
        url,
        timeout=timeout,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "uk-UA,uk;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": origin + "/",
            "Connection": "keep-alive",
        },
    )
    response.raise_for_status()
    return response.content


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=2, min=4, max=30),
    retry=retry_if_exception(_is_retryable),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    reraise=True,
)
def fetch_feed_with_retry(url: str, timeout: int = 30) -> bytes:
    """Fetch a supplier feed with automatic retry on transient HTTP errors.

    Retries up to 3 attempts (1 initial + 2 retries) with exponential backoff
    (4s, 8s). Only retries on transient errors (connection, timeout, HTTP status);
    XML parse errors or other exceptions are NOT retried.

    Args:
        url: Feed URL to fetch.
        timeout: Request timeout in seconds (default 30).

    Returns:
        Raw bytes of the HTTP response body.

    Raises:
        requests.ConnectionError: After 3 failed connection attempts.
        requests.Timeout: After 3 timeouts.
        requests.HTTPError: After 3 non-2xx responses.
    """
    return fetch_feed(url, timeout)
