"""Notification service: check rules against new products and dispatch alerts."""

import logging
from datetime import datetime, timezone

from sqlalchemy import select

from app.extensions import db
from app.models.notification_rule import Notification, NotificationRule
from app.models.supplier_product import SupplierProduct
from app.services.telegram_notifier import send_telegram_message

logger = logging.getLogger(__name__)


def check_and_notify(new_products: list[SupplierProduct]) -> int:
    """Check all active rules against new products and dispatch notifications.

    Args:
        new_products: List of newly created SupplierProduct instances.

    Returns:
        Total number of notifications created.
    """
    if not new_products:
        return 0

    rules = db.session.execute(
        select(NotificationRule).where(NotificationRule.is_active == True)  # noqa: E712
    ).scalars().all()

    if not rules:
        return 0

    total_notifications = 0

    for rule in rules:
        matching = _match_products(rule, new_products)
        if not matching:
            continue

        # Create UI notifications if enabled
        if rule.ui_enabled:
            for product in matching:
                notification = Notification(
                    rule_id=rule.id,
                    supplier_product_id=product.id,
                    message=_format_notification_message(rule, product),
                )
                db.session.add(notification)
                total_notifications += 1

        # Send grouped Telegram notification if enabled
        if rule.telegram_enabled:
            _send_telegram_for_rule(rule, matching)

    db.session.commit()
    logger.info("Created %d notifications for %d rules", total_notifications, len(rules))
    return total_notifications


def get_unread_notifications(limit: int = 20) -> list[Notification]:
    """Return recent unread notifications for UI display.

    Args:
        limit: Maximum number of notifications to return.

    Returns:
        List of unread Notification records, newest first.
    """
    return db.session.execute(
        select(Notification)
        .where(Notification.is_read == False)  # noqa: E712
        .order_by(Notification.created_at.desc())
        .limit(limit)
    ).scalars().all()


def get_unread_count() -> int:
    """Return count of unread notifications."""
    from sqlalchemy import func

    return db.session.execute(
        select(func.count(Notification.id)).where(
            Notification.is_read == False  # noqa: E712
        )
    ).scalar() or 0


def mark_notifications_read(notification_ids: list[int]) -> int:
    """Mark given notifications as read.

    Args:
        notification_ids: List of notification IDs to mark read.

    Returns:
        Number of notifications updated.
    """
    if not notification_ids:
        return 0

    notifications = db.session.execute(
        select(Notification).where(
            Notification.id.in_(notification_ids),
            Notification.is_read == False,  # noqa: E712
        )
    ).scalars().all()

    count = 0
    for n in notifications:
        n.is_read = True
        count += 1

    db.session.commit()
    return count


def get_recent_notifications(limit: int = 20) -> list[Notification]:
    """Return recent notifications (both read and unread) for display.

    Args:
        limit: Maximum number of notifications to return.

    Returns:
        List of Notification records, newest first.
    """
    return db.session.execute(
        select(Notification)
        .order_by(Notification.created_at.desc())
        .limit(limit)
    ).scalars().all()


def _match_products(
    rule: NotificationRule, products: list[SupplierProduct]
) -> list[SupplierProduct]:
    """Match products against a single rule's criteria.

    Args:
        rule: The notification rule to check.
        products: List of products to check against.

    Returns:
        List of products matching the rule criteria.
    """
    criteria_type = rule.criteria_type.lower()
    criteria_value = rule.criteria_value.strip()

    if criteria_type == "keyword":
        keywords = [k.strip().lower() for k in criteria_value.split(",") if k.strip()]
        return [
            p for p in products
            if any(kw in (p.name or "").lower() for kw in keywords)
        ]

    elif criteria_type == "brand":
        brand_value = criteria_value.lower()
        return [
            p for p in products
            if p.brand and brand_value in p.brand.lower()
        ]

    elif criteria_type == "price_range":
        try:
            parts = criteria_value.split("-")
            min_cents = int(parts[0].strip())
            max_cents = int(parts[1].strip()) if len(parts) > 1 else float("inf")
        except (ValueError, IndexError):
            logger.warning(
                "Invalid price_range criteria '%s' for rule %d",
                criteria_value, rule.id,
            )
            return []
        return [
            p for p in products
            if p.price_cents is not None and min_cents <= p.price_cents <= max_cents
        ]

    elif criteria_type == "category":
        # Reserved for future: match against product category if available
        cat_value = criteria_value.lower()
        return [
            p for p in products
            if cat_value in (p.name or "").lower()
        ]

    else:
        logger.warning("Unknown criteria_type '%s' for rule %d", criteria_type, rule.id)
        return []


def _format_notification_message(
    rule: NotificationRule, product: SupplierProduct
) -> str:
    """Format a human-readable notification message."""
    price_str = ""
    if product.price_cents is not None:
        price_str = f", цена: {product.price_cents / 100:.2f} {product.currency or 'EUR'}"

    return (
        f"Новый товар по правилу \"{rule.name}\": "
        f"{product.name}{price_str}"
    )


def _send_telegram_for_rule(
    rule: NotificationRule, products: list[SupplierProduct]
) -> bool:
    """Send a single grouped Telegram message for all matching products in a rule.

    Groups products to avoid spam -- one message per rule.
    """
    if not products:
        return False

    lines = [f"<b>Правило: {rule.name}</b>"]
    lines.append(f"Тип: {rule.criteria_type} = {rule.criteria_value}")
    lines.append(f"Найдено товаров: {len(products)}\n")

    for p in products[:10]:  # Limit to 10 products per message
        price_str = ""
        if p.price_cents is not None:
            price_str = f" - {p.price_cents / 100:.2f} {p.currency or 'EUR'}"
        lines.append(f"- {p.name}{price_str}")

    if len(products) > 10:
        lines.append(f"\n... и ещё {len(products) - 10} товаров")

    text = "\n".join(lines)
    return send_telegram_message(text)
