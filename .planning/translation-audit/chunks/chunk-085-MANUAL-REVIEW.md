# chunk-085 — Manual Review (W2)

**Источник:** `chunk-085.xlsx` (75 SKU, rows 2-76)
**Фиксы:** `chunk-085-fixed.xlsx`
**Бранч:** translation-audit/w2 (W2 — параллельный воркер, ФИНАЛЬНЫЙ chunk в диапазоне 055-085)
**Формат-эталон:** chunk-019 (категории blk триплет / blknotrip / blknochg / blkfix / SKIP-НП).

## Обзор

- 75 SKU rows 2..76
- **5 SKIP-НП preliminary (HURAKAN):** r3 (HKN-ISV5P шприц колбасный), r20 (HKN-ISH5P), r21 (HKN-ISV5P), r32 (HKN-ISV7P), r69 (HKN-EF16 чебуречница)
- Батч = 8 SKU; ожидается ~10 батчей (8×9 + 3 = 75)

## Категории

- **blk триплет** (TRIP): c5←c7 + c36 полный RU-перевод тела (c35==c36 source UA)
- **blknotrip**: c5←c7, тело c36 уже RU (без перевода)
- **blknochg**: c5==c7 genuine RU, c36 не менять
- **blkfix**: c5/c36 содержит UA остатки/typo → точечная правка
- **SKIP-НП**: бренд ∈ {HURAKAN, APACH, FAGOR, TATRA, COLD, PROJECT SYSTEMS, ASTORIA, ARRIS, MAXIMA} → ячейки не менять, тело из фида НП позже

## Прогресс

### b1 (rows 2-9, SKU 1-8) — 8/75 DONE

- **TRIP 4** (c5←c7 + c36 RU faithful):
  - r6 SKU5 art=479241642 FROSTY SH-3 — Шприц колбасный 3 л горизонтальный, цилиндр и корпус н/с, объем 3 л, 4 насадки Ø16/22/32/38 мм, две скорости, габариты 470х230х240 мм
  - r7 SKU6 art=479243219 FROSTY SH-5 — Шприц колбасный 5 л горизонтальный, объем 5 л, габариты 590х230х240 мм (same template)
  - r8 SKU7 art=479244052 FROSTY SH-7 — Шприц колбасный 7 л горизонтальный, объем 7 л, габариты 830х230х240 мм (same template)
  - r9 SKU8 art=479246896 FROSTY SV-3 — Шприц колбасный 3 л **вертикальный**, габариты 300х340х570 мм (same template, only orientation+dims differ)
- **blknochg 3** (c5==c7 genuine RU, c36 уже RU):
  - r2 SKU1 art=1536892541 FROSTY FL288 white — Шкаф холодильный, c36_len 515
  - r4 SKU3 art=2044205614 Frosty EVS-15N — Шприц колбасный электрический, c36_len 683
  - r5 SKU4 art=2354729311 Frosty SEV12 — Шприц колбасный электрический, c36_len 846
- **SKIP-НП 1** HURAKAN:
  - r3 SKU2 art=1546890217 Hurakan HKN-ISV5P BLACK Шприц колбасный (тело из фида НП позже)
- **Verify:** 48 PASS / 0 FAIL
- Без новых OQ

### b2 (rows 10-17, SKU 9-16) — 16/75 DONE

- **TRIP 4** (c5←c7 + c36 RU faithful):
  - r10 SKU9 art=479313108 FROSTY SV-5 — Шприц колбасный 5 л вертикальный, 300х340х690 (same SV template as b1.r9)
  - r11 SKU10 art=479314413 FROSTY SV-7 — 7 л вертикальный, 300х340х830
  - r12 SKU11 art=479317523 FROSTY SV-10 — 10 л вертикальный, 300х340х580
  - r17 SKU16 art=1145162184 Hendi 282090 — Шприц колбасный 7 л вертикальный (наполнитель фарша); расширенное body (силиконовая прокладка отдельно, цилиндр 140x460(h), габариты 300x300x(H)770мм мм — typo «мм мм» в source сохранён faithful)
- **blknochg 4** (c5==c7 genuine RU):
  - r13 SKU12 art=1137316611 GoodFood SF3VS — Шприц колбасный вертикальный, c36_len 460
  - r14 SKU13 art=1137324164 GoodFood SF7VS — c36_len 462
  - r15 SKU14 art=1137326083 GoodFood SF10VS — c36_len 462
  - r16 SKU15 art=1137329926 GoodFood SF15VS — c36_len 462
- **Verify:** 48 PASS / 0 FAIL
- Без новых OQ
