"""Feed endpoints — public YML serving + authenticated custom-feed management.

Public (no auth, Horoshop fetches these):
  /feed/yml                       — main feed: all suppliers
  /feed/yml/supplier/<slug>       — per-supplier feed
  /feed/yml/custom/<token>        — ad-hoc selection feed
  /feed/prices.yml                — narrow: price-only (legacy CLI use)
  /feed/availability.yml          — narrow: availability-only (legacy CLI use)

Authenticated:
  /feeds/custom                   — list registered custom feeds
  /feeds/custom/<token>/delete    — POST: drop file + registry row
"""

import re

from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    send_from_directory,
    url_for,
)
from flask_login import login_required
from sqlalchemy import select

from app.extensions import db
from app.models.custom_feed import CustomFeed
from app.models.supplier import Supplier
from app.services.yml_generator import delete_custom_feed

feed_bp = Blueprint("feed", __name__)

_SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,49}$")
_TOKEN_RE = re.compile(r"^[0-9a-f]{12}$")


def _serve_file(filename: str):
    yml_dir = current_app.config["YML_OUTPUT_DIR"]
    try:
        return send_from_directory(yml_dir, filename, mimetype="application/xml")
    except FileNotFoundError:
        abort(404)


def _serve_config(config_key: str):
    return _serve_file(current_app.config[config_key])


@feed_bp.route("/feed/yml")
def serve_yml():
    """Full main feed — public, no auth."""
    return _serve_config("YML_FILENAME")


@feed_bp.route("/feed/yml/supplier/<slug>")
def serve_supplier_yml(slug: str):
    """Per-supplier feed at labresta-feed-<slug>.yml — public, no auth."""
    if not _SLUG_RE.match(slug):
        abort(404)
    exists = db.session.execute(
        select(Supplier.id).where(Supplier.slug == slug)
    ).first()
    if exists is None:
        abort(404)
    return _serve_file(f"labresta-feed-{slug}.yml")


@feed_bp.route("/feed/yml/custom/<token>")
def serve_custom_yml(token: str):
    """Custom-selection feed at labresta-feed-custom-<token>.yml — public, no auth."""
    if not _TOKEN_RE.match(token):
        abort(404)
    cf = db.session.execute(
        select(CustomFeed).where(CustomFeed.token == token)
    ).scalar_one_or_none()
    if cf is None:
        abort(404)
    return _serve_file(cf.filename)


@feed_bp.route("/feed/prices.yml")
def serve_prices_yml():
    """Narrow price-only feed — public, no auth."""
    return _serve_config("YML_PRICES_FILENAME")


@feed_bp.route("/feed/availability.yml")
def serve_availability_yml():
    """Narrow availability-only feed — public, no auth."""
    return _serve_config("YML_AVAILABILITY_FILENAME")


@feed_bp.route("/feeds/custom")
@login_required
def custom_feeds_list():
    """List registered custom feeds with delete actions."""
    feeds = db.session.execute(
        select(CustomFeed).order_by(CustomFeed.created_at.desc())
    ).scalars().all()
    return render_template("feeds/custom_list.html", feeds=feeds)


@feed_bp.route("/feeds/custom/<token>/delete", methods=["POST"])
@login_required
def custom_feed_delete(token: str):
    """Drop the YML file and the CustomFeed row, then redirect to the list."""
    if not _TOKEN_RE.match(token):
        abort(404)
    deleted = delete_custom_feed(token)
    if deleted:
        flash(f"Кастомный фид {token} удалён.", "success")
    else:
        flash(f"Кастомный фид {token} не найден.", "error")
    return redirect(url_for("feed.custom_feeds_list"))
