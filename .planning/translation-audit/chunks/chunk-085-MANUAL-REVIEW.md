# chunk-085 — Manual Review (W2)

**Источник:** `chunk-085.xlsx` (75 SKU, rows 2-76)
**Фиксы:** `chunk-085-fixed.xlsx`
**Бранч:** translation-audit/w2 (W2 — параллельный воркер, ФИНАЛЬНЫЙ chunk в диапазоне 055-085)
**Формат-эталон:** chunk-019 (категории blk триплет / blknotrip / blknochg / blkfix / SKIP-НП).

## Обзор

- 75 SKU rows 2..76
- **5 SKIP-НП preliminary (HURAKAN):** r3 (HKN-ISV5P шприц колбасный), r20 (HKN-ISH5P), r21 (HKN-ISV5P), r32 (HKN-ISV7P), r69 (HKN-EF16 чебуречница)
- Батч = 8 SKU; ожидается ~10 батчей (8×9 + 3 = 75)

## Категории

- **blk триплет** (TRIP): c5←c7 + c36 полный RU-перевод тела (c35==c36 source UA)
- **blknotrip**: c5←c7, тело c36 уже RU (без перевода)
- **blknochg**: c5==c7 genuine RU, c36 не менять
- **blkfix**: c5/c36 содержит UA остатки/typo → точечная правка
- **SKIP-НП**: бренд ∈ {HURAKAN, APACH, FAGOR, TATRA, COLD, PROJECT SYSTEMS, ASTORIA, ARRIS, MAXIMA} → ячейки не менять, тело из фида НП позже

## Прогресс

(заполняется по батчам)
