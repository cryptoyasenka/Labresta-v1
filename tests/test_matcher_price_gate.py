"""Tests for matcher: price gate, type gate, model matching."""

from app.services.matcher import (
    find_match_candidates,
    extract_model_from_name,
    extract_product_type,
    extract_voltages,
    meaningful_tokens,
    after_brand_remainder,
    MAX_PRICE_RATIO,
)


def _make_prom(id, name, brand="TestBrand", price=10000, model=None, article=None,
               display_article=None):
    return {
        "id": id, "name": name, "brand": brand, "price": price,
        "model": model, "article": article, "display_article": display_article,
    }


class TestDisplayArticleFastPath:
    """Manufacturer SKU (display_article) embedded in supplier name → fast-path match."""

    def test_display_article_substring_in_supplier_name_matches(self):
        prom = [
            _make_prom(1, "Міксер планетарний Sirman Plutone LT10", "Sirman",
                       price=4308500, display_article="60SN002"),
        ]
        result = find_match_candidates(
            "Mixer planetary 60SN002 Sirman LT10", "Sirman", prom,
            supplier_price_cents=4300000,
        )
        assert len(result) == 1
        assert result[0]["score"] == 100.0
        assert result[0]["confidence"] == "high"

    def test_supplier_article_equals_display_article(self):
        prom = [
            _make_prom(1, "Гриль Sirman Mobile PRO", "Sirman",
                       price=2500000, display_article="30142502"),
        ]
        result = find_match_candidates(
            "Гриль PRO 1/1G", "Sirman", prom,
            supplier_price_cents=2500000,
            supplier_article="30142502",
        )
        assert len(result) == 1
        assert result[0]["score"] == 100.0

    def test_paren_code_mismatch_rejects_despite_fuzzy_100(self):
        # Supplier has article in parens WY9ENRA.0011923; catalog display_article
        # WY9ENRA.0002427 — different SKUs. Must reject even though names are
        # near-identical (fuzz would score ~100).
        prom = [
            _make_prom(
                1, "Rational iVario Pro 2-S сковорода багатофункціональна", "Rational",
                price=1947000, display_article="WY9ENRA.0002427"
            ),
        ]
        result = find_match_candidates(
            "Сковорода багатофункціональна Rational iVario Pro 2-S (WY9ENRA.0011923)",
            "Rational", prom, supplier_price_cents=2259800,
        )
        assert len(result) == 0

    def test_paren_code_match_keeps_candidate(self):
        # Supplier parenthesized code matches catalog display_article → keep.
        prom = [
            _make_prom(
                1, "Rational iVario Pro 2-S", "Rational",
                price=1947000, display_article="WY9ENRA.0002427"
            ),
        ]
        result = find_match_candidates(
            "Сковорода Rational iVario Pro 2-S (WY9ENRA.0002427)",
            "Rational", prom, supplier_price_cents=1947000,
        )
        assert len(result) == 1

    def test_short_display_article_is_not_substring_matched(self):
        # display_article shorter than 4 chars must not trigger substring
        # fast-path to avoid trivial collisions.
        prom = [
            _make_prom(1, "Випадковий товар A1", "Sirman",
                       price=1000, display_article="A1"),
        ]
        result = find_match_candidates(
            "Зовсім інший товар A1 коробка", "Sirman", prom,
            supplier_price_cents=1000,
        )
        assert all(c["score"] < 100 for c in result)

    def test_sub6_display_article_not_substring_matched(self):
        # `LT10` is 4 chars but could collide inside `LT10XXX` inside another
        # brand's unrelated SKU. Substring branch requires >=6 chars now;
        # equality path still works for direct sup_article == prom_display.
        prom = [
            _make_prom(1, "Слайсер Sirman LT10", "Sirman",
                       price=500000, display_article="LT10"),
        ]
        result = find_match_candidates(
            "Sirman somemodel LT10XXXPACK", "Sirman", prom,
            supplier_price_cents=510000,
        )
        # Must not fast-confirm via substring of short SKU.
        assert all(c["score"] < 100 for c in result)



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
        """When supplier brand is None, only match against no-brand catalog entries."""
        # Same-name pp but with a brand → must be excluded under new cross-brand policy
        prom = [
            _make_prom(1, "Товар TestBrand ABC", "TestBrand", 10000),
        ]
        result = find_match_candidates(
            "Товар TestBrand ABC", None, prom,
            supplier_price_cents=10000,
        )
        assert len(result) == 0


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

    def test_no_supplier_brand_requires_no_brand_catalog(self):
        """When supplier brand is missing, only no-brand catalog entries are eligible."""
        # A pp with brand is excluded (can't verify cross-brand); a no-brand pp
        # with identical name and high score passes.
        prom = [
            _make_prom(1, "Товар Brand ABC", "Brand", 10000),
            _make_prom(2, "Товар Brand ABC", None, 10000),
        ]
        result = find_match_candidates(
            "Товар Brand ABC", None, prom,
            supplier_price_cents=10000,
        )
        assert len(result) == 1
        assert result[0]["prom_product_id"] == 2


