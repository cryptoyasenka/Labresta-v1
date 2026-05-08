"""Regenerate the main YML feed once on container startup.

Railway containers have ephemeral filesystem — every deploy recreates
instance/feeds/ empty, so /feed/yml returns 404 until the next scheduled
sync writes the file. This script restores the feed immediately after
deploy by querying current confirmed matches and writing the YML.

Failure is non-fatal: if the DB isn't ready or any other error occurs,
log it and exit 0 so gunicorn still starts.
"""
import logging
import sys
import traceback

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("yml_startup")

try:
    from app import create_app
    from app.services.yml_generator import regenerate_yml_feed

    app = create_app()
    with app.app_context():
        result = regenerate_yml_feed()
        log.info(
            "YML restored on startup: %d offers (%d available, %d unavailable) -> %s",
            result.get("total", 0),
            result.get("available", 0),
            result.get("unavailable", 0),
            result.get("file_path", "?"),
        )
except Exception as e:
    log.warning("YML startup regeneration skipped: %s", e)
    traceback.print_exc(file=sys.stderr)

sys.exit(0)
