"""Tests for bracket-discriminator gate in find_match_candidates.

The gate rejects candidates when BOTH sp and pp have parens content AND the
parens tokens (after stripping voltage/numeric/quantity-unit noise) form
disjoint non-empty sets. The driving case is Moretti Forni T64E where
supplier sends 'T64E (no stand)' and catalog has 'T64E (на базі)': both
contain parens, both contain real discriminator words ('no stand' vs 'на
базі'), and the two sets don't overlap — so the pair is clearly a
variant/non-variant mismatch, not the same product.

The gate must NOT fire when:
  - only one side has parens (too many legitimate cases — SP minimal, PP
    verbose, or artikul in parens on one side);
  - both sides have parens but content is only voltage/numeric/quantity
    ('(380)' vs '(380 В)' — same voltage, different formatting);
  - bracket sets overlap (at least one shared meaningful token).
"""

from app.services.matcher import find_match_candidates


def _make_prom(id, name, brand="Moretti Forni", price=943500, model=None,
               article=None, display_article=None):
    return {
        "id": id, "name": name, "brand": brand, "price": price,
        "model": model, "article": article, "display_article": display_article,
    }


class TestBracketDiscriminatorRejectsMismatch:
    """Bracket content must block candidate when it signals a variant mismatch."""

    def test_moretti_no_stand_vs_na_bazi_rejected(self):
        # Exact production case: SP (no stand) vs PP (на базі) — different
        # comprehensiveness of the package. Must NOT produce a candidate.
        prom = [
            _make_prom(1, "Піч для піци конвеєрна Moretti Forni T64E (на базі)",
                       price=943500),
        ]
        result = find_match_candidates(
            "Піч для піци Moretti Forni T64E (no stand)",
            "Moretti Forni", prom,
            supplier_price_cents=916600,
        )
        assert result == []

    def test_bracket_content_overlap_still_passes(self):
        # Both sides have parens, and they share at least one meaningful
        # token ('sous vide' on both). Overlap → not a mismatch.
        prom = [
            _make_prom(1, "Sirman Softcooker XP (технологія Sous Vide)",
                       brand="Sirman", price=150000),
        ]
        result = find_match_candidates(
            "Sirman Softcooker XP (Sous Vide)", "Sirman", prom,
            supplier_price_cents=150000,
        )
        assert len(result) >= 1


class TestBracketDiscriminatorIgnoresNoise:
    """Voltage, numbers, quantity units don't count as discriminators."""

    def test_voltage_formatting_both_sides_passes(self):
        # (380) vs (380 В) — same voltage, formatting difference only.
        # Bracket-noise stripper must eat '380' and 'в', leaving empty set
        # on both sides → gate does NOT fire.
        prom = [
            _make_prom(1, "Картоплечистка Fimar PPN10 (380 В)",
                       brand="Fimar", price=120000),
        ]
        result = find_match_candidates(
            "Картоплечистка Fimar PPN10 (380)", "Fimar", prom,
            supplier_price_cents=120000,
        )
        assert len(result) >= 1

    def test_quantity_markers_both_sides_passes(self):
        # (9,4 л) vs (10 л) — pure numeric/unit content, gate must not fire
        # on them alone. (This is test of noise-stripping; the matcher may
        # still reject on price or other grounds, but the bracket gate
        # itself must classify these as noise-only and not-a-discriminator.)
        prom = [
            _make_prom(1, "Кутер Sirman C9VV (9,4 л)",
                       brand="Sirman", price=100000),
        ]
        result = find_match_candidates(
            "Кутер Sirman C9VV (10 л)", "Sirman", prom,
            supplier_price_cents=100000,
        )
        # Stripper removes digits and 'л' → both sides have empty
        # discriminator → gate must not reject. Other gates may still let
        # it through.
        assert len(result) >= 1


class TestBracketDiscriminatorOneSidedNotAffected:
    """Gate requires parens on BOTH sides. One-sided parens pass through."""

    def test_artikul_in_sp_parens_pp_plain_passes(self):
        # SP has artikul '(A150513)' in parens, PP plain text 'A150513'.
        # One-sided parens → gate must not fire.
        prom = [
            _make_prom(1, "Рисоварка 8 л Bartscher A150513",
                       brand="Bartscher", price=30000),
        ]
        result = find_match_candidates(
            "Мультиварка Bartscher (A150513)", "Bartscher", prom,
            supplier_price_cents=30000,
            supplier_article="A150513",
        )
        assert len(result) >= 1

    def test_sp_no_stand_pp_plain_base_passes(self):
        # SP carries '(no stand)' (base/no-stand version), PP is plain
        # catalog base entry. This is the legitimate SP→PP-base mapping
        # and gate must not reject it (only one side has parens).
        prom = [
            _make_prom(1, "Піч для піци конвеєрна Moretti Forni T64E",
                       price=839200),
        ]
        result = find_match_candidates(
            "Піч для піци Moretti Forni T64E (no stand)",
            "Moretti Forni", prom,
            supplier_price_cents=916600,
        )
        assert len(result) >= 1


class TestBracketDiscriminatorEmptyAndEdge:
    """Defensive: empty parens, parens with only whitespace, nested."""

    def test_empty_parens_both_sides_passes(self):
        # '()' on both sides → empty discriminator set → gate does not fire.
        prom = [
            _make_prom(1, "Fimar TV4000 ()", brand="Fimar", price=50000),
        ]
        result = find_match_candidates(
            "Fimar TV4000 ()", "Fimar", prom,
            supplier_price_cents=50000,
        )
        assert len(result) >= 1
