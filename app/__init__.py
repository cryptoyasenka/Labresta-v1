import os

from flask import Flask

from app.extensions import configure_sqlite_wal, csrf, db, login_manager


def create_app(config_name="default"):
    app = Flask(__name__, instance_relative_config=True)

    # Ensure instance folder exists (Windows-safe, see Research Pitfall 4)
    os.makedirs(app.instance_path, exist_ok=True)

    # Load config
    if config_name == "default":
        app.config.from_object("app.config.DefaultConfig")
    else:
        app.config.from_object(f"app.config.{config_name}")

    # Init extensions
    db.init_app(app)
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
    app.register_blueprint(settings_bp, url_prefix="/settings")

    # Initialize scheduler (before CLI, after blueprints)
    from app.scheduler import init_scheduler

    init_scheduler(app)

    # Register CLI commands
    from app.cli import create_admin_command, sync_command

    app.cli.add_command(sync_command)
    app.cli.add_command(create_admin_command)

    # Context processor for pending review badge count
    @app.context_processor
    def inject_pending_review_count():
        from flask_login import current_user

        if current_user.is_authenticated:
            from sqlalchemy import func, select

            from app.models.product_match import ProductMatch

            count = (
                db.session.execute(
                    select(func.count(ProductMatch.id)).where(
                        ProductMatch.status == "candidate"
                    )
                ).scalar()
                or 0
            )
            return {"pending_review_count": count}
        return {"pending_review_count": 0}

    # Ensure all models are registered with SQLAlchemy before create_all
    from app.models import (  # noqa: F401
        PromProduct,
        Supplier,
        SupplierProduct,
        ProductMatch,
        SyncRun,
        User,
        MatchRule,
    )

    # Create tables on first run
    with app.app_context():
        db.create_all()

    return app
