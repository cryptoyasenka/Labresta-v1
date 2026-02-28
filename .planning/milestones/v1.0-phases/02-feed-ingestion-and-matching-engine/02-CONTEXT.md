# Phase 2: Feed Ingestion and Matching Engine - Context

**Gathered:** 2026-02-27
**Status:** Ready for planning (CLI area not discussed — Claude's discretion)

<domain>
## Phase Boundary

Headless sync pipeline: fetch MARESTO feed on schedule, retry on failure, produce fuzzy match candidates ranked by confidence for human review. No UI in this phase — all interaction via CLI/scripts. Confirmed matches persist across syncs. Disappeared products are detected and flagged.

</domain>

<decisions>
## Implementation Decisions

### Match confidence & thresholds
- 3 уровня уверенности: Высокий (>80%), Средний (60-80%), Низкий (<60%)
- Порог отсечки: 60% — ниже этого совпадение не показывается вообще
- Топ-3 кандидата на каждый товар MARESTO
- Товары без кандидатов выше порога помечаются как «без пары» — отдельный список
- В Phase 4 UI пользователь сможет удалить товары «без пары» из синхронизации
- Все совпадения требуют ручного подтверждения — никакого авто-одобрения в MVP

### Sync failure behavior
- Лог ошибок в БД + уведомление в Telegram при сбоях
- Telegram-бот нужно создать (через BotFather), токен и chat_id в .env
- Порог для Telegram-уведомления — на усмотрение Claude (количество неудачных попыток подряд)
- При недоступности фида — ничего не менять на prom.ua, оставить последние известные цены
- Retry с backoff при сбоях (tenacity)

### Disappeared products
- Товар помечается как пропавший после 2 синхронизаций подряд без него в фиде (~8 часов)
- Пропавший товар → поставить «нет в наличии» (available=false) в YML для prom.ua
- Если пропавший товар снова появился в фиде — НЕ восстанавливать автоматически, пометить как «требует проверки» для ручного подтверждения оператором

### Claude's Discretion
- CLI / скрипты: как запускать синхронизацию вручную, формат вывода, уровни подробности
- Точное количество retry-попыток перед Telegram-уведомлением
- Формат Telegram-сообщений об ошибках
- Детали реализации state machine для match статусов

</decisions>

<specifics>
## Specific Ideas

- Товары «без пары» должны быть видны как отдельная группа — пользователь должен понимать, что эти товары MARESTO не нашли соответствия на prom.ua
- Telegram-уведомления только при серьёзных сбоях, не спамить при кратковременных проблемах

</specifics>

<deferred>
## Deferred Ideas

- Удаление товаров «без пары» из синхронизации через UI — Phase 4
- Ручное восстановление пропавших товаров через UI — Phase 4

</deferred>

---

*Phase: 02-feed-ingestion-and-matching-engine*
*Context gathered: 2026-02-27*
