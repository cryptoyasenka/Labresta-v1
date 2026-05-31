"""The audit script's OPTIONAL --mapping flag must be opt-in only.

Phase 9 "Option B" is a DRAFT what-if: `scripts/audit_category_analogy.py`
gained a `--mapping <path.json>` flag that rewrites a feed category to a store
label BEFORE reconcile (so a mapped label exact-matches the store set at
confidence 100). The shipped default (Option A) must stay byte-for-byte: with no
mapping the override layer is a no-op. These tests pin that contract at the unit
level (no DB / no app context) so the default path can never silently change.
"""

from __future__ import annotations

import json

from scripts.audit_category_analogy import _load_mapping


def test_load_mapping_none_is_empty():
    """No --mapping → empty dict → the getter applies zero overrides (baseline)."""
    assert _load_mapping(None) == {}
    assert _load_mapping("") == {}


def test_load_mapping_drops_nulls_and_meta_keys(tmp_path):
    """null = genuine gap (no override → fuzzy reconcile runs); `_`-keys are docs."""
    p = tmp_path / "m.json"
    p.write_text(
        json.dumps(
            {
                "_README": "ignore me",
                "Feed/Real": "Store/Real",
                "Feed/Gap": None,
                "Feed/Blank": "   ",
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    m = _load_mapping(str(p))
    assert m == {"Feed/Real": "Store/Real"}
    assert "Feed/Gap" not in m  # null never overrides
    assert "_README" not in m  # meta key never overrides


def test_mapping_override_semantics_match_getter(tmp_path):
    """The rewrite the getter performs: mapped→store label, else raw passthrough.

    Mirrors `mapping.get(raw.strip(), raw)` so a mapped label is rewritten (and
    will exact-match the store set at conf 100) while an unmapped/null label is
    returned verbatim (unchanged fuzzy reconcile path)."""
    p = tmp_path / "m.json"
    p.write_text(
        json.dumps({"Feed/Mapped": "Store/Mapped", "Feed/Gap": None}, ensure_ascii=False),
        encoding="utf-8",
    )
    mapping = _load_mapping(str(p))

    def rewrite(raw):  # identical expression to the script's _feed_getter
        return mapping.get(raw.strip(), raw)

    assert rewrite("Feed/Mapped") == "Store/Mapped"  # mapped → store label
    assert rewrite("Feed/Gap") == "Feed/Gap"  # null entry → passthrough (no override)
    assert rewrite("Feed/Unknown") == "Feed/Unknown"  # unmapped → passthrough

    # With NO mapping the same expression is the identity (baseline path).
    empty = _load_mapping(None)
    assert empty.get("Feed/Mapped", "Feed/Mapped") == "Feed/Mapped"
