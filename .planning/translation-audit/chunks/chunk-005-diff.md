# chunk-005 UA+RU revision diff (84 SKU)

**Source:** `.planning/translation-audit/chunks/chunk-005.xlsx` (84 rows × 14 operator UA/RU fields)
**Brand family:** mixed — REEDNEE, Tatra, Oztiryakiler, Airhot, Hendi, Spidocook, ATA, Silver, Hurakan, FROSTY, Unox, GoodFood, EWT INOX, Apach, GGM Gastro International, Kogast.
**Categories:** electric plates (ATA K7EVC continuation), мангалы/гриллы (Airhot/Hendi/Apach), griddle surfaces (Silver gas), various.

**Apply rule:** Ключ применения — Артикул, не порядковый номер. Каждый `Было/Стало` блок строго scoped к артикулу указанному в SKU header.

**Standard locked patterns from chunk-004:**
- META trunc UA: drop trailing `, плити електричні для` (or category equivalent)
- META trunc RU: `Плиты элект` → `Плиты электрические` (or category equivalent)
- `Так` → `Да` (RU `Наличие`/`наявність` fields)
- empty `<li>Наличие базы</li>` → `<li>Наличие базы Нет</li>` (if UA confirms Ні)
- `Двери` pl → `Дверь` sg + strip trailing dot on optional model SKUs (`K7PORTA.` etc.)
- `с четырьмя/двумя/шести` → `с 4/2/6`
- `и духовка` (nominative leak) → `и духовкой` (instrumental)
- Missing `Вт` unit in `Электрическая мощность, N` → restore
- UA decimal `.` → `,`
- UA `<p> </p>` empty / structural defects → flag, don't fix automatically
- **NEVER** write Ukrainian `електро`/`електрична` inside RU "Было" blocks (mixed-Cyrillic broke anchors twice in chunk-004)

**New patterns to watch in this chunk (mixed-brand):**
- Brand-specific cross-keyword stuffing (e.g. Hendi META containing Apach terms)
- Silver gas griddle terms (`поверхня для смаження газова` → `поверхня для смаження`/`griddle`)
- Tatra/Kogast/EWT INOX EU-spec terms

---
