"""HTTP feed fetcher — returns raw bytes to preserve encoding."""

import logging

import requests
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

logger = logging.getLogger(__name__)


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


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=2, min=4, max=30),
    retry=retry_if_exception_type(
        (requests.ConnectionError, requests.Timeout, requests.HTTPError)
    ),
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
