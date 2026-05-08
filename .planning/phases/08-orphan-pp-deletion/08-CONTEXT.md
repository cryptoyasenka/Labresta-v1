# Phase 8: Orphan PP → Deletion Candidate

**Gathered:** 2026-05-08
**Status:** Ready for planning

## Phase Boundary

Закрыть gap, вскрытый при ревью Astim: PromProduct без confirmed match по бренду который carries только один поставщик, при этом этого артикула в фиде поставщика нет → значит товар фактически снят с продажи у единственного источника, и его надо помечать как кандидата на удаление с Horoshop.

Сейчас «Видалення» (`/matches/deletion-candidates`) показывает только matches с `deletion_candidate=True`, который ставит Stage 4 на УЖЕ confirmed/manual парах. Осиротевшие PP (никогда не имели confirmed match) этот pipeline не видит.

**В скоупе:** auto-detection + UI badge + лог. **Вне скоупа:** автоудаление с Horoshop, изменение существующего Stage 4, новый supplier-onboarding flow.

## Concrete trigger case (Astim, 2026-05-08)

26 Hendi PP без confirmed match. Из них:
- 17 **отсутствуют в фиде Astim вообще** — например `238608` (тепаньяки), `199961` (коптильний пістолет), `598962` (диспенсер), `211366` (кип'ятильник), `272411/272602/272701/272404` (обігрівачі), `193679`, `707487`, `707517`, `515068`, `515143`, `676905`, `673751`, `673768`, `673782`. Эти точно надо удалять.
- 9 имеют candidate match но R0 не сработал (артикул в `display_article` но не в `name`). Решаются вручную, не через эту фазу.

Astim — единственный поставщик Hendi у нас. То есть «brand carries by only one supplier» — частый случай, не edge case.

## Decisions

- **Trigger:** одно правило, двух-уровневое:
  - L1 (high confidence): PP brand=X, **ровно один** активный supplier carries X, в SP-фиде **нет** SP с `article == pp.display_article` И `is_deleted=False` И `available is not False` → orphan.
  - L2 (lower confidence, не auto-flag): PP brand=X carried by N>1 suppliers, ни у одного не существует SP с этим article. Включаем в отчёт но не флажим автоматически (может быть фид одного поставщика глюкнул).
- **Где исполняется:** новый Stage 4.5 в `sync_pipeline.run_full_sync` после Stage 4 (disappeared products), до Stage 5 (rule_matcher). Запускается **после** sync ВСЕХ поставщиков, не на каждый supplier-sync (нужен полный snapshot фидов чтобы не false-positive).
- **Где хранится:** новая таблица `OrphanPP` (или extend `PromProduct.orphan_flagged_at` + `orphan_reason`). Решение в плане. Я склоняюсь к колонкам на `PromProduct` — никакого join'а не нужно, easier filtering.
- **UI:** «Видалення» текущая страница расширяется секцией «Сирітські товари каталогу» рядом с deletion candidates. Тот же flow «mark as deleted on Horoshop» / «cancel». confirmed_by-аналог не нужен — это не match, это PP-флаг.
- **YML:** orphan PP **никак не влияют** на YML feed (там только confirmed matches). YML не трогаем.
- **Идемпотентность:** при каждом запуске Stage 4.5 пересчитывает orphan-set с нуля. Если PP вернулась в фид — флаг снимается. Если оператор уже отметил «удалено вручную» — не возвращаем.
- **Operator decision interaction:** уже есть `PromProduct.operator_decision` (`pending|needs_delete|needs_request|keep_searching|reviewed`). Stage 4.5 ставит `operator_decision='needs_delete'` если `pending`. Не перезаписывает уже принятые решения.

## Out-of-scope

- Удаление через API Horoshop (unsafe, ручной шаг operator'а).
- Удаление PP-строки из БД (никогда не делаем — только soft-flag).
- Изменение R0 / matcher логики.
- Новые brand-aliases (Hendi vs HENDI и т.п. — уже норм).

## Risks

- **False positive** если фид Astim временно пришёл битым (5597 → 100 строк) и пол-каталога станет orphan. Mitigation: сравниваем размер фида с предыдущим успешным; если падение >50%, Stage 4.5 НЕ выполняется в этом sync run.
- **Stage 4.5 после каждого supplier-sync vs только после fetch-all** — нужно строго после fetch-all, иначе пока другие поставщики ещё не пробежали, их SP не в БД (false positive). План должен зафиксировать.
- **Race с manual operator_decision** — двойная проверка: trigger пишет `needs_delete` ТОЛЬКО если текущее значение `pending` или NULL.

## Success criteria

1. После прогона на сегодняшнем snapshot — minimum 17 Hendi PP помечены as orphan (`needs_delete`).
2. На `/matches/deletion-candidates?tab=orphan` видно их с PP id, name, brand, last seen в фиде (или «никогда»), кнопка «удалить из Horoshop вручную / cancel flag».
3. Если Astim фетч рандомно вернёт 100 строк — Stage 4.5 пропускается, лог `WARN: feed_size_drop, skipping orphan check`.
4. Запуск Stage 4.5 второй раз подряд НЕ меняет состояние (идемпотентно).
5. Операторская колонка `operator_decision='reviewed'` (вручную закрытая) НЕ перезаписывается обратно в `needs_delete`.

## Open questions for planning

- OrphanPP отдельная таблица vs колонки на PromProduct? *(склоняюсь к колонкам)*
- Brand normalization для intersect: lower-case достаточно или нужен нормализатор `Hendi` ≡ `HENDI` ≡ `HENDi`? *(сейчас уже есть `func.lower` в products.py — повторим)*
- L2 (multi-supplier brand orphans) — генерим в эту же фазу или отдельный отчёт позже? *(склоняюсь — позже, эта фаза только L1)*
- Триггер только из sync_pipeline, или ещё CLI command для ручного запуска без sync? *(добавим CLI — `flask sync flag-orphans` — для тестов и отладки)*

