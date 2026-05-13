# Horoshop CMS — чек-лист правок Cat H (11 кейсов)

**Цель:** убрать коллизии `display_article` между разными брендами/моделями, чтобы matcher Step 0a больше не пропускал автоматч.

**Поле которое правим:** в карточке товара Horoshop оно называется **«Артикул на сайті»** (это `display_article` в нашей БД).

**Как открыть карточку в админке:** Horoshop admin → **Каталог → Товари** → в поиске вставить ссылку (или название из колонки «Что искать») → клик по строке → откроется редактор карточки. Поле «Артикул на сайті» обычно сверху в первой вкладке. После правки — **Зберегти**.

---

## ⚡ ОДИН РАЗ: подсказка по навигации

У каждой строки ниже есть ссылка на **публичную страницу товара**. Можешь сначала кликнуть, убедиться что это правильный товар (увидишь фото и название), потом в админке ищешь по slug из URL или по названию.

Slug = последняя часть URL после `labresta.com.ua/`. Например для `https://labresta.com.ua/kuter-dlia-khumusa-ozti-spm-20-fc/` slug = `kuter-dlia-khumusa-ozti-spm-20-fc`.

---

## 🟢 7 правок где поле НУЖНО ВПИСАТЬ конкретное значение

### #1a Ozti SPM 70 FC → `0830.00070.02`
- 🔗 https://labresta.com.ua/kuter-dlia-khumusa-ozti-spm-70-fc/
- Сейчас в поле «Артикул на сайті»: `0830.00020.00` (неправильно — это код SPM 20)
- Вписать: **`0830.00070.02`** (источник: Maresto feed SP#327)
- Сохранить

### #6 FROSTY RC-30 → `000006797`
- 🔗 https://labresta.com.ua/rysovarka-frosty-rc-30/
- Сейчас: `240403` (это код Hendi 5.4L)
- Вписать: **`000006797`** (источник: Кодаки SP#6504)
- Сохранить

### #7a FROSTY IC80A → `000006955`
- 🔗 https://labresta.com.ua/podribniuvach-lodu-frosty-ic80a/
- Сейчас: `271599` (это код Hendi)
- Вписать: **`000006955`** (источник: Кодаки SP#6316)
- Сохранить

### #8b Sirman TM INOX з дисками (набір 1) → `40752102P-K1`
- 🔗 https://labresta.com.ua/ovocherizka-sirman-tm-inox-z-dyskamy-nabir-1/
- Сейчас: `40752102P` (тот же что у базовой версии без дисков — коллизия)
- Вписать: **`40752102P-K1`** (K = Komplekt, 1 = набір 1)
- Сохранить

### #9b Sirman IP 10 M → `40802652F`
- 🔗 https://labresta.com.ua/farshemishalka-sirman-ip-10-m/
- Сейчас: `40802852F` (это код IP 20 M — больший)
- Вписать: **`40802652F`** (источник: sirman.com)
- Сохранить

### #10a Sirman CICLONE 28 VT + A35 → `66520502-A35`
- 🔗 https://labresta.com.ua/mikser-zanuriuvalnyi-sirman-ciclone-28-vt-podribniuvach-a35/
- Сейчас: `66520502K1.2`
- Вписать: **`66520502-A35`**
- Сохранить

### #10b Sirman CICLONE 28 VT + A25 → `66520502-A25`
- 🔗 https://labresta.com.ua/mikser-zanuriuvalnyi-sirman-ciclone-28-vt-podribniuvach-a25/
- Сейчас: `66520502K1.2` (та же коллизия что и #10a)
- Вписать: **`66520502-A25`**
- Сохранить

---

## 🧹 5 правок где поле НУЖНО ОЧИСТИТЬ (стереть, оставить пустым)

Почему чистим: Maresto/локальные feed'ы этих брендов не передают `<artikul>` — правильного значения у нас нет. Очистка снимает коллизию с Hendi и даёт нормальному match'у работать через имя+бренд.

### #2 Spidocook SP300
- 🔗 https://labresta.com.ua/poverkhnia-dlia-smazhennia-spidocook-sp300-sklokerymika/
- Сейчас: `203149` (это Hendi)
- Очистить поле «Артикул на сайті» (пусто)
- Сохранить

### #4 Fimar PFD27
- 🔗 https://labresta.com.ua/plyta-induktsiina-fimar-pfd27/
- Сейчас: `239766` (это Hendi)
- Очистить
- Сохранить

### #5 Roller Grill PIS 30
- 🔗 https://labresta.com.ua/plyta-induktsiina-roller-grill-pis-30/
- Сейчас: `239780` (это Hendi)
- Очистить
- Сохранить

### #7b GoodFood ICE777
- 🔗 https://labresta.com.ua/lodopodribniuvach-goodfood-ice777/
- Сейчас: `271599` (это Hendi)
- Очистить
- Сохранить

### #11 Saro SKZ-12
- 🔗 https://labresta.com.ua/supnytsia-saro-skz-12/
- Сейчас: `860526` (это Hendi)
- Очистить
- Сохранить

---

## 🗑️ #3 — НЕ в Horoshop, а в нашем UI

PP#4371 FROSTY VP-81 и PP#4372 FROSTY VP-2Y40 уже помечены `phase8_orphan` системой. В Horoshop **ничего не трогать**, только в нашем UI:

1. Открыть [localhost:5000/matches/deletion-candidates?tab=orphan](http://localhost:5000/matches/deletion-candidates?tab=orphan) (или прод-URL приложения)
2. Фильтр по бренду: **FROSTY**
3. Найти PP#4371 (VP-81) и PP#4372 (VP-2Y40)
4. По каждому нажать **«Видалено»** (или «Залишити» если решишь что нужны)

---

## ✅ Что НЕ трогать (оставить как есть)

Эти PP — правильные владельцы артикулов, ничего не правим:

- PP#3237 Ozti SPM 20 FC = `0830.00020.00` ✓
- PP#3275 Sirman TM INOX (220) Normale = `40752102P` ✓
- PP#3439 Sirman IP 20 M = `40802852F` ✓
- Все PP Hendi с этими артикулами (337/3859/2218 и т.д.) — оставить как есть, Hendi был законным владельцем

---

## После того как все правки в Horoshop сохранены

Скажи мне в чате «Cat H готово в Horoshop» — я обновлю TaskList (отмечу #1-11 как completed), запушу финальный коммит и мы перейдём к следующей задаче из бэклога (AD46 cleanup / Cat B sibling / Cat B-rev / Phase L smoke-test / Manual Astim review).
