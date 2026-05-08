"""Stage 4.5: flag PromProducts as orphan-deletion candidates.

Runs after fetch-all completes. Identifies PPs whose brand is carried by
exactly one enabled supplier, but that supplier's feed does not contain a
SupplierProduct with article matching pp.display_article. Such PPs are
de-facto out of stock — flagged via operator_decision='needs_delete'.

When pp.display_article is empty, fall back to scanning pp.name for any
SP article from that supplier (mirrors matcher fast-path for catalogs
where the SKU lives only inside the product name — Hurakan/Apach NP rows).

Sanity guards:
  - If any single supplier's recent SP-recency dropped >50%, skip the
    whole run (broken-feed protection — same logic as Stage 4).
  - Never overwrites operator_decision if it was set manually (note != AUTO_NOTE).
  - Idempotent: re-running with the same data produces no changes.
  - Reversible: if a PP returns to feed, the auto-flag is cleared.
"""
from __future__ import annotations

import logging
import re
from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select

from app.extensions import db
from app.models.catalog import PromProduct
from app.models.product_match import ProductMatch
from app.models.supplier import Supplier
from app.models.supplier_product import SupplierProduct
from app.services.brand_supplier_overrides import is_excluded as _brand_supplier_excluded
from app.services.matcher import _fix_cyrillic_homoglyphs

logger = logging.getLogger(__name__)

AUTO_NOTE = "auto:phase8_orphan"


def _now_naive() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _stale_window() -> timedelta:
    """How fresh `last_seen_at` must be to count as 'this sync'.
    4h cron interval + 1h buffer."""
    return timedelta(hours=5)


def _dead_supplier_ids() -> set[int]:
    """Return ids of enabled suppliers with 0 SPs in latest sync window.

    'Dead' = consistently broken feed (e.g. external 403 / DNS failure),
    not a one-off transient drop. Used to optionally exclude such suppliers
    from brand-anchor count + drop-check."""
    cutoff = _now_naive() - _stale_window()
    rows = db.session.execute(
        select(
            Supplier.id,
            func.count(SupplierProduct.id).filter(
                SupplierProduct.last_seen_at >= cutoff
            ).label("recent"),
            func.count(SupplierProduct.id).label("total"),
        )
        .join(SupplierProduct, SupplierProduct.supplier_id == Supplier.id, isouter=True)
        .where(Supplier.is_enabled.is_(True))
        .group_by(Supplier.id)
    ).all()
    return {sid for sid, recent, total in rows if total > 0 and (recent or 0) == 0}


def _brand_supplier_counts(exclude_supplier_ids: set[int] | None = None) -> dict[str, list[int]]:
    """Return {lower(brand): [supplier_id, ...]} for enabled suppliers
    that have at least one SP with that brand.

    Args:
        exclude_supplier_ids: supplier ids to skip (e.g. dead suppliers).
    """
    excluded = exclude_supplier_ids or set()
    rows = db.session.execute(
        select(
            func.lower(SupplierProduct.brand),
            SupplierProduct.supplier_id,
        )
        .join(Supplier, Supplier.id == SupplierProduct.supplier_id)
        .where(
            Supplier.is_enabled.is_(True),
            SupplierProduct.brand.isnot(None),
        )
        .distinct()
    ).all()
    out: dict[str, list[int]] = {}
    for brand_lower, sup_id in rows:
        if not brand_lower:
            continue
        if sup_id in excluded:
            continue
        if _brand_supplier_excluded(brand_lower, sup_id):
            continue  # hardcoded blocklist (e.g. Hendi at Кодаки)
        out.setdefault(brand_lower, []).append(sup_id)
    return out


def _pp_articles_in_supplier(supplier_id: int) -> set[str]:
    """Return set of SP.article (lower-cased) for one supplier, non-null."""
    rows = db.session.execute(
        select(func.lower(SupplierProduct.article)).where(
            SupplierProduct.supplier_id == supplier_id,
            SupplierProduct.article.isnot(None),
        )
    ).all()
    return {a for (a,) in rows if a}


def _supplier_article_strings(supplier_id: int) -> list[str]:
    """Raw SP article strings (preserve case+spacing) for in-name boundary scan."""
    rows = db.session.execute(
        select(SupplierProduct.article).where(
            SupplierProduct.supplier_id == supplier_id,
            SupplierProduct.article.isnot(None),
            SupplierProduct.article != "",
        )
    ).all()
    seen: set[str] = set()
    out: list[str] = []
    for (art,) in rows:
        if not art:
            continue
        key = art.strip()
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(key)
    return out


