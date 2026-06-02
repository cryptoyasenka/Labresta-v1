"""OPT-IN AI re-check of an ALREADY-GENERATED Horoshop create-card XLSX.

This is R2 (AI RE-CHECK), NOT an AI tier in the live generator. The generator's
chain stays feed→analogy→fallback with AI OFF, and its auto-picked «Раздел» is
authoritative. This script is a SEPARATE, on-demand audit Yana runs by hand: it
asks an LLM to independently classify each card and REPORTS only the rows where
the model DISAGREES with the auto category (or has no confident opinion). It
NEVER writes/overrides a category and touches NO database.

Provider-agnostic: any OpenAI-compatible /chat/completions endpoint works. Pick
it with --base-url + --model and point --api-key-env at the env var that holds
the key. Defaults target NVIDIA NIM (integrate.api.nvidia.com/v1, NVIDIA_API_KEY)
for back-compat, but nothing here is NVIDIA-specific.

Default state of the whole feature is OFF: nothing happens unless you (a) run
THIS script AND (b) have the chosen key env var set (NVIDIA_API_KEY by default).
With no key it prints a notice and exits 0 — running it blind is harmless.

Usage:
    # NVIDIA default: key in NVIDIA_API_KEY, newest horoshop-export*.xlsx as corpus
    python scripts/ai_recheck_categories.py instance/add-novyy-proekt.xlsx
    python scripts/ai_recheck_categories.py add.xlsx --limit 20         # smoke run

    # any OpenAI-compatible provider (example values):
    python scripts/ai_recheck_categories.py add.xlsx \\
        --export "horoshop-export 26.05.26.xlsx" \\
        --base-url https://api.openai.com/v1 \\
        --api-key-env OPENAI_API_KEY \\
        --model gpt-4o-mini \\
        --out instance/ai-recheck.csv --throttle 1.6

Calls are throttled (~1.6s apart by default) to respect provider rate limits such
as NVIDIA's ~40 req/min free tier; tune with --throttle for your provider.
"""

import argparse
import csv
import os
import sys
import time
from pathlib import Path

import openpyxl

# Allow running as `python scripts/ai_recheck_categories.py` from anywhere.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.services.add_horoshop_file import (  # exact create-card headers, NOT retyped
    H_ARTICLE,
    H_BRAND,
    H_CATEGORY,
    H_NAME_RU,
    H_NAME_UA,
)
from app.services.category_export import read_category_corpus
from app.services.category_resolver import (
    DEFAULT_AI_MODEL,
    NVIDIA_BASE_URL,
    AICategoryResolver,
)

_REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_THROTTLE_S = 1.6  # ~37.5 req/min, under NVIDIA's ~40 rpm free cap
_REPORT_FIELDS = ["Артикул", "Название", "авто-Раздел", "ИИ-Раздел", "пометка"]
_NOTE_DISAGREE = "расхождение"
_NOTE_NO_OPINION = "нет уверенного варианта (ИИ вернул None)"


class _ShimSP:
    """Tiny duck-typed stand-in mirroring the SP attrs the resolver reads.

    AICategoryResolver pulls `.name`, `.brand`, `.description` via getattr (same
    names as the live SupplierProduct). The generated XLSX carries no per-row
    description, so it stays empty — name+brand drive the classification.
    """

    __slots__ = ("name", "brand", "description")

    def __init__(self, name: str, brand: str, description: str = ""):
        self.name = name
        self.brand = brand
        self.description = description


