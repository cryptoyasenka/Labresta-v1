# Matching Audit Report

**Generated:** prod snapshot
**Total PP:** 5683 | **Total SP:** 12881 | **Confirmed matches:** 2549 | **Rejected:** 33
**Dead suppliers excluded:** [1, 3]

## Summary table

| Cat | Description | Count | Risk | Action |
|-----|-------------|-------|------|--------|
| A | Exact-anchor gap (false neg) | 0 | HIGH conf | Visual check → bulk confirm |
| B | Sibling SKU gap (false neg) | 13 | MED | Per-row review |
| B-rev | PP-extends-SP (rare) | 9 | MED | Per-row review |
| C | Voltage mismatch in confirmed | 0 | HIGH risk | Unconfirm |
| D | Name divergence (overlap <30%) | 267 | MED risk | Visual check |
| E | M:1 violations | 0 | MUST FIX | Pick one |
| F | Short-anchor confirmed (<4 chars) | 0 | LOW risk | Spot-check |
| G | Rejected with exact anchor | 0 | review | Re-evaluate |
| H | Duplicate display_article | 11 | catalog | Merge/clean |

## Cat A — Exact-anchor gap (HIGH confidence false negatives)

PP без confirmed match де `pp.display_article == sp.article` точно. Це найбезпечніша категорія до bulk-confirm після візуальної перевірки. Колонка `dup` означає що display_article повторюється у каталозі (collision risk).

## Cat B — Sibling SKU gap (SP=anchor+suffix)

⚠ ОБЕРЕЖНО: suffix може означати реальний variant. Yana 2026-05-09: AD46DV ↔ AD46M = різні печі. Не сматчити автоматично.

### Apach — 3 шт.
  PP#1008 anchor='ad46d' name='Піч конвекційна Apach AD46D'
      → SP#5107 sup='Новый Проект' art='AD46DI ECO' fld='ad46dieco' suffix='ieco'
  PP#1341 anchor='ash05k' name='Апарат (шаф) шокового заморожування Apach ASH05K (NEW)'
      → SP#4634 sup='Новый Проект' art='ASH05K R290' fld='ash05kr290' suffix='r290'
  PP#3039 anchor='ahm250v250' name='Міксер погружний Apach AHM250V250'
      → SP#5106 sup='Новый Проект' art='AHM250V250C' fld='ahm250v250c' suffix='c'

### Fagor — 1 шт.
  PP#1741 anchor='afn801' name='Морозильна шафа FAGOR NEO CONCEPT AFN-801 (-18...-22°С, нерж.)'
      → SP#4916 sup='Новый Проект' art='AFN-801 EXP' fld='afn801exp' suffix='exp'

### Hurakan — 7 шт.
  PP#999 anchor='hkndhd10g' name='ДЕГІДРАТОР HURAKAN HKN-DHD10G'
      → SP#4602 sup='Новый Проект' art='HKN-DHD10GM' fld='hkndhd10gm' suffix='m'
  PP#1000 anchor='hkndhd16g' name='ДЕГІДРАТОР HURAKAN HKN-DHD16G'
      → SP#4604 sup='Новый Проект' art='HKN-DHD16GM' fld='hkndhd16gm' suffix='m'
  PP#1001 anchor='hkndhd12g' name='ДЕГІДРАТОР HURAKAN HKN-DHD12G'
      → SP#4603 sup='Новый Проект' art='HKN-DHD12GM' fld='hkndhd12gm' suffix='m'
  PP#3718 anchor='hkncfv60' name='Соковижималка для твердих HURAKAN HKN-CFV60'
      → SP#4637 sup='Новый Проект' art='HKN-CFV60M' fld='hkncfv60m' suffix='m'
  PP#3864 anchor='hknhbh850m' name='Блендер Hurakan HKN-HBH850M PRO COVER'
      → SP#4833 sup='Новый Проект' art='HKN-HBH850M PRO' fld='hknhbh850mpro' suffix='pro'
  PP#3891 anchor='hknblw2' name='Блендер Hurakan HKN-BLW2 grey'
      → SP#5092 sup='Новый Проект' art='HKN-BLW2 grey' fld='hknblw2grey' suffix='grey'
      → SP#4910 sup='Новый Проект' art='HKN-BLW2 red' fld='hknblw2red' suffix='red'
  PP#3918 anchor='hkntr65' name='Подрібнювач льоду HURAKAN HKN-TR65'
      → SP#4695 sup='Новый Проект' art='HKN-TR65M' fld='hkntr65m' suffix='m'

