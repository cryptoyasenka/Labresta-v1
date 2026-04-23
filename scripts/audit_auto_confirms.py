"""Read-only audit of R1-R4 auto-confirm rules + Stage 5 user rules.

Checks five risk surfaces:
  1. Volume: how many matches were auto-confirmed vs human-confirmed.
  2. R2 subset-risk: confirmed pairs where sp/pp tokens differ by exactly
     one ASCII-alpha token (single-letter SKU suffix case like APRI-47 vs
     APRI-47P). High risk of bundle/variant misconfirm.
  3. R1 parens-risk: confirmed pairs where sp.name or pp.name contains '(...)'
     content (meaningful_tokens strips parens → variant differences inside
     parens are invisible to the rule).
  4. R4 reject sample: 10 recent rejects with sibling confirmed pair.
  5. 1:1 invariant: pp_ids with >1 confirmed/manual match (should be 0).

Pure read-only. Exits non-zero only on crash.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import select, func, or_

from app import create_app
from app.extensions import db
from app.models.catalog import PromProduct
from app.models.product_match import ProductMatch
from app.models.supplier_product import SupplierProduct
from app.services.matcher import (
    after_brand_remainder,
    extract_model_from_name,
    meaningful_tokens,
    normalize_model,
)


def _section(title):
    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


def q1_volume():
    _section("1. VOLUME by confirmed_by source")
    rows = db.session.execute(
        select(ProductMatch.confirmed_by, ProductMatch.status, func.count(ProductMatch.id))
        .group_by(ProductMatch.confirmed_by, ProductMatch.status)
        .order_by(func.count(ProductMatch.id).desc())
    ).all()
    total_by_status = {}
    for by, status, cnt in rows:
        print(f"  {status:10s}  confirmed_by={by!r:40s}  {cnt}")
        total_by_status[status] = total_by_status.get(status, 0) + cnt
    print(f"  --- totals: {total_by_status}")


def q2_r2_single_letter_diff():
    _section("2. R2-RISK: confirmed auto-pairs where tokens differ by 1 ASCII-alpha token")
    rows = db.session.execute(
        select(ProductMatch, SupplierProduct, PromProduct)
        .join(SupplierProduct, ProductMatch.supplier_product_id == SupplierProduct.id)
        .join(PromProduct, ProductMatch.prom_product_id == PromProduct.id)
        .where(
            ProductMatch.status == "confirmed",
            ProductMatch.confirmed_by.like("%bulk_auto_confirm%"),
        )
    ).all()
    hits = []
    for m, sp, pp in rows:
        sup_t = meaningful_tokens(after_brand_remainder(sp.name or "", sp.brand))
        prom_t = meaningful_tokens(after_brand_remainder(pp.name or "", pp.brand))
        if sup_t == prom_t:
            continue
        # strict-subset in either direction, diff-set is all single-letter ASCII alpha
        if sup_t < prom_t:
            diff = prom_t - sup_t
        elif prom_t < sup_t:
            diff = sup_t - prom_t
        else:
            continue
        if not diff:
            continue
        if all(len(t) == 1 and t.isascii() and t.isalpha() for t in diff):
            hits.append((m, sp, pp, diff))
    print(f"  Found {len(hits)} suspicious R2 auto-confirms")
    for m, sp, pp, diff in hits[:30]:
        print(f"    match#{m.id}  price={m.score}  diff={diff}")
        print(f"      SP#{sp.id}: {sp.name!r}  price_cents={sp.price_cents}")
        print(f"      PP#{pp.id}: {pp.name!r}  price={pp.price}")


def q3_r1_parens_risk():
    _section("3. R1-RISK: confirmed auto-pairs where sp.name or pp.name contains parens")
    rows = db.session.execute(
        select(ProductMatch, SupplierProduct, PromProduct)
        .join(SupplierProduct, ProductMatch.supplier_product_id == SupplierProduct.id)
        .join(PromProduct, ProductMatch.prom_product_id == PromProduct.id)
        .where(
            ProductMatch.status == "confirmed",
            ProductMatch.confirmed_by.like("%bulk_auto_confirm%"),
            or_(SupplierProduct.name.like("%(%"), PromProduct.name.like("%(%")),
        )
    ).all()
    print(f"  Found {len(rows)} auto-confirmed pairs with parens in name")
    for m, sp, pp in rows[:30]:
        print(f"    match#{m.id}")
        print(f"      SP#{sp.id}: {sp.name!r}")
        print(f"      PP#{pp.id}: {pp.name!r}")


def q4_r4_rejects():
    _section("4. R4 REJECTS sample: 10 rejected matches (auto-rejected)")
    rows = db.session.execute(
        select(ProductMatch, SupplierProduct, PromProduct)
        .join(SupplierProduct, ProductMatch.supplier_product_id == SupplierProduct.id)
        .join(PromProduct, ProductMatch.prom_product_id == PromProduct.id)
        .where(ProductMatch.status == "rejected")
        .limit(10)
    ).all()
    print(f"  Showing {len(rows)} rejected matches")
    for m, sp, pp in rows:
        print(f"    match#{m.id}  score={m.score}")
        print(f"      SP#{sp.id}: {sp.name!r}")
        print(f"      PP#{pp.id}: {pp.name!r}")
        # Find sibling confirmed for same sp
        sibling = ProductMatch.query.filter_by(
            supplier_product_id=sp.id,
        ).filter(ProductMatch.status.in_(("confirmed", "manual"))).first()
        if sibling:
            spp = db.session.get(PromProduct, sibling.prom_product_id)
            print(f"      sibling confirmed → PP#{spp.id}: {spp.name!r}")
        else:
            print(f"      (no sibling confirmed — pure reject)")


def q5_one_to_one():
    _section("5. 1:1 INVARIANT: pp_ids with >1 confirmed/manual")
    rows = db.session.execute(
        select(ProductMatch.prom_product_id, func.count(ProductMatch.id))
        .where(ProductMatch.status.in_(("confirmed", "manual")))
        .group_by(ProductMatch.prom_product_id)
        .having(func.count(ProductMatch.id) > 1)
    ).all()
    if not rows:
        print("  OK — no violations")
        return
    for pp_id, cnt in rows:
        pp = db.session.get(PromProduct, pp_id)
        print(f"  PP#{pp_id} ({pp.name!r}) has {cnt} confirmed/manual matches:")
        mms = ProductMatch.query.filter_by(prom_product_id=pp_id).filter(
            ProductMatch.status.in_(("confirmed", "manual"))
        ).all()
        for mm in mms:
            sp = db.session.get(SupplierProduct, mm.supplier_product_id)
            print(f"    match#{mm.id}  by={mm.confirmed_by}  SP#{sp.id}: {sp.name!r}")


def q6_parens_variant_collision():
    """For every R1/R3 auto-confirm with parens, check if the catalog has
    ANOTHER pp with the same normalized model. If yes, the parens content
    may be the actual discriminator — auto-confirm is suspicious."""
    _section("6. R1 PARENS + SIBLING-PP EXISTS (variant-collision risk)")
    rows = db.session.execute(
        select(ProductMatch, SupplierProduct, PromProduct)
        .join(SupplierProduct, ProductMatch.supplier_product_id == SupplierProduct.id)
        .join(PromProduct, ProductMatch.prom_product_id == PromProduct.id)
        .where(
            ProductMatch.status == "confirmed",
            ProductMatch.confirmed_by.like("%bulk_auto_confirm%"),
            or_(SupplierProduct.name.like("%(%"), PromProduct.name.like("%(%")),
        )
    ).all()
    hits = []
    for m, sp, pp in rows:
        pp_key = (
            normalize_model(pp.article)
            or normalize_model(pp.model)
            or normalize_model(pp.display_article)
            or normalize_model(extract_model_from_name(pp.name or "", pp.brand))
        )
        if not pp_key or len(pp_key) < 4:
            continue
        siblings = db.session.execute(
            select(PromProduct).where(
                PromProduct.id != pp.id,
                PromProduct.brand == pp.brand,
            )
        ).scalars().all()
        sibling_hits = []
        for s in siblings:
            s_key = (
                normalize_model(s.article)
                or normalize_model(s.model)
                or normalize_model(s.display_article)
                or normalize_model(extract_model_from_name(s.name or "", s.brand))
            )
            if s_key == pp_key:
                sibling_hits.append(s)
        if sibling_hits:
            hits.append((m, sp, pp, sibling_hits))
    print(f"  Found {len(hits)} auto-confirms where catalog has another pp with SAME normalized model")
    for m, sp, pp, siblings in hits:
        print(f"    match#{m.id}  confirmed_by={m.confirmed_by}")
        print(f"      SP#{sp.id}: {sp.name!r}")
        print(f"      PP#{pp.id} (confirmed): {pp.name!r}")
        for s in siblings[:3]:
            print(f"      PP#{s.id} (sibling, NOT matched): {s.name!r}")


def q7_all_rejected_counts():
    _section("7. REJECTED status — does R4 ever fire?")
    rows = db.session.execute(
        select(ProductMatch.confirmed_by, func.count(ProductMatch.id))
        .where(ProductMatch.status == "rejected")
        .group_by(ProductMatch.confirmed_by)
    ).all()
    if not rows:
        print("  ZERO rejected matches in product_matches — R4 never fired or rejects are deleted")
        return
    for by, cnt in rows:
        print(f"  confirmed_by={by!r}  {cnt}")


import re as _re
_PAREN_RE = _re.compile(r"\(([^)]*)\)")
# Numbers, units, voltage markers that don't count as discriminators
_PAREN_NOISE = _re.compile(
    r"\b(?:220|230|380|400|[вb]|kw|квт|вт|w|мм|см|м|л|кг|г|мл|шт|штук|рівн[іь]|"
    r"літрів|літри|літра|gn|[.,\d/xх\s-]+)\b",
    _re.IGNORECASE,
)


def _parens_discriminator(name: str) -> set[str]:
    """Return significant tokens from parens content, stripping units/voltage."""
    out = set()
    for m in _PAREN_RE.finditer(name or ""):
        inner = m.group(1).lower()
        inner = _PAREN_NOISE.sub(" ", inner)
        for tok in _re.split(r"[\s,./+\-]+", inner):
            tok = tok.strip()
            if tok and len(tok) >= 2 and not tok.isdigit():
                out.add(tok)
    return out


def q8_candidate_bracket_discriminator_mismatch():
    """Candidate matches where BOTH sp and pp have parens content that differs
    in non-numeric/non-voltage tokens. These are suspect candidates that the
    current matcher generates at high score but shouldn't."""
    _section("8. CANDIDATE matches with conflicting parens discriminators (score ≥ 90)")
    rows = db.session.execute(
        select(ProductMatch, SupplierProduct, PromProduct)
        .join(SupplierProduct, ProductMatch.supplier_product_id == SupplierProduct.id)
        .join(PromProduct, ProductMatch.prom_product_id == PromProduct.id)
        .where(
            ProductMatch.status == "candidate",
            ProductMatch.score >= 90,
            SupplierProduct.name.like("%(%"),
            PromProduct.name.like("%(%"),
        )
    ).all()
    hits = []
    for m, sp, pp in rows:
        sp_disc = _parens_discriminator(sp.name)
        pp_disc = _parens_discriminator(pp.name)
        if not sp_disc or not pp_disc:
            continue
        if sp_disc == pp_disc:
            continue
        if sp_disc & pp_disc:  # partial overlap — skip
            continue
        hits.append((m, sp, pp, sp_disc, pp_disc))
    print(f"  Found {len(hits)} suspect candidates")
    for m, sp, pp, sd, pd in hits:
        print(f"    match#{m.id}  score={m.score}")
        print(f"      SP#{sp.id}: {sp.name!r}  disc={sd}")
        print(f"      PP#{pp.id}: {pp.name!r}  disc={pd}")


