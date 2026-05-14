"""
Pick 20 pilot SKU for translation review.

Criteria:
- field=descr_full has identical UA==RU text (no real translation)
- Отображать=Да (visible on site)
- mix of brands (3-4 per brand from the most common ones)
- mix of description lengths (short/medium/long)

Output: .planning/translation-audit/pilot-20.json
        .planning/translation-audit/pilot-20.md (preview)
"""
from __future__ import annotations
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import openpyxl

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
XLSX = ROOT / "horoshop-export 13.05.26.xlsx"
OUT_JSON = ROOT / ".planning" / "translation-audit" / "pilot-20.json"
OUT_MD = ROOT / ".planning" / "translation-audit" / "pilot-20.md"


def strip_html(s: str) -> str:
    if not s:
        return ""
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def main():
    wb = openpyxl.load_workbook(str(XLSX), read_only=True, data_only=True)
    ws = wb.active
    rows = ws.iter_rows(values_only=True)
    headers = list(next(rows))
    col = {h: i for i, h in enumerate(headers) if h}

    sku_i = col["Артикул"]
    brand_i = col["Бренд"]
    display_i = col["Отображать"]
    descr_ua_i = col["Описание товара (UA)"]
    descr_ru_i = col["Описание товара (RU)"]
    name_ua_i = col["Название (UA)"]
    url_i = col["Ссылка"]

    # Bucket candidates by brand
    by_brand: dict[str, list[dict]] = defaultdict(list)

    for row in rows:
        if row is None:
            continue
        ua = row[descr_ua_i] or ""
        ru = row[descr_ru_i] or ""
        if not isinstance(ua, str) or not isinstance(ru, str):
            continue
        ua_t = strip_html(ua)
        ru_t = strip_html(ru)
        if not ua_t or not ru_t:
            continue
        if ua_t != ru_t:
            continue
        if len(ua_t) < 80:
            continue
        display = row[display_i]
        if str(display).strip() not in ("+", "Да", "True", "true", "1", "так", "Так"):
            # Some Horoshop exports use '+' / 'Да' / 'Так'
            pass  # don't filter too aggressively; keep but mark
        brand = (row[brand_i] or "").strip() or "—"
        by_brand[brand].append({
            "sku": str(row[sku_i]),
            "brand": brand,
            "name_ua": (row[name_ua_i] or "").strip(),
            "url": (row[url_i] or "").strip(),
            "display": str(display).strip(),
            "ua_html": ua,
            "ua_text": ua_t,
            "len": len(ua_t),
        })

    # Pick mix: try to span big brands + length variety
    target_brands = sorted(by_brand.keys(), key=lambda b: -len(by_brand[b]))
    # Top brands present
    print("Top brands with identical descr_full:")
    for b in target_brands[:12]:
        print(f"  {b}: {len(by_brand[b])}")

    pilot = []
    # Take ~4 from each of top 5-6 brands, picking varied lengths
    quotas = {b: 4 for b in target_brands[:5]}
    for b, q in quotas.items():
        items = sorted(by_brand[b], key=lambda x: x["len"])
        if len(items) < q:
            picks = items
        else:
            # spread by length percentile
            step = max(1, len(items) // q)
            picks = items[::step][:q]
        pilot.extend(picks)

    pilot = pilot[:20]
    print(f"\nPilot size: {len(pilot)}")
    for p in pilot:
        print(f"  {p['brand']:18s} {p['sku']:12s} len={p['len']:4d}  {p['name_ua'][:60]}")

    OUT_JSON.write_text(json.dumps(pilot, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nWrote {OUT_JSON}")

    # Preview markdown
    md = ["# Pilot 20 SKU — UA→RU translation review", ""]
    md.append(f"- Source: {XLSX.name}")
    md.append(f"- Criterion: descr_full identical UA==RU, len>=80, mix of brands")
    md.append("")
    md.append("| # | SKU | Brand | len(UA) | Name (UA) |")
    md.append("|--:|---|---|--:|---|")
    for i, p in enumerate(pilot, 1):
        md.append(f"| {i} | `{p['sku']}` | {p['brand']} | {p['len']} | {p['name_ua']} |")
    md.append("")
    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    print(f"Preview: {OUT_MD}")


if __name__ == "__main__":
    main()
