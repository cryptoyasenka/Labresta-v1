#!/usr/bin/env python3
# Phase A — Damage assessment
# Read-only. Compares PRE-INCIDENT (20.05) vs LIVE-NOW (21.05) for the
# 943 SKUs that broken import touched, plus 4 residual SKUs.
#
# Per (SKU, col) cell, classifies:
#   KEPT          PRE == LIVE (both non-empty or both empty)        — no damage
#   WIPED         PRE non-empty, LIVE empty                          — DAMAGED, not recovered
#   CHANGED-OK    PRE non-empty, LIVE non-empty, differ              — value moved (recovery applied or other edit)
#   APPEARED      PRE empty, LIVE non-empty                          — new content arrived (recovery / chunks)
#
# Output: .planning/STATE-AUDIT/PHASE-A-DAMAGE.md
# DOES NOT MODIFY ANY XLSX. DOES NOT WRITE TO HOROSHOP.

import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from pathlib import Path
import openpyxl
from collections import defaultdict, Counter

ROOT = Path(r'C:\Projects\labresta-sync')
PRE_FILE  = ROOT / 'horoshop-export 20.05.26.xlsx'
LIVE_FILE = ROOT / 'horoshop-export 21.05.26.xlsx'
BROKEN_FILE = ROOT / 'horoshop-import-2026-05-20.xlsx'
OUT_DIR = ROOT / '.planning' / 'STATE-AUDIT'
OUT_FILE = OUT_DIR / 'PHASE-A-DAMAGE.md'

# Content cols that broken import touched
CONTENT_COLS = [
    'Название (UA)', 'Название (RU)',
    'Название модификации (UA)', 'Название модификации (RU)',
    'META keywords (UA)', 'META keywords (RU)',
    'Описание товара (UA)', 'Описание товара (RU)',
]

# Residual recovery SKUs (Track #2 — desc only)
TRACK2_SKUS = ['2110282234', '1582804831', '2062006550']  # GoodFood, BECKERS, TATRA
# Track #1 mod_name recovery (17 SKUs); add SIRMAN
TRACK1_KNOWN = ['1766968161']  # SIRMAN — others extracted from horoshop-fix-mod-name-2026-05-21-b.xlsx if present

def norm(v):
    """Normalize cell value for comparison: empty/None → '', strip whitespace."""
    if v is None:
        return ''
    s = str(v).strip()
    return s

def load_xlsx_by_art(path, cols_subset=None):
    """Load xlsx → {art: {col: value}}. cols_subset filters columns."""
    wb = openpyxl.load_workbook(path, data_only=True, read_only=True)
    ws = wb.active
    rows = ws.iter_rows(values_only=True)
    hdr = list(next(rows))
    col_idx = {h: i for i, h in enumerate(hdr) if h}
    by_art = {}
    art_idx = col_idx.get('Артикул')
    if art_idx is None:
        raise SystemExit(f'No Артикул col in {path}')
    use_cols = cols_subset if cols_subset else list(col_idx.keys())
    for row in rows:
        if row[art_idx] is None:
            continue
        art = norm(row[art_idx])
        if not art:
            continue
        rec = {}
        for c in use_cols:
            if c in col_idx:
                rec[c] = norm(row[col_idx[c]])
        by_art[art] = rec
    wb.close()
    return by_art, hdr

