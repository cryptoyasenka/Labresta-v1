import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class DefaultConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-change-me")
    _db_url = os.environ.get("DATABASE_URL", "")
    # Railway provides postgres:// — SQLAlchemy 2.x requires postgresql://
    if _db_url.startswith("postgres://"):
        _db_url = _db_url.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = _db_url or (
        "sqlite:///" + os.path.join(basedir, "instance", "labresta.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session / remember-me
    REMEMBER_COOKIE_DURATION = timedelta(days=365)
    REMEMBER_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=365)
    SESSION_COOKIE_SAMESITE = "Lax"

    # CSRF token is bound to the session (which lasts 365 days); the default
    # 1-hour time limit would break long manual-review sessions with an
    # opaque "Unexpected token '<'" on the client when the reject/confirm
    # POST hits a 400 HTML error page.
    WTF_CSRF_TIME_LIMIT = None

    # FTP settings (used in Plan 04)
    FTP_HOST = os.environ.get("FTP_HOST", "")
    FTP_USER = os.environ.get("FTP_USER", "")
    FTP_PASS = os.environ.get("FTP_PASS", "")
    FTP_REMOTE_PATH = os.environ.get("FTP_REMOTE_PATH", "")

    # YML feed output
    YML_OUTPUT_DIR = os.path.join(basedir, "instance", "feeds")
    YML_FILENAME = "labresta-feed.yml"
    YML_PRICES_FILENAME = "labresta-prices.yml"
    YML_AVAILABILITY_FILENAME = "labresta-availability.yml"
