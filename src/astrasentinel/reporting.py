"""Structured, provenance-aware reports for the educational digital twin.

Reports deliberately make no inference about spacecraft operational health.
All parts are serializable plain Python types suitable for JSON or archival CSV.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def build_mission_report(
    orbit: dict[str, Any],
    weather: dict[str, Any],
    telemetry: dict[str, Any],
    rocket: dict[str, Any],
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    """Combine already-evaluated engines into a snapshot with explicit limitations."""
    instant = generated_at or datetime.now(timezone.utc)
    instant = instant.astimezone(timezone.utc)
    points = orbit.get("points", [])
    records = telemetry.get("records", [])
    if not points or not records or not rocket.get("points"):
        raise ValueError("Mission report requires nonempty orbit, telemetry and rocket data")
    mid = points[len(points) // 2]
    metrics = telemetry["model_metrics"]
    return {
        "schema_version": "1.0",
        "project": "AstraSentinel AI",
        "generated_at_utc": instant.isoformat(),
        "mode": "educational_research_demonstration",
        "satellite": {
            "name": orbit["name"],
            "catalog_id": orbit["catalog_id"],
            "orbital_elements_source": orbit["source"],
            "orbital_elements_url": orbit["source_url"],
            "orbital_elements_epoch_utc": orbit["epoch"],
            "orbital_elements_age_hours": orbit["elements_age_hours"],
            "orbit_status": orbit["status"],
            "coordinate_frame": orbit["frame"],
            "inclination_deg": orbit["inclination_deg"],
            "period_minutes": orbit["period_minutes"],
            "sample_count": len(points),
            "sample_midpoint_utc": mid["time"],
            "sample_midpoint_altitude_km": mid["altitude_km"],
        },
        "space_weather": {
            "source": weather["source"],
            "status": weather["status"],
            "observation_age_hours": weather["age_hours"],
            "planetary_kp": weather["latest_kp"],
            "geomagnetic_level": weather["level"],
            "observation_count": len(weather["points"]),
            "source_url": weather["source_url"],
        },
        "telemetry_ai": {
            "dataset_source": telemetry["source"],
            "live_spacecraft_telemetry": False,
            "model": metrics["model"],
            "training_samples": metrics["training_samples"],
            "sample_count": len(records),
            "flagged_samples": sum(bool(row["anomaly"]) for row in records),
            "synthetic_evaluation": {
                "precision": metrics["precision"],
                "recall": metrics["recall"],
                "false_alarm_rate": metrics["false_alarm_rate"],
                "confusion_matrix": metrics["confusion_matrix"],
                "label_source": metrics["label_source"],
            },
        },
        "rocket_simulation": {
            "scenario": rocket["configuration"],
            "metrics": rocket["metrics"],
            "integration_samples": len(rocket["points"]),
            "assumptions": rocket["assumptions"],
        },
        "limitations": [
            "Orbital data are public element estimates, not spacecraft telemetry.",
            "Earth-fixed coordinates are approximate, not flight-grade navigation.",
            "All spacecraft health training and validation data are synthetic.",
            "Anomaly scores and synthetic metrics are not failure probabilities.",
            "Rocket dynamics and atmospheric density are simplified educational models.",
            "Demo or stale source data are always labeled and must not be read as live.",
        ],
        "documentation": {
            "repo": "https://github.com/harshakavali81-collab/AstraSentinel-AI",
            "api": "/docs",
            "science": "docs/PHYSICS.md",
            "model_card": "docs/MODEL_CARD.md",
        },
    }
