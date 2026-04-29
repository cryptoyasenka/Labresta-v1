"""Regression tests for article-style dash gluing in tokenization.

Background: РП-Україна writes Unox SKUs as "XEKPT-08EU-C" while Maresto and
the catalog write "XEKPT08EUC". Without dash gluing the supplier produces
{xekpt, 08, eu, c} and the catalog produces {xekpt, 08, euc} — the
containment gate rejects them.

The fix glues `[A-Z0-9]-[A-Z0-9]` runs (uppercase article-style only) before
the split-by-dash step. This file pins the new behavior and the safety
boundaries: lowercase words, Cyrillic compounds, and size fractions must
stay unaffected.
"""

from __future__ import annotations

from app.services.matcher import meaningful_tokens


class TestDashGlueArticleStyle:
    def test_uppercase_dashed_sku_matches_glued_form(self):
        a = meaningful_tokens("Лист випічний UNOX XEKPT-08EU-C")
        b = meaningful_tokens("Лист випічний Unox XEKPT08EUC")
        assert a == b, (
            f"РП dashed SKU and catalog glued SKU must tokenize identically: "
            f"{sorted(a)} vs {sorted(b)}"
        )

    def test_three_segment_uppercase_glues(self):
        a = meaningful_tokens("Піч UNOX XEFR-03EU-ELDV")
        b = meaningful_tokens("Піч Unox XEFR03EUELDV")
        assert a == b

    def test_four_segment_uppercase_glues(self):
        a = meaningful_tokens("Піч UNOX XEBC-04EU-E1RM-MP")
        b = meaningful_tokens("Піч Unox XEBC04EUE1RMMP")
        assert a == b

    def test_dash_with_digit_neighbour_glues(self):
        # Digit on the left, letter on the right.
        a = meaningful_tokens("Гриль AIRHOT SL-300")
        b = meaningful_tokens("Гриль AIRHOT SL300")
        assert a == b


class TestDashGlueDoesNotBreakExistingBehaviour:
    def test_lowercase_compound_still_splits(self):
        # Lowercase compounds like "кофе-машина" must remain split — the
        # regex requires uppercase on at least one side.
        tokens = meaningful_tokens("кофе-машина automatic")
        assert "кофе" in tokens
        assert "машина" in tokens

    def test_cyrillic_dash_compound_unchanged(self):
        # Cyrillic letters are not in the [A-Z0-9] class, so the regex
        # never fires and the existing split-on-dash behavior is kept.
        tokens = meaningful_tokens("прес-кіп для ножів")
        # Both halves of the compound should appear separately (≥2 chars).
        assert "прес" in tokens or "кіп" in tokens

    def test_gn_size_fraction_unchanged(self):
        a = meaningful_tokens("Шафа GN-1/1")
        b = meaningful_tokens("Шафа GN1/1")
        # Both tokenize to {gn, 1} via slash split; the dash-glue must not
        # introduce a new {gn1} token or collapse the digits.
        assert a == b
        assert "gn" in a
        assert "1" in a

    def test_letter_only_fragment_stays_dash_split(self):
        # Critical safety: HKN-FNT-M vs HKN-FNT-A in PP catalog (pp#3269 vs
        # pp#3291) are real distinct products. The glue regex must NOT fire
        # on letter-only article fragments — otherwise they collapse to
        # 'hknfntm' / 'hknfnta' and _near_duplicate_token treats them as
        # siblings, causing false matches between separate SKUs. Only
        # fragments that contain at least one digit are glued (real-world
        # SKU codes where variants differ in digits, not letters).
        tokens = meaningful_tokens("Hurakan HKN-FNT-M з набором дисків")
        assert "hkn" in tokens
        assert "fnt" in tokens
        assert "m" in tokens
        # The glued form must NOT appear.
        assert "hknfntm" not in tokens

    def test_letter_only_siblings_distinguishable(self):
        a = meaningful_tokens("HURAKAN HKN-FNT-M")
        b = meaningful_tokens("HURAKAN HKN-FNT-A")
        assert a != b
        # Both must contain the suffix as a separate token so the
        # containment gate can distinguish them downstream.
        assert "m" in a
        assert "a" in b


class TestUnoxXEVCFamily:
    """Concrete Unox examples from РП feed that motivated the fix."""

    def test_xevc_03eu_e1rm_matches_catalog(self):
        sup = meaningful_tokens("Пароконвектомат UNOX XEVC-0311-E1RM")
        cat = meaningful_tokens(
            "Пароконвектомат UNOX XEVC0311E1RM ONE на 3 рівні"
        )
        # Supplier tokens must be a subset of catalog tokens.
        assert sup.issubset(cat) or sup - cat == set(), (
            f"sup tokens not contained in catalog tokens: "
            f"sup={sorted(sup)} cat={sorted(cat)} extras={sorted(sup - cat)}"
        )

    def test_xebpc_08eu_b_matches_glued(self):
        a = meaningful_tokens("Піч UNOX XEBPC-08EU-B")
        b = meaningful_tokens("Піч Unox XEBPC08EUB")
        assert a == b