class TestVoltageVariantGate:
    """Same model with different voltage is a different SKU — must reject."""

    def test_220_vs_380_rejected(self):
        """М'ясорубка TC12U (220) must NOT match TC12U (380)."""
        prom = [
            _make_prom(1, "М'ясорубка Everest TC12U (380), 1/2 унгер", "Everest", 50000),
        ]
        result = find_match_candidates(
            "М'ясорубка Everest TC12U (220)", "Everest", prom,
            supplier_price_cents=50000,
        )
        assert len(result) == 0

    def test_220_with_v_suffix_rejected(self):
        """'(220)' vs '(380 В)' must reject (V suffix optional)."""
        prom = [
            _make_prom(1, "Тісторозкатка Fimar SI320 (380 В)", "Fimar", 50000),
        ]
        result = find_match_candidates(
            "Тісторозкатка ел. Fimar SI320 (220)", "Fimar", prom,
            supplier_price_cents=50000,
        )
        assert len(result) == 0

    def test_same_voltage_still_matches(self):
        """Same voltage on both sides must still match."""
        prom = [
            _make_prom(1, "Картоплечистка Fimar PPN10 (220 В)", "Fimar", 50000),
        ]
        result = find_match_candidates(
            "Картоплечистка Fimar PPN10 (220)", "Fimar", prom,
            supplier_price_cents=50000,
        )
        assert len(result) == 1

    def test_voltage_on_one_side_only_kept(self):
        """If only one side has voltage info, don't reject (no evidence to reject)."""
        prom = [
            _make_prom(1, "Фритюрниця Bartscher A162412E", "Bartscher", 50000),
        ]
        result = find_match_candidates(
            "Фритюрниця ел. наст. Bartscher A162412E (220)", "Bartscher", prom,
            supplier_price_cents=50000,
        )
        assert len(result) == 1

    def test_phase_1f_extracts_220_230(self):
        """'1ф' phase marker must imply 220/230 V family."""
        assert extract_voltages("Apach ATS 22 UT повний унгер 1ф") == {"220", "230"}

    def test_phase_3f_extracts_380_400(self):
        """'3ф' phase marker must imply 380/400 V family."""
        assert extract_voltages("Apach ATS 22 UT 3ф") == {"380", "400"}

    def test_phase_1f_vs_380v_rejected(self):
        """sp '1ф' must NOT match pp '380 В' — different phase variant.
        Regression from sp#5113 6th regen: pp#2985 '380 В' appeared as
        secondary candidate alongside correct pp#2974 '220 В' because
        sup_voltages was empty (no explicit '220' in sup name)."""
        prom = [
            _make_prom(
                1, "М'ясорубка Apach APACH ATS 22 UT 380 В (повний унгер)",
                "Apach", 50000,
            ),
        ]
        result = find_match_candidates(
            "М'ясорубка Apach ATS 22 UT повний унгер 1ф.", "Apach", prom,
            supplier_price_cents=50000,
        )
        assert len(result) == 0

    def test_phase_3f_vs_220v_rejected(self):
        """sp '3ф' must NOT match pp '220 В' (1-phase variant)."""
        prom = [
            _make_prom(
                1, "М'ясорубка Apach ATS12U 1/2 унгер 220 В", "Apach", 50000,
            ),
        ]
        result = find_match_candidates(
            "М'ясорубка Apach ATS 12 U 1/2 унгер 3ф.", "Apach", prom,
            supplier_price_cents=50000,
        )
        assert len(result) == 0

    def test_phase_1f_matches_220v_explicit(self):
        """sp '1ф' must match pp '220 В' (same phase family)."""
        prom = [
            _make_prom(
                1, "М'ясорубка Apach ATS12U 1/2 унгер 220 В", "Apach", 50000,
            ),
        ]
        result = find_match_candidates(
            "М'ясорубка Apach ATS 12 U 1/2 унгер 1ф.", "Apach", prom,
            supplier_price_cents=50000,
        )
        assert len(result) == 1

    def test_phase_3f_matches_380v_explicit(self):
        """sp '3ф' must match pp '380 В' (same phase family)."""
        prom = [
            _make_prom(
                1, "М'ясорубка Apach APACH ATS 22 UT 380 В (повний унгер)",
                "Apach", 50000,
            ),
        ]
        result = find_match_candidates(
            "М'ясорубка Apach ATS 22 UT повний унгер 3ф.", "Apach", prom,
            supplier_price_cents=50000,
        )
        assert len(result) == 1

    def test_phase_marker_ignored_without_context(self):
        """Isolated '1' or '3' must not trigger phase inference — the full
        'ф'/'ph' suffix is required. 'ATS 12' must not resolve to 220 V."""
        assert extract_voltages("ATS 12 U 1/2") == set()
        assert extract_voltages("APACH 300 3 секции") == set()


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


class TestExtendedVoltageGate:
    """Voltage gate recognizes '380 В' inside multi-value parens and bare form."""

    def test_voltage_inside_multi_value_parens(self):
        """'(13 кг/год, 380 В)' vs '(13 кг/год, 220 В)' must be rejected."""
        prom = [
            _make_prom(
                1,
                "Прес макаронний Fimar PF40E з ножем (13 кг/год, 220 В)",
                "Fimar",
                254500,
            ),
        ]
        result = find_match_candidates(
            "Машина для макароних виробів Fimar PF40E з ножем (13 кг/год, 380 В)",
            "Fimar", prom,
            supplier_price_cents=281600,
        )
        assert len(result) == 0

    def test_bare_voltage_without_parens(self):
        """'Fimar XYZ 380 В' vs 'Fimar XYZ 220 В' rejected."""
        prom = [
            _make_prom(1, "Прес Fimar XYZ 220 В 8 кг/год", "Fimar", 100000),
        ]
        result = find_match_candidates(
            "Прес Fimar XYZ 380 В 8 кг/год", "Fimar", prom,
            supplier_price_cents=100000,
        )
        assert len(result) == 0

    def test_canonical_voltage_set(self):
        """Only 220/230/380/400 treated as voltages — 100/500 ignored (could be dimensions)."""
        assert extract_voltages("Something (100)") == set()
        assert extract_voltages("Something (500)") == set()
        assert extract_voltages("Something (220)") == {"220"}
        assert extract_voltages("380 В") == {"380"}
        assert extract_voltages("230 В, нерж") == {"230"}

    def test_dimension_numbers_not_confused_with_voltage(self):
        """'300 мм' is NOT a voltage — no 'В' letter."""
        assert extract_voltages("диск 300 мм") == set()


