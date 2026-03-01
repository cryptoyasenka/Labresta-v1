import json
import logging
import os
import tempfile

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import login_required
from sqlalchemy import select

from app.extensions import db
from app.models.notification_rule import Notification
from app.models.product_match import ProductMatch
from app.models.supplier import Supplier
from app.models.supplier_product import SupplierProduct
from app.models.sync_run import SyncRun
from app.services.excel_parser import (
    convert_google_sheets_url,
    get_preview_data,
    is_google_sheets_url,
    parse_excel_products,
    validate_xlsx_response,
    REQUIRED_FIELDS,
)
from app.services.feed_fetcher import fetch_feed, fetch_feed_with_retry
from app.services.feed_parser import parse_supplier_feed, save_supplier_products

logger = logging.getLogger(__name__)

suppliers_bp = Blueprint("suppliers", __name__)

# Field choices for column mapping dropdowns
FIELD_CHOICES = [
    ("skip", "— Пропустить —"),
    ("name", "Название"),
    ("brand", "Бренд"),
    ("model", "Модель"),
    ("price", "Цена"),
    ("available", "Наявність"),
]


@suppliers_bp.route("/")
@login_required
def supplier_list():
    suppliers = db.session.execute(
        select(Supplier).order_by(Supplier.name)
    ).scalars().all()
    return render_template("suppliers/list.html", suppliers=suppliers)


@suppliers_bp.route("/add", methods=["GET", "POST"])
@login_required
def supplier_add():
    if request.method == "POST":
        errors = _validate_supplier_form(request.form)
        if errors:
            return render_template(
                "suppliers/form.html",
                supplier=None,
                form_data=request.form,
                errors=errors,
            )

        feed_url = request.form.get("feed_url", "").strip() or None
        supplier = Supplier(
            name=request.form["name"].strip(),
            feed_url=feed_url,
            discount_percent=float(request.form.get("discount_percent", 0)),
        )
        db.session.add(supplier)
        db.session.commit()

        # If Google Sheets URL, redirect to mapping preview
        if feed_url and is_google_sheets_url(feed_url):
            try:
                download_url = convert_google_sheets_url(feed_url)
                raw_bytes = fetch_feed_with_retry(download_url)
                validate_xlsx_response(raw_bytes)

                fd, tmp_path = tempfile.mkstemp(suffix=".xlsx")
                os.close(fd)
                with open(tmp_path, "wb") as f:
                    f.write(raw_bytes)

                preview = get_preview_data(tmp_path)
                session[f"excel_temp_{supplier.id}"] = tmp_path
                session[f"excel_preview_{supplier.id}"] = preview

                flash(f"Поставщик '{supplier.name}' добавлен. Настройте маппинг колонок.", "success")
                return redirect(url_for("suppliers.supplier_mapping_preview", supplier_id=supplier.id))
            except Exception as e:
                logger.exception("Failed to download Google Sheets for supplier %s", supplier.name)
                flash(
                    f"Поставщик '{supplier.name}' добавлен, но не удалось загрузить файл: {e}",
                    "error",
                )
                return redirect(url_for("suppliers.supplier_list"))

        flash(f"Поставщик '{supplier.name}' добавлен.", "success")
        return redirect(url_for("suppliers.supplier_list"))

    return render_template("suppliers/form.html", supplier=None, form_data=None, errors=None)


@suppliers_bp.route("/<int:supplier_id>/edit", methods=["GET", "POST"])
@login_required
def supplier_edit(supplier_id):
    supplier = db.session.get(Supplier, supplier_id)
    if not supplier:
        flash("Поставщик не найден.", "error")
        return redirect(url_for("suppliers.supplier_list"))

    if request.method == "POST":
        errors = _validate_supplier_form(request.form)
        if errors:
            return render_template(
                "suppliers/form.html",
                supplier=supplier,
                form_data=None,
                errors=errors,
            )

        supplier.name = request.form["name"].strip()
        supplier.feed_url = request.form.get("feed_url", "").strip() or None
        supplier.discount_percent = float(request.form.get("discount_percent", 0))
        db.session.commit()
        flash(f"Поставщик '{supplier.name}' обновлён.", "success")
        return redirect(url_for("suppliers.supplier_list"))

    return render_template("suppliers/form.html", supplier=supplier, form_data=None, errors=None)


@suppliers_bp.route("/<int:supplier_id>/toggle", methods=["POST"])
@login_required
def supplier_toggle(supplier_id):
    supplier = db.session.get(Supplier, supplier_id)
    if not supplier:
        flash("Поставщик не найден.", "error")
        return redirect(url_for("suppliers.supplier_list"))

    supplier.is_enabled = not supplier.is_enabled
    db.session.commit()
    status = "включён" if supplier.is_enabled else "выключен"
    flash(f"Поставщик '{supplier.name}' {status}.", "success")
    return redirect(url_for("suppliers.supplier_list"))


