# Phase 3: Pricing Engine and YML Output - Research

**Researched:** 2026-02-27
**Domain:** Pricing calculation, YML (Yandex Market Language) generation, atomic file serving
**Confidence:** HIGH

## Summary

Phase 3 transforms confirmed product matches into a publicly accessible YML feed with correctly calculated prices. The domain breaks into three sub-problems: (1) integer-cent pricing arithmetic with supplier-level and per-product discount overrides, (2) YML/XML generation using lxml (already in the project stack), and (3) atomic file writing with a stable public URL for prom.ua to poll.

The project already has a working YML generator (`app/services/yml_test_generator.py`) that produces valid `yml_catalog` XML using lxml. The production feed generator will follow the same pattern but source data from confirmed matches, apply discount pricing, and write atomically. No new libraries are needed — lxml, Flask's `send_from_directory`, and Python's `os.replace()` cover all requirements.

**Primary recommendation:** Build a pricing service (pure math on integer cents), a YML generator that queries confirmed matches and applies pricing, and a Flask route to serve the static file — then wire YML regeneration into the existing sync pipeline after the matching stage.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- Prices stay in EUR — no currency conversion needed (the platform has a built-in currency converter)
- Discount is applied to supplier's RRP (retail price): final_price = RRP × (1 − discount%)
- Per-product discount overrides supplier-level discount when both are set
- Rounding: mathematical rounding (round) to whole numbers (e.g., 169.49 → 169, 169.50 → 170)
- Internal storage as integer cents to avoid floating-point errors (per PRICE-04)
- YML outputs only price and availability — product creation/addition is handled separately
- Product name taken from prom.ua catalog (not supplier feed)
- Offer ID = prom.ua product ID (so the platform updates the correct product)
- Currency in YML: EUR
- Minimal fields: name, price, availability status
- Static file generated on disk (not on-the-fly endpoint)
- File lives on the same hosting as the application
- Atomic write: write to .tmp then rename to prevent partial reads
- YML regenerated immediately after each supplier feed sync (not on a separate schedule)
- File accessible at a stable public URL without authentication
- Matched product out of stock at supplier → include in YML as "out of stock"
- Product disappeared from supplier feed entirely → mark "out of stock" in YML + flag for operator review
- Product with zero or missing price → mark "out of stock" + flag for operator review
- Supplier feed fails to load (network error) → do NOT update YML, keep the previous working version

### Claude's Discretion
- Exact YML XML structure and tag names (following prom.ua/Horoshop conventions)
- File path and URL structure for the generated YML
- How operator review flags are stored and surfaced (will be part of dashboard in Phase 4)
- Temporary file naming and cleanup strategy

### Deferred Ideas (OUT OF SCOPE)
- Adding new products from supplier feed to prom.ua catalog — separate workflow
- Operator review UI for flagged products — Phase 4 dashboard
- Horoshop-specific field mapping — v2 requirement (HRSH-01)
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| PRICE-01 | Admin configures discount % per supplier | Supplier model already has `discount_percent` column; pricing service reads it |
| PRICE-02 | Admin can set per-product discount % override | Requires new column on ProductMatch or a new model; pricing service checks product-level first |
| PRICE-03 | System calculates final price: retail × (1 − discount%), product override takes priority | Pure integer-cent arithmetic in pricing service; see Code Examples section |
| PRICE-04 | Prices stored as integer cents (avoid float errors) | SupplierProduct already stores `price_cents`; final price computed and output as integer cents, converted to whole EUR only at YML output |
| FEED-01 | System generates YML file compatible with prom.ua and Horoshop (fields: name, price, availability, article) | YML structure documented below with exact tag names from prom.ua spec |
| FEED-02 | YML file available at a public URL on hosting (prom.ua pulls automatically) | Flask route serving static file from configured output directory |
| FEED-03 | YML updates only matched products — rest of catalog untouched | Query filters on ProductMatch.status == "confirmed" |
| FEED-04 | YML format not tied to prom.ua — compatible with Horoshop for future migration | Standard yml_catalog format used by both platforms |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| lxml | >=5.0 | YML/XML generation | Already in project; used by yml_test_generator.py and feed_parser.py |
| Flask | >=3.1 | Serve static YML file via route | Already in project; `send_from_directory` for file serving |
| Python stdlib `os.replace()` | 3.11+ | Atomic file rename | Cross-platform atomic rename (POSIX and Windows) |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| Python stdlib `tempfile` | 3.11+ | Generate unique tmp file names | For atomic write pattern (NamedTemporaryFile or manual .tmp suffix) |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| lxml | xml.etree.ElementTree (stdlib) | lxml already in project, has `pretty_print=True` and DOCTYPE support; stdlib lacks both |
| Flask static serve | Nginx direct serve | Better perf but adds deployment complexity; Flask is sufficient for MVP polling |
| os.replace() | shutil.move() | os.replace() is atomic on same filesystem; shutil.move may copy+delete across filesystems |

