# SPEC-PHASE3 — код-уровневая спецификация Фазы 3 (НЕ исполнять до сигнала 0.5)

**Статус:** спецификация, построена read-only-чтением репо 2026-05-18. Код в репо НЕ
писался. Цель — сделать Фазу 3 почти механической, когда W1 освободит main (0.5).
Все ссылки на строки — снимок 2026-05-18; при старте Фазы 3 перепроверить (W1 мог сдвинуть).

Источники (прочитаны read-only): `app/services/rp_parser.py`,
`app/services/yml_generator.py` (1-130, 175-280, 330-465),
`app/services/feed_parser.py:120-225`, `app/models/supplier_product.py`.

---

## 0. Ключевое открытие — Ф3.2 МЕНЬШЕ, чем в PLAN.md

`feed_parser.save_supplier_products()` (feed_parser.py:120-224) **УЖЕ** персистит
`description`, `image_url`, `images`, `params` из dict — и на INSERT (строки 194-197),
и на UPDATE (строки 169-180), причём с нужной нам семантикой:

```python
new_description = p.get("description")
if new_description:                 # пустое/None из фида НЕ затирает существующее
    existing.description = new_description
# то же для image_url / images / params
```

→ Это **ровно** идемпотентное «фид-источник-правды, но частичный/битый фид не стирает
данные», которое нам нужно для рекуррентного цикла. **Патч `save_supplier_products`
для description/image_url/images НЕ нужен.** Остаётся единственный пробел —
`description_ru`: нет колонки в модели, нет ветки в upsert.

**Следствие:** Ф3.2 сворачивается к: (1) решение 0.3 + миграция `description_ru`;
(2) `np_parser` кладёт правильные ключи в dict; (3) +1 ветка в обеих половинах
upsert (INSERT и UPDATE) по образцу `description`.

---

## Ф3.1 — `app/services/np_parser.py` (новый файл)

**Образец 1:1 — `app/services/rp_parser.py`** (структура подтверждена чтением):
модульный docstring с «verified sheet shape» + инвариантами → helper-функции →
`parse_*(file_path, supplier_id) -> tuple[list[dict], list[str]]` (products, errors),
products совместимы с `save_supplier_products()`.

Сигнатура: `def parse_np_feed(file_path: str, supplier_id: int) -> tuple[list[dict], list[str]]`

Колонки НП-xlsx (FINDINGS §2, verified): A=`id`(внутр, НЕ ключ), **B=`Артикул`→`article`**
(якорь, = `SupplierProduct.article` для sup 2), H(idx7)=`description_uk`→`description`,
Q(idx16)=`description_ru`→`description_ru`, D(idx3)=`Фото` `;`-список →
`image_url`(1-й) + `images`(JSON всех), J(idx9)=`attr_brend_uk`→`brand`.

dict на строку (ТОЛЬКО поля тела+фото; цену/наличие/имя НЕ трогаем — их даёт
существующий excel_parser-путь, не дублировать):
```
{
  "supplier_id": supplier_id,
  "external_id": <тот же external_id, что генерит текущий excel_parser-путь>,  # см. ⚠ ниже
  "article":     <B Артикул>,
  "brand":       <J attr_brend_uk, _strip_country_suffix как в rp_parser>,
  "description":    <H description_uk, как есть с <br>>,
  "description_ru": <Q description_ru, как есть с <br>>,
  "image_url":   <1-й URL из D>,
  "images":      json.dumps([все URL из D.split(";"), trimmed, непустые]),
  # name/price/currency/available — НЕ включать (см. ниже)
}
```

⚠ **Контракт upsert — критично.** `save_supplier_products` матчит существующую sp по
`(supplier_id, external_id)` (UniqueConstraint `uq_supplier_product`, feed_parser.py:151-154).
Если `np_parser` положит `external_id` иной, чем основной НП-путь (excel_parser) — будет
СОЗДАН дубликат sp, а не обновлён нужный. **Решение:** `np_parser` НЕ создаёт записи; он
должен ДОобогащать существующие. Два безопасных варианта (финализировать в коде):
  (a) `np_parser` возвращает только `{supplier_id, external_id, description,
      description_ru, image_url, images}` — но `save_supplier_products` на INSERT
      требует `name`/`price_cents`/`available` (строки 183-198, прямой `p["name"]` —
      KeyError при отсутствии). → НЕ переиспользовать `save_supplier_products` напрямую
      для np_parser-дикта.
  (b) **Рекомендация:** отдельная узкая функция персистенции
      `enrich_sp_bodies(rows)` (НЕ `save_supplier_products`): по `(supplier_id=2,
      article==B)` находит существующую sp (она уже создана основным excel_parser-путём
      при обычном sync) и пишет ТОЛЬКО 5 полей тела/фото по образцу строк 169-180.
      Матч по `article`, не по `external_id` (у НП якорь — артикул B; external_id
      основного пути — это НП внутренний `id` из col A, нестабилен как ключ тела).
      Если sp не найдена (товар в НП-фиде есть, но основной путь его не завёл —
      немтаченный хвост) → в errors, в Фазе 7.

