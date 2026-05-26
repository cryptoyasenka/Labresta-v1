# PHASE B — Intended translation propagation
**Question:** for each translation edit we made in chunks 016–029, did it reach LIVE?
**Method:** parse all `chunk-NNN-diff.md` 016–029 → for each edit, compute `intended = apply(pre_incident, diff)` → compare to LIVE
**Inputs:**
- PRE-INCIDENT: `horoshop-export 20.05.26.xlsx` (read-only)
- LIVE-NOW: `horoshop-export 21.05.26.xlsx` (read-only)
- Chunks: 016..029 (14 files)

## Top-level — 725 edits classified
| Flag | Count | % | Meaning |
|---|---:|---:|---|
| OK | 336 | 46.3% | translation reached LIVE |
| STALE | 20 | 2.8% | edit stayed only in our file, LIVE = pre-incident value |
| WIPED | 0 | 0.0% | LIVE is empty, broken import wiped, never recovered |
| WRONG | 0 | 0.0% | LIVE has something else (manual edit / collision) |
| FAIL | 369 | 50.9% | PARTIAL patch could not be applied (base differs / was not found) |
| **TOTAL** | 725 | 100.0% | |

## Per-chunk breakdown
| Chunk | Edits | OK | STALE | WIPED | WRONG | FAIL |
|---|---:|---:|---:|---:|---:|---:|
| 016 | 96 | 48 | **0** | 0 | 0 | 48 |
| 017 | 48 | 26 | **0** | 0 | 0 | 22 |
| 018 | 38 | 17 | **0** | 0 | 0 | 21 |
| 019 | 67 | 33 | **0** | 0 | 0 | 34 |
| 020 | 35 | 15 | **0** | 0 | 0 | 20 |
| 021 | 28 | 13 | **0** | 0 | 0 | 15 |
| 022 | 82 | 41 | **0** | 0 | 0 | 41 |
| 023 | 61 | 28 | **0** | 0 | 0 | 33 |
| 024 | 63 | 26 | **0** | 0 | 0 | 37 |
| 025 | 56 | 28 | **0** | 0 | 0 | 28 |
| 026 | 42 | 20 | **0** | 0 | 0 | 22 |
| 027 | 53 | 26 | **0** | 0 | 0 | 27 |
| 028 | 30 | 15 | **0** | 0 | 0 | 15 |
| 029 | 26 | 0 | **20** | 0 | 0 | 6 |

## Per-column breakdown
| Column | OK | STALE | WIPED | WRONG | FAIL |
|---|---:|---:|---:|---:|---:|
| Название модификации (RU) | 336 | **8** | 0 | 0 | 0 |
| Описание товара (RU) | 0 | **5** | 0 | 0 | 369 |
| Описание товара (UA) | 0 | **7** | 0 | 0 | 0 |

## STALE matrix (chunk × column) — actionable
Numbers in this table = translations we did but LIVE still shows pre-incident value. Non-zero cell = we can re-emit them safely if we want them live.

| Chunk | Название модификации (RU) | Описание товара (RU) | Описание товара (UA) |
|---|---:|---:|---:|
| 029 | 8 | 5 | 7 |

## Samples — STALE (per column, first 8 each)

### Название модификации (RU) — 20 STALE
(showing 8)
- chunk-029 `756820696`
  - PRE/LIVE (same): `Мінібар FROSTY BC-70`
  - INTENDED:        `Минибар FROSTY BC-70`
- chunk-029 `1861418399`
  - PRE/LIVE (same): `Холодильна шафа барна REEDNEE LG128`
  - INTENDED:        `Шкаф холодильный барный REEDNEE LG128`
- chunk-029 `1861432292`
  - PRE/LIVE (same): `Холодильна шафа барна REEDNEE LG198S`
  - INTENDED:        `Шкаф холодильный барный REEDNEE LG198S`
- chunk-029 `2198692061`
  - PRE/LIVE (same): `Вітрина холодильна EWT INOX RT78B black`
  - INTENDED:        `Витрина холодильная EWT INOX RT78B black`
- chunk-029 `2198699235`
  - PRE/LIVE (same): `Вітрина холодильна EWT INOX RT78B white`
  - INTENDED:        `Витрина холодильная EWT INOX RT78B white`
- chunk-029 `2288293724`
  - PRE/LIVE (same): `Вітрина холодильна EWT INOX RT98B white`
  - INTENDED:        `Витрина холодильная EWT INOX RT98B white`
