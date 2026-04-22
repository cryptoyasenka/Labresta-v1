# Сверка Лабреста Х.xlsx с БД

**Всего в файле: 178 товаров**

| Статус | Кол-во |
|---|---|
| ✅ Сматчено confirmed/manual | 163 |
| 🟡 Только candidate (нужен клик Confirm) | 2 |
| 🔴 SP есть, но нет match-строки (скорер не нашёл PP) | 7 |
| ⚫ Вообще нет как SP в БД (проблема фида?) | 6 |

---

## 🟡 Candidate — нужно подтвердить (2)

Эти товары уже есть как матчи-кандидаты. Просто открой и нажми Confirm.

- **IP-20F** (SP#4992) — МІКСЕР ПЛАНЕТАРНИЙ HURAKAN HKN-IP 20F НА 20 Л
  - [Открыть](http://127.0.0.1:5050/matches?supplier_id=2&status=candidate&search=IP-20F)
- **PSL730** (SP#5076) — ПОВЕРХНЯ ДЛЯ СМАЖЕННЯ HURAKAN HKN-PSL730 ГЛАДКА
  - [Открыть](http://127.0.0.1:5050/matches?supplier_id=2&status=candidate&search=PSL730)

---

## 🔴 SP есть, но нет match-строки (7)

Скорер не нашёл подходящий PP в каталоге — либо артикул в каталоге отличается, либо PP вообще нет.
Решение: пойти в UI, найти SP, нажать 'Сопоставить вручную' и поискать по имени.

- **C1** (SP#4966) — АПАРАТ ДЛЯ ПРИГОТУВАННЯ ЦУКРОВОЇ ВАТИ HURAKAN HKN-C1
  - Labresta URL (справочно): https://labresta.com.ua/aparat-dlia-pryhotuvannia-solodkoi-vaty-hurakan-hkn-c1/
  - [Найти SP в UI](http://127.0.0.1:5050/products/supplier?search=C1)
- **DHD10G** (SP#4602) — ДЕГІДРАТОР HURAKAN HKN-DHD10G
  - Labresta URL (справочно): https://labresta.com.ua/dehidrator-hurakan-hkn-dhd10g/
  - [Найти SP в UI](http://127.0.0.1:5050/products/supplier?search=DHD10G)
- **DHD12G** (SP#4603) — ДЕГІДРАТОР HURAKAN HKN-DHD12G
  - Labresta URL (справочно): https://labresta.com.ua/dehidrator-hurakan-hkn-dhd12g/
  - [Найти SP в UI](http://127.0.0.1:5050/products/supplier?search=DHD12G)
- **DHD16G** (SP#4604) — ДЕГІДРАТОР HURAKAN HKN-DHD16G
  - Labresta URL (справочно): https://labresta.com.ua/dehidrator-hurakan-hkn-dhd16g/
  - [Найти SP в UI](http://127.0.0.1:5050/products/supplier?search=DHD16G)
- **DL775** (SP#5067) — ЛАМПА ІНФРАЧЕРВОНА HURAKAN HKN-DL775, 190 ММ БРОНЗОВА
  - Labresta URL (справочно): https://labresta.com.ua/infrachervona-lampa-hurakan-hkn-dl775-bronzova-dlia-pidihrivu-strav/
  - [Найти SP в UI](http://127.0.0.1:5050/products/supplier?search=DL775)
- **DL800** (SP#5068) — ЛАМПА ІНФРАЧЕРВОНА HURAKAN HKN-DL800, 275 ММ БРОНЗОВА
  - Labresta URL (справочно): https://labresta.com.ua/infrachervona-lampa-hurakan-hkn-dl800-bronza-dlia-pidihrivannia-strav/
  - [Найти SP в UI](http://127.0.0.1:5050/products/supplier?search=DL800)
- **HM250** (SP#5106) — СЛАЙСЕР HURAKAN HKN-HM250. 250 ММ
  - Labresta URL (справочно): https://labresta.com.ua/slaiser-hurakan-hkn-hm250/
  - [Найти SP в UI](http://127.0.0.1:5050/products/supplier?search=HM250)

---

## ⚫ Нет как SP в БД вообще (6)

Эти товары в файле Лабреста Х есть, но в фиде поставщика (БД SP) отсутствуют.
Возможные причины: поставщик снял с фида, товар ignored, артикул в фиде другой.

- **IMF25-25** — ЛЬОДОГЕНЕРАТОР ЗАЛИВНОГО ТИПУ HURAKAN HKN-IMF25 25-30 КГ КУБИК
  - NP URL: https://np.com.ua/product/lodohenerator-zalyvnoho-typu-hurakan-hkn-imf25-25-30-kh-kubyk/
  - Labresta URL: https://labresta.com.ua/lodohenerator-hurakan-hkn-imf25-kubyk/
- **12CR-SCE** — М'ЯСОРУБКА  HURAKAN HKN-12(CR) SCE 170 КГ/ГОД
  - NP URL: https://np.com.ua/ru/product/myasorubka-170-kg-god-hkn-12cr-sce-2/
  - Labresta URL: https://labresta.com.ua/miasorubka-hurakan-hkn-12cr-sce/
- **DRT520** — ТІСТОРОЗКАТКА HURAKAN HKN-DRT520
  - NP URL: https://np.com.ua/ru/product/tiestoraskatka-hurakan-hkn-drt520/
  - Labresta URL: https://labresta.com.ua/tistorozkatka-hurakan-hkn-drt520/
- **DRF520** — ТІСТОРОЗКАТКА ПІДЛОГОВА HURAKAN HKN-DRF520
  - NP URL: https://np.com.ua/ru/product/testoraskatka-napolnaya-hurakan-hkn-drf520/
  - Labresta URL: https://labresta.com.ua/tistorozkatka-hurakan-hkn-drf520/
- **GX1410BNS-1400L** — ШАФА МОРОЗИЛЬНА HURAKAN HKN-GX1410BTS 1400 Л
  - NP URL: https://np.com.ua/ru/product/shkaf-morozylnyj-hurakan-hkn-gx1410bns-1400l/
  - Labresta URL: https://labresta.com.ua/shafa-morozylna-hurakan-hkn-gx1410bts/
- **ISV5P-BLACK** — ШПРИЦ ДЛЯ КОВБАС HURAKAN HKN-ISV5P BLACK , 5 л
  - NP URL: https://np.com.ua/ru/product/shprycz-dlya-kolbas-5-l-hkn-isv5p-black/
  - Labresta URL: https://labresta.com.ua/shpryts-kovbasnyi-hurakan-hkn-isv5p-black/2458/