@suppliers_bp.route("/<int:supplier_id>/delete", methods=["POST"])
@login_required
def supplier_delete(supplier_id):
    supplier = db.session.get(Supplier, supplier_id)
    if not supplier:
        flash("Поставщик не найден.", "error")
        return redirect(url_for("suppliers.supplier_list"))

    name = supplier.name

    # Get supplier product IDs for cascading deletes
    sp_ids = [
        row[0]
        for row in db.session.execute(
            select(SupplierProduct.id).where(SupplierProduct.supplier_id == supplier_id)
        ).all()
    ]

    if sp_ids:
        # Delete notifications linked to these supplier products
        db.session.execute(
            Notification.__table__.delete().where(
                Notification.supplier_product_id.in_(sp_ids)
            )
        )
        # Delete matches linked to these supplier products
        db.session.execute(
            ProductMatch.__table__.delete().where(
                ProductMatch.supplier_product_id.in_(sp_ids)
            )
        )
        # Delete supplier products
        db.session.execute(
            SupplierProduct.__table__.delete().where(
                SupplierProduct.supplier_id == supplier_id
            )
        )

    # Delete sync runs
    db.session.execute(
        SyncRun.__table__.delete().where(SyncRun.supplier_id == supplier_id)
    )

    # Delete supplier
    db.session.delete(supplier)
    db.session.commit()

    flash(f"Поставщик '{name}' и все связанные данные удалены.", "success")
    return redirect(url_for("suppliers.supplier_list"))


@suppliers_bp.route("/<int:supplier_id>/fetch", methods=["POST"])
@login_required
def supplier_fetch(supplier_id):
    supplier = db.session.get(Supplier, supplier_id)
    if not supplier:
        flash("Поставщик не найден.", "error")
        return redirect(url_for("suppliers.supplier_list"))

    try:
        if supplier.feed_url and is_google_sheets_url(supplier.feed_url):
            # Excel pipeline: download, validate, parse with saved mapping
            if not supplier.column_mapping:
                flash("Маппинг колонок не настроен. Сначала настройте колонки.", "error")
                return redirect(url_for("suppliers.supplier_list"))

            download_url = convert_google_sheets_url(supplier.feed_url)
            raw_bytes = fetch_feed_with_retry(download_url)
            validate_xlsx_response(raw_bytes)

            fd, tmp_path = tempfile.mkstemp(suffix=".xlsx")
            os.close(fd)
            try:
                with open(tmp_path, "wb") as f:
                    f.write(raw_bytes)

                mapping = json.loads(supplier.column_mapping)
                products, errors = parse_excel_products(
                    tmp_path, mapping["columns"], mapping["header_row"], supplier.id
                )

                for err in errors:
                    logger.warning("Excel parse: %s", err)

                if len(errors) > len(products):
                    flash(
                        f"Слишком много ошибок парсинга ({len(errors)} ошибок, "
                        f"{len(products)} товаров). Проверьте маппинг колонок.",
                        "error",
                    )
                    return redirect(url_for("suppliers.supplier_list"))

                result = save_supplier_products(products)
                msg = (
                    f"Excel фид загружен: {result['total']} товаров "
                    f"({result['created']} новых, {result['updated']} обновлено)."
                )
                if errors:
                    msg += f" Предупреждений: {len(errors)}."
                flash(msg, "success")
            finally:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
        elif supplier.feed_url:
            # YML pipeline
            raw_bytes = fetch_feed(supplier.feed_url)
            products = parse_supplier_feed(raw_bytes, supplier.id)
            result = save_supplier_products(products)
            flash(
                f"Фид загружен: {result['total']} товаров "
                f"({result['created']} новых, {result['updated']} обновлено).",
                "success",
            )
        else:
            flash("URL фида не указан. Загрузите файл вручную.", "error")
    except Exception as e:
        logger.exception("Feed fetch failed for supplier %s", supplier.name)
        flash(f"Ошибка загрузки фида: {e}", "error")

    return redirect(url_for("suppliers.supplier_list"))


@suppliers_bp.route("/<int:supplier_id>/upload", methods=["POST"])
@login_required
def supplier_upload(supplier_id):
    """Accept .xlsx file upload and redirect to column mapping preview."""
    supplier = db.session.get(Supplier, supplier_id)
    if not supplier:
        flash("Поставщик не найден.", "error")
        return redirect(url_for("suppliers.supplier_list"))

    file = request.files.get("file")
    if not file or not file.filename:
        flash("Файл не выбран.", "error")
        return redirect(url_for("suppliers.supplier_list"))

    if not file.filename.lower().endswith(".xlsx"):
        flash("Допустимы только файлы .xlsx.", "error")
        return redirect(url_for("suppliers.supplier_list"))

    try:
        fd, tmp_path = tempfile.mkstemp(suffix=".xlsx")
        os.close(fd)
        file.save(tmp_path)

        preview = get_preview_data(tmp_path)
        session[f"excel_temp_{supplier.id}"] = tmp_path
        session[f"excel_preview_{supplier.id}"] = preview

        return redirect(url_for("suppliers.supplier_mapping_preview", supplier_id=supplier.id))
    except Exception as e:
        logger.exception("File upload failed for supplier %s", supplier.name)
        flash(f"Ошибка обработки файла: {e}", "error")
        return redirect(url_for("suppliers.supplier_list"))


