# STATE AUDIT — план «навести порядок в состоянии»

**Создан:** 2026-05-21
**Драйвер:** Yana, выбрала option «Навести порядок в состоянии» после Horoshop recovery
**Блокер сейчас:** ждём fresh LIVE export от Yana (она экспортит вручную завтра)

---

## Цель

Один документ `.planning/STATE-AUDIT/STATE-SUMMARY.md` с тремя срезами для каждой пары (SKU, колонка):
1. **PRE-INCIDENT** — `horoshop-export 20.05.26.xlsx` (16:08 до битого импорта 22:29)
2. **INTENDED** — что МЫ хотели: chunks 016-029 fixed.xlsx + 3 fix files (mod-name-b, desc-ru, desc-ua)
3. **LIVE NOW** — свежий export от Yana (см. блокер ниже)

Каждая ячейка получает флаг:
- ✅ `OK` — LIVE = INTENDED
- 🟡 `STALE` — LIVE = PRE-INCIDENT (правка из chunks НЕ дошла до LIVE)
- 🔴 `WIPED` — LIVE пуста (битый импорт стёр, не восстановили)
- 🟠 `WRONG` — LIVE отличается и от INTENDED и от PRE-INCIDENT (что-то третье)
- ⚪ `UNTOUCHED` — мы это поле никогда не правили (контроль)

## Скоп

~1500 SKU где мы как-либо касались:
- 943 SKU из `horoshop-import-2026-05-20.xlsx` (битый импорт)
- 17 SKU Track #1 mod_name recovery (commit `0c15219`)
- 4 SKU Track #2 residual recovery (3 PASS + 1 TATRA pending)
- ~600 SKU из chunks 016-029 fixed.xlsx (объединение)
- ⚠ остальные 4100+ SKU — НЕ в скопе (только контрольный сэмпл ~50 для sanity check)

## Inputs

| Файл | Где лежит | Что даёт |
|---|---|---|
| `horoshop-export 20.05.26.xlsx` | `C:\Projects\labresta-sync\` | PRE-INCIDENT, 5632 SKU |
| `horoshop-import-2026-05-20.xlsx` | `C:\Projects\labresta-sync\` | Что битый импорт залил (943 SKU) |
| `horoshop-fix-mod-name-2026-05-21-b.xlsx` | `C:\Projects\labresta-sync\` | Track #1b restore (1 SKU) |
| `horoshop-fix-desc-ru-2026-05-21.xlsx` | `C:\Projects\labresta-sync\` | Track #2 desc(RU) restore (2 SKU) |
| `horoshop-fix-desc-ua-2026-05-21.xlsx` | `C:\Projects\labresta-sync\` | Track #2 desc(UA) restore (1 SKU TATRA — НЕ ИМПОРТИРОВАН) |
| `chunks/chunk-{016..029}-fixed.xlsx` | `.planning/translation-audit/chunks/` | Translation work product |
| **`horoshop-export-2026-05-21-postrecovery.xlsx`** | **ОЖИДАЕТСЯ ЗАВТРА от Yana** | LIVE NOW (свежий export) |

## Outputs

```
.planning/STATE-AUDIT/
├── STATE-SUMMARY.md         # топ-уровень dashboard: счётчики по флагам, top-issues
├── per-column/
│   ├── nazvanie-mod-ru.md   # детально по «Название модификации (RU)»
│   ├── opisanie-ru.md       # детально по «Описание товара (RU)»
│   ├── opisanie-ua.md       # детально по «Описание товара (UA)»
│   └── ...                  # 9 колонок битого импорта
├── per-track/
│   ├── track1-mod-name.md   # 17 SKU mod_name recovery — проверка на LIVE
│   ├── track2-desc.md       # 4 SKU desc recovery (TATRA отдельно)
│   └── chunks-translation.md# chunks 016-029 — на LIVE доехали или нет
└── matcher-impact.md        # отдельный документ: как matcher block связан с косяками
```

## Скрипты (которые мне писать завтра)

1. **`scripts/_state_load.py`** — загружает все 4 источника в pandas DataFrames по `Артикул`. Output: pickle для быстрых пересчётов.
2. **`scripts/_state_classify.py`** — для каждой (SKU, col) ячейки вычисляет флаг (OK/STALE/WIPED/WRONG/UNTOUCHED). Output: `.planning/STATE-AUDIT/_state_flags.json`.
3. **`scripts/_state_report.py`** — рендерит `.md` файлы по флагам. Per-column, per-track, summary.

NB: НИ ОДИН скрипт НЕ модифицирует исходные xlsx, НЕ пишет в Horoshop, НЕ создаёт новых импорт-файлов. Read-only audit.

## TATRA — pending

SKU 2062006550 desc(UA) — наш fix-файл загружен в Horoshop import wizard (Yana увидит preview-таблицу с 691-char текстом), финальная кнопка «Імпортувати» **не нажата**. Один клик Yana = recovery 4/4 закрыт.

**Не блокирует audit** — audit пометит эту ячейку как 🔴 WIPED. После клика Yana пометка изменится на ✅ OK. Можно сделать клик когда удобно: до audit, во время, или после.

## NEXT ACTION когда unblock

Когда Yana положит `horoshop-export-2026-05-21-postrecovery.xlsx` в `C:\Projects\labresta-sync\`:
1. Я (или next Claude после compact) запускаю `python scripts/_state_load.py`
2. Затем `python scripts/_state_classify.py`
3. Затем `python scripts/_state_report.py`
4. Презентую Yana топ-уровень: сколько 🔴 WIPED, сколько 🟡 STALE, какие top-issues
5. Решаем дальнейший приоритет на основе цифр

## Constraints (durable)

- xlsx/json source NEVER mod (read-only)
- В коммитах НИКАКИХ следов AI: без Co-Authored-By, без «Generated with Claude»
- Author=LabResta <labresta@labresta.ua>
- `git -c commit.gpgsign=false`
- NO `--force`
- Explicit `git add <path>`, не `-A`
- Скрипты НЕ коммитить пока Yana явно не дала «коммить»

## Что НЕ делаем в этой фазе

- НЕ собираем новые импорт-файлы для Horoshop
- НЕ трогаем chunks 029-054 (W1) и 055+ (W2) — пауза
- НЕ разбираемся с matcher'ом (отдельная задача после audit)
- НЕ заливаем НП-feed (после matcher unblock)
- НЕ переписываем `_build_horoshop_import.py` — переписываем ПОСЛЕ audit, когда понятна картина
