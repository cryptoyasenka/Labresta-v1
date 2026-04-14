"""Merge duplicate SupplierProduct rows by (supplier_id, name, brand).

MARESTO периодически меняет external_id у того же товара — в БД копятся
дубликаты SupplierProduct с одинаковым именем/брендом. Matcher находит их
повторно, UI показывает лишние строки, 1:1 инвариант начинает ломаться.

Логика:
  - Группируем по (supplier_id, lower(strip(name)), lower(strip(brand)))
  - В группе >1 строк → winner = max(id) (самая свежая), остальные = losers
  - Для каждого loser:
      * переносим все ProductMatch на winner (remap supplier_product_id)
      * при конфликте (winner уже имеет match с тем же pp_id) оставляем
        строку с высшим приоритетом статуса (manual > confirmed > candidate > rejected),
        лишнюю удаляем
  - Удаляем loser SupplierProduct

--dry-run по умолчанию. --apply чтобы закоммитить.
--supplier-id N — ограничить одним поставщиком.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from collections import defaultdict

from app import create_app
from app.extensions import db
from app.models.product_match import ProductMatch
from app.models.supplier_product import SupplierProduct


STATUS_PRIORITY = {"manual": 4, "confirmed": 3, "candidate": 2, "rejected": 1}


def _norm(s: str | None) -> str:
    return (s or "").strip().lower()


def _key(sp: SupplierProduct) -> tuple[int, str, str]:
    return (sp.supplier_id, _norm(sp.name), _norm(sp.brand))


def _pick_winner_match(a: ProductMatch, b: ProductMatch) -> tuple[ProductMatch, ProductMatch]:
    """Return (keep, drop) — keep has higher status priority; tie → higher id."""
    pa, pb = STATUS_PRIORITY.get(a.status, 0), STATUS_PRIORITY.get(b.status, 0)
    if pa != pb:
        return (a, b) if pa > pb else (b, a)
    return (a, b) if a.id >= b.id else (b, a)


def find_duplicate_groups(supplier_id: int | None) -> dict[tuple, list[SupplierProduct]]:
    q = SupplierProduct.query
    if supplier_id:
        q = q.filter(SupplierProduct.supplier_id == supplier_id)
    groups: dict[tuple, list[SupplierProduct]] = defaultdict(list)
    for sp in q.all():
        if not _norm(sp.name):
            continue
        groups[_key(sp)].append(sp)
    return {k: v for k, v in groups.items() if len(v) > 1}


def run(apply: bool, supplier_id: int | None) -> None:
    app = create_app()
    with app.app_context():
        groups = find_duplicate_groups(supplier_id)
        print(f"Duplicate groups: {len(groups)}")
        if not groups:
            print("Nothing to do.")
            return

        total_losers = 0
        total_matches_moved = 0
        total_matches_dropped = 0
        total_sp_deleted = 0

        for key, rows in sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0])):
            rows_sorted = sorted(rows, key=lambda r: r.id, reverse=True)
            winner = rows_sorted[0]
            losers = rows_sorted[1:]
            total_losers += len(losers)
            print(
                f"\n  supplier={key[0]} name={key[1][:60]!r} brand={key[2]!r}: "
                f"winner=sp#{winner.id} (ext={winner.external_id}), "
                f"losers={[f'sp#{l.id}(ext={l.external_id})' for l in losers]}"
            )

            winner_matches: dict[int, ProductMatch] = {
                m.prom_product_id: m
                for m in ProductMatch.query.filter_by(supplier_product_id=winner.id).all()
            }

            for loser in losers:
                loser_matches = ProductMatch.query.filter_by(
                    supplier_product_id=loser.id
                ).all()
                for lm in loser_matches:
                    existing = winner_matches.get(lm.prom_product_id)
                    if existing is None:
                        print(
                            f"    move match#{lm.id} pp={lm.prom_product_id} "
                            f"status={lm.status} → sp#{winner.id}"
                        )
                        if apply:
                            lm.supplier_product_id = winner.id
                        winner_matches[lm.prom_product_id] = lm
                        total_matches_moved += 1
                    else:
                        keep, drop = _pick_winner_match(existing, lm)
                        print(
                            f"    conflict pp={lm.prom_product_id}: "
                            f"keep match#{keep.id}({keep.status}), drop match#{drop.id}({drop.status})"
                        )
                        if apply:
                            if keep is lm:
                                db.session.delete(existing)
                                db.session.flush()
                                lm.supplier_product_id = winner.id
                                db.session.flush()
                                winner_matches[lm.prom_product_id] = lm
                            else:
                                db.session.delete(lm)
                                db.session.flush()
                        total_matches_dropped += 1

                print(f"    delete sp#{loser.id}")
                if apply:
                    db.session.delete(loser)
                total_sp_deleted += 1

        print("\n=== Summary ===")
        print(f"Groups:           {len(groups)}")
        print(f"Losers:           {total_losers}")
        print(f"Matches moved:    {total_matches_moved}")
        print(f"Matches dropped:  {total_matches_dropped}")
        print(f"SP deleted:       {total_sp_deleted}")

        if not apply:
            print("\nDRY-RUN — pass --apply to commit.")
            return

        db.session.commit()
        print("\nAPPLIED.")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--apply", action="store_true")
    p.add_argument("--supplier-id", type=int, default=None)
    args = p.parse_args()
    run(args.apply, args.supplier_id)


if __name__ == "__main__":
    main()
