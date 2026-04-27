"""Integration tests for /suppliers endpoints."""

from app.models.supplier import Supplier
from app.models.supplier_brand_discount import SupplierBrandDiscount


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

    def test_form_renders_margin_fields_with_current_values(self, client, db):
        sup = Supplier(
            name="S",
            discount_percent=10.0,
            pricing_mode="flat",
            eur_rate_uah=52.5,
            min_margin_uah=700.0,
            cost_rate=0.8,
        )
        db.session.add(sup)
        db.session.commit()

        resp = client.get(f"/suppliers/{sup.id}/edit")
        assert resp.status_code == 200
        html = resp.get_data(as_text=True)
        assert 'name="eur_rate_uah"' in html
        assert 'name="min_margin_uah"' in html
        assert 'name="cost_rate"' in html
        assert 'value="52.5"' in html
        assert 'value="700.0"' in html
        assert 'value="0.8"' in html

    def test_add_persists_margin_fields(self, client, db):
        resp = client.post(
            "/suppliers/add",
            data={
                "name": "NewSup",
                "feed_url": "",
                "discount_percent": "10",
                "pricing_mode": "flat",
                "eur_rate_uah": "53.0",
                "min_margin_uah": "600",
                "cost_rate": "0.7",
            },
            follow_redirects=False,
        )
        assert resp.status_code == 302
        sup = db.session.execute(_select_supplier_by_name("NewSup")).scalar_one()
        assert sup.eur_rate_uah == 53.0
        assert sup.min_margin_uah == 600.0
        assert sup.cost_rate == 0.7

    def test_add_uses_defaults_when_margin_fields_omitted(self, client, db):
        resp = client.post(
            "/suppliers/add",
            data={
                "name": "DefaultSup",
                "feed_url": "",
                "discount_percent": "10",
                "pricing_mode": "flat",
            },
            follow_redirects=False,
        )
        assert resp.status_code == 302
        sup = db.session.execute(_select_supplier_by_name("DefaultSup")).scalar_one()
        assert sup.eur_rate_uah == 51.15
        assert sup.min_margin_uah == 500.0
        assert sup.cost_rate == 0.75

    def test_edit_updates_margin_fields(self, client, db):
        sup = Supplier(
            name="S",
            discount_percent=10.0,
            pricing_mode="flat",
            min_margin_uah=500.0,
            cost_rate=0.75,
        )
        db.session.add(sup)
        db.session.commit()

        resp = client.post(
            f"/suppliers/{sup.id}/edit",
            data={
                "name": "S",
                "feed_url": "",
                "discount_percent": "10",
                "pricing_mode": "flat",
                "eur_rate_uah": "52.0",
                "min_margin_uah": "800",
                "cost_rate": "0.7",
            },
            follow_redirects=False,
        )
        assert resp.status_code == 302
        db.session.refresh(sup)
        assert sup.eur_rate_uah == 52.0
        assert sup.min_margin_uah == 800.0
        assert sup.cost_rate == 0.7

    def test_edit_rejects_invalid_cost_rate(self, client, db):
        sup = Supplier(name="S", discount_percent=10.0, pricing_mode="flat")
        db.session.add(sup)
        db.session.commit()

        resp = client.post(
            f"/suppliers/{sup.id}/edit",
            data={
                "name": "S",
                "feed_url": "",
                "discount_percent": "10",
                "pricing_mode": "flat",
                "cost_rate": "1.5",
            },
            follow_redirects=False,
        )
        assert resp.status_code == 200  # rendered with error, no redirect
        html = resp.get_data(as_text=True)
        assert "Доля закупки" in html

    def test_edit_rejects_negative_min_margin(self, client, db):
        sup = Supplier(name="S", discount_percent=10.0, pricing_mode="flat")
        db.session.add(sup)
        db.session.commit()

        resp = client.post(
            f"/suppliers/{sup.id}/edit",
            data={
                "name": "S",
                "feed_url": "",
                "discount_percent": "10",
                "pricing_mode": "flat",
                "min_margin_uah": "-100",
            },
            follow_redirects=False,
        )
        assert resp.status_code == 200
        html = resp.get_data(as_text=True)
        assert "Мин. маржа" in html


def _select_supplier_by_name(name):
    from sqlalchemy import select
    return select(Supplier).where(Supplier.name == name)
