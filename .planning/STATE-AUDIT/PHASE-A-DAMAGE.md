# PHASE A — Damage assessment (read-only)
**Generated:** Phase A of state audit per `.planning/STATE-AUDIT-PLAN.md`
**Inputs:**
- PRE-INCIDENT: `horoshop-export 20.05.26.xlsx` (5632 SKUs)
- LIVE-NOW: `horoshop-export 21.05.26.xlsx` (5632 SKUs)
- Broken import (scope): `horoshop-import-2026-05-20.xlsx` (943 SKUs)
- Track #2 residual SKUs: ['2110282234', '1582804831', '2062006550']
- Track #1 known SKU: ['1766968161']

**Total audit scope:** 943 SKUs × 8 content columns = 7544 cells

## Top-level damage summary (cell counts)
| Flag | Count | % |
|---|---:|---:|
| KEPT | 6208 | 82.3% |
| KEPT-EMPTY | 0 | 0.0% |
| CHANGED-OK | 1336 | 17.7% |
| APPEARED | 0 | 0.0% |
| WIPED | 0 | 0.0% |
| **TOTAL** | 7544 | 100.0% |

### Reading the flags
- **KEPT** — PRE non-empty, LIVE same value (cell never broke / fully recovered to original)
- **KEPT-EMPTY** — PRE empty, LIVE empty (never had content)
- **CHANGED-OK** — PRE non-empty, LIVE non-empty, different value (translation applied or content updated)
- **APPEARED** — PRE empty, LIVE non-empty (new content arrived)
- **WIPED** — PRE non-empty, LIVE EMPTY (broken import damage, NOT recovered)

## Per-column damage breakdown
| Column | KEPT | KEPT-EMPTY | CHANGED-OK | APPEARED | WIPED |
|---|---:|---:|---:|---:|---:|
| Название (UA) | 928 | 0 | 15 | 0 | **0** |
| Название (RU) | 931 | 0 | 12 | 0 | **0** |
| Название модификации (UA) | 928 | 0 | 15 | 0 | **0** |
| Название модификации (RU) | 332 | 0 | 611 | 0 | **0** |
| META keywords (UA) | 873 | 0 | 70 | 0 | **0** |
| META keywords (RU) | 889 | 0 | 54 | 0 | **0** |
| Описание товара (UA) | 702 | 0 | 241 | 0 | **0** |
| Описание товара (RU) | 625 | 0 | 318 | 0 | **0** |

## Per-SKU rollup
- SKUs with ≥1 WIPED cell (NOT fully recovered): **0**
- SKUs with content changes (CHANGED-OK or APPEARED) but no WIPED: **880**
- SKUs with no changes vs PRE: **63**

## Samples — WIPED cells (per column, first 5 each)

### Название (UA) — no WIPED ✅

### Название (RU) — no WIPED ✅

### Название модификации (UA) — no WIPED ✅

### Название модификации (RU) — no WIPED ✅

### META keywords (UA) — no WIPED ✅

### META keywords (RU) — no WIPED ✅

### Описание товара (UA) — no WIPED ✅

### Описание товара (RU) — no WIPED ✅

## Samples — CHANGED-OK cells (per column, first 5 each)

### Название (UA) — 15 CHANGED-OK cells
- `1131875858`
  - PRE:  `Гриль-саламанандра AIRHOT SGE-580 Salamander з жарковою поверхнею`
  - LIVE: `Гриль-саламандра AIRHOT SGE-580 Salamander з жарочною поверхнею / жаркова / жаро`
- `1136081897`
  - PRE:  `Поверхня для смаження SILVER 2149 (комб.) електрична`
  - LIVE: `Поверхня для смаження Silver 2149 (комб.) електрична`
- `1153759435`
  - PRE:  `Гриль-саламанандра інфрачервоний Roller Grill SEM 600 Q`
  - LIVE: `Гриль-саламандра інфрачервоний Roller Grill SEM 600 Q`
- `1153763826`
  - PRE:  `Гриль-саламанандра Roller Grill SEM 600 PDS`
  - LIVE: `Гриль-саламандра Roller Grill SEM 600 PDS`
- `1387478313`
  - PRE:  `Плита індукційна Tehma 4 х 2,8 кВт на 4 конфоркиподовжена (1500х600 мм)`
  - LIVE: `Плита індукційна Tehma 4 х 2,8 кВт на 4 конфорки, подовжена (1500х600 мм)`

