# INCIDENT — Track #2 (`Описание (RU)`) не доехал в LIVE

**Дата обнаружения:** 2026-05-21
**Severity:** High (607 ручных переводов остались на диске, LIVE-карточки до сих пор показывают укр. текст в RU)
**Status:** Identified → Fix in progress (extractor + xlsx)

---

## TL;DR

Закрыли 23 чанка (chunk-007 … chunk-029), написали 607 ручных RU-переводов описаний (`blk триплет`), но **ни один не попал в LIVE Horoshop**. Track #1 (`Назв. модиф. (RU)`) проехал, потому что для него Yana сделала отдельный adhoc xlsx-импорт. Для `Описание (RU)` build-script так и не был написан, аудит шёл по diff.md без проверки parity с `chunk-NN-fixed.xlsx`.

## Verified evidence (2026-05-21)

Прямой LIVE-снимок `horoshop-export 21.05.26.xlsx` (3 SKU выборка из chunk-019 blk триплет):

| Артикул | Бренд / модель | Назв. модиф. (RU) | Описание (RU) |
|---|---|---|---|
| 2289556549 | Frosty FOV-20D | ✅ чистый RU | ❌ 62 UA-символа (`і`, `ї`, `є`) |
| 2494024457 | Tecnodom FEM04NEPSV | ✅ чистый RU | ❌ 44 UA-символа |
| 2551261210 | Unox XF033 | ✅ чистый RU | ❌ 112 UA-символов |

Все три SKU имеют в `chunk-019-diff.md` полный написанный RU-перевод HTML тег-в-tag (между `**Стало:** (полный перевод RU тег-в-tag):` и закрывающим ` ``` `). Параллельные ` ``` ``` `-блоки в `chunk-NN-fixed.xlsx` для тех же SKU **не были созданы** — `fixed.xlsx` обновлялся только для Track #1 строк.

## Root cause analysis

### Что пошло не так

1. **Pipeline split, но без parity-чека.** Track #1 (mod_name) и Track #2 (desc) шли как два независимых output'а одного и того же batch-аудита: diff.md описывал ОБА, но fixed.xlsx собирался только для mod_name (потому что для него существовал ad-hoc `_build_horoshop_fix_mod_name.py`).
2. **Build-script for desc never written.** В `scripts/` есть `_build_horoshop_fix_mod_name.py`, `_build_horoshop_fix_residual.py`, `_build_horoshop_import.py`, `_build_horoshop_mini5.py` — но **нет** `_build_horoshop_fix_desc_ru.py`. Никто не заметил, потому что Track #2 не был частью per-batch close-checklist.
3. **Idempotent assertions checked diff.md, not LIVE.** Per-batch `_apply0NN_bN.py` ассерт-проверяли только что diff.md обновился — не было кросс-проверки «текст в diff.md ∈ fixed.xlsx ∈ LIVE».
4. **STATE-AUDIT Phase B мисинтерпретация.** Аудит 369 ячеек с маркером `(полностью идентично UA — украинский текст)` ошибочно классифицировал их как «deliberate marker = leave RU=UA». На самом деле этот маркер — BEFORE-state blk триплет fix'a, и означает «здесь UA-копия в RU, нужен перевод в `**Стало:**`». Эта мисинтерпретация замаскировала проблему ещё на 1 spring.
5. **No LIVE-parity smoke-test.** Между закрытием chunk-NN и началом chunk-NN+1 не было «возьми 1 SKU из закрытого, проверь LIVE через xlsx-snapshot». Если бы был — отлов бы случился на chunk-008 (50 переводов в воздухе), а не на chunk-029 (607).

### Что НЕ пошло не так

- Сами переводы — корректные. RU HTML тег-в-tag, structure 1:1, кир.х 0x445 verbatim, операторские термины переведены. Просто застряли на диске.
- chunk-NN-diff.md как single source of truth для переводов — рабочий формат. Текст оттуда тривиально извлекаем regex'ом.
- Track #1 (mod_name) реально доехал — это подтверждает что Horoshop import работает, проблема не в платформе.

## Fix (in progress)

### Шаг 1 — Extractor (этот спринт)

`scripts/_extract_blk_translations_from_diffs.py`:
- regex-scan всех `chunk-007…029-diff.md` (+ chunk-030 после b1)
- pattern: `## SKU N/M …(Артикул NNNN)…` + `**Стало:** (полный перевод RU тег-в-тег):` + ` ``` <RU HTML> ``` `
- emit `.planning/translation-audit/horoshop-fix-desc-ru-FULL.xlsx` [Артикул, Описание (RU)]
- Yana импортирует в Horoshop одним заходом

### Шаг 2 — Parity-check для будущих чанков

После каждого batch-close: assert `len(blk триплет SKU в diff.md) == len(matching RU desc rows в fixed.xlsx)`. Иначе FAIL батча.

### Шаг 3 — Per-chunk close-checklist дополнить

В `.planning/translation-audit/chunks/INDEX.md` (или новый `CLOSE-CHECKLIST.md`) добавить bullet «Track #2 desc xlsx собран?» как обязательный gate для CLOSED-статуса.

### Шаг 4 — Random LIVE-parity smoke-test

При закрытии каждого 5-го чанка: взять 1 рандомный SKU из blk триплет → diff его `Описание (RU)` против последнего `horoshop-export *.xlsx` → должно быть idempotent.

## Lessons

1. **Diff.md ≠ deliverable.** Любой текст в diff.md без parity-связки с fixed.xlsx — это draft, а не applied fix.
2. **Track decomposition нуждается в parity-чеке.** Если задача дробится на N tracks с разными build-script'ами, недостающий script должен ловиться в close-gate, а не визуальным аудитом.
3. **Audit script with "FAIL count" недостаточен.** STATE-AUDIT Phase B вернул 369 FAIL — но классифицировал их неправильно, и количество в логе стало алиби. Нужна была проверка interpretation (что значит этот marker?), не только count.
4. **LIVE — единственный источник истины.** Все промежуточные xlsx/json/md могут расходиться. Smoke-тест против actual LIVE снимка раз в N батчей — дёшево и ловит дрейф рано.

---

**Discovered by:** Yana 2026-05-21 («сознательная маркировка RU=UA — в смысле ру=юа? ка так?» — вопрос триггернул пересмотр STATE-AUDIT Phase B классификации).
