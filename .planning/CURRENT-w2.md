# CURRENT-w2 — LabResta translation audit (W2 параллельный воркер)

**Last touched:** 2026-05-18 (chunk-057 scaffold — продолжение chunk-056)
**Status:** **chunk-057 scaffold** (chunk-057-diff.md + chunk-057-MANUAL-REVIEW.md созданы, source скопирован+прозондирован 54 SKU; 0/54); chunk-056 ЗАКРЫТ 91/91; chunk-055 ЗАКРЫТ 86/86; OQ#1 chunk-055 (SKU 10 модель-код) + OQ#1 chunk-056 (SKU 67) ждут ответа Yana (не блокируют); next: scaffold-коммит + push → СРАЗУ chunk-057 батч 1 SKU 1-8 (НЕПРЕРЫВНЫЙ режим)

> **РЕЖИМ: НЕПРЕРЫВНЫЙ НОЧНОЙ (Yana 2026-05-18).** НЕ останавливаться после одного батча. После коммита+push сразу следующий батч (range +8), пока весь диапазон chunk-055…085 не закрыт. Контекст переполнился → снапшот+auto-compact+restore из этого файла, продолжать. Cron 15m = только страховка на смерть сессии. Стоп только: весь диапазон готов, ИЛИ нужен ответ Yana (тогда зафиксировать OQ и идти дальше по остальным SKU). См. memory `feedback-w2-continuous-night-mode`.

## Диапазон W2
- ТОЛЬКО chunk-055 … chunk-085. НИКОГДА не трогать chunk-≤054 (W1) и не редактировать main.
- Ветка: `translation-audit/w2`. Push в `origin translation-audit/w2` (НЕ main).
- State-файл W2: этот файл. НЕ трогать `.planning/CURRENT.md` (W1).

