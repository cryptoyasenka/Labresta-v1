#!/usr/bin/env python3
# Phase B — Intended propagation audit
# Read-only. Compares INTENDED (apply chunk diffs to PRE-INCIDENT) vs LIVE-NOW.
# Tells you which translations got through the broken builder and which
# stayed only in our chunk files.
#
# Per (SKU, col) edit, classifies:
#   OK         LIVE == INTENDED                      — translation reached LIVE
#   STALE      LIVE == PRE-INCIDENT                  — edit stayed in chunk file only
#   WIPED      LIVE empty, INTENDED non-empty        — broken import wiped, never recovered
#   WRONG      LIVE != INTENDED and != PRE, non-empty — something else (manual edit / collision)
#   FAIL       PARTIAL patch failed at parse time    — can't compute INTENDED reliably
#
# Output: .planning/STATE-AUDIT/PHASE-B-PROPAGATION.md
# DOES NOT MODIFY ANY XLSX. DOES NOT WRITE TO HOROSHOP.

import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, r'C:\Projects\labresta-sync\scripts')

from pathlib import Path
import openpyxl
from collections import defaultdict, Counter

# Import builder's parser (read-only use)
import importlib.util
spec = importlib.util.spec_from_file_location(
    'builder', r'C:\Projects\labresta-sync\scripts\_build_horoshop_import.py'
)
builder = importlib.util.module_from_spec(spec)
# parse_chunk() uses relative path CHUNK_DIR — make CWD the project root before exec
os.chdir(r'C:\Projects\labresta-sync')
spec.loader.exec_module(builder)

ROOT = Path(r'C:\Projects\labresta-sync')
PRE_FILE  = ROOT / 'horoshop-export 20.05.26.xlsx'
LIVE_FILE = ROOT / 'horoshop-export 21.05.26.xlsx'
OUT_DIR = ROOT / '.planning' / 'STATE-AUDIT'
OUT_FILE = OUT_DIR / 'PHASE-B-PROPAGATION.md'

# Yana asked for 016-029. CLOSED in builder = 016-028; 029 is in_progress (~24 SKU done).
CHUNKS_TO_AUDIT = list(range(16, 30))  # 016..029

# Field name canonical mapping (handles aliases used in older diff.md)
FIELD_MAP_ALIASES = {
    'Описание (RU)': 'Описание товара (RU)',
    'Описание (UA)': 'Описание товара (UA)',
    'Назв.мод (RU)': 'Название модификации (RU)',
    'Назв.мод (UA)': 'Название модификации (UA)',
}


def norm(v):
    if v is None:
        return ''
    return str(v).strip()


def canon_field(f):
    return FIELD_MAP_ALIASES.get(f, f)


def load_xlsx_full(path):
    """Load entire xlsx → {art: {col: value}}."""
    wb = openpyxl.load_workbook(path, data_only=True, read_only=True)
    ws = wb.active
    rows = ws.iter_rows(values_only=True)
    hdr = list(next(rows))
    col_idx = {h: i for i, h in enumerate(hdr) if h}
    art_idx = col_idx.get('Артикул')
    by_art = {}
    for row in rows:
        if row[art_idx] is None:
            continue
        art = norm(row[art_idx])
        if not art:
            continue
        rec = {c: norm(row[col_idx[c]]) for c in col_idx}
        by_art[art] = rec
    wb.close()
    return by_art


def compute_intended(pre_val, edit):
    """Apply a single Edit to pre_val and return intended new value.
    Returns (intended_str_or_None, fail_reason_or_None)."""
    if edit.rtype == 'FULL':
        return edit.stale, None
    # PARTIAL: apply str.replace per fragment pair
    if not pre_val:
        return None, 'partial_on_empty_base'
    if not edit.was_frags:
        return None, 'partial_no_was'
    new_val = pre_val
    for w, s in zip(edit.was_frags, edit.stale_frags):
        w = w.strip().strip('`').strip()
        s = s.strip().strip('`').strip()
        if not w:
            continue
        if w not in new_val:
            return None, f'partial_was_not_found:{w[:50]!r}'
        new_val = new_val.replace(w, s, 1)
    return new_val, None


