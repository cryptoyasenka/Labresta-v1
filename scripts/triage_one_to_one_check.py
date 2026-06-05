#!/usr/bin/env python
"""Read-only one-to-one cross-check for candidate triage (#12).

Complements .planning/candidate-triage-2026-06-05.md. The triage buckets each
candidate on the PromProduct<->SupplierProduct TEXT axis alone (article, name,
brand, score). This script adds the INVARIANT layer
(CLAUDE.md #15 / feedback_labresta_one_to_one): a candidate whose PromProduct
ALREADY holds a confirmed/manual match must NOT be confirmed, because a PP may
hold at most one supplier (1 pp <-> 1 supplier). Such a "recommend-CONFIRM" row
is therefore a CONFLICT, not safe-to-confirm, regardless of text score.

READ-ONLY: opens the DB with mode=ro and only SELECTs. Asserts the match-status
snapshot is identical before and after (zero mutation).

Run from repo root:  .venv/Scripts/python.exe scripts/triage_one_to_one_check.py
"""
import re
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "instance" / "labresta.db"
REPORT = ROOT / ".planning" / "candidate-triage-2026-06-05.md"


def status_counts(cur):
    cur.execute("SELECT status, COUNT(*) FROM product_matches GROUP BY status")
    return dict(cur.fetchall())


def confirm_ids_from_report(text):
    """match_ids listed under '## recommend-CONFIRM' up to the next '## ' header."""
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
    con = sqlite3.connect(f"file:{DB.as_posix()}?mode=ro", uri=True)
    cur = con.cursor()

    before = status_counts(cur)

    cur.execute("SELECT COUNT(*) FROM product_matches WHERE status='candidate'")
    total_cand = cur.fetchone()[0]

    # (a) ALL candidates sitting on an already-matched PP
    cur.execute(
        """
        SELECT COUNT(*) FROM product_matches x
        WHERE x.status='candidate'
          AND EXISTS (SELECT 1 FROM product_matches o
                      WHERE o.prom_product_id = x.prom_product_id
                        AND o.status IN ('confirmed','manual'))
        """
    )
    cand_on_matched_pp = cur.fetchone()[0]

    # (b) recommend-CONFIRM rows that are one-to-one conflicts
    report = REPORT.read_text(encoding="utf-8")
    confirm_ids = confirm_ids_from_report(report)
    conflicts = []
    for mid in confirm_ids:
        cur.execute("SELECT prom_product_id, status FROM product_matches WHERE id=?", (mid,))
        row = cur.fetchone()
        if not row:
            continue
        pp, _st = row
        cur.execute(
            """SELECT id, status FROM product_matches
               WHERE prom_product_id=? AND status IN ('confirmed','manual')
               ORDER BY id""",
            (pp,),
        )
        held = cur.fetchall()
        if held:
            conflicts.append((mid, pp, held))

    after = status_counts(cur)
    con.close()

    print("=== DB status snapshot (product_matches) ===")
    print("BEFORE:", before)
    print("AFTER :", after)
    print("identical:", before == after)
    print()
    print("=== one-to-one cross-check ===")
    print(f"candidates total                 : {total_cand}")
    print(f"candidates on already-matched PP : {cand_on_matched_pp}/{total_cand}")
    print(f"recommend-CONFIRM parsed         : {len(confirm_ids)}")
    print(f"  of which one-to-one conflicts  : {len(conflicts)}")
    print(f"  SAFE to confirm (no conflict)  : {len(confirm_ids) - len(conflicts)}")
    print()
    print("conflict match_ids (CONFIRM bucket): " + ", ".join(str(m) for m, _, _ in conflicts))
    print()
    print("detail (match_id -> PP -> already-held match(es)):")
    for mid, pp, held in conflicts:
        held_s = ", ".join(f"{hid}:{hst}" for hid, hst in held)
        print(f"  m{mid}  PP{pp}  held=[{held_s}]")


if __name__ == "__main__":
    main()