### Robot Coupe — 1 шт.
  PP#3599 anchor='28173' name='Диск для овочерізки Robot Coupe 28173'
      → SP#4709 sup='Новый Проект' art='28173W' fld='28173w' suffix='w'

### Sirman — 1 шт.
  PP#2967 anchor='tc12' name="М'ясорубка SIRMAN TC-12 E, 220 В"
      → SP#5134 sup='Новый Проект' art='TC 12 E / 230V 1PH non-C' fld='tc12e' suffix='e'

## Cat B-reverse — PP-extends-SP (rare, suspicious)

### Airhot — 1 шт.
  PP#54 anchor='ip3500d' name='Плита індукційна AIRHOT IP3500 D настільна'
      → SP#6704 sup='РП Україна' art=None pp_extra='d'
      → SP#6698 sup='РП Україна' art=None pp_extra='d'
      → SP#6699 sup='РП Україна' art=None pp_extra='d'

### Apach — 1 шт.
  PP#1007 anchor='ad46mv' name='Піч конвекційна Apach AD46MV'
      → SP#5096 sup='Новый Проект' art='AD46M ECO' pp_extra='v'

### Ceado — 1 шт.
  PP#3771 anchor='m98t' name='Міксер молочний CEADO M98T + насадка для кавових напоїв'
      → SP#5099 sup='Новый Проект' art='M98' pp_extra='t'

### Hurakan — 4 шт.
  PP#3131 anchor='hknip40fm' name='Міксер планетарний Hurakan HKN-IP40FM'
      → SP#4526 sup='Новый Проект' art='HKN-IP40F' pp_extra='m'
  PP#5394 anchor='hknwnc160cdw' name='Шафа холодильна для вина HURAKAN HKN-WNC160CDW'
      → SP#4957 sup='Новый Проект' art='HKN-WNC160CD' pp_extra='w'
  PP#5560 anchor='hknisv5p' name='Шприц ковбасний Hurakan HKN-ISV5P BLACK'
      → SP#4459 sup='Новый Проект' art='HKN-ISV5' pp_extra='p'
  PP#5578 anchor='hknisv5p' name='Шприц ковбасний Hurakan HKN-ISV5P BLACK'
      → SP#4459 sup='Новый Проект' art='HKN-ISV5' pp_extra='p'

### Sirman — 2 шт.
  PP#3108 anchor='66520502k12' name='Міксер занурювальний Sirman CICLONE 28 VT+ подрібнювач A35'
      → SP#4777 sup='Новый Проект' art='66520502' pp_extra='k12'
  PP#3109 anchor='66520502k12' name='Міксер занурювальний Sirman CICLONE 28 VT+ подрібнювач A25'
      → SP#4777 sup='Новый Проект' art='66520502' pp_extra='k12'

## Cat C — Voltage mismatch in confirmed (FALSE POSITIVE)

Confirmed matches where SP voltage tags ∩ PP voltage tags = ∅. Yana правило: 220 ↔ 380 = different SKU.

  (none)

## Cat D — Name divergence in confirmed (overlap <30%)

