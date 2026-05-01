"""Sync pipeline orchestrator — fetch, parse, save, detect disappeared products."""

import json
import logging
import os
import tempfile
from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select

from app.extensions import db
from app.models.product_match import ProductMatch
from app.models.supplier import Supplier
from app.models.supplier_product import SupplierProduct
from app.models.sync_run import SyncRun
from app.services.excel_parser import (
    convert_google_sheets_url,
    is_google_sheets_url,
    is_xlsx_url,
    parse_excel_products,
    validate_xlsx_response,
)
from app.services.rp_parser import parse_rp_sheet
from app.services.feed_fetcher import fetch_feed_with_retry
from app.services.feed_parser import parse_supplier_feed, save_supplier_products
from app.services.kodaki_adapter import apply_supplier_adapter
from app.services.telegram_notifier import (
    notify_disappeared_products,
    notify_sync_failure,
)
from app.views.dashboard import SyncProgress

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

    # Skip re-sync if the supplier was successfully synced within the last 2 hours.
    # Prevents IP-based rate limiting on suppliers like MARESTO that block frequent requests.
    _COOLDOWN = timedelta(hours=2)
    if supplier.last_fetched_at and supplier.last_fetch_status == "success":
        _age = datetime.now(timezone.utc) - supplier.last_fetched_at.replace(tzinfo=timezone.utc)
        if _age < _COOLDOWN:
            logger.info(
                "Skipping '%s' — synced successfully %s ago (cooldown 2h)",
                supplier.name, _age,
            )
            return "skipped"

    sync_run = SyncRun(
        supplier_id=supplier.id,
        started_at=datetime.now(timezone.utc),
        status="running",
    )
    db.session.add(sync_run)
    db.session.commit()

    tmp_path = None
    try:
        is_rp = supplier.parser_type == "rp"
        _feed_url = supplier.feed_url or ""
        is_excel = not is_rp and (is_google_sheets_url(_feed_url) or is_xlsx_url(_feed_url))

        # Stage 1: Fetch
        if is_rp and supplier.feed_url:
            download_url = (
                convert_google_sheets_url(supplier.feed_url)
                if is_google_sheets_url(supplier.feed_url)
                else supplier.feed_url
            )
            logger.info("Stage 1/7: Fetching RP feed from %s", download_url)
            SyncProgress.update("fetching", 0)
            raw_bytes = fetch_feed_with_retry(download_url)
        elif is_rp and not supplier.feed_url:
            raise ValueError(
                "Поставщик '%s' (тип RP) не имеет URL фида." % supplier.name
            )
        elif is_excel:
            # Check column_mapping before fetching — skip gracefully if not configured
            if not supplier.column_mapping:
                msg = (
                    "Маппинг колонок не настроен для поставщика '%s'. "
                    "Настройте через страницу поставщика." % supplier.name
                )
                logger.warning(msg)
                raise ValueError(msg)

            download_url = (
                convert_google_sheets_url(supplier.feed_url)
                if is_google_sheets_url(supplier.feed_url)
                else supplier.feed_url
            )
            logger.info("Stage 1/7: Fetching Excel feed from %s", download_url)
            SyncProgress.update("fetching", 0)
            raw_bytes = fetch_feed_with_retry(download_url)
        elif not supplier.feed_url:
            # File-upload-only supplier without feed_url — skip scheduled sync
            msg = (
                "Поставщик '%s' не имеет URL фида. "
                "Загрузите файл вручную через страницу поставщика." % supplier.name
            )
            logger.warning(msg)
            raise ValueError(msg)
        else:
            logger.info("Stage 1/7: Fetching feed from %s", supplier.feed_url)
            SyncProgress.update("fetching", 0)
            raw_bytes = fetch_feed_with_retry(supplier.feed_url)

        # Stage 2: Parse
        logger.info("Stage 2/7: Parsing feed")
        if is_rp:
            validate_xlsx_response(raw_bytes)
            fd, tmp_path = tempfile.mkstemp(suffix=".xlsx")
            os.close(fd)
            with open(tmp_path, "wb") as f:
                f.write(raw_bytes)
            products, rp_errors = parse_rp_sheet(tmp_path, supplier.id)
            for err in rp_errors:
                logger.warning("RP parse (sync): %s", err)
        elif is_excel:
            validate_xlsx_response(raw_bytes)
            fd, tmp_path = tempfile.mkstemp(suffix=".xlsx")
            os.close(fd)
            with open(tmp_path, "wb") as f:
                f.write(raw_bytes)

            mapping = json.loads(supplier.column_mapping)
            products, errors = parse_excel_products(
                tmp_path, mapping["columns"], mapping["header_row"], supplier.id
            )

            for err in errors:
                logger.warning("Excel parse: %s", err)

            # Sanity check: >50% error rate aborts sync
            if len(errors) > len(products):
                raise ValueError(
                    "Слишком много ошибок парсинга (%d ошибок, %d товаров). "
                    "Проверьте маппинг колонок." % (len(errors), len(products))
                )
        else:
            raw_bytes = apply_supplier_adapter(raw_bytes, supplier.feed_url)
            products = parse_supplier_feed(raw_bytes, supplier.id)

        sync_run.products_fetched = len(products)
        logger.info("Parsed %d products from feed", len(products))
        SyncProgress.update("parsing", len(products), len(products))

        # Stage 3: Save
        logger.info("Stage 3/7: Saving products")
        result = save_supplier_products(products)
        sync_run.products_created = result["created"]
        sync_run.products_updated = result["updated"]
        logger.info(
            "Saved: %d created, %d updated",
            result["created"],
            result["updated"],
        )
        SyncProgress.update(
            "saving", result["total"], result["total"],
            created=result["created"], updated=result["updated"],
        )

        # Notify about new products matching notification rules
        if result["created"] > 0:
            try:
                from app.services.notification_service import check_and_notify

                # Fetch newly created products (last N created for this supplier)
                new_prods = db.session.execute(
                    select(SupplierProduct)
                    .where(SupplierProduct.supplier_id == supplier.id)
                    .order_by(SupplierProduct.id.desc())
                    .limit(result["created"])
                ).scalars().all()
                check_and_notify(new_prods)
            except Exception as notify_err:
                logger.warning("Notification check failed: %s", notify_err)

        # Check for reappeared products (after save updates last_seen_at)
        _handle_reappeared_products(supplier.id)

        # Stage 4: Detect disappeared
        logger.info("Stage 4/7: Detecting disappeared products")
        disappeared_count = _detect_disappeared(supplier, len(products), sync_run)
        logger.info("Disappeared products flagged: %d", disappeared_count)

        # Stage 5: Apply match rules (before fuzzy matching)
        logger.info("Stage 5/7: Applying match rules")
        from app.services.rule_matcher import apply_match_rules
        rules_applied = apply_match_rules(supplier.id)
        logger.info("Match rules applied: %d auto-confirmed", rules_applied)

        # Stage 6: Run fuzzy matching for new/unmatched products
        logger.info("Stage 6/7: Running fuzzy matching")
        from app.services.matcher import run_matching_for_supplier

        candidates = run_matching_for_supplier(supplier.id)
        sync_run.match_candidates_generated = candidates
        logger.info("Match candidates generated: %d", candidates)
        SyncProgress.update("matching", candidates, candidates)

        # Stage 6.5: Safe auto-confirm pass (R1-R4) — promote identical-token
        # candidates so the operator doesn't see 100% matches sitting in the
        # review queue after every sync.
        logger.info("Stage 6.5/7: Safe auto-confirm (bulk_auto_confirm rules)")
        from scripts.bulk_auto_confirm import apply_rules as _apply_safe_rules
        auto_stats = _apply_safe_rules(apply=True, confirmed_by="sync:bulk_auto_confirm")
        logger.info(
            "Auto-confirm: %d confirmed, %d rejected (R4), per_rule=%s",
            auto_stats["confirmed"], auto_stats["rejected"], auto_stats["per_rule"],
        )

        # Stage 7: Regenerate YML feed (only runs if all prior stages succeeded)
        logger.info("Stage 7/7: Regenerating YML feed")
        from app.services.yml_generator import regenerate_yml_feed

        yml_result = regenerate_yml_feed()
        logger.info(
            "YML feed regenerated: %d offers (%d available, %d unavailable)",
            yml_result["total"],
            yml_result["available"],
            yml_result["unavailable"],
        )
        SyncProgress.update("yml_generation", yml_result["total"], yml_result["total"])

        sync_run.status = "success"
        return "success"

    except Exception as e:
        logger.error("Sync failed for supplier '%s': %s", supplier.name, e)
        sync_run.status = "error"
        sync_run.error_message = str(e)[:1000]
        notify_sync_failure(supplier.name, str(e), attempt_count=3)
        return "error"

    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
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
    deletion_candidates = 0
    for product in stale_products:
        product.available = False
        product.needs_review = True

        # Handle existing matches:
        # confirmed/manual → mark deletion_candidate (product was live in Horoshop)
        # candidate         → auto-reject (was never confirmed, nothing to delete)
        matches = db.session.execute(
            select(ProductMatch).where(
                ProductMatch.supplier_product_id == product.id,
                ProductMatch.status.in_(["confirmed", "manual", "candidate"]),
            )
        ).scalars().all()
        for match in matches:
            if match.status in ("confirmed", "manual"):
                match.deletion_candidate = True
                deletion_candidates += 1
            else:
                match.status = "rejected"

    if count > 0:
        logger.info(
            "Flagged %d deletion candidates for supplier '%s'",
            deletion_candidates,
            supplier.name,
        )
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
