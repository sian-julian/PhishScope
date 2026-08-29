import pytest
from backend.app import app
from hybrid.engine import analyze_url
from backend.utils.trusted_loader import is_trusted_domain

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_trusted_domain_is_trusted():
    assert is_trusted_domain("https://google.com")
    assert is_trusted_domain("https://youtube.com")
    assert is_trusted_domain("https://github.com")

def test_subdomains_are_trusted():
    assert is_trusted_domain("https://docs.google.com")
    assert is_trusted_domain("https://a.b.c.google.com")

def test_lookalikes_are_not_trusted():
    assert not is_trusted_domain("https://google.com.fake-site.xyz")
    assert not is_trusted_domain("https://google-login.xyz")
    assert not is_trusted_domain("https://fakejw.org")

def test_analyze_trusted_domain():
    result = analyze_url("https://google.com/")
    assert result["hybrid"]["verdict"] == "SAFE"
    assert result["hybrid"]["trusted_domain"] is True
    assert result["hybrid"]["decision_source"] == "trusted_domain"

def test_analyze_normal_domain():
    # Example non-trusted but safe domain
    result = analyze_url("https://example.com/")
    assert "hybrid" in result
    assert result["hybrid"]["trusted_domain"] is False
    assert result["hybrid"]["decision_source"] == "hybrid"

def test_api_trusted_domain(client):
    response = client.post("/analyze", json={"url": "https://google.com/"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["hybrid"]["verdict"] == "SAFE"
    assert data["hybrid"]["trusted_domain"] is True
    assert data["hybrid"]["decision_source"] == "trusted_domain"

def test_api_normal_domain(client):
    response = client.post("/analyze", json={"url": "https://example.com/"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["hybrid"]["trusted_domain"] is False
    assert data["hybrid"]["decision_source"] == "hybrid"
