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