def _newest_export() -> Path | None:
    """Newest `horoshop-export *.xlsx` in the repo root (the app's corpus source)."""
    candidates = sorted(
        _REPO_ROOT.glob("horoshop-export*.xlsx"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return candidates[0] if candidates else None


def _parse_args(argv) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("xlsx", help="path to the generated create-card XLSX to re-check")
    p.add_argument(
        "--export",
        default=None,
        help="Horoshop export .xlsx for the allowed «Раздел» label set "
        "(default: newest horoshop-export*.xlsx in the repo root)",
    )
    p.add_argument(
        "--model",
        default=DEFAULT_AI_MODEL,
        help=f"model id, OpenAI-compatible (default {DEFAULT_AI_MODEL})",
    )
    p.add_argument(
        "--base-url",
        default=NVIDIA_BASE_URL,
        help=f"OpenAI-compatible API base URL (default {NVIDIA_BASE_URL})",
    )
    p.add_argument(
        "--api-key-env",
        default="NVIDIA_API_KEY",
        help="env var holding the provider API key (default NVIDIA_API_KEY)",
    )
    p.add_argument(
        "--limit", type=int, default=None, help="re-check only the first N rows (smoke run)"
    )
    p.add_argument("--out", default=None, help="report path (default: <input>.ai-recheck.csv)")
    p.add_argument(
        "--throttle",
        type=float,
        default=DEFAULT_THROTTLE_S,
        help=f"seconds between API calls (default {DEFAULT_THROTTLE_S}; NVIDIA ~40 rpm)",
    )
    return p.parse_args(argv)


def _find_col(header, label: str) -> int | None:
    """0-based index of the first header cell whose value == ``label`` (exact)."""
    for idx, cell in enumerate(header):
        if isinstance(cell, str) and cell.strip() == label:
            return idx
    return None


def _read_rows(xlsx_path: str) -> tuple[list[dict], list[str]]:
    """Read the create-card XLSX into row dicts {article,name,brand,auto_category}.

    Headers are located by the EXACT create-card constants imported from
    add_horoshop_file (the file was written with those strings). A missing
    «Артикул» or «Раздел» header aborts with an error rather than mis-reading.
    """
    wb = openpyxl.load_workbook(xlsx_path, read_only=True, data_only=True)
    ws = wb.active
    row_iter = ws.iter_rows(values_only=True)
    try:
        header = next(row_iter)
    except StopIteration:
        wb.close()
        return [], ["XLSX is empty (no header row)"]

    col_article = _find_col(header, H_ARTICLE)
    col_category = _find_col(header, H_CATEGORY)
    if col_article is None or col_category is None:
        wb.close()
        missing = [
            lbl
            for lbl, col in ((H_ARTICLE, col_article), (H_CATEGORY, col_category))
            if col is None
        ]
        return [], [f"XLSX missing required header(s): {', '.join(missing)}"]

    col_name_ua = _find_col(header, H_NAME_UA)
    col_name_ru = _find_col(header, H_NAME_RU)
    col_brand = _find_col(header, H_BRAND)

    def _cell(row, idx):
        if idx is None or len(row) <= idx:
            return ""
        return (str(row[idx]).strip() if row[idx] is not None else "")

    rows: list[dict] = []
    for row in row_iter:
        article = _cell(row, col_article)
        name_ua = _cell(row, col_name_ua)
        name_ru = _cell(row, col_name_ru)
        if not article and not name_ua and not name_ru:
            continue  # blank trailing row
        rows.append({
            "article": article,
            "name": name_ua or name_ru,
            "name_ru": name_ru,
            "brand": _cell(row, col_brand),
            "auto_category": _cell(row, col_category),
        })
    wb.close()
    return rows, []


def main(argv=None) -> int:
    args = _parse_args(argv if argv is not None else sys.argv[1:])

    # OPT-IN gate: with no key, do NOTHING (zero network) and exit cleanly.
    if not os.environ.get(args.api_key_env):
        print(
            f"AI-перепроверка категорий ВЫКЛЮЧЕНА: переменная окружения "
            f"{args.api_key_env} не задана.\n"
            "Это опциональная функция (по умолчанию OFF). Чтобы включить — "
            f"экспортируй ключ провайдера в {args.api_key_env}:\n"
            f"    setx {args.api_key_env} \"<api-key>\"   (Windows, новый терминал)\n"
            "Для не-NVIDIA провайдера укажи также --base-url и --model "
            "(и при необходимости --api-key-env).\n"
            "Сетевые запросы НЕ выполнялись. Файл не изменён."
        )
        return 0

    xlsx_path = args.xlsx
    if not Path(xlsx_path).is_file():
        print(f"ABORT: входной XLSX не найден: {xlsx_path}")
        return 2

    export_path = args.export or (str(_newest_export()) if _newest_export() else None)
    if not export_path or not Path(export_path).is_file():
        print(
            "ABORT: не найден Horoshop-экспорт для списка разделов. "
            "Укажи --export <horoshop-export ....xlsx>."
        )
        return 2

    # Allowed «Раздел» label set — the SAME loader the app uses (read-only file).
    corpus, corpus_errs = read_category_corpus(export_path)
    for e in corpus_errs:
        print(f"  export warning: {e}")
    store_cats = {r["category"] for r in corpus if r.get("category")}
    if not store_cats:
        print(f"ABORT: в экспорте {export_path} нет ни одного «Раздел».")
        return 2

    rows, read_errs = _read_rows(xlsx_path)
    for e in read_errs:
        print(f"  XLSX error: {e}")
    if read_errs:
        return 2
    if args.limit is not None:
        rows = rows[: args.limit]

    print(
        f"Экспорт: {export_path}\n"
        f"Разделов в каталоге: {len(store_cats)}\n"
        f"Провайдер: {args.base_url}  (ключ из ${args.api_key_env})\n"
        f"Строк к проверке: {len(rows)}  (модель: {args.model}, "
        f"пауза {args.throttle}s между запросами)\n"
    )

    resolver = AICategoryResolver(
        store_cats,
        enabled=True,
        model=args.model,
        base_url=args.base_url,
        api_key_env=args.api_key_env,
    )

    report_rows: list[dict] = []
    checked = 0
    errors = 0
    for i, r in enumerate(rows):
        shim = _ShimSP(name=r["name"], brand=r["brand"])
        try:
            res = resolver.resolve(shim, brand=r["brand"])
        except Exception as exc:  # noqa: BLE001 — surface, don't crash the whole run
            errors += 1
            print(f"  [{i+1}/{len(rows)}] ошибка API для {r['article']!r}: {exc}")
            if i < len(rows) - 1:
                time.sleep(args.throttle)
            continue
        checked += 1

        ai_label = res.category
        auto = r["auto_category"]
        if ai_label is None:
            note = _NOTE_NO_OPINION
        elif ai_label != auto:
            note = _NOTE_DISAGREE
        else:
            # Agreement → not a finding; the auto category stands. Skip.
            if i < len(rows) - 1:
                time.sleep(args.throttle)
            continue

        report_rows.append({
            "Артикул": r["article"],
            "Название": r["name"],
            "авто-Раздел": auto,
            "ИИ-Раздел": ai_label or "",
            "пометка": note,
        })

        if i < len(rows) - 1:
            time.sleep(args.throttle)  # NVIDIA ~40 rpm free cap

    # Report → CSV (utf-8-sig so Excel opens Cyrillic correctly).
    out_path = Path(args.out) if args.out else Path(xlsx_path).with_suffix(".ai-recheck.csv")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=_REPORT_FIELDS)
        w.writeheader()
        w.writerows(report_rows)

    disagreements = sum(1 for r in report_rows if r["пометка"] == _NOTE_DISAGREE)
    no_opinion = sum(1 for r in report_rows if r["пометка"] == _NOTE_NO_OPINION)
    summary = (
        f"\nПроверено строк: {checked}; расхождений: {disagreements}; "
        f"без уверенного варианта: {no_opinion}"
        + (f"; ошибок API: {errors}" if errors else "")
        + f"\nОтчёт: {out_path}\n"
        "ВАЖНО: это только аудит — автоматически выбранный «Раздел» НЕ менялся."
    )
    print(summary)
    return 0


if __name__ == "__main__":
    sys.exit(main())
