#!/usr/bin/env python
"""Confirm the 1:1-safe recommend-CONFIRM candidates from the 2026-06-05 triage.

Source: .planning/candidate-triage-2026-06-05.md  (## recommend-CONFIRM, 61 rows)
Companion read-only checks: scripts/triage_candidates_readonly.py (bucketing) and
scripts/triage_one_to_one_check.py (1:1 invariant). The latter found 15 of the 61
sit on a PP that already holds a confirmed/manual match (conflicts) -> 46 are safe.

This script does NOT trust that count blindly: it feeds ALL 61 ids through the app's
OWN invariant guard `_pp_already_claimed` (the exact function the UI confirm uses), so
the 15 conflicts are skipped live, plus any candidate-vs-candidate PP collision inside
the batch (first wins). It mirrors confirm_match() semantics:
    status='confirmed'; confirmed_at=utcnow; confirmed_by=<tag>; cleanup sibling candidates
DELIBERATE deviations from the HTTP endpoint (documented):
  - confirmed_by = "triage-batch-2026-06-05" (no current_user in a script)
  - no current_user.matches_processed bump (cosmetic per-user stat)
  - no log_action() audit row (needs request ctx); the commit + this console summary
    + the triage dossier are the audit trail.
It does NOT touch product names (that is confirm-update, a different endpoint).

SAFE BY DEFAULT: dry-run (rolls back). Pass --apply to commit.
Backup before --apply: instance/backups/labresta.db.bak-2026-06-05-confirm46

Run from repo root:
    .venv/Scripts/python.exe scripts/confirm_safe_candidates.py            # dry-run
    .venv/Scripts/python.exe scripts/confirm_safe_candidates.py --apply     # commit
"""
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / ".planning" / "candidate-triage-2026-06-05.md"
CONFIRMED_BY = "triage-batch-2026-06-05"


def confirm_ids_from_report(text):
    """match_ids under '## recommend-CONFIRM' up to the next '## ' header."""
    start = text.index("## recommend-CONFIRM")
    rest = text[start + len("## recommend-CONFIRM"):]
    end = rest.find("\n## ")
    section = rest if end == -1 else rest[:end]
    ids = []
    for line in section.splitlines():
        m = re.match(r"\s*\|\s*(\d+)\s*\|", line)
        if m:
            ids.append(int(m.group(1)))
    return ids


def main():
    apply = "--apply" in sys.argv[1:]

    sys.path.insert(0, str(ROOT))
    from app import create_app
    from app.extensions import db
    from app.models import ProductMatch
    from app.views.matches import _pp_already_claimed, _cleanup_other_candidates

    ids_arg = next((a for a in sys.argv[1:] if a.startswith("--ids=")), None)
    if ids_arg:
        ids = [int(x) for x in ids_arg.split("=", 1)[1].split(",") if x.strip()]
        source = f"--ids ({len(ids)})"
    else:
        ids = confirm_ids_from_report(REPORT.read_text(encoding="utf-8"))
        source = "report recommend-CONFIRM"

    app = create_app()
    with app.app_context():
        def counts():
            from sqlalchemy import func
            rows = db.session.query(ProductMatch.status, func.count()).group_by(
                ProductMatch.status).all()
            return {s: c for s, c in rows}

        before = counts()
        now = datetime.now(timezone.utc)

        confirmed, skipped_claimed, skipped_intrabatch, missing, not_candidate = [], [], [], [], []
        claimed_in_batch = {}  # pp_id -> match_id that claimed it in THIS batch

        for mid in ids:
            m = db.session.get(ProductMatch, mid)
            if m is None:
                missing.append(mid)
                continue
            if m.status != "candidate":
                not_candidate.append((mid, m.status))
                continue
            existing = _pp_already_claimed(m.prom_product_id, exclude_match_id=m.id)
            if existing:
                skipped_claimed.append((mid, m.prom_product_id, existing.id, existing.status))
                continue
            if m.prom_product_id in claimed_in_batch:
                skipped_intrabatch.append((mid, m.prom_product_id, claimed_in_batch[m.prom_product_id]))
                continue
            m.status = "confirmed"
            m.confirmed_at = now
            m.confirmed_by = CONFIRMED_BY
            cleaned = _cleanup_other_candidates(m.supplier_product_id, m.id)
            claimed_in_batch[m.prom_product_id] = m.id
            confirmed.append((mid, m.supplier_product_id, m.prom_product_id, cleaned))

        siblings_deleted = sum(c for *_, c in confirmed)

        print(f"=== confirm_safe_candidates  ({'APPLY' if apply else 'DRY-RUN'}) ===")
        print(f"report recommend-CONFIRM ids : {len(ids)}")
        print(f"status BEFORE                : {before}")
        print()
        print(f"WILL CONFIRM                 : {len(confirmed)}")
        print(f"skipped (PP already claimed) : {len(skipped_claimed)}")
        print(f"skipped (intra-batch PP dup) : {len(skipped_intrabatch)}")
        print(f"skipped (status != candidate): {len(not_candidate)}")
        print(f"missing (id not found)       : {len(missing)}")
        print(f"sibling candidates to delete : {siblings_deleted}")
        print()
        print("confirm ids: " + ", ".join(str(m) for m, *_ in confirmed))
        print()
        print("skipped-claimed (mid -> PP -> held by):")
        for mid, pp, hid, hst in skipped_claimed:
            print(f"  m{mid}  PP{pp}  held=m{hid}:{hst}")
        if skipped_intrabatch:
            print("skipped intra-batch dup:")
            for mid, pp, keeper in skipped_intrabatch:
                print(f"  m{mid}  PP{pp}  taken-in-batch-by m{keeper}")
        if not_candidate:
            print("not-candidate (already processed):")
            for mid, st in not_candidate:
                print(f"  m{mid}  status={st}")
        if missing:
            print("missing ids: " + ", ".join(str(m) for m in missing))

        if apply:
            db.session.commit()
            print("\n>>> COMMITTED. status AFTER:", counts())
        else:
            db.session.rollback()
            print("\n>>> DRY-RUN: rolled back, no changes written.")


if __name__ == "__main__":
    main()
