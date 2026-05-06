"""Reject stale Gooder candidates that violate the SP-model-in-PP-name rule.

The matcher (commit 0a5c8c9) now prevents these from being created, but
existing bad candidates in the DB still block correct matches via claimed_pp_ids.
This script rejects them so the matcher can create correct pairs on next run.

Run: python scripts/fix_gooder_bad_candidates.py [--apply]
Default is dry-run. Pass --apply to actually update DB.
"""
import os, sys, re
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

APPLY = "--apply" in sys.argv

from app import create_app
from app.extensions import db
from app.models.product_match import ProductMatch
from app.models.supplier_product import SupplierProduct
from app.models.catalog import PromProduct
from sqlalchemy import select

GOODER_SUPPLIER_ID = 7


def normalize_model(value):
    if not value or not value.strip():
        return ""
    # strip /pl suffix, keep only [a-z0-9]
    v = re.sub(r"/pl$", "", value.strip(), flags=re.IGNORECASE)
    return re.sub(r"[^a-z0-9]", "", v.lower())


app = create_app()
with app.app_context():
    # Load all candidate matches for Gooder SPs
    rows = db.session.execute(
        select(ProductMatch, SupplierProduct, PromProduct)
        .join(SupplierProduct, ProductMatch.supplier_product_id == SupplierProduct.id)
        .join(PromProduct, ProductMatch.prom_product_id == PromProduct.id)
        .where(
            SupplierProduct.supplier_id == GOODER_SUPPLIER_ID,
            ProductMatch.status == "candidate",
        )
    ).all()

    print(f"Total Gooder candidate matches: {len(rows)}")
    print(f"Mode: {'APPLY' if APPLY else 'DRY-RUN (pass --apply to commit)'}")
    print("=" * 70)

    to_reject = []
    for match, sp, pp in rows:
        sp_model_key = sp.article or sp.model
        if not sp_model_key:
            continue  # no model — sub-rule doesn't apply, keep
        norm_key = normalize_model(sp_model_key)
        if len(norm_key) < 4:
            continue  # too short — sub-rule doesn't apply
        has_alpha = any(c.isalpha() for c in norm_key)
        has_digit = any(c.isdigit() for c in norm_key)
        if not (has_alpha and has_digit):
            continue  # not alphanumeric mix — sub-rule doesn't apply

        pp_norm = normalize_model(pp.name or "")
        pp_disp_norm = normalize_model(pp.display_article or "")

        brand_norm = normalize_model(sp.brand or "")
        norm_stripped = norm_key[: -len(brand_norm)] if brand_norm and norm_key.endswith(brand_norm) else norm_key
        if len(norm_stripped) < 4:
            norm_stripped = norm_key
        model_in_pp = (
            norm_key in pp_norm or norm_stripped in pp_norm
            or norm_key in pp_disp_norm or norm_stripped in pp_disp_norm
        )
        if not model_in_pp:
            to_reject.append((match, sp, pp, norm_key, pp_norm))

    print(f"Bad candidates to reject: {len(to_reject)}")
    print()
    for match, sp, pp, norm_key, pp_norm in to_reject:
        print(f"  REJECT match id={match.id}: SP '{sp.name}' (model_key={norm_key!r})")
        print(f"         -> PP '{pp.name}' (norm={pp_norm[:40]!r})")
        if APPLY:
            match.status = "rejected"

    if APPLY and to_reject:
        db.session.commit()
        print(f"\nDone: {len(to_reject)} candidates rejected.")
        print("Now run the matcher: click 'Перезапустити matcher' for Gooder in the UI.")
    elif not APPLY:
        print("\nDry-run complete. Run with --apply to commit changes.")
