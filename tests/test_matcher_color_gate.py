"""Tests for Step 4.88 color-variant gate.

Catalog often splits the same model by color (HKN-LPD150S BLACK +
HKN-LPD150S WHITE). The gate runs after Step 4.87 and before Step 4.9.
It is symmetric and conservative: it rejects only when BOTH sides carry
color tags and the tag sets are disjoint.

Multilingual color words (uk/ru/en) collapse to canonical family tags
('black', 'white', 'silver', 'inox', ...) so 'BLACK' / 'чорна' / 'чёрный'
all compare as the same color.

Exceptions:
  - PP carries no color anywhere → pass (could be base row; Stage A
    handles the sibling-aware downgrade for that case).
  - SP carries no color → gate inert.
  - SP supplier_article appears verbatim in PP full text → bypass
    (mirrors Step 4.87 article bypass).
  - candidate has _skip_post_gates (display_article fast-match) → bypass.
"""

from app.services.matcher import _extract_colors, find_match_candidates


def _make_prom(id, name, brand="Hurakan", price=80000, model=None,
               article=None, display_article=None):
    return {
        "id": id, "name": name, "brand": brand, "price": price,
        "model": model, "article": article, "display_article": display_article,
    }


class TestExtractColors:
    """Direct sanity checks on the color extractor."""

    def test_english_uppercase_caught(self):
        assert _extract_colors("HKN-LPD150S BLACK") == {"black"}
        assert _extract_colors("HKN-LPD150S WHITE") == {"white"}

    def test_ukrainian_forms_caught(self):
        assert _extract_colors("Hurakan HKN-LPD150S, чорна") == {"black"}
        assert _extract_colors("Стіл біла поверхня") == {"white"}

    def test_russian_forms_caught(self):
        assert _extract_colors("Шкаф чёрный, нержавеющий") == {"black", "inox"}

    def test_inox_caught(self):
        assert _extract_colors("Apach AMR-10 нержавіюча сталь") == {"inox"}
        assert _extract_colors("Stainless steel grill") == {"inox"}

    def test_no_color_returns_empty(self):
        assert _extract_colors("Apach AMR-10") == set()
        assert _extract_colors("Sirman Mantegna 300") == set()

    def test_short_substrings_not_hijacked(self):
        # 'син' as part of 'синхронний' — not in our wordlist, so no false hit.
        # 'сер' as part of 'серія' — same.
        # 'ред' as part of 'reduce' — 'red' wordlist requires word boundary.
        assert _extract_colors("Reduce series synchronous") == set()
        assert _extract_colors("Серія Bistro") == set()

    def test_multiple_parts_unioned(self):
        assert _extract_colors("HKN-LPD150S", "art-bl-001", "BLACK") == {"black"}

    def test_empty_input(self):
        assert _extract_colors() == set()
        assert _extract_colors("") == set()
        assert _extract_colors("", None, "") == set()


