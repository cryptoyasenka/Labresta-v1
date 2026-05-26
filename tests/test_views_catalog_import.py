"""Integration tests for the two-step catalog import flow.

Upload -> preview (nothing written) -> confirm (applied) / cancel (discarded).
"""

import io

import openpyxl

from app.models.catalog import PromProduct


def _xlsx_bytes(headers, rows):
    """Build an in-memory .xlsx file with the given header row and data rows."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(headers)
    for r in rows:
        ws.append(r)
    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf


HEADERS = ["Артикул", "Назва (UA)", "Ціна", "Назва (RU)"]


def test_upload_shows_preview_without_writing(client, db):
    db.session.add(
        PromProduct(
            external_id="A1",
            name="старое имя",
            name_ru="перевод воркера",
            price=1000,
        )
    )
    db.session.commit()

    xlsx = _xlsx_bytes(HEADERS, [["A1", "новое имя", "20.0", "испорч RU"]])
    resp = client.post(
        "/catalog/import",
        data={"file": (xlsx, "horoshop-export.xlsx")},
        content_type="multipart/form-data",
    )

    assert resp.status_code == 200
    body = resp.get_data(as_text=True)
    assert "Проверка импорта" in body
    assert "horoshop-export.xlsx" in body  # filename echoed for the operator

    # DB untouched at the preview step.
    obj = db.session.query(PromProduct).filter_by(external_id="A1").one()
    assert obj.name == "старое имя"
    assert obj.price == 1000

    # Session carries a staging token.
    with client.session_transaction() as sess:
        assert "catalog_import" in sess


def test_confirm_applies_and_preserves_translation(client, db):
    db.session.add(
        PromProduct(
            external_id="A2",
            name="старое имя",
            name_ru="перевод воркера",
            price=1000,
        )
    )
    db.session.commit()

    xlsx = _xlsx_bytes(HEADERS, [["A2", "новое имя", "20.0", "испорч RU"]])
    client.post(
        "/catalog/import",
        data={"file": (xlsx, "horoshop-export.xlsx")},
        content_type="multipart/form-data",
    )

    resp = client.post("/catalog/import/confirm", follow_redirects=True)
    assert resp.status_code == 200

    obj = db.session.query(PromProduct).filter_by(external_id="A2").one()
    assert obj.name == "новое имя"  # catalog field applied
    assert obj.price == 2000
    assert obj.name_ru == "перевод воркера"  # translation preserved

    # Staging cleared after confirm.
    with client.session_transaction() as sess:
        assert "catalog_import" not in sess


def test_cancel_discards_without_writing(client, db):
    db.session.add(PromProduct(external_id="A3", name="старое имя", price=1000))
    db.session.commit()

    xlsx = _xlsx_bytes(HEADERS, [["A3", "новое имя", "20.0", ""]])
    client.post(
        "/catalog/import",
        data={"file": (xlsx, "wrong-file.xlsx")},
        content_type="multipart/form-data",
    )

    resp = client.post("/catalog/import/cancel", follow_redirects=True)
    assert resp.status_code == 200

    obj = db.session.query(PromProduct).filter_by(external_id="A3").one()
    assert obj.name == "старое имя"  # nothing applied
    assert obj.price == 1000
    with client.session_transaction() as sess:
        assert "catalog_import" not in sess


def test_confirm_without_session_redirects(client, db):
    """Confirm with no staged upload (expired session) is handled gracefully."""
    resp = client.post("/catalog/import/confirm", follow_redirects=True)
    assert resp.status_code == 200
    assert "истекла" in resp.get_data(as_text=True)
