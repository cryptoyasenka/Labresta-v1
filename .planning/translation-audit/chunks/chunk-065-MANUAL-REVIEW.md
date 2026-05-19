# chunk-065 — manual review (W2)

**Source:** `horoshop-export 13.05.26.xlsx` chunk-065 (81 SKU)
**Apply key:** `Артикул` (col1, scoped per row)
**Status:** b1 DONE 8/81 (b2 предстоит; batch=8, b11=SKU81 1 SKU)
**Worker:** W2 (параллельный, диапазон chunk-055 … chunk-085); продолжение chunk-064
**Last updated:** chunk-065 b1 (W2)

Эталон формата: chunk-019-MANUAL-REVIEW.md / chunk-064-MANUAL-REVIEW.md. Категории: blk триплет / blknotrip / blknochg / SKIP-НП. Кумул. OQ закрыты.

## SKIP-НП (НП-эксклюзивные бренды, forward-only, тело из фида НП позже)

| # | SKU | Артикул | Бренд | Название (UA) | Примечание |
|---|---|---|---|---|---|
| prelim | 64 | 1147781261 | HURAKAN | Вафельниця HURAKAN HKN-GES2M для бельгійських вафель | HURAKAN — НП-эксклюзив, тело из фида НП позже |
| prelim | 69 | 2059494027 | Hurakan | Вафельниця Hurakan HKN-GES2L | HURAKAN — НП-эксклюзив, тело из фида НП позже |
| prelim | 70 | 2059501393 | Hurakan | Вафельниця гонконгська Hurakan HKN-GES5HK | HURAKAN — НП-эксклюзив, тело из фида НП позже |

## Открытые вопросы chunk-065

_(нумерация отдельная, начинается с #1; пока нет)_

---

## b1 — SKU 1-8 (rows 2-9), 8/81

**Категории:** blk триплет 1 · blknotrip 0 · blknochg 7 · SKIP-НП 0 = 8.

| # | SKU | Артикул | Бренд / модель | Категория | Действие |
|---|---|---|---|---|---|
| 1 | 1 | 2121426618 | Hendi 211427 Concept Line | blk триплет | col5 ← c7 (genuine RU «Кипятильник Concept Line Hendi 211427»); col36 — faithful RU перевод описания (skel==c35, dims==c35: 230/502/1650/357/275/380/16/3.09, deg/degL пустые, UA-clean, без ё) |
| 2 | 2 | 2172891828 | GoodFood WB30A | blknochg | c5==c7 genuine RU, c35!=c36 (c36 уже RU) — fixed НЕ тронут |
| 3 | 3 | 2188566582 | GoodFood WB08 RED | blknochg | c5==c7 genuine RU, c35!=c36 (c36 уже RU, открывается `<h4>`) — fixed НЕ тронут |
| 4 | 4 | 2190227669 | GoodFood WB08 BLACK | blknochg | c5==c7 genuine RU, c35!=c36 (c36 уже RU, открывается `<h4>`) — fixed НЕ тронут |
| 5 | 5 | 2190229516 | GoodFood WB30S | blknochg | c5==c7 genuine RU, c35!=c36 (c36 уже RU, открывается `<h4>`) — fixed НЕ тронут |
| 6 | 6 | 2190231269 | GoodFood WB20S | blknochg | c5==c7 genuine RU, c35!=c36 (c36 уже RU, открывается `<h4>`) — fixed НЕ тронут |
| 7 | 7 | 2190243226 | GoodFood WB06DW | blknochg | c5==c7 genuine RU, c35!=c36 (c36 уже RU, открывается `<h4>`) — fixed НЕ тронут |
| 8 | 8 | 2190246661 | GoodFood WB08DW | blknochg | c5==c7 genuine RU, c35!=c36 (c36 уже RU, открывается `<h4>`) — fixed НЕ тронут |

**Verify:** 89 PASS / 0 FAIL (ART 81 rows + TRIP 1 + blknochg 7).

**Глоссарий b1:** +12 net-new (Hendi 211427 Concept Line RU перевод) + ~6 reuse; см. `chunk-glossary-w2.md` (757 → 769).

**Soft-notes (pre-existing в c36 датасете, не наша правка):** GoodFood blknochg SKU2-8 — c36 уже переведено: SKU2 открывается `<p>` (без `<h4>`); SKU3-8 открываются `<h4>` (вместо `<p>` как в c35); используется «общепита» (UA «громадського харчування»); в c35 встречается `&#39;` HTML-entity-апостроф. Эти отличия pre-existing в c36, fixed.xlsx не трогаем.

**Открытых вопросов b1:** нет.

---

<!-- Сводка по батчу b2 ниже. -->
