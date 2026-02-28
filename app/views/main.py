from flask import Blueprint, render_template
from flask_login import login_required

from app.extensions import db
from app.models.catalog import PromProduct
from app.models.supplier import Supplier

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@login_required
def index():
    total_suppliers = db.session.query(Supplier).count()
    enabled_suppliers = db.session.query(Supplier).filter_by(is_enabled=True).count()
    catalog_count = db.session.query(PromProduct).count()

    return render_template(
        "index.html",
        total_suppliers=total_suppliers,
        enabled_suppliers=enabled_suppliers,
        catalog_count=catalog_count,
    )