class TestAfterBrandContainmentGate:
    """Subset-containment gate rejects cross-variant false positives."""

    def test_brema_abs_vs_inox_rejected(self):
        """CB184AHC ABS must not match CB184AHC INOX — material variant."""
        prom = [
            _make_prom(
                1, "Льодогенератор Brema CB184AHC INOX, корпус нерж 21 кг/добу",
                "Brema", 100800,
            ),
            _make_prom(
                2, "Льодогенератор Brema CB184AHC ABS, корпус пластик 21 кг/добу",
                "Brema", 94000,
            ),
        ]
        result = find_match_candidates(
            "Льодогенератор Brema CB184AHC ABS", "Brema", prom,
            supplier_price_cents=94000,
        )
        ids = {r["prom_product_id"] for r in result}
        assert 2 in ids
        assert 1 not in ids

    def test_cl30_bistro_vs_bistro_plus6_rejected(self):
        """CL30 Bistro must not match CL30 BISTRO+6 дисків — variant suffix."""
        prom = [
            _make_prom(1, "Овочерізка Robot Coupe CL30 BISTRO", "Robot Coupe", 120700),
            _make_prom(2, "Овочерізка Robot Coupe CL30 BISTRO+6 дисків", "Robot Coupe", 148800),
        ]
        result = find_match_candidates(
            "Овочерізка ел. Robot Coupe CL30 Bistro", "Robot Coupe", prom,
            supplier_price_cents=120700,
        )
        ids = {r["prom_product_id"] for r in result}
        assert 1 in ids
        assert 2 not in ids

    def test_star_plus_40_vs_60_rejected(self):
        """STAR PLUS 40 must not match STAR PLUS 60 — size digit differ."""
        prom = [
            _make_prom(1, "Тістоміс LP Group STAR PLUS 40 (65 л)", "LP Group", 823100),
            _make_prom(2, "Тестомес LP Group STAR PLUS 60 (80 л)", "LP Group", 848700),
        ]
        result = find_match_candidates(
            "Тістоміс LP Group STAR PLUS 40", "LP Group", prom,
            supplier_price_cents=860200,
        )
        ids = {r["prom_product_id"] for r in result}
        assert 1 in ids
        assert 2 not in ids

    def test_entry_max_8_vs_4_rejected(self):
        """Entry Max 8 must not match Entry Max 4 even when voltage tag is identical."""
        prom = [
            _make_prom(1, "Піч для піци Pizza Group Entry Max 4 (380)", "Pizza Group", 114200),
            _make_prom(2, "Піч для піци Pizza Group Entry Max 8 (380В)", "Pizza Group", 189700),
        ]
        result = find_match_candidates(
            "Піч для піци Pizza Group Entry Max 8 (380)", "Pizza Group", prom,
            supplier_price_cents=199500,
        )
        ids = {r["prom_product_id"] for r in result}
        assert 2 in ids
        assert 1 not in ids

    def test_reednee_white_vs_black_rejected(self):
        """REEDNEE RT78B white must not match REEDNEE RT78B black."""
        prom = [
            _make_prom(1, "Шафа холодильна REEDNEE RT78B white", "REEDNEE", 36400),
            _make_prom(2, "Шафа холодильна REEDNEE RT78B black", "REEDNEE", 36400),
        ]
        result = find_match_candidates(
            "Шафа-вітрина холодильна REEDNEE RT78B white", "REEDNEE", prom,
            supplier_price_cents=33500,
        )
        ids = {r["prom_product_id"] for r in result}
        assert 1 in ids
        assert 2 not in ids

    def test_supplier_with_extras_matches_base_prom(self):
        """'LP Group VIS60 + решітка + ЭПУ' should still match base PROM 'LP Group VIS60'.

        Bidirectional rule: PROM tokens are subset of SUP tokens — accessories added on
        supplier side shouldn't prevent matching to the base catalog entry.
        """
        prom = [
            _make_prom(1, "Тістоміс LP Group VIS60", "LP Group", 940500),
        ]
        result = find_match_candidates(
            "Тістоміс LP Group VIS60 + решітка з нерж. сталі + ЭПУ",
            "LP Group", prom,
            supplier_price_cents=1011300,
        )
        assert any(r["prom_product_id"] == 1 for r in result)

    def test_synonym_prefix_type_does_not_block(self):
        """'Міксер погружний' vs 'Міксер заглибний' differ before brand (type synonyms).

        Containment gate operates on after-brand remainder only, so type-word synonyms
        (погружний/заглибний/занурювальний) must not cause rejection.
        """
        prom = [
            _make_prom(
                1, "Міксер заглибний Robot Coupe CMP250 Combi", "Robot Coupe", 86400,
            ),
        ]
        result = find_match_candidates(
            "Міксер погружний Robot Coupe CMP250 Combi", "Robot Coupe", prom,
            supplier_price_cents=98100,
        )
        assert len(result) == 1

    def test_voltage_tags_ignored_by_containment(self):
        """Containment gate ignores voltage-number tokens (handled by voltage gate).

        Supplier 'Fimar GR8D (220)' should still match PROM 'Fimar GR8D' even though
        '220' is absent from the PROM side.
        """
        prom = [
            _make_prom(1, "Сиротертка Fimar GR8D", "Fimar", 45800),
        ]
        result = find_match_candidates(
            "Сиротерка Fimar GR8D (220)", "Fimar", prom,
            supplier_price_cents=45800,
        )
        assert len(result) == 1

    def test_meaningful_tokens_drops_stopwords_and_voltage(self):
        """'STAR PLUS 40 (380 В)' → {'star','plus','40'}."""
        assert meaningful_tokens("STAR PLUS 40 (380 В)") == {"star", "plus", "40"}

    def test_after_brand_remainder_handles_whitespace_brand(self):
        """'RESTO ITALIA' stored brand finds 'Restoitalia' in the name."""
        name = "Тістоміс Restoitalia SK402VTW"
        assert "SK402VTW" in after_brand_remainder(name, "RESTO ITALIA")


class TestLetterSpaceDigitModel:
    """Catalog sometimes stores model with a space ('R 301', 'E 44', 'L 22').

    The first letter + following digit token must be glued so extract_model_from_name
    returns 'r301' rather than dropping the letter and returning bare '301',
    which would fail strict equality against supplier's joined 'R301'.
    """

    def test_glues_letter_space_digit(self):
        assert extract_model_from_name(
            "Кухонний процесор Robot Coupe R 301 Ultra + 4 диски", "Robot Coupe"
        ) == "r301"

    def test_supplier_joined_matches_catalog_spaced(self):
        prom = [
            _make_prom(1, "Кухонний процесор Robot Coupe R 301 Ultra + 4 диски",
                       "Robot Coupe", price=100000),
        ]
        result = find_match_candidates(
            "Кухоний процесор Robot Coupe R301 Ultra (220) + 4 диска",
            "Robot Coupe", prom, supplier_price_cents=100000,
        )
        assert len(result) == 1
        assert result[0]["prom_product_id"] == 1

    def test_glues_two_letter_uppercase_prefix(self):
        """'IP 3500', 'XR 10' — 1-4 uppercase letters glue to following digits."""
        assert extract_model_from_name(
            "Плита AIRHOT IP 3500 настільна", "AIRHOT"
        ) == "ip3500"

    def test_does_not_glue_lowercase_word(self):
        """Lowercase prose words must NOT glue to digits ('для 10' stays split)."""
        assert extract_model_from_name(
            "Піч Sirman для 10 рівнів XYZ 99", "Sirman"
        ) == "xyz99"

    def test_mixedcase_word_not_glued(self):
        """'Sirman Sirio 2 Cromato' — 'Sirio' is mixed-case (not all-uppercase)."""
        assert extract_model_from_name(
            "Міксер Sirman Sirio 2 Cromato", "Sirman"
        ) == ""

    def test_containment_gate_sees_glued_token(self):
        """pp 'R 301 Ultra' and sp 'R301 Ultra' must produce same tokens for gate.

        With compound letter↔digit split, both forms canonicalize to the same
        segmented set {r, 301, ultra, 4, диски/диска} regardless of whether
        the source wrote the SKU glued or spaced."""
        from app.services.matcher import meaningful_tokens
        pp_tokens = meaningful_tokens("R 301 Ultra + 4 диски")
        sp_tokens = meaningful_tokens("R301 Ultra + 4 диска")
        # Both forms produce the same SKU segments after glue + boundary split.
        assert {"r", "301"} <= pp_tokens
        assert {"r", "301"} <= sp_tokens
        # The descriptor tokens align so containment succeeds regardless of
        # the verb form ("диски" vs "диска" differ but are not SKU tokens).
        assert pp_tokens - {"диски"} == sp_tokens - {"диска"}


class TestSizeFractionNotModel:
    """Size-notation fractions (1/2, I/2) must not be extracted as model codes."""

    def test_arabic_fraction_not_extracted(self):
        from app.services.matcher import extract_model_from_name
        # "1/2" is a half-size designation, not a model
        assert extract_model_from_name(
            "Гриль Salamandra MOBILE PRO 1/2 G", "Salamandra"
        ) == ""

    def test_roman_fraction_not_extracted(self):
        from app.services.matcher import extract_model_from_name
        # Supplier Roman-numeral variant of the same size
        assert extract_model_from_name(
            "SALAMANDRA MOBILE PRO I/2 G", "SALAMANDRA"
        ) == ""

    def test_supplier_roman_matches_catalog_arabic(self):
        """sp#3734 case: Roman I/2 vs Arabic 1/2 should not trigger name-model mismatch."""
        from app.services.matcher import find_match_candidates
        prom = [{
            "id": 515,
            "name": "Гриль Salamandra MOBILE PRO 1/2 G",
            "brand": "Salamandra",
            "price": 100000,
            "model": "",
            "article": "",
            "display_article": "",
        }]
        hits = find_match_candidates(
            "SALAMANDRA MOBILE PRO I/2 G",
            "SALAMANDRA",
            prom,
            supplier_price_cents=100000,
        )
        assert any(h["prom_product_id"] == 515 for h in hits), (
            "Salamandra Roman I/2 should match catalog Arabic 1/2"
        )

    def test_real_model_still_extracted(self):
        """Regression: genuine models with digits are still extracted."""
        from app.services.matcher import extract_model_from_name
        assert extract_model_from_name(
            "Піч конвекційна Unox XFT133", "Unox"
        ) == "xft133"
        assert extract_model_from_name(
            "Диск для овочерізки Robot Coupe 28054", "Robot Coupe"
        ) == "28054"


