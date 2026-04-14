"""Shared fixtures for tests requiring Flask app context and database."""

import os

import pytest
from flask_login.test_client import FlaskLoginClient

from app.extensions import db as _db


@pytest.fixture(scope="session")
def app():
    """Create application for testing with in-memory SQLite."""
    from flask import Flask
    from app.extensions import configure_sqlite_wal, csrf, db, login_manager

    import os
    app_dir = os.path.join(os.path.dirname(__file__), '..', 'app')
    flask_app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder=os.path.join(app_dir, 'templates'),
    )
    os.makedirs(flask_app.instance_path, exist_ok=True)

    flask_app.config.update({
        "TESTING": True,
        "SECRET_KEY": "test-secret",
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "WTF_CSRF_ENABLED": False,
    })

    flask_app.test_client_class = FlaskLoginClient

    db.init_app(flask_app)
    configure_sqlite_wal(flask_app)
    login_manager.init_app(flask_app)
    csrf.init_app(flask_app)

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return db.session.get(User, int(user_id))

    # Register all blueprints needed for tests (base.html references several endpoints)
    from app.views.main import main_bp
    from app.views.matches import matches_bp
    from app.views.audit import audit_bp
    from app.views.catalog import catalog_bp
    from app.views.dashboard import dashboard_bp
    from app.views.feed import feed_bp
    from app.views.logs import logs_bp
    from app.views.products import products_bp
    from app.views.settings import settings_bp
    from app.views.suppliers import suppliers_bp
    from app.views.auth import auth_bp
    flask_app.register_blueprint(main_bp)
    flask_app.register_blueprint(matches_bp, url_prefix="/matches")
    flask_app.register_blueprint(audit_bp, url_prefix="/audit")
    flask_app.register_blueprint(catalog_bp, url_prefix="/catalog")
    flask_app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
    flask_app.register_blueprint(feed_bp)
    flask_app.register_blueprint(logs_bp, url_prefix="/logs")
    flask_app.register_blueprint(products_bp, url_prefix="/products")
    flask_app.register_blueprint(settings_bp, url_prefix="/settings")
    flask_app.register_blueprint(suppliers_bp, url_prefix="/suppliers")
    flask_app.register_blueprint(auth_bp, url_prefix="/auth")

    # Import all models
    from app.models import (  # noqa: F401
        PromProduct, Supplier, SupplierProduct, ProductMatch,
        SyncRun, User, MatchRule, NotificationRule, Notification,
    )

    with flask_app.app_context():
        db.create_all()

    yield flask_app


@pytest.fixture()
def db(app):
    """Provide a clean database for each test."""
    with app.app_context():
        yield _db
        _db.session.rollback()
        for table in reversed(_db.metadata.sorted_tables):
            _db.session.execute(table.delete())
        _db.session.commit()


@pytest.fixture()
def session(db):
    """Alias for tests that take a `session` parameter instead of `db`."""
    yield db.session


@pytest.fixture()
def client(app, db):
    """Test client with authenticated user via FlaskLoginClient."""
    from app.models.user import User

    user = User(email="test@test.com", name="Test User", role="admin")
    user.set_password("test123")
    db.session.add(user)
    db.session.commit()

    with app.test_client(user=user) as c:
        yield c