Confirmed де SP/PP назви майже не перетинаються. Можливий duplicate Horoshop card або wrong bind. Перевірити вручну.

  match#6222 ov=0.00 sup='Астим'  score=100.0
    PP#4297 "Кип'ятильник HENDI 209899, 20л (підходить для глінтвейну)"
    SP#13239 'Кипятильник - заварочна машина з одинарними стінками - 20 L - 230V / 2200W - 384x268x (H) '
  match#3678 ov=0.00 sup='Кодаки'  score=85.5
    PP#3862 'Блендер FROSTY 010'
    SP#5371 'Двигун для блендера BL-010Е'
  match#2397 ov=0.00 sup='Кодаки'  score=85.5
    PP#3194 'Куттер FROSTY HR-6'
    SP#5375 'Кутер HR- 6 (220 В)'
  match#6011 ov=0.00 sup='Астим'  score=100.0
    PP#1073 'Лист гладкий Hendi (GN1/1) 808429'
    SP#12497 'Деко для випічки GN 1/1 325x530 мм'
  match#6345 ov=0.00 sup='Астим'  score=100.0
    PP#3228 'Сыротерка Hendi 226827 для твердих сирів'
    SP#15823 'Сиротерка, 380 Вт'
  match#2398 ov=0.00 sup='Кодаки'  score=85.5
    PP#3195 'Куттер FROSTY HR-9'
    SP#5460 'Кутер HR- 9 (220 В)'
  match#6020 ov=0.00 sup='Астим'  score=100.0
    PP#4635 'Вакуумний пакувальник Hendi 970362'
    SP#11709 'Вакуум-пакувальна машина Profi Line 350 - безкамерна'
  match#2471 ov=0.00 sup='Кодаки'  score=63.41
    PP#1827 'Мінібар FROSTY BC-70'
    SP#5238 'Міні-бар BC- 70 black (220 В)'
  match#6164 ov=0.00 sup='Астим'  score=100.0
    PP#1271 'Решітка чавунна Hendi (GN1/1) 932018'
    SP#12474 'Ґрати чавунні GN 1/1'
  match#6480 ov=0.00 sup='Астим'  score=100.0
    PP#1844 'Холодильний мінібар Hendi 233900'
    SP#16956 'Шафа холодильна, 1-дверна,93 л, 500x500x(H)900 мм'
  match#6482 ov=0.00 sup='Астим'  score=100.0
    PP#1845 'Холодильний мінібар Hendi 233917'
    SP#16960 'Шафа холодильна, розсувні дверцята, 228 л, 900x500x(H)900 мм'
  match#6321 ov=0.00 sup='Астим'  score=100.0
    PP#4389 'Електрична млинниця Hendi 212028 однопостовая'
    SP#15444 'Поверхня для млинців одинарна - 230V / 3000W - 470x509x(H)161 mm'
  match#6012 ov=0.00 sup='Астим'  score=100.0
    PP#1072 'Перфорований лист Hendi (600х400) 808221'
    SP#12501 'Деко для випічки перфороване з антипригарним покриттям - 600 x 400 мм'
  match#6283 ov=0.00 sup='Астим'  score=100.0
    PP#5574 'Шприц ковбасний Hendi 282090'
    SP#14342 'Наповнювач фаршу Profi Line – вертикальний, 7 л'
  match#6284 ov=0.00 sup='Астим'  score=100.0
    PP#5591 'Шприц ковбасний Hendi 282083'
    SP#14343 'Наповнювач фаршу для ковбас, електричний, 15 л'
  match#6397 ov=0.00 sup='Астим'  score=100.0
    PP#989 'Дегідратор Hendi 229064'
    SP#16371 'Сушарка для харчових продуктів Kitchen Line - 7 підносів - 230V / 500W - 345x450x(H)315 mm'
  match#2445 ov=0.00 sup='Кодаки'  score=85.5
    PP#3196 'Куттер FROSTY HR-12'
    SP#5544 'Кутер HR-12 (220 В)'
  match#6106 ov=0.00 sup='Астим'  score=100.0
    PP#1704 'Гранитор 2х12 л Hendi 274224'
    SP#12427 'Гранітор 2x 12 л'
  match#6225 ov=0.06 sup='Астим'  score=100.0
    PP#4239 "Кип'ятльник HENDI 211106, 6л , подвійна стінка"
    SP#13238 'Кип&#39;ятильник - машина кавоварки з подвійними стінками - 6 L - 220-240V / 1500W - ø241x'
  match#6229 ov=0.07 sup='Астим'  score=100.0
    PP#800 'Інфрачервона лампа Hendi 273845'
    SP#13333 'Конічна лампа для підігріву страв з регульованою висотою - чорна- 230V / 250W - ø275x (H) '
  match#6398 ov=0.07 sup='Астим'  score=100.0
    PP#987 'Дегідратор Hendi 229033 (6 полиць)'
    SP#16372 'Сушарка для харчових продуктів Profi Line - цифрова панель управління, 6 полиць, 340x450x('
  match#6311 ov=0.07 sup='Астим'  score=100.0
    PP#930 'Низькотемпературна піч Hendi 225479'
    SP#15360 'Піч для приготування їжі  при низьких температурах  - 230V / 1200W - 495x690x(H)415 mm'
  match#3294 ov=0.07 sup='Новый Проект'  score=85.5
    PP#4494 'Посудомийна машина Apach AF500 DIG DD'
    SP#4958 'Посудомийка Apach AF500DIG DD фронтальна з дозатором миючого засобу електронна панель керу'
  match#6010 ov=0.08 sup='Астим'  score=100.0
    PP#1268 'Перфорований лист Hendi (600х400) 808214'
    SP#12496 'Деко для випічки - з тристоронньою відбортовкою, алюміній, 600x400 мм - перфорований'
  match#802 ov=0.08 sup='MARESTO'  score=100.0
    PP#4931 'Мийний засіб RATIONAL Self Cooking Center (100 шт./пач.)'
    SP#3237 'Таблетки миючі Rational 56.00.210 (упаковка)'
  match#6056 ov=0.09 sup='Астим'  score=100.0
    PP#4759 'Кисть кондитерська Hendi 515365, силіконова, плоска, 50x235 мм'
    SP#15036 'Пензлик кондитерський, силіконовий, плоский, 50x235 мм'
  match#6055 ov=0.09 sup='Астим'  score=100.0
    PP#4758 'Кисть кондитерська Hendi 515358, силіконова, плоска, 35x235 мм'
    SP#15035 'Пензлик кондитерський, силіконовий, плаский,  35x235 мм'
  match#6228 ov=0.09 sup='Астим'  score=100.0
    PP#1272 'Пароконвектомат Hendi 225929 (4xGN 2/3)'
    SP#13292 'Конвектомат мультифункціональний 4xGN 2/3 з паропарозволоженням - 230V / 3000W - 620x555x('
  match#6054 ov=0.09 sup='Астим'  score=100.0
    PP#4757 'Кисть кондитерская Hendi 515228, деревянная ручка - плоская, 20x210 мм, 2 шт.'
    SP#15033 'Пензлик кондитерський, плаский 20x210 мм, 2 шт.'
  match#6013 ov=0.10 sup='Астим'  score=100.0
    PP#1068 'Перфорований лист Hendi (GN1/1) 808405'
    SP#12516 'Деко перфороване для випічки GN1/1 325x530 мм'
  match#6068 ov=0.10 sup='Астим'  score=100.0
    PP#1071 'Перфорований лист Hendi (GN1/1) 808306'
    SP#12500 'Деко для випічки перфороване GN1/1 325x530 мм'
  match#6002 ov=0.10 sup='Астим'  score=100.0
    PP#3103 'Міксер який Hendi 224373 з вінчиком'
    SP#11606 'Блендер занурювальний Hendi 250 з регулюванням швидкості'
  match#6009 ov=0.10 sup='Астим'  score=100.0
    PP#1069 'Лист гладкий Hendi (600х400) 808207'
    SP#12495 'Деко для випічки - з тристоронньою відбортовкою, 600х400 мм'
  match#6031 ov=0.10 sup='Астим'  score=100.0
    PP#3621 'Диспенсер для буфету трьох-ярусний Hendi 428245'
    SP#11941 'Вітрина для фуршету – 3-х ярусна'
  match#6035 ov=0.10 sup='Астим'  score=100.0
    PP#2418 'Вітрина кондитерська 1,8 м HENDI 233467'
    SP#11973 'Вітрина холодильна з двома полицями, 610 л, 1815x675x (H) 1210 мм'
  match#6267 ov=0.10 sup='Астим'  score=100.0
    PP#4199 'Марміт HENDI 470619 модель Fiora GN 1/1, 9 л (чафингдиш)'
    SP#14070 'Марміт, підігрів паливою пастою - круглий, 3,5 л'
  match#6472 ov=0.10 sup='Астим'  score=100.0
    PP#2417 'Вітрина кондитерська 1,2 м HENDI 233450'
    SP#16847 'Холодильна вітрина з двома полицями, 410 л, 1215x675x(H)1210 мм'
  match#6449 ov=0.10 sup='Астим'  score=100.0
    PP#4478 'Тостер інфрачервоний Hendi 262214'
    SP#16666 'Тостер Milan-Toast + 6 затискачів для тостів, 3000 Вт'
  match#6107 ov=0.10 sup='Астим'  score=100.0
    PP#4332 'Вафельниця Hendi 212103 для бельгійських вафель'
    SP#11758 'Вафельниця 230V / 1500W - 320x437x(H)251 mm'
  match#6371 ov=0.11 sup='Астим'  score=100.0
    PP#4958 'Сковорода ø140 мм HENDI 627600'
    SP#15974 'Сковорода алюмінієва &quot;Marble Professional&quot;, Ø200x(H)45 мм'
  match#6372 ov=0.11 sup='Астим'  score=100.0
    PP#4959 'Сковорода ø180 мм HENDI 627617'
    SP#15975 'Сковорода алюмінієва &quot;Marble Professional&quot;, Ø240x(H)45 мм'
  match#6381 ov=0.11 sup='Астим'  score=100.0
    PP#4969 'Сковорода ø320 мм HENDI 838617'
    SP#15987 'Сковорода без кришки Kitchen Line, Ø320x(H)55 мм'
  match#6067 ov=0.11 sup='Астим'  score=100.0
    PP#1269 'Перфорований лист Hendi (GN2/3) 808313'
    SP#12499 'Деко для випічки GN2/3 354x325 мм'
  match#6379 ov=0.11 sup='Астим'  score=100.0
    PP#4967 'Сковорода ø240 мм HENDI 838501'
    SP#15985 'Сковорода без кришки Kitchen Line, Ø240x(H)45 мм'
  match#2852 ov=0.11 sup='Кодаки'  score=85.5
    PP#2883 'Тісторозкатка Frosty FDV-520'
    SP#5857 'Тісторозкатка для листкового тіста FDV520 (220 В)'
  match#6380 ov=0.11 sup='Астим'  score=100.0
    PP#4968 'Сковорода ø280 мм HENDI 838600'
    SP#15986 'Сковорода без кришки Kitchen Line, Ø280x(H)50 мм'
  match#6090 ov=0.11 sup='Астим'  score=100.0
    PP#4954 'Каструля 50 л HENDI 834701'
    SP#13099 'Каструля висока з кришкою Budget Line, 50 л, Ø400x(H)400 мм'
  match#6197 ov=0.11 sup='Астим'  score=100.0
    PP#4957 'Каструля 9 л HENDI 837306'
    SP#13102 'Каструля висока з кришкою Kitchen Line, 13,50 л, Ø280x(H)220 мм'
  match#2851 ov=0.11 sup='Кодаки'  score=82.45
    PP#2884 'Тісторозкатка Frosty FDV-520B'
    SP#5772 'Тісторозкатка для листкового тіста FDV520B (220 В)'
  match#2853 ov=0.11 sup='Кодаки'  score=85.5
    PP#2885 'Тісторозкатка Frosty FDV-630'
    SP#5942 'Тісторозкатка для листкового тіста FDV630 (220 В)'
  match#6202 ov=0.11 sup='Астим'  score=100.0
    PP#4956 'Каструля 9 л HENDI 837306'
    SP#13106 'Каструля висока з кришкою Kitchen Line, 9 л, Ø240x(H)200 мм'
  match#6402 ov=0.11 sup='Астим'  score=100.0
    PP#3472 'Тендерайзер Hendi 843451'
    SP#16504 'Тендерайзер Profi Line 51 лез 42x150x(H) 118 - червоний'
  match#6403 ov=0.11 sup='Астим'  score=100.0
    PP#3473 'Тендерайзер Hendi 843468'
    SP#16505 'Тендерайзер Profi Line 51 лез 42x150x(H)118 - білий'
  match#6199 ov=0.11 sup='Астим'  score=100.0
    PP#4986 'Каструля 20 л HENDI 837603'
    SP#13104 'Каструля висока з кришкою Kitchen Line, 20 л, Ø320x(H)270 мм'
  match#6200 ov=0.11 sup='Астим'  score=100.0
    PP#4982 'Каструля 37 л HENDI 832707'
    SP#13111 'Каструля висока з кришкою Profi Line, 37 л, Ø360x(H)360 мм'
  match#6404 ov=0.11 sup='Астим'  score=100.0
    PP#3474 'Тендерайзер Hendi 843468'
    SP#16506 'Тендерайзер Profi Line 51 лез 42x150x(H)118 - чорний'
  match#996 ov=0.11 sup='MARESTO'  score=100.0
    PP#4630 'ТЕРМОПАКУВАЛЬНИЙ АПАРАТ SIRMAN 45К СЕ'
    SP#4043 'Пакувальник "гарячий стіл" Sirman 45K (40602300)'
  match#6386 ov=0.11 sup='Астим'  score=100.0
    PP#4976 'Сотейник 5 л HENDI 838303'
    SP#16155 'Сотейник без кришки Kitchen Line, 5 л, Ø240x(H)115 мм'
  match#6477 ov=0.11 sup='Астим'  score=100.0
    PP#5623 'Чайник 1,8 л Hendi бездротовий 209981'
    SP#16896 'Чайник електричний  - 1,8 л - 230V / 2150W - 221x163x(H)249 mm'
  match#6091 ov=0.11 sup='Астим'  score=100.0
    PP#4983 'Каструля 71 л HENDI 834909'
    SP#13100 'Каструля висока з кришкою Budget Line, 71 л, Ø450x(H)450 мм'
  ... +207 more