→ Ф3.1 + Ф3.2 объединяются: новый `np_parser.parse_np_feed` (читает) +
`np_parser.enrich_sp_bodies` ИЛИ `scripts/np_sync_bodies`-сторона (пишет sp). Точку
персистенции (внутри np_parser vs отдельная функция) финализировать в коде — обе
не трогают generic `save_supplier_products` (регрессия других поставщиков = 0).

Helpers переиспользовать из паттерна rp_parser: `_strip_country_suffix` (бренд),
`openpyxl.load_workbook(path, read_only=True, data_only=True)`, errors-список.

---

## Ф3.2 — колонка `SupplierProduct.description_ru` (решение 0.3)

Текущая модель (`app/models/supplier_product.py:31-34`):
```python
description = db.Column(db.Text, nullable=True)
image_url   = db.Column(db.String(500), nullable=True)   # Main picture from feed
images      = db.Column(db.Text, nullable=True)          # All picture URLs, JSON array
params      = db.Column(db.Text, nullable=True)
```
Нет `description_ru`. Рекомендация 0.3 = **новая колонка** (аддитивно, безопасно):

1. Модель: добавить строкой ниже `description`:
   `description_ru = db.Column(db.Text, nullable=True)  # RU body from NP feed`
2. `scripts/migrate_add_sp_description_ru.py` (одноразово, прецедент — др. `migrate_*.py`):
   `ALTER TABLE supplier_products ADD COLUMN description_ru TEXT;`
   SQLite ADD COLUMN nullable без default — безопасно/аддитивно, существующие строки
   получают NULL, другие поставщики не ломаются. Идемпотентность: проверить
   `PRAGMA table_info(supplier_products)` перед ALTER.
3. Персистенция: в `save_supplier_products` ИЛИ в узкой `enrich_sp_bodies` добавить
   ветку-близнец `description` (preserve-on-empty):
   ```python
   new_description_ru = p.get("description_ru")
   if new_description_ru:
       existing.description_ru = new_description_ru
   ```
   и в INSERT-ветке `description_ru=p.get("description_ru")`.

Регрессия: тест «другой поставщик (MARESTO) без description_ru — upsert не падает,
колонка NULL»; тест «повторный np-sync на неизменном фиде — 0 изменений в БД».

---

## Ф3.3 — `scripts/np_sync_bodies.py` (sp → pp, идемпотентно)

Прецедент стиля: `scripts/bulk_auto_confirm.py` (`--dry-run` default, `--apply`).
Логика: для `supplier_id=2`, `ProductMatch` status∈{confirmed,manual} & `published=1`,
бренд∈scope(9) → на каждой паре:
```
pp.description_ua = sp.description       # только если отличается
pp.description_ru = sp.description_ru
pp.image_url      = sp.image_url
pp.images         = sp.images
```
**Только эти 4 атрибута.** Присваивать ТОЛЬКО при реальном отличии (иначе нулевой
дифф/нет UPDATE — контроль идемпотентности Фазы 6). `--dry-run` (default) печатает
дифф (N карточек, какие поля), `--apply` коммитит + AuditLog. Перезапись руками-
правленого pp = фид-правда (решение Q-перезапись, дефолт — фид-правда; ждёт подтв.).

✅ Поля pp ПОДТВЕРЖДЕНЫ (read-only `app/models/catalog.py:20-23`, 2026-05-18):
`PromProduct.image_url`(String500,«Main photo»), `images`(Text,«Gallery URLs, JSON
array»), `description_ua`(Text), `description_ru`(Text) — имена 1:1 совпадают с sp-
стороной, трансляции не нужно. Маппинг Ф3.3/Ф3.4 в этом файле корректен как написан.

---

## Ф3.4 — `yml_generator.sync_np_body(match_ids)` (новый узкий фид)

**Шаблон 1:1 — `sync_prices` (yml_generator.py:339-401)**. Собственный offer-цикл,
НЕ `_build_offer_xml`. Переиспользуемые хелперы (все существуют, проверено):
`_query_published_matches(match_ids, supplier_ids)` (44-71, УЖЕ AND-комбинирует —
вызвать с `supplier_ids=[2]`), `_shop_skeleton()` →`(root, offers_el)` (175),
`_is_available_for_offer(match)` (190), `_compute_price_eur(match)` (200),
`is_valid_price`, `_write_xml_atomic(root, dir, filename)` (231).

