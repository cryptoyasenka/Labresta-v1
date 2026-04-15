"""Regression tests for scripts/bulk_auto_confirm.py classify_single.

Protects the invariant "100% fuzzy score is NOT bulletproof — only identical
meaningful tokens (after brand strip) are safe to auto-confirm" (CLAUDE.md #3).

Origin: 2026-04-11 MARESTO re-import produced 576 matches at score=100, but
sampling found misfires like "Sirman Sirio 2 Cromato" vs "Sirman Sirio 2 CC 900".
bulk_auto_confirm must reject such pairs even when fuzzy would score 100.
"""

from app.extensions import db
from app.models.catalog import PromProduct
from app.models.product_match import ProductMatch
from app.models.supplier import Supplier
from app.models.supplier_product import SupplierProduct
from scripts.bulk_auto_confirm import classify_single


def _pair(db_session, sp_name, pp_name, sp_brand="Sirman", pp_brand="Sirman",
          sp_price=10000, pp_price=10000):
    supplier = Supplier(name="T", feed_url="http://t.xml")
    db_session.add(supplier)
    db_session.flush()

    sp = SupplierProduct(
        supplier_id=supplier.id, external_id=f"SP-{sp_name[:8]}",
        name=sp_name, brand=sp_brand, price_cents=sp_price, available=True,
    )
    pp = PromProduct(
        external_id=f"PP-{pp_name[:8]}", name=pp_name, brand=pp_brand,
        price=pp_price,
    )
    db_session.add_all([sp, pp])
    db_session.flush()

    match = ProductMatch(
        supplier_product_id=sp.id, prom_product_id=pp.id,
        score=100.0, status="candidate",
    )
    db_session.add(match)
    db_session.flush()
    return match


class TestClassifySingleIdentityRule:
    """R1 (tokens-equal) is the ONLY safe bulk-confirm rule."""

    def test_identical_meaningful_tokens_returns_r1(self, app, db):
        with app.app_context():
            m = _pair(db.session, "Sirman Sirio 2 Cromato", "Sirman Sirio 2 Cromato")
            assert classify_single(m) == "R1:tokens-equal"
            db.session.rollback()

    def test_sirio_2_cromato_vs_sirio_2_cc_900_rejected(self, app, db):
        """The exact historical misfire from 2026-04-11 MARESTO import."""
        with app.app_context():
            m = _pair(db.session, "Sirman Sirio 2 Cromato", "Sirman Sirio 2 CC 900")
            assert classify_single(m) is None
            db.session.rollback()

    def test_zippy_2_vs_faby_cream_2_rejected(self, app, db):
        """Second historical misfire — both had score=100 via fuzzy."""
        with app.app_context():
            m = _pair(db.session, "CAB ZIPPY 2", "CAB Faby Cream 2", sp_brand="CAB", pp_brand="CAB")
            assert classify_single(m) is None
            db.session.rollback()

    def test_different_brand_rejected_even_if_tokens_equal(self, app, db):
        with app.app_context():
            m = _pair(db.session, "Sirman Sirio 2", "Sirio 2",
                      sp_brand="Sirman", pp_brand="OtherBrand")
            assert classify_single(m) is None
            db.session.rollback()

    def test_empty_supplier_brand_rejected(self, app, db):
        """Cross-brand guard — empty brand never bulk-confirmed."""
        with app.app_context():
            m = _pair(db.session, "Sirio 2", "Sirman Sirio 2",
                      sp_brand="", pp_brand="Sirman")
            assert classify_single(m) is None
            db.session.rollback()

    def test_extra_token_on_pp_side_rejected(self, app, db):
        """Supplier has subset of catalog tokens — R1 requires EQUALITY, not subset."""
        with app.app_context():
            m = _pair(db.session, "Sirman Sirio 2", "Sirman Sirio 2 Cromato",
                      sp_price=10000, pp_price=50000)  # price band would also fail R2
            assert classify_single(m) is None
            db.session.rollback()
