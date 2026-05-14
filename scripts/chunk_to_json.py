"""
Dump operator-owned text fields from chunk-NN.xlsx to chunk-NN.json for review.

Output: list of dicts, one per SKU. Each dict has:
- "n":          1-based position in chunk
- "артикул":    str
- "url":        product URL alias from Horoshop XLSX (col "Псевдонім URL")
- "бренд":      str
- + 10 operator UA/RU pairs (only non-empty values included to shorten output)

Usage:
  python scripts/chunk_to_json.py 002              # → chunks/chunk-002.json
  python scripts/chunk_to_json.py 002 003 004      # batch
  python scripts/chunk_to_json.py --all            # all 85 chunks
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

import openpyxl

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
CHUNKS_DIR = ROOT / ".planning" / "translation-audit" / "chunks"

OPERATOR_FIELDS = [
    "Название (UA)", "Название (RU)",
    "Название модификации (UA)", "Название модификации (RU)",
    "HTML title (UA)", "HTML title (RU)",
    "META keywords (UA)", "META keywords (RU)",
    "META description (UA)", "META description (RU)",
    "h1 заголовок (UA)", "h1 заголовок (RU)",
    "Описание товара (UA)", "Описание товара (RU)",
    "Короткое описание (UA)", "Короткое описание (RU)",
    "Текст акции (UA)", "Текст акции (RU)",
    "Описание для маркетплейсов (UA)", "Описание для маркетплейсов (RU)",
]
EXTRA_FIELDS = ["Артикул", "Бренд", "Псевдонім URL", "Раздел", "Ціна"]


def dump_chunk(n: int) -> Path:
    xlsx = CHUNKS_DIR / f"chunk-{n:03d}.xlsx"
    out = CHUNKS_DIR / f"chunk-{n:03d}.json"
    if not xlsx.exists():
        print(f"  skip chunk-{n:03d}: {xlsx} not found")
        return out
    wb = openpyxl.load_workbook(str(xlsx), read_only=True, data_only=True)
    ws = wb.active
    rows_iter = ws.iter_rows(values_only=True)
    headers = list(next(rows_iter))
    col = {h: i for i, h in enumerate(headers) if h}

    items = []
    for i, row in enumerate(rows_iter, 1):
        if row is None or row[col.get("Артикул", 0)] is None:
            continue
        item: dict = {"n": i}
        for h in EXTRA_FIELDS:
            if h in col:
                v = row[col[h]]
                if v is not None and v != "":
                    item[h.lower()] = v
        for h in OPERATOR_FIELDS:
            if h in col:
                v = row[col[h]]
                if v is not None and v != "":
                    item[h] = v
        items.append(item)

    out.write_text(
        json.dumps(items, ensure_ascii=False, indent=1),
        encoding="utf-8",
    )
    print(f"  dumped chunk-{n:03d}: {len(items)} SKU → {out.name} ({out.stat().st_size:,} bytes)")
    return out


def main(argv: list[str]):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return
    if argv[0] == "--all":
        nums = sorted(
            int(p.stem.split("-")[1])
            for p in CHUNKS_DIR.glob("chunk-*.xlsx")
            if "-fixed" not in p.stem
        )
    else:
        nums = [int(a) for a in argv]
    for n in nums:
        dump_chunk(n)


if __name__ == "__main__":
    main(sys.argv[1:])
