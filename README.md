# Labresta

Automated price and availability sync from supplier XML feeds to [prom.ua](https://prom.ua/) marketplace.

> **Status:** Active development (v0.1.0)

## What it does

Labresta connects supplier data feeds with your marketplace storefront:

- **XML feed parsing** — reads supplier price lists with automatic encoding detection
- **Fuzzy product matching** — matches supplier items to your catalog using rapidfuzz
- **Price & stock sync** — keeps pricing and availability up to date automatically
- **Scheduled updates** — runs sync jobs on a configurable schedule
- **FTP upload** — pushes updated YML feed to your storefront hosting
- **Web dashboard** — manage sync rules, monitor status, review logs

## Architecture

```
Supplier XML feeds
        │
        ▼
  Feed parser (lxml + chardet)
        │
        ▼
  Fuzzy matching engine (rapidfuzz)
        │
        ▼
  PostgreSQL / SQLite (SQLAlchemy + Alembic)
        │
        ▼
  YML feed generator ──► FTP upload to prom.ua
        │
        ▼
  Flask web dashboard (monitoring + config)
```

## Stack

- **Python 3.11+** — core runtime
- **Flask** — web framework + dashboard
- **SQLAlchemy + Alembic** — ORM and database migrations
- **lxml** — XML feed parsing
- **rapidfuzz** — fuzzy string matching for product mapping
- **APScheduler** — scheduled sync jobs
- **openpyxl** — Excel import/export support

## Getting started

```bash
git clone https://github.com/cryptoyasenka/Labresta-v1
cd Labresta-v1
pip install uv
uv sync
cp .env.example .env
# fill in .env (see below)
python run.py
```

## Environment variables

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Flask secret key for sessions |
| `FTP_HOST` | FTP server for feed upload |
| `FTP_USER` | FTP username |
| `FTP_PASS` | FTP password |
| `FTP_REMOTE_PATH` | Remote path for YML feed (e.g. `/public_html/feed.yml`) |

## License

MIT