### Название (RU) — 12 CHANGED-OK cells
- `1136081897`
  - PRE:  `Жарочная поверхность SILVER 2149 (комб.) электрическая`
  - LIVE: `Жарочная поверхность Silver 2149 (комб.) электрическая`
- `1582778887`
  - PRE:  `Фритюрница BECKERS FB 4 LT`
  - LIVE: `Фритюрница BECKERS FB 4 LTA`
- `1582812924`
  - PRE:  `Фритюрница BECKERS FB 4+4 LT`
  - LIVE: `Фритюрница BECKERS FB 4+4 LTA`
- `1582816216`
  - PRE:  `Фритюрница BECKERS FB 6+6 LT`
  - LIVE: `Фритюрница BECKERS FB 6+6 LTA`
- `1766968161`
  - PRE:  `Термопроцесор SIRMAN Softcooker LIGHT (Sous Vide)`
  - LIVE: `Термопроцессор SIRMAN Softcooker LIGHT (Sous Vide)`

### Название модификации (UA) — 15 CHANGED-OK cells
- `1131875858`
  - PRE:  `Гриль-саламанандра AIRHOT SGE-580 Salamander з жарковою поверхнею`
  - LIVE: `Гриль-саламандра AIRHOT SGE-580 Salamander з жарочною поверхнею`
- `1136081897`
  - PRE:  `Поверхня для смаження SILVER 2149 (комб.) електрична`
  - LIVE: `Поверхня для смаження Silver 2149 (комб.) електрична`
- `1153759435`
  - PRE:  `Гриль-саламанандра інфрачервоний Roller Grill SEM 600 Q`
  - LIVE: `Гриль-саламандра інфрачервоний Roller Grill SEM 600 Q`
- `1153763826`
  - PRE:  `Гриль-саламанандра Roller Grill SEM 600 PDS`
  - LIVE: `Гриль-саламандра Roller Grill SEM 600 PDS`
- `1387478313`
  - PRE:  `Плита індукційна Tehma 4 х 2,8 кВт на 4 конфоркиподовжена (1500х600 мм)`
  - LIVE: `Плита індукційна Tehma 4 х 2,8 кВт на 4 конфорки, подовжена (1500х600 мм)`

### Название модификации (RU) — 611 CHANGED-OK cells
- `1009168845`
  - PRE:  `Плита-табурет газова Hendi 147801`
  - LIVE: `Плита-табурет газовая Hendi 147801`
- `1042057453`
  - PRE:  `Стіл холодильний REEDNEE GN3100TN`
  - LIVE: `Стол холодильный REEDNEE GN3100TN`
- `1042567057`
  - PRE:  `Стіл холодильний REEDNEE GN2100TN`
  - LIVE: `Стол холодильный REEDNEE GN2100TN`
- `1045612322`
  - PRE:  `Плита газова EWT INOX TTGC2`
  - LIVE: `Плита газовая EWT INOX TTGC2`
- `1045615998`
  - PRE:  `Плита газова EWT INOX TTGC4`
  - LIVE: `Плита газовая EWT INOX TTGC4`

### META keywords (UA) — 70 CHANGED-OK cells
- `1009168845`
  - PRE:  `плита газова, плита на газ, плита на газе, пимак, плита газова пімак, пімак, пли`
  - LIVE: `плита газова, плита-табурет, hendi, hendi 147801, kitchen line, плита промислова`
- `1045612322`
  - PRE:  `pimak, плита газова, плита на газ, плита на газе, пимак, плита газова пімак, газ`
  - LIVE: `pimak, плита газова, плита на газ, плита на газе, пимак, плита газова пімак, газ`
- `1045618489`
  - PRE:  `pimak, плита газова, плита на газ, плита на газе, пимак, плита газова пімак, газ`
  - LIVE: `pimak, плита газова, плита на газ, плита на газе, пимак, плита газова пімак, газ`
- `1122665946`
  - PRE:  `pimak, плита газова, плита на газ, плита на газе, пимак, плита газова пімак, пім`
  - LIVE: `плита газова, wok, плита wok, casta, casta kc02120070ba, kc02120070ba, плита газ`
- `1136081897`
  - PRE:  `remta, r, 82, lpg, газ, газовий, газова, гриль, ремта, смажена, поверхню, гладка`
  - LIVE: `Silver, 2149, гриль, смажена, поверхня, комбінована, неіржавка сталь, сталь, неі`