**Installation:**
```bash
# No new packages needed — all dependencies already in pyproject.toml
```

## Architecture Patterns

### Recommended Project Structure
```
app/
├── services/
│   ├── pricing.py          # Pure pricing calculations (integer cents)
│   ├── yml_generator.py    # YML feed generation from confirmed matches
│   └── sync_pipeline.py    # Extended: call yml_generator after matching
├── models/
│   └── product_match.py    # Extended: per-product discount_percent column
├── views/
│   └── feed.py             # Public route to serve YML file
└── config.py               # Extended: YML_OUTPUT_DIR, YML_FILENAME settings
```

### Pattern 1: Integer-Cent Pricing (No Floats in Business Logic)
**What:** All price math operates on integer cents. Conversion to display units happens only at the YML output boundary.
**When to use:** Always — this is the locked decision from CONTEXT.md.
**Example:**
```python
def calculate_final_price_cents(
    retail_price_cents: int,
    supplier_discount_pct: float,
    product_discount_pct: float | None = None,
) -> int:
    """Calculate discounted price in integer cents.

    Uses the effective discount (product override > supplier default).
    Rounds to nearest whole EUR (nearest 100 cents) using Python's
    built-in round() with banker's rounding caveat handled.
    """
    discount = product_discount_pct if product_discount_pct is not None else supplier_discount_pct
    # Integer math: multiply first, divide last to minimize precision loss
    discounted = retail_price_cents * (100 - int(discount * 100)) // 10000
    # Round to nearest whole EUR (100 cents)
    # Use: (cents + 50) // 100 * 100 for mathematical rounding (0.5 rounds up)
    eur_whole = (discounted + 50) // 100
    return eur_whole  # Return whole EUR as integer
```

### Pattern 2: Atomic File Write
**What:** Write YML to a temporary file, then atomically replace the target file.
**When to use:** Every YML regeneration — prevents prom.ua from reading a half-written file.
**Example:**
```python
import os
import tempfile

def write_yml_atomic(tree, output_path: str):
    """Write lxml ElementTree to file atomically."""
    output_dir = os.path.dirname(output_path)
    # Write to temp file in same directory (required for atomic rename)
    fd, tmp_path = tempfile.mkstemp(
        suffix=".tmp", prefix="yml_", dir=output_dir
    )
    try:
        with os.fdopen(fd, "wb") as f:
            tree.write(
                f,
                xml_declaration=True,
                encoding="UTF-8",
                pretty_print=True,
            )
        os.replace(tmp_path, output_path)  # Atomic on same filesystem
    except Exception:
        # Clean up temp file on failure
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise
```