def _build_sp_article_boundary_re(raw_article: str) -> re.Pattern | None:
    """Compile a word-boundary regex for an SP article in pp.name.

    Mirrors matcher.py:1217-1221 fast-path: requires len>=5, has digit OR
    non-alphanumeric structure (skip pure-letter weak signals like
    "HKNFNTMNEW"); rejects dash-suffix continuation so 'HKN-GXSD2GN' won't
    falsely match 'HKN-GXSD2GN-SC'.
    """
    if not raw_article or len(raw_article) < 5:
        return None
    has_digit = any(c.isdigit() for c in raw_article)
    has_structure = any(not c.isalnum() for c in raw_article)
    if not (has_digit or has_structure):
        return None
    raw_article_fixed = _fix_cyrillic_homoglyphs(raw_article)
    escaped = re.escape(raw_article_fixed)
    escaped = re.sub(r"(\\[ \t])+", r"\\s+", escaped)
    if not any(c.isspace() for c in raw_article_fixed):
        escaped = re.sub(
            r"(?<=[A-Za-zА-Яа-яЁёІіЇїЄєҐґ])(?=\d)"
            r"|(?<=\d)(?=[A-Za-zА-Яа-яЁёІіЇїЄєҐґ])",
            r"\\s*",
            escaped,
        )
    return re.compile(
        rf"(?<![0-9A-Za-zА-Яа-яЁёІіЇїЄєҐґ]){escaped}"
        rf"(?![0-9A-Za-zА-Яа-яЁёІіЇїЄєҐґ]|-[0-9A-Za-zА-Яа-яЁёІіЇїЄєҐґ])",
        re.IGNORECASE | re.UNICODE,
    )


def _any_sp_article_in_pp_name(pp_name: str | None, sp_articles: list[str]) -> bool:
    """True if at least one SP article appears (word-boundary) inside pp.name.

    Used as fallback orphan check for PPs without display_article — the SKU
    lives inside the name (HURAKAN HKN-DHD10G in 'ДЕГІДРАТОР HURAKAN HKN-DHD10G').
    """
    if not pp_name:
        return False
    name_fixed = _fix_cyrillic_homoglyphs(pp_name)
    for art in sp_articles:
        rx = _build_sp_article_boundary_re(art)
        if rx is None:
            continue
        if rx.search(name_fixed):
            return True
    return False


def _pps_with_confirmed_match() -> set[int]:
    """Return PP ids that already have a confirmed/manual match."""
    rows = db.session.execute(
        select(ProductMatch.prom_product_id)
        .where(ProductMatch.status.in_(["confirmed", "manual"]))
        .distinct()
    ).all()
    return {pid for (pid,) in rows}


def _feed_drop_check(exclude_supplier_ids: set[int] | None = None) -> tuple[bool, str]:
    """Skip orphan run if any enabled supplier had a *partial* drop
    (>50% of SPs disappeared in last sync window).

    A *fully dead* supplier (recent=0) is treated separately: pass
    `exclude_supplier_ids={dead_ids}` to skip them from this check
    (they are also excluded from brand-anchor counting).
    """
    excluded = exclude_supplier_ids or set()
    enabled = db.session.execute(
        select(Supplier.id, Supplier.name).where(Supplier.is_enabled.is_(True))
    ).all()
    cutoff = _now_naive() - _stale_window()
    for sup_id, sup_name in enabled:
        if sup_id in excluded:
            continue
        total = db.session.execute(
            select(func.count(SupplierProduct.id)).where(
                SupplierProduct.supplier_id == sup_id
            )
        ).scalar() or 0
        recent = db.session.execute(
            select(func.count(SupplierProduct.id)).where(
                SupplierProduct.supplier_id == sup_id,
                SupplierProduct.last_seen_at >= cutoff,
            )
        ).scalar() or 0
        if total > 10 and recent < total * 0.5:
            return False, (
                f"supplier {sup_name!r}: only {recent}/{total} SPs seen "
                "in last sync window (>50% drop) — skipping orphan run"
            )
    return True, ""


