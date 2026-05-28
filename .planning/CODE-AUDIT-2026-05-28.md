# CODE AUDIT — labresta-sync — 2026-05-28

**Запрос Yana:** «сделай полный глубокий аудит проекта labresta-sync. Ищи ошибки кода,
консистентности и дырки. Работай в ночном режиме.»

**Базовая точка:** HEAD = `c313b0f`. Предыдущий аудит `CODE-AUDIT-2026-05-26.md`
покрыл ядро матчера, sync_pipeline, pricing, yml_generator, частично вьюхи —
корректностных багов в гейтах матчера НЕ нашёл, пофикшены P-1/P-2/P-3/M-1, затем
P-4 (margin_below UAH) и manual_match reuse. Этот проход — свежий, фокус на областях,
которые прошлый аудит покрыл слабее: web-слой (`views/`), сервисы парсинга/импорта,
cross-cutting (транзакции, `.first()` без уникальности, секреты, консистентность).

**Легенда серьёзности:** P = priority bug (корректность/данные/безопасность),
M = minor/perf/by-design, POSITIVE = проверено и хорошо.

---

## Scope checklist (что прочитано целиком)

- [ ] app/__init__.py + config + extensions + scheduler
- [ ] app/views/matches.py (2034)
- [ ] app/views/suppliers.py (800)
- [ ] app/views/products.py (745)
- [ ] app/views/settings.py (381)
- [ ] app/views/catalog.py (241)
- [ ] app/views/dashboard.py (302)
- [ ] app/views/feed.py / logs.py / audit.py / auth.py / main.py
- [ ] app/services/catalog_import.py (462)
- [ ] app/services/kodaki_adapter.py (403)
- [ ] app/services/excel_parser.py (371)
- [ ] app/services/rp_parser.py (281)
- [ ] app/services/feed_parser.py (251)
- [ ] app/services/feed_fetcher.py (91)
- [ ] app/services/rematch_job.py (286)
- [ ] app/services/orphan_detector.py (361)
- [ ] app/services/rule_matcher.py (180)
- [ ] app/services/notification_service.py / telegram_notifier.py
- [ ] app/services/export_service.py / ftp_upload.py
- [ ] app/services/brand_supplier_overrides.py / audit_service.py
- [ ] models/*

---

## FINDINGS

### P-1 — Reject-кнопка УДАЛЯЕТ строку → отклонённый матч воскресает на следующем sync
**Файлы:** `app/views/matches.py:688` (`reject_match`), `app/views/matches.py:1199` (bulk reject).
**Статус:** НАЙДЕНО, не пофикшено (требует решения — см. ниже).

`reject_match` и bulk-reject делают `db.session.delete(match)`, тогда как ВСЕ остальные
reject-пути ставят `status="rejected"` и сохраняют строку:
- `mark_for_catalog` (`matches.py:1441`) → `status="rejected"`
- `resolve_conflict` action=keep (`matches.py:1316`) → `status="rejected"`
- `_detect_disappeared` (`sync_pipeline.py:358`) candidate→`rejected`

Матчер (`run_matching_for_supplier`, `matcher.py:2111-2114`) пере-создание пары блокирует
ТОЛЬКО если `(sp_id, pp_id)` есть в `existing_pairs` (любой статус) ИЛИ `rejected_pairs`
(status='rejected'). Удалённая строка не попадает ни туда, ни туда. → На следующем
полном sync `find_match_candidates(sp)` может снова вернуть тот же pp (если он всё ещё
лучший по score), пара не в existing/rejected → **кандидат пере-создаётся, оператор видит
ровно тот матч, который только что отклонил**.

Комментарий в `matcher.py:2062-2063` явно декларирует инвариант «user-rejected candidates
are never recreated» — delete-путь его нарушает. mark_new/conflict/disappeared защищены,
reject-кнопка (самый частый путь!) — нет.

**Последствия:** (1) повторная ручная работа оператора; (2) риск — оператор по ошибке
подтвердит ранее отклонённый неверный матч → неправильная цена/товар уйдёт в живой
Horoshop. Severity: medium-correctness.

**Предлагаемый фикс:** в `reject_match` и bulk-reject заменить `db.session.delete(match)`
на `match.status = "rejected"` (+ `confirmed_at/by` для аудита). `find_match_for_product`
с `exclude_prom_ids=[rejected_prom_id]` всё равно найдёт альтернативу для ДРУГОГО pp, а
сохранённая 'rejected'-строка (sp, rejected_pp) защитит от воскрешения. Уже-существующий
guard в `find_match_for_product:1971` (existing-pair → None) и в manual_match (промоут
existing_pair) делают это безопасным. Нужен тест: reject → sync → пара НЕ пере-создана.
**Требует подтверждения Yana** (меняет видимое поведение: rejected-строки начнут
накапливаться в БД; раньше reject их стирал). Не автономный фикс — это product-решение.

### M-1 (this audit) — bulk-reject не пере-сурфейсит альтернативу как одиночный reject
**Файл:** `matches.py:1202-1206`. Одиночный `reject_match` при `find_match_for_product()`
→ existing-row промоутит её обратно в candidate (699-709); bulk-reject просто
`if new_match: db.session.add(new_match)` — если `find_match_for_product` вернул None
(пара уже существует), ничего не сурфейсит. Минорная UX-несостыковка, НЕ 500 (guard в
find_match_for_product). Низкий приоритет.

### M-2 (this audit) — нет глобального мьютекса на sync (cron × manual × per-supplier)
**Файлы:** `dashboard.py:222` (guard только на manual-trigger), `scheduler.py:20`
(cron зовёт `run_full_sync()` без guard), `suppliers.py:653` (per-supplier sync без guard
и без SyncProgress). Single gunicorn worker + 4 threads → теоретически возможен оверлап
cron-sync и ручного sync в разных тредах. Stage 6.5 гоняет ГЛОБАЛЬНЫЙ bulk_auto_confirm
каждый раз → при оверлапе может отработать дважды; `SyncProgress` (глобальный temp-file
singleton) затрётся. Это carryover S-1 из прошлого аудита (by-design, низкая вероятность —
оператор редко кликает во время cron). Записано как осознанно-терпим, не блокер.

### M-3 (this audit) — SECRET_KEY дефолтится в "dev-key-change-me"
**Файл:** `config.py:12`. Если в проде env `SECRET_KEY` не выставлен, сессии и CSRF
подписываются публично-известным ключом → форжабельны. На Railway почти наверняка
выставлен, но кода-страховки (hard-fail при дефолте в проде) нет. Рекомендация: при
`not DEBUG and SECRET_KEY == "dev-key-change-me"` поднимать RuntimeError. Низкий риск
(скорее всего уже выставлен), но дёшево закрыть. **Проверить у Yana, выставлен ли env.**

### POSITIVE (проверено, багов нет)
- `sync_pipeline.py:276` — M-1 (rollback на error-пути) из прошлого аудита НА МЕСТЕ.
- `matches.py:278` — P-4 (rate=1 для UAH в margin_below фильтре) НА МЕСТЕ.
- Матчер dedup надёжен: `existing_pairs`/`rejected_pairs`/`claimed_pp_ids`, SA-Row→tuple
  каст (matcher.py:2046-2048) корректен, 1pp↔1supplier guard на источнике (Step 3.6).
- `find_match_for_product:1971` — existing-pair guard корректен (не 500-ит на reject).
- `manual_match` (c313b0f) корректно реюзает existing_pair вместо INSERT → нет uq_match_pair 500.
- Scheduler: single worker (`--workers 1 --threads 4`) → cron не дублируется; debug-guard корректен.
- Sync-trigger guard (409 already_running) есть для manual-пути.

---

## Last touched
2026-05-28 — прочитано: app core, sync_pipeline, dashboard, matcher dedup, matches.py
(query builder, reject/confirm/bulk/manual/resolve-conflict). Найдено P-1 + 3×M.
Дальше: products.py, suppliers.py, settings.py, catalog.py, parser-сервисы.
