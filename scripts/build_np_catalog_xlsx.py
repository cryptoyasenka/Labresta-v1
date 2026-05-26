"""CLI wrapper: build the НП Channel-2 catalog import file (native Horoshop xlsx).

The build logic lives in ``app.services.np_catalog`` so the operator download
endpoint (app/views/feed.py) and this script share one implementation without a
view ever importing from scripts/. This file is just the command-line entry
point; Yana imports the produced file by hand in Horoshop (invariant #13).

Default output: instance/np-catalog-<ts>.xlsx. Read-only against the DB except
for the optional file write. Dry-run-safe.
"""

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import create_app
from app.services.np_catalog import (  # noqa: E402  (re-exported for tests)
    DEFAULT_FEED,
    NP_SUPPLIER_ID,
    SCOPE_BRANDS,
    _gallery_str,
    build_catalog_rows,
    build_workbook,
    write_workbook,
)

__all__ = [
    "DEFAULT_FEED", "NP_SUPPLIER_ID", "SCOPE_BRANDS",
    "_gallery_str", "build_catalog_rows", "build_workbook", "write_workbook",
    "run", "main",
]


def run(feed_path: str, out_path: str | None) -> None:
    app = create_app()
    with app.app_context():
        headers, rows, errors = build_catalog_rows(feed_path)
        print(f"Matched NP-exclusive SKU emitted: {len(rows)}")
        if errors:
            print(f"Warnings: {len(errors)}")
            for e in errors[:10]:
                print(f"  - {e}")
            if len(errors) > 10:
                print(f"  ... +{len(errors) - 10} more")
        if not rows:
            print("Nothing to write.")
            return
        if out_path is None:
            ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
            out_path = str(Path(app.instance_path) / f"np-catalog-{ts}.xlsx")
        path = write_workbook(headers, rows, out_path)
        print(f"Wrote {len(rows)} rows → {path}")
        print("Import by hand in Horoshop; map the «Галерея» column (FINAL-MODEL §3).")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--feed", default=DEFAULT_FEED)
    p.add_argument("--out", default=None)
    args = p.parse_args()
    run(args.feed, args.out)


if __name__ == "__main__":
    main()
