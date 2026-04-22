"""Verify all products from Лабреста Х.xlsx are matched in DB.

Strategy: extract article (HKN-XXX pattern) from name, look up SP by article,
check match status. Report anything that's in the file but not confirmed/manual.
"""
import json
import re
from app import create_app
from app.extensions import db
from app.models.supplier_product import SupplierProduct
from app.models.product_match import ProductMatch


NAME_ANCHOR_RE = re.compile(r"HKN[- ]([A-Z0-9][A-Z0-9]*(?:[- ][A-Z0-9]+)?)", re.IGNORECASE)


def extract_anchor(name: str, url: str) -> str | None:
    """Return a short uniquely-identifying tail (e.g. 'WD-120L', 'DRT520').

    Takes at most 2 tokens after `HKN-` because:
    - 1 token: `HKN-PCORN` → "PCORN" (single-word products)
    - 2 tokens: `HKN-WD-120L` → "WD-120L" (model + size)
    URLs often append descriptive words (color, capacity, shape) that the
    SP article doesn't have, so we stop early. If 2-token match misses,
    find_sp falls back to 1-token.
    """
    if url:
        m = re.search(r"hkn-([a-z0-9\-]+?)/?\s*$", url, re.IGNORECASE)
        if m:
            tokens = [t for t in m.group(1).rstrip("/").split("-") if t]
            if tokens:
                return "-".join(tokens[:2]).upper()
    if name:
        m = NAME_ANCHOR_RE.search(name.upper())
        if m:
            return m.group(1).upper().replace(" ", "-")
    return None


def _first_token(anchor: str) -> str:
    return anchor.split("-")[0] if anchor else anchor


def _anchor_variants(anchor: str) -> list[str]:
    """Patterns to try when searching SP.article/name/external_id.

    Suppliers are inconsistent: "HKN WD-120L", "HKN-WD-120L", "HKNWD120L",
    "WD-120L" all refer to the same product. Generate ilike patterns for
    each plausible normalisation.
    """
    a = anchor.strip("- ")
    variants = {a, a.replace("-", " "), a.replace("-", ""), a.replace("-", "_")}
    return [f"%{v}%" for v in variants if v]


def _hkn_patterns(anchor: str) -> list[str]:
    """Patterns that include an HKN prefix — tried FIRST because short anchors
    ("C1", "A2") are too generic for a bare `%C1%` search (matches AC12, PC10,
    etc; .first() returns the wrong SP). HKN-anchored patterns disambiguate.
    """
    a = anchor.strip("- ")
    if not a:
        return []
    bodies = {a, a.replace("-", " "), a.replace("-", ""), a.replace("-", "_")}
    pats: list[str] = []
    for b in bodies:
        pats.extend([f"HKN-{b}%", f"HKN {b}%", f"HKN{b}%"])
    return pats


def find_sp(session, supplier_id: int, anchor: str):
    """Look up an SP by anchor. Tiered: HKN-prefixed exact-ish first, then
    loose substring fallback. Three tiers total:

      1. HKN-{anchor}* — disambiguates short generic anchors.
      2. %anchor% — loose substring on article/external_id/name.
      3. %first_token% — last resort when anchor has descriptive suffix.
    """
    from sqlalchemy import or_ as sa_or

    def _search(patterns: list[str]):
        for pat in patterns:
            sp = session.query(SupplierProduct).filter(
                SupplierProduct.supplier_id == supplier_id,
                sa_or(
                    SupplierProduct.article.ilike(pat),
                    SupplierProduct.external_id.ilike(pat),
                    SupplierProduct.name.ilike(pat),
                ),
            ).first()
            if sp:
                return sp
        return None

    # Tier 1: HKN-prefixed variants (both full anchor and first token)
    for tier_anchor in (anchor, _first_token(anchor)):
        if not tier_anchor:
            continue
        sp = _search(_hkn_patterns(tier_anchor))
        if sp:
            return sp

    # Tier 2 & 3: loose substring
    seen: set[str] = set()
    for tier in (anchor, _first_token(anchor)):
        if not tier or tier in seen:
            continue
        seen.add(tier)
        sp = _search(_anchor_variants(tier))
        if sp:
            return sp
    return None


def main():
    with open("labresta_x_dump.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # Find products sheet
    prod_sheet = None
    for sheet in data.values():
        if sheet["max_row"] > 100:
            prod_sheet = sheet
            break

    rows = prod_sheet["rows"]
    # Data starts at row 5; columns: 0=№, 1=np_url, 2=name, 3=price_np, 4=rts, 5=lab_price, 6=lab_url
    products = []
    for r in rows[5:]:
        if not r or not isinstance(r[0], int):
            continue
        products.append({
            "num": r[0],
            "np_url": r[1],
            "name": r[2],
            "np_price": r[3],
            "rts_price": r[4],
            "lab_price": r[5],
            "lab_url": r[6],
            "discount": r[7],
            "diff": r[8],
        })
    print(f"Products in file: {len(products)}")

    # SPLIT: "надо сматчить" = есть и np_url и lab_url.
    # Если нет lab_url — товара нет в Horoshop, матчить не надо.
    needed = [p for p in products if p.get("np_url") and p.get("lab_url")]
    not_in_horoshop = [p for p in products if p.get("np_url") and not p.get("lab_url")]
    print(f"  'нужны' (есть в Horoshop): {len(needed)}")
    print(f"  'не в Horoshop' (lab_url пустой): {len(not_in_horoshop)}")
    products = needed  # только эти надо проверять

    app = create_app()
    with app.app_context():
        # Stats
        matched_ok = []      # has confirmed/manual match
        matched_cand = []    # has only candidate match
        no_match = []        # SP exists but no match
        no_sp = []           # SP not in DB at all
        no_article = []      # Can't extract article

        for p in products:
            art = extract_anchor(p["name"] or "", p["np_url"] or "")
            if not art:
                no_article.append(p)
                continue

            sp = find_sp(db.session, 2, art)
            if not sp:
                no_sp.append({**p, "article": art})
                continue

            matches = db.session.query(ProductMatch).filter_by(
                supplier_product_id=sp.id
            ).all()
            has_confirmed = any(m.status in ("confirmed", "manual") for m in matches)
            has_candidate = any(m.status == "candidate" for m in matches)

            if has_confirmed:
                matched_ok.append({"sp_id": sp.id, "article": art, **p})
            elif has_candidate:
                matched_cand.append({"sp_id": sp.id, "article": art, **p})
            else:
                no_match.append({"sp_id": sp.id, "article": art, **p})

    print(f"\n=== RESULTS ===")
    print(f"Fully matched (confirmed/manual): {len(matched_ok)}")
    print(f"Only candidate (needs Yana click): {len(matched_cand)}")
    print(f"SP exists but NO match row: {len(no_match)}")
    print(f"Not in DB as SP at all: {len(no_sp)}")
    print(f"Could not extract article: {len(no_article)}")

    out = {
        "summary": {
            "total": len(products),
            "matched_ok": len(matched_ok),
            "matched_candidate": len(matched_cand),
            "no_match": len(no_match),
            "no_sp": len(no_sp),
            "no_article": len(no_article),
        },
        "matched_candidate": matched_cand,
        "no_match": no_match,
        "no_sp": no_sp,
        "no_article": no_article,
    }
    with open("labresta_x_verify.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2, default=str)
    print(f"\nDetails in labresta_x_verify.json")


if __name__ == "__main__":
    main()
