"""Sync НП content (body + photos) from SupplierProduct → PromProduct.

Channel-2 DB projection: for NP-exclusive matched cards, push the feed-sourced
body/photo fields stored on the supplier product onto the catalog product so the
app's own views reflect NP content. (The Horoshop store itself is updated via the
native Excel import — see FINAL-MODEL.md §1; this keeps the local catalog in sync.)

Scope, strictly:
  - supplier_id = 2 (Новый проект)
  - ProductMatch.status in {confirmed, manual} AND published = 1
  - sp.brand in the 9 NP-exclusive brands

For each in-scope match, assign ONLY these four fields, and ONLY when the feed
value is non-empty AND differs from what's stored (preserve-on-empty, idempotent):
    pp.description_ua ← sp.description
    pp.description_ru ← sp.description_ru
    pp.image_url      ← sp.image_url
    pp.images         ← sp.images

Worker-owned translation protection (catalog-import invariant) is NOT violated:
for NP exclusives the feed RU body IS the authoritative source.

Dry-run by default. --apply to commit (+ one summary AuditLog entry).
"""

import argparse
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from datetime import datetime, timezone

from app import create_app
from app.extensions import db
from app.models.audit_log import AuditLog
from app.models.catalog import PromProduct
from app.models.product_match import ProductMatch
from app.models.supplier_product import SupplierProduct

NP_SUPPLIER_ID = 2

SCOPE_BRANDS = {
    "HURAKAN", "APACH", "FAGOR", "TATRA", "COLD",
    "PROJECT SYSTEMS", "ASTORIA", "ARRIS", "MAXIMA",
}

# sp attribute → pp attribute
FIELD_MAP = {
    "description": "description_ua",
    "description_ru": "description_ru",
    "image_url": "image_url",
    "images": "images",
}


def _in_scope(brand: str | None) -> bool:
    return bool(brand) and brand.strip().upper() in SCOPE_BRANDS


def collect_changes(supplier_id: int = NP_SUPPLIER_ID) -> list[dict]:
    """Return per-card pending changes (no DB writes).

    Each entry: {match_id, pp_id, external_id, brand, fields: {pp_attr: (old, new)}}.
    Only in-scope, confirmed/manual, published matches with a real diff appear.
    """
    matches = (
        ProductMatch.query
        .join(SupplierProduct,
              ProductMatch.supplier_product_id == SupplierProduct.id)
        .filter(
            SupplierProduct.supplier_id == supplier_id,
            ProductMatch.status.in_(["confirmed", "manual"]),
            ProductMatch.published.is_(True),
        )
        .all()
    )

    changes: list[dict] = []
    for m in matches:
        sp: SupplierProduct = m.supplier_product
        pp: PromProduct = m.prom_product
        if not sp or not pp or not _in_scope(sp.brand):
            continue

        diff: dict[str, tuple] = {}
        for sp_attr, pp_attr in FIELD_MAP.items():
            new_val = getattr(sp, sp_attr)
            if not new_val:  # preserve-on-empty: never wipe pp with empty feed value
                continue
            old_val = getattr(pp, pp_attr)
            if old_val != new_val:
                diff[pp_attr] = (old_val, new_val)

        if diff:
            changes.append({
                "match_id": m.id,
                "pp_id": pp.id,
                "external_id": pp.external_id,
                "brand": sp.brand,
                "fields": diff,
            })
    return changes


def sync_bodies(apply: bool, supplier_id: int = NP_SUPPLIER_ID) -> dict:
    """Compute (and optionally apply) sp→pp body/photo sync.

    Must run inside a Flask app context. Returns stats dict:
        {matches_in_scope, cards_changed, per_field: {pp_attr: count}, applied}
    """
    changes = collect_changes(supplier_id)

    per_field: Counter = Counter()
    for ch in changes:
        for pp_attr in ch["fields"]:
            per_field[pp_attr] += 1

    stats = {
        "cards_changed": len(changes),
        "per_field": dict(per_field),
        "applied": apply,
    }

    if not apply or not changes:
        return stats

    pp_ids = [ch["pp_id"] for ch in changes]
    pp_by_id = {
        pp.id: pp for pp in PromProduct.query.filter(PromProduct.id.in_(pp_ids)).all()
    }
    for ch in changes:
        pp = pp_by_id.get(ch["pp_id"])
        if not pp:
            continue
        for pp_attr, (_old, new_val) in ch["fields"].items():
            setattr(pp, pp_attr, new_val)

    db.session.add(AuditLog(
        user_name="script:np_sync_bodies",
        action="np_sync_bodies",
        details=(
            '{"cards_changed": %d, "per_field": %s}'
            % (len(changes), dict(per_field))
        ),
    ))
    db.session.commit()
    return stats


def run(apply: bool) -> None:
    app = create_app()
    with app.app_context():
        changes = collect_changes()
        print(f"In-scope cards with pending changes: {len(changes)}")
        per_field: Counter = Counter()
        for ch in changes:
            for f in ch["fields"]:
                per_field[f] += 1
        for f, c in sorted(per_field.items()):
            print(f"  {f}: {c}")
        for ch in changes[:15]:
            flds = ", ".join(ch["fields"].keys())
            print(f"  pp {ch['external_id']} [{ch['brand']}] → {flds}")
        if len(changes) > 15:
            print(f"  ... +{len(changes) - 15} more")
        if not apply:
            print("\nDRY-RUN — pass --apply to commit.")
            return
        stats = sync_bodies(apply=True)
        print(f"\nAPPLIED: {stats['cards_changed']} cards updated.")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--apply", action="store_true")
    args = p.parse_args()
    run(args.apply)


if __name__ == "__main__":
    main()
