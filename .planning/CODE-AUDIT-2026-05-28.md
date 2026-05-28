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

### ✅ M-4 — FIXED (branch audit/2026-05-28-hardening) — XXE/entity-bomb hardening
**Фикс применён:** `feed_parser._parse_xml` теперь оба пути через
`etree.XMLParser(resolve_entities=False, no_network=True, huge_tree=False)` (зеркало
kodaki_adapter). Поведение для валидных фидов byte-identical (предопределённые сущности
`&amp;` и пр. резолвятся, кастомные/внешние — нет). Тесты: `test_audit_2026_05_28_hardening.py`
(3 шт.: кастомная сущность не разворачивается, внешняя SYSTEM не фетчится, `&amp;`+обычный
фид парсятся как раньше). Полный сьют 708 passed. ⚠️ НА ВЕТКЕ, не в main — Yana review+merge.

### M-4 (this audit) — XXE/entity-bomb: один XML-путь без hardening (инконсистентность)
**Файл:** `feed_parser.py:235` и `:243` (`_parse_xml`).
Все три адаптера в `kodaki_adapter.py` (kodaki/gooder/astim) парсят строго через
`etree.XMLParser(recover=True, resolve_entities=False, no_network=True, huge_tree=False)`.
А основной `_parse_xml` (путь для YML-фидов: НП, РП-через?, любой не-адаптерный
поставщик) использует голый `etree.fromstring(raw_bytes)` БЕЗ этих защит, и в fallback
тоже только `recover=True` без `resolve_entities=False/no_network=True`. → единственный
XML-вход без защиты от entity-expansion (billion laughs) и внешних сущностей.
Поставщики semi-trusted (URL настраивает оператор), риск низкий, но это явная
инконсистентность с уже принятым в проекте паттерном. **Фикс дёшев и безопасен**
(чистое добавление защиты, happy-path не меняется): вынести общий hardened-parser и
звать его в обоих ветках `_parse_xml`. Кандидат на автономный фикс + тест.

### M-5 (this audit) — N+1 в `save_supplier_products`
**Файл:** `feed_parser.py:150`. По одному `SELECT ... WHERE supplier_id AND external_id`
на каждый товар фида (НП ~700, Кодаки ~559, итого тысячи round-trip'ов за sync). Не
корректность — perf. Можно one-shot предзагрузить `{(supplier_id, external_id): row}`
по `supplier_id`. Низкий приоритет (sync асинхронный, не в request-path для cron).

### M-6 (this audit) — латентно: Horoshop-импорт обнуляет `pp.article`
**Файл:** `catalog_import.py:232-243,428-429`. `article` входит в `CATALOG_FIELDS`
(перезаписывается всегда на UPDATE), НО среди Horoshop-алиасов (`COLUMN_ALIASES`) нет
ни одного, дающего поле `article` — Horoshop отдаёт `артикул`→`external_id` и
`артикул для відображення`→`display_article`. Только prom.ua-формат (`код_товару`)
маппится в `article`. → Импорт Horoshop-выгрузки делает `setattr(existing,"article",None)`
для всех товаров. **Сейчас не кусается**: у Horoshop-товаров `article` и так None
(подтверждается отчётом импорта 2026-05-26 — `changed["article"]` не фигурировал =0),
поэтому None→None = no-op. **Риск латентный:** если в БД попадут prom.ua-товары с
заполненным `article`, последующий Horoshop-импорт его сотрёт. Матчер читает `pp.article`
(article fast-path). Фикс: либо убрать `article` из `CATALOG_FIELDS` (Horoshop им не
владеет), либо защищать как translation-поле. Низкий приоритет, но это реальная
кросс-форматная инконсистентность. **Проверить у Yana:** есть ли prom.ua-товары в проде.
POSITIVE здесь же: preview/save шарят `_normalize_product`+`CATALOG_FIELDS` → не разойдутся;
`preserve_translations` защищает name_ru/description_ru by construction; commit атомарный.

### ✅ M-7 — FIXED (branch audit/2026-05-28-hardening) — open-redirect guard
**Фикс применён:** `auth._is_safe_next()` пропускает только path-absolute same-site URL
(`/...`, не `//`, без scheme/netloc); `login` обнуляет небезопасный `next` перед redirect.
Тесты: unit на `_is_safe_next` (accept local / reject offsite+empty+js:) + integration
(POST login с `next=https://evil.com` не уводит на evil.com). ⚠️ НА ВЕТКЕ, не в main.

### M-7 (this audit) — open redirect в login через `next`
**Файл:** `auth.py:33-34`. `next_page = request.args.get("next")` → `redirect(next_page or ...)`
без проверки, что URL локальный. `/auth/login?next=https://evil.com` после успешного
логина уводит оператора на внешний сайт (фишинг-вектор). Severity низкая (внутренний
инструмент на 1 оператора), но это учебный open-redirect. Фикс: валидировать через
`url_has_allowed_host_and_scheme(next_page, request.host)` (есть в werkzeug/flask-login)
или отбрасывать любой next с непустым netloc. Безопасный автономный фикс + тест.

### INFO-2 (this audit) — login игнорирует результат `login_user()` + is_active
**Файл:** `auth.py:28-31`. Проверяется только `check_password`; возврат `login_user()`
не используется. Flask-Login `login_user` сам откажет деактивированному (`is_active=False`)
юзеру и вернёт False — но код всё равно пишет `last_login_at` и редиректит. Деактивированный
не получит доступ (сессия не выставится → @login_required отбросит назад), но увидит
петлю редиректа вместо «аккаунт отключён», и `last_login_at` обновится ложно. Минор UX.
Нет rate-limit на логин (brute-force) — informational, внутр. инструмент.

### INFO-1 (this audit) — feed_fetcher без SSRF-фильтра приватных IP
**Файл:** `feed_fetcher.py:45`. `requests.get(url)` без ограничения схемы/хоста и без
ограничения редиректов на приватные диапазоны. URL берётся из `supplier.feed_url`,
который ставит ТОЛЬКО аутентифицированный оператор (login_required) → реальной SSRF-дыры
нет (threat model = единственный доверенный оператор). Defense-in-depth: блокировать
private/loopback IP и `file://`. Informational, не блокер.

### POSITIVE (проверено, багов нет)
- `catalog.py` — staging импорта защищён: token-regex `^[0-9a-f]{32}$`, suffix-whitelist,
  синтетическое имя файла парсеру, stale-cleanup, `preserve_translations=True` на confirm.
  Path traversal невозможен.
- `rule_matcher.apply_match_rules` — корректен: skip confirmed/manual, respect rejected
  (line 148), upgrade candidate→confirmed, 1:1 через нарастающий `claimed_pp_ids`, no N+1.
- `excel_parser` / `rp_parser` — защитный парсинг, round() в cents корректен, EUR-only
  документирован, two-step preview не даёт залить мусор вслепую.
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
