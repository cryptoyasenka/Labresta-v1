"""HTTP feed fetcher — returns raw bytes to preserve encoding."""

import ipaddress
import logging
import socket
from urllib.parse import urljoin, urlparse

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


_MAX_REDIRECTS = 5


def _assert_public_url(url: str) -> None:
    """Reject feed URLs that aren't plain HTTP(S) to a public host (SSRF guard).

    Defence-in-depth: supplier feed URLs are operator-entered, so this stops a
    mistyped or hostile URL from reaching internal services — cloud metadata
    (169.254.169.254), localhost, or RFC-1918 ranges — or a non-HTTP scheme
    such as file://. Every address the host resolves to must be public.

    Raises:
        ValueError: scheme not http/https, host missing/unresolvable, or any
            resolved IP is private/loopback/link-local/reserved/multicast.
    """
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(
            f"Feed URL scheme not allowed: {parsed.scheme!r} (http/https only)"
        )
    host = parsed.hostname
    if not host:
        raise ValueError(f"Feed URL has no host: {url!r}")
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    try:
        infos = socket.getaddrinfo(host, port, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Cannot resolve feed URL host {host!r}: {exc}") from exc
    for info in infos:
        ip = ipaddress.ip_address(info[4][0])
        if (ip.is_private or ip.is_loopback or ip.is_link_local
                or ip.is_reserved or ip.is_multicast or ip.is_unspecified):
            raise ValueError(
                f"Feed URL host {host!r} resolves to non-public IP {ip} — refusing fetch"
            )


def fetch_feed(url: str, timeout: int = 30) -> bytes:
    """Fetch a supplier feed URL and return raw bytes.

    CRITICAL: Always returns response.content (bytes), never .text (str).
    This prevents encoding corruption — the XML parser handles encoding
    detection from the raw byte stream and XML declaration.

    Redirects are followed manually (max _MAX_REDIRECTS) so every hop — not
    just the initial URL — passes _assert_public_url. Legitimate http->https
    redirects keep working; a redirect into an internal address is blocked.

    Args:
        url: Feed URL to fetch.
        timeout: Request timeout in seconds (default 30).

    Returns:
        Raw bytes of the HTTP response body.

    Raises:
        ValueError: URL (or a redirect hop) is non-HTTP(S) or resolves to a
            non-public IP.
        requests.HTTPError: On non-2xx status codes.
        requests.RequestException: On connection/timeout errors.
    """
    session = requests.Session()
    current = url
    for _ in range(_MAX_REDIRECTS + 1):
        _assert_public_url(current)
        parsed = urlparse(current)
        origin = f"{parsed.scheme}://{parsed.netloc}"
        response = session.get(
            current,
            timeout=timeout,
            allow_redirects=False,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                ),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "uk-UA,uk;q=0.9,en;q=0.8",
                "Accept-Encoding": "gzip, deflate",
                "Referer": origin + "/",
                "Connection": "keep-alive",
            },
        )
        if response.is_redirect:
            location = response.headers.get("Location")
            if not location:
                break
            current = urljoin(current, location)
            continue
        response.raise_for_status()
        return response.content
    raise requests.TooManyRedirects(
        f"Exceeded {_MAX_REDIRECTS} redirects fetching {url!r}"
    )


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
