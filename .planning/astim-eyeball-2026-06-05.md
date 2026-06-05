# astim — NEEDS-EYEBALL refinement (2026-06-05)

Read-only refinement of the 10 **astim** rows under `## NEEDS-EYEBALL` in `candidate-triage-2026-06-05.md`. No DB writes — every `match_id` was re-verified against `product_matches` (all `status=candidate`, pp_id/sp_id confirmed) and each PP was checked for a 1:1 conflict via `SELECT … WHERE prom_product_id=? AND id<>? AND status IN ('confirmed','manual')`. **No PP and no SP is held by any confirmed/manual match** — so there are zero invariant-#15 rejects here; every reject is a genuine domain (product-type / size) mismatch.

Root cause of the bucket: the auto-matcher scored these on **article-number equality** (PP `display_article` == SP `article`). That signal is unreliable for astim — for the score-100 rows the SP "article" is an internal/order id, and for the score-86 rows the SP article does not even equal the PP display_article (`617908` vs `525197`, `975862` vs `596883`). The **product names** are the source of truth, and in 9 of 10 cases they describe entirely different products. Only m4444 (citrus juicer ≈ citrus press, code 695906 byte-identical) is a real match.

Counts: **10 total — CONFIRM(clean) 0 / CONFIRM(judgment) 1 / AMBIGUOUS 0 / REJECT 9** (all 9 = domain mismatch, 0 = #15).

| match_id | PP (brand + key tokens) | SP (brand + key tokens) | score | 1:1 | REC | reason |
|---:|---|---|---|:---:|---|---|
| 4436 | (no brand) Ніж ЯНАГИБА 24см SEKIRYU SR-240S — sushi knife | (no brand) Шестерня ковбасного шприца 282571… — sausage-stuffer gear | 100 | free | REJECT(domain) | product types unrelated (knife vs gear); match only on internal-id art `103` |
| 4437 | Hendi Контейнер для тіста 14л `880906` — dough container | (no brand) Контейнер для їжі GN 1/1 `470190` — GN food container | 100 | free | REJECT(domain) | different Hendi product/code (880906 vs 470190), different type/capacity |
| 4444 | Hendi Соковижималка/прес для цитрусових `695906` — citrus press | (no brand) Соковитискач для цитрусових `695906` — citrus juicer | 100 | free | CONFIRM(judgment) | code 695906 byte-identical; соковижималка/прес ≈ соковитискач (synonyms), same type, no size clash |
| 4445 | Hendi Тирса/тріска для копчення `Z CZE1996951` — woodchips 250г | (no brand) Тріска для копчення дуб `Z CZE1996951` — woodchips 150г | 100 | free | REJECT(domain) | same product type but capacity differs: 250г vs 150г |
| 4438 | Hendi Форма для піци `617908` ø240 — pizza pan | HENDI Дерев'яна лопатка для млинців `525197` — pancake spatula | 86 | free | REJECT(domain) | unrelated product types; articles differ (617908 vs 525197) |
| 4439 | Hendi Форма для піци `617953` ø360 — pizza pan | HENDI Дерев'яна лопатка для млинців `525197` — pancake spatula | 86 | free | REJECT(domain) | unrelated product types; articles differ (617953 vs 525197); SP 8376 fanned to 3 PPs |
| 4440 | Hendi Форма для піци `617984` ø500 — pizza pan | HENDI Дерев'яна лопатка для млинців `525197` — pancake spatula | 86 | free | REJECT(domain) | unrelated product types; articles differ (617984 vs 525197); SP 8376 fanned to 3 PPs |
| 4441 | Hendi Сифон для вершків `975862` Kurt Scheller блакитний — cream siphon | HENDI Відкривачка для пляшок настінна `596883` — wall bottle opener | 86 | free | REJECT(domain) | unrelated product types; articles differ (975862 vs 596883) |
| 4442 | Hendi Сифон для вершків `975855` Kurt Scheller жовтий — cream siphon | HENDI Відкривачка для пляшок настінна `596883` — wall bottle opener | 86 | free | REJECT(domain) | unrelated product types; articles differ (975855 vs 596883); SP 7700 fanned to 3 PPs |
| 4443 | Hendi Сифон для вершків `975879` Kurt Scheller зелений — cream siphon | HENDI Відкривачка для пляшок настінна `596883` — wall bottle opener | 86 | free | REJECT(domain) | unrelated product types; articles differ (975879 vs 596883); SP 7700 fanned to 3 PPs |

Notes:
- "1:1 = free" means no other `confirmed`/`manual` match holds that PP (or that SP) — verified in DB.
- SP 8376 (lopatka) is auto-fanned across PPs 1938/1939/1940; SP 7700 (vidkryvachka) across PPs 4705/4706/4707. Even ignoring the type clash, one SP cannot legitimately satisfy three distinct PPs — all six are rejected on the product-type mismatch directly.

## Decisions

**CONFIRM (clean):** none

**CONFIRM (judgment):** 4444 — Hendi citrus juicer; SP article `695906` == PP display_article `695906`, product type agrees (соковижималка/прес ≈ соковитискач), no dimension conflict, PP/SP both free. SP brand null + article-driven origin → judgment tier rather than silent auto-confirm.

**AMBIGUOUS:** none

**REJECT — invariant #15 (PP already held):** none

**REJECT — domain mismatch:** 4436, 4437, 4445, 4438, 4439, 4440, 4441, 4442, 4443 (9)
- 4436 — knife vs sausage-stuffer gear; matched only on internal-id article.
- 4437 — dough container (880906) vs GN food container (470190); different code/type/capacity.
- 4445 — smoking woodchips, weight differs 250г vs 150г.
- 4438 / 4439 / 4440 — pizza pan vs pancake spatula (SP 8376); article 617xxx vs 525197.
- 4441 / 4442 / 4443 — cream siphon vs wall bottle opener (SP 7700); article 975xxx vs 596883.
