"""
Read-only audit of unique values in 4 borderline fields of horoshop XLSX.

Fields:
- col  8: Раздел       (categories with " / " hierarchy delimiter)
- col 38: Цвет
- col 39: Тип гарантии
- col 47: Состояние товара

Output: .planning/translation-audit/borderline-values.md
        Each section sorted by count desc, with SKU samples for spot-check.

Purpose: Yana reviews → returns approved list → we clean only orphographic/unification
issues within that list, never rename structure (risk: break Horoshop category hierarchy).
"""
from __future__ import annotations
import sys
from collections import Counter, defaultdict
from pathlib import Path

import openpyxl

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
XLSX = ROOT / "horoshop-export 13.05.26.xlsx"
OUT = ROOT / ".planning" / "translation-audit" / "borderline-values.md"

FIELDS = [
    ("Раздел", "Раздел"),
    ("Цвет", "Цвет"),
    ("Тип гарантии", "Тип гарантии"),
    ("Состояние товара", "Состояние товара"),
]


def main():
    wb = openpyxl.load_workbook(str(XLSX), read_only=True, data_only=True)
    ws = wb.active
    rows = ws.iter_rows(values_only=True)
    headers = list(next(rows))
    col = {h: i for i, h in enumerate(headers) if h}

    sku_i = col["Артикул"]
    brand_i = col["Бренд"]
    name_ua_i = col["Название (UA)"]

    field_indices = {label: col[header] for label, header in FIELDS}

    counters: dict[str, Counter] = {label: Counter() for label, _ in FIELDS}
    samples: dict[str, dict[str, list[tuple]]] = {
        label: defaultdict(list) for label, _ in FIELDS
    }

    total_rows = 0
    for row in rows:
        if row is None:
            continue
        total_rows += 1
        sku = str(row[sku_i]) if row[sku_i] is not None else ""
        brand = (row[brand_i] or "").strip() if isinstance(row[brand_i], str) else ""
        name_ua = (row[name_ua_i] or "").strip()[:60] if isinstance(row[name_ua_i], str) else ""

        for label, _ in FIELDS:
            raw = row[field_indices[label]]
            if raw is None:
                val = "<empty>"
            else:
                val = str(raw).strip()
                if not val:
                    val = "<empty>"
            counters[label][val] += 1
            if len(samples[label][val]) < 3:
                samples[label][val].append((sku, brand, name_ua))

    md = [
        "# Borderline field values audit",
        "",
        f"- Source: `{XLSX.name}`",
        f"- Total rows: {total_rows}",
        f"- Generated for Yana review (read-only)",
        "",
        "## How to use this report",
        "",
        "Yana — пройди 4 секции ниже, для каждого значения отметь одно из:",
        "- **OK** — оставить как есть",
        "- **FIX → \"новое значение\"** — есть опечатка / неточность, заменить на указанное",
        "- **MERGE → \"каноничное значение\"** — это вариант существующего значения (например \"Сріблястий\" + \"сріблястий\" → MERGE → \"Сріблястий\")",
        "- **DELETE** — значение должно быть пустым у этих SKU",
        "",
        "После review этот файл становится approved-списком: я чищу 4 поля ТОЛЬКО в его пределах,",
        "не делаю переименований структуры (риск — поломать иерархию Horoshop).",
        "",
        "---",
        "",
    ]

    for label, _ in FIELDS:
        c = counters[label]
        md.append(f"## {label}")
        md.append("")
        md.append(f"Уникальных значений: **{len(c)}**, всего непустых строк: **{sum(v for k, v in c.items() if k != '<empty>')}**, пустых: **{c.get('<empty>', 0)}**")
        md.append("")
        md.append("| # | Значение | Count | Sample SKU 1 | Sample SKU 2 | Sample SKU 3 | Yana verdict |")
        md.append("|--:|---|--:|---|---|---|---|")
        for i, (val, cnt) in enumerate(c.most_common(), 1):
            if val == "<empty>":
                continue
            s = samples[label][val]
            s_cells = []
            for j in range(3):
                if j < len(s):
                    sku, brand, name = s[j]
                    s_cells.append(f"`{sku}` {brand} {name}")
                else:
                    s_cells.append("—")
            display_val = val.replace("|", "\\|")
            md.append(f"| {i} | `{display_val}` | {cnt} | {s_cells[0]} | {s_cells[1]} | {s_cells[2]} |  |")
        md.append("")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(md), encoding="utf-8")
    print(f"Wrote {OUT}")
    print()
    for label, _ in FIELDS:
        c = counters[label]
        non_empty = sum(v for k, v in c.items() if k != "<empty>")
        empty = c.get("<empty>", 0)
        print(f"  {label}: {len(c)-1 if '<empty>' in c else len(c)} unique non-empty values, {non_empty} rows non-empty, {empty} empty")


if __name__ == "__main__":
    main()
