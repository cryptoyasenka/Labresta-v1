"""Tests for np_parser — НП native [КАТАЛОГ] content feed."""

import json

import openpyxl
import pytest

from app.models.supplier import Supplier
from app.models.supplier_product import SupplierProduct
from app.services.np_parser import (
    _split_gallery,
    _strip_country_suffix,
    enrich_sp_bodies,
    parse_np_feed,
)

SUPPLIER_ID = 2

# 24 native Horoshop headers, verbatim from np-feed.xlsx (2026-05-18).
HEADERS = [
    "id", "Артикул", "[КАТАЛОГ] Цена", "[КАТАЛОГ] Фото", "[КАТАЛОГ] Наличие",
    "[КАТАЛОГ] Отображать", "title_uk", "description_uk", "categories_uk",
    "attr_brend_uk", "attr_contry_uk", "attr_dimensions_uk", "attr_power_uk",
    "attr_voltage_uk", "attr_weight_uk", "title_ru", "description_ru",
    "categories_ru", "attr_brend_ru", "attr_contry_ru", "attr_dimensions_ru",
    "attr_power_ru", "attr_voltage_ru", "attr_weight_ru",
]


def _row(article, title_uk, desc_uk, brand, title_ru, desc_ru, photo):
    r = [""] * 24
    r[1] = article
    r[3] = photo
    r[6] = title_uk
    r[7] = desc_uk
    r[9] = brand
    r[15] = title_ru
    r[16] = desc_ru
    return r


def _make_np_xlsx(path, data_rows):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Worksheet"
    ws.append(HEADERS)
    for r in data_rows:
        ws.append(r)
    wb.save(path)
    wb.close()


# ===========================================================================
# Unit helpers
# ===========================================================================

class TestHelpers:
    def test_strip_country_suffix(self):
        assert _strip_country_suffix("HURAKAN (Китай)") == "HURAKAN"
        assert _strip_country_suffix("APACH") == "APACH"

    def test_split_gallery_basic(self):
        assert _split_gallery("a.jpg;b.jpg") == ["a.jpg", "b.jpg"]

    def test_split_gallery_dedup_and_trim(self):
        assert _split_gallery(" a.jpg ; a.jpg ;b.jpg; ") == ["a.jpg", "b.jpg"]

    def test_split_gallery_empty(self):
        assert _split_gallery("") == []
        assert _split_gallery(None) == []


# ===========================================================================
# parse_np_feed
# ===========================================================================

class TestParseNpFeed:
    def test_extracts_all_content_fields(self, tmp_path):
        p = tmp_path / "np.xlsx"
        _make_np_xlsx(p, [
            _row("HKN-IMC25", "Льодогенератор UA", "Тіло UA<br>рядок",
                 "HURAKAN", "Ледогенератор RU", "Тело RU<br>строка",
                 "https://np/a.jpeg;https://np/b.jpeg"),
        ])
        rows, errors = parse_np_feed(str(p), SUPPLIER_ID)
        assert errors == []
        assert len(rows) == 1
        r = rows[0]
        assert r["supplier_id"] == SUPPLIER_ID
        assert r["article"] == "HKN-IMC25"
        assert r["brand"] == "HURAKAN"
        assert r["name"] == "Льодогенератор UA"
        assert r["name_ru"] == "Ледогенератор RU"
        assert r["description"] == "Тіло UA<br>рядок"
        assert r["description_ru"] == "Тело RU<br>строка"
        assert r["image_url"] == "https://np/a.jpeg"
        assert json.loads(r["images"]) == ["https://np/a.jpeg", "https://np/b.jpeg"]

    def test_country_suffix_stripped_from_brand(self, tmp_path):
        p = tmp_path / "np.xlsx"
        _make_np_xlsx(p, [
            _row("X1", "u", "d", "FAGOR (Іспанія)", "r", "dr", "x.jpg"),
        ])
        rows, _ = parse_np_feed(str(p), SUPPLIER_ID)
        assert rows[0]["brand"] == "FAGOR"

    def test_missing_article_warns_not_crashes(self, tmp_path):
        p = tmp_path / "np.xlsx"
        _make_np_xlsx(p, [
            _row("", "has title but no article", "d", "APACH", "r", "dr", "x.jpg"),
            _row("OK-1", "u", "d", "APACH", "r", "dr", "x.jpg"),
        ])
        rows, errors = parse_np_feed(str(p), SUPPLIER_ID)
        assert len(rows) == 1
        assert rows[0]["article"] == "OK-1"
        assert any("missing Артикул" in e for e in errors)

    def test_duplicate_article_skipped(self, tmp_path):
        p = tmp_path / "np.xlsx"
        _make_np_xlsx(p, [
            _row("DUP", "first", "d", "APACH", "r", "dr", "x.jpg"),
            _row("DUP", "second", "d", "APACH", "r", "dr", "x.jpg"),
        ])
        rows, errors = parse_np_feed(str(p), SUPPLIER_ID)
        assert len(rows) == 1
        assert rows[0]["name"] == "first"
        assert any("duplicate" in e for e in errors)

    def test_no_photo_yields_none(self, tmp_path):
        p = tmp_path / "np.xlsx"
        _make_np_xlsx(p, [
            _row("NP-1", "u", "d", "TATRA", "r", "dr", ""),
        ])
        rows, _ = parse_np_feed(str(p), SUPPLIER_ID)
        assert rows[0]["image_url"] is None
        assert rows[0]["images"] is None


