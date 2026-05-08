"""Unit tests for Phase 8 orphan_detector (Stage 4.5)."""
from datetime import datetime, timedelta, timezone

from app.models.catalog import PromProduct
from app.models.product_match import ProductMatch
from app.models.supplier import Supplier, slugify_supplier_name
from app.models.supplier_product import SupplierProduct
from app.services.orphan_detector import AUTO_NOTE, flag_orphan_pps


def _mk_supplier(db, name, enabled=True):
    s = Supplier(
        name=name,
        slug=slugify_supplier_name(name),
        feed_url=f"http://example/{slugify_supplier_name(name)}.xml",
        is_enabled=enabled,
    )
    db.session.add(s)
    db.session.flush()
    return s


def _mk_sp(db, supplier_id, brand, article, *, fresh=True):
    seen = datetime.now(timezone.utc).replace(tzinfo=None)
    if not fresh:
        seen -= timedelta(days=2)
    sp = SupplierProduct(
        supplier_id=supplier_id,
        external_id=f"{supplier_id}-{article}",
        name=f"sp-{article}",
        brand=brand,
        article=article,
        available=True,
        last_seen_at=seen,
    )
    db.session.add(sp)
    db.session.flush()
    return sp


def _mk_pp(db, brand, display_article, **kwargs):
    pp = PromProduct(
        external_id=f"pp-{display_article or 'none'}-{kwargs.get('extid_suffix', '')}",
        name=f"PP-{display_article}",
        brand=brand,
        display_article=display_article,
        **{k: v for k, v in kwargs.items() if k != "extid_suffix"},
    )
    db.session.add(pp)
    db.session.flush()
    return pp


def test_l1_flags_when_brand_has_single_supplier_no_match(db):
    s = _mk_supplier(db, "Astim")
    _mk_sp(db, s.id, "Hendi", "111111")
    pp_orphan = _mk_pp(db, "Hendi", "999999")
    pp_kept = _mk_pp(db, "Hendi", "111111")
    db.session.commit()

    result = flag_orphan_pps()
    assert result["flagged"] == 1
    assert result["L1_total"] == 1
    db.session.refresh(pp_orphan)
    db.session.refresh(pp_kept)
    assert pp_orphan.operator_decision == "needs_delete"
    assert pp_orphan.operator_decision_note == AUTO_NOTE
    assert pp_orphan.operator_decision_at is not None
    assert pp_kept.operator_decision is None


def test_does_not_overwrite_manual_decision(db):
    s = _mk_supplier(db, "Astim")
    _mk_sp(db, s.id, "Hendi", "111111")
    pp = _mk_pp(
        db, "Hendi", "999999",
        operator_decision="keep_searching",
        operator_decision_note="manual: still hunting",
    )
    db.session.commit()

    flag_orphan_pps()
    db.session.refresh(pp)
    assert pp.operator_decision == "keep_searching"
    assert pp.operator_decision_note == "manual: still hunting"


def test_does_not_overwrite_manual_needs_delete(db):
    """If operator manually set needs_delete (note != AUTO_NOTE), don't touch."""
    s = _mk_supplier(db, "Astim")
    _mk_sp(db, s.id, "Hendi", "111111")
    pp = _mk_pp(
        db, "Hendi", "999999",
        operator_decision="needs_delete",
        operator_decision_note="manual: confirmed dead SKU",
    )
    db.session.commit()

    flag_orphan_pps()
    db.session.refresh(pp)
    assert pp.operator_decision == "needs_delete"
    assert pp.operator_decision_note == "manual: confirmed dead SKU"


def test_skips_pp_with_confirmed_match(db):
    s = _mk_supplier(db, "Astim")
    sp = _mk_sp(db, s.id, "Hendi", "111111")
    pp = _mk_pp(db, "Hendi", "999999")  # not in feed by article
    m = ProductMatch(
        supplier_product_id=sp.id,
        prom_product_id=pp.id,
        status="confirmed",
        score=100,
    )
    db.session.add(m)
    db.session.commit()

    flag_orphan_pps()
    db.session.refresh(pp)
    assert pp.operator_decision is None


def test_skips_when_brand_has_multiple_suppliers(db):
    s1 = _mk_supplier(db, "Astim")
    s2 = _mk_supplier(db, "Maresto")
    _mk_sp(db, s1.id, "Hendi", "111")
    _mk_sp(db, s2.id, "Hendi", "222")
    pp = _mk_pp(db, "Hendi", "999999")
    db.session.commit()

    result = flag_orphan_pps()
    db.session.refresh(pp)
    assert pp.operator_decision is None
    assert result["flagged"] == 0
    assert result["brand_single_supplier_count"] == 0


def test_clears_auto_flag_when_pp_returns_to_feed(db):
    s = _mk_supplier(db, "Astim")
    pp = _mk_pp(
        db, "Hendi", "111111",
        operator_decision="needs_delete",
        operator_decision_note=AUTO_NOTE,
    )
    _mk_sp(db, s.id, "Hendi", "111111")
    db.session.commit()

    result = flag_orphan_pps()
    assert result["cleared"] == 1
    db.session.refresh(pp)
    assert pp.operator_decision is None
    assert pp.operator_decision_note is None


def test_idempotent_second_run_is_noop(db):
    s = _mk_supplier(db, "Astim")
    _mk_sp(db, s.id, "Hendi", "111")
    _mk_pp(db, "Hendi", "999")
    db.session.commit()

    r1 = flag_orphan_pps()
    r2 = flag_orphan_pps()
    assert r1["flagged"] == 1
    assert r2["flagged"] == 0
    assert r2["cleared"] == 0


def test_dry_run_does_not_commit(db):
    s = _mk_supplier(db, "Astim")
    _mk_sp(db, s.id, "Hendi", "111")
    pp = _mk_pp(db, "Hendi", "999")
    db.session.commit()

    result = flag_orphan_pps(dry_run=True)
    assert result["flagged"] == 1
    db.session.refresh(pp)
    assert pp.operator_decision is None  # not committed


def test_sanity_guard_skips_on_feed_drop(db):
    s = _mk_supplier(db, "Astim")
    # 20 stale + 1 fresh → recent (1) < 50% of total (21).
    for i in range(20):
        _mk_sp(db, s.id, "Hendi", f"old{i}", fresh=False)
    _mk_sp(db, s.id, "Hendi", "fresh1", fresh=True)
    _mk_pp(db, "Hendi", "999")
    db.session.commit()

    result = flag_orphan_pps()
    assert result["flagged"] == 0
    assert "drop" in result["skipped_reason"].lower()


def test_pp_without_display_article_treated_as_orphan(db):
    """Edge case: PP with brand but no display_article cannot be matched → orphan."""
    s = _mk_supplier(db, "Astim")
    _mk_sp(db, s.id, "Hendi", "111")
    pp = _mk_pp(db, "Hendi", None)
    db.session.commit()

    result = flag_orphan_pps()
    assert result["flagged"] == 1
    db.session.refresh(pp)
    assert pp.operator_decision == "needs_delete"
    assert pp.operator_decision_note == AUTO_NOTE


def test_disabled_supplier_excluded_from_brand_count(db):
    """Brand carried only by disabled suppliers shouldn't count as single-supplier."""
    s_off = _mk_supplier(db, "OldSupplier", enabled=False)
    _mk_sp(db, s_off.id, "Hendi", "111")
    pp = _mk_pp(db, "Hendi", "999")
    db.session.commit()

    result = flag_orphan_pps()
    db.session.refresh(pp)
    assert pp.operator_decision is None
    assert result["brand_single_supplier_count"] == 0
