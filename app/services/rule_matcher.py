"""Rule matcher: auto-confirm products that match active MatchRule entries."""

import logging
from datetime import datetime, timezone

from sqlalchemy import select

from app.extensions import db
from app.models.catalog import PromProduct
from app.models.match_rule import MatchRule
from app.models.product_match import ProductMatch
from app.models.supplier_product import SupplierProduct

logger = logging.getLogger(__name__)


def apply_match_rules(supplier_id: int) -> int:
    """Apply active match rules to unconfirmed supplier products.

    Products with existing confirmed/manual matches are skipped.
    Candidate matches for the same pair are upgraded to confirmed.
    Rejected matches are never overwritten.

    Args:
        supplier_id: The supplier whose products to process.

    Returns:
        Number of auto-confirmed matches.
    """
    # 1. Get all active rules
    rules = MatchRule.query.filter_by(is_active=True).all()
    if not rules:
        return 0

    # 2. Find supplier products that already have confirmed/manual matches
    confirmed_ids_query = (
        select(ProductMatch.supplier_product_id)
        .join(SupplierProduct, ProductMatch.supplier_product_id == SupplierProduct.id)
        .where(
            SupplierProduct.supplier_id == supplier_id,
            ProductMatch.status.in_(["confirmed", "manual"]),
        )
        .distinct()
    )
    confirmed_ids = set(db.session.execute(confirmed_ids_query).scalars().all())

    # 3. Get eligible supplier products (available, not already confirmed/manual)
    eligible_products = db.session.execute(
        select(SupplierProduct).where(
            SupplierProduct.supplier_id == supplier_id,
            SupplierProduct.available == True,  # noqa: E712
            SupplierProduct.id.not_in(confirmed_ids) if confirmed_ids else True,
        )
    ).scalars().all()

    count = 0

    for sp in eligible_products:
        for rule in rules:
            # Check name match (exact)
            if sp.name != rule.supplier_product_name_pattern:
                continue

            # Check brand match if rule specifies brand
            if rule.supplier_brand is not None and rule.supplier_brand != "":
                if sp.brand != rule.supplier_brand:
                    continue

            # Verify prom product still exists (stale rule check)
            prom_product = db.session.get(PromProduct, rule.prom_product_id)
            if prom_product is None:
                logger.warning(
                    "Stale rule id=%d: prom_product_id=%d no longer exists, skipping",
                    rule.id,
                    rule.prom_product_id,
                )
                continue

            # Check for existing match with same pair
            existing = ProductMatch.query.filter_by(
                supplier_product_id=sp.id,
                prom_product_id=rule.prom_product_id,
            ).first()

            if existing is not None:
                if existing.status == "rejected":
                    # Don't override operator's rejection
                    continue
                if existing.status in ("confirmed", "manual"):
                    # Already handled (defensive)
                    continue
                if existing.status == "candidate":
                    # Upgrade candidate to confirmed
                    existing.status = "confirmed"
                    existing.score = 100.0
                    existing.confirmed_by = f"rule:{rule.id}"
                    existing.confirmed_at = datetime.now(timezone.utc)
                    count += 1
                    break  # This product is matched, move to next product
            else:
                # Create new confirmed match
                new_match = ProductMatch(
                    supplier_product_id=sp.id,
                    prom_product_id=rule.prom_product_id,
                    score=100.0,
                    status="confirmed",
                    confirmed_by=f"rule:{rule.id}",
                    confirmed_at=datetime.now(timezone.utc),
                )
                db.session.add(new_match)
                count += 1
                break  # This product is matched, move to next product

    db.session.commit()
    return count