### META keywords (RU) — 54 CHANGED-OK cells
- `1009168845`
  - PRE:  `плита газовая, плита на газу, плита на газе, газова пліта, газова плита, плита н`
  - LIVE: `плита газовая, плита-табурет, hendi, hendi 147801, kitchen line, плита промышлен`
- `1045612322`
  - PRE:  `pimak, плита газовая, плита на газу, плита на газе, пимак, плита газовая пимак, `
  - LIVE: `pimak, плита газовая, плита на газу, плита на газе, пимак, плита газовая пимак, `
- `1045615998`
  - PRE:  `pimak, плита газовая, плита на газу, плита на газе, пимак, плита газовая пимак, `
  - LIVE: `pimak, плита газовая, плита на газу, плита на газе, пимак, плита газовая пимак, `
- `1045618489`
  - PRE:  `pimak, плита газовая, плита на газу, плита на газе, пимак, плита газовая пимак, `
  - LIVE: `pimak, плита газовая, плита на газу, плита на газе, пимак, плита газовая пимак, `
- `1122665946`
  - PRE:  `pimak, плита газовая, плита на газу, плита на газе, пимак, плита газовая пимак, `
  - LIVE: `плита газовая, wok, плита wok, casta, casta kc02120070ba, kc02120070ba, плита га`

### Описание товара (UA) — 241 CHANGED-OK cells
- `1110574295`
  - PRE:  `<p>Рисоварка корисним об&#39;ємом 5,4 л (загальний об&#39;єм &mdash; 10 літрів) `
  - LIVE: `<p>Рисоварка корисним об&#39;ємом 5,4 л (загальний об&#39;єм &mdash; 10 літрів) `
- `1122644991`
  - PRE:  `<h2>Гриль Тепаньяки Casta TEP3/120E електричний.</h2> <ul>
<li>на открытой базе<`
  - LIVE: `<h2>Гриль Тепаньяки Casta TEP3/120E електричний.</h2> <ul>
<li>на відкритій базі`
- `1122665946`
  - PRE:  `<h2>Плита газова Casta KC02120070BA WOK.</h2> <ul>
<li>на открытой базе</li>
<li`
  - LIVE: `<h2>Плита газова Casta KC02120070BA WOK.</h2> <ul>
<li>на відкритій базі</li>
<l`
- `1122669838`
  - PRE:  `<h2>Жаркова поверхня електрична Casta L7KTE1BAL гладка.</h2> <ul>
<li>гладка</li`
  - LIVE: `<h2>Жарочна поверхня електрична Casta L7KTE1BAL гладка.</h2>`
- `1140471779`
  - PRE:  `<p>Пароконвектомат UNOX XEVC0711E1RM лінія ONE &ndash; це високоякісне обладнанн`
  - LIVE: `<p>Пароконвектомат UNOX XEVC0711E1RM лінія ONE &ndash; це високоякісне обладнанн`

### Описание товара (RU) — 318 CHANGED-OK cells
- `1009168845`
  - PRE:  `<h2>Модель Kitchen Line - для пропану і бутану. Включаючи набір конвертерів, яки`
  - LIVE: `<h2>Модель Kitchen Line — для пропана и бутана. Включая набор конвертеров, котор`
- `1009182279`
  - PRE:  `<h2>Плита газовая GoodFood GP6 на 6 конфорок.</h2> <ul>
<li>Горелки: 6 * 32,925 `
  - LIVE: `<h2>Плита газовая GoodFood GP6 на 6 конфорок.</h2> <ul>
<li>Горелки: 6 * 32,925 `
- `1045612322`
  - PRE:  `<h2>Плита газова настільна EWT INOX TTGC2 на 2 конфорки</h2> <ul>
<li>Чавунні ре`
  - LIVE: `<h2>Плита газовая настольная EWT INOX TTGC2 на 2 конфорки</h2> <ul>
<li>Чугунные`
- `1045615998`
  - PRE:  `<h2>Плита газова настільна EWT INOX TTGC4 на 4 конфорки</h2> <ul>
<li>Чавунні ре`
  - LIVE: `<h2>Плита газовая настольная EWT INOX TTGC4 на 4 конфорки</h2> <ul>
<li>Чугунные`
- `1045618489`
  - PRE:  `<h2>Плита газова настільна EWT INOX TTGC6 на 6 конфорок</h2> <ul>
<li>Чавунні ре`
  - LIVE: `<h2>Плита газовая настольная EWT INOX TTGC6 на 6 конфорок</h2> <ul>
<li>Чугунные`

## All WIPED SKUs (for manual recovery planning)
None — no WIPED cells anywhere in scope. ✅