- chunk-029 `1158533303`
  - PRE/LIVE (same): `Холодильний мінібар Hendi 233900`
  - INTENDED:        `Холодильный минибар Hendi 233900`
- chunk-029 `1158547556`
  - PRE/LIVE (same): `Холодильний мінібар Hendi 233917`
  - INTENDED:        `Холодильный минибар Hendi 233917`

### Описание товара (RU) — 20 STALE
(showing 5)
- chunk-029 `1861402673`
  - PRE/LIVE (same): `<h2> Барный холодильный шкаф компактный Hata DR200S S/S201 с корпусом из нержавеющей стали AISI 201.</h2> <p>Может служи`
  - INTENDED:        `<h2> Барный холодильный шкаф компактный Hata DR200S S/S201 с корпусом из нержавеющей стали AISI 201.</h2> <p>Может служи`
- chunk-029 `1861402673`
  - PRE/LIVE (same): `<h2> Барный холодильный шкаф компактный Hata DR200S S/S201 с корпусом из нержавеющей стали AISI 201.</h2> <p>Может служи`
  - INTENDED:        `<h2> Барный холодильный шкаф компактный Hata DR200S S/S201 с корпусом из нержавеющей стали AISI 201.</h2> <p>Может служи`
- chunk-029 `1861402673`
  - PRE/LIVE (same): `<h2> Барный холодильный шкаф компактный Hata DR200S S/S201 с корпусом из нержавеющей стали AISI 201.</h2> <p>Может служи`
  - INTENDED:        `<h2> Барный холодильный шкаф компактный Hata DR200S S/S201 с корпусом из нержавеющей стали AISI 201.</h2> <p>Может служи`
- chunk-029 `1861418399`
  - PRE/LIVE (same): `<h2>Барна холодильна шафа REEDNEE LG128 зі скляною двецею у чорному корпусі.</h2> <ul>
<li>обсяг 128 л</li>
<li>корпус ч`
  - INTENDED:        `<h2>Барный холодильный шкаф REEDNEE LG128 со стеклянной дверцей в чёрном корпусе.</h2> <ul>
<li>объём 128 л</li>
<li>кор`
- chunk-029 `1861432292`
  - PRE/LIVE (same): `<h2>Барна холодильна шафа REEDNEE LG198S з двома скляними дверима в чорному корпусі.</h2> <ul>
<li>обсяг 198 л</li>
<li>`
  - INTENDED:        `<h2>Барный холодильный шкаф REEDNEE LG198S с двумя стеклянными дверями в чёрном корпусе.</h2> <ul>
<li>объём 198 л</li>
`

### Описание товара (UA) — 20 STALE
(showing 7)
- chunk-029 `1861402673`
  - PRE/LIVE (same): `<h2>Барна холодильна шафа компактна Hata DR200S S/S201 з корпусом з нержавіючої сталі AISI 201.</h2> <p>Може служити як `
  - INTENDED:        `<h2>Барна холодильна шафа компактна Hata DR200S S/S201 з корпусом з нержавіючої сталі AISI 201.</h2> <p>Може служити як `
- chunk-029 `1861402673`
  - PRE/LIVE (same): `<h2>Барна холодильна шафа компактна Hata DR200S S/S201 з корпусом з нержавіючої сталі AISI 201.</h2> <p>Може служити як `
  - INTENDED:        `<h2>Барна холодильна шафа компактна Hata DR200S S/S201 з корпусом з нержавіючої сталі AISI 201.</h2> <p>Може служити як `
