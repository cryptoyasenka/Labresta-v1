"""M-3: production (Postgres) must refuse to boot with the placeholder
SECRET_KEY (forgeable sessions/CSRF). Local sqlite dev and tests keep the
default harmlessly."""

from app import _secret_key_is_insecure

DEFAULT = "dev-key-change-me"
REAL = "a-real-64-char-secret"


def test_production_postgres_with_default_key_is_insecure():
    assert _secret_key_is_insecure(
        "postgresql://u:p@host/db", DEFAULT, is_testing=False
    ) is True


def test_production_postgres_with_real_key_is_ok():
    assert _secret_key_is_insecure(
        "postgresql://u:p@host/db", REAL, is_testing=False
    ) is False


def test_local_sqlite_with_default_key_is_ok():
    # Local dev fallback URI — placeholder key is harmless here.
    assert _secret_key_is_insecure(
        "sqlite:///instance/labresta.db", DEFAULT, is_testing=False
    ) is False


def test_testing_bypasses_guard_even_on_postgres():
    assert _secret_key_is_insecure(
        "postgresql://u:p@host/db", DEFAULT, is_testing=True
    ) is False