@suppliers_bp.route("/<int:supplier_id>/mapping")
@login_required
def supplier_mapping_preview(supplier_id):
    """Show column mapping preview page with auto-detected mappings and dropdowns."""
    supplier = db.session.get(Supplier, supplier_id)
    if not supplier:
        flash("Поставщик не найден.", "error")
        return redirect(url_for("suppliers.supplier_list"))

    preview_key = f"excel_preview_{supplier_id}"
    preview_data = session.get(preview_key)

    # Re-download if no data or data has empty headers (stale session)
    if not preview_data or not preview_data.get("all_headers"):
        # Try to re-download for Google Sheets suppliers
        if supplier.feed_url and is_google_sheets_url(supplier.feed_url):
            try:
                download_url = convert_google_sheets_url(supplier.feed_url)
                raw_bytes = fetch_feed_with_retry(download_url)
                validate_xlsx_response(raw_bytes)

                fd, tmp_path = tempfile.mkstemp(suffix=".xlsx")
                os.close(fd)
                with open(tmp_path, "wb") as f:
                    f.write(raw_bytes)

                preview_data = get_preview_data(tmp_path)
                session[f"excel_temp_{supplier_id}"] = tmp_path
            except Exception as e:
                logger.exception("Failed to download for mapping preview")
                flash(f"Не удалось загрузить файл для предпросмотра: {e}", "error")
                return redirect(url_for("suppliers.supplier_list"))
        else:
            flash("Нет данных для предпросмотра. Загрузите файл заново.", "error")
            return redirect(url_for("suppliers.supplier_list"))

    return render_template(
        "suppliers/mapping_preview.html",
        supplier=supplier,
        preview_data=preview_data,
        field_choices=FIELD_CHOICES,
    )


@suppliers_bp.route("/<int:supplier_id>/mapping/confirm", methods=["POST"])
@login_required
def supplier_mapping_confirm(supplier_id):
    """Confirm column mapping and run initial product import."""
    supplier = db.session.get(Supplier, supplier_id)
    if not supplier:
        flash("Поставщик не найден.", "error")
        return redirect(url_for("suppliers.supplier_list"))

    header_row = int(request.form.get("header_row", 0))

    # Read column assignments from form
    columns = {}
    for key, value in request.form.items():
        if key.startswith("col_") and value != "skip":
            col_idx = key.replace("col_", "")
            columns[col_idx] = value

    # Validate required fields are assigned
    assigned_fields = set(columns.values())
    mapping_required = {"name", "price"}
    missing = mapping_required - assigned_fields
    if missing:
        missing_names = {
            "name": "Название",
            "price": "Цена",
        }
        missing_labels = [missing_names.get(f, f) for f in missing]
        flash(f"Не назначены обязательные колонки: {', '.join(missing_labels)}.", "error")
        return redirect(url_for("suppliers.supplier_mapping_preview", supplier_id=supplier.id))

    # Save mapping to supplier
    mapping = {"header_row": header_row, "columns": columns}
    supplier.column_mapping = json.dumps(mapping, ensure_ascii=False)
    db.session.commit()

    # If temp file exists, run initial import
    temp_key = f"excel_temp_{supplier_id}"
    tmp_path = session.pop(temp_key, None)
    # Clean up preview data from session
    session.pop(f"excel_preview_{supplier_id}", None)

    if tmp_path and os.path.exists(tmp_path):
        try:
            products, errors = parse_excel_products(
                tmp_path, columns, header_row, supplier.id
            )

            for err in errors:
                logger.warning("Excel parse: %s", err)

            if len(errors) > len(products):
                flash(
                    f"Маппинг сохранён, но слишком много ошибок парсинга "
                    f"({len(errors)} ошибок, {len(products)} товаров). "
                    f"Проверьте маппинг колонок.",
                    "error",
                )
                return redirect(url_for("suppliers.supplier_list"))

            result = save_supplier_products(products)
            msg = (
                f"Маппинг сохранён. Импортировано {result['total']} товаров "
                f"({result['created']} новых, {result['updated']} обновлено)."
            )
            if errors:
                msg += f" Предупреждений: {len(errors)}."
            flash(msg, "success")
        except Exception as e:
            logger.exception("Initial import failed for supplier %s", supplier.name)
            flash(f"Маппинг сохранён, но импорт не удался: {e}", "error")
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    else:
        flash("Маппинг колонок сохранён.", "success")

    return redirect(url_for("suppliers.supplier_list"))


def _validate_supplier_form(form):
    """Validate supplier form data. Returns dict of field -> error message, or empty dict."""
    errors = {}
    if not form.get("name", "").strip():
        errors["name"] = "Название обязательно."
    # feed_url is optional (for file-upload-only suppliers)

    discount = form.get("discount_percent", "0")
    try:
        val = float(discount)
        if val < 0 or val > 100:
            errors["discount_percent"] = "Скидка должна быть от 0 до 100."
    except (ValueError, TypeError):
        errors["discount_percent"] = "Скидка должна быть числом."

    return errors
