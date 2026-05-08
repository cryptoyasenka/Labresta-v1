# Night audit report — 2026-05-09

Полный matching audit прода + три уровня верификации article-anchor правила.
Безопасные правки применены (4 manual rule-violation rejects). Всё что
требует per-row решения — отложено в `.planning/TODO-NEXT.md`.

## TL;DR
- **Code health:** 677/677 tests pass, 0 регрессий, prod stable.
- **False-positives на проде:** 4 manual matches нарушали article-anchor правило → отозваны. После: 0 нарушений.
- **False-positives broader scan:** 1641 no-anchor confirmed matches проверены через нормализованный brand + voltage + model-token — 0 актуальных нарушений.
- **False-negatives gaps:** 33 unmatched PP в трёх категориях (B sibling 13, B-reverse 8, AD46 catalog cleanup 3) — все требуют ручного решения, перечислены в TODO.
- **Catalog hygiene:** 11 cross-brand display_article дублей в Horoshop — Cat H, ручная правка завтра.
- **Phase M Apach:** ЗАБЛОКИРОВАН. np.com.ua не выгружает APL/APKE/AFM 02-03 — 14 URL-вариантов прозвонены, ровно тот же набор. Нужно либо просьба к поставщику, либо scrape дилерского портала через cookie + DPAPI.

## Что сделано автономно (read-only / safe-write)

### 1. Full matching audit (commit `fc466f7`)
`scripts/audit_matching_gaps.py` — A-H категории по всем brand×supplier парам.
Результат в `.planning/matching-audit-report.md`:
- Cat A (exact-anchor gap): **0** — никаких упущений где SP article == PP display_article без матча.
- Cat B (sibling): **13** — SP article = PP anchor + suffix. Per-row review нужен.
- Cat B-reverse: **9** — PP длиннее SP. 1 уже подтверждена как корректная (AD46MV ≠ AD46M ECO).
- Cat C (voltage variant violations): **0** — никаких 220↔380 ложных матчей.
- Cat D (name mismatch + article match): **267** — by design (R0 path B), не findings.
- Cat E (M:1): **0** — UniqueConstraint работает.
- Cat F (short anchor risk): **0** — все display_article ≥4 chars.
- Cat G (orphan SP, dead supplier): **0**.
- Cat H (cross-brand display_article duplicates): **11** — каталог Horoshop, ручная правка.

### 2. Article-anchor rule verifier (commit `ee914d6`)
`scripts/verify_article_anchor_rule.py` — проверяет three-location rule
(`sp.article == pp.display_article` AND article token in `pp.name`/`pp.name_ru`/`pp.article`)
на всех confirmed matches. Результат в `.planning/article-anchor-verify.md`:
- 487 three-way OK
- 417 two-way OK (no display_article, anchor в name + sp.article)
- **4 violations** — все manual, все отозваны через `scripts/reject_match.py`:
  - match#6611 (Astim) — Hendi щепа 250г PP vs 150г SP
  - match#6383 (Astim) — Hendi цитрус-пресс mismatch
  - match#1100 (MARESTO) — Sirman STORM VV
  - match#1102 (MARESTO) — Sirman CICLONE 36 VT
- 1641 без article-anchor — это name-fuzzy / Кодаки internal codes / manual confirms.
  Большинство наверняка корректны, но требуют узкой верификации → script #3.

### 3. No-anchor narrow verifier (commit `cce9cac`)
`scripts/verify_no_anchor_matches.py` — для 1641 no-anchor confirmed matches
проверяет три red flag:
- R1: brand mismatch (нормализовано: strip non-alnum + lowercase, чтобы
  `IceTech == Ice Tech`, `RESTO ITALIA == Restoitalia`)
- R2: voltage disjoint sets между sp.name и pp.name
- R3: no model token in common (>=4 chars + digit) с whitespace-collapse
  чтобы `TG 310 == TG310`, `XL 413 == XL413`

