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
