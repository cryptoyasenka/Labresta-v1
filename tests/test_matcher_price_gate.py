"""Tests for price plausibility gate in fuzzy matcher."""

from app.services.matcher import find_match_candidates, MAX_PRICE_RATIO


def _make_prom(id, name, brand="TestBrand", price=10000):
    return {"id": id, "name": name, "brand": brand, "price": price}


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
