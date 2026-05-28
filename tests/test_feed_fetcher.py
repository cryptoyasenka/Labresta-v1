"""INFO-1: feed_fetcher must refuse non-HTTP(S) URLs and URLs that resolve to
internal/private IPs (SSRF defence-in-depth). Operator-entered feed URLs are
the input, so a mistyped/hostile URL must not reach localhost, RFC-1918
ranges, or the cloud metadata endpoint.

Numeric-IP and scheme cases are used so the tests never depend on DNS/network.
"""

import pytest

import app.services.feed_fetcher as ff
from app.services.feed_fetcher import _assert_public_url


class TestAssertPublicUrl:
    def test_allows_public_ip(self):
        # Public IP literals — getaddrinfo on a literal does not hit the network.
        _assert_public_url("http://8.8.8.8/feed.xml")
        _assert_public_url("https://1.1.1.1/feed.xml")

    @pytest.mark.parametrize("url", [
        "http://127.0.0.1/x",                          # loopback
        "http://169.254.169.254/latest/meta-data/",    # cloud metadata (link-local)
        "http://10.0.0.5/x",                           # RFC-1918
        "http://192.168.1.10/x",                       # RFC-1918
        "http://172.16.0.1/x",                         # RFC-1918
        "http://[::1]/x",                              # IPv6 loopback
        "http://0.0.0.0/x",                            # unspecified
    ])
    def test_blocks_internal_ip(self, url):
        with pytest.raises(ValueError):
            _assert_public_url(url)

    @pytest.mark.parametrize("url", [
        "file:///etc/passwd",
        "ftp://1.2.3.4/x",
        "gopher://1.2.3.4/x",
    ])
    def test_blocks_non_http_scheme(self, url):
        with pytest.raises(ValueError):
            _assert_public_url(url)

    def test_blocks_missing_host(self):
        with pytest.raises(ValueError):
            _assert_public_url("http:///nohost")


def test_fetch_feed_refuses_internal_before_any_request(monkeypatch):
    """The guard must fire before a socket is opened — no request to the
    internal address may happen at all."""
    def _boom(*a, **k):
        raise AssertionError("network call must not happen for an internal URL")

    monkeypatch.setattr(ff.requests.Session, "get", _boom)
    with pytest.raises(ValueError):
        ff.fetch_feed("http://127.0.0.1:8080/x")