class TestContainmentCrossBrandPosition:
    """Sub-brand/family tokens may sit before the brand on one side and after
    on the other. Containment should not treat that positional asymmetry as a
    real difference."""

    def test_salamandra_before_brand_does_not_block_containment(self):
        """Real sp#3734 pattern: 'Sirman SALAMANDRA ... I/2' vs catalog
        'Salamandra SIRMAN ... 1/2' — salamandra is in both full names but
        appears after brand only on supplier side."""
        from app.services.matcher import find_match_candidates
        prom = [{
            "id": 515,
            "name": "Гриль Salamandra SIRMAN Mobile PRO 1/2 G",
            "brand": "Sirman",
            "price": 138800,
            "model": "",
            "article": "",
            "display_article": "30143502",
        }]
        hits = find_match_candidates(
            "Гриль саламандра електричний Sirman SALAMANDRA MOBILE PRO I/2 G",
            "Sirman", prom, supplier_price_cents=138800,
        )
        assert any(h["prom_product_id"] == 515 for h in hits)

    def test_sibling_size_variant_still_rejected(self):
        """1/1 G sibling of 1/2 G must still be rejected by containment — size
        digit '1' vs '2' is a legitimate variant discriminator."""
        from app.services.matcher import find_match_candidates
        prom = [{
            "id": 502,
            "name": "Гриль Salamandra SIRMAN Mobile PRO 1/1 G",
            "brand": "Sirman",
            "price": 138800,
            "model": "",
            "article": "",
            "display_article": "30142502",
        }]
        hits = find_match_candidates(
            "Гриль саламандра електричний Sirman SALAMANDRA MOBILE PRO I/2 G",
            "Sirman", prom, supplier_price_cents=138800,
        )
        assert not any(h["prom_product_id"] == 502 for h in hits), (
            "1/1 G sibling must still reject vs supplier's 1/2 G"
        )

    def test_brema_abs_vs_inox_still_rejected(self):
        """Regression: variant markers (ABS vs INOX) in after-brand must still
        discriminate even with the positional-asymmetry relaxation."""
        from app.services.matcher import find_match_candidates
        prom = [{
            "id": 1,
            "name": "Льдогенератор Brema VB150 INOX",
            "brand": "Brema",
            "price": 100000,
            "model": "", "article": "", "display_article": "",
        }]
        hits = find_match_candidates(
            "Льдогенератор Brema VB150 ABS", "Brema", prom,
            supplier_price_cents=100000,
        )
        assert not any(h["prom_product_id"] == 1 for h in hits)


class TestDigitOnlyDiscriminator:
    """Containment gate must reject asymmetric subset when the diff is a
    pure-digit token — that digit is the model discriminator.

    Real bug: sp#683 'Moretti Forni Neapolis 4' matched pp#2001
    'Moretti Forni Neapolis (без розстійки)' at 92% WRatio because
    extract_model_from_name cannot latch onto a single-digit model
    ('4' has length 1 with no letter, so it's skipped). Cross-side
    cancellation then left `{neapolis, 4}` vs `{neapolis}` and
    subset_morph accepted `{neapolis} ⊆ {neapolis, 4}`.
    """

    def test_neapolis_4_vs_base_neapolis_rejected(self):
        """sp 'Neapolis 4' must NOT match pp 'Neapolis (без розстійки)'."""
        prom = [
            _make_prom(
                1, "Піч для піци Moretti Forni Neapolis (без розстійки)",
                "Moretti Forni", 900000,
            ),
        ]
        result = find_match_candidates(
            "Піч для піци Moretti Forni Neapolis 4",
            "Moretti Forni", prom, supplier_price_cents=900000,
        )
        assert not any(r["prom_product_id"] == 1 for r in result), (
            "Single-digit model suffix '4' must discriminate from base model"
        )

    def test_base_neapolis_vs_neapolis_4_rejected(self):
        """Reverse direction: sp 'Neapolis' must NOT match pp 'Neapolis 4'."""
        prom = [
            _make_prom(
                1, "Піч для піци Moretti Forni Neapolis 4",
                "Moretti Forni", 900000,
            ),
        ]
        result = find_match_candidates(
            "Піч для піци Moretti Forni Neapolis (без розстійки)",
            "Moretti Forni", prom, supplier_price_cents=900000,
        )
        assert not any(r["prom_product_id"] == 1 for r in result)

    def test_long_catalog_description_not_treated_as_discriminator(self):
        """Regression: PROM row with a long description ('21 кг/добу') contains
        digits embedded among descriptive words — those are NOT pure digit
        extras and must NOT trigger the discriminator guard, otherwise
        identical-model rows with verbose catalog descriptions would fail."""
        prom = [
            _make_prom(
                1, "Льодогенератор Brema CB184AHC ABS, корпус пластик 21 кг/добу",
                "Brema", 94000,
            ),
        ]
        result = find_match_candidates(
            "Льодогенератор Brema CB184AHC ABS", "Brema", prom,
            supplier_price_cents=94000,
        )
        assert len(result) == 1, "Mixed digit+text extras should not reject"

    def test_descriptor_extras_still_match_base(self):
        """Regression: non-digit accessory tokens (решітка/ЭПУ) must still
        allow containment subset — only digit-only extras are gated out."""
        prom = [
            _make_prom(1, "Тістоміс LP Group VIS60", "LP Group", 940500),
        ]
        result = find_match_candidates(
            "Тістоміс LP Group VIS60 + решітка з нерж. сталі + ЭПУ",
            "LP Group", prom, supplier_price_cents=1011300,
        )
        assert any(r["prom_product_id"] == 1 for r in result)

    def test_voltage_tag_not_treated_as_discriminator(self):
        """Regression: '220' in the name is filtered by meaningful_tokens,
        so the digit-only guard must not trip on voltage-only asymmetry."""
        prom = [
            _make_prom(1, "Сиротертка Fimar GR8D", "Fimar", 45800),
        ]
        result = find_match_candidates(
            "Сиротерка Fimar GR8D (220)", "Fimar", prom,
            supplier_price_cents=45800,
        )
        assert len(result) == 1

    def test_digit_only_discriminator_helper(self):
        """Unit test: fires only when extras on a side are purely digits."""
        from app.services.matcher import _digit_only_discriminator
        # supplier extra {4} is pure-digit → discriminator
        assert _digit_only_discriminator({"neapolis", "4"}, {"neapolis"}) is True
        # prom extra {4} is pure-digit → discriminator (symmetric)
        assert _digit_only_discriminator({"neapolis"}, {"neapolis", "4"}) is True
        # prom extra mixes digits and descriptive words → not discriminator
        assert _digit_only_discriminator(
            {"cb184ahc", "abs"},
            {"cb184ahc", "abs", "корпус", "21", "кг"},
        ) is False
        # both sides have non-digit extras → not discriminator
        assert _digit_only_discriminator({"vis60", "решітка"}, {"vis60"}) is False
        # identical sets → not discriminator
        assert _digit_only_discriminator({"vis60"}, {"vis60"}) is False
        # prom extra {1, 2} pure-digit → discriminator (sibling size variant)
        assert _digit_only_discriminator({"pro"}, {"pro", "1", "2"}) is True

    def test_roman_fraction_normalized_in_meaningful_tokens(self):
        """Regression: meaningful_tokens('MOBILE PRO I/2 G') produces the same
        digit tokens as 'MOBILE PRO 1/2 G' so containment doesn't see a
        spurious {1} / {2} asymmetry between catalog Arabic and supplier Roman."""
        from app.services.matcher import meaningful_tokens
        sup = meaningful_tokens("SALAMANDRA MOBILE PRO I/2 G")
        pp = meaningful_tokens("Salamandra MOBILE PRO 1/2 G")
        # Both sides must contain the digits 1 and 2 after normalization.
        assert "1" in sup and "2" in sup
        assert "1" in pp and "2" in pp


