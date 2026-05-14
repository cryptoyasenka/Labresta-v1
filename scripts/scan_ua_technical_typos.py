"""
Scan UA-language fields in horoshop-export 13.05.26.xlsx for technical
typo patterns that survive copy-translation:

- numeric value + wrong unit (Ст вместо Вт, кв вместо кВт, etc.)
- broken Cyrillic+Latin mixes (°З вместо °C, оС вместо °C)
- garbled abbreviations (потужність с цифрой и не-Вт единицей)

Read-only. Outputs:
- .planning/translation-audit/ua-typos.md  (counts + examples)
- .planning/translation-audit/ua-typos.csv (per-occurrence rows)
"""
from __future__ import annotations

import csv
import re
import sys
from collections import Counter, defaultdict
from html import unescape
from pathlib import Path

import openpyxl

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
XLSX = ROOT / "horoshop-export 13.05.26.xlsx"
OUT_DIR = ROOT / ".planning" / "translation-audit"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_MD = OUT_DIR / "ua-typos.md"
OUT_CSV = OUT_DIR / "ua-typos.csv"

UA_COLS = [
    ("name", "Название (UA)"),
    ("mod_name", "Название модификации (UA)"),
    ("html_title", "HTML title (UA)"),
    ("meta_keys", "META keywords (UA)"),
    ("meta_desc", "META description (UA)"),
    ("h1", "h1 заголовок (UA)"),
    ("descr_full", "Описание товара (UA)"),
    ("descr_short", "Короткое описание (UA)"),
    ("promo", "Текст акции (UA)"),
    ("marketplace", "Описание для маркетплейсов (UA)"),
]

# Patterns of suspected typos.
# Each entry: (code, regex, human description, sample-extract group index)
PATTERNS = [
    # "5,0 Ст" / "1500 Ст" — Ст ≠ Вт (Ст = століття in Ukrainian)
    ("digit_ST",
     re.compile(r"(\d+[,.]?\d*)\s*Ст\b"),
     "Число + 'Ст' — почти всегда должно быть 'Вт' (Watt)"),

    # "Потужність: ... Ст" anywhere in 30 chars after слово
    ("potuzhnist_ST",
     re.compile(r"[Пп]отужн[іі]сть[^\n]{1,40}\bСт\b"),
     "После 'потужність' встречается 'Ст' (должно быть Вт/кВт)"),

    # "°З" вместо "°C" — кирилличная З вместо латинской C
    ("celsius_Z",
     re.compile(r"°\s*[ЗЭз]"),
     "°З или °Э — кирилличная буква вместо латинской C"),

    # "оС" / "о С" — текстовая запись °C
    ("celsius_text_oC",
     re.compile(r"\b\d+[,.]?\d*\s*оС\b"),
     "'оС' как 'градусы Цельсия' — нестандартная запись (надо °C)"),

    # "Кв" в смысле кВт — нестандартное сокращение
    ("kv_instead_kvt",
     re.compile(r"(\d+[,.]?\d*)\s*[Кк]в\b(?!т|\.)"),
     "Число + 'Кв' — вероятно должно быть 'кВт'"),

    # "Напруга: ... В" должно быть, но иногда '8' латинское B
    ("voltage_latin_B",
     re.compile(r"\b\d+\s*B\b"),
     "Число + латинская 'B' — должно быть кириллической 'В'"),

    # Latin 'C' in middle of Cyrillic word (OCR artifact)
    ("latin_C_in_cyr",
     re.compile(r"[а-яіїєґ]C[а-яіїєґ]"),
     "Латинская 'C' внутри кирилличного слова (OCR-артефакт)"),

    # "Гц" misspelled as "Гд" / "Гч"
    ("Hz_typo",
     re.compile(r"\b(\d+[,.]?\d*)\s*Г[дч]\b"),
     "Число + 'Гд'/'Гч' — должно быть 'Гц'"),

    # "кВт год" должно быть "кВт·год" or "кВт ч"
    # Skipped — too noisy.

    # Russian function words inside UA text: "что", "или", "также"
    ("ru_func_word",
     re.compile(r"\b(что|или|также|если|только|чтобы|потому что)\b"),
     "Русское служебное слово в UA-тексте"),

    # "В" одиночное after digit with дюйми/inches confusion — too noisy, skip.

    # Doubled letters from autocorrect: "пллита", "індукцційна"
    ("triple_letter",
     re.compile(r"([а-яіїєґА-ЯІЇЄҐ])\1\1"),
     "Утроенная буква подряд (опечатка)"),
]


