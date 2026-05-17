import os

from app import create_app

app = create_app()

if __name__ == "__main__":
    # Production serves `run:app` via gunicorn (see railway.toml / Procfile);
    # this block is the local dev entrypoint only. Debug stays off unless
    # explicitly opted in, so an accidental `python run.py` in a
    # prod-like environment never exposes the Werkzeug debugger / PIN.
    debug = os.environ.get("FLASK_DEBUG", "").lower() in ("1", "true", "yes")
    app.run(debug=debug)