class TestShortAlphaDiscriminator:
    """Asymmetric short alphabetic extras (RD/LD/B/F/ABS/INOX) discriminate
    SKUs just like asymmetric digits. Real bug: НП supplier's 'Asber GT-500 DD'
    was falsely matched to Horoshop's 'ASBER GT-500 RD DD' at 80% because
    containment subset rule treated {rd} as a pass-through accessory, and
    'Asber GE-500 B DD' lost its discriminating 'B' to the 1-char filter,
    becoming indistinguishable from 'Asber GE-500 DD'."""

    def test_asber_gt500_dd_does_not_match_gt500_rd_dd(self):
        """Supplier 'GT-500 DD' must NOT match catalog 'GT-500 RD DD' — 'RD'
        is a SKU variant, not an accessory. Containment subset rule must reject."""
        prom = [
            _make_prom(
                1, "Посудомийна машина ASBER GT-500 RD DD", "Asber", 150000,
            ),
        ]
        result = find_match_candidates(
            "Посудомийка фронтальна Asber GT-500 DD", "Asber", prom,
            supplier_price_cents=150000,
        )
        assert not any(r["prom_product_id"] == 1 for r in result), (
            "'GT-500 DD' ⊂ 'GT-500 RD DD' must be rejected: 'RD' is SKU discriminator"
        )

    def test_asber_gt500_rd_dd_does_not_match_gt500_dd(self):
        """Reverse direction: supplier 'GT-500 RD DD' must NOT match catalog
        'GT-500 DD' — same logic, opposite side."""
        prom = [
            _make_prom(
                1, "Посудомийна машина ASBER GT-500 DD", "Asber", 140000,
            ),
        ]
        result = find_match_candidates(
            "Посудомийка фронтальна Asber GT-500 RD DD", "Asber", prom,
            supplier_price_cents=140000,
        )
        assert not any(r["prom_product_id"] == 1 for r in result)

    def test_asber_ge500_b_dd_does_not_match_ge500_rd_dd(self):
        """'GE-500 B DD' and 'GE-500 RD DD' are distinct SKU variants — both
        have a discriminating suffix, neither is subset of the other. The
        1-char 'B' must be preserved in tokenization so this fails subset."""
        prom = [
            _make_prom(
                1, "Посудомийна машина ASBER GE-500 RD DD", "Asber", 150000,
            ),
        ]
        result = find_match_candidates(
            "Посудомийка фронтальна Asber GE-500 B DD", "Asber", prom,
            supplier_price_cents=150000,
        )
        assert not any(r["prom_product_id"] == 1 for r in result)

    def test_asber_identical_gt500_rd_dd_still_matches(self):
        """Regression: same exact variant on both sides must still match 100%."""
        prom = [
            _make_prom(
                1, "Посудомийна машина ASBER GT-500 RD DD", "Asber", 150000,
            ),
        ]
        result = find_match_candidates(
            "Посудомийка фронтальна Asber GT-500 RD DD", "Asber", prom,
            supplier_price_cents=150000,
        )
        assert len(result) == 1
        assert result[0]["prom_product_id"] == 1
        assert result[0]["score"] >= 90

    def test_descriptor_word_still_matches_base(self):
        """Regression: long descriptor on one side ('кухонний', 'запасний') must
        still match base product — short_alpha triggers only for ≤4 char tokens."""
        prom = [
            _make_prom(1, "Тістоміс LP Group VIS60", "LP Group", 940500),
        ]
        result = find_match_candidates(
            "Тістоміс LP Group VIS60 запасний кухонний",
            "LP Group", prom, supplier_price_cents=940500,
        )
        assert any(r["prom_product_id"] == 1 for r in result)

    def test_short_alpha_discriminator_helper(self):
        """Unit: fires only when one side has short-alpha extras exclusively."""
        from app.services.matcher import _short_alpha_discriminator
        # One-sided 'rd' extra → discriminator
        assert _short_alpha_discriminator({"gt500", "dd"}, {"gt500", "rd", "dd"}) is True
        # Reverse direction → discriminator
        assert _short_alpha_discriminator({"gt500", "rd", "dd"}, {"gt500", "dd"}) is True
        # Both sides have extras → not discriminator (subset_morph handles it)
        assert _short_alpha_discriminator({"x", "rd"}, {"x", "ld"}) is False
        # One side has LONG extra ('решітка' 7 chars) → descriptor, not discriminator
        assert _short_alpha_discriminator(
            {"vis60"}, {"vis60", "решітка"}
        ) is False
        # Mixed extras (short + long) on one side → descriptor
        assert _short_alpha_discriminator(
            {"cb184ahc"}, {"cb184ahc", "abs", "корпус"}
        ) is False
        # Identical sets → not discriminator
        assert _short_alpha_discriminator({"vis60"}, {"vis60"}) is False
        # Digit-only extra → not handled here (digit_only_discriminator covers it)
        assert _short_alpha_discriminator({"neapolis"}, {"neapolis", "4"}) is False

    def test_one_char_latin_letter_kept_in_tokens(self):
        """Regression: 'GE-500 B DD' must produce token 'b' so it discriminates
        from 'GE-500 DD' at containment. Pre-fix, 1-char letters were dropped."""
        from app.services.matcher import meaningful_tokens
        assert "b" in meaningful_tokens("Asber GE-500 B DD")

    def test_one_char_cyrillic_still_filtered(self):
        """Regression: Ukrainian prepositions 'з'/'в'/'і' stay filtered — only
        Latin 1-char letters are kept as potential SKU suffixes."""
        from app.services.matcher import meaningful_tokens
        tokens = meaningful_tokens("решітка з нерж сталі")
        assert "з" not in tokens
        assert "нерж" in tokens


