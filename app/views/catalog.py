"""Catalog import and listing blueprint."""

import glob
import os
import re
import time
import uuid

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import login_required
from sqlalchemy import func

from app.extensions import db
from app.models.catalog import PromProduct
from app.services.catalog_import import (
    parse_catalog_file,
    preview_catalog_import,
    save_catalog_products,
)

catalog_bp = Blueprint("catalog", __name__)

ALLOWED_EXTENSIONS = {"csv", "xls", "xlsx"}

# Two-step import: the uploaded file is staged on disk between the preview and
# the confirm step, keyed by an opaque token kept in the session (never trusts a
# client-supplied path). Stale staged files are swept after this many seconds.
STAGING_SUBDIR = "import_staging"
STAGING_MAX_AGE_SECONDS = 3600
_TOKEN_RE = re.compile(r"^[0-9a-f]{32}$")


def _allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def _staging_dir() -> str:
    d = os.path.join(current_app.instance_path, STAGING_SUBDIR)
    os.makedirs(d, exist_ok=True)
    return d


def _cleanup_stale_staging() -> None:
    """Opportunistically delete staged files older than STAGING_MAX_AGE_SECONDS."""
    now = time.time()
    for path in glob.glob(os.path.join(_staging_dir(), "*")):
        try:
            if now - os.path.getmtime(path) > STAGING_MAX_AGE_SECONDS:
                os.unlink(path)
        except OSError:
            pass


def _staged_path(token: str, suffix: str) -> str | None:
    """Resolve a staged file path from a session token, or None if invalid/missing.

    The token must match our own uuid4 hex format and the suffix must be an
    allowed extension — this rules out any path traversal even though the values
    only ever come from our own session.
    """
    if not token or not _TOKEN_RE.match(token):
        return None
    if suffix.lstrip(".").lower() not in ALLOWED_EXTENSIONS:
        return None
    path = os.path.join(_staging_dir(), f"{token}{suffix}")
    return path if os.path.exists(path) else None


@catalog_bp.route("/")
@login_required
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
@login_required
def catalog_import_form():
    """Show the file upload form."""
    return render_template("catalog/import.html")


@catalog_bp.route("/import", methods=["POST"])
@login_required
def catalog_import_upload():
    """Step 1: stage the uploaded file and show a preview of what would change.

    Nothing is written to the DB here — the operator must confirm on the
    preview page. This guards against importing the wrong file by accident.
    """
    if "file" not in request.files:
        flash("Файл не выбран.", "danger")
        return redirect(url_for("catalog.catalog_import_form"))

    file = request.files["file"]

    if file.filename == "" or file.filename is None:
        flash("Файл не выбран.", "danger")
        return redirect(url_for("catalog.catalog_import_form"))

    if not _allowed_file(file.filename):
        flash(
            "Неподдерживаемый формат файла. Загрузите .csv, .xls или .xlsx файл.",
            "danger",
        )
        return redirect(url_for("catalog.catalog_import_form"))

    _cleanup_stale_staging()

    # Drop any previously staged-but-unconfirmed file for this session.
    _discard_staged()

    token = uuid.uuid4().hex
    suffix = "." + file.filename.rsplit(".", 1)[1].lower()
    staged_path = os.path.join(_staging_dir(), f"{token}{suffix}")

    try:
        file.save(staged_path)
        # Parse with a safe synthetic name so the parser only sees the extension.
        products = parse_catalog_file(staged_path, f"import{suffix}")
        preview = preview_catalog_import(products)
    except ValueError as e:
        if os.path.exists(staged_path):
            os.unlink(staged_path)
        flash(f"Ошибка разбора файла: {e}", "danger")
        return redirect(url_for("catalog.catalog_import_form"))
    except Exception as e:
        if os.path.exists(staged_path):
            os.unlink(staged_path)
        flash(f"Непредвиденная ошибка: {e}", "danger")
        return redirect(url_for("catalog.catalog_import_form"))

    session["catalog_import"] = {
        "token": token,
        "suffix": suffix,
        "filename": file.filename,
    }

    return render_template(
        "catalog/import_preview.html",
        preview=preview,
        filename=file.filename,
    )


@catalog_bp.route("/import/confirm", methods=["POST"])
@login_required
def catalog_import_confirm():
    """Step 2: re-read the staged file and actually upsert the products."""
    staged = session.get("catalog_import")
    if not staged:
        flash("Сессия импорта истекла. Загрузите файл заново.", "warning")
        return redirect(url_for("catalog.catalog_import_form"))

    path = _staged_path(staged.get("token", ""), staged.get("suffix", ""))
    if not path:
        session.pop("catalog_import", None)
        flash(
            "Загруженный файл не найден (сессия истекла). Загрузите его заново.",
            "warning",
        )
        return redirect(url_for("catalog.catalog_import_form"))

    try:
        products = parse_catalog_file(path, f"import{staged['suffix']}")
        result = save_catalog_products(products)
        flash(
            f"Импортировано {result['total']} товаров "
            f"({result['created']} новых, {result['updated']} обновлено, "
            f"{result['skipped']} пропущено).",
            "success",
        )
        return redirect(url_for("catalog.catalog_list"))
    except ValueError as e:
        flash(f"Ошибка импорта: {e}", "danger")
        return redirect(url_for("catalog.catalog_import_form"))
    except Exception as e:
        flash(f"Непредвиденная ошибка: {e}", "danger")
        return redirect(url_for("catalog.catalog_import_form"))
    finally:
        _discard_staged()


@catalog_bp.route("/import/cancel", methods=["POST"])
@login_required
def catalog_import_cancel():
    """Discard a staged-but-unconfirmed upload."""
    _discard_staged()
    flash("Импорт отменён. Ничего не изменено.", "info")
    return redirect(url_for("catalog.catalog_import_form"))


def _discard_staged() -> None:
    """Delete the session's staged file (if any) and clear the session key."""
    staged = session.pop("catalog_import", None)
    if not staged:
        return
    path = _staged_path(staged.get("token", ""), staged.get("suffix", ""))
    if path:
        try:
            os.unlink(path)
        except OSError:
            pass
