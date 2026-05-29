"""Generate the MARESTO availability XLSX for manual Horoshop import.

WHY a local script (not a web button): MARESTO's feed returns 403 from Railway
(prod) but 200 from a local machine, so `stock_status` can only be populated
where the feed is reachable. This script runs the full local chain:

    fetch MARESTO feed -> parse (captures <stock>) -> save (LOCAL DB) ->
    build_maresto_file -> write .xlsx

then YOU import the .xlsx into Horoshop by hand (partial import: it updates only
«Наявність», leaving price/photo/description untouched). The status mapping is
locked in app/services/maresto_stock.py.

⚠️ Before the first bulk import, run a 1-ROW empirical import test on the live
store to confirm the 4 named statuses map through the «Наличие» column (see
.planning/RESEARCH-horoshop-availability-and-new-offers.md and the
feedback_labresta_live_import rule — the live import stays your hand).

Usage:
    python scripts/generate_maresto_availability.py [output.xlsx]
    python scripts/generate_maresto_availability.py --no-fetch   # build from current DB only
"""

import sys
from pathlib import Path

# Allow running as `python scripts/generate_maresto_availability.py` from anywhere.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import requests
from sqlalchemy import select

from app import create_app
from app.extensions import db
from app.models.supplier import Supplier
from app.services.feed_parser import parse_supplier_feed, save_supplier_products
from app.services.maresto_horoshop_file import build_maresto_file, MARESTO_SUPPLIER_SLUG

DEFAULT_OUT = Path(__file__).resolve().parent.parent / "instance" / "maresto_availability.xlsx"
FALLBACK_URL = "https://mrst.com.ua/include/price.xml"


def main() -> int:
    args = [a for a in sys.argv[1:]]
    no_fetch = "--no-fetch" in args
    out_args = [a for a in args if not a.startswith("--")]
    out_path = Path(out_args[0]) if out_args else DEFAULT_OUT

    app = create_app()
    with app.app_context():
        url = str(db.engine.url)
        # HARD GUARD: this script writes SupplierProduct rows; never touch prod.
        if "sqlite" not in url.lower() or any(
            t in url.lower() for t in ("rlwy", "railway", "postgres", "psycopg")
        ):
            print(f"ABORT: DB is not local sqlite ({url}). Refusing to write.")
            return 2
        print(f"DB: {url}")

        supplier = db.session.execute(
            select(Supplier).where(Supplier.slug == MARESTO_SUPPLIER_SLUG)
        ).scalar_one_or_none()
        if supplier is None:
            print(f"ABORT: supplier slug={MARESTO_SUPPLIER_SLUG!r} not found.")
            return 2

        if no_fetch:
            print("--no-fetch: building from current DB stock_status.")
        else:
            feed_url = supplier.feed_url or FALLBACK_URL
            print(f"Fetching {feed_url} ...")
            resp = requests.get(
                feed_url, timeout=60, headers={"User-Agent": "LabResta-Sync/1.0"}
            )
            if resp.status_code != 200:
                print(f"ABORT: feed returned HTTP {resp.status_code} "
                      f"(MARESTO 403s from Railway — run this locally).")
                return 1
            products = parse_supplier_feed(resp.content, supplier.id)
            res = save_supplier_products(products)
            print(f"Synced feed: {res['created']} created, {res['updated']} updated, "
                  f"{res['total']} total.")

        data, manifest = build_maresto_file()
        if manifest.get("error"):
            print(f"ABORT: {manifest['error']}")
            return 1

        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(data)

        print("\n=== MARESTO availability file ===")
        print(f"  rows: {manifest['total']} (from {manifest['matches_considered']} confirmed matches)")
        for status, n in sorted(manifest["per_status"].items(), key=lambda kv: -kv[1]):
            print(f"    {status}: {n}")
        if manifest["skipped_no_status"]:
            print(f"  skipped (no <stock> / unknown): {manifest['skipped_no_status']}")
        print(f"  file: {out_path}")
        print("\nNext: import this file in Horoshop by hand (1-row test first!).")
        return 0


if __name__ == "__main__":
    sys.exit(main())
