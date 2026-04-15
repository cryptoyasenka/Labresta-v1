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
