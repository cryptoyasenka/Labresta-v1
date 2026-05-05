"""One-time migration: insert Гудер (gooder.kiev.ua) supplier record.

Run AFTER confirming the two config values below with Yana:
  - EUR_RATE_UAH  — the EUR/UAH rate used in margin calculations
  - COST_RATE     — fraction of Gooder retail we pay (0.80 = buy at 80% of price)

Usage:
    .venv/Scripts/python.exe scripts/add_gooder_supplier.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app import create_app
from app.extensions import db
from app.models.supplier import Supplier

# ── Config — confirm with Yana before running ──────────────────────────────
EUR_RATE_UAH = 45.0   # EUR/UAH rate for margin calculations
COST_RATE    = 0.85   # 15% supplier discount → we pay 85% of their retail
# ──────────────────────────────────────────────────────────────────────────

def main():
    if EUR_RATE_UAH is None or COST_RATE is None:
        print("ERROR: Set EUR_RATE_UAH and COST_RATE in this script before running.")
        sys.exit(1)

    app = create_app()
    with app.app_context():
        existing = db.session.execute(
            db.select(Supplier).where(Supplier.feed_url == "https://gooder.kiev.ua/xml.xml")
        ).scalar_one_or_none()

        if existing:
            print(f"Supplier already exists: id={existing.id} name={existing.name!r}")
            sys.exit(0)

        supplier = Supplier(
            name="Гудер",
            feed_url="https://gooder.kiev.ua/xml.xml",
            discount_percent=5.0,
            pricing_mode="flat",
            eur_rate_uah=EUR_RATE_UAH,
            cost_rate=COST_RATE,
            min_margin_uah=500.0,
            parser_type="auto",
            is_enabled=True,
        )
        db.session.add(supplier)
        db.session.commit()
        db.session.refresh(supplier)
        print(f"Created supplier: id={supplier.id} name={supplier.name!r} slug={supplier.slug!r}")
        print(f"  discount={supplier.discount_percent}%  eur_rate={supplier.eur_rate_uah}  cost_rate={supplier.cost_rate}")


if __name__ == "__main__":
    main()