class TestCompoundAndDashSplit:
    """Horoshop frequently writes model codes slitno ('ATS12U', 'HKN-LPD150S')
    while supplier feeds split them ('ATS 12 U', 'HKN LPD 150 S'). Without
    letter↔digit boundary split and dash split, 'Apach ATS12U 1/2 унгер' does
    not align with supplier's 'Apach ATS 12 U 1/2 унгер 1ф' in the containment
    gate — the correct match falls out of top-3 and the wrong plain 'ATS 12
    1Ф' wins 95% via token_sort on descriptor words."""

    def test_compound_split_letter_digit_letter(self):
        from app.services.matcher import _split_alnum_boundary
        # All direct letter↔digit transitions split (slitny SKUs canonicalize
        # to the same segments as the razdelny form).
        assert _split_alnum_boundary("ats12u") == ["ats", "12", "u"]
        assert _split_alnum_boundary("hknlpd150s") == ["hknlpd", "150", "s"]
        assert _split_alnum_boundary("75pe") == ["75", "pe"]
        assert _split_alnum_boundary("vis60") == ["vis", "60"]
        assert _split_alnum_boundary("eft60") == ["eft", "60"]
        # '+' is preserved by _TOKEN_STRIP_RE and breaks direct letter↔digit
        # adjacency, so "BISTRO+6" bundle marker stays whole.
        assert _split_alnum_boundary("bistro+6") == ["bistro+6"]
        # Pure letters or pure digits pass through.
        assert _split_alnum_boundary("hknfntm") == ["hknfntm"]
        assert _split_alnum_boundary("150") == ["150"]
        assert _split_alnum_boundary("abc") == ["abc"]

    def test_meaningful_tokens_splits_ats12u(self):
        from app.services.matcher import meaningful_tokens
        tokens = meaningful_tokens("Apach ATS12U 1/2 унгер 220 В")
        assert "ats" in tokens
        assert "12" in tokens
        assert "u" in tokens
        assert "унгер" in tokens
        # Voltage filtered.
        assert "220" not in tokens

    def test_meaningful_tokens_splits_dashed_sku(self):
        from app.services.matcher import meaningful_tokens
        tokens = meaningful_tokens("Hurakan HKN-FNT-M з набором дисків")
        assert "hkn" in tokens
        assert "fnt" in tokens
        assert "m" in tokens
        # 1-char Cyrillic 'з' (preposition) still filtered.
        assert "з" not in tokens

    def test_dash_split_preserves_eft_60_slash_2(self):
        """Regression: 'EFT-60/2' and 'EFT 60/2' must produce identical tokens
        now that '-' splits. Both → {eft, 60, 2}."""
        from app.services.matcher import meaningful_tokens
        a = meaningful_tokens("Apach EFT-60/2")
        b = meaningful_tokens("Apach EFT 60/2")
        assert a == b

    def test_vis60_plus_accessories_still_matches(self):
        """Regression: compound split fires on 'VIS60' → {vis, 60}, but supplier
        'VIS60 + решітка + ЭПУ' vs prom 'VIS60' must still pass containment
        because prom's tokens {vis, 60} are a subset of sup's."""
        prom = [
            _make_prom(1, "Тістоміс LP Group VIS60", "LP Group", 940500),
        ]
        result = find_match_candidates(
            "Тістоміс LP Group VIS60 + решітка + ЭПУ",
            "LP Group", prom, supplier_price_cents=940500,
        )
        assert any(r["prom_product_id"] == 1 for r in result)

    def test_ats12u_matches_razdelny_supplier(self):
        """sp 'Apach ATS 12 U 1/2 унгер 1ф' must find pp 'Apach ATS12U 1/2
        унгер 220 В' through containment after compound-split aligns the
        merged/razdelny artikul."""
        prom = [
            _make_prom(1, "М'ясорубка Apach ATS12U 1/2 унгер 220 В", "Apach", 50000),
        ]
        result = find_match_candidates(
            "М'ясорубка Apach ATS 12 U 1/2 унгер 1ф.", "Apach", prom,
            supplier_price_cents=50000,
        )
        assert any(r["prom_product_id"] == 1 for r in result)

    def test_ats_12_u_unger_does_not_match_plain_ats_12(self):
        """Core bug case: sp 'Apach ATS 12 U 1/2 унгер 1ф' must NOT match
        pp 'APACH ATS 12 1Ф' (the plain, non-unger version) — the lone 'u'
        in asymmetric extras is an SKU marker, not a prose descriptor."""
        prom = [
            _make_prom(1, "М'ясорубка APACH ATS 12 1Ф", "Apach", 50000),
        ]
        result = find_match_candidates(
            "М'ясорубка Apach ATS 12 U 1/2 унгер 1ф.", "Apach", prom,
            supplier_price_cents=50000,
        )
        assert not any(r["prom_product_id"] == 1 for r in result)

    def test_hkn_fnt_m_does_not_match_fnt_a(self):
        """sp 'Hurakan Hkn-fnt-m' must NOT match pp 'Hurakan HKN-FNT-A' —
        the 'M' vs 'A' suffix is a model variant. Pre-fix, dash-strip merged
        both to 'hknfntm' / 'hknfnta' which near_duplicate_token saw as
        morphological siblings (6/7 char common prefix)."""
        prom = [
            _make_prom(
                1, "ОВОЧЕРІЗКА HURAKAN HKN-FNT-A З НАБОРОМ ДИСКІВ",
                "Hurakan", 80000,
            ),
        ]
        result = find_match_candidates(
            "Овочерізка Hurakan Hkn-fnt-m з набором дисків NEW",
            "Hurakan", prom, supplier_price_cents=80000,
        )
        assert not any(r["prom_product_id"] == 1 for r in result)

    def test_asymmetric_sku_suffix_helper(self):
        from app.services.matcher import _asymmetric_sku_suffix
        # sup has 1-char Latin in extras, prom extras empty → True
        assert _asymmetric_sku_suffix(
            {"ats", "12", "u", "1", "2", "унгер"}, {"ats", "12"}
        ) is True
        # prom has 1-char Latin in extras, sup extras empty → True
        assert _asymmetric_sku_suffix(
            {"ats", "12"}, {"ats", "12", "u", "1", "2", "унгер"}
        ) is True
        # Both sides have extras → False (subset_morph handles it)
        assert _asymmetric_sku_suffix({"x", "u"}, {"x", "r"}) is False
        # No 1-char Latin in extras (just long Cyrillic) → False, descriptor
        assert _asymmetric_sku_suffix(
            {"vis60"}, {"vis60", "решітка", "эпу"}
        ) is False
        # No 1-char Latin (digits only) → False, handled by digit_only
        assert _asymmetric_sku_suffix(
            {"neapolis"}, {"neapolis", "4"}
        ) is False
        # Identical sets → False
        assert _asymmetric_sku_suffix({"x"}, {"x"}) is False
        # 1-char Cyrillic extra → False (rule is Latin-only; Cyrillic 1-char
        # gets filtered at tokenization anyway)
        assert _asymmetric_sku_suffix({"x"}, {"x", "з"}) is False


