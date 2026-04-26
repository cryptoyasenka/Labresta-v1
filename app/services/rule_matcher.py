"""Rule matcher: auto-confirm products that match active MatchRule entries."""

import logging
from datetime import datetime, timezone

from sqlalchemy import select, true

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

    # Set of prom_product_ids already claimed by a confirmed/manual match
    # (enforces 1 pp ↔ 1 active supplier match invariant).
    claimed_pp_ids = set(
        db.session.execute(
            select(ProductMatch.prom_product_id)
            .where(ProductMatch.status.in_(["confirmed", "manual"]))
            .distinct()
        ).scalars().all()
    )

    # 3. Get eligible supplier products (not already confirmed/manual).
    # Include unavailable — match stays valid when stock returns.
    eligible_products = db.session.execute(
        select(SupplierProduct).where(
            SupplierProduct.supplier_id == supplier_id,
            SupplierProduct.id.not_in(confirmed_ids) if confirmed_ids else true(),
        )
    ).scalars().all()

    # 3.5. Preload prom products referenced by rules in ONE query — avoids an
    # N+1 SELECT inside the for sp × for rule loop. Stale rule rows are detected
    # by absence in the dict (vs. db.session.get returning None).
    rule_pp_ids = {r.prom_product_id for r in rules}
    prom_by_id: dict[int, PromProduct] = {}
    if rule_pp_ids:
        prom_by_id = {
            pp.id: pp for pp in db.session.execute(
                select(PromProduct).where(PromProduct.id.in_(rule_pp_ids))
            ).scalars().all()
        }

    # 3.6. Preload existing (sp_id, pp_id) ProductMatch rows for the pairs the
    # rules might touch — single query instead of two .first() lookups per
    # (sp, rule) iteration. Loaded via ORM so mutation flows back through the
    # session (status upgrade on line ~127).
    eligible_sp_ids = [sp.id for sp in eligible_products]
    existing_by_pair: dict[tuple[int, int], ProductMatch] = {}
    if eligible_sp_ids and rule_pp_ids:
        existing_by_pair = {
            (pm.supplier_product_id, pm.prom_product_id): pm
            for pm in db.session.execute(
                select(ProductMatch).where(
                    ProductMatch.supplier_product_id.in_(eligible_sp_ids),
                    ProductMatch.prom_product_id.in_(rule_pp_ids),
                )
            ).scalars().all()
        }

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
            prom_product = prom_by_id.get(rule.prom_product_id)
            if prom_product is None:
                logger.warning(
                    "Stale rule id=%d: prom_product_id=%d no longer exists, skipping",
                    rule.id,
                    rule.prom_product_id,
                )
                continue

            # Skip if the prom product is already claimed by a DIFFERENT sp —
            # enforces 1:1 invariant. Leave the pair as a candidate so the
            # operator sees the collision and can unconfirm the other side,
            # then continue evaluating remaining rules: another rule with the
            # same name_pattern but different brand filter may target a free pp.
            if rule.prom_product_id in claimed_pp_ids:
                pair = (sp.id, rule.prom_product_id)
                existing_for_pair = existing_by_pair.get(pair)
                if existing_for_pair is None:
                    new_candidate = ProductMatch(
                        supplier_product_id=sp.id,
                        prom_product_id=rule.prom_product_id,
                        score=100.0,
                        status="candidate",
                    )
                    db.session.add(new_candidate)
                    existing_by_pair[pair] = new_candidate
                logger.info(
                    "Rule id=%d: pp#%d already claimed, leaving sp#%d as candidate",
                    rule.id, rule.prom_product_id, sp.id,
                )
                continue

            # Check for existing match with same pair
            existing = existing_by_pair.get((sp.id, rule.prom_product_id))

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
                    claimed_pp_ids.add(rule.prom_product_id)
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
                existing_by_pair[(sp.id, rule.prom_product_id)] = new_match
                claimed_pp_ids.add(rule.prom_product_id)
                count += 1
                break  # This product is matched, move to next product

    db.session.commit()
    return count
