# Финальные loop-промпты W1 и W2 (copy-paste) — с правилом SKIP-НП

Вставлять в `/loop` в СВЕЖЕМ терминале по чек-листу PLAN.md. Интервал петли = 15 мин.
НЕ запускать из сессии c01dc1d4 (read-only). Сначала шаги 1-2 чек-листа (дождаться чистой границы W1, `ac-off`).

**Изменение vs PLAN.md:** добавлено правило SKIP-НП (9 НП-эксклюзивных брендов, forward-only). Раздел brand-skip в PLAN.md этим списком заменяется. Цель — сократить время воркера; тело этих товаров обновим из фида НП отдельно, параллельно.

---

## ОБЩЕЕ ПРАВИЛО SKIP-НП (вшито в оба промпта ниже — здесь для справки)

- НП-эксклюзивные бренды (поставщик «Новый проект», тело будет обновлено из фида НП отдельно):
  **HURAKAN / Hurakan / Хуракан · APACH / Apach / Апач · FAGOR / Fagor / Фагор · TATRA / Tatra / Татра · COLD / Cold / Колд · PROJECT SYSTEMS · ASTORIA / Astoria · ARRIS / Arris · MAXIMA / Maxima**. Сопоставление бренда — без учёта регистра, латиница И кириллица.
- Для каждого SKU, встречающегося ВПЕРЁД от текущей точки CURRENT.md: если бренд ∈ списка → НЕ переписывать RU, НЕ писать зонд-скрипты, НЕ делать scratch-дамп, НЕ тратить xhigh-анализ. Просто распознать бренд → пометить `SKIP-НП (brand=<X>, тело из фида НП позже)` в chunk-NN-MANUAL-REVIEW.md → следующий SKU. Ячейки этого SKU в chunk-NN-fixed.xlsx НЕ менять.
- SKIP-НП засчитывается в N/N закрытия чанка как отдельная категория (наравне с blk/blknochg). Чанк закрывается штатно.
- НЕ возвращаться к закрытым чанкам и уже обработанным SKU. Правило ТОЛЬКО вперёд, к непройденному. Ретро-прохода нет.
- Бренды НЕ из списка (ROBOT COUPE, SIRMAN, SCAN, ASBER, CEADO, BARTSCHER, и любые иные) — обрабатывать как обычно, НЕ скипать.

---

## W1 — существующий воркер (дерево `C:\Projects\labresta-sync`, ветка `main`)

```
Idempotent loop-шаг аудита перевода LabResta UA→RU. Ты — W1.

ПЕРВЫМ ДЕЛОМ каждый заход:
1. cd C:\Projects\labresta-sync; git status; git log -5 --oneline; прочитай .planning/CURRENT.md.
2. Состояние:
   - Незакоммиченный дифф → ты в середине батча: ДОКОММИТЬ текущий батч по сложившимся правилам, новый в этот заход НЕ начинать, затем продолжай.
   - Чисто → следующий батч от точки в CURRENT.md.
   - Работы нет / батч уже сделан → дубликат-триггер, ничего не делай, заверши заход.

ТВОЙ ДИАПАЗОН: доделать chunk-020 если не закрыт, затем ТОЛЬКО chunk-021 … chunk-054. Не трогать chunk-055+ (это W2) и chunk-≤020 (закрыты — НЕ переоткрывать).

>>> ПРАВИЛО SKIP-НП (forward-only, приоритет над переводом) <<<
НП-эксклюзивные бренды: HURAKAN/Hurakan/Хуракан, APACH/Apach/Апач, FAGOR/Fagor/Фагор, TATRA/Tatra/Татра, COLD/Cold/Колд, PROJECT SYSTEMS, ASTORIA/Astoria, ARRIS/Arris, MAXIMA/Maxima (сравнение без регистра, латиница И кириллица).
Для каждого SKU ВПЕРЁД от текущей точки: если его бренд ∈ этого списка → НЕ переписывать RU, НЕ писать зонд-скрипты, НЕ делать scratch-дамп, НЕ тратить xhigh-анализ. Только: распознать бренд → пометить «SKIP-НП (brand=<X>, тело из фида НП позже)» в chunk-NN-MANUAL-REVIEW.md → следующий SKU; ячейки этого SKU в chunk-NN-fixed.xlsx не менять. SKIP-НП считается в N/N закрытия как отдельная категория. НЕ возвращаться к закрытым чанкам / обработанным SKU — только вперёд, ретро-прохода нет. Бренды НЕ из списка (ROBOT COUPE, SIRMAN, SCAN, ASBER, CEADO, BARTSCHER, прочие) — обрабатывать обычно, НЕ скипать.

ПРОЦЕСС для НЕ-скип SKU — ровно тот что уже сложился, НЕ переизобретай:
- Эталон формата: chunk-019-MANUAL-REVIEW.md + chunk-019-diff.md, та же структура и категории (blk / blknotrip / blknochg / SKIP-НП).
- Правила перевода: memory feedback_labresta_ua_ru_translation_rules. Workflow per chunk: .planning/translation-audit/chunks/INDEX.md. chunk-NN.xlsx — источник, НЕ менять. Писать chunk-NN-fixed.xlsx + chunk-NN-diff.md + chunk-NN-MANUAL-REVIEW.md; сомнения → chunk-NN-questions.md.
- Батч = 8 SKU. После каждого батча: контент-коммит + маркер-коммит «CURRENT: chunk-NNN X/Y ...», push в origin main. Между чанками: «chunk-NNN scaffold (... продолжение chunk-NNN-1)». Обновлять .planning/CURRENT.md каждый батч.

ЗАПРЕЩЕНО: править колонку Status в INDEX.md (не поддерживается). В коммитах НИКАКИХ следов AI — без Co-Authored-By, без «Generated with Claude», автор только Yana. Не хардкодить секреты.

STOP: когда «chunk-054 CLOSED 54/54» закоммичен и запушен — напечатай итог (по 021–054: сколько SKU переведено, сколько SKIP-НП) и заверши петлю; новый чанк НЕ скаффолдить.
```

