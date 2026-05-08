"""Diagnose why MARESTO sync (supplier_id=1) fails on every run."""
import sys
from app import create_app
from app.extensions import db
from app.models import SyncRun, Supplier

sys.stdout.reconfigure(encoding="utf-8")

app = create_app()
with app.app_context():
    sup = db.session.get(Supplier, 1)
    print(f"=== Supplier ===")
    print(f"  id=1 name={sup.name!r}")
    print(f"  feed_url={sup.feed_url!r}")
    print(f"  parser_type={getattr(sup, 'parser_type', '?')}")
    print(f"  is_active={getattr(sup, 'is_active', '?')}")
    print()
    print(f"=== Last 5 MARESTO sync runs ===")
    runs = SyncRun.query.filter_by(supplier_id=1).order_by(
        SyncRun.id.desc()
    ).limit(5).all()
    for r in runs:
        print(f"  id={r.id} status={r.status}")
        print(f"    started={r.started_at} done={r.completed_at}")
        print(f"    error={r.error_message!r}")
        print()
