# CURRENT — labresta-sync (Flask supplier sync app)

**Last touched:** 2026-05-15 — **chunk-005 in progress 32/84** (last commits `354aa6b` SKU 25-32 Apach combo griddle+FROSTY griddles+Silver/Isikgaz · `b64d1d1` SKU 17-24 Unox/Apach розстоєчні шафи [awaiting Yana review] · `0070dc1` SKU 9-16 FROSTY/Kogast/EWT INOX/GoodFood/Unox · `326a9d7` SKU 5-8 [awaiting Yana review] · `1d4f0df` SKU 1-4 ATA). chunk-004 DONE 65/65 (`c5f9a5b`), chunk-003 DONE 69/69 (`a91f98d`), chunk-002 DONE 74/74 (`259a943`). chunk-001 still blocked by 8 Yana-questions. Multiple chunk-005 SKU had RU=UA full copy — translated per locked term list, flagged in `.planning/translation-audit/chunks/chunk-005-questions.md` (`e92a762`). HTML structural defects (SKU 26/27 FROSTY GH-550/760) flagged manual, no auto-fix. Next: chunk-005 SKU 33-40 dump+apply.

## ✅ DONE 2026-05-14 — Cat H closed + clean Horoshop XLSX upload + DB hygiene

**Cat H (11 коллизий) — закрыт:**
- 7 Hendi-vs-non-Hendi очищены в БД + Horoshop CMS (Yana). Tasks #2/#4/#5/#6/#7/#11 completed.
- 4 внутри-бренда (Ozti, Sirman ×3, FROSTY) оставлены — это ручные коды, могут совпасть с будущим feed'ом.
- Verification: `scripts/verify_cat_h_article_ownership.py` (commit `d45b510`) — 6 артикулов реально в Астим feed (Hendi distributor).

**XLSX upload 13.05.26 — успешно:**
- CSRF fix (commit `d9a53a5`): template `app/templates/catalog/import.html` теперь содержит `<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">`. Раньше форма была без токена, любой POST падал.
- Backup сделан до загрузки: `backups/pre-catalog-import_2026-05-13_1658.json` (5683 PPs + 2689 matches, 20.8 MB).
- Импорт: 5632 строк → 0 новых, 5632 обновлено, 0 пропущено.
- Verifier `scripts/verify_after_catalog_import.py` (commit `cfafb8d`): все 9 проверок green. 7 Cat H PPs остались display_article=NULL post-import.

**bench_pp* мусор удалён:**
- 50 синтетических строк (IDs 5684-5733, brand=Sirman, name="Sirman Mantegna NN", price=1000 EUR, created 2026-04-26 20:29:13 одной транзакцией) — артефакт perf-benchmark скрипта, прогнавшегося против прода. Не в Horoshop, 0 matches.
- Audit `scripts/audit_bench_pp_pollution.py` (commit `5d8277d`) → подтвердил scope.
- Delete `scripts/delete_bench_pp_pollution.py` (commit `a5a6a56`) → 50 удалено с --apply (2026-05-14 06:10).
- Total PromProducts: 5683 → **5633**. Verifier baseline скорректирован.

**Текущее состояние БД:**
- 5633 PromProducts (всё реальный Horoshop каталог)
- 2689 ProductMatches (2546 confirmed/manual)
- 6 suppliers: MARESTO 861, НП 373, Кодаки 559, РП 187, Гудер 79, Астим 487 (= 2546 total)
- 12890 SupplierProducts

