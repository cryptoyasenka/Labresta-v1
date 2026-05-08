"""Quick prod-DB inspection — supplier/match counts + sample wrong matches."""
import sys
from app import create_app
from app.extensions import db
from app.models import ProductMatch, Supplier, SupplierProduct, PromProduct
from sqlalchemy import func

# Force UTF-8 stdout
sys.stdout.reconfigure(encoding="utf-8")

app = create_app()
with app.app_context():
    print("=== Suppliers ===")
    for s in Supplier.query.order_by(Supplier.id).all():
        print(f"  id={s.id} name={s.name!r}")

    print()
    print("=== SP counts per supplier ===")
    rows = db.session.query(
        SupplierProduct.supplier_id, func.count(SupplierProduct.id)
    ).group_by(SupplierProduct.supplier_id).all()
    for sid, cnt in rows:
        print(f"  supplier_id={sid}: {cnt} SP rows")

    print()
    print("=== Match status by supplier (joined via SP) ===")
    rows = db.session.query(
        SupplierProduct.supplier_id,
        ProductMatch.status,
        func.count(ProductMatch.id),
    ).join(
        SupplierProduct, ProductMatch.supplier_product_id == SupplierProduct.id
    ).group_by(
        SupplierProduct.supplier_id, ProductMatch.status
    ).order_by(
        SupplierProduct.supplier_id, ProductMatch.status
    ).all()
    for sid, status, cnt in rows:
        print(f"  supplier={sid} status={status}: {cnt}")

    print()
    print("=== Total candidates (badge value) ===")
    print(f"  {ProductMatch.query.filter_by(status='candidate').count()}")

    print()
    print("=== ALL candidates detail ===")
    cands = ProductMatch.query.filter_by(status="candidate").order_by(
        ProductMatch.id.desc()
    ).all()
    for m in cands:
        sp = SupplierProduct.query.get(m.supplier_product_id)
        pp = PromProduct.query.get(m.prom_product_id)
        sp_name = (sp.name or "?")[:60] if sp else "?"
        sp_art = sp.article if sp else "?"
        sp_sup = sp.supplier_id if sp else "?"
        pp_name = ((pp.name or pp.name_ru or "?")[:60]) if pp else "?"
        pp_disp = pp.display_article if pp else "?"
        pp_art = pp.article if pp else "?"
        print(
            f"  m={m.id} sup={sp_sup} score={m.score} status={m.status}\n"
            f"    SP[id={m.supplier_product_id} art={sp_art!r}] {sp_name}\n"
            f"    PP[id={m.prom_product_id} disp={pp_disp!r} art={pp_art!r}] {pp_name}"
        )

    print()
    print("=== Astim CONFIRMED last 5 (sanity) ===")
    confirmed = db.session.query(ProductMatch).join(
        SupplierProduct, ProductMatch.supplier_product_id == SupplierProduct.id
    ).filter(
        SupplierProduct.supplier_id == 8,
        ProductMatch.status.in_(["confirmed", "manual"]),
    ).order_by(ProductMatch.id.desc()).limit(5).all()
    for m in confirmed:
        sp = SupplierProduct.query.get(m.supplier_product_id)
        pp = PromProduct.query.get(m.prom_product_id)
        sp_name = (sp.name or "?")[:60] if sp else "?"
        pp_name = ((pp.name or pp.name_ru or "?")[:60]) if pp else "?"
        print(
            f"  m={m.id} score={m.score} status={m.status} confirmed_by={m.confirmed_by}\n"
            f"    SP[art={sp.article!r}] {sp_name}\n"
            f"    PP[disp={pp.display_article!r}] {pp_name}"
        )
