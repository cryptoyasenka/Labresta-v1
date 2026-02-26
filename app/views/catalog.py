from flask import Blueprint, render_template

catalog_bp = Blueprint("catalog", __name__)


@catalog_bp.route("/")
def catalog_index():
    return render_template("catalog/index.html")
