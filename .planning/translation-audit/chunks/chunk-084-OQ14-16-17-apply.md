# chunk-084 OQ #14 / #16 / #17 apply — 2026-05-21

**Status:** APPLIED (per Yana decisions via AskUserQuestion, ref W2-OQ-ANSWERS.md).

## OQ #14 — r4 Tefcold FSC100

- **ART=2139145953**, col36 RU body
- **Замена (1 вхождение):** `FS80CP` → `FSC100` в h2 проз
- **Verification (tefcold.com + whitegoods.ru):** FSC100 canonical = 100/60 л, +2..+10°C, 655×390×930, 51/46 кг, R600A, 0.22 кВт — body specs точно совпадают. Опечатка модели в проз была copypasta от r2 FS80CP (specs которого случайно совпали).
- Категория r4 переходит blknochg → blkfix.
- **Forward W1:** col35 UA body «FS80CP → FSC100».

## OQ #16 — r21/r22/r23/r24 Gi Metal AC-SP (4 SKU щёток для чистки печи)

- **col5 + col7 RU** для 4 SKU (8 правок суммарно)
- **Замена:** Latin `c` (U+0063) → Cyrillic `с` (U+0441) в `чиcтки` → `чистки`
- **Причина:** mixed-script typo в source feed canonical c7. c5←c7 verbatim → Latin c пропагирован. Поломан SEO/поиск по «чистка» в Horoshop.
- **Note:** c36 body уже использовал правильный Cyrillic `с` (не трогался).

## OQ #17 — r39 REEDNEE RT78B white

- **ART=641916589**, col36 RU body
- **Замена (1 вхождение):** `REEDNEE RT78L` → `REEDNEE RT78B` в h2 проз
- **Specs не тронуты.**
- **Verification (maresto.ua = поставщик):** REEDNEE RT78B canonical specs = 78 л / 0..+12°C / 0.17 кВт / 428×386×960 / R600a / 220В / 33.8 кг (брутто 36.2) — body в фиде УЖЕ описывает эти specs верно. Web-specs «RT78L» (resko.com.ua / vagi-axis / nenwell) были про разные бренды / комплектации, не REEDNEE. Specs mismatch concern → СНЯТ.
- Категория r39 переходит blknochg → blkfix (был triplet после b5, теперь blkfix по h2 model code).
- Source URL: https://maresto.ua/ua/catalog/kholodilnoe_oborudovanie/shkaf_vitrina_kholodilnaya_reednee_rt78b_white.html

## OQ #15 — r6 Tefcold UF50GCP (PENDING)

- col36 RU body уже переписан W2 в b1 как faithful UA→RU (908 chars, specs 48л/R290/-24..-12/154Вт/570×530×657/42кг).
- Yana попросила сверить через https://www.tefcold.com/ — `/uf50gcp` 404. Pending: alternative URL or accept-as-is.
- NOT APPLIED в этом коммите.
