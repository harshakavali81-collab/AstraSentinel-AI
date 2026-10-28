"""A focused single-account demo gate; not a complete production auth system."""
import base64

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.basic_auth import configure_demo_auth, valid_basic_auth


def header(username: str, password: str) -> str:
    raw = f"{username}:{password}".encode()
    return "Basic " + base64.b64encode(raw).decode()


def test_valid_basic_auth_rejects_bad_and_malformed_credentials():
    assert valid_basic_auth(header("test", "strong:password"), "test", "strong:password")
    for bad in (None, "", "Bearer token", "Basic !", header("test", "incorrect"),
                header("another", "strong:password")):
        assert not valid_basic_auth(bad, "test", "strong:password")


def test_authentication_gate_allows_health_and_protects_website():
    app = FastAPI()

    @app.get("/api/health")
    def health():
        return {"ok": True}

    @app.get("/")
    def home():
        return {"home": "protected"}

    assert configure_demo_auth(app, {
        "ASTRA_DEMO_AUTH": "1",
        "ASTRA_DEMO_USER": "astrareviewer",
        "ASTRA_DEMO_PASSWORD": "test-only-credentials",
    })
    client = TestClient(app)
    assert client.get("/api/health").status_code == 200
    response = client.get("/")
    assert response.status_code == 401
    assert "Basic realm" in response.headers["www-authenticate"]
    assert client.get("/", headers={"Authorization": header("astrareviewer", "wrong")}).status_code == 401
    assert client.get("/", headers={"Authorization": header("astrareviewer", "test-only-credentials")}).status_code == 200


def test_missing_credentials_fail_closed_when_enabled():
    with pytest.raises(RuntimeError):
        configure_demo_auth(FastAPI(), {"ASTRA_DEMO_AUTH": "1"})
    with pytest.raises(RuntimeError):
        configure_demo_auth(FastAPI(), {
            "ASTRA_DEMO_AUTH": "1", "ASTRA_DEMO_USER": "test", "ASTRA_DEMO_PASSWORD": "",
        })


def test_local_development_does_not_require_credentials():
    assert configure_demo_auth(FastAPI(), {"ASTRA_DEMO_AUTH": "0"}) is False
