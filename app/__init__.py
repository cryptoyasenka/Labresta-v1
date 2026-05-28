import os

from flask import Flask, jsonify, request
from flask_wtf.csrf import CSRFError
from werkzeug.middleware.proxy_fix import ProxyFix

from app.extensions import configure_sqlite_wal, csrf, db, login_manager


def _wants_json_response() -> bool:
    """AJAX requests should get JSON errors, not HTML error pages.

    Our fetchWithCSRF wrapper always sends X-CSRFToken + Content-Type: application/json,
    so either signal is enough. Also check Accept header for explicit XHRs.
    """
    if request.headers.get("X-CSRFToken"):
        return True
    if request.is_json:
        return True
    accept = request.accept_mimetypes
    return accept.best == "application/json" or (
        accept["application/json"] > accept["text/html"]
    )


def _secret_key_is_insecure(uri: str, secret_key: str, is_testing: bool) -> bool:
    """True when the app must refuse to boot: a production deployment (Postgres
    on Railway — local dev uses sqlite) still signing sessions and CSRF tokens
    with the publicly-known placeholder key, which makes them forgeable. Tests
    and local sqlite dev keep the default harmlessly."""
    if is_testing:
        return False
    return uri.startswith("postgresql") and secret_key == "dev-key-change-me"


def create_app(config_name="default"):
    app = Flask(__name__, instance_relative_config=True)

    # Trust Railway's reverse proxy for HTTPS scheme + correct host in url_for(_external=True)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # Ensure instance folder exists (Windows-safe, see Research Pitfall 4)
    os.makedirs(app.instance_path, exist_ok=True)

    # Load config
    if config_name == "default":
        app.config.from_object("app.config.DefaultConfig")
    else:
        app.config.from_object(f"app.config.{config_name}")

    # SAFETY: refuse to bind a test app to the production DB.
    # Overriding SQLALCHEMY_DATABASE_URI after db.init_app() has no effect —
    # the engine is already bound. Tests that forget to pass an in-memory URI
    # before create_app() would silently wipe instance/labresta.db on cleanup.
    is_testing = os.environ.get("TESTING") == "1" or app.config.get("TESTING")
    if is_testing:
        uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
        if ":memory:" not in uri and "labresta.db" in uri:
            raise RuntimeError(
                f"Refusing to bind test app to production DB: {uri}. "
                "Set SQLALCHEMY_DATABASE_URI to 'sqlite:///:memory:' in the "
                "config BEFORE calling create_app()."
            )

    # SAFETY: refuse to boot a production (Postgres) app with the placeholder
    # SECRET_KEY — sessions and CSRF tokens would be forgeable.
    if _secret_key_is_insecure(
        app.config.get("SQLALCHEMY_DATABASE_URI", ""),
        app.config.get("SECRET_KEY", ""),
        is_testing,
    ):
        raise RuntimeError(
            "SECRET_KEY is the insecure default 'dev-key-change-me' on a "
            "production (Postgres) deployment. Set the SECRET_KEY environment "
            "variable — sessions and CSRF tokens are forgeable otherwise."
        )

    # Init extensions
    db.init_app(app)
    if app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite"):
        configure_sqlite_wal(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User

        return db.session.get(User, int(user_id))

    # Register blueprints
    from app.views.auth import auth_bp
    from app.views.catalog import catalog_bp
    from app.views.dashboard import dashboard_bp
    from app.views.feed import feed_bp
    from app.views.logs import logs_bp
    from app.views.main import main_bp
    from app.views.matches import matches_bp
    from app.views.products import products_bp
    from app.views.audit import audit_bp
    from app.views.settings import settings_bp
    from app.views.suppliers import suppliers_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(suppliers_bp, url_prefix="/suppliers")
    app.register_blueprint(catalog_bp, url_prefix="/catalog")
    app.register_blueprint(feed_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(matches_bp, url_prefix="/matches")
    app.register_blueprint(products_bp, url_prefix="/products")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
    app.register_blueprint(logs_bp, url_prefix="/logs")
    app.register_blueprint(audit_bp, url_prefix="/audit")
    app.register_blueprint(settings_bp, url_prefix="/settings")

    # Initialize scheduler (before CLI, after blueprints)
    from app.scheduler import init_scheduler

    init_scheduler(app)

    # JSON error handlers for AJAX endpoints (avoids the opaque
    # "Unexpected token '<'" JSON.parse crash in the client when the
    # server would otherwise return an HTML error page).
    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        if _wants_json_response():
            return jsonify({
                "status": "error",
                "code": "csrf_invalid",
                "message": "Сессия устарела, обновите страницу (Ctrl+F5).",
            }), 400
        return e.description, 400

    @app.errorhandler(404)
    def handle_not_found(e):
        if _wants_json_response():
            return jsonify({
                "status": "error",
                "code": "not_found",
                "message": "Объект не найден. Обновите страницу — список мог измениться.",
            }), 404
        return e, 404

    @app.errorhandler(500)
    def handle_server_error(e):
        if _wants_json_response():
            return jsonify({
                "status": "error",
                "code": "server_error",
                "message": "Внутренняя ошибка сервера. Посмотрите логи.",
            }), 500
        return e, 500

    # Register CLI commands
    from app.cli import create_admin_command, flag_orphans_command, sync_command

    app.cli.add_command(sync_command)
    app.cli.add_command(create_admin_command)
    app.cli.add_command(flag_orphans_command)

    # Context processor for pending review badge count
    @app.context_processor
    def inject_pending_review_count():
        from flask_login import current_user

        if current_user.is_authenticated:
            from sqlalchemy import func, select

            from app.models.product_match import ProductMatch

            # Exclude "dead" candidates — prom_product already claimed by a
            # confirmed/manual match (backend refuses to confirm them anyway).
            # Mirrors the hide-claimed filter on the matches review page.
            claimed_pp_ids = select(ProductMatch.prom_product_id).where(
                ProductMatch.status.in_(("confirmed", "manual"))
            )
            count = (
                db.session.execute(
                    select(func.count(ProductMatch.id)).where(
                        ProductMatch.status == "candidate",
                        ProductMatch.prom_product_id.not_in(claimed_pp_ids),
                    )
                ).scalar()
                or 0
            )
            deletion_count = (
                db.session.execute(
                    select(func.count(ProductMatch.id)).where(
                        ProductMatch.deletion_candidate == True  # noqa: E712
                    )
                ).scalar()
                or 0
            )
            # Unread notification count for navbar bell
            from app.services.notification_service import get_unread_count

            unread_count = get_unread_count()
            return {
                "pending_review_count": count,
                "deletion_candidate_count": deletion_count,
                "unread_notification_count": unread_count,
            }
        return {"pending_review_count": 0, "deletion_candidate_count": 0, "unread_notification_count": 0}

    # Ensure all models are registered with SQLAlchemy before create_all.
    # Importing the package runs app/models/__init__.py, which imports every
    # model module for its registration side effect. Bind to an alias: a bare
    # `import app.models` would rebind the local name `app` (this function's
    # Flask instance) to the `app` package module, breaking the
    # `app.app_context()` call immediately below.
    import app.models as _models  # noqa: F401

    # Create tables on first run
    with app.app_context():
        db.create_all()

    return app
