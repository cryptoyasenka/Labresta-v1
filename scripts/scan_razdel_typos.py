"""
Sanity scan over `Раздел` (col 8) for obvious typos.

Checks:
- latin letters mixed inside Cyrillic word (a/o/e/c/p/y/x confusables)
- triple-letter sequences (likely autocorrect artifacts)
- duplicate categories differing only in case / whitespace / punctuation
- empty path segments (// or trailing /)
- mixed UA/RU letters in same word (suspicious)

Output: .planning/translation-audit/category-typos.md
Read-only. Suggests fixes for Horoshop CMS, does not modify data.
"""
from __future__ import annotations
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import openpyxl

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
XLSX = ROOT / "horoshop-export 13.05.26.xlsx"
OUT = ROOT / ".planning" / "translation-audit" / "category-typos.md"

LATIN_CONFUSABLES = set("aopecpyxABCEHKMOPTXaopecyx")
UA_ONLY = set("іїєґІЇЄҐ")
RU_ONLY = set("ыъэЫЪЭёЁ")


def has_latin_inside_cyrillic(word: str) -> bool:
    cyr = any('Ѐ' <= c <= 'ӿ' for c in word)
    lat = any(c in LATIN_CONFUSABLES for c in word)
    return cyr and lat


def find_issues(category: str) -> list[str]:
    issues = []
    if "//" in category:
        issues.append("double slash")
    if category != category.strip():
        issues.append("leading/trailing whitespace")
    if category.endswith("/") or category.startswith("/"):
        issues.append("path edge slash")
    if "  " in category:
        issues.append("double space")
    if re.search(r"([а-яА-ЯіїєґІЇЄҐ])\1{2,}", category):
        issues.append("triple letter")
    for word in re.findall(r"[\w']+", category):
        if has_latin_inside_cyrillic(word):
            issues.append(f"latin-in-cyrillic word: {word!r}")
        ua = set(word) & UA_ONLY
        ru = set(word) & RU_ONLY
        if ua and ru:
            issues.append(f"mixed UA+RU letters: {word!r}")
    return issues


def main():
    wb = openpyxl.load_workbook(str(XLSX), read_only=True, data_only=True)
    ws = wb.active
    rows = ws.iter_rows(values_only=True)
    headers = list(next(rows))
    col = {h: i for i, h in enumerate(headers) if h}

    counter: Counter = Counter()
    for row in rows:
        if row is None:
            continue
        v = row[col["Раздел"]]
        if v is None:
            continue
        counter[str(v).strip()] += 1

    md = ["# Category typos audit — `Раздел` (col 8)", ""]
    md.append(f"- Total unique categories: **{len(counter)}**")
    md.append(f"- Total products: **{sum(counter.values())}**")
    md.append(f"- Source: `{XLSX.name}`")
    md.append("")
    md.append("## How to use this report")
    md.append("")
    md.append("Yana — категории правятся в **Horoshop CMS** (админка → Каталог → Разделы), не через XLSX.")
    md.append("Любое переименование категории в админке автоматически перемещает все товары.")
    md.append("")
    md.append("---")
    md.append("")

    # 1. Per-category issues
    issues_found = []
    for cat, cnt in counter.most_common():
        problems = find_issues(cat)
        if problems:
            issues_found.append((cat, cnt, problems))

    md.append(f"## Per-category issues ({len(issues_found)})")
    md.append("")
    if not issues_found:
        md.append("_None found — категории чистые с точки зрения механических опечаток._")
    else:
        md.append("| Category | Products | Issues |")
        md.append("|---|--:|---|")
        for cat, cnt, problems in issues_found:
            md.append(f"| `{cat}` | {cnt} | {'; '.join(problems)} |")
    md.append("")

    # 2. Near-duplicate categories (case-insensitive or whitespace-different)
    norm_to_cats: dict[str, list[str]] = defaultdict(list)
    for cat in counter:
        norm = re.sub(r"\s+", " ", cat.lower().strip())
        norm_to_cats[norm].append(cat)

    near_dups = [(norm, cats) for norm, cats in norm_to_cats.items() if len(cats) > 1]
    md.append(f"## Near-duplicate categories ({len(near_dups)})")
    md.append("")
    md.append("Категории отличающиеся только регистром / пробелами / пунктуацией.")
    md.append("")
    if not near_dups:
        md.append("_None found._")
    else:
        md.append("| Normalized | Variants | Counts |")
        md.append("|---|---|---|")
        for norm, cats in near_dups:
            variants = " / ".join(f"`{c}`" for c in cats)
            counts = " + ".join(str(counter[c]) for c in cats)
            md.append(f"| `{norm}` | {variants} | {counts} |")
    md.append("")

    # 3. Path depth distribution (sanity check)
    depth_counter = Counter()
    for cat in counter:
        depth = cat.count("/") + 1
        depth_counter[depth] += counter[cat]

    md.append("## Path depth distribution")
    md.append("")
    md.append("| Levels | Product count |")
    md.append("|--:|--:|")
    for d, cnt in sorted(depth_counter.items()):
        md.append(f"| {d} | {cnt} |")
    md.append("")

    # 4. Top-level segments (1st part of path)
    top_level = Counter()
    for cat, cnt in counter.items():
        top = cat.split("/")[0].strip()
        top_level[top] += cnt

    md.append("## Top-level segments")
    md.append("")
    md.append("| Top-level | Total products |")
    md.append("|---|--:|")
    for top, cnt in top_level.most_common():
        md.append(f"| `{top}` | {cnt} |")
    md.append("")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(md), encoding="utf-8")
    print(f"Wrote {OUT}")
    print()
    print(f"Issues found: {len(issues_found)}")
    print(f"Near-duplicates: {len(near_dups)}")
    print(f"Top-level segments: {len(top_level)}")
    print(f"Path depth: {dict(sorted(depth_counter.items()))}")


if __name__ == "__main__":
    main()
