"""SGP4 orbit propagation, TEME positions and approximate Earth-fixed display coordinates.

The rotation deliberately ignores polar motion and precision Earth-orientation corrections.
Display coordinates are educational and unsuitable for maneuver or collision decisions.
"""
from __future__ import annotations

import math
from datetime import datetime, timedelta, timezone
from sgp4.api import Satrec, jday
from .ingestion import satellite_elements

EARTH_RADIUS_KM = 6378.137


def gmst_radians(jd: float) -> float:
    t = (jd - 2451545.0) / 36525.0
    degrees = (280.46061837 + 360.98564736629 * (jd - 2451545.0)
               + 0.000387933 * t * t - t * t * t / 38710000.0)
    return math.radians(degrees % 360)


def teme_to_ecef(position: tuple[float, float, float], jd: float) -> list[float]:
    theta = gmst_radians(jd)
    x, y, z = position
    return [math.cos(theta) * x + math.sin(theta) * y,
            -math.sin(theta) * x + math.cos(theta) * y, z]


def propagate(elements: dict, center: datetime | None = None,
              samples: int = 121, span_minutes: int = 96) -> dict:
    if not 2 <= samples <= 301 or not 1 <= span_minutes <= 180:
        raise ValueError("Out-of-range orbit sampling")
    satellite = Satrec.twoline2rv(elements["line1"], elements["line2"])
    epoch_jd = satellite.jdsatepoch + satellite.jdsatepochF
    epoch = datetime.fromtimestamp((epoch_jd - 2440587.5) * 86400,
                                   tz=timezone.utc)
    if center is None:
        now = datetime.now(timezone.utc)
        # Avoid extrapolating a years-old TLE to present time.
        center = now if elements["source"] == "CelesTrak" and abs(
            (now - epoch).total_seconds()) < 72 * 3600 else epoch
    center = center.astimezone(timezone.utc)
    points = []
    for i in range(samples):
        offset = ((i / (samples - 1)) - 0.5) * span_minutes * 60
        date = center + timedelta(seconds=offset)
        jd, fraction = jday(date.year, date.month, date.day, date.hour,
                            date.minute, date.second + date.microsecond / 1e6)
        error, r, _velocity = satellite.sgp4(jd, fraction)
        if error != 0:
            raise ValueError("SGP4 error code " + str(error))
        ecef = teme_to_ecef(r, jd + fraction)
        radius = math.sqrt(sum(x * x for x in r))
        points.append({
            "time": date.isoformat(),
            "ecef_km": [round(v, 3) for v in ecef],
            "altitude_km": round(radius - EARTH_RADIUS_KM, 2),
            "latitude_deg": round(math.degrees(math.asin(ecef[2] / radius)), 3),
            "longitude_deg": round(math.degrees(math.atan2(ecef[1], ecef[0])), 3),
        })
    mean_motion = satellite.no_kozai * 1440 / (2 * math.pi)  # rev/day
    age_hours = (datetime.now(timezone.utc) - epoch).total_seconds() / 3600
    return {
        "name": elements["name"], "catalog_id": 25544,
        "source": elements["source"], "source_url": elements["source_url"],
        "epoch": epoch.isoformat(), "elements_age_hours": round(age_hours, 1),
        "status": ("demo" if elements["source"] != "CelesTrak"
                   else "current" if abs(age_hours) <= 72 else "stale"),
        "frame": "ECEF approximation from TEME (simplified GMST rotation)",
        "inclination_deg": round(math.degrees(satellite.inclo), 2),
        "period_minutes": round(1440 / mean_motion, 2),
        "earth_radius_km": EARTH_RADIUS_KM,
        "points": points,
    }


def current_orbit() -> dict:
    return propagate(satellite_elements())
