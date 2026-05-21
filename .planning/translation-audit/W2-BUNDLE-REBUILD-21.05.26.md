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
2. **Full bundle:** если TEST OK → загрузить `w2-horoshop-import-055-085.xlsx` (1248 SKU × 9 cols — см. v2 ниже).
3. Если что-то пойдёт не так → restore via `w2-horoshop-import-055-085.bak-21.05.26-pre-OQ-apply.xlsx` (старая версия до OQ apply) или `w2-horoshop-import-055-085.bak-21.05.26-4col-ru-only.xlsx` (предыдущий rebuild без UA).

---

## v2 expansion — 9 cols RU+UA (Yana ack 2026-05-21)

**Causa:** v1 содержал только 3 RU translation-cols, но W2 чистил и UA, и META keywords RU/UA. Yana pushback: «а что по укр столбцам?»

### Coverage check (всё на 2168 строк по 31 chunk)

| col | non_empty | changed | поле | в bundle? |
|---|---|---|---|---|
| c04 | 2168 | 3 | Название модификации (UA) | ✅ v2 |
| c05 | 2168 | 874 | Название модификации (RU) | ✅ v1+v2 |
| c06 | 2168 | 3 | Название (UA) | ✅ v2 |
| c07 | 2168 | 11 | Название (RU) | ✅ v1+v2 |
| c22 | **0** | 0 | HTML title (UA) | ⛔ всегда пусто |
| c23 | **0** | 0 | HTML title (RU) | ⛔ всегда пусто |
| c24 | 2168 | 0 | META keywords (UA) | ✅ v2 (write-through) |
| c25 | 2168 | **523** | META keywords (RU) | ✅ v2 |
| c26 | **0** | 0 | META description (UA) | ⛔ всегда пусто |
| c27 | **0** | 0 | META description (RU) | ⛔ всегда пусто |
| c28 | **0** | 0 | h1 (UA) | ⛔ всегда пусто |
| c29 | **0** | 0 | h1 (RU) | ⛔ всегда пусто |
| c35 | 2168 | **7** | Описание товара (UA) | ✅ v2 |
| c36 | 2168 | **1007** | Описание товара (RU) | ✅ v1+v2 |
| c37 | **0** | 0 | Короткое описание (UA) | ⛔ всегда пусто |
| c38 | **0** | 0 | Короткое описание (RU) | ⛔ всегда пусто |

**8/16 cells всегда пусты в W2 fixed.xlsx** — их НЕ включаем (Horoshop сотрёт).

### Schema v2 (9 cols)

```
c01 Артикул
c04 Название модификации (UA)
c05 Название модификации (RU)
c06 Название (UA)
c07 Название (RU)
c24 META keywords (UA)
c25 META keywords (RU)
c35 Описание товара (UA)
c36 Описание товара (RU)
```

### Stats v2

- written: **1248 строк × 9 cols** (vs v1 1009 строк × 4 cols)
- +239 строк восстановлено (где W2 правил UA/META, а RU был без изменений)
- skip_np: 115
- unchanged_vs_source: 805 (детекция по всем 8 trans cols)
- empty_filled_from_horoshop: 0
- row_excluded_empty_after_fallback: 0
- **0 пустых ячеек в bundle ✓**

### OQ apply v2 verification (13/13 PASS)

Проверены OQ #10, #11 (RU+UA), #12, #14, #15 (RU+UA), #17 — все токены present/absent как ожидалось.

### Backup tree

- `*.bak-21.05.26-pre-OQ-apply.xlsx` — оригинал до OQ apply (4 col RU-only)
- `*.bak-21.05.26-4col-ru-only.xlsx` — rebuild v1 (4 col RU-only post-OQ)
- `*.xlsx` (current) — rebuild v2 (9 col RU+UA post-OQ)
