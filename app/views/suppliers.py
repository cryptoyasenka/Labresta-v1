from flask import Blueprint

suppliers_bp = Blueprint("suppliers", __name__)


@suppliers_bp.route("/")
def supplier_list():
    return "Suppliers - coming soon"
