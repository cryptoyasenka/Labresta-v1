"""Tests for Step 0 model-identifier gate in find_match_candidates.

When a supplier offer carries only generic category words (Cyrillic
'Вітрина холодильна', 'Льодогенератор') with no digit/Latin token and no
article/model field, fuzzy-matching produces ~90% hits against every
same-class catalog entry — drowning review. The gate must suppress those
without blocking legitimate SPs that have a model identifier in any form:
name digits, Latin-alpha tokens, or explicit article/model fields.
"""

from app.services.matcher import find_match_candidates


def _make_prom(id, name, brand="Tecnodom", price=477100, model=None,
               article=None, display_article=None):
    return {
        "id": id, "name": name, "brand": brand, "price": price,
        "model": model, "article": article, "display_article": display_article,
    }


class TestDiscriminatorGateSuppressesGenericSP:
    """SP with only Cyrillic category tokens must produce zero candidates."""

    def test_vitrina_holodilna_generates_no_candidates(self):
        # The exact SP from Maresto that prompted the gate: name is bare
        # "Вітрина холодильна", brand=Tecnodom, no article, no model.
        prom = [
            _make_prom(1, "Вітрина холодильна Tecnodom EVOK90VW",    price=477100),
            _make_prom(2, "Вітрина холодильна Tecnodom EVOK90V290",  price=477100),
            _make_prom(3, "Вітрина холодильна Tecnodom P-EVOK150V",  price=477100),
        ]
        result = find_match_candidates(
            "Вітрина холодильна", "Tecnodom", prom,
            supplier_price_cents=477100,
        )
        assert result == []

    def test_single_cyrillic_category_word_no_candidates(self):
        prom = [
            _make_prom(1, "Льодогенератор Brema CB174",  brand="Brema", price=100000),
            _make_prom(2, "Льодогенератор Brema GB903",  brand="Brema", price=120000),
        ]
        result = find_match_candidates(
            "Льодогенератор", "Brema", prom,
            supplier_price_cents=110000,
        )
        assert result == []

    def test_long_cyrillic_phrase_no_candidates(self):
        prom = [
            _make_prom(1, "Машина для виробництва макаронних виробів Fimar MPF 1.5N",
                       brand="Fimar", price=300000),
        ]
        result = find_match_candidates(
            "Машина для виробництва макаронних виробів", "Fimar", prom,
            supplier_price_cents=300000,
        )
        assert result == []


class TestDiscriminatorGateAllowsValidSP:
    """SPs with real identifiers must not be blocked by the gate."""

    def test_digit_token_passes_gate(self):
        # SP name has digit "47" → gate must defer to the regular pipeline
        # (which finds the identical pp via fuzzy at 100%).
        prom = [
            _make_prom(1, "Плита Apach APRI-47", brand="Apach", price=50100),
        ]
        result = find_match_candidates(
            "Плита Apach APRI-47", "Apach", prom,
            supplier_price_cents=50100,
        )
        assert len(result) == 1
        assert result[0]["prom_product_id"] == 1

    def test_latin_token_passes_gate(self):
        # "Apparat Sirman Softcooker XP" — after-brand tokens {softcooker, xp}
        # are pure Latin, represent a model family. Gate must pass.
        prom = [
            _make_prom(1, "Апарат низькотемпературного приготування Sirman Softcooker XP",
                       brand="Sirman", price=150000),
        ]
        result = find_match_candidates(
            "Апарат низькотемпературного приготування Sirman Softcooker XP",
            "Sirman", prom, supplier_price_cents=150000,
        )
        assert len(result) == 1

    def test_article_field_bypasses_gate(self):
        # Imaginary case: SP name is bare Cyrillic BUT article is set.
        # Article alone is a strong identifier — gate must defer.
        prom = [
            _make_prom(1, "Міксер Sirman Plutone LT10", brand="Sirman",
                       price=430000, display_article="60SN002"),
        ]
        result = find_match_candidates(
            "Міксер",          # would be blocked on name alone
            "Sirman", prom,
            supplier_price_cents=430000,
            supplier_article="60SN002",
        )
        # Fast-path via article must still fire.
        assert len(result) == 1
        assert result[0]["score"] == 100.0

    def test_model_field_bypasses_gate(self):
        prom = [
            _make_prom(1, "Плита APACH APRI-47P", brand="Apach", price=50100),
        ]
        result = find_match_candidates(
            "Плита",           # generic name
            "Apach", prom,
            supplier_price_cents=50100,
            supplier_model="APRI-47",
        )
        # Gate bypassed (supplier_model present); name-model extraction then
        # latches onto APRI-47 ⊂ APRI-47P and produces a candidate.
        assert len(result) >= 1
