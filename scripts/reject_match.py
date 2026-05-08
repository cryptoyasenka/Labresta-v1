"""Reject a single ProductMatch by id.

Sets status='rejected'. Does not delete the row (UniqueConstraint is preserved
so the matcher's rule_matcher will skip this PP↔SP pair on next run).

Usage:
  $env:DATABASE_URL = "<DATABASE_PUBLIC_URL>"
  & .venv/Scripts/python.exe scripts/reject_match.py --id 6611 \
      --reason "size mismatch 250g vs 150g (yana 2026-05-09)"

Prints a before/after summary. Asks for explicit confirmation before commit.
"""
import argparse
import os
import sys
from datetime import datetime, timezone

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy import select

from app import create_app
from app.extensions import db
from app.models.product_match import ProductMatch
from app.models.supplier_product import SupplierProduct
from app.models.catalog import PromProduct
from app.models.supplier import Supplier


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", type=int, required=True, help="ProductMatch.id to reject")
    ap.add_argument("--reason", type=str, required=True, help="Why (logged to confirmed_by)")
    ap.add_argument("--yes", action="store_true", help="Skip the y/N prompt and apply")
    args = ap.parse_args()

    app = create_app()
    with app.app_context():
        m = db.session.get(ProductMatch, args.id)
        if not m:
            print(f"ERROR: match#{args.id} not found")
            return 1

        sp = db.session.get(SupplierProduct, m.supplier_product_id)
        pp = db.session.get(PromProduct, m.prom_product_id)
        sup = db.session.get(Supplier, sp.supplier_id) if sp else None

        print(f"\nmatch#{m.id}")
        print(f"  status:       {m.status} → rejected")
        print(f"  score:        {m.score}")
        print(f"  confirmed_by: {m.confirmed_by!r}")
        print(f"  reason:       {args.reason!r}")
        print()
        print(f"  PP#{pp.id if pp else '?'}  brand={(pp.brand if pp else '')!r}")
        print(f"    disp={pp.display_article if pp else '?'!r}")
        print(f"    name={(pp.name if pp else '')[:100]!r}")
        print(f"  SP#{sp.id if sp else '?'}  sup={(sup.name if sup else '?')!r}")
        print(f"    art={(sp.article if sp else '')!r}")
        print(f"    name={(sp.name if sp else '')[:100]!r}")
        print()

        if m.status == "rejected":
            print("Already rejected — nothing to do.")
            return 0

        if not args.yes:
            ans = input("Apply rejection? [y/N] ").strip().lower()
            if ans != "y":
                print("Aborted.")
                return 0

        prev_status = m.status
        prev_cb = m.confirmed_by
        m.status = "rejected"
        m.confirmed_at = datetime.now(timezone.utc)
        m.confirmed_by = f"reject:{args.reason}"[:100]
        db.session.commit()

        print(f"OK: match#{m.id} {prev_status} → rejected")
        print(f"  prev confirmed_by={prev_cb!r}")
        print(f"  new  confirmed_by={m.confirmed_by!r}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
