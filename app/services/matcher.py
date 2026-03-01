"""Fuzzy matching engine with brand blocking for supplier-to-catalog matching.

Uses rapidfuzz WRatio scorer with brand-based blocking to reduce search space.
Match candidates are ranked and stored for human review — no auto-approve.
"""

import logging
import re
import unicodedata

from rapidfuzz import fuzz, process, utils
from sqlalchemy import select

from app.extensions import db
from app.models.catalog import PromProduct
from app.models.product_match import ProductMatch
from app.models.supplier_product import SupplierProduct

logger = logging.getLogger(__name__)

# --- Confidence thresholds (per user decisions from CONTEXT.md) ---
# Benchmark (2026-02-27, 3 MARESTO products vs 6101 prom.ua catalog):
#   100% products found candidates, avg top-1 score 85.5%, all high-confidence.
#   60% cutoff validated as reasonable for Cyrillic product names with WRatio.
SCORE_CUTOFF = 60.0  # User decision: 60% minimum threshold
MATCH_LIMIT = 3  # User decision: top-3 candidates per product
CONFIDENCE_HIGH = 80.0  # >80% = High confidence
CONFIDENCE_MEDIUM = 60.0  # 60-80% = Medium confidence
# Below 60% = Low (filtered out by SCORE_CUTOFF, never stored)

BRAND_MATCH_THRESHOLD = 80  # Fuzzy brand match threshold for blocking
MAX_PRICE_RATIO = 3.0  # Reject candidates where price differs by more than 3x

# --- Model / article matching ---
MODEL_MATCH_THRESHOLD = 90  # Article/model >=90% similar for fast-path (score=100)
MODEL_BOOST_POINTS = 10.0  # Bonus points when model/article matches (>=80%)
MODEL_MISMATCH_PENALTY = 15.0  # Penalty when both have model but they differ
MODEL_BOOST_THRESHOLD = 80  # Minimum similarity for model boost

# --- Product type gate ---
TYPE_MATCH_THRESHOLD = 50  # Minimum type similarity to keep candidate
MIN_TYPE_LENGTH = 2  # Minimum chars for extracted type to be usable


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


def normalize_model(value: str | None) -> str:
    """Normalize a model/article string for comparison."""
    if not value or not value.strip():
        return ""
    return value.strip().lower()


def extract_product_type(name: str, brand: str | None) -> str:
    """Extract product type from name — words before the brand.

    Example: "Макароноварка ел. Angelo Po 0S1CP1E" with brand "Angelo Po"
             → "Макароноварка ел."
    """
    if not name:
        return ""
    if not brand or not brand.strip():
        return ""

    name_lower = name.lower()
    brand_lower = brand.strip().lower()

    idx = name_lower.find(brand_lower)
    if idx <= 0:
        return ""

    type_part = name[:idx].strip()
    # Remove trailing punctuation/noise
    type_part = re.sub(r"[\s.,:;()\-]+$", "", type_part).strip()

    if len(type_part) < MIN_TYPE_LENGTH:
        return ""

    return type_part


