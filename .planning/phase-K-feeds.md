# Phase K — Per-supplier & custom feeds

Decisions locked 2026-04-16 with Yana.

## Goal
Move from one monolithic `labresta-feed.yml` to stable per-supplier URLs + ad-hoc custom selections, so Horoshop can import any subset independently.

## Scope of each generated YML (MVP)
- `<offer>` contains: `id`, `available`, `vendorCode`, `price`, `currencyId`
- **No** description / images in MVP. Backlog: add behind a `include_rich=True` flag when Yana asks.

## Stable URLs
| Route | File | Who regenerates |
|---|---|---|
| `/feed/yml` | `labresta-feed.yml` | «Обновить всех» on `/suppliers` header |
| `/feed/yml/supplier/<slug>` | `labresta-feed-<slug>.yml` | per-supplier buttons on `/suppliers/<id>` |
| `/feed/yml/custom/<token>` | `labresta-feed-custom-<token>.yml` | «Собрать фид из выбранного» on `/matches` |

- Slug = transliterated lowercase supplier name (MARESTO → `maresto`, Кодаки → `kodaki`). Stored on `Supplier.slug UNIQUE`.
- Custom token = first 12 hex of sha256(sorted match_ids). Deterministic: same selection → same token → same URL.
- Custom files **live forever** until Yana clicks «Удалить» on a token list page (`/feeds/custom`).

## Two actions per scope
- **«Обновить из источника»** — fetch → parse → save DB → regenerate YML. Long (1-2 min per supplier). Available on `/suppliers/<id>` and `/suppliers` header («Обновить всех из источников»).
- **«Только пересобрать YML»** — regenerate from current DB without fetch. Fast. Available on all three scopes.

## Narrow price/availability feeds (phase D, existing)
- **UI buttons on `/matches` get removed** — they duplicate per-supplier YML.
- Code in `yml_generator.sync_prices` / `sync_availability` stays for CLI access. Files `labresta-prices.yml` / `labresta-availability.yml` continue to be written when those functions are called.

## Implementation plan

### K.1 Schema
- `Supplier.slug VARCHAR(50) UNIQUE NOT NULL` — migration `migrate_add_supplier_slug.py`, autogen slugs for existing rows (MARESTO → maresto).

### K.2 Generator refactor
- Extract `_build_offer_xml(match, include_rich=False)` helper.
- Generalize `regenerate_yml_feed(supplier_ids=None, match_ids=None, filename=None)` — filters the query, writes to arbitrary filename.
- Thin wrappers:
  - `regenerate_all_feed()` → all, `labresta-feed.yml`
  - `regenerate_supplier_feed(supplier_id)` → `labresta-feed-<slug>.yml`
  - `regenerate_custom_feed(match_ids)` → `labresta-feed-custom-<token>.yml`, returns token
- **`in_feed` flag semantics:** currently regen sets in_feed=True for included matches and False for everyone else. With multi-file feeds this is ambiguous. Decision: `in_feed` reflects membership in the **main `/feed/yml`** (all-suppliers). Per-supplier and custom do not touch `in_feed`.

### K.3 Routes
- `app/views/feed.py` adds `/feed/yml/supplier/<slug>` and `/feed/yml/custom/<token>`.
- 404 if file not yet generated.

### K.4 UI
- **`/suppliers/<id>` detail page:** two buttons «Обновить из источника» / «Только пересобрать YML», plus a copy-to-clipboard URL field for `/feed/yml/supplier/<slug>`.
- **`/suppliers` header:** «Обновить всех из источников» and «Пересобрать общий YML».
- **`/matches`:** row checkboxes + sticky toolbar «Собрать фид из выбранного (N)» → modal with custom URL + copy button. Remove the existing «Обновить цены» / «Обновить наличие» buttons.
- **New page `/feeds/custom`:** list of all custom tokens with date, match_ids preview, URL, delete button.

### K.5 Tests
- Regen supplier=1 doesn't touch supplier=2 offers in output.
- Custom token deterministic for same match_ids set regardless of order.
- Custom file survives other regenerations (isolation per filename).
- Narrow-feed buttons no longer present in `/matches` render.
- in_feed flag only updates on main feed regen.

### K.6 Docs
- CLAUDE.md invariant «feed routing»: add section describing the three scopes.
- README: update feed URL list.

## Blockers / dependencies
- None — phase is independent of Kodaki feed format. Can start immediately.
- Kodaki onboarding (feed_type column, per-supplier economics, currency guard) is a separate phase once Yana sends Kodaki feed specs.

## Open questions (resolved)
- ✅ Custom TTL = forever
- ✅ Narrow feeds: keep code, remove UI (ii)
- ✅ «Обновить всех» button on `/suppliers` header
- ✅ Two separate buttons (fetch+regen vs regen-only)
- ✅ MVP = price + avail only, rich feed (desc + images) deferred to backlog
