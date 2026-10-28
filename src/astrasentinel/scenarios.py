"""Deterministic, bounded rocket parameter experiments.

This package deliberately compares *educational 1D rocket simulations* and never
returns operational launch guidance, mission success odds, or safety margins.
"""
from __future__ import annotations

from dataclasses import asdict, replace
import math

from .rocket import RocketConfig, simulate

PARAMETERS = {
    "thrust_n": ("N", 0.0, 20_000_000.0),
    "propellant_kg": ("kg", 0.0, 1_000_000.0),
    "density_multiplier": ("× sea-level model", 0.2, 5.0),
    "drag_coefficient": ("dimensionless", 0.0, 3.0),
    "area_m2": ("m²", 0.01, 1000.0),
}


def compare_scenarios(
    parameter: str,
    values: list[float],
    baseline: RocketConfig | None = None,
) -> dict:
    """Return baseline and 2-7 variation summaries with downsampled plot data."""
    if parameter not in PARAMETERS:
        raise ValueError("Unsupported comparison parameter")
    if not 2 <= len(values) <= 7:
        raise ValueError("Provide between two and seven scenario values")
    if not all(isinstance(v, (float, int)) and math.isfinite(v) for v in values):
        raise ValueError("Scenario values must be finite numbers")
    lo, hi = PARAMETERS[parameter][1:]
    if any(not lo <= v <= hi for v in values):
        raise ValueError("Scenario values outside supported physics bounds")
    if len(set(values)) != len(values):
        raise ValueError("Scenario values must be unique")
    baseline = baseline or RocketConfig()
    baseline.validate()
    base = simulate(baseline)
    base_apogee = base["metrics"]["apogee_km"]
    scenarios = []
    for i, value in enumerate(values):
        config = replace(baseline, **{parameter: value})
        config.validate()
        result = simulate(config)
        points = result["points"]
        stride = max(1, math.ceil(len(points) / 180))
        curve = [{"time_s": p["time_s"], "altitude_km": p["altitude_km"],
                  "velocity_m_s": p["velocity_m_s"]}
                 for p in points[::stride]]
        if curve[-1]["time_s"] != points[-1]["time_s"]:
            curve.append({k: points[-1][k] for k in
                          ("time_s", "altitude_km", "velocity_m_s")})
        scenarios.append({
            "id": "scenario_" + str(i + 1),
            "value": value,
            "configuration": asdict(config),
            "metrics": result["metrics"],
            "apogee_delta_vs_baseline_pct":
                round(100 * (result["metrics"]["apogee_km"] - base_apogee)
                      / base_apogee, 2) if base_apogee else None,
            "curve": curve,
        })
    return {
        "mode": "deterministic_educational_parameter_study",
        "parameter": parameter,
        "parameter_unit": PARAMETERS[parameter][0],
        "baseline": {"configuration": asdict(baseline), "metrics": base["metrics"]},
        "scenarios": scenarios,
        "assumptions": base["assumptions"],
        "disclaimer": (
            "Only a simplified deterministic 1D point-mass model is compared. "
            "No uncertainty analysis, real vehicle validation, trajectory guidance, "
            "launch safety assessment, or spacecraft flight prediction is provided."
        ),
    }
