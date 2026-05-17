"""Backup PromProduct + ProductMatch to JSON before Horoshop XLSX import.

Output: backups/pre-catalog-import_YYYY-MM-DD_HHMM.json (gitignored).
Restore via scripts/restore_pp_from_backup.py.

Read-only on DB.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from app import create_app
from app.models import PromProduct, ProductMatch

sys.stdout.reconfigure(encoding="utf-8")


def pp_row(pp: PromProduct) -> dict:
    return {
        "id": pp.id,
        "external_id": pp.external_id,
        "name": pp.name,
        "name_ru": pp.name_ru,
        "brand": pp.brand,
        "model": pp.model,
        "article": pp.article,
        "display_article": pp.display_article,
        "price": pp.price,
        "currency": pp.currency,
        "page_url": pp.page_url,
        "image_url": pp.image_url,
        "images": pp.images,
        "description_ua": pp.description_ua,
        "description_ru": pp.description_ru,
        "imported_at": pp.imported_at.isoformat() if pp.imported_at else None,
        "operator_decision": pp.operator_decision,
        "operator_decision_note": pp.operator_decision_note,
        "operator_decision_at": pp.operator_decision_at.isoformat() if pp.operator_decision_at else None,
    }


def match_row(m: ProductMatch) -> dict:
    return {
        "id": m.id,
        "supplier_product_id": m.supplier_product_id,
        "prom_product_id": m.prom_product_id,
        "score": m.score,
        "status": m.status,
        "created_at": m.created_at.isoformat() if m.created_at else None,
        "confirmed_at": m.confirmed_at.isoformat() if m.confirmed_at else None,
        "confirmed_by": m.confirmed_by,
        "discount_percent": m.discount_percent,
        "name_synced": m.name_synced,
        "feed_name": m.feed_name,
        "price_synced_at": m.price_synced_at.isoformat() if m.price_synced_at else None,
        "availability_synced_at": m.availability_synced_at.isoformat() if m.availability_synced_at else None,
        "in_feed": m.in_feed,
        "published": m.published,
        "deletion_candidate": m.deletion_candidate,
    }


def main() -> int:
    app = create_app()
    with app.app_context():
        pps = PromProduct.query.order_by(PromProduct.id).all()
        matches = ProductMatch.query.order_by(ProductMatch.id).all()
        payload = {
            "taken_at": datetime.now(timezone.utc).isoformat(),
            "purpose": "Pre-import safety dump (Horoshop XLSX catalog import)",
            "pp_count": len(pps),
            "match_count": len(matches),
            "prom_products": [pp_row(p) for p in pps],
            "product_matches": [match_row(m) for m in matches],
        }
        ts = datetime.now().strftime("%Y-%m-%d_%H%M")
        out = Path("backups") / f"pre-catalog-import_{ts}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        size_mb = out.stat().st_size / 1024 / 1024
        print(f"✅ Backup saved: {out}")
        print(f"   {len(pps)} PromProducts + {len(matches)} ProductMatches ({size_mb:.1f} MB)")
        print(f"\nRestore: .venv/Scripts/python.exe scripts/restore_pp_from_backup.py {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