class TestPureLetterArticleFastPath:
    """Pure-letter manufacturer SKUs (HKN-FNT-M, HKN-LPD-S) are valid article
    codes but normalize_model strips dashes leaving no digit. The symmetric
    fast-path check accepts when the supplier article appears verbatim inside
    the prom product name — needed for sp#4698 where descriptor extras differ
    ('з набором дисків' vs 'з електронним блоком') blocking the containment
    gate, and extract_model_from_name returns '' because the SKU has no digit
    token."""

    def test_pure_letter_article_in_prom_name_matches(self):
        """sp 'Hurakan Hkn-fnt-m NEW з набором дисків' (article='HKN-FNT-M NEW')
        must match pp 'HURAKAN HKN-FNT-M NEW з електронним блоком' via
        substring of normalized article inside normalized prom name."""
        prom = [
            _make_prom(
                1, "ОВОЧЕРІЗКА HURAKAN HKN-FNT-M NEW З ЕЛЕКТРОННИМ БЛОКОМ",
                "Hurakan", 80000,
            ),
        ]
        result = find_match_candidates(
            "Овочерізка Hurakan Hkn-fnt-m NEW з набором дисків",
            "Hurakan", prom, supplier_price_cents=80000,
            supplier_article="HKN-FNT-M NEW",
        )
        assert any(r["prom_product_id"] == 1 for r in result)

    def test_pure_letter_article_does_not_match_different_suffix(self):
        """Counter-check: article 'HKN-FNT-M' must NOT match pp 'HKN-FNT-A'.
        Normalized 'hknfntm' is not a substring of normalized 'hknfnta'."""
        prom = [
            _make_prom(
                1, "ОВОЧЕРІЗКА HURAKAN HKN-FNT-A З НАБОРОМ ДИСКІВ",
                "Hurakan", 80000,
            ),
        ]
        result = find_match_candidates(
            "Овочерізка Hurakan Hkn-fnt-m з набором дисків",
            "Hurakan", prom, supplier_price_cents=80000,
            supplier_article="HKN-FNT-M",
        )
        assert not any(r["prom_product_id"] == 1 for r in result)

    def test_short_article_does_not_trigger_fast_path(self):
        """Short raw articles (<6 chars after normalize) must not trigger the
        substring check — 'CE' or 'UL' could appear in any product name."""
        prom = [
            _make_prom(1, "Pizza oven CE certified", "Apach", 80000),
            _make_prom(2, "Completely different product", "Apach", 80000),
        ]
        result = find_match_candidates(
            "Apach oven", "Apach", prom, supplier_price_cents=80000,
            supplier_article="CE",
        )
        # Neither should match via pure-letter fast-path (too short).
        fast_path_matches = [r for r in result if r.get("score") == 100.0]
        assert len(fast_path_matches) == 0

    def test_letters_only_no_dash_article_rejected(self):
        """Article without dash in raw form must not trigger the check —
        'HKNFNTMNEW' as a single alphabetic string is too weak a signal to
        bypass the containment gate (no SKU structure to anchor on)."""
        prom = [
            _make_prom(
                1, "Apach HKNFNTMNEW product with totally unrelated words",
                "Apach", 80000,
            ),
        ]
        result = find_match_candidates(
            "Apach totally unrelated product desc",
            "Apach", prom, supplier_price_cents=80000,
            supplier_article="HKNFNTMNEW",
        )
        # No dash in raw article → fast-path skipped.
        # Fuzzy + containment will reject because tokens don't overlap.
        assert not any(r["prom_product_id"] == 1 for r in result)

    def test_cyrillic_homoglyph_in_sku_normalized_to_latin(self):
        """sp#4983 article 'GXSN2ТN' (Cyrillic Т) must normalize to the same
        value as pure-Latin 'GXSN2TN' so catalog lookup matches."""
        from app.services.matcher import normalize_model
        assert normalize_model("GXSN2ТN") == normalize_model("GXSN2TN") == "gxsn2tn"
        assert normalize_model("HKN-GXSN3ТN") == normalize_model("HKN-GXSN3TN") == "hkngxsn3tn"

    def test_pure_cyrillic_not_transliterated(self):
        """Real Cyrillic words must not be transliterated — only mixed-script
        corrupted SKUs are fixed."""
        from app.services.matcher import normalize_model
        # Pure Cyrillic 'автомат' stays as Cyrillic letters (then stripped by
        # the [^a-z0-9] filter → empty).
        assert normalize_model("АВТОМАТ") == ""
        # Pure Latin unchanged.
        assert normalize_model("XFT133") == "xft133"

    def test_digit_bearing_article_does_not_bypass_voltage_gate(self):
        """sp#4529 regression: article 'ATS12U 1/2' (has digits) must NOT
        skip the voltage/phase post-gate via pure-letter fast-path. sp is
        3ф, pp is 1ф (220В) — must be rejected even though the SKU
        substring matches."""
        prom = [
            _make_prom(
                1, "М'ясорубка Apach ATS12U 1/2 унгер 220 В",
                "Apach", 50000,
            ),
        ]
        result = find_match_candidates(
            "М'ясорубка Apach ATS 12 U 1/2 унгер 3ф.",
            "Apach", prom, supplier_price_cents=50000,
            supplier_article="ATS12U 1/2",
        )
        # article has digits → pure-letter fast-path must not fire.
        # Voltage gate rejects 3ф vs 220В (which resolves to 1ф).
        assert not any(r["prom_product_id"] == 1 for r in result)


