# chunk-068 MANUAL REVIEW (W2)

**Status:** chunk-068 b1 DONE 8/50 (TRIP 4 + blknotrip 0 + blknochg 4 + SKIP-НП 0; OQ 0; 90 PASS) — следующий b2 (SKU 9-16, rows 10-17)
**Last updated:** chunk-068 b1 DONE 8/50

## Структура

- Источник: `chunk-068.xlsx` (RO)
- Operating target: `chunk-068-fixed.xlsx` (gitignored, скопирован из source при scaffold)
- Diff: `chunk-068-diff.md`
- Glossary: см. сводный `chunk-glossary-w2.md`
- Questions: `chunk-068-questions.md` (создаётся только при возникновении вопросов)

## Категории SKU (как в chunk-019/067)

- **TRIP (blk триплет):** c5==c4 UA-leak ИЛИ c35==c36 UA both → перевод c5←c7 + c36 faithful RU body skel==c35 / dims match
- **blknotrip:** c35!=c36 whitespace/skel-eq True (минор whitespace-only) → c5/c36 переписать с faithful skel c35
- **blknochg:** c5==c7 genuine RU + c36 genuine RU без UA-mark → НЕ трогаем
- **SKIP-НП:** brand ∈ {HURAKAN, APACH, FAGOR, TATRA, COLD, PROJECT SYSTEMS, ASTORIA, ARRIS, MAXIMA} → НЕ трогаем, тело из НП-фида позже

## Constraints (из chunk-067 carry-over)

- Без Ё в RU c36; UA `&#39;` → RU без апостр
- «тэн» через «э» (не «е», не «ё») — established in chunk-067 b7/b8
- Source typos faithful live (см. chunk-067: «конвеерный», «попа зливу», 1-мм dim variance)
- HTML entities preserved (`&mdash;`, `&ndash;`, `&Oslash;`, `&deg;`, `&#39;`)

## b1 (SKU 1-8, rows 2-9) — DONE 8/50

**Категории:** TRIP 4 + blknotrip 0 + blknochg 4 + SKIP-НП 0 = 8/8. Verify 90 PASS / 0 FAIL.

**TRIP (4) — Frosty посудомоечные/стакано-мойки:**
- r6 SKU5 ART 2080385348 **Frosty ECO35** Машина для мойки стаканов (бокалов): c5←c7 (`Машина для мойки стаканов (бокалов) Frosty ECO35`); c36 ← faithful RU body 25 строк (16-li main + 4-li комплект + 1-li материал; dims `30/350х350/276/2/1,5/9/3/55/2/4/2,70/220/430/485/660/30.00/1/1`; «миття» → «мойка», «келихів» → «бокалов», «корзин/год» → «корзин/час», «Об&#39;єм мийного бака» → «Объем моечного бака», «Опція: зливний насос» → «Опция: сливной насос», `&ordm;С` preserved).
- r7 SKU6 ART 2080393304 **Frosty ECO1000 3ph** Посудомоечная машина купольного типа: c5←c7; c36 24 строки (14-li main + 5-li комплект + 1-li материал; dims `60/20/15`, `1080/360/270` корзин/тарелок/час, `9,80` кВт/`380`В; «3 мийні цикли: 1/3 і 4 хв.» → «3 моечных цикла: 1/3 и 4 мин.», «Максимальний діаметр тарілок» → «Максимальный диаметр тарелок»).
- r8 SKU7 ART 2080397413 **Frosty ECO50 1ph** Посудомоечная машина фронтального типа: c5←c7; c36 27 строк (17-li main + 5-li комплект + 1-li материал; `<p><strong>Технические характеристики:</strong></p>`; dims `60/20`, `1080/360`, `3,40` кВт/`220`В; «2 мийні цикли: 1 хв і 3 хв» → «2 моечных цикла: 1 мин и 3 мин», «Вага: 60 кг» preserved «Вес: 60 кг»).
- r9 SKU8 ART 2080400876 **Frosty ECO50 3ph** Посудомоечная машина фронтального типа: c5←c7; c36 27 строк (same template как r8 но `6,65` кВт/`380`В + «Вага: 60.00» → «Вес: 60.00»; small variations «Допустимий тиск подачі води 2-4 бар» без двоеточия).

**blknochg (4) — fixed rows НЕ изменены:**
- r2 SKU1 ART 2045399173 **Empero EMP.500-380-SDF** Посудомоечная машина: c5==c7 RU OK, c36 без UA-mark, skel-eq True (len35=1388 / len36=1406).
- r3 SKU2 ART 2053905002 **Crystal CRW 500 TPD** Посудомоечная машина с помпой слива: c5==c7 RU OK, c36 без UA-mark, skel-eq True.
- r4 SKU3 ART 2053911972 **Crystal CRW 1000 TPD** Посудомоечная машина с помпой слива (купольная): c5==c7 RU OK, c36 без UA-mark, skel-eq True.
- r5 SKU4 ART 2054635608 **Adler EVO 1000 PD** Посудомоечная машина: c5==c7 RU OK, c36 без UA-mark, skel-eq True.

**SKIP-НП:** 0 в b1.

**OQ:** 0 новых открытых вопросов.

**Verify breakdown:** 50 ART regression + 4 TRIP × 7 checks (c4 untouched / c5==c7 / skel-eq / dims-eq / no UA / no Ё / nl-eq) = 28 + 4 blknochg × 3 checks (c4/c5/c36 unchanged vs RO) = 12. Total **90 PASS / 0 FAIL**.