class TestStep488ConflictRejects:
    """Color conflict rejected — sibling PP with the wrong color is filtered.

    These cases overlap with Step 4.9 (after-brand token containment),
    but Step 4.88 makes the rejection reason explicit and provides
    defense in depth: Step 4.9 may pass when meaningful_tokens strips
    a color word inside parens, while Step 4.88 still inspects raw
    full text including parens.
    """

    BLACK_PP = "Вітрина холодильна квадратна Hurakan HKN-LPD150S Black 0,9 м"
    WHITE_PP = "Вітрина холодильна квадратна Hurakan HKN-LPD150S White 0,9 м"

    def test_english_BLACK_picks_black_pp_only(self):
        prom = [
            _make_prom(1, self.BLACK_PP, price=80000),
            _make_prom(2, self.WHITE_PP, price=80000),
        ]
        result = find_match_candidates(
            "Вітрина холодильна Hurakan HKN-LPD150S BLACK 0,9 м",
            "Hurakan", prom,
            supplier_price_cents=80000,
        )
        ids = [r["prom_product_id"] for r in result]
        assert 1 in ids
        assert 2 not in ids

    def test_english_WHITE_picks_white_pp_only(self):
        prom = [
            _make_prom(1, self.BLACK_PP, price=80000),
            _make_prom(2, self.WHITE_PP, price=80000),
        ]
        result = find_match_candidates(
            "Вітрина холодильна Hurakan HKN-LPD150S WHITE 0,9 м",
            "Hurakan", prom,
            supplier_price_cents=80000,
        )
        ids = [r["prom_product_id"] for r in result]
        assert 2 in ids
        assert 1 not in ids

    def test_color_in_paren_still_rejected(self):
        # SP has color word inside parens — meaningful_tokens (used by
        # Step 4.85/4.9) STRIPS paren content, so those gates may not
        # see the color. Step 4.88 inspects raw full text, so a black/
        # white discord still rejects.
        prom = [_make_prom(
            1,
            "Вітрина Hurakan HKN-LPD150S 0,9 м (White)",
            price=80000,
        )]
        result = find_match_candidates(
            "Вітрина Hurakan HKN-LPD150S 0,9 м (Black)",
            "Hurakan", prom,
            supplier_price_cents=80000,
        )
        # Either Step 4.85 (paren disc disjoint) OR Step 4.88 catches.
        # The important property: candidate is rejected, not auto-confirmed.
        assert result == []

    def test_color_in_pp_display_article_rejects_conflict(self):
        # PP carries color only in display_article (not in name). Step 4.9
        # works on names; without Step 4.88 a SP with a different color
        # could slip past. Step 4.88 reads full text incl. display_article.
        prom = [_make_prom(
            1,
            "Вітрина холодильна Hurakan HKN-LPD150S 0,9 м",
            display_article="HKN-LPD150S BLACK",
            price=80000,
        )]
        result = find_match_candidates(
            "Вітрина холодильна Hurakan HKN-LPD150S WHITE 0,9 м",
            "Hurakan", prom,
            supplier_price_cents=80000,
        )
        assert result == []


class TestStep488NoRegression:
    """Cases that must keep passing (no PP color tag → gate inert)."""

    def test_inox_sp_vs_plain_pp_passes(self):
        # PP base row carries no color; SP adds 'нержавіюча сталь'.
        # Gate must NOT reject — PP simply doesn't tag the color.
        prom = [_make_prom(1, "М'ясорубка Apach AMR-10 з насадкою",
                           brand="Apach", price=120000)]
        result = find_match_candidates(
            "М'ясорубка Apach AMR-10 нержавіюча сталь з насадкою",
            "Apach", prom,
            supplier_price_cents=120000,
        )
        assert any(r["prom_product_id"] == 1 for r in result)

    def test_no_color_sp_vs_color_pp_passes(self):
        # SP without color, PP with Black label — gate is inert (no SP color).
        # Stage A will downgrade this when a sibling exists; Stage B alone
        # must NOT block.
        prom = [_make_prom(1,
                           "Вітрина холодильна Hurakan HKN-LPD150S Black 0,9 м",
                           price=80000)]
        result = find_match_candidates(
            "Вітрина холодильна Hurakan HKN-LPD150S 0,9 м",
            "Hurakan", prom,
            supplier_price_cents=80000,
        )
        assert any(r["prom_product_id"] == 1 for r in result)

    def test_same_color_both_sides_passes(self):
        prom = [_make_prom(1,
                           "Вітрина холодильна Hurakan HKN-LPD150S Black 0,9 м",
                           price=80000)]
        result = find_match_candidates(
            "Вітрина холодильна Hurakan HKN-LPD150S BLACK 0,9 м",
            "Hurakan", prom,
            supplier_price_cents=80000,
        )
        assert any(r["prom_product_id"] == 1 for r in result)


class TestStep488ArticleBypass:
    """SP supplier_article verbatim in PP → bypass color gate."""

    def test_supplier_article_in_pp_bypasses_color_conflict(self):
        # SP says 'чорна' but supplier_article verbatim appears in PP name —
        # strong evidence of correct row, ignore color discord.
        prom = [_make_prom(
            1,
            "Вітрина холодильна Hurakan HKN-LPD150S-BL White 0,9 м",
            price=80000,
        )]
        result = find_match_candidates(
            "Вітрина холодильна Hurakan HKN-LPD150S-BL чорна 0,9 м",
            "Hurakan", prom,
            supplier_price_cents=80000,
            supplier_article="HKN-LPD150S-BL",
        )
        assert any(r["prom_product_id"] == 1 for r in result)
