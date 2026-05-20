# chunk-075 MANUAL REVIEW (W2, продолжение chunk-074)

**Status:** chunk-075 b3 DONE 24/54 (cum TRIP 3 / blknotrip 0 / blknochg 19 / blkfix 0 / SKIP-НП 2; 821 PASS / 0 FAIL) — next b4 (SKU 25-32, rows 26-33)
**Last updated:** chunk-075 b3 (24/54)

**Объём:** 54 SKU rows 2..55. ART 2044220842..1090581793.

**Категории (preliminary по бренд-префиксам):**
- Шкафы расстоечные Frosty/Moretti Forni/GoodFood/Ефес (~28 в начале r2-r31)
- Шкафы расстоечные APACH/FAGOR/HURAKAN/COLD (SKIP-НП внутри блока)
- Шокеры (тестомесы / охладители?) (~5: r37/41/44/46/47)
- Холодильное / морозильное оборудование (~6: r48-53)
- PIMAK / Tecnodom / прочее

**SKIP-НП preliminary (12 rows):**
- r3 HURAKAN HKN-XLT196M
- r4 APACH APE12ABQ D
- r32 FAGOR (TBD model)
- r33 FAGOR (TBD model)
- r34 APACH (TBD model)
- r35 HURAKAN (TBD model)
- r36 HURAKAN (TBD model)
- r38 COLD (TBD model)
- r42 APACH (TBD model)
- r43 APACH (TBD model)
- r45 COLD (TBD model)
- r54 HURAKAN (TBD model)

**Cumulative state (start):** TRIP 0 + blknotrip 0 + blknochg 0 + blkfix 0 + SKIP-НП 0 = 0/54.

**Plan (batches):**
- b1: SKU 1-8 (r2-9)
- b2: SKU 9-16 (r10-17)
- b3: SKU 17-24 (r18-25)
- b4: SKU 25-32 (r26-33)
- b5: SKU 33-40 (r34-41)
- b6: SKU 41-48 (r42-49)
- b7 FINAL: SKU 49-54 (r50-55) — 6 SKUs

---

## b1 DONE 8/54 (Status update)

**Status:** chunk-075 b1 DONE 8/54 (cum TRIP 3 / blknotrip 0 / blknochg 3 / blkfix 0 / SKIP-НП 2; 709 PASS / 0 FAIL) — next b2 (SKU 9-16, rows 10-17)

**b1 распределение (SKU 1-8):**
- TRIP 3: r2 Frosty VF-15, r7 Moretti Forni L80/S100E, r8 Moretti Forni 0A000810
- blknochg 3: r5 GoodFood PR13TS, r6 GoodFood PR16TS, r9 Эфес ШР-6-GN 1/1
- SKIP-НП 2: r3 HURAKAN HKN-XLT196M, r4 APACH APE12ABQ D

**Quirks:** r2 «м&#39;якішу»→«мякиша» (HTML-апостроф снят); r8 mixed source (RU intro + UA body); r8 «Дека для випічки»→«Противни для выпечки».

---

## b2 DONE 16/54 (Status update)

**Status:** chunk-075 b2 DONE 16/54 (cum TRIP 3 / blknotrip 0 / blknochg 11 / blkfix 0 / SKIP-НП 2; 765 PASS / 0 FAIL) — next b3 (SKU 17-24, rows 18-25)

**b2 распределение (SKU 9-16):** blknochg 8 — полный блок Эфес ШР-6/8/10 / GN1/1 / GN2/1 / -К варианты (r10-r17), все c5==c7 «Шкаф расстоечный Эфес ...» genuine RU, c36 genuine RU bodies. Fixed cells НЕ тронуты.

---

## b3 DONE 24/54 (Status update)

**Status:** chunk-075 b3 DONE 24/54 (cum TRIP 3 / blknotrip 0 / blknochg 19 / blkfix 0 / SKIP-НП 2; 821 PASS / 0 FAIL) — next b4 (SKU 25-32, rows 26-33)

**b3 распределение (SKU 17-24):** blknochg 8 — смешанный блок: PIMAK MYK1 (r18 расстоечный) + Эфес пекарские ШПЭ-1/2/3/4 (r19-r23) + Эфес жарочный ШЖЭ-1-GN1/1 (r24) + Эфес ШПЭ-3 дубль (r25, мощность 20,16 vs 20,6 у r22). Все c5==c7 genuine RU, c36 genuine RU. Fixed cells НЕ тронуты. Source quirk r19 «комплектеп» preserved.
