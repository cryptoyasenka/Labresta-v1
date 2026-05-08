# TODO — после ночного аудита 2026-05-09

Полный matching audit + article-anchor verify прогнаны на проде. 4 manual rule-violations отозваны. Остальное — на завтра.

## Высокий приоритет (false-positive риски нулевые, чисто catalog hygiene)

### 1. Cat H — 11 cross-brand display_article дублей в каталоге Horoshop
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

Действие: руками в Horoshop поправить display_article у бренд-чужаков (поставить НЕ-Hendi артикул) или удалить дубль если PP не нужен. Детали в `.planning/matching-audit-report.md` Cat H.

### 2. Catalog cleanup — 3 AD46 PPs убрать из Horoshop
- PP#1007 AD46MV
- PP#1015 AD46DV
- PP#1008 AD46D (статус у поставщика не подтверждён — сначала проверить)

Подтверждено через dealer portal: AD46MV/DV у np.com.ua нет. AD46D — проверить.

## Средний приоритет (false-negative gaps, требуют per-row решения)

### 3. Cat B sibling — 13 unmatched PPs где SP article = anchor + suffix
- **Hurakan ×7** (горячая зона): HKN-DHD10G/12G/16G ↔ +M; HKN-CFV60 ↔ +M; HKN-TR65 ↔ +M; HKN-HBH850M ↔ +PRO; HKN-BLW2 grey ↔ grey/red
- **Apach ×3**: AD46D ↔ DI ECO (точно разные!), ASH05K ↔ +R290, AHM250V250 ↔ +C
- **Fagor ×1**: AFN-801 ↔ +EXP
- **Robot Coupe ×1**: 28173 ↔ +W
- **Sirman ×1**: TC-12 ↔ TC 12 E

Каждый требует: эта suffix variant — тот же SKU (сматчить) или реально другой (оставить unmatched)? Per-row через UI `/matches/`.

### 4. Cat B-reverse — 8 unmatched где PP длиннее SP
- Hurakan: HKN-IP40FM↔IP40F, HKN-WNC160CDW↔WNC160CD, HKN-ISV5P↔ISV5 (2 PPs)
- Sirman: 66520502K12↔66520502 (2 PPs)
- Ceado: M98T↔M98
- Airhot: IP3500D (SPs без article на РП Україна)
- Apach: AD46MV↔AD46M ECO — НЕ матчить (Yana правило)

## Большая зона (не блокирует, но стоит проверить)

### 5. 1641 confirmed без article-anchor
Эти матчи прошли через name-fuzzy / Кодаки internal codes / manual confirms — не через R0 article anchor. Большинство наверняка правильные (Кодаки использует свои внутренние коды, модель лежит в name), но требует узкой верификации:
- brand match (must be exact)
- модель-токен присутствует в обоих names
- voltage compatible

Нужен новый скрипт `scripts/verify_no_anchor_matches.py`. Если найдутся подозрительные — отчёт по убыванию score.

## Старые pending

- **Phase L smoke-test** (UI conflict modal на `/matches/?supplier_id=4`) — Yana ручная проверка
- **Phase M apply** для Apach — заблокирован пока поставщик не расширит фид
- **Manual Astim review** — 7 fuzzy candidates (carry-over)
- **MARESTO unblock** — Railway IP заблокирован Cloudflare поставщика
- **Open question**: `suppliers_fetch_all(exclude_dead_suppliers=True)` default — ждёт твоего решения

## Артефакты ночной сессии 2026-05-09

- `scripts/audit_matching_gaps.py` — full A-H аудит (commit `fc466f7`)
- `scripts/verify_article_anchor_rule.py` — three-location rule verifier (commit `ee914d6`)
- `scripts/reject_match.py` — параметризованный reject tool (commit `ee914d6`)
- `scripts/check_ad46_state.py` — gitignored, локально для проверки AD46
- `.planning/matching-audit-report.md` — A=0 B=13 B-rev=9 C=0 D=267 E=0 F=0 G=0 H=11
- `.planning/article-anchor-verify.md` — 487 three-way + 417 two-way + 4 violations + 1641 no-anchor
- 4 reject'a на проде: match#6611, #6383, #1100, #1102 (все были manual `Admin`)
- Memory: `feedback_labresta_ad46_suffix_skus.md` — правило AD46 suffix=SKU

См. также `.planning/CURRENT.md` для актуального состояния.
