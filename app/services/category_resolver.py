"""Category resolution strategy for the Horoshop create-file builder.

A create-file row MUST carry a `[КАТАЛОГ] Раздел` — Horoshop errors on a row
with no category and will NOT create the missing category itself (RESEARCH
Q2/Pitfall 2). This module defines the resolver INTERFACE plus the CORE's only
tier: a fallback resolver that hands every product a single holding category.

The smart tiers (feed_category / analogy / AI) are layered on in plan 09-02
behind this SAME interface — `build_resolver` is forward-compatible: it accepts
an `export_rows` corpus (unused by the fallback tier) and a `strategies` tuple,
and silently ignores strategy names it does not yet recognise, so 09-02 can
grow it without touching the core.

Pure: no DB, no network. Resolvers take an SP-like object (anything exposing
`.brand`, `.name`, etc.) so they stay unit-testable.

IMPORTANT: the fallback holding category «Новые товары / на разбор» MUST be
pre-created in the Horoshop admin before any bulk import — Horoshop does not
create missing categories on import.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable


# The holding category every unmatched card lands in until an operator sorts it.
# MUST exist in Horoshop admin before importing (Horoshop won't create it).
DEFAULT_FALLBACK_CATEGORY = "Новые товары / на разбор"


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
) -> CategoryResolver:
    """Factory for the resolver chain.

    The CORE ships ``strategies=("fallback",)``. Plan 09-02 will recognise the
    extra strategy names ('feed', 'analogy', 'ai') and consult ``export_rows``
    (the Horoshop-export-derived category corpus) — those resolvers get inserted
    AHEAD of the fallback here. Unknown strategy names are ignored (forward-
    compatible) so 09-02 grows this without breaking the core.

    Args:
        export_rows: category corpus derived from the uploaded Horoshop export.
            Unused by the fallback tier (kept for the 09-02 smart tiers).
        strategies: ordered strategy names to assemble into the chain.
        fallback_category: holding category for the fallback tier.

    Returns:
        A CategoryResolver (a ChainResolver) whose ``resolve`` always returns a
        non-empty category when "fallback" is among the strategies.
    """
    resolvers: list[CategoryResolver] = []
    # 09-02 inserts feed/analogy/ai resolvers here, keyed off `strategies` and
    # built from `export_rows`, ahead of the fallback.
    if "fallback" in strategies:
        resolvers.append(FallbackResolver(fallback_category))
    return ChainResolver(resolvers)
