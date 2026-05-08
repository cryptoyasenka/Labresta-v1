"""One-time migration: insert Astim (astim.in.ua) supplier record.

Usage:
    .venv/Scripts/python.exe scripts/add_astim_supplier.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app import create_app
from app.extensions import db
from app.models.supplier import Supplier

# Confirmed with Yana on 2026-05-07.
DISCOUNT_PERCENT = 15.0
COST_RATE = 0.74  # 26% procurement discount -> we pay 74% of retail.
MIN_MARGIN_UAH = 600.0
# Astim feed prices are UAH, so eur_rate is not used in margin math after the
# UAH clamp fix; keep an explicit value to avoid an implicit DB default.
EUR_RATE_UAH = 51.15
FEED_URL = "https://astim.in.ua/toDealers.xml"


def main():
    app = create_app()
    with app.app_context():
        existing = db.session.execute(
            db.select(Supplier).where(Supplier.feed_url == FEED_URL)
        ).scalar_one_or_none()

        if existing:
            print(f"Supplier already exists: id={existing.id} name={existing.name!r}")
            return

        supplier = Supplier(
            name="Астим",
            feed_url=FEED_URL,
            discount_percent=DISCOUNT_PERCENT,
            pricing_mode="flat",
            eur_rate_uah=EUR_RATE_UAH,
            cost_rate=COST_RATE,
            min_margin_uah=MIN_MARGIN_UAH,
            parser_type="auto",
            is_enabled=True,
        )
        db.session.add(supplier)
        db.session.commit()
        db.session.refresh(supplier)
        print(
            f"Created supplier: id={supplier.id} name={supplier.name!r} "
            f"slug={supplier.slug!r}"
        )
        print(
            f"  discount={supplier.discount_percent}% "
            f"cost_rate={supplier.cost_rate} "
            f"min_margin={supplier.min_margin_uah} "
            f"eur_rate={supplier.eur_rate_uah}"
        )


if __name__ == "__main__":
    main()
