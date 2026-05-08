# TODO — после ночного аудита 2026-05-09

Полный matching audit + article-anchor verify + no-anchor narrow verify прогнаны на проде.
4 manual rule-violations отозваны. Остальное расписано ниже с тегами:

- **[NEEDS YANA]** — нужно твоё решение / клик в UI / правка в Horoshop / контакт с поставщиком
- **[CLAUDE CAN]** — могу сделать сама без риска (read-only анализ / dossier для тебя)
- **[BLOCKED]** — заблокировано внешним фактором, не разблокируется автономно

## 🔴 NEEDS YANA — высокий приоритет (catalog hygiene)

### 1. [NEEDS YANA] Cat H — 11 cross-brand display_article дублей в каталоге Horoshop
Hendi-артикулы попали в PP других брендов (явные баги ввода):
- `203149` — Hendi + Spidocook
- `239766` — Hendi + Fimar
- `239780` — Hendi + Roller Grill
- `240403` — Hendi + FROSTY
- `271599` — Hendi + FROSTY + GoodFood
- `860526` — Hendi + Saro

Same-brand но разные модели:
- `08300002000` — Ozti SPM 20 vs SPM 70
- `212004` — FROSTY VP-81 vs VP-2Y40
- `40752102p` — Sirman TM INOX вариант 1 vs набор 1
- `40802852f` — Sirman IP 20 M vs IP 10 M
- `66520502k12` — Sirman CICLONE 28 + A35 vs A25

**Действие:** руками в Horoshop поправить display_article у бренд-чужаков (поставить НЕ-Hendi артикул) или удалить дубль если PP не нужен. Детали в `.planning/matching-audit-report.md` Cat H. Если нужен dossier с деталями каждого PP — скажи, могу собрать.

### 2. [NEEDS YANA] Catalog cleanup — 3 AD46 PPs убрать из Horoshop
- PP#1007 AD46MV
- PP#1015 AD46DV
- PP#1008 AD46D (статус у поставщика не подтверждён — сначала проверить через dealer portal)

Подтверждено через dealer portal: AD46MV/DV у np.com.ua нет. AD46D — проверить.

## 🟡 NEEDS YANA — средний приоритет (per-row решения)

### 3. [NEEDS YANA] Cat B sibling — 13 unmatched PPs где SP article = anchor + suffix
- **Hurakan ×7** (горячая зона): HKN-DHD10G/12G/16G ↔ +M; HKN-CFV60 ↔ +M; HKN-TR65 ↔ +M; HKN-HBH850M ↔ +PRO; HKN-BLW2 grey ↔ grey/red
- **Apach ×3**: AD46D ↔ DI ECO (точно разные!), ASH05K ↔ +R290, AHM250V250 ↔ +C
- **Fagor ×1**: AFN-801 ↔ +EXP
- **Robot Coupe ×1**: 28173 ↔ +W
- **Sirman ×1**: TC-12 ↔ TC 12 E

Каждый требует: эта suffix variant — тот же SKU (сматчить) или реально другой (оставить unmatched)? Per-row через UI `/matches/`. Могу собрать dossier с фото / описаниями обоих SP/PP — скажи если нужен.

### 4. [NEEDS YANA] Cat B-reverse — 8 unmatched где PP длиннее SP
- Hurakan: HKN-IP40FM↔IP40F, HKN-WNC160CDW↔WNC160CD, HKN-ISV5P↔ISV5 (2 PPs)
- Sirman: 66520502K12↔66520502 (2 PPs)
- Ceado: M98T↔M98
- Airhot: IP3500D (SPs без article на РП Україна)
- Apach: AD46MV↔AD46M ECO — НЕ матчить (Yana правило)

Per-row через UI.

### 5. [NEEDS YANA] Manual Astim review — 7 fuzzy candidates (carry-over)
На `/matches/?supplier_id=8&status=candidate` — отклонить m=6620, 6618, 6611 + подтвердить 7 fuzzy.