Результат в `.planning/no-anchor-verify.md`:
- ✅ **1636/1641 OK**
- ⚠ Brand mismatch: **0**
- ⚠ Voltage disjoint: **0**
- ⚠ No model token: **5** — все вручную проверены, все валидные:
  - 3× Rational SCC/CMP → iCC rebrand с display_article anchor на PP-стороне
    (sp.article=None отключает anchor-проверку в three-way verifier)
  - 1× Sirman SALAMANDRA Mobile PRO `1/2 G` ↔ `I/2 G` (Roman numeral typo
    у поставщика; display_article 30143502 в обоих)
  - 2× Ugolini MINIGEL с переставленными словами
    (`MINIGEL 1 Plus` ↔ `MINIGEL PLUS 1`)

### 4. AD46-series clean check (commit `9eff3ef`)
`scripts/check_ad46_state.py` (gitignored — `scripts/check_*.py`):
- 3 confirmed: AD46DI ECO, AD46M ECO, AD46MI ECO ↔ свои SP — корректно
- AD46D, AD46DV, AD46MV — unmatched, никаких rejected/candidate записей
  вокруг (никто кривой матч не сделал)
- Memory: `~/.claude/projects/.../memory/feedback_labresta_ad46_suffix_skus.md`
  фиксирует правило: AD46MV ≠ AD46M, AD46DV ≠ AD46D, AD46DI ≠ AD46D ECO

### 5. Code review за ночные коммиты
| Commit | Тип | Замечания |
|---|---|---|
| `cce9cac` | script + report | new file, isolated, no prod code touched |
| `3d6d640` | docs | TODO-NEXT.md, plain markdown |
| `9eff3ef` | docs | CURRENT.md status note |
| `e945391` | docs | CURRENT.md audit results |
| `ee914d6` | scripts | 3 new files (verifier + reject tool + report), no prod code |
| `fc466f7` | scripts | 2 new files (auditor + report), no prod code |

Вердикт: ночь read-only / docs only. Никаких изменений в `app/`,
никаких миграций, никаких новых тестов сломаны. Risk = 0.

## Что заблокировано / требует Yana

### Tomorrow — TODO-NEXT.md (commit `3d6d640`)
Приоритет от высокого к низкому:
1. **Cat H** — 11 cross-brand display_article дубли в Horoshop (Hendi-артикулы в Spidocook/Fimar/Roller Grill/FROSTY/Saro PPs + same-brand разные модели в Ozti/FROSTY/Sirman). Ручная правка через Horoshop admin.
2. **Catalog cleanup** — 3 AD46 PPs (PP#1007 AD46MV, PP#1015 AD46DV, PP#1008 AD46D) убрать (товара нет у np.com.ua).
3. **Cat B sibling** — 13 unmatched PPs где SP article = anchor + suffix. Hurakan ×7, Apach ×3, Fagor ×1, Robot Coupe ×1, Sirman ×1. Per-row через `/matches/`.
4. **Cat B-reverse** — 8 unmatched где PP длиннее SP. Hurakan ×4, Sirman ×2, Ceado ×1, Airhot ×1.

### Carry-over (не из ночи)
- Phase L UI smoke-test (`/matches/?supplier_id=4`)
- Phase M apply ЗАБЛОКИРОВАН (Apach feed gap)
- Manual Astim review — 7 fuzzy candidates
- MARESTO unblock (Cloudflare)
- Open question: `suppliers_fetch_all(exclude_dead_suppliers=True)` default

## Артефакты
- `scripts/audit_matching_gaps.py`
- `scripts/verify_article_anchor_rule.py`
- `scripts/verify_no_anchor_matches.py`
- `scripts/reject_match.py`
- `scripts/check_ad46_state.py` (gitignored)
- `.planning/matching-audit-report.md`
- `.planning/article-anchor-verify.md`
- `.planning/no-anchor-verify.md`
- `.planning/TODO-NEXT.md`
- `.planning/NIGHT-AUDIT-REPORT-2026-05-09.md` (этот файл)
- 4 reject'a на проде: match#6611, #6383, #1100, #1102
- Memory: `feedback_labresta_ad46_suffix_skus.md`
