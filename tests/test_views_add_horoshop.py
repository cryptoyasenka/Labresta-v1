"""Endpoint tests for the Horoshop create-file UI (/feeds/add).

Verifies the wiring the builder's pure tests can't: the supplier+brand picker,
the upload→temp→build→download path, exclusion of matched products, the
fallback category when no export is uploaded, and login_required on both routes.
Seeds one supplier with unmatched SupplierProducts (no ProductMatch) plus one
matched SP (confirmed) that must be excluded.
"""

import io

import openpyxl

from app.models.catalog import PromProduct
from app.models.product_match import ProductMatch
from app.models.supplier import Supplier
from app.models.supplier_product import SupplierProduct
from app.services.add_horoshop_file import (
    HEADERS, H_ARTICLE, H_CATEGORY, H_VISIBLE,
)
from app.services.category_resolver import DEFAULT_FALLBACK_CATEGORY


def _export_bytes():
    """Tiny Horoshop-export xlsx (header + 2 data rows) for the upload field."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Worksheet"
    ws.append(["Артикул", "Название (UA)", "Бренд", "Раздел"])
    ws.append(["EX-1", "Існуюча картка", "HURAKAN", "Холодильне обладнання"])
    ws.append(["EX-2", "Інша картка", "APACH", "Печі"])
    buf = io.BytesIO()
    wb.save(buf)
    wb.close()
    return buf.getvalue()


def _seed(session):
    """One supplier: 2 unmatched SPs (HURAKAN, APACH) + 1 matched SP (excluded)."""
    supplier = Supplier(
        name="Тест Постачальник", slug="test-supplier",
        discount_percent=15.0, pricing_mode="flat", is_enabled=True,
    )
    session.add(supplier)
    session.flush()

    sp_unmatched = SupplierProduct(
        supplier_id=supplier.id, external_id="ext-u1",
        name="Льодогенератор HKN", brand="HURAKAN", article="ART-UNMATCHED",
        price_cents=84500, currency="EUR", available=True, needs_review=False,
    )
    sp_other_brand = SupplierProduct(
        supplier_id=supplier.id, external_id="ext-u2",
        name="Піч APACH", brand="APACH", article="ART-APACH",
        price_cents=50000, currency="EUR", available=True, needs_review=False,
    )
    sp_matched = SupplierProduct(
        supplier_id=supplier.id, external_id="ext-m1",
        name="Матчений товар", brand="HURAKAN", article="ART-MATCHED",
        price_cents=60000, currency="EUR", available=True, needs_review=False,
    )
    session.add_all([sp_unmatched, sp_other_brand, sp_matched])
    session.flush()

    pp = PromProduct(
        external_id="999900", name="Картка", name_ru="Карточка",
        brand="HURAKAN", price=60000,
        page_url="https://labresta.com.ua/999900/",
    )
    session.add(pp)
    session.flush()

    match = ProductMatch(
        supplier_product_id=sp_matched.id, prom_product_id=pp.id,
        score=100.0, status="confirmed", published=True, confirmed_by="test",
    )
    session.add(match)
    session.commit()
    return supplier, sp_unmatched, sp_other_brand, sp_matched


def _load_rows(resp):
    wb = openpyxl.load_workbook(
        io.BytesIO(resp.get_data()), read_only=True, data_only=True
    )
    ws = wb["Worksheet"]
    rows = list(ws.iter_rows(values_only=True))
    wb.close()
    return rows


def test_add_page_renders_supplier_picker(client, session):
    _seed(session)
    resp = client.get("/feeds/add")
    assert resp.status_code == 200
    body = resp.get_data(as_text=True)
    assert "Тест Постачальник" in body
    assert "Додати товари без матчу" in body


def test_add_page_lists_unmatched_brands(client, session):
    supplier, *_ = _seed(session)
    resp = client.get(f"/feeds/add?supplier_id={supplier.id}")
    assert resp.status_code == 200
    body = resp.get_data(as_text=True)
    # Brands of unmatched SPs appear.
    assert "HURAKAN" in body
    assert "APACH" in body
    # HURAKAN has exactly one UNMATCHED SP (the matched HURAKAN SP must not
    # inflate the badge to 2).
    assert ">2<" not in body.split("HURAKAN")[1].split("</li>")[0]


def test_generate_downloads_native_xlsx_with_category(client, session):
    supplier, *_ = _seed(session)
    resp = client.post(
        "/feeds/add/generate",
        data={
            "supplier_id": str(supplier.id),
            "brands": ["HURAKAN"],
            "export": (io.BytesIO(_export_bytes()), "export.xlsx"),
        },
        content_type="multipart/form-data",
    )
    assert resp.status_code == 200
    assert "spreadsheetml" in resp.headers["Content-Type"]

    rows = _load_rows(resp)
    assert list(rows[0]) == HEADERS
    assert len(rows) == 2  # header + one HURAKAN unmatched product
    data = dict(zip(HEADERS, rows[1]))
    assert data[H_ARTICLE] == "ART-UNMATCHED"        # supplier article, not a pp id
    assert data[H_CATEGORY]                           # non-empty Раздел
    assert data[H_VISIBLE] == "1"


def test_generate_excludes_matched_products(client, session):
    supplier, *_ = _seed(session)
    resp = client.post(
        "/feeds/add/generate",
        data={"supplier_id": str(supplier.id)},  # no brands = all unmatched
        content_type="multipart/form-data",
    )
    assert resp.status_code == 200
    rows = _load_rows(resp)
    articles = {dict(zip(HEADERS, r)).get(H_ARTICLE) for r in rows[1:]}
    assert "ART-MATCHED" not in articles
    assert "ART-UNMATCHED" in articles
    assert "ART-APACH" in articles


def test_generate_without_export_uses_fallback(client, session):
    supplier, *_ = _seed(session)
    resp = client.post(
        "/feeds/add/generate",
        data={"supplier_id": str(supplier.id), "brands": ["HURAKAN"]},
        content_type="multipart/form-data",
    )
    assert resp.status_code == 200
    rows = _load_rows(resp)
    assert len(rows) >= 2
    for r in rows[1:]:
        assert dict(zip(HEADERS, r))[H_CATEGORY] == DEFAULT_FALLBACK_CATEGORY


def test_generate_unknown_supplier_redirects(client, session):
    _seed(session)
    resp = client.post(
        "/feeds/add/generate",
        data={"supplier_id": "999999"},
        content_type="multipart/form-data",
    )
    assert resp.status_code in (302, 303)


def test_routes_login_required(client, session):
    # The shared `client` fixture is authenticated; build a bare client.
    with client.application.test_client() as anon:
        get_resp = anon.get("/feeds/add", follow_redirects=False)
        assert get_resp.status_code in (301, 302)
        post_resp = anon.post(
            "/feeds/add/generate", data={"supplier_id": "1"},
            follow_redirects=False,
        )
        assert post_resp.status_code in (301, 302)
