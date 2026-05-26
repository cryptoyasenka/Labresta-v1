"""Quick preview of a chunk JSON — print 1-line summary per SKU."""
from __future__ import annotations
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
CHUNKS_DIR = ROOT / ".planning" / "translation-audit" / "chunks"


def main(n: int, start: int = 1, count: int = 0):
    p = CHUNKS_DIR / f"chunk-{n:03d}.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    end = start + count if count else len(data) + 1
    for x in data:
        if not (start <= x["n"] < end):
            continue
        nm = x.get("Название (UA)") or x.get("Название (RU)") or ""
        nm = nm[:70]
        print(f'  {x["n"]:2d} | {x.get("артикул"):>14} | {x.get("бренд") or "-":12s} | {nm}')


if __name__ == "__main__":
    n = int(sys.argv[1])
    start = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    count = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    main(n, start, count)
