"""Generate readable markdown report from labresta_x_verify.json."""
import json


def main():
    with open("labresta_x_verify.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    s = data["summary"]
    lines = [
        "# Сверка Лабреста Х.xlsx с БД",
        "",
        f"**Всего в файле: {s['total']} товаров**",
        "",
        "| Статус | Кол-во |",
        "|---|---|",
        f"| ✅ Сматчено confirmed/manual | {s['matched_ok']} |",
        f"| 🟡 Только candidate (нужен клик Confirm) | {s['matched_candidate']} |",
        f"| 🔴 SP есть, но нет match-строки (скорер не нашёл PP) | {s['no_match']} |",
        f"| ⚫ Вообще нет как SP в БД (проблема фида?) | {s['no_sp']} |",
        "",
        "---",
        "",
        f"## 🟡 Candidate — нужно подтвердить ({s['matched_candidate']})",
        "",
        "Эти товары уже есть как матчи-кандидаты. Просто открой и нажми Confirm.",
        "",
    ]
    for p in data["matched_candidate"]:
        art = p["article"]
        lines.append(f"- **{art}** (SP#{p['sp_id']}) — {p['name']}")
        lines.append(f"  - [Открыть](http://127.0.0.1:5050/matches?supplier_id=2&status=candidate&search={art})")
    lines.append("")

    lines.extend([
        "---",
        "",
        f"## 🔴 SP есть, но нет match-строки ({s['no_match']})",
        "",
        "Скорер не нашёл подходящий PP в каталоге — либо артикул в каталоге отличается, либо PP вообще нет.",
        "Решение: пойти в UI, найти SP, нажать 'Сопоставить вручную' и поискать по имени.",
        "",
    ])
    for p in data["no_match"]:
        art = p["article"]
        lines.append(f"- **{art}** (SP#{p['sp_id']}) — {p['name']}")
        lines.append(f"  - Labresta URL (справочно): {p['lab_url']}")
        lines.append(f"  - [Найти SP в UI](http://127.0.0.1:5050/products/supplier?search={art})")
    lines.append("")

    lines.extend([
        "---",
        "",
        f"## ⚫ Нет как SP в БД вообще ({s['no_sp']})",
        "",
        "Эти товары в файле Лабреста Х есть, но в фиде поставщика (БД SP) отсутствуют.",
        "Возможные причины: поставщик снял с фида, товар ignored, артикул в фиде другой.",
        "",
    ])
    for p in data["no_sp"]:
        art = p["article"]
        lines.append(f"- **{art}** — {p['name']}")
        lines.append(f"  - NP URL: {p['np_url']}")
        lines.append(f"  - Labresta URL: {p['lab_url']}")
    lines.append("")

    with open("LABRESTA_X_REPORT.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("Wrote LABRESTA_X_REPORT.md")
    print(f"\n{s['matched_ok']}/{s['total']} done, {s['total']-s['matched_ok']} to review")


if __name__ == "__main__":
    main()
