"""Repair the 1pp ↔ 1 supplier invariant for existing data.

For each (supplier_id, prom_product_id) group with more than one non-rejected
ProductMatch, keep one winner and reject the rest. Winner priority:

    1. confirmed
    2. manual
    3. candidate with the highest score (tie-broken by lowest id)

Losers get status='rejected' and confirmed_by='cleanup:invariant_repair'.

Dry-run by default. Pass --apply to commit changes.
"""

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import select

from app import create_app
from app.extensions import db
from app.models.product_match import ProductMatch
from app.models.supplier_product import SupplierProduct


STATUS_PRIORITY = {"confirmed": 0, "manual": 1, "candidate": 2}


def _winner_key(m: ProductMatch) -> tuple:
    """Sort key — lower wins. Priority by status, then -score, then id."""
    return (
        STATUS_PRIORITY.get(m.status, 99),
        -(m.score or 0.0),
        m.id,
    )


def find_duplicate_groups():
    """Return list of (supplier_id, pp_id, [matches...]) for groups > 1."""
    rows = db.session.execute(
        select(ProductMatch, SupplierProduct.supplier_id)
        .join(SupplierProduct, ProductMatch.supplier_product_id == SupplierProduct.id)
        .where(ProductMatch.status != "rejected")
    ).all()

    groups: dict[tuple[int, int], list[ProductMatch]] = {}
    for match, supplier_id in rows:
        key = (supplier_id, match.prom_product_id)
        groups.setdefault(key, []).append(match)

    return [(sup, pp, ms) for (sup, pp), ms in groups.items() if len(ms) > 1]


def cleanup(apply: bool, confirmed_by: str = "cleanup:invariant_repair") -> dict:
    groups = find_duplicate_groups()
    now = datetime.now(timezone.utc)
    rejected_count = 0
    kept_breakdown = {"confirmed": 0, "manual": 0, "candidate": 0}
    rejected_breakdown = {"confirmed": 0, "manual": 0, "candidate": 0}
    sample_actions: list[str] = []

    for sup_id, pp_id, matches in groups:
        ordered = sorted(matches, key=_winner_key)
        winner = ordered[0]
        losers = ordered[1:]
        kept_breakdown[winner.status] = kept_breakdown.get(winner.status, 0) + 1

        for m in losers:
            rejected_breakdown[m.status] = rejected_breakdown.get(m.status, 0) + 1
            rejected_count += 1
            if apply:
                m.status = "rejected"
                m.confirmed_at = now
                m.confirmed_by = confirmed_by
            if len(sample_actions) < 10:
                sample_actions.append(
                    f"sup#{sup_id} pp#{pp_id}: keep match#{winner.id} ({winner.status}) "
                    f"reject match#{m.id} (was {ordered[ordered.index(m)].status})"
                )

    if apply:
        db.session.commit()

    return {
        "groups": len(groups),
        "rejected": rejected_count,
        "kept_breakdown": kept_breakdown,
        "rejected_breakdown": rejected_breakdown,
        "sample_actions": sample_actions,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Commit changes. Default is dry-run.",
    )
    parser.add_argument(
        "--confirmed-by",
        default="cleanup:invariant_repair",
        help="Value to write into rejected.confirmed_by for audit.",
    )
    args = parser.parse_args()

    app = create_app()
    with app.app_context():
        stats = cleanup(apply=args.apply, confirmed_by=args.confirmed_by)

    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"=== invariant cleanup — {mode} ===")
    print(f"  duplicate groups: {stats['groups']}")
    print(f"  matches to reject: {stats['rejected']}")
    print(f"  kept by status:    {stats['kept_breakdown']}")
    print(f"  rejected by status: {stats['rejected_breakdown']}")
    print()
    print("  sample (first 10):")
    for s in stats["sample_actions"]:
        print(f"    {s}")
    if not args.apply:
        print()
        print("  Re-run with --apply to commit.")


if __name__ == "__main__":
    main()