class TestDigitBearingArticleFastPath:
    """A2 gap fix (2026-04-22): when catalog pp has no explicit
    article/display_article, a full SKU embedded in pp.name must still
    be recognized as a match — even when the article contains digits.
    Common cases: HKN-20SN2V (Hurakan), AFN-1602 EXP (Fagor),
    AC800dig DD (Apach), ACB130.65B A R290 (Apach).
    """

    def test_hkn_20sn2v_digit_article_in_prom_name_matches(self):
        """sp 'Тістоміс Hurakan HKN-20SN2V на 20 л дві швидкості' (article
        'HKN-20SN2V' has digits) must match pp 'Тістоміс Hurakan HKN-20SN2V,
        20 л, 2 шв.' even though descriptor extras differ."""
        prom = [
            _make_prom(
                1, "Тістоміс Hurakan HKN-20SN2V, 20 л, 2 шв.",
                "Hurakan", 50000,
            ),
        ]
        result = find_match_candidates(
            "Тістоміс Hurakan HKN-20SN2V на 20 л дві швидкості",
            "Hurakan", prom, supplier_price_cents=50000,
            supplier_article="HKN-20SN2V",
        )
        assert any(r["prom_product_id"] == 1 for r in result)

    def test_afn_1602_exp_multiword_article_matches(self):
        """sp 'Шафа морозильна Fagor AFN-1602 EXP NEO Concept 1400 л'
        (article 'AFN-1602 EXP' has digits + space) must match
        pp 'Морозильна шафа FAGOR NEO CONCEPT AFN-1602 EXP'."""
        prom = [
            _make_prom(
                1, "Морозильна шафа FAGOR NEO CONCEPT AFN-1602 EXP (-18...-22 °C, неірж.)",
                "Fagor", 600000,
            ),
        ]
        result = find_match_candidates(
            "Шафа морозильна Fagor AFN-1602 EXP NEO Concept 1400 л",
            "Fagor", prom, supplier_price_cents=600000,
            supplier_article="AFN-1602 EXP",
        )
        assert any(r["prom_product_id"] == 1 for r in result)

    def test_ac800dig_dd_mixed_case_article_matches(self):
        """sp article 'AC800dig DD' (mixed case, digit) must match
        pp 'Посудомийна машина APACH AC800DIG DD' via case-insensitive
        boundary check."""
        prom = [
            _make_prom(1, "Посудомийна машина APACH AC800DIG DD", "Apach", 300000),
        ]
        result = find_match_candidates(
            "Посудомийка Apach AC800DIG DD купольна з дозатором",
            "Apach", prom, supplier_price_cents=300000,
            supplier_article="AC800dig DD",
        )
        assert any(r["prom_product_id"] == 1 for r in result)

    def test_acb130_punctuation_article_matches(self):
        """sp article 'ACB130.65B A R290' (has dots + digits + spaces)
        must match pp 'Льдогенератор Apach ACB130.65B A R290, 130 кг/доб'."""
        prom = [
            _make_prom(1, "Льдогенератор Apach ACB130.65B A R290, 130 кг/доб",
                       "Apach", 150000),
        ]
        result = find_match_candidates(
            "Льодогенератор Apach ACB130.65B A R290",
            "Apach", prom, supplier_price_cents=150000,
            supplier_article="ACB130.65B A R290",
        )
        assert any(r["prom_product_id"] == 1 for r in result)

    def test_prefix_collision_rejected_by_word_boundary(self):
        """sp article 'APE8AD' must NOT match pp 'Посудомийна машина Apach
        APE8ADS' — the article is a prefix of a longer SKU, word-boundary
        guard must reject."""
        prom = [
            _make_prom(1, "Посудомийна машина Apach APE8ADS на 8 кошик 450×340 мм",
                       "Apach", 250000),
        ]
        result = find_match_candidates(
            "Посудомийка Apach APE8AD",
            "Apach", prom, supplier_price_cents=250000,
            supplier_article="APE8AD",
        )
        assert not any(r["prom_product_id"] == 1 for r in result)

    def test_fast_path_skips_when_pp_has_own_article(self):
        """Catalog has explicit pp.article = 'XFT134'. sp.article='XFT133'.
        pp.name does contain 'XFT133' accidentally in a descriptor. The
        new fast-path must NOT fire because pp has its own article (would
        otherwise conflict with the model-field gate)."""
        prom = [
            _make_prom(1, "Unox XFT134 something XFT133 descriptor",
                       "Unox", 100000, article="XFT134"),
        ]
        result = find_match_candidates(
            "Unox oven XFT133",
            "Unox", prom, supplier_price_cents=100000,
            supplier_article="XFT133",
        )
        # Model-field gate rejects because pp.article != sp.article
        assert not any(r["prom_product_id"] == 1 for r in result)

    def test_fast_path_respects_voltage_gate(self):
        """sp 'HKN-INDUCTION 1ф' must not match pp 'HKN-INDUCTION 380В'
        via the new article fast-path — voltage gate still applies."""
        prom = [
            _make_prom(1, "Плита індукційна HURAKAN HKN-INDUCT-01 380 В",
                       "Hurakan", 80000),
        ]
        result = find_match_candidates(
            "Плита індукційна Hurakan HKN-INDUCT-01 1ф",
            "Hurakan", prom, supplier_price_cents=80000,
            supplier_article="HKN-INDUCT-01",
        )
        # 1ф (220/230) vs pp 380 В → voltage gate rejects
        assert not any(r["prom_product_id"] == 1 for r in result)

    def test_fast_path_does_not_fire_for_short_article(self):
        """Short article (<6 chars normalized) must not trigger — avoids
        trivial substring collisions like 'A100' in product descriptions."""
        prom = [
            _make_prom(1, "Apach A100 product with totally unrelated words",
                       "Apach", 80000),
            _make_prom(2, "Apach completely different A100 xxx",
                       "Apach", 80000),
        ]
        result = find_match_candidates(
            "Apach mixer different product",
            "Apach", prom, supplier_price_cents=80000,
            supplier_article="A100",
        )
        fast_path_matches = [r for r in result if r.get("score") == 100.0]
        assert len(fast_path_matches) == 0


class TestArticleSuffixCross:
    """SP article is a prefix of PP article separated by a dash suffix
    (or vice versa). These are DIFFERENT SKU variants — must not match.

    Real incident 2026-04-22: HKN-GXSD2GN/3GN saladetta family. SP article
    'HKN-GXSD2GN' (no suffix) matched PP name 'Саладета HURAKAN HKN-GXSD2GN-SC'
    at 100% via the digit-bearing article fast-path (SP article was a substring
    of PP name; boundary regex allowed '-' as a word boundary, so '-SC' after
    the anchor was ignored). The -SC / -GC variants are distinct products in
    the catalog — cross-matching corrupts the feed.
    """

    def test_sp_no_suffix_must_not_match_pp_with_dash_suffix(self):
        prom = [
            _make_prom(1, "Саладета HURAKAN HKN-GXSD2GN-SC", "Hurakan", 80000),
        ]
        result = find_match_candidates(
            "Саладета Hurakan HKN-GXSD2GN 2-х дверна з гранітною поверхнею",
            "Hurakan", prom, supplier_price_cents=80000,
            supplier_article="HKN-GXSD2GN",
        )
        assert not any(r["prom_product_id"] == 1 for r in result)

    def test_sp_with_dash_suffix_must_not_match_pp_without_suffix(self):
        prom = [
            _make_prom(1, "Саладетта HURAKAN HKN-GXSD2GN", "Hurakan", 80000),
        ]
        result = find_match_candidates(
            "Саладета Hurakan HKN-GXSD2GN-SC 2-х дверна",
            "Hurakan", prom, supplier_price_cents=80000,
            supplier_article="HKN-GXSD2GN-SC",
        )
        assert not any(r["prom_product_id"] == 1 for r in result)

    def test_sp_gc_must_not_match_pp_sc(self):
        prom = [
            _make_prom(1, "Саладетта HURAKAN HKN-GXSD3GN-SC", "Hurakan", 80000),
        ]
        result = find_match_candidates(
            "Саладета Hurakan HKN-GXSD3GN-GC 3-х дверна",
            "Hurakan", prom, supplier_price_cents=80000,
            supplier_article="HKN-GXSD3GN-GC",
        )
        assert not any(r["prom_product_id"] == 1 for r in result)

    def test_sp_with_suffix_still_matches_pp_same_suffix(self):
        """Positive control: exact suffix match still flows through fast-path."""
        prom = [
            _make_prom(1, "Саладета HURAKAN HKN-GXSD2GN-SC", "Hurakan", 80000),
        ]
        result = find_match_candidates(
            "Саладета Hurakan HKN-GXSD2GN-SC 2-х дверна",
            "Hurakan", prom, supplier_price_cents=80000,
            supplier_article="HKN-GXSD2GN-SC",
        )
        assert any(r["prom_product_id"] == 1 for r in result)

    def test_sp_no_suffix_matches_pp_no_suffix(self):
        """Positive control: both sides without suffix — same SKU, must match."""
        prom = [
            _make_prom(1, "Саладетта HURAKAN HKN-GXSD2GN", "Hurakan", 80000),
        ]
        result = find_match_candidates(
            "Саладета Hurakan HKN-GXSD2GN 2-х дверна з гранітною поверхнею",
            "Hurakan", prom, supplier_price_cents=80000,
            supplier_article="HKN-GXSD2GN",
        )
        assert any(r["prom_product_id"] == 1 for r in result)