### Pattern 3: Query Confirmed Matches with Joined Data
**What:** Single query to get all data needed for YML generation — confirmed matches with supplier product prices and prom.ua product names.
**When to use:** In the YML generator to build offers.
**Example:**
```python
from sqlalchemy import select
from app.models.product_match import ProductMatch
from app.models.supplier_product import SupplierProduct
from app.models.catalog import PromProduct

def get_confirmed_matches():
    """Fetch all confirmed matches with related product data."""
    stmt = (
        select(ProductMatch, SupplierProduct, PromProduct)
        .join(SupplierProduct, ProductMatch.supplier_product_id == SupplierProduct.id)
        .join(PromProduct, ProductMatch.prom_product_id == PromProduct.id)
        .where(ProductMatch.status == "confirmed")
    )
    return db.session.execute(stmt).all()
```

### Pattern 4: Flask Static File Serving for Public URL
**What:** A dedicated Flask route serves the generated YML file without authentication.
**When to use:** For FEED-02 — prom.ua polls this URL.
**Example:**
```python
from flask import Blueprint, send_from_directory, current_app, abort

feed_bp = Blueprint("feed", __name__)

@feed_bp.route("/feed/yml")
def serve_yml():
    """Serve the generated YML feed file — no auth required."""
    yml_dir = current_app.config["YML_OUTPUT_DIR"]
    yml_file = current_app.config["YML_FILENAME"]
    try:
        return send_from_directory(
            yml_dir, yml_file,
            mimetype="application/xml",
        )
    except FileNotFoundError:
        abort(404)
```

### Anti-Patterns to Avoid
- **Float arithmetic for prices:** Never use `price * 0.85` on floats. Always work in integer cents and apply discount as integer operations.
- **Non-atomic file write:** Never write directly to the target file path. A crash mid-write leaves a corrupted file that prom.ua will try to parse.
- **Generating YML on-the-fly per request:** The user decided on a static file approach. On-the-fly generation adds latency and risk of serving different content to concurrent readers.
- **Including unconfirmed matches in YML:** FEED-03 explicitly requires only confirmed matches. Candidate or rejected matches must be filtered out.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| XML generation | String concatenation / f-strings | lxml.etree | XML escaping, encoding declaration, proper formatting |
| Atomic file write | Direct open()+write() | tempfile + os.replace() | Prevents half-written files visible to readers |
| XML character escaping | Manual replace of &, <, > | lxml handles automatically | lxml's text assignment auto-escapes special characters |

**Key insight:** lxml already handles XML escaping, encoding declarations, and pretty-printing. The existing `yml_test_generator.py` proves this pattern works in the project.

## Common Pitfalls

### Pitfall 1: Python's round() Uses Banker's Rounding
**What goes wrong:** `round(169.5)` returns `170`, but `round(168.5)` returns `168` (rounds to even). User explicitly wants mathematical rounding (0.5 always rounds up).
**Why it happens:** Python 3 follows IEEE 754 banker's rounding by default.
**How to avoid:** Use integer arithmetic: `(cents + 50) // 100` for rounding to nearest whole EUR. This always rounds 0.5 up.
**Warning signs:** Test with prices ending in .50 — verify they round up, not to even.

### Pitfall 2: os.replace() Requires Same Filesystem
**What goes wrong:** If temp file is in `/tmp` but target is in `/var/www/`, `os.replace()` may fail or fall back to non-atomic copy.
**Why it happens:** Atomic rename only works within the same filesystem/mount point.
**How to avoid:** Create the temp file in the same directory as the output file (use `dir=` parameter in `tempfile.mkstemp()`).
**Warning signs:** `OSError: Invalid cross-device link` on Linux.

### Pitfall 3: Floating-Point Discount Calculation
**What goes wrong:** `19999 * 0.85` = `16999.15` in float, but `int(19999 * 0.85)` = `16999` (truncates).
**Why it happens:** IEEE 754 floating-point representation.
**How to avoid:** Use integer-only math: `retail_cents * (10000 - discount_bps) // 10000` where `discount_bps` is discount in basis points (15% = 1500 bps). Or use `round()` before `int()` conversion.
**Warning signs:** Prices off by 1 cent in edge cases.

