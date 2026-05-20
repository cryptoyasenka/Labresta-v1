# chunk-079 manual review (W2)

**Status:** chunk-079 b7 DONE 56/58 (cum TRIP 1 / blknotrip 0 / blknochg 55 / blkfix 0 / SKIP-НП 0; 505 PASS / 0 FAIL) — next b8 FINAL (SKU 57-58, rows 58-59, 2 SKU). 3 OQ (c079 #1 r12 FSC1000H; #2 r14 FSC1950S; #3 r46/r47 Tehma 3-door body=2-door).

## Параметры

- Source: `.planning/translation-audit/chunks/chunk-079.xlsx` (RO).
- Working copy: `.planning/translation-audit/chunks/chunk-079-fixed.xlsx` (gitignored).
- Range: 58 SKU rows 2..59. ART 2140760718..2046767826.
- Header row: c1 Артикул, c4 NM_UA, c5 NM_RU, c7 NAZV_RU, c35 DSC_UA, c36 DSC_RU.
- Распределение батчей: b1 rows 2-9 (SKU 1-8), b2 rows 10-17 (SKU 9-16), b3 rows 18-25 (SKU 17-24), b4 rows 26-33 (SKU 25-32), b5 rows 34-41 (SKU 33-40), b6 rows 42-49 (SKU 41-48), b7 rows 50-57 (SKU 49-56), b8 rows 58-59 (SKU 57-58, 2 финальный).

## SKIP-НП preliminary

- (пусто) — сканирование по brand-list дало 0 совпадений.

## Категории (определяются per-батч probe)

TRIP / blknotrip / blknochg / blkfix / SKIP-НП.

## OQ (chunk-079)

(пусто на момент scaffold)


## b1 (SKU 1-8, rows 2-9) — DONE 8/58

**Категории:** blk триплет 0 / blknotrip 0 / blknochg 8 / blkfix 0 / SKIP-НП 0.

### blknochg (c5==c7 genuine RU, c36 unchanged)

- **r2** SKU=1 ART=2140760718 Tefcold UR600SG — c5==c7 RU clean.
- **r3** SKU=2 ART=2140762562 Tefcold RK500SNACK — c5==c7 RU clean.
- **r4** SKU=3 ART=2140764901 Tefcold NC2500G — c5==c7 RU clean (c36 body упоминает «NC2500» без G — наследие источника, не наш write).
- **r5** SKU=4 ART=2140771607 Tefcold FS890H — c5==c7 RU clean.
- **r6** SKU=5 ART=2140773390 Tefcold FSC890S — c5==c7 RU clean.
- **r7** SKU=6 ART=2140774704 Tefcold FSC890H — c5==c7 RU clean.
- **r8** SKU=7 ART=2140777191 Tefcold RK710G — c5==c7 RU clean.
- **r9** SKU=8 ART=2140783030 Tefcold RKS600 — c5==c7 RU clean.

**Verify:** 72 PASS / 0 FAIL. Без новых OQ.


## b2 (SKU 9-16, rows 10-17) — DONE 16/58

**Категории:** blk триплет 0 / blknotrip 0 / blknochg 8 / blkfix 0 / SKIP-НП 0.

### blknochg (c5==c7 genuine RU, c36 unchanged)

- **r10** SKU=9 ART=2141128896 Tefcold FS1002S — c5==c7 RU clean.
- **r11** SKU=10 ART=2141131104 Tefcold FSC1000S — c5==c7 RU clean.
- **r12** SKU=11 ART=2141133910 Tefcold FSC1000H — c5==c7 RU clean (⚠ c35/c36 body упоминает «FSC1000S» вместо FSC1000H — наследие источника, источник переиспользовал описание sibling-SKU). ⇒ OQ c079 #1.
- **r13** SKU=12 ART=2141135512 Tefcold FS1202H — c5==c7 RU clean.
- **r14** SKU=13 ART=2141140987 Tefcold FSC1950S — c5==c7 RU clean (⚠ c35/c36 body упоминает «FS1202H» — описание sibling-SKU, не FSC1950S). ⇒ OQ c079 #2.
- **r15** SKU=14 ART=2141146470 Tefcold FSC1950H — c5==c7 RU clean.
- **r16** SKU=15 ART=2141154883 Tefcold FS1202S — c5==c7 RU clean.
- **r17** SKU=16 ART=2141159745 Tefcold ATOM MAXI C2DB — c5==c7 RU clean.

**Verify:** 72 PASS / 0 FAIL. 2 новых OQ.

### Открытые вопросы (новые)

- **OQ c079 #1**: r12 SKU=11 ART=2141133910 Tefcold **FSC1000H** — название (c4/c5/c7) указывает на FSC1000H, но тело описания (c35/c36) дословно идентично r11 FSC1000S и упоминает модель «FSC1000S» в первом предложении. Источник: ETL переиспользовал описание sibling-SKU. Не наш write. Решение Yana: либо переписать body под FSC1000H (нужен спец-лист модели), либо принять как есть.
- **OQ c079 #2**: r14 SKU=13 ART=2141140987 Tefcold **FSC1950S** — название указывает на FSC1950S, но тело описания (c35/c36) идентично r13 FS1202H и упоминает «FS1202H». Источник: cross-paste из соседнего SKU. Не наш write. Решение Yana: переписать body под FSC1950S или принять.


## b3 (SKU 17-24, rows 18-25) — DONE 24/58

**Категории:** blk триплет 0 / blknotrip 0 / blknochg 8 / blkfix 0 / SKIP-НП 0.

### blknochg (c5==c7 genuine RU, c36 unchanged)

- **r18** SKU=17 ART=2141162757 Tefcold FSC1200S — c5==c7 RU clean.
- **r19** SKU=18 ART=2141164488 Tefcold FSC1200H — c5==c7 RU clean.
- **r20** SKU=19 ART=2141165352 Tefcold NC5000G — c5==c7 RU clean (c36 body упоминает «NC5000» без G — наследие источника, тот же паттерн что r4 NC2500G).
- **r21** SKU=20 ART=2141167671 Tefcold GUC140 — c5==c7 RU clean (c36 «Шкаф холодильник» вместо «Шкаф холодильный» — наследие источника, не наш write).
- **r22** SKU=21 ART=2141173104 Tefcold FSC1000H BLACK — c5==c7 RU clean.
- **r23** SKU=22 ART=2141175210 Tefcold FSC1200H BLACK — c5==c7 RU clean.
- **r24** SKU=23 ART=2141177828 Tefcold RK1010 — c5==c7 RU clean.
- **r25** SKU=24 ART=2141180004 Tefcold FS1600H — c5==c7 RU clean.

**Verify:** 72 PASS / 0 FAIL. Без новых OQ.


## b4 (SKU 25-32, rows 26-33) — DONE 32/58

**Категории:** blk триплет 0 / blknotrip 0 / blknochg 8 / blkfix 0 / SKIP-НП 0.

### blknochg (c5==c7 genuine RU, c36 unchanged)

- **r26** SKU=25 ART=2141184019 Tefcold ATOM MAXI C3DB — c5==c7 RU clean.
- **r27** SKU=26 ART=2141187105 Tefcold FSC1600H — c5==c7 RU clean.
- **r28** SKU=27 ART=2141187732 Tefcold NC7500G — c5==c7 RU clean (c36 body «NC7500» без G — наследие, тот же паттерн что r4/r20).
- **r29** SKU=28 ART=2215585521 UBC Large 1200 л — c5==c7 RU clean.
- **r30** SKU=29 ART=2379537724 Ubc Energy AD — c5==c7 RU clean.
- **r31** SKU=30 ART=2492499126 Tefcold Atom Maxi C1DB — c5==c7 RU clean.
- **r32** SKU=31 ART=2492520954 Tefcold Atom Maxi C1DBB — c5==c7 RU clean.
- **r33** SKU=32 ART=907890667 Angelo Po AF1N (шкаф расстоечно-холодильный) — c5==c7 RU clean.

**Verify:** 72 PASS / 0 FAIL. Без новых OQ.


## b5 (SKU 33-40, rows 34-41) — DONE 40/58

**Категории:** blk триплет 1 / blknotrip 0 / blknochg 7 / blkfix 0 / SKIP-НП 0.

### TRIP (c5 ← c7; c36 ← faithful RU body)

- **r34** SKU=33 ART=1090576697 Tecnodom AF04EKOTN — c5 был UA «Шафа холодильна Tecnodom AF04EKOTN», c7 уже RU. Переписан c5→«Шкаф холодильный Tecnodom AF04EKOTN»; c36 переведён полностью с UA (был дубль c35): «Шкаф холодильный Tecnodom AF04EKOTN среднетемпературный с облицовкой из нержавеющей стали»; ТТХ — объем 400 л, глухие двери, цифровой дисплей, динамическое охлаждение, авторазмораживание, автоиспарение конденсата, 3 полки-решетки GN1/1 пласт., термоизоляция 50 мм, регулируемые ножки, 0..+10 °C, R404A, 700х620х1900, 0,385 кВт/220 В.

### blknochg (c5==c7 genuine RU, c36 unchanged)

- **r35** SKU=34 ART=1174595266 Samaref PF 700M TN нерж. — c5==c7 RU clean.
- **r36** SKU=35 ART=2379520133 Ubc Dynamic Plus — c5==c7 RU clean.
- **r37** SKU=36 ART=2493959296 Tecnodom AF14PKMTN290 — c5==c7 RU clean.
- **r38** SKU=37 ART=2106846233 Frosty FTD400SS — c5==c7 RU clean.
- **r39** SKU=38 ART=2106847262 Frosty FTD600SS — c5==c7 RU clean.
- **r40** SKU=39 ART=2239432973 GoodFood BC160BW2LED — c5==c7 RU clean.
- **r41** SKU=40 ART=2239439273 GoodFood BC160BW2LEDCOL — c5==c7 RU clean.

**Verify:** 73 PASS / 0 FAIL. Без новых OQ.


## b6 (SKU 41-48, rows 42-49) — DONE 48/58

**Категории:** blk триплет 0 / blknotrip 0 / blknochg 8 / blkfix 0 / SKIP-НП 0.

### blknochg (c5==c7 genuine RU, c36 unchanged)

- **r42** SKU=41 ART=2239461449 GoodFood BC360BW2LEDCOL — c5==c7 RU clean.
- **r43** SKU=42 ART=2239481157 GoodFood BC480BW2LEDCOL — c5==c7 RU clean.
- **r44** SKU=43 ART=507525747 Tehma двухдверный 1400х600 — c5==c7 RU clean.
- **r45** SKU=44 ART=507526237 Tehma двухдверный 1400х700 — c5==c7 RU clean.
- **r46** SKU=45 ART=676001802 Tehma трехдверный 1860х600 — c5==c7 RU clean (⚠ c36 body начинается «Двухдверный...» — generic body 2-door применён к 3-door модели). ⇒ OQ c079 #3.
- **r47** SKU=46 ART=676001803 Tehma трехдверный 1860х700 — c5==c7 RU clean (та же проблема — generic body 2-door для 3-door). ⇒ OQ c079 #3 (та же).
- **r48** SKU=47 ART=482287828 GGM KTS147ND#2T (-2…+8°С) 1,36х0,7 м — c5==c7 RU clean (c36 содержит «столGGM» без пробела — наследие источника).
- **r49** SKU=48 ART=676001805 Tehma четырехдверный 2320х600 — c5==c7 RU clean.

**Verify:** 72 PASS / 0 FAIL. 1 новый OQ (#3 покрывает r46/r47).

### Открытые вопросы (новые)

- **OQ c079 #3**: r46 ART=676001802 + r47 ART=676001803 Tehma **трёхдверные** холодильные столы (1860х600 / 1860х700) — c4/c5/c7 корректно указывают «трехдверный», но c36 body начинается «Двухдверный холодильный стол в стандартном исполнении...» — описание двухдверного стола применено к 3-door SKU. Источник: переиспользовал body sibling-модели (2-door). Не наш write. Решение Yana: либо «Двухдверный» → «Трёхдверный» (без Ё → «Трехдверный»), либо принять как generic body.

## b7 (SKU 49-56, rows 50-57) — DONE 56/58

**Категории:** blk триплет 0 / blknotrip 0 / blknochg 8 / blkfix 0 / SKIP-НП 0.

### blknochg (c5==c7 genuine RU, c36 unchanged)

- **r50** SKU=49 ART=676001806 Tehma четырехдверный 2320х700 — c5==c7 RU clean.
- **r51** SKU=50 ART=676001807 Tehma на 4 ящика 1400х700 — c5==c7 RU clean (c36 body «на 4 выдвижных ящика» вместо «ящиков» — наследие источника, не наш write).
- **r52** SKU=51 ART=676001808 Tehma на 6 ящиков 1860х700 — c5==c7 RU clean (c36 «на 6 выдвижных ящика» — наследие, как r51).
- **r53** SKU=52 ART=1499588290 Tehma на 4 ящика 1400х600 — c5==c7 RU clean (c36 «на 4 выдвижных ящика» — наследие).
- **r54** SKU=53 ART=1499593560 Tehma на 6 ящиков 1860х600 — c5==c7 RU clean (c36 «на 6 выдвижных ящика» — наследие).
- **r55** SKU=54 ART=530982358 Tefcold SA910-I — c5==c7 RU clean.
- **r56** SKU=55 ART=1861387206 Tefcold GS91 — c5==c7 RU clean (c36 «нержвеющей» вместо «нержавеющей» — опечатка источника, не наш write).
- **r57** SKU=56 ART=1861396318 Tefcold SA1365 S/S — c5==c7 RU clean.

**Verify:** 72 PASS / 0 FAIL. Без новых OQ.

