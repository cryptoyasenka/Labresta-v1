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

import io
import os
import re
import tempfile
from datetime import datetime, timezone

from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    send_from_directory,
    url_for,
)
from flask_login import login_required
from sqlalchemy import func, select

from app.extensions import db
from app.models.custom_feed import CustomFeed
from app.models.product_match import ProductMatch
from app.models.supplier import Supplier
from app.models.supplier_product import SupplierProduct
from app.services.audit_service import log_action
from app.services.feed_fetcher import fetch_feed_with_retry
from app.services.np_horoshop_file import NP_SUPPLIER_SLUG, build_np_file
from app.services.yml_generator import delete_custom_feed

feed_bp = Blueprint("feed", __name__)

_SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,49}$")
_TOKEN_RE = re.compile(r"^[0-9a-f]{12}$")


def _serve_file(filename: str, *, label: str):
    """Serve a YML from YML_OUTPUT_DIR or render a friendly 'not built yet' page.

    The page is HTML (status 404) so a person opening the URL in a browser sees
    instructions instead of a blank Werkzeug error. For Horoshop and other bots
    the 404 status still signals 'no feed', which is the correct semantics.
    """
    yml_dir = current_app.config["YML_OUTPUT_DIR"]
    if not os.path.isfile(os.path.join(yml_dir, filename)):
        return render_template(
            "feeds/missing.html",
            filename=filename,
            label=label,
        ), 404
    return send_from_directory(yml_dir, filename, mimetype="application/xml")


@feed_bp.route("/feed/yml")
def serve_yml():
    """Full main feed — public, no auth."""
    return _serve_file(current_app.config["YML_FILENAME"], label="главный фид")


@feed_bp.route("/feed/yml/supplier/<slug>")
def serve_supplier_yml(slug: str):
    """Per-supplier feed at labresta-feed-<slug>.yml — public, no auth."""
    if not _SLUG_RE.match(slug):
        abort(404)
    supplier = db.session.execute(
        select(Supplier).where(Supplier.slug == slug)
    ).scalar_one_or_none()
    if supplier is None:
        abort(404)
    return _serve_file(
        f"labresta-feed-{slug}.yml",
        label=f"фид поставщика {supplier.name}",
    )


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
    return _serve_file(
        cf.filename,
        label=f"кастомный фид «{cf.name or cf.token}»",
    )


@feed_bp.route("/feed/prices.yml")
def serve_prices_yml():
    """Narrow price-only feed — public, no auth."""
    return _serve_file(current_app.config["YML_PRICES_FILENAME"], label="фид цен")


@feed_bp.route("/feed/availability.yml")
def serve_availability_yml():
    """Narrow availability-only feed — public, no auth."""
    return _serve_file(
        current_app.config["YML_AVAILABILITY_FILENAME"],
        label="фид наличия",
    )


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


# ========== НП exclusive-brands → native Horoshop content file (Channel 2) ==========
# The operator ticks brands, clicks generate; we fetch the live NP feed, join it
# with the matcher DB and hand back a native-schema XLSX to import by hand into
# Horoshop (description UA/RU + photo + price + availability). The live import
# stays Yana's hand (invariant #13) — we only produce the file.

# The 9 exclusive «Новый проект» brands (latin labels as they appear in the feed).
NP_BRANDS = [
    "HURAKAN", "APACH", "FAGOR", "TATRA", "COLD",
    "PROJECT SYSTEMS", "ASTORIA", "ARRIS", "MAXIMA",
]


def _np_supplier_or_none():
    return db.session.execute(
        select(Supplier).where(Supplier.slug == NP_SUPPLIER_SLUG)
    ).scalar_one_or_none()


def _np_brand_match_counts(supplier_id: int) -> dict[str, int]:
    """Indicative per-brand count of NP published matches — DB only, no feed
    fetch (so the page loads instantly). The exact, feed-joined numbers come
    back in the manifest after generation."""
    rows = db.session.execute(
        select(SupplierProduct.brand, func.count(ProductMatch.id))
        .join(ProductMatch, ProductMatch.supplier_product_id == SupplierProduct.id)
        .where(
            SupplierProduct.supplier_id == supplier_id,
            ProductMatch.status.in_(("confirmed", "manual")),
            ProductMatch.published.is_(True),
        )
        .group_by(SupplierProduct.brand)
    ).all()
    by_norm: dict[str, int] = {}
    for brand, cnt in rows:
        key = (brand or "").strip().lower()
        by_norm[key] = by_norm.get(key, 0) + cnt
    return {b: by_norm.get(b.strip().lower(), 0) for b in NP_BRANDS}


@feed_bp.route("/feeds/np")
@login_required
def np_file_page():
    """Brand-picker page for the NP Horoshop content file."""
    supplier = _np_supplier_or_none()
    counts = _np_brand_match_counts(supplier.id) if supplier else {b: 0 for b in NP_BRANDS}
    return render_template(
        "feeds/np.html",
        brands=NP_BRANDS,
        counts=counts,
        supplier=supplier,
    )


@feed_bp.route("/feeds/np/generate", methods=["POST"])
@login_required
def np_file_generate():
    """Fetch the live NP feed, build the native Horoshop XLSX for the ticked
    brands, and return it as a download."""
    supplier = _np_supplier_or_none()
    if supplier is None:
        flash("Постачальник «Новий проект» не знайдений.", "error")
        return redirect(url_for("feed.np_file_page"))
    if not supplier.feed_url:
        flash("У постачальника «Новий проект» не вказано feed_url.", "error")
        return redirect(url_for("feed.np_file_page"))

    selected = request.form.getlist("brands")
    if not selected:
        flash("Оберіть хоча б один бренд.", "error")
        return redirect(url_for("feed.np_file_page"))

    # Download the live NP feed to a temp file — build_np_file is pure over a
    # local path, keeping the network out of the builder (and its tests).
    try:
        raw = fetch_feed_with_retry(supplier.feed_url)
    except Exception as exc:  # network / HTTP / SSRF guard
        flash(f"Не вдалося завантажити фід НП: {exc}", "error")
        return redirect(url_for("feed.np_file_page"))

    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
            tmp.write(raw)
            tmp_path = tmp.name
        xlsx_bytes, manifest = build_np_file(selected, tmp_path)
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)

    log_action("np_file_generate", details={
        "brands": selected,
        "total": manifest.get("total"),
        "with_photo": manifest.get("with_photo"),
        "no_photo": manifest.get("no_photo"),
        "unmatched": manifest.get("unmatched"),
        "missing_feed_row": manifest.get("missing_feed_row"),
        "skipped_no_price": manifest.get("skipped_no_price"),
    })
    db.session.commit()

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M")
    return send_file(
        io.BytesIO(xlsx_bytes),
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name=f"np-horoshop-{stamp}.xlsx",
    )