- chunk-029 `1861418399`
  - PRE/LIVE (same): `<h2>Барна холодильна шафа REEDNEE LG128 зі скляною двецею у чорному корпусі.</h2> <ul>
<li>обсяг 128 л</li>
<li>корпус ч`
  - INTENDED:        `<h2>Барна холодильна шафа REEDNEE LG128 зі скляною дверцею у чорному корпусі.</h2> <ul>
<li>обсяг 128 л</li>
<li>корпус `
- chunk-029 `1861418399`
  - PRE/LIVE (same): `<h2>Барна холодильна шафа REEDNEE LG128 зі скляною двецею у чорному корпусі.</h2> <ul>
<li>обсяг 128 л</li>
<li>корпус ч`
  - INTENDED:        `<h2>Барна холодильна шафа REEDNEE LG128 зі скляною двецею у чорному корпусі.</h2> <ul>
<li>обсяг 128 л</li>
<li>корпус ч`
- chunk-029 `1861418399`
  - PRE/LIVE (same): `<h2>Барна холодильна шафа REEDNEE LG128 зі скляною двецею у чорному корпусі.</h2> <ul>
<li>обсяг 128 л</li>
<li>корпус ч`
  - INTENDED:        `<h2>Барна холодильна шафа REEDNEE LG128 зі скляною двецею у чорному корпусі.</h2> <ul>
<li>обсяг 128 л</li>
<li>корпус ч`
- chunk-029 `1861432292`
  - PRE/LIVE (same): `<h2>Барна холодильна шафа REEDNEE LG198S з двома скляними дверима в чорному корпусі.</h2> <ul>
<li>обсяг 198 л</li>
<li>`
  - INTENDED:        `<h2>Барна холодильна шафа REEDNEE LG198S з двома скляними дверима в чорному корпусі.</h2> <ul>
<li>обсяг 198 л</li>
<li>`
- chunk-029 `1861432292`
  - PRE/LIVE (same): `<h2>Барна холодильна шафа REEDNEE LG198S з двома скляними дверима в чорному корпусі.</h2> <ul>
<li>обсяг 198 л</li>
<li>`
  - INTENDED:        `<h2>Барна холодильна шафа REEDNEE LG198S з двома скляними дверима в чорному корпусі.</h2> <ul>
<li>обсяг 198 л</li>
<li>`

## Samples — FAIL (per column, first 8 each)

### Описание товара (RU) — 369 FAIL
(showing 8)
- chunk-016 `477739756` — reason: `partial_was_not_found:'(полностью идентично UA — украинский текст)'`
  - PRE:  `<h3>Піч конвекційна Unox XB693 на 6 рівнів: ідеальний вибір для професійної кухн`
  - LIVE: `<h3>Піч конвекційна Unox XB693 на 6 рівнів: ідеальний вибір для професійної кухн`
- chunk-016 `477739760` — reason: `partial_was_not_found:'(полностью идентично UA — украинский текст)'`
  - PRE:  `<h3>Конвекційна піч Unox XB 893 &ndash; ваш ідеальний помічник на кухні 🍴</h3> <`
  - LIVE: `<h3>Конвекційна піч Unox XB 893 &ndash; ваш ідеальний помічник на кухні 🍴</h3> <`
- chunk-016 `477739781` — reason: `partial_was_not_found:'(полностью идентично UA — украинский текст)'`
  - PRE:  `<h3>Пароконвектомат Unox XEBC10EUEPRM лінія Plus: Ідеальне поєднання ефективност`
  - LIVE: `<h3>Пароконвектомат Unox XEBC10EUEPRM лінія Plus: Ідеальне поєднання ефективност`
- chunk-016 `505661168` — reason: `partial_was_not_found:'(полностью идентично UA — украинский текст)'`
  - PRE:  `<p>Піч конвекційна Unox XF003 Roberta &mdash; це ідеальне рішення для ресторанів`
  - LIVE: `<p>Піч конвекційна Unox XF003 Roberta &mdash; це ідеальне рішення для ресторанів`
- chunk-016 `505816134` — reason: `partial_was_not_found:'(полностью идентично UA — украинский текст)'`
  - PRE:  `<h3>Пароконвектомат Unox XEVC0711EPRM лінія PLUS: продуктивність, інновації та н`
  - LIVE: `<h3>Пароконвектомат Unox XEVC0711EPRM лінія PLUS: продуктивність, інновації та н`
- chunk-016 `525347671` — reason: `partial_was_not_found:'(полностью идентично UA — украинский текст)'`
  - PRE:  `<h3>Піч конвекційна Apach AD44M ECO: острівна піч для бездоганної техніки</h3> <`
  - LIVE: `<h3>Піч конвекційна Apach AD44M ECO: острівна піч для бездоганної техніки</h3> <`
- chunk-016 `525347672` — reason: `partial_was_not_found:'(полностью идентично UA — украинский текст)'`
  - PRE:  `<h3>Піч конвекційна Apach AD44MH ECO: ідеальне рішення для вашого бізнесу! 🧑&zwj`
  - LIVE: `<h3>Піч конвекційна Apach AD44MH ECO: ідеальне рішення для вашого бізнесу! 🧑&zwj`
- chunk-016 `525347673` — reason: `partial_was_not_found:'(полностью идентично UA — украинский текст)'`
  - PRE:  `<h3>Піч конвекційна Apach AD44M: надійність, ефективність та ідеальний результат`
  - LIVE: `<h3>Піч конвекційна Apach AD44M: надійність, ефективність та ідеальний результат`