def flag_orphan_pps(*, dry_run: bool = False, exclude_dead_suppliers: bool = False) -> dict:
    """Flag orphan PPs (Stage 4.5).

    Args:
        dry_run: If True, don't write to DB — just return what WOULD change.
        exclude_dead_suppliers: If True, suppliers with 0 fresh SPs (broken
            feeds, e.g. permanent 403) are excluded from both the drop-check
            and brand-anchor count. Use when one supplier is known-broken
            but others are fine.

    Returns:
        dict with keys: flagged, cleared, skipped_reason (or empty string),
        L1_total, brand_single_supplier_count, dead_supplier_ids.
    """
    dead_ids = _dead_supplier_ids() if exclude_dead_suppliers else set()

    ok, reason = _feed_drop_check(exclude_supplier_ids=dead_ids)
    if not ok:
        logger.warning("Stage 4.5 skipped: %s", reason)
        return {
            "flagged": 0,
            "cleared": 0,
            "skipped_reason": reason,
            "L1_total": 0,
            "brand_single_supplier_count": 0,
            "dead_supplier_ids": sorted(dead_ids),
        }

    # IMPORTANT: dead suppliers are excluded ONLY from the drop-check above,
    # NOT from the brand-anchor count below. A brand carried by a (possibly dead)
    # supplier is still considered "covered" — we don't want to false-flag PPs
    # whose intended supplier is just temporarily broken.
    #
    # But: if a brand's ONLY supplier is dead, we cannot reliably classify its
    # PPs as orphan (its article list is stale). Skip those brands entirely.
    brand_supps = _brand_supplier_counts()
    matched_pp_ids = _pps_with_confirmed_match()

    single_supp_brands = {
        b: sids[0]
        for b, sids in brand_supps.items()
        if len(sids) == 1 and sids[0] not in dead_ids
    }
    article_index: dict[int, set[str]] = {}
    article_raw_index: dict[int, list[str]] = {}
    for sup_id in set(single_supp_brands.values()):
        article_index[sup_id] = _pp_articles_in_supplier(sup_id)
        article_raw_index[sup_id] = _supplier_article_strings(sup_id)

    pps = db.session.execute(
        select(PromProduct).where(PromProduct.brand.isnot(None))
    ).scalars().all()

    now = _now_naive()
    flagged = 0
    cleared = 0
    L1_orphans: list[int] = []

    def _clear_auto_flag(pp) -> bool:
        """Clear our auto-flag if it's still set. Returns True if cleared."""
        if pp.operator_decision == "needs_delete" and pp.operator_decision_note == AUTO_NOTE:
            if not dry_run:
                pp.operator_decision = None
                pp.operator_decision_note = None
                pp.operator_decision_at = now
            return True
        return False

    for pp in pps:
        brand_l = (pp.brand or "").lower().strip()
        if not brand_l:
            continue
        sup_id = single_supp_brands.get(brand_l)
        if sup_id is None:
            # Brand no longer single-supplier (or has 0) — clear stale auto-flag
            # if we previously set it (e.g. a 2nd supplier was added since).
            if _clear_auto_flag(pp):
                cleared += 1
            continue
        if pp.id in matched_pp_ids:
            # PP got a confirmed match since we flagged it — clear stale auto-flag.
            if _clear_auto_flag(pp):
                cleared += 1
            continue

        disp = (pp.display_article or "").lower().strip()
        articles = article_index.get(sup_id, set())
        if disp:
            is_orphan = disp not in articles
        else:
            # Fallback for catalogs whose SKU lives only in pp.name (Hurakan/
            # Apach NP rows have no Horoshop article/display field): scan
            # pp.name for any SP article from this supplier with the same
            # word-boundary regex matcher fast-path uses. If none of the
            # supplier's articles is present in the name, the PP is orphan.
            sp_arts = article_raw_index.get(sup_id, [])
            is_orphan = not _any_sp_article_in_pp_name(pp.name, sp_arts)

        note_is_ours = pp.operator_decision_note == AUTO_NOTE
        current = pp.operator_decision

        if is_orphan:
            L1_orphans.append(pp.id)
            # Flag only if currently NULL/pending OR previously auto-set by us.
            if current in (None, "pending") or note_is_ours:
                if not (current == "needs_delete" and note_is_ours):
                    if not dry_run:
                        pp.operator_decision = "needs_delete"
                        pp.operator_decision_note = AUTO_NOTE
                        pp.operator_decision_at = now
                    flagged += 1
        else:
            # PP is back in feed — clear ONLY our own auto-flag.
            if _clear_auto_flag(pp):
                cleared += 1

    if not dry_run:
        db.session.commit()

    logger.info(
        "Stage 4.5 done: flagged=%d cleared=%d L1_total=%d single_supplier_brands=%d",
        flagged, cleared, len(L1_orphans), len(single_supp_brands),
    )
    return {
        "flagged": flagged,
        "cleared": cleared,
        "skipped_reason": "",
        "L1_total": len(L1_orphans),
        "brand_single_supplier_count": len(single_supp_brands),
        "dead_supplier_ids": sorted(dead_ids),
    }
