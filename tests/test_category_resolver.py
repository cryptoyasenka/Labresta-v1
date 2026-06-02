"""Tests for app.services.category_resolver — the CORE fallback-only tier.

Plan 09-02 appends tests here for the smart tiers (feed / analogy / AI). For
the CORE we only assert: the FallbackResolver always hands back the holding
category, and the build_resolver factory (fallback-only) resolves every product
to a non-empty Раздел. Pure: SPs are tiny duck-typed stand-ins.
"""

import openpyxl

from app.services.category_export import read_category_corpus
from app.services.category_resolver import (
    DEFAULT_FALLBACK_CATEGORY,
    AICategoryResolver,
    AnalogyResolver,
    CategoryResult,
    ChainResolver,
    FallbackResolver,
    FeedCategoryResolver,
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


# =========================================================================== #
# Task 2: category_export.read_category_corpus
# =========================================================================== #
# Canonical export header labels (mirrors app/services/category_export.py).
_EXPORT_HEADER = [
    "Артикул",                              # 0  external_id
    "id",                                   # 1
    "Артикул для отображения на сайте",     # 2  display_article
    "Описание категории (UA)",              # 3
    "Описание категории (RU)",              # 4
    "Название (UA)",                        # 5  name
    "Название (RU)",                        # 6
    "Бренд",                                # 7  brand
    "Раздел",                               # 8  category
]


def _make_export(tmp_path, data_rows, *, header=None, sheet="Sheet1"):
    """Write a tiny Horoshop-export workbook; data_rows keyed by header label."""
    hdr = header if header is not None else _EXPORT_HEADER
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = sheet
    ws.append(hdr)
    idx = {label: i for i, label in enumerate(hdr)}
    for spec in data_rows:
        row = [None] * len(hdr)
        for label, val in spec.items():
            if label in idx:
                row[idx[label]] = val
        ws.append(row)
    path = tmp_path / "horoshop-export.xlsx"
    wb.save(path)
    wb.close()
    return str(path)


def test_read_corpus_basic(tmp_path):
    path = _make_export(tmp_path, [
        {
            "Артикул": "624348659",
            "Артикул для отображения на сайте": "GF-IC30",
            "Название (UA)": "Плита індукційна GoodFood IC30 DOUBLE",
            "Бренд": "GoodFood",
            "Раздел": "Плити професійні/Індукційні плити",
        },
        {
            "Артикул": "777",
            "Название (UA)": "Льодогенератор Hurakan HKN-IMC25",
            "Бренд": "HURAKAN",
            "Раздел": "Холодильне та морозильне обладнання/Льодогенератори",
        },
    ])
    rows, errors = read_category_corpus(path)
    assert errors == []
    assert len(rows) == 2
    by_id = {r["external_id"]: r for r in rows}
    assert by_id["624348659"]["category"] == "Плити професійні/Індукційні плити"
    assert by_id["624348659"]["brand"] == "GoodFood"
    assert by_id["624348659"]["display_article"] == "GF-IC30"
    assert by_id["777"]["name"] == "Льодогенератор Hurakan HKN-IMC25"
    assert by_id["777"]["category"].endswith("Льодогенератори")


def test_read_corpus_aborts_without_razdel(tmp_path):
    header = [h for h in _EXPORT_HEADER if h != "Раздел"]
    path = _make_export(
        tmp_path,
        [{"Артикул": "1", "Название (UA)": "x", "Бренд": "B"}],
        header=header,
    )
    rows, errors = read_category_corpus(path)
    assert rows == []
    assert len(errors) == 1
    assert "Раздел" in errors[0]


def test_read_corpus_skips_empty_category(tmp_path):
    path = _make_export(tmp_path, [
        {"Артикул": "1", "Бренд": "B", "Раздел": ""},      # blank → skipped
        {"Артикул": "2", "Бренд": "B", "Раздел": None},    # None → skipped
        {"Артикул": "3", "Бренд": "B", "Раздел": "Печі/Конвекційні"},
    ])
    rows, errors = read_category_corpus(path)
    assert errors == []
    assert [r["external_id"] for r in rows] == ["3"]


# =========================================================================== #
# Task 3: FeedCategoryResolver
# =========================================================================== #
_STORE_CATS = {
    "Холодильне та морозильне обладнання/Льодогенератори",
    "Плити професійні (варильні поверхні)/Індукційні плити",
    "Печі/Конвекційні печі",
}


def test_feed_exact_match():
    # Feed category equals a store category → source "feed", confidence 100.
    cat = "Печі/Конвекційні печі"
    r = FeedCategoryResolver(_STORE_CATS, lambda sp: cat)
    res = r.resolve(_SP())
    assert res.category == cat
    assert res.source == "feed"
    assert res.confidence == 100.0


def test_feed_reconciles_to_store():
    # Feed wording differs from the store tree but reconciles to it.
    feed_cat = "Холодильне обладнання/Льодогенератори"
    store_cat = "Холодильне та морозильне обладнання/Льодогенератори"
    r = FeedCategoryResolver(_STORE_CATS, lambda sp: feed_cat)
    res = r.resolve(_SP())
    assert res.category == store_cat          # reconciled to the store value
    assert res.category in _STORE_CATS        # never invents a category
    assert res.source == "feed"
    assert res.confidence >= 80.0


def test_feed_no_match_falls_through():
    # A feed category with no store analog → category None (chain falls through).
    r = FeedCategoryResolver(_STORE_CATS, lambda sp: "Барне обладнання/Шейкери")
    res = r.resolve(_SP())
    assert res.category is None
    assert res.source == "feed"


def test_feed_no_feed_category_returns_none():
    r = FeedCategoryResolver(_STORE_CATS, lambda sp: None)
    res = r.resolve(_SP())
    assert res.category is None
    assert res.source == "feed"


# --- Phase 9: OPT-IN feed→store mapping (Option B) ------------------------- #
# A feed label that would NOT reconcile on its own is rewritten by an explicit
# mapping to a store label and resolves at confidence 100 — and WITHOUT the
# mapping the SAME input behaves exactly as the baseline (pin equivalence).
_UNRECONCILED_FEED = "Барне обладнання/Шейкери"  # see test_feed_no_match_falls_through
_MAPPED_STORE = "Печі/Конвекційні печі"          # a real store label in _STORE_CATS


def test_feed_mapping_rewrites_unreconciled_label_to_store_at_100():
    # Opt-in: the unreconcilable feed label is mapped → store label, conf 100.
    r = FeedCategoryResolver(
        _STORE_CATS,
        lambda sp: _UNRECONCILED_FEED,
        mapping={_UNRECONCILED_FEED: _MAPPED_STORE},
    )
    res = r.resolve(_SP())
    assert res.category == _MAPPED_STORE       # rewritten to the mapped store value
    assert res.category in _STORE_CATS         # still never invents a category
    assert res.source == "feed"                # source unchanged
    assert res.confidence == 100.0             # exact store hit after rewrite


def test_feed_mapping_none_is_baseline_equivalence():
    # WITHOUT a mapping (None) the SAME input is byte-for-byte the baseline:
    # the unreconcilable feed label still falls through (category None).
    getter = lambda sp: _UNRECONCILED_FEED  # noqa: E731
    baseline = FeedCategoryResolver(_STORE_CATS, getter).resolve(_SP())
    mapped_none = FeedCategoryResolver(
        _STORE_CATS, getter, mapping=None
    ).resolve(_SP())
    mapped_empty = FeedCategoryResolver(
        _STORE_CATS, getter, mapping={}
    ).resolve(_SP())
    assert baseline.category is None
    assert (mapped_none.category, mapped_none.source) == (None, "feed")
    assert (mapped_empty.category, mapped_empty.source) == (None, "feed")
    # An unmapped label under a NON-empty mapping also passes through unchanged.
    other = FeedCategoryResolver(
        _STORE_CATS, getter, mapping={"Інше/Геть інше": _MAPPED_STORE}
    ).resolve(_SP())
    assert other.category is None and other.source == "feed"


def test_build_resolver_threads_category_mapping_into_feed_tier():
    # build_resolver passes category_mapping into the feed tier; an unreconciled
    # feed label resolves via the map at conf 100, else (no map) falls through to
    # fallback. Pins the factory-level opt-in wiring.
    mapped = build_resolver(
        export_rows=[],
        strategies=("feed", "analogy", "fallback"),
        store_categories=_STORE_CATS,
        feed_category_getter=lambda sp: _UNRECONCILED_FEED,
        category_mapping={_UNRECONCILED_FEED: _MAPPED_STORE},
    ).resolve(_SP())
    assert mapped.category == _MAPPED_STORE
    assert mapped.source == "feed"
    assert mapped.confidence == 100.0

    # No mapping → the same unreconciled label falls through to fallback.
    unmapped = build_resolver(
        export_rows=[],
        strategies=("feed", "analogy", "fallback"),
        store_categories=_STORE_CATS,
        feed_category_getter=lambda sp: _UNRECONCILED_FEED,
    ).resolve(_SP())
    assert unmapped.source == "fallback"
    assert unmapped.category == DEFAULT_FALLBACK_CATEGORY


# =========================================================================== #
# Task 3: AnalogyResolver
# =========================================================================== #
def _corpus():
    # Two HURAKAN cards in DIFFERENT categories + one other-brand card.
    return [
        {
            "external_id": "H-ICE",
            "name": "Льодогенератор Hurakan HKN-IMC25 кубик",
            "brand": "HURAKAN",
            "category": "Холодильне та морозильне обладнання/Льодогенератори",
        },
        {
            "external_id": "H-OVEN",
            "name": "Піч конвекційна Hurakan HKN-XF023",
            "brand": "HURAKAN",
            "category": "Печі/Конвекційні печі",
        },
        {
            "external_id": "A-PLITA",
            "name": "Плита індукційна Apach AT200",
            "brand": "APACH",
            "category": "Плити професійні (варильні поверхні)/Індукційні плити",
        },
    ]


def test_analogy_same_brand_top1():
    r = AnalogyResolver(_corpus(), cutoff=60.0)
    # A HURAKAN ice-maker SP whose name tokens match the H-ICE card.
    sp = _SP(brand="HURAKAN", name="Льодогенератор заливного типу Hurakan HKN-IMC40 кубик")
    res = r.resolve(sp, brand="HURAKAN")
    assert res.category == "Холодильне та морозильне обладнання/Льодогенератори"
    assert res.source == "analogy"
    assert res.analog_id == "H-ICE"
    assert res.confidence >= 60.0


def test_analogy_below_cutoff_returns_none():
    r = AnalogyResolver(_corpus(), cutoff=90.0)
    # Same brand but weak token overlap vs either HURAKAN card.
    sp = _SP(brand="HURAKAN", name="Серветниця настільна металева")
    res = r.resolve(sp, brand="HURAKAN")
    assert res.category is None
    assert res.source == "analogy"


def test_analogy_no_brand_returns_none():
    r = AnalogyResolver(_corpus(), cutoff=60.0)
    sp = _SP(brand="", name="Льодогенератор Hurakan HKN-IMC25")
    res = r.resolve(sp, brand="")
    assert res.category is None
    assert res.source == "analogy"


def test_analogy_unknown_brand_returns_none():
    r = AnalogyResolver(_corpus(), cutoff=60.0)
    sp = _SP(brand="NONEXISTENT", name="Льодогенератор HKN-IMC25")
    res = r.resolve(sp, brand="NONEXISTENT")
    assert res.category is None


def test_analogy_cyrillic_latin_brand_normalized():
    # Brand blocking must survive a Cyrillic/Latin mix (HURAKAN vs ХУРАКАН-like).
    corpus = [{
        "external_id": "C1",
        "name": "Тістоміс HURAKAN HKN-20",
        "brand": "HURAKAN",
        "category": "Тісто/Тістоміси",
    }]
    r = AnalogyResolver(corpus, cutoff=50.0)
    sp = _SP(brand="Hurakan", name="Тістоміс HURAKAN HKN-20CN")
    res = r.resolve(sp, brand="Hurakan")
    assert res.category == "Тісто/Тістоміси"
    assert res.source == "analogy"


# =========================================================================== #
# Task 3: AICategoryResolver (disabled stub)
# =========================================================================== #
def test_ai_disabled_returns_none_no_network(monkeypatch):
    # Disabled by default: returns None and never constructs an HTTP client.
    import app.services.category_resolver as cr

    # If any code path tried to import requests/httpx and call it, fail loudly.
    def _boom(*a, **k):
        raise AssertionError("AI disabled path must make ZERO network calls")

    monkeypatch.setattr(cr, "_ai_complete", _boom, raising=False)
    r = AICategoryResolver(_STORE_CATS, enabled=False)
    res = r.resolve(_SP(), brand="HURAKAN")
    assert res.category is None
    assert res.source == "ai"
    assert res.confidence == 0.0


def test_ai_enabled_returns_label_in_store_set(monkeypatch):
    # Enabled path: the model returns a label that IS a store category verbatim →
    # resolve returns that label, source "ai", positive confidence. No real HTTP:
    # _ai_complete is monkeypatched.
    import app.services.category_resolver as cr

    label = "Печі/Конвекційні печі"
    assert label in _STORE_CATS
    monkeypatch.setenv("NVIDIA_API_KEY", "nvapi-test")
    captured = {}

    def _fake(*, model, messages, api_key, base_url, timeout):
        captured["api_key"] = api_key
        captured["model"] = model
        return label

    monkeypatch.setattr(cr, "_ai_complete", _fake, raising=False)
    r = AICategoryResolver(_STORE_CATS, enabled=True)
    res = r.resolve(_SP(), brand="HURAKAN")
    assert res.category == label
    assert res.source == "ai"
    assert res.confidence > 0.0
    assert captured["api_key"] == "nvapi-test"  # key read from env, passed through


def test_ai_enabled_normalizes_wrapping_quotes(monkeypatch):
    # ONE light normalization: strip wrapping quotes/whitespace before membership.
    # NO fuzzy matching — only an exact (post-strip) store label is accepted.
    import app.services.category_resolver as cr

    label = "Печі/Конвекційні печі"
    monkeypatch.setenv("NVIDIA_API_KEY", "nvapi-test")
    monkeypatch.setattr(
        cr, "_ai_complete",
        lambda **kw: f'  "{label}"  ',  # quoted + padded
        raising=False,
    )
    res = AICategoryResolver(_STORE_CATS, enabled=True).resolve(_SP())
    assert res.category == label
    assert res.source == "ai"


def test_ai_enabled_junk_label_returns_none(monkeypatch):
    # Model hallucinates a label NOT in the store set → category None (no opinion);
    # the resolver NEVER invents a category.
    import app.services.category_resolver as cr

    monkeypatch.setenv("NVIDIA_API_KEY", "nvapi-test")
    monkeypatch.setattr(
        cr, "_ai_complete",
        lambda **kw: "Совершенно выдуманная категория",
        raising=False,
    )
    res = AICategoryResolver(_STORE_CATS, enabled=True).resolve(_SP(), brand="HURAKAN")
    assert res.category is None
    assert res.source == "ai"
    assert res.confidence == 0.0


def test_ai_enabled_none_sentinel_returns_none(monkeypatch):
    # The prompt tells the model to answer "NONE" when nothing fits → no opinion.
    import app.services.category_resolver as cr

    monkeypatch.setenv("NVIDIA_API_KEY", "nvapi-test")
    monkeypatch.setattr(cr, "_ai_complete", lambda **kw: "NONE", raising=False)
    res = AICategoryResolver(_STORE_CATS, enabled=True).resolve(_SP())
    assert res.category is None
    assert res.source == "ai"


def test_ai_enabled_missing_key_raises_and_skips_call(monkeypatch):
    # Enabled but no API key in env → RuntimeError, and _ai_complete is NEVER
    # called (no network attempt without a key).
    import pytest

    import app.services.category_resolver as cr

    monkeypatch.delenv("NVIDIA_API_KEY", raising=False)

    def _boom(**kw):
        raise AssertionError("must not call _ai_complete without an API key")

    monkeypatch.setattr(cr, "_ai_complete", _boom, raising=False)
    r = AICategoryResolver(_STORE_CATS, enabled=True)
    with pytest.raises(RuntimeError):
        r.resolve(_SP(), brand="HURAKAN")


def test_ai_enabled_custom_base_url_and_key_env(monkeypatch):
    # Provider-agnostic: a custom base_url + api_key_env are read and forwarded
    # to _ai_complete verbatim (any OpenAI-compatible endpoint, not just NVIDIA).
    import app.services.category_resolver as cr

    label = "Печі/Конвекційні печі"
    assert label in _STORE_CATS
    monkeypatch.delenv("NVIDIA_API_KEY", raising=False)
    monkeypatch.setenv("FOO_KEY", "sk-x")
    captured = {}

    def _fake(*, model, messages, api_key, base_url, timeout):
        captured["api_key"] = api_key
        captured["base_url"] = base_url
        return label

    monkeypatch.setattr(cr, "_ai_complete", _fake, raising=False)
    r = AICategoryResolver(
        _STORE_CATS,
        enabled=True,
        base_url="https://prov.example/v1",
        api_key_env="FOO_KEY",
    )
    res = r.resolve(_SP())
    assert res.category == label
    assert captured["base_url"] == "https://prov.example/v1"  # custom endpoint
    assert captured["api_key"] == "sk-x"  # key read from the custom env var


def test_ai_enabled_custom_key_env_missing_raises(monkeypatch):
    # The opt-in gate keys on the CUSTOM api_key_env: if that var is unset,
    # resolve raises RuntimeError and never calls _ai_complete (no network).
    import pytest

    import app.services.category_resolver as cr

    monkeypatch.delenv("FOO_KEY", raising=False)

    def _boom(**kw):
        raise AssertionError("must not call _ai_complete without the custom-env key")

    monkeypatch.setattr(cr, "_ai_complete", _boom, raising=False)
    r = AICategoryResolver(_STORE_CATS, enabled=True, api_key_env="FOO_KEY")
    with pytest.raises(RuntimeError):
        r.resolve(_SP())


# =========================================================================== #
# Task 3: build_resolver chain feed → analogy → fallback (AI gated off)
# =========================================================================== #
def test_chain_feed_then_analogy_then_fallback():
    corpus = _corpus()
    store_cats = {r["category"] for r in corpus}

    # Feed getter: only ART-FEED carries a (store-reconcilable) feed category.
    feed_map = {"ART-FEED": "Печі/Конвекційні печі"}
    getter = lambda sp: feed_map.get(getattr(sp, "article", None))

    resolver = build_resolver(
        corpus,
        strategies=("feed", "analogy", "fallback"),
        store_categories=store_cats,
        feed_category_getter=getter,
        analogy_cutoff=60.0,
    )

    # 1) Feed hit.
    sp_feed = _SP(brand="HURAKAN", name="що завгодно")
    sp_feed.article = "ART-FEED"
    res = resolver.resolve(sp_feed, brand="HURAKAN")
    assert res.source == "feed"
    assert res.category == "Печі/Конвекційні печі"

    # 2) Feed misses → analogy hits (HURAKAN ice-maker).
    sp_an = _SP(brand="HURAKAN", name="Льодогенератор Hurakan HKN-IMC40 кубик")
    sp_an.article = "ART-NO-FEED"
    res = resolver.resolve(sp_an, brand="HURAKAN")
    assert res.source == "analogy"
    assert res.category == "Холодильне та морозильне обладнання/Льодогенератори"

    # 3) Both miss → fallback holding category.
    sp_fb = _SP(brand="", name="Невідомий предмет")
    sp_fb.article = "ART-NONE"
    res = resolver.resolve(sp_fb, brand="")
    assert res.source == "fallback"
    assert res.category == DEFAULT_FALLBACK_CATEGORY
    assert res.category  # every SP gets a non-empty category (REQ-03)


def test_build_resolver_ai_off_by_default_excludes_ai_tier():
    corpus = _corpus()
    resolver = build_resolver(
        corpus,
        strategies=("feed", "analogy", "ai", "fallback"),
        store_categories={r["category"] for r in corpus},
        feed_category_getter=lambda sp: None,
        ai_enabled=False,
    )
    # AI tier present but disabled → returns None and the chain still resolves
    # via analogy/fallback (no NotImplementedError raised).
    sp = _SP(brand="", name="нічого")
    res = resolver.resolve(sp, brand="")
    assert res.category == DEFAULT_FALLBACK_CATEGORY


def test_build_resolver_feed_omitted_without_getter():
    # "feed" requested but no getter → tier silently omitted; analogy/fallback run.
    corpus = _corpus()
    resolver = build_resolver(
        corpus,
        strategies=("feed", "analogy", "fallback"),
        feed_category_getter=None,
    )
    sp = _SP(brand="HURAKAN", name="Льодогенератор Hurakan HKN-IMC40 кубик")
    res = resolver.resolve(sp, brand="HURAKAN")
    assert res.source == "analogy"
