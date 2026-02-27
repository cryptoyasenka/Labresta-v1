from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def configure_sqlite_wal(app):
    """Enable WAL journal mode for SQLite to prevent locking between scheduler and web."""
    with app.app_context():
        from sqlalchemy import event

        @event.listens_for(db.engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA journal_mode=WAL;")
            cursor.close()
