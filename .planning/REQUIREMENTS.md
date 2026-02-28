# Requirements: LabResta Sync

**Defined:** 2026-03-01
**Core Value:** Ціни і наявність на prom.ua завжди актуальні — без ручної роботи щодня.

## v1.1 Requirements

Requirements for milestone v1.1 — Tech Debt + Excel Suppliers.

### Excel/Google Sheets

- [ ] **EXCEL-01**: Оператор може додати постачальника з типом "Excel" і вказати URL Google Sheets або завантажити файл
- [ ] **EXCEL-02**: Система скачує Excel-файл за публічним URL Google Sheets (автоконвертація URL в /export?format=xlsx)
- [ ] **EXCEL-03**: Система парсить Excel: витягує назву, ціну, наявність з колонок аркуша
- [ ] **EXCEL-04**: Парсер Excel використовує ту саму модель SupplierProduct, що й YML-парсер (save_supplier_products сумісність)

### Matching

- [ ] **MTCH-01**: MatchRule застосовується автоматично при синхронізації — товари з правилами отримують підтверджений матч без fuzzy-кроку

### Pricing

- [ ] **PRC-01**: Оператор може задати індивідуальну знижку (discount_percent) для конкретного товару через UI матчів

### UX / Notifications

- [ ] **UX-01**: notifications.js завантажується глобально на всіх сторінках (badge polling працює скрізь)
- [ ] **UX-02**: Оператори (роль operator) бачать колокольчик і мають доступ до своїх сповіщень без помилки 403

### Code Cleanup

- [ ] **CLEAN-01**: Видалити мертвий код: ftp_upload.py
- [ ] **CLEAN-02**: Видалити мертвий код: yml_test_generator.py

## v1.2+ Requirements

Deferred to future release. Tracked but not in current roadmap.

### Excel Enhancements

- **EXCEL-05**: Збережений маппінг колонок для кожного постачальника (JSON на моделі Supplier)
- **EXCEL-06**: Підтримка ПДВ-перемикача для постачальників з цінами без ПДВ
- **EXCEL-07**: Multi-sheet workbook — вибір аркуша за назвою або індексом

### Matching Enhancements

- **MTCH-02**: Exact-match по артикулу коли постачальник надає артикул/SKU

### Data Format

- **DATA-01**: Підтримка CSV-файлів як джерела постачальника

## Out of Scope

| Feature | Reason |
|---------|--------|
| Підтримка .xls (старий формат) | Потребує xlrd, проблеми безпеки; Google Sheets дає .xlsx |
| AI/LLM авторозпізнавання колонок | Залежність від зовнішнього API, keyword matching достатній |
| Real-time polling Google Sheets | Google rate limits; prom.ua імпортує кожні 4 год |
| CSV підтримка | Складність з кодуванням (cp1251/utf-8, delimiters); відкладено до v1.2+ |
| Email-сповіщення | Telegram достатньо |
| Автододавання товарів з фіду на prom.ua | Ручний контроль над каталогом |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| EXCEL-01 | — | Pending |
| EXCEL-02 | — | Pending |
| EXCEL-03 | — | Pending |
| EXCEL-04 | — | Pending |
| MTCH-01 | — | Pending |
| PRC-01 | — | Pending |
| UX-01 | — | Pending |
| UX-02 | — | Pending |
| CLEAN-01 | — | Pending |
| CLEAN-02 | — | Pending |

**Coverage:**
- v1.1 requirements: 10 total
- Mapped to phases: 0
- Unmapped: 10 ⚠️

---
*Requirements defined: 2026-03-01*
*Last updated: 2026-03-01 after initial definition*
