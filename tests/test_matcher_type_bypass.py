"""Tests for type-gate model-equality bypass in find_match_candidates.

The type gate (Step 4.5) rejects candidates when SP's product-type words
diverge from PP's — "Плита" vs "Шафа" is a legitimate reject. But Horoshop
uses inconsistent type words for the same SKU: "Міксер ручний" on the
supplier side and "Міксер погружний" in catalog for AFM250VV200. Those
differ enough that token_sort_ratio falls below TYPE_MATCH_THRESHOLD, so
without a bypass the real pair never becomes a candidate.

The bypass: if normalized SP model (from supplier_article / supplier_model
/ name extraction) equals normalized PP model (from article/model/display
fields or name extraction), the type mismatch is a naming quirk, not a
product mismatch — let the candidate through.
"""

from app.services.matcher import find_match_candidates


def _make_prom(id, name, brand="Apach", price=1920000, model=None,
               article=None, display_article=None):
    return {
        "id": id, "name": name, "brand": brand, "price": price,
        "model": model, "article": article, "display_article": display_article,
    }


class TestTypeGateBypassOnModelEquality:
    """Model equality overrides type-gate rejection."""

    def test_afm250vv200_matches_across_mixer_type_variants(self):
        # Real case: "Міксер ручний Apach AFM250VV200" (supplier "Новый Проект")
        # should match "Міксер погружний Apach AFM 250 VV 200" in Horoshop.
        # Both SKUs normalize to "afm250vv200".
        prom = [
            _make_prom(
                1, "Міксер погружний Apach AFM 250 VV 200",
                brand="Apach", price=1924400,
            ),
        ]
        result = find_match_candidates(
            "Міксер ручний Apach AFM250VV200", "Apach", prom,
            supplier_price_cents=1620000,   # 380 EUR ≈ 16200 UAH
            supplier_article="AFM250VV200",
        )
        assert len(result) == 1
        assert result[0]["prom_product_id"] == 1

    def test_bypass_uses_name_extracted_model_when_no_article(self):
        # SP has no explicit article but the model "afm250vv200" is extractable
        # from name. PP catalog has the same SKU with spaces. Bypass still fires.
        prom = [
            _make_prom(
                1, "Міксер погружний Apach AFM 250 VV 200",
                brand="Apach", price=1924400,
            ),
        ]
        result = find_match_candidates(
            "Міксер ручний Apach AFM250VV200", "Apach", prom,
            supplier_price_cents=1620000,
        )
        assert len(result) == 1

    def test_bypass_uses_pp_display_article_field(self):
        # PP carries the SKU in its `display_article` field (Horoshop's
        # "Артикул для відображення"). Fast-path display_article branch sets
        # _skip_post_gates=True so the candidate bypasses every subsequent gate.
        prom = [
            _make_prom(
                1, "Міксер погружний професійний",
                brand="Apach", price=1924400, display_article="AFM250VV200",
            ),
        ]
        result = find_match_candidates(
            "Міксер ручний Apach AFM250VV200", "Apach", prom,
            supplier_price_cents=1620000,
            supplier_article="AFM250VV200",
        )
        assert len(result) == 1


class TestTypeGateStillRejectsDifferentModels:
    """The bypass must not weaken the gate for genuine type mismatches."""

    def test_different_models_still_rejected(self):
        # Different SKU in pp — type gate must still reject because model
        # equality check fails. Fuzzy wouldn't pass either, but we want the
        # type gate to have the final word when model normalization diverges.
        prom = [
            _make_prom(
                1, "Блендер для молочних коктейлів Apach BX99",
                brand="Apach", price=1500000,
            ),
        ]
        result = find_match_candidates(
            "Міксер ручний Apach AFM250VV200", "Apach", prom,
            supplier_price_cents=1620000,
            supplier_article="AFM250VV200",
        )
        # BX99 != AFM250VV200 → no bypass → type gate (or earlier gates) reject.
        assert result == []

    def test_no_bypass_when_both_models_empty(self):
        # Generic SP with no model info and PP with no model info — gate
        # behaves exactly as before (type-score-only reject).
        prom = [
            _make_prom(
                1, "Шафа холодильна Apach",
                brand="Apach", price=1500000,
            ),
        ]
        result = find_match_candidates(
            "Плита Apach", "Apach", prom,
            supplier_price_cents=1500000,
        )
        # "Плита" vs "Шафа холодильна" → type gate rejects, no model to save it.
        # Also the Step 0 gate would reject this SP anyway (no discriminator).
        assert result == []
