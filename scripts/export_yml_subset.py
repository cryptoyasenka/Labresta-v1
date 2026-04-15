"""Export a small subset of the main YML feed for safe-mode Horoshop import testing.

Reads the generated feed (default: instance/feeds/labresta-feed.yml), picks
offers by artikul (--artikuls / --artikuls-file) or by first-N (--limit),
writes a new YML file with the same shop header and only the chosen offers.

Typical use: pick 5–10 items, serve the subset via ngrok, run Horoshop's
import pointed at the subset URL, verify that one product updates correctly,
then switch Horoshop to the full feed URL.

Examples:
    python scripts/export_yml_subset.py --limit 5
    python scripts/export_yml_subset.py --artikuls 10303502T,101200
    python scripts/export_yml_subset.py --artikuls-file test_items.txt \
        --output instance/feeds/labresta-feed-subset.yml
    python scripts/export_yml_subset.py --limit 10 --available-only
"""

import argparse
import sys
from pathlib import Path

from lxml import etree

DEFAULT_INPUT = Path(__file__).resolve().parent.parent / "instance" / "feeds" / "labresta-feed.yml"


def _load_artikuls(args: argparse.Namespace) -> set[str] | None:
    if args.artikuls:
        return {a.strip() for a in args.artikuls.split(",") if a.strip()}
    if args.artikuls_file:
        path = Path(args.artikuls_file)
        if not path.is_file():
            print(f"Ошибка: файл {path} не найден.", file=sys.stderr)
            sys.exit(2)
        return {
            line.strip()
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        }
    return None


def _offer_matches(offer: etree._Element, wanted: set[str] | None, available_only: bool) -> bool:
    if available_only and offer.get("available", "").lower() != "true":
        return False
    if wanted is None:
        return True
    offer_id = offer.get("id", "")
    vendor_el = offer.find("vendorCode")
    vendor_code = vendor_el.text if vendor_el is not None and vendor_el.text else ""
    return offer_id in wanted or vendor_code in wanted


def export_subset(
    input_path: Path,
    output_path: Path,
    wanted: set[str] | None,
    limit: int | None,
    available_only: bool,
) -> dict:
    if not input_path.is_file():
        print(f"Ошибка: исходный YML не найден: {input_path}", file=sys.stderr)
        print("Сначала сгенерируйте фид: POST /suppliers/<id>/regenerate-feed или UI-кнопка.", file=sys.stderr)
        sys.exit(2)

    parser = etree.XMLParser(strip_cdata=False, remove_blank_text=True)
    tree = etree.parse(str(input_path), parser)
    root = tree.getroot()

    shop = root.find("shop")
    if shop is None:
        print("Ошибка: в исходном YML нет <shop> — файл повреждён?", file=sys.stderr)
        sys.exit(2)

    offers_el = shop.find("offers")
    if offers_el is None:
        print("Ошибка: в <shop> нет <offers>.", file=sys.stderr)
        sys.exit(2)

    all_offers = list(offers_el)
    kept: list[etree._Element] = []
    for offer in all_offers:
        if _offer_matches(offer, wanted, available_only):
            kept.append(offer)
            if limit is not None and len(kept) >= limit:
                break

    # Rebuild offers element with just the kept offers.
    for child in list(offers_el):
        offers_el.remove(child)
    for offer in kept:
        offers_el.append(offer)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    tree.write(
        str(output_path),
        xml_declaration=True,
        encoding="UTF-8",
        pretty_print=True,
        doctype='<!DOCTYPE yml_catalog SYSTEM "shops.dtd">',
    )

    return {
        "input": str(input_path),
        "output": str(output_path),
        "total_offers": len(all_offers),
        "kept_offers": len(kept),
    }


def _build_arg_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", type=Path, default=DEFAULT_INPUT,
                    help=f"path to source YML (default: {DEFAULT_INPUT})")
    ap.add_argument("--output", type=Path, default=None,
                    help="path to subset YML (default: <input>-subset.yml alongside input)")
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--artikuls", help="comma-separated list of external_id / vendorCode to keep")
    group.add_argument("--artikuls-file", help="file with one artikul per line")
    group.add_argument("--limit", type=int, help="take first N offers (after --available-only filter)")
    ap.add_argument("--available-only", action="store_true",
                    help="skip offers with available=\"false\"")
    return ap


def main(argv: list[str] | None = None) -> int:
    ap = _build_arg_parser()
    args = ap.parse_args(argv)

    wanted = _load_artikuls(args)
    if wanted is not None and not wanted:
        print("Ошибка: список артикулов пуст.", file=sys.stderr)
        return 2

    input_path = args.input
    if args.output is None:
        output_path = input_path.with_name(input_path.stem + "-subset.yml")
    else:
        output_path = args.output

    stats = export_subset(
        input_path=input_path,
        output_path=output_path,
        wanted=wanted,
        limit=args.limit,
        available_only=args.available_only,
    )

    print(f"Готово: {stats['kept_offers']} из {stats['total_offers']} offer(s) -> {stats['output']}")
    if wanted is not None:
        missing = wanted - {
            offer.get("id", "") for offer in etree.parse(stats["output"]).getroot().iter("offer")
        } - {
            (offer.find("vendorCode").text if offer.find("vendorCode") is not None else "")
            for offer in etree.parse(stats["output"]).getroot().iter("offer")
        }
        missing.discard("")
        if missing:
            print(f"Внимание: не найдены в фиде артикулы: {sorted(missing)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
