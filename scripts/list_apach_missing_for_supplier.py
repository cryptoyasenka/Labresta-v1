"""Generate the list of Apach SKUs missing from np.com.ua dealer-export feed,
grouped by product series, ready to paste into a supplier message.

Reads PromProduct rows where brand='Apach' that have no confirmed/manual
ProductMatch. Article is extracted from name (display_article is empty for
these PPs). Output groups by series prefix (APL / APKE / AFM / AD46 / ...)
so Yana can mark "Очікується" rows by hand against the dealer portal.

Yana already confirmed:
  - AD46MV: not at supplier at all → flagged for our catalog cleanup, not feed request
  - APL: in catalog, out of stock (Очікується) — supplier should still feed it
  - APKE-77: "Очікується 26.05.2026" — same

Run on prod (read-only):
  $env:DATABASE_URL="<DATABASE_PUBLIC_URL>"
  & .venv/Scripts/python.exe scripts/list_apach_missing_for_supplier.py
"""
import os
import re
import sys
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy import func, select

from app import create_app
from app.extensions import db
from app.models.catalog import PromProduct
from app.models.product_match import ProductMatch

# Yana's note 2026-05-09: AD46MV — реально нет у поставщика, не просим добавить.
# Filter pattern matches both "AD46MV" alone and inside name (case-insensitive).
NOT_AT_SUPPLIER_PATTERNS = [r"\bAD46MV\b"]


def extract_article(pp: PromProduct) -> str:
    """Pull the article token from name. PP names follow patterns like:
        'Плита електрична APACH APRE-77P'
        'Apach AD46MV'
        'Планетарний міксер Apach APL 5B 1Ф'
        'Котел APACH APKE-77'
    Strategy: case-insensitive find of 'apach', then take alphanumeric token
    sequence right after it (allowing dashes, dots, spaces, digits) until
    we hit a phase suffix (1Ф/3Ф/220В/380В) or paren or end.
    """
    name = pp.name or pp.name_ru or ""
    m = re.search(r"\bapach\b\s*[\"']?\s*", name, flags=re.IGNORECASE)
    if not m:
        return ""
    tail = name[m.end():].strip()
    # stop at phase markers, parens, common suffixes
    stop_re = re.compile(r"\s*(?:[1-3]\s*Ф|220\s*В|380\s*В|\(|з\s+|для\s+|\d+\s*л\b|чотири|три|2-|3-|4-|–|—)",
                         flags=re.IGNORECASE)
    sm = stop_re.search(tail)
    if sm:
        tail = tail[:sm.start()]
    # strip trailing punctuation/whitespace
    tail = re.sub(r"[\s,;:.]+$", "", tail)
    # collapse multiple spaces
    tail = re.sub(r"\s+", " ", tail).strip()
    return tail


# Status notes Yana confirmed against the dealer portal on 2026-05-09:
#   - APL ×8 (planetary mixers): "є в базі, нема у наявності, очікується"
#   - APKE-77 (kettle):           "Очікується 26.05.2026"
#   - AFM 02 / AFM 03 (refrig. tables): visible on dealer portal (screenshot)
# Everything else needs visual check by Yana.
STATUS_RULES = [
    (r"^APL\b",   "ОЧІКУЄТЬСЯ (Yana бачила на порталі — буде у наявності)"),
    (r"^APKE\b",  "ОЧІКУЄТЬСЯ 26.05.2026 (Yana, скрин 2026-05-09)"),
    (r"^AFM\s*02\b", "Є на дилер-порталі (Yana, скрин 2026-05-09)"),
    (r"^AFM\s*03\b", "Є на дилер-порталі (Yana, скрин 2026-05-09)"),
]


def status_label(article: str) -> str:
    a = article.upper()
    for pattern, label in STATUS_RULES:
        if re.search(pattern, a):
            return label
    return "потребує перевірки на дилер-порталі"


def status_priority(article: str) -> int:
    """Lower number = print first. Confirmed «очікується» go first."""
    a = article.upper()
    if re.search(r"^APKE\b", a):
        return 0          # explicit «Очікується 26.05.2026»
    if re.search(r"^APL\b", a):
        return 1          # «буде у наявності»
    if re.search(r"^AFM\s*0[23]\b", a):
        return 2          # confirmed visible on portal
    return 9              # needs check


SERIES_RULES = [
    ("APL (планетарний міксер)",  r"^APL\b"),
    ("APKE (котел)", r"^APKE\b"),
    ("AFM (стіл холодильний/морозильний)", r"^AFM\b"),
    ("APRE (плита електрична)", r"^APRE\b"),
    ("APRG (плита газова)", r"^APRG\b"),
    ("AD46 (піч конвекційна)", r"^AD46"),
    ("AP5/AP10 (пароконвектомат)", r"^AP(?:5|10)"),
    ("ASH (шок-заморожування)", r"^ASH"),
    ("ASM (тістоміс)", r"^ASM"),
    ("ASF (тісторозкатка)", r"^ASF"),
    ("AHM (міксер занурювальний)", r"^AHM"),
    ("AMX (мілкшейк)", r"^AMX"),
    ("AMS (піч для піци)", r"^AMS"),
    ("AMT (конвеєрна піч)", r"^AMT"),
    ("ACS (соковижималка)", r"^ACS"),
    ("ACG (кавомолка)", r"^ACG"),
    ("AK (посудомийна)", r"^AK\b"),
    ("M30 (ферментатор)", r"^M30\b"),
    ("L33 (тістоміс)", r"^L33"),
]


