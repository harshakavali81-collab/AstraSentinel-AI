import os
import pytest

@pytest.fixture(autouse=True)
def offline_mode(monkeypatch):
    # The full test suite must never contact external satellite/weather services.
    monkeypatch.setenv("ASTRA_OFFLINE", "1")
