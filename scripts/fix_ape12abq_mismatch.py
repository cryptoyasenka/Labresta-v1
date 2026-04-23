"""Fix APE12ABQ vs APE12ABQ D false-confirmation.

Problem (found 2026-04-23):
  - m#1722 CONFIRMED sp#4989 `APE12ABQ` -> pp#5009 `APACH APE12ABQ D` (WRONG,
    D is a different SKU per Yana)
  - m#1723 CANDIDATE sp#5024 `APE12ABQ D` -> pp#5009 `APACH APE12ABQ D` (correct
    pair, needs promotion)
  - pp#312 `APACH APE12ABQ` is orphan (should be paired with sp#4989)

Actions (idempotent, dry-run by default):
  1. m#1722 status -> 'rejected' (clears the wrong confirmation)
  2. Insert new match sp#4989 <-> pp#312 status='confirmed' score=100
  3. m#1723 status -> 'confirmed'

Run with --apply to commit. No --apply => prints what WOULD happen.
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import create_app
from app.extensions import db
from app.models.catalog import PromProduct
from app.models.product_match import ProductMatch
from app.models.supplier_product import SupplierProduct


SP_BASE_ID = 4989     # article APE12ABQ
SP_DVAR_ID = 5024     # article APE12ABQ D
PP_BASE_ID = 312      # APACH APE12ABQ (orphan)
PP_DVAR_ID = 5009     # APACH APE12ABQ D

WRONG_MATCH_ID = 1722    # confirmed sp#4989 -> pp#5009 (WRONG)
CORRECT_CANDIDATE_ID = 1723  # candidate sp#5024 -> pp#5009 (needs promotion)


def verify_preconditions() -> bool:
    """Sanity-check the DB state matches what we expect before mutating."""
    sp_base = db.session.get(SupplierProduct, SP_BASE_ID)
    sp_dvar = db.session.get(SupplierProduct, SP_DVAR_ID)
    pp_base = db.session.get(PromProduct, PP_BASE_ID)
    pp_dvar = db.session.get(PromProduct, PP_DVAR_ID)
    wrong = db.session.get(ProductMatch, WRONG_MATCH_ID)
    cand = db.session.get(ProductMatch, CORRECT_CANDIDATE_ID)

    ok = True
    if not sp_base or (sp_base.article or "").strip().upper() != "APE12ABQ":
        print(f"  FAIL sp#{SP_BASE_ID} article mismatch: {sp_base.article if sp_base else None!r}")
        ok = False
    if not sp_dvar or (sp_dvar.article or "").strip().upper() != "APE12ABQ D":
        print(f"  FAIL sp#{SP_DVAR_ID} article mismatch: {sp_dvar.article if sp_dvar else None!r}")
        ok = False
    if not pp_base or "APE12ABQ" not in (pp_base.name or "") or " D" in pp_base.name.upper().replace("APE12ABQ", ""):
        pass  # loose check below
    if not pp_base:
        print(f"  FAIL pp#{PP_BASE_ID} not found")
        ok = False
    if not pp_dvar or "APE12ABQ D" not in (pp_dvar.name or "").upper():
        print(f"  FAIL pp#{PP_DVAR_ID} name mismatch: {pp_dvar.name if pp_dvar else None!r}")
        ok = False
    if not wrong:
        print(f"  FAIL m#{WRONG_MATCH_ID} not found")
        ok = False
    elif wrong.supplier_product_id != SP_BASE_ID or wrong.prom_product_id != PP_DVAR_ID:
        print(f"  FAIL m#{WRONG_MATCH_ID} pair changed: sp#{wrong.supplier_product_id} pp#{wrong.prom_product_id}")
        ok = False
    elif wrong.status != "confirmed":
        print(f"  WARN m#{WRONG_MATCH_ID} status already {wrong.status!r} (expected 'confirmed' — perhaps already fixed)")
    if not cand:
        print(f"  FAIL m#{CORRECT_CANDIDATE_ID} not found")
        ok = False
    elif cand.supplier_product_id != SP_DVAR_ID or cand.prom_product_id != PP_DVAR_ID:
        print(f"  FAIL m#{CORRECT_CANDIDATE_ID} pair changed")
        ok = False

    return ok


def show_plan() -> None:
    print("--- Before ---")
    for mid in (WRONG_MATCH_ID, CORRECT_CANDIDATE_ID):
        m = db.session.get(ProductMatch, mid)
        print(f"  m#{m.id} status={m.status} sp#{m.supplier_product_id} -> pp#{m.prom_product_id} score={m.score}")
    existing_new = db.session.query(ProductMatch).filter_by(
        supplier_product_id=SP_BASE_ID, prom_product_id=PP_BASE_ID
    ).one_or_none()
    print(f"  sp#{SP_BASE_ID} <-> pp#{PP_BASE_ID}: "
          f"{'exists m#'+str(existing_new.id)+' status='+existing_new.status if existing_new else 'absent'}")
    print()
    print("--- Will do ---")
    print(f"  1. m#{WRONG_MATCH_ID}: status confirmed -> rejected")
    print(f"  2. Insert confirmed match sp#{SP_BASE_ID} <-> pp#{PP_BASE_ID} score=100.0")
    print(f"  3. m#{CORRECT_CANDIDATE_ID}: status candidate -> confirmed")


def apply_changes() -> None:
    now = datetime.now(timezone.utc)

    wrong = db.session.get(ProductMatch, WRONG_MATCH_ID)
    if wrong.status == "confirmed":
        wrong.status = "rejected"
        wrong.confirmed_at = None
        wrong.confirmed_by = None
        print(f"  [1] m#{WRONG_MATCH_ID}: confirmed -> rejected")
    else:
        print(f"  [1] m#{WRONG_MATCH_ID}: already {wrong.status}, skipping")

    existing_new = db.session.query(ProductMatch).filter_by(
        supplier_product_id=SP_BASE_ID, prom_product_id=PP_BASE_ID
    ).one_or_none()
    if existing_new is None:
        new_match = ProductMatch(
            supplier_product_id=SP_BASE_ID,
            prom_product_id=PP_BASE_ID,
            score=100.0,
            status="confirmed",
            created_at=now,
            confirmed_at=now,
            confirmed_by="fix_ape12abq_mismatch.py",
        )
        db.session.add(new_match)
        print(f"  [2] Inserted sp#{SP_BASE_ID} <-> pp#{PP_BASE_ID} confirmed")
    else:
        if existing_new.status != "confirmed":
            existing_new.status = "confirmed"
            existing_new.confirmed_at = now
            existing_new.confirmed_by = "fix_ape12abq_mismatch.py"
            existing_new.score = 100.0
            print(f"  [2] sp#{SP_BASE_ID} <-> pp#{PP_BASE_ID}: promoted to confirmed (was {existing_new.status})")
        else:
            print(f"  [2] sp#{SP_BASE_ID} <-> pp#{PP_BASE_ID}: already confirmed, skipping")

    cand = db.session.get(ProductMatch, CORRECT_CANDIDATE_ID)
    if cand.status != "confirmed":
        cand.status = "confirmed"
        cand.confirmed_at = now
        cand.confirmed_by = "fix_ape12abq_mismatch.py"
        print(f"  [3] m#{CORRECT_CANDIDATE_ID}: candidate -> confirmed")
    else:
        print(f"  [3] m#{CORRECT_CANDIDATE_ID}: already confirmed, skipping")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Commit changes (default: dry-run)")
    args = parser.parse_args()

    app = create_app()
    with app.app_context():
        if not verify_preconditions():
            print("PRECONDITIONS FAILED — aborting")
            return 1

        show_plan()
        print()

        if not args.apply:
            print("DRY-RUN. Use --apply to commit.")
            return 0

        apply_changes()
        db.session.commit()
        print()
        print("APPLIED.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
