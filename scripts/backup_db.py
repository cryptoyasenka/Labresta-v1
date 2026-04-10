"""Copy instance/labresta.db to backups/labresta-YYYYMMDD-HHMMSS.db.

Run before destructive operations (sync, catalog import, test runs). Uses
SQLite's online backup API so it's safe to run while the app is up.
"""

from __future__ import annotations

import sqlite3
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SOURCE_DB = PROJECT_ROOT / "instance" / "labresta.db"
BACKUP_DIR = PROJECT_ROOT / "backups"
KEEP_LAST = 20


def backup() -> Path:
    if not SOURCE_DB.exists():
        raise FileNotFoundError(f"Source DB not found: {SOURCE_DB}")

    BACKUP_DIR.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    target = BACKUP_DIR / f"labresta-{stamp}.db"

    src = sqlite3.connect(str(SOURCE_DB))
    dst = sqlite3.connect(str(target))
    try:
        src.backup(dst)
    finally:
        dst.close()
        src.close()

    prune_old()
    return target


def prune_old() -> None:
    backups = sorted(BACKUP_DIR.glob("labresta-*.db"))
    for old in backups[:-KEEP_LAST]:
        old.unlink(missing_ok=True)


if __name__ == "__main__":
    try:
        path = backup()
        print(f"Backup created: {path} ({path.stat().st_size // 1024} KB)")
    except Exception as exc:
        print(f"Backup failed: {exc}", file=sys.stderr)
        sys.exit(1)
