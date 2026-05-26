# PLAN — Рекуррентный фид НП: цена+наличие+ОПИСАНИЕ(UA+RU)+ГАЛЕРЕЯ ФОТО (без имени)

**Статус:** план, НЕ исполнять. Все скрипты/правки ниже — **спецификация**.
**Финальная схема (зафиксирована с Yana 2026-05-18):**
Отдельный **узкий YML-фид** для матченных НП-товаров 9 эксклюзивных брендов. Состав `<offer>`:
`id` + `vendorCode` + `price` + `currencyId` + `oldprice`(если есть скидка) + `available`
+ `<description>`(UA) + `<description_ru>` + `<picture>`×N (галерея).
**ИМЯ (`name`/`name_ru`) в фид НЕ входит** — ✅ ПОДТВЕРЖДЕНО Yana 2026-05-18
(«названия пока не добавляем в обновление»). «Пока» = решение текущее; узкий фид,
который мы сами формируем, тривиально позволяет добавить `<name>` позже одной строкой,
если понадобится — дизайн дверь не закрывает. Защита домена W1/W2; имена не цель этой
задачи; исключение полностью убирает timing-риск vs аудит перевода.
**Контроль безопасности — на уровне СОДЕРЖИМОГО фида**, не настройкой Horoshop:
имени в файле нет → перетереть имя физически нельзя; профиль Horoshop может быть «импортируй всё».
**Рекуррентно:** одна кнопка в UI (и/или плановый job) перегенерирует фид; стабильный URL не
меняется; Horoshop тянет тот же URL по расписанию.
**Безопасность процесса:** все артефакты — только `C:\Users\Yana\labresta-np-feed-plan\`.
Прод read-only, снимает Yana/по отмашке. Код пишется в репо **только после освобождения main
от воркера W1**. Полный live-импорт — только с явным go-ahead.

GATE пройден (FINDINGS.md): тело в фиде = ровно то, что на сайте; RU настоящий; галерея до 10 фото.

---

## Зафиксированные решения (2026-05-18)

| # | Что | Решение |
|---|-----|---------|
| Доставка | способ | Отдельный узкий фид (образец `sync_prices`/`sync_availability`), стабильный URL |
| Состав | поля offer | price + currencyId + oldprice + available + description(UA) + description_ru + picture×N |
| Имя | name/name_ru | **Исключено** ✅ подтв. Yana 2026-05-18 («пока не добавляем») — домен W1/W2; door open на потом |
| Цена/наличие | в этом фиде? | **Да**, как в основном post-match фиде |
| Фото | сколько | Вся галерея (`pp.image_url`=1-е, `pp.images` JSON=остальные) |
| Описание | языки | UA+RU обязательно, оба грузятся в Horoshop |
| Whitelist | какие товары | `custom_feed` (match_ids→token→стабильный URL); охват = scope 9 брендов и/или ручной выбор на `/matches` |
| Порядок | прогон | Сначала тест на 1 товаре (канарейка HKN-PICO12M) → масса матченных → хвост немтаченных |
| Рекуррентность | как | 1 кнопка UI + идемпотентная перегенерация; исчезновение из фида — существующий «Зниклі матчі» |
| Исчезновение | политика | НЕ новая: существующий механизм (sync_pipeline `last_seen_at`/`needs_review` → стр. «Кандидати на видалення з Horoshop»). Q-дрейф ЗАКРЫТ |
| Тайминг кода | vs W1 | Спек+мокап сейчас (вариант a); код+тест — после сигнала «main свободен» |
| Объём | прод-счёт | Локально ~370 матчено (ОК для дизайна); авторитет прода — на исполнении |

---

## Фаза 0 — Согласование (BLOCKING, без кода)

Большинство закрыто таблицей выше. Осталось подтвердить с Yana:
- 0.1 **Имя в фиде: исключаем?** — ✅ ЗАКРЫТО Yana 2026-05-18: «названия пока не
  добавляем в обновление». Фид без `name`/`name_ru`/`vendor`. «Пока» → пересмотрабельно,
  дизайн оставляет дверь открытой (добавить `<name>` в `sync_np_body` = 1 строка).
- 0.2 **Whitelist по умолчанию:** вся 9-брендовая scope-выборка одной кнопкой / ручной выбор
  на `/matches` / оба режима (мокап заложил оба).
- 0.3 **Хранение `description_ru` на sp:** новая колонка `SupplierProduct.description_ru`
  (рекомендация, аддитивная мини-миграция) ИЛИ write-through сразу в `pp.description_ru`.
- 0.4 4 точки UI-MOCKUP.md (меню/превью/лог пропущенных).
- 0.5 Сигнал «W1 закончил main» → старт кода Фазы 3.
- 0.6 Прод-снимок матчинга снимает Yana / read-only отмашка (Фаза 1, на исполнении).

---

## Фаза 1 — Авторитетный снимок сопоставления (read-only прод, на исполнении)

`snapshot_np_match.py` (spec; Yana/read-only): НП-фид × прод-БД (`supplier_id=2`,
`ProductMatch` confirmed/manual **`published=1`**) → `{np_article, pp_external_id, pp_brand,
has_desc_uk, has_desc_ru, photo_count}`. Фильтр 9 брендов (latin+cyr). Выход:
`np-match-snapshot.json` + `np-match-summary.md`. Сверить дельту с локальным (~370/690).
Только чтение.

---

## Фаза 2 — Бэкап (BLOCKING, до любой записи)

`backup_np_cards.py` (spec, read-only источник): по `pp_external_id[]` — ручная выгрузка
из админки Horoshop `backup/horoshop-cards-before-*.xlsx` (истина магазина) + read-only
прод-дамп PP (`description_ua/ru,image_url,images,name,price`) `backup/pp-before-*.json`.
`restore_np_cards_dryrun.py` (spec): собирает восстановительный фид «до», dry-run
валидация (схема/UTF-8/счёт/спот-чек 5), НЕ импортирует. Критерий: restore валиден +
ручной спот-чек Yana 3-5 карточек. Хранить до стабильного цикла + 30 дней.

---

## Фаза 3 — Код (отдельная ветка репо, ТОЛЬКО после освобождения main от W1)

Каждая правка — со своим регрессионным тестом (стиль инвариантов `CLAUDE.md`).

3.1 **`app/services/np_parser.py`** (spec; прецедент `app/services/rp_parser.py`):
парсит `np-feed.xlsx` — B=`article`, H=`description`(UA), Q=`description_ru`,
D→`image_url`(1-й URL)+`images`(JSON всех `;`-URL), J=`attr_brend_uk`→`brand`.
Цену/наличие НЕ парсит (их даёт текущий `parse_excel_products` путь — не дублировать).
Возвращает list[dict] совместимый с `save_supplier_products()` + ключи description/
description_ru/image_url/images. HTML тела как есть (`<br>`).

3.2 **Персистенция на `SupplierProduct`** (spec; см. SPEC-PHASE3.md §0/Ф3.2):
⚠ **уточнено чтением кода:** `feed_parser.save_supplier_products` УЖЕ персистит
description/image_url/images/params (feed_parser.py:169-180,194-197) с нужной
preserve-on-empty семантикой — **расширять для них НЕ надо**. Пробел только
`description_ru` (нет колонки). → решение 0.3 = новая колонка
`SupplierProduct.description_ru` + `scripts/migrate_add_sp_description_ru.py`
(`ALTER TABLE … ADD COLUMN description_ru TEXT`, идемпотентно) + 1 ветка-близнец
`description` в upsert. ⚠ Якорь обновления — `(supplier_id=2, article==B)`, НЕ
`external_id` (иначе дубль sp): тело пишет узкая `enrich_sp_bodies`, НЕ generic
`save_supplier_products` (на INSERT требует name/price — KeyError). Регрессия: др.
поставщики не ломаются (колонка NULL, аддитивно).

3.3 **`scripts/np_sync_bodies.py`** (spec; идемпотентный sp→pp): для `supplier_id=2`,
confirmed/manual/published, scope-бренды — `pp.description_ua←sp.description`,
`pp.description_ru←sp.description_ru`, `pp.image_url←sp.image_url`, `pp.images←sp.images`.
**Только эти 4 поля** (whitelist на уровне ORM-атрибутов). Если значение не изменилось —
не присваивать (нулевой дифф/нет записи в БД). `--dry-run` (default) дифф; `--apply` пишет.
Перезапись существующего тела/фото в pp = фид источник правды (подтверждено решением E).

3.4 **Новый узкий фид `sync_np_body(match_ids)`** в `yml_generator.py` (spec; собственный
offer-цикл по образцу `sync_prices`/`sync_availability` — НЕ через общий `_build_offer_xml`):
  - offer = `id`=pp.external_id, `vendorCode`, `price` (через `_compute_price_eur`),
    `currencyId`, `oldprice` (если retail>price), `available` (`_is_available_for_offer`),
    `<description>`=CDATA(pp.description_ua), `<description_ru>`=CDATA(pp.description_ru),
    `<picture>`=pp.image_url + по одному `<picture>` на каждый pp.images (дедуп с главным).
  - **БЕЗ `<name>`/`<name_ru>`/`<vendor>`** (решение «без имени»).
  - Под `if` — без фото нет пустых `<picture>`; без desc нет пустых тегов.
  - Регрессия: общий `_build_offer_xml` и существующие фиды не меняются ни на байт.

3.5 **Стабильный URL + регистрация** (spec): переиспользовать `custom_feed`
(`regenerate_custom_feed`/`custom_feed_token`, `models/custom_feed.py`) — но генерация
через `sync_np_body` вместо `_build_offer_xml`. Вариант: новая функция
`regenerate_np_body_feed(match_ids, name)` → файл `labresta-feed-npbody-<token>.yml`,
роут `/feed/yml/npbody/<token>` (или переиспользовать `/feed/yml/custom/<token>` с
отдельным реестром). Точную форму URL финализировать в Фазе 3 (спека). Token
детерминирован по match_ids → URL не протухает, повторная генерация перезаписывает файл.

3.6 **UI: меню + 1 кнопка** (spec; см. UI-MOCKUP.md): эндпоинт по образцу
`matches.py:regenerate_custom_feed`/`sync_prices` — POST `{match_ids|scope}` →
`regenerate_np_body_feed` → вернуть URL+состав. Кнопка «Згенерувати/оновити фід»,
превью состава, лог пропущенных (нет фото/нет ru/битый URL — валидация 3.7).

3.7 **Валидация фото-URL** (spec): HEAD/GET по фото (хотя бы дельта new/changed); 404/битые →
не писать в pp, лог в манифест/UI.

3.8 **Рекуррентность** (spec): `np_parser` подключить в `sync_pipeline.run_full_sync` для
`supplier_id=2` (текущий путь цены/наличия НЕ ломать) → после sync вызвать `np_sync_bodies`
→ перегенерация фида. Точку вызова (в pipeline vs scheduled job vs кнопка) финализировать.

**Выход:** ветка + зелёные регрессы + локальный dry-run-дифф. Прод/Horoshop НЕ трогались.

---

## Фаза 4 — Тест на 1 товаре (live, по отмашке)

Канарейка `HKN-PICO12M` (карточка уже = фид → чистый контроль; в фиде 2 фото, на сайте 1 →
2-е должно добавиться, тело не «прыгнуть», цена/наличие корректны, **имя не изменилось**).
`export_yml_subset`-аналог на 1 external_id → ngrok-тоннель (инв.#13) → Yana импортирует →
ручная проверка вживую. Дефект → откат `backup/restore-candidate.*`. Масса не стартует
пока 4.x не подтверждён письменно.

---

## Фаза 5 — Полный прогон по матченным scope-SKU (live, с go-ahead)

Свежий бэкап → переключить Horoshop на стабильный URL фида (уже содержит всех матченных
scope с price+avail+desc+gallery) → только матченные, немтаченные ≈320 не входят →
окно после прохода W1/W2 по chunk (#13) → пост-проверка `verify_np_body_applied.py`
(spec, read-only) + спот-чек Yana 5 карточек. `verify-after.md`.

---

## Фаза 6 — Стабилизация рекуррентного цикла

Расписание sync (частота — с Yana). 2-3 цикла на неизменном фиде → нулевой дифф
`np_sync_bodies` (контроль идемпотентности/нормализации/фото-дедупа). Дрейф фида
(new/changed/removed) корректен; removed → существующий «Зниклі матчі», тело pp НЕ зануляется.
Алерт на скачок числа изменяемых карточек.

---

## Фаза 7 — Хвост: немтаченные ≈320 (отдельно)

A1 (~100) bulk-confirm `/matches`; A2 (~105) баг pure-letter fast-path в matcher (фикс+тест);
бренды 0-каталога (Project Systems/Astoria/Maxima) — проверить написание бренда (Q10).
После доматчивания дельта сама попадает в рекуррентный цикл (3.3/3.8).

---

## Риски и откат

| Риск | Митигейшн |
|---|---|
| Фид перетирает имя/категорию | **Снято дизайном** — name в offer не эмитится; контроль на содержимом файла |
| Локальный снапшот ≠ прод | Фаза 1 read-only прод-снимок на исполнении |
| Код в main ломает W1 | Фаза 3 только после сигнала Yana (0.5); отдельная ветка |
| Битые фото-URL галереи | Фаза 3.7 HEAD/GET; битые → не писать, лог |
| Перезапись руками-правленого pp фидом | Решение E (фид=правда) + бэкап Фазы 2; тест-1 на уже-совпадающей карточке |
| Не идемпотентно (дифф на неизменном) | Фаза 6 — 2-3 контрольных цикла |
| Removed-артикул зануляет тело | Фаза 6/«Зниклі матчі» — тело НЕ занулять |
| Свет/отключка | Артефакты в план-каталоге; код атомарными коммитами в ветке |
| **Откат** | `backup/restore-candidate.*` (Фаза 2), проверен dry-run |

---

## Карта артефактов

```
C:\Users\Yana\labresta-np-feed-plan\ :
  np-feed.xlsx, np-probe-dump.txt, probe_np_feed.py        — есть (GATE)
  scratch_pico12m.txt, scratch_photo_dist.txt              — есть (сверки)
  PLAN.md, QUESTIONS.md, FINDINGS.md, UI-MOCKUP.md         — есть
  SPEC-PHASE3.md                                            — есть (код-уровень Ф3, read-only-выведено)
  snapshot_np_match.py/.json, np-match-summary.md          — Ф1 spec/выход
  backup_np_cards.py, restore_np_cards_dryrun.py, backup/  — Ф2
  verify_np_body_applied.py, verify-after.md               — Ф5
  import/                                                   — Ф4/5

Репо (ТОЛЬКО после освобождения main от W1, отдельная ветка):
  app/services/np_parser.py                          Ф3.1
  feed_parser.save_supplier_products (правка)         Ф3.2
  scripts/migrate_add_sp_description_ru.py            Ф3.2 (если решение 0.3=колонка)
  scripts/np_sync_bodies.py                          Ф3.3
  yml_generator.sync_np_body / regenerate_np_body_feed  Ф3.4-3.5 (новые, общий _build_offer_xml не трогать)
  views/matches.py эндпоинт + шаблон + пункт меню     Ф3.6
  sync_pipeline (правка, supplier_id=2)               Ф3.8
```

Скрипты/правки spec — **не запускать/не писать** в окне планирования.
