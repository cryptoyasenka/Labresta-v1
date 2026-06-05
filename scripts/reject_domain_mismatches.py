#!/usr/bin/env python
"""Reject the 28 domain-mismatch candidates surfaced by the 2026-06-05/06 NEEDS-EYEBALL triage.

These are matches the auto-matcher fired on article-NUMBER equality (or a shared SP
fanned across siblings) where the product NAMES describe genuinely different items —
or a near-miss SKU suffix/model variant whose correct sibling was already confirmed.
They are NOT #15 (PP-already-held) conflicts (those are Yana's keep-vs-switch policy
and are left untouched) and NOT ambiguous rows. Sources (per-row evidence):
    .planning/astim-eyeball-2026-06-05.md        (## REJECT - domain mismatch, 9)
    .planning/guder-eyeball-2026-06-05.md         (### REJECT -> Domain mismatch, 5)
    .planning/rp-ukrayina-eyeball-2026-06-05.md   (REJECT -> by domain mismatch, 3)
    .planning/kodaki-eyeball-2026-06-05.md         (REJECT -> domain, 11)

Mirrors the app's reject_match()/bulk reject semantics (matches.py:682, :1212):
    status='rejected'; confirmed_at=utcnow; confirmed_by=<tag>
The status='rejected' (not delete) is the load-bearing part: it lands the (sp,pp) pair
in rejected_pairs so the next full sync will NOT resurrect the candidate
(matcher.py "user-rejected candidates are never recreated").

DELIBERATE deviations from the HTTP endpoint (documented):
  - confirmed_by = "triage-reject-2026-06-06" (no current_user in a script)
  - NO find_match_for_product re-match step. The endpoint re-matches the SP after a
    reject to suggest the next candidate; this is a bulk CLEANUP of known-wrong matches,
    and re-matching would re-create candidate noise on exactly the odd/fanned SPs we are
    clearing (spatula SP8376->3 PPs, opener SP7700->3 PPs, VENETO SP7086->3 PPs). The
    resurrection guard is preserved regardless. Orphaned SPs can be re-matched later by
    a normal matcher run if Yana wants them paired.
  - no current_user.matches_processed bump; no log_action() audit row (needs request ctx)
    — the commit + this console summary + the four eyeball dossiers are the audit trail.
Rejecting a candidate releases nothing (only confirmed/manual hold the 1:1 claim), so this
cannot create a #15 violation.

SAFE BY DEFAULT: dry-run (rolls back). Pass --apply to commit. Aborts on a prod DB URL.
Run from repo root:
    .venv/Scripts/python.exe scripts/reject_domain_mismatches.py            # dry-run
    .venv/Scripts/python.exe scripts/reject_domain_mismatches.py --apply     # commit
"""
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REJECTED_BY = "triage-reject-2026-06-06"

# 28 domain-mismatch match_ids, grouped by source dossier (provenance = audit trail).
DOMAIN_REJECT = {
    "astim": [4436, 4437, 4438, 4439, 4440, 4441, 4442, 4443, 4445],          # 9
    "guder": [3805, 3806, 3831, 4382, 4383],                                   # 5
    "rp-ukrayina": [3725, 3732, 3733],                                         # 3
    "kodaki": [3592, 3594, 3596, 3608, 3639, 3678, 3683, 3685, 3687, 3689, 3690],  # 11
}


def main():
    apply = "--apply" in sys.argv[1:]
    allow_prod = "--allow-prod" in sys.argv[1:]

    ids_arg = next((a for a in sys.argv[1:] if a.startswith("--ids=")), None)
    if ids_arg:
        ids = [int(x) for x in ids_arg.split("=", 1)[1].split(",") if x.strip()]
        source = f"--ids ({len(ids)})"
    else:
        ids = [mid for group in DOMAIN_REJECT.values() for mid in group]
        source = "built-in domain-mismatch list"

    sys.path.insert(0, str(ROOT))
    from app import create_app
    from app.extensions import db
    from app.models import ProductMatch
    from sqlalchemy import func

    app = create_app()
    db_url = app.config.get("SQLALCHEMY_DATABASE_URI", "")
    print(f"DB: {db_url}")
    if ("rlwy.net" in db_url or "railway.app" in db_url) and not allow_prod:
        print(">>> ABORT: looks like a PROD DB. Pass --allow-prod only if you really mean it.")
        sys.exit(1)

    with app.app_context():
        def counts():
            rows = db.session.query(ProductMatch.status, func.count()).group_by(
                ProductMatch.status).all()
            return {s: c for s, c in rows}

        before = counts()
        now = datetime.now(timezone.utc)

        rejected, not_candidate, missing = [], [], []
        for mid in ids:
            m = db.session.get(ProductMatch, mid)
            if m is None:
                missing.append(mid)
                continue
            if m.status != "candidate":
                not_candidate.append((mid, m.status))
                continue
            m.status = "rejected"
            m.confirmed_at = now
            m.confirmed_by = REJECTED_BY
            rejected.append((mid, m.supplier_product_id, m.prom_product_id))

        print(f"=== reject_domain_mismatches  ({'APPLY' if apply else 'DRY-RUN'}) ===")
        print(f"source                       : {source}")
        print(f"ids in                       : {len(ids)}")
        print(f"status BEFORE                : {before}")
        print()
        print(f"WILL REJECT                  : {len(rejected)}")
        print(f"skipped (status != candidate): {len(not_candidate)}")
        print(f"missing (id not found)       : {len(missing)}")
        print()
        print("reject ids: " + ", ".join(str(m) for m, *_ in rejected))
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
