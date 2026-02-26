from flask import Blueprint

catalog_bp = Blueprint("catalog", __name__)


@catalog_bp.route("/")
def catalog_index():
    return "Catalog import - coming soon"