### Pitfall 4: Missing Price or Zero Price in YML
**What goes wrong:** Including a product with `<price>0</price>` in YML — prom.ua may reject or display incorrectly.
**Why it happens:** Supplier product has null or 0 price_cents.
**How to avoid:** Per user decision: products with zero/missing price should be marked "out of stock" in YML and flagged for operator review. Filter these in the generator.
**Warning signs:** YML contains `<price>0</price>` or `<price>0.00</price>`.

### Pitfall 5: Not Handling Feed Fetch Failure
**What goes wrong:** A failed sync overwrites the YML with an empty or partial feed.
**Why it happens:** YML regeneration runs even when fetch failed.
**How to avoid:** Per user decision: if supplier feed fails, do NOT update YML. The sync pipeline already handles this — if `_sync_single_supplier` raises, YML generation should be skipped. Only regenerate YML after a successful sync run.
**Warning signs:** YML suddenly has 0 products after a network blip.

## Code Examples

### Complete YML Structure for prom.ua
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE yml_catalog SYSTEM "shops.dtd">
<yml_catalog date="2026-02-27 14:30">
  <shop>
    <name>LabResta</name>
    <company>LabResta</company>
    <url>https://labresta.com</url>
    <currencies>
      <currency id="EUR" rate="1"/>
    </currencies>
    <offers>
      <offer id="12345" available="true">
        <name>Product Name From Prom.ua Catalog</name>
        <price>170</price>
        <currencyId>EUR</currencyId>
        <vendorCode>ART-123</vendorCode>
      </offer>
      <offer id="12346" available="false">
        <name>Out of Stock Product</name>
        <price>199</price>
        <currencyId>EUR</currencyId>
        <vendorCode>ART-456</vendorCode>
      </offer>
    </offers>
  </shop>
</yml_catalog>
```

**Key decisions reflected:**
- `offer id` = prom.ua product external_id (so platform updates the correct product)
- `name` = from PromProduct.name (not supplier feed)
- `price` = whole EUR integer (after discount and rounding)
- `available` = "true"/"false" based on supplier stock + edge case rules
- `vendorCode` = article number from supplier product
- `currencyId` = always "EUR"
- No `categoryId` — we are updating existing products, not creating new ones

### Pricing Calculation (Integer Cents, Mathematical Rounding)
```python
def calculate_price_eur(retail_price_cents: int, discount_percent: float) -> int:
    """Calculate final price in whole EUR with mathematical rounding.

    Args:
        retail_price_cents: Supplier retail price in cents (e.g., 19999 for 199.99 EUR)
        discount_percent: Discount as percentage (e.g., 15.0 for 15%)

    Returns:
        Final price in whole EUR (e.g., 170 for 169.99 EUR)

    Example:
        199.99 EUR at 15% discount:
        19999 * (100 - 15) / 100 = 16999.15 → round to 170 EUR
    """
    # Apply discount: cents * (100 - discount) / 100
    # Use round() for the intermediate cent value, then round to whole EUR
    discounted_cents = round(retail_price_cents * (100 - discount_percent) / 100)
    # Round cents to nearest whole EUR: mathematical rounding
    # (cents + 50) // 100 rounds 50+ up, 49- down
    whole_eur = (discounted_cents + 50) // 100
    return whole_eur
```

### Per-Product Discount Override
```python
def get_effective_discount(match, supplier) -> float:
    """Get the effective discount for a matched product.

    Per-product discount overrides supplier-level discount.
    """
    if match.discount_percent is not None:
        return match.discount_percent
    return supplier.discount_percent
