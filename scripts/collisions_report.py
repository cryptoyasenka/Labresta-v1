"""Report prom_product rows that have >1 confirmed/manual matches.

Такие коллизии блокируют partial UNIQUE INDEX (scripts/migrate_unique_prom_match.py)
и ломают 1:1 инвариант. Этот скрипт выгружает всё в CSV для ручного разбора:
оператор решает какой SupplierProduct на самом деле соответствует pp,
остальные — reject.

CSV columns:
  pp_id, pp_name, pp_brand, pp_price_uah,
  match_id, match_status, match_score, match_confirmed_by, match_confirmed_at,
  sp_id, sp_external_id, sp_name, sp_brand, sp_price_eur, sp_available

По умолчанию пишет в reports/prom_collisions_YYYYMMDD-HHMMSS.csv
"""

import argparse
import csv
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from sqlalchemy import func, select

from app import create_app
from app.extensions import db
from app.models.catalog import PromProduct
from app.models.product_match import ProductMatch
from app.models.supplier_product import SupplierProduct


def run(out_path: Path | None) -> None:
    app = create_app()
    with app.app_context():
        collision_pp_ids = [
            pp_id
            for pp_id, cnt in db.session.execute(
                select(ProductMatch.prom_product_id, func.count(ProductMatch.id))
                .where(ProductMatch.status.in_(["confirmed", "manual"]))
                .group_by(ProductMatch.prom_product_id)
                .having(func.count(ProductMatch.id) > 1)
            ).all()
        ]

        print(f"Collisions: {len(collision_pp_ids)} prom_products with >1 confirmed/manual matches")
        if not collision_pp_ids:
            return

        if out_path is None:
            out_path = Path(__file__).resolve().parent.parent / "reports" / (
                f"prom_collisions_{datetime.now().strftime('%Y%m%d-%H%M%S')}.csv"
            )
        out_path.parent.mkdir(parents=True, exist_ok=True)

        rows_out = 0
        with out_path.open("w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f)
            w.writerow([
                "pp_id", "pp_name", "pp_brand", "pp_price_uah",
                "match_id", "match_status", "match_score",
                "match_confirmed_by", "match_confirmed_at",
                "sp_id", "sp_external_id", "sp_name", "sp_brand",
                "sp_price_eur", "sp_available",
            ])
            for pp_id in collision_pp_ids:
                pp = db.session.get(PromProduct, pp_id)
                matches = (
                    ProductMatch.query
                    .filter(
                        ProductMatch.prom_product_id == pp_id,
                        ProductMatch.status.in_(["confirmed", "manual"]),
                    )
                    .order_by(ProductMatch.status.desc(), ProductMatch.id.asc())
                    .all()
                )
                for m in matches:
                    sp = db.session.get(SupplierProduct, m.supplier_product_id)
                    w.writerow([
                        pp.id, pp.name, pp.brand, float(pp.price) if pp.price else "",
                        m.id, m.status, m.score,
                        m.confirmed_by or "",
                        m.confirmed_at.isoformat() if m.confirmed_at else "",
                        sp.id if sp else "",
                        sp.external_id if sp else "",
                        sp.name if sp else "",
                        sp.brand if sp else "",
                        (sp.price_cents / 100.0) if sp and sp.price_cents else "",
                        bool(sp.available) if sp else "",
                    ])
                    rows_out += 1
                w.writerow([])  # blank row between groups for readability

        print(f"Wrote {rows_out} rows to {out_path}")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=Path, default=None)
    args = p.parse_args()
    run(args.out)


if __name__ == "__main__":
    main()
