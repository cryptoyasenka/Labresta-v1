"""Flask CLI commands for manual sync pipeline execution."""

import click
from flask.cli import with_appcontext


@click.command("sync")
@click.option("--supplier-id", type=int, default=None, help="Sync specific supplier by ID")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging output")
@with_appcontext
def sync_command(supplier_id, verbose):
    """Run the sync pipeline manually.

    Fetches supplier feeds, detects disappeared products, and runs fuzzy matching.
    Without --supplier-id, syncs all enabled suppliers.

    Examples:
        uv run flask sync
        uv run flask sync --supplier-id 1
        uv run flask sync -v
    """
    import logging

    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    from app.services.sync_pipeline import run_full_sync

    run_full_sync(supplier_id)
    click.echo("Sync complete.")
