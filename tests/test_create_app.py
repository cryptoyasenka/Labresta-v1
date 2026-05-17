"""Guard the production app factory.

The rest of the suite builds its own ``Flask(...)`` instance in
``conftest.py`` and never calls :func:`app.create_app`. That left the
factory — the exact entrypoint gunicorn (``gunicorn run:app``) and every
startCommand migration script use in production — completely untested. A
refactor that rebound the local name ``app`` to the ``app`` package module
inside ``create_app`` shipped green (683 passed) yet broke every prod
deploy with ``AttributeError: module 'app' has no attribute 'app_context'``.

This module exercises ``create_app()`` directly so that class of
regression fails here instead of in a Railway healthcheck.

``create_app()`` is called exactly once: it starts the APScheduler as a
process-global side effect, so a second call in the same process raises
SchedulerAlreadyRunningError (an unrelated factory limitation). One call
is enough — before the fix it raised AttributeError before returning.
"""

import flask


def test_create_app_returns_usable_flask_instance():
    """The factory must return the Flask instance with a working context.

    Before the fix, ``import app.models`` inside ``create_app`` rebound the
    local name ``app`` to the package module, so ``create_app()`` raised
    ``AttributeError: module 'app' has no attribute 'app_context'`` at
    ``with app.app_context():`` — never reaching this assertion.
    """
    from app import create_app

    application = create_app()

    assert isinstance(application, flask.Flask), (
        f"create_app() returned {type(application)!r}; the local `app` name "
        "was likely shadowed (e.g. by a bare `import app.models`)."
    )

    with application.app_context():
        assert flask.current_app is not None
