import os

from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class DefaultConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-change-me")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "instance", "labresta.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # FTP settings (used in Plan 04)
    FTP_HOST = os.environ.get("FTP_HOST", "")
    FTP_USER = os.environ.get("FTP_USER", "")
    FTP_PASS = os.environ.get("FTP_PASS", "")
    FTP_REMOTE_PATH = os.environ.get("FTP_REMOTE_PATH", "")
