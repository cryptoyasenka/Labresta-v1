"""Tests for scripts/export_yml_subset.py — safe-mode YML subset exporter."""

import sys
from pathlib import Path

import pytest
from lxml import etree

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.export_yml_subset import export_subset, main  # noqa: E402


def _write_fixture_yml(path: Path, offers: list[dict]) -> None:
    root = etree.Element("yml_catalog", date="2026-04-15 12:00")
    shop = etree.SubElement(root, "shop")
    etree.SubElement(shop, "name").text = "LabResta"
    currencies = etree.SubElement(shop, "currencies")
    etree.SubElement(currencies, "currency", id="EUR", rate="1")
    offers_el = etree.SubElement(shop, "offers")
    for o in offers:
        offer = etree.SubElement(
            offers_el, "offer",
            id=o["id"],
            available=o.get("available", "true"),
        )
        etree.SubElement(offer, "name").text = o.get("name", o["id"])
        etree.SubElement(offer, "price").text = o.get("price", "10.0")
        etree.SubElement(offer, "currencyId").text = "EUR"
        etree.SubElement(offer, "vendorCode").text = o.get("vendor", o["id"])

    tree = etree.ElementTree(root)
    tree.write(
        str(path),
        xml_declaration=True,
        encoding="UTF-8",
        pretty_print=True,
        doctype='<!DOCTYPE yml_catalog SYSTEM "shops.dtd">',
    )


@pytest.fixture
def source_yml(tmp_path: Path) -> Path:
    path = tmp_path / "feed.yml"
    _write_fixture_yml(path, [
        {"id": "A1", "available": "true"},
        {"id": "A2", "available": "true"},
        {"id": "A3", "available": "false"},
        {"id": "A4", "available": "true"},
        {"id": "A5", "available": "true"},
    ])
    return path


def _parse_offer_ids(path: Path) -> list[str]:
    tree = etree.parse(str(path))
    return [o.get("id") for o in tree.getroot().iter("offer")]


def test_limit_keeps_first_n_offers(source_yml, tmp_path):
    out = tmp_path / "subset.yml"
    stats = export_subset(source_yml, out, wanted=None, limit=3, available_only=False)

    assert stats["kept_offers"] == 3
    assert stats["total_offers"] == 5
    assert _parse_offer_ids(out) == ["A1", "A2", "A3"]


def test_limit_with_available_only_skips_unavailable(source_yml, tmp_path):
    out = tmp_path / "subset.yml"
    stats = export_subset(source_yml, out, wanted=None, limit=3, available_only=True)

    assert stats["kept_offers"] == 3
    # A3 is unavailable so should be skipped
    assert _parse_offer_ids(out) == ["A1", "A2", "A4"]


def test_artikul_filter_picks_matching_offers(source_yml, tmp_path):
    out = tmp_path / "subset.yml"
    stats = export_subset(
        source_yml, out, wanted={"A2", "A5"}, limit=None, available_only=False,
    )

    assert stats["kept_offers"] == 2
    assert set(_parse_offer_ids(out)) == {"A2", "A5"}


def test_artikul_filter_matches_vendor_code(tmp_path):
    source = tmp_path / "feed.yml"
    _write_fixture_yml(source, [
        {"id": "X1", "vendor": "ART-100"},
        {"id": "X2", "vendor": "ART-200"},
    ])
    out = tmp_path / "subset.yml"
    stats = export_subset(source, out, wanted={"ART-200"}, limit=None, available_only=False)

    assert stats["kept_offers"] == 1
    assert _parse_offer_ids(out) == ["X2"]


def test_output_preserves_shop_header_and_dtd(source_yml, tmp_path):
    out = tmp_path / "subset.yml"
    export_subset(source_yml, out, wanted={"A1"}, limit=None, available_only=False)

    text = out.read_text(encoding="utf-8")
    assert "<!DOCTYPE yml_catalog SYSTEM" in text
    assert "<name>LabResta</name>" in text
    assert "<currency" in text


def test_missing_source_exits_with_code_2(tmp_path):
    with pytest.raises(SystemExit) as exc:
        export_subset(
            tmp_path / "missing.yml",
            tmp_path / "out.yml",
            wanted=None,
            limit=1,
            available_only=False,
        )
    assert exc.value.code == 2


def test_cli_limit_end_to_end(source_yml, tmp_path, capsys):
    out = tmp_path / "subset.yml"
    rc = main([
        "--input", str(source_yml),
        "--output", str(out),
        "--limit", "2",
    ])
    assert rc == 0
    captured = capsys.readouterr()
    assert "2 из 5" in captured.out
    assert _parse_offer_ids(out) == ["A1", "A2"]


def test_cli_warns_about_missing_artikul(source_yml, tmp_path, capsys):
    out = tmp_path / "subset.yml"
    rc = main([
        "--input", str(source_yml),
        "--output", str(out),
        "--artikuls", "A1,NOPE",
    ])
    assert rc == 0
    captured = capsys.readouterr()
    # One matched (A1), one did not (NOPE) — expect the warning on stderr
    assert "не найдены" in captured.err
    assert "NOPE" in captured.err
