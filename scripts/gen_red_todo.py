"""Generate RED_TODO.md — the 38 unresolved red rows grouped by score."""

import json
from urllib.parse import quote
from app import create_app
from app.extensions import db
from app.models.product_match import ProductMatch
from sqlalchemy import select
from sqlalchemy.orm import joinedload

BASE = "http://127.0.0.1:5050"


def search_link(text):
    return f"{BASE}/matches?supplier_id=2&status=candidate&search={quote(text)}"


def main():
    app = create_app()
    with app.app_context():
        with open("red_check_result.json", encoding="utf-8") as f:
            data = json.load(f)

        cand_ids = [r["candidate_match_id"] for r in data["np_candidate"]]
        matches = db.session.execute(
            select(ProductMatch)
            .options(
                joinedload(ProductMatch.supplier_product),
                joinedload(ProductMatch.prom_product),
            )
            .where(
                ProductMatch.id.in_(cand_ids),
                ProductMatch.status == "candidate",
            )
        ).scalars().all()

        def article_key(m):
            return (
                m.supplier_product.article
                or m.prom_product.article
                or m.supplier_product.name[:30]
            )

        def bucket(m):
            s = m.score
            if s == 100:
                return "1_ambiguous_100"
            if s >= 95:
                return "2_score_95_99"
            if s >= 90:
                return "3_score_90_94"
            if s >= 85:
                return "4_score_85_89"
            return "5_score_lt_85"

        groups = {}
        for m in matches:
            groups.setdefault(bucket(m), []).append(m)

        no_match = data["pp_no_match"]

        lines = []
        lines.append("# 38 красных на ручную разборку\n")
        lines.append(
            f"Общая страница: {BASE}/matches?supplier_id=2&status=candidate"
            "&sort=score&order=desc&per_page=100\n"
        )

        if "1_ambiguous_100" in groups:
            g = groups["1_ambiguous_100"]
            lines.append(
                f"\n## AMBIGUOUS score=100 ({len(g)}) — один SP к нескольким PP"
            )
            lines.append(
                "Саладета -GC vs -SC реально разные модели. "
                "Решить: какой из PP оставить; другой — reject.\n"
            )
            for m in sorted(g, key=lambda x: x.supplier_product_id):
                lines.append(
                    f"- match **#{m.id}** (SP#{m.supplier_product_id}) "
                    f"score={m.score}"
                )
                lines.append(f"  - SP: {m.supplier_product.name}")
                lines.append(f"  - PP: {m.prom_product.name}")
                lines.append(f"  - [Открыть]({search_link(article_key(m))})\n")

        headers = [
            ("2_score_95_99", "## score 95-99"),
            ("3_score_90_94", "## score 90-94"),
            ("4_score_85_89", "## score 85-89"),
            ("5_score_lt_85", "## score <85"),
        ]
        for key, title in headers:
            if key not in groups:
                continue
            g = sorted(groups[key], key=lambda x: -x.score)
            lines.append(f"\n{title} ({len(g)})\n")
            for m in g:
                lines.append(f"- match **#{m.id}** score={m.score}")
                lines.append(f"  - SP: {m.supplier_product.name}")
                lines.append(f"  - PP: {m.prom_product.name}")
                lines.append(f"  - [Открыть]({search_link(article_key(m))})\n")

        if no_match:
            lines.append(
                f"\n## БЕЗ матча ({len(no_match)}) — PP в Horoshop, SP нет"
            )
            lines.append(
                "Варианты: найти SP вручную в /products/supplier и сделать "
                "manual-match; либо если у НП этого товара нет — оставить "
                "как есть.\n"
            )
            for r in no_match:
                lines.append(f"- PP#{r['pp_id']}: {r['pp_name']}")
                lines.append(f"  - Labresta URL: {r['labresta_url']}")
                lines.append(f"  - НП URL: {r['np_url']}")
                search_q = quote(r["name"][:30])
                lines.append(
                    f"  - [Поиск SP]({BASE}/products/supplier"
                    f"?supplier_id=2&search={search_q})\n"
                )

        with open("RED_TODO.md", "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print("Written RED_TODO.md")
        for k in sorted(groups):
            print(f"  {k}: {len(groups[k])}")
        print(f"  no_match: {len(no_match)}")


if __name__ == "__main__":
    main()
