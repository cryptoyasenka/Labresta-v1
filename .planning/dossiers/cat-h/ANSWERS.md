# Cat H — точные ответы (что вписать в display_article)

**Generated:** 2026-05-12 ночной авто-проход через `scripts/lookup_cat_h_wrong_owners.py`
**Method:** read-only prod-DB lookup в feed'ах поставщиков (Maresto / Кодаки / НП / Астим / Гудер / РП)
**Source of truth:** SP-записи в production-БД (для каждого WRONG-PP искала родной model-token в `supplier_products.name`)

---

## 🟢 Группа A — Hendi vs не-Hendi (7 правок)

| # | WRONG PP | бренд + модель | новый `display_article` | источник |
|---|---|---|---|---|
| 2 | **PP#347** | Spidocook SP300 | **очистить** (поле пустое) | Maresto SP#1896 не имеет artikul в feed |
| 4 | **PP#80** | Fimar PFD27 | **очистить** | Maresto SP#2357 не имеет artikul |
| 5 | **PP#154** | Roller Grill PIS 30 | **очистить** | в feed'ах нет вообще (орфан) |
| 6 | **PP#958** | FROSTY RC-30 | `000006797` | Кодаки SP#6504 ✓ существующий match#2617 |
| 7a | **PP#3933** | FROSTY IC80A | `000006955` | Кодаки SP#6316 ✓ существующий match#3663 |
| 7b | **PP#3932** | GoodFood ICE777 | **очистить** | в feed'ах нет (орфан) |
| 11 | **PP#4179** | Saro SKZ-12 | **очистить** | в feed'ах нет (орфан) |

**Важно про "очистить":**
- Spidocook/Fimar/Roller Grill/GoodFood/Saro: их Maresto/локальные feed'ы **не передают** `<artikul>`, поэтому правильного значения для display_article у нас нет. Очистка снимает коллизию с Hendi (Hendi сможет нормально матчиться через свой 100% Astim confirmed).
- Существующие matches (PP#347→SP#1896 Maresto, PP#80→SP#2357 Maresto, PP#958→SP#6504 Кодаки) останутся живы — они confirmed через `bulk:identical-name` или score-based, не зависят от display_article.

**Действие в Horoshop:** найти PP по ID (или page URL), в карточке поправить поле «Артикул на сайте» (display_article).

---

## 🟡 Группа B — same-brand model variants

### #1 — `0830.00020.00`: Ozti SPM 20 FC vs SPM 70 FC

**Анализ паттерна:**
- `0830.00020.00` — суффикс `00020` похож на «20» → правильный для **SPM 20**
- В Maresto feed SP#327: `Кутер Oztiryakiler SPM70 2SPD (0830.00070.02)` → артикул SPM 70 = `0830.00070.02`

**Вывод:**

| PP | бренд + модель | новый `display_article` |
|---|---|---|
| **PP#3237** | Ozti SPM 20 FC | `0830.00020.00` — **правильный, не трогать** |
| **PP#3261** | Ozti SPM 70 FC | `0830.00070.02` (взято из Maresto SP#327) |

### #3 — `212004`: FROSTY VP-81 vs VP-2Y40

**Оба** PP помечены `operator_decision='needs_delete'` (note `auto:phase8_orphan`) — Phase 8 уже квалифицировала их как orphans. Ни одного SP в feed'ах с токенами `VP-81` / `VP-2Y40` не найдено.

**Действие:** закрыть оба через `/matches/deletion-candidates?tab=orphan` → бренд FROSTY → «Видалено» по обоим.

### #8 — `40752102P`: Sirman TM INOX Normale vs з дисками (набір 1) ⚠️ PARTIAL

**Источник:** sirman.com `/ru-RU/.../vegetable-cutter/tm-inox/40752102P` + altekpro.ru показывают `40752102P 119983` для базового TM INOX 220V CE. **`40752102P` — официальный код базы.**

| PP | модель | новый `display_article` |
|---|---|---|
| **PP#3275** | TM INOX (220) Normale | `40752102P` — **правильный владелец** (база без комплекта дисков) |
| **PP#3276** | TM INOX з дисками (набір 1) | ❓ **код для версии с дисками не найден** — sirman.com не показывает отдельный SKU, np.com.ua вернул 403. Гипотеза: тот же `40752102P` + bundle на стороне магазина, или внутренний labresta-код для пакета. |

**Рекомендация Yana утром:** проверить np.com.ua вручную (логин дилера) — у них товар `/ovocherezka-tm-inox-s-komplektom-dyskov/` точно имеет какой-то код. Либо у Maresto спросить артикул "TM INOX + DSK". Если не найдётся — поставить пометку `40752102P-K1` (labresta-internal) у PP#3276 чтобы снять коллизию, или **очистить** display_article у одного из двух.

### #9 — `40802852F`: Sirman IP 20 M vs IP 10 M ✅ RESOLVED

**Источник:** sirman.com официальный каталог (страница `/en-GB/food-processing/meat-processing/ip-20-m/40802852F` подтверждает + page показывает IP 10 M code).

| PP | модель | новый `display_article` |
|---|---|---|
| **PP#3439** | Sirman IP 20 M | `40802852F` — **правильный владелец, не трогать** |
| **PP#3455** | Sirman IP 10 M | `40802652F` (с sirman.com) |

Паттерн: `408028**52**F` (20kg) vs `408026**52**F` (10kg) — Sirman кодирует размер позицией 5-6.

### #10 — `66520502K1.2`: Sirman CICLONE 28 VT + A35 vs + A25 ⚠️ DEFERRED

**Источник:** sirman.com + premiumgastro.pl + mattysequipment.com.au подтверждают: `66520502` — официальный Sirman SKU для **базового** CICLONE 28 VT 250mm shaft. **A35/A25 — отдельные подрібнювачі** (Sirman не продаёт их как один SKU, это собственные комплекты labresta).

| PP | модель | новый `display_article` |
|---|---|---|
| **PP#3108** | CICLONE 28 VT + подрібнювач A35 | предложение: `66520502-A35` (labresta-internal) или `66520502` без `K1.2` |
| **PP#3109** | CICLONE 28 VT + подрібнювач A25 | предложение: `66520502-A25` или другой |

`66520502K1.2` — labresta-internal маркировка пакета (не Sirman SKU). Решение полностью **за Yana** — она решит как разделять комплекты. Если у магазина нет нужды кодировать комплекты артикулом — можно **очистить** display_article у одного из двух.

---

## 🔧 Что ещё могу сделать автономно

- [x] Прогнала `lookup_cat_h_wrong_owners.py` для всех 11 пар (commit будет ниже)
- [ ] WebFetch sirman.com для #8/#9/#10 — попробую сейчас по бренд-каталогу
- [ ] Не могу делать write в Horoshop (нужен Yana login + это live store)
- [ ] Не могу удалять PP в БД (это её решение через UI / Phase 8 workflow)

## 📌 Утром Yana

Открыть этот файл первым. По нему пройти 7 правок Группы A + 2 в Группе B (Ozti #1) в Horoshop CMS. Для Группы B #3 — `/matches/deletion-candidates?tab=orphan` UI. Для #8/#9/#10 — ждать пока я не вернусь с sirman.com результатами (или сделать самостоятельно по знанию каталога).
