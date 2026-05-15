"""Dump ALL operator fields for a SKU range of a chunk to a UTF-8 scratch file.

Usage: python scripts/_dump_batch.py 009 1 8   # chunk-009, SKU n in [1..8]
Reads chunk-NNN.json (keyed by field NAME, robust to per-SKU missing fields).
Writes .planning/scratch_skubatch.txt (UTF-8) — Read that, never stdout.
"""
import io
import json
import sys

chunk = sys.argv[1]
lo = int(sys.argv[2])
hi = int(sys.argv[3])

d = json.load(io.open(f".planning/translation-audit/chunks/chunk-{chunk}.json", encoding="utf-8"))

FIELD_ORDER = [
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

out = []
for r in d:
    n = r.get("n")
    if not (lo <= n <= hi):
        continue
    art = r.get("артикул")
    brand = r.get("бренд")
    out.append(f"\n{'='*78}\n===== SKU {n}  |  Артикул {art}  |  {brand} =====\n{'='*78}")
    for f in FIELD_ORDER:
        if f in r and r[f] not in (None, ""):
            out.append(f"\n--- {f} ---")
            out.append(str(r[f]))
io.open(".planning/scratch_skubatch.txt", "w", encoding="utf-8").write("\n".join(out))
n_sku = len([r for r in d if lo <= r.get("n", -1) <= hi])
print(f"wrote {n_sku} SKU ({lo}-{hi}) of chunk-{chunk} to .planning/scratch_skubatch.txt")
