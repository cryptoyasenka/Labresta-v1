# W2 Horoshop import bundle rebuild — 2026-05-21

**Trigger:** Yana — после применения OQ #1-17 и закрытия W2 диапазона 055-085 нужна пересборка `w2-horoshop-import-055-085.xlsx`, чтобы Horoshop-import отражал OQ-правки. Старый bundle = `02:34`, его выгрузили до OQ apply (HEAD `b519497`) — устарел.

**Safety guard (Yana):** "проверь чтоб не было пустых ячеек в колонках — иначе в этом месте данные которые были на Horoshop сотрутся."

## Schema (без изменений — match prior bundle)

| Output col | Source chunk col | Horoshop col name |
|---|---|---|
| c01 Артикул | c01 | Артикул |
| c02 Название модификации (RU) | c05 | Название модификации (RU) |
| c03 Название (RU) | c07 | Название (RU) |
| c04 Описание товара (RU) | c36 | Описание товара (RU) |

RU-only, 4 столбца. UA-правки и SEO RU-поля (HTML title / META / h1 / short desc) — отдельный workflow, не в этом bundle.

## Sources

- 31 × `chunk-NN-fixed.xlsx` (`055..085`, 2168 строк суммарно)
- 31 × `chunk-NN.xlsx` (source, для unchanged-detection)
- `C:\Projects\labresta-sync\horoshop-export 21.05.26.xlsx` (5632 SKU, fresh today 11:42) — fallback для пустых ячеек

## Filters

- **SKIP-НП brand exclusion**: бренд ∈ {Hurakan, Apach, Fagor, Tatra, Cold, Project Systems, Astoria, Arris, Maxima} (exact match, case-insensitive; кириллица + латиница).
  - **Bug fix:** первая попытка использовала substring match — `"cold" in "tefcold"` → False-positive по Tefcold (7 SKU потеряны, включая OQ#14 r4 FSC100 и OQ#15 r6 UF50GCP). Заменено на exact equality.
- **Unchanged vs source exclusion**: если все 3 целевые ячейки fixed.xlsx (c5/c7/c36) идентичны source — строка пропускается (W2 не вносил правок → нечего импортировать).

## Empty-cell guard

Для каждой строки, для каждой из 3 RU-ячеек:
1. Если fixed.xlsx ячейка пуста → fallback к Horoshop export (sохраняем текущее живое значение)
2. Если и в Horoshop пусто → строка **исключается из bundle** (предотвращает wipe)

## Результат

- **1009 строк записано** (vs prior bundle 964 строки)
  - +45 SKUs восстановлены после fix substring-bug «Tefcold ≠ Cold»
- **Stats:**
  - total_seen: 2168
  - skip_np: 115 (post-fix; pre-fix было 275)
  - unchanged_vs_source: 1044
  - empty_filled_from_horoshop: 0
  - row_excluded_empty_after_fallback: 0
  - not_in_horoshop_warn: 0
  - **written: 1009**
- **0 пустых ячеек в bundle** ✓
- **0 fallback-кейсов** (все RU-поля корректно заполнены в fixed.xlsx) ✓
- **0 SKU отсутствует в Horoshop export** ✓

## OQ apply verification (spot check, 11/11 PASS)

| OQ | Chunk r ART | Token expected | Result |
|---|---|---|---|
| 10 | c080 r35 ART=2402036548 | `G-EF400GSS` present | ✓ |
| 11 | c081 r48 ART=908202884 | `BLACK` present, `VIP` absent | ✓ ✓ |
| 12 | c082 r35 ART=2043415778 | `68-168` present, `68-169` absent | ✓ ✓ |
| 14 | c084 r4 ART=2139145953 | `FSC100` present, `FS80CP` absent | ✓ ✓ |
| 15 | c084 r6 ART=2141730389 | `220-240V` present, `220-230V` absent | ✓ ✓ |
| 17 | c084 r39 ART=641916589 | `RT78B` present, `RT78L` absent | ✓ ✓ |

## Files

- `w2-horoshop-import-055-085.xlsx` ← НОВЫЙ bundle (gitignored)
- `w2-horoshop-import-055-085.bak-21.05.26-pre-OQ-apply.xlsx` ← backup старого (gitignored)
- `w2-horoshop-import-TEST-1.xlsx` ← 1 SKU sample для safe-mode импорта (1ое SKU из chunk-055)
- `_w2_rebuild_bundle.py` ← reproducible script (tracked в git)

## Next step (Yana)

1. **Safe-mode test:** загрузить `w2-horoshop-import-TEST-1.xlsx` в Horoshop через `/import` UI → проверить что 1 SKU обновился корректно (не сотерлось ничего лишнего) → визуально на сайте.
2. **Full bundle:** если TEST OK → загрузить `w2-horoshop-import-055-085.xlsx` (1009 SKU).
3. Если что-то пойдёт не так → restore via `w2-horoshop-import-055-085.bak-21.05.26-pre-OQ-apply.xlsx` (старая версия до OQ apply).
