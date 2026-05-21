# chunk-084 OQ #15 apply — 2026-05-21

**Status:** APPLIED (per Yana direct verification via tefcold.com).

## Verification source

- **Tefcold UF50GCP canonical page:** https://www.tefcold.com/uf50gcp-16332
- Item Number: 16332 (Tefcold URL pattern `/<model>-<id>`; ранее пробовал `/uf50gcp` без id → 404).

## Правка

- **SKU:** r6 ART=2141730389 Tefcold UF50GCP (морозильный шкаф настольный, стеклянная дверь с подогревом)
- **Поля:** col35 UA + col36 RU body
- **Замена (1× в каждом столбце):** `220-230V` → `220-240V` в характеристике «Электрическое питание / Електричне живлення»
- **Причина:** Tefcold canon = `220-240 V / 50 Hz` (стандартный евро-диапазон). UA-источник имел опечатку `220-230V` — пропагирована в RU как faithful UA→RU. Canonical numeric fix.
- Категория r6 переходит blknochg → blkfix.

## Сверка всех specs vs Tefcold canon

Все 12 параметров body соответствуют Tefcold UF50GCP canon:

| Поле | RU body | Tefcold canon | Verdict |
|---|---|---|---|
| Объём | 48 л | "50 / 48 l" (gross/net useful) | ✓ (упрощено до useful — допустимо) |
| Темп. режим | -24 .. -12 °C | -24 to -12 °C | ✓ |
| Хладагент | R290 | R290 | ✓ |
| Мощность | 154 Вт | 154 W | ✓ |
| **Питание** | **220-230V** | **220-240/50 V/Hz** | **⚠️ FIXED → 220-240V** |
| Длина | 570 мм | 570 mm | ✓ |
| Глубина | 530 мм | 530 mm | ✓ |
| Высота | 657 мм | 657 mm | ✓ |
| Вес | 42 кг | "46 / 42 kg" (net/gross) | ✓ (упрощено) |
| Дверь | стеклянная с подогревом самозакрывающаяся | 1 heated hinged glass door | ✓ |
| Полки | 2 решетчатые белые 440×210 мм | 2 wire shelves white 440 x 210 mm | ✓ |
| Тип охлаждения | Статическое | Static cooling | ✓ |

## Items NOT in body (canon mentions, но UA source не содержал — не добавляем)

Climate class 4, Energy class C, Daily 2.82 kWh/24h, Annual 1031 kWh/year, EEI 22%, Noise 45 dB(A), Refrigerant charge 45 g, Lock, Display area 0.23 m², Mechanical controller, Manual defrost, Aluminium interior. Faithful UA→RU policy — не выдумываем.

## OQ #15 closed

`W2-OQ-ANSWERS.md` cum table OQ#15 update: PENDING → APPLIED 2026-05-21.
