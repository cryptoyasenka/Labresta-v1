import logging
import os

import requests

logger = logging.getLogger(__name__)


def send_telegram_message(text: str) -> bool:
    """Send a message via Telegram Bot API.

    Returns True on success, False if not configured or on failure.
    Gracefully degrades — never crashes the sync pipeline over a notification.
    """
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        logger.debug("Telegram not configured, skipping notification")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
    }

    try:
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        return True
    except requests.RequestException as exc:
        logger.warning("Telegram notification failed: %s", exc)
        return False


def notify_sync_failure(
    supplier_name: str, error: str, attempt_count: int = 0
) -> bool:
    """Notify about a permanent sync failure (after all retries exhausted)."""
    text = (
        "\u26a0\ufe0f <b>Sync Failed</b>\n"
        f"Supplier: {supplier_name}\n"
        f"Error: {error[:200]}\n"
        f"Retries exhausted: {attempt_count}"
    )
    return send_telegram_message(text)


def notify_disappeared_products(supplier_name: str, count: int) -> bool:
    """Notify when products disappear from a supplier feed."""
    if count <= 0:
        return False

    text = (
        f"\u26a0\ufe0f {count} products disappeared from "
        f"{supplier_name} feed. Marked as unavailable."
    )
    return send_telegram_message(text)
