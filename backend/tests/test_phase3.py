"""Phase 3 Flask REST API tests."""

from __future__ import annotations

import backend.app as app_module
import pytest


@pytest.fixture()
def client():
    """Provide an isolated Flask test client."""
    app_module.app.config.update(TESTING=True, PROPAGATE_EXCEPTIONS=False)
    with app_module.app.test_client() as test_client:
        yield test_client


def test_index_returns_api_metadata(client) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.is_json is True
    assert response.get_json() == {
        "name": "PhishScope API",
        "version": "0.3",
        "phase": "3",
        "author": "Sian Julian",
        "status": "running",
    }


def test_health_returns_healthy_status(client) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}


def test_analyze_valid_url_returns_scoring_response(client) -> None:
    response = client.post("/analyze", json={"url": "https://google.com"})
    payload = response.get_json()
    assert response.status_code == 200
    assert payload["score"] == 0
    assert payload["verdict"] == "SAFE"
    assert payload["features"]["url"] == "https://google.com"


def test_analyze_g00gle_xyz_returns_phase_two_result(client) -> None:
    response = client.post("/analyze", json={"url": "https://g00gle.xyz"})
    payload = response.get_json()
    assert response.status_code == 200
    assert payload["score"] == 30
    assert payload["verdict"] == "SAFE"
    assert payload["confidence"] == "LOW"
    assert payload["triggered_rules"] == 2
    assert payload["reasons"] == ["Suspicious TLD (.xyz).", "ASCII lookalike detected."]


def test_analyze_dangerous_url(client) -> None:
    response = client.post(
        "/analyze",
        json={"url": "https://secure-hdfc-login-verify.xyz"},
    )
    payload = response.get_json()
    assert response.status_code == 200
    assert payload["score"] == 65
    assert payload["verdict"] == "DANGEROUS"
    assert payload["confidence"] == "HIGH"
    assert payload["triggered_rules"] == 4


def test_analyze_large_url(client) -> None:
    url = "https://secure-login-verification-hdfc-account-update.xyz/" + "a" * 100
    response = client.post("/analyze", json={"url": url})
    payload = response.get_json()
    assert response.status_code == 200
    assert payload["features"]["url_length"] > 75
    assert "URL exceeds 75 characters." in payload["reasons"]


def test_analyze_missing_url_returns_bad_request(client) -> None:
    response = client.post("/analyze", json={})
    assert response.status_code == 400
    assert response.get_json() == {"error": "URL is required."}


def test_analyze_invalid_key_returns_bad_request(client) -> None:
    response = client.post("/analyze", json={"abc": "123"})
    assert response.status_code == 400
    assert response.get_json() == {"error": "URL is required."}


@pytest.mark.parametrize("url", ["", "   ", None, 123])
def test_analyze_missing_or_non_string_url_returns_bad_request(client, url) -> None:
    response = client.post("/analyze", json={"url": url})
    assert response.status_code == 400
    assert response.get_json() == {"error": "URL is required."}


@pytest.mark.parametrize("url", ["....", "abc", "////", "http://"])
def test_analyze_invalid_url_returns_bad_request(client, url: str) -> None:
    response = client.post("/analyze", json={"url": url})
    assert response.status_code == 400
    assert response.get_json() == {"error": "Invalid URL."}


def test_analyze_rejects_non_json_content_type(client) -> None:
    response = client.post("/analyze", data="url=https://google.com", content_type="text/plain")
    assert response.status_code == 415
    assert response.get_json() == {"error": "Unsupported Media Type"}


def test_analyze_rejects_missing_content_type(client) -> None:
    response = client.post("/analyze", data='{"url":"https://google.com"}')
    assert response.status_code == 415
    assert response.get_json() == {"error": "Unsupported Media Type"}


def test_analyze_rejects_invalid_json_body(client) -> None:
    response = client.post("/analyze", data="{", content_type="application/json")
    assert response.status_code == 400
    assert response.get_json() == {"error": "URL is required."}


def test_analyze_benchmark_is_opt_in(client) -> None:
    response = client.post("/analyze", json={"url": "https://google.com", "benchmark": True})
    assert response.status_code == 200
    assert response.get_json()["execution_time_ms"] >= 0


def test_analyze_does_not_include_benchmark_by_default(client) -> None:
    response = client.post("/analyze", json={"url": "https://google.com"})
    assert response.status_code == 200
    assert "execution_time_ms" not in response.get_json()


def test_analyze_only_treats_boolean_true_as_benchmark_request(client) -> None:
    response = client.post("/analyze", json={"url": "https://google.com", "benchmark": "true"})
    assert response.status_code == 200
    assert "execution_time_ms" not in response.get_json()


def test_unknown_route_returns_json_not_found(client) -> None:
    response = client.get("/unknown")
    assert response.status_code == 404
    assert response.is_json is True
    assert response.get_json() == {"error": "Not Found"}


@pytest.mark.parametrize(
    ("method", "path"),
    [("get", "/analyze"), ("post", "/health"), ("delete", "/")],
)
def test_unsupported_methods_return_json(client, method: str, path: str) -> None:
    response = getattr(client, method)(path)
    assert response.status_code == 405
    assert response.is_json is True
    assert response.get_json() == {"error": "Method Not Allowed"}


def test_cors_header_is_available_to_browser_clients(client) -> None:
    response = client.get("/health", headers={"Origin": "https://example.com"})
    assert response.status_code == 200
    assert response.headers["Access-Control-Allow-Origin"] == "https://example.com"


def test_internal_errors_return_json(client, monkeypatch) -> None:
    def raise_error(_: str) -> dict:
        raise RuntimeError("simulated extractor failure")

    monkeypatch.setattr(app_module, "extract_features", raise_error)
    response = client.post("/analyze", json={"url": "https://google.com"})
    assert response.status_code == 500
    assert response.get_json() == {"error": "Internal Server Error"}
