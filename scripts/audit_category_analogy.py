"""Evidence audit: run the category resolver chain over REAL unmatched products.

WHY this script (RESEARCH Q4 step 5 + REQ-06): decision D3 says the create-card
«Раздел» is assigned by analogy with similar existing cards, with AI only as a
Yana-approved option. Before anyone trusts that, we need to SEE the chain's
choices on real data — which categories it picks, at what confidence, via which
tier, and (for НП) which feed categories do NOT reconcile to the store tree and
would therefore need a manual mapping. This produces the evidence consumed by
CATEGORY-PROPOSAL.md so Yana can choose ship-no-AI / enable-AI / mapping-table.

READ-ONLY. It queries products + an uploaded Horoshop export corpus and a local
NP feed; it writes NOTHING to the DB and makes NO network calls (the feed is a
local path). The AI tier stays OFF (ai_enabled=False) — zero network.

A HARD PROD GUARD (copied from generate_maresto_availability.py) refuses to run
against anything that isn't local sqlite, so it can never touch prod even though
it only reads (CLAUDE.md #10/#13).

Usage:
    python scripts/audit_category_analogy.py --export "horoshop-export 26.05.26.xlsx"
        [--supplier novyy-proekt] [--np-feed .planning/plans/np-feed/np-feed.xlsx]
        [--cutoff 60] [--out instance/category-analogy-audit.csv]
"""

import argparse
import csv
import sys
from collections import Counter
from pathlib import Path

# Allow running as `python scripts/audit_category_analogy.py` from anywhere.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import select

from app import create_app
from app.extensions import db
from app.models.supplier import Supplier
from app.services.add_horoshop_file import _query_unmatched
from app.services.category_export import read_category_corpus
from app.services.category_resolver import (
    DEFAULT_ANALOGY_CUTOFF,
    FeedCategoryResolver,
    build_resolver,
)
from app.services.np_parser import parse_np_feed

DEFAULT_SUPPLIER = "novyy-proekt"  # the ~205-item NP bucket (D2/D3 focus)
DEFAULT_OUT = (
    Path(__file__).resolve().parent.parent / "instance" / "category-analogy-audit.csv"
)
_CSV_FIELDS = [
    "article", "name", "brand", "chosen_category", "confidence", "source", "analog_id",
]


def _parse_args(argv) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--export", required=True, help="Horoshop export .xlsx (category corpus)")
    p.add_argument("--supplier", default=DEFAULT_SUPPLIER, help="supplier slug (default: NP)")
    p.add_argument("--np-feed", default=None, help="local NP feed .xlsx (enables the feed tier)")
    p.add_argument("--cutoff", type=float, default=DEFAULT_ANALOGY_CUTOFF, help="analogy cutoff 0..100")
    p.add_argument("--out", default=str(DEFAULT_OUT), help="CSV output path")
    return p.parse_args(argv)


def main(argv=None) -> int:
    args = _parse_args(argv if argv is not None else sys.argv[1:])

    app = create_app()
    with app.app_context():
        url = str(db.engine.url)
        # HARD GUARD: read-only, but never let it be pointed at prod.
        if "sqlite" not in url.lower() or any(
            t in url.lower() for t in ("rlwy", "railway", "postgres", "psycopg")
        ):
            print(f"ABORT: DB is not local sqlite ({url}). Refusing to run.")
            return 2
        print(f"DB: {url}")

        supplier = db.session.execute(
            select(Supplier).where(Supplier.slug == args.supplier)
        ).scalar_one_or_none()
        if supplier is None:
            print(f"ABORT: supplier slug={args.supplier!r} not found.")
            return 2

        # Category corpus from the export (the «Раздел» catalog_import drops).
        corpus, corpus_errs = read_category_corpus(args.export)
        if corpus_errs:
            for e in corpus_errs:
                print(f"  export warning: {e}")
        store_cats = {r["category"] for r in corpus if r.get("category")}
        print(
            f"Corpus: {len(corpus)} rows, {len(store_cats)} distinct store categories, "
            f"{len({r['brand'] for r in corpus if r.get('brand')})} brands."
        )

        # Optional NP feed → per-article category getter (enables the feed tier).
        feed_by_article: dict[str, dict] = {}
        if args.np_feed:
            feed_content, feed_errs = parse_np_feed(args.np_feed)
            if feed_errs:
                print(f"  NP feed parse warnings: {len(feed_errs)}")
            feed_by_article = {
                (art or "").strip(): row for art, row in feed_content.items()
            }
            print(f"NP feed: {len(feed_by_article)} articles (feed tier ENABLED).")
        else:
            print("NP feed: none (feed tier disabled → analogy→fallback).")

        def _feed_getter(sp):
            fr = feed_by_article.get((getattr(sp, "article", None) or "").strip())
            return fr.get("category") if fr else None

        resolver = build_resolver(
            corpus,
            strategies=("feed", "analogy", "fallback"),
            feed_category_getter=(_feed_getter if feed_by_article else None),
            ai_enabled=False,  # decision D3 — AI off; this is the evidence run.
            analogy_cutoff=args.cutoff,
        )

        pairs = _query_unmatched(supplier.id)
        print(f"Unmatched {supplier.slug!r} products: {len(pairs)}")

        rows: list[dict] = []
        by_source = Counter()
        cat_dist = Counter()
        for sp, _ri in pairs:
            res = resolver.resolve(sp, brand=sp.brand)
            by_source[res.source] += 1
            cat_dist[res.category or "(none)"] += 1
            rows.append({
                "article": (sp.article or "").strip(),
                "name": sp.name or "",
                "brand": sp.brand or "",
                "chosen_category": res.category or "",
                "confidence": f"{res.confidence:.1f}",
                "source": res.source,
                "analog_id": res.analog_id or "",
            })

        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=_CSV_FIELDS)
            w.writeheader()
            w.writerows(rows)
        print(f"\nWrote {len(rows)} rows -> {out_path}")

        # ---- Console summary -------------------------------------------------
        print("\n=== BY SOURCE ===")
        for src in ("feed", "analogy", "ai", "fallback", "none"):
            if by_source.get(src):
                pct = 100.0 * by_source[src] / max(len(rows), 1)
                print(f"  {src:9s} {by_source[src]:5d}  ({pct:4.1f}%)")

        print("\n=== TOP ASSIGNED CATEGORIES ===")
        for cat, n in cat_dist.most_common(15):
            print(f"  {n:5d}  {cat}")

        # ---- NP feed <-> store reconciliation delta --------------------------
        # Distinct feed categories that did NOT reconcile to a store label, so
        # Yana sees exactly which feed categories need a store-tree mapping.
        if feed_by_article:
            fr_resolver = FeedCategoryResolver(store_cats, _feed_getter)
            feed_cats = {
                (r.get("category") or "").strip()
                for r in feed_by_article.values()
                if (r.get("category") or "").strip()
            }
            unreconciled = sorted(
                fc for fc in feed_cats
                if fr_resolver.reconcile(fc).category is None
            )
            print(
                f"\n=== FEED <-> STORE RECONCILIATION ===\n"
                f"  distinct feed categories: {len(feed_cats)}\n"
                f"  reconciled to store tree: {len(feed_cats) - len(unreconciled)}\n"
                f"  UNRECONCILED (need a store-tree mapping): {len(unreconciled)}"
            )
            for fc in unreconciled[:40]:
                print(f"    - {fc}")
            if len(unreconciled) > 40:
                print(f"    ... +{len(unreconciled) - 40} more (see proposal)")
        else:
            print("\n=== FEED <-> STORE RECONCILIATION ===\n  (no NP feed supplied)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
