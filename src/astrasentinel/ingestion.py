"""CelesTrak and NOAA adapters with transparent, labeled offline fallback.

CelesTrak GP data is cached for two hours to comply with its update guidance.
Never interpret the bundled 2024 TLE or synthetic weather as current observations.
"""
from __future__ import annotations

import os
import time
from datetime import datetime, timedelta, timezone
from typing import Any

import httpx

TLE_URL = "https://celestrak.org/NORAD/elements/gp.php?CATNR=25544&FORMAT=TLE"
KP_URL = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"
DEMO_TLE = (
    "ISS (ZARYA)",
    "1 25544U 98067A   24067.51782528  .00016688  00000+0  30549-3 0  9999",
    "2 25544  51.6402  18.3614 0005489 293.6311 186.4045 15.50038627442751",
)
_cache: dict[str, tuple[float, Any]] = {}


def cached_json_or_text(url: str, ttl: int, parse_json: bool = False) -> Any:
    """Bounded request with cache. Failures are also cached briefly to avoid hammering sources."""
    now = time.monotonic()
    if url in _cache and _cache[url][0] > now:
        value = _cache[url][1]
        if isinstance(value, Exception):
            raise value
        return value
    try:
        response = httpx.get(url, timeout=10.0, follow_redirects=True,
                             headers={"User-Agent": "AstraSentinelAI-Educational/1.0"})
        response.raise_for_status()
        value = response.json() if parse_json else response.text
        _cache[url] = (now + ttl, value)
        return value
    except (httpx.HTTPError, ValueError) as exc:
        _cache[url] = (now + 120, exc)
        raise


def valid_tle_checksum(line: str) -> bool:
    """Classic TLE modulo-10 checksum: digits plus minus signs, excluding the last digit."""
    return (len(line) == 69 and line[-1].isdigit()
            and (sum(int(c) for c in line[:-1] if c.isdigit())
                 + line[:-1].count("-")) % 10 == int(line[-1]))


def parse_tle(text: str) -> tuple[str, str, str]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for idx in range(len(lines) - 1):
        if lines[idx].startswith("1 ") and lines[idx + 1].startswith("2 "):
            line1, line2 = lines[idx], lines[idx + 1]
            if (len(line1) < 69 or len(line2) < 69 or line1[2:7] != line2[2:7]
                    or not valid_tle_checksum(line1) or not valid_tle_checksum(line2)):
                raise ValueError("Malformed or mismatched TLE")
            name = lines[idx - 1] if idx > 0 else "NORAD 25544"
            return name, line1, line2
    raise ValueError("No TLE records found")


def satellite_elements() -> dict[str, Any]:
    if os.getenv("ASTRA_OFFLINE", "0") == "1":
        name, line1, line2 = DEMO_TLE
        return {"name": name, "line1": line1, "line2": line2,
                "source": "bundled_historical_demo", "source_url": TLE_URL}
    try:
        name, line1, line2 = parse_tle(cached_json_or_text(TLE_URL, 7200))
        return {"name": name, "line1": line1, "line2": line2,
                "source": "CelesTrak", "source_url": TLE_URL}
    except (httpx.HTTPError, ValueError):
        name, line1, line2 = DEMO_TLE
        return {"name": name, "line1": line1, "line2": line2,
                "source": "bundled_historical_demo", "source_url": TLE_URL}


def normalize_kp(payload: Any) -> list[dict[str, Any]]:
    """Accept both NOAA's post-March-2026 object records and old array records."""
    if not isinstance(payload, list) or not payload:
        raise ValueError("Invalid NOAA payload")
    rows = payload
    if isinstance(rows[0], list):
        headers = rows[0]
        rows = [dict(zip(headers, record)) for record in rows[1:]]
    result = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        try:
            date = str(row.get("time_tag", ""))
            stamp = datetime.fromisoformat(date.replace("Z", "+00:00"))
            stamp = (stamp.replace(tzinfo=timezone.utc) if stamp.tzinfo is None
                     else stamp.astimezone(timezone.utc))
            kp = float(row.get("Kp", row.get("kp_index", row.get("kp"))))
            if not (0 <= kp <= 9):
                continue
            result.append({"time": stamp.isoformat(), "kp": round(kp, 2)})
        except (ValueError, TypeError, OverflowError):
            continue
    if not result:
        raise ValueError("No usable NOAA Kp observations")
    result.sort(key=lambda sample: sample['time'])
    return result[-56:]


def space_weather() -> dict[str, Any]:
    if os.getenv("ASTRA_OFFLINE", "0") != "1":
        try:
            points = normalize_kp(cached_json_or_text(KP_URL, 900, True))
            observed = datetime.fromisoformat(points[-1]["time"])
            observed = observed.replace(tzinfo=observed.tzinfo or timezone.utc)
            age_h = (datetime.now(timezone.utc) - observed).total_seconds() / 3600
            latest = points[-1]["kp"]
            return {
                "source": "NOAA SWPC", "source_url": KP_URL,
                "status": "live" if -1 <= age_h <= 12 else "stale",
                "age_hours": round(age_h, 1), "latest_kp": latest,
                "level": kp_level(latest), "points": points,
            }
        except (httpx.HTTPError, ValueError):
            pass
    origin = datetime(2024, 1, 1, tzinfo=timezone.utc)
    points = [{"time": (origin + timedelta(hours=3 * i)).isoformat(),
               "kp": [1.0, 1.3, 2.0, 2.7, 3.3, 2.3, 1.7, 1.0][i % 8]}
              for i in range(48)]
    return {
        "source": "synthetic_historical_demo", "source_url": KP_URL,
        "status": "demo", "age_hours": None,
        "latest_kp": points[-1]["kp"], "level": kp_level(points[-1]["kp"]),
        "points": points,
    }


def kp_level(value: float) -> str:
    # NOAA geomagnetic storm threshold begins at Kp 5.
    if value >= 7:
        return "severe storm conditions"
    if value >= 5:
        return "geomagnetic storm conditions"
    if value >= 4:
        return "active"
    return "quiet to unsettled"