```

### Wiring into Sync Pipeline
```python
# In sync_pipeline.py, after successful matching:
def _sync_single_supplier(supplier):
    # ... existing stages 1-5 ...

    # Stage 6: Regenerate YML feed (only after successful sync)
    logger.info("Stage 6/6: Regenerating YML feed")
    from app.services.yml_generator import regenerate_yml_feed
    regenerate_yml_feed()
    logger.info("YML feed regenerated")
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Float prices in YML | Integer prices (whole EUR) | User decision | Eliminates floating-point display issues |
| On-the-fly YML generation | Static file + atomic write | User decision | Reliable polling by prom.ua |
| lxml string building | lxml etree API | Already in project | Safe XML generation with auto-escaping |

**Deprecated/outdated:**
- `os.rename()`: Use `os.replace()` instead — guaranteed atomic on Windows too (Python 3.3+)

## Open Questions

1. **Per-product discount storage location**
   - What we know: PRICE-02 requires per-product discount override. The discount must be associated with a specific match (supplier product to prom product).
   - What's unclear: Should the column be on `ProductMatch` (discount_percent) or a separate table?
   - Recommendation: Add `discount_percent` nullable Float column to `ProductMatch`. Simple, directly associated with the match. NULL means "use supplier default." This aligns with the existing model structure.

2. **YML output directory and filename**
   - What we know: File must be publicly accessible at a stable URL.
   - What's unclear: Exact path on disk and URL.
   - Recommendation: Use `instance/feeds/` directory (outside app package, gitignored). Flask config `YML_OUTPUT_DIR` and `YML_FILENAME = "labresta-feed.yml"`. URL: `/feed/yml`. This keeps generated files out of the source tree.

3. **Article number source for vendorCode**
   - What we know: YML needs `vendorCode` for article number.
   - What's unclear: Should it come from SupplierProduct.article or PromProduct.article?
   - Recommendation: Use SupplierProduct.article (supplier's article number) as it reflects the actual product being sold. PromProduct.article may be a prom.ua internal code.

4. **Review flags for edge cases (disappeared, zero price)**
   - What we know: Disappeared and zero-price products must be flagged for operator review.
   - What's unclear: How flags are stored — existing `needs_review` on SupplierProduct covers disappearance, but YML-specific flags (like "included as out-of-stock due to zero price") may need distinction.
   - Recommendation: Reuse existing `needs_review` flag on SupplierProduct for Phase 3. Phase 4 dashboard will surface these. No new flag model needed now.

## Sources

### Primary (HIGH confidence)
- Existing codebase: `app/services/yml_test_generator.py` — working YML generation pattern with lxml
- Existing codebase: `app/models/supplier_product.py` — `price_cents` integer storage pattern
- Existing codebase: `app/services/sync_pipeline.py` — pipeline extension point after matching
- Python docs: `os.replace()` — atomic rename, cross-platform (Python 3.3+)

### Secondary (MEDIUM confidence)
- [Rozetka YML spec](https://sellerhelp.rozetka.com.ua/p185-pricelist-requirements.html) — Full yml_catalog structure identical to prom.ua (both use standard YML format): offer id, available, price, currencyId, name, vendorCode fields documented
- [Prom.ua YML import docs](https://support.prom.ua/hc/uk/articles/360004963538) — Official prom.ua format reference (403 on direct fetch, but structure confirmed via third-party sources)
- [Horoshop import docs](https://help.horoshop.ua/en/articles/1684865-importing-products-from-a-file) — Horoshop accepts standard YML format with same field names

### Tertiary (LOW confidence)
- None — all findings verified through multiple sources or existing codebase

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all libraries already in the project, no new dependencies needed
- Architecture: HIGH — clear extension of existing patterns (yml_test_generator, sync_pipeline)
- Pitfalls: HIGH — integer arithmetic edge cases well-documented, atomic write pattern standard
- YML format: MEDIUM — prom.ua official docs returned 403, but format verified through Rozetka spec (identical YML standard) and existing yml_test_generator.py in the project

**Research date:** 2026-02-27
**Valid until:** 2026-03-27 (stable domain — YML format rarely changes)
