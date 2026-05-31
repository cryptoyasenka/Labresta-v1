"""Tests for app.services.category_resolver — the CORE fallback-only tier.

Plan 09-02 appends tests here for the smart tiers (feed / analogy / AI). For
the CORE we only assert: the FallbackResolver always hands back the holding
category, and the build_resolver factory (fallback-only) resolves every product
to a non-empty Раздел. Pure: SPs are tiny duck-typed stand-ins.
"""

from app.services.category_resolver import (
    DEFAULT_FALLBACK_CATEGORY,
    CategoryResult,
    ChainResolver,
    FallbackResolver,
    build_resolver,
)


class _SP:
    def __init__(self, brand="HURAKAN", name="НП товар"):
        self.brand = brand
        self.name = name


def test_fallback_resolver_returns_holding_category():
    r = FallbackResolver()
    res = r.resolve(_SP(), brand="HURAKAN")
    assert isinstance(res, CategoryResult)
    assert res.category == DEFAULT_FALLBACK_CATEGORY
    assert res.source == "fallback"
    assert res.confidence == 0.0


def test_fallback_resolver_custom_category():
    r = FallbackResolver(fallback_category="Холодильне обладнання")
    res = r.resolve(_SP())
    assert res.category == "Холодильне обладнання"
    assert res.source == "fallback"


def test_build_resolver_fallback_only_resolves_every_sp():
    resolver = build_resolver(export_rows=[], strategies=("fallback",))
    for brand in ("HURAKAN", "APACH", None, ""):
        res = resolver.resolve(_SP(brand=brand), brand=brand)
        assert res.category == DEFAULT_FALLBACK_CATEGORY
        assert res.category  # non-empty Раздел guaranteed


def test_build_resolver_ignores_unknown_strategies():
    # Forward-compatible: 09-02's strategy names are silently ignored by the core
    # so the chain still ends with the fallback and yields a category.
    resolver = build_resolver(
        export_rows=[], strategies=("feed", "analogy", "ai", "fallback")
    )
    res = resolver.resolve(_SP(), brand="HURAKAN")
    assert res.category == DEFAULT_FALLBACK_CATEGORY


def test_chain_resolver_empty_yields_none():
    # An empty chain (no fallback) returns category=None / source="none".
    res = ChainResolver([]).resolve(_SP())
    assert res.category is None
    assert res.source == "none"


def test_chain_resolver_first_non_empty_wins():
    class _Yes:
        def resolve(self, sp, *, brand=None):
            return CategoryResult(category="Печі", confidence=90.0, source="feed")

    class _No:
        def resolve(self, sp, *, brand=None):
            return CategoryResult(category=None, confidence=0.0, source="none")

    chain = ChainResolver([_No(), _Yes(), FallbackResolver()])
    res = chain.resolve(_SP())
    assert res.category == "Печі"
    assert res.source == "feed"
