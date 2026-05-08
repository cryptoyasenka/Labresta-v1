"""End-to-end prod verification — covers all sync_pipeline stages.

Checks:
1. SyncRun history (stuck? latest per supplier?)
2. SP freshness (last sync per supplier, row counts)
3. Stage 4 (disappeared) — deletion_candidate flag set anywhere?
4. Stage 5/6 (matching) — candidate counts match claim
5. Stage 6.5 (auto-confirm) — 487 Astim confirmed, breakdown by rule_used
6. Stage 7 (YML) — file exists, mtime fresh?
7. Data integrity — M:1 violations (1 PP, multiple confirmed matches)
8. Astim-10-candidates — all display_article duplicates?
9. Orphan PP (Hendi without supplier match) — count for Phase 8 baseline
"""
import os
import sys
from datetime import datetime, timezone, timedelta

from app import create_app
from app.extensions import db
from app.models import (
    ProductMatch, Supplier, SupplierProduct, PromProduct, SyncRun,
)
from sqlalchemy import func, and_

sys.stdout.reconfigure(encoding="utf-8")


def hr(title):
    print()
    print("=" * 70)
    print(f"  {title}")
    print("=" * 70)


app = create_app()
with app.app_context():
    suppliers = {s.id: s.name for s in Supplier.query.all()}

    # 1. SyncRun history
    hr("1. SYNC RUNS — stuck / recent / per-supplier")
    stuck = SyncRun.query.filter_by(status="running").all()
    print(f"  STUCK running: {len(stuck)}")
    for sr in stuck:
        age = datetime.now(timezone.utc) - sr.started_at.replace(tzinfo=timezone.utc) \
            if sr.started_at and sr.started_at.tzinfo is None \
            else datetime.now(timezone.utc) - sr.started_at
        print(f"    id={sr.id} supplier_id={sr.supplier_id} started={sr.started_at} age={age}")

    today = datetime.now(timezone.utc) - timedelta(hours=24)
    recent = SyncRun.query.filter(SyncRun.started_at >= today).order_by(
        SyncRun.id.desc()
    ).all()
    print(f"  Runs last 24h: {len(recent)}")
    for sr in recent[:30]:
        sup = suppliers.get(sr.supplier_id, "?")
        print(f"    id={sr.id} sup={sup!r} status={sr.status} "
              f"start={sr.started_at} done={sr.completed_at}")

    # Per-supplier last successful sync
    print()
    print("  Last successful sync per supplier:")
    for sid, sname in sorted(suppliers.items()):
        last = SyncRun.query.filter_by(supplier_id=sid, status="success").order_by(
            SyncRun.id.desc()
        ).first()
        if last:
            age = datetime.now(timezone.utc) - last.completed_at.replace(tzinfo=timezone.utc) \
                if last.completed_at and last.completed_at.tzinfo is None \
                else (datetime.now(timezone.utc) - last.completed_at if last.completed_at else None)
            print(f"    sup={sname!r:25} id={last.id} done={last.completed_at} age={age}")
        else:
            print(f"    sup={sname!r:25} NEVER SUCCEEDED")

    # 2. SP freshness
    hr("2. SUPPLIER PRODUCTS — freshness per supplier")
    for sid, sname in sorted(suppliers.items()):
        cnt = SupplierProduct.query.filter_by(supplier_id=sid).count()
        latest = db.session.query(func.max(SupplierProduct.last_seen_at)).filter_by(
            supplier_id=sid
        ).scalar()
        print(f"  sup={sname!r:25} rows={cnt:>5} latest_last_seen={latest}")

    # 3. Stage 4 deletion_candidate flag
    hr("3. STAGE 4 — disappeared products → deletion_candidate")
    flagged = ProductMatch.query.filter_by(deletion_candidate=True).count()
    print(f"  ProductMatch.deletion_candidate=True: {flagged}")
    if flagged:
        sample = ProductMatch.query.filter_by(deletion_candidate=True).limit(5).all()
        for m in sample:
            sp = db.session.get(SupplierProduct, m.supplier_product_id)
            pp = db.session.get(PromProduct, m.prom_product_id)
            sname = suppliers.get(sp.supplier_id, "?") if sp else "?"
            print(f"    m={m.id} sup={sname} status={m.status} "
                  f"PP={(pp.name or pp.name_ru or '?')[:50] if pp else '?'}")

    # 4. Match status & R0 rule breakdown
    hr("4. MATCHES BY STATUS + R0 RULE BREAKDOWN")
    statuses = db.session.query(
        SupplierProduct.supplier_id,
        ProductMatch.status,
        func.count(ProductMatch.id),
    ).join(
        SupplierProduct, ProductMatch.supplier_product_id == SupplierProduct.id
    ).group_by(
        SupplierProduct.supplier_id, ProductMatch.status,
    ).order_by(SupplierProduct.supplier_id, ProductMatch.status).all()
    for sid, status, cnt in statuses:
        sname = suppliers.get(sid, "?")
        print(f"  sup={sname!r:25} status={status:>10}: {cnt}")

    print()
    print("  confirmed_by breakdown (rule provenance):")
    rule_breakdown = db.session.query(
        ProductMatch.confirmed_by, func.count(ProductMatch.id),
    ).filter(
        ProductMatch.status.in_(["confirmed", "manual"])
    ).group_by(ProductMatch.confirmed_by).order_by(
        func.count(ProductMatch.id).desc()
    ).all()
    for rule, cnt in rule_breakdown:
        print(f"    {rule!r:60}: {cnt}")

    # 5. Stage 7 — YML files
    hr("5. STAGE 7 — YML FEED FILES")
    yml_paths = []
    for root in ["instance", "static", "data", "."]:
        if os.path.isdir(root):
            for fn in os.listdir(root):
                if fn.endswith(".xml") or fn.endswith(".yml"):
                    yml_paths.append(os.path.join(root, fn))
    if not yml_paths:
        print("  (no YML/XML files found in instance/static/data/.)")
    for p in yml_paths:
        st = os.stat(p)
        mtime = datetime.fromtimestamp(st.st_mtime, tz=timezone.utc)
        age = datetime.now(timezone.utc) - mtime
        print(f"  {p}: size={st.st_size:>10} mtime={mtime} age={age}")

    # 6. Data integrity — M:1 violations
    hr("6. DATA INTEGRITY — M:1 violations (1 PP → multiple confirmed)")
    multi = db.session.query(
        ProductMatch.prom_product_id, func.count(ProductMatch.id),
    ).filter(
        ProductMatch.status.in_(["confirmed", "manual"])
    ).group_by(ProductMatch.prom_product_id).having(
        func.count(ProductMatch.id) > 1
    ).all()
    print(f"  PP with >1 confirmed/manual match: {len(multi)}")
    for pp_id, cnt in multi[:10]:
        pp = db.session.get(PromProduct, pp_id)
        print(f"    pp_id={pp_id} count={cnt} name={(pp.name or pp.name_ru or '?')[:50] if pp else '?'}")
        # Show offending matches
        ms = ProductMatch.query.filter_by(prom_product_id=pp_id).filter(
            ProductMatch.status.in_(["confirmed", "manual"])
        ).all()
        for m in ms:
            sp = db.session.get(SupplierProduct, m.supplier_product_id)
            print(f"      m={m.id} sup={suppliers.get(sp.supplier_id) if sp else '?'} "
                  f"art={sp.article if sp else '?'} status={m.status} by={m.confirmed_by}")

    # 7. Astim 10 candidates — verify they're all "display_article duplicate" pattern
    hr("7. ASTIM 10 CANDIDATES — sanity check")
    astim_cands = db.session.query(ProductMatch).join(
        SupplierProduct, ProductMatch.supplier_product_id == SupplierProduct.id
    ).filter(
        SupplierProduct.supplier_id == 8,
        ProductMatch.status == "candidate",
    ).order_by(ProductMatch.id.desc()).all()
    print(f"  Total Astim candidates: {len(astim_cands)}")
    for m in astim_cands:
        sp = db.session.get(SupplierProduct, m.supplier_product_id)
        pp = db.session.get(PromProduct, m.prom_product_id)
        sp_art = sp.article or "?"
        pp_disp = pp.display_article or "?"
        in_name = sp_art.lower() in (pp.name or "").lower() or sp_art.lower() in (pp.name_ru or "").lower()
        flag = "DISPLAY_ART_OK_NAME_FAIL" if (sp_art == pp_disp and not in_name) \
            else ("FUZZY" if m.score < 100 else "OTHER")
        print(f"    m={m.id} score={m.score} flag={flag}")
        print(f"      SP[art={sp_art!r}] {(sp.name or '?')[:55]}")
        print(f"      PP[disp={pp_disp!r}] {(pp.name or pp.name_ru or '?')[:55]}")

    # 8. Orphan Hendi PP (Phase 8 baseline)
    hr("8. ORPHAN PP — Hendi without confirmed match (Phase 8 baseline)")
    # PP with brand=Hendi
    hendi_total = PromProduct.query.filter(
        func.lower(PromProduct.brand) == "hendi"
    ).count()
    print(f"  Total Hendi PP: {hendi_total}")

    # Hendi PP with confirmed/manual match
    hendi_with_match = db.session.query(
        func.count(func.distinct(ProductMatch.prom_product_id))
    ).join(
        PromProduct, ProductMatch.prom_product_id == PromProduct.id
    ).filter(
        func.lower(PromProduct.brand) == "hendi",
        ProductMatch.status.in_(["confirmed", "manual"]),
    ).scalar()
    print(f"  Hendi PP with confirmed match: {hendi_with_match}")
    print(f"  Hendi PP WITHOUT confirmed match: {hendi_total - hendi_with_match}")

    # Cross-check: of those, how many missing from Astim feed?
    matched_ids = db.session.query(ProductMatch.prom_product_id).filter(
        ProductMatch.status.in_(["confirmed", "manual"])
    ).distinct().subquery()
    orphans = PromProduct.query.filter(
        func.lower(PromProduct.brand) == "hendi",
        PromProduct.id.notin_(db.session.query(matched_ids.c.prom_product_id))
    ).all()
    astim_articles = set(
        a for (a,) in db.session.query(SupplierProduct.article).filter_by(
            supplier_id=8
        ).all() if a
    )
    truly_orphan = []
    have_candidate = 0
    for pp in orphans:
        if pp.display_article and pp.display_article in astim_articles:
            have_candidate += 1
        else:
            truly_orphan.append(pp)
    print(f"  Of unmatched Hendi: have candidate in Astim feed: {have_candidate}")
    print(f"  Of unmatched Hendi: TRULY ORPHAN (not in Astim feed): {len(truly_orphan)}")
    print("  Sample truly-orphan (max 10):")
    for pp in truly_orphan[:10]:
        print(f"    pp_id={pp.id} disp={pp.display_article!r} "
              f"name={(pp.name or pp.name_ru or '?')[:55]}")

    # 9. Badge sanity
    hr("9. BADGE 14 — ground truth")
    # Reproduce inject_pending_review_count logic
    claimed_pp = db.session.query(ProductMatch.prom_product_id).filter(
        ProductMatch.status.in_(["confirmed", "manual"])
    ).distinct().subquery()
    badge = ProductMatch.query.filter(
        ProductMatch.status == "candidate",
        ProductMatch.prom_product_id.notin_(db.session.query(claimed_pp.c.prom_product_id))
    ).count()
    print(f"  Computed badge value: {badge}")
    print(f"  Total candidates: {ProductMatch.query.filter_by(status='candidate').count()}")

    print()
    print("=" * 70)
    print("DONE")