def find_match_candidates(
    supplier_product_name: str,
    supplier_brand: str | None,
    prom_products: list[dict],
    score_cutoff: float = SCORE_CUTOFF,
    limit: int = MATCH_LIMIT,
    supplier_price_cents: int | None = None,
    supplier_model: str | None = None,
    supplier_article: str | None = None,
) -> list[dict]:
    """Find top match candidates for a supplier product against prom catalog.

    Uses brand-based blocking to reduce search space, then WRatio scorer
    for fuzzy name matching, with product type gate and model matching.

    Args:
        supplier_product_name: Name of the supplier product to match.
        supplier_brand: Brand/vendor of the supplier product (optional).
        prom_products: List of dicts with keys: id, name, brand, price,
            model (optional), article (optional).
        score_cutoff: Minimum score threshold (default 60%).
        limit: Maximum candidates to return (default 3).
        supplier_price_cents: Supplier product price in cents (optional).
        supplier_model: Supplier product model field (optional).
        supplier_article: Supplier product article/vendorCode (optional).

    Returns:
        List of candidate dicts sorted by score descending:
        [{"prom_product_id": int, "score": float, "prom_name": str,
          "confidence": str}, ...]
    """
    if not prom_products or not supplier_product_name:
        return []

    # Step 1: Brand-based blocking
    candidates_pool = prom_products
    brand_was_matched = False
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
            brand_was_matched = True
        # If brand not found in catalog, fall back to all prom_products

    # Step 2: Build choices dict — {prom_id: normalized_name}
    choices = {p["id"]: normalize_text(p["name"]) for p in candidates_pool}

    if not choices:
        return []

    # Step 2.5: Article/Model exact-match fast path
    fast_match_ids = set()
    fast_matches = []
    sup_model = normalize_model(supplier_model)
    sup_article = normalize_model(supplier_article)

    if sup_model or sup_article:
        for p in candidates_pool:
            prom_article = normalize_model(p.get("article"))
            prom_model = normalize_model(p.get("model"))

            matched = False
            if sup_article and prom_article:
                if fuzz.ratio(sup_article, prom_article) >= MODEL_MATCH_THRESHOLD:
                    matched = True
            if not matched and sup_model and prom_model:
                if fuzz.ratio(sup_model, prom_model) >= MODEL_MATCH_THRESHOLD:
                    matched = True

            if matched and p["id"] not in fast_match_ids:
                fast_match_ids.add(p["id"])
                fast_matches.append(
                    {
                        "prom_product_id": p["id"],
                        "score": 100.0,
                        "prom_name": p["name"],
                        "confidence": "high",
                    }
                )
                if len(fast_matches) >= limit:
                    break

    # Step 3: Extract matches using rapidfuzz WRatio
    fuzzy_limit = limit - len(fast_matches)
    fuzzy_output = []
    if fuzzy_limit > 0:
        results = process.extract(
            normalize_text(supplier_product_name),
            choices,
            scorer=fuzz.WRatio,
            processor=utils.default_process,
            score_cutoff=score_cutoff,
            limit=fuzzy_limit + len(fast_match_ids),  # extra to compensate for skips
        )

        # Step 4: Build result list (skip fast-path matches)
        for matched_name, score, prom_id in results:
            if prom_id in fast_match_ids:
                continue
            fuzzy_output.append(
                {
                    "prom_product_id": prom_id,
                    "score": round(score, 2),
                    "prom_name": matched_name,
                    "confidence": get_confidence_label(score),
                }
            )
            if len(fuzzy_output) >= fuzzy_limit:
                break

    # Step 4.5: Type gate — reject candidates where product types differ
    if brand_was_matched and supplier_brand:
        supplier_type = extract_product_type(supplier_product_name, supplier_brand)
        if supplier_type:
            type_filtered = []
            for candidate in fuzzy_output:
                # Find prom product brand for type extraction
                prom_brand = None
                prom_name_full = candidate["prom_name"]
                for p in candidates_pool:
                    if p["id"] == candidate["prom_product_id"]:
                        prom_brand = p.get("brand") or supplier_brand
                        prom_name_full = p["name"]
                        break

                prom_type = extract_product_type(prom_name_full, prom_brand)
                if prom_type:
                    type_score = fuzz.token_sort_ratio(
                        supplier_type.lower(), prom_type.lower()
                    )
                    if type_score < TYPE_MATCH_THRESHOLD:
                        logger.debug(
                            "Type gate rejected: '%s' vs '%s' (score=%d) for prom_id=%d",
                            supplier_type,
                            prom_type,
                            type_score,
                            candidate["prom_product_id"],
                        )
                        continue
                # If type couldn't be extracted, let it pass
                type_filtered.append(candidate)
            fuzzy_output = type_filtered

    # Step 4.6: Model boost/penalty — adjust score based on model similarity
    if sup_model or sup_article:
        for candidate in fuzzy_output:
            prom_model = ""
            prom_article = ""
            for p in candidates_pool:
                if p["id"] == candidate["prom_product_id"]:
                    prom_model = normalize_model(p.get("model"))
                    prom_article = normalize_model(p.get("article"))
                    break

            # Check article first, then model
            best_ratio = 0.0
            has_both = False
            if sup_article and prom_article:
                has_both = True
                best_ratio = fuzz.ratio(sup_article, prom_article)
            elif sup_model and prom_model:
                has_both = True
                best_ratio = fuzz.ratio(sup_model, prom_model)

            if has_both:
                if best_ratio >= MODEL_BOOST_THRESHOLD:
                    candidate["score"] = min(
                        100.0, round(candidate["score"] + MODEL_BOOST_POINTS, 2)
                    )
                else:
                    candidate["score"] = max(
                        0.0, round(candidate["score"] - MODEL_MISMATCH_PENALTY, 2)
                    )
                candidate["confidence"] = get_confidence_label(candidate["score"])

    # Merge fast-path + fuzzy, sort by score
    output = fast_matches + fuzzy_output
    output.sort(key=lambda x: x["score"], reverse=True)
    output = output[:limit]

    # Filter out candidates that dropped below cutoff after penalty
    output = [c for c in output if c["score"] >= score_cutoff]

    # Step 5: Price plausibility gate — reject implausible price ratios
    if supplier_price_cents and supplier_price_cents > 0:
        plausible = []
        for candidate in output:
            prom_price = None
            for p in candidates_pool:
                if p["id"] == candidate["prom_product_id"]:
                    prom_price = p.get("price")
                    break
            if prom_price and prom_price > 0:
                ratio = max(supplier_price_cents / prom_price, prom_price / supplier_price_cents)
                if ratio > MAX_PRICE_RATIO:
                    logger.debug(
                        "Price plausibility rejected: supplier=%d vs prom=%d (ratio=%.1fx) for prom_id=%d",
                        supplier_price_cents, prom_price, ratio, candidate["prom_product_id"],
                    )
                    continue
            plausible.append(candidate)
        output = plausible

    return output


