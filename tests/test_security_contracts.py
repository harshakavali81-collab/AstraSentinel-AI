"""Static regression checks for basic nginx and Compose safety measures."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_reverse_proxy_defense_in_depth():
    config = (ROOT / "frontend" / "nginx.conf").read_text()
    assert "limit_req_zone" in config
    assert "limit_req zone=astrasentinel_api" in config
    assert "client_max_body_size 32k" in config
    assert 'add_header X-Content-Type-Options "nosniff" always;' in config
    assert 'add_header X-Frame-Options "DENY" always;' in config
    assert "Content-Security-Policy" in config
    assert "proxy_pass http://backend:8000" in config


def test_restricted_compose_hides_backend_and_uses_loopback():
    config = (ROOT / "docker-compose.private.yml").read_text()
    assert "127.0.0.1:3000:80" in config
    assert 'expose: ["8000"]' in config
    assert '"8000:8000"' not in config
    assert "ASTRA_OFFLINE" in config
