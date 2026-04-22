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


class TestPricingModeForm:
    def test_add_per_brand_supplier_persists_rates(self, client, db):
        resp = client.post(
            "/suppliers/add",
            data={
                "name": "Новый Проект",
                "feed_url": "",
                "discount_percent": "17",
                "pricing_mode": "per_brand",
                "brand_name[]": ["HURAKAN", "SIRMAN", "ROBOT COUPE"],
                "brand_discount[]": ["15", "20", "20"],
            },
            follow_redirects=False,
        )
        assert resp.status_code == 302
        sup = db.session.execute(
            _select_supplier_by_name("Новый Проект")
        ).scalar_one()
        assert sup.pricing_mode == "per_brand"
        assert sup.discount_percent == 17.0
        rows = {(r.brand, r.discount_percent) for r in sup.brand_discounts}
        assert rows == {("HURAKAN", 15.0), ("SIRMAN", 20.0), ("ROBOT COUPE", 20.0)}

    def test_edit_replaces_brand_rates(self, client, db):
        sup = Supplier(name="Edit-me", discount_percent=10.0, pricing_mode="flat")
        db.session.add(sup)
        db.session.commit()

        # switch to per_brand with two rows
        resp = client.post(
            f"/suppliers/{sup.id}/edit",
            data={
                "name": "Edit-me",
                "feed_url": "",
                "discount_percent": "17",
                "pricing_mode": "per_brand",
                "brand_name[]": ["HURAKAN", "BARTSCHER"],
                "brand_discount[]": ["15", "20"],
            },
            follow_redirects=False,
        )
        assert resp.status_code == 302
        db.session.refresh(sup)
        assert sup.pricing_mode == "per_brand"
        assert len(sup.brand_discounts) == 2

        # re-edit, drop BARTSCHER, add CEADO
        resp = client.post(
            f"/suppliers/{sup.id}/edit",
            data={
                "name": "Edit-me",
                "feed_url": "",
                "discount_percent": "17",
                "pricing_mode": "per_brand",
                "brand_name[]": ["HURAKAN", "CEADO"],
                "brand_discount[]": ["15", "20"],
            },
            follow_redirects=False,
        )
        assert resp.status_code == 302
        db.session.refresh(sup)
        brands = {r.brand for r in sup.brand_discounts}
        assert brands == {"HURAKAN", "CEADO"}

    def test_edit_updates_same_brand_new_rate(self, client, db):
        """Replace HURAKAN=15% with HURAKAN=14% in one request.

        Exercises DELETE + INSERT on the same unique key (supplier_id, brand)
        within a single transaction — SQLAlchemy must order DELETE before
        INSERT at flush time for the UNIQUE constraint not to trip.
        """
        sup = Supplier(name="S", discount_percent=10.0, pricing_mode="per_brand")
        db.session.add(sup)
        db.session.flush()
        from app.models.supplier_brand_discount import SupplierBrandDiscount
        db.session.add(
            SupplierBrandDiscount(supplier_id=sup.id, brand="HURAKAN", discount_percent=15.0)
        )
        db.session.commit()

        resp = client.post(
            f"/suppliers/{sup.id}/edit",
            data={
                "name": "S",
                "feed_url": "",
                "discount_percent": "10",
                "pricing_mode": "per_brand",
                "brand_name[]": ["HURAKAN"],
                "brand_discount[]": ["14"],
            },
            follow_redirects=False,
        )
        assert resp.status_code == 302
        db.session.refresh(sup)
        assert len(sup.brand_discounts) == 1
        assert sup.brand_discounts[0].brand == "HURAKAN"
        assert sup.brand_discounts[0].discount_percent == 14.0

    def test_edit_blank_rows_are_ignored(self, client, db):
        sup = Supplier(name="S", discount_percent=10.0, pricing_mode="flat")
        db.session.add(sup)
        db.session.commit()

        resp = client.post(
            f"/suppliers/{sup.id}/edit",
            data={
                "name": "S",
                "feed_url": "",
                "discount_percent": "17",
                "pricing_mode": "per_brand",
                "brand_name[]": ["HURAKAN", "", "  "],
                "brand_discount[]": ["15", "", ""],
            },
            follow_redirects=False,
        )
        assert resp.status_code == 302
        db.session.refresh(sup)
        assert len(sup.brand_discounts) == 1

    def test_edit_rejects_invalid_discount(self, client, db):
        sup = Supplier(name="S", discount_percent=10.0, pricing_mode="flat")
        db.session.add(sup)
        db.session.commit()

        resp = client.post(
            f"/suppliers/{sup.id}/edit",
            data={
                "name": "S",
                "feed_url": "",
                "discount_percent": "17",
                "pricing_mode": "per_brand",
                "brand_name[]": ["HURAKAN"],
                "brand_discount[]": ["150"],  # out of range
            },
            follow_redirects=False,
        )
        assert resp.status_code == 200  # rendered with error
        db.session.refresh(sup)
        assert sup.pricing_mode == "flat"  # not updated
        assert sup.brand_discounts == []

    def test_edit_switch_to_flat_preserves_brand_rows(self, client, db):
        """Flipping away from per_brand shouldn't delete rates — they can be
        re-activated by switching back later.
        """
        sup = Supplier(name="S", discount_percent=10.0, pricing_mode="per_brand")
        db.session.add(sup)
        db.session.flush()
        from app.models.supplier_brand_discount import SupplierBrandDiscount
        db.session.add(
            SupplierBrandDiscount(supplier_id=sup.id, brand="HURAKAN", discount_percent=15.0)
        )
        db.session.commit()

        resp = client.post(
            f"/suppliers/{sup.id}/edit",
            data={
                "name": "S",
                "feed_url": "",
                "discount_percent": "10",
                "pricing_mode": "flat",
            },
            follow_redirects=False,
        )
        assert resp.status_code == 302
        db.session.refresh(sup)
        assert sup.pricing_mode == "flat"
        assert len(sup.brand_discounts) == 1  # preserved

    def test_form_renders_pricing_mode_selector(self, client, db):
        sup = Supplier(name="S", discount_percent=10.0, pricing_mode="per_brand")
        db.session.add(sup)
        db.session.commit()

        resp = client.get(f"/suppliers/{sup.id}/edit")
        assert resp.status_code == 200
        html = resp.get_data(as_text=True)
        assert 'name="pricing_mode"' in html
        assert 'value="per_brand"' in html
        assert 'По брендам' in html


def _select_supplier_by_name(name):
    from sqlalchemy import select
    return select(Supplier).where(Supplier.name == name)
