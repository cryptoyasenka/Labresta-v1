"""APScheduler configuration for automated feed sync.

CRITICAL: Debug mode pitfall (Research Pitfall 1)
Flask debug mode spawns a reloader that creates TWO processes.
APScheduler must only start in the child process (WERKZEUG_RUN_MAIN == "true")
or in production (not debug mode). Otherwise every job executes twice.
"""

import os
import logging

from flask_apscheduler import APScheduler

logger = logging.getLogger(__name__)

scheduler = APScheduler()


@scheduler.task("interval", id="sync_feeds", hours=4, misfire_grace_time=900)
def scheduled_sync():
    """Fetch all enabled supplier feeds, detect disappeared products, and run matching."""
    logger.info("Scheduled sync triggered")
    from app.services.sync_pipeline import run_full_sync

    run_full_sync()
    logger.info("Scheduled sync completed")


def init_scheduler(app):
    """Initialize and start the scheduler with Flask app.

    Uses MemoryJobStore (default) — sufficient for MVP single-process deployment.
    The interval job is re-registered on every app startup, so persistence is not needed.
    """
    app.config["SCHEDULER_API_ENABLED"] = False  # No REST API for scheduler

    scheduler.init_app(app)

    # Prevent double execution in Flask debug mode
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true" or not app.debug:
        scheduler.start()
        logger.info("Scheduler started — sync job registered every 4 hours")
    else:
        logger.debug("Scheduler NOT started (reloader parent process)")
