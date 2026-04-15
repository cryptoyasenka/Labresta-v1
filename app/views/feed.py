"""Public feed endpoints — serve generated YML files without authentication.

Three flavors:
  /feed/yml             — full catalog (price + availability + name + description)
  /feed/prices.yml      — narrow: price-only (Horoshop config decides scope)
  /feed/availability.yml — narrow: availability-only

Horoshop fetches these URLs on schedule; operator triggers regen via UI.
"""

from flask import Blueprint, abort, current_app, send_from_directory

feed_bp = Blueprint("feed", __name__)


def _serve(config_key: str):
    yml_dir = current_app.config["YML_OUTPUT_DIR"]
    yml_file = current_app.config[config_key]
    try:
        return send_from_directory(yml_dir, yml_file, mimetype="application/xml")
    except FileNotFoundError:
        abort(404)


@feed_bp.route("/feed/yml")
def serve_yml():
    """Full YML feed — public, no auth."""
    return _serve("YML_FILENAME")


@feed_bp.route("/feed/prices.yml")
def serve_prices_yml():
    """Narrow price-only feed — public, no auth."""
    return _serve("YML_PRICES_FILENAME")


@feed_bp.route("/feed/availability.yml")
def serve_availability_yml():
    """Narrow availability-only feed — public, no auth."""
    return _serve("YML_AVAILABILITY_FILENAME")
