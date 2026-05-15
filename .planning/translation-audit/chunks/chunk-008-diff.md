# chunk-008 translation diff (86 SKU, FROSTY-dominant грили/лавовые/Salamander continuation)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-008 (86 SKU, продолжение chunk-007)
**Apply key:** `Артикул` (scoped per row)
**Status:** in progress 0/86

**Brands:** FROSTY (24), Airhot (10), GGM Gastro International (7), Pimak (6), Hendi (5), GAM (5), ARRIS (4), Bartscher (4), REEDNEE (4), GoodFood (4), Hurakan (3), Roller Grill (3), Sirman (2), Apach (2), Saro/Kogast/Bertos (×1)

**Standing rules** (inherited from chunk-001 — chunk-007):
- UA term `жаркова`/`жарильна`/`смарочна` → `жарочна` (locked Yana 2026-05-14)
- RU machine artifact `жареная поверхность` → `жарочная поверхность`; `жареная для жарки` → `жарочная` (drop дубля)
- UA `Контейнер для сбору жиру` → `Контейнер для збирання жиру` (ONLY предлог); RU `Контейнер по сбору жира` → `для сбора`
- UA/RU `мм :` → `мм:`
- RU `от NN до NNN&deg;C` → `от NN&deg;C до NNN&deg;C` ТОЛЬКО если UA имеет оба &deg;C и значения совпадают; иначе FLAG
- decimal `N.N` → `N,N` обе локали (Yana 2026-05-14): замена разделителя, точность сохранена; already-comma/integers без изменений; weight `NN.00` → FLAG
- RU-leak UA `і`→`и`; 🔴 RU=UA полная укр. копия → AUTO full RU translate (структура HTML tag-в-tag, ✅ АВТО)
- Название модификации (RU) на украинском → AUTO перевод по Название (RU)
- Очевидный typo (удвоение/выпадение слога) → AUTO; однозначная машинная мистрансляция → AUTO + note
- FLAG (НЕ авто, → MANUAL-REVIEW русский): T5 surface conflict; RU temp values ≠ UA; RU `<br />` склейка; spec single vs text dual zone; `Два контейнера`→`контейнери`; `2,9 літр`→`літра`; weight `NN.00`; UA title без дескриптора что есть в body+RU; source data error UA=RU → soft note

---
