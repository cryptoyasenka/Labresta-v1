# CURRENT — labresta-sync (Flask supplier sync app)

**Last touched:** 2026-05-08 (ночь — Phase 8 + Hendi exclusion APPLIED to prod)
**Status:** Phase 8 + post-apply фикс + Hendi×Кодаки exclusion применены. Yana указала "Hendi только у Астима" — у Кодаки 2 Hendi корзины (sp_id=6076, 6160), мешали detection. Захардкожен `BRAND_SUPPLIER_EXCLUSIONS = {"hendi": {3}}` в `app/services/brand_supplier_overrides.py`, применён в orphan_detector + matcher + rule_matcher. После apply: **27 orphans на проде** — Hendi 17, FROSTY 6, GI.Metal 4. **661/661 tests**. Все коммиты запушены, Railway auto-deploys.

## Open files
- (none — Phase 8 closed)

## Next step
1. **Yana — UI триаж 10 настоящих orphans:** `/matches/deletion-candidates?tab=orphan` (badge=10), фильтр по бренду, для каждой строки выбрать **Видалено / Залишити / Запит**.
2. **Manual Astim review** (carry-over): отклонить m=6620, 6618, 6611 + подтвердить 7 fuzzy candidates на `/matches/?supplier_id=8&status=candidate`.
3. **MARESTO unblock** (опционально): MARESTO всё ещё 0/4509 fresh на проде (id=1 в `dead_supplier_ids`). Whitelist Railway egress IP через support, либо local-fetch скрипт. Пока не починится — `flask flag-orphans` без `--exclude-dead-suppliers` блокируется sanity guard'ом, и `suppliers_fetch_all` тоже скипает Stage 4.5.
4. **Open question:** должен ли `suppliers_fetch_all` тоже передавать `exclude_dead_suppliers=True`? Сейчас OFF (safe default). Решение за Yana — описано в SUMMARY.

## Phase 8 commits (today)
- `51d274c` Task 1 — service + 11 tests
- `11aa107` Task 2 — wire-in + CLI
- `cd1e91b` Task 3 — UI tab + brand filter + clear-flag endpoint
- `3f9f07a` fix — skip no-display-article + `--exclude-dead-suppliers`
- `d27a7e0` SUMMARY (initial)
- `fb89ace` follow-up fix: keep dead in anchor + clear-on-recovery + 3 new tests (APPLIED to prod via railway run + DATABASE_PUBLIC_URL: 16 cleared, 10 remain)

## Prod audit (2026-05-08, scripts/verify_prod.py)
- Astim: 487 confirmed, 10 candidates (3 display_art_dup, 7 fuzzy false-pos)
- MARESTO: 857 confirmed, 10 candidates (но sync error всегда — см ниже)
- Кодаки: 559 conf, 9 cand. Гудер: 76, 2. РП: 187, 56. НП: 371, 21.
- Total candidates=108, badge=14 (correct по logic — исключает PP с другим confirmed match)
- 0 stuck SyncRuns. 0 M:1 violations. 17 truly-orphan Hendi PP (Phase 8 baseline).

## Three problems found and resolved (2026-05-08)
1. **YML 404 на проде — FIXED** (commit `4f15e58`). Root cause: Railway эфемерная FS стирает `instance/feeds/` при каждом deploy. Fix: `scripts/regenerate_yml_on_startup.py` в startCommand перед gunicorn (с `|| echo` fallback). Verified: `/feed/yml` HTTP 200, 7.4 MB, 2548 offers.
2. **MARESTO sync падает 403 Forbidden — KNOWN ISSUE** (commit `4f89bda` диагностический скрипт). Root cause: `mrst.com.ua/include/price.xml` возвращает 200 OK с локалки, но 403 с Railway. Заголовки парсера нормальные (Chrome 124 UA + Referer). Это IP-блок (Cloudflare WAF против Railway-диапазона). Не наш баг. Fix потребовал бы whitelist на стороне MARESTO или прокси.
3. **Stage 4 deletion_candidate=0 везде — НЕ БАГ**. Логика корректна: триггер срабатывает только если SP не виден ≥9h И есть confirmed/manual match. Все суппортеры свежие; MARESTO падает на Stage 1 (403) до Stage 4 не доходит. 17 orphan Hendi PP — отдельная история (никогда не были в фиде Astim) → Phase 8 закроет именно этот gap.

## Decisions made earlier today (2026-05-08)
- 484 Astim R0 confirms applied via `apply_rules(apply=True, confirmed_by='manual:astim_first_apply')`. Per-rule: только R0 fired. r4_rejects=0.
- YML push в Horoshop = pull-модель (Horoshop сам тянет по URL), активного FTP push в `sync_pipeline.run_full_sync` нет. Stage 7 пишет YML только локально.
- 9 не-confirmed Astim candidates — R0 path B провалился потому что артикул только в `display_article`, не в `pp.name`. Path A провалился потому что `pp.article=None`. По правилу всё корректно. Yana подтвердит вручную.
- 26 Hendi PP без confirmed match. 17 из них в фиде Astim отсутствуют → real gap → Phase 8.
- Stuck SyncRun id=36, 37 (от 2026-05-05) помечены `failed` чтобы UI спиннер разблокировать.

## Constraints (carried over)
- LIVE store, никакого активного FTP push без go-ahead.
- 1 PP ↔ 1 confirmed supplier match (M:1 forbidden).
- 100% name match НЕ bulletproof — only identical names safe to bulk-confirm.
- Voltage variants (220 vs 380) = different SKU, never auto-match.

## Apply result (2026-05-08)
- `confirmed`: 484 (all Astim R0 — article anchor + display_article match)
- `singles`: 689, `multis`: 19, `skipped_claimed`: 91
- `per_rule`: `R0:article-name+display_article` = 484 (only rule that fired)
- `r4_rejects`: 0, `rejected`: 0
- 19 multis did not auto-confirm (R3 conditions not met — expected, leaves them for manual UI review)

## Constraints / decisions
- **LIVE store** — never push full Horoshop import without explicit go-ahead + safe-mode plan
- Horoshop only, never prom.ua
- 1 caталожный товар ↔ 1 confirmed supplier match (M:1 forbidden)
- 100% name match is NOT bulletproof — only identical names safe to bulk-confirm
- Voltage variants (220 vs 380) = different SKU, never auto-match
- `<oldprice>` in YML overrides Horoshop card "Знижка %" (fixed 2026-04-23, commit `ed8182f`)
- Finish Maresto first before adding new suppliers
- Proper fix > workaround: clean data via merge/delete scripts, не оставлять сирот
- 491 tests at commit `6908d11`

**Last commit:** 2026-05-08 — `feat(bulk_auto_confirm): R0 article anchor rule`
**Memory pointers:**
- `~/.claude/projects/C--Users-Yana/memory/project_labresta.md`
- `~/.claude/projects/C--Users-Yana/memory/project_labresta_horoshop_import.md`
- `~/.claude/projects/C--Users-Yana/memory/project_labresta_feed_mgmt_plan.md`

## Existing .planning artifacts
_Phase plans already exist in this dir — check `ls .planning/` before starting; CURRENT.md complements them with right-now state._
