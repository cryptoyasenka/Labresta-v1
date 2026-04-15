# LabResta Sync

Automated price and availability sync from supplier feeds to the **Horoshop** storefront at [labresta.com.ua](https://labresta.com.ua/).

> **Status:** Active development · SQLite (WAL) · 269+ tests green
>
> **Live store warning:** price and feed actions touch the production catalogue. See [CLAUDE.md](CLAUDE.md) for the guardrails that must not be bypassed.

## What it does

- **Feed parsing** — reads supplier YML / Excel / Google Sheets with automatic encoding detection
- **Fuzzy product matching** — rapidfuzz WRatio + brand/type/voltage/containment/price gates
- **Rule matching** — deterministic rules applied before fuzzy (see `app/services/rule_matcher.py`)
- **Auto-discount** — per-supplier closure-price calculation capped at 19% with a UAH-margin floor
- **Narrow-feed sync** — generates `labresta-prices.yml` / `labresta-availability.yml` for Horoshop import
- **Rebind workflow** — swap the supplier side of a confirmed match without breaking the 1 pp ↔ 1 sp invariant
- **Web dashboard** — manage matches, run audits, trigger syncs, review action log

## Architecture

```
Supplier feeds (YML / Excel / GSheets)
        │
        ▼
  Feed parser (lxml + chardet + openpyxl)
        │
        ▼
  Rule matcher  ──►  Fuzzy matcher (rapidfuzz)
        │                 │
        │  gates: brand / type / price / voltage
        │         strict-model / containment / display_article
        ▼                 ▼
             SQLite WAL (SQLAlchemy)
                 │
                 ▼
  YML generator ──► Horoshop (ngrok/cloudflared tunnel)
                 │
                 ▼
  Flask dashboard (matches, audit, suppliers, action log)
```

## Stack

- **Python 3.11+** (uv / pyproject)
- **Flask 3.1** — web framework + dashboard
- **SQLAlchemy** + SQLite (WAL mode)
- **APScheduler** — scheduled sync jobs
- **rapidfuzz** — fuzzy string matching
- **lxml** — YML parsing/generation
- **openpyxl** — Excel feed support
- **Chart.js** — dashboard visuals

Schema migrations are plain Python scripts under `scripts/migrate_*.py` (no Alembic).

## Getting started

```bash
git clone https://github.com/cryptoyasenka/Labresta-v1
cd Labresta-v1
pip install uv
uv sync
cp .env.example .env
# fill in .env (see below)
python run.py                    # starts on :5000
# admin login: admin@labresta.ua / admin123
```

Run the test suite:

```bash
.venv/Scripts/python.exe -m pytest
```

## Environment variables

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Flask secret key for sessions |
| `DATABASE_URL` | SQLite path (default `sqlite:///instance/labresta.db`) |
| `TESTING` | Set to `1` only in tests — triggers safety guard refusing to bind to production DB |
| `FTP_HOST` / `FTP_USER` / `FTP_PASS` / `FTP_REMOTE_PATH` | Optional: FTP upload of generated YML |

## Matching rules & invariants

See **[CLAUDE.md](CLAUDE.md)** for the complete contract. Highlights you must not violate:

1. **1 pp ↔ 1 confirmed/manual match** — enforced by partial UNIQUE INDEX `uq_match_prom_confirmed`.
2. **Voltage variants are distinct SKUs** — `(220)` and `(380)` of the same model never match.
3. **100 % fuzzy score is not bulletproof** — only identical meaningful tokens (after brand strip) are safe to bulk-confirm.
4. **Cross-brand reject when supplier brand is empty** — no promoting "Слайсер" to anything.
5. **Live-store actions require explicit go-ahead** — auto-discount apply and Horoshop import are gated behind `force=1` / subset preview.

Matcher gates live in `app/services/matcher.py`; the bulk-confirm safety rule in `scripts/bulk_auto_confirm.py`; the TESTING safety guard in `app/__init__.py:20-31`.

## Load-bearing scripts

| Script | Purpose | Safety |
|--------|---------|--------|
| `scripts/audit_candidates.py` | Rerun matcher on `candidate` rows, find stale/missing | `--dry-run` default, `--apply` writes |
| `scripts/merge_duplicate_sp.py` | Merge duplicate SupplierProduct rows (migrate matches to canonical) | Writes — take a backup first |
| `scripts/collisions_report.py` | List pp rows with >1 active match (1pp↔1sp violations) | Read-only |
| `scripts/apply_auto_discount.py` | Fill `discount_percent` per formula | **Live catalogue** — `--dry-run` first |
| `scripts/export_yml_subset.py` | Filter a generated YML to 5-10 offers for safe-mode Horoshop import | Read-only |
| `scripts/bulk_auto_confirm.py` | Auto-confirm R1 (tokens-equal) / R2 (subset + tight price) | Writes — `--dry-run` first |
| `scripts/diagnose_sp_match.py` | Trace why a SupplierProduct has no candidate | Read-only |
| `scripts/backup_db.py` | SQLite online backup, keeps last 20 | Safe |
| `scripts/migrate_*.py` | One-shot schema migrations | Already applied on prod — do not rerun |

## License

MIT