def classify_series(article: str) -> str:
    a = article.upper().strip()
    for label, pattern in SERIES_RULES:
        if re.search(pattern, a):
            return label
    return "Інше"


def is_not_at_supplier(article: str, name: str) -> bool:
    text = f"{article} {name}"
    return any(re.search(p, text, flags=re.IGNORECASE) for p in NOT_AT_SUPPLIER_PATTERNS)


def main() -> int:
    app = create_app()
    with app.app_context():
        confirmed_pp_ids = set(db.session.execute(
            select(ProductMatch.prom_product_id).where(
                ProductMatch.status.in_(("confirmed", "manual"))
            )
        ).scalars().all())

        pps = db.session.execute(
            select(PromProduct).where(
                func.lower(PromProduct.brand) == "apach"
            )
        ).scalars().all()

        missing = [pp for pp in pps if pp.id not in confirmed_pp_ids]

        # Build records: (pp_id, article, name, series, status, prio)
        records = []
        excluded = []
        for pp in missing:
            art = extract_article(pp)
            name = (pp.name or pp.name_ru or "").strip()
            if is_not_at_supplier(art, name):
                excluded.append((pp.id, art, name))
                continue
            series = classify_series(art) if art else "Інше"
            status = status_label(art)
            prio = status_priority(art)
            records.append((pp.id, art, name, series, status, prio))

        # Sort: priority first (confirmed «очікується» go first), then series, then article
        records.sort(key=lambda r: (r[5], r[3], r[1]))

        # Group by series
        by_series = defaultdict(list)
        for rec in records:
            by_series[rec[3]].append(rec)

        print(f"\n{'='*78}")
        print(f"Apach PP без confirmed match — згруповано за серіями")
        print(f"  Всього у каталозі:               {len(pps)}")
        print(f"  З confirmed match:               {len(pps) - len(missing)}")
        print(f"  БЕЗ match (відсутні у фіді):     {len(missing)}")
        print(f"  Виключено (нема у постачальника): {len(excluded)}")
        print(f"  До запиту постачальнику:         {len(records)}")
        print(f"{'='*78}\n")

        if excluded:
            print("### ВИКЛЮЧЕНО (Yana підтвердила: реально немає у постачальника)\n")
            for pp_id, art, name in excluded:
                print(f"  PP#{pp_id}  art={art!r}  {name[:80]!r}")
            print("  → ці позиції не просимо додати у фід; їх треба прибрати з нашого каталогу.\n")

        # Series order: SERIES_RULES order is already arranged with confirmed
        # «очікується» series (APL, APKE, AFM) at the top.
        series_order = [label for label, _ in SERIES_RULES] + ["Інше"]

        for series in series_order:
            rows = by_series.get(series, [])
            if not rows:
                continue
            confirmed = sum(1 for r in rows if r[5] < 9)
            print(f"### {series} — {len(rows)} шт.  ({confirmed} підтверджено)")
            print(f"  {'Артикул':<25} {'Назва':<60}  Статус")
            print(f"  {'-'*25} {'-'*60}  {'-'*45}")
            for pp_id, art, name, _, status, _prio in rows:
                print(f"  {art:<25} {name[:60]:<60}  {status}")
            print()

        # --- Block ready to paste into supplier message ---
        print(f"\n{'='*78}")
        print("BLOCK FOR SUPPLIER MESSAGE (Ukrainian, copy-paste below)")
        print(f"{'='*78}\n")
        print("Шановні колеги!\n")
        print("Звертаємося щодо дилер-експорту з np.com.ua (dealer_id=69781).")
        print("У вашому дилерському кабінеті у каталозі Apach ми бачимо суттєво")
        print("більше моделей, ніж потрапляє у XLSX/CSV-експорт (зараз 158 SKU).")
        print("Перевірили всі параметри URL (filetype=xlsx|csv|xml|yml,")
        print("platform=horoshop|prom|opencart|woocommerce, без platform,")
        print("with_all=1/with_full=1/include_disabled=1) — результат однаковий.\n")
        print("Прохання додати у дилер-експорт наступні позиції,")
        print("які присутні у вашому дилерському кабінеті, але відсутні у фіді:\n")

        # Confirmed «очікується» first
        print("  ── ПОЗИЦІЇ У СТАТУСІ «ОЧІКУЄТЬСЯ» (підтверджено клієнтом за дилер-порталом) ──\n")
        printed_any_confirmed = False
        for series in series_order:
            rows = [r for r in by_series.get(series, []) if r[5] < 9]
            if not rows:
                continue
            printed_any_confirmed = True
            print(f"  {series}:")
            for pp_id, art, name, _, status, _prio in rows:
                print(f"    • {art}  —  {name}   [{status}]")
            print()
        if not printed_any_confirmed:
            print("  (немає)\n")

        print("  ── РЕШТА ПОЗИЦІЙ (у наявності або під замовлення на дилер-порталі) ──\n")
        for series in series_order:
            rows = [r for r in by_series.get(series, []) if r[5] >= 9]
            if not rows:
                continue
            print(f"  {series}:")
            for pp_id, art, name, _, _status, _prio in rows:
                print(f"    • {art}  —  {name}")
            print()

        print("Дякуємо!\n")
        print(f"{'='*78}\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