def main():
    print(f'Loading PRE-INCIDENT: {PRE_FILE.name}')
    pre, _ = load_xlsx_by_art(PRE_FILE, ['Артикул'] + CONTENT_COLS)
    print(f'  → {len(pre)} SKUs')

    print(f'Loading LIVE-NOW: {LIVE_FILE.name}')
    live, _ = load_xlsx_by_art(LIVE_FILE, ['Артикул'] + CONTENT_COLS)
    print(f'  → {len(live)} SKUs')

    print(f'Loading BROKEN import scope: {BROKEN_FILE.name}')
    broken, _ = load_xlsx_by_art(BROKEN_FILE, ['Артикул'] + CONTENT_COLS)
    print(f'  → {len(broken)} SKUs (scope for audit)')

    scope = set(broken.keys()) | set(TRACK2_SKUS) | set(TRACK1_KNOWN)
    print(f'Total audit scope: {len(scope)} SKUs')

    # Sanity: which scope SKUs missing from LIVE?
    missing_live = [s for s in scope if s not in live]
    missing_pre  = [s for s in scope if s not in pre]
    print(f'Scope SKUs missing from LIVE: {len(missing_live)}')
    print(f'Scope SKUs missing from PRE:  {len(missing_pre)}')

    # Per-cell classification
    counters = Counter()          # flag → count
    per_col = defaultdict(Counter)  # col → flag → count
    per_sku_flags = defaultdict(list)  # sku → [(col, flag)]
    sample_wiped_by_col = defaultdict(list)  # col → [(sku, pre_value_excerpt)]
    sample_appeared_by_col = defaultdict(list)
    sample_changed_by_col = defaultdict(list)

    for sku in sorted(scope):
        if sku not in pre or sku not in live:
            continue  # handled in missing report
        pre_rec, live_rec = pre[sku], live[sku]
        for col in CONTENT_COLS:
            pv = pre_rec.get(col, '')
            lv = live_rec.get(col, '')
            if pv == lv:
                flag = 'KEPT' if pv else 'KEPT-EMPTY'
            elif pv and not lv:
                flag = 'WIPED'
                if len(sample_wiped_by_col[col]) < 5:
                    sample_wiped_by_col[col].append((sku, pv[:120]))
            elif not pv and lv:
                flag = 'APPEARED'
                if len(sample_appeared_by_col[col]) < 5:
                    sample_appeared_by_col[col].append((sku, lv[:120]))
            else:
                flag = 'CHANGED-OK'
                if len(sample_changed_by_col[col]) < 5:
                    sample_changed_by_col[col].append((sku, pv[:80], lv[:80]))
            counters[flag] += 1
            per_col[col][flag] += 1
            if flag in ('WIPED','CHANGED-OK','APPEARED'):
                per_sku_flags[sku].append((col, flag))

    # Identify pure-WIPED SKUs (have WIPED but no recovery)
    wiped_skus = [s for s, fs in per_sku_flags.items() if any(f=='WIPED' for c,f in fs)]
    fully_recovered = [s for s, fs in per_sku_flags.items() if all(f!='WIPED' for c,f in fs) and any(f in ('CHANGED-OK','APPEARED') for c,f in fs)]

    # Write report
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    L = []
    L.append('# PHASE A — Damage assessment (read-only)\n')
    L.append(f'**Generated:** Phase A of state audit per `.planning/STATE-AUDIT-PLAN.md`\n')
    L.append(f'**Inputs:**\n')
    L.append(f'- PRE-INCIDENT: `{PRE_FILE.name}` ({len(pre)} SKUs)\n')
    L.append(f'- LIVE-NOW: `{LIVE_FILE.name}` ({len(live)} SKUs)\n')
    L.append(f'- Broken import (scope): `{BROKEN_FILE.name}` ({len(broken)} SKUs)\n')
    L.append(f'- Track #2 residual SKUs: {TRACK2_SKUS}\n')
    L.append(f'- Track #1 known SKU: {TRACK1_KNOWN}\n')
    L.append(f'\n**Total audit scope:** {len(scope)} SKUs × {len(CONTENT_COLS)} content columns = {len(scope)*len(CONTENT_COLS)} cells\n')

    L.append('\n## Top-level damage summary (cell counts)\n')
    L.append('| Flag | Count | % |\n|---|---:|---:|\n')
    total = sum(counters.values())
    for f in ['KEPT','KEPT-EMPTY','CHANGED-OK','APPEARED','WIPED']:
        n = counters[f]
        L.append(f'| {f} | {n} | {n/total*100:.1f}% |\n')
    L.append(f'| **TOTAL** | {total} | 100.0% |\n')

    L.append('\n### Reading the flags\n')
    L.append('- **KEPT** — PRE non-empty, LIVE same value (cell never broke / fully recovered to original)\n')
    L.append('- **KEPT-EMPTY** — PRE empty, LIVE empty (never had content)\n')
    L.append('- **CHANGED-OK** — PRE non-empty, LIVE non-empty, different value (translation applied or content updated)\n')
    L.append('- **APPEARED** — PRE empty, LIVE non-empty (new content arrived)\n')
    L.append('- **WIPED** — PRE non-empty, LIVE EMPTY (broken import damage, NOT recovered)\n')

    L.append('\n## Per-column damage breakdown\n')
    L.append('| Column | KEPT | KEPT-EMPTY | CHANGED-OK | APPEARED | WIPED |\n')
    L.append('|---|---:|---:|---:|---:|---:|\n')
    for col in CONTENT_COLS:
        c = per_col[col]
        L.append(f'| {col} | {c["KEPT"]} | {c["KEPT-EMPTY"]} | {c["CHANGED-OK"]} | {c["APPEARED"]} | **{c["WIPED"]}** |\n')

    L.append(f'\n## Per-SKU rollup\n')
    L.append(f'- SKUs with ≥1 WIPED cell (NOT fully recovered): **{len(wiped_skus)}**\n')
    L.append(f'- SKUs with content changes (CHANGED-OK or APPEARED) but no WIPED: **{len(fully_recovered)}**\n')
    L.append(f'- SKUs with no changes vs PRE: **{len(scope) - len(wiped_skus) - len(fully_recovered) - len(missing_live)}**\n')

    if missing_live:
        L.append(f'\n### SKUs missing from LIVE export ({len(missing_live)})\n')
        for s in missing_live[:30]:
            L.append(f'- `{s}`\n')
        if len(missing_live) > 30:
            L.append(f'- ... and {len(missing_live)-30} more\n')

    L.append('\n## Samples — WIPED cells (per column, first 5 each)\n')
    for col in CONTENT_COLS:
        samples = sample_wiped_by_col[col]
        if not samples:
            L.append(f'\n### {col} — no WIPED ✅\n')
            continue
        L.append(f'\n### {col} — {per_col[col]["WIPED"]} WIPED cells\n')
        for sku, pv in samples:
            L.append(f'- `{sku}` — PRE: `{pv}`\n')

    L.append('\n## Samples — CHANGED-OK cells (per column, first 5 each)\n')
    for col in CONTENT_COLS:
        samples = sample_changed_by_col[col]
        if not samples:
            continue
        L.append(f'\n### {col} — {per_col[col]["CHANGED-OK"]} CHANGED-OK cells\n')
        for sku, pv, lv in samples:
            L.append(f'- `{sku}`\n  - PRE:  `{pv}`\n  - LIVE: `{lv}`\n')

    L.append('\n## All WIPED SKUs (for manual recovery planning)\n')
    if wiped_skus:
        L.append(f'\nTotal: {len(wiped_skus)} SKUs with at least one WIPED cell. Per-SKU detail:\n\n')
        for sku in sorted(wiped_skus)[:200]:
            cols = [c for c,f in per_sku_flags[sku] if f=='WIPED']
            L.append(f'- `{sku}` — WIPED cols: {cols}\n')
        if len(wiped_skus) > 200:
            L.append(f'\n... and {len(wiped_skus)-200} more (see classified data for full list)\n')
    else:
        L.append('None — no WIPED cells anywhere in scope. ✅\n')

    OUT_FILE.write_text(''.join(L), encoding='utf-8')
    print(f'\n✅ Report written: {OUT_FILE}')
    print(f'\n=== Top-level ===')
    for f in ['KEPT','KEPT-EMPTY','CHANGED-OK','APPEARED','WIPED']:
        print(f'  {f:14s}: {counters[f]:6d}')
    print(f'\nWIPED SKUs (≥1 cell): {len(wiped_skus)}')
    print(f'Recovered SKUs (CHANGED-OK/APPEARED, no WIPED): {len(fully_recovered)}')

if __name__ == '__main__':
    main()