## Status
- [x] CURRENT-w2.md создан (первый заход W2)
- [x] chunk-055 scaffold: `chunk-055-diff.md` + `chunk-055-MANUAL-REVIEW.md` + `chunk-glossary-w2.md`
- [x] chunk-055.xlsx source скопирован в W2 (gitignored, read-only)
- [x] chunk-055 батч SKU 1-8 → 8/86 (blknochg 4 / blk триплет 2 / blknotrip 2 / SKIP-НП 0; OQ 0)
- [x] chunk-055 батч SKU 9-16 → 16/86 (blknotrip 4 / blk триплет 2 / blknochg 2 / SKIP-НП 0; OQ#1 SKU 10 модель-код)
- [x] chunk-055 батч SKU 17-24 → 24/86 (blknochg 3 / blk триплет 5 / blknotrip 0 / SKIP-НП 0; OQ 0, кумул. OQ#1 SKU 10)
- [x] chunk-055 батч SKU 25-32 → 32/86 (blk триплет 3 / blknochg 3 / SKIP-НП 2 (Hurakan 27/29) / blknotrip 0; OQ 0, кумул. OQ#1 SKU 10)
- [x] chunk-055 батч SKU 33-40 → 40/86 (blknochg 7 (Dadaux 33-37 + Sirman 38/39) / blk триплет 1 (Fimar SE1550 SKU 40) / SKIP-НП 0 / blknotrip 0; OQ 0, кумул. OQ#1 SKU 10)
- [x] chunk-055 батч SKU 41-48 → 48/86 (blknochg 7 (Sirman 42/43 + Fimar 44 + GoodFood 45-48) / blk триплет 1 (Fimar SE1550 220 SKU 41) / SKIP-НП 0 / blknotrip 0; OQ 0, кумул. OQ#1 SKU 10)
- [x] chunk-055 батч SKU 49-56 → 56/86 (blknochg 6 (GoodFood 49 + Frosty 50/56 + FIMAR 53/54/55) / blk триплет 2 (Frosty DS1000 SKU 51 + FIMAR E3 SKU 52) / SKIP-НП 0 / blknotrip 0; OQ 0, кумул. OQ#1 SKU 10)
- [x] chunk-055 батч SKU 57-64 → 64/86 (blk триплет 8 (диски овощерезки Frosty E1/E5/FM/H3/H4/H7/H8/H10) / blknochg 0 / blknotrip 0 / SKIP-НП 0; OQ 0, кумул. OQ#1 SKU 10)
- [x] chunk-055 батч SKU 65-72 → 72/86 (blk триплет 8 (диски овощерезки Frosty H14/HU2.5/HU4/HU10/P2/P4/PB2/PB4) / blknochg 0 / blknotrip 0 / SKIP-НП 0; OQ 0, кумул. OQ#1 SKU 10)
- [x] chunk-055 батч SKU 73-80 → 80/86 (blk триплет 5 (Frosty T 8/T10 + Нож-диск FS100 + FIMAR B 8/B10) / blknochg 3 (FIMAR D8*8/D10*10/D12*12 genuine RU `Диск для овощерезки FIMAR D*`) / blknotrip 0 / SKIP-НП 0; OQ 0, кумул. OQ#1 SKU 10; +3 термина, кумул. 47)
- [x] chunk-055 батч SKU 81-86 → 86/86 (blk триплет 5 (FIMAR D20x20/E1/E4/E5/E8) / blknochg 1 (FIMAR E6 genuine RU, soft-note δ=5 vs 6) / blknotrip 0 / SKIP-НП 0; OQ 0, кумул. OQ#1 SKU 10; +0 терминов, кумул. 47) — **chunk-055 ЗАКРЫТ**
- [x] chunk-056 scaffold (W2, продолжение chunk-055) — COMMITTED fbca2e0
- [x] chunk-056 батч SKU 1-8 → 8/91 (blk триплет 6 (Fimar E10/E14/H 2.5/H 4/H 8/V) / blknochg 2 (Fimar H 6/H10 genuine RU) / blknotrip 0 / SKIP-НП 0; реальная дробь SKU3 2.5→2,5; OQ 0, кумул. OQ#1 SKU 10 chunk-055; +7 строк глоссария, кумул. 54)
- [x] chunk-056 батч SKU 9-16 → 16/91 (blk триплет 6 (Fimar Z3/Z4/Z7/Z2 + RC 27070/27164) / blknochg 2 (Frosty D8/D10 genuine RU) / blknotrip 0 / SKIP-НП 0; реальные дроби веса SKU15 0.64/0.7, SKU16 0.5; soft-note SKU13 `магневый` genuine RU; OQ 0, кумул. OQ#1 SKU 10 chunk-055; +6 строк глоссария, кумул. 60)
- [x] chunk-056 батч SKU 17-24 → 24/91 (blk триплет 8 (Robot Coupe 28004/28016/28051/28052/28053/28054/28057/28058) / blknochg 0 / blknotrip 0 / SKIP-НП 0; реальные дроби веса SKU17 0.7/SKU18 0.5/SKU19-20 0.61/SKU21 0.59+0.7/SKU22 0.58+0.7/SKU23 0.5; SKU19↔20 идентичные UA-копии; OQ 0, кумул. OQ#1 SKU 10 chunk-055; +13 строк глоссария, кумул. 73)
- [x] chunk-056 батч SKU 25-32 → 32/91 (blk триплет 8 (Robot Coupe 28059/28061/28062/28063/28064/28065/28101/28110) / blknochg 0 / blknotrip 0 / SKIP-НП 0; реальные дроби SKU25 0.6/SKU26 0.5/SKU27-28 0.59+0.7/SKU29 0.61+0.7/SKU30-31 0.7/SKU32 1.3; OQ 0, кумул. OQ#1 SKU 10 chunk-055; +6 строк глоссария, кумул. 79)
- [x] chunk-056 батч SKU 33-40 → 40/91 (blk триплет 8 (Robot Coupe 28111/28114/28134/28135/28195/28197 + комплекты 1960/1961) / blknochg 0 / blknotrip 0 / SKIP-НП 0; реальные дроби SKU33 1.3/SKU34 1.14+1.3/SKU35 1.3/SKU36 1.18+1.3/SKU37 0.7/SKU38 0.7/SKU39 3.5/SKU40 4.68; Latin x 2,5x2,5/12 x 12 x 12 SKU37/38 policy-B; `<ul>\n<li>` `\n`-склеен verbatim; OQ 0, кумул. OQ#1 SKU 10 chunk-055; +8 строк глоссария, кумул. 87)
- [x] chunk-056 батч SKU 41-48 → 48/91 (blk триплет 8 (RC 28189 комплект-пюре + Frosty E2/D8A/D10А/D12А/D20A + RC 27069/28067 spec-блок) / blknochg 0 / blknotrip 0 / SKIP-НП 0; реальные дроби Вес: 0.40/0.36/0.32/0.27; целые Вес 3 / Вес брутто 0,45/0,41/0,4/0,35 как в источнике; Latin x policy-B; `<br />`+`\n` verbatim SKU48; финал D10А/D12А кир. А / D20A/E2 лат. A; OQ 0, кумул. OQ#1 SKU 10 chunk-055; +19 строк глоссария, кумул. 106)
- [x] chunk-056 батч SKU 49-56 → 56/91 (blk триплет 5 (RC 28073/28115/28113/1933/28208 replace-from-source) / blknochg 3 (RC 28173/27219 + Fimar E2 genuine RU descUA!=descRU LIVE не переписан) / blknotrip 0 / SKIP-НП 0; двойств. x SKU53 кир.х(0445)+лат.x(0078) byte-точно; `<br />`+`\n` verbatim SKU53; модель-коды CL/R verbatim; 2 soft-note (SKU51 дубль-предлог / SKU56 магневый — НЕ нумер. OQ); реальных дробей нет; OQ 0, кумул. OQ#1 SKU 10 chunk-055; +9 строк глоссария, кумул. 115)
- [x] chunk-056 батч SKU 57-64 → 64/91 (blk триплет 4 (RC 27786/28112/1945 + Fimar A2 replace-from-source) / blknochg 4 (Bezzera Arcadia/ARCA1DE2NG3 + GGM Catarina KMF2 + Nuova Simonelli OSCAR II genuine RU descUA!=descRU LIVE не переписан) / blknotrip 0 / SKIP-НП 0; 10х10х10 кир.х(0445) SKU58 dim-integrity / 4*4мм * SKU59 / несбаланс.( R402 SKU59 verbatim; 2 soft-note SKU62 Диамерт / SKU63 помещения-изляция НЕ нумер.; реальн. дроби Вес 0,27/1,19/1,3/0,5, целое Вес 2; OQ 0, кумул OQ#1 SKU10 chunk-055; +6 строк глоссария, кумул 121)
- [x] chunk-056 батч SKU 65-72 → 72/91 (blk триплет 2 (Hendi 208656/428245 replace-from-source) / blknotrip 1 (Hendi 208342 нок-бокс — бренд+код language-neutral, только descRU перевод) / blknochg 5 (Nuova Simonelli APPIA LIFE S 2GR/Appia Life 1Gr S/APPIA II V 1GR/Appia Compact Life S 2GR/APPIA LIFE V 2GR genuine RU descUA!=descRU LIVE не переписан) / SKIP-НП 0; габариты Ø250x(H)70мм/190x240x(H)410/265x162x(H):100 Latin x(0078) dim-integrity byte-точно; UA-апостроф об'ємом→объемом SKU71; **OQ#1 chunk-056 SKU67 Nuova Simonelli APPIA II V 1GR ↔ genuine RU Appia Life 1Gr V** (UA-описание само Appia Life V 1Gr; customer-facing рассинхрон модель-кода, НЕ авто-фикс, chunk-056-questions.md создан); 1 soft-note SKU66 теплообмеником→теплообменником НЕ нумер.; реальных дробей в blk/blknotrip нет; OQ chunk-056 = 1 (#1 SKU67), кумул OQ#1 SKU10 chunk-055; +6 строк глоссария, кумул 127)
- [x] chunk-056 батч SKU 73-80 → 80/91 (blk триплет 3 (Hendi 208380/208649/208670 replace-from-source) / blknotrip 1 (Hendi 208731 темпер Ø58 — бренд+код language-neutral, только descRU перевод) / blknochg 4 (Nuova Simonelli Appia Compact Life V 2GR/Oscar II AD + Bezzera B2016 DE/White/PM//White genuine RU descUA!=descRU LIVE не переписан) / SKIP-НП 0; габариты 275x175x(H)110/205x150x(H)45/100x150x(H)45/ø58x(h)95(lc ø U+00F8) Latin x(0078) dim-integrity byte-точно; UA-копия quirk Дерев'яна забарвлений ручка→Деревянная окрашенная ручка SKU76; темного дерева SKU73 language-neutral (false-pos UA_MARK снят); 3 soft-note НЕ нумер. (SKU77 профессиональнаяNuova склейка / SKU79 PM//White двойной слеш / SKU76 рассогл. рода); новых нумер. OQ НЕТ; OQ chunk-056 = 1 (#1 SKU67), кумул OQ#1 SKU10 chunk-055; +6 строк глоссария, кумул 133)
- [x] chunk-056 батч SKU 81-88 → 88/91 (blk триплет 3 (Hendi 211472/Bartscher 190193/Hendi PROFI LINE 208533 replace-from-source) / blknochg 5 (Nuova Simonelli Oscar Mood Tank/Saro ECO/GGM KC2W/KC3S/KC3W genuine RU descUA!=descRU LIVE не переписан) / blknotrip 0 / SKIP-НП 0; реальн. дроби SKU83 6.5→6,5/7.82→7,82, UA-уже-запятая 1,8 SKU88; UA_MARK false-pos сняты Перколятор(идент.UA/RU)+Контрольна(префикс RU Контрольная); 3 soft-note НЕ нумер. (SKU82 рассогл. тело Кавоварку/имя Кавомашина UA-копии / SKU85-87 GGM genuine RU изляция→изоляция / SKU81 genuine тело кофеварка); новых нумер. OQ НЕТ; OQ chunk-056=1 (#1 SKU67), кумул OQ#1 SKU10 chunk-055; +10 строк глоссария кумул 143)
- [x] chunk-056 батч SKU 89-91 → 91/91 (blk триплет 3 (Hendi 208304 проточная кофеварка / TOP LINE BY WEGA 208915 1гр. / 208939 2гр. replace-from-source) / blknochg 0 / blknotrip 0 / SKIP-НП 0; габариты 200х385х430 кир.х(0445) / 530x555x515 / 740x555x515 лат.x(0078) dim-integrity byte-точно; UA-апостроф об'єму/кип'ятку/Об'єм SKU90→0; UA-уже-запятая 1,8×2/2,9/10,5/3,7 сохранены, реальных .-дробей нет; 1 soft-note НЕ нумер. (SKU91 смешанная UA/RU UA-копия — уже-RU строки byte-точно, переведены только UA-сегменты); `Тенів`→`ТЭНов` note глоссарий; новых нумер. OQ НЕТ; OQ chunk-056=1 (#1 SKU67), кумул OQ#1 SKU10 chunk-055; +11 строк глоссария кумул 154) — **chunk-056 ЗАКРЫТ**
- [x] scaffold chunk-057 (W2, продолжение chunk-056): chunk-057-diff.md + chunk-057-MANUAL-REVIEW.md созданы; source скопирован, прозондирован (54 SKU); chunk-glossary-w2.md НЕ пересоздан (общий, 154 строки, продолжается)
- [ ] scaffold-коммит chunk-057 + CURRENT-w2 маркер + push → chunk-057 батч 1 SKU 1-8 → … chunk-085

## chunk-055 итог (ЗАКРЫТ)
- 86/86. blknochg 36 / blk триплет 42 / blknotrip 6 / SKIP-НП 2 (Hurakan SKU 27/29). Открытых вопросов 1 (OQ#1 SKU 10 Hendi 843468/843499 — ждёт ответа Yana, не блокирует).

## chunk-056 итог (ЗАКРЫТ)
- 91/91. blk триплет 64 / blknochg 25 / blknotrip 2 / SKIP-НП 0. Открытых вопросов 1 (OQ#1 SKU 67 Nuova Simonelli APPIA II V 1GR ↔ Appia Life V 1Gr — ждёт ответа Yana, не блокирует). Глоссарий кумул. 154 строки.

## chunk-057 факты
- 54 SKU (openpyxl rows 2..55, row = SKU + 1). Первый: Артикул `902327287` Hendi `Кавомашина Hendi PROFI LINE XXL 208991 (автомат)`. Последний SKU54: Артикул `525346665` Apach `Соковижималка для цитрусових Apach ACS1 ECO`.
- Колонка `Бренд` в источнике дублирует числовой `Артикул` — бренд определяется per-SKU по `Название` (col6). Зонд: SKU1-4 Hendi (кавомашина / нок-боксы / підставка), SKU5-8 Victoria Arduino Black Eagle.
- **SKIP-НП:** зонд → 1 NP-suspect hit = **SKU54 (Артикул `525346665`) Apach** — **APACH** в НП-списке → SKIP-НП (вносится при батче 7). Прочие бренды НЕ в НП-списке, обрабатываются обычно (подтверждается per-батч по `Название`).
- Батч = 8 SKU, 7 батчей (последний батч 7 = SKU 49-54 = 6 SKU).

## Open files
- `.planning/translation-audit/chunks/chunk-057-diff.md` — diff (scaffold, **IN PROGRESS 0/54**)
- `.planning/translation-audit/chunks/chunk-057-MANUAL-REVIEW.md` — ручная проверка (scaffold, **IN PROGRESS 0/54**)
- `.planning/translation-audit/chunks/chunk-057.xlsx` — source (read-only, gitignored, скопирован из main worktree)
- `.planning/translation-audit/chunks/chunk-057-fixed.xlsx` — НЕ создан (создаётся при батче 1: `cp chunk-057.xlsx chunk-057-fixed.xlsx` один раз)
- `.planning/translation-audit/chunks/chunk-glossary-w2.md` — сводный глоссарий W2 (общий накопительный, **154 строки**; chunk-057 продолжает, НЕ пересоздан)
- chunk-056 (ЗАКРЫТ): chunk-056-diff.md / chunk-056-MANUAL-REVIEW.md DONE 91/91; chunk-056-fixed.xlsx 91/91 verified `=== ALL OK ===`; chunk-056-questions.md OQ#1 SKU67 ждёт Yana
- chunk-055 (ЗАКРЫТ): chunk-055-diff.md / chunk-055-MANUAL-REVIEW.md DONE 86/86; chunk-055-fixed.xlsx 86/86 verified; OQ#1 SKU 10 ждёт Yana

## Next step
**chunk-057 scaffold готов** (chunk-057-diff.md + chunk-057-MANUAL-REVIEW.md созданы, source скопирован+прозондирован 54 SKU). Далее без остановки (НЕПРЕРЫВНЫЙ режим):
1. Очистить scratch `_w2_probe_057.py` / `_w2_probe_057.txt`.
2. **scaffold-коммит** (контент: новые `chunk-057-diff.md` + `chunk-057-MANUAL-REVIEW.md`) автор LabResta `chunk-057 scaffold (W2, продолжение chunk-056)` → затем CURRENT-w2 маркер-коммит `CURRENT-w2: chunk-057 scaffold (W2, продолжение chunk-056)` → push origin translation-audit/w2.
3. **СРАЗУ chunk-057 батч 1 SKU 1-8** (rows 2..9, openpyxl `range(2,10)` / SKU `range(1,9)`): дамп → SKIP-НП-чек бренда по `Название` → категоризация (blk триплет / blknochg / blknotrip / SKIP-НП) → `_w2_apply_057_b1.py` (ПЕРВЫЙ батч chunk-057: `cp chunk-057.xlsx chunk-057-fixed.xlsx` ОДИН раз, затем edit by Артикул; SURV для chunk-057 стартует с нуля — анкеры b1.. свои) → `=== ALL OK ===` → 4 артефакта (diff entries+summary Status N/54 + MANUAL-REVIEW + glossary новые термины + CURRENT-w2) → 2 коммита (контент+маркер) автор LabResta → push.
4. Затем батчи 2-7 chunk-057 (батч 7 = SKU 49-54 = 6 SKU, SKU54 Apach → SKIP-НП), затем chunk-058 … chunk-085. НЕ останавливаться (НЕПРЕРЫВНЫЙ режим), пока весь диапазон не закрыт или не нужен ответ Yana.

Методология (та же W1, что chunk-055/056): для каждого SKU дамп UA/RU name+nm+desc+kw в UTF-8-файл. SKIP-НП-чек бренда по `Название` (HURAKAN/APACH/FAGOR/TATRA/COLD/PROJECT SYSTEMS/ASTORIA/ARRIS/MAXIMA — case-insens, лат+кир; **chunk-057: зонд → SKU54 Apach в НП-списке → SKIP-НП при батче 7; прочие (Hendi, Victoria Arduino, …) НЕ в списке → обычная обработка, подтверждается per-батч**) → если бренд в списке: пометить «SKIP-НП» в MANUAL-REVIEW, fixed.xlsx не менять, отд. категория, только вперёд. Иначе: `desc UA==RU` False→**blknochg** (genuine рус., LIVE НЕ переписывать, «Было/Стало: без изменений»; совпадение длин при разном контенте всё равно blknochg — прец. SKU 35/53/54/85) / True→полный тег-в-tag RU-перевод (**blk триплет** если Назв.мод RU=nm_ua UA-leak а Назв RU genuine→ставим Назв.мод RU=nazv_ru; **blknotrip** если Назв/Назв.мод бренд+код language-neutral). META keywords всегда faithful. Апостроф `&#39;`/`'`→0 RU. Реальные дроби `N.N`→`N,N` ТОЛЬКО UA-копии (blk/blknotrip). Вес `NN.00` политика A verbatim. Латин.x(0x78) габариты глоб.B verbatim; кир.х(0x445) no-op. `&delta;`/`&ndash;`/`(Д*Ш*В)`/disc-коды/voltage language-neutral verbatim. Source-typo в UA-копии (переводится) → авто-норма + glossary note. Source-typo/расхождение значения в genuine RU (blknochg) → soft-note в MANUAL-REVIEW НЕ нумеровать (прец. SKU 18/38/39/85). Модель-код в NAME UA↔genuine-RU рассинхрон → нумерованный Открытый вопрос НЕ авто-фикс (прец. OQ#1 SKU 10).

**fixed.xlsx (chunk-057 ПЕРВЫЙ батч):** `cp .planning/translation-audit/chunks/chunk-057.xlsx .planning/translation-audit/chunks/chunk-057-fixed.xlsx` (один раз при б1), затем edit by Артикул, save, reopen read_only VERIFY booleans. Со 2-го батча — load СУЩЕСТВУЮЩИЙ chunk-057-fixed.xlsx (НЕ копировать source). SURV-анкеры chunk-057 свои (стартуют с нуля, не наследуются от chunk-056). Scratch `_w2_*` удалять после (glob `_w2_*bNN*` МИНУЕТ `_w2_bNN_result.txt` — удалять явно).

После батча: контент-коммит (chunk-057-diff.md entries+summary Status N/54 + chunk-057-MANUAL-REVIEW.md + chunk-glossary-w2.md новые термины; НЕ fixed.xlsx/НЕ CURRENT-w2) → коммит CURRENT-w2 маркер «CURRENT-w2: chunk-057 батч X-Y COMMITTED N/54» → push origin translation-audit/w2. Обновлять CURRENT-w2 каждый батч. **НЕПРЕРЫВНЫЙ режим — не останавливаться, пока весь диапазон 055-085 не закрыт или не нужен ответ Yana (тогда зафиксировать OQ и идти дальше по остальным SKU). 7 батчей chunk-057, последний батч 7 = SKU 49-54 (6 SKU).**

## Workflow напоминание
- Источник: `chunk-NN.xlsx` (read-only, копируется из `C:/Projects/labresta-sync/.planning/translation-audit/chunks/` — gitignored). Python: `C:/Projects/labresta-sync/.venv/Scripts/python.exe` (в W2 .venv нет).
- Выход: `chunk-NN-fixed.xlsx` (gitignored) + `chunk-NN-diff.md` + `chunk-NN-MANUAL-REVIEW.md` (в git). Сомнения → `chunk-NN-questions.md`.
- Батч = 8 SKU. Между чанками: scaffold-коммит «chunk-NNN scaffold (W2, продолжение chunk-NNN-1)».
- ЗАПРЕЩЕНО: Status в INDEX.md; коммит/push в main; следы AI в коммитах (автор только Yana, без Co-Authored-By/Generated with Claude); хардкод секретов.

## Decisions / constraints
- W2 .venv отсутствует → используется python main-воркт ри `C:/Projects/labresta-sync/.venv/Scripts/python.exe` (openpyxl 3.1.5 OK).
- chunk-NN.xlsx gitignored (`*.xlsx`), source копируется из main worktree, в W2 read-only.
- chunk-glossary-w2.md — новый файл (у W1 нет отдельного сводного, термины внутри его MANUAL-REVIEW). W1-глоссарий = READ-ONLY референс.
- INDEX.md Status НЕ править (W1 владеет статус-доской).
