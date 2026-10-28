"""Validate repository-only contracts for deployable single-container architecture."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_standalone_build_and_source_are_complete():
    dockerfile = (ROOT / "Dockerfile.standalone").read_text()
    source = (ROOT / "backend/standalone.py").read_text()
    assert "npm run build" in dockerfile
    assert "COPY --from=frontend-builder" in dockerfile
    assert "backend.standalone:app" in dockerfile
    assert "ASTRA_OFFLINE=1" in dockerfile
    assert 'app.mount("/", StaticFiles(' in source
    assert 'WEB_DIST / "index.html"' in source
    assert "main.app" not in source.lower()


def test_standalone_compose_binds_loopback_only():
    spec = (ROOT / "docker-compose.standalone.yml").read_text()
    assert "Dockerfile.standalone" in spec
    assert "127.0.0.1:8080:8000" in spec
    assert "ASTRA_OFFLINE" in spec


def test_host_manifests_do_not_embed_secrets_or_api_tokens():
    render = (ROOT / "render.yaml").read_text()
    railway = (ROOT / "railway.json").read_text()
    assert "Dockerfile.standalone" in render
    assert "Dockerfile.standalone" in railway
    assert "healthCheckPath" in render
    assert "healthcheckPath" in railway
    assert "secret" not in render.lower()
