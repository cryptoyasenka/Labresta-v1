# Backlog — tasks parked for later

## Apply-discount UI for per-brand suppliers with editable EUR rate

**Status:** not started
**Created:** 2026-04-22 (during НП onboarding, Session 15)

### Problem
Per-brand режим (например Новый Проект: HURAKAN 15, SIRMAN/ROBOT COUPE/CEADO/BARTSCHER 20, fallback 17) сейчас
применяет % как есть. На дешёвых товарах это может дать маржу <500 грн или даже минус.

MARESTO решает это через существующий endpoint `/suppliers/<id>/apply-discount`, который гоняет
`calculate_auto_discount` с фиксированным target=19%, min_margin=500 грн, cost_rate=0.75.
У per_brand поставщиков эта кнопка в UI не доступна / не работает по брендам.

### Что сделать
1. **UI на странице поставщика** — кнопка "Пересчитать скидки с маржой ≥500 грн".
   - Показывать только для `pricing_mode='per_brand'` и `pricing_mode='auto_margin'`.
   - Dry-run превью (distribution по %), потом apply.
2. **Поле "Курс EUR"** — редактируемое прямо в форме поставщика (уже есть `eur_rate_uah`
   в модели, но не выводится в form.html). Оператор должен видеть текущий и менять перед пересчётом.
3. **Расширить `/suppliers/<id>/apply-discount` endpoint** — для `pricing_mode='per_brand'`
   брать `target_discount` индивидуально через `resolve_discount_percent(None, supplier, sp.brand)`
   (бренд HURAKAN → target 15, неизвестный бренд → target 17).
4. **Тесты:** dry-run + real + force на НП-образном поставщике с 2+ брендами и ценами
   в 3 бакетах (target держится / margin-capped / zero).

### Параметры (от Yana)
- Курс EUR по умолчанию: **52 UAH** (сейчас у обоих в БД стоит 51.15 — обновить при апдейте формы)
- Минимальная маржа: **500 грн** (константа, как у MARESTO)
- Доля закупки: **75%** (cost_rate=0.75, как у MARESTO)

### Почему отложено
Yana хочет сначала визуально проверить UI добавления поставщика и пройти импорт xlsx для НП.
Margin-cap логика — следующий шаг, но не на сегодня.
