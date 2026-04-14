"""
Catalog CSV/XLS/XLSX import service.

Parses export files from Horoshop or prom.ua admin panels,
normalizes headers, and upserts products into the PromProduct table.
"""

import csv
import io
from datetime import datetime, timezone

import chardet
import openpyxl

from app.extensions import db
from app.models.catalog import PromProduct

# Column alias mapping: export headers -> internal field names
# Supports both Horoshop and prom.ua formats
COLUMN_ALIASES = {
    # --- Horoshop export headers ---
    "артикул": "external_id",
    "артикул для отображения на сайте": "display_article",
    "артикул для відображення на сайті": "display_article",
    "назва (ua)": "name",
    "название (ua)": "name",
    "назва модифікації (ua)": "name",
    "название модификации (ua)": "name",
    "назва (ru)": "name_ru",
    "название (ru)": "name_ru",
    "бренд": "brand",
    "ціна": "price",
    "цена": "price",
    "валюта": "currency",
    "посилання": "page_url",
    "ссылка": "page_url",
    "фото": "image_url",
    "галерея": "images",
    "описание товара (ua)": "description_ua",
    "опис товару (ua)": "description_ua",
    "описание товара (ru)": "description_ru",
    "опис товару (ru)": "description_ru",
    # --- Prom.ua export headers ---
    "унікальний_ідентифікатор": "external_id",
    "уникальный_идентификатор": "external_id",
    "ідентифікатор_товару": "external_id",
    "идентификатор_товара": "external_id",
    "назва_позиції": "name",
    "название_позиции": "name",
    "код_товару": "article",
    "код_товара": "article",
    "виробник": "brand",
    "производитель": "brand",
    "посилання_на_сторінку_товару": "page_url",
    "ссылка_на_страницу_товара": "page_url",
}


def normalize_header(header: str) -> str:
    """Strip whitespace and lowercase a header string."""
    return header.strip().lower()


def map_headers(raw_headers: list[str]) -> dict[int, str]:
    """
    Map column indices to internal field names via COLUMN_ALIASES.

    Args:
        raw_headers: List of raw header strings from the first row of the file.

    Returns:
        Dict mapping column index -> internal field name for recognized columns.

    Raises:
        ValueError: If 'external_id' or 'name' column is not found.
    """
    mapping = {}
    mapped_fields = set()
    for idx, header in enumerate(raw_headers):
        normalized = normalize_header(header)
        if normalized in COLUMN_ALIASES:
            field = COLUMN_ALIASES[normalized]
            # First column wins — skip duplicates for the same field
            if field not in mapped_fields:
                mapping[idx] = field
                mapped_fields.add(field)

    # Validate required columns
    missing = []
    if "external_id" not in mapped_fields:
        missing.append("external_id")
    if "name" not in mapped_fields:
        missing.append("name")

    if missing:
        recognized = [f"{idx}: {field}" for idx, field in mapping.items()]
        unrecognized = [
            raw_headers[i] for i in range(len(raw_headers)) if i not in mapping
        ]
        raise ValueError(
            f"Missing required columns: {missing}. "
            f"Recognized: {recognized}. "
            f"Unrecognized headers: {unrecognized}"
        )

    return mapping


def parse_csv(file_stream: io.TextIOBase, encoding: str = "utf-8") -> list[dict]:
    """
    Parse a CSV file stream into a list of product dicts.

    Args:
        file_stream: Text-mode file stream.
        encoding: Not used directly (stream should already be decoded), kept for API consistency.

    Returns:
        List of dicts with mapped field names.
    """
    reader = csv.reader(file_stream)

    # First row = headers
    try:
        raw_headers = next(reader)
    except StopIteration:
        raise ValueError("CSV file is empty")

    mapping = map_headers(raw_headers)

    products = []
    for row in reader:
        if not row or all(cell.strip() == "" for cell in row):
            continue  # skip empty rows
        product = {}
        for idx, field_name in mapping.items():
            if idx < len(row):
                product[field_name] = row[idx].strip()
            else:
                product[field_name] = ""
        products.append(product)

    return products


