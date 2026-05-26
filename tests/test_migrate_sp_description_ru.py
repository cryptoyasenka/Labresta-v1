"""Regression test for the description_ru migration script.

Verifies the idempotent ADD COLUMN helper: adds the column when missing,
is a no-op on re-run, and never touches other columns.
"""

import sqlite3

from scripts.migrate_add_sp_description_ru import column_exists, ensure_columns


def _make_legacy_table(conn):
    """A supplier_products table WITHOUT description_ru (pre-migration shape)."""
    conn.execute(
        "CREATE TABLE supplier_products ("
        "  id INTEGER PRIMARY KEY,"
        "  supplier_id INTEGER NOT NULL,"
        "  external_id TEXT NOT NULL,"
        "  name TEXT NOT NULL,"
        "  description TEXT"
        ")"
    )
    conn.execute(
        "INSERT INTO supplier_products (supplier_id, external_id, name, description)"
        " VALUES (1, 'sku-1', 'Item', 'UA body')"
    )
    conn.commit()


def test_adds_column_when_missing(tmp_path):
    db = tmp_path / "t.db"
    conn = sqlite3.connect(db)
    try:
        _make_legacy_table(conn)
        assert not column_exists(conn, "supplier_products", "description_ru")

        ensure_columns(conn)
        conn.commit()

        assert column_exists(conn, "supplier_products", "description_ru")
        # Existing row preserved, new column NULL.
        row = conn.execute(
            "SELECT description, description_ru FROM supplier_products"
        ).fetchone()
        assert row == ("UA body", None)
    finally:
        conn.close()


def test_idempotent_rerun(tmp_path):
    db = tmp_path / "t.db"
    conn = sqlite3.connect(db)
    try:
        _make_legacy_table(conn)
        ensure_columns(conn)
        conn.commit()
        # Second run must not raise and must not duplicate the column.
        ensure_columns(conn)
        conn.commit()
        cols = [r[1] for r in conn.execute("PRAGMA table_info(supplier_products)")]
        assert cols.count("description_ru") == 1
    finally:
        conn.close()
