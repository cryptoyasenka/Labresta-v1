# Global UA term sweep: `жаркова|жарильна|смарочна` → `жарочна`

**Дата:** 2026-05-15 (ночной режим)
**Триггер:** в chunk-005 (griddles) обнаружено `жаркова`/`жарильна`/`смарочна` как UA-варианты — locked term по гайду Yana 2026-05-14 = `жарочна`. Глобальный sweep по `horoshop-export 13.05.26.xlsx` 5632 SKU.

## Сводка по chunk'ам

| chunk | hits | поля | статус |
|-------|------|------|---|
| 005 | 23 | META UA + Опис UA/RU | ✅ применено в `chunk-005-diff.md` (точечно через batches SKU 33-48 + SKU 73-84) |
| 006 | 2 | Опис UA | ⏳ inherit-at-audit |
| 007 | 4 | Опис UA/RU | ⏳ inherit-at-audit |
| 008 | 1 | META UA | ⏳ inherit-at-audit |
| 060 | 5 | Опис UA/RU | ⏳ inherit-at-audit |
| 061 | 1 | Опис UA/RU | ⏳ inherit-at-audit |
| 062 | 1 | Опис UA | ⏳ inherit-at-audit |
| 066 | 3 | Опис UA/RU | ⏳ inherit-at-audit |
| 075 | 6 | META UA | ⏳ inherit-at-audit |

**Total:** 46 rows w/ hits across 9 chunks. 23 уже зафикшены в chunk-005-diff.md.

## Артикулы для inherit-at-audit (вне chunk-005)

### chunk-006 (2 SKU)
- 524323432 — Опис UA
- 524323433 — Опис UA

### chunk-007 (4 SKU)
- 524338456 — Опис UA+RU
- 524825369 — Опис UA
- 781296769 — Опис UA+RU
- 1122669838 — Опис UA+RU (`Жаркова` capitalized)

### chunk-008 (1 SKU)
- 1131875858 — META UA

### chunk-060 (5 SKU)
- 421477548, 421477549, 421477550, 421477552, 421477553 — Опис UA+RU (vendor family, same fix pattern)

### chunk-061 (1 SKU)
- 421477551 — Опис UA+RU (часть той же vendor family)

### chunk-062 (1 SKU)
- 421619025 — Опис UA

### chunk-066 (3 SKU)
- 470824217, 470824365 — Опис UA+RU
- 1973306904 — Опис UA

### chunk-075 (6 SKU)
- 1149685697, 2074266783, 2074276047, 2074284298, 2074290168, 2074302923 — META UA (vendor batch typo, same fix pattern)

## Правило, которое нужно применять при аудите этих chunk'ов

1. UA `жаркова` (любой регистр) → `жарочна` (locked term Yana 2026-05-14).
2. UA `жарильна` → `жарочна` (single-word vs double-word нюанс не различаем — поверхня жарочна).
3. UA `смарочна` → `жарочна` (typo, скорее всего автозамена `сма`+`жа` спутала).
4. **НЕ трогать** RU описания, если RU=полный валидный перевод (`жарочная` уже корректное русское слово). Менять только UA или RU-кальку с UA-typo.
5. Apply key = Артикул. Scope per row.

## Откуда rule

Per `feedback_labresta_ua_ru_translation_rules.md` + scopes locked в chunk-001/-002/-003/-004 retro фиксов. Подтверждено Yana 2026-05-14 → переплыло в правила.

---

**Last updated:** 2026-05-15
