"""Authentication blueprint: login, logout routes."""

from datetime import datetime, timezone
from urllib.parse import urlparse

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.extensions import db
from app.models.user import User

auth_bp = Blueprint("auth", __name__)


def _is_safe_next(target: str | None) -> bool:
    """True only for same-site path-absolute URLs (e.g. ``/matches/?x=1``).

    Guards the post-login redirect against an open-redirect: a crafted
    ``?next=https://evil.com`` (or protocol-relative ``//evil.com``) must not
    bounce the operator off-site. We only ever generate local ``next`` targets,
    so anything with a scheme or host is rejected outright.
    """
    if not target or not target.startswith("/") or target.startswith("//"):
        return False
    parsed = urlparse(target)
    return not parsed.scheme and not parsed.netloc


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        remember = bool(request.form.get("remember"))

        user = db.session.execute(
            db.select(User).where(User.email == email)
        ).scalar_one_or_none()

        if user and user.check_password(password):
            login_user(user, remember=remember)
            user.last_login_at = datetime.now(timezone.utc)
            db.session.commit()

            next_page = request.args.get("next")
            if not _is_safe_next(next_page):
                next_page = None
            return redirect(next_page or url_for("main.index"))

        flash("Неверный email или пароль", "danger")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Вы вышли из системы", "success")
    return redirect(url_for("auth.login"))
