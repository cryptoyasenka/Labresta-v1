"""Flask CLI commands for manual sync pipeline execution and admin management."""

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


@click.command("flag-orphans")
@click.option("--dry-run", is_flag=True, help="Show what would change without writing to DB")
@click.option(
    "--exclude-dead-suppliers",
    is_flag=True,
    help="Exclude suppliers with 0 fresh SPs (e.g. permanent 403 feeds) from both "
    "the drop-check and brand-anchor count. Use when a supplier is known-broken.",
)
@with_appcontext
def flag_orphans_command(dry_run, exclude_dead_suppliers):
    """Run Stage 4.5 orphan-PP detection manually.

    Flags PromProducts whose brand is carried by a single enabled supplier
    when that supplier's feed does not contain the SKU. Reversible: if the
    PP returns to feed, the auto-flag is cleared.

    Examples:
        flask flag-orphans --dry-run
        flask flag-orphans
        flask flag-orphans --dry-run --exclude-dead-suppliers
    """
    from app.services.orphan_detector import flag_orphan_pps

    result = flag_orphan_pps(
        dry_run=dry_run,
        exclude_dead_suppliers=exclude_dead_suppliers,
    )
    mode = "DRY-RUN" if dry_run else "APPLY"
    click.echo(f"[{mode}] Stage 4.5 orphan detection:")
    click.echo(f"  flagged: {result['flagged']}")
    click.echo(f"  cleared: {result['cleared']}")
    click.echo(f"  L1_total: {result['L1_total']}")
    click.echo(f"  brand_single_supplier_count: {result['brand_single_supplier_count']}")
    if result.get("dead_supplier_ids"):
        click.echo(f"  dead_supplier_ids excluded: {result['dead_supplier_ids']}")
    if result["skipped_reason"]:
        click.echo(f"  skipped: {result['skipped_reason']}")


@click.command("create-admin")
@click.option("--email", prompt="Admin email")
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
@click.option("--name", prompt="Admin name")
@with_appcontext
def create_admin_command(email, password, name):
    """Create an admin user for the management UI.

    Examples:
        uv run flask create-admin --email admin@example.com --password secret --name Admin
    """
    from app.extensions import db
    from app.models.user import User

    existing = db.session.execute(
        db.select(User).where(User.email == email.strip().lower())
    ).scalar_one_or_none()

    if existing:
        click.echo(f"Error: user with email '{email}' already exists.")
        raise SystemExit(1)

    user = User(
        email=email.strip().lower(),
        name=name.strip(),
        role="admin",
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    click.echo(f"Admin user '{user.name}' ({user.email}) created successfully.")