def main():
    print(f'Loading PRE-INCIDENT: {PRE_FILE.name}')
    pre = load_xlsx_full(PRE_FILE)
    print(f'  → {len(pre)} SKUs')
    print(f'Loading LIVE-NOW: {LIVE_FILE.name}')
    live = load_xlsx_full(LIVE_FILE)
    print(f'  → {len(live)} SKUs')
    print()

    flag_total = Counter()
    flag_per_chunk = defaultdict(Counter)
    flag_per_col = defaultdict(Counter)
    flag_per_chunk_col = defaultdict(Counter)
    samples = {f: defaultdict(list) for f in ['STALE','WRONG','WIPED','FAIL']}
    edits_per_chunk = {}
    missing_skus_by_chunk = defaultdict(list)

    for n in CHUNKS_TO_AUDIT:
        try:
            edits, skipped = builder.parse_chunk(n)
        except FileNotFoundError:
            print(f'chunk-{n:03d}: NO diff.md, skipping')
            continue
        edits_per_chunk[n] = len(edits)
        print(f'chunk-{n:03d}: {len(edits)} edits ({len(skipped)} skipped at parse)')
        for e in edits:
            art = e.art
            fld = canon_field(e.field)
            if art not in pre or art not in live:
                missing_skus_by_chunk[n].append(art)
                continue
            pre_val = pre[art].get(fld, '')
            live_val = live[art].get(fld, '')
            intended, fail = compute_intended(pre_val, e)
            if fail is not None:
                flag = 'FAIL'
                if len(samples[flag][fld]) < 8:
                    samples[flag][fld].append((n, art, fail, pre_val[:80], live_val[:80]))
            elif live_val == intended:
                flag = 'OK'
            elif live_val == pre_val:
                flag = 'STALE'
                if len(samples[flag][fld]) < 8:
                    samples[flag][fld].append((n, art, pre_val[:120], intended[:120], live_val[:120]))
            elif live_val == '':
                flag = 'WIPED'
                if len(samples[flag][fld]) < 8:
                    samples[flag][fld].append((n, art, pre_val[:120], intended[:120]))
            else:
                flag = 'WRONG'
                if len(samples[flag][fld]) < 8:
                    samples[flag][fld].append((n, art, pre_val[:80], intended[:80], live_val[:80]))
            flag_total[flag] += 1
            flag_per_chunk[n][flag] += 1
            flag_per_col[fld][flag] += 1
            flag_per_chunk_col[(n, fld)][flag] += 1

    total = sum(flag_total.values())
    print(f'\n=== TOTAL: {total} edits classified ===')
    for f in ['OK','STALE','WIPED','WRONG','FAIL']:
        n = flag_total[f]
        pct = (n/total*100) if total else 0
        print(f'  {f:6s}: {n:5d}  ({pct:5.1f}%)')

    # Write report
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    L = []
    L.append('# PHASE B — Intended translation propagation\n')
    L.append(f'**Question:** for each translation edit we made in chunks 016–029, did it reach LIVE?\n')
    L.append(f'**Method:** parse all `chunk-NNN-diff.md` 016–029 → for each edit, compute `intended = apply(pre_incident, diff)` → compare to LIVE\n')
    L.append(f'**Inputs:**\n')
    L.append(f'- PRE-INCIDENT: `{PRE_FILE.name}` (read-only)\n')
    L.append(f'- LIVE-NOW: `{LIVE_FILE.name}` (read-only)\n')
    L.append(f'- Chunks: 016..029 ({len(CHUNKS_TO_AUDIT)} files)\n')

    L.append(f'\n## Top-level — {total} edits classified\n')
    L.append('| Flag | Count | % | Meaning |\n|---|---:|---:|---|\n')
    meanings = {
        'OK': 'translation reached LIVE',
        'STALE': 'edit stayed only in our file, LIVE = pre-incident value',
        'WIPED': 'LIVE is empty, broken import wiped, never recovered',
        'WRONG': 'LIVE has something else (manual edit / collision)',
        'FAIL': 'PARTIAL patch could not be applied (base differs / was not found)',
    }
    for f in ['OK','STALE','WIPED','WRONG','FAIL']:
        n = flag_total[f]
        pct = (n/total*100) if total else 0
        L.append(f'| {f} | {n} | {pct:.1f}% | {meanings[f]} |\n')
    L.append(f'| **TOTAL** | {total} | 100.0% | |\n')

    L.append('\n## Per-chunk breakdown\n')
    L.append('| Chunk | Edits | OK | STALE | WIPED | WRONG | FAIL |\n')
    L.append('|---|---:|---:|---:|---:|---:|---:|\n')
    for n in CHUNKS_TO_AUDIT:
        if n not in edits_per_chunk:
            continue
        c = flag_per_chunk[n]
        L.append(f'| {n:03d} | {edits_per_chunk[n]} | {c["OK"]} | **{c["STALE"]}** | {c["WIPED"]} | {c["WRONG"]} | {c["FAIL"]} |\n')

    L.append('\n## Per-column breakdown\n')
    L.append('| Column | OK | STALE | WIPED | WRONG | FAIL |\n')
    L.append('|---|---:|---:|---:|---:|---:|\n')
    for col in sorted(flag_per_col.keys()):
        c = flag_per_col[col]
        L.append(f'| {col} | {c["OK"]} | **{c["STALE"]}** | {c["WIPED"]} | {c["WRONG"]} | {c["FAIL"]} |\n')

    # Detail STALE breakdown by chunk×col — the actionable matrix
    L.append('\n## STALE matrix (chunk × column) — actionable\n')
    L.append('Numbers in this table = translations we did but LIVE still shows pre-incident value. ')
    L.append('Non-zero cell = we can re-emit them safely if we want them live.\n\n')
    used_cols_for_matrix = sorted(set(c for (_, c), v in flag_per_chunk_col.items() if v['STALE']))
    if used_cols_for_matrix:
        L.append('| Chunk | ' + ' | '.join(used_cols_for_matrix) + ' |\n')
        L.append('|---|' + '|'.join(['---:']*len(used_cols_for_matrix)) + '|\n')
        for n in CHUNKS_TO_AUDIT:
            if n not in edits_per_chunk:
                continue
            row_vals = [flag_per_chunk_col[(n, c)]['STALE'] for c in used_cols_for_matrix]
            if sum(row_vals) > 0:
                L.append(f'| {n:03d} | ' + ' | '.join(str(v) for v in row_vals) + ' |\n')
    else:
        L.append('_No STALE cells — every chunk edit reached LIVE._\n')

    # Samples
    for flag in ['STALE','WIPED','WRONG','FAIL']:
        if not samples[flag]:
            continue
        L.append(f'\n## Samples — {flag} (per column, first 8 each)\n')
        for col, items in samples[flag].items():
            L.append(f'\n### {col} — {sum(v[flag] for v in flag_per_col.values() if col in flag_per_col and flag_per_col[col][flag])} {flag}\n')
            L.append(f'(showing {len(items)})\n')
            for item in items:
                if flag == 'FAIL':
                    n, art, reason, pre_v, live_v = item
                    L.append(f'- chunk-{n:03d} `{art}` — reason: `{reason}`\n  - PRE:  `{pre_v}`\n  - LIVE: `{live_v}`\n')
                elif flag == 'STALE':
                    n, art, pre_v, intended_v, live_v = item
                    L.append(f'- chunk-{n:03d} `{art}`\n  - PRE/LIVE (same): `{live_v}`\n  - INTENDED:        `{intended_v}`\n')
                elif flag == 'WIPED':
                    n, art, pre_v, intended_v = item
                    L.append(f'- chunk-{n:03d} `{art}`\n  - PRE:      `{pre_v}`\n  - INTENDED: `{intended_v}`\n  - LIVE:     (empty)\n')
                else:  # WRONG
                    n, art, pre_v, intended_v, live_v = item
                    L.append(f'- chunk-{n:03d} `{art}`\n  - PRE:      `{pre_v}`\n  - INTENDED: `{intended_v}`\n  - LIVE:     `{live_v}`\n')

    if missing_skus_by_chunk:
        L.append('\n## SKUs from chunks not found in export (rare)\n')
        for n, arts in missing_skus_by_chunk.items():
            L.append(f'- chunk-{n:03d}: {len(arts)} missing — first 5: {arts[:5]}\n')

    OUT_FILE.write_text(''.join(L), encoding='utf-8')
    print(f'\n✅ Report written: {OUT_FILE}')


if __name__ == '__main__':
    main()
