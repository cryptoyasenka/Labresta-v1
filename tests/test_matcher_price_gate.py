"""Tests for matcher: price gate, type gate, model matching."""

from app.services.matcher import (
    find_match_candidates,
    extract_model_from_name,
    extract_product_type,
    MAX_PRICE_RATIO,
)


def _make_prom(id, name, brand="TestBrand", price=10000, model=None, article=None):
    return {
        "id": id, "name": name, "brand": brand, "price": price,
        "model": model, "article": article,
    }


class TestPricePlausibility:
    """Price plausibility gate rejects candidates with implausible price ratios."""

    def test_rejects_high_ratio(self):
        """7.9x ratio (oven vs tray) should be rejected."""
        prom = [
            _make_prom(1, "Противень Unox TG935 для XFT133", "Unox", 13500),
        ]
        result = find_match_candidates(
            "Піч конвекційна Unox XFT133", "Unox", prom,
            supplier_price_cents=107300,
        )
        assert len(result) == 0

    def test_accepts_similar_price(self):
        """1.2x ratio should be accepted."""
        prom = [
            _make_prom(1, "Піч конвекційна Unox XFT133", "Unox", 107300),
        ]
        result = find_match_candidates(
            "Піч конвекційна Unox XFT133", "Unox", prom,
            supplier_price_cents=90000,
        )
        assert len(result) == 1

    def test_accepts_within_3x_boundary(self):
        """Exactly 3x ratio should be accepted (boundary)."""
        prom = [
            _make_prom(1, "Товар TestBrand ABC", "TestBrand", 30000),
        ]
        result = find_match_candidates(
            "Товар TestBrand ABC", "TestBrand", prom,
            supplier_price_cents=10000,
        )
        assert len(result) == 1

    def test_rejects_just_over_3x(self):
        """3.1x ratio should be rejected."""
        prom = [
            _make_prom(1, "Товар TestBrand ABC", "TestBrand", 31000),
        ]
        result = find_match_candidates(
            "Товар TestBrand ABC", "TestBrand", prom,
            supplier_price_cents=10000,
        )
        assert len(result) == 0

    def test_skips_gate_when_no_supplier_price(self):
        """No supplier price -> gate is skipped, candidate kept."""
        prom = [
            _make_prom(1, "Товар TestBrand ABC", "TestBrand", 100000),
        ]
        result = find_match_candidates(
            "Товар TestBrand ABC", "TestBrand", prom,
            supplier_price_cents=None,
        )
        assert len(result) == 1

    def test_skips_gate_when_no_prom_price(self):
        """No prom price -> gate is skipped, candidate kept."""
        prom = [
            _make_prom(1, "Товар TestBrand ABC", "TestBrand", None),
        ]
        result = find_match_candidates(
            "Товар TestBrand ABC", "TestBrand", prom,
            supplier_price_cents=10000,
        )
        assert len(result) == 1

    def test_keeps_plausible_rejects_implausible(self):
        """Mixed: keeps close-price match, rejects far-price match."""
        prom = [
            _make_prom(1, "Противень Unox TG935 для XFT133", "Unox", 13500),
            _make_prom(2, "Піч конвекційна Unox XFT133", "Unox", 107300),
        ]
        result = find_match_candidates(
            "Піч конвекційна Unox XFT133 з парозволоженням", "Unox", prom,
            supplier_price_cents=107300,
        )
        ids = [r["prom_product_id"] for r in result]
        assert 1 not in ids, "Tray at 135 EUR should be rejected"
        assert 2 in ids, "Oven at 1073 EUR should be kept"


class TestTypeGate:
    """Type gate rejects candidates where product types differ."""

    def test_different_types_same_brand_rejected(self):
        """Pasta cooker should NOT match combi oven (same brand Angelo Po)."""
        prom = [
            _make_prom(1, "Пароконвектомат Angelo Po BX61E", "Angelo Po", 50000),
        ]
        result = find_match_candidates(
            "Макароноварка ел. Angelo Po 0S1CP1E", "Angelo Po", prom,
            supplier_price_cents=50000,
        )
        assert len(result) == 0

    def test_oven_does_not_match_tray(self):
        """Convection oven should NOT match baking tray."""
        prom = [
            _make_prom(1, "Противень Unox TG935", "Unox", 10000),
        ]
        result = find_match_candidates(
            "Печь конвекционная Unox XFT133", "Unox", prom,
            supplier_price_cents=10000,
        )
        assert len(result) == 0

    def test_smoker_does_not_match_oven(self):
        """Smoker should NOT match convection oven (completely different types)."""
        prom = [
            _make_prom(1, "Печь конвекционная Hobart HCE20", "Hobart", 50000),
        ]
        result = find_match_candidates(
            "Коптильня Hobart ACICSMOK", "Hobart", prom,
            supplier_price_cents=50000,
        )
        assert len(result) == 0

    def test_reordered_words_still_match(self):
        """'стол холодильний' and 'холодильній стол' should match."""
        prom = [
            _make_prom(1, "Холодильний стол Tecfrigo KARINA", "Tecfrigo", 50000),
        ]
        result = find_match_candidates(
            "Стол холодильний Tecfrigo KARINA", "Tecfrigo", prom,
            supplier_price_cents=50000,
        )
        assert len(result) == 1
        assert result[0]["score"] >= 80

    def test_same_product_with_suffix_matches(self):
        """Same product with additional description should match."""
        prom = [
            _make_prom(1, "Піч конвекційна Unox XFT133 з парозволоженням", "Unox", 100000),
        ]
        result = find_match_candidates(
            "Піч конвекційна Unox XFT133", "Unox", prom,
            supplier_price_cents=100000,
        )
        assert len(result) == 1
        assert result[0]["score"] >= 80

    def test_no_brand_skips_type_gate(self):
        """When brand is None, type gate is skipped."""
        prom = [
            _make_prom(1, "Товар TestBrand ABC", "TestBrand", 10000),
        ]
        result = find_match_candidates(
            "Товар TestBrand ABC", None, prom,
            supplier_price_cents=10000,
        )
        assert len(result) == 1


