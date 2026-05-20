# chunk-068 MANUAL REVIEW (W2)

**Status:** scaffold 0/50 (batch=8 b1..b6 по 8 + b7=2 SKU = 50; rows 2..51; first ART 2045399173 / last ART 2434126712)
**Last updated:** chunk-068 scaffold (W2, продолжение chunk-067 ЗАКРЫТ 74/74)

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
