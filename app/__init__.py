import os

from flask import Flask

from app.extensions import configure_sqlite_wal, db


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

    # Register blueprints
    from app.views.main import main_bp
    from app.views.suppliers import suppliers_bp
    from app.views.catalog import catalog_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(suppliers_bp, url_prefix="/suppliers")
    app.register_blueprint(catalog_bp, url_prefix="/catalog")

    # Register CLI commands
    from app.cli import sync_command

    app.cli.add_command(sync_command)

    # Ensure all models are registered with SQLAlchemy before create_all
    from app.models import Supplier, PromProduct, SupplierProduct, ProductMatch, SyncRun  # noqa: F401

    # Create tables on first run
    with app.app_context():
        db.create_all()

    return app
