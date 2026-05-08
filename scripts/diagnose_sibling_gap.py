"""Diagnose Phase N gap: PP without confirmed match where a "sibling" SP
exists at the supplier (same brand, model-prefix relation but not exact).

Run: python scripts/diagnose_sibling_gap.py --brand Hurakan --supplier-id 4

Reports for each unmatched PP in `--brand`:
  - extracted pp_model (via matcher.extract_model_from_name)
  - sibling SPs at supplier whose article OR name-model starts with pp_model
    followed by a separator (sibling = different SKU variant)
  - exact-model SPs whose article == pp_model (should have matched but didn't)
  - any existing rejected/candidate match between PP and sibling SPs

This is read-only — no DB writes, no matcher changes. Output is a punch list
for deciding whether Phase N's matcher change is worth implementing.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy import func, select

from app import create_app
from app.extensions import db
from app.models.catalog import PromProduct
from app.models.product_match import ProductMatch
from app.models.supplier_product import SupplierProduct
from app.services.matcher import extract_model_from_name, normalize_model


def _is_separator(ch: str) -> bool:
    return not ch.isalnum()


def _is_sibling_extension(longer: str, shorter: str) -> tuple[bool, str]:
    """Return (True, suffix) if `longer` extends `shorter` with a separator
    or non-empty alphanumeric suffix. Used to detect SKU-variant relation
    (HKN-DL800 → HKN-DL800-silver, HKN-DHD10G → HKN-DHD10GM).
    """
    if not longer or not shorter or longer == shorter:
        return False, ""
    if len(longer) <= len(shorter):
        return False, ""
    if not longer.startswith(shorter):
        return False, ""
    tail = longer[len(shorter):]
    if not tail:
        return False, ""
    if _is_separator(tail[0]):
        return True, tail
    if tail[0].isalpha() and len(tail) <= 4:
        return True, tail
    return False, ""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--brand", required=True)
    parser.add_argument("--supplier-id", type=int, required=True)
    parser.add_argument("--limit", type=int, default=0,
                        help="Limit reported unmatched PPs (0 = all)")
    args = parser.parse_args()

    app = create_app()
    with app.app_context():
        # Brand match is case-insensitive: catalog and supplier feeds may
        # disagree on casing (e.g. Hurakan vs HURAKAN).
        brand_lower = args.brand.lower()
        unmatched = db.session.execute(
            select(PromProduct).where(func.lower(PromProduct.brand) == brand_lower)
        ).scalars().all()

        # Filter to those without confirmed/manual match
        confirmed_pp_ids = set(db.session.execute(
            select(ProductMatch.prom_product_id).where(
                ProductMatch.status.in_(("confirmed", "manual"))
            )
        ).scalars().all())

        unmatched = [pp for pp in unmatched if pp.id not in confirmed_pp_ids]

        sps = db.session.execute(
            select(SupplierProduct).where(
                SupplierProduct.supplier_id == args.supplier_id,
                func.lower(SupplierProduct.brand) == brand_lower,
            )
        ).scalars().all()

        sp_index = []
        for sp in sps:
            sp_art_norm = normalize_model(sp.article) if sp.article else ""
            sp_name_model_norm = normalize_model(
                extract_model_from_name(sp.name or "", args.brand)
            )
            sp_index.append((sp, sp_art_norm, sp_name_model_norm))

        print(f"\n{'='*78}")
        print(f"Phase N diagnostic — brand={args.brand} supplier_id={args.supplier_id}")
        print(f"{'='*78}")
        print(f"Unmatched PPs in brand: {len(unmatched)}")
        print(f"SPs at supplier+brand:  {len(sps)}")
        print()

        if args.limit:
            unmatched = unmatched[:args.limit]

        cat_a = []  # exact-model SPs that should have matched
        cat_b = []  # sibling SPs (longer SKU)
        cat_b_reverse = []  # PP_model is longer than SP article
        cat_none = []  # no nearby SP at all

        for pp in unmatched:
            pp_model = normalize_model(
                extract_model_from_name(pp.name or "", args.brand)
            )
            pp_disp_norm = normalize_model(pp.display_article) if pp.display_article else ""

            # Effective anchor — display_article wins, else name-extracted model
            anchor = pp_disp_norm or pp_model
            if not anchor or len(anchor) < 4:
                cat_none.append((pp, anchor, []))
                continue

            exact_hits = []
            sibling_hits = []
            reverse_hits = []

            for sp, sp_art_norm, sp_name_model_norm in sp_index:
                # exact: SP article (or name-model) == pp anchor
                if sp_art_norm and sp_art_norm == anchor:
                    exact_hits.append((sp, "article=anchor"))
                    continue
                if sp_name_model_norm and sp_name_model_norm == anchor:
                    exact_hits.append((sp, "name_model=anchor"))
                    continue

                # sibling: SP extends pp anchor
                for sp_field_name, sp_field_val in (
                    ("article", sp_art_norm),
                    ("name_model", sp_name_model_norm),
                ):
                    if not sp_field_val:
                        continue
                    is_ext, tail = _is_sibling_extension(sp_field_val, anchor)
                    if is_ext:
                        sibling_hits.append((sp, sp_field_name, tail))
                        break

                # reverse: pp anchor extends SP article (pp longer than sp)
                for sp_field_name, sp_field_val in (
                    ("article", sp_art_norm),
                    ("name_model", sp_name_model_norm),
                ):
                    if not sp_field_val or len(sp_field_val) < 4:
                        continue
                    is_rev, tail = _is_sibling_extension(anchor, sp_field_val)
                    if is_rev:
                        reverse_hits.append((sp, sp_field_name, tail))
                        break

            if exact_hits:
                cat_a.append((pp, anchor, exact_hits))
            elif sibling_hits:
                cat_b.append((pp, anchor, sibling_hits))
            elif reverse_hits:
                cat_b_reverse.append((pp, anchor, reverse_hits))
            else:
                cat_none.append((pp, anchor, []))

        def _print_match_status(pp_id: int, sp_id: int) -> str:
            m = db.session.execute(
                select(ProductMatch).where(
                    ProductMatch.prom_product_id == pp_id,
                    ProductMatch.supplier_product_id == sp_id,
                )
            ).scalar_one_or_none()
            if m is not None:
                return f"match#{m.id} status={m.status}"
            # SP may be confirmed to a DIFFERENT pp — surface that.
            other = db.session.execute(
                select(ProductMatch).where(
                    ProductMatch.supplier_product_id == sp_id,
                    ProductMatch.status.in_(("confirmed", "manual")),
                )
            ).scalar_one_or_none()
            if other is not None:
                return f"no-match-row, BUT SP confirmed to PP#{other.prom_product_id} (m#{other.id})"
            return "no-match-row, SP also unmatched"

        print(f"--- Cat A: exact-model SP exists but no candidate ({len(cat_a)} PPs) ---")
        print("(matcher should have surfaced these — gate filtered them)")
        for pp, anchor, hits in cat_a[:20]:
            print(f"\n  PP#{pp.id} anchor={anchor!r} name={pp.name!r}")
            for sp, why in hits[:3]:
                status = _print_match_status(pp.id, sp.id)
                print(f"    SP#{sp.id} art={sp.article!r} name={sp.name!r}  ({why}, {status})")

        print(f"\n--- Cat B: sibling SP (SP=anchor+suffix) ({len(cat_b)} PPs) ---")
        print("(SP is more specific variant of PP — Phase N target)")
        for pp, anchor, hits in cat_b[:20]:
            print(f"\n  PP#{pp.id} anchor={anchor!r} name={pp.name!r}")
            for sp, field, tail in hits[:5]:
                status = _print_match_status(pp.id, sp.id)
                print(f"    SP#{sp.id} {field}={getattr(sp, field if field=='article' else 'name')!r}  (suffix={tail!r}, {status})")

        print(f"\n--- Cat B-reverse: PP-anchor=SP+suffix ({len(cat_b_reverse)} PPs) ---")
        print("(PP is more specific than SP — rare, but worth flagging)")
        for pp, anchor, hits in cat_b_reverse[:10]:
            print(f"\n  PP#{pp.id} anchor={anchor!r} name={pp.name!r}")
            for sp, field, tail in hits[:3]:
                status = _print_match_status(pp.id, sp.id)
                print(f"    SP#{sp.id} {field}={getattr(sp, field if field=='article' else 'name')!r}  (pp_extra={tail!r}, {status})")

        print(f"\n--- Cat None: no nearby SP ({len(cat_none)} PPs) ---")
        print("(SP truly missing from supplier feed — Phase M / orphan target)")
        for pp, anchor, _ in cat_none[:20]:
            print(f"  PP#{pp.id} anchor={anchor!r} name={pp.name!r}")

        print(f"\n{'='*78}")
        print(f"SUMMARY  brand={args.brand} supplier_id={args.supplier_id}")
        print(f"{'='*78}")
        print(f"  Cat A (exact, gate-filtered):  {len(cat_a):>4}")
        print(f"  Cat B (SP-extends-anchor):     {len(cat_b):>4}  <- Phase N target")
        print(f"  Cat B-reverse (PP-extends-SP): {len(cat_b_reverse):>4}")
        print(f"  Cat None (truly missing):      {len(cat_none):>4}  <- Phase M target")
        print(f"  Total unmatched in brand:      {len(unmatched):>4}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
