# Article-Anchor Rule Verification

**Total confirmed/manual matches:** 2549

## Summary

- ✅ Three-way anchor (display_article == sp.article AND in name/pp.article): **487**
- ✅ Two-way (no display_article but article in name + sp.article): **417**
- ⚠ Rule violations (display_article == sp.article but NOT in name/pp.article): **4**
- ℹ No article-anchor at all (fuzzy / mismatched / manual): **1641**

## ⚠ Rule violations (auto-confirmed but anchor missing from name)

These 4 confirmed matches violate the three-location rule.
They should have stayed in 'candidate' status pending manual review.

### Астим — 2 шт.
  match#6611 status=confirmed score=100.0 anchor='zcze1996951'
    PP#935 disp='Z CZE1996951' pp.article=None
      name   = 'Тирса (тріска) для копчення Hendi (250 гр)'
      name_ru= 'Опилки для копчения Hendi (150 гр)'
    SP#16693 art='Z CZE1996951'
      name   = 'Тріска для копчення - дуб, 150 г'
  match#6383 status=confirmed score=100.0 anchor='695906'
    PP#3708 disp='695906' pp.article=None
      name   = 'Соковижималка (прес) для цитрусових Hendi'
      name_ru= 'Соковыжималка (пресс) для цитрусовых Hendi'
    SP#16150 art='695906'
      name   = 'Соковитискач для цитрусових, 225x180x510(H) мм'

### Новый Проект — 2 шт.
  match#1100 status=confirmed score=100.0 anchor='66110302'
    PP#3086 disp='66110302' pp.article=None
      name   = 'Міксер занурювальний Sirman STORM VV'
      name_ru= 'Миксер погружной Sirman STORM VV'
    SP#4776 art='66110302'
      name   = 'Міксер ручний Sirman Storm VV з насадкою блендер 160 мм'
  match#1102 status=confirmed score=100.0 anchor='66530502'
    PP#3101 disp='66530502' pp.article=None
      name   = 'Міксер погружний Sirman CICLONE 36 VT з насадкою блендер 350 мм'
      name_ru= 'Миксер погружной Sirman CICLONE 36 VT с насадкой блендер 350 мм'
    SP#4773 art='66530502'
      name   = 'Міксер ручний Sirman Ciclone 36 VT з насадкою блендер 350 мм'

## ℹ No article-anchor at all (fuzzy/manual confirmed)

### display_article='10273302' != sp.article='MIRRA 275 CE' — 1 шт.
  match#1330 sup='Новый Проект' score=100.0
    PP#3351 disp='10273302' 'Слайсер Sirman MIRRA 275 CE'
    SP#4802 art='MIRRA 275 CE' 'Слайсер Sirman Mirra 275 CE'

### display_article='240403' != sp.article='000006797' — 1 шт.
  match#2617 sup='Кодаки' score=95.0
    PP#958 disp='240403' 'Рисоварка FROSTY RC-30'
    SP#6504 art='000006797' 'Рисоварка RC-30 (220 В)'

### display_article='271599' != sp.article='000006955' — 1 шт.
  match#3663 sup='Кодаки' score=73.55
    PP#3933 disp='271599' 'Подрібнювач льоду Frosty IC80A'
    SP#6316 art='000006955' 'Льодоподрібнювач IC80A (220 В)'

### display_article='69100002' != sp.article='SOFTCOOKER XP' — 1 шт.
  match#3805 sup='Новый Проект' score=100.0
    PP#925 disp='69100002' 'Апарат Sous Vide SIRMAN SOFTCOOKER XP (Y09) (термопроцесор)'
    SP#4896 art='SOFTCOOKER XP' 'Апарат низькотемпературного приготування Sirman Softcooker XP'

### display_article='70-KPP1' != sp.article='000006436' — 1 шт.
  match#3654 sup='Кодаки' score=100.0
    PP#51 disp='70-KPP1' 'Плита індукційна FROSTY 70-KPP1 настільна'
    SP#6068 art='000006436' 'Плита індукційна 70-KPP1 (220 В)'

### display_article='9016' != sp.article='000009016' — 1 шт.
  match#2853 sup='Кодаки' score=85.5
    PP#2885 disp='9016' 'Тісторозкатка Frosty FDV-630'
    SP#5942 art='000009016' 'Тісторозкатка для листкового тіста FDV630 (220 В)'

### display_article='AF-32R/120' != sp.article='000005975' — 1 шт.
  match#2527 sup='Кодаки' score=100.0
    PP#1942 disp='AF-32R/120' 'Лопата для піци Gi Metal AF-32R/120'
    SP#6310 art='000005975' 'AF-32R/120 Лопата для піци'

### display_article='AF-37R/120' != sp.article='000005977' — 1 шт.
  match#3645 sup='Кодаки' score=100.0
    PP#1943 disp='AF-37R/120' 'Лопата для піци Gi Metal AF-37R/120 Aurora'
    SP#6394 art='000005977' 'AF-37R/120 Лопата для піци'

### display_article='AF-41R/120' != sp.article='000005978' — 1 шт.
  match#2529 sup='Кодаки' score=100.0
    PP#1944 disp='AF-41R/120' 'Лопата для піци Gi Metal AF-41R/120'
    SP#6477 art='000005978' 'AF-41R/120 Лопата для піци'