def parse_xlsx(file_path: str) -> list[dict]:
    """
    Parse an XLSX file into a list of product dicts.

    Args:
        file_path: Path to the .xlsx file on disk.

    Returns:
        List of dicts with mapped field names.
    """
    wb = openpyxl.load_workbook(file_path, read_only=True)

    # Try known sheet name first, fall back to first sheet
    if "Export Products Sheet" in wb.sheetnames:
        ws = wb["Export Products Sheet"]
    else:
        ws = wb[wb.sheetnames[0]]

    rows = ws.iter_rows(values_only=True)

    # First row = headers
    try:
        raw_headers = [str(h) if h is not None else "" for h in next(rows)]
    except StopIteration:
        wb.close()
        raise ValueError("XLSX file is empty")

    mapping = map_headers(raw_headers)

    products = []
    for row in rows:
        if not row or all(cell is None or str(cell).strip() == "" for cell in row):
            continue  # skip empty rows
        product = {}
        for idx, field_name in mapping.items():
            if idx < len(row):
                val = row[idx]
                product[field_name] = str(val).strip() if val is not None else ""
            else:
                product[field_name] = ""
        products.append(product)

    wb.close()
    return products


def parse_catalog_file(file_path: str, filename: str) -> list[dict]:
    """
    Dispatch to the correct parser based on file extension.

    Args:
        file_path: Path to the uploaded file on disk.
        filename: Original filename (used to detect extension).

    Returns:
        List of product dicts.

    Raises:
        ValueError: For unsupported file extensions or parse errors.
    """
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    if ext == "csv":
        # Detect encoding
        with open(file_path, "rb") as f:
            raw_data = f.read()
        detected = chardet.detect(raw_data)
        encoding = detected.get("encoding") or "utf-8"

        # Try detected encoding, fall back to cp1251
        try:
            text = raw_data.decode(encoding)
        except (UnicodeDecodeError, LookupError):
            text = raw_data.decode("cp1251")

        return parse_csv(io.StringIO(text), encoding=encoding)

    elif ext in ("xls", "xlsx"):
        return parse_xlsx(file_path)

    else:
        raise ValueError(
            f"Unsupported file format: .{ext}. Supported formats: .csv, .xls, .xlsx"
        )


def save_catalog_products(products: list[dict]) -> dict:
    """
    Upsert parsed products into the PromProduct table.

    Matches on external_id (unique). Updates existing records, inserts new ones.

    Args:
        products: List of product dicts from parse_catalog_file.

    Returns:
        Dict with keys: created, updated, skipped, total.
    """
    created = 0
    updated = 0
    skipped = 0

    for product in products:
        ext_id = product.get("external_id", "").strip()
        name = product.get("name", "").strip()

        # Skip rows missing required fields
        if not ext_id or not name:
            skipped += 1
            continue

        # Parse price: string -> float -> cents (int)
        price = None
        raw_price = product.get("price", "").strip()
        if raw_price:
            try:
                price = int(float(raw_price) * 100)
            except (ValueError, TypeError):
                price = None

        currency = product.get("currency", "").strip() or None
        article = product.get("article", "").strip() or None
        display_article = product.get("display_article", "").strip() or None
        brand = product.get("brand", "").strip() or None
        page_url = product.get("page_url", "").strip() or None
        name_ru = product.get("name_ru", "").strip() or None
        image_url = product.get("image_url", "").strip() or None
        images = product.get("images", "").strip() or None
        description_ua = product.get("description_ua", "").strip() or None
        description_ru = product.get("description_ru", "").strip() or None

        # Check if product already exists
        existing = db.session.execute(
            db.select(PromProduct).where(PromProduct.external_id == ext_id)
        ).scalar_one_or_none()

        if existing:
            existing.name = name
            existing.name_ru = name_ru
            existing.brand = brand
            existing.article = article
            existing.display_article = display_article
            existing.price = price
            existing.currency = currency
            existing.page_url = page_url
            existing.image_url = image_url
            existing.images = images
            existing.description_ua = description_ua
            existing.description_ru = description_ru
            existing.imported_at = datetime.now(timezone.utc)
            updated += 1
        else:
            new_product = PromProduct(
                external_id=ext_id,
                name=name,
                name_ru=name_ru,
                brand=brand,
                article=article,
                display_article=display_article,
                price=price,
                currency=currency,
                page_url=page_url,
                image_url=image_url,
                images=images,
                description_ua=description_ua,
                description_ru=description_ru,
            )
            db.session.add(new_product)
            created += 1

    db.session.commit()

    return {
        "created": created,
        "updated": updated,
        "skipped": skipped,
        "total": created + updated,
    }