# ===========================================================================
# enrich_sp_bodies  (against in-memory DB)
# ===========================================================================

@pytest.fixture()
def np_supplier(session):
    s = Supplier(name="Новый проект", feed_url="http://np", slug="novyy-proekt")
    session.add(s)
    session.commit()
    return s


def _seed_sp(session, supplier_id, article, **kw):
    sp = SupplierProduct(
        supplier_id=supplier_id,
        external_id=article,
        name=kw.get("name", "Existing name"),
        article=article,
        price_cents=kw.get("price_cents", 100000),
        currency="EUR",
        available=True,
        description=kw.get("description"),
        description_ru=kw.get("description_ru"),
        image_url=kw.get("image_url"),
        images=kw.get("images"),
    )
    session.add(sp)
    session.commit()
    return sp


class TestEnrichSpBodies:
    def _rows(self, supplier_id, article, **over):
        base = {
            "supplier_id": supplier_id, "article": article, "brand": "HURAKAN",
            "name": "n", "name_ru": "nr",
            "description": "UA body", "description_ru": "RU body",
            "image_url": "https://np/a.jpg",
            "images": json.dumps(["https://np/a.jpg", "https://np/b.jpg"]),
        }
        base.update(over)
        return [base]

    def test_enriches_existing_sp(self, session, np_supplier):
        sp = _seed_sp(session, np_supplier.id, "HKN-IMC25")
        res = enrich_sp_bodies(self._rows(np_supplier.id, "HKN-IMC25"))
        assert res["updated"] == 1
        assert res["missing"] == []
        session.refresh(sp)
        assert sp.description == "UA body"
        assert sp.description_ru == "RU body"
        assert sp.image_url == "https://np/a.jpg"
        assert json.loads(sp.images) == ["https://np/a.jpg", "https://np/b.jpg"]
        # name/price untouched (Channel 1 owns those)
        assert sp.name == "Existing name"
        assert sp.price_cents == 100000

    def test_idempotent_rerun_no_writes(self, session, np_supplier):
        _seed_sp(session, np_supplier.id, "HKN-IMC25")
        enrich_sp_bodies(self._rows(np_supplier.id, "HKN-IMC25"))
        res2 = enrich_sp_bodies(self._rows(np_supplier.id, "HKN-IMC25"))
        assert res2["updated"] == 0
        assert res2["unchanged"] == 1

    def test_empty_feed_value_does_not_wipe(self, session, np_supplier):
        sp = _seed_sp(session, np_supplier.id, "HKN-IMC25",
                      description_ru="kept RU")
        res = enrich_sp_bodies(
            self._rows(np_supplier.id, "HKN-IMC25", description_ru=None)
        )
        session.refresh(sp)
        assert sp.description_ru == "kept RU"  # not wiped by None

    def test_missing_sp_reported_not_created(self, session, np_supplier):
        res = enrich_sp_bodies(self._rows(np_supplier.id, "GHOST-1"))
        assert res["updated"] == 0
        assert res["missing"] == ["GHOST-1"]
        # no row created
        cnt = session.query(SupplierProduct).filter_by(article="GHOST-1").count()
        assert cnt == 0

    def test_other_supplier_untouched(self, session, np_supplier):
        # An sp with the same article but a DIFFERENT supplier must not match.
        other = Supplier(name="Other", feed_url="http://o")
        session.add(other)
        session.commit()
        sp_other = _seed_sp(session, other.id, "HKN-IMC25",
                            description="other UA")
        enrich_sp_bodies(self._rows(np_supplier.id, "HKN-IMC25"))
        session.refresh(sp_other)
        assert sp_other.description == "other UA"  # untouched
