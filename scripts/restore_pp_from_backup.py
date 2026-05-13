"""Restore PromProduct fields from a backup JSON produced by backup_before_catalog_import.py.

Restores only PromProduct (the table that catalog_import.py overwrites).
Does NOT touch product_matches — those aren't affected by catalog import and
are backed up only for forensic reference.

Match strategy: by PromProduct.id (stable across catalog imports since external_id
is the matching key but id is the FK target for matches — never mutated).

Usage:
    .venv/Scripts/python.exe scripts/restore_pp_from_backup.py <backup.json>          # dry-run
    .venv/Scripts/python.exe scripts/restore_pp_from_backup.py <backup.json> --apply  # commit
"""
import json
import sys
from datetime import datetime
from pathlib import Path

from app import create_app
from app.extensions import db
from app.models import PromProduct

sys.stdout.reconfigure(encoding="utf-8")

RESTORE_FIELDS = [
    "name", "name_ru", "brand", "article", "display_article",
    "price", "currency", "page_url", "image_url", "images",
    "description_ua", "description_ru",
]


def parse_dt(s):
    return datetime.fromisoformat(s) if s else None


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: restore_pp_from_backup.py <backup.json> [--apply]")
        return 2
    path = Path(sys.argv[1])
    apply = "--apply" in sys.argv
    mode = "APPLY" if apply else "DRY-RUN"
    if not path.exists():
        print(f"❌ Backup file not found: {path}")
        return 1

    data = json.loads(path.read_text(encoding="utf-8"))
    backup_pps = data["prom_products"]
    print(f"Backup taken: {data['taken_at']}")
    print(f"Restoring {len(backup_pps)} PromProducts  [{mode}]")
    print("=" * 90)

    app = create_app()
    with app.app_context():
        changed = 0
        missing = 0
        unchanged = 0
        for row in backup_pps:
            pp = db.session.get(PromProduct, row["id"])
            if pp is None:
                missing += 1
                print(f"  ⚠️  PP#{row['id']} missing in DB (was deleted post-backup)")
                continue
            diffs = []
            for f in RESTORE_FIELDS:
                cur = getattr(pp, f)
                bak = row.get(f)
                if cur != bak:
                    diffs.append(f"{f}: {cur!r} → {bak!r}")
                    if apply:
                        setattr(pp, f, bak)
            if diffs:
                changed += 1
                if changed <= 50:
                    print(f"  PP#{pp.id}: {len(diffs)} field(s) restored")
                    for d in diffs[:3]:
                        print(f"      {d}")
            else:
                unchanged += 1
        if apply:
            db.session.commit()
            print(f"\n✅ Committed: {changed} PPs restored, {unchanged} unchanged, {missing} missing")
        else:
            print(f"\nDRY-RUN: {changed} PPs would be restored, {unchanged} unchanged, {missing} missing")
            print("Re-run with --apply to commit.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
