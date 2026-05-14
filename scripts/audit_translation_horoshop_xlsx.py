"""
Translation audit for Horoshop XLSX export.

Reads `horoshop-export 13.05.26.xlsx` and flags rows where UA/RU text fields
look broken: missing translation, identical text in both languages, wrong-
language tokens (Russian-only letters in UA column / Ukrainian-only letters
in RU column), HTML tag mismatches, etc.

Read-only. Writes a markdown report to `.planning/translation-audit.md` and
companion CSVs in `.planning/translation-audit/`.
"""
from __future__ import annotations

import csv
import io
import os
import re
import sys
from collections import Counter, defaultdict
from html import unescape
from pathlib import Path

import openpyxl

# --- config ---------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent
XLSX = ROOT / "horoshop-export 13.05.26.xlsx"
OUT_DIR = ROOT / ".planning" / "translation-audit"
OUT_REPORT = ROOT / ".planning" / "translation-audit.md"

# Force UTF-8 stdout for human-readable progress
sys.stdout.reconfigure(encoding="utf-8")

# Paired UA/RU columns from the Horoshop export header.
# (canonical name, UA header, RU header)
PAIRS = [
    ("name",         "Название (UA)",                  "Название (RU)"),
    ("mod_name",     "Название модификации (UA)",      "Название модификации (RU)"),
    ("html_title",   "HTML title (UA)",                "HTML title (RU)"),
    ("meta_keys",    "META keywords (UA)",             "META keywords (RU)"),
    ("meta_desc",    "META description (UA)",          "META description (RU)"),
    ("h1",           "h1 заголовок (UA)",              "h1 заголовок (RU)"),
    ("descr_full",   "Описание товара (UA)",           "Описание товара (RU)"),
    ("descr_short",  "Короткое описание (UA)",         "Короткое описание (RU)"),
    ("promo",        "Текст акции (UA)",               "Текст акции (RU)"),
    ("marketplace",  "Описание для маркетплейсов (UA)", "Описание для маркетплейсов (RU)"),
]

# Letters present in Ukrainian but NOT in Russian alphabet
UA_ONLY_LETTERS = set("іїєґІЇЄҐ")
# Letters present in Russian but NOT in Ukrainian alphabet
RU_ONLY_LETTERS = set("ыъэЫЪЭёЁ")

# Tokens that look Russian: ending in -ый/-ий/-ой/-ая/-ое/-ого/-ому/-ыми
RU_SUFFIX_RE = re.compile(r"\b\w+(ый|ой|ая|ое|ого|ому|ыми|ыми|ться|ться)\b", re.IGNORECASE)
# Ukrainian-only frequent function words
UA_WORDS = {"та", "що", "як", "для", "із", "або", "цей", "ця", "це", "ці",
            "є", "ось", "є", "не", "вже", "тільки", "лише"}
RU_WORDS = {"и", "что", "как", "для", "из", "или", "этот", "эта", "это", "эти",
            "есть", "вот", "уже", "только", "лишь", "также"}

TAG_RE = re.compile(r"<([a-zA-Z][a-zA-Z0-9]*)\b[^>]*>")


