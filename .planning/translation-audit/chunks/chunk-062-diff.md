# chunk-062 translation diff (81 SKU — грили контактні / роликові / теплові вітрини; W2 диапазон 055-085, продолжение chunk-061)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-062 (81 SKU)
**Apply key:** `Артикул` (scoped per row)
**Status:** IN PROGRESS 0/81 (blk триплет 0 / blknochg 0 / blknotrip 0 / SKIP-НП 0; Открытых вопросов 0)
**Worker:** W2 (параллельный воркер, диапазон chunk-055 … chunk-085; W1 ведёт chunk-001 … chunk-054)
**Scaffold:** chunk-062 scaffold (W2, продолжение chunk-061). chunk-061 ЗАКРЫТ 67/67 (blk триплет 29 / blknochg 34 / blknotrip 0 / SKIP-НП 4; OQ 0). chunk-062 = 81 SKU, openpyxl rows 2..82; первый SKU1 ART2424757446 «Гриль контактний SARO PG 1B», последний SKU81 ART2059507443 «Теплова вітрина Hurakan WD-120L». 11 батчей (б1-10 ×8 = 80, б11 = SKU81 ×1 финальный). SKIP-НП зонд по `Название` (NP-список HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA — Lat+Cyr): **6 hits — все HURAKAN**: SKU34 (ART736117487 «Гриль роликовий HURAKAN HKN-GW7M»), SKU53 (ART2375841678 «Гриль роликовий HURAKAN HKN-GW11M»), SKU54 (ART2375848556 «Гриль роликовий HURAKAN HKN-GW9M»), SKU66 (ART901422138 «Теплова вітрина HURAKAN HKN-WD2»), SKU67 (ART1168676811 «Теплова вітрина HURAKAN HKN-WD3M»), SKU81 (ART2059507443 «Теплова вітрина Hurakan WD-120L»). Эти SKU → SKIP-НП (тело из фида НП позже), вносятся в таблицу при обработке батчей б5 (SKU34) / б7 (SKU53/54) / б9 (SKU66/67) / б11 (SKU81). Прочие бренды (SARO и др.) НЕ в НП-списке — обрабатываются обычно.

Категории (эталон chunk-019 / chunk-061): **blk триплет** = `descUA==descRU` True И col5==col4 (UA-leak имя) И col7 (NAZVRU) genuine RU → col5←col7 + col36 полный тег-в-tag перевод source col35. **blknotrip** = lang-neutral бренд+код имя (col5==col4 не UA-leak) → переводится только col36. **blknochg** = `descUA!=descRU` (отдельный чистый genuine RU, col5==col7) → fixed.xlsx НЕ трогается; артефакты/опечатки soft-note (НЕ нумеруются). **SKIP-НП** = NP-эксклюзивный бренд (forward-only, тело из фида НП позже).

---