Скелет (СПЕКА, не коммит):
```python
def sync_np_body(match_ids: list[int] | None = None) -> dict:
    matches = _query_published_matches(match_ids, supplier_ids=[2])
    root, offers_el = _shop_skeleton()
    synced, skipped = [], 0
    for match in matches:
        pp = match.prom_product
        sp = match.supplier_product
        if not is_valid_price(sp.price_cents):
            skipped += 1; continue
        is_av = _is_available_for_offer(match)
        price_eur = _compute_price_eur(match)
        retail_eur = (sp.price_cents or 0) / 100.0
        offer = etree.SubElement(offers_el, "offer",
                                 id=str(pp.external_id),
                                 available="true" if is_av else "false")
        etree.SubElement(offer, "vendorCode").text = str(pp.external_id)
        etree.SubElement(offer, "price").text = f"{price_eur:.1f}"
        if retail_eur > price_eur + 0.05:                      # как _build_offer_xml:104
            etree.SubElement(offer, "oldprice").text = f"{retail_eur:.1f}"
        cid = (sp.currency or "EUR") if sp.currency in ("EUR","UAH") else "EUR"
        etree.SubElement(offer, "currencyId").text = cid
        # --- тело (CDATA, как _build_offer_xml:112-117) ---
        if pp.description_ua:
            etree.SubElement(offer, "description").text = etree.CDATA(pp.description_ua)
        if pp.description_ru:
            etree.SubElement(offer, "description_ru").text = etree.CDATA(pp.description_ru)
        # --- галерея ---
        pics = []
        if pp.image_url: pics.append(pp.image_url)
        if pp.images:
            try: pics += [u for u in json.loads(pp.images) if u]
            except (ValueError, TypeError): pass
        seen = set()
        for u in pics:                       # дедуп, главное фото первым
            if u in seen: continue
            seen.add(u)
            etree.SubElement(offer, "picture").text = u
        # БЕЗ <name>/<name_ru>/<url>/<vendor>  (решение 0.1, подтв. Yana)
        synced.append(match.id)
    out = _write_xml_atomic(root, current_app.config["YML_OUTPUT_DIR"], <filename>)
    return {"total": len(synced), "skipped": skipped, "path": out, ...}
```
Регрессия (fence): тест «`_build_offer_xml` байт-в-байт не изменился»;
тест «sync_np_body НЕ эмитит `<name>`/`<name_ru>`/`<url>`/`<vendor>`»;
тест «галерея: image_url + images, дедуп, главное первым»;
тест «нет описания → нет пустого `<description>`»; тест «нет фото → нет `<picture>`».

---

## Ф3.5 — стабильный URL

Переиспользовать `custom_feed_token(match_ids)` (yml_generator.py:74, детерминирован
sha256 sorted set [:12]) + реестр `CustomFeed`. Новая `regenerate_np_body_feed(
match_ids, name)` = аналог `regenerate_custom_feed`, но генерит через `sync_np_body`,
файл `labresta-feed-npbody-<token>.yml`, роут `/feed/yml/npbody/<token>` (валидация
`_TOKEN_RE=^[0-9a-f]{12}$` как существующая, против path-traversal). Альтернатива —
тот же `/feed/yml/custom/<token>` с флагом «npbody» в реестре; форму финализировать
в коде. Токен детерминирован → URL не протухает, перегенерация перезаписывает файл.

---

## Ф3.6 — UI (эндпоинт + кнопка + меню)

Эндпоинт — образец `views/matches.py:regenerate_custom_feed` (POST `{match_ids|scope}`
→ функция → JSON `{url, count, skipped, log}`). Кнопка/меню/превью — UI-MOCKUP.md.
Лог пропущенных = errors из np_parser + skipped из sync_np_body + Ф3.7.

## Ф3.7 — валидация фото-URL
HEAD/GET по дельте new/changed фото; 4xx/5xx/timeout → не писать в pp, в лог-манифест.
Не блокирует тело (текст и фото независимы).

## Ф3.8 — рекуррентность
`np_parser.parse_np_feed` + `enrich_sp_bodies` подключить в `sync_pipeline.run_full_sync`
для `supplier_id=2` ПОСЛЕ существующего `parse_excel_products` (line ~166; основной путь
заводит sp с name/price/available — НЕ ломать; np-обогащение идёт вторым шагом, по
`article`). Затем `np_sync_bodies` → `regenerate_np_body_feed`. Точку (pipeline vs job
vs только кнопка) финализировать; дефолт — в pipeline после save, идемпотентно.

---

## Чек-лист старта Фазы 3 (когда 0.5 придёт)
1. Перепроверить номера строк (W1 мог сдвинуть): `_build_offer_xml`, `sync_prices`,
   `save_supplier_products`, модели SupplierProduct/PromProduct. (Имена полей pp —
   уже подтверждены, см. Ф3.3 ✅; перепроверить лишь, что W1 их не переименовал.)
2. Ветка от свежего main. Каждая правка + регрессионный тест (стиль инвариантов CLAUDE.md).
3. Порядок: миграция → модель → np_parser+enrich → np_sync_bodies → sync_np_body →
   regenerate_np_body_feed → роут → UI → pipeline-hook. Атомарные коммиты.
4. Локальный dry-run-дифф на `instance/labresta.db?mode=ro`-копии. Прод/Horoshop НЕ трогать.
