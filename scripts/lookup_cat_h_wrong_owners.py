"""Cat H: read-only lookup of supplier-side SP records for each WRONG-PP in Group A.

For each WRONG owner (non-Hendi PP that received Hendi's display_article by mistake),
find SP rows in supplier feeds that match the PP's true model token (e.g. Spidocook SP300,
Fimar PFD27, Saro SKZ-12). Output: candidate (sup, article, name) — what to write into
display_article on Horoshop side.

No writes. Safe to run via `railway run python scripts/lookup_cat_h_wrong_owners.py`.
"""
import sys
from app import create_app
from app.extensions import db
from app.models import PromProduct, Supplier, SupplierProduct

sys.stdout.reconfigure(encoding="utf-8")

# (PP id, brand, key token to search in SP.name, optional second token)
TARGETS = [
    # ----- Group A (Hendi vs non-Hendi) -----
    (347, "Spidocook", "SP300", None),
    (80, "Fimar", "PFD27", None),
    (154, "Roller Grill", "PIS 30", "PIS30"),
    (958, "FROSTY", "RC-30", "RC30"),
    (3933, "FROSTY", "IC80A", None),
    (3932, "GoodFood", "ICE777", None),
    (4179, "Saro", "SKZ-12", "SKZ12"),
    # ----- Group B (same-brand model variants) -----
    # #1 Ozti SPM 20 vs SPM 70
    (3237, "Ozti", "SPM 20", "SPM20"),
    (3261, "Ozti", "SPM 70", "SPM70"),
    # #3 FROSTY VP-81 vs VP-2Y40
    (4371, "FROSTY", "VP-81", "VP81"),
    (4372, "FROSTY", "VP-2Y40", "VP2Y40"),
    # #8 Sirman TM INOX Normale vs з дисками
    (3275, "Sirman", "TM INOX", "Normale"),
    (3276, "Sirman", "TM INOX", "набір"),
    # #9 Sirman IP 20 M vs IP 10 M
    (3439, "Sirman", "IP 20 M", "IP-20"),
    (3455, "Sirman", "IP 10 M", "IP-10"),
    # #10 Sirman CICLONE 28 VT + A35 vs + A25
    (3108, "Sirman", "CICLONE 28", "A35"),
    (3109, "Sirman", "CICLONE 28", "A25"),
]


def fmt_sp(sp: SupplierProduct, sup_name: str) -> str:
    art = sp.article or "—"
    name = (sp.name or "?")[:100]
    return f"      SP#{sp.id} sup={sup_name!r:<10} art={art!r:<25} {name}"


def main() -> int:
    app = create_app()
    with app.app_context():
        suppliers = {s.id: s.name for s in Supplier.query.all()}
        print("=== Cat H Group A — supplier-side lookups ===")
        print(f"(suppliers: {suppliers})")
        print()

        for pp_id, brand, tok1, tok2 in TARGETS:
            pp = PromProduct.query.get(pp_id)
            if not pp:
                print(f"PP#{pp_id} NOT FOUND")
                continue

            pp_name = (pp.name or pp.name_ru or "?")[:80]
            print(f"PP#{pp_id} brand={pp.brand!r} disp={pp.display_article!r}")
            print(f"  name: {pp_name}")
            print(f"  searching SP.name ILIKE for: {tok1!r}", end="")
            if tok2:
                print(f" or {tok2!r}", end="")
            print()

            patterns = [f"%{tok1}%"]
            if tok2:
                patterns.append(f"%{tok2}%")

            from sqlalchemy import or_
            q = SupplierProduct.query.filter(
                or_(*[SupplierProduct.name.ilike(p) for p in patterns])
            ).order_by(SupplierProduct.supplier_id, SupplierProduct.id)
            sps = q.all()

            if not sps:
                print(f"    NO MATCHES — token absent from all supplier feeds")
            else:
                print(f"    FOUND {len(sps)} SP candidates:")
                for sp in sps[:15]:
                    sup_name = suppliers.get(sp.supplier_id, f"sup{sp.supplier_id}")
                    print(fmt_sp(sp, sup_name))
                if len(sps) > 15:
                    print(f"    ... +{len(sps)-15} more (truncated)")
            print()

        print("=== done — no writes performed ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
