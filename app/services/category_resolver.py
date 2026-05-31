"""Category resolution strategy for the Horoshop create-file builder.

A create-file row MUST carry a `[КАТАЛОГ] Раздел` — Horoshop errors on a row
with no category and will NOT create the missing category itself (RESEARCH
Q2/Pitfall 2). This module defines the resolver INTERFACE plus a chain of
pluggable tiers:

  feed_category → analogy → (ai, gated OFF) → fallback

  * FallbackResolver  — the CORE's always-on tier (one holding category).
  * FeedCategoryResolver — places a feed-supplied category into «Раздел»,
    reconciled to the store tree (NEVER pushes a category the store lacks —
    Horoshop won't create it). For NP the feed category comes from the extended
    np_parser `categories_uk`.
  * AnalogyResolver — for suppliers whose feed carries no category: blocks
    candidates by brand, ranks by name-token similarity over the export «Раздел»
    corpus (matcher PRIMITIVES only — the full pipeline's price/voltage gates
    over-reject same-category items, RESEARCH Q4/Pitfall 6), applies a cutoff.
  * AICategoryResolver — a DISABLED, gated stub (RESEARCH Q5(c) + decision D3).
    Disabled by default → returns None with ZERO network. Enabling it is a
    config flip (`strategies=(...,"ai")` + `ai_enabled=True`), not a refactor;
    the enabled path is intentionally unimplemented until Yana approves (REQ-06).

Pure: no DB, no network. Resolvers take an SP-like object (anything exposing
`.brand`, `.name`, etc.) so they stay unit-testable.

IMPORTANT: the fallback holding category «Новые товары / на разбор» MUST be
pre-created in the Horoshop admin before any bulk import — Horoshop does not
create missing categories on import.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Protocol, runtime_checkable

from rapidfuzz import fuzz

from app.services.matcher import (
    _transliterate_cyr,
    meaningful_tokens,
    normalize_text,
)


# The holding category every unmatched card lands in until an operator sorts it.
# MUST exist in Horoshop admin before importing (Horoshop won't create it).
DEFAULT_FALLBACK_CATEGORY = "Новые товары / на разбор"

# Default thresholds (0..100). Feed reconciliation is stricter than analogy:
# a near-miss feed label should still map to the same store leaf, while analogy
# is comparing whole product names so a lower bar still yields a real analog.
DEFAULT_RECONCILE_CUTOFF = 80.0
DEFAULT_ANALOGY_CUTOFF = 60.0


def _norm_brand(brand: str | None) -> str:
    """Normalized brand key for blocking — lowercased + transliterated.

    Cyrillic/Latin mixes ('Hurakan' vs 'ХУРАКАН') collapse to one key so the
    analogy index blocks them together (RESEARCH Q4).
    """
    if not brand:
        return ""
    return _transliterate_cyr(normalize_text(brand)).strip()


def _leaf(category: str) -> str:
    """The leaf segment of a '/'-separated category path."""
    return category.rsplit("/", 1)[-1].strip() if category else ""


@dataclass(frozen=True)
class CategoryResult:
    """Outcome of resolving a Horoshop category for one supplier product."""

    category: str | None      # qualified Horoshop path, e.g. "Холод/Льодогенератори"
    confidence: float         # 0.0 .. 100.0
    source: str               # "feed" | "analogy" | "ai" | "fallback" | "none"
    analog_id: str | None = None


@runtime_checkable
class CategoryResolver(Protocol):
    """A resolver maps a supplier product to a Horoshop category."""

    def resolve(self, sp, *, brand: str | None = None) -> CategoryResult: ...


class FallbackResolver:
    """Always returns the holding category — the CORE's only tier.

    Guarantees every row has a non-empty Раздел so the file imports on its own,
    with no smart-category code. Plan 09-02 inserts smarter resolvers ahead of
    this one in the chain.
    """

    def __init__(self, fallback_category: str = DEFAULT_FALLBACK_CATEGORY):
        self.fallback_category = fallback_category

    def resolve(self, sp, *, brand: str | None = None) -> CategoryResult:
        return CategoryResult(
            category=self.fallback_category,
            confidence=0.0,
            source="fallback",
        )


class FeedCategoryResolver:
    """Tier 0: place a feed-supplied category into «Раздел», reconciled to store.

    For NP (the ~205-item bulk of Phase 9) the feed itself carries the category
    (`categories_uk`), so this resolves most NP rows with no analogy. BUT the
    feed wording differs from the store tree (feed «Холодильне обладнання/…» vs
    store «Холодильне та морозильне обладнання/…») and Horoshop will NOT create a
    missing category — so the feed value is reconciled to the store label set and
    a value NOT in that set never leaves this resolver (the chain falls through).

    Optionally an explicit feed→store ``mapping`` (Option B, opt-in) is consulted
    FIRST: when a feed label is a key in the mapping, it is rewritten to the store
    value BEFORE reconcile, so a mapped label exact-matches the store set and
    resolves at confidence 100 (source unchanged = "feed"). ``None``/``{}`` ⇒
    behaviour is byte-for-byte the baseline (unchanged fuzzy reconcile). This is
    the SAME ``mapping.get(label, label)`` rewrite the audit ``--mapping`` flag
    applies — kept consistent so the live path matches the measured what-if.

    Args:
        store_categories: the allowed «Раздел» label set (distinct export values).
        feed_category_getter: callable ``sp -> str | None`` returning the SP's
            feed category (None when the SP carries none → chain falls through).
        reconcile_cutoff: min token_sort_ratio for a non-exact reconcile (0..100).
        mapping: optional feed→store override dict (Option B). None/{} ⇒ no-op.
    """

    def __init__(
        self,
        store_categories: set[str],
        feed_category_getter: Callable[[object], str | None],
        *,
        reconcile_cutoff: float = DEFAULT_RECONCILE_CUTOFF,
        mapping: dict[str, str] | None = None,
    ):
        self.store_categories = {c for c in (store_categories or set()) if c}
        self.feed_category_getter = feed_category_getter
        self.reconcile_cutoff = reconcile_cutoff
        # Opt-in feed→store rewrite map. Empty by default → reconcile unchanged.
        self.mapping = dict(mapping) if mapping else {}
        # Pre-normalize the store labels once (full path + leaf) for matching.
        self._store_norm = [
            (c, normalize_text(c), normalize_text(_leaf(c)))
            for c in self.store_categories
        ]

    def reconcile(self, feed_category: str | None) -> CategoryResult:
        """Reconcile a feed category to a store label (public for the audit).

        When an opt-in ``mapping`` is set, the feed label is first rewritten via
        ``mapping.get(label, label)`` (same expression as the audit's getter);
        with no mapping this is the identity, so the path below is unchanged.
        """
        fc = (feed_category or "").strip()
        if not fc:
            return CategoryResult(None, 0.0, "feed")
        # Opt-in Option-B rewrite (no-op when mapping is empty).
        fc = self.mapping.get(fc, fc)

        # Exact match wins outright.
        if fc in self.store_categories:
            return CategoryResult(fc, 100.0, "feed")

        # Else rank store labels by token similarity, leaf-aware: a feed
        # «…/Льодогенератори» should snap to the store «…/Льодогенератори» even
        # when the parent segment differs. Score the better of full-path and
        # leaf-vs-leaf so a matching leaf is rewarded but a coincidental leaf in
        # the wrong tree still has to clear the cutoff on the full path too.
        fc_norm = normalize_text(fc)
        fc_leaf = normalize_text(_leaf(fc))
        best_cat = None
        best_score = 0.0
        for cat, cat_norm, cat_leaf in self._store_norm:
            full = fuzz.token_sort_ratio(fc_norm, cat_norm)
            leaf = fuzz.token_sort_ratio(fc_leaf, cat_leaf) if fc_leaf and cat_leaf else 0.0
            score = max(full, leaf)
            if score > best_score:
                best_score = score
                best_cat = cat

        if best_cat is not None and best_score >= self.reconcile_cutoff:
            return CategoryResult(best_cat, best_score, "feed")
        return CategoryResult(None, 0.0, "feed")

    def resolve(self, sp, *, brand: str | None = None) -> CategoryResult:
        return self.reconcile(self.feed_category_getter(sp))


class AnalogyResolver:
    """Tier 1: copy the «Раздел» of the most similar same-brand export card.

    Blocks candidates by normalized brand (RESEARCH Q4 step 2 — no brand means no
    analog, fall through to fallback), then ranks the brand's cards by
    rapidfuzz.token_sort_ratio over meaningful_tokens(name). Reuses matcher
    PRIMITIVES only — NOT find_match_candidates, whose price/voltage gates
    over-reject items that share a category (RESEARCH Q4/Pitfall 6).

    Pure: takes the export_rows corpus (from read_category_corpus); no DB/network.
    """

    def __init__(self, export_rows, *, cutoff: float = DEFAULT_ANALOGY_CUTOFF):
        self.cutoff = cutoff
        # Pre-index by normalized brand → list of (token_string, category, id).
        # token_sort_ratio wants a string, so join the meaningful_tokens set into
        # a stable space-separated string (transliterated for Cyr/Lat parity).
        self._by_brand: dict[str, list[tuple[str, str, str | None]]] = {}
        for r in export_rows or []:
            category = (r.get("category") or "").strip()
            if not category:
                continue
            b = _norm_brand(r.get("brand"))
            if not b:
                continue
            self._by_brand.setdefault(b, []).append(
                (self._tok_string(r.get("name")), category, r.get("external_id"))
            )

    @staticmethod
    def _tok_string(name: str | None) -> str:
        toks = meaningful_tokens(_transliterate_cyr(name or ""))
        return " ".join(sorted(toks))

    def resolve(self, sp, *, brand: str | None = None) -> CategoryResult:
        b = _norm_brand(brand if brand is not None else getattr(sp, "brand", None))
        if not b:
            return CategoryResult(None, 0.0, "analogy")  # no brand → fall through
        candidates = self._by_brand.get(b)
        if not candidates:
            return CategoryResult(None, 0.0, "analogy")

        sp_tokens = self._tok_string(getattr(sp, "name", None))
        best_cat = None
        best_id = None
        best_score = 0.0
        for tok_string, category, ext_id in candidates:
            score = fuzz.token_sort_ratio(sp_tokens, tok_string)
            if score > best_score:
                best_score = score
                best_cat = category
                best_id = ext_id

        if best_cat is not None and best_score >= self.cutoff:
            return CategoryResult(best_cat, best_score, "analogy", analog_id=best_id)
        return CategoryResult(None, 0.0, "analogy")


class AICategoryResolver:
    """Tier 2: NVIDIA-backed classifier — DISABLED, gated stub (RESEARCH Q5c, D3).

    Default (``enabled=False``): ``resolve`` returns category=None IMMEDIATELY —
    no HTTP client is imported or constructed, zero network. This is the
    "config flip, not refactor" guarantee.

    Enabled path (``enabled=True``): intentionally unimplemented until Yana
    approves wiring (REQ-06). The intended shape (verify at wire time, do NOT
    hardcode now):
      * OpenAI-compatible NVIDIA endpoint (https://integrate.api.nvidia.com/v1),
        key from ``api_key_env`` (NVIDIA_API_KEY); ~40 RPM free tier.
      * Give the model the FLAT deduped «Раздел» label set + the product
        name/brand/short-description; constrain the output to exactly one label.
      * Validate the returned label ∈ store_categories, else return None
        (so the chain falls through to fallback). Non-determinism → carry a
        needs-review flag for the audit.
    """

    def __init__(
        self,
        store_categories: set[str],
        *,
        enabled: bool = False,
        model: str | None = None,
        api_key_env: str = "NVIDIA_API_KEY",
    ):
        self.store_categories = {c for c in (store_categories or set()) if c}
        self.enabled = enabled
        self.model = model
        self.api_key_env = api_key_env

    def resolve(self, sp, *, brand: str | None = None) -> CategoryResult:
        if not self.enabled:
            # Default path: no network, no key read, no client construction.
            return CategoryResult(None, 0.0, "ai")
        raise NotImplementedError(
            "AI category tier not wired — pending Yana's go-ahead (REQ-06). "
            "Enable is a config flip (strategies+ai_enabled), not a refactor; "
            "verify the NVIDIA endpoint/model at wire time."
        )


class ChainResolver:
    """Ordered list of resolvers; the first non-empty category wins.

    FallbackResolver is normally last, so a non-empty category is guaranteed.
    If the chain is empty (or every resolver returns no category), resolve()
    yields a CategoryResult with category=None and source="none".
    """

    def __init__(self, resolvers: list[CategoryResolver]):
        self.resolvers = resolvers

    def resolve(self, sp, *, brand: str | None = None) -> CategoryResult:
        for r in self.resolvers:
            res = r.resolve(sp, brand=brand)
            if res.category:
                return res
        return CategoryResult(category=None, confidence=0.0, source="none")


def build_resolver(
    export_rows,
    *,
    strategies: tuple[str, ...] = ("fallback",),
    fallback_category: str = DEFAULT_FALLBACK_CATEGORY,
    store_categories: set[str] | None = None,
    feed_category_getter: Callable[[object], str | None] | None = None,
    ai_enabled: bool = False,
    ai_model: str | None = None,
    analogy_cutoff: float = DEFAULT_ANALOGY_CUTOFF,
    reconcile_cutoff: float = DEFAULT_RECONCILE_CUTOFF,
    category_mapping: dict[str, str] | None = None,
) -> CategoryResolver:
    """Factory for the resolver chain.

    Composes the requested tiers IN ORDER, with the fallback always last so a
    non-empty «Раздел» is guaranteed when "fallback" is requested. The
    recommended SMART chain for the builder is
    ``strategies=("feed","analogy","fallback")`` with ``ai_enabled=False`` (AI
    off by default — decision D3). A future Yana-approved flip passes
    ``strategies=(...,"ai")`` + ``ai_enabled=True`` + ``ai_model=...`` — no
    refactor. Unknown strategy names are ignored (forward-compatible).

    Args:
        export_rows: category corpus from read_category_corpus (feeds the
            AnalogyResolver and, by default, the store-category label set).
        strategies: ordered tier names to assemble ("feed"/"analogy"/"ai"/
            "fallback").
        fallback_category: holding category for the fallback tier.
        store_categories: allowed «Раздел» label set; defaults to the distinct
            categories in ``export_rows``.
        feed_category_getter: ``sp -> str | None`` for the feed tier. The "feed"
            tier is OMITTED if this is None (e.g. no NP feed uploaded).
        ai_enabled: insert the AI tier as ENABLED (default False → disabled stub).
        ai_model: model id for the (future) enabled AI path.
        analogy_cutoff / reconcile_cutoff: thresholds (0..100).
        category_mapping: optional feed→store override dict (Option B, opt-in).
            Threaded into the feed tier; None/{} ⇒ behaviour unchanged.

    Returns:
        A ChainResolver whose ``resolve`` always returns a non-empty category
        when "fallback" is among the strategies.
    """
    if store_categories is None:
        store_categories = {
            r["category"] for r in (export_rows or []) if r.get("category")
        }

    resolvers: list[CategoryResolver] = []
    if "feed" in strategies and feed_category_getter is not None:
        resolvers.append(
            FeedCategoryResolver(
                store_categories,
                feed_category_getter,
                reconcile_cutoff=reconcile_cutoff,
                mapping=category_mapping,
            )
        )
    if "analogy" in strategies:
        resolvers.append(AnalogyResolver(export_rows or [], cutoff=analogy_cutoff))
    if "ai" in strategies:
        resolvers.append(
            AICategoryResolver(store_categories, enabled=ai_enabled, model=ai_model)
        )
    if "fallback" in strategies:
        resolvers.append(FallbackResolver(fallback_category))
    return ChainResolver(resolvers)
