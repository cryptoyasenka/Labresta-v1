"""Sync pipeline orchestrator — fetch, parse, save, detect disappeared products."""

import logging
from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select

from app.extensions import db
from app.models.supplier import Supplier
from app.models.supplier_product import SupplierProduct
from app.models.sync_run import SyncRun
from app.services.feed_fetcher import fetch_feed_with_retry
from app.services.feed_parser import parse_supplier_feed, save_supplier_products
from app.services.telegram_notifier import (
    notify_disappeared_products,
    notify_sync_failure,
)

logger = logging.getLogger(__name__)


def run_full_sync(supplier_id: int | None = None):
    """Run the full sync pipeline for one or all enabled suppliers.

    Args:
        supplier_id: If given, sync only this supplier. Otherwise sync all enabled.
    """
    if supplier_id is not None:
        supplier = db.session.get(Supplier, supplier_id)
        if not supplier:
            logger.error("Supplier with id=%d not found", supplier_id)
            return
        suppliers = [supplier]
    else:
        suppliers = db.session.execute(
            select(Supplier).where(Supplier.is_enabled == True)  # noqa: E712
        ).scalars().all()

    if not suppliers:
        logger.info("No enabled suppliers to sync")
        return

    results = []
    for supplier in suppliers:
        result = _sync_single_supplier(supplier)
        results.append(result)

    success_count = sum(1 for r in results if r == "success")
    error_count = sum(1 for r in results if r == "error")
    logger.info(
        "Sync complete: %d suppliers processed (%d success, %d error)",
        len(results),
        success_count,
        error_count,
    )


def _sync_single_supplier(supplier: Supplier) -> str:
    """Execute the full sync pipeline for a single supplier.

    Stages: fetch -> parse -> save -> detect reappeared -> detect disappeared.
    Creates a SyncRun audit record with try/finally to guarantee completion tracking.

    Returns:
        Final status string: "success" or "error".
    """
    logger.info("Starting sync for supplier '%s' (id=%d)", supplier.name, supplier.id)

    sync_run = SyncRun(
        supplier_id=supplier.id,
        started_at=datetime.now(timezone.utc),
        status="running",
    )
    db.session.add(sync_run)
    db.session.commit()

    try:
        # Stage 1: Fetch
        logger.info("Stage 1/6: Fetching feed from %s", supplier.feed_url)
        raw_bytes = fetch_feed_with_retry(supplier.feed_url)

        # Stage 2: Parse
        logger.info("Stage 2/6: Parsing feed")
        products = parse_supplier_feed(raw_bytes, supplier.id)
        sync_run.products_fetched = len(products)
        logger.info("Parsed %d products from feed", len(products))

        # Stage 3: Save
        logger.info("Stage 3/6: Saving products")
        result = save_supplier_products(products)
        sync_run.products_created = result["created"]
        sync_run.products_updated = result["updated"]
        logger.info(
            "Saved: %d created, %d updated",
            result["created"],
            result["updated"],
        )

        # Check for reappeared products (after save updates last_seen_at)
        _handle_reappeared_products(supplier.id)

        # Stage 4: Detect disappeared
        logger.info("Stage 4/6: Detecting disappeared products")
        disappeared_count = _detect_disappeared(supplier, len(products), sync_run)
        logger.info("Disappeared products flagged: %d", disappeared_count)

        # Stage 5: Run fuzzy matching for new/unmatched products
        logger.info("Stage 5/6: Running fuzzy matching")
        from app.services.matcher import run_matching_for_supplier

        candidates = run_matching_for_supplier(supplier.id)
        sync_run.match_candidates_generated = candidates
        logger.info("Match candidates generated: %d", candidates)

        # Stage 6: Regenerate YML feed (only runs if all prior stages succeeded)
        logger.info("Stage 6/6: Regenerating YML feed")
        from app.services.yml_generator import regenerate_yml_feed

        yml_result = regenerate_yml_feed()
        logger.info(
            "YML feed regenerated: %d offers (%d available, %d unavailable)",
            yml_result["total"],
            yml_result["available"],
            yml_result["unavailable"],
        )

        sync_run.status = "success"
        return "success"

    except Exception as e:
        logger.error("Sync failed for supplier '%s': %s", supplier.name, e)
        sync_run.status = "error"
        sync_run.error_message = str(e)[:1000]
        notify_sync_failure(supplier.name, str(e), attempt_count=3)
        return "error"

    finally:
        sync_run.completed_at = datetime.now(timezone.utc)
        db.session.commit()


def _detect_disappeared(
    supplier: Supplier, current_count: int, sync_run: SyncRun
) -> int:
    """Flag products missing from feed for 2+ consecutive syncs.

    Includes a sanity check: if feed product count dropped >50% compared to
    existing records, skip disappearance detection (likely a broken/partial feed).

    Args:
        supplier: The supplier being synced.
        current_count: Number of products in the current feed.
        sync_run: Current SyncRun record to update.

    Returns:
        Number of products flagged as disappeared.
    """
    # Sanity check: count existing products for this supplier
    previous_count = db.session.execute(
        select(func.count(SupplierProduct.id)).where(
            SupplierProduct.supplier_id == supplier.id
        )
    ).scalar() or 0

    if previous_count > 0 and current_count < previous_count * 0.5:
        logger.warning(
            "Feed product count dropped >50%% (%d -> %d) for supplier '%s', "
            "skipping disappearance detection",
            previous_count,
            current_count,
            supplier.name,
        )
        return 0

    # Threshold: 2 sync intervals (4h each) + 1h buffer = 9 hours
    threshold = datetime.now(timezone.utc) - timedelta(hours=9)

    # Find stale products that haven't been seen recently
    stale_products = db.session.execute(
        select(SupplierProduct).where(
            SupplierProduct.supplier_id == supplier.id,
            SupplierProduct.last_seen_at < threshold,
            SupplierProduct.available == True,  # noqa: E712
            SupplierProduct.needs_review == False,  # noqa: E712
        )
    ).scalars().all()

    count = len(stale_products)
    for product in stale_products:
        product.available = False
        product.needs_review = True

    if count > 0:
        notify_disappeared_products(supplier.name, count)
        logger.info(
            "Flagged %d disappeared products for supplier '%s'",
            count,
            supplier.name,
        )

    sync_run.products_disappeared = count
    db.session.commit()
    return count


def _handle_reappeared_products(supplier_id: int):
    """Log visibility for products that reappeared in feed after being flagged.

    Per user decision: reappeared products are NOT auto-restored.
    They stay needs_review=True and available=False for manual confirmation.
    This function only provides log visibility.
    """
    # Products that were flagged but now have a recent last_seen_at
    # (save_supplier_products updates last_seen_at for all seen products)
    recent_threshold = datetime.now(timezone.utc) - timedelta(hours=4)

    reappeared = db.session.execute(
        select(SupplierProduct).where(
            SupplierProduct.supplier_id == supplier_id,
            SupplierProduct.needs_review == True,  # noqa: E712
            SupplierProduct.available == False,  # noqa: E712
            SupplierProduct.last_seen_at >= recent_threshold,
        )
    ).scalars().all()

    for product in reappeared:
        logger.info(
            "Product '%s' (id=%d) reappeared in feed but needs manual review",
            product.name,
            product.id,
        )
