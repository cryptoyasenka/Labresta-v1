"""chunk-029 close prep — insert missing SKU 47 + 48 SKIP-НП stubs in diff.md.

These two Apach SKUs (AMT 40 art=1504706007, AMT 65 art=1504742155) were
processed in b6 batch (mentioned in MR.md tables and counted in chunk-029 SKIP-НП
cumul) but their dedicated diff.md sections were skipped by the b6 writer.
Recover them before close — mirror compact SKIP-НП stub format used for SKU 49.
"""
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

p = '.planning/translation-audit/chunks/chunk-029-diff.md'
s = open(p, 'r', encoding='utf-8').read()
orig_len = len(s)

# Idempotency guards
assert s.count('## SKU 47/79 — ') == 0, 'SKU 47 stub already present'
assert s.count('## SKU 48/79 — ') == 0, 'SKU 48 stub already present'
assert s.count('## SKU 46/79 — ') == 1, 'SKU 46 header anchor not unique'
assert s.count('## SKU 49/79 — ') == 1, 'SKU 49 header anchor not unique'

# Anchor: end of SKU 46 section = right before SKU 49 header (since 47/48 missing).
# Compact SKIP-НП stub format mirrors SKU 49.
STUB_47 = (
    "## SKU 47/79 — Печь для пиццы конвейерная APACH AMT 40 (Артикул 1504706007) — SKIP-НП (NP-эксклюзив)\n\n"
    "**Поле:** Все ячейки\n"
    "**Было:** UA-leak (`desc UA==RU` True, `nm_ua==nm_ru` True)\n"
    "**Стало:** без изменений — тело из фида НП позже\n\n"
    "*(SKIP-НП — brand=Apach ∈ NP-эксклюзив SET (word-boundary Lat caps + Cyr match "
    "`Apach`). POL3 правило activated: НЕ переписываем RU, НЕ trogaem UA, cells в "
    "`chunk-029-fixed.xlsx` не модифицируем. **ПЕРВЫЙ Apach в chunk-029** "
    "(sister-pair с SKU 48 AMT 65). AMT 40 = конвейерная pizza-печь AMT-серия "
    "(35-45 піц/год Ø45 cm). Кумул. SKIP-НП chunk-029 после SKU 47 = 6 "
    "(Hurakan×5 b1+b2 + Apach×1 b6). Open questions 0.)*\n\n"
    "*(scoped к row Артикул=1504706007)*\n\n"
    "---\n\n"
)

STUB_48 = (
    "## SKU 48/79 — Печь для пиццы конвейерная APACH AMT 65 (Артикул 1504742155) — SKIP-НП (NP-эксклюзив)\n\n"
    "**Поле:** Все ячейки\n"
    "**Было:** UA-leak (`desc UA==RU` True, `nm_ua==nm_ru` True)\n"
    "**Стало:** без изменений — тело из фида НП позже\n\n"
    "*(SKIP-НП — brand=Apach ∈ NP-эксклюзив SET (word-boundary Lat caps + Cyr match "
    "`Apach`). POL3 правило activated: НЕ переписываем RU, НЕ trogaem UA, cells в "
    "`chunk-029-fixed.xlsx` не модифицируем. **ВТОРОЙ Apach в chunk-029** "
    "(sister-pair с SKU 47 AMT 40 b6). AMT 65 = конвейерная pizza-печь AMT-серия "
    "(extended chamber-size sister-model). Кумул. SKIP-НП chunk-029 после SKU 48 = 7 "
    "(Hurakan×5 b1+b2 + Apach×2 b6 SKU 47/48). Open questions 0.)*\n\n"
    "*(scoped к row Артикул=1504742155)*\n\n"
    "---\n\n"
)

# Insert before SKU 49 header
anchor = '## SKU 49/79 — '
idx = s.index(anchor)
new_s = s[:idx] + STUB_47 + STUB_48 + s[idx:]

# Sanity
assert new_s.count('## SKU 47/79 — ') == 1
assert new_s.count('## SKU 48/79 — ') == 1
assert new_s.count('## SKU 49/79 — ') == 1
assert new_s.endswith('---\n')

# Count SKU headers — must be exactly 79 now
hdrs = re.findall(r'^## SKU (\d+)/79 — ', new_s, re.M)
assert len(hdrs) == 79, f'expected 79 headers after recovery, got {len(hdrs)}'
present = sorted(set(int(n) for n in hdrs))
assert present == list(range(1, 80)), f'gaps in SKU header set: {present}'

open(p, 'w', encoding='utf-8', newline='').write(new_s)

v = open(p, 'r', encoding='utf-8').read()
print('len delta ==', len(v) - orig_len)
print('SKU 47 added ==', v.count('## SKU 47/79 — '))
print('SKU 48 added ==', v.count('## SKU 48/79 — '))
print('SKU 49 kept ==', v.count('## SKU 49/79 — '))
print('total /79 headers ==', len(re.findall(r'^## SKU \d+/79 — ', v, re.M)))
print('ends --- ==', v.endswith('---\n'))
print('DONE _recover029_sku47_48 — 2 SKIP-НП stubs inserted, 79/79 headers complete.')
