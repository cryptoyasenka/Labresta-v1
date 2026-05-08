# CURRENT — labresta-sync (Flask supplier sync app)

**Last touched:** 2026-05-09 (Night audit closed clean; TODO-NEXT.md saved for tomorrow's per-row work)

## Audit results (2026-05-09 — night session)
- `.planning/matching-audit-report.md` (commit `fc466f7`): A=0 B=13 B-rev=9 C=0 D=267 E=0 F=0 G=0 H=11
- `.planning/article-anchor-verify.md` (commit `ee914d6`): 487 three-way + 417 two-way + **4 rule violations** + 1641 no-anchor (fuzzy/manual)
- 4 violations отозваны (все были `confirmed_by='Admin'` manual): match#6611 (Hendi щепа 250г vs 150г SP), #6383 (Hendi цитрус-пресс), #1100 (Sirman STORM VV), #1102 (Sirman CICLONE 36 VT). Re-verify: 0 violations осталось, total confirmed 2549→2545.
- `.planning/no-anchor-verify.md` (commit `cce9cac`): **1641 confirmed без article-anchor — clean**. 1636/1641 OK по brand+voltage+model-token; 0 brand mismatches, 0 voltage disjoint, 5 no_model_token все вручную проверены — все валидные (Rational SCC→iCC rebrand с display_article anchor на PP-стороне; Sirman 1/2 vs I/2 typo; Ugolini MINIGEL с переставленными словами).

## TODO для Yana завтра
См. **`.planning/TODO-NEXT.md`** (commit `3d6d640`). Приоритет:
1. Cat H — 11 cross-brand display_article дублей в Horoshop (catalog hygiene, ручками)
2. Catalog cleanup — 3 AD46 PPs (PP#1007/1015/1008) убрать из Horoshop
3. Cat B sibling (13 шт.) — per-row через `/matches/` UI
4. Cat B-reverse (8 шт.) — per-row решение

**Status:** Прозвонены 14 URL-вариантов np.com.ua/dealer-export (`scripts/_probe_np_url_variants.py` — temp, удалён). Финальный вывод: **поставщик np.com.ua не выгружает APL/APKE/AFM 02-03 ни в одном формате/параметре**. Любой из {`filetype=xlsx|csv|xml|yml`} × {без `platform`, `platform=prom|opencart|woocommerce|horoshop`} × {`with_all=1|with_full=1|include_disabled=1|include_unavailable=1`} = тот же набор 690 уникальных SKU. `platform=horoshop` режет вдвое (691 строк) только потому что фильтрует одну локаль (UA), без него — 1382 строки = 690 RU + 691 UA версий тех же товаров. Apach = 158 уникальных (316 RU+UA). APL: 0 hit. APKE: 0 hit. AFM 02/03: 0 hit. AD46: только AD46MI ECO / AD46M ECO / AD46DI ECO (AD46MV/DV отсутствуют — Yana подтвердила). **Проблема НЕ в URL и НЕ в парсере. Поставщик технически не экспортирует часть каталога**. Phase M apply остаётся ЗАБЛОКИРОВАН.

## Open files
- (none — Phase L и Phase M закрыты at commit level, awaits manual smoke-test)

## Next step
1. **Yana — Phase L smoke-test:** открыть `/matches/?supplier_id=4`, выделить 5-10 НП кандидатов, нажать «Подтвердить». Должен появиться `#conflictResolveModal` с per-row кнопками **Оставить** / **Переключить** вместо старого toast'а. По каждой строке клик → должна faded'нуться + статус «Кандидат отклонён» / «Переключено». Закрыть → reload.
2. **Phase M apply — ЗАБЛОКИРОВАН. Технических вариантов больше нет.** URL-варианты исчерпаны (см. Status). Остались два пути: **(A)** написать поставщику np.com.ua с просьбой расширить дилер-экспорт (показать им скрин дилерского портала где APL/APKE/AFM 02 есть, а в XLSX их нет — спросить почему `dealer_id=69781` выдаёт неполный набор), **(B)** scrape дилерского портала по логину manager@labresta.com — но Cloudflare блокирует headless Chromium, нужен реальный браузер с DPAPI cookie или ручной экспорт по сессии. **Для Apach — не применять Phase M ни на одном уровне** пока не дополним фид. Альтернатива: per-brand whitelist в `flag_orphan_pps` — пропускать Apach до починки.
3. **Phase N — diagnostic step done, matcher change deferred:** скрипт `scripts/diagnose_sibling_gap.py` (commit `bdaca6c`) классифицирует unmatched PP в 4 категории: Cat A (exact-anchor SP — gate filtered), Cat B (SP=anchor+suffix), Cat B-reverse (PP=SP+suffix), Cat None (no nearby SP). На local-DB Hurakan/supplier_id=2 (stale): 4/5/4/18. **Yana — прогнать на проде:** `railway run python scripts/diagnose_sibling_gap.py --brand Hurakan --supplier-id 4` чтобы увидеть реальные числа и решить — стоит ли матчер модифицировать. Локалка показала важный сюрприз: некоторые Cat A SPs **уже привязаны к другим PP** (duplicate Horoshop card problem — PP#3864 vs PP#3902), что матчер-изменение НЕ решит. Для них нужен другой workflow (rebind или slim card cleanup).
2. **Yana — UI триаж 10 настоящих orphans Phase 8:** `/matches/deletion-candidates?tab=orphan` (badge=10), фильтр по бренду, **Видалено / Залишити / Запит**.
3. **Manual Astim review** (carry-over): отклонить m=6620, 6618, 6611 + подтвердить 7 fuzzy candidates на `/matches/?supplier_id=8&status=candidate`.
4. **MARESTO unblock** (опционально): MARESTO всё ещё 0/4509 fresh на проде (id=1 в `dead_supplier_ids`). Whitelist Railway egress IP через support, либо local-fetch скрипт.
5. **Open question (deferred):** должен ли `suppliers_fetch_all` передавать `exclude_dead_suppliers=True`? Решение за Yana — risk decision (auto-cron должен ли стрелять пока MARESTO навсегда мёртв?). Текущий код — OFF (safe default). НЕ автономно.

## Phase L commits (тонкая ночь)
- `7f442d7` backend — `_build_conflict_payload` + enriched `skipped_claimed` + `POST /matches/resolve-conflict` (keep/switch) + 11 tests
- `14367b4` frontend — `#conflictResolveModal` в `review.html` + `populateConflictModal/resolveConflict/buildConflictRow` в `matches.js`. Backward-compat fallback на старый toast если payload без `entry.candidate`.

## Phase N diag commit (после M)
- `bdaca6c` — `scripts/diagnose_sibling_gap.py` read-only классификатор unmatched PP. Local Hurakan/sup_id=2 baseline: 4 Cat A (DL800/DL775 silver+black/HBH850M PRO COVER/BLW2 grey — но 3/4 SP уже в другом PP), 5 Cat B (DHD10G/12G/16G→GM, CFV60→M, TR65→M — но TR65 SP уже в PP#3934), 4 Cat B-reverse (IP40FM/WNC160CDW/ISV5P×2), 18 Cat None.

## Phase M commit
- `0b9b5e2` — `feat(phase-M): orphan flag for PP without display_article via name scan`. Helpers `_supplier_article_strings` / `_build_sp_article_boundary_re` / `_any_sp_article_in_pp_name` + fallback ветка в `flag_orphan_pps` когда `disp` пуст. 5 новых тестов. Total 21/21 orphan_detector + 677/677 suite.
- `938ed00` docs(planning) — CURRENT update Phase M done.

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

**Last commit:** 2026-05-08 — `feat(phase-N): diagnostic script for sibling-gap analysis` (`bdaca6c`)
**Memory pointers:**
- `~/.claude/projects/C--Users-Yana/memory/project_labresta.md`
- `~/.claude/projects/C--Users-Yana/memory/project_labresta_horoshop_import.md`
- `~/.claude/projects/C--Users-Yana/memory/project_labresta_feed_mgmt_plan.md`

## Existing .planning artifacts
_Phase plans already exist in this dir — check `ls .planning/` before starting; CURRENT.md complements them with right-now state._