### display_article='AF-45R/120' != sp.article='000005979' — 1 шт.
  match#3646 sup='Кодаки' score=100.0
    PP#1945 disp='AF-45R/120' 'Лопата для піци Gi Metal AF-45R/120 Aurora'
    SP#5210 art='000005979' 'AF-45R/120 Лопата для піци'

### no display_article + no name hit — 583 шт.
  match#3634 sup='Кодаки' score=82.61
    PP#1370 disp=None 'Стіл для піци FROSTY PS903 холодильний'
    SP#5829 art='000005766' 'Стіл для піци PS903 (220 В)'
  match#2560 sup='Кодаки' score=95.0
    PP#5000 disp=None 'Диспенсер для пластівців Frosty JVD-5'
    SP#5740 art='000006191' 'Диспенсер для пластівців JVD-5'
  match#2561 sup='Кодаки' score=95.0
    PP#4999 disp=None 'Диспенсер для пластівців Frosty JVT-5'
    SP#5825 art='000006192' 'Диспенсер для пластівців JVT-5'
  match#2729 sup='Кодаки' score=95.0
    PP#5466 disp=None 'Шафа барна Frosty GN320HS'
    SP#6014 art='000008388' 'Шафа барна GN320HS (220 В)'
  match#3705 sup='Кодаки' score=86.62
    PP#5537 disp=None 'Шафа холодильна Frosty RT-78B-1 Black'
    SP#6199 art='000009075' 'Шафа холодильна RT-78B-1, black (220 В)'
  match#2293 sup='Кодаки' score=95.0
    PP#1960 disp=None 'Лопата для піци квадратна Gi Metal A-37R/120'
    SP#6176 art='000000621' 'A-37R/120 Лопата для піци квадратна'
  match#2294 sup='Кодаки' score=95.0
    PP#1965 disp=None 'Лопата для піци кругла Gi Metal A-41/120'
    SP#5294 art='000000623' 'A-41/120 Лопата для піци кругла'
  match#2295 sup='Кодаки' score=95.0
    PP#2055 disp=None 'Лопата для піци кругла Gi Metal A-50/120'
    SP#5379 art='000000626' 'A-50/120 Лопата для піци кругла'
  match#2710 sup='Кодаки' score=95.0
    PP#1722 disp=None 'Фризер STAFF BFX 600A для твердого морозива'
    SP#5415 art='000008023' 'Фризер для твердого морозива BFX  600A (380 В)'
  match#2656 sup='Кодаки' score=95.0
    PP#1344 disp=None 'Апарат (шафа) шокового заморожування Frosty BCF60'
    SP#6171 art='000007337' 'Апарат шокового заморожування BCF60 (220 В)'
  ... +573 more

### supplier has no article — 1048 шт.
  match#438 sup='MARESTO' score=100.0
    PP#962 disp=None 'Рисоварка REEDNEE SA8236 (8 л)'
    SP#3554 art=None 'Рисоварка REEDNEE SA8236'
  match#439 sup='MARESTO' score=100.0
    PP#963 disp=None 'Рисоварка REEDNEE SB8155 (10 л)'
    SP#3555 art=None 'Рисоварка REEDNEE SB8155'
  match#809 sup='MARESTO' score=100.0
    PP#2804 disp=None 'Тістоміс Alimacchine SM10FM'
    SP#2045 art=None 'Тістоміс Alimacchine SM10FM'
  match#810 sup='MARESTO' score=100.0
    PP#2805 disp=None 'Тістоміс Alimacchine SM10VET2V'
    SP#2049 art=None 'Тістоміс Alimacchine SM10VET2V'
  match#815 sup='MARESTO' score=100.0
    PP#2696 disp=None 'Тістоміс LP Group VIS80 + решітка з нерж. сталі + ЭПУ'
    SP#2061 art=None 'Тістоміс LP Group VIS80 + решітка з нерж. сталі + ЭПУ'
  match#817 sup='MARESTO' score=100.0
    PP#2809 disp=None 'Тістоміс Pizza Group IR17VS , 17 літрів, варіатор швидкості'
    SP#1641 art=None 'Тістоміс Pizza Group IR17VS'
  match#1089 sup='MARESTO' score=100.0
    PP#3247 disp='2117' 'Кухонний процесор Robot Coupe R211XL Ultra + 2 диски (Куттер/Овочерізка)'
    SP#1180 art=None 'Кухоний процесор Robot Coupe R211XL ULTRA (220) + 2 диска'
  match#3104 sup='РП Україна' score=100.0
    PP#4407 disp=None 'Апарат для попкорну AIRHOT POP-6'
    SP#6640 art=None 'Апарат для попкорну AIRHOT POP-6'
  match#3105 sup='РП Україна' score=100.0
    PP#4378 disp=None 'Млинниця AIRHOT BE-1'
    SP#6690 art=None 'Млинниця AIRHOT BE-1'
  match#956 sup='MARESTO' score=100.0
    PP#3402 disp=None 'Картоплечистка EWT INOX X6D'
    SP#3514 art=None 'Картоплечистка EWT INOX X6D'
  ... +1038 more