## Cat E — M:1 violations (one PP claimed by multiple confirmed)

  (none — invariant holds)

## Cat F — Short-anchor confirmed (display_article <4 chars)

Низький ризик але worth spot-check — короткі коди типу M30/AK можуть співпасти випадково.

  (none)

## Cat G — Rejected with exact anchor (review operator decisions)

Match у status=rejected, але `sp.article == pp.display_article`. Можливо помилкове відхилення — варто переглянути.

  (none)

## Cat H — Duplicate display_article in catalog (merge candidates)

Той самий `display_article` присутній у кількох PP. Matcher Step 0a explicitly skips when there are 2+ collisions, тож матч не створюється — це блокує Cat A.

  disp='08300002000' (2 PPs):
    PP#3237 brand='Ozti' 'Кутер для хумуса OZTI SPM 20 FC'
    PP#3261 brand='Ozti' 'Кутер для хумуса OZTI SPM 70 FC'
  disp='203149' (2 PPs):
    PP#337 brand='Hendi' 'Поверхня для смаження Hendi 203149 гладка'
    PP#347 brand='Spidocook' 'Поверхня для смаження Spidocook SP300 склокериміка'
  disp='212004' (2 PPs):
    PP#4371 brand='FROSTY' 'Млинниця FROSTY VP-81'
    PP#4372 brand='FROSTY' 'Млинниця FROSTY VP-2Y40'
  disp='239766' (2 PPs):
    PP#78 brand='Hendi' 'Плита індукційна Hendi Вок 3500 Profi Line 239766'
    PP#80 brand='Fimar' 'Плита індукційна Fimar PFD27'
  disp='239780' (2 PPs):
    PP#29 brand='Hendi' 'Плита індукційна Hendi 239780 Kitchen Line'
    PP#154 brand='Roller Grill' 'Плита індукційна Roller Grill PIS 30'
  disp='240403' (2 PPs):
    PP#954 brand='Hendi' 'Рисоварка 5,4 л HENDI 240403'
    PP#958 brand='FROSTY' 'Рисоварка FROSTY RC-30'
  disp='271599' (3 PPs):
    PP#3932 brand='GoodFood' 'Льодоподрібнювач GoodFood ICE777'
    PP#3933 brand='FROSTY' 'Подрібнювач льоду Frosty IC80A'
    PP#3935 brand='Hendi' 'Подрібнювач для льоду Hendi 271599'
  disp='40752102p' (2 PPs):
    PP#3275 brand='Sirman' 'Овочерізка Sirman TM INOX (220) Normale'
    PP#3276 brand='Sirman' 'Овочерізка Sirman TM INOX з дисками (набір 1)'
  disp='40802852f' (2 PPs):
    PP#3439 brand='Sirman' 'Фаршеміс Sirman IP 20 M'
    PP#3455 brand='Sirman' 'Фаршемішалка Sirman IP 10 M'
  disp='66520502k12' (2 PPs):
    PP#3108 brand='Sirman' 'Міксер занурювальний Sirman CICLONE 28 VT+ подрібнювач A35'
    PP#3109 brand='Sirman' 'Міксер занурювальний Sirman CICLONE 28 VT+ подрібнювач A25'
  disp='860526' (2 PPs):
    PP#4160 brand='Hendi' 'Супниця 8 л Hendi 860526'
    PP#4179 brand='Saro' 'Супниця SARO SKZ-12'

---
END OF REPORT
