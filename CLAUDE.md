# LabResta Sync — правила для будущих сессий

Этот файл — контракт для Claude Code и новых разработчиков. Здесь зафиксированы инварианты, накопленные за 12+ сессий фиксов. **Не откатывай эти правила без явной причины и тестов.**

## Что это за проект

Flask-приложение, синхронизирует цены и наличие поставщиков (MARESTO и др.) с интернет-магазином **Horoshop** (labresta.com.ua). Приложение генерирует YML-фиды (общий, по поставщику, кастомные подборки — см. инвариант #14) и отдаёт их Horoshop на импорт. **Это live-магазин**, любые ошибки матчинга = реальные убытки.

- Stack: Flask 3.1, SQLAlchemy, SQLite (WAL), APScheduler, lxml, rapidfuzz, openpyxl
- Запуск: `.venv/Scripts/python.exe run.py` (порт 5000)
- Тесты: `.venv/Scripts/python.exe -m pytest` (269+ тестов должны быть зелёными)
- Admin: admin@labresta.ua / admin123

## Терминология

- **SupplierProduct (sp)** — товар из фида поставщика
- **PromProduct (pp)** — товар из каталога Horoshop. Таблица `prom_products` — **исторически** названа так (раньше был prom.ua), сейчас это Horoshop-каталог, **не меняй название таблицы**.
- **ProductMatch** — связка sp ↔ pp со скором, статусом (`candidate` / `confirmed` / `manual` / `rejected`), скидкой, `name_synced`.

## Инварианты матчера (не ломать)

### 1. Voltage-варианты — разные SKU
Модель `(220)` и `(380)` — это физически разные товары. Никогда не матчить.
- Код: `app/services/matcher.py:51-71` (`VOLTAGE_TAGS`, `VOLTAGE_RE`, `extract_voltages`)
- Тесты: `tests/test_matcher_price_gate.py` (класс про voltage)

### 2. 1 pp ↔ 1 active supplier match
Каталожный товар может иметь максимум ОДИН `confirmed` или `manual` матч. Гарантируется partial UNIQUE INDEX.
- Миграция: `scripts/migrate_unique_prom_match.py` (индекс `uq_match_prom_confirmed`)
- Runtime-чек при rebind: `app/views/matches.py` (409 Conflict если pp уже claimed)
- Тесты: `tests/test_views_matches.py`
- **Нарушения** чинятся через `scripts/merge_duplicate_sp.py` + `scripts/collisions_report.py`, НЕ удалением записей вручную.

### 3. 100% fuzzy score НЕ bulletproof
Только identical meaningful tokens (после снятия бренда) можно bulk-confirm. Fuzzy 100% без совпадения токенов = candidate, не confirmed.
- Код: `scripts/bulk_auto_confirm.py:77-94` (`classify_single`, R1 = `sup == prom` set equality)
- R2 (subset + tight price ±band) — отдельное слабое правило, не путать с R1.

### 4. Cross-brand reject при пустом бренде поставщика
Если у sp пустой `brand`, не матчим к pp с непустым брендом. Иначе "Слайсер" матчится ко всему.
- Код: `app/services/matcher.py:528-554` (Both-None policy в brand gate)

### 5. Letter-space-digit glue
`R 301` ↔ `R301`, `IP 3500` ↔ `IP3500`. Работает на 1-4 заглавных буквах перед цифрой. Стопворды (PLUS/MAXI/PRO/ULTRA/...) пропускаются, чтобы "STAR PLUS 40" не клеилось в PLUS40.
- Код: `app/services/matcher.py:266-288` (`_GLUE_STOPWORDS`, `_glue_letter_digit`)
- Применяется в: `extract_model_from_name` и `meaningful_tokens`

### 6. Морфологическое равенство токенов
«диска» ↔ «диски», «кухонний» ↔ «кухоний» — общий префикс ≥min(len)−2, оба ≥4 символов, в расходящемся хвосте нет цифр.
- Код: `app/services/matcher.py:331-378` (`_near_duplicate_token`, `_tokens_subset_morph`)

### 7. Cyrillic→Latin транслитерация в type gate
«Гриль саламандра» vs «Гриль Salamandra» — до фикса давал score 22 (нет overlap), сейчас ~70.
- Код: `app/services/matcher.py:454-461` (`_transliterate_cyr`), вызывается перед `fuzz.token_sort_ratio` в type gate

### 8. Size-fraction tokens не попадают в model
`I/2`, `1/2`, `II/IV` — размерные дроби, не модельный суффикс. `extract_model_from_name` возвращает `""` для таких токенов, чтобы гейт не сравнивал "i2" vs "12".
- Код: `app/services/matcher.py:293-311` (`_is_size_fraction`, `_normalize_roman_fractions`)

### 9. Pure-digit-only containment diff = reject
Если containment gate различает sp и pp только цифровыми токенами (Neapolis vs Neapolis 4) — это разные SKU, reject.
- Код: `app/services/matcher.py:378-398` (`_digit_only_discriminator`)

### 10. TESTING safety guard (критическая история)
2026-04-10 тест-фикстура стёрла prod БД. После фикса: если `TESTING=1` и URI указывает на прод БД — `RuntimeError` при старте.
- Код: `app/__init__.py:20-31`
- Shared session fixture: `tests/conftest.py`
- Бэкапы: `scripts/backup_db.py` (SQLite online backup, keeps last 20)

### 11. Horoshop, не prom.ua
Магазин — labresta.com.ua на Horoshop. `prom_products` / `PromProduct` — легаси название таблицы/модели, не переименовывать (сломает миграции). В UI и новых комментариях — **Horoshop**.

### 12. Auto-discount формула
`Closure price = MARESTO_retail × (1 − d/100)`. Rate 0.75 (MARESTO wholesale = retail −25%). Target 19%, capped чтобы UAH-маржа ≥500 грн при EUR 51.15. Ceil-to-favor-customer.
- Код: `app/services/pricing.py` (`calculate_auto_discount(retail_cents, eur_rate) -> int %`)
- Тесты: `tests/test_pricing.py`
- Формула:
  - `retail ≥ 162.9 EUR` → 19%
  - `39.1 ≤ retail < 162.9` → `ceil(100*(0.25 − 500/(retail×rate)))`
  - `retail < 39.1` → 0%

### 13. Live-store guard
Изменения, которые видны покупателю, требуют явного go-ahead:
- Auto-discount apply — `POST /suppliers/<id>/apply-discount` требует `force=1`, dry-run по умолчанию.
- Horoshop import — сначала `scripts/export_yml_subset.py` (5-10 offers), тоннель, проверка 1 товара в live, **потом** полный фид.

### 14. Feed routing — три scope, один источник правды
Phase K разделил YML-фиды на три области, каждая с устойчивым URL и отдельным файлом. Не путать.

| Scope | URL | Файл | Кто триггерит | Влияет на `in_feed` |
|---|---|---|---|---|
| Main (всё) | `/feed/yml` | `labresta-feed.yml` | «Пересобрать общий YML» на `/suppliers` или `/matches` | **Да** (только этот) |
| По поставщику | `/feed/yml/supplier/<slug>` | `labresta-feed-<slug>.yml` | «Пересобрать YML» в строке поставщика | Нет |
| Кастомная подборка | `/feed/yml/custom/<token>` | `labresta-feed-custom-<token>.yml` | «Собрать фид из выбранного» на `/matches` | Нет |

- `Supplier.slug` — uniq, автогенерится на insert (`maresto`, `kodaki`). Не редактировать вручную после первой генерации, иначе URL у Horoshop протухнет.
- `token` = `sha256(sorted(match_ids))[:12]` — детерминирован, та же выборка → тот же URL → тот же файл (перезаписывается).
- Кастомные фиды живут вечно; удаляются только через `/feeds/custom` (UI delete).
- Узкие фиды (`labresta-prices.yml`, `labresta-availability.yml`) остались для CLI (`yml_generator.sync_prices/sync_availability`); UI-кнопки убраны в K.4 — их перекрыли per-supplier фиды.
- Код: `app/services/yml_generator.py` (`regenerate_yml_feed` / `regenerate_supplier_feed` / `regenerate_custom_feed` / `custom_feed_token`), `app/views/feed.py` (роуты + slug/token regex-валидация против path-traversal), `app/models/custom_feed.py`.

## Порядок работы (не нарушать без спроса)

1. Полировка матчинга → цены/наличие → UI фиксы → формирование фида → **только потом** новые поставщики.
2. **Никаких новых поставщиков** пока Maresto pipeline не закрыт (цены + наличие + UI). Очередь: Меркс → Кодаки → Gooder → РП Україна.
3. Чистить данные правильно — merge/delete скрипты, а не «пусть будут сироты».

## Load-bearing скрипты (`scripts/`)

| Скрипт | Что делает | Опасность |
|--------|-----------|-----------|
| `audit_candidates.py` | Прогоняет матчер по candidate rows, находит stale/missing | `--dry-run` безопасно, `--apply` меняет БД |
| `merge_duplicate_sp.py` | Сливает дубликаты SupplierProduct (переносит матчи на каноническую запись) | Меняет БД, делай backup |
| `collisions_report.py` | Находит нарушения 1pp↔1sp | Read-only |
| `apply_auto_discount.py` | Заполняет `discount_percent` по формуле #12 | **LIVE!** всегда `--dry-run` сначала |
| `export_yml_subset.py` | Фильтрует YML до 5-10 offers для safe-mode импорта | Read-only |
| `bulk_auto_confirm.py` | Автоподтверждает R1 (identical tokens) / R2 (subset + tight price) | Меняет БД, `--dry-run` сначала |
| `diagnose_sp_match.py` | Трассирует почему у SP нет кандидата | Read-only |
| `backup_db.py` | SQLite online backup (хранит 20) | Безопасно |
| `migrate_*.py` | Одноразовые миграции схемы | Уже применены, не запускать повторно |

## Добавление нового поставщика (чеклист)

1. `feed_parser.py` — поддерживает ли формат фида нового supplier (YML/Excel/GSheets)?
2. Добавить запись в таблицу `suppliers` (брендовые настройки, eur_rate_uah если нужно).
3. Прогнать один цикл: fetch → parse → save → rules → fuzzy, посмотреть кандидатов на `/products/supplier?supplier_id=N`.
4. Вручную подтвердить первые 20-30 матчей, найти регрессии в гейтах (voltage, containment, transliteration сработают автоматически).
5. **НЕ запускать `apply_auto_discount.py` пока не согласовано** — каждый поставщик имеет свой `eur_rate_uah`.
6. Матч-правила (rule_matcher) добавляются вручную через UI или seed-скрипт.

## Критические исторические инциденты

- **2026-04-10** — тест стёр prod DB (см. #10 выше).
- **Session 8** — cross-brand matches проскакивали при пустом supplier.brand → фикс #4.
- **Session 9** — letter-space-digit, containment, transliteration — целая серия matcher bugs, каждый с регрессионным тестом.
- **Session 11+** — Neapolis 4 vs Neapolis false match из-за digit-only containment diff → фикс #9.

## Где искать актуальный статус

Roadmap, блокеры, backlog — в memory Клода: `project_labresta.md`, `project_labresta_feed_mgmt_plan.md`. Этот файл — только про инварианты, он меняется редко.

## Knowledge graph (graphify)

В корне есть `graphify-out/` — knowledge graph всего кода LabResta (1728 узлов, 4466 связей, 38 communities, AST-only без LLM). Используй его **прежде чем** многократно grep'ать или Read'ить большие куски кода.

**Когда обращаться к графу:**
- Архитектурный вопрос ("что использует `SupplierProduct`?", "как связаны `ProductMatch` и `AuditLog`?", "какие функции вызывают `find_match_candidates`?") — экономия токенов 50-70%
- Перед рефакторингом — посмотри god nodes и communities в `graphify-out/GRAPH_REPORT.md`, чтобы оценить blast radius
- Понять незнакомый модуль — открой граф, найди ноду, посмотри её связи

**Как обращаться:**
- Быстрый обзор: `graphify-out/GRAPH_REPORT.md` (god nodes, communities, surprising connections)
- Точечный запрос: `graphify query "вопрос"` (BFS по графу, ~локально, дешёво)
- Путь между концептами: `graphify path "ProductMatch" "AuditLog"`
- Объяснение ноды: `graphify explain "find_match_candidates"`

**Когда НЕ полагаться на граф:**
- Доменные/исторические вопросы ("почему phase K", "что было в session 9") — в графе их нет, в `.graphifyignore` исключены `.planning/`, `audit_*.md`, `RED_TODO.md`
- Дебаг конкретного теста — читай failure напрямую
- Вопрос про данные (БД, прайсы, импорт-файлы) — граф про код, не про данные

**Пересборка после изменений кода:** `graphify update .` (запускать из корня проекта; бесплатно, ~30 секунд, AST-only). Делать не нужно после каждого коммита, но полезно перед серьёзным рефакторингом.

**Что НЕ должно попадать в граф** (зафиксировано в `.graphifyignore`): `.env`, `instance/`, `*.db*`, `backups/`, `*.xlsx/*.xls/*.pdf`, `audit_*`, `red_*`, `np_*`, `.planning/`, `.claude/`, `claude-acc*.bat`, `reports/`, `logs/`. Если добавляешь что-то с секретами/клиентскими данными — обнови `.graphifyignore` ДО следующей пересборки.
