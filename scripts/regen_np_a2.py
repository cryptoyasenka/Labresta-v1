"""Regen NP matcher (supplier_id=2) to pick up A2-gap fast-path."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.services.matcher import run_matching_for_supplier

app = create_app()
with app.app_context():
    added = run_matching_for_supplier(2)
    print(f"NEW candidate rows added: {added}")
