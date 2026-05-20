# chunk-084 — Manual Review (W2)

**Источник:** `chunk-084.xlsx` (71 SKU, rows 2-72)
**Фиксы:** `chunk-084-fixed.xlsx`
**Бранч:** translation-audit/w2 (W2 — параллельный воркер)
**Формат-эталон:** chunk-019 (категории blk триплет / blknotrip / blknochg / blkfix / SKIP-НП).

## Обзор

- 71 SKU rows 2..72
- 0 SKIP-НП preliminary (no HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA detected in c4/c5)
- Батч = 8 SKU; ожидается ~9 батчей (8+8+8+8+8+8+8+8+7)

## Категории

- **blk триплет** (TRIP): c5←c7 + c36 полный RU-перевод тела (c35==c36 source UA)
- **blknotrip**: c5←c7, тело c36 уже RU (без перевода)
- **blknochg**: c5==c7 genuine RU, c36 не менять
- **blkfix**: c5/c36 содержит UA остатки/typo → точечная правка
- **SKIP-НП**: бренд ∈ {HURAKAN, APACH, FAGOR, TATRA, COLD, PROJECT SYSTEMS, ASTORIA, ARRIS, MAXIMA} → ячейки не менять, тело из фида НП позже

## Прогресс

(заполняется по батчам)


## b1 (SKU 1-8, rows 2-9) — DONE 8/71

**Категории:** blk триплет 0 / blknotrip 0 / blknochg 7 / blkfix 1 / SKIP-НП 0.

### blknochg (c5==c7 genuine RU, c36 unchanged)

- **r2** SKU=1 ART=2139115558 Tefcold FS80CP (настольный, 60 л, R600A) — c5==c7 RU clean, c36 RU полный (1165 chars).
- **r3** SKU=2 ART=2139127391 Tefcold SCU1220 — c5==c7 RU clean, c36 RU полный (1079 chars).
- **r4** SKU=3 ART=2139145953 Tefcold FSC100 — c5==c7 RU clean, c36 RU полный (1186 chars). **Замечание (OQ #14):** c35 UA и c36 RU body начинаются с "Шафа/Шкаф ... настільна/настольный FS80CP Tefcold..." — модель в прозе FS80CP, а c4/c5/c6/c7 = FSC100. Source typo (либо прозу скопировали с r2, либо c4-c7 ошибочно). Не правлено (blknochg forward-only).
- **r5** SKU=4 ART=2140074926 Tefcold VOC100 (холодильник для напитков) — c5==c7 RU clean, c36 RU полный (901 chars).
- **r7** SKU=6 ART=2141740167 Tefcold UF200V морозильный — c5==c7 RU clean, c36 RU полный (1166 chars).
- **r8** SKU=7 ART=2141746935 Tefcold UF200VS морозильный — c5==c7 RU clean, c36 RU полный (1145 chars).
- **r9** SKU=8 ART=2141750051 Tefcold UF100GCP морозильный — c5==c7 RU clean, c36 RU полный (1017 chars).

### blkfix (точечная правка c36 prose)

- **r6** SKU=5 ART=2141730389 Tefcold UF50GCP морозильный (48 л, R290, 154 Вт) — c5==c7 RU clean (no change), но c36 RU **начиналась с тела другого продукта** "Морозильный шкаф GoodFood RTD99L &ndash; профессиональное коммерческое..." (это body GoodFood RTD99L из chunk-083 r25). Specs list в c36 матчил c35 UF50GCP (R290, 48 л, 154 Вт), но prose-первый параграф contaminated. Переписан prose как faithful RU UA→RU c35: "Шкаф морозильный настольный UF50GCP Tefcold предназначен для кратковременного хранения, экспонирования и продажи продуктов." + полный список спеков. Новая длина c36: 908. **Замечание (OQ #15).**

### Открытые вопросы (новые в b1)

- **OQ #14 (W2 cum #14):** r4 SKU=3 Tefcold FSC100 — body prose (c35 UA + c36 RU faithfully translated) ссылается на модель "FS80CP" вместо "FSC100". Source feed contamination. Specs (60 л, +2..+10°C, R600A, 655×390×930, 46 кг) совпадают со специфическими параметрами FSC100, либо это дубликат body r2 FS80CP. Требует Yana подтверждения какая прозу-стартовая модель правильная.
- **OQ #15 (W2 cum #15):** r6 SKU=5 Tefcold UF50GCP — c36 RU исходно содержал body GoodFood RTD99L (chunk-083 r25). Translator copy-paste error / source contamination. Body переписан в b1 как faithful RU перевод c35. Yana может проверить точность нового RU prose.

**Verify:** 28 PASS / 0 FAIL.

**Cumulative chunk-084:** 8/71 (TRIP 0 / blknotrip 0 / blknochg 7 / blkfix 1 / SKIP-НП 0; 28 PASS / 0 FAIL).
