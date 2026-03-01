"""Settings blueprint: user management CRUD, sync config, and notifications."""

from functools import wraps

from flask import Blueprint, abort, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import select

from app.extensions import db
from app.models.notification_rule import NotificationRule, Notification
from app.models.user import User
from app.services.notification_service import (
    get_recent_notifications,
    get_unread_notifications,
    mark_notifications_read,
)

settings_bp = Blueprint("settings", __name__)


def admin_required(f):
    """Decorator to restrict access to admin users only."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)

    return decorated_function


# --- User Management ---


@settings_bp.route("/users")
@login_required
@admin_required
def user_list():
    """User list (admin only)."""
    users = db.session.execute(
        select(User).order_by(User.created_at.desc())
    ).scalars().all()
    return render_template("settings/users.html", users=users)


@settings_bp.route("/users/create", methods=["POST"])
@login_required
@admin_required
def user_create():
    """Create a new user (admin only)."""
    email = request.form.get("email", "").strip().lower()
    name = request.form.get("name", "").strip()
    password = request.form.get("password", "")
    role = request.form.get("role", "operator")

    # Validation
    if not email or not name or not password:
        flash("Все поля обязательны", "danger")
        return redirect(url_for("settings.user_list"))

    if len(password) < 8:
        flash("Пароль должен быть не менее 8 символов", "danger")
        return redirect(url_for("settings.user_list"))

    if role not in ("admin", "operator"):
        flash("Недопустимая роль", "danger")
        return redirect(url_for("settings.user_list"))

    # Check email uniqueness
    existing = db.session.execute(
        select(User).where(User.email == email)
    ).scalar_one_or_none()
    if existing:
        flash(f"Пользователь с email {email} уже существует", "danger")
        return redirect(url_for("settings.user_list"))

    user = User(email=email, name=name, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    flash(f"Пользователь {name} создан", "success")
    return redirect(url_for("settings.user_list"))


@settings_bp.route("/users/<int:user_id>/edit", methods=["POST"])
@login_required
@admin_required
def user_edit(user_id):
    """Edit user details (admin only)."""
    user = db.session.get(User, user_id)
    if not user:
        abort(404)

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    role = request.form.get("role", user.role)

    if not name or not email:
        flash("Имя и email обязательны", "danger")
        return redirect(url_for("settings.user_list"))

    if role not in ("admin", "operator"):
        flash("Недопустимая роль", "danger")
        return redirect(url_for("settings.user_list"))

    # Prevent admin from demoting themselves if they're the last admin
    if user.id == current_user.id and role != "admin":
        admin_count = db.session.execute(
            select(db.func.count(User.id)).where(
                User.role == "admin", User.is_active == True  # noqa: E712
            )
        ).scalar() or 0
        if admin_count <= 1:
            flash("Нельзя снять роль администратора — вы единственный админ", "danger")
            return redirect(url_for("settings.user_list"))

    # Check email uniqueness (exclude current user)
    existing = db.session.execute(
        select(User).where(User.email == email, User.id != user.id)
    ).scalar_one_or_none()
    if existing:
        flash(f"Email {email} уже используется другим пользователем", "danger")
        return redirect(url_for("settings.user_list"))

    user.name = name
    user.email = email
    user.role = role
    db.session.commit()

    flash(f"Пользователь {name} обновлён", "success")
    return redirect(url_for("settings.user_list"))


@settings_bp.route("/users/<int:user_id>/password", methods=["POST"])
@login_required
@admin_required
def user_password(user_id):
    """Change user password (admin only)."""
    user = db.session.get(User, user_id)
    if not user:
        abort(404)

    password = request.form.get("password", "")
    if len(password) < 8:
        flash("Пароль должен быть не менее 8 символов", "danger")
        return redirect(url_for("settings.user_list"))

    user.set_password(password)
    db.session.commit()

    flash(f"Пароль для {user.name} изменён", "success")
    return redirect(url_for("settings.user_list"))


@settings_bp.route("/users/<int:user_id>/toggle", methods=["POST"])
@login_required
@admin_required
def user_toggle(user_id):
    """Toggle user active/inactive (admin only)."""
    user = db.session.get(User, user_id)
    if not user:
        abort(404)

    # Prevent deactivating self
    if user.id == current_user.id:
        flash("Нельзя деактивировать свой аккаунт", "danger")
        return redirect(url_for("settings.user_list"))

    user.is_active = not user.is_active
    db.session.commit()

    status = "активирован" if user.is_active else "деактивирован"
    flash(f"Пользователь {user.name} {status}", "success")
    return redirect(url_for("settings.user_list"))


# --- Sync Settings ---


@settings_bp.route("/sync")
@login_required
@admin_required
def sync_settings():
    """Sync settings view (admin only, read-only for MVP)."""
    from app.models.supplier import Supplier

    suppliers = db.session.execute(
        select(Supplier).order_by(Supplier.name)
    ).scalars().all()

    # Matching thresholds from matcher module
    from app.services.matcher import (
        CONFIDENCE_HIGH,
        CONFIDENCE_MEDIUM,
        MAX_PRICE_RATIO,
        SCORE_CUTOFF,
    )

    config = {
        "sync_interval_hours": 4,
        "misfire_grace_time": 900,
        "confidence_high": CONFIDENCE_HIGH,
        "confidence_medium": CONFIDENCE_MEDIUM,
        "score_cutoff": SCORE_CUTOFF,
        "max_price_ratio": MAX_PRICE_RATIO,
    }

    return render_template(
        "settings/sync.html",
        suppliers=suppliers,
        config=config,
    )


# --- Notification Settings ---


@settings_bp.route("/notifications")
@login_required
def notifications():
    """Notification page: full management for admin, list-only for operator."""
    recent = get_recent_notifications(limit=50)
    if current_user.is_admin:
        rules = db.session.execute(
            select(NotificationRule).order_by(NotificationRule.created_at.desc())
        ).scalars().all()
        return render_template(
            "settings/notifications.html",
            rules=rules,
            recent_notifications=recent,
        )
    # Operator: simplified view — notification list only, no rule management
    return render_template(
        "settings/notifications_operator.html",
        recent_notifications=recent,
    )


@settings_bp.route("/notifications/create", methods=["POST"])
@login_required
@admin_required
def notification_rule_create():
    """Create a new notification rule."""
    name = request.form.get("name", "").strip()
    criteria_type = request.form.get("criteria_type", "").strip()
    criteria_value = request.form.get("criteria_value", "").strip()
    telegram_enabled = request.form.get("telegram_enabled") == "on"
    ui_enabled = request.form.get("ui_enabled") == "on"

    # Validation
    if not name or not criteria_type or not criteria_value:
        flash("Все поля обязательны", "danger")
        return redirect(url_for("settings.notifications"))

    valid_types = ("keyword", "brand", "price_range", "category")
    if criteria_type not in valid_types:
        flash(f"Недопустимый тип критерия: {criteria_type}", "danger")
        return redirect(url_for("settings.notifications"))

    rule = NotificationRule(
        name=name,
        criteria_type=criteria_type,
        criteria_value=criteria_value,
        telegram_enabled=telegram_enabled,
        ui_enabled=ui_enabled,
        created_by=current_user.name,
    )
    db.session.add(rule)
    db.session.commit()

    flash(f"Правило \"{name}\" создано", "success")
    return redirect(url_for("settings.notifications"))


@settings_bp.route("/notifications/<int:rule_id>/edit", methods=["POST"])
@login_required
@admin_required
def notification_rule_edit(rule_id):
    """Edit an existing notification rule."""
    rule = db.session.get(NotificationRule, rule_id)
    if not rule:
        abort(404)

    name = request.form.get("name", "").strip()
    criteria_type = request.form.get("criteria_type", "").strip()
    criteria_value = request.form.get("criteria_value", "").strip()
    telegram_enabled = request.form.get("telegram_enabled") == "on"
    ui_enabled = request.form.get("ui_enabled") == "on"
    is_active = request.form.get("is_active") == "on"

    if not name or not criteria_type or not criteria_value:
        flash("Все поля обязательны", "danger")
        return redirect(url_for("settings.notifications"))

    valid_types = ("keyword", "brand", "price_range", "category")
    if criteria_type not in valid_types:
        flash(f"Недопустимый тип критерия: {criteria_type}", "danger")
        return redirect(url_for("settings.notifications"))

    rule.name = name
    rule.criteria_type = criteria_type
    rule.criteria_value = criteria_value
    rule.telegram_enabled = telegram_enabled
    rule.ui_enabled = ui_enabled
    rule.is_active = is_active
    db.session.commit()

    flash(f"Правило \"{name}\" обновлено", "success")
    return redirect(url_for("settings.notifications"))


@settings_bp.route("/notifications/<int:rule_id>/delete", methods=["POST"])
@login_required
@admin_required
def notification_rule_delete(rule_id):
    """Soft-delete a notification rule (set is_active=False)."""
    rule = db.session.get(NotificationRule, rule_id)
    if not rule:
        abort(404)

    rule.is_active = False
    db.session.commit()

    flash(f"Правило \"{rule.name}\" деактивировано", "success")
    return redirect(url_for("settings.notifications"))


@settings_bp.route("/notifications/toggle-telegram", methods=["POST"])
@login_required
@admin_required
def toggle_telegram():
    """Toggle Telegram notifications globally for all active rules."""
    # Get current state: if any rule has telegram on, turn all off; else turn all on
    active_rules = db.session.execute(
        select(NotificationRule).where(NotificationRule.is_active == True)  # noqa: E712
    ).scalars().all()

    any_enabled = any(r.telegram_enabled for r in active_rules)
    new_state = not any_enabled

    for rule in active_rules:
        rule.telegram_enabled = new_state
    db.session.commit()

    status = "включены" if new_state else "отключены"
    flash(f"Telegram-уведомления {status}", "success")
    return redirect(url_for("settings.notifications"))


# --- Notification API endpoints ---


@settings_bp.route("/api/notifications/unread")
@login_required
def api_notifications_unread():
    """JSON endpoint for navbar notification badge polling."""
    notifications = get_unread_notifications(limit=10)
    return jsonify([
        {
            "id": n.id,
            "message": n.message,
            "created_at": n.created_at.strftime("%d.%m.%Y %H:%M") if n.created_at else "",
            "is_read": n.is_read,
        }
        for n in notifications
    ])


@settings_bp.route("/api/notifications/mark-read", methods=["POST"])
@login_required
def api_notifications_mark_read():
    """Mark notifications as read."""
    data = request.get_json(silent=True) or {}
    ids = data.get("ids", [])
    if not ids:
        return jsonify({"error": "No IDs provided"}), 400

    count = mark_notifications_read(ids)
    return jsonify({"marked": count})
