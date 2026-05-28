"""Integration tests for /products/supplier filters and sort."""

from app.models.supplier import Supplier
from app.models.supplier_product import SupplierProduct


def _seed(session):
    supplier = Supplier(
        name="S1", feed_url="http://s1.xml", discount_percent=0, is_enabled=True
    )
    session.add(supplier)
    session.flush()
    items = [
        SupplierProduct(
            supplier_id=supplier.id,
            external_id=f"E{i}",
            name=n,
            brand=b,
            price_cents=p,
            available=True,
        )
        for i, (n, b, p) in enumerate(
            [
                ("Плита Sirman X", "Sirman", 30000),
                ("Миксер Sirman Y", "Sirman", 10000),
                ("Слайсер Fimar Z", "Fimar", 50000),
                ("Печь Fimar Q", "Fimar", 20000),
            ],
            start=1,
        )
    ]
    session.add_all(items)
    session.commit()
    return supplier


def test_brand_filter_narrows_results(client, session):
    _seed(session)
    resp = client.get("/products/supplier?brand=Sirman")
    assert resp.status_code == 200
    body = resp.data.decode("utf-8")
    assert "Плита Sirman X" in body
    assert "Миксер Sirman Y" in body
    assert "Слайсер Fimar Z" not in body


def test_brand_dropdown_lists_distinct_brands(client, session):
    _seed(session)
    resp = client.get("/products/supplier")
    body = resp.data.decode("utf-8")
    # Dropdown should contain each brand once as an <option>.
    assert body.count('value="Sirman"') == 1
    assert body.count('value="Fimar"') == 1


def test_price_sort_asc(client, session):
    _seed(session)
    resp = client.get("/products/supplier?sort=price&order=asc")
    body = resp.data.decode("utf-8")
    # Cheapest (10000) must appear before most expensive (50000).
    assert body.index("Миксер Sirman Y") < body.index("Слайсер Fimar Z")


def test_price_sort_desc(client, session):
    _seed(session)
    resp = client.get("/products/supplier?sort=price&order=desc")
    body = resp.data.decode("utf-8")
    assert body.index("Слайсер Fimar Z") < body.index("Миксер Sirman Y")


def test_brand_filter_persists_in_pagination_links(client, session):
    _seed(session)
    resp = client.get("/products/supplier?brand=Sirman")
    body = resp.data.decode("utf-8")
    # Filter param should flow into filter_params used by sort_header + pagination.
    assert "brand=Sirman" in body


def test_brand_dropdown_excludes_deleted_products(client, session):
    """Brands belonging ONLY to is_deleted rows must not appear in the default
    (show_deleted=false) dropdown — otherwise selecting them returns 0 rows."""
    supplier = _seed(session)
    # Orphan brand that only appears on a deleted row.
    session.add(
        SupplierProduct(
            supplier_id=supplier.id,
            external_id="E99",
            name="Old Wega Machine",
            brand="Wega",
            price_cents=70000,
            available=True,
            is_deleted=True,
        )
    )
    session.commit()
    resp = client.get("/products/supplier")
    body = resp.data.decode("utf-8")
    assert 'value="Wega"' not in body
    # And the non-deleted brands are still there.
    assert 'value="Sirman"' in body


def test_brand_dropdown_preserves_active_filter_when_out_of_scope(client, session):
    """If the active brand is not in the scoped list (e.g. supplier changed),
    the dropdown must still render it as an option so the user sees the filter."""
    supplier_a = _seed(session)  # has Sirman + Fimar
    supplier_b = Supplier(
        name="S2", feed_url="http://s2.xml", discount_percent=0, is_enabled=True
    )
    session.add(supplier_b)
    session.flush()
    session.add(
        SupplierProduct(
            supplier_id=supplier_b.id,
            external_id="B1",
            name="Блендер OtherBrand",
            brand="OtherBrand",
            price_cents=10000,
            available=True,
        )
    )
    session.commit()
    # Ask for supplier_b's view but with brand=Sirman (out of scope).
    resp = client.get(f"/products/supplier?supplier_id={supplier_b.id}&brand=Sirman")
    body = resp.data.decode("utf-8")
    # Sirman should still be listed so user sees the applied filter.
    assert 'value="Sirman"' in body
    assert 'value="Sirman" selected' in body or 'selected>Sirman' in body


class TestForcePriceValidation:
    """POST /products/supplier/<id>/force-price — must validate before
    persisting: price_forced=True makes the value sticky (sync won't fix it),
    so a non-numeric input must 400 (not 500) and a zero/negative/foreign
    currency must be rejected before it reaches the live feed."""

    def _one(self, session):
        supplier = Supplier(
            name="FP", feed_url="http://fp.xml", discount_percent=0, is_enabled=True
        )
        session.add(supplier)
        session.flush()
        sp = SupplierProduct(
            supplier_id=supplier.id, external_id="FP1", name="Test",
            brand="B", price_cents=10000, currency="EUR", available=True,
        )
        session.add(sp)
        session.commit()
        return sp.id

    def test_valid_force_sets_price(self, client, session):
        sp_id = self._one(session)
        resp = client.post(
            f"/products/supplier/{sp_id}/force-price",
            json={"price_cents": 25000, "currency": "EUR"},
        )
        assert resp.status_code == 200, resp.get_data(as_text=True)
        session.expire_all()
        sp = session.get(SupplierProduct, sp_id)
        assert sp.price_cents == 25000
        assert sp.price_forced is True

    def test_non_numeric_price_returns_400_not_500(self, client, session):
        sp_id = self._one(session)
        resp = client.post(
            f"/products/supplier/{sp_id}/force-price",
            json={"price_cents": "abc"},
        )
        assert resp.status_code == 400
        session.expire_all()
        sp = session.get(SupplierProduct, sp_id)
        assert sp.price_cents == 10000  # untouched
        assert sp.price_forced is False

    def test_non_positive_price_rejected(self, client, session):
        sp_id = self._one(session)
        for bad in (0, -500):
            resp = client.post(
                f"/products/supplier/{sp_id}/force-price",
                json={"price_cents": bad},
            )
            assert resp.status_code == 400, f"price_cents={bad} should be rejected"
        session.expire_all()
        sp = session.get(SupplierProduct, sp_id)
        assert sp.price_forced is False

    def test_foreign_currency_rejected(self, client, session):
        sp_id = self._one(session)
        resp = client.post(
            f"/products/supplier/{sp_id}/force-price",
            json={"price_cents": 5000, "currency": "USD"},
        )
        assert resp.status_code == 400
        session.expire_all()
        sp = session.get(SupplierProduct, sp_id)
        assert sp.price_forced is False