---

## W2 — новый воркер (дерево `C:\Projects\labresta-sync-w2`, ветка `translation-audit/w2`)

Перед запуском: `git worktree add ../labresta-sync-w2 -b translation-audit/w2` (из labresta-sync, на чистой границе W1).

```
Idempotent loop-шаг аудита перевода LabResta UA→RU. Ты — W2 (параллельный воркер).

ПЕРВЫМ ДЕЛОМ каждый заход:
1. cd C:\Projects\labresta-sync-w2; git status; git branch --show-current (должно быть translation-audit/w2 — если нет, СТОП и сообщи); git log -5 --oneline.
2. Прочитай .planning/CURRENT-w2.md. Нет файла → первый заход: создай .planning/CURRENT-w2.md, начни с chunk-055 scaffold.
3. Состояние:
   - Незакоммиченный дифф → доделай/докоммить текущий батч, новый в этот заход не начинать.
   - Чисто → следующий батч от точки в CURRENT-w2.md.
   - Работы нет / батч уже сделан → дубликат-триггер, заверши заход.

ТВОЙ ДИАПАЗОН: ТОЛЬКО chunk-055 … chunk-085. НИКОГДА не трогать chunk-≤054 (это W1) и не редактировать main.

>>> ПРАВИЛО SKIP-НП (forward-only, приоритет над переводом) <<<
НП-эксклюзивные бренды: HURAKAN/Hurakan/Хуракан, APACH/Apach/Апач, FAGOR/Fagor/Фагор, TATRA/Tatra/Татра, COLD/Cold/Колд, PROJECT SYSTEMS, ASTORIA/Astoria, ARRIS/Arris, MAXIMA/Maxima (без регистра, латиница И кириллица).
Для каждого SKU ВПЕРЁД от текущей точки: если бренд ∈ списка → НЕ переписывать RU, НЕ писать зонд-скрипты, НЕ scratch-дамп, НЕ xhigh-анализ. Только: распознать → пометить «SKIP-НП (brand=<X>, тело из фида НП позже)» в chunk-NN-MANUAL-REVIEW.md → следующий SKU; ячейки в chunk-NN-fixed.xlsx не менять. SKIP-НП считается в N/N как отдельная категория. НЕ возвращаться к обработанному — только вперёд. Бренды НЕ из списка (ROBOT COUPE, SIRMAN, SCAN, ASBER, CEADO, BARTSCHER, прочие) — обрабатывать обычно.

ПРОЦЕСС для НЕ-скип SKU — идентичен основному воркеру:
- Эталон формата: chunk-019-MANUAL-REVIEW.md + chunk-019-diff.md (категории blk / blknotrip / blknochg / SKIP-НП).
- Правила: memory feedback_labresta_ua_ru_translation_rules. Workflow per chunk: INDEX.md. chunk-NN.xlsx — источник, не менять. Писать chunk-NN-fixed.xlsx + chunk-NN-diff.md + chunk-NN-MANUAL-REVIEW.md; сомнения → chunk-NN-questions.md.
- Термины: внутри своих chunk-NN-MANUAL-REVIEW.md; ДОПОЛНИТЕЛЬНО сводный chunk-glossary-w2.md (новые UA→RU термины) для merge-ревью Yana. Накопленный глоссарий основного воркера — READ-ONLY референс, НЕ редактировать.
- Свой state-файл: .planning/CURRENT-w2.md (НЕ трогать .planning/CURRENT.md — это W1).
- Батч = 8 SKU. После каждого: контент-коммит + маркер «CURRENT-w2: chunk-NNN X/Y ...», push в origin translation-audit/w2 (НЕ в main). Между чанками: «chunk-NNN scaffold (W2, продолжение chunk-NNN-1)». Обновлять .planning/CURRENT-w2.md каждый батч.

ЗАПРЕЩЕНО: править Status в INDEX.md; коммитить/пушить в main; следы AI в коммитах (без Co-Authored-By / «Generated with Claude», автор только Yana); хардкод секретов.

STOP: когда «chunk-085 CLOSED 85/85» закоммичен и запушен в translation-audit/w2 — напечатай итог (по 055–085: переведено / SKIP-НП) и заверши петлю.
```

---

## После завершения обоих

```
cd C:\Projects\labresta-sync
git checkout main
git merge --no-ff translation-audit/w2
# конфликтов не ожидается (дизъюнктные chunk-файлы; CURRENT-w2.md отдельный; INDEX.md никто не правил)
# если всплыл глоссарий — разрулить вручную с Yana
git worktree remove ../labresta-sync-w2   # после успешного merge
```
Затем: финальное ревью + (ОТДЕЛЬНО, параллельно) синхронизация обновления тела товара из фида НП для SKIP-НП брендов — под бэкап, по правилам live-store. Перед заливом тел подтвердить description_ru != description_uk на многих строках фида (не на одной).
```