### 6. [NEEDS YANA] Phase L smoke-test
UI conflict modal на `/matches/?supplier_id=4` — выделить 5-10 НП кандидатов, нажать «Подтвердить», проверить что появляется `#conflictResolveModal` с per-row кнопками.

## 🚫 BLOCKED — нужно внешнее действие

### 7. [BLOCKED] Phase M Apach — np.com.ua не выгружает APL/APKE/AFM 02-03
14 URL-вариантов прозвонены, тот же набор 158 уникальных Apach SKU. Два пути:
- **(A) [NEEDS YANA]** написать поставщику np.com.ua с просьбой расширить дилер-экспорт. Показать скрин дилерского портала где APL/APKE/AFM 02 есть, а в XLSX dealer_id=69781 — нет.
- **(B) [BLOCKED]** scrape дилерского портала через DPAPI cookie + реальный браузер. Headless Chromium блокирует Cloudflare. Технически решаемо но нужен ручной экспорт сессии.

### 8. [BLOCKED] MARESTO unblock — Cloudflare блокирует Railway IP
mrst.com.ua/include/price.xml: 200 OK с локалки, 403 с Railway. Решения:
- whitelist Railway egress IP через MARESTO support — **[NEEDS YANA]** контакт
- proxy через VPS — отдельный инфраструктурный шаг

### 9. [NEEDS YANA] Open question — `suppliers_fetch_all(exclude_dead_suppliers=True)` default
Risk decision: должен ли auto-cron стрелять пока MARESTO навсегда мёртв? Текущий код OFF (safe default). Если хочешь — могу собрать tradeoff doc с pros/cons обоих вариантов.

## ✅ DONE сегодня (read-only / safe-write)

- 4 manual rule-violations rejected: match#6611, #6383, #1100, #1102 (commit `e945391`)
- Full matching audit прогнан: A=0 B=13 B-rev=9 C=0 D=267 E=0 F=0 G=0 H=11 (commit `fc466f7`)
- Article-anchor rule verifier на проде: 487 three-way + 417 two-way + 4 violations + 1641 no-anchor (commit `ee914d6`)
- AD46-series check: чистая БД, никаких кривых матчей вокруг (commit `9eff3ef`)
- No-anchor narrow verifier: 1641/1641 OK (1636 + 5 manually verified) (commit `cce9cac`)
- Night audit closing report (commit `5104dfe`)

## 🤖 [CLAUDE CAN] — что могу сделать сама без тебя

Если оставишь auto-continue включённым — могу пройтись по этому списку. Все read-only, никаких изменений в `app/`, никаких миграций, никаких живых API звонков:

1. **Per-row dossiers для Cat H (11 шт)** — для каждого дубля собрать side-by-side: оба PP с фото-URL, ценой, описанием, всеми SP confirmed/candidate. Сохранить в `.planning/dossiers/cat-h-{disp_article}.md`. Завтра ты пройдёшь и за 30 сек/PP примешь решение вместо 5 мин копания.
2. **Per-row dossiers для Cat B sibling (13 шт)** — то же самое: PP с anchor + кандидат-SP с suffix, рядом цены + описания, чтобы решить "тот же SKU или нет".
3. **Per-row dossiers для Cat B-reverse (8 шт)** — то же.
4. **Astim fuzzy dossier (7 candidates)** — собрать каждого кандидата с context.
5. **Tradeoff doc для exclude_dead_suppliers** — pros/cons обоих вариантов default, без принятия решения за тебя.
6. **Скрипт-helper extraction** — три аудит-скрипта повторяют railway DB connection pattern, можно вынести в `scripts/_lib/db.py`. Pure refactor, тестируемо.
7. **README в `scripts/`** — описать audit pipeline (audit → verify → reject → re-verify), чтобы будущая ты не забыла последовательность.

Если хочешь чтобы я сделала всё или часть — скажи "делай 1,2,4" например, и включи ночной режим (`ac-on`).