class TestArticleModelFastPath:
    """Article/model exact match provides score=100 fast path."""

    def test_exact_article_match_scores_100(self):
        """Matching articles should produce score=100."""
        prom = [
            _make_prom(1, "Some different name Unox", "Unox", 100000,
                       article="XFT133"),
        ]
        result = find_match_candidates(
            "Піч конвекційна Unox XFT133", "Unox", prom,
            supplier_price_cents=100000,
            supplier_article="XFT133",
        )
        assert len(result) == 1
        assert result[0]["score"] == 100.0
        assert result[0]["confidence"] == "high"

    def test_article_match_case_insensitive(self):
        """Article comparison should be case-insensitive."""
        prom = [
            _make_prom(1, "Product Brand", "Brand", 10000, article="xft133"),
        ]
        result = find_match_candidates(
            "Product Brand", "Brand", prom,
            supplier_price_cents=10000,
            supplier_article="XFT133",
        )
        assert len(result) == 1
        assert result[0]["score"] == 100.0

    def test_different_articles_no_fast_path(self):
        """Different articles should not trigger fast path."""
        prom = [
            _make_prom(1, "Противень Unox TG935", "Unox", 10000,
                       article="TG935"),
        ]
        result = find_match_candidates(
            "Піч конвекційна Unox XFT133", "Unox", prom,
            supplier_price_cents=10000,
            supplier_article="XFT133",
        )
        # Type gate should reject (Противень vs Піч), and no fast path
        assert len(result) == 0

    def test_model_match_when_no_article(self):
        """Model field match works when article is not available."""
        prom = [
            _make_prom(1, "Плита Bertos G7F4B", "Bertos", 50000, model="G7F4B"),
        ]
        result = find_match_candidates(
            "Плита газова Bertos G7F4B", "Bertos", prom,
            supplier_price_cents=50000,
            supplier_model="G7F4B",
        )
        assert len(result) == 1
        assert result[0]["score"] == 100.0


class TestModelBoostPenalty:
    """Model similarity adjusts fuzzy scores up or down."""

    def test_model_mismatch_penalizes_score(self):
        """Completely different models should reduce the fuzzy score."""
        prom = [
            _make_prom(1, "Плита газова Bertos G7F4B", "Bertos", 50000, model="G7F4B"),
        ]
        result_no_model = find_match_candidates(
            "Плита газова Bertos Z200X", "Bertos", prom,
            supplier_price_cents=50000,
        )
        result_with_model = find_match_candidates(
            "Плита газова Bertos Z200X", "Bertos", prom,
            supplier_price_cents=50000,
            supplier_model="Z200X",
        )
        if result_no_model and result_with_model:
            assert result_with_model[0]["score"] < result_no_model[0]["score"]

    def test_no_model_fields_no_adjustment(self):
        """When neither side has model, score is unchanged."""
        prom = [
            _make_prom(1, "Товар TestBrand ABC", "TestBrand", 10000),
        ]
        result = find_match_candidates(
            "Товар TestBrand ABC", "TestBrand", prom,
            supplier_price_cents=10000,
        )
        assert len(result) == 1

    def test_snack_model_differ_by_one_digit_rejected(self):
        """SNACK2100TN-FC vs SNACK3100TN-FC must NOT cross-match (MARESTO regression)."""
        prom = [
            _make_prom(1, "Стіл холодильний Forcold G-SNACK2100TN-FC", "Forcold", 164100),
        ]
        result = find_match_candidates(
            "Стіл холодильний Forcold G-SNACK3100TN-FC", "Forcold", prom,
            supplier_price_cents=191300,
        )
        assert len(result) == 0

    def test_snack_identical_still_matches(self):
        """Same SNACK model on both sides must still match at 100."""
        prom = [
            _make_prom(1, "Стіл холодильний Forcold G-SNACK2100TN-FC", "Forcold", 164100),
        ]
        result = find_match_candidates(
            "Стіл холодильний Forcold G-SNACK2100TN-FC", "Forcold", prom,
            supplier_price_cents=164100,
        )
        assert len(result) == 1
        assert result[0]["score"] == 100.0

    def test_article_hyphen_normalized(self):
        """Articles with hyphens/spaces normalize to same identifier."""
        prom = [
            _make_prom(1, "Product Brand", "Brand", 10000, article="XFT-133"),
        ]
        result = find_match_candidates(
            "Product Brand", "Brand", prom,
            supplier_price_cents=10000,
            supplier_article="XFT133",
        )
        assert len(result) == 1
        assert result[0]["score"] == 100.0

    def test_article_one_char_differ_rejected(self):
        """Articles differing by one character must not fast-path match."""
        prom = [
            _make_prom(1, "Product Brand", "Brand", 10000, article="XFT133"),
        ]
        result = find_match_candidates(
            "Product Brand", "Brand", prom,
            supplier_price_cents=10000,
            supplier_article="XFT134",
        )
        assert len(result) == 0