def find_match_for_product(
    supplier_product,
    exclude_prom_ids: list[int] | None = None,
) -> ProductMatch | None:
    """Find the best match candidate for a single supplier product.

    Used by the match review UI when a match is rejected and the system
    needs to find an alternative candidate.

    Args:
        supplier_product: SupplierProduct instance to match.
        exclude_prom_ids: List of prom product IDs to exclude (e.g., rejected ones).

    Returns:
        A new ProductMatch instance (not yet added to session) or None.
    """
    prom_all = db.session.execute(select(PromProduct)).scalars().all()

    exclude_set = set(exclude_prom_ids or [])
    prom_list = [
        {"id": p.id, "name": p.name, "brand": p.brand, "price": p.price,
         "model": p.model, "article": p.article}
        for p in prom_all
        if p.id not in exclude_set
    ]

    if not prom_list:
        return None

    candidates = find_match_candidates(
        supplier_product.name,
        supplier_product.brand,
        prom_list,
        supplier_price_cents=supplier_product.price_cents,
        supplier_model=supplier_product.model,
        supplier_article=supplier_product.article,
        limit=1,
    )

    if not candidates:
        return None

    best = candidates[0]

    # Check if this pair already exists
    existing = db.session.execute(
        select(ProductMatch).where(
            ProductMatch.supplier_product_id == supplier_product.id,
            ProductMatch.prom_product_id == best["prom_product_id"],
        )
    ).scalar_one_or_none()

    if existing:
        return None

    return ProductMatch(
        supplier_product_id=supplier_product.id,
        prom_product_id=best["prom_product_id"],
        score=best["score"],
        status="candidate",
    )


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
        {"id": p.id, "name": p.name, "brand": p.brand, "price": p.price,
         "model": p.model, "article": p.article}
        for p in prom_all
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
        candidates = find_match_candidates(
            sp.name, sp.brand, prom_list,
            supplier_price_cents=sp.price_cents,
            supplier_model=sp.model,
            supplier_article=sp.article,
        )
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
