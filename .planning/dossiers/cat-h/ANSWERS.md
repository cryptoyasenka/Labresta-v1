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

### #8 — `40752102P`: Sirman TM INOX Normale vs з дисками (набір 1) ✅ RESOLVED (suffix-style 2026-05-13)

**Источник:** sirman.com подтверждает `40752102P` как базовый Sirman SKU. WebSearch + WebFetch на `torgoborud.com.ua/ua/.../ovocherizka-sirman-tm-inox-z-komplektom-diskiv` **подтвердил**: украинский магазин публикует тот же артикул `40752102P` для версии с комплектом дисків. **Sirman продаёт обе версии под одним SKU** — диски (DF3, DF8, DT3, PS8, DQ8) идут как accessories, отдельного SKU для bundle нет.

**Это значит:** PP#3275 и PP#3276 имеют одинаковый официальный Sirman артикул. Коллизия — внутренняя проблема labresta-каталога, не Sirman.

| PP | модель | новый `display_article` |
|---|---|---|
| **PP#3275** | TM INOX (220) Normale | `40752102P` — **правильный владелец, не трогать** (база) |
| **PP#3276** | TM INOX з дисками (набір 1) | `40752102P-K1` |

**Yana 2026-05-13:** выбран suffix-style по аналогии с #10 CICLONE. Базовый Sirman SKU `40752102P` остаётся как корень (для будущей привязки к feed'у Sirman/Maresto если появится), `-K1` (Komplekt 1) различает bundle для matcher Step 0a и для покупателя на карточке.

**История проверок:**
- sirman.com — официальный каталог не показывает отдельный SKU для bundle (Sirman продаёт диски как accessories)
- technofood.com.ua → `4557447739` (магазинный internal код, не Sirman)
- kiy-v.ua → нет 4075-кода, только модель
- primus-shop → 429 rate-limit
- np.com.ua прямой WebFetch → 403 Cloudflare (нужен логин-дилера, в `apach-missing-list.md` подтверждено что Yana видела портал руками)
- torgoborud.com.ua → `40752102P` (тот же базовый артикул)

### #9 — `40802852F`: Sirman IP 20 M vs IP 10 M ✅ RESOLVED

**Источник:** sirman.com официальный каталог (страница `/en-GB/food-processing/meat-processing/ip-20-m/40802852F` подтверждает + page показывает IP 10 M code).

| PP | модель | новый `display_article` |
|---|---|---|
| **PP#3439** | Sirman IP 20 M | `40802852F` — **правильный владелец, не трогать** |
| **PP#3455** | Sirman IP 10 M | `40802652F` (с sirman.com) |

Паттерн: `408028**52**F` (20kg) vs `408026**52**F` (10kg) — Sirman кодирует размер позицией 5-6.

### #10 — `66520502K1.2`: Sirman CICLONE 28 VT + A35 vs + A25 ✅ RESOLVED (suffix-style 2026-05-13)

**Источник:** sirman.com + premiumgastro.pl + mattysequipment.com.au подтверждают: `66520502` — официальный Sirman SKU для **базового** CICLONE 28 VT 250mm shaft. **A35/A25 — отдельные подрібнювачі** (Sirman не продаёт их как один SKU, это собственные комплекты labresta).

| PP | модель | новый `display_article` |
|---|---|---|
| **PP#3108** | CICLONE 28 VT + подрібнювач A35 | `66520502-A35` |
| **PP#3109** | CICLONE 28 VT + подрібнювач A25 | `66520502-A25` |

**Yana 2026-05-13:** выбран suffix-style. Базовый Sirman SKU `66520502` сохраняется как корень (для будущей привязки если появится в feed'е), `-A35`/`-A25` отличают комплекты для matcher Step 0a и для покупателя.

---

## 🔧 Что ещё могу сделать автономно

- [x] Прогнала `lookup_cat_h_wrong_owners.py` для всех 11 пар (commit будет ниже)
- [ ] WebFetch sirman.com для #8/#9/#10 — попробую сейчас по бренд-каталогу
- [ ] Не могу делать write в Horoshop (нужен Yana login + это live store)
- [ ] Не могу удалять PP в БД (это её решение через UI / Phase 8 workflow)

## 📌 Утром Yana

Открыть этот файл первым. **Все 11 кейсов закрыты** (10 прямых правок display_article + 1 deletion-candidates через UI). Пройти по таблицам сверху вниз в Horoshop CMS.

**Сводка финальных значений display_article:**

| # | PP | новый `display_article` | действие |
|---|---|---|---|
| 1 | PP#3237 Ozti SPM 20 FC | `0830.00020.00` | не трогать |
| 1 | PP#3261 Ozti SPM 70 FC | `0830.00070.02` | вписать |
| 2 | PP#347 Spidocook | (пусто) | очистить |
| 3a | PP#4371 FROSTY VP-81 | — | UI deletion |
| 3b | PP#4372 FROSTY VP-2Y40 | — | UI deletion |
| 4 | PP#80 Fimar | (пусто) | очистить |
| 5 | PP#154 Roller Grill | (пусто) | очистить |
| 6 | PP#958 FROSTY RC-30 | `000006797` | вписать |
| 7a | PP#3933 FROSTY IC80A | `000006955` | вписать |
| 7b | PP#3932 GoodFood ICE777 | (пусто) | очистить |
| 8a | PP#3275 Sirman TM INOX Normale | `40752102P` | не трогать |
| 8b | PP#3276 Sirman TM INOX з дисками | `40752102P-K1` | вписать |
| 9a | PP#3439 Sirman IP 20 M | `40802852F` | не трогать |
| 9b | PP#3455 Sirman IP 10 M | `40802652F` | вписать |
| 10a | PP#3108 CICLONE 28 + A35 | `66520502-A35` | вписать |
| 10b | PP#3109 CICLONE 28 + A25 | `66520502-A25` | вписать |
| 11 | PP#4179 Saro SKZ-12 | (пусто) | очистить |