def strip_html(s: str) -> str:
    if not s:
        return ""
    s = re.sub(r"<[^>]+>", " ", s)
    s = unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def excerpt(text: str, match: re.Match, pad: int = 40) -> str:
    s, e = match.start(), match.end()
    return text[max(0, s - pad):min(len(text), e + pad)].replace("\n", " ")


def main():
    print(f"Loading {XLSX.name}...")
    wb = openpyxl.load_workbook(str(XLSX), read_only=True, data_only=True)
    ws = wb.active
    rows = ws.iter_rows(values_only=True)
    headers = list(next(rows))
    col_idx = {h: i for i, h in enumerate(headers) if h}
    sku_col = col_idx["Артикул"]
    display_col = col_idx.get("Отображать")

    pairs = []
    for name, hdr in UA_COLS:
        i = col_idx.get(hdr)
        if i is None:
            print(f"  ! missing column: {hdr}")
            continue
        pairs.append((name, i))

    findings = defaultdict(list)  # code -> list of {sku, field, excerpt, full_match}
    stats = Counter()

    total = 0
    for row in rows:
        if row is None:
            continue
        total += 1
        sku = row[sku_col]
        display = row[display_col] if display_col is not None else ""

        for name, i in pairs:
            raw = row[i] or ""
            if not isinstance(raw, str):
                raw = str(raw)
            text = strip_html(raw) if name in ("descr_full", "descr_short") else raw

            for code, regex, desc in PATTERNS:
                for m in regex.finditer(text):
                    stats[f"{code}:{name}"] += 1
                    findings[code].append({
                        "sku": sku,
                        "field": name,
                        "display": display,
                        "match": m.group(0),
                        "excerpt": excerpt(text, m),
                    })

    print(f"Rows: {total}")

    # CSV with all occurrences
    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["code", "sku", "field", "display", "match", "excerpt"])
        for code, items in findings.items():
            for it in items:
                w.writerow([code, it["sku"], it["field"], it["display"],
                            it["match"], it["excerpt"]])

    # MD report
    lines = [f"# UA technical typo scan — {XLSX.name}", ""]
    lines.append(f"- Rows scanned: {total}")
    lines.append(f"- UA columns: {len(pairs)}")
    lines.append("")
    lines.append("## Counts (pattern × field)")
    lines.append("")
    lines.append("| pattern | field | hits | description |")
    lines.append("|---|---|---:|---|")
    code_to_desc = {c: d for c, _, d in PATTERNS}
    for code, _, desc in PATTERNS:
        per_field = Counter()
        for it in findings.get(code, []):
            per_field[it["field"]] += 1
        if not per_field:
            lines.append(f"| `{code}` | — | 0 | {desc} |")
            continue
        for field, n in sorted(per_field.items(), key=lambda x: -x[1]):
            lines.append(f"| `{code}` | {field} | {n} | {desc} |")
    lines.append("")
    lines.append("## Totals per pattern")
    lines.append("")
    lines.append("| pattern | hits |")
    lines.append("|---|---:|")
    totals = Counter()
    for code, items in findings.items():
        totals[code] = len(items)
    for code, _, _ in PATTERNS:
        lines.append(f"| `{code}` | {totals.get(code, 0)} |")
    lines.append("")
    lines.append("## Samples (first 10 per pattern)")
    lines.append("")
    for code, _, desc in PATTERNS:
        items = findings.get(code, [])
        if not items:
            continue
        lines.append(f"### `{code}` — {len(items)} hits — {desc}")
        lines.append("")
        seen_sku = set()
        shown = 0
        for it in items:
            if it["sku"] in seen_sku:
                continue
            seen_sku.add(it["sku"])
            lines.append(f"- `{it['sku']}` · `{it['field']}` · match=`{it['match']}` · …{it['excerpt']}…")
            shown += 1
            if shown >= 10:
                break
        lines.append("")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"Report: {OUT_MD}")
    print(f"CSV:    {OUT_CSV}")


if __name__ == "__main__":
    main()
