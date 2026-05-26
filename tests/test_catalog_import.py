"""Unit tests for save_catalog_products — two-channel field separation.

The catalog import must update catalog-owned fields (name UA, brand, price,
description_ua, ...) from a Horoshop export, but must NOT overwrite the
worker-owned translation fields (name_ru, description_ru) on update — those
live only here in pp and Horoshop's RU columns are corrupted/stale.
"""

from app.models.catalog import PromProduct
from app.services.catalog_import import preview_catalog_import, save_catalog_products


def test_update_preserves_translations_by_default(session):
    """Existing product: name_ru/description_ru survive a catalog re-import."""
    pp = PromProduct(
        external_id="P1",
        name="Піч конвекційна (стара UA)",
        name_ru="Печь конвекционная (чистый перевод воркера)",
        description_ua="опис UA старий",
        description_ru="описание RU чистое от воркера",
        brand="Apach",
        price=10000,
        currency="EUR",
    )
    session.add(pp)
    session.commit()

    # Horoshop export row: fresh catalog data + CORRUPTED RU (ukr text in RU field)
    rows = [
        {
            "external_id": "P1",
            "name": "Піч конвекційна (новий UA)",
            "name_ru": "Піч конвекційна (зіпсований RU)",  # corrupted — must be ignored
            "description_ua": "опис UA новий",
            "description_ru": "опис RU зіпсований",  # corrupted — must be ignored
            "brand": "Apach",
            "price": "150.0",
            "currency": "EUR",
        }
    ]
    result = save_catalog_products(rows)

    assert result == {"created": 0, "updated": 1, "skipped": 0, "total": 1}

    obj = session.get(PromProduct, pp.id)
    # Catalog-owned: updated
    assert obj.name == "Піч конвекційна (новий UA)"
    assert obj.description_ua == "опис UA новий"
    assert obj.price == 15000
    # Worker-owned: preserved
    assert obj.name_ru == "Печь конвекционная (чистый перевод воркера)"
    assert obj.description_ru == "описание RU чистое от воркера"


def test_insert_takes_all_fields_including_translations(session):
    """Brand-new product: no translation to protect, so name_ru is taken from row."""
    rows = [
        {
            "external_id": "NEW1",
            "name": "Новий товар UA",
            "name_ru": "Новый товар RU",
            "description_ua": "опис UA",
            "description_ru": "описание RU",
            "brand": "Hurakan",
            "price": "200.0",
            "currency": "EUR",
        }
    ]
    result = save_catalog_products(rows)

    assert result["created"] == 1
    orm = session.query(PromProduct).filter_by(external_id="NEW1").one()
    assert orm.name == "Новий товар UA"
    assert orm.name_ru == "Новый товар RU"
    assert orm.description_ru == "описание RU"
    assert orm.price == 20000


def test_preserve_false_overwrites_translations(session):
    """Opt-out path (authoritative source): translations ARE overwritten."""
    pp = PromProduct(
        external_id="P2",
        name="Товар UA",
        name_ru="старый RU",
        description_ru="старое описание RU",
        price=5000,
    )
    session.add(pp)
    session.commit()

    rows = [
        {
            "external_id": "P2",
            "name": "Товар UA",
            "name_ru": "новый RU (авторитетный)",
            "description_ru": "новое описание RU",
            "price": "60.0",
        }
    ]
    result = save_catalog_products(rows, preserve_translations=False)

    assert result["updated"] == 1
    orm = session.query(PromProduct).filter_by(external_id="P2").one()
    assert orm.name_ru == "новый RU (авторитетный)"
    assert orm.description_ru == "новое описание RU"


def test_update_still_overwrites_catalog_fields(session):
    """Price/brand/url etc. remain authoritative from the export on update."""
    pp = PromProduct(
        external_id="P3",
        name="старое имя",
        brand="OldBrand",
        price=1000,
        page_url="http://old",
        image_url="http://old.jpg",
    )
    session.add(pp)
    session.commit()

    rows = [
        {
            "external_id": "P3",
            "name": "новое имя",
            "brand": "NewBrand",
            "price": "99.0",
            "page_url": "http://new",
            "image_url": "http://new.jpg",
        }
    ]
    save_catalog_products(rows)

    orm = session.query(PromProduct).filter_by(external_id="P3").one()
    assert orm.name == "новое имя"
    assert orm.brand == "NewBrand"
    assert orm.price == 9900
    assert orm.page_url == "http://new"
    assert orm.image_url == "http://new.jpg"


# --- preview_catalog_import: read-only dry-run -------------------------------


def test_preview_counts_created_updated_skipped_without_writing(session):
    """Preview reports created/updated/skipped and does NOT touch the DB."""
    session.add(PromProduct(external_id="E1", name="старое имя", price=1000))
    session.commit()

    rows = [
        {"external_id": "E1", "name": "новое имя", "price": "20.0"},  # update
        {"external_id": "NEW", "name": "новый товар", "price": "30.0"},  # create
        {"external_id": "", "name": "без id"},  # skip
    ]
    result = preview_catalog_import(rows)

    assert result["created"] == 1
    assert result["updated"] == 1
    assert result["skipped"] == 1
    assert result["total"] == 2

    # Nothing written: existing row unchanged, no NEW row inserted.
    obj = session.query(PromProduct).filter_by(external_id="E1").one()
    assert obj.name == "старое имя"
    assert obj.price == 1000
    assert session.query(PromProduct).filter_by(external_id="NEW").first() is None


def test_preview_changed_counts_only_real_differences(session):
    """changed[field] counts a field only when its value actually differs."""
    session.add(
        PromProduct(external_id="E2", name="имя", brand="Apach", price=1000)
    )
    session.commit()

    rows = [
        # name same, brand same, price differs -> only price counted
        {"external_id": "E2", "name": "имя", "brand": "Apach", "price": "50.0"}
    ]
    result = preview_catalog_import(rows)

    assert result["changed"]["price"] == 1
    assert result["changed"]["name"] == 0
    assert result["changed"]["brand"] == 0


def test_preview_flags_cleared_fields_wrong_file_signal(session):
    """A file missing a column that the row had populated shows as 'cleared'."""
    session.add(
        PromProduct(
            external_id="E3",
            name="имя",
            price=1000,
            brand="Apach",
            page_url="http://x",
        )
    )
    session.commit()

    # Row carries only name — brand/price/page_url absent => would be cleared.
    rows = [{"external_id": "E3", "name": "имя"}]
    result = preview_catalog_import(rows)

    assert result["cleared"]["price"] == 1
    assert result["cleared"]["brand"] == 1
    assert result["cleared"]["page_url"] == 1
    # name is unchanged, so not cleared
    assert result["cleared"]["name"] == 0


def test_preview_counts_protected_translations(session):
    """translations_protected counts existing rows holding worker translations."""
    session.add(
        PromProduct(
            external_id="E4",
            name="имя",
            name_ru="перевод воркера",
            price=1000,
        )
    )
    session.add(PromProduct(external_id="E5", name="имя2", price=2000))  # no RU
    session.commit()

    rows = [
        {"external_id": "E4", "name": "имя", "price": "50.0"},
        {"external_id": "E5", "name": "имя2", "price": "60.0"},
    ]
    result = preview_catalog_import(rows)

    assert result["translations_protected"] == 1  # only E4 has a translation
