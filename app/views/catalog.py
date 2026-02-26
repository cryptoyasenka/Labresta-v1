"""Catalog import and listing blueprint."""

import os
import tempfile

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from sqlalchemy import func

from app.extensions import db
from app.models.catalog import PromProduct
from app.services.catalog_import import parse_catalog_file, save_catalog_products

catalog_bp = Blueprint("catalog", __name__)

ALLOWED_EXTENSIONS = {"csv", "xls", "xlsx"}


def _allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@catalog_bp.route("/")
def catalog_list():
    """List imported products with search and pagination."""
    page = request.args.get("page", 1, type=int)
    per_page = 50
    q = request.args.get("q", "").strip()

    query = db.select(PromProduct).order_by(PromProduct.id.desc())

    if q:
        query = query.where(PromProduct.name.ilike(f"%{q}%"))

    # Count total matching
    count_query = db.select(func.count()).select_from(PromProduct)
    if q:
        count_query = count_query.where(PromProduct.name.ilike(f"%{q}%"))
    total = db.session.execute(count_query).scalar()

    # Paginate
    offset = (page - 1) * per_page
    products = db.session.execute(query.offset(offset).limit(per_page)).scalars().all()

    total_pages = (total + per_page - 1) // per_page if total > 0 else 1

    return render_template(
        "catalog/list.html",
        products=products,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages,
        q=q,
    )


@catalog_bp.route("/import", methods=["GET"])
def catalog_import_form():
    """Show the file upload form."""
    return render_template("catalog/import.html")


@catalog_bp.route("/import", methods=["POST"])
def catalog_import_upload():
    """Handle file upload, parse, and upsert products."""
    if "file" not in request.files:
        flash("No file selected.", "danger")
        return redirect(url_for("catalog.catalog_import_form"))

    file = request.files["file"]

    if file.filename == "" or file.filename is None:
        flash("No file selected.", "danger")
        return redirect(url_for("catalog.catalog_import_form"))

    if not _allowed_file(file.filename):
        flash(
            "Unsupported file format. Please upload a .csv, .xls, or .xlsx file.",
            "danger",
        )
        return redirect(url_for("catalog.catalog_import_form"))

    # Save to temp file
    tmp = None
    try:
        suffix = "." + file.filename.rsplit(".", 1)[1].lower()
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        file.save(tmp)
        tmp.close()

        # Parse and save
        products = parse_catalog_file(tmp.name, file.filename)
        result = save_catalog_products(products)

        flash(
            f"Imported {result['total']} products "
            f"({result['created']} new, {result['updated']} updated, "
            f"{result['skipped']} skipped).",
            "success",
        )
        return redirect(url_for("catalog.catalog_list"))

    except ValueError as e:
        flash(f"Import error: {e}", "danger")
        return redirect(url_for("catalog.catalog_import_form"))

    except Exception as e:
        flash(f"Unexpected error: {e}", "danger")
        return redirect(url_for("catalog.catalog_import_form"))

    finally:
        if tmp and os.path.exists(tmp.name):
            os.unlink(tmp.name)
