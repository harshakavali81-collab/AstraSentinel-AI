"""Optional HTTP Basic access gate for a hosted educational demo.

Use only behind an HTTPS terminator. This is a simple single-account demo
access control, not OAuth, SSO, RBAC or a substitute for edge rate limiting.
"""
from __future__ import annotations

import base64
import binascii
import hmac
import os
from collections.abc import Mapping

from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse


def valid_basic_auth(header: str | None, username: str, password: str) -> bool:
    """Check two UTF-8 credentials without leaking which field was wrong."""
    if not isinstance(header, str) or len(header) > 4096:
        return False
    scheme, sep, token = header.partition(" ")
    if not sep or scheme.lower() != "basic" or not token:
        return False
    try:
        decoded = base64.b64decode(token, validate=True).decode("utf-8")
        provided_user, provided_password = decoded.split(":", 1)
    except (ValueError, UnicodeError, binascii.Error):
        return False
    user_ok = hmac.compare_digest(provided_user.encode(), username.encode())
    password_ok = hmac.compare_digest(provided_password.encode(), password.encode())
    return user_ok and password_ok


def configure_demo_auth(app: FastAPI, settings: Mapping[str, str] | None = None) -> bool:
    """Register middleware only for standalone deployments that opt in.

    The public /api/health endpoint is intentionally exempt to allow platform
    readiness checks without exposing the application data or documentation.
    """
    env = os.environ if settings is None else settings
    enabled = env.get("ASTRA_DEMO_AUTH", "0") == "1"
    if not enabled:
        return False
    username = env.get("ASTRA_DEMO_USER", "")
    password = env.get("ASTRA_DEMO_PASSWORD", "")
    if not username or not password or ":" in username:
        raise RuntimeError("Demo Basic Auth requires a username and password in host secrets")

    @app.middleware("http")
    async def demo_basic_auth(request: Request, call_next):
        if request.url.path == "/api/health":
            return await call_next(request)
        if not valid_basic_auth(request.headers.get("authorization"), username, password):
            return PlainTextResponse(
                "AstraSentinel demo credentials required",
                status_code=401,
                headers={
                    "WWW-Authenticate": 'Basic realm="AstraSentinel AI Demo", charset="UTF-8"',
                    "Cache-Control": "no-store",
                },
            )
        return await call_next(request)

    return True
