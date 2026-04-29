"""Tests for Step 4.91 pool-uniqueness-gated identical-model containment bypass.

Background: when supplier and catalog share an identical extracted model
code (e.g. Maresto "Unox XV393 Cheflux" vs catalog "Unox XV393 на 5 рівнів"),
the standard containment gate rejects them because neither side's after-brand
tokens are a subset of the other (sup={xv393, cheflux} vs cat={xv393, 5,
рівнів, ...}). Step 4.91 adds a fallback bypass that accepts when:

  - both sides extract the same normalized model
  - the catalog has exactly ONE PP with that brand+model (uniqueness gate)
  - neither side's asymmetric extras are entirely short-Latin alpha tokens
    (those look like SKU markers — ABS/INOX/RD — and indicate a real variant)

The uniqueness gate prevents a single supplier SP from matching all sibling
PPs in catalog families (Sirman TC-22 has 5 variants, Hendi GN1/1 has 6).
The short-Latin guard preserves the Brema VB150 ABS vs INOX rejection.
"""

from app.services.matcher import find_match_candidates


def _make_prom(id, name, brand, price=120000, model=None,
               article=None, display_article=None):
    return {
        "id": id, "name": name, "brand": brand, "price": price,
        "model": model, "article": article, "display_article": display_article,
    }


class TestStep491BypassFires:
    """Identical model + pool-unique + non-SKU extras → bypass accepts."""

    def test_unox_cheflux_matches_unique_catalog_pp(self):
        # Real Maresto-vs-catalog case: SP "Unox XV393 Cheflux" should match
        # the only catalog PP carrying XV393 ("Unox XV393 на 5 рівнів").
        # sup_extras={cheflux} — 7 chars, NOT short-Latin → guard allows.
        # cat_extras include Cyrillic descriptors → not short-Latin.
        prom = [_make_prom(1, "Шафа Unox XV393 на 5 рівнів",
                           brand="Unox", price=400000)]
        result = find_match_candidates(
            "Шафа Unox XV393 Cheflux", "Unox", prom,
            supplier_price_cents=400000,
        )
        assert any(r["prom_product_id"] == 1 for r in result)


class TestStep491ShortLatinGuardBlocksBypass:
    """Both sides' asymmetric extras are short-Latin alpha → bypass blocked."""

    def test_brema_vb150_abs_vs_inox_still_rejected(self):
        # sup_extras={abs} (3 chars, ASCII alpha) — short-Latin SKU marker.
        # cat_extras={inox} (4 chars, ASCII alpha) — short-Latin SKU marker.
        # Both look like real variant codes — bypass refused, reject preserved.
        prom = [_make_prom(1, "Льдогенератор Brema VB150 INOX",
                           brand="Brema", price=200000)]
        result = find_match_candidates(
            "Льдогенератор Brema VB150 ABS", "Brema", prom,
            supplier_price_cents=200000,
        )
        assert all(r["prom_product_id"] != 1 for r in result)


class TestStep491UniquenessGateBlocksBypass:
    """Pool has >1 PP sharing the same brand+model → bypass blocked."""

    def test_sirman_tc22_sibling_family_distinguished(self):
        # Two catalog PPs both carrying Sirman TC22 — without the uniqueness
        # gate, a single SP "Sirman TC22 з насадкою" would bypass-match BOTH
        # via identical model. With the gate, _pool_model_counts['tc22']=2,
        # bypass is blocked, neither sibling is accepted by the bypass route.
        prom = [
            _make_prom(1, "Sirman TC22 з ножем",
                       brand="Sirman", price=120000),
            _make_prom(2, "Sirman TC22 з тертушкою",
                       brand="Sirman", price=120000),
        ]
        result = find_match_candidates(
            "Sirman TC22 з насадкою", "Sirman", prom,
            supplier_price_cents=120000,
        )
        # The bypass would have accepted both. With the gate, neither is
        # accepted via this path. (If the discriminator chain finds them
        # genuinely indistinguishable, the test still passes — what matters
        # is that the bypass route doesn't unify the family.)
        bypass_pp_ids = {r["prom_product_id"] for r in result}
        # If both were accepted via bypass, that's the regression we're
        # guarding against. Assert the family is NOT collapsed.
        assert not (1 in bypass_pp_ids and 2 in bypass_pp_ids), (
            f"Pool-uniqueness gate failed: both sibling PPs in result "
            f"{bypass_pp_ids} — bypass collapsed the TC22 family."
        )


class TestStep491LetterOnlyModelNoBypass:
    """SKU is letter-only (no digits) → extract_model returns "" → no bypass."""

    def test_hendi_hkn_fnt_letter_only_distinguished(self):
        # "HKN-FNT-M" and "HKN-FNT-A" have no digit tokens after dash-glue
        # — extract_model_from_name returns "". With empty model code,
        # _sup_model_for_bypass = "" → bypass guard short-circuits.
        # The two letter-suffix variants stay distinguished.
        prom = [_make_prom(1, "Hendi HKN-FNT-A", brand="Hendi", price=50000)]
        result = find_match_candidates(
            "Hendi HKN-FNT-M", "Hendi", prom,
            supplier_price_cents=50000,
        )
        assert all(r["prom_product_id"] != 1 for r in result)


class TestStep491DifferentNormalizedModelsNoBypass:
    """Models differ after normalize_model → equality check fails, no bypass."""

    def test_xebpc08eub_vs_xebpc08euc_distinguished(self):
        # SP extract_model='xebpc08euc', PP extract_model='xebpc08eub'.
        # Different normalized strings — bypass equality check fails,
        # falls back to original silent reject behavior.
        prom = [_make_prom(1, "Шафа Unox XEBPC08EUB", brand="Unox", price=300000)]
        result = find_match_candidates(
            "Шафа Unox XEBPC08EUC", "Unox", prom,
            supplier_price_cents=300000,
        )
        assert all(r["prom_product_id"] != 1 for r in result)
