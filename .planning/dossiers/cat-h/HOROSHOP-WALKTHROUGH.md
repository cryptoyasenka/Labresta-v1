# Horoshop CMS — чек-лист правок Cat H (7 кейсов)

**Цель:** убрать коллизии `display_article` между Hendi и не-Hendi карточками, чтобы matcher Step 0a больше не пропускал автоматч из-за дубля артикула.

**Правило (Yana 2026-05-13):** правим **только** там где Hendi-артикул случайно попал в карточку другого бренда. Внутри-бренда коллизии (Ozti↔Ozti, Sirman↔Sirman, FROSTY↔FROSTY) **не трогаем** — там display_article это ручные коды Yana, и для Sirman/Ozti они могут совпасть с будущим feed'ом, когда поставщика подключим.

**Поле которое правим:** в карточке товара Horoshop оно называется **«Артикул на сайті»** (это `display_article` в нашей БД).

**Как открыть карточку в админке:** Horoshop admin → **Каталог → Товари** → в поиске вставить slug из URL (или название) → клик по строке → откроется редактор. Поле «Артикул на сайті» обычно сверху в первой вкладке. После правки — **Зберегти**.

**Почему чистим, а не вписываем своё значение:** Maresto/Кодаки/локальные feed'ы этих 7 брендов не передают `<artikul>` в YML — правильного значения для display_article у нас нет. Очистка снимает коллизию с Hendi, существующие matches остаются живы (они confirmed через `bulk:identical-name` или score, не зависят от display_article).

**Verification source:** `scripts/verify_cat_h_article_ownership.py` (read-only prod-DB lookup) подтвердил что все 7 артикулов ниже реально приходят из Астим (бренд-распределитель Hendi) — значит Hendi-карточки законные владельцы.

---

## 🧹 7 правок — ОЧИСТИТЬ поле «Артикул на сайті»

### #1 Spidocook SP300
- 🔗 https://labresta.com.ua/poverkhnia-dlia-smazhennia-spidocook-sp300-sklokerymika/
- Сейчас: `203149` (это Hendi Blue Line)
- **Очистить → пусто → Зберегти**

### #2 Fimar PFD27
- 🔗 https://labresta.com.ua/plyta-induktsiina-fimar-pfd27/
- Сейчас: `239766` (это Hendi Profi Line Вок)
- **Очистить → пусто → Зберегти**

### #3 Roller Grill PIS 30
- 🔗 https://labresta.com.ua/plyta-induktsiina-roller-grill-pis-30/
- Сейчас: `239780` (это Hendi)
- **Очистить → пусто → Зберегти**

### #4 FROSTY RC-30
- 🔗 https://labresta.com.ua/rysovarka-frosty-rc-30/
- Сейчас: `240403` (это Hendi рисоварка 5.4л)
- **Очистить → пусто → Зберегти**

### #5 FROSTY IC80A
- 🔗 https://labresta.com.ua/podribniuvach-lodu-frosty-ic80a/
- Сейчас: `271599` (это Hendi млин для льоду)
- **Очистить → пусто → Зберегти**

### #6 GoodFood ICE777
- 🔗 https://labresta.com.ua/lodopodribniuvach-goodfood-ice777/
- Сейчас: `271599` (это Hendi, тот же что у #5)
- **Очистить → пусто → Зберегти**

### #7 Saro SKZ-12
- 🔗 https://labresta.com.ua/supnytsia-saro-skz-12/
- Сейчас: `860526` (это Hendi супниця UNIQ)
- **Очистить → пусто → Зберегти**

---

## ✅ Что НЕ трогать (оставить как есть)

**Hendi-карточки** с этими артикулами — законные владельцы:
- PP#337 Hendi Blue Line поверхня (`203149`) ✓
- PP#3859 Hendi Profi Line Вок (`239766`) ✓
- PP#2218 Hendi плита (`239780`) ✓
- PP#? Hendi рисоварка 5.4л (`240403`) ✓
- PP#? Hendi млин для льоду (`271599`) ✓
- PP#? Hendi супниця UNIQ (`860526`) ✓

**Внутри-бренда коллизии — НЕ трогаем по правилу Yana 2026-05-13:**
- Ozti SPM 20 FC ↔ SPM 70 FC (`0830.00020.00`) — оба Ozti, ждём feed
- Sirman TM INOX Normale ↔ з дисками (`40752102P`) — оба Sirman, ждём feed
- Sirman IP 20 M ↔ IP 10 M (`40802852F`) — оба Sirman, ждём feed
- Sirman CICLONE + A35 ↔ + A25 (`66520502K1.2`) — оба Sirman, ждём feed
- FROSTY VP-81 ↔ VP-2Y40 (`212004`) — оба FROSTY, не Hendi-коллизия

> **Note про FROSTY VP-81/VP-2Y40:** обе карточки уже помечены системой `phase8_orphan`. Если решишь удалить — отдельно через `/matches/deletion-candidates?tab=orphan` → бренд FROSTY → «Видалено». Это **отдельная задача**, не часть Cat H walkthrough.

---

## После того как все 7 правок в Horoshop сохранены

Скажи мне в чате «Cat H готово в Horoshop» — обновлю TaskList (отмечу 7 пунктов completed), запушу финальный коммит, перейдём к следующей задаче из бэклога (AD46 cleanup / Cat B sibling / Cat B-rev / Phase L smoke-test / Manual Astim review).
