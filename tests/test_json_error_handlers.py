"""Verify AJAX error responses are JSON, not HTML.

Regression for: "Unexpected token '<', \"<!doctype \"... is not valid JSON"
when reject/confirm POST hits a 400/404/500 HTML error page.
"""
import pytest
from flask import Flask, jsonify
from flask_wtf.csrf import CSRFError


@pytest.fixture
def mini_app():
    """Minimal Flask app with the same error handlers as create_app()."""
    from app import _wants_json_response

    app = Flask(__name__)
    app.config.update(SECRET_KEY="test", TESTING=True, WTF_CSRF_TIME_LIMIT=None)

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        if _wants_json_response():
            return jsonify({
                "status": "error",
                "code": "csrf_invalid",
                "message": "Сессия устарела, обновите страницу (Ctrl+F5).",
            }), 400
        return e.description, 400

    @app.errorhandler(404)
    def handle_not_found(e):
        if _wants_json_response():
            return jsonify({"status": "error", "code": "not_found"}), 404
        return "<html>not found</html>", 404

    @app.errorhandler(500)
    def handle_server_error(e):
        if _wants_json_response():
            return jsonify({"status": "error", "code": "server_error"}), 500
        return "<html>oops</html>", 500

    @app.route("/raise-csrf", methods=["POST"])
    def raise_csrf():
        raise CSRFError("csrf failed")

    @app.route("/raise-500", methods=["POST"])
    def raise_500():
        raise RuntimeError("boom")

    return app


class TestJsonErrorHandlers:
    def test_csrf_error_returns_json_when_xhr(self, mini_app):
        client = mini_app.test_client()
        resp = client.post("/raise-csrf", headers={"X-CSRFToken": "anything"})
        assert resp.status_code == 400
        assert resp.is_json
        body = resp.get_json()
        assert body["status"] == "error"
        assert body["code"] == "csrf_invalid"

    def test_csrf_error_returns_html_when_browser_form(self, mini_app):
        client = mini_app.test_client()
        resp = client.post("/raise-csrf", headers={"Accept": "text/html"})
        assert resp.status_code == 400
        assert not resp.is_json

    def test_404_returns_json_when_xhr(self, mini_app):
        client = mini_app.test_client()
        resp = client.post("/does-not-exist", headers={"X-CSRFToken": "x"})
        assert resp.status_code == 404
        assert resp.is_json
        assert resp.get_json()["code"] == "not_found"

    def test_404_returns_html_when_browser(self, mini_app):
        client = mini_app.test_client()
        resp = client.get("/does-not-exist", headers={"Accept": "text/html"})
        assert resp.status_code == 404
        assert not resp.is_json

    def test_500_returns_json_when_xhr(self, mini_app):
        client = mini_app.test_client()
        mini_app.config["PROPAGATE_EXCEPTIONS"] = False
        resp = client.post("/raise-500", headers={"X-CSRFToken": "x"})
        assert resp.status_code == 500
        assert resp.is_json
        assert resp.get_json()["code"] == "server_error"

    def test_json_content_type_triggers_json_response(self, mini_app):
        client = mini_app.test_client()
        resp = client.post(
            "/does-not-exist",
            json={"x": 1},  # sends Content-Type: application/json
        )
        assert resp.status_code == 404
        assert resp.is_json
