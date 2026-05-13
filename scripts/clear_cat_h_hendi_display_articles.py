"""Cat H: clear display_article on 7 PPs where it carries a Hendi code by mistake.

Yana's rule (2026-05-13): only Hendi-vs-not-Hendi collisions are fixed. Intra-brand collisions
(Ozti↔Ozti, Sirman↔Sirman, FROSTY↔FROSTY) are left alone — those manual codes may match future
supplier feeds.

Verification source: scripts/verify_cat_h_article_ownership.py — all 6 articles below appear in
Астим feed (Hendi distributor), so Hendi PPs are the legitimate owners.

Usage:
    .venv/Scripts/python.exe scripts/clear_cat_h_hendi_display_articles.py           # dry-run
    .venv/Scripts/python.exe scripts/clear_cat_h_hendi_display_articles.py --apply   # commit
"""
import sys

from app import create_app
from app.extensions import db
from app.models import PromProduct

sys.stdout.reconfigure(encoding="utf-8")

# (pp_id, expected current display_article, hint for the log)
TARGETS = [
    (347,  "203149", "Spidocook SP300"),
    (80,   "239766", "Fimar PFD27"),
    (154,  "239780", "Roller Grill PIS 30"),
    (958,  "240403", "FROSTY RC-30"),
    (3933, "271599", "FROSTY IC80A"),
    (3932, "271599", "GoodFood ICE777"),
    (4179, "860526", "Saro SKZ-12"),
]


def main() -> int:
    apply = "--apply" in sys.argv
    mode = "APPLY" if apply else "DRY-RUN"

    app = create_app()
    with app.app_context():
        print("=" * 90)
        print(f"Cat H: clear display_article on 7 Hendi-collision PPs  [{mode}]")
        print("=" * 90)

        cleared = 0
        skipped_missing = 0
        skipped_mismatch = 0
        already_empty = 0

        for pp_id, expected, hint in TARGETS:
            pp = db.session.get(PromProduct, pp_id)
            if pp is None:
                print(f"  PP#{pp_id:<5} ({hint:<22}) — ❌ NOT FOUND")
                skipped_missing += 1
                continue
            current = pp.display_article
            if current is None or current == "":
                print(f"  PP#{pp_id:<5} ({hint:<22}) — already empty, skip")
                already_empty += 1
                continue
            if current != expected:
                print(
                    f"  PP#{pp_id:<5} ({hint:<22}) — ⚠️  current={current!r} != expected={expected!r}, "
                    f"SKIP (manual check needed)"
                )
                skipped_mismatch += 1
                continue
            print(
                f"  PP#{pp_id:<5} ({hint:<22}) — display_article={current!r} → NULL"
            )
            if apply:
                pp.display_article = None
            cleared += 1

        if apply and cleared > 0:
            db.session.commit()
            print(f"\n✅ Committed: {cleared} PPs updated.")
        elif apply:
            print(f"\nNo changes committed (nothing to clear).")
        else:
            print(
                f"\nDRY-RUN: would clear {cleared} PPs. "
                f"Re-run with --apply to commit."
            )

        print("-" * 90)
        print(
            f"Summary: cleared={cleared}, already_empty={already_empty}, "
            f"mismatch={skipped_mismatch}, missing={skipped_missing}"
        )
        print("=" * 90)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
