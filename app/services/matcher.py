"""Fuzzy matching engine with brand blocking for supplier-to-catalog matching.

Uses rapidfuzz WRatio scorer with brand-based blocking to reduce search space.
Match candidates are ranked and stored for human review — no auto-approve.
"""

import logging
import unicodedata

from rapidfuzz import fuzz, process, utils
from sqlalchemy import select

from app.extensions import db
from app.models.catalog import PromProduct
from app.models.product_match import ProductMatch
from app.models.supplier_product import SupplierProduct

logger = logging.getLogger(__name__)

# --- Confidence thresholds (per user decisions from CONTEXT.md) ---
SCORE_CUTOFF = 60.0  # User decision: 60% minimum threshold
MATCH_LIMIT = 3  # User decision: top-3 candidates per product
CONFIDENCE_HIGH = 80.0  # >80% = High confidence
CONFIDENCE_MEDIUM = 60.0  # 60-80% = Medium confidence
# Below 60% = Low (filtered out by SCORE_CUTOFF, never stored)

BRAND_MATCH_THRESHOLD = 80  # Fuzzy brand match threshold for blocking


def normalize_text(text: str) -> str:
    """Apply NFC unicode normalization to handle Cyrillic edge cases.

    Applied before rapidfuzz's default_process to ensure consistent
    comparison of Ukrainian/Cyrillic product names (Research Pitfall 5).
    """
    if not text:
        return ""
    return unicodedata.normalize("NFC", text)


def get_confidence_label(score: float) -> str:
    """Map a fuzzy match score to a confidence tier label.

    Used by Phase 4 UI for display.
    """
    if score >= CONFIDENCE_HIGH:
        return "high"
    elif score >= CONFIDENCE_MEDIUM:
        return "medium"
    else:
        return "low"


def find_match_candidates(
    supplier_product_name: str,
    supplier_brand: str | None,
    prom_products: list[dict],
    score_cutoff: float = SCORE_CUTOFF,
    limit: int = MATCH_LIMIT,
) -> list[dict]:
    """Find top match candidates for a supplier product against prom catalog.

    Uses brand-based blocking to reduce search space (from ~5950 to ~50-200
    per brand), then WRatio scorer for fuzzy name matching.

    Args:
        supplier_product_name: Name of the supplier product to match.
        supplier_brand: Brand/vendor of the supplier product (optional).
        prom_products: List of dicts with keys: id, name, brand.
        score_cutoff: Minimum score threshold (default 60%).
        limit: Maximum candidates to return (default 3).

    Returns:
        List of candidate dicts sorted by score descending:
        [{"prom_product_id": int, "score": float, "prom_name": str,
          "confidence": str}, ...]
    """
    if not prom_products or not supplier_product_name:
        return []

    # Step 1: Brand-based blocking
    candidates_pool = prom_products
    if supplier_brand and supplier_brand.strip():
        brand_lower = supplier_brand.strip().lower()
        brand_filtered = [
            p
            for p in prom_products
            if p.get("brand")
            and fuzz.ratio(p["brand"].lower(), brand_lower) > BRAND_MATCH_THRESHOLD
        ]
        if brand_filtered:
            candidates_pool = brand_filtered
        # If brand not found in catalog, fall back to all prom_products

    # Step 2: Build choices dict — {prom_id: normalized_name}
    choices = {p["id"]: normalize_text(p["name"]) for p in candidates_pool}

    if not choices:
        return []

    # Step 3: Extract matches using rapidfuzz WRatio
    results = process.extract(
        normalize_text(supplier_product_name),
        choices,
        scorer=fuzz.WRatio,
        processor=utils.default_process,
        score_cutoff=score_cutoff,
        limit=limit,
    )

    # Step 4: Build result list
    # results format: [(matched_text, score, key), ...]
    output = []
    for matched_name, score, prom_id in results:
        output.append(
            {
                "prom_product_id": prom_id,
                "score": round(score, 2),
                "prom_name": matched_name,
                "confidence": get_confidence_label(score),
            }
        )

    return output


def run_matching_for_supplier(supplier_id: int) -> int:
    """Run fuzzy matching for all unmatched products of a supplier.

    Skips products that already have confirmed or manual matches.
    Creates ProductMatch rows with status='candidate' for human review.

    Args:
        supplier_id: ID of the supplier to process.

    Returns:
        Count of new match candidates generated.
    """
    # Step 1: Get supplier product IDs with confirmed/manual matches (skip these)
    matched_ids_query = (
        select(ProductMatch.supplier_product_id)
        .where(ProductMatch.status.in_(["confirmed", "manual"]))
        .distinct()
    )
    matched_ids = set(
        db.session.execute(matched_ids_query).scalars().all()
    )

    # Step 2: Get unmatched, available supplier products
    sp_query = select(SupplierProduct).where(
        SupplierProduct.supplier_id == supplier_id,
        SupplierProduct.available == True,  # noqa: E712
        SupplierProduct.id.notin_(matched_ids) if matched_ids else True,
    )
    unmatched_products = db.session.execute(sp_query).scalars().all()

    # Step 3: Load all prom products
    prom_all = db.session.execute(select(PromProduct)).scalars().all()
    prom_list = [
        {"id": p.id, "name": p.name, "brand": p.brand} for p in prom_all
    ]

    if not unmatched_products or not prom_list:
        logger.info(
            "No unmatched products or no prom catalog for supplier %d",
            supplier_id,
        )
        return 0

    # Step 4: Match each unmatched product
    total_candidates = 0
    for sp in unmatched_products:
        candidates = find_match_candidates(sp.name, sp.brand, prom_list)
        for c in candidates:
            # Check if pair already exists (avoid duplicates)
            existing = db.session.execute(
                select(ProductMatch).where(
                    ProductMatch.supplier_product_id == sp.id,
                    ProductMatch.prom_product_id == c["prom_product_id"],
                )
            ).scalar_one_or_none()

            if existing is None:
                match = ProductMatch(
                    supplier_product_id=sp.id,
                    prom_product_id=c["prom_product_id"],
                    score=c["score"],
                    status="candidate",
                )
                db.session.add(match)
                total_candidates += 1

    db.session.commit()
    logger.info(
        "%d new match candidates generated for supplier %d",
        total_candidates,
        supplier_id,
    )
    return total_candidates
