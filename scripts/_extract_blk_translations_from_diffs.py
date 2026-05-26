"""Track #2 recovery: extract all blk триплет RU descriptions from closed chunks.

Walks .planning/translation-audit/chunks/chunk-0??-diff.md, finds every
`**Поле:** Описание товара (RU)` block whose `**Стало:**` is a full
RU translation tag-в-tag (inside a code fence), and emits one xlsx
[Артикул, Описание товара (RU)] for Horoshop import.

Parity assertion: extractor row count MUST equal
`grep -c "Стало:.*полный перевод RU"` across all input files.
"""
import sys, re, glob, subprocess
from openpyxl import Workbook

sys.stdout.reconfigure(encoding='utf-8')

CHUNKS_DIR = '.planning/translation-audit/chunks/'
OUT_XLSX = '.planning/translation-audit/horoshop-fix-desc-ru-FULL.xlsx'

# Match SKU section header — e.g.:
#   ## SKU 17/58 — Печь подовая Frosty FOV-20D (Артикул 2289556549) — 🔴 RU=UA + ...
sku_split_pat = re.compile(
    r'^## SKU (\d+)/(\d+)\s*[—\-–]\s*(.+?)\(Артикул\s+(\d+)\)',
    re.MULTILINE
)

# Within a SKU section, capture the RU desc translation between fences.
# Anchors on `**Поле:** Описание товара (RU)` first to avoid catching
# any mod_name/meta blocks that happen to contain similar markers.
stalo_pat = re.compile(
    r'\*\*Поле:\*\*\s*Описание товара\s*\(RU\)'
    r'.*?'
    r'\*\*Стало:\*\*\s*\(полный перевод[^\n]*\):?\s*\n+'
    r'```[^\n]*\n(.*?)\n```',
    re.DOTALL
)

def extract_one(diff_path):
    """Return list of (chunk, sku_n, sku_total, title, artikul, html) tuples."""
    text = open(diff_path, 'r', encoding='utf-8').read()
    chunk = diff_path.replace('\\', '/').split('/')[-1].replace('-diff.md', '')
    sku_matches = list(sku_split_pat.finditer(text))
    rows = []
    for i, m in enumerate(sku_matches):
        sku_n, sku_total, title, artikul = m.group(1), m.group(2), m.group(3).strip(), m.group(4)
        start = m.end()
        end = sku_matches[i+1].start() if i+1 < len(sku_matches) else len(text)
        section = text[start:end]
        sm = stalo_pat.search(section)
        if sm:
            html = sm.group(1).strip()
            rows.append((chunk, sku_n, sku_total, title, artikul, html))
    return rows

def main():
    diff_files = sorted(glob.glob(CHUNKS_DIR + 'chunk-0??-diff.md'))
    print(f'Scanning {len(diff_files)} diff.md files...')

    all_rows = []
    per_chunk_count = {}
    for f in diff_files:
        rows = extract_one(f)
        chunk_name = f.replace('\\', '/').split('/')[-1].replace('-diff.md', '')
        per_chunk_count[chunk_name] = len(rows)
        all_rows.extend(rows)

    print('\n--- per chunk ---')
    for chunk, cnt in sorted(per_chunk_count.items()):
        if cnt > 0:
            print(f'  {chunk}: {cnt}')

    # Parity check vs grep
    print('\n--- parity check ---')
    grep_out = subprocess.run(
        ['grep', '-c', r'Стало:.*полный перевод RU'] + diff_files,
        capture_output=True, text=True, encoding='utf-8'
    ).stdout.strip().split('\n')
    grep_total = sum(int(l.rsplit(':', 1)[-1]) for l in grep_out if l)
    print(f'  grep total markers: {grep_total}')
    print(f'  extractor matched:  {len(all_rows)}')
    if grep_total != len(all_rows):
        print('  ❌ PARITY MISMATCH — aborting xlsx write')
        sys.exit(1)
    print('  ✅ parity OK')

    # Duplicate artikul check
    seen = {}
    for r in all_rows:
        a = r[4]
        if a in seen:
            print(f'  ⚠️  DUPLICATE artikul {a} in {seen[a]} and {r[0]}/SKU {r[1]}')
        else:
            seen[a] = f'{r[0]}/SKU {r[1]}'
    print(f'  unique artikuls: {len(seen)}')

    # Sanity sample: SKU 17 Frosty FOV-20D from chunk-019
    sample = [r for r in all_rows if r[4] == '2289556549']
    if sample:
        c, n, _, t, a, h = sample[0]
        print(f'\n--- sample sanity (chunk-019 SKU 17, Frosty FOV-20D) ---')
        print(f'  chunk: {c}, sku: {n}, artikul: {a}')
        print(f'  html length: {len(h)} chars')
        print(f'  html starts: {h[:80]!r}')
        # Verify NO UA chars in extracted RU
        ua_chars = sum(1 for ch in h if ch in 'іїєґІЇЄҐ')
        print(f'  UA-glyph count in extracted RU: {ua_chars}  ({"✅ clean" if ua_chars == 0 else "❌ UA-leak"})')

    # Write xlsx
    wb = Workbook()
    ws = wb.active
    ws.title = 'desc-ru-fix'
    ws.append(['Артикул', 'Описание товара (RU)'])
    for _, _, _, _, artikul, html in all_rows:
        ws.append([artikul, html])
    wb.save(OUT_XLSX)
    print(f'\n--- written ---')
    print(f'  {OUT_XLSX}: {len(all_rows)} rows ({len(seen)} unique artikuls)')

if __name__ == '__main__':
    main()
