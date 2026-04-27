import json
import logging
import os
import tempfile

from flask import (
    Blueprint,
    flash,
    jsonify,
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
from app.models.supplier_brand_discount import SupplierBrandDiscount
from app.models.supplier_product import SupplierProduct
from app.models.sync_run import SyncRun
from app.services.audit_service import log_action
from app.services.excel_parser import (
    convert_google_sheets_url,
    get_preview_data,
    is_google_sheets_url,
    is_xlsx_url,
    parse_excel_products,
    validate_xlsx_response,
)
from app.services.feed_fetcher import fetch_feed, fetch_feed_with_retry
from app.services.feed_parser import parse_supplier_feed, save_supplier_products
from app.services.kodaki_adapter import apply_supplier_adapter
from app.services.rp_parser import parse_rp_sheet
from app.services.sync_pipeline import run_full_sync
from app.services.yml_generator import regenerate_supplier_feed

logger = logging.getLogger(__name__)

suppliers_bp = Blueprint("suppliers", __name__)

# Field choices for column mapping dropdowns
FIELD_CHOICES = [
    ("skip", "— Пропустить —"),
    ("name", "Название"),
    ("brand", "Бренд"),
    ("model", "Модель"),
    ("article", "Артикул"),
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
        mode = (request.form.get("pricing_mode") or "flat").strip() or "flat"
        parser_type = (request.form.get("parser_type") or "auto").strip() or "auto"
        supplier = Supplier(
            name=request.form["name"].strip(),
            feed_url=feed_url,
            discount_percent=float(request.form.get("discount_percent", 0)),
            pricing_mode=mode,
            parser_type=parser_type,
        )
        raw_rate = request.form.get("eur_rate_uah", "").strip()
        if raw_rate:
            supplier.eur_rate_uah = float(raw_rate)
        raw_min = request.form.get("min_margin_uah", "").strip()
        if raw_min:
            supplier.min_margin_uah = float(raw_min)
        raw_cost = request.form.get("cost_rate", "").strip()
        if raw_cost:
            supplier.cost_rate = float(raw_cost)
        db.session.add(supplier)
        db.session.flush()  # need supplier.id for brand_discounts FK

        if mode == "per_brand":
            try:
                brand_rows = _parse_brand_discounts_form(request.form)
            except ValueError as exc:
                db.session.rollback()
                return render_template(
                    "suppliers/form.html",
                    supplier=None,
                    form_data=request.form,
                    errors={"brand_discounts": str(exc)},
                )
            _replace_brand_discounts(supplier, brand_rows)

        db.session.commit()

        if feed_url and supplier.parser_type == "rp":
            # RP Україна pipeline: section-grouped xlsx, no column mapping step.
            try:
                download_url = (
                    convert_google_sheets_url(feed_url)
                    if is_google_sheets_url(feed_url)
                    else feed_url
                )
                raw_bytes = fetch_feed_with_retry(download_url)
                validate_xlsx_response(raw_bytes)
                fd, tmp_path = tempfile.mkstemp(suffix=".xlsx")
                os.close(fd)
                try:
                    with open(tmp_path, "wb") as f:
                        f.write(raw_bytes)
                    products, errors = parse_rp_sheet(tmp_path, supplier.id)
                    for err in errors:
                        logger.warning("RP parse (add): %s", err)
                    result = save_supplier_products(products)
                    msg = (
                        f"Поставщик '{supplier.name}' добавлен. РП фід: "
                        f"{result['total']} товарів ({result['created']} нових)."
                    )
                    if errors:
                        msg += f" Попереджень: {len(errors)}."
                    flash(msg, "success")
                finally:
                    if os.path.exists(tmp_path):
                        os.unlink(tmp_path)
            except Exception as e:
                logger.exception("RP feed fetch failed for supplier %s", supplier.name)
                flash(
                    f"Поставщик '{supplier.name}' добавлен, але не вдалося завантажити фід: {e}",
                    "error",
                )
            return redirect(url_for("suppliers.supplier_list"))

        # Excel-by-URL path: Google Sheets OR a direct .xlsx URL.
        # Both flow through the same mapping-preview UX — only the
        # download step differs.
        if feed_url and (is_google_sheets_url(feed_url) or is_xlsx_url(feed_url)):
            try:
                if is_google_sheets_url(feed_url):
                    download_url = convert_google_sheets_url(feed_url)
                else:
                    download_url = feed_url
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
                logger.exception("Failed to download xlsx for supplier %s", supplier.name)
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

        mode = (request.form.get("pricing_mode") or "flat").strip() or "flat"
        brand_rows: list[tuple[str, float]] = []
        if mode == "per_brand":
            try:
                brand_rows = _parse_brand_discounts_form(request.form)
            except ValueError as exc:
                return render_template(
                    "suppliers/form.html",
                    supplier=supplier,
                    form_data=request.form,
                    errors={"brand_discounts": str(exc)},
                )

        supplier.name = request.form["name"].strip()
        supplier.feed_url = request.form.get("feed_url", "").strip() or None
        supplier.discount_percent = float(request.form.get("discount_percent", 0))
        supplier.pricing_mode = mode
        supplier.parser_type = (request.form.get("parser_type") or "auto").strip() or "auto"

        raw_rate = request.form.get("eur_rate_uah", "").strip()
        if raw_rate:
            supplier.eur_rate_uah = float(raw_rate)
        raw_min = request.form.get("min_margin_uah", "").strip()
        if raw_min:
            supplier.min_margin_uah = float(raw_min)
        raw_cost = request.form.get("cost_rate", "").strip()
        if raw_cost:
            supplier.cost_rate = float(raw_cost)

        if mode == "per_brand":
            _replace_brand_discounts(supplier, brand_rows)
        # flat / auto_margin: leave brand_discounts untouched so the operator
        # can flip back to per_brand without re-entering rates. They're
        # ignored by resolve_discount_percent unless pricing_mode == 'per_brand'.

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
        if supplier.parser_type == "rp" and supplier.feed_url:
            # RP Україна pipeline: section-grouped xlsx, no column mapping needed.
            download_url = (
                convert_google_sheets_url(supplier.feed_url)
                if is_google_sheets_url(supplier.feed_url)
                else supplier.feed_url
            )
            raw_bytes = fetch_feed_with_retry(download_url)
            validate_xlsx_response(raw_bytes)
            fd, tmp_path = tempfile.mkstemp(suffix=".xlsx")
            os.close(fd)
            try:
                with open(tmp_path, "wb") as f:
                    f.write(raw_bytes)
                products, errors = parse_rp_sheet(tmp_path, supplier.id)
                for err in errors:
                    logger.warning("RP parse (fetch): %s", err)
                result = save_supplier_products(products)
                msg = (
                    f"РП фід: {result['total']} товарів "
                    f"({result['created']} нових, {result['updated']} оновлено)."
                )
                if errors:
                    msg += f" Попереджень: {len(errors)}."
                flash(msg, "success")
            finally:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
        elif supplier.feed_url and (
            is_google_sheets_url(supplier.feed_url) or is_xlsx_url(supplier.feed_url)
        ):
            # Excel pipeline: download, validate, parse with saved mapping
            if not supplier.column_mapping:
                flash("Маппинг колонок не настроен. Сначала настройте колонки.", "error")
                return redirect(url_for("suppliers.supplier_list"))

            if is_google_sheets_url(supplier.feed_url):
                download_url = convert_google_sheets_url(supplier.feed_url)
            else:
                download_url = supplier.feed_url
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
            raw_bytes = apply_supplier_adapter(raw_bytes, supplier.feed_url)
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
        # Try to re-download for Excel-by-URL suppliers (Google Sheets or direct xlsx)
        if supplier.feed_url and (is_google_sheets_url(supplier.feed_url) or is_xlsx_url(supplier.feed_url)):
            try:
                if is_google_sheets_url(supplier.feed_url):
                    download_url = convert_google_sheets_url(supplier.feed_url)
                else:
                    download_url = supplier.feed_url
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


@suppliers_bp.route("/<int:supplier_id>/regenerate-feed", methods=["POST"])
@login_required
def supplier_regenerate_feed(supplier_id):
    """Regenerate the per-supplier YML at labresta-feed-<slug>.yml.

    Does not touch the main feed and does not flip in_feed flags.
    """
    supplier = db.session.get(Supplier, supplier_id)
    if not supplier:
        return jsonify({"status": "error", "message": "Поставщик не найден"}), 404
    try:
        result = regenerate_supplier_feed(supplier_id)
    except Exception as exc:  # pragma: no cover — surfaced to UI
        logger.exception("Per-supplier feed regen failed for %s", supplier.name)
        return jsonify({"status": "error", "message": str(exc)}), 500
    log_action("regenerate_supplier_feed", details={
        "supplier_id": supplier.id,
        "supplier_name": supplier.name,
        "supplier_slug": result.get("supplier_slug"),
        "total": result["total"],
        "available": result["available"],
        "unavailable": result["unavailable"],
    })
    return jsonify({"status": "ok", **result})


@suppliers_bp.route("/fetch-all", methods=["POST"])
@login_required
def suppliers_fetch_all():
    """Run the full sync pipeline for every enabled supplier.

    Synchronous: blocks the request until all suppliers finish (or fail).
    Each supplier's run is recorded as a SyncRun row and individual errors
    are isolated — one supplier's failure does not abort the others.
    """
    enabled = db.session.execute(
        select(Supplier).where(Supplier.is_enabled.is_(True)).order_by(Supplier.name)
    ).scalars().all()
    if not enabled:
        return jsonify({
            "status": "ok",
            "summary": {"total": 0, "ok": 0, "failed": 0},
            "results": [],
            "message": "Нет активных поставщиков для обновления.",
        })

    results = []
    ok = 0
    failed = 0
    for supplier in enabled:
        try:
            run_full_sync(supplier_id=supplier.id)
            results.append({
                "supplier_id": supplier.id,
                "name": supplier.name,
                "status": "ok",
            })
            ok += 1
        except Exception as exc:
            logger.exception("fetch-all: supplier %s failed", supplier.name)
            results.append({
                "supplier_id": supplier.id,
                "name": supplier.name,
                "status": "error",
                "message": str(exc),
            })
            failed += 1

    log_action("fetch_all_suppliers", details={
        "total": len(enabled),
        "ok": ok,
        "failed": failed,
    })

    return jsonify({
        "status": "ok",
        "summary": {"total": len(enabled), "ok": ok, "failed": failed},
        "results": results,
    })


VALID_PRICING_MODES = {"flat", "per_brand", "auto_margin"}


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

    mode = form.get("pricing_mode", "flat").strip() or "flat"
    if mode not in VALID_PRICING_MODES:
        errors["pricing_mode"] = "Недопустимый режим скидок."

    raw_rate = form.get("eur_rate_uah", "").strip()
    if raw_rate:
        try:
            v = float(raw_rate)
            if v <= 0:
                errors["eur_rate_uah"] = "Курс EUR/UAH должен быть больше 0."
        except (ValueError, TypeError):
            errors["eur_rate_uah"] = "Курс EUR/UAH должен быть числом."

    raw_min = form.get("min_margin_uah", "").strip()
    if raw_min:
        try:
            v = float(raw_min)
            if v < 0:
                errors["min_margin_uah"] = "Мин. маржа не может быть отрицательной."
        except (ValueError, TypeError):
            errors["min_margin_uah"] = "Мин. маржа должна быть числом."

    raw_cost = form.get("cost_rate", "").strip()
    if raw_cost:
        try:
            v = float(raw_cost)
            if v <= 0 or v >= 1:
                errors["cost_rate"] = "Доля закупки должна быть в диапазоне (0, 1)."
        except (ValueError, TypeError):
            errors["cost_rate"] = "Доля закупки должна быть числом."

    return errors


def _parse_brand_discounts_form(form) -> list[tuple[str, float]]:
    """Pull parallel brand_name[] + brand_discount[] arrays from the form.

    Drops blank rows. Raises ValueError with a human message on any malformed
    discount value so the caller can surface it as a form error.
    """
    names = form.getlist("brand_name[]")
    discounts = form.getlist("brand_discount[]")
    rows: list[tuple[str, float]] = []
    for raw_brand, raw_disc in zip(names, discounts):
        brand = (raw_brand or "").strip()
        if not brand and not (raw_disc or "").strip():
            continue  # blank row — user added then left empty
        if not brand:
            raise ValueError("Название бренда не может быть пустым.")
        try:
            d = float(raw_disc)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Скидка для '{brand}' должна быть числом.") from exc
        if d < 0 or d > 100:
            raise ValueError(f"Скидка для '{brand}' должна быть от 0 до 100.")
        rows.append((brand, d))
    # dedupe on lowercased brand, last-write-wins (matches DB UNIQUE semantics)
    seen: dict[str, tuple[str, float]] = {}
    for brand, d in rows:
        seen[brand.strip().lower()] = (brand, d)
    return list(seen.values())


def _replace_brand_discounts(supplier: Supplier, rows: list[tuple[str, float]]) -> None:
    """Replace supplier.brand_discounts with the given rows (delete-then-insert)."""
    for existing in list(supplier.brand_discounts):
        db.session.delete(existing)
    db.session.flush()
    for brand, pct in rows:
        db.session.add(
            SupplierBrandDiscount(
                supplier_id=supplier.id,
                brand=brand,
                discount_percent=pct,
            )
        )