def strip_html(s: str) -> str:
    if not s:
        return ""
    s = re.sub(r"<[^>]+>", " ", s)
    s = unescape(s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def tag_counter(s: str) -> Counter:
    return Counter(m.group(1).lower() for m in TAG_RE.finditer(s or ""))


def has_ua_only(s: str) -> bool:
    return any(c in UA_ONLY_LETTERS for c in s)


def has_ru_only(s: str) -> bool:
    return any(c in RU_ONLY_LETTERS for c in s)


def cyrillic_ratio(s: str) -> float:
    cyr = sum(1 for c in s if "Ѐ" <= c <= "ӿ")
    return cyr / max(len(s), 1)


def looks_empty(s: str) -> bool:
    return not s or not s.strip()


# --- main -----------------------------------------------------------------

def main():
    print(f"Loading {XLSX.name} ...")
    wb = openpyxl.load_workbook(str(XLSX), read_only=True, data_only=True)
    ws = wb.active

    rows = ws.iter_rows(values_only=True)
    headers = list(next(rows))
    print(f"Columns: {len(headers)}")

    # Locate columns
    col_idx = {h: i for i, h in enumerate(headers) if h}
    sku_col = col_idx.get("Артикул")
    url_col = None
    for h, i in col_idx.items():
        if "url" in str(h).lower() or "ссылка" in str(h).lower() or "посилання" in str(h).lower():
            url_col = i
            break

    pair_idx = []
    for name, ua_h, ru_h in PAIRS:
        ua_i = col_idx.get(ua_h)
        ru_i = col_idx.get(ru_h)
        if ua_i is None or ru_i is None:
            print(f"  ! pair {name}: missing column (UA={ua_i}, RU={ru_i})")
            continue
        pair_idx.append((name, ua_i, ru_i))

    print(f"Paired columns found: {len(pair_idx)} of {len(PAIRS)}")

    # Issue buckets
    issues = defaultdict(list)  # issue_code -> [{sku, field, ua, ru, note}]
    stats = Counter()

    total = 0
    for r_i, row in enumerate(rows, start=2):
        if row is None:
            continue
        total += 1
        sku = row[sku_col] if sku_col is not None else ""
        url = row[url_col] if url_col is not None else ""

        for name, ua_i, ru_i in pair_idx:
            ua = (row[ua_i] or "")
            ru = (row[ru_i] or "")
            if not isinstance(ua, str):
                ua = str(ua)
            if not isinstance(ru, str):
                ru = str(ru)

            ua_txt = strip_html(ua) if name in ("descr_short", "descr_full") else ua.strip()
            ru_txt = strip_html(ru) if name in ("descr_short", "descr_full") else ru.strip()

            ua_empty = looks_empty(ua_txt)
            ru_empty = looks_empty(ru_txt)

            # 1. one side empty, other not
            if ua_empty and not ru_empty:
                stats[f"{name}:missing_UA"] += 1
                issues["missing_UA"].append((sku, name, "", ru_txt[:200], url))
                continue
            if ru_empty and not ua_empty:
                stats[f"{name}:missing_RU"] += 1
                issues["missing_RU"].append((sku, name, ua_txt[:200], "", url))
                continue
            if ua_empty and ru_empty:
                continue

            # 2. identical text in both columns (likely missed translation)
            if ua_txt == ru_txt and len(ua_txt) > 3:
                # ignore brand/SKU-only lines
                if cyrillic_ratio(ua_txt) > 0.3:
                    stats[f"{name}:identical"] += 1
                    issues["identical_ua_ru"].append(
                        (sku, name, ua_txt[:200], ru_txt[:200], url)
                    )

            # 3. wrong-language letters
            if has_ru_only(ua_txt):
                stats[f"{name}:ru_letters_in_UA"] += 1
                # extract offending tokens
                bad = [w for w in re.findall(r"\b\w+\b", ua_txt) if has_ru_only(w)]
                issues["ru_letters_in_UA"].append(
                    (sku, name, ua_txt[:200], ", ".join(bad[:10]), url)
                )
            if has_ua_only(ru_txt):
                stats[f"{name}:ua_letters_in_RU"] += 1
                bad = [w for w in re.findall(r"\b\w+\b", ru_txt) if has_ua_only(w)]
                issues["ua_letters_in_RU"].append(
                    (sku, name, ru_txt[:200], ", ".join(bad[:10]), url)
                )

            # 4. HTML tag-shape mismatch in long descriptions
            if name in ("descr_short", "descr_full"):
                t_ua = tag_counter(ua)
                t_ru = tag_counter(ru)
                if t_ua != t_ru:
                    diff = []
                    keys = set(t_ua) | set(t_ru)
                    for k in sorted(keys):
                        a, b = t_ua.get(k, 0), t_ru.get(k, 0)
                        if a != b:
                            diff.append(f"{k}: UA={a}/RU={b}")
                    stats[f"{name}:tag_mismatch"] += 1
                    issues["html_tag_mismatch"].append(
                        (sku, name, "; ".join(diff[:8]),
                         f"len(UA)={len(ua_txt)} len(RU)={len(ru_txt)}", url)
                    )

            # 5. length asymmetry — translation likely truncated/missing chunks
            if name in ("descr_full", "descr_short", "meta_desc"):
                la, lb = len(ua_txt), len(ru_txt)
                if la > 50 and lb > 50:
                    ratio = max(la, lb) / max(min(la, lb), 1)
                    if ratio >= 2.0:
                        stats[f"{name}:length_skew"] += 1
                        issues["length_skew_2x"].append(
                            (sku, name, f"UA={la}", f"RU={lb}", url)
                        )

    print(f"Rows processed: {total}")

    # --- emit CSVs ---
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for code, rows_list in issues.items():
        path = OUT_DIR / f"{code}.csv"
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f)
            w.writerow(["sku", "field", "ua_or_diff", "ru_or_bad", "url"])
            for r in rows_list:
                w.writerow(r)
        print(f"  {code}: {len(rows_list)} rows -> {path.name}")

    # --- markdown report ---
    lines = []
    lines.append(f"# Translation audit — {XLSX.name}")
    lines.append("")
    lines.append(f"- Rows: {total}")
    lines.append(f"- Paired UA/RU columns: {len(pair_idx)}")
    lines.append("")
    lines.append("## Issue counts (per field × kind)")
    lines.append("")
    by_kind = defaultdict(Counter)
    for key, n in stats.items():
        field, kind = key.split(":", 1)
        by_kind[kind][field] = n
    lines.append("| kind | field | count |")
    lines.append("|---|---|---:|")
    for kind in sorted(by_kind):
        for field, n in sorted(by_kind[kind].items(), key=lambda x: -x[1]):
            lines.append(f"| {kind} | {field} | {n} |")
    lines.append("")
    lines.append("## Totals by kind")
    lines.append("")
    lines.append("| kind | total |")
    lines.append("|---|---:|")
    totals_by_kind = Counter()
    for key, n in stats.items():
        _, kind = key.split(":", 1)
        totals_by_kind[kind] += n
    for kind, n in sorted(totals_by_kind.items(), key=lambda x: -x[1]):
        lines.append(f"| {kind} | {n} |")
    lines.append("")
    lines.append("## Samples")
    lines.append("")
    for code, rows_list in sorted(issues.items(), key=lambda kv: -len(kv[1])):
        lines.append(f"### {code} — {len(rows_list)} rows")
        lines.append("")
        lines.append("First 5 examples (sku · field · UA/diff · RU/bad):")
        lines.append("")
        for r in rows_list[:5]:
            sku, field, a, b, url = r
            lines.append(f"- `{sku}` · `{field}` · UA={a!r} · RU={b!r}")
        lines.append("")

    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nReport: {OUT_REPORT}")
    print(f"CSVs:   {OUT_DIR}")


if __name__ == "__main__":
    main()