## Backlog (следующее)
1. **UA→RU перевод каталога** — IN PROGRESS 2026-05-15. **Chunk-001:** 83/83 source audit done, ЗАБЛОКИРОВАН 8 вопросами Yana в `.planning/translation-audit/chunks/chunk-001-questions.md`. **Chunk-002:** 74/74 source audit DONE (last commit `259a943`, 9 SKU batches). **Chunk-003:** PENDING (next). Workflow per batch: `python -c "..."` dump 5-8 SKU из `chunk-NNN.json` → Read `.planning/scratch_skubatch.txt` → Edit-append `chunk-NNN-diff.md` перед final `---` → commit. После всех чанков (003-085): `scripts/apply_chunk_diff.py` (openpyxl, key Артикул) собирает master-fixed.xlsx → drift check vs fresh Horoshop re-export → Yana ручная загрузка `/catalog/import` + `backup_before_catalog_import.py` сначала.
2. **Починка характеристик в Horoshop CMS** — NEXT после перевода. На странице товара (пример: `labresta.com.ua/ru/parokonvektomat-unox-xevc0711e1rm-liniia-one/`) 4 свойства отображаются **зачёркнутыми**: `Номінальна напруга`, `Страна производитель`, `Вид обладнання`, `Номінальна споживана потужність`. Причина: свойства в Horoshop CMS помечены как архивные/неактивные (значения остались привязанными к товарам, но Property labels выведены из активного списка). Также часть свойств UA-only без RU-перевода имени. Скоуп: пройти **Каталог → Свойства товаров** в Horoshop, восстановить активный статус + дозаполнить UA+RU имена для всех зачёркнутых свойств. Рекомендованный вариант A (unarchive + переименование) безопаснее B (создать новые + перепривязать значения). Подзадача-помощь от меня: когда будем чистить описания товаров в XLSX-чанках — отдельно собрать таблицу всех уникальных `Характеристика → значение` из HTML-описаний с готовыми UA+RU вариантами как референс для импорта свойств в CMS.
3. **Прогресс-бар на /catalog/import** — UX улучшение. Корень: catalog_import делает 5632 индивидуальных SELECT+UPDATE round-trip через Railway proxy ~80-120 сек, впритык gunicorn timeout 120s. Решение: `INSERT ... ON CONFLICT DO UPDATE` одной операцией → импорт упадёт до ~5-10 сек, прогресс-бар не нужен.
4. **AD46 cleanup** — 3 PPs убрать из Horoshop (PP#1007/1015/1008). Apach AD46MV/DV/D ≠ AD46M/MI/DI ECO.
5. **Cat B sibling (13 шт.)** — per-row через `/matches/` UI.
6. **Cat B-reverse (8 шт.)** — per-row решение.
7. **Phase L smoke-test** — `/matches/?supplier_id=4`, выделить 5-10 НП кандидатов, подтвердить, проверить #conflictResolveModal.
8. **Manual Astim review** (7 fuzzy + 3 reject).

## Memory rule установлено
- `feedback_labresta_backup_before_catalog_import.md` — перед каждой XLSX загрузкой backup + offer restore.
- TODO: добавить memory "не запускать perf-benchmark против прода без явного флага" (после bench_pp инцидента).

---

## ⏸ Prior session — 2026-05-13 (Cat H plan rewritten, Horoshop pass ждёт Yana)

**CSRF fix pushed (commit `d9a53a5`):** `app/templates/catalog/import.html` form was missing
`<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">`. Every POST /catalog/import
failed with "The CSRF token is missing" — that template hadn't been used in months. Fix is one
line, pushed to main, Railway redeploys ~1-2 min after push.

**Post-upload verifier (commit `cfafb8d`):** `scripts/verify_after_catalog_import.py` —
read-only check after Yana's upload. Confirms 7 Cat H PPs still NULL, counts unchanged
(PPs ≥ 5683, matches = 2689, suppliers = 6), spot-checks fields. Points to restore command
if anything fails.

**Backup taken pre-upload (commit `e9fed2a`):** `backups/pre-catalog-import_2026-05-13_1658.json`
— 5683 PPs + 2689 matches, 20.8 MB. Restore via `scripts/restore_pp_from_backup.py`.

**Cat H DB clears already applied (commit `44279fe`):** 7 PPs cleared in DB. Yana also cleared
the Horoshop cards (her words 2026-05-13). If both halves done correctly, post-upload verifier
will pass.

**Next concrete actions:**
1. Yana retries XLSX upload via `/catalog/import` (fresh page load to pick up new csrf_token)
2. If 200 OK: Yana runs `.venv/Scripts/python.exe scripts/verify_after_catalog_import.py`
3. If verifier passes: I close tasks #2/#4/#5/#6/#7/#11 (Cat H done)
4. If verifier fails: restore via `scripts/restore_pp_from_backup.py backups/pre-catalog-import_2026-05-13_1658.json --apply`

**Файлы (committed, deployed):**
- `app/templates/catalog/import.html` — CSRF token added
- `scripts/verify_after_catalog_import.py` — new post-upload verifier
- `scripts/backup_before_catalog_import.py` + `scripts/restore_pp_from_backup.py` — pre-import safety
- `scripts/clear_cat_h_hendi_display_articles.py` — Cat H clear script (already applied)

---

## ⏸ Prior session — 2026-05-13 (Cat H plan rewritten, Horoshop pass ждёт Yana)

**Cat H финализирован.** Правило Yana 2026-05-13: правим **только** Hendi-vs-не-Hendi коллизии. Внутри-бренда (Ozti↔Ozti, Sirman↔Sirman, FROSTY↔FROSTY) НЕ ТРОГАТЬ — там display_article это ручные коды, для Sirman/Ozti они могут совпасть с будущим feed'ом когда подключим поставщика.

**Финальный план — 7 правок (clear display_article):**
- PP#347 Spidocook SP300 (`203149` Hendi) → очистить
- PP#80 Fimar PFD27 (`239766` Hendi) → очистить
- PP#154 Roller Grill PIS 30 (`239780` Hendi) → очистить
- PP#958 FROSTY RC-30 (`240403` Hendi) → очистить
- PP#3933 FROSTY IC80A (`271599` Hendi) → очистить
- PP#3932 GoodFood ICE777 (`271599` Hendi) → очистить
- PP#4179 Saro SKZ-12 (`860526` Hendi) → очистить

**Verification:** `scripts/verify_cat_h_article_ownership.py` (2026-05-13, read-only prod-DB) — все 6 артикулов реально из Астим feed (Hendi distributor); 5 внутри-бренда артикулов нет ни у одного поставщика (Yana-entered).

**Не трогаем:** Ozti `0830.00020.00`, Sirman `40752102P` / `40802852F` / `66520502K1.2`, FROSTY `212004` — внутри-бренда коллизии. FROSTY VP-81/VP-2Y40 уже phase8_orphan, отдельная UI-задача (не Cat H).

**Файлы (commit pending):**
- `.planning/dossiers/cat-h/HOROSHOP-WALKTHROUGH.md` — переписан под 7 clear-only
- `.planning/dossiers/cat-h/ANSWERS.md` — переписан под финальный план
- `scripts/verify_cat_h_article_ownership.py` — новый verify-скрипт

**Предыдущие commits на ветке (suffix-style план, теперь obsolete):** `ef29a1c` lookup, `028689b` sirman.com, `d52733e` CURRENT, `d88777c` UA shops, `dc46ca3` #10 suffix, `92bb23f` #8 closed, `bed9fb7` CURRENT update, `6f64c17` HOROSHOP-WALKTHROUGH (suffix). Не откатываю — следующий коммит просто фиксирует финальный план.

**Не закрыто:** Tasks в TaskList — pending до физической правки 7 PPs в Horoshop CMS (диагноз готов, action за Yana).

**Следующее после Horoshop pass** (выбор Yana из TODO-NEXT.md):
1. AD46 cleanup — 3 PPs убрать (PP#1007/1015/1008)
2. Cat B sibling (13 шт.) — per-row через UI
3. Cat B-reverse (8 шт.) — per-row
4. Phase L smoke-test
5. Manual Astim review (7 fuzzy + 3 reject)

---

## Session 2026-05-09 — auto_sync_enabled (commits `1e91fcc`, `9f3b3bc`, `a0d6599`)

---

---

## Session 2026-05-09 — auto_sync_enabled (commits `1e91fcc`, `9f3b3bc`, `a0d6599`)
- **Кнопка «Обновить данные» удалена** с дашборда (только перерисовывала виджеты, путала оператора). Page и так auto-poll'ит.
- **`Supplier.auto_sync_enabled`** (bool, default True, NOT NULL) + Postgres миграция `migrate_add_supplier_auto_sync_pg.py` в `railway.toml` startCommand. Прод: миграция отработала, в логах `auto_sync_enabled migration: done.`
- **`run_full_sync(supplier_id=None, *, manual=False)`** — крон (`manual=False`) фильтрует `auto_sync_enabled=True`; ручные кнопки (`manual=True`) и per-supplier path игнорируют флаг.
- **Toggle endpoint** `POST /suppliers/<id>/toggle-auto-sync` + badge `Авто-синк OFF` (warning) + кнопка «Авто-синк OFF/ON» в `/suppliers/`.
- **MARESTO snapped on prod** через UI (`auto_sync_enabled=False`) — крон больше не дёргает 403'ящий feed. Verified в БД: `(1, 'MARESTO', True, False)`, остальные `True`.
- **Tests**: 6 в `tests/test_sync_pipeline_auto_sync.py` (cron skip, manual include, per-supplier ignore, is_enabled=False guard, toggle endpoint flip + 404). Suite 677→683 passed.

## Audit results (2026-05-09 — night session)
- `.planning/matching-audit-report.md` (commit `fc466f7`): A=0 B=13 B-rev=9 C=0 D=267 E=0 F=0 G=0 H=11
- `.planning/article-anchor-verify.md` (commit `ee914d6`): 487 three-way + 417 two-way + **4 rule violations** + 1641 no-anchor (fuzzy/manual)
- 4 violations отозваны (все были `confirmed_by='Admin'` manual): match#6611 (Hendi щепа 250г vs 150г SP), #6383 (Hendi цитрус-пресс), #1100 (Sirman STORM VV), #1102 (Sirman CICLONE 36 VT). Re-verify: 0 violations осталось, total confirmed 2549→2545.
- `.planning/no-anchor-verify.md` (commit `cce9cac`): **1641 confirmed без article-anchor — clean**. 1636/1641 OK по brand+voltage+model-token; 0 brand mismatches, 0 voltage disjoint, 5 no_model_token все вручную проверены — все валидные (Rational SCC→iCC rebrand с display_article anchor на PP-стороне; Sirman 1/2 vs I/2 typo; Ugolini MINIGEL с переставленными словами).

## Per-row dossiers (commit `02318e3`)
**`.planning/dossiers/INDEX.md`** — 42 dossier-файла собраны из прода:
- `cat-h/` 11 шт. — каждый duplicate display_article с обоими PP, фото, ценами, описаниями
- `cat-b/` 13 шт. — PP + suffix-кандидат-SP с voltage check
- `cat-b-rev/` 9 шт. (был 8, prod refresh +1)
- `astim-fuzzy/` 9 шт. (был 7, prod refresh +2)

Регенерация: `.venv/Scripts/python.exe scripts/build_dossiers.py --cat all`

## TODO для Yana завтра
См. **`.planning/TODO-NEXT.md`** (commit `7c96966`+). Приоритет:
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