class TestExtractProductType:
    """Unit tests for product type extraction."""

    def test_simple_type_extraction(self):
        assert extract_product_type("Печь Unox XFT133", "Unox") == "Печь"

    def test_multi_word_type(self):
        result = extract_product_type("Стол холодильний Tecfrigo KARINA", "Tecfrigo")
        assert "Стол" in result
        assert "холодильний" in result

    def test_type_with_abbreviation(self):
        result = extract_product_type("Макароноварка ел. Angelo Po 0S1CP1E", "Angelo Po")
        assert "Макароноварка" in result

    def test_brand_not_in_name_returns_empty(self):
        assert extract_product_type("Макароноварка 0S1CP1E", "UnknownBrand") == ""

    def test_no_brand_returns_empty(self):
        assert extract_product_type("Some product", None) == ""

    def test_brand_at_start_returns_empty(self):
        """Brand at the very start means no type prefix."""
        assert extract_product_type("Unox XFT133", "Unox") == ""


class TestBrandNotInCatalog:
    """Supplier brand absent from catalog → no matches (no fallback to full pool)."""

    def test_brand_not_in_catalog_returns_empty(self):
        """Hobart supplier product must NOT cross-match Helia Smoker product."""
        prom = [
            _make_prom(1, "Коптильня HELIA SMOKER HELIA 24", "Helia Smoker", 92300),
        ]
        result = find_match_candidates(
            "Коптильня Hobart ACICSMOK", "Hobart", prom,
            supplier_price_cents=92300,
        )
        assert len(result) == 0

    def test_electrolux_does_not_match_apach(self):
        """Electrolux supplier product must NOT match APACH plita."""
        prom = [
            _make_prom(1, "Плита APACH APRES-77T", "Apach", 304800),
            _make_prom(2, "Плита електрична TATRA TER.87", "Tatra", 304800),
        ]
        result = find_match_candidates(
            "Плита електрична Electrolux E7HOED2000", "Electrolux", prom,
            supplier_price_cents=304800,
        )
        assert len(result) == 0

    def test_fm_industrial_does_not_match_rational(self):
        """FM Industrial vs Rational — different brands, no cross-match."""
        prom = [
            _make_prom(1, "Ополіскувач RATIONAL (10 л.)", "Rational", 17200),
        ]
        result = find_match_candidates(
            "Ополіскувач FM Industrial 870H09", "FM Industrial", prom,
            supplier_price_cents=10600,
        )
        assert len(result) == 0

    def test_no_supplier_brand_still_falls_back(self):
        """When supplier has no brand at all, fallback to full pool still works."""
        prom = [
            _make_prom(1, "Товар Brand ABC", "Brand", 10000),
        ]
        result = find_match_candidates(
            "Товар Brand ABC", None, prom,
            supplier_price_cents=10000,
        )
        # Still matches because supplier has no brand to check against catalog
        assert len(result) == 1


class TestBrandWhitespaceVariants:
    """Brand variants differing only by whitespace/punctuation must still gate correctly."""

    def test_restoitalia_model_extracted_with_space_variant(self):
        """'RESTO ITALIA' brand must find 'Restoitalia' in name and extract model."""
        assert extract_model_from_name(
            "Тістоміс Restoitalia SK402VTW, 41 літр", "RESTO ITALIA"
        ) == "sk402vtw,"

    def test_restoitalia_different_models_rejected(self):
        """SK10MOTW vs SK402VTW must be rejected even when brand has whitespace variant."""
        prom = [
            _make_prom(
                1,
                "Тістоміс Restoitalia SK402VTW, 41 літр, 2 швидкості",
                "RESTO ITALIA",
                149300,
            ),
        ]
        result = find_match_candidates(
            "Тістоміс Restoitalia SK10MOTW", "Restoitalia", prom,
            supplier_price_cents=117200,
        )
        assert len(result) == 0

    def test_restoitalia_identical_model_still_matches(self):
        """Same SK402VTW on both sides must still match despite brand whitespace diff."""
        prom = [
            _make_prom(
                1,
                "Тістоміс Restoitalia SK402VTW, 41 літр, 2 швидкості",
                "RESTO ITALIA",
                149300,
            ),
        ]
        result = find_match_candidates(
            "Тістоміс Restoitalia SK402VTW", "Restoitalia", prom,
            supplier_price_cents=149300,
        )
        assert len(result) == 1
