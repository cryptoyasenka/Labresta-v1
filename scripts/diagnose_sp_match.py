"""Diagnose why a SupplierProduct has no (or wrong) match candidate.

Usage:
    python scripts/diagnose_sp_match.py --sp-id 582 --pp-filter Softcooker
    python scripts/diagnose_sp_match.py --sp-id 582  # all catalog (slow, no filter)

Runs `find_match_candidates` against a pp-pool restricted by a name substring
(or the full catalog if no filter), with matcher DEBUG logging enabled so every
gate that drops a candidate prints its verdict. Also prints the raw WRatio
score for every pp in the filtered pool regardless of cutoff, so you can see
whether the issue is "score < 60" (fuzzy cutoff), "brand blocked", or a
post-fuzzy gate rejection.

Read-only — does not write to DB.
"""

import argparse
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from rapidfuzz import fuzz, process, utils
from sqlalchemy import select

from app import create_app
from app.extensions import db
from app.models.catalog import PromProduct
from app.models.supplier_product import SupplierProduct
from app.services import matcher as matcher_mod
from app.services.matcher import (
    after_brand_remainder,
    extract_article_codes,
    extract_model_from_name,
    extract_product_type,
    extract_voltages,
    find_match_candidates,
    meaningful_tokens,
    normalize_model,
    normalize_text,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sp-id", type=int, required=True)
    parser.add_argument(
        "--pp-filter",
        type=str,
        default=None,
        help="Case-insensitive substring restricting the pp pool (e.g. 'Softcooker').",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=15,
        help="How many top pp by raw WRatio to print (default 15).",
    )
    args = parser.parse_args()

    # Turn on matcher DEBUG so every gate prints its rejection reason.
    logging.basicConfig(
        level=logging.DEBUG,
        format="    [gate] %(message)s",
        stream=sys.stdout,
    )
    # Silence sqlalchemy noise.
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)

    app = create_app()
    with app.app_context():
        sp = db.session.get(SupplierProduct, args.sp_id)
        if not sp:
            print(f"ERROR: SupplierProduct #{args.sp_id} not found")
            return 1

        print(f"=== SupplierProduct #{sp.id} ===")
        print(f"  supplier_id : {sp.supplier_id}")
        print(f"  external_id : {sp.external_id}")
        print(f"  name        : {sp.name!r}")
        print(f"  brand       : {sp.brand!r}")
        print(f"  model       : {sp.model!r}")
        print(f"  article     : {sp.article!r}")
        print(f"  price_cents : {sp.price_cents}")
        print(f"  available   : {sp.available}")
        print()

        # Derive sup-side tokens/model/voltage for the report.
        sup_name_model = extract_model_from_name(sp.name, sp.brand) if sp.brand else ""
        sup_after = (
            meaningful_tokens(after_brand_remainder(sp.name, sp.brand))
            if sp.brand
            else meaningful_tokens(sp.name)
        )
        sup_voltages = extract_voltages(sp.name)
        sup_paren = [normalize_model(c) for c in extract_article_codes(sp.name)]
        sup_paren = [c for c in sup_paren if c]
        sup_type = extract_product_type(sp.name, sp.brand or "") if sp.brand else ""

        print("=== Derived supplier-side fields ===")
        print(f"  name-model         : {sup_name_model!r} (norm={normalize_model(sup_name_model)!r})")
        print(f"  after-brand tokens : {sorted(sup_after)}")
        print(f"  voltages           : {sup_voltages}")
        print(f"  paren codes        : {sup_paren}")
        print(f"  product type       : {sup_type!r}")
        print()

        # Load pp pool.
        prom_all = db.session.execute(select(PromProduct)).scalars().all()
        if args.pp_filter:
            needle = args.pp_filter.lower()
            prom_all = [p for p in prom_all if needle in (p.name or "").lower()]
        print(f"=== PP pool: {len(prom_all)} rows ===")

        # Raw WRatio scores (no gates) against the filtered pool.
        sup_norm = normalize_text(sp.name)
        choices = {p.id: normalize_text(p.name) for p in prom_all}
        raw = process.extract(
            sup_norm,
            choices,
            scorer=fuzz.WRatio,
            processor=utils.default_process,
            limit=args.top,
        )
        print(f"--- Top {args.top} by raw WRatio (no gates) ---")
        pp_by_id = {p.id: p for p in prom_all}
        for matched_name, score, pp_id in raw:
            pp = pp_by_id[pp_id]
            prom_model = normalize_model(
                extract_model_from_name(pp.name, pp.brand or sp.brand or "")
            )
            prom_after = (
                meaningful_tokens(after_brand_remainder(pp.name, pp.brand or sp.brand or ""))
            )
            prom_volt = extract_voltages(pp.name)
            diff_tokens = sup_after ^ prom_after
            print(f"  pp#{pp.id:5d} score={score:5.1f}  brand={pp.brand!r}")
            print(f"            name  : {pp.name!r}")
            print(f"            model : sp={normalize_model(sup_name_model)!r} vs pp={prom_model!r}"
                  f"  {'MATCH' if prom_model and normalize_model(sup_name_model) == prom_model else 'DIFF' if prom_model else '(pp empty)'}")
            print(f"            volt  : sp={sup_voltages} vs pp={prom_volt}")
            print(f"            tokens: pp-after={sorted(prom_after)}")
            if diff_tokens:
                print(f"                    diff   ={sorted(diff_tokens)}")
            print(f"            disp_art={pp.display_article!r}  article={pp.article!r}")
        print()

        # Now run find_match_candidates end-to-end against the same pool.
        # Gates log rejections at DEBUG.
        prom_list = [
            {
                "id": p.id,
                "name": p.name,
                "brand": p.brand,
                "price": p.price,
                "model": p.model,
                "article": p.article,
                "display_article": p.display_article,
            }
            for p in prom_all
        ]
        print("=== find_match_candidates (with gates; DEBUG rejections inline) ===")
        matcher_mod.logger.setLevel(logging.DEBUG)
        cands = find_match_candidates(
            sp.name,
            sp.brand,
            prom_list,
            supplier_price_cents=sp.price_cents,
            supplier_model=sp.model,
            supplier_article=sp.article,
            score_cutoff=0.0,  # see everything
            limit=50,
        )
        print(f"--- Survivors: {len(cands)} ---")
        for c in cands:
            print(f"  pp#{c['prom_product_id']}  score={c['score']}  {c['prom_name']!r}")


if __name__ == "__main__":
    raise SystemExit(main() or 0)