def q9_one_sided_parens():
    """Candidate matches where ONE side has parens and the other doesn't.
    Often benign (SP short, PP verbose) but can hide variants."""
    _section("9. CANDIDATE one-sided parens with non-numeric content (score ≥ 95)")
    rows = db.session.execute(
        select(ProductMatch, SupplierProduct, PromProduct)
        .join(SupplierProduct, ProductMatch.supplier_product_id == SupplierProduct.id)
        .join(PromProduct, ProductMatch.prom_product_id == PromProduct.id)
        .where(
            ProductMatch.status == "candidate",
            ProductMatch.score >= 95,
        )
    ).all()
    hits = []
    for m, sp, pp in rows:
        sp_has = "(" in (sp.name or "")
        pp_has = "(" in (pp.name or "")
        if sp_has == pp_has:
            continue
        disc = _parens_discriminator(sp.name if sp_has else pp.name)
        if disc:
            hits.append((m, sp, pp, disc, "sp" if sp_has else "pp"))
    print(f"  Found {len(hits)} candidates with one-sided non-trivial parens (score ≥95)")
    for m, sp, pp, disc, side in hits[:30]:
        print(f"    match#{m.id}  score={m.score}  parens-on={side}  disc={disc}")
        print(f"      SP#{sp.id}: {sp.name!r}")
        print(f"      PP#{pp.id}: {pp.name!r}")


def main():
    app = create_app()
    with app.app_context():
        q1_volume()
        q2_r2_single_letter_diff()
        q3_r1_parens_risk()
        q4_r4_rejects()
        q5_one_to_one()
        q6_parens_variant_collision()
        q7_all_rejected_counts()
        q8_candidate_bracket_discriminator_mismatch()
        q9_one_sided_parens()


if __name__ == "__main__":
    main()
