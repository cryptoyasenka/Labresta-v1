"""Integration tests for /suppliers endpoints.

Covers /suppliers/<id>/apply-discount (dry-run preview + real apply, force flag,
skip-existing behavior, supplier not found).
"""

from datetime import datetime, timezone

from app.models.catalog import PromProduct
from app.models.product_match import ProductMatch
from app.models.supplier import Supplier
from app.models.supplier_product import SupplierProduct


def _seed_supplier_with_matches(session, n_conf=3, eur_rate=51.15):
    """Create a supplier + n_conf confirmed matches at varying retail prices.

    Prices are chosen so `calculate_auto_discount` yields 3 distinct buckets:
    19% (high), mid (margin-capped), 0% (too cheap).
    """
    supplier = Supplier(
        name="MARESTO-test",
        feed_url="http://test.xml",
        discount_percent=0,
        eur_rate_uah=eur_rate,
        is_enabled=True,
    )
    session.add(supplier)
    session.flush()

    # 3 products with retail prices hitting different bands of calculate_auto_discount.
    # At eur_rate=51.15 and min_margin=500:
    #   retail >= 162.9 EUR → 19%
    #   39.1 <= retail < 162.9 → margin-capped integer
    #   retail < 39.1 EUR → 0%
    prices_eur = [200.0, 60.0, 20.0]
    matches = []
    for i, p_eur in enumerate(prices_eur):
        sp = SupplierProduct(
            supplier_id=supplier.id,
            external_id=f"SP{i}",
            name=f"Product {i}",
            brand="Brand",
            price_cents=int(p_eur * 100),
            available=True,
        )
        session.add(sp)
        pp = PromProduct(
            external_id=f"PROM{i}",
            name=f"Product {i}",
            brand="Brand",
            price=int(p_eur * 100),
        )
        session.add(pp)
        session.flush()
        match = ProductMatch(
            supplier_product_id=sp.id,
            prom_product_id=pp.id,
            score=95.0,
            status="confirmed",
            discount_percent=None,
            confirmed_at=datetime.now(timezone.utc),
            confirmed_by="seed",
        )
        session.add(match)
        matches.append(match)
    session.commit()
    return supplier, matches


class TestApplyDiscountEndpoint:
    def test_dry_run_returns_distribution_without_writing(self, client, db):
        supplier, matches = _seed_supplier_with_matches(db.session)
        resp = client.post(f"/suppliers/{supplier.id}/apply-discount?dry_run=1")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["status"] == "ok"
        assert data["dry_run"] is True
        assert data["scanned"] == 3
        assert data["changed"] == 3  # all NULL → all change
        # DB still has NULLs
        for m in matches:
            db.session.refresh(m)
            assert m.discount_percent is None

    def test_real_apply_fills_nulls(self, client, db):
        supplier, matches = _seed_supplier_with_matches(db.session)
        resp = client.post(f"/suppliers/{supplier.id}/apply-discount")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["changed"] == 3
        # high-price match gets 19, low-price gets 0
        for m in matches:
            db.session.refresh(m)
            assert m.discount_percent is not None
        prices = sorted(matches, key=lambda m: m.supplier_product.price_cents)
        assert prices[0].discount_percent == 0.0   # 20 EUR → cap at retail
        assert prices[-1].discount_percent == 19.0  # 200 EUR → full target

    def test_apply_preserves_existing_discount_without_force(self, client, db):
        supplier, matches = _seed_supplier_with_matches(db.session)
        # Manually set override on one match
        matches[0].discount_percent = 5.0
        db.session.commit()

        resp = client.post(f"/suppliers/{supplier.id}/apply-discount")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["scanned"] == 2  # the 5%-override one is excluded
        assert data["changed"] == 2

        db.session.refresh(matches[0])
        assert matches[0].discount_percent == 5.0  # override preserved

    def test_apply_with_force_overwrites_existing(self, client, db):
        supplier, matches = _seed_supplier_with_matches(db.session)
        matches[0].discount_percent = 5.0  # override on highest-priced match
        db.session.commit()

        resp = client.post(f"/suppliers/{supplier.id}/apply-discount?force=1")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["force"] is True
        assert data["scanned"] == 3

        db.session.refresh(matches[0])
        # 200 EUR retail → auto = 19%, override overwritten
        assert matches[0].discount_percent == 19.0

    def test_supplier_not_found_returns_404(self, client, db):
        resp = client.post("/suppliers/99999/apply-discount")
        assert resp.status_code == 404
        assert resp.get_json()["status"] == "error"

    def test_ignores_non_confirmed_matches(self, client, db):
        supplier, matches = _seed_supplier_with_matches(db.session)
        matches[0].status = "candidate"
        db.session.commit()

        resp = client.post(f"/suppliers/{supplier.id}/apply-discount?dry_run=1")
        data = resp.get_json()
        assert data["scanned"] == 2  # candidate excluded
