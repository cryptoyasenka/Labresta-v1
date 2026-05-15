# Railway deploys via railway.toml [deploy] startCommand, which also runs
# the DB migrations and startup tasks before launching gunicorn. This
# Procfile is the fallback for Procfile-based runners (foreman/honcho/
# Heroku-style) and is kept in sync with the railway.toml gunicorn args.
#
# Single worker + threads (not multiple workers) is deliberate: the app
# uses SQLite in WAL mode, so one writer process avoids "database is
# locked" under write contention while threads provide request concurrency.
web: gunicorn run:app --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 120
