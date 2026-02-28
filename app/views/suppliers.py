import logging

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from sqlalchemy import select

from app.extensions import db
from app.models.supplier import Supplier
from app.services.feed_fetcher import fetch_feed
from app.services.feed_parser import parse_supplier_feed, save_supplier_products

logger = logging.getLogger(__name__)

suppliers_bp = Blueprint("suppliers", __name__)


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

        supplier = Supplier(
            name=request.form["name"].strip(),
            feed_url=request.form["feed_url"].strip(),
            discount_percent=float(request.form.get("discount_percent", 0)),
        )
        db.session.add(supplier)
        db.session.commit()
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
        supplier.feed_url = request.form["feed_url"].strip()
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


@suppliers_bp.route("/<int:supplier_id>/fetch", methods=["POST"])
@login_required
def supplier_fetch(supplier_id):
    supplier = db.session.get(Supplier, supplier_id)
    if not supplier:
        flash("Поставщик не найден.", "error")
        return redirect(url_for("suppliers.supplier_list"))

    try:
        raw_bytes = fetch_feed(supplier.feed_url)
        products = parse_supplier_feed(raw_bytes, supplier.id)
        result = save_supplier_products(products)
        flash(
            f"Фид загружен: {result['total']} товаров "
            f"({result['created']} новых, {result['updated']} обновлено).",
            "success",
        )
    except Exception as e:
        logger.exception("Feed fetch failed for supplier %s", supplier.name)
        flash(f"Ошибка загрузки фида: {e}", "error")

    return redirect(url_for("suppliers.supplier_list"))


def _validate_supplier_form(form):
    """Validate supplier form data. Returns dict of field -> error message, or empty dict."""
    errors = {}
    if not form.get("name", "").strip():
        errors["name"] = "Название обязательно."
    if not form.get("feed_url", "").strip():
        errors["feed_url"] = "URL фида обязателен."

    discount = form.get("discount_percent", "0")
    try:
        val = float(discount)
        if val < 0 or val > 100:
            errors["discount_percent"] = "Скидка должна быть от 0 до 100."
    except (ValueError, TypeError):
        errors["discount_percent"] = "Скидка должна быть числом."

    return errors
