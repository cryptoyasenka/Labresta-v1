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
    name = kwargs.pop("name", None) or f"PP-{display_article}"
    extid_suffix = kwargs.pop("extid_suffix", "")
    pp = PromProduct(
        external_id=f"pp-{display_article or 'none'}-{extid_suffix or name[:8]}",
        name=name,
        brand=brand,
        display_article=display_article,
        **kwargs,
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


def test_pp_without_display_article_falls_back_to_name_scan(db):
    """PP without display_article: Phase M fallback scans pp.name for any
    SP article from the supplier. With the helper-default name 'PP-None'
    no SP article is contained → orphan."""
    s = _mk_supplier(db, "Astim")
    _mk_sp(db, s.id, "Hendi", "111111")
    pp = _mk_pp(db, "Hendi", None)
    db.session.commit()

    result = flag_orphan_pps()
    assert result["flagged"] == 1
    db.session.refresh(pp)
    assert pp.operator_decision == "needs_delete"


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


def test_exclude_dead_suppliers_unblocks_run(db):
    """If a supplier has 0 fresh SPs (broken feed), exclude_dead_suppliers=True
    bypasses the drop-check sanity guard for that supplier. Dead suppliers
    REMAIN in the brand-anchor count: a brand carried by a temporarily-dead
    supplier is still considered 'covered' (we don't false-flag PPs whose
    intended supplier is just temporarily broken)."""
    s_dead = _mk_supplier(db, "BrokenFeed")  # all stale
    s_live = _mk_supplier(db, "Astim")
    # Dead supplier: 11 stale SPs, 0 fresh — total>10 so drop check would trip
    for i in range(11):
        _mk_sp(db, s_dead.id, "Hendi", f"old{i}", fresh=False)
    # Live supplier: fresh SPs only
    _mk_sp(db, s_live.id, "Hendi", "111", fresh=True)
    pp_orphan = _mk_pp(db, "Hendi", "999")
    pp_kept = _mk_pp(db, "Hendi", "111")
    db.session.commit()

    blocked = flag_orphan_pps()
    assert blocked["flagged"] == 0
    assert "drop" in blocked["skipped_reason"].lower()

    result = flag_orphan_pps(exclude_dead_suppliers=True)
    # Drop-check bypassed (no skipped_reason), dead supplier listed,
    # but Hendi has 2 suppliers (BrokenFeed + Astim) → NOT single-supplier
    # → no orphans flagged.
    assert result["flagged"] == 0
    assert result["skipped_reason"] == ""
    assert s_dead.id in result["dead_supplier_ids"]
    assert result["brand_single_supplier_count"] == 0
    db.session.refresh(pp_orphan)
    db.session.refresh(pp_kept)
    assert pp_orphan.operator_decision is None
    assert pp_kept.operator_decision is None


def test_skips_brand_only_at_dead_supplier(db):
    """If a brand's only supplier is dead (broken feed), we cannot reliably
    classify its PPs as orphan — skip rather than flag using stale data."""
    s_dead = _mk_supplier(db, "BrokenFeed")
    # 11 stale SPs → counts as dead (recent==0, total>0)
    for i in range(11):
        _mk_sp(db, s_dead.id, "Hendi", f"old{i}", fresh=False)
    pp = _mk_pp(db, "Hendi", "999")
    db.session.commit()

    result = flag_orphan_pps(exclude_dead_suppliers=True)
    assert result["flagged"] == 0
    assert s_dead.id in result["dead_supplier_ids"]
    assert result["brand_single_supplier_count"] == 0
    db.session.refresh(pp)
    assert pp.operator_decision is None


def test_clears_when_brand_no_longer_single_supplier(db):
    """If a brand was single-supplier (auto-flagged orphan) but a 2nd supplier
    is added later that also carries the brand, the auto-flag must clear on
    next run — same reversibility guarantee as 'PP returns to feed'."""
    s1 = _mk_supplier(db, "Astim")
    _mk_sp(db, s1.id, "Hendi", "111")
    pp = _mk_pp(
        db, "Hendi", "999",
        operator_decision="needs_delete",
        operator_decision_note=AUTO_NOTE,
    )
    db.session.commit()

    # Simulate a second supplier joining with the same brand.
    s2 = _mk_supplier(db, "Maresto")
    _mk_sp(db, s2.id, "Hendi", "222")
    db.session.commit()

    result = flag_orphan_pps()
    assert result["flagged"] == 0
    assert result["cleared"] == 1
    db.session.refresh(pp)
    assert pp.operator_decision is None
    assert pp.operator_decision_note is None


def test_clears_when_pp_gets_confirmed_match(db):
    """If a PP was auto-flagged but later got a confirmed match, the auto-flag
    must clear on next run."""
    s = _mk_supplier(db, "Astim")
    sp = _mk_sp(db, s.id, "Hendi", "111")
    pp = _mk_pp(
        db, "Hendi", "999",
        operator_decision="needs_delete",
        operator_decision_note=AUTO_NOTE,
    )
    db.session.commit()

    # A confirmed match appears between runs.
    db.session.add(ProductMatch(
        supplier_product_id=sp.id,
        prom_product_id=pp.id,
        status="confirmed",
        score=100,
    ))
    db.session.commit()

    result = flag_orphan_pps()
    assert result["flagged"] == 0
    assert result["cleared"] == 1
    db.session.refresh(pp)
    assert pp.operator_decision is None
    assert pp.operator_decision_note is None


def test_exclude_dead_does_not_skip_partial_drop(db):
    """exclude_dead only excludes recent==0 suppliers. A supplier with PARTIAL
    drop (recent>0 but <50%) must still trip the sanity guard."""
    s = _mk_supplier(db, "FlakySupplier")
    for i in range(20):
        _mk_sp(db, s.id, "Hendi", f"old{i}", fresh=False)
    _mk_sp(db, s.id, "Hendi", "fresh1", fresh=True)
    _mk_pp(db, "Hendi", "999")
    db.session.commit()

    result = flag_orphan_pps(exclude_dead_suppliers=True)
    assert result["flagged"] == 0
    assert "drop" in result["skipped_reason"].lower()


# ---------------------------------------------------------------------------
# Phase M: fallback for PPs without display_article — SKU inside pp.name
# (Hurakan/Apach NP rows; catalog has no Horoshop article column filled)
# ---------------------------------------------------------------------------
def test_no_display_flag_orphan_when_no_sp_article_in_name(db):
    """PP without display_article and no matching SP article in pp.name → orphan."""
    s = _mk_supplier(db, "Новый Проект")
    _mk_sp(db, s.id, "Hurakan", "HKN-DHD10GM")  # supplier carries different SKU
    pp_orphan = _mk_pp(db, "Hurakan", None, name="Кип'ятильник Hurakan HKN-HVN10")
    db.session.commit()

    result = flag_orphan_pps()
    assert result["flagged"] == 1
    db.session.refresh(pp_orphan)
    assert pp_orphan.operator_decision == "needs_delete"
    assert pp_orphan.operator_decision_note == AUTO_NOTE


def test_no_display_keeps_pp_when_sp_article_present_in_name(db):
    """PP without display_article but pp.name contains an SP article → not orphan."""
    s = _mk_supplier(db, "Новый Проект")
    _mk_sp(db, s.id, "Hurakan", "HKN-J45SN2V")
    pp_kept = _mk_pp(
        db, "Hurakan", None,
        name="Тістоміс Hurakan HKN-J45SN2V на 45 л (380B)",
    )
    db.session.commit()

    result = flag_orphan_pps()
    assert result["flagged"] == 0
    db.session.refresh(pp_kept)
    assert pp_kept.operator_decision is None


def test_no_display_dash_suffix_is_different_sku(db):
    """SP 'HKN-GXSD2GN' must NOT save a PP whose name has 'HKN-GXSD2GN-SC' —
    they are different SKUs (matcher fast-path rejects same boundary case)."""
    s = _mk_supplier(db, "Новый Проект")
    _mk_sp(db, s.id, "Hurakan", "HKN-GXSD2GN")
    pp_orphan = _mk_pp(
        db, "Hurakan", None,
        name="Шафа холодильна HURAKAN HKN-GXSD2GN-SC",
    )
    db.session.commit()

    result = flag_orphan_pps()
    assert result["flagged"] == 1
    db.session.refresh(pp_orphan)
    assert pp_orphan.operator_decision == "needs_delete"


def test_no_display_short_or_pure_letter_sp_article_ignored(db):
    """SP articles below len 5 or pure-letter no-structure must not save
    PPs (too weak a signal — same gate as matcher fast-path)."""
    s = _mk_supplier(db, "Новый Проект")
    _mk_sp(db, s.id, "Hurakan", "ABCD")          # too short — ignored
    _mk_sp(db, s.id, "Hurakan", "HKNFNTMNEW")    # pure letters, no structure — ignored
    pp_orphan = _mk_pp(
        db, "Hurakan", None,
        name="Гриль HURAKAN ABCD контактний HKNFNTMNEW",
    )
    db.session.commit()

    result = flag_orphan_pps()
    assert result["flagged"] == 1
    db.session.refresh(pp_orphan)
    assert pp_orphan.operator_decision == "needs_delete"


def test_no_display_back_in_feed_clears_auto_flag(db):
    """When PP without display gets an SP article (back in feed),
    a previously auto-set 'needs_delete' is cleared."""
    s = _mk_supplier(db, "Новый Проект")
    pp = _mk_pp(
        db, "Hurakan", None,
        name="ДЕГІДРАТОР HURAKAN HKN-DHD10G",
        operator_decision="needs_delete",
        operator_decision_note=AUTO_NOTE,
    )
    _mk_sp(db, s.id, "Hurakan", "HKN-DHD10G")
    db.session.commit()

    result = flag_orphan_pps()
    assert result["cleared"] == 1
    db.session.refresh(pp)
    assert pp.operator_decision is None
    assert pp.operator_decision_note is None
