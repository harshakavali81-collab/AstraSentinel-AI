"""Serve the built React dashboard and science API from a single FastAPI process.

This module deliberately does not alter backend.main, which remains the
separate-service API used by development and docker-compose.yml.
"""
from __future__ import annotations

import os
from pathlib import Path

from fastapi.staticfiles import StaticFiles

from backend.main import app

WEB_DIST = Path(os.getenv("ASTRA_WEB_DIST", "/app/web_dist")).resolve()
if not (WEB_DIST / "index.html").is_file():
    raise RuntimeError(
        "Frontend build missing. Run npm run build in frontend/ and set "
        "ASTRA_WEB_DIST to the absolute dist directory, or use Dockerfile.standalone."
    )

# Mount LAST: /api/*, /docs and /openapi.json must retain their FastAPI routes.
app.mount("/", StaticFiles(directory=WEB_DIST, html=True), name="mission-dashboard")
