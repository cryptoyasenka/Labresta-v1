"""Public feed endpoint — serves generated YML without authentication."""

from flask import Blueprint, abort, current_app, send_from_directory

feed_bp = Blueprint("feed", __name__)


@feed_bp.route("/feed/yml")
def serve_yml():
    """Serve the generated YML feed — public, no auth required."""
    yml_dir = current_app.config["YML_OUTPUT_DIR"]
    yml_file = current_app.config["YML_FILENAME"]
    try:
        return send_from_directory(yml_dir, yml_file, mimetype="application/xml")
    except FileNotFoundError:
        abort(404)
